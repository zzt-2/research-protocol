# Verifications — 论文写作专题（自适应 CPR 方向）

## V001: Fig.2--4 数据、视觉与输出格式验证

> date: 2026-07-13
> 关联：S011 / D009 / R018

### 验证项

- [x] 三个绘图脚本可独立运行并生成 PDF/PNG。
- [x] Fig.2 保留六场景且无卖点数字、箭头和图内 headline。
- [x] Fig.3 共 3×7=21 点，逐点等于 `_a4_switch_30seed_fixed.json` 的 `switch_vs_nda_db_mean`，正值方向为相对固定 NDA 的 BER reduction。
- [x] Fig.4 的显示曲线、交叉点求解与标记位置共用原始点间 log-BER 线性插值，交叉点为 18.0/16.9/10.7 dB（显示精度一位小数）。
- [x] 三图坐标命名、字体层级和图例在最终尺寸下可读；PDF 为矢量输出且字体嵌入。
- [x] Fig.1 未修改；未运行实验或改动结果 JSON。

### 证据

- `python -m py_compile plot_fig2_ber.py plot_fig3_gain.py plot_fig4_crossover.py`：exit 0。
- 三个脚本重新运行：exit 0；Fig.3 输出 21 个源数据值；Fig.4 输出 weak=18.0129、moderate=16.8661、strong=10.7026 dB。
- PNG：Fig.2 2291×2640 @ 320 dpi；Fig.3 1072×801 @ 300 dpi；Fig.4 2113×1153 @ 300 dpi。
- PDF：Fig.2 7.16×8.25 in；Fig.3 3.5686×2.6735 in；Fig.4 7.0524×3.8485 in；均为矢量内容且字体嵌入。
- 独立 verifier 复核结论：Critical=0，Important=0，PASS。
- 目标脚本及本轮新增规格/日志的定向 `git diff --check`：exit 0。全仓检查仅命中既有无关文件 `.sessions/2026-06-20-problem-driven-redirection/decisions.md:1300` 的 EOF 空行，本轮未改该文件。

### 结论

PASS

## V002: Fig.1/Fig.2 draw.io 三版候选视觉门

> date: 2026-07-13
> 关联：S016 / D013 / D015 / R020 / R022

### 验证项

- [x] Fig.1 v2a/v2b/v2c 三版均保留连续 raw 主链、Adaptive CPR 局部重点和 Fig.2 关联入口。
- [x] Fig.2 v2a/v2b/v2c 均保留 raw、estimate、control 三类流向，DA/NDA 并行，selector 与 phase compensation 的公共后级接口。
- [x] Fig.2 三个 control rail 与 selected-estimate 交叉点均有 bridge mask；独立 critic 确认没有 junction 误读。
- [x] 六份 draw.io 根节点为 `mxfile`，六份 SVG 根节点为 `svg`，每份 draw.io 含一个 `mxGraphModel`。
- [x] 六个 PNG 均为 2148 px 宽，Fig.1 约 7.16 × 2.5 in，Fig.2 约 7.16 × 3.53 in；四角为近白背景，未见裁切。
- [x] 旧 `fig1_system_block.svg`、`fig1_system_overview.svg`、`fig2_adaptive_cpr.svg` 未被修改。

### 证据

- `python tmp/render_fig12_variants.py`：六个 SVG 均重新导出 PDF/PNG，输出尺寸 2148×750（Fig.1）或 2148×1059（Fig.2）。
- 独立 critic `/root/batch_d_architecture_synthesis`：六版全部 PASS；Fig.2 bridge mask 位置分别为 v2a `(x≈960,y≈260)`、v2b `(x≈1070,y≈345)`、v2c `(x≈1040,y≈320)`。
- 定向 XML/SVG 解析、禁用词扫描、PNG 四角近白像素检查：PASS。
- 旧文件定向 `git diff`：空。

### 结论

PARTIAL

### 结构性复核补充

技术语义、源文件、尺寸和线路独立性门通过；但用户复核指出六版仍是低密度模块链/空泳道，缺少总览—局部层级和内容承载型机制结构。因此本验证不能作为最终视觉质量通过，已转入 S017/D016 结构重设计。

## V003: Fig.1/Fig.2 v3 组合节点单原型验证

> date: 2026-07-13
> 关联：S017 / D016 / D013

### 验证项

