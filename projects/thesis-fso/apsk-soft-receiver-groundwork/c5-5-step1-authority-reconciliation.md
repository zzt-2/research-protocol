# C5-5 reliability-prioritized LDPC scheduling/budget — Groundwork Step 1 authority reconciliation

> T078｜2026-08-30｜authority `d7acd9f7b1e1583d47280ef93cbdb89db58e2df9`
> 范围：候选特定 GW Step 1；只读本地文献、read notes、Sionna 2.0.1 源码和项目 codec authority；无实现、仿真、下载或 Step 2。

## 1. Terminal 与一句话裁决

```text
STEP1_C5_5_EVIDENCE_GAP_BOUNDED
```

`Q-C5-5` 可以形成一个诚实、可量化且与 C5-0/C5-1 独立的硕士级问题；receiver-visible IAO 和一个不需自写 BP decoder 的 **budget-only 最小接口路径**也成立。当前不能给 `PASS_READY_FOR_STEP2`，因为唯一直接命中的 2019 residual/informed scheduling 文献只存在于 T041 元数据，仓库没有其全文/read note，无法核对 residual 定义、真实更新粒度、equal-edge-update 公平性与 exact collision。该缺口可由一个有界 Step 2 获取/精读包关闭。

## 2. 已确认事实

### 2.1 当前科学与 codec authority

- C5-0 已按 D057/V032 关闭：同一 frozen cell 上，receiver-visible pilot statistic 对 held-out reliability 的 Spearman `rho=0.98566540`，但 B0/O1 info-BER 为 `0.04929352/0.05333900`，`B0-O1` paired 95% CI 全负；这只否定一维 payload-variance auxiliary scalar，不否定 decoder-internal scheduling/budget（`.sessions/2026-07-09-thesis-writing/decisions.md:2065-2089`；`verifications.md:780-800`）。
- 目标 codec 已由 T076 关闭 correctness：DP-(8,8)-16APSK → 5G LDPC BG2，`k=1024,n=1536,Qm=4,Z=104`，mapper/label、LLR sign、rate recovery、16 filler、clip 顺序和 fresh 20-iteration decode 均通过（`projects/thesis-fso/worker-logs/step-076-c5-0-apsk-ldpc-correctness.md:32-74`）。
- 当前项目 decoder 是 fixed NMS：`alpha=0.75`、offset `0`、20 iterations、hard information bits、`return_state=False`，且没有显式 `cn_schedule`，因此采用 Sionna 默认 flooding（`projects/simulation/explore/coded-decoder-feedback/codec.py:150-164`）。项目 wrapper 每次 fresh decode，拒绝 `message_state/warm_state`，只返回 hard info bits（同文件 `:178-193`；`ch5-apsk-llr-calibration/correctness.py:323-384`）。
- 当前 receipt 的 `bp_iterations=20×codewords` 是配置计数，不是实际收敛轮数或公平 edge-update 计数（`projects/simulation/explore/coded-decoder-feedback/codec.py:319-327`；`projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md` 的 capability matrix）。

### 2.2 本地全文与索引事实

| 对象 | 本地证据 | 可承重事实 | Step 1 角色 |
|---|---|---|---|
| Wu et al. 2010 AN-/AO-MS | `papers/doi/10.1109_lcomm.2010.07.100508/content.md` + read note | 每轮按 check-sum 的 satisfied/unsatisfied state 切换两组 normalization/offset；全文明确 dynamic termination、fixed NMS/OMS comparator 和约 `0.15/0.1 dB` 结果 | `PRIMITIVE_COLLISION` + 正确 fixed NMS/OMS authority |
| He et al. 2021 NR-LDPC post-processing | `papers/doi/10.1109_wcsp52459.2021.9613326/content.md` | BG2、layered first stage、CRC early stop、unsatisfied-check threshold 后才进入第二阶段 | `RELATED / CHEAP_ABSORPTION`；不是纯 schedule/budget 方法 |
| Baldi et al. 2016 hybrid MRB/OSD | `papers/doi/10.1186_s13638-016-0769-z/content.md` | iterative decoder failure 后才调用 MRB；明确平均/最坏复杂度与 latency；`Imax 100→200` 增益 `<0.1 dB`、最坏 latency 翻倍 | `RELATED / CHEAP_ABSORPTION`；不是纯 schedule/budget 方法 |
| Zhao et al. 2023 narrowed SBF | `papers/doi/10.1109_iccc59590.2023.10507492/content.md` | syndrome、channel reliability 与 iteration termination 可执行 | `RELATED`；动作是 bit flipping，超出 C5-5 身份 |
| Residual-decaying informed dynamic scheduling, DOI `10.1109/ACCESS.2019.2899106` | 仅 `ldpc-receiver-authority.md:73` 与 T041 search metadata | 题名/DOI/OA 身份可定位；仓库无 `content.md`、无 read note | **DIRECT FULLTEXT GAP**；不能判 exact collision 或 equal-update 合法性 |
| Chen–Fossorier 2005 reduced-complexity decoding | T044 明记 exact identity miss | exact 全文缺失；错误近邻未冒充 | 非阻塞 provenance debt；Wu 全文 + 目标代码 correctness 已足够冻结 fixed NMS/OMS M |

