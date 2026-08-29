# C5-5 reliability-driven LDPC budget — GW Step 3 frozen-fulltext read

> T080｜2026-08-30｜authority `bc5c0cbff3528d1c24db9a2775b3d23dc1aff232`
> 范围：只精读 T079 冻结的两篇全文，裁决动作链、ordinary early-stop 吸收与唯一 Q#；无搜索、下载、实现、仿真或 Step 3.5。

## 1. Facts-first receipt

- task-control validator：`PASS`（CP021 / epoch 21 / `C5_5_GW_STEP3_FROZEN_FULLTEXT_READ`）。
- identity：`2/2 PASS`；完整全文精读：`2/2`。
- 冻结池只有：
  1. `papers/doi/10.1587_transfun.2024eal2080/content.md`；
  2. `papers/doi/10.1109_wcsp52459.2021.9613326/content.md`。
- DOI `10.1109/ACCESS.2019.2899106` 仍无合格全文；错配的 2007 arXiv 未读取、未用于结论。
- Liu 2025 的 `content.md` 丢失部分公式/Algorithm 1 图像；承重公式由同目录 canonical `source.pdf` 的 Eq. (1)/(11) 只读核对。He 2021 的 legacy `source.pdf` 是 plaintext，本文只以 canonical `content.md` 承重并保留 source-format debt。
- 两篇均由独立只读 subagent 完整提取；主任务随后逐行复核承重位置。逐篇 read notes：
  - `papers/_read_notes/10.1587_transfun.2024eal2080.md`
  - `papers/_read_notes/10.1109_wcsp52459.2021.9613326.md`

## 2. 逐篇标准条目

### 2.1 Liu et al. 2025 — RL-CBP

- **身份/来源**：正式发表，IEICE Transactions on Fundamentals，2025；DOI `10.1587/transfun.2024EAL2080`；title check=`match`。
- **核心贡献**：RL-CBP 用较短的 check-belief reliability list 近似 RBP 的全 residual 动态调度，只在 list 内选择优先更新的 check node，以减少比较开销（`content.md:91-107`）。选中节点后更新 B2V、posterior、V2C、C2B 与相邻 reliability/list；其动作是译码内部的局部消息更新顺序（`:109-129`）。
- **状态/输入**：check-belief 及其内部更新幅度。check-belief 表示 parity check 满足的后验对数比；调度 reliability 为更新前后 check-belief 的绝对变化量（source.pdf Eq. (1)/(11)；`content.md:53-57,121-129`）。它们 receiver-computable，但属于 decoder-internal state，不是译码前外部 channel/pilot reliability。
- **动作/停止**：从短 list 选最大 reliability check node，局部更新后持续维护 list；全部 check-belief 为正或达到固定最大迭代数时停止（`:103-141`）。最大迭代数不随 reliability 改变，也没有码字间预算分配。
- **设置**：BPSK-AWGN，rate 1/2，码长 2048/8192，regular (3,6) 与指定 irregular LDPC，PEG 构码，最大 50 iterations，最终 list size 64（`:129-145,175`）。
- **baselines**：FBP/BP、LBP、RBP、CBP（`:161-187`）。
- **结果/复杂度**：2048 irregular code、BER 约 `1e-5` 时，相对 CBP/LBP/FBP 约有 `0.06/0.11/0.16 dB` 增益并接近 RBP；报告平均迭代、消息更新、乘加与比较数，但没有 equal-total-edge-update、P95 latency 或 wall-clock 公平合同（`:173-199`）。
- **实验完备性**：有两码长、regular/irregular 与 list-size 扫描；无 seeds、CI、error bars、硬件时延/内存或统一调参声明。VVUQ=`2/3,1/3,1/3`。
- **DRL 字段**：状态空间/动作空间/奖励/网络架构均 `N/A（传统确定性译码算法，非 MDP/DRL）`；实际消息状态与确定性调度动作另行如上提取。
- **适配性**：是 reliability-driven LDPC computation 的直接强邻居；不支持“外部预译码可靠性→码字级 `num_iter` 档位”已被实现。

### 2.2 He et al. 2021 — quantized NMS + TS post-processing

