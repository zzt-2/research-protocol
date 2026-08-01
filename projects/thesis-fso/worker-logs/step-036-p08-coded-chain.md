# step-036 — P08 G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL coded-chain 扩展包

> 2026-08-01 | campaign P08 | family G（coded-LLR-calibration，新族）| executor: 主线程协调 + 子 agent
> 上游：D047（scope-change 授权 coded-chain 场景扩展）+ 用户 P08 执行指令
> 验收：独立 verifier（待）

## 任务

用户 P08 执行指令：scope-change 授权建立 source-auditable 最小真实 coded baseline，运行
G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL。端到端完成 Phase 0A→0B→算法正确性门→Phase A→
(条件 B)→C→独立 verifier→单次 commit。不 push。

## Phase 0A：标准码来源门（CLOSED — 选 5G NR LDPC，DVB-S2 不可闭合）

子 agent 审计 3 候选（sionna 2.0.1 / commpy 1.1.0 / ldpc 2.4.1）：
- **DVB-S2 不可闭合**：sionna v2.0 已删除 DVB-S2（grep `dvb` 零命中），`ldpc` 是 QEC 工具包（非经典 LDPC），`commpy` 只带手写 rate-½ demo protograph（非标准码）。
- **选 5G NR LDPC（sionna 2.0.1，Apache-2.0）**：3GPP TS 38.212 BG1/BG2 base graph 作可审计 CSV（`sionna/phy/fec/ldpc/codes/5G_bg1.csv`、`5G_bg2.csv`）；systematic encoder（`_encode_fast` mod-2）；normalized-min-sum decoder（num_iter/llr_max/cn_update callable 全可控）。
- **主线程独立验证**（torch 2.6.0+cu124 env）：`LDPC5GEncoder(k=1024,n=1536)` → BG2/Z=104/k_ldpc=1040/n_ldpc=5408；|Hc|=0（valid codeword）；轻度噪声 decode BER=0.0。**注意**：sionna 2.0.1 装时会拉 torch≥2.13，需手动重装 `torch==2.6.0+cu124` 保 CUDA env（已恢复，CUDA True）。

### 冻结 coded_contract

| 项 | 值 |
|---|---|
| standard/version | 3GPP TS 38.212 5G NR LDPC（BG2），Rel-15 |
| n (coded on-air) | 1536 |
| k (info) | 1024 |
| rate | 2/3 |
| encoder | LDPC5GEncoder systematic（3GPP Gauss-elim + mod-2 gather） |
| decoder | normalized min-sum, flooding, α=0.75 |
| iterations | 20（固定，无 early termination） |
| normalization α | 0.75 |
| LLR clipping | llr_max=20.0 |
| sign convention | decoder input = logit = log(p(b=1)/p(b=0))；BPSK bit b→x=(1−2b)：logit=−2y/σ² |
| interleaver | 3GPP TS 38.212 §5.4.2.2 sub-block + triangle bit-interleaver（num_bits_per_symbol=4 for 16QAM） |
| padding/shortening | 3GPP filler bits (k→k_ldpc) + 2Z punctured info cols |
| net rate | 2/3 |
| modulation | 16QAM Gray-coded BICM |

**声明约束**（用户 Phase 0A 指令）：称"5G NR LDPC BICM component"——通用 FSO BICM 标准 baseline，**不声称卫星专用 DVB-S2**；所有方法共用同一码；code choice 作 baseline 限定不包装为创新。

## Phase 0B / 算法正确性门 / Phase A / B / C / verifier

（执行中，详见下方追加段）

## 物理信道 + 接收机选择（用户 binding，2026-08-01）

源码核查发现：现有 P01-P07 冻结接收链是 (8,8)-16APSK 单偏振（`generate_shared_realization_apsk`，
M0=8 八次方载波恢复），**不支持 16QAM**。真 16QAM 只在双偏振发生器 + `_modulation.qam16_mod`，
无冻结接收链。

**用户 binding（选项 1）**：coded-chain 建在双偏振 SOP 信道（`generate_shared_realization_dp
(modulation='qam16')`，GG 幅度+SOP 旋转+AWGN，与 thesis dual-pol OSL 锚点一致），新建最小冻结
16QAM 接收链：blind/pilot MMSE 均衡 + amp_limit + decide（复用 modulation-agnostic 函数）+
qam16 max-log LLR + LDPC 译码。GG/SOP 残差是 P08 问题的 C。

### 冻结 M-C-A（最终，双偏振 16QAM）

- **M**（冻结方法/baseline）：双偏振 16QAM receiver 用标准 max-log LLR 配单一 receiver-visible
  全局噪声尺度 σ²=1/(2γ_bar)（与 `decide`/`estimate_h_blind_perblock` 假设一致）。
- **C**（条件）：双偏振 GG 时变幅度 + SOP 旋转 + 接收机均衡残差使等化符号误差呈异方差/非高斯
  （深衰落块噪声大、SOP 旋转未完全补偿时残差有方向性）；有限码长 soft LDPC normalized-min-sum
  对 LLR 置信度过/欠敏感。