`papers/index.json` 对上述 residual-scheduling、Wu 和 Chen–Fossorier 的题名/DOI均为 0 命中，因此本报告不把 index 当作“已收录全文”证据；以实际 `content.md`/read note 路径和 T044 identity ledger 为准。T044 的 6 篇 qualified fulltexts 中没有 residual/informed scheduling（`projects/thesis-fso/apsk-soft-receiver-groundwork/step2-coverage-report.md:8-43`）。

## 3. Q-C5-5：M-C-A 与四判据

### 3.1 冻结陈述

**Q-C5-5**：充分调优的 fixed NMS/OMS `M`，在共同 DP-(8,8)-16APSK+BICM/5G-BG2-LDPC 接收机中、面对码字间 receiver-visible reliability 不均且平均/P95 计算预算受限的条件 `C`，因其对所有码字使用静态 flooding/layered 顺序和统一最大迭代预算，不能用当前码字的 channel reliability、unsatisfied-check/syndrome 与 stall trajectory 分配后续 edge updates 的原因 `A`，是否会把计算浪费在已容易收敛/继续无效的码字上，并使困难但可恢复码字得不到预算；一个 bounded reliability-prioritized budget controller 能否在相同总 CN/VN edge-update 预算下改善 FER/BER，或在 FER/BER 非劣下减少平均/P95 updates/latency？

这里的 `A` 是可审计的结构差异，不是“星地场景没人做过”。目标场景是否真的有足够的 convergence/budget heterogeneity 仍为后续 occurrence/headroom 问题；Step 1 不预写增益。

### 3.2 四判据

| 判据 | verdict | 依据与限制 |
|---|---|---|
| 1. 具体 M-C-A | `PASS` | M、C、A 已分别锁定；current fixed 20/flooding 代码与 Sionna API均可审计。 |
| 2. 方法产出形态 | `PASS` | 可复用产出为 `risk/state observer → bounded continuation/budget rule → stop/fallback → cost receipt`，不是一次性 BER 曲线。 |
| 3. 近期 baseline | `PASS_WITH_CLAIM_LIMIT` | He 2021 提供 recent NR-BG2 quantized NMS/layered/early-stop baseline；目标实现提供同 BG2/Z 的正确 fixed NMS。Wu 2010 只作经典直接 authority。 |
| 4. 可量化对标 | `PASS` | FER/BER、total directed edge-message updates、decoder calls、平均/P95 latency、stop reason、未收敛率均可 paired 比较。 |

四判据形式上 `4/4`，但 direct scheduling prior-art/fulltext 未闭合，所以本 terminal 是 bounded evidence gap，不是 Step 2-ready PASS。

## 4. Receiver-visible IAO

### 4.1 Input

| 输入 | receiver-visible | 当前项目 seam | 使用边界 |
|---|---:|---|---|
| 当前码字 channel LLR 及 `|L_ch|` 分布 | 是 | `READY` | 最小 v0 的唯一必需输入；只能来自 demapper 输出。 |
| per-iteration hard estimate / posterior | 是（算法层） | `LIBRARY_READY / ADAPTER_MISSING` | Sionna v2c callback 给 `x_hat`；soft output需另构 decoder。 |
| syndrome / unsatisfied-check count | 是（由 hard graph estimate + H 计算） | `ADAPTER_MISSING` | 禁止对 `info_hat` re-encode 后算 syndrome；那会恒为合法码字。 |
| message residual / stall trajectory | 是（由相邻 callback message/state 计算） | `LIBRARY_READY / ADAPTER_MISSING` | residual 定义必须由 direct scheduling 全文冻结，不能自创。 |
| iteration/layer index、剩余预算 | 是 | `LIBRARY_READY / ADAPTER_MISSING` | callback 有 iteration；budget ledger 需新 receipt。 |

### 4.2 Action

冻结的最小合法候选只做 **budget**，不先声称动态 layer/edge priority 已可用：

1. 所有码字先执行相同的固定首段 `i0`；或在更窄 v0 中，仅以 frozen channel-reliability bin 选择一个预注册 `num_iter`。
2. 若后续 adapter 暴露 syndrome/stall，则只在固定 checkpoints 决定 `STOP / CONTINUE_WITH_BOUNDED_REMAINING_BUDGET`。
3. 总预算用 edge-message updates 记账；从 easy/clearly-stalled codewords 节省的预算只能在预注册 population-level budget 下分给 high-risk codewords。
4. 不改变 Ch3 CPR、Ch4 demux、APSK demapper LLR、LDPC parity-check matrix、CN update equation或 bit-flipping/OSD action。