- **身份/来源**：正式发表，IEEE WCSP 2021；DOI `10.1109/WCSP52459.2021.9613326`；title check=`match`。
- **核心贡献**：第一阶段使用 5-bit layered quantized NMS；CRC failure 后计算 syndrome，只在 `||s||<=10` 时用离线 trapping-set/error-offset patterns 执行 CSCD/SA-CSCD 位翻转，以降低 NR BG2 LDPC 的 high-SNR error floor（`content.md:11-27,93-111,139-147`）。
- **状态/输入**：第一阶段 decoded bits/codeword、CRC pass/fail；失败后使用 syndrome、unsatisfied-check count、BG 与离线 pattern table。它们可由接收端获得，但不是译码前外部 reliability（`:95-111`）。
- **动作/停止**：CRC pass 时停止第一阶段；否则在固定 first-stage cap 后触发 syndrome-gated post-processing，逐 cyclic-shift candidate 翻位并 CRC，首个 pass 即停（`:47,99-109,164`）。正文未说明 CRC 每轮还是固定 checkpoint 检查。
- **设置**：BPSK-AWGN，NR QC-LDPC BG2，`K=3840/1440/960`、rate `2/3,1/2,1/4`，5-bit uniform quantization，layered schedule，最大 100 iterations（`:47,95-99,162-166`）。
- **baselines**：layered BP 与同码 quantized NMS；WiMAX NMS 是异码结构参照，不是同码公平 budget baseline（`:47-55,164-176`）。
- **结果/复杂度**：一个稀有事件点为 `1.82e8` trials / 100 errors / FER `5.47e-7`；论文报告 error floor 降至原来的约 `1/2–1/10`，`K=1440` 低 FER 区约 `0.3 dB`，但未报告平均/P95 iterations、edge updates、runtime、pattern activation rate 或 storage 数值（`:47,194-202`）。
- **实验完备性**：多 K/rate，但只有 AWGN；无 seeds/CI/error bars，缺 equal-update、公平 post-processing 成本与 pattern train/eval independence。VVUQ=`2/3,2/3,1/3`。
- **DRL 字段**：状态/动作/奖励/网络均 `N/A（传统确定性译码与后处理，非 MDP/DRL）`；实际 CRC/syndrome 控制状态与 bit-flip 动作另行如上提取。
- **适配性**：ordinary CRC early stop 是 C5-5 必须面对的 cheap comparator；TS rescue 是 post-failure bit-flip strong neighbor，不是 iteration-budget action。

## 3. 九字段动作碰撞

### 3.1 Liu 2025 vs Q-C5-5

| 字段 | 判定 | 全文事实与差异 |
|---|---|---|
| 1 target code/decoder | different | RL-CBP/CBP vs 同一 fixed NMS/OMS 的 per-call `num_iter`（`:99-129`） |
| 2 context | different | BPSK-AWGN regular/irregular LDPC vs DP-(8,8)-16APSK+BICM coherent-FSO（`:129-141`） |
| 3 receiver-visible input | different | decoder-internal check-belief residual vs 由当前码字 channel LLR 派生的 predecode reliability statistic |
| 4 state statistic | different | `abs(Omega_new-Omega_old)` vs current-codeword LLR-derived reliability bin（source.pdf Eq. (11)） |
| 5 action | different | 选 next check node/edge vs 选少量 `num_iter` 档位（`:103-129`） |
| 6 granularity/timing | different | 码字内部局部更新后反复决策 vs 每码字译码前一次 |
| 7 update/stop/budget | different | dynamic list schedule + all-positive stop + fixed cap 50 vs frozen reliability-bin→iteration cap（`:129-141`） |
| 8 output/objective | different | BER、平均迭代与解析比较复杂度 vs decoded bits、BER/FER 与真实平均/P95 updates |
| 9 cost/fairness | different | 操作数与 convergence-speed 假设；无 equal-total-update 合同（`:185-199`） |

**裁决**：`STRONG_NEIGHBOR / PRIMITIVE_OVERLAP / NOT_EXACT_COLLISION`。它否定宽泛的“首次 reliability-driven LDPC scheduling”，但不占据 C5-5 的外部输入、码字级预算接口与决策时序。

### 3.2 He 2021 vs Q-C5-5

| 字段 | 判定 | 全文事实与差异 |
|---|---|---|
| 1 target code/decoder | different | 同属 NMS family，但 He 是其 5-bit layered NR-BG2 配置；Q 要在目标 fixed NMS/OMS exact codec/config 上选择 cap（`:95-99,164`） |
| 2 context | different | BPSK-AWGN high-SNR error floor vs DP-APSK/BICM coherent-FSO（`:47,95`） |
| 3 receiver-visible input | different | decoded bits/CRC/syndrome/TS patterns vs 当前码字 LLR 派生的 predecode reliability statistic（`:99-111`） |
| 4 state statistic | different | CRC pass/fail、`||s||`、syndrome pattern vs current-codeword LLR-derived reliability bin |
| 5 action | different | stop / TS bit flips vs `num_iter` 档位（`:99-109`） |
| 6 granularity/timing | different | CRC-pass stop（check cadence UNKNOWN）或 first-stage failure 后 vs 译码前 per-codeword |
| 7 update/stop/budget | different | cap100 + CRC stop + syndrome gate + rescue CRC stop vs reliability-conditioned cap（`:47,99-109,164`） |
| 8 output/objective | different | bits + high-SNR FER/error floor vs bits + BER/FER + cost Pareto |
| 9 cost/fairness | different | 定性 controllable complexity；无 average/P95/equal-update 数字（`:109,147`） |

