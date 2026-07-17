# Topic Index: Direction Lab 可遵守性与控制器试运行

> 状态: active（2026-07-17 建立） | 创建: 2026-07-17 | 最后更新: 2026-07-17

## 专题信息

- **slug**: 2026-07-17-direction-lab-governance-pilot
- **性质**: 框架试运行 / 可遵守性观察，不是正式研究方向

## 范围边界

- **原始目标**：观察 AI 在真实 Direction Lab 推进中如何失守规则，并确定哪些约束应由脚本、状态机或人工判断承担。
- **当前范围**：在双偏振星地 OSL 真实地基上建立完整 ML Candidate Universe、CandidateMap 与 BatchQueue；门控通过后运行一个受控的小型 paired batch，同时继续测试状态、manifest、证据等级、失败退出、代码 provenance、stale 传播和恢复能力。
- **明确不含**：不产出论文结论；不把 pilot 结果当研究结果；不大规模重构现有仿真代码；不创建正式 skill；不替代 `framework-evolution` 的协议设计。
- **范围变更记录**：2026-07-17，D004：由纯治理 shadow pilot 扩展为真实地基 sandbox 候选运行；原因是用户显式要求把 pilot v1 用到真实研究地基并跑完第一批。正式 Groundwork/论文晋级仍明确不含。

## 不变量

- pilot 的治理目标继续有效；真实候选仅作为 sandbox 载荷，候选结果不得自动晋级正式 Groundwork 或论文材料。
- 所有运行必须有 `run_id` 和 manifest；无 manifest 的行为只能标记为观察记录。
- pilot 期间发现的违规不得静默修复，必须保留原始违规、拦截点和修复方式。
- 不因 AI 偶然遵守一次就判定规则有效，必须观察重复轮次和恢复场景。

## 已确认结论

### 不变量

- Direction Lab 的生产 schema 先在 pilot 中压测，再决定实现范围。

### 其他结论

- 暂定采用三层控制：脚本硬门、状态机门、AI 判断门。
- 暂定将“违规成本”和“规则复杂度”同时记录，避免只靠增加规则解决问题。

## 进展线索

- **S001**：试运行目标、观察矩阵和退出条件（本专题首 session）。
- **H001**：新对话启动交接，冻结首轮范围为 sandbox 选择、3-5 个最小硬门、RED 压力测试和独立验证。
- **H002**：第二阶段改为一个主对话连续运行；实现 receipt/evidence gate 后依次完成正常、诱惑、stale/绕过和无历史上下文恢复四轮测试。
- **H003**：冻结提交 `44adff7` 的 pilot v1，进入 5 个真实 shadow 工作循环或一个完整候选批次的单主对话观察期；观察结束后分析完整对话历史。
- **H004**：将 pilot v1 接到双偏振星地 OSL Groundwork 真实地基，先导入 anchor/CandidateMap/BatchQueue，再启动第一批小型 paired batch。
- **D003/H004 修正**：地基是场景、baseline、证据和死路的约束源，不是 ML 候选边界；真实运行先枚举完整处理链的 ML Candidate Universe，再统一排序和批跑。
- **D004/S004**：用户显式批准 scope change；本专题进入真实地基 sandbox 批次，但正式 Groundwork/论文晋级继续阻断。
- **S002**：收 H002 核验、receipt/evidence gate 最小设计、TDD 计划与四轮压力测试过程记录。
- **S003**：完成 5 个真实 shadow 工作循环；核心行为/P0 隔离 PASS，恢复阈值未覆盖，整体 PARTIAL。
- **D001**：选择审计账本背书的最小 receipt/evidence gate；签名与不可变存储留作债务。
- **D002**：execute 结果必须有 execution audit/result hash，并防止同一 receipt replay。
- **V004/V005**：独立 verifier 先发现 result provenance/replay 漏口；修复后 34 tests 与黑盒复核通过，Round 4 hash provenance 仍为 PARTIAL。
- **V001**：B5 隔离输入的首版控制器 RED/GREEN 与独立 verifier PASS（9 tests）。
- **V002**：独立黑盒复核发现 PROMOTE 证据缺失、未知动作和 baseline stale 处理等漏口；结论 PARTIAL，暂不扩展 schema。
- **V003**：修复最小硬门并由独立 verifier 复核，22 tests PASS；manifest 签名/来源绑定列为正式 schema 阶段债务。
- **S004**：完成真实地基的全景 Candidate Universe、CandidateMap、BatchQueue 与 B001 首批 paired batch；范围保持 sandbox-only。
- **V007**：B001 controller/EvidenceGate/source closure/指标泄漏审计及独立 verifier 均 PASS；监督式线性/MLP 仅作机制级 `ADVANCE_SPECIFIC`，AE 为 `RETIRE_SPECIFIC`，未晋级正式研究或论文。

## 未决项

- pilot 使用哪个已有小批次作为沙盒输入；（已定 B5）
- 首批强制脚本的最小集合；（已定 5 个硬门）
- 观察窗口和违规收敛阈值；
- pilot 结束后由谁独立复核。

## 当前位置

首轮压力测试核心行为经 V004/V005 复核为 PASS；S003/V006 已完成 5 个真实 shadow 循环，整体保持 PARTIAL。S004/V007 已完成真实地基全景扫描与 B001 首批 paired batch；B001 仅在精确预注册域内形成机制级观察，formal Groundwork/Step 4a/论文晋级仍阻断。
