# [R003] Post-T012 carrier remap 与 B9 evidence-adapter 选择

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D014

## 调研问题

T012 因 task-interface contract 在科学工作开始前终止、mission 连续 12 包
`mission_method_delta=NONE` 后，哪条合法路线最可能恢复方法生产，而不重复修复、
跳过 Groundwork 门或把治理工作冒充方法？

## 发现

### 1. 当前共同边界

- live D014、formal D025、V033 与 CP012 一致：当前无 active scientific
  carrier；T012 是 `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`，不是 C15
  science negative。
- foreground epoch 30 只允许 Recover、Portfolio Map 与 Task Preparation；新
  workline 激活前禁止 Step 3、MVE 和其他科学实验。
- CP012 的 streak 为 same-axis=2、repair=1、no-method=12；上一包
  `UNDERWEIGHT / DRIFT_RISK`，所以本轮不能继续做第四次 T012 amendment。

### 2. 至少四个候选的六维比较

| carrier | 方法形态 | 预期增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **B9 virtual-carrier self-coherent + DRE** | 数字域虚拟载波替代额外 optical carrier；低比特 DAC 上用 DRE 动态量化与序列优化降低带内量化噪声。候选增量是只使用合法因果/预配置链路状态的 DRE/CSPR 复杂度或稳健性适配；精确输入与适配律待 Step 3 闭合 | source-native DRE 相对同架构 w/o-DRE 的 RO 对照约为 3/1/0.5 dB SNR（3/4/5 PNOB）；这是正向量化噪声锚，不是相对传统 CPR 的 dB 优势 | 主包装假设：“面向星地低比特 DAC 自相干 FSO 的数字分辨率增强与复杂度—稳健性适配。”；回退包装为固定 DRE 的场景迁移边界或复杂度/性能折中 | **HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE**。JLT 2023 accepted fulltext、DOI/title/metadata 闭合，且有 Step-3-like 旧笔记；但当前 formal owner 下尚无 candidate-specific Step 1–3、星地 M-C-A、canonical DRE/DC-Value provenance 或合法 comparator ladder。不得直接实现/实验 | 中：先复用已有全文和共享索引完成 Step 1，再闭合 acquisition/canonical 与 Step 3；无需先建设自相干全链 | Step 1 若出现 novelty saturation、无星地 task-fit 或不足三源，立即回池；Step 3 若四判据/M-C-A/可部署输入不成立，优先回 C15 新合同，不进入 MVE |
| **C15 blind-equalization cost/update** | reduced-constellation/Sato、CMA/MMA、RDE/radius-directed 或 staged cost/update，追求 PM-16QAM 收敛、跟踪或复杂度折中 | 若 canonical lineage 与 task-fit 成立，可能形成低复杂度分阶段盲均衡方法 | “面向动态星地 PM-16QAM 的低复杂度分阶段盲均衡代价。” | **UNRESOLVED / RETURNED_TO_POOL**。T011 只有 OpenAlex coverage；T012 未执行 source/canonical science。C15 未被 Kill，但 same-axis=2 且 one-last T012 已退出 | 中：仍需 canonical/source closure、Step 2 coverage confirmation 与 Step 3；不得把新任务伪装成第四次 T012 amendment | 只有新合同能避开 T012 task-interface 路线并证明比新机制更有方法价值时再激活；canonical collision 或四判据失败即换族 |
| **B1 adaptive phase window** | receiver-visible 噪声/相位创新条件选择 VV phase window | 固定窗在噪声—相位噪声比变化时可能非最优 | “面向 GG 衰落与 Wiener 相位噪声的自适应相位窗。” | **FORMAL_ELIGIBLE_BUT_PROHIBITED_REPAIR**。Step 1–3 存在，但 T007/T008 的 no-crossing proxy、oracle candidate、π/2 branch、BER population 与 working-region 均未闭合 | 高：第三次 evaluator/working-region 重建；D002/D014 明确禁止 | 只有新的独立 evaluator/source 证据改变身份债务时才能复议；当前不选 |
| **A4 deployable CPR selector** | 因果接收状态在 DA/NDA CPR 路线间选择或融合 | 理论上可在深衰落/导频可靠性变化时降低 outage | “面向星地深衰落的可部署 DA/NDA 载波恢复选择器。” | **BLOCKED_IDENTITY / RETURNED_TO_POOL**。T009 暴露 pilot/TX-truth、DA/NDA frequency-stage、working-region 与 artifact closure 四类 P0 | 高：第二个 A4 identity/evaluator repair；D005 明确不开 | 只有独立外部证据或新合法实现改变四类 P0 时复议；当前不选 |

