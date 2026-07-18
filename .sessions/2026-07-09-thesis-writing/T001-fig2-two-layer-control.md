# Task Brief: Fig.2 两层控制带修订

> 来源: S017 | 产出位置: `projects/simulation/figures/fig2_adaptive_cpr.*` 与 Fig.1 v5 同步资产
> 日期: 2026-07-14
> 唯一文档: 执行方只需本 brief、当前 draw.io、正文 Method 和现有 Fig.1 v5 builder/tests

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol`。用户刚手工微调 `fig2_adaptive_cpr.drawio` 的连线。

**任务**：用 TDD 只替换 Fig.2 的 Control path，使其准确呈现 CV gate 与 blind-h/effective-SNR/13 dB 两层选择，并在 Fig.2 验收后刷新 Fig.1 v5 内嵌的完整 Fig.2 thumbnail。

**最高纪律**：

1. 不覆盖或重建用户已调整的非控制边、三泳道、DA/NDA、selector、raw spine、phase compensation、downstream DSP。
2. 不把 DA/NDA 画成串行 early exit；两候选仍共享同一输入并行产生相位估计。
3. 不写完整公式、CV 系数、margin、proxy floor 或 crossover 数值；固定决策值必须精确为 `13 dB`。
4. draw.io 是编辑权威源；SVG/PDF 是交付，PNG 是预览。所有新语义边必须绑定 source/target 且正交。
5. 不改论文正文、caption、仿真代码、结果数据或 Fig.1 的其他结构；不提交 git。

## 1. 已冻结设计

Control path 的外部输入和到 selector 的上行控制关系保持。内部替换为：

`Window power statistics → CV < τ_CV? → {NDA if yes / otherwise → Blind ĥ_dsp + Effective SNR γ̂_eff → γ̂_eff < 13 dB? → DA if yes · NDA if no} → Branch command → Estimator selector`。

建议在现有橙色背景内使用两行紧凑组合：第一行保留 measurement 与 CV gate，第二行承载 blind proxy/effective SNR 和 13 dB gate；两层结果在 selector 正下方的小型 `Branch command` 合流，以保留现有上行控制线的总体方向。允许局部延长 Control path 高度，但不得移动上部估计器和中部 raw path。

## 2. TDD 与实施

1. 新建 `projects/simulation/tests/test_fig2_two_layer_drawio.py`。
2. 在修改 draw.io 前，记录当前所有非控制边的 source/target/style/geometry 签名为测试常量；测试要求实施后逐项不变。
3. 写入新规格断言并先运行 RED：旧标签 `Per-block SNR measurement`、`γ_blk`、`Fixed SNR threshold` 不得存在；新节点、两层分支、`13 dB`、`Branch command` 必须存在；所有语义边绑定并正交。
4. 用 `apply_patch` 最小修改当前 `fig2_adaptive_cpr.drawio`。不得从旧 SVG、旧模板或生成器重建全图。
5. 运行聚焦测试 GREEN，再运行 `validate_drawio.py`。
6. 用 diagrams.net 从当前 draw.io 依次导出同名 SVG、PNG、PDF；目标尺寸查看无穿字、交叉假 junction 或裁切。
7. 运行/补充 Fig.1 v5 builder 测试，重建 `fig1_system_model_v5.drawio`，确保其 `cpr_image` payload 对应更新后的完整 Fig.2 PNG；重新导出 Fig.1 v5 SVG/PNG/PDF。

## 3. 验收

- [ ] Fig.2 图内不再出现旧单层控制标签。
- [ ] CV yes 路径明确输出 NDA；otherwise 明确进入 blind `ĥ_dsp` / `γ̂_eff`。
- [ ] 第二层明确显示 `< 13 dB`，并给出 yes→DA、no→NDA 映射。
- [ ] 两层结果只通过一个 `Branch command` 驱动 selector。
- [ ] 非控制边签名与用户修改后的基线完全一致。
- [ ] raw data bypass selector；DA/NDA 同输入并行；selected `θ̂` 侧向注入 phase compensation。
- [ ] draw.io validator 无 error/warning；目标尺寸视觉审查无 Critical/Important。
- [ ] Fig.1 v5 内嵌 thumbnail 与新 Fig.2 PNG 一致，Fig.1 其他结构不变。

## 4. 回传

报告写入 `projects/simulation/worker-tasks/fig2-two-layer-control-report.md`，包含 RED/GREEN 命令、结构计数、保留边签名检查、导出文件和任何 concerns。