- [x] 两份 v3 draw.io 源可解析，且组合节点的内部接口/阶段/连接边存在。
- [x] Fig.1 主链与 CPR zoom 的父子锚点可追踪；独立审查发现的 mini CPR 源—SVG 边不同步已修复。
- [x] Fig.2 DA/NDA 候选、selector、measurement、threshold、phase compensation 均为可编辑组合节点；raw/estimate/control 三类流保留颜色与线型冗余编码。
- [x] Fig.2 控制线在 raw bridge 处拆为上下两段，几何上留出空隙，不再形成真实交点。
- [x] PDF 纸面宽度约 7.16 in；Fig.2 派生 SVG/PDF/PNG 无 `Text is not SVG - cannot display` 残留。
- [x] 源文件定向禁语义扫描无 pilot/M0/BER/spectrum/constellation/waveform 等命中。
- [ ] 用户尚未完成最终审美/密度拍板，故本条只验证技术原型，不替代最终视觉验收。

### 证据

- XML 解析与计数：`fig1_system_overview_v3.drawio` = 62 vertices / 18 edges；`fig2_adaptive_cpr_v3.drawio` = 69 vertices / 19 edges。
- PNG 尺寸：Fig.1 `2148×1047`；Fig.2 `2148×999`。
- PDF mediabox：Fig.1 `515.52×251.28 pt`（7.16×3.49 in）；Fig.2 `515.52×239.75632 pt`（7.16×3.33 in）。
- 独立审查先定位 Fig.1 mini CPR 源—SVG 不一致与 Fig.2 bridge 交点；修复后 Fig.1 内部边已同步，Fig.2 控制上下段与 raw bridge 的 gap=80 px。
- 确定性扫描：两份 draw.io XML `PASS`；禁语义 `FORBIDDEN_NONE`；Fig.2 SVG fallback `False`。

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

交付 v3 预览给用户选择；根据用户反馈再决定是否微调组合节点密度或生成风格变体。未经确认不改 Fig.3--5、caption、正文或 LaTeX 工程。

## V004: A+C 形态板图形词汇验证

> date: 2026-07-14
> 关联：S017 / D016

### 验证项

- [x] 形态板覆盖层叠长矩形、嵌套 mini、外部括号、并行候选轨道、侧向注入、meter/threshold 与连接器尺度。
- [x] SVG/PDF/PNG 可读取；draw.io XML 可解析；未发现 pilot/M0/BER/waveform/constellation/spectrum 等禁语义。
- [x] 低饱和、无渐变/阴影/3D；箭头样例已比 v3 主链克制。
- [ ] 形态板中的 m2/m4/m5 仍有卡片化和短横条残留；不能把该板直接视为最终图形库。
- [ ] draw.io 形态板的 polyline 目前主要是无 source/target 的手工线，仅用于看形态，不作为最终连接器质量证据。

### 证据

- SVG 根尺寸 `1600×1050`，PNG `3000×1969`；PDF 一页可抽取文字，无明显裁切/乱码。
- draw.io XML：`70 vertices / 24 edges`，解析 `PASS`；定向禁语义扫描 `0 命中`。
- 独立 reviewer：六类图形族覆盖 `PASS`；整体形态可进入下一轮单原型，但同质化门 `PARTIAL`，优先改造 m2/m4/m5。

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

用户先审阅形态板；若方向确认，下一轮只把 4–5 个 motif 分配到 Fig.1/Fig.2 的具体语义节点，优先消除候选处理和补偿算子的卡片化，不扩展无语义装饰。

## V005: Fig.2 语义图元单原型验证

> date: 2026-07-13
> 关联：S017 / D017 / R022

### 验证项

- [x] `r_k` 通过深蓝 raw spine 连续进入 `Phase compensation` 和 `Common downstream DSP`，不经过 selector。
- [x] 同一输入显式分叉到并行 `DA estimator` 与 `NDA estimator`，输出 `θ̂_DA`/`θ̂_NDA` 汇入唯一 `Estimator selector`。
- [x] `Per-block SNR measurement → γ_blk → Fixed SNR threshold γ_th → Estimator selector` 控制方向单向，crossover 处白色断口避免 junction 误读。
- [x] `Selected θ̂` 由 selector 侧向进入 phase compensation；测量表盘输入/输出端口均真实接线，无悬空箭头。
- [x] 每个复杂图元均有语义：层叠处理片、六边形 selector、表盘测量、菱形阈值、相位旋转符号、公共 DSP 层叠片；未加入波形、星座、频谱、BER、pilot 或 M0。
- [x] 7.16 in 目标尺寸下短标签/线旁标签已提高到约 8.4–9.4 pt；PNG/PDF 无裁切或乱码；去色后线型与形状仍可区分。