动态 layer/edge priority 是 **Step 2 后的可选 richer action**。`static cn_schedule ≠ receiver-driven dynamic priority`：当前 `cn_schedule` 为构造期静态 buffer，不是 per-call/per-codeword priority seam；不得把“库有 custom schedule”写成“项目已能按 reliability 动态排序”。

### 4.3 Output

- decoded information bits；
- `stop_reason ∈ {syndrome_zero/CRC_pass, budget_exhausted, stall_abort}`（当前尚未实现）；
- per-codeword `CN_updates`、`VN_updates`、decoder calls、configured/actually executed segments；
- FER/BER scorer-only 结果；
- 平均、P95、最坏 updates/latency 与未收敛率。

### 4.4 明确禁用的 truth

TX information/coded bits、payload symbols/labels、true SNR/noise variance、true channel/Jones/phase、oracle error positions、最终正确性、BER/FER、未来 frame/sample 均不得进入 risk、priority、stop、budget 或 fallback。它们只在 action/output 冻结后进入 scorer。

## 5. 方法身份与独立性

`Q-C5-5` 的唯一方法身份是 **LDPC decoder 内部/调用侧的 update-budget allocation**。它不得：

- 改 Ch3 CPR、Ch4 RDE/demux 或 post-Ch4 residual bridge；
- 改 APSK constellation、labeling、exact/max-log demapper 或 LLR scale；
- 重命名 C5-0 scalar calibration、C5-1 structured covariance、C5-2 syndrome/bit-flipping/OSD rescue；
- 把 AN-/AO-MS 的 syndrome-conditioned alpha/beta 切换改名为 scheduling；
- 把 standard layered、额外 fixed iterations 或 ordinary early stopping 单独包装成候选。

claim ceiling 固定为：**经典 LDPC complexity-control/scheduling 原子在共同星地 APSK 接收链上的 bounded migration/extension**；不声称首次、SOTA、首创 schedule 或全面优于经典 decoder。

## 6. Collision / absorption ledger

| collision class | 对象 | 吸收关系 | C5-5 剩余空间 |
|---|---|---|---|
| `EXACT_COLLISION` | 未确认 | direct residual/informed scheduling 全文缺失，不能据题名判 exact | `UNKNOWN`，由 Step 2 关闭 |
| `PRIMITIVE_COLLISION` | Wu 2010 AN-/AO-MS | 吸收“unsatisfied check → 改 alpha/beta/offset”完整原子 | C5-5 不改 CN equation，只分配顺序/预算 |
| `RELATED / CHEAP_ABSORPTION` | He 2021 | 吸收 CRC early-stop、syndrome-threshold conditional second stage 与 generic layered-first-stage 包装 | 需胜同 stop rule 的 fixed NMS/OMS，不能靠第二阶段 rescue |
| `RELATED / CHEAP_ABSORPTION` | Baldi 2016 hybrid MRB | 吸收“只在 decoder failure 后花额外成本”和未计 OSD/retry 的收益 | 需在 equal-update 下证明预算规则本身增量 |
| `RELATED` | Zhao 2023 SBF | 吸收 syndrome+reliability bit-flipping/rescue | C5-5 禁止 bit flips/list search |
| `BACKGROUND / STANDARD` | Sionna flooding/layered/custom schedule | 吸收把标准 layered 或静态 CN 顺序当新方法 | 候选必须有 receiver-state-conditioned budget/order delta |

## 7. Baseline 与 equal-update 公平合同

### 7.1 主 baseline

同一目标 BG2/Z=104、`k/n=1024/1536`、同 interleaver/rate recovery、filler、LLR clip、CN update 数值精度与相同 external syndrome/CRC stop rule 下，充分调优的 fixed NMS/OMS：

- flooding 与 standard layered 各自独立调优；
- alpha/beta、最大迭代数和 static per-iteration LUT 只在 disjoint development slice 冻结；
- 当前 `alpha=.75/20/flooding` 是正确实现锚，不是已充分调优的科学 baseline。

### 7.2 强制廉价替代

1. fixed NMS/OMS 获得与候选相同总 edge-update 数的额外固定 iterations；
2. standard flooding 与 Sionna standard layered；
3. static per-iteration alpha/beta LUT；
4. ordinary syndrome/CRC early stop；
5. frozen channel-reliability-bin → fixed iteration LUT（防止复杂 stall controller 只是在复现简单 risk binning）。

### 7.3 预算单位