**裁决**：`ORDINARY_EARLY_STOP_PRIMITIVE_OVERLAP / MANDATORY_CHEAP_COMPARATOR / NOT_EXACT_COLLISION`。TS post-processing 另属 post-failure rescue，不是 C5-5 身份。

## 4. Cross-paper synthesis

### 4.1 动作链边界

| 对象 | runtime statistic | action | timing | cap/budget |
|---|---|---|---|---|
| Liu RL-CBP | decoder-internal check-belief residual | 选择局部 check-node/edge 更新顺序 | 每次局部消息更新后 | fixed max=50；不按 reliability 改 cap |
| He ordinary stop | CRC success | 已成功则停止 | 译码过程中，检查频率 UNKNOWN | fixed max=100；不预分困难码字预算 |
| He TS stage | CRC failure + syndrome/TS pattern | bit flips + candidate CRC | first-stage failure 后 | post-processing search，非 BP iteration budget |
| Q-C5-5 | 当前码字 channel LLR 派生的 predecode reliability statistic | 选择少量 frozen `num_iter` 档位 | 每码字译码前一次 | 同一 fixed NMS/OMS 的 per-call cap |

### 4.2 Ordinary early-stop absorption verdict

```text
NOT_COMPLETE_ABSORPTION / MANDATORY_CHEAP_COMPARATOR / EMPIRICAL_ABSORPTION_UNKNOWN
```

ordinary CRC/check-satisfaction early stop 会让已经成功的 easy codeword 少做迭代（实际节省取决于未报告的 check cadence），因此它可能吸收 C5-5 的大部分**平均成本**收益，不能只拿 fixed-20 无早停作对手。但对尚未通过 CRC/syndrome 的码字，它仍使用统一预设 cap，不能借 predecode reliability 区分 hopeless 与 difficult-but-recoverable 并选择低/中/高预算档位。两篇均未给 `high-cap + ordinary early stop` 与 LLR-derived reliability LUT 的 equal-total-update BER/FER—平均/P95 成本比较，因此“经验上已完全吸收”仍是 UNKNOWN，不能据机制相邻直接判 `ABSORBED_CLOSE`。

### 4.3 P0 2019 缺失的影响

P0 缺失使“该 specific residual-decaying paper 是否完整重复”保持 UNKNOWN，故不能声称“完全重复未发现”“首次”或 prior-art closure。它不阻塞本次 candidate-level Q#：Liu 2025 已足以确认最接近的 direct scheduling 邻居位于 decoder-internal residual、局部 edge/check-node scheduling，而 frozen Q# 位于 external predecode reliability、per-codeword cap；He 2021 又单独冻结了 ordinary early-stop 的廉价吸收边界。因此 P0 是 **Step 3.5 provenance/exact-collision debt 与 claim-ceiling limiter**，不是当前 Q#/IAO 为空的证据。

## 5. 唯一 canonical Q-C5-5

### 5.1 M-C-A 与四判据

**Q-C5-5**：充分调优且带 ordinary syndrome/CRC early stop 的 fixed NMS/OMS `M`，在共同 DP-(8,8)-16APSK+BICM/5G-BG2-LDPC 接收机中、面对码字间 receiver-visible reliability 不均且平均/P95 edge-update 预算受限的条件 `C`，因其对尚未通过 CRC/syndrome 的码字仍采用统一预设最大迭代 cap、不能在译码前用当前码字 LLR 派生的 reliability 区分 hopeless 与 difficult-but-recoverable 并选择预算档位的假设 `A`，是否会产生不合适的预算分配；一个 frozen reliability-bin→iteration-cap rule 能否在相同真实更新成本下改善 FER/BER，或在 FER/BER 非劣下减少平均/P95 成本？

| 判据 | 结果 | 依据与边界 |
|---|---|---|
| 1 具体 M-C-A | ✅ | M 已含 ordinary early stop；C/A 指向“未成功码字统一 cap”而不是泛化动态调度 |
| 2 方法产出形态 | ✅ | 可复用的 receiver-visible reliability bin、冻结预算 LUT 与 cost receipt |
| 3 近期 baseline | ✅（claim 受限） | He 2021 提供 recent layered quantized NMS+CRC stop；Liu 2025 提供 recent direct dynamic-scheduling neighbor |
| 4 可量化对标 | ✅ | BER/FER、CN/VN edge updates、平均/P95/最坏成本与 latency 可 paired 比较 |

### 5.2 Receiver-visible IAO

