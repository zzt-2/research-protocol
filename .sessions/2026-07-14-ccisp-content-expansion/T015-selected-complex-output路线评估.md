# T015：真实 selected complex-output mux 路线评估

> 任务类型：只读讨论 / 事实核查 / change contract 草拟
> 预留产出：`R013-selected-complex-output路线评估.md`
> 当前授权：DIAGNOSE + PROPOSE；禁止进入实现与实验

## 目标

评估“实现真实 selected complex-output mux”到底能带来什么、当前实现距离它有多远，以及最低限度需要改什么、重验什么。核心不是替既定方向背书，而是区分：

1. 只修复论文与 Fig.2 的 selected-output 实现真实性；
2. 形成真正由控制器选择输出分支的 adaptive CPR receiver；
3. 形成不依赖发送比特消歧、可在线部署的 adaptive CPR algorithm。

最终给出可供主线程拍板的三档路线和一个不过度声称的 change contract 草案，不修改任何工程文件。

## 工作目录与必读

- 工作目录：`D:\code\study\research-protocol`
- 论文工程：`D:\code\study\research-protocol\projects\simulation\paper\ccisp2026`
- 先完整读取根目录 `AGENTS.md`。
- 使用 `session-governance`，续接 `.sessions/2026-07-14-ccisp-content-expansion`，不得另建专题。
- 使用 `paper-writing` 审查“论文声称—算法对象—实现—指标”是否闭合。
- 读取 `sim-preflight`，但本任务只做路线评估；它不得被用来绕过 Groundwork/Contract 门控或授权开跑。
- 必读专题文件：`topic-index.md`、`decisions.md` 中 D014/D015、`verifications.md` 中 V010、`R011-selected-output实现真实性追踪.md`、`voice.md`。
- 必读实现与资产：权威 common-768 评估脚本 `_a4_switch_common768_30seed.py` 及其权威 JSON（先确定 exact path）、`projects/simulation/common/_recovery.py`、`projects/simulation/common/_modulation.py`、`projects/simulation/paper/ccisp2026/sections/method.tex`、Fig.2 权威 draw.io 源及论文内图题/引用。

## 硬边界

- 只读。禁止修改论文、图片、Skill、仿真代码、参数、数据和 JSON。
- 禁止运行新仿真，禁止借本任务调阈值、参数、分支算法或场景。
- 禁止把“两个分支都能返回复数序列”当成“已实现输出 mux”。
- 禁止承诺 BER 增益。若只把既有逐窗 error-count mux 改写成同判决的复数序列 mux，在确定性 hard demod 与同一消歧规则下，预期应是 BER bit-exact，而不是更优。
- 禁止把仍然计算两条分支的后处理 mux 宣称为计算量降低。
- 禁止把使用 `tx_bits` 的事后 M-APSK 相位模糊消解称为可部署的在线接收输出。
- 禁止称为“新估计器”；需要判断它最多能否支撑 D014 的 adaptive CPR scheme/method，以及何种实现深度才接近导师所说的“估计算法”。
- 所有结论必须给出 exact `file:line`；grep 只能生成候选，必须读上下文。

## 必须独立核验的当前事实

不要照抄 R011。至少独立验证以下三项，并记录 caller → callee → returned object → metric/use site：

1. DA/NDA recovery 函数实际返回哪些对象，复数输出和相位估计是否存在。
2. 权威 common-768 caller 是否先计算两条分支、是否丢弃 `phi_est`、selector 在何时决策、最终 mux 的对象到底是复数序列、bits、还是 error counts。
3. NDA 的八重相位模糊如何处理，是否读取 `tx_bits`，该读取发生在选路前后何处。
4. Fig.2 与 `method.tex` 当前声称的 selected phase / phase compensation / common downstream output 到底强于实现的哪一层。

若 R011 与当前文件不一致，以当前权威文件为准，并报告漂移，不得静默沿用旧结论。

## 三层定义必须分开

### A. 指标等价的 post-hoc complex-output mux

- 两个 CPR 分支照常全部运行；
- selector 仍按当前窗口判决；
- 在统一 demod 前选择已恢复的复数序列；
- 仍可沿用当前仅供离线 BER 评估的 `tx_bits` 消歧。

判断它是否只修复“selected sequence 真实存在”，以及为什么通常不改变当前 common-768 BER、不节省分支计算。

### B. 功能性 branch-routed adaptive CPR receiver

