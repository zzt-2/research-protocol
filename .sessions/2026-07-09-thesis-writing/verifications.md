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

## V017: 跨技术对象章级包装独立终验

> status: PASS
> date: 2026-08-13
> 关联：D035 / S024 / T029–T032 / R026

### 验证项

- [x] P11、P05、P08-R2 的动作链与 baseline 身份准确。
- [x] P11 仅使用实际固定 20 dB、X-output、runner-defined BER 与 goodput proxy；BER CI 跨零，CMA=`UNRESOLVED`。
- [x] P05 明确为原始 RX 上独立运行的 CMA receiver；baseline 为 15-epoch frozen supervised Butterfly FIR；改善仅落在 fixed-label BER。
- [x] P08-R2 新增动作仅为冻结 `alpha=.875, offset=.1`；prefix calibration 是共享底座，clip 贡献已删除。
- [x] “无需补实验即可有限包装”只基于现有局部命题真实、baseline 公平，并未取消真实性底线。
- [x] CPR、双偏振均衡、coded receiver 分组合理；P11/P05 同属均衡对象，没有重复计数。
- [x] 未授权实验、检索、Groundwork 或正文写作；外部 exact recipe 仍为 `NOT_CHECKED`。

### 结论

PASS，7/7；P0/P1/P2=`0/0/0`。R026 可作为下一轮战略取舍的只读事实底座，不代表 thesis spine 已拍板。

## V018: 三条方法补强 handoff 接收与主线程复验

> date: 2026-08-13
> 关联：S025 / D036 / D037 / H017–H019

### 验证项

- [x] P05 commit 血缘与范围：`fae3c69` 的 parent 为 `b9072d0`，`11dbafa` 只修 H017/唯一报告裁决文字；worktree clean，累计 diff-check PASS。
- [x] P05 结果重算：`verification.v1.json` 为 PASS，30 rows/6 cells/每格5 seeds；两个 20 dB 绑定格 CMA mean=`0.09763616/0.09935064`，6/6 cells 每格 5/5 wins，truth audit 三项为 0。
- [x] P05 fresh test：`python -m pytest projects/simulation/tests/test_p05_online_cma_strengthening.py -q --disable-warnings --maxfail=1` → `10 passed in 2.97s`。
- [x] P11 commit 血缘与范围：`ad18050` 的 parent 为 `b9072d0`，`d50c619` 只清理三份报告 whitespace；worktree clean，累计 diff-check PASS。
- [x] P11 结果重算：analysis terminal=`P11_STRENGTHENED`；LS−Adam pooled BER=`−7.7164391e-7`、95% CI=`[-1.9641845e-6,0]`；goodput delta=`391905.026 bit/frame`、95% CI=`[391763.140,392000]`；独立 verifier `ACCEPT`、P0/P1=`0/0`。
- [x] P11 fresh test：`python -m pytest projects/simulation/explore/p11-pilot-efficient-butterfly-fir/test_p11_strengthening.py -q --disable-warnings --maxfail=1` → `8 passed in 4.12s`。
- [x] P08-R2 commit 血缘与范围：`c9bb440` 的 parent 为 `b9072d0`，`b160f6a` 只清理 preregistration EOF whitespace；worktree clean，累计 diff-check PASS。
- [x] P08-R2 结果重算：terminal=`CONFIRMED_LOCAL_IMPROVEMENT`、primary gate=true；12 dB B0/full FER=`0.143125/0.1390625`、差=`0.0040625`、95% CI=`[0.001875,0.00671875]`；verification=`19/19 PASS`。
- [x] P08-R2 fresh test：`python -m pytest projects/simulation/tests/test_p08r2_strengthening.py -q --disable-warnings --maxfail=1` → `8 passed in 4.57s`。
- [x] Handoff 治理：每份 H 至少三条事实已对 raw/aggregate/verification/code diff 核验；registry `conflicts_with=[]`，依赖未改变；三任务未生成新候选、未改 Skill/controller/正式论文正文。

### 证据

```text
P05: 10 passed in 2.97s
P11: 8 passed in 4.12s
P08: 8 passed in 4.57s

P05 cumulative git diff --check: exit=0
P11 cumulative git diff --check: exit=0
P08 cumulative git diff --check: exit=0

P05 commits: fae3c694e71414d3f47b075d3dd4fa5eaad69746 + 11dbafa
P11 commits: ad180508308e288ac74bdd9a4b745d1cb03f3266 + d50c619
P08 commits: c9bb440189b11217f2e91ea74e9a971914c70813 + b160f6a
```

### 结论

PASS。三份独立任务的实现、结果、claim boundary、提交血缘和 handoff 均可接收；P05 的原始包装裁决已按 D032 分层纠正。该 PASS 表示证据包可以进入主线选择与受控集成，不表示三个提交已经合并，也不表示最终 thesis spine 已获用户确认。

## V019: Ch4/Ch5 correctness 门与 CP008 开放验证

> status: PASS
> date: 2026-08-30
> 关联：S028 / D045–D046 / T053–T058

### 验证项

- [x] Ch4 首次独立验证发现真实 update-target 缺陷，而非把测试通过当 correctness：`z=0.9+0j` 时 nearest-point ring 与 canonical nearest radius 分叉且梯度反号。
- [x] T058 只修复 gate feature / update target 分离；plain、cheap、candidate、oracle 四臂统一使用 canonical nearest-radius update，candidate 保留 point-ring gate，cheap 使用 native-ring gate。
- [x] Ch4 修复后独立 fresh 验证：`7 passed in 0.37s`；四臂分叉测试一致；paired unique hash=`1`；LS identity error=`0`、random-J error=`2.289170737184863e-16`；receipt=`CORRECTNESS_ONLY / NO_METHOD_SIGNAL`；blockers=`[]`。
- [x] Ch5 structured-covariance 独立 fresh 验证：`13 passed in 2.50s`；ring DoF=`23/24`；B1/B2/B3/C1 独立算术最大误差不超过 `5.204170427930421e-18`；LLR brute-force 最大误差 `9.094947017729282e-13`；correctness PASS。
- [x] T055 没有被误写为 Ch5 科学失败：其结论是没有现成 target residual artifact；equal circular AWGN 只能作 control。唯一合法下一动作是建立 receiver-visible post-Ch4→per-pol Ch3 known-pilot residual bridge。
- [x] CP008 只开放 Ch4 预注册有界开发、Ch5 bridge correctness、Ch4 冻结后的一格 occurrence 和独立科学验证；不开放无界调参、新损伤、完整 coded grid、FINAL 方法结论或正文。

### 结论

PASS。两条算法 seam 的 implementation correctness 均已由不同上下文接收；Ch4 可以进入预注册 development，Ch5 可以关闭真实 residual bridge blocker。该 PASS 不代表任何方法已有性能信号，也不替代后续 confirmation。

## V020: C4-2 科学停机与 Ch5 bridge 修复门复核

> status: PARTIAL
> date: 2026-08-30
> 关联：S028 / D046–D047 / T059–T063

### 验证项

- [x] T062 独立重算 T059 的 126 条 raw 记录、18 个 cell-seed 组和 36 个 count-match 对；BER、AUROC、oracle headroom 与停机原因均复现。
- [x] C4-2 的终态为 `D/STOP_NO_METHOD_SIGNAL`，原因是传统 RDE 已无可用 oracle headroom，而非算法实现错误、实验无效或被错误流程提前否决。
- [x] T062 的 `PARTIAL` 仅来自跨 CRLF/LF worktree 的 receipt SHA 可移植性；执行 worktree 内原始文件与 receipt hash 一致，不要求修复或重跑已停路线。
- [x] T061 确认 Ch5 的真实 observation→Ch4→per-pol Ch3 顺序、8-fold ambiguity、truth/future/polarization firewall 成立。
- [ ] Ch5 frozen-arm 数值 provenance 与 acquisition-preamble 连续 shared-scalar 时序仍待 T063 修复后由独立 verifier 接收；在此之前 occurrence 禁止。
- [x] CP009 只开放 C4-1 专属 Step 3.5、Ch5 bridge 窄修复及独立验证；单格 occurrence 仍以 bridge verifier PASS 为条件。