### 证据

- SVG：`projects/simulation/figures/fig2_adaptive_cpr.svg`，viewBox `1100×560`，宽度 `7.16 in`。
- PNG：`projects/simulation/figures/fig2_adaptive_cpr.png`，`2150×1094`；PDF：`projects/simulation/figures/fig2_adaptive_cpr.pdf`。
- Render command: `python -c "import cairosvg; cairosvg.svg2png(url='projects/simulation/figures/fig2_adaptive_cpr.svg', write_to='projects/simulation/figures/fig2_adaptive_cpr.png', output_width=2150, output_height=1094, background_color='white'); cairosvg.svg2pdf(url='projects/simulation/figures/fig2_adaptive_cpr.svg', write_to='projects/simulation/figures/fig2_adaptive_cpr.pdf')"`。
- 独立 reviewer `/root/motif_board_independent_review` 最终结论：PASS；确认语义流、连接器、字号、PDF 文本和禁语义扫描均通过。

### 结论

PASS（语义原型门）。这不是 Fig.1/Fig.2 最终落版，也不替代 D013 的最终编辑源决定。

### 后续

用户先审阅语义版 Fig.2；未经确认不迁移到 Fig.1、不扩展风格变体、不做 caption/正文联动。

## V006: Fig.2 背景泳道与图元修订验证

> date: 2026-07-14
> 关联：S017 / D017 / R022

### 验证项

- [x] 三块横向淡色背景直接标注冻结标签 `Phase-estimate path`、`Data path`、`Control path`，独立图例已删除。
- [x] `Per-block SNR measurement` 为单一旁路矩形；歧义叠片和表盘均已删除，不再暗示 buffer、packet queue 或物理仪表。
- [x] `Phase compensation` 为主数据链上的普通矩形，`Selected θ̂` 从顶部侧向注入；循环箭头、NCO/VCO、CORDIC 等未引入。
- [x] raw/control 交叉处橙色控制线在 `y=276…296` 断开，深蓝 raw spine 连续无遮挡；raw bypass selector 的不变量可直接追踪。
- [x] `γ_blk` 输出段由 16 px 延长至 41 px；独立复核未发现新增断线、遮挡或裁切。
- [x] SVG XML 可解析；PNG/PDF 重新导出，PNG 为 `2150×1094` RGB。

### 证据

- 渲染输出：`render PASS`；`fig2_adaptive_cpr.svg`、`.png`、`.pdf` 已于 2026-07-14 重新生成。
- 确定性扫描：6 个所需标签均命中；`Measurement and selection`、`Received-sample layer`、`Phase-estimation layer`、旧表盘弧线 `A24,24` 与 `Minimal visual key` 均不存在。
- 独立 reviewer `/root/fig2_lane_revision_review` 首轮 PARTIAL，指出 raw/control 交叉语义反转和叠片歧义；修复后复核 PASS，确认两项缺陷关闭。

### 结论

PASS（背景泳道和图元修订门）。最终审美仍由用户拍板；本条不授权迁移到 Fig.1。

## V007: Fig.2 draw.io 编辑源验证

> date: 2026-07-14
> 关联：S017 / D013 / D017 / R022

### 验证项

- [x] `fig2_adaptive_cpr.drawio` XML 可解析，使用未压缩 `mxGraphModel`，节点、背景、端子和 waypoints 可逐项编辑。
- [x] 三个背景带分别为 `y=20..320`、`320..450`、`450..660`，两处几何间隔均为 0。
- [x] 12/12 条语义边均有 source/target，12/12 声明 `orthogonalEdgeStyle`。
- [x] raw、DA/NDA、`γ_blk → γ_th → selector`、`Selected θ̂ → Phase compensation` 拓扑符合 R022。
- [x] `Selected θ̂` 与 control 竖轨导出后相距 20 px，不再共享线段或形成伪 junction；raw/control 交叉仍保留 gap。
- [x] 最右输出使用可编辑三角端子，`e_output` 绑定 `downstream → output_terminal`，无回折短尾。
- [x] diagrams.net 直接导出的 SVG/PNG/PDF 无裁切、断线、文字重叠或错误汇合。

### 证据

