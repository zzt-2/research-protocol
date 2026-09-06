# Task Brief: Ch4 作者可组织材料卡闭合

> 来源: S028 / D072 / V046 / T092 / T094 | 产出: 可由作者自行取用和组合的第四章正式材料卡
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 34
  action_class: CH4_AUTHOR_MATERIAL_CARDS_AND_INDEX
  mission_checkpoint: CP034
```
<!-- RDL-TASK-CONTROL:END -->

## 前置条件

仅在 T094 terminal=`CH4_FORMAL_MATERIALS_AUDIT_PASS` 后执行。若 T094 有 P0/P1，停止本任务并回报主线程；不得自行修改科学数据、仿真程序或冻结口径。

## 唯一任务

把已通过独立核数的 Ch4 formal 结果整理成作者可逐项取用的素材库。允许重写既有旧 confirmation 写作材料，但**禁止生成连续章节正文**，禁止改论文总纲、论文正文、科学 artifacts、Skill/controller，禁止运行仿真、reducer、bootstrap 或文献检索。

## 必做产物

1. 重写 `fact-matrix.md`：以 canonical formal raw/aggregate、V046 和 T094 为唯一数字 authority；每条事实含证据指针、图表入口、可写结论、必须披露与禁止外推。
2. 重写 `algorithm-box.md`：给出共同方向估计和两种尺度判据；明确 B3 的 `tau=1` 只形成基准逆矩阵，随后按每个观测闭式标定；明确 B2 在 moderate/Np2 为 `tau=0.5`、其他 formal slice 为 `tau=1`。
3. 重写 `claim-and-citation-ledger.md`：formal 可写主张、必须披露、禁止主张、现有本地引用入口及证据层级。只使用仓库已有来源，不补论文。
4. 重写 `chapter-blueprint.md` 为“材料地图/组织清单”：4.1–4.7 每节仅列问题、可写事实、公式、图表入口、解释顺序、必须披露、禁止外推；不得写成连续段落。
5. 新建 `author-material-index.md`：作者总入口，按“方法身份、数学推导、配置、结果、机理、边界、跨章接口、答辩准备”索引所有可用材料，并标记旧 confirmation 资产为历史材料。
6. 新建 `reviewer-question-bank.md`：至少 10 个最可能的导师/评阅人问题，每题只给证据答案要点和材料指针，不写答辩稿。
7. 更新 `method-figure-semantic-brief.md` 与 `generate_method_figure.py`，重生成 `figures/ch4-method-flow.{svg,png}`：共同 `Q=UV^H` 方向分支、Frobenius 尺度主变体、pilot-reconstruction 尺度强变体、B2 独立 baseline、两路输出到 Ch3 CPR 的模块接口；图内明确“未联合验证”。
8. 新建 `thesis-spine-integration-notes.md`：只记录 Ch3/Ch4 的共同母模型、允许不同的章节抽象、物理处理顺序、不得声称联合 BER，以及旧 `thesis-framework.md` 的失效项；不得修改总纲。
9. 更新 `README.md`：将正式素材入口置顶，区分 formal / historical / internal-verification，避免作者误取旧四格、旧全局 `tau=1` 或内部 SHA/gate 语言。
10. 收掉 T094 的三项 P2：BER 图纵轴上限由 0.3 放宽到约 0.4；robustness 图将“同条件配对”限定为“各场景内同条件比较”；删除 scientific evidence 目录中已精确定位的根级与 `tests/` 下两个 `__pycache__`，不得扩大删除范围。

## 冻结科学口径

- 方法族：结构约束方向—尺度解耦短导频偏振解复用。
- 主变体：Frobenius 尺度；强变体/消融：pilot reconstruction 尺度；不得声称主变体优于强变体。
- primary comparator：独立 development split 调参的 singular-value-floor baseline；moderate/Np2 `tau=0.5`，其余正式 scene×Np `tau=1`。
- 工程 BER `3.8e-3`：Np2 gain `0.8705 dB`，95% CI `[0.6182,1.0883]`；Np4 gain `0.1209 dB`，CI `[0.0189,0.2392]`。Np4 只能称“统计稳定的小幅优势”。
- Ch4 输出为 post-demux / pre-CPR、uncoded pre-FEC symbols；Ch3 仅为模块接口，未验证联合运行。
- 非酉扫描的 `delta` 只称结构失配强度，不称 PDL dB；`delta>=0.1` 的反转必须保留为边界。
- O1 是 truth-only 理论参考，不是可部署 baseline。
- 内部 C4/B2/B3 编码、Grade、gate、SHA、任务号不得进入作者主入口；可留在 provenance/verification 文件。

## 完成自检

- 所有 formal 数字与已审 CSV/aggregate exact；旧 14/18 dB 四格不再承担正式结论。
- 作者只读 README + author-material-index 即能找到每个未来小节所需事实、公式、图、表和边界。
- 所有材料保持卡片、表格、要点或公式形态；不得出现可直接冒充完整 4.x 正文的连续长段落。
- 方法图 PNG/SVG 无截断、无重叠，黑白可区分；运行 py_compile 和图件确定性检查。
- 交付时列出改动文件、命令、P0/P1/P2 和 terminal=`CH4_AUTHOR_MATERIAL_CARDS_READY_FOR_REVIEW`。