### 结论

PARTIAL。C4-2 的科学停机可接收并允许轮换 C4-1；Ch5 bridge 的主链正确但仍有两个明确、局部、可验证的 correctness 缺口。当前没有任何 Ch4/Ch5 方法达到 FINAL 或可写正文状态。

## V021: Ch5 residual bridge 修复独立复验

> status: PASS
> date: 2026-08-30
> 关联：S028 / D047 / T060–T065 / V020

### 验证项

- [x] T065 在独立 worktree fresh 执行两份 Ch5 tests，结果为 `33 passed in 3.24s`；correctness smoke exit 0，未运行 occurrence。
- [x] `--mode occurrence` 仍被 argparse 以 exit 2 拒绝，证明修复任务没有偷跑科学 cell。
- [x] frozen-arm canonical snapshot 的 5 个字段与实际 runner 入参一致；逐项改变 `mu/ring_threshold/decision_threshold` 时 `bundle_hash` 均改变而 `realization_hash` 保持。
- [x] bundle required fields 为 `25/25`，snapshot 为 `5/5`，missing=`0`，offline-only exported=`0`；hash 由 verifier 独立重算，不依赖 receipt 布尔值。
- [x] nonzero scalar sentinel 下 preamble RX、observation RX、Ch4 `W` 均发生变化；完整连续 trace 为 `176=16+160`，分界 `[0,16)/[16,176)`，三项重建误差均为 `0.0`。
- [x] offline truth、future observation、polarization swap 与 8-fold APSK rotation firewall/equivariance 均通过；rotation=`8/8`，`W` swap 最大误差 `2.220446049250313e-16`。
- [x] verifier 只新增指定报告与必要 usage log，P0/P1/P2=`0/0/0`。

### 结论

PASS。V020 的 Ch5 两个局部 correctness 缺口已经关闭；按 D047 可另派且仅派一格 target-residual occurrence smoke。该结论不表示 C5-1 已有方法信号，也不授权性能 grid、调参、新损伤或最终方法声称。

## V022: Ch5 单格 target-residual occurrence 主控复算

> status: PASS
> date: 2026-08-30
> 关联：S028 / D047–D048 / T066 / V021

### 验证项

- [x] T066 只运行一个冻结 cell：64/64 windows，seeds `2000..2063`，unique config/realization/bundle hashes=`1/64/64`；未运行第二 cell、新损伤、LDPC/FER 或性能网格。
- [x] 主控 fresh 执行三份 Ch5 tests 为 `43 passed in 7.90s`；task-control validator 按正确 CLI 返回 `PASS`；`git diff --check` 无新增 whitespace error。
- [x] 主控不调用 bridge、不重跑 occurrence，只从 `occurrence_raw.json` 重建 64 个 `WindowResidual` 并调用冻结 reducer；重建结果相对 aggregate 的 D1/D2/D3 点估计和 CI 最大绝对差为 `0.0`。
- [x] 独立重算 terminal=`DETECTABLE_OCCURRENCE`；D3 mean=`0.08706082672196491`，95% CI=`[0.06426738777629103,0.11128300328694596]`。
- [x] split 为 calibration `0..31` / evaluation `32..63`，bootstrap 以 32 个 evaluation windows 为 cluster、PCG64 seed=`2026083001`、2000 resamples；raw/receipt 的种子和 hash 数量一致。
- [x] 执行线发现并修复的 `point_counts` 只影响报告审计计数；主统计、CI 与 terminal 在 raw-only 重建前后逐值不变。

### 结论

PASS。目标共同链中存在可复现的非圆/点相关 residual covariance，允许 C5-1 进入一次预注册 bounded BER/GMI development。该 PASS 不是方法性能结论，不授权无界调参、完整 coded grid、fresh confirmation 或正式正文。

## V023: C4-1 Step 4a 纸面维度与 correctness manifest 独立审查

> status: PASS
> date: 2026-08-30
> 关联：S028 / D048–D049 / T064 / T068

### 验证项

- [x] 独立审查确认一般复 2×2 矩阵为 8 个实自由度，`g>0 + U(2)` 为 5 个；balanced pilots 下 post-LS scaled-polar 与 direct constrained objective 代数等价。
- [x] A0/A′/A/B、`PAPER_DIMENSIONS_PASS_WITH_BOUNDARY` 与本地 T048/T064/platform authority 相容；`5/8` 只保留为白噪声、小扰动下一阶 MSE 机制，不冒充 BER 数字。
- [x] 报告明确禁止把 polar/Procrustes、direct constrained form 或 unitary Jones estimation计为新原子；claim 仅为 target-scene classical migration。
- [x] 初审两个 Important 已修：C3 现检查理论 `rho=(1+delta)/(1-delta)` 与 paired bias/residual；C5 只对 exact-zero/rank-deficient/NaN/Inf fail-closed，near-zero 阈值留待 development 前预注册。
- [x] Minor 已修：C2 写成 `P(LHR)=LP(H)R`、`W(LHR)=R^H W(H)L^H` 与 complex global-scale 的精确恒等式。

### 结论

PASS。C4-1 纸面维度和修订后的 C0–C5 correctness manifest 可接收；这只授权 correctness 与有界 headroom，不代表已有 BER 增益或最终方法。

## V024: Ch5 structured-covariance held-out 开发独立复算

> status: PARTIAL
> date: 2026-08-30
> 关联：S028 / D048–D049 / T067 / V022

### 验证项

- [x] 主控与独立 verifier 均从 raw 重建 64 windows；相对 aggregate 最大数值差=`0.0`，terminal=`NO_METHOD_SIGNAL`，grade=`D`，Round 2=`0`。
- [x] seeds=`3000..3063`；tune/eval=`0..31/32..63` 互斥穷尽；config/realization/bundle unique=`1/64/64`；C1 `kappa=64`、B3 shrinkage=`1.0` 均只由 tune split 选择。
- [x] 主控 fresh 四份 Ch5 tests=`54 passed in 8.40s`；独立 verifier=`54 passed in 8.34s`；manifest/raw/aggregate/receipt hash 与 truth firewall PASS。
- [x] B2、C1 相对 B1 的 BER 点估计略低，但 BER/GMI 95% CI 均跨 0；B3 的 GMI/BER 显著退化，故没有满足预注册的 C1/simple/GMI-only signal。
- [ ] 可复用 runner 的 future simple-winner 分支有一个 P2：若 B2/B3 同时满足 simple signal，代码无条件选 B2，未执行“不劣才优先简单臂”。当前 raw 未进入该分支，科学终态不受影响；C5-1 已关闭，不为死分支另开修复。

### 结论

PARTIAL。T067 的本次科学负终态和所有数字可接收，足以关闭 C5-1 并禁止 Round 2；PARTIAL 仅限制该 runner 未来复用，不构成重跑或救场理由。

## V025: C4-1 scaled-unitary 有界开发与 raw 独立复算

> status: PASS
> date: 2026-08-30
> 关联：S028 / D049–D050 / T069 / V023

### 验证项

