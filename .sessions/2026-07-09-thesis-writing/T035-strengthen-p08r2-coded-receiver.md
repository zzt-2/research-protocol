# [T035] 全面补强 P08-R2 编码 FSO 接收方法

> 来源: S025 / D036 | 独立 Codex task | 日期: 2026-08-13

## 0. 唯一目标

只补强 P08-R2：在 receiver-visible prefix residual calibration、MMSE/LLR 前端的共同链路上，为目标 operating point 冻结 normalized/offset min-sum decoder 配置，并相对正确 B0 receiver 展示 FER 改善。把它补成证据全面、命名诚实的硕士方法章候选；做不成就明确降级，不换题。

## 1. 必读与启动

1. 读取 `AGENTS.md`、`sim-preflight/SKILL.md` 及其恢复、运行、约束、参数真相源、MVE/对照验证、文档纪律和使用日志子文件。
2. 读取本专题 `topic-index.md` 的不变量、D032/D034–D036、R026、T031，以及 P08-R2 原代码、chronology、结果和 worker logs。
3. 冻结事实：B0 已含 32-symbol prefix calibration；B2 相对 B0 的实际 delta 是 decoder alpha/offset 配置；clip=20 被共同 `llr_max=20` 吸收；O2 只作 oracle。
4. 先预注册 corrected/pristine confirmation 的场景、paired trajectories、指标和停止判据；不得用旧 chronology 冒充新确认。

## 2. 必须补齐

- **真相修复**：逐调用链冻结 receiver-visible information、metric signature、state lifecycle；确认 hidden gamma 不进入 B2；不得声称相同 X/Y prefix 可完整识别 2×2 channel。
- **正式对照**：B0 与 B2 共享 prefix calibration/MMSE/LLR 前缀，只比较冻结 decoder 配置；O2 显式标 oracle，不作可部署 baseline。
- **覆盖度**：以既有 weak/1000 Hz/12 dB 为中心扩成小 SNR 邻域；使用足以观察 FER 差异的 paired trajectories，并报告 gain/tie/loss、CI、pre-FEC 与 post-FEC/FER 口径。
- **归因**：至少分离 alpha-only、offset-only、clip-only 与 full frozen configuration；如果 clip 仍被共同上限吸收，明确记为无独立贡献。参数必须先在开发集冻结，再在独立确认集评估。
- **代价**：报告 decoder iterations、每码字额外运算、存储、运行时间，以及 prefix overhead 与可部署信息边界。
- **碰撞检查**：冻结实际 recipe 后，仅检索“目标 FSO operating point + receiver-visible prefix calibration + frozen normalized/offset min-sum configuration”的完全重复。全文精读和 web 检索必须委托 subagent；不泛搜新编码方向。有限检索不得写“证明首次”。
- **章级产物**：给准确章标题、问题定义、框图、方程/伪代码、3–5 小节、主图/主表、三条有限贡献、限制和 claim ceiling。

## 3. 禁止

- 不把 prefix calibration 归到 B2 新贡献，不把 oracle truth 写成 receiver-visible，不把 clip=20 重复计功。
- 不因增益小于旧 MDE、动作含参数 tuning 或只在局部 operating point 有效而自动否决。
- 不转向新编码/新候选，不修改 Skill/controller/正式论文正文或主专题聚合文件。

## 4. 停机与交付

最多两轮主实验循环。若 pristine confirmation 中 B2 对 B0 的 paired FER 改善方向不能复现，或开发/确认泄漏、hidden truth、共享前缀误归因导致现有命题消失，停止并降级，不继续搜索 alpha/offset 追正。

唯一报告：`projects/thesis-fso/direction-lab/harvest/p08r2-coded-receiver-thesis-grade-strengthening.md`。
唯一 handoff：`.sessions/2026-07-09-thesis-writing/H019-p08r2-coded-receiver-strengthening.md`。
完成后做独立 verifier 审查，单次统一 commit，不 push、不合并；最终回复给出结论、关键数字、证据路径、commit 和未解决债务。
