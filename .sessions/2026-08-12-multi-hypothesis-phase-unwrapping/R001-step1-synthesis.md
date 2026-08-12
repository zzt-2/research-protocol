# [R001] K2 Groundwork Step 1 综合

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D001

## 调研问题

Wang TSP 2022 phase-unwrapping suffix pollution 是否有可迁移到 coherent FSO residual CFO + laser Wiener PN 的物理前提、近期 task-matched baseline 和未被 exact action 占据的低复杂度设计空间？

## 发现

### 1. Step 1 质量门

| 门 | 数字 | 判定 |
|---|---:|---|
| query / round | 11 / 2 | 三路线均完成宽搜+定向补查 |
| raw / title-dedup / semantic | 278 / 242 / 138 | PASS（≥20） |
| 实际贡献源 | S2 / OpenAlex / SerpAPI Scholar = 3 | PASS |
| formal | 98/138=`71.01%` | PASS（≥50%） |
| must-read | 12 | PASS（≥5） |
| 技术路线 | 3 | PASS（≥3） |

机械口径和 query 见 `R002-step1-search-receipt.md`；逐项动作与碰撞见 `R003-step1-candidate-collision-matrix.md`。

### 2. Published defect 与物理迁移分开

- **source defect**：Wang estimator 以 unwrapped phase 为输入；一次 unwrap failure 会污染全部后继累计点。论文为展示 estimator 本体在较大 `ω0/N/σp²` 时丢弃 failed runs。该事实是一手 published defect，不等于 target FSO occurrence 已成立。
- **迁移前提**：2020 JLT space-ground coherent optical link 明确包含 residual frequency mismatch、laser phase noise、turbulence 与 DPLL；2019 coherent wireless optical CSSC-CPE 把 turbulence/linewidth 与 cycle slip 联系；2025 inter-satellite CPR 直接处理 Doppler FO + laser PN，并讨论 slip/complexity。故 transfer 是可证伪而非凭空类比。
- **边界**：laser Wiener PN 与 atmospheric turbulence phase 必须分开建模；后续若自然 target slice 没有 suffix errors 或性能损害，应快速停止。

### 3. 三条路线

1. **unwrap / cycle-slip route**：original/improved unwrap、LMMSE-WPA、CSSC-CPE 与 multi-hypothesis winding。该路线提供 published defect 和最便宜 repair/avoidance comparator。
2. **mixture / sequence route**：full Tikhonov mixture、maximum order 2/3、KL merge/prune、pilot confidence recovery，以及 fixed-lag/sequence tracker neighbors。该路线是能力上界与 complexity comparator。
3. **coherent optical/FSO low-complexity CPR route**：space-ground DPLL、satellite all-digital OPLL、reduced-rate Kalman、pilot-UKF/reset、2024 low-cost optical CPR、2025 inter-satellite feedback+feedforward CPR。该路线提供任务适配、实现和近期 baseline。

### 4. 两个待审设计形态（不是方法卡）

| complexity/action field | D1 bounded 3-hypothesis fixed-lag unwrap | D2 reliability-triggered expansion |
|---|---|---|
| input | receiver `|r_k|`、principal phase、causal CFO/PN prediction | D1 输入 + receiver-visible normalized innovation / amplitude-informed variance / branch margin |
| hypothesis state | 固定最多 `H=3` 相邻 winding 分支 | 默认 `H=1`，仅 receiver-visible trigger 时扩到 `H≤3` |
| score | Wang AOPN/Wiener prior 下的 causal likelihood；具体式留待全文 | 同 D1；trigger 不读 true phase/CFO/label |
| merge/prune | duplicate-equivalent merge + top-3 bounded prune；细节待闭合 | trigger window 内同 D1，恢复可靠后收缩到单轨 |
| lag/commit | 固定 lag `L` 后提交最老 prefix；必须报告最坏延迟 | 同一 fixed-lag commit；不得无限等待 confidence |
| fallback | original/improved unwrap 或 pilot reset；all-ambiguous 明示 failure | 不触发时 exact no-op 单轨；持续 ambiguous 时 pilot reset/failure flag |
| output | unwrapped phase sequence + confidence/failure metadata，送回原 ML/MAP | 同 D1，且输出 expansion-used 标志供复杂度审计 |
| cost contract | worst-case `O(H)` score、bounded merge；memory `O(HL)`，`H=3` | worst-case 同 D1；expected cost 与 trigger rate 一并报告 |

D1/D2 都必须与 full mixture、fixed order 2/3、original/improved unwrap、LMMSE-WPA、CSSC-CPE、pilot reset 和近期 optical CPR 比较。上述表只冻结后续检索字段，不证明算法有效或新颖。

### 5. Direct competitor / collision

- TCOM 2016=`FULL_GENERAL_SUPERSET / MANDATORY_COMPARATOR`：相同能力原子包括 multi-trajectory、likelihood、merge/prune、bounded order、confidence/pilot recovery；不同完整链为 coded MPSK+LDPC soft input、全序列 forward/backward mixture、posterior/LLR output，无 fixed-lag unwrap-sequence commit。
- 2019 CSSC-CPE=`CHEAP_ABSORPTION_RISK`：检测 slip position/direction 后修正，可能吸收“错误后修复”，但摘要未给并行 bounded winding/fixed-lag action。
- 2021 reduced-rate Kalman、2020 pilot-UKF/reset、2020/2023 DPLL/OPLL=`CHEAP_OR_IMPLEMENTATION_NEIGHBOR`。
- 2025 inter-satellite feedback+feedforward CPR=`CLOSEST_2019_PLUS_TASK_BASELINE`；摘要未显示 D1/D2 完整链，Step 2/3 必须闭合。
- 2024 low-cost/improved optical CPR 与 2026 blind-CPR slip mitigation=`RECENT_COLLISION_DEBT`；只凭 metadata/abstract 不裁 exact/non-exact。

## 结论

`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。

理由：三路线与全部质量门通过，published defect 与 target transfer 分开，strong/full-general/cheap comparators 均已进入矩阵；当前没有一手证据确认 D1/D2 完整 input→decision→action→output exact collision。该 terminal 只表示 Step 1 evidence pool 合格，不是 Q#、Go、方法、METHOD_SIGNAL 或论文贡献。

## 对决策的影响

建立 D002。下一合法动作仅为主控确认后进入 Step 2，获取/绑定至少五篇 CORE，优先闭合 TCOM 2016、Wang 2022、2019 CSSC-CPE、2025 inter-satellite CPR 和最接近的 2024/2026 optical CPR；未确认前停止。