- 确定性检查：`DRAWIO_XML=PASS`；`EDGES=12, BOUND=12, ORTHOGONAL=12`；`BAND_SEAMS=0,0`。
- 导出：PNG `2755×1315 RGB`；PDF 1 页；SVG XML 可解析。
- 独立 reviewer `/root/fig2_drawio_review` 首轮 PARTIAL，定位两项路由缺陷；修复后复核 PASS，并确认四份文件一致。

### 结论

PASS（Fig.2 draw.io 编辑源门）。最终节点间距与个别折点仍可由用户在 draw.io 中微调；Fig.1 未实施。

## V008: Fig.1 v4 语义、结构与目标尺寸视觉验证

> date: 2026-07-14
> 关联：S017 / D013 / D018

### 验证项

- [x] `r_k` 从信道公式直接进入 `Adaptive carrier recovery`；未引入双偏振、DAC、laser、90° hybrid、TIA、ADC 或独立 coherent-reception 前端。
- [x] `(8,8)-16APSK`、Gamma--Gamma block fading、`sqrt(h_b(k))`、residual frequency offset、linear Doppler rate、Wiener laser phase noise、complex AWGN 与接收公式均与正文和正式信道实现一致。
- [x] 时间尺度只表达一个 256-sample DSP window；channel ticks 按 `100+100+56` 分段，不再暗示跨 DSP-window 连续性，关闭了正文抽象与正式仿真实现之间的图示契约风险。
- [x] Fig.1 未重复 Fig.2 的 DA/NDA、selector、CV、threshold 或控制流，仅用 `Detailed in Fig. 2` 标记跨图接口。
- [x] draw.io 为原生可编辑 XML；8/8 条语义边绑定 source/target 且为正交边；主链中心对齐，三区背景连续，时间轴面板不越过 channel 区。
- [x] PDF 在 7.16 in 目标宽度重渲染后关键最小文字约 7.1 pt，可读；无截断、乱码、遮挡、粗重箭头、冗余图例或队列式时间轴误读。

### 证据

- 编辑源：`projects/simulation/figures/fig1_system_model_v4.drawio`；同源导出：`.svg/.png/.pdf`。
- 确定性验证器：`72 cells / 8 edges / 0 errors / 0 warnings`。
- PDF：1 page，`1080 × 402.96 pt`，未加密；以 180 dpi、1289 px 宽重渲染模拟 7.16 in 双栏目标尺寸，视觉检查正常。
- 独立语义 reviewer 最终 PASS：Critical 0 / Important 0 / Minor 0；确认单窗 `100+100+56` 表达关闭实现契约问题。
- 独立视觉 reviewer 最终 PASS：Critical 0 / Important 0；其唯一 Minor（mapper 输出 `exitY=0.55` 小台阶）随后改为 `0.5` 并重新导出、复验。

### 结论

PASS（Fig.1 v4 单原型门）。该结论覆盖语义、可编辑结构和目标尺寸视觉质量；最终审美由用户审阅，且不授权本轮进入 caption、正文图号或 LaTeX 联动。

### 后续

等待用户审阅成品；只按明确反馈做局部修改。

## V009: Fig.1 v5 真实模型微型图验证

> date: 2026-07-14
> 关联：S017 / D019 / D020

### 验证项

- [x] 五类微图均来自项目真实模型：公开16APSK调制接口、同一256-sample shared realization、接收方程反算AWGN、实际demodulator的401×401判决网格。
- [x] `h/phi/tx/rx_raw` 来自同一 realization；block fading 变点严格为100和200，即 `100+100+56`。
- [x] 展示参数 `15 dB / moderate / seed 2000` 仅用于确定性机制资产，manifest 明确不是论文实验结果；未调用结果保存链。
- [x] 五个 image cells 全部是内嵌 data URI、`connectable=0`，无本地盘符、`file:` 或HTTP图像依赖；标签、公式、锚点和语义边仍为原生 draw.io cell。
- [x] 8/8 条语义边绑定有效 source/target且为正交边；v4冻结主链、三区、公式和时间尺度保持。
- [x] 完整 Fig.2 thumbnail 的目标尺寸失败已按 D020 截断；最终 CPR 无不可读缩略图，只保留短标签和跨图引用。
- [x] 7.16 in 等效目标宽度下，APSK星座、阶梯衰落、相位轨迹、AWGN点云和demod判决区均可辨认角色，节点内无不可读小字。

### 证据