1. **Input**：只使用当前码字 channel LLR 在译码前计算的预注册 reliability statistic；不得读取 TX bits、true SNR/noise、payload labels、oracle error positions、未来帧或最终正确性。pilot/channel summary 不属于已冻结 v0；若 Step 3.5 需要加入，必须另行取得动作与来源证据。
2. **Statistic**：少量预注册 reliability bins；v0 不依赖 decoder-internal message truth/state。若未来使用 syndrome/stall，须另立 adapter 与动作边界，不能偷换本 Q#。
3. **Action**：从少量冻结档位选择同一 fixed NMS/OMS 的 per-call `num_iter` cap；CN equation、alpha/beta、schedule、demapper、Ch3/Ch4 均不变。
4. **Output**：decoded information bits；scorer-only BER/FER；实际执行的 CN/VN directed-edge updates、decoder calls、ordinary stop reason、平均/P95/最坏成本与 latency。
5. **最低预算身份**：先只允许 per-codeword predecode cap selection；不扩为 dynamic edge priority、TS rescue、自写 BP、跨码字在线借贷或 decoder-internal controller。

### 5.3 可证伪目标与停止条件

- 必须先证明 current-codeword LLR-derived reliability 与“同一 fixed decoder 达到成功/继续有用所需 updates”有稳定关系。
- candidate 必须对 `high-cap tuned NMS/OMS + ordinary syndrome/CRC early stop` 提供增量；只胜无早停 fixed-20 不成立。
- 在 equal-total-update 下不得被 extra fixed iterations、ordinary early stop 或 frozen reliability-bin LUT 的更简单版本完整吸收。
- 若 high-cap ordinary early stop 在 BER/FER—平均/P95 成本上完全支配，或 LLR-derived reliability 对 needed iterations 无增量，判 `ABSORBED/NO_HEADROOM`；本任务不执行该验证。

## 6. 公平 comparator ladder

| comparator | 两篇全文支持 | 本次冻结的后续合同 |
|---|---|---|
| tuned fixed NMS/OMS | He 支持 layered quantized NMS；OMS 与目标配置调优非文献事实 | 同 BG2/Z/clip/CRC stop，alpha/beta/cap 在 disjoint development slice 冻结 |
| ordinary syndrome/CRC early stop | He 直接支持；Liu 支持 all-check-beliefs-positive stop | 必须与 candidate 同 decoder、同 CRC/syndrome、同 stop checkpoint |
| equal-total-update extra fixed iterations | 两篇均未实验支持 | 必须按真实 CN/VN directed-edge updates 对齐，不能用 nominal iterations 代替 |
| standard flooding/layered | Liu 比较 FBP/LBP；He 使用 layered | 两者各自公平调优并报告实际 cost |
| frozen reliability-bin→iteration LUT | 两篇均未直接支持 | 它本身就是最小 C5-5 candidate/cheap form，不得再叠复杂 stall controller冒充增益 |
| internal dynamic schedule | Liu 的 RBP/RL-CBP 直接支持 | 只作强邻居/可选 comparator，不与 per-call cap 混为同一动作 |
| TS post-processing | He 直接支持 | 只在声称涉及 error-floor rescue 时列；不属于 budget-only 主身份 |

复杂度主口径冻结为每码字实际 CN/VN directed-edge updates，并另报 sorting/LUT/callback、decoder construction、平均/P95 wall latency和峰值状态内存。两篇的平均迭代/解析操作数或定性 complexity 不能冒充该公平合同。

## 7. Step 3 terminal

```text
STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5
```

- **Q#**：`Q-C5-5`，唯一，四判据 `4/4`。
- **ordinary early-stop**：不是九字段完整吸收；是 mandatory cheap comparator，经验吸收程度 UNKNOWN。
- **exact collision**：两篇均 `NOT_EXACT_COLLISION`；Liu=`STRONG_NEIGHBOR/PRIMITIVE_OVERLAP`，He=`EARLY_STOP_PRIMITIVE_OVERLAP`。P0-specific collision 仍 UNKNOWN。
- **claim ceiling**：只允许“目标 DP-(8,8)-16APSK coherent-FSO 接收机中，当前码字 LLR 派生的 receiver-visible predecode reliability 驱动 fixed NMS/OMS 码字级迭代 cap 的经典预算迁移/扩展”。不得声称首次、SOTA、全面领先、近期工作均未做过或已有 BER/FER/复杂度收益。
- **blocker**：进入另一个 checkpoint 的 Step 3.5 没有 candidate-level blocker；但 P0 2019 合格全文缺失是 exact-collision/provenance debt，ordinary early-stop 的实证吸收与 equal-update 成本仍是后续 paper/experiment gate，不得在本 terminal 内补证。
- **唯一下一步**：回主控决定是否另开 bounded Step 3.5 exact-recipe/collision closure；本任务不进入 Step 3.5。
