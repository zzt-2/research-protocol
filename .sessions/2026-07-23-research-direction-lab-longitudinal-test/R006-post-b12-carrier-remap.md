# [R006] Post-B12 carrier remap：B4、B6、C15 formal readiness

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D019 / formal D030

## 调研问题

T015 因物理合同错误与 direct robust-CPR novelty collision 在 dispatch 前撤回后，
B4、B6、C15 中是否存在可直接激活并运行 seed 的 legal scientific carrier？若
不存在，哪个一次性 formalization package 最能缩短到
`CONSTRUCT_CREATED + FAIR_COMPARISON_RUN + METHOD_SIGNAL` 的路径？

## 发现

### 1. 三候选六维比较

当前仍不足三个 runnable scientific carrier；实际上三者均未达到可运行 seed 的
formal readiness。下表逐项证明其状态，不把“family 未 Kill”“已有代码”或
“能做 formalization”偷换成 active scientific carrier。

| candidate | 方法形态 | 预期 method delta | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **C15 collapse-safe、scale-fair staged blind equalizer（推荐 formalization workline）** | 先用 Godard/CMA 保留 outward recovery gradient，再由 receiver-visible ring occupancy、cost/update norm 或 fade confidence 决定切换到 RDE/ring-aware tracking；各 cost 独立 tuning 或显式 update normalization，异常时回退/重置 | **T016 本身必须为 `NONE`**；它只闭合 Step 1 view、recent identity 与 canonical staging。独立 promotion 和覆盖面确认后，后续 Step 3 才能冻结 M-C-A/Q#；再下一方法包才可能同包得到 `CONSTRUCT_CREATED + FAIR_COMPARISON_RUN` | “面向动态星地 PM-16QAM 湍流与 SOP 漂移的接收可见置信度门控、尺度公平分阶段盲均衡方法。” | **HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE**。T011 只有 OpenAlex 一个实际 source family，Step 1 未完成；T012 是 `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`，Step 2/3 未启动。旧三 cost 共用 `mu=0.03` 且初始梯度约相差 19×，只能保留 raw diagnostic，不能继承机制 verdict。但 family 未 Kill，且已有 candidate-specific source identity schema、五项 recent fulltext、三篇 canonical 精确题名和公平实现骨架 | 一个全新 disk-native adapter：从 T011 archives + frozen shared index 形成 atomic-source ≥3、去重 ≥20、≥2 技术子方向、8–12 篇 priority pool；只读闭合五项 recent identity，并把三篇 canonical stage 到 worktree。主仓 promotion 另包执行；不得续改 T012 | actual source <3、pool/coverage 门失败或 canonical 3/3 staging 不闭合即返回池，不给第二个 C15 source package；Step 3 发现 JR-CMA/VAE/CMA→RDE 已占满该 M-C-A，或找不到星地 task-specific residual problem，则不进 MVE；公平 probe 不胜 tuned staged chain/cheap rule 即 Kill 该具体 contract |
| **B4 时延约束多速率双环载波恢复** | 锚论文现有 PADE 粗频偏外环 + V–V 残频/相位内环只能作 source-native baseline；唯一未闭合假设是按 receiver hardware delay/parallelism 调度环路更新率，且不得把湍流相位并入环路传函 | 当前 **`NONE`**。Q1 是源方法，Q2 PCS/符号率路线维度错位并碰撞历史 4B Kill，Q3 只有假设、没有 carrier-specific M-C-A | “面向高并行星地相干接收的时延约束多速率双环载波恢复，以慢速 PADE 外环与快速 V–V 内环协同扩展动态捕获范围并约束残频和资源代价。”该句只可作候选，不可对外声称 | **HYPOTHESIS_ONLY / MCA_BLOCKED**。源文已给双环；卫星综述的反馈时延问题属于 timing recovery，载波慢漂移反而可低速更新。合法全文/参数仍为 partial/manual-required；现有代码无 PADE 和双反馈状态机 | 一次 B4-Q3 formalization：闭合合法全文与 PADE/环路参数、找到载波专属时延问题证据、完成直接竞品 collision 与 comparator contract。即使成功仍需新建 PADE/双环基础实现 | 全文/参数不闭合、无载波专属时延证据或发现直接多速率竞品，任一即退出；禁止用 seed 修补，也不转 PCS/Rs 旧轴 |
| **B6 Z-ODPLL / atan2 鉴相器残余构造** | Q1 的逐样本 `VV四次方→MAF→atan2` 已是论文方法；Q2 单做 Z 域只是分析工具，若纳入湍流相位/多普勒环路则撞 D006；Q3 没有独立 construct | **`NONE`**。复现 atan2 是 baseline，不是我方方法；旧 D006 环路方向已经给出 0/−0.7/−2.5 dB 与强档劣化，不能换名重开 | 当前只能写源方法事实：“逐样本 atan2 鉴相器将鉴相增益与接收功率解耦并扩大时延容限。”不能写成我方贡献 | **NOT_READY / NO_POSITIVE_METHOD_CONTRACT**。2025 ODPLL 已进一步组合 Z-transform、VV/atan2、FPGA 时延和 Doppler，直接压缩“atan2 + Z-ODPLL”的残余新颖性 | 最多一次无 seed 的 source identity/residual novelty adjudication，并先修 `literature_notes.md` 中错误 DOI；公平对手至少含 source-native atan2-OPLL、匹配带宽/时延/AGC 的 sine-OPLL 与 2025 Z-ODPLL。现有仓库没有 OPLL/ODPLL 光电环路实现 | 找不到不进入 D006 红线、又未被 2023/2025 源覆盖的 residual construct，即记 `NO_LEGAL_B6_CONSTRUCT` 并退出；不得把 source reproduction 记作方法 |