- **A**（断言）：单一 AWGN 全局尺度可能使 LLR 在异方差块过置信（深衰落）或欠置信（高 SNR 块），
  增加 FER、译码迭代数或所需 SNR；receiver-visible 局部尺度估计可能改善。

### runtime 信息边界（冻结）

合法：equalized symbol / 已知 pilot / AGC-receiver metadata / calibration prefix / 严格过去
decision residual / decoder convergence-iteration（只在其自然时序内）。
禁止：TX bits / true h-theta / 全 scored window 事后 residual / oracle affine / test-label
fitting / future frame / CRC 翻标签路线。TX truth 仅用于 BER/FER/NLL/GMI scoring。

## 算法正确性门（ALL 12 PASS）

脚本 `p08_correctness_gate.py`。12 项检查全 PASS：
1. matrix/source hash（bg2 csv sha256 可审计）
2. H·c=0 on 20 random info frames（max|Hc|=0）
3. noise-free encode→demap→decode BER=0
4. LLR sign/bit order/Gray 全 16 labels
5. all-zero codeword 对称
6. AWGN FER 单调下降
7. AWGN waterfall 三区（fail 6-8dB / waterfall 9dB / success 10-14dB）
8. syndrome-zero early-stop（sionna fixed-iter 配置）
9. max_iter (20 vs 5) 与 normalization (α=0.75 vs 1.0) 真生效
10. interleave/padding/order 可逆（noiseless mod→demap round-trip）
11. high-confidence LLR hard-decision == 原始 bits
12. decoder 不读 TX truth（AST 静态审计）

artifacts: `results/p08_coded_chain/p08_correctness_gate.json`, `p08_awgn_waterfall.json`

## Phase A 问题门（verdict = PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE）

脚本 `p08_phaseA_gate.py`。冻结（读 test 前）：dev seeds 1000-1009（tune 用 5）/ test seeds 1100-1114（15）
× scenes weak/moderate/strong × f_G {100,1000} × Es/N0 {13,15,17,19} dB × 16 codewords/pol
（FER step 1/16）。MDE=0.15dB，FER target=0.1。

dev best: B1 T=1.1 (dev FER 0.2164 vs B0 0.2172，几乎无差异); B2 {α=0.75,off=0.1,clip=20} (0.2164)。

test pooled FER（4 SNR）:
| method | 13dB | 15dB | 17dB | 19dB |
|---|---|---|---|---|
| B0     | 0.284 | 0.180 | 0.133 | 0.121 |
| B1     | 0.284 | 0.180 | 0.133 | 0.117 |
| B2     | 0.284 | 0.180 | 0.133 | 0.122 |
| oracle | 0.284 | 0.178 | 0.133 | 0.098 |

@ref 19dB paired: B0-conv delta +0.0038 CI=[+0.0000,+0.0104]; conv-oracle delta +0.0191
CI=[+0.0000,+0.0483]（CI_lo=0 边界）。

**per-scene/fG 诚实分解**（关键）：oracle 相对 conv 的增益**几乎全集中在 19dB-moderate**
（+0.062/+0.052）；其余 cell 全 +0.000。13/15/17dB 绝大多数 cell FER=0.200（=3-5/16 cw 失败）——
这是**突发深衰落（burst-fade）regime**：深 GG 衰落抹掉连续码字，**任何 LLR 校准都救不回**
（信号确实丢了）。oracle（per-symbol residual σ²）也无济于事——深衰落里残差 σ² 同样大，
decoder 已无能为力。

**结论（PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE）**：dual-pol GG/SOP 信道下 coded loss 的主导
机制是**不可恢复的突发深衰落**，不是 LLR 置信度失配。单一 AWGN 全局 σ² 与最强传统校准（B1/B2）
表现近乎相同，oracle（完美 per-symbol σ²）只在 19dB-moderate 边界区有 ~6% FER 相对改善，其余
zero headroom。Phase B/C 不运行（gate 顺序：Phase A 问题不存在 → 不进方法工厂）。

artifacts: `results/p08_coded_chain/p08_phaseA_gate.json`, `p08_phaseA_raw_rows.json`

## Phase B / Phase C：不运行

gate 顺序：Phase A 判 PROBLEM_ABSENT → 不进 Phase B 方法工厂，不进 Phase C 公平比较。
唯一允许科学终态选 DIAGNOSTIC_METHOD_SIGNAL（未达）；本轮 verdict 为有效科学负面。

## 治理结论（待 verifier 后定稿）

- P08 counts_as_valid_package=True（有效科学执行，诚实负面回答 coded-LLR 问题为"否"）。
- campaign accepted_valid 7→**8**/10（G 族 coded-LLR-calibration）。
- 不产方法卡/不晋升/不建 pre-formal carrier（verdict 非 METHOD_SIGNAL）。
- P09 只准备不运行：LLR 问题被诚实判 absent → P09 选 coded operating-boundary 或
  receiver-ranking，但须重新过 problem gate。