- [x] 独立 verifier fresh 运行目标测试为 `13 passed in 4.10s`；C0–C5 全部 PASS，correctness 通过内存 sink 执行且未改工作区。
- [x] raw/manifest 独立重算确认 4 cells × 64 windows，每格 32 tune + 32 evaluation；B1 参数=`0.01/0.001/0.001/0.01`，B2 四格均为 `tau=1.0`，均只由 tune split 选择。
- [x] 256 个 realization hash 与 256 个 observation hash 全部唯一；各 window 所有 arms 共用同一 realization，未发现 truth、future、seed 或 evaluation tuning 泄漏。
- [x] C4 相对 strongest deployable B2 的 BER 与 95% paired CI：`14dB,Np2 -0.00536919 [-0.01063747,-0.00040052]`；`18dB,Np2 -0.00284195 [-0.00631275,-0.000000691]`；`14dB,Np4 -0.00202084 [-0.00388319,-0.00032601]`；`18dB,Np4 +0.00021172 [-0.00078237,+0.00117698]`。
- [x] B2 相对 B0 在四格均显著改善，且未被隐藏；oracle total errors=`197517`、B2 total errors=`261340`，仍有真实 headroom。
- [x] SNR/幅度语义一致：16APSK 单位平均功率，复 AWGN 方差=`10^(-SNR/10)`，Gamma–Gamma fading 后不重新归一。
- [x] 独立 claim 审查确认 B2 与 C4 使用同一 `UV^H` 方向；证据支持 scaled-unitary 公共增益—偏振矩阵联合估计，不支持“更好的偏振旋转”。
- [x] 集成时发现且定位为 LF/CRLF checkout 改变 manifest byte hash；只新增该 seam 的 `.gitattributes` 并恢复原始字节。主 worktree fresh `13 passed in 4.19s`，raw-only reducer 9/9 PASS，重算 aggregate SHA256=`9c236830edc29c96edbe6698a048c910c4d6775486bc51ec2d82b460a2cc2ccb`；没有重跑或改写 BER raw。

### 结论

PASS。T069 的 `C4_STRUCTURED_SIGNAL / PROVISIONAL_A` 开发证据可接收，只允许按 D050 做一次固定配方、全新 seeds 的 confirmation。该 PASS 不是 FINAL，也不得把共同尺度估计增益改写成新偏振旋转算法。

## V026: C5-0 Step 2 全文覆盖与 baseline 身份复核

> status: PASS
> date: 2026-08-30
> 关联：S028 / D049–D051 / T070

### 验证项

- [x] 6 篇 qualified fulltexts 的身份与正文质量成立：4 篇 arXiv HTML、Layton 12 页 Springer PDF、Xie 5 页 IEEE 完整纯文本全文；没有用只具标题/摘要的 Zhang 或 simplified APSK demapper 补数量。
- [x] A 桶 4 篇，Szczecinski 式(12)与 Alvarado 式(34)提供可执行 scalar calibration 原子；B 桶 3 篇，覆盖 known-symbol residual、pilot SNR 与 pilot covariance 到 soft metric；C 桶 4 篇，包含 APSK direct 与 coherent-fiber direct context。
- [x] Layton canonical PDF magic=`%PDF-1.4`、SHA256=`b53c96bd24de33c978febb65ea0f9e374e0420332a4d3aba8ec40ab0582b84df`；4 份新增 arXiv metadata JSON 可解析，报告引用的全部 explicit content paths 存在。
- [x] 独立审查发现报告曾把 B0 写成 matched likelihood/正确噪声统计；主线程已修为同一 mismatched demapper 的 `s=1/alpha=1`，并把 matched statistics 单列为 `B_match/O1`。原审查者复核为 PASS，唯一 P1 已关闭。
- [x] Yoshida 的 `s_o=SNR/SNRhat` 含真实 SNR，不能直接包装成纯 pilot 在线公式；Layton 是高维 per-point covariance 邻居而非 scalar；两条边界已进入 Step 3 必答项。
- [x] 没有 FSO direct 或 APSK scalar 原文，因此 claim ceiling 仅为向 APSK/FSO 的受限场景迁移；按 D031–D032 这不阻断 Step 3，也不等于已证明新颖性或性能。
- [x] 集成保留并未覆盖并发修改的 `papers/index.json`、`search-archive/_index/all-papers.jsonl` 与仅时间戳 metadata；Step 3 使用显式 canonical paths，不依赖这两个聚合索引。未引入仿真、Skill/controller 或论文正文改动。

### 结论

PASS。T070 的确切终态为 `STEP2_READY_FOR_STEP3`，允许按 D051 精读冻结六篇全文。该 PASS 只证明输入证据足够，不允许 Step 3.5、候选实现、仿真或方法结论。

## V027: C4-1 fresh confirmation 独立 raw 复算与方法准入

> status: PASS
> date: 2026-08-30
> 关联：S028 / D050–D052 / T069 / T071 / V025

### 验证项

- [x] 独立 verifier fresh 运行该 seam 目标测试=`19 passed in 4.94s`；`git diff --cached --check` PASS。全仓三个范围外既有 collection errors 已披露，T071 未修改相关模块，不能据此声称全仓 suite 通过。
- [x] 独立脚本绕过项目 aggregate 直接从 confirmation raw 重算 4×64 windows；四格 C4−B2 mean/95% CI 分别为 `-0.00609922 [-0.00954738,-0.00306168]`、`-0.00188351 [-0.00354064,-0.00019817]`、`-0.00324726 [-0.00548053,-0.00143516]`、`-0.00112247 [-0.00216106,-0.00026414]`。
- [x] Np=2 pooled B2/C4 BER=`0.06076145/0.05608821`，mean=`-0.00467324`、95% CI=`[-0.00686385,-0.00282661]`、相对降幅=`7.69%`；冻结终态精确复现为 `C4_CONFIRMED_STRUCTURED_SIGNAL`。
- [x] 256 个 seed、realization hash、observation hash 均唯一；development seed overlap=`0`；B1=`0.01/0.001/0.001/0.01`、B2=`tau=1.0` 固定，无 confirmation 调参。
- [x] manifest/raw/aggregate/receipt、runner/reducer/tests 与五个 development artifact hash 全部匹配；`.gitattributes` 的 confirmation JSON/Python EOL 规则有效。
- [x] receiver API 不含 `H_true` 或 payload truth；truth 只进入 O1/scorer。paired realization、finiteness、seed/split 与 truth firewall 均 PASS。
- [x] P0/P1=`0/0`；P2 仅为场景覆盖有限与全仓既有 collection errors。独立 verifier 明确认为证据足以由主控标记 `THESIS_METHOD_READY`，但只支持公共尺度估计的有限 BER 改善。

### 结论

PASS。C4-1 满足 D041/D052 的硕士方法章最低证据合同，主控可冻结为 `THESIS_METHOD_READY` 并停止科学实验。下一步只允许章级材料化；不得把 PASS 改写成新偏振旋转、SOTA 或完整论文实验已经完成。

## V028: Ch4 写作包与 C5-0 Step 3 双线验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D052–D053 / T072–T073 / V027

### 验证项

- [x] T073 的 15 个文件覆盖九类交付：README、fact matrix、chapter blueprint、algorithm box、claim/citation ledger、raw-derived CSV、结果图脚本+SVG/PNG、方法图 semantic brief+SVG/PNG、verification 与 independent review。
- [x] 独立 reviewer 绕过包内脚本从 confirmation raw 重算四格与 pooled Np=2，CSV 最大绝对差仅 `4.8633e-11`（十位小数序列化）；B2/C4 同 `UV^H` 方向身份被保留，P0/P1=`0/0`。
- [x] 两个初始 P2 已关闭：橙色控制箭头不再压诊断文字，四格增益标注均移到完整柱群上方；主控实际查看修复后两张 PNG，文字、箭头、图例和零起点均可接受。
- [x] 主 worktree 集成后 fresh 执行 `plot_ch4_results.py --check-only` 返回 `PASS: raw-only CSV/figure derivation matches D052/V027`；`git diff --cached --check` 通过。
- [x] T072 完成冻结六篇 6/6 fulltext read、六条 read-log receipt、四份新 read note 与两份重读补充；唯一 `Q-C5-0` 四判据 `4/4`。
- [x] T072 独立内容 reviewer 初审只发现 Szczecinski `g_n/SIR` receiver-visibility 分类 P2，收紧为 `UNKNOWN/model-oracle` 后复核 `PASS / P0-P1-P2=0-0-0`。
- [x] C5-0 baseline 已正确区分 B0 mismatched `s=1` 与 B_match/O1；truth/offline GMI、true SNR、receiver-known pilots 和 direct plug-in comparator 边界均显式记录。
- [x] T072 terminal 精确为 `STEP3_CLASSICAL_MIGRATION_READY_FOR_STEP3_5`；没有联网扩搜、实现、仿真、Step 3.5 偷跑或正式正文修改。

### 结论