- 测试：`test_fig1_v5_assets.py` + `test_fig1_v5_builder.py` 联合 14 PASS。
- draw.io validator：`61 cells / 8 edges / 0 errors / 0 warnings`；其中5个embedded image cells。
- 同源产物：`projects/simulation/figures/fig1_system_model_v5.drawio/.svg/.png/.pdf`。
- 独立资产 reviewer：spec PASS / code quality PASS；独立 builder reviewer 最终 PASS；最终全量 reviewer PASS，可交用户审美验收。
- PDF 为1页 `1080 × 402.96 pt`，插入论文时按7.16 in宽缩放；目标宽度等效重渲染无裁切、丢图、乱码或坏字形。

### 结论

PASS。Fig.1 v5 已通过真实图元来源、结构可编辑性、目标尺寸可读性和独立最终审查；最终审美仍由用户决定。

### 后续

只按用户审美反馈做局部调整；不自动扩展到 Fig.2、caption、正文或 LaTeX。

## V010: Fig.1 v5 D021 中央通道与完整 Fig.2 缩略图验证

> date: 2026-07-14
> 关联：S017 / D021

### 验证项

- [x] 中央接收公式已删除；`channel_model` 仅保留为空值语义锚点，独立原生文本精确为 `Composite FSO channel`。
- [x] 中央受损星座直接来自与 fading、phase、AWGN 相同 realization 的 `rx_raw`，没有另起实验或伪造机制图。
- [x] CPR 节点恢复完整 Fig.2 的非白边界裁切；原图 `2755×1315`，裁切框 `(18,18,2745,1305)`，嵌入内容 `2727×1287` 逐像素一致，未删除内部内容。
- [x] 7 个 image cells 均为内嵌 data URI、`connectable=0`，无本地路径或 HTTP 依赖；8 条语义边均绑定有效端点且保持正交。
- [x] 三条 impairment injection 标签 `amplitude factor √h`、`phase`、`additive` 已显式错开竖线和箭头；标签底色与通道背景相同，目标尺寸下无穿字或假符号。
- [x] 三区背景、主数据流、单个 256-sample DSP window 与 `100+100+56` channel-block 时间尺度均未改变。

### 证据

- 联合测试：`test_fig1_v5_assets.py` + `test_fig1_v5_builder.py` 新鲜运行 `18 passed`。
- draw.io validator：`64 cells / 8 edges / 0 errors / 0 warnings`；其中 7 个 embedded image cells，外部路径计数 0。
- 同源导出：`projects/simulation/figures/fig1_system_model_v5.drawio/.svg/.png/.pdf`；PDF 1 页，`1053.12 × 377.04 pt`。
- 独立 builder reviewer：Critical 0 / Important 0 / Minor 0；确认中央资产、完整 Fig.2 payload、边与三区契约。
- 独立最终 reviewer 首轮发现注入标签碰撞 Important 1；局部修复并重新导出后复核 PASS，Critical 0 / Important 0，未见新裁切、重叠、破图或主链回归。

### 结论

PASS。D021 已按用户明确覆盖落地，可交用户做最终审美验收；本条不授权修改 Fig.2 源、caption、正文或 LaTeX。

### 后续

等待用户审阅当前成品；只按明确反馈做局部调整。

## V011: Fig.2 两层控制带与 Fig.1 缩略图联动验证

> date: 2026-07-14
> 关联：S017 / D022 / T001

### 验证项

- [x] Fig.2 Control path 已从旧单层 `Per-block SNR measurement → γ_blk → γ_th` 改为 `Window power statistics → CV gate → {yes: NDA / otherwise: blind ĥ_dsp → γ̂_eff → fixed 13 dB comparison} → Branch command → Estimator selector`。
- [x] CV yes 分支明确为 NDA；第二层 `<13 dB` yes 分支为 DA、no 分支为 NDA，与 Method 和 `_a4_switch_30seed_fixed.py` 一致。
- [x] DA/NDA 仍共享同一输入并行产生 `θ̂_DA/θ̂_NDA`；raw data bypass selector；`Selected θ̂` 仍侧向注入公共 phase compensation。
- [x] 用户修改后的 9 条非控制边 source/target/style/geometry 签名全部保持；三背景带和上/中两条语义带未重建。
- [x] 17/17 条 Fig.2 语义边均绑定有效端点且为正交边；无穿字、假 junction、裁切或 broken image。
- [x] Fig.1 v5 已重新嵌入更新后的完整 Fig.2 非白边界裁切；像素级测试通过，Fig.1 其余 8 条边、三区和时间轴保持。