关键证据：

- C15 science/task 状态分别见
  `projects/thesis-fso/direction-lab/portfolio/current.yaml`、
  `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`、
  `projects/thesis-fso/worker-logs/step-012-c15-source-recovery-and-acquire.md`
  与 science-scout `verifications.md#V006`；
- B4 锚方法见 shared main
  `D:\code\study\research-protocol\papers\doi\10.1016_j.optcom.2023.129312\content.md`
  （sha256 `ce080cd4...de9e36`）和
  `D:\code\study\research-protocol\papers\_read_notes\_B4-dual-feedback-loop-increment.md`
  （sha256 `f80c8d10...c8a5`）；
- B6 锚方法与 direct competitor 见
  `D:\code\study\research-protocol\papers\doi\10.3390_photonics10121312\content.md`
  （sha256 `f8eed543...5b61`）、
  `D:\code\study\research-protocol\papers\doi\10.1109_ICSOS66026.2025.11443174\content.md`
  （sha256 `52ec61d5...360b`）和
  `D:\code\study\research-protocol\papers\_read_notes\_B6-z-odpll-opll-increment.md`
  （sha256 `e319e009...92c2`）；
- D006 旧环路边界与 4B Kill 见
  `.sessions/2026-06-20-problem-driven-redirection/decisions.md`。
- 三项审计的可恢复摘要与完整 hash 见 `verifications.md#V041`。

### 2. 其他候选为何不补足“三个 runnable carrier”

这些候选用于证明没有被漏掉的 direct-ready 替代项，不重新打开其既有退出边界：

| candidate | formal readiness 不成立的原因 |
|---|---|
| B2 | fade-freeze + pilot fallback 三个 Go 条件均失败；同一 `h` 均衡口径下 pilot 与 blind fade-block BER 约 `0.00330 vs 0.00322`，无真实增量 |
| B3 | CPE CRB 约 0 dB；算法时间窗内 Doppler 跳变约 7 Hz、FOE 分辨率约 610 kHz，相差约五个数量级；三切口物理 FAIL |
| B5 | 六类 adaptation scan 均无足够信号，已正式关闭具体增量路线 |
| B7 | Gardner 范围优势解决的是当前星地参数域不存在的问题，不能以更大范围冒充方法增量 |
| B11-Q2 | 与既有 NDA-ML 湍流验证同轴，VV/BPS 同为 blind NDA；已裁决为伪增量 |
| B1/A4/B10/B9/B12 | 分别受第三 evaluator repair、第二 identity repair、第二 lifecycle repair、第三 Step 1 package、第二 novelty/implementation repair 的显式禁令约束 |