PASS。Ch4 terminal 可升为 `CH4_WRITE_PACKAGE_READY`，已经具备直接开始写章的内部材料，但不等于正式正文已完成。C5-0 具备一个合法的硕士级经典迁移 Q# 和 Step 3.5 入口；尚无 BER/FER 方法证据，不得写成 Ch5 已成立。

## V029: C5-0 Step 3.5 exact-recipe 与代数边界验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D053–D054 / T074 / V028

### 验证项

- [x] T074 只运行 Round 1 并按时限停止；异构 feed 分别保留 raw=`2/211/134/40`、family 1 raw=`UNKNOWN`，没有虚加成跨 feed unique 总数，也没有把 source/tool failure 记成“无文献”。
- [x] 九字段矩阵逐项区分 Q-C5-0 与 Yoshida/Alvarado/Wu/Shibata/Cao/Layton；没有单篇证据同时匹配目标平台、observation、input、statistic/cadence、action/freedom、decoder interaction 与 output。
- [x] max-log B2=B3 的严格条件与推导成立；exact APP 用 partition-ratio 必要充分条件表述为“一般不等价”，并保留逐 bit 核查债务，不再把 dominant-symbol 近似写成普遍严格特例。
- [x] hard sign、maximum-metric ordering、finite-iteration BP/NMS 与 GMI/ASI 四类语义已分离；固定系数 normalized min-sum 的正齐次性表述已修正。
- [x] 任务内独立 reviewer 首轮 `P0/P1/P2=0/3/1`，三项 P1 修复后复核 `0/0/1`；剩余 P2 是部分外部邻居缺逐字段页/式指针，未闭合字段已降为 `UNKNOWN`/非承重。
- [x] 主 worktree 集成后另一独立上下文再核为 `PASS / P0=0, P1=0, P2=3`；三个 P2 均为局部措辞/证据完整度，不改变 `STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM`。其中 per-frame scalar 歧义已由主控修为“frame 内共同且两臂同映射不破坏 B2=B3”。
- [x] 暂存白名单只有 `step3-5-exact-recipe-closure.md` 与本轮治理文件；未暂存并发论文索引、缓存或历史实验日志。未实现、未仿真、未修改 Ch4/Skill/controller/正式论文正文。

### 结论

PASS。C5-0 可以按有限 claim 进入纸面 Step 4a，但不允许直接实现或仿真。下一门必须先证明自然 reliability mismatch、B0→O1 headroom，并审计固定 normalized min-sum 正齐次性与 clipping/B1/B3 吸收风险。

## V030: C5-0 Step 4a 纸面可行性与 B2 冻结接口身份验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D054–D055 / T075 / V029

### 验证项

- [x] T075 唯一 terminal=`PAPER_DIMENSIONS_PASS_B2`，报告中仅 header 与 final 两处；旧 `PAPER_DIMENSIONS_PASS_B3_MIGRATION` 为 0 次。
- [x] 64-window natural residual reduction 由独立上下文复算为 `min=0.01410175, median=0.06547005, max=1.16298215, mean=0.15833991, CV=1.69147304`；报告只将其用于 observation/causal possibility，未冒充 BER/FER。
- [x] fixed-NMS 正齐次、B1 stationary 边界、内部 adaptive threshold/filler 重参数化、max-log B2=B3 与 exact-APP 一般不等价均诚实披露；强替代限制 claim，不被删除或伪装成不存在。
- [x] C0–C6 覆盖 APSK label/sign、`N0`/`N0/2`、max-log identity、exact-APP non-identity、bit order/interleaver、clip/filler placement、truth firewall 与 paired lifecycle。
- [x] 独立验收为 `PASS / P0=0, P1=0, P2=1`。唯一 P2 是 demapper preclip `30` 来自旧 Gray-16QAM adapter、目标 APSK 尚未 receipted；主控已改为“若目标 APSK seam 沿用当前 LDPC adapter/backend 的候选合同”，不再冒充冻结事实。
- [x] 暂存白名单只有 T075 报告与本轮治理/任务 brief；未暂存并发论文索引、缓存、历史日志或实验输出。T075 未实现、未仿真、未跑 BER/FER。

### 结论

PASS。C5-0 只获得 B2 correctness-only 入口；方法仍为 `CANDIDATE`。CP017 只允许闭合目标 APSK→5G LDPC 接口和 C0–C6，不允许自然 occurrence、headroom、BER/FER 或调参。

## V031: C5-0 APSK→LDPC correctness 与 B2 action 验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D055–D056 / T076 / V030

### 验证项

- [x] T076 最终 terminal=`CORRECTNESS_PASS_B2_ACTION`；targeted correctness 在任务 worktree 为 `10 passed`，主 evidence worktree 集成后 fresh 为 `10 passed in 8.14s`。
- [x] 既有 codec 回归 `ldpc_noiseless_roundtrip_one_cw / every_decode_fresh_state / b1_exact_reencode_nll` 在任务侧与主 evidence worktree 均为 `3 passed`；主侧 fresh=`3 passed, 15 deselected in 6.22s`。
- [x] APSK owner=`m16apsk_mod`，联合 constellation/label hash=`684fa7045c351f816e77eb1480784b013d8c100b3939b63d71b05b3b9b8ed879`；LLR 正号表示 bit 1，complex `N0=E|n|²`、per-real=`N0/2`。
- [x] live Sionna 2.0.1 receipt 为 BG2、`Z=104`、`k_ldpc=1040`、16 filler=`-20`；seam 不手工执行 `out_int_inv`。实际链为 `clip30 → B2 → decode clip30 → backend clip20 → out_int_inv/rate recovery/filler → BP clip20`。
- [x] all-zero、single-one、walking-label、random 四例的 coded→LLR sign error 与 decoded information-bit error 均为 0；one-scalar-per-physical-frame、两偏振/全部 codewords 共享、fresh decoder lifecycle 与 truth API 隔离成立。
- [x] 未裁剪 max-log 下 B2=B3 `<=1e-12`；exact APP 在测试网格四个 bits 均出现稳定 nonidentity，B3 因而保留为 distinct same-budget comparator。
- [x] 首轮外部独立复核发现两项 P1：decoder 顺序写错、真实 B1 arm 缺失；两项均经明确 RED→GREEN 修复。修复后独立 reviewer=`PASS / P0=0, P1=0, P2=0`，没有把初审 FAIL 从历史中删除。
- [x] 三文件白名单、task-control validator、`py_compile` 与 `git diff --check` 均 PASS；没有运行 natural occurrence、headroom、BER/FER、GMI optimization、参数搜索或新损伤。

### 结论

PASS。T076 证明 B2 在目标冻结 codec 中是合法、可执行、可由自然固定边界产生非齐次效应的 receiver action，但不证明方法性能。CP018 只可开放一个继承 T066 的预注册自然单格，按 pilot→held-out reliability、B0→O1、B1/B2/B3 顺序门控；不得直接进入多格开发。

## V032: C5-0 单格 reliability/headroom 与停机验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D056–D057 / T077 / V031

### 验证项