### 证据

- TDD：旧源 RED 为 `1 passed, 4 failed`；局部实施后 Fig.2 聚焦测试 `5 passed`。
- 最终新鲜联合测试：`test_fig2_two_layer_drawio.py` + `test_fig1_v5_assets.py` + `test_fig1_v5_builder.py`，`23 passed in 8.68s`。
- draw.io validator：Fig.2 `49 cells / 17 edges / 0 errors / 0 warnings`；Fig.1 `64 cells / 8 edges / 0 errors / 0 warnings`。
- 同源导出：`fig2_adaptive_cpr.drawio/.svg/.png/.pdf` 与 `fig1_system_model_v5.drawio/.svg/.png/.pdf`；两份 PDF 均为 1 页。
- 独立语义/结构 reviewer：Spec compliance PASS、Code/test quality PASS，Critical/Important/Minor 均为 0。
- 独立目标尺寸 reviewer：Fig.2 以 7.16 in、300 dpi 等效宽度重渲染 PASS；Critical/Important 均为 0。仅记录 Fig.1 旧有 `phase` 标签与点划线略近的非阻断 Minor，本轮未扩大范围处理。

### 结论

PASS。Fig.2 两层控制资产及同步后的 Fig.1 v5 已达到技术嵌入门，可交用户最终审美验收；论文主控不得自行改 draw.io 语义或在 PDF 上补字。

### 后续

向 CCISP 内容补强主控回传新资产路径和 V011；论文实际引用从 v3 切换到 v5、caption 联动与最终编译由主控执行。

## V012: CCISP→学位论文 extension packaging 诊断独立终验

> status: PASS
> date: 2026-08-03
> 关联: R023 / D023 / D024

### 验证范围

独立 fresh-context verifier（未参与本轮 dossier 编写）按 brief 14 项核查清单逐项验证。结论 **14/14 PASS**。

### 验证项

