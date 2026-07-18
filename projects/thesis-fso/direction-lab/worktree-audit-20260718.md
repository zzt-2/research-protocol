# Direction Lab worktree audit — 2026-07-18

> 只读快照；命令：`git status --porcelain=v1 -uall`。本文件不判定所有权，也不授权清理、恢复、暂存或提交。

## 总览

- dirty 文件级条目：1538
- tracked modified：141
- tracked deleted：62
- untracked：1335
- B001/B002/B003 批次目录：无 dirty 条目
- B004：不存在

为避免重复计数，下表按“Direction Lab → 生成物/artifact → thesis-fso 其他 → 其他项目 → 用户工作/配置 → 来源不明”的优先级分类。分类依据仅是路径和扩展名，因此“用户工作”和“来源不明”不能被解释为可清理项。

| 类别 | 数量 | 说明 |
|---|---:|---|
| Direction Lab 本轮相关 | 78 | `direction-lab/` 与 governance pilot 专题 |
| thesis-fso 其他 | 5 | thesis-fso 中不属于 Direction Lab 的文件 |
| 其他项目 | 124 | 其他 `projects/` 内容，排除已识别生成物 |
| 生成物 / artifact | 659 | `tmp`、artifact/results/figures、常见二进制或结果扩展名 |
| 用户工作 / 配置 | 363 | 其他 session、文档、代码与配置；不得擅自处理 |
| 来源无法判断 | 309 | 无法仅凭路径可靠归属 |

已存在的可读生成文件约 568 个、约 202.60 MiB。较大的例子包括 `tmp/pdfs/b2/B2-01.pdf`（5.80 MiB）、`pdf_toc.pdf`（4.78 MiB）和仿真图像预览（单文件约 3.29 MiB）。这些内容不宜批量进入 Git；P03 smoke artifact 虽然体积小，也应按隔离产物处理，不能整目录盲目暂存。

## Direction Lab 未提交内容

当前相关 dirty 条目由两部分组成：Direction Lab 项目目录 64 条、governance pilot 专题 14 条。

若把入口桥接文件 `projects-overview.md`、`projects/thesis-fso/master-state.md` 和共享 `.sessions/_registry.yaml`、`.sessions/profile.md` 一并算入“控制面相关”，提交后宽口径为 81 条；本报告主表采用严格目录口径 78 条，四个桥接/共享文件中 `projects-overview.md` 已在本轮安全提交，其余三个在并行风险中单列。

- 已跟踪且有修改的控制面文件包括 `README.md`、`process.md`、`implementation-plan.md`、`canonical-state.yaml`、`failure-registry.yaml`、`master-state.md`、governance pilot 的索引/决策/验证/voice，以及全局 session registry/profile。
- 未跟踪内容包括 Candidate Universe/Map/Queue/Registry 快照、P01/P02/P03 Scout 文件、state projection/reducer、测试与工具，以及 governance pilot 的 H001、S005–S010、T001–T002。
- P03 `interface-smoke-v1` 是被取代的历史 smoke；`interface-smoke-v2` 是当前接口验证产物。两者都不是论文证据，也不应当作正式性能结果提交。

## 并行修改风险

- `master-state.md`、Direction Lab 入口文件和 governance pilot 聚合文件在本轮开始前已经 dirty；整文件暂存可能混入此前或并行对话的修改。
- 多个 untracked Candidate/Queue/Registry/Scout 文件形成相互引用的控制面集合；只提交其中一部分可能制造悬空指针。
- `.sessions/_registry.yaml` 与 `.sessions/profile.md` 是跨专题共享文件，存在最高的并行对话冲突风险。
- `projects/simulation/`、`tmp/`、其他 session 和其他项目均不在本轮授权范围内。

因此本轮不执行 `restore`、`reset`、删除、批量 stage 或批量提交。若要提交，应先在独立、干净的边界内逐文件确认差异所有权和引用闭包。

## 可复现审计

```powershell
git status --porcelain=v1 -uall
git status --short --untracked-files=all -- projects/thesis-fso/direction-lab projects/thesis-fso/master-state.md projects-overview.md .sessions/2026-07-17-direction-lab-governance-pilot .sessions/_registry.yaml .sessions/profile.md
git status --short -- projects/thesis-fso/direction-lab/batches/B001* projects/thesis-fso/direction-lab/batches/B002* projects/thesis-fso/direction-lab/batches/B003*
Test-Path projects/thesis-fso/direction-lab/batches/B004*
```
