# [R005] Groundwork Step 3 direct-competitor synthesis

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D004

## 调研问题

9 篇 qualified 全文是否支持一个具体、可证伪、对近期 baseline 可量化且与 full/cheap alternatives 边界可辨的 Q；D1/D2 哪个仍具有完整方法输出形态？

## 发现

### 精读闭包

9/9 title gate PASS 并完成结构化精读。C05/C09/C10 的公式声称已回看 source PDF；C11 仅使用 publisher chrome 后的正文；C02/C08 由 source TeX 手工闭合 title gate。canonical read notes、专题 owner 与项目 read-log 均已落盘；C08 复用已存在 canonical note且不修改其 unrelated dirty 内容。

### Direct/full/cheap action matrix

| 方法 | 关键动作 | 复杂度/时延 | 对 D1/D2 的裁决 |
|---|---|---|---|
| C01/C14 | H=1 adjacent-difference unwrap，lag0立即commit | O(1)/sample | reference + strongest simple baseline；published suffix defect |
| C09 CSSC | buffered `δ` threshold→hard suffix ±π/2 correction | O(1) rolling, O(N+L) buffer | D2 trigger/repair强廉价吸收；无 parallel tracks |
| C02 Tikhonov mixture | M-way expand→likelihood→KL/CMVM→L cap/`φ`→pilot recovery→fwd/bwd LLR | O(ML²)/symbol/decoder iteration；无fixed lag | primitive capability full-general superset；task-contract strong neighbor，非exact |
| C10 reduced-rate KF | one Gaussian phase/CFO state every m symbols + endpoint interpolation + adaptive Q | exact RA/RM/LUT；fixed m buffer | 占fixed-lag和reliability-adaptation原子；无 discrete wrap hypotheses |
| C11 atan2 OPLL | fourth-power+MAF+atan2 amplitude-independent loop | 30/35ns loop, O(L) memory | 吸收 vague fade-reliability D2 动机 |
| C12 hybrid CPR | feedback coarse + N=64 feedforward residual | 4K mult+67K add；11μs lock | 近期强 cheap；吸收 low-SNR slip 动机，非exact |
| C05 residual carrier | Tx carrier+digital beating common-mode PN cancellation | system/info overhead, DSP cost未报 | system-level alternative；receiver-only scope外 |
| C08 AGC+DPLL | AGC+single second-order PLL | O(1), 1.4ms acquisition | FSO cheap neighbor，非multi-hypothesis |

### C02 边界

C02 在多轨迹、fixed order2/3、likelihood、merge/prune、confidence、pilot recovery的能力轴是 `FULL_GENERAL_SUPERSET`；但其输入为 coded MPSK+pilots+LDPC soft，正式输出是 block forward/backward LLR，没有 residual-CFO/integer-wrap state、fixed-lag commit、fixed end-to-end latency/memory或 unwrapped-sequence output。因此对 Q001 完整任务合同是 `STRONG_NEIGHBOR`，不是 exact collision，也不是 task-contract full superset。

### D1/D2 disposition

- D2 不作为独立 Q：C09/C10/C11/C12 已分别覆盖 hard reliability trigger、innovation adaptation、fade-independent discriminator、fixed feedback slip suppression。仅“低可靠时扩展”不足以形成方法章。
- D1 保留为唯一问题输出形态：`decoder-free single-tone receiver input → explicit H≤3 discrete 2π-wrap hypotheses → receiver-only likelihood/merge-prune → fixed-lag commit → one unwrapped sequence + confidence/fallback flag`。这是一套 task/resource/output contract，不是对“多假设/fixed lag/H=3”的独占声明。

### Baseline ladder

1. traditional unoptimized：C14/C01 H=1 unwrap→Wang ML/MAP；
2. enhanced cheap：C09、C10、C12；FSO fade stress 下 C08/C11；
3. full-general：C02 unlimited/adaptive + fixed order2/3；
4. different-information system alternative：C05，单列 Tx-assisted budget。

### Canonical Q001

`M=Wang C01 single-path Fu–Kam unwrap→joint ML/MAP；C=coherent FSO residual CFO + laser Wiener PN，receiver需decoder-free且fixed memory/worst latency；A=H=1 lag0 greedy unwrap假设每个adjacent principal increment的唯一branch始终正确，错误commit污染suffix；而full mixture的decoder/pilot/bidirectional合同及资源/输出不适配。`

| glossary 判据 | 证据 | 结论 |
|---|---|---|
| 1 技术矛盾 | C01 :343–357/:423–451；C02 :126–138/:297–319 | PASS |
| 2 方法产出 | bounded H≤3/fixed-lag/commit/fallback/unwrapped output完整合同 | PASS |
| 3 当前 baseline | C01 2022；C10 2021/C11 2023/C05 2024/C12 2025；C02 mandatory | PASS |
| 4 可量化 | unwrap failure/suffix length/MSE/BER + ops/memory/worst/average latency | PASS |

## 结论

`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`。

Q001 四判据 4/4；full-general 与 cheap comparator 边界可辨，D2 已合并为可选 component/ablation。此 terminal 只授权“存在 Step 3.5 exact-action closure 入口”，不证明目标 FSO defect 已发生，不构成方法、新颖性、Go 或 `METHOD_SIGNAL`。

## 对决策的影响

建立 D005：Step 3 收口并冻结唯一 Q001 与 baseline ladder。下一合法动作只有另行授权的 Groundwork Step 3.5；不得直接进 Step 4a、实现或仿真。