1. PASS — CCISP 是完整会议稿（main.tex + sections/* + V026/V027/V028 PASS）。
2. PASS — 合法 headline 数字（abstract/results: 9 dB / 0.8–1.5 dB / fixed NDA / common-payload BER-ratio / 30 seeds / 400 windows / 三档 downlink）。
3. PASS — 旧撤回数字未复活（26/29/uplink/1.2–1.9/3.1 dB/旧 error floor 全在"禁止复活/withdrawn"语境，无当真复活）。
4. PASS — tracked main.pdf 非权威（hash 56f2fb… ≠ V026 D5EC13FE… ≠ V028 06D45979…）；权威 = LaTeX 源 + V026–V028。minor 表征偏差：dossier 写"旧 7/8 页构建"，实际 main.log 现为 5 页（历史构建痕迹），核心主张 TRUE。
5. PASS — 投稿状态 = CONFERENCE_MANUSCRIPT_COMPLETE / SUBMISSION_STATUS_UNKNOWN，无投稿编号/回执/录用；未声称已投/已录。
6. PASS — P01/P02/P04 确与 CCISP 两阶段 selector 主线相关（worker-logs/decisions 明示 selector robustness）。
7. PASS — P03 定点 = 仅数值精度/实现可行性（无 FPGA LUT/DSP/功耗）；P08-R2 coded = PARTIAL（无 pre-test freeze receipt，D051）；均非新算法。
8. PASS — G1（D057）/P09（D053）INVALIDATED 仅 threats-to-validity；AMC（D008/D009）背景一句不进主包装。
9. PASS — Package A/B/C/D 各有统一中心问题。
10. PASS — 唯一 thesis blueprint（Ch1–Ch6，非菜单）；明确答 Ch4 鲁棒性贡献（非新算法）、Ch5 实现贡献（限定）、不需要第二算法。
11. PASS — 唯一小包（统一鲁棒性表 P01+P04）有价值非重复：预注册 PASS/FAIL、增强 Ch4、复用 anchor、不开新方向、3 个不推荐包均有理由。
12. PASS — git status 改动仅限 5 harvest dossier + .sessions thesis-writing（R023/decisions/voice/topic-index）+ 既有 p05_run*.log；**未改** CCISP tex/results/仿真代码/Skill。
13. PASS — 治理一致：R023 存在、D023/D024 带 依据、voice.md 2026-08-03 段、topic-index 三处更新；_registry.yaml 未新开专题（续 thesis-writing）；未放 AMC 专题。
14. PASS — `git diff --check` exit 0，无空白错误。

### 结论

PASS（14/14）。本轮 packaging 诊断内部一致、证据支撑、守保护路径。minor 表征偏差（main.pdf 页数标签）不影响核心主张。

### 来源

独立 fresh-context verifier agent（agent_d9c184ce），2026-08-03，未参与 dossier 编写。

## V013: 硕士论文方法包装逆向工程与内核重审独立终验

> status: PASS
> date: 2026-08-03
> 关联: S018 / D026 / T011

### 验证项

1. PASS — 用户“每个核心技术章必须有方法”已进入 D025/D026 正式决策。
2. PASS — 旧 34/32 篇调研为何失效有文件+行号证据，且区分目录、摘要和方法章。
3. PASS — recipe library 含 12 篇真实硕士卡；A1/A7/A11/A12 已反查全文元数据、章节范围和 delta。
4. PASS — 每张卡包含 baseline→actual delta、公式/流程、实验、消融与边界，不是创新点抄录。
5. PASS — R1–R5 各有至少两篇真实实例；R6 经 A11/A12 定向反证后为 `0/12 REJECT_NOT_OBSERVED`，未硬凑。
6. PASS — invalidated/unauthorized 数字仅处于 prohibited/boundary 语境，没有复活。
7. PASS — 2A–2D 均有 action/baseline 或因缺 action 明确降级，grade 一致。
8. PASS — Ch3/2A/2B 的框图、流程、实验、消融和否决条件均已定义。
9. PASS — 两套 spine 均逐章审计；唯一推荐 S1 明标 B−/CONDITIONAL，未把 Ch4/Ch5 冒充完成。
10. PASS — 2A/2B 已给具体 method shape，Phase G 不触发，未创建 missing-method-search-target。
11. PASS — 未写正式论文正文、未跑实验、未改 Skill。
12. PASS — voice、D023/D024→D025→D026 血缘、topic-index、registry 与 6 个 supersession banner 一致。
13. PASS — `git diff --check` exit 0；两份 YAML 可解析；17 条 inventory evidence path 均存在；4 个 p05 logs 仍为 untracked 且不在 diff。

### 证据

- fresh-context verifier 逐文件读取四个主产物，并抽查 A1/A7/A11/A12 本地全文。
- HEAD：`dd2aab4526a36a92a07bc6c7fd0a3eedaf7b6462`。
- verdict：**READY_TO_COMMIT**；Critical 0 / Important 0 / Minor 0。

### 结论

PASS（13/13）。D026 的唯一推荐是条件式规划合同：Ch3 READY，Ch4/Ch5 各待一个 bounded package；本验证不把条件式方法宣称为完成。

### 后续

另开执行对话，先遵循 sim-preflight 与所属 GW gate，只执行 2A calibration-aware cross-grid bounded package；2A 通过后再单独处理 2B formal cost/latency+float-Q package。

## V014: T012 历史资产硕士级重裁独立终验

> date: 2026-08-12
> 关联：S019 / D028 / T012

### 验证项

- [x] A/B 全查：CCISP、select-before-execute、P01、P11 逐项沿 owner/worker/D/V 核对 → 2 个 A 与 2 个 B 均有 reference、动作链、baseline、数字或唯一 bounded gap；P11 只限实际 20 dB，必须修 gamma 注入并面对 blind CMA。
- [x] C 档抽查：P02、P03、P1、K2、RML-FSTS、AMC Q-A/Q-B → 均只具调参、组件、竞争边界或 testbed/action-contract 价值，没有被“强邻居存在”误记为永久无效。
- [x] D 档抽查：P04、P07、G1、P09、C3、oversampled Q1、coded C1、Q001 → 分别有 problem-absent、scale/cost/truth artifact、物理前提不足、exact-equivalence 或显式 scientific gate FAIL，未因 thesis-grade 放宽而错误复活。
- [x] 全量映射：解析 YAML 并与 Markdown 表逐 ID 对照 → 26 个独立 ID，无重复；A/B/C/D=2/2/11/11；4 个 aliases 均 counts_toward_total=false。
- [x] 证据闭包：遍历 YAML evidence → 41/41 路径存在；K2 路径已在预检中修正为 R006-step3-5-exact-action-closure.md。
- [x] 推荐闭包：priority_order 与正文一致 → P01 唯一 Ch4 下一包，P11 第二顺位，branch_route_b 只需论文整合。
- [x] current-view：D027 superseded→D028 active；S019 COMPLETE；topic-index/registry terminal、计数、唯一推荐一致 → PASS。
- [x] 范围与 dirty 隔离：git diff --check PASS；T012 allowlist 为 4 个治理文件 + verifications.md + 2 个新 owner；既有 papers/index/__pycache__/p05/coded logs 未纳入任务改动。

### 证据

独立 fresh-context verifier 初判：内容映射通过，但 V014 尚未落盘，导致 D028/topic-index/registry 的 V014 指针悬空；初判 P0/P1/P2=0/1/0，PARTIAL。

确定性重算：

- terminal=THESIS_GRADE_CANDIDATE_AVAILABLE
- counts={READY_FOR_THESIS_PACKAGING:2, NEEDS_ONE_BOUNDED_CONFIRMATION:2, SUPPORTING_ONLY:11, PERMANENTLY_INVALID:11, independent_total:26}
- yaml assets=26，duplicate IDs=[]，aliases=4
- evidence_refs=41，missing=[]
- D027 status=superseded，D027 被取代=D028，D028 active
- S019 COMPLETE；topic/current registry 均指向 D028/V014
- git diff --check: empty output

本条即为 bounded repair；没有修改历史 V001–V013。

### 结论

PASS

P0/P1/P2 = 0/0/0。

## V015: 九个具体方法逐项只读审计验证

> status: PASS
> date: 2026-08-13
> 关联：S023 / D032 / D033 / T019–T027 / R025

### 验证项

- [x] 九个对象均由独立单方法 subagent 回传，未在一个汇总对话中替代逐项判断。
- [x] 全程未运行实验/复算脚本，未联网检索或下载论文，未补 Groundwork，未新建候选，未修改 Skill/controller/仿真代码/论文正文。
- [x] P11 已保持 corrected confirmation=`NOT_RUN`、CMA absorption=`UNRESOLVED`，未误写为科学失败。
- [x] P05 已按实际动作链纠正为独立在线 CMA 接收机，不再称 Butterfly continuation。
- [x] P03 已纠正 Q(64,40) bypass identity 与 Q(8,6) 部署候选的混写；历史 R023 已加显式纠错。
- [x] CCISP 仅使用 9 dB、三档 downlink GG、fixed NDA、common-payload BER-ratio `0.832–1.496 dB` 的 canonical headline。
- [x] 所有方法均按 D032 判断；经典动作、参数差别、场景迁移、廉价替代或强邻居未被当作自动否决。
- [x] P06 因实际输入为 truth-scored SER，仅限离线预测；这是四条真实性底线的限制，不是期刊级 novelty gate。
- [x] 九项外部完全重复状态均明确为 `NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`，没有伪装成已完成文献查重。

### 结论

PASS。九项逐项审计完成，八项具有可命名具体 recipe，P06 仅具离线预测身份。该验证只确认本地证据解释与审计纪律，不代表外部 exact-duplicate 检索已完成，也不授权恢复执行。

独立只读 verifier 按 T028 八项逐条复核：8/8 PASS，P0/P1/P2=`0/0/0`；未参与 R025 编写，未修改文件。

## V016: CCISP 会议代号与方法正式名称核验

> status: PASS
> date: 2026-08-13
> 关联：D034 / S023 / R025

### 验证项

- [x] `projects/simulation/paper/ccisp2026/main.tex` 的论文标题为 `Adaptive Carrier Phase Recovery for Turbulent Satellite--Ground FSO Links`。
- [x] `projects/simulation/paper/ccisp2026/sections/method.tex` 的方法节标题为 `Received-Power-Aware Adaptive Carrier Phase Recovery`。
- [x] `CCISP 2026` 在本地资料中用于会议投稿计划、投稿工程、官方模板和会议约束，不是上述方法的正式名称或已定义算法缩写。
- [x] P01、P02、select-before-execute 与 P03 均复用同一 received-power-aware adaptive CPR 内核的 selector、分支或实现合同，适合计为一个 CPR 方法族的子方法，不宜在论文总体上计为四个彼此独立的核心方法。

### 结论

PASS。D034 的术语纠正有源码证据；R025 原同族 spine 推荐撤回合理。本验证不决定 P11/P05/P08-R2 谁承重，也不授权执行。
