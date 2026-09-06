# Task Brief: Ch4 formal 图表材料独立审查

> 来源: S028 / D072 / V046 / T092 | 产出: T092 图表/表格/CSV 的独立核数与专业性审查
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

## 唯一任务

以只读方式独立审查 T092 生成的五份 CSV、五组 formal 结果图、三张候选表、README、提取/绘图脚本和 verification。不得复用实现者结论自证，不得修改任何文件。发现问题只报告给主线程，由主线程另派最小修复。

## 独立数字复核

1. 不导入 `extract_ch4_formal_plot_data.py` 或 `plot_ch4_formal_results.py`；直接读取 immutable raw/aggregate。
2. 重算并逐行核对：
   - BER curve CSV 的全部 `(scene,Np,SNR,method)` integer errors/bits、Jeffreys BER、tau map；
   - required-SNR CSV 四项 crossing/gain/CI 与 aggregate exact；
   - pilot sensitivity 的 moderate Np2/4/8/16 crossing 与 25 dB BER；
   - mechanism 的 matched channel NMSE / inherited semantics / inverse residual；
   - mismatch 的 delta0 exact reference 与五个 positive-delta cells。
3. 报告逐 CSV row count、key coverage、最大绝对差与 first mismatch；不得运行 bootstrap、reducer 或任何仿真。

## 脚本与 artifact 审查

- 运行提取脚本 `--check-only`、绘图脚本、py_compile；重复绘图前后 SVG/PNG hashes 稳定。
- XML parse 全部 SVG；读取 PNG 尺寸/非空；确认无 simulation tmp/checkpoint。
- 现场核 raw/aggregate/receipt/manifest/lock SHA 保持 D071/V046 exact。
- 检查 `__pycache__` 等非交付物是否残留，若有列为 P2 cleanup，不自行删除。

## 语义与视觉审查

逐张查看 PNG，核：文字不截断、不重叠、曲线不裁掉、对数轴/门限/单位准确、黑白可区分、图例使用外部语义名。重点检查：

- O1 只标理论参考；
- Np4 标为小幅优势；
- strong required-SNR 不被裁；
- B3 channel NMSE 不作为校准后估计量；
- mismatch `delta` 只称非酉/结构失配强度，不称 PDL dB；
- 图和表不声称 Ch3+Ch4 已联合仿真；
- B2 moderate/Np2 tau=0.5，其余 formal slice tau=1；
- B3 的 tau=1 只定义基准逆矩阵，逐观测重构标量不是固定 1。

## 专业材料审查

- README、三表与 captions 是否足以让作者不看内部报告也能正确使用；
- 是否仍含旧 14/18 dB 四格作为正式结论、全局 tau=1、全局只差尺度等陈旧口径；
- 是否把 mixed summaries、runtime、Grade/SHA/内部代码名带入作者材料；
- 是否明确 formal 主张、强邻居、边界与旧 confirmation 替代关系。

## 禁止

- 不修改文件，不生成新正文/素材卡，不运行 simulation/reducer/bootstrap，不检索文献。
- 不因图看起来合理就跳过 raw/CSV 全量核数。
- 不把 P2 风格意见升级为科学 P1，也不把数字/语义错误降级为风格意见。

## 输出

只在回复中返回：检查命令、全量 row counts/max diff、视觉逐图结论、P0/P1/P2、是否允许 T095 作者素材卡更新。成功 terminal=`CH4_FORMAL_MATERIALS_AUDIT_PASS`；任一数字/标签/图意 P1 为 `CH4_FORMAL_MATERIALS_AUDIT_FAIL`。
