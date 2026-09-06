# Task Brief: Ch4 formal 图表与可追溯数据材料化

> 来源: S028 / D071 / V046 / T091 | 产出: 完整 Ch4 formal 图、表、派生数据与验证记录
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 33
  action_class: CH4_FORMAL_FIGURE_AND_TABLE_MATERIALIZATION
  mission_checkpoint: CP033
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只读 canonical raw/aggregate/receipt，把已经冻结的 Ch4 方法证据材料化为可供完整学位论文章节使用的专业图、表和派生 CSV。不得新增科学计算口径，不运行仿真/reducer/bootstrap，不改科学 artifacts。

## 读者与叙事目标

- 读者：硕士论文导师、盲审评阅人与答辩委员。
- 核心问题：短导频下无约束 2×2 pilot-LS 会把多余估计噪声带入求逆；利用 `H≈gQ` 的结构，把方向与公共尺度解耦，可在完全 receiver-visible 的条件下改善偏振解复用。
- 主方法：channel-domain Frobenius scale criterion（内部 C4_FWD）；强变体/消融：pilot-reconstruction scale criterion（内部 B3_PSC）；主对手：tuned singular-value-floor LS（内部 B2_TUNED）。
- 结果主张：只承重 moderate Np2/Np4 相对 B2_TUNED 的 required-SNR gain；B3 与 C4 近等效，不声称 C4 胜 B3。

## 冻结权威

- raw: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_raw.json`, SHA `642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`
- aggregate: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_aggregate.json`, SHA `916c4ba5f75703a5a63bc40931e74d161ad3e61ac0b72baa918b77de95c55602`
- receipt: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_receipt.json`, SHA `0fac1304f9aa8a4a4463c14ed5a43059a04b5c1de031b69c1d7fa9f03376e697`
- 独立终验：`projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/canonical-formal-statistics-independent-verification.md`
- 格式纪律：使用 paper-writing、design-paper-figures 与 external-output 的论文读者/图文/claim 规则；成品不得出现 D/T/CP、Grade、P0/P1、SHA 或门禁语言。

## 必须生成

全部写入 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/`：

1. `extract_ch4_formal_plot_data.py`：只读 raw/aggregate，确定性生成下列 CSV；带 frozen hash 检查与 `--check-only`。
2. `data/ch4-formal-ber-curves.csv`：至少含 scene、Np、SNR、method、errors、bits、Jeffreys BER；不得混 development/confirmation。
3. `data/ch4-formal-required-snr.csv`：四项 headline crossing/gain/CI 的逐字段表。
4. `data/ch4-formal-pilot-sensitivity.csv`：moderate Np2/4/8/16 的 matched-method BER/required-SNR 数据；crossing 不存在时必须显式 status，不造数。
5. `data/ch4-formal-mismatch.csv` 与 `data/ch4-formal-mechanism.csv`：只用 matched cells；不得把跨条件 mean-window BER 冒充因果证据。
6. `plot_ch4_formal_results.py`：从上述 CSV 生成 SVG+PNG，风格适合中文硕士论文，颜色/线型/marker 对黑白打印可区分，文字尺寸可读，不用截断纵轴制造夸张。
7. 至少四组正式图：
   - `figures/ch4-formal-ber-curves.{svg,png}`：moderate Np2/Np4 完整 5–41 dB BER–SNR 双面板，含 3.8e-3 水平线；至少 B0、B2、C4、B3，O1 用弱化视觉并明确理论参考。
   - `figures/ch4-formal-pilot-sensitivity.{svg,png}`：说明导频数变化；优先采用 matched required-SNR/固定 SNR BER，不能用混合全 SNR 均值。
   - `figures/ch4-formal-mechanism.{svg,png}`：channel NMSE / inverse residual 或其他 aggregate 中已冻结且标签合法的 matched metric；不把 B3 inherited channel-NMSE 当成自身 estimator 证据。
   - `figures/ch4-formal-robustness-boundary.{svg,png}`：weak/moderate/strong 与 nonunitary mismatch 的 matched 展示，标题与 caption 定位为“适用性与边界”，不得包装为全场景鲁棒领先。
8. 三张正文候选表：
   - `tables/ch4-formal-configuration.md`
   - `tables/ch4-formal-headline-results.md`
   - `tables/ch4-method-role-comparison.md`
9. `formal-figure-table-verification.md`：记录数据来源、命令、输出、逐数字锚点、SVG/PNG存在性与基本视觉 QA；列出不得承重的图/结论。
10. 更新包内 `README.md` 的状态与导航，但保留历史 confirmation 文件并明确其已被 formal 证据取代，不删除旧资产。

## 数字锚点

- engineering BER threshold=`3.8e-3`。
- C4 vs B2: Np2 gain `0.8704737986888702 dB`, CI `[0.6181620906133724,1.0882735019907583]`; Np4 `0.12094920868253212 dB`, CI `[0.018893188115411522,0.23922696650353503]`。
- B3 vs B2: Np2 `0.8747306637573224 dB`, CI `[0.6288589548885479,1.0784282413486024]`; Np4 `0.10803335253753943 dB`, CI `[0.02575230869563915,0.2025646753230283]`。
- 所有四项 crossing status=`STABLE`、bootstrap valid=`5000/5000`。

## 视觉与写作标准

- 每张图只回答一个问题；caption 给出场景、统计口径、比较对象、边界。
- 方法显示名必须语义化：普通 LS、调参奇异值下限、前向误差尺度、导频重构尺度、理想 CSI 参考。内部代码仅在数据列另存，不作图例主名。
- BER 纵轴对数，完整 SNR 横轴；低 BER 的 Jeffreys floor 必须诚实呈现。
- 不把 0.12 dB 画成“巨大提升”；required-SNR 图应显示 CI 和实际数值。
- SVG 必须可编辑，PNG 只作预览。不要用 AI 生成位图。

## 验证

1. `python extract_ch4_formal_plot_data.py` 与 `--check-only` 均 PASS；重复运行输出字节稳定。
2. `python plot_ch4_formal_results.py` 成功；全部 SVG 能被 XML parser 读取，PNG 尺寸合理且非空。
3. 从 CSV 反算四项 headline 数字与 V046 exact；曲线点的 errors/bits 必须来自 raw integer counts。
4. 只读确认 raw/aggregate/receipt/manifest/lock SHA 未变，未产生 simulation tmp/checkpoint。

## 禁止

- 不运行任何 simulation/formal/reducer/bootstrap，不补 SNR、seed、scene、Np、mismatch。
- 不修改 `projects/simulation/` 下任何文件，不改旧 raw/aggregate/receipt/manifest/lock。
- 不写完整第四章正文，不检索文献，不恢复 Ch5，不修改 Skill/controller/总论文。
- 不隐藏 B3，不声称 first/SOTA/全面领先，不从 mixed descriptive summaries 推导因果。

## 回报

返回：文件清单、运行命令、四项数字核对、视觉 QA 摘要、P0/P1/P2 与 terminal。成功 terminal=`CH4_FORMAL_FIGURES_TABLES_READY`；任一数字/标签/来源错误则 `CH4_FORMAL_FIGURES_TABLES_INVALID`。
