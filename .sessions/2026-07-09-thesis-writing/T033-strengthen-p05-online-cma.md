# [T033] 全面补强 P05 固定流标签在线 CMA 均衡

> 来源: S025 / D036 | 独立 Codex task | 日期: 2026-08-13

## 0. 唯一目标

只补强 P05：在强 Gamma-Gamma 湍流与偏振扰动下，以从原始双偏振接收信号独立运行的标准 Godard-with-z CMA，替换 frozen supervised Butterfly equalizer，并以固定流标签 BER/失配率衡量输出身份连续性。把它补成证据全面、命名诚实的硕士方法章候选；做不成就明确降级，不换题。

## 1. 必读与启动

1. 读取 `AGENTS.md`、`sim-preflight/SKILL.md` 及其恢复、运行、约束、参数真相源、MVE/对照验证、文档纪律和使用日志子文件。
2. 读取本专题 `topic-index.md` 的不变量、D032/D034–D036、R026、T030，以及 P05 原代码、结果和 worker logs。
3. 先核对 git/worktree 隔离与 clean baseline；未通过 preflight 不运行。
4. 把冻结假设、指标、场景网格、seeds、PASS/STOP 判据写入方法专属预注册文件后再跑。

## 2. 必须补齐

- **真相修复**：彻底移除 `continued Butterfly` 错名；确认 CMA 没有加载 Butterfly 权重。核清 15/20 epoch、Phase A/B seed 复用和 `mean_pi` 字段误名。
- **正式对照**：同一 shared realization 下比较 frozen supervised Butterfly 与 online CMA；不得故意降低 baseline 训练质量。固定流 BER 为主，PI-BER、swap/identity-loss rate 为辅助。
- **覆盖度**：至少覆盖既有 `f_G=30/100`，并把 20 dB 单点扩成一个小 SNR 邻域；采用 paired fresh seeds 和可复算 CI。若计算预算不允许全矩阵，先保两端 f_G，再给出预注册的最小三点 SNR 扫描。
- **归因**：给收敛曲线、输出置换/相位处理、初始化与状态 reset 审计；做最小必要消融，解释优势来自在线 blind adaptation 与固定标签目标，而不是计分或重置 artifact。
- **代价**：报告每 symbol/block 运算、迭代/收敛长度、运行时间和训练数据需求。
- **碰撞检查**：冻结实际 recipe 后，仅检索“强湍流/偏振扰动 FSO + fixed-stream-label + independent online CMA replacement”的完全重复。全文精读和 web 检索必须委托 subagent；不泛搜新方法。有限检索不得写“证明首次”。
- **章级产物**：给准确章标题、问题定义、框图、方程/伪代码、3–5 小节、主图/主表、三条有限贡献、限制和 claim ceiling。

## 3. 禁止

- 不另造 CMA 变体，不转向 P11/CPR/decoder，不启动新候选 Groundwork。
- 不以“CMA 经典”“存在更强盲均衡器”否决；也不需要穷举廉价替代。
- 不修改 Skill、controller、正式论文正文或主专题聚合文件。
- 不把 fixed-label 优势写成 PI-BER 全面优势，不声称新的 CMA 原子或数学 label-lock 保证。

## 4. 停机与交付

最多两轮主实验循环。若清洁正式确认中 fixed-label 改善方向不能复现，或优势来自 artifact/不公平 baseline，停止并降级为分析/基线章节资产，不调参追正。

唯一报告：`projects/thesis-fso/direction-lab/harvest/p05-online-cma-thesis-grade-strengthening.md`。
唯一 handoff：`.sessions/2026-07-09-thesis-writing/H017-p05-online-cma-strengthening.md`。
完成后做独立 verifier 审查，单次统一 commit，不 push、不合并；最终回复给出结论、关键数字、证据路径、commit 和未解决债务。