- [x] target mapping/物理时序/codec smoke 闭合：每帧一个 `k=1024,n=1536` BG2 codeword，经 pol-major 384 个 APSK non-pilot slots；4-symbol Ch4 preamble + 256 observation/pol，GG block 跨界精确为 `252+4`。
- [x] 8 个 smoke seeds 使用真实 `TargetApskCodec`，每帧 B0/B1/B2/B3/O1 都是 fresh 20-iteration decode；artifact 明示 live backend，truth 声称收窄为 receiver API 排除与同输入确定性重放。
- [x] B1 calibration 使用独立 seeds `3000..3063` 与 15 个预注册 scalar；按 FER→BER→`|log s|`→数值 tie-break 冻结 `s=1.0`，18 frame errors、4893 bit errors。
- [x] Gate 1 固定 128 帧只统计不译码；`rho=0.9856654001`，one-sided lower=`0.9758980392`，10,000 次 physical-frame bootstrap，terminal=PASS。
- [x] Gate 2 只在 Gate 1 PASS 后追加同一 manifest 到 512 帧，并逐帧重放核对 pair/mapping/received-observation/codeword hashes；B0/O1 BER=`0.0492935181/0.0533390045`，FER=`0.2578125/0.255859375`。
- [x] `BER_B0-BER_O1=-0.00404548645`，95% CI=`[-0.00556197166,-0.00266070366]`；FER difference=`0.001953125`，CI=`[0,0.005859375]`，仅 1 个 discordant FER pair。terminal=`SINGLE_CELL_NO_HEADROOM` 正确。
- [x] Gate 3 未开放；512-frame raw 每帧只有 B0/O1，B1/B2/B3 无 evaluation 结果。没有换 cell、调参、追加样本、新损伤或 GMI/uncoded 替代。
- [x] 独立 raw 复算确认 split、B1、rho、BER/FER、paired CI 与 terminal；raw-only audit 摘要链补强后 512/512 可离线重算。最终 reviewer=`PASS / P0=0, P1=0, P2=3`，三个 P2 为 truth mutation 强度、T066 seed 非 bit-exact 措辞和 resume 校验薄，不改变负 terminal。
- [x] 主 evidence worktree fresh targeted/T076/backend 回归为 `14 passed + 10 passed + 3 passed`；`git diff --cached --check` PASS，未暂存并发论文索引、缓存或历史实验日志。

### 结论

PASS。C5-0 在目标 frozen cell 中有很强的 pilot→payload reliability signal，但其 scorer-only scalar auxiliary oracle 没有 coded BER headroom；该形态按 D056 关闭且不得救场。CP019 只可轮换 C5-5 candidate-specific GW Step 1，不授权实现或仿真。

## V033: C5-5 Step 1 authority reconciliation 验收

> status: PASS
> date: 2026-08-30
> 关联：S028 / D057–D058 / T078 / V032

### 验证项

- [x] T078 terminal=`STEP1_C5_5_EVIDENCE_GAP_BOUNDED`；未把 evidence gap 写成科学失败，也未用题名/元数据冒充全文。
- [x] `Q-C5-5` 的 M-C-A 与 receiver-visible IAO 闭合：channel/pilot reliability → per-codeword bounded iteration budget → decoded bits + BER/FER/edge-update/平均/P95成本；truth denylist 明确。
- [x] 方法身份已收缩为 budget-only；static `cn_schedule` 与 dynamic priority、库级 callbacks/state 与项目 seam 均被分开，最小 `num_iter` adapter 不需自写 BP。
- [x] collision/absorption ledger 包含 Wu 2010 adaptive NOMS、ordinary early-stop、failure-triggered extra work、syndrome/bit-flipping rescue、fixed extra iterations、flooding/layered 与 static LUT；强邻居限制 claim，不被隐藏。
- [x] 本地全文审计确认 DOI `10.1109/ACCESS.2019.2899106` 仅有 identity/metadata，无 `content.md`/read note；唯一 blocking gap 精确、可由 Step 2 有界关闭。
- [x] 独立只读审查给出同一 `EVIDENCE_GAP`：四判据 3 PASS+1 PARTIAL，最危险吸收是 syndrome early-stop；最小 seam 同样为 per-call `num_iter` 分组调用，无需重写 decoder。
- [x] 任务侧 task-control、双文件白名单、内容锚点与 `git diff --cached --check` 均 PASS；未实现、仿真、下载、修改 `.sessions/`/Skill/controller/正文或进入 Step 2。

### 结论

PASS。C5-5 已形成硕士级方法候选和有界接口路径，但尚非可实现/可仿真的方法；CP020 只允许一个窄 Step 2 获取包，之后必须另开 Step 3 精读并专门裁决 ordinary early-stop/equal-update 是否完整吸收。

## V034: C5-5 Step 2 bounded acquisition 验收

> date: 2026-08-30
> status: PASS
> 关联: D059 / T079 / S028

### 验证对象

T079 的检索归档、2019 DOI identity-mismatch receipt、两篇 qualified fulltexts、coverage report、worker log、论文索引增量与独立审查结论。

### 验证结果

1. **范围与计数 PASS**：审计 3 个目标身份，形成 2 篇 qualified Step 3 pool，未超过“2019 direct + 至多 2 篇 comparator”的 bounded acquisition 范围；2/4 预注册 query 实际运行，没有借失败扩大搜索。
2. **身份安全 PASS**：DOI `10.1109/ACCESS.2019.2899106` 的下载候选被核为 arXiv `cs/0702111v2`、2007 年入侵检测论文，标题 overlap=`0.3333`，已拒绝并只留 mismatch metadata；错误正文和错误源文件没有进入承重证据池。
3. **冻结全文质量 PASS**：Liu et al. 的正式发表年份更正为 2025，PDF=`2,882,056` bytes，清理后 content=`239` total / `100` effective lines，SHA-256=`ED0B33DF4531A0AD2CA92BF6CF420CECFC59D9EA7CA59514B141078375D79509`；He et al. 2021 既有 content=`231` total / `122` effective lines，可支持 early-stop/max-iteration 精读，legacy `source.pdf` 为 plaintext 的债务已显式披露。
4. **覆盖边界 PASS**：两篇全文分别覆盖 reliability-driven dynamic scheduling 与 CRC/syndrome early stop/max-iteration 工程口径；它们足以组成有界 Step 3 read pool，但不等于 P0 exact collision 已排除，也不证明 Q-C5-5 存活。
5. **独立审查与集成复验 PASS**：任务 verifier 首轮指出发表年、尾随空格和 line count 三项问题，修复后复验 `READY=YES / P0-P1-P2=0-0-0`。接入主 worktree 后，独立控制面 verifier 又发现 PowerShell binary-patch 管道曾把 PDF 损坏为 `27,731` B 的空格文本，并指出 registry 仍停在 CP020；主控从 clean T079 task worktree 精确恢复 artifact 并更新 registry。最终 main worktree fresh receipt 为 PDF=`2,882,056` B、magic=`%PDF`、SHA-256=`FAB2C2718D02544B9A1DDD55B0B0A2A5AEF3A7B504429F9C6C9BA0BC907F214E`，content SHA-256=`ED0B33DF4531A0AD2CA92BF6CF420CECFC59D9EA7CA59514B141078375D79509`；task-control、`git diff --cached --check` 与 staged scope 均 PASS。任务提交为 `2426f50dde12928c01a0b69651f2a4578414078d`。

### 结论

PASS。T079 已把 C5-5 的全文缺口缩成冻结两篇的 Step 3 精读包，并诚实保留 2019 P0 未取得这一未知。CP021 只允许结构化全文精读与动作吸收裁决；不得检索、下载、实现、仿真或提前进入 Step 3.5。

## V035: C5-5 Step 3 frozen-fulltext read 验收

> date: 2026-08-30
> status: PASS
> 关联: D060 / T080 / S028

### 验证项

- [x] 冻结全文恰好 `2/2`，identity=`2/2 PASS`；没有读取或承重使用错配的 2007 arXiv，也没有扩搜、下载、实现、仿真或进入 Step 3.5。
- [x] Liu 2025 的 state/action 被核为 decoder-internal check-belief residual→local check/edge order，fixed cap=50；He 2021 被核为 layered quantized NMS + CRC/syndrome stop + failure 后 TS bit-flip，fixed cap=100。两者均与 Q-C5-5 的 current-codeword channel-LLR-derived predecode statistic→per-codeword `num_iter` cap 九字段不完全相同。
- [x] ordinary early-stop 裁决精确为 `NOT_COMPLETE_ABSORPTION / MANDATORY_CHEAP_COMPARATOR / EMPIRICAL_ABSORPTION_UNKNOWN`；没有把 cheap comparator 隐去，也没有把未实测吸收写成科学失败或性能结论。
- [x] 唯一 Q-C5-5 的 M-C-A 四判据 `4/4`，claim ceiling 限于目标 DP-(8,8)-16APSK coherent-FSO receiver 中的经典预算迁移；P0 2019 缺失继续限制 prior-art closure/first claim。
- [x] 任务独立 reviewer 初审 `PASS_WITH_P2 / P0-P1-P2=0-0-4`；四项措辞/证据边界全部修订，原 reviewer fresh `RECHECK: PASS`。task-control、identity、read-log、scope 与 `git diff --check` 均 PASS。
- [x] T080 精确修改 5 个文件，任务 commit=`28262945417a7c264052ee85ccffeafea6a28710`；主 worktree 以 no-commit 方式接入，未暂存并发论文索引、缓存或历史实验日志。