- 控制器先决定分支；
- 每个窗口只执行被选 CPR 分支并输出统一复数序列；
- 明确 control feature、判决时点、状态重置、均衡输入、分支状态与 downstream demod 接口；
- 离线评估可以暂时保留 genie-aided ambiguity resolution，但必须显式标注不可部署边界。

判断它是否比 A 更能支撑 adaptive CPR algorithm/method 身份，是否可能降低分支计算，以及结果等价需要哪些前提。

### C. 可部署的 online adaptive CPR algorithm

- 分支选择与相位模糊消解都不读取发送比特；
- 给出 online ambiguity resolver / differential or coded aid / state mechanism 所需的最小研究问题，而不是凭空指定方案；
- 判断这是否已构成新增算法、需要 Groundwork/Contract、新 baseline 和新实验，而非普通实现修复。

## 必答问题

1. 当前到底“有什么”和“缺什么”？用 truth table 对齐论文声称、Fig.2、caller、callee、输出对象、metric。
2. A/B/C 各自能新增哪些可证明能力：论文定位与 Fig.2 真实性、BER、计算量、EVM/LLR/FEC/burst/sequence-level analysis、在线可部署性。
3. 哪些效果只是表达/接口闭环，哪些是算法能力，哪些必须靠新结果证明？
4. 每条路线涉及哪些 exact files/functions/interfaces；只列 delta，不写代码。
5. A 是否只是审计性修复，仍不足以回答导师“应该是估计算法”？B 为什么可能更接近，但仍不能自动证明算法贡献？C 为什么可能超出当前投稿修复范围？
6. 当前任务属于 implementation repair 还是 new algorithm scope？分别触发哪些 session、Groundwork/Contract、sim-preflight 门控？
7. 在 7 页且用户要求精炼的背景下，哪条路线的论文叙事收益足以覆盖新增解释与验证成本？不得用增加篇幅作为默认收益。

## 预注册验证预测

- A：在现有 common-768 全部权威 case/seed/window 上，selected complex sequence 经同一 ambiguity resolution 与 hard demod 后的逐窗 errors，应与当前 error-count mux**零不一致**；selector counts 和两条 fixed-branch 结果保持不变。
- A 若出现 BER 改善或不一致：优先视为实现错误、消歧时点变化、指标变化或数据对齐错误，不能直接写成算法增益。
- B：先给出在何种数据依赖和状态条件下应与 A 等价；若控制输入依赖尚未执行的分支输出，则“先选后跑”不可直接成立。
- C：未闭合 non-genie ambiguity resolver 前，deployable selected output 必须判 BLOCKED；不得用 post-hoc `tx_bits` 结果代替。
- 所有路线：没有 fresh rerun 与独立 verifier 前，禁止形成新的数字或性能声称。

还要列出负例：未经消歧的 NDA raw complex output 不应被错误要求与已消歧 BER 完全等价；hard-BER 等价不得外推为 EVM/LLR/FEC 等价。

## 交付结构

将结果写入 `.sessions/2026-07-14-ccisp-content-expansion/R013-selected-complex-output路线评估.md`，使用 research note 必备锚点，并至少包含：

1. 已核验当前真相表（含 exact `file:line`）
2. A/B/C 定义与边界
3. 效果矩阵：真实性、BER、计算量、新指标、可部署性、对 adaptive CPR 定位的支撑强度
4. 分路线实现 delta（文件/函数/接口级，不写代码）
5. ambiguity-resolution 决策树
6. 预注册验证计划、PASS/BLOCKED 标准与反例
7. 范围、证据、工期/运行成本风险；无法从项目事实量化的项目不得编数字
8. 三档建议：保守、推荐、激进；说明为什么，也说明为什么不选另外两档
9. 下一轮可执行 change contract 草案；必须标 `DRAFT / NOT APPROVED`
10. 最终 `PASS / PARTIAL / BLOCKED`：分别评价当前事实闭合、路线可决策性、可实现性、可部署性，以及仍需用户拍板/导师澄清的事项

## 验收标准

- [ ] 独立核验不少于 3 条关键事实，均有 exact `file:line`
- [ ] A/B/C 没有混称，genie-aided 与 deployable 没有混称
- [ ] 明确写出 A 的默认预测是 BER 不变，而非增益
- [ ] 没有把“双分支仍全跑”写成计算节省
- [ ] 给出可执行、可否决且不过拟合的验证合同
- [ ] 没有修改任何非 `.sessions` 文件，没有运行仿真
- [ ] 未经用户批准，不得进入代码、论文、图或数据 WRITE

