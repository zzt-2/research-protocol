# [T034] 全面补强 P11 少导频 Complex-LS Butterfly FIR

> 来源: S025 / D036 | 独立 Codex task | 日期: 2026-08-13

## 0. 唯一目标

只补强 P11：用分布式少量 pilots 对 2×2、11-tap Butterfly FIR 的四组复系数做 complex least-squares 标定，并相对高标签成本的 supervised equalizer 展示净有效载荷/训练开销优势。把它补成证据全面、命名诚实的硕士方法章候选；做不成就明确降级，不换题。

## 1. 必读与启动

1. 读取 `AGENTS.md`、`sim-preflight/SKILL.md` 及其恢复、运行、约束、参数真相源、MVE/对照验证、文档纪律和使用日志子文件。
2. 读取本专题 `topic-index.md` 的不变量、D030/D032/D034–D036、V014–V015、R026、T029，以及两个 P11 重复执行记录和所有 P11 原代码/结果/worker logs。
3. 冻结事实：此前两个对话都没有运行实验；那不是科学 FAIL。先验证 authority、true-SNR 注入、shared realization 和评分口径，再预注册。
4. clean baseline 或 preflight 不通过时先报告，不带病运行。

## 2. 必须补齐

- **真相修复**：确认 SNR/gamma 真正进入信号链；评分改为 X/Y 双偏振、payload-only BER，并明确 training/pilot positions 的排除规则。
- **正式对照**：至少保留正确实现的高标签 supervised Butterfly baseline；同一 shared realization、相同接收帧、相同 tap/延迟与公平训练预算。普通 LS/RLS/CMA 只在它们回答同一命题且实现已可靠时作为辅助，不把强邻居变成准入门。
- **覆盖度**：从既有 20 dB 单点扩为小 SNR 邻域；扫描有解释力的 pilot fraction，至少包含原 1% 与高标签基准；使用 paired fresh seeds、双偏振统计和 CI。
- **归因**：分别报告 BER、pilot-adjusted goodput、失配/条件数、系数估计稳定性；用最小消融确认增益来自 complex 2×2 sparse-pilot calibration 和训练开销差，而不是计分位置、单偏振挑选或 SNR 注入错误。
- **代价**：给求解复杂度、矩阵尺寸、训练开销、推理数据流、运行时间和适用的块静态/跟踪边界。
- **碰撞检查**：冻结实际 recipe 后，仅检索“2×2 Butterfly complex-LS + distributed sparse pilots + 目标 FSO 场景 + goodput/label-budget 比较”的完全重复。全文精读和 web 检索必须委托 subagent；不泛搜新 estimator。有限检索不得写“证明首次”。
- **章级产物**：给准确章标题、问题定义、框图、方程/伪代码、3–5 小节、主图/主表、三条有限贡献、限制和 claim ceiling。

## 3. 禁止

- 不补开放式 P11 Groundwork，不转向新 estimator/新候选，不修改 Skill/controller/正式论文正文。
- 不因 LS 经典、CMA 可能更强或 BER 差 CI 跨零自动否决；P11 的主要改善可落在训练开销与 goodput，但数字必须按合法口径重算。
- 不声称新 LS/CNN、online tracking、跨 SNR 普适领先，或把 X-only 旧分数继续冒充双偏振结论。
- 不修改主专题聚合文件。

## 4. 停机与交付

最多两轮主实验循环。若修复真相后 1% pilot 的双偏振 payload-only BER/goodput 命题不成立，或改善由 scoring artifact 产生，停止并降级；不得靠不断调 pilot/SNR 追正。

唯一报告：`projects/thesis-fso/direction-lab/harvest/p11-sparse-pilot-butterfly-ls-thesis-grade-strengthening.md`。
唯一 handoff：`.sessions/2026-07-09-thesis-writing/H018-p11-sparse-pilot-ls-strengthening.md`。
完成后做独立 verifier 审查，单次统一 commit，不 push、不合并；最终回复给出结论、关键数字、证据路径、commit 和未解决债务。