### 结论

PASS。C5-5 在 candidate level 存活并具备 Step 3.5 入口，但当前按用户 D060 优先级暂停，不自动继续。CP022 唯一主线改为 Ch4 production-evidence design/preflight；本验证不授权 Ch4 或 Ch5 仿真。

## V036: Ch4 production-evidence 设计与 preflight 验收

> date: 2026-08-30
> status: PASS
> 关联: D060–D061 / T081 / S028

### 验证项

- [x] 完整方法章论证链已冻结：星地双偏振短导频问题、scaled-unitary receiver action、公平 B0/B2/B3_PSC/O1 梯队、全 BER–SNR、pilot efficiency、NMSE/residual 机制、三档 turbulence、dimensionless mismatch boundary、复杂度与 Ch3 CPR 接口。
- [x] 旧 confirmation 与新证据严格分层：T071 raw/aggregate/receipt immutable；A1 逐窗复现 256 个 historical observation hashes 只隔离 demapper；A2 才切换新 SeedSequence production seam。
- [x] B3_PSC 已冻结为 pilot-only 非负实 scalar LS calibration；production-seam bridge 同时要求 pooled Np2 C4 对 B2/B3_PSC 的 CI upper `<0`，且 Np4 的 `BER_C4-BER_comparator` CI lower `<=0`。
- [x] 三档 `(alpha,beta)` 从 `SimulationConfig().turbulence` resolved snapshot 读取；`0.2/1.6/3.5` 正确称 plane-wave Rytov variance，rounded-parameter scintillation indices=`0.193752/0.907895/1.122449`。
- [x] formal production 一次固定 128 latent windows/cell；B2 tuning split/目标函数/tie rule、mismatch formula/levels/boundary、SNR 延伸、Jeffreys crossing 与整曲线 joint-latent bootstrap 均在首次数字前冻结。
- [x] 第一轮 independent preflight=`NEEDS_REPAIR/P0-P1-P2=0-5-0`；修复后第二个 verifier fresh terminal=`CH4_PRODUCTION_PREFLIGHT_READY/P0-P1=0-0`。task-control validator 与 `git diff --check` PASS；全程未运行仿真或产生新 BER。

### 结论

PASS。T081 已把 Ch4 章级目标变成可执行的十任务计划，并设置最短因果止损门。CP023 只允许 TDD 修复公共 16APSK hard demapper；本验证不授权 historical replay、smoke 或 production。

## V037: common 16APSK demapper correctness repair 验收

> date: 2026-08-30
> status: PASS
> 关联: D061–D062 / T082 / S028

### 验证项

- [x] RED 证据真实：冻结 `0.9155 exp(j*pi/8)` 反例历史判为 outer `1000`，全局最近 inner=`0000`；平方距离 `0.1621480540 < 0.3456643325`。固定 512 点云另有 `17/2048` bit mismatch。
- [x] 实现 diff 为最小 `2 insertions/4 deletions`：删除 `thr/is_outer` 与 `| is_outer`，保留 gamma、radii、16 constellation points、Gray mapping、normalization、modulator 和严格 `<` tie rule。
- [x] 实现者 focused GREEN=`3 passed`，T082 指定 8 文件回归=`113 passed in 25.80s`；py_compile、task-control、四文件 scope 与 `git diff --check` PASS。
- [x] 独立 reviewer 不复用任务 test helper，以 seed `918273645` 自建 oracle 并核 16,384 新点；label/bit mismatch=`0/0`，最小 nearest gap=`3.1324e-05`，无 tie 干扰。
- [x] reviewer fresh focused=`3 passed`、`test_common=69 passed`、P0-P1-P2=`0-0-0`；四个 T071 confirmation artifacts 当前 hash 与 HEAD 一致。
- [x] 全程未运行 BER replay、cell、smoke、grid 或 production；PASS 未被转述为 C4 信号仍在。

### 结论

PASS。公共 16APSK hard demapper 已符合全 16 点欧氏最近邻合同。CP024 只允许 T083 对旧 256 observations 做 A1 exact replay；不授权新 RNG、B3_PSC、smoke 或 production。

## V038: Ch4 corrected-demapper historical replay 验收

> date: 2026-08-30
> status: PASS
> 关联: D062–D063 / T083 / S028

### 验证项

- [x] source `confirmation_manifest/raw` hashes 与冻结 authority 一致；历史 `confirmation_manifest/raw/aggregate/receipt` 相对 HEAD unchanged，新 artifacts 未覆盖旧资产。
- [x] 全部 4 cells×64 windows 的 seed、gain、realization hash、observation hash、payload bits identity=`256/256`；五臂机制量 channel NMSE/inverse residual/rho=`1280/1280` exact identity，独立审查最大绝对差为 0。
- [x] corrected demapper 下四格 B2→C4 BER 分别为 `0.0851679→0.0768876`、`0.0732136→0.0694785`、`0.0402689→0.0356407`、`0.0227985→0.0210624`。
- [x] 独立 reviewer 未导入 runner/reducer，使用 PCG64 seed `2026083005`、5000 resamples、每 named comparison reset 复算；pooled Np2 D=`-0.00645423`、95% CI=`[-0.00868396,-0.00433086]`，两格 Np4 CI lower=`-0.00560524/-0.00302410`，与 aggregate/receipt 精确一致。
- [x] raw-only、schema/counts、manifest/source/code/result hashes、receiver-action truth firewall 与 terminal 重判均 PASS；reviewer P0-P1-P2=`0-0-0`。
- [x] 实现 TDD RED=`5 failed`、GREEN=`5 passed`；实现者与主线程邻接 focused suite 均为 `27 passed`，py_compile、task-control 和 diff-check PASS。
- [x] seam `.gitattributes` 已补四个新 JSON 的稳定 EOL 规则，避免 fresh checkout 字节 SHA 漂移；不改变内容或科学结论。

### 结论

PASS。corrected global-ML demapper 没有吸收历史 C4-vs-B2 承重信号，A1 因果重放闭合。CP025 只开放 production kernel TDD 和独立 correctness review；新 RNG/B3_PSC 的 A2 BER bridge、smoke 与 formal production 仍未授权。

## V039: Ch4 production core correctness 验收

> date: 2026-08-30
> status: PASS
> 关联: D063–D064 / T084 / S028

### 验证项

- [x] `Np=2/4/8/16` balanced Gram 全 PASS；七路 PCG64/SeedSequence 的 component set、entropy、完整 spawn key、exact replay 与 latent hashes 经独立 oracle `7/7` 验证。
- [x] 同 latent 的 5→35 dB 解析 noise-scale ratio=`31.6227766`，跨 SNR/Np bits/Q/gain/payload-noise 保持一致，pilot noise 使用冻结 prefix。
- [x] weak/moderate/strong 从 central params runtime resolve 为 `(11.6,10.1)/(4.0,1.9)/(4.2,1.4)`，scintillation index 复算约 `0.193752/0.907895/1.122449`；kernel 未复制第二份参数 authority。
- [x] B2 tau=1 与 C4 共享 `VU^H`；B3_PSC normal/negative-numerator/zero-or-nonfinite denominator/nonfinite output closed-form oracle 全 PASS，receiver signature/source 无 hidden truth。
- [x] mismatch power-preservation 与 singular-ratio oracle PASS；unsupported/invalid/nonfinite paths fail closed。
- [x] 初审真实发现 consumer provenance P1：篡改 spawn key 或 turbulence metadata 仍被接受，terminal=`INVALID/P0-P1-P2=0-1-1`。17 个 mutation cases 真实 RED 后做最小修复，fresh reviewer 复放 17/17 全拒绝；初审历史未覆盖。
- [x] repair 后 focused=`46 passed`，py_compile、task-control、三文件 scope、diff-check PASS；主线程 fresh 同套=`46 passed`。
- [x] final P0-P1-P2=`0-0-1`；P2 仅要求把 B3 NMSE 标为 calibration 前 inherited B2 estimate，post-calibration 作用看 inverse residual。