### 3. B9 的磁盘证据与证据上限

主仓共享论文库：

- `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2023.3270673/metadata.json`
  记录 title/DOI、`download_status=success`、Zenodo accepted version；
- 同目录 `content.md:5-25,37-43,109,125-171,233-253` 支持 virtual carrier、
  low-resolution DAC、DRE、DC-Value、42 m FSO 与 3/4/5-PNOB 对照；
- `.sessions/2026-07-02-carrier-sync-v2-deep-read/S005-conversation3-b8b9b10-eval.md:65-80`
  与
  `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b8b9-self-coherent.md:27-40`
  保存旧的全文提取和六维切法；
- `projects/thesis-fso/literature_notes.md:607-613` 记录 B9-Q1/Q2/Q3 与范围迁移
  债务。

这些材料证明“有正式全文锚、正向量化信号和可讨论的方法形态”，不证明当前
formal Step 1–3 已完成。尤其：

1. 约 3 dB 是同一 virtual-carrier 架构下 DRE vs. RO，不能冒充相对传统 coherent
   CPR 的方法优势；
2. 实验是 42 m outdoor FSO，不是 LEO-ground 深湍流；
3. 当前没有 source-native DRE/DC-Value/virtual-carrier 实现；
4. comparator 仍缺任务匹配的传统 quantization-noise-shaping ladder；
5. APN 跨场景全文的 metadata 与 Yoffe DRE canonical provenance 尚未完全闭合。

因此 B9 只能从 Step 1 evidence adapter 起步，不能直接成为 runnable carrier。

### 4. 为什么 B9 比至少两个替代项更可能产生 METHOD_SIGNAL

- **相对 C15**：B9 已有可复核正向 dB 锚、明确技术动作和新机制；C15 的
  source/canonical science 尚未执行，且已连续两个同轴包。B9 的下一包可直接
  判断新方法空间是否有三源/两路线/传统 comparator 支撑，信息增益高于第四次
  C15 task-interface 路径。
- **相对 B1**：B9 是未消耗 repair 配额的新机制；B1 继续需要第三次 evaluator
  重建，违反现有退出边界，且即使工程 PASS 也仍可能停在 working-region 身份。
- **相对 A4**：B9 的首债务是可逆的文献/formalization 闭环；A4 需第二次修复
  四类 P0 的 evaluator/identity，成本和复发风险更高。

该比较只选择“最值得 formalize 的候选”，不预支 `METHOD_SIGNAL`。T013 Step 1
完成仍只能记 `mission_method_delta=NONE`。

## 结论

选择 **B9 evidence-adapter/formalization** 作为下一 workline，但保持
`NO_ACTIVE_SCIENTIFIC_CARRIER`。最小下一包 T013 只完成 candidate-specific
Groundwork Step 1：

- 复用主仓共享索引和已有全文锚，同时运行必要的定向多源检索；
- 闭合 ≥20 candidates、≥3 source families、≥2 mechanism routes、≥5 必读、
  正式发表 ≥50% 与 AI 语义审查；
- 明确 DRE canonical、DC-Value/virtual-carrier lineage、传统量化噪声整形
  comparator 与星地 task-fit 的 acquisition debt；
- 完成后停在 `STEP1_COMPLETE_AWAITING_ACQUIRE`，不足门槛则返回 remap；
- 不下载、精读、实现或实验。

候选正向合同仅作为待验证假设：

- `positive_method_target`：在低比特 virtual-carrier self-coherent 星地 FSO 中，
  用因果可部署或预配置链路状态选择 DRE/CSPR 的复杂度—稳健性设置，并保留
  source-native fixed-DRE/RO 安全回退；
- `minimal_construct`：须等 Step 3/3.5/4a 后才能冻结，当前未授权；
- `fair_comparator`：RO without DRE、source-native fixed DRE，以及经全文闭合的
  任务匹配传统 noise-shaping 方法；
- `primary_packaging`：星地低比特 DAC 自相干 FSO 的分辨率增强与稳健适配；
- `fallback_packaging`：固定 DRE 的星地迁移边界或复杂度/性能折中；
- `next_positive_action`：完成 T013 Step 1 coverage/collision adjudication。

## 对决策的影响

- live 新建 D015，formal 新建 D026；二者只激活 B9 formalization workline，
  不激活 scientific carrier；
- foreground control 递增为 epoch 31 / CP012，并只增加
  `CANDIDATE_FORMALIZATION`；
- 新建 T013，独立 dispatch verifier PASS 前不执行；
- Step 2、Step 3、3.5、4a/MVE、Step 5、Contract、Execute 继续锁定。