### 3. 为什么 T016 比 B4、B6 更可能最终产生 METHOD_SIGNAL

1. **相对 B4**：C15 已有明确正向 construct、主 comparator、cheap rule、fresh-seed
   公平性条件和可复用 2×2 FIR runner；B4-Q3 连 carrier-specific “时延为何使现有
   方法不足”的 M-C-A 都没有，而且还缺 PADE/双环基础实现。C15 的路径是
   “Step 1–2 → Step 3 → 方法包”两道已知科学门；B4 仍是“先证明问题存在”，
   方法路径与增量均未定义。
2. **相对 B6**：C15 的 generic staged adaptation 虽有 collision 风险，但 residual
   contract 尚可由 Step 3 fail-closed 裁决；B6 的 atan2、Z-transform、FPGA 时延
   与 Doppler 已被 2023/2025 直接源覆盖，且进入湍流环路会撞 D006。B6 下一包只能
   证明“没有剩余构造”，不能建立正向方法链。
3. **不预支方法产出**：T016 只关闭 formal readiness 债，预期
   `mission_method_delta=NONE`。选择它的理由是它是唯一会解除一个具体方法合同
   的上游硬门，而不是把 formalization 包装成方法。若一次性门失败，立即轮换，
   不重复 T012 或新增 evaluator repair。

### 4. T016 一次性合同边界

- action class：`CANDIDATE_FORMALIZATION`；formal active scientific carrier
  仍为 `NONE`，不运行 seed/MVE；
- Step 1：只复用 T011 七份 archive 与项目 shared index，按实际
  `source_api/source` 身份合并；必须满足去重 ≥20、actual source family ≥3、
  正式发表占比 ≥50%、必读 ≥5、覆盖 ≥2 个技术子方向，并形成 8–12 篇 acquisition
  pool。历史来源标签、空返回或重复记录不得凑源；
- Step 2 preparation：只读核对五项现有 recent fulltext 的
  title/DOI/metadata/index 和每篇 `content.md >=50` 有效行；对 Sato 1975、
  Godard 1980、Yang–Werner–Dumont 2002 各执行至多一条 exact-title IEEE
  staging，遵守 `gw-acquire.md` 止损且不写 shared main repo；
- 产出 source view、acquisition pool、identity report、staging receipts、
  preliminary coverage-gap report 和 worker log；3/3 staging PASS 时停在
  `AWAITING_CANONICAL_PROMOTION`，不请求 coverage confirmation，不精读、
  不写 Q#、不实现、不实验；
- 任一 source/canonical/coverage 硬门失败即
  `BLOCKED_FORMAL_READINESS`，C15 返回池且不再给第二个 source package。

## 结论

选择 `C15_DISK_NATIVE_FORMALIZATION_ADAPTER` 作为下一 foreground workline，
但**不激活 scientific carrier**。它是一次性 Step 1–2 证据包，不能产生
`METHOD_SIGNAL`；其价值是以最低已知成本解锁当前唯一具备具体正向方法合同、
合法比较器和可复用实现资产的候选。新 live/formal owner、T016 和独立 dispatch
review 完成前继续禁止 seed/MVE。

## 对决策的影响

- live 新建 D020，formal owner 新建 D031；
- foreground 递增到 epoch 38 / CP015 /
  `C15_FORMALIZATION_PREP`，formal active scientific carrier 保持 `NONE`；
- 新建 T016，取代而非修订 T012；T016 接收前不追加 CP016；
- T016 完成后由不同 agent 独立裁决 formal disposition、method delta、streak
  与 drift；若到达 canonical-promotion 门，另建受控 promotion package；只有
  promotion/coverage report 验收后才向用户请求极短覆盖面授权，不要求其阅读
  日志或判断科学正确性。