### 结论

PASS。production kernel 的随机总体、authority、廉价对照和结构边界 correctness 已闭合。CP026 只开放 fixed A2 production-seam bridge；Task 5 smoke/tuning、formal manifest 与完整 production 仍未授权。

## V040: Ch4 A2 production-seam bridge 与方法身份裁决

> date: 2026-08-30
> status: PARTIAL
> 关联: D064–D065 / T085 / S028

### 验证项

- [x] canonical raw 恰含 latent IDs `20000..20063`、4 cells、5 arms，census=`64/256/1280`；same-SNR payload pairing=`128/128`、O1 Np pairing=`128/128`。
- [x] 独立 reviewer 未导入 runner/reducer，按 PCG64 seed `2026083006`、5000 resamples、每比较重置，直接从 raw 复算逐格和 pooled 64-cluster统计；artifact P0-P1-P2=`0-0-0`。
- [x] C4−B2 pooled Np2=`-0.00558591`、95% CI=`[-0.00835918,-0.00305787]`；C4−B3_PSC=`-0.000125408`、95% CI=`[-0.000800651,+0.000549561]`，故 frozen terminal=`CHEAP_COMPARATOR_NOT_CLEARED`，Task 5 未被旧 D064 自动开放。
- [x] 探索性但非 thesis 的 B3−B2 pooled Np2=`-0.00546050`、95% CI=`[-0.00768733,-0.00342591]`；B3−B0=`-0.01092815`、95% CI=`[-0.01371816,-0.00827978]`，且四格两组 CI upper 均 `<0`。该信号只支撑 D065 重新冻结候选，不冒充正式证据。
- [x] raw SHA 在 canonical 后保持 `4ef32e16d4ce252634686e8e3dc6e0f94dbff4daad18ef12691b491c875e33ed`；frozen core/common/scaled code binding PASS，truth firewall 由 T084 frozen core hash链闭合。
- [x] 过程债如实保留：raw 生成 runner SHA=`871ec566...`，post-run authority-validation runner SHA=`934bf414...`；receipt 将 reproducible-generation binding 标为 `PARTIAL`，未用当前 runner 冒充实际生成器。
- [x] fresh root focused tests=`59 passed`；实现者更宽 frozen suite=`68 passed`，py_compile、task-control、scope、历史不可变性与 diff-check PASS。

### 结论

PARTIAL。A2 artifact 与科学复算有效，但“C4 显著清除 B3”科学门失败且生成器字节复现绑定仅 PARTIAL。D065 不把该失败涂成 PASS；它只依据既有硕士级标准把强邻居从自动否决门降为 claim-ceiling/ablation，并开放一次不含 formal production 的 tuning+smoke+manifest freeze。

## V041: Ch4 方向—尺度方法族 production freeze 验收

> date: 2026-08-30
> status: PASS
> 关联: D065–D066 / T086 / S028

### 验证项

- [x] canonical tuning census=`96/1152/8064`，IDs=`21000..21031` 与 T085/smoke/formal 全部零重叠；每 cell 恰有五个 B2 tau、C4 与固定 tau=1 B3，equal bits/pairing/truth firewall PASS。
- [x] 独立 reviewer 未导入 runner/reducer，从 raw 以 pooled-count Jeffreys→三SNR等权mean-log10复算全部12个选择，objective最大绝对差=`0.0`；moderate/Np2=`0.5`，其余=`1.0`，独立 terminal=`CH4_FAMILY_PRODUCTION_FREEZE_READY`。
- [x] tuned B2 不满足全12格同时支配 C4/B3；development objective只作 baseline freeze，不升级为论文数字或 formal 方法结论。
- [x] ID20999与ID21999均只在所有Git worktree外的OS temp运行；后者核10 actual+1 delta0 reference、H/observation exact identity、positive-delta共享base noise与O1 truth separation。
- [x] stale tests SHA P1 已在 code/tests冻结后重签 receipt；immutable raw/aggregate hashes保持 `00161c...fa315`/`9af3b3...31378`，新receipt=`afa918...e2fc`，11项actual hashes现场全匹配。
- [x] scientific manifest SHA=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；formal IDs、5:2:41网格、scene/Np/mismatch、两套bootstrap、crossing、A/B/C/F、tau lineage 与future execution interface均冻结，T087 hashes仍为null。
- [x] 实现者与独立 verifier fresh focused tests=`27/27`，六文件py_compile、task-control、不可变core/common/scaled/T085、scope与diff-check PASS。

### 结论

PASS，final P0-P1-P2=`0-0-3`。三个P2只限制辅助hash复核、temp guard自动枚举与双文件发布恢复性，不改变 tuning raw、scientific manifest或T087入口。CP028只开放 formal execution seam TDD、ID29999全网格单latent smoke和tracked execution lock；formal IDs仍禁止运行。

## V042: Ch4 formal execution seam 首个 tracked lock 终态验收

> date: 2026-08-30
> status: FAIL
> 关联: D066–D067 / T087 / S028

### 验证项

- [x] T087 initial RED=`15 failed`；四项 runner/reducer P1 与 freezer direct-CLI P1 均以真实 RED→GREEN 修复，pre-lock focused suite最终=`19/19 PASS`，五文件py_compile与task-control PASS。
- [x] 唯一 ID29999 OS-temp smoke exit=0、耗时约3.03s；独立 raw-only复核 census=`1/3/119/595/ref1`、scene cells=`19/81/19`、五臂/τ/truth/RNG namespace/cross-Np pairing/delta0 identity全部PASS；grade=`null`、未报告科学数字。
- [x] 首个 tracked lock SHA=`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`，scientific manifest、runner/reducer/entry/tests、四项frozen dependency、HEAD、Python/NumPy/platform与formal ID域绑定均现场一致；无 formal raw/aggregate/receipt。
- [ ] lock生成后的 fresh focused suite 仅 `17/19`：builder 与 direct-CLI 两项测试把“canonical lock不存在”写成永久断言，导致预冻结测试不能在合法终态复验。
- [x] 独立 reviewer 未修改 code/tests/lock、未运行 formal ID，并在 post-lock failure 后立即 NO-GO。

### 结论

FAIL。T087 的科学设计、runner/reducer/entry 与唯一 smoke 证据继续有效，但 SHA=`3942883a...a45a492` 的首个 canonical lock 不能作为 formal authority。D067/CP029只开放测试终态语义与lock重冻修复；formal IDs `30000..30127`继续禁止。

## V043: Ch4 replacement execution lock 终态自洽验收

> date: 2026-08-30
> status: PASS
> 关联: D067–D068 / T088 / S028

### 验证项