主口径为每 codeword 的 `CN directed-edge updates` 与 `VN directed-edge updates` 分开记录，再报告二者之和；不得用“1 iteration”直接对齐 flooding、layered 与 custom schedule。当前同一 codec 的历史 introspection 为 `num_edges=5360`，因此一轮 flooding 对每条图边各完成一次 CN 与一次 VN message update；具体是否把二者合计为 `2E` 必须在未来合同中显式冻结，不能混用。另报 sorting/priority bookkeeping、callback、decoder construction、平均/P95 wall latency和峰值状态内存。

## 8. Sionna 2.0.1 / 项目 interface audit

| 能力 | 库级事实 | 项目 seam | Step 1 verdict |
|---|---|---|---|
| `cn_schedule` | 5G decoder 支持 `flooding`、`layered` 或构造期 2-D CN groups；每 row 是一个 subiteration | 当前未传，固定默认 flooding | static comparator `READY`；receiver-driven order `NOT_READY` |
| per-call `num_iter` | `call(..., num_iter=i)` 支持 | wrapper 固定 20、不透传 | `LIBRARY_READY / BOUNDED_ADAPTER` |
| callbacks | v2c 得到 `(msg_vn,it,x_hat)`；c2v 得到 `(msg_cn,it)`，并必须返回同形状消息 | callbacks 为空 | `LIBRARY_READY / ADAPTER_MISSING` |
| state | `return_state=True` 返回 `msg_v2c`，call 接受 `msg_v2c` | `return_state=False`，wrapper 显式拒绝 state | `LIBRARY_READY / ADAPTER_MISSING` |
| soft/full output | `hard_out=False` 可返回 logits；`return_infobits=False` 返回 on-air full codeword order | 只返回 hard info bits | `LIBRARY_READY / ADAPTER_MISSING` |
| native early stop | 源码明确 batching 下无 early stopping | 无 stop reason/actual iterations | `NOT_AVAILABLE`；需 external segmented wrapper |
| syndrome/stall | 可由 callback `x_hat` + decoder PCM 或 consecutive state 外算 | 无 API；旧 re-encode helper 仅能做 encoder correctness | `BOUNDED_ADAPTER`，必须单测 mapping |

安装源码证据：`C:/Users/zzt/.venvs/torch/Lib/site-packages/sionna/phy/fec/ldpc/decoding.py:107-136,314-342,733-786,838-910,1323-1362,1523-1542,1571-1593`。`cn_schedule` 是构造期 state，`num_iter/msg_v2c` 才是 per-call；Sionna 明确没有 native early stop。

### 8.1 接口门

- **最小 budget-only 路径：OPEN WITH BOUNDED ADAPTER。** 复用已验证 TargetApskCodec/BG2 mapping，只为 candidate-local decoder 透传 `num_iter`；若使用 checkpoint continuation，再启用 `return_state` 并外部计算 syndrome/stall。历史 read-only BOM 对 decoder state/callback adapter 的估计为 2–3 日，远低于三月窗口；这不是本任务的实现授权。
- **receiver-driven layer/edge priority：BLOCKED FOR NOW。** Sionna custom schedule 是构造期静态索引；per-codeword dynamic priority 需要独立 decoder construction/rebuilt indices 或内部 patch。缺 direct scheduling fulltext前，不把它作为最小合法动作。
- **整套 BP 自写：NOT REQUIRED。** 因 budget-only 路径存在，本候选不触发 `INTERFACE_OR_TIME_BLOCKED` terminal。

## 9. UNKNOWN 与 bounded gaps

1. **G1 — direct scheduling fulltext（阻塞 Step 1 PASS）**：本地没有 DOI `10.1109/ACCESS.2019.2899106` 正文/read note。Step 2 只需回答：residual 定义、更新粒度、decay/priority rule、flooding/layered/RBP comparator、equal-edge-update 口径、priority overhead，以及是否已完整覆盖 Q-C5-5 的 input/action/output。
2. **G2 — recent budget-control neighbor（claim/collision debt）**：现有全文给出了 adaptive NOMS、early stop和 failure-triggered rescue，但没有一篇近期全文直接核对“receiver reliability/stall → variable BP budget under equal updates”。Step 2 最多补 1–2 篇该动作族的 recent primary fulltexts；不得扩成泛搜。
3. **G3 — target occurrence（后续 formal gate，不由 Step 2 填）**：目标 BG2/Z=104 在自然 DP-APSK population 上的 convergence-iteration、syndrome/stall 与 risk heterogeneity 尚未观测；当前 20 固定轮 receipt 不能替代。该项只记录，不授权 smoke/仿真。

## 10. 唯一下一步

由主控另派一个 **C5-5 GW Step 2 bounded acquisition/read package**：优先合法取得并精读 `10.1109/ACCESS.2019.2899106`，再至多补 1–2 篇 recent reliability/stall-aware BP scheduling/budget primary fulltexts，关闭 exact collision 与 equal-update ledger。Step 2 仍不得实现 adapter、运行 decoder、进入 Step 3 或修改本 terminal。
