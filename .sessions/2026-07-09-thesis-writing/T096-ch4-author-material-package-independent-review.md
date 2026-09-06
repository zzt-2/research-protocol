# Task Brief: Ch4 作者素材包独立终审

> 来源: S028 / D072 / V046–V047 / T095 | 产出: 作者可组织材料包的独立终验
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 34
  action_class: INDEPENDENT_MATERIAL_PACKAGE_REVIEW
  mission_checkpoint: CP034
```
<!-- RDL-TASK-CONTROL:END -->

## 前置条件与边界

只在 T095 terminal=`CH4_AUTHOR_MATERIAL_CARDS_READY_FOR_REVIEW` 后执行。全程只读，不修改文件，不运行仿真/reducer/bootstrap，不检索或下载文献，不写连续章节正文。

## 唯一任务

独立判断 T095 后的材料包能否让作者在不阅读内部 gate/SHA/task 历史的情况下，正确找到并组织 Ch4 的方法、数字、图表、边界和跨章接口；同时确认没有把旧 confirmation 口径、内部研究语言或未验证主张带回作者入口。

## 必查

1. **数字**：抽取所有材料中的 BER、required SNR、gain、CI、Np、SNR、tau、delta 与样本规模；逐项对照已通过 T094 的 formal CSV/aggregate。任何承重数字不一致为 P1。
2. **方法身份**：共同 `Q=UV^H`、Frobenius 尺度、pilot-reconstruction 尺度、B2 tuned floor、B0 LS、O1 truth-only 的输入—动作—输出和角色是否准确；B3 不得被写成固定尺度 1，C4 不得声称优于 B3。
3. **主张边界**：Np4 只能是统计稳定的小幅优势；`delta` 不是 PDL dB；Ch3 是下游模块接口且未联合验证；无 PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC 全链结论。
4. **作者可用性**：README 和 `author-material-index.md` 是否可作为双入口；4.1–4.7 是否各有事实、公式、图表、解释顺序、披露和禁写项；旧 14/18 dB 资产是否清楚标为 historical。
5. **形态边界**：材料应为卡片、表格、公式、清单与短说明，不得形成可冒充完整 4.x 章节的连续正文；不得出现 Grade、gate、SHA、P0/P1、D/T/CP、内部 arm code 作为作者叙事。
6. **引用**：只核仓库已有来源与证据层级；摘要级来源不得承重 exact formula，“经典迁移”不得被抬成首次或 SOTA。
7. **图件**：fresh 运行两个绘图脚本 check-only、方法图生成与 py_compile；视觉查看更新后的 BER、robustness 和 method-flow PNG，检查裁切、重叠、单位、线型、模块接口和“未联合验证”。验证 SVG 可解析、PNG 非空、重复生成 hash 稳定。
8. **科学冻结**：raw/aggregate/receipt/manifest/execution-lock hashes 与 V046 exact；确认没有新增 simulation raw/tmp/checkpoint 或改科学 artifacts。
9. **清理**：T094 三项 P2 已收口，两个精确 `__pycache__` 不再存在；不把仓库其他无关脏文件归责 T095。

## 输出

返回：检查命令、材料覆盖矩阵、数字/方法/引用/视觉结论、P0/P1/P2、是否可标记作者材料包 ready。成功 terminal=`CH4_AUTHOR_MATERIAL_PACKAGE_PASS`；任一数字、方法身份、claim ceiling、作者误用风险为 P1 并 terminal=`CH4_AUTHOR_MATERIAL_PACKAGE_FAIL`。