- [x] invalid lock存在态先复现`17/19`；两项测试最小修复后独立与主线程fresh均=`19/19`，无skip/xfail、collected仍为19。
- [x] 旧lock只在1674 bytes且SHA exact=`3942883a...a45a492`时删除；lock absent态focused=`19/19`，五文件pycompile、task-control与不可变SHA均PASS。
- [x] freezer direct CLI只成功运行一次；replacement lock SHA=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`，tests SHA=`cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1`。
- [x] lock present态实现者、主线程与独立reviewer fresh均=`19/19`；runner/reducer/entry、manifest、四项dependency、HEAD、environment与populations actual match。
- [x] 两项修复分别验证pure builder与受控direct-CLI不会改变canonical lock bytes、不会留下`.tmp`；独立reviewer另复放受控缺锁分支2/2 PASS。
- [x] 无`.tmp`、checkpoint、formal raw/aggregate/receipt；未重跑ID29999或任何formal ID。

### 结论

PASS，terminal=`CH4_FORMAL_EXECUTION_LOCK_REPAIR_READY`，final P0-P1-P2=`0-0-3`。CP030只开放一次canonical formal raw production；formal reduction、grade、作图与正文仍未授权。

## V044: Ch4 canonical formal raw 独立结构验收

> date: 2026-08-30
> status: PASS
> 关联: D068–D069 / T089 / S028

### 验证项

- [x] pre-run independent gate P0/P1=`0/0`：fresh focused=`19/19`、pycompile5、双锁/HEAD/environment/bound hashes、truth firewall、empty artifact门全部PASS。
- [x] exact `--formal`仅运行一次，exit=0、wall=`409.5s`、stdout=`CH4_FORMAL_PRODUCTION_COMPLETE`；raw SHA=`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`、size=`89,419,500` bytes。
- [x] 独立标准库扫描确认IDs=`30000..30127`、census=`128/384/15232/76160/ref128`，roles/runtime/tau/bits/truth marker exact。
- [x] 2688 namespace、2688 scene-latent hashes、106624 cell-latent关系、15232 H、45696 observation、76160 action hashes、2432 cross-Np groups与128 delta0 exact/no-row全部PASS。
- [x] post-run raw/manifest/lock/bound files SHA前后exact；fresh focused=`19/19`、pycompile5、task-control/diff-check PASS；checkpoint/aggregate/receipt/tmp absent。
- [x] 实现者与reviewer均未运行reducer、未汇总BER/grade、未运行第二次formal。

### 结论

PASS，terminal=`CH4_CANONICAL_FORMAL_RAW_READY`，final P0-P1-P2=`0-0-3`。CP031只开放一次canonical reduction与独立raw-only统计复算；图表、正文和Ch5仍关闭。

## V045: Ch4 首次 canonical reducer 入口验收

> date: 2026-08-30
> status: FAIL
> 关联: D069–D070 / T090 / S028

### 验证项

- [x] pre-run P0/P1=`0/0`，fresh focused=`19/19`、pycompile5、raw/双锁/bound hashes与empty artifact门全部PASS。
- [x] direct reducer只运行一次，exit=1、wall=`4.1s`；失败栈位于`_save_temp()`首次import `projects.simulation.common.save_results`。
- [x] `reduce_raw()`在失败前已于内存完成，故不将其错误标为pre-statistics；没有stdout terminal或canonical artifact。
- [x] aggregate、receipt及二者tmp均absent；raw/manifest/lock与八项bound/dependency共11项hash保持exact。
- [x] 独立无写入probe确认显式`PYTHONPATH=repo;simulation;seam`可import common/core/entry，environment与lock exact，且不改变11项bytes或artifact census。
- [x] 未修改bound code、未重跑reducer/formal、未读取或接收内存统计。

### 结论

FAIL，terminal=`FAILED_PRE_WRITE_IMPORT_PATH`。失败不否定raw或统计合同，但T090未产生canonical artifacts。D070/CP032只开放一次显式PYTHONPATH publication attempt；图表、正文与再次formal仍禁止。

## V046: Ch4 canonical formal statistics 与章节准入验收

> date: 2026-08-30
> status: PASS
> 关联: D070–D071 / T091 / S028

### 验证项

- [x] corrected publication 只执行一次，exit=0、wall=`5.0s`、terminal=`CH4_FORMAL_REDUCTION_ACCEPTED`；aggregate/receipt terminal 与 grade 均合法。
- [x] raw/manifest/execution-lock/aggregate/receipt 五项现场 SHA exact，receipt 内四项 artifact binding exact；无 `.tmp` 残留。
- [x] 独立 reviewer 不导入 runner/reducer，从 raw 重算 570 pooled groups、76 paired-cell comparisons、4 whole-curve comparisons、grade 与 descriptive summaries。
- [x] 与 aggregate/receipt 的 757 个结构/数值节点全部一致，最大绝对数值差=`0.0`；census=`128/384/15232/76160/ref128`。
- [x] C4_FWD 相对 B2_TUNED 的 moderate Np2/Np4 required-SNR gains 分别为 `0.870474 dB` 与 `0.120949 dB`，95% CI lower 均 `>0`；四项 crossing 均 STABLE，whole-curve bootstrap 均 `5000/5000` valid。
- [x] grade=`A`、chapter gate=`true`；fresh focused tests=`19/19`、pycompile、task-control、13 项 bound hashes 与无 tmp 检查全部 PASS。
- [x] 三项 P2 已转为写作 claim ceiling：Np4 小幅、B3 强邻居近等效、混合 summary 不作因果承重。

### 结论

PASS，terminal=`CH4_CANONICAL_FORMAL_STATISTICS_READY`，P0-P1-P2=`0-0-3`。D071/CP033 允许只读提取 canonical 证据并生成正式图表、表格和完整第四章草稿；禁止新增实验、改科学 artifacts 或恢复 Ch5。

## V047: Ch4 formal 图表材料独立验收

> date: 2026-08-30
> status: PASS
> 关联: D072 / T092–T094 / S028

### 验证项

- [x] 独立 reviewer 未导入提取/绘图/runner/reducer，直接遍历 immutable raw 的 `128/15232/76160` 层级并核对 128 个 delta0 exact references。
- [x] 五份 CSV 行数为 `570/4/20/190/30`，共 814 行；key coverage 全，逐字段最大绝对差均 `0.0`，first mismatch 均无。
- [x] B2 formal tau map exact；B3 的 15,232 个逐观测尺度均非固定 1，channel-NMSE semantics 全部为 `pre_calibration_inherited`。
- [x] 提取/绘图 check-only、pycompile、临时目录两次确定性绘图、SVG XML/文本与 PNG 尺寸/非空检查均 PASS；十份图 hash 两次稳定且与 worktree exact。
- [x] raw/aggregate/receipt/manifest/execution-lock 五项 SHA 与 V046 exact；无 simulation tmp/partial/checkpoint。
- [x] 五图、README 与三表的 O1、Np4 小幅、B3、mismatch、Ch3 接口和 B2 参数语义均 PASS。
- [x] 三项 P2 仅为视觉余量、标题限定和两个 `__pycache__` 清理，不改变数字、方法身份或 claim ceiling，已交 T095 收口。

### 结论

PASS，terminal=`CH4_FORMAL_MATERIALS_AUDIT_PASS`，P0-P1-P2=`0-0-3`。允许 T095 更新作者可组织材料卡；继续禁止完整章节正文、总纲改写、新仿真、重归约与 Ch5。

## V048: Ch4 作者可组织材料包终验

> date: 2026-08-30
> status: PASS
> 关联: D072–D073 / T095–T096 / S028

### 验证项

- [x] README 与作者总索引形成双入口；4.1–4.7 每节均有问题、事实、公式、图表、披露和禁止外推项，材料保持卡片/表格/公式/清单形态而非连续正文。
- [x] formal CSV check-only、绘图 check-only、三个生成脚本 pycompile、两个临时目录重复生成、SVG XML、PNG 非空与三张关键图人工视觉检查均 PASS；12 个图文件 byte-stable。
- [x] 四项 headline gain/CI、5–41 dB 网格、工程参考 BER、128 配对簇、导频敏感性、机理与失配反转边界均与 V046/V047 exact。
- [x] 方法角色、B2 tau map、B3 逐观测尺度、O1 truth-only、Np4 小幅、Ch3模块接口/未联合验证和引用层级全部正确。
- [x] 旧 14/18 dB 资产明确标为 historical；作者入口无 Grade/gate/SHA/P0/P1/D/T/CP 或内部 arm code；五项科学 artifact hashes 与 V046 exact。
- [x] T096 两项 P2 已最小修复：主方法短名统一为“前向误差尺度”，Q12 指针改为 M07/E08；独立定向复核无新问题。
- [x] 两个指定 scientific `__pycache__` 已精确删除；无 simulation tmp/checkpoint；未运行仿真、reducer、bootstrap 或文献检索。

### 结论

PASS，terminal=`CH4_AUTHOR_MATERIAL_PACKAGE_PASS`，final P0-P1-P2=`0-0-0`。Ch4 可标记 `CH4_AUTHOR_MATERIALS_READY`；按 D073 停机并等待用户以后取材或另行改变范围。
