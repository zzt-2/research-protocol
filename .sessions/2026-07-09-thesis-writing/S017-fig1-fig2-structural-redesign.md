# [S017] Fig.1/Fig.2 结构重设计规格：总览—局部层级与机制密度

> 2026-07-13 | 视觉结构重设计 | 语义版 Fig.2 原型已生成并通过独立审查，Fig.1 待迁移
> 2026-07-14 续接 | Fig.1 证据审计与单原型实施
> 2026-07-14 收尾 | Fig.1 v4 语义、结构、目标尺寸视觉独立审查 PASS

## 目标

针对 S016 六版“语义正确但结构过于简单”的反馈，重新定义 Fig.1/Fig.2 的信息架构：从“模块排列的风格变体”转为“总览—局部层级 + 内容承载型机制图”。先落一版 Fig.1 和一版 Fig.2 原型，经视觉审查后再考虑变体。

## 记录

### 1. 已验证的结构缺口

- S016 的 Fig.1 三版本质都是五个主模块加不同外框/色带，没有父级—局部层级、语义微缩图或内部结构。
- S016 的 Fig.2 三版虽然区分 raw/estimate/control，但主要仍是三条空泳道和若干独立方框，缺少重复候选处理列、决策中心和阶段节奏。
- 本地参考语料中的 B1-01/B1-02 以“宏观系统 + 关键局部放大”制造层级；B2-02/B2-04 以重复阶段、判据节点和反馈关系承载机制；B3-01 以共享输入/输出、候选流和控制器形成工程密度。
- 因此，当前问题不是颜色或 renderer，而是把 R022 的“无关细节减法”误执行成“有意义结构也减掉”。

### 2. Fig.1 v3 结构

采用“系统总览 + CPR 局部放大”两尺度构图：

- **主系统带**：保留 `Tx → FSO channel → Coherent Rx → Adaptive CPR → Common downstream DSP` 的单向主链，作为第一阅读顺序。
- **CPR zoom**：从 `Adaptive CPR` 位置引出一个有明确父级锚点的局部卡片，展示一层机制预览：`r_k`、`DA estimator`、`NDA estimator`、`Estimator selector`、`Phase compensation`。
- **重复控制**：zoom 不放公式、阈值数值、BER、crossover、频谱或星座；完整 `γ_blk → γ_th → selector` 关系留在 Fig.2，避免两图变成同一张图的复制品。
- **身份连续**：zoom 使用与主链相同的 `Adaptive CPR` 身份标记，并用 `Fig. 2` 作为展开入口；不生成第二条完整业务 raw path。
- **视觉层级**：主系统带低饱和、低对比；CPR zoom 使用略高的边框/底色和局部连接线，但不使用阴影、渐变或 3D。

### 3. Fig.2 v3 结构

采用“共享输入 + 候选处理列 + 决策中心 + 公共补偿”的 receiver-local 机制图：

- **左侧共享输入**：`r_k` 进入一个明确分叉点，深蓝 raw data spine 连续贯穿到 `Phase compensation` 和 `Common downstream DSP`。
- **中部候选列**：DA/NDA 不再只是两个盒子，而是上下同构、左右对齐的候选处理列；两列各自输出 `θ̂_DA`/`θ̂_NDA`，再汇入单一 `Estimator selector`。
- **决策中心**：`Estimator selector` 作为唯一中心判据/路由节点，输出 `Selected θ̂`；不画 early-exit 或串联“DA 失败再 NDA”的误导结构。
- **控制平面**：`Per-block SNR measurement → Fixed SNR threshold γ_th → Estimator selector` 与 selector 垂直/近邻对齐，避免长距离回折和无标记穿越。
- **右侧公共后级**：`Selected θ̂ → Phase compensation → Common downstream DSP`，明确估计量侧向注入、业务数据不经过 selector。
- **轻量图例**：保留紧凑三项线型图例：raw data、phase estimate、measurement/control；图例不扩展成说明面板。

### 4. 装饰边界

- 允许少量低饱和底色、细分组框、阶段编号/小型连接标记，用来强化层级和阅读顺序。
- 禁止把波形、星座、频谱、图标、3D、渐变或密集反馈线当成装饰堆入图中。
- 任何新增小图元必须能回答“它表达输入、候选、判据、选择、补偿中的哪一项”；回答不了就不画。
- 可见标签仍以 R022 冻结标签为主；未在冻结清单中的新术语先不写入图内。

### 5. 组合节点语法（用户确认后实施）

- **处理器卡**：`DA estimator` / `NDA estimator` 采用同构外壳，包含共享输入端、3 个无标签阶段条和估计输出端；阶段条只表达重复处理级，不引入新的算法名。
- **选择中枢**：`Estimator selector` 采用六边形外壳、内部核心和 DA/NDA/Control/Selected 四类接口，表达候选汇聚与控制判据。
- **补偿算子**：`Phase compensation` 采用数据主干输入/输出与 `Selected θ̂` 侧向注入端，避免把估计流误画成数据串行链。
- **测量/阈值卡**：`Per-block SNR measurement` 使用无刻度 block meter；`Fixed SNR threshold γ_th` 使用带内部阈值标记的比较卡。
- **共同约束**：内部最多一层小结构；低饱和填充；无渐变、阴影、3D、波形、星座或频谱装饰。组合图元必须对应输入、候选、判据、选择或补偿中的一种语义。

### 6. 实现与审查记录

- 新增 `projects/simulation/figures/fig1_system_overview_v3.drawio/.svg/.pdf/.png`：主链与 CPR zoom 的父子锚点保留，draw.io 源补齐 mini CPR 的分叉、候选、selector 和 phase 连接。
- 新增 `projects/simulation/figures/fig2_adaptive_cpr_v3.drawio/.svg/.pdf/.png`：DA/NDA 组合处理器卡、selector 中枢、测量卡、阈值卡和端口化补偿算子均可编辑；控制线在 raw bridge 处拆段留白。
- 确定性检查：两份 draw.io XML 可解析；Fig.1 62 vertices/18 edges，Fig.2 69 vertices/19 edges；源文件禁语义扫描无命中；PDF 均为 7.16 in 宽（Fig.1 3.49 in 高，Fig.2 3.33 in 高）；Fig.2 PNG 2148×999 且无 `Text is not SVG` 残留。
- 独立审查先发现并推动修复了 Fig.1 源—SVG 内部边不同步和 Fig.2 控制线交点；修复后 Fig.1 组合边已同步，Fig.2 几何断口已验证。最终审美仍留给用户审阅，不在本记录中替代用户拍板。

### 7. A+C 形态板

- 用户指出 v3 的箭头过重、连接器不顺、所有节点都复用“框内短条”装饰，要求参考 B1-01/B2-04/B3-01 的多图形语法；用户确认先做形态板再改整图。
- 新增 `projects/simulation/figures/fig1_fig2_motif_board_v1.drawio/.svg/.pdf/.png`，并列展示：层叠长矩形、嵌套 CPR mini、外部括号、DA/NDA 并行轨道、Selected θ 侧向注入、block meter/threshold ruler、连接器尺度。
- 独立审查结论：形态覆盖 PASS，仍同质化 PARTIAL。下一轮应至少把候选处理和补偿算子改成非卡片式（层叠片、窗口化 mini、主干+侧口），不要把板上的短横条和大箭头直接复制到最终图。
- 形态板是词汇验证板，不是最终 Fig.1/Fig.2；draw.io 中部分线目前是无 source/target 的手工 polyline，不能直接当最终连接器模板。

### 8. 原型门控

单原型完成后，独立审查必须逐项检查：

1. Fig.1 主系统带和 CPR zoom 的父子身份是否一眼可追踪。
2. Fig.1 zoom 是否只提供结构预览，没有复制 Fig.2 的完整数据/控制链。
3. Fig.2 的 DA/NDA 候选是否同构、并行、可追踪到 selector。
4. raw、estimate、control 三类流向是否由颜色之外的线型/位置/形状冗余编码。
5. 缩小到目标论文尺寸后，主链、候选列、selector、`θ̂`、`γ_blk`、`γ_th` 和图例是否仍可读。
6. 装饰是否只强化层级，没有制造新的技术含义或视觉噪声。

### 9. 用户纠偏后的语义版 Fig.2 原型

用户明确否决把形态板继续作为设计基础：问题不是图案数量，而是图元没有对应真实语义。参考图的可迁移规则被收窄为“语义—形状映射”：

- DA/NDA 使用层叠处理片表达重复处理阶段；
- `Estimator selector` 使用六边形表达候选汇聚/路由；
- `Per-block SNR measurement` 使用表盘/测量端口表达测量；
- `Fixed SNR threshold γ_th` 使用菱形表达判据；
- `Phase compensation` 内部使用相位旋转符号，并保留 `Selected θ̂` 侧向端口；
- `Common downstream DSP` 使用层叠后级片表达公共处理链；
- 深蓝实线、绿色短虚线、橙色点划线分别承载 raw data、phase estimate、measurement/control，颜色之外由线型、位置和图元冗余编码。

原型文件：`projects/simulation/figures/fig2_adaptive_cpr.svg`，预览：同名 `.png/.pdf`。独立审查确认 raw 主链、DA/NDA 并行、`γ_blk → γ_th → selector`、`Selected θ̂` 侧向注入均正确；控制线 crossover 采用白色断口避免 junction 误读；测量表盘两侧已补齐端口连接；PDF 无裁切/乱码，V005=PASS。该 SVG 仍是语义视觉原型，不重新拍板 D013 的最终编辑源路线。

### 10. 背景泳道与论文原生图元修订

用户进一步澄清：不要独立图例，而要由三块横向淡色背景直接承担 `Phase-estimate path`、`Data path`、`Control path` 的空间分区。对本地论文图的复核显示，测量通常使用旁路 estimator/measurement 矩形，相位补偿通常使用主链矩形并由估计量侧向输入；表盘和循环箭头缺乏论文工程图依据。

据此局部修改 `projects/simulation/figures/fig2_adaptive_cpr.svg/.png/.pdf`：删除底部图例、测量表盘和相位循环箭头；加入三条低饱和背景带；`Per-block SNR measurement` 改为单一旁路处理块，`Phase compensation` 改为普通主链处理块并保留顶部 `Selected θ̂` 端口。初版曾尝试三张小叠片表示 sample block，但独立审查确认它也可能被误读为 buffer/packet queue/repeated frames，且标签本身已表达 per-block，故删除。复核同时发现旧白色 mask 使 raw spine 视觉断开，现改为橙色 control connector 在交叉处留 20 px 断口，深蓝 raw spine 连续无遮挡。V006=PASS；仍待用户审美拍板，不迁移到 Fig.1。

### 11. Fig.2 正式 draw.io 编辑源

用户要求泳道无间隔，并指出 SVG 手工折线不够横平竖直；同时明确本轮只做 Fig.2，Fig.1 留待讨论粗稿。新建 `projects/simulation/figures/fig2_adaptive_cpr.drawio` 作为正式编辑源，并由本机 diagrams.net 直接导出同名 `.svg/.pdf/.png`：三条背景带在 `y=320`、`y=450` 精确相接，间隔均为 0；12 条语义边全部绑定 source/target 且使用 `orthogonalEdgeStyle`；节点、背景、端子和 waypoint 均可在 draw.io 中手工调整。

独立审查首轮发现 `Selected θ̂` 与 control 共享局部竖轨，以及最右输出箭头回折。修复后两条竖轨间距 20 px；输出端改为独立可编辑三角端子，连接边不再回折。复核 V007=PASS。当前仅有非阻断观察：橙色控制竖线距 `Data path` 标签较近，用户可在 draw.io 中直接微调。

### 12. Fig.1 事实审计与失败回溯

主线曾把参考图中的双偏振 X/Y 链带入 Fig.1 讨论，但项目正文与正式仿真器只实现单个复基带序列 `s_k → r_k`，没有双偏振数据结构、Jones 矩阵或偏振解复用。问题根因是跳过 Semantic Brief，直接从参考图迁移器件/结构，违反 D017 与 Semantic Primitive Evidence Gate。

权威源核对结果：

- `system_model.tex` 冻结 `(8,8)-16APSK`、`r_k = sqrt(h_b)s_k exp(jφ_k)+n_k`、Gamma--Gamma 块衰落、残余频偏、线性 Doppler、Wiener 激光相位噪声和复 AWGN。
- `system_model.tex` 冻结两种分区：`N_ch=100` symbols 的 atmospheric channel block，以及 `N_DSP=256` samples 的 DSP window。
- `method.tex` 冻结 Fig.2 负责 DA/NDA、窗口统计与 branch selection；Fig.1 不复制这些内部控制关系。
- DAC、激光器、调制器、90° hybrid、TIA、ADC 和双偏振均无当前系统源证据，不进入 Fig.1。

### 13. Fig.1 Semantic Brief（D018）

**论点**：在一条连续复基带主路上解释发送信号、三类信道作用、接收信号和载波恢复位置；同时显示信道块与 DSP 窗两种真实时间尺度。Fig.1 回答“系统信号如何形成、受什么作用、CPR 在何处”，Fig.2 回答“自适应 CPR 如何选择”。

**冻结主链**：`Information bits → (8,8)-16APSK modulation → s_k → FSO channel model → r_k → Adaptive carrier recovery → 16APSK demodulation → Detected bits`。`r_k` 已是离散复基带观测，不另画无模型依据的 coherent-reception 前端块。

**冻结扰动职责**：

- `h_b(k)`：Gamma--Gamma irradiance block fading，以乘性幅度项 `sqrt(h_b(k))` 进入信号模型；
- `φ_k`：由 residual frequency offset、linear Doppler 和 Wiener laser phase noise 组成，以 `exp(jφ_k)` 进入信号模型；
- `n_k`：complex AWGN，以加性项进入接收信号。

**箭头分类**：主链为 data/signal flow；三类扰动到信道算子的连接为 impairment injection；`Expanded in Fig. 2` 为 cross-figure reference，不是信号或控制流；两种分区只做 scale annotation，不使用箭头。

**允许的非文字图元及证据**：

- two-ring 16APSK constellation：来自 `(8,8)-16APSK` 源机制；
- piecewise-constant block strip：来自 `h_b(k)` 在 100-symbol channel block 内恒定；
- within-window tick axes：来自单次正式仿真实现的 256-sample DSP window，以及其中 `100+100+56` 的 Gamma--Gamma channel blocks；只表达窗内尺度，不声称跨 DSP window 连续。

**禁止项**：双偏振、器件级相干接收链、DA/NDA/selector/CV/threshold mini、BER/crossover/结果数字、装饰性频谱/星座云、仪表盘、循环箭头和无含义短线。

### 14. 单原型实施计划与否决条件

**假设 H1**：把 Fig.1 从五框位置图升级为“信号模型主链 + 三类扰动注入 + 双时间尺度注释”，能在不重复 Fig.2、不虚构硬件的前提下提高信息密度。

**实施切片**：只生成 `fig1_system_model_v4.drawio` 一个原型；验证后从同一源导出 SVG/PDF/PNG。旧版本不覆盖。

**布局规格**：宽幅论文图；连续的 Transmitter / Atmospheric FSO channel / Coherent receiver DSP 三个语义区域；主链保持左到右；信道区域集中承载公式与三类注入；接收区域只显示 carrier-recovery 位置与 demodulation；两条分区带置于主链下方并错位对齐，不充当图例。

**否决条件**：任一可见图元无源机制；双时间尺度被误读为数据缓存/队列；主链不能一眼连续追踪；Fig.1 出现 Fig.2 的 selector/control 机制；目标双栏宽度下公式或标签不可读；独立审查判定信息密度仍主要来自装饰而非机制。任一成立即不进入风格扩展。

### 15. Fig.1 v4 实施与验证结果

- 新增 `projects/simulation/figures/fig1_system_model_v4.drawio`，并从同一 diagrams.net 源导出 `.svg/.png/.pdf`。PDF 作为论文出版物，draw.io 作为人工整理源，PNG 作为预览。
- 三个连续背景区分别承载 Transmitter、Atmospheric FSO channel、Coherent receiver DSP；主链不含双偏振、DAC/laser/hybrid/TIA/ADC 或独立 coherent-reception 前端。
- 信道区仅使用有源机制的组合图元：two-ring 16APSK、Gamma--Gamma block strip、三类 impairment injection、接收公式，以及单个 256-sample DSP window 内 `100+100+56` 的 channel-block 刻度。
- 独立语义审查首先发现“跨两个 DSP windows 连续”的图示与正式仿真每 256 samples 重新生成 realization 不一致；未扩大范围修改代码，而是把尺度图收缩到一个 DSP window，从而关闭契约问题。
- 最终 draw.io 验证为 72 cells / 8 bound orthogonal edges / 0 error / 0 warning；7.16 in 目标宽度 PDF 重渲染可读。独立语义审查与独立视觉审查均为 PASS，Critical/Important 均为 0。

### 16. Fig.1 v5 真实微型图设计与实施计划（D019）

**失败诊断**：v4 的外部信息架构已通过，但节点内部仍依赖人工简笔 shape 与偏长文字；既有 QA 缺少“内部视觉是否为真实科研对象”的绝对锚点，属于 M3 评估维度盲区。

**资产契约**：一次调用正式 `generate_shared_realization_apsk`，固定 `N=256`、`SNR=15 dB`、`scene=moderate`、`seed=2000`，从同一 realization 取得 `tx/h/phi/rx_raw`，并反算实际 noise。16APSK 点与判决区域分别通过公开 `m16apsk_mod/m16apsk_demod` 生成。参数只用于可复现的机制缩略图，不作为论文结果数字。

**五类真实微图**：

1. modulation：实际 `(8,8)-16APSK` 16 点星座；
2. block fading：实际 256 样本窗口内 `100+100+56` 的 `h_k` 阶梯轨迹；
3. carrier phase：同一 realization 的总 `phi_k` 轨迹，不拆分或放大分量；
4. AWGN：从接收信号精确反算的 complex-noise I/Q 样本云；
5. demodulation：由实际 demodulator 网格计算的判决区域与 16 个星座点。

CPR 初始设计是不再自画 mini，而使用现有 Fig.2 的真实缩略预览；目标尺寸验证后由 D020 否决：完整 Fig.2 压进小节点只剩不可读纹理。最终保留中性 `Adaptive carrier recovery` 原生块与 `Detailed in Fig. 2`，不为“每个节点都必须有图”牺牲可读性。其余微图无内部文字、图题、图例和坐标刻度。

**文件与任务**：

- 新建 `projects/simulation/figures/fig1_v5_assets/generate_assets.py`，输出紧裁切 SVG/PNG 和 manifest；确定性测试检查点数、块边界、噪声重构误差和输出文件。
- 新建 `projects/simulation/figures/build_fig1_system_model_v5.py`，从 v4 复制布局，删除旧简笔 cells，内嵌 data-URI 微图，标签与8条语义边继续使用原生 cell/anchor。
- 生成 `fig1_system_model_v5.drawio/.svg/.png/.pdf`，运行 draw.io validator、data-URI/本地路径扫描、PDF 目标尺寸重渲染，再由独立语义 reviewer 与视觉 reviewer 分开验收。

**退出判据**：任一微图不是实际模型输出；缩小后只剩“纹理”而无法识别技术角色；缩略图内出现不可读小字；data URI 外链本地路径；主链边失去绑定；或独立审查出现 Critical/Important，即停止并局部返工，不扩展到 Fig.2。

### 17. Fig.1 v5 实施与验证结果

- 真实资产生成器使用同一个 `N=256`、15 dB、moderate、seed 2000 realization，生成双环16APSK、`100+100+56` block fading、总 carrier-phase 轨迹、complex-AWGN I/Q 云和实际 demodulator 判决区；这些参数在 manifest 中明确标为 mechanism-only，不是论文结果。
- 首次 draw.io 组装暴露 `data:image/...;base64,...` 被 style 分号截断的 broken-image 缺陷；通过回归测试改为无裸分号 data URI 后关闭。
- 完整 Fig.2 CPR thumbnail 在目标尺寸只剩纹理，按 D020 删除；CPR 最终保留两行短标签和 `Detailed in Fig. 2`。
- 最终产物为 `fig1_system_model_v5.drawio/.svg/.png/.pdf`；结构计数 61 cells / 8 bound orthogonal edges / 5 embedded images / 0 errors / 0 warnings。
- 两份聚焦测试联合 14 PASS；独立资产审查、builder 审查、目标尺寸视觉复审和最终全量 reviewer 均 PASS，Critical/Important 为 0。V009 记录完整证据。

### 18. 用户审美覆盖与 v5 局部重构计划（D021）

用户在审阅 v5 后明确提出两项覆盖：中央不保留公式；完整 Fig.2 必须压入 CPR 节点，即使不可读。中央节点方案在纯文字框、人工叠片与真实受损星座之间选择后，用户确认真实受损星座。

**冻结改法**：

- `channel_model` 继续作为三类 impairment injection 和主链的语义锚点，但其值清空；加入原生短标签 `Composite FSO channel`。
- 资产生成器从同一 realization 的 `rx_raw` 生成无文字 `received_signal.svg`，作为 fading、phase、AWGN 联合作用后的真实视觉结果；不另跑实验、不引用结果数字。
- CPR 恢复完整 `fig2_adaptive_cpr.png` thumbnail。该图在 Fig.1 中只承担“这里展开为 Fig.2”的视觉索引，用户明确接受内部小字不可读；外部标题和 `Detailed in Fig. 2` 仍保持可读。
- 三背景区、时间尺度、主链几何和8条绑定正交边不变。

**TDD 与验收**：先让资产测试因缺 `received_signal.svg` 失败，再实现；随后让 builder 测试因公式仍存在、中央图缺失和 CPR thumbnail 缺失而失败，再实现。最终检查中央无接收公式、7个内嵌图像、无外部路径、8条绑定边、同源PDF/PNG/SVG及目标尺寸预览。

### 19. D021 实施与验证结果

- 资产生成器从原有 shared realization 的 `rx_raw` 生成 `received_signal.svg`；manifest 明确标记 `mechanism-only figure asset` 与 `paper_result: false`。
- 中央信道节点改为原生短标签 `Composite FSO channel` 与真实受损星座；接收公式不再出现在 vertex 文本中。
- CPR 节点恢复完整 Fig.2 的非白边界裁切；内部内容逐像素保留，外部标题、缩略图和 `Detailed in Fig. 2` 三层互不重叠。
- 首次目标尺寸复审发现三条扰动注入标签被竖线/箭头干扰；根因为 edge label 使用默认路径位置。通过显式 relative position 与 offset 局部修复，未改变术语、拓扑或 D021 内容。
- 最终联合测试 18 PASS；draw.io validator 为 64 cells / 8 bound orthogonal edges / 7 embedded images / 0 errors / 0 warnings；独立最终视觉复核 PASS。完整证据见 V010。

### 20. Fig.2 两层控制语义修订计划（D022）

CCISP 内容补强后的 Method 已把 selector 明确为两层规则，而当前 Fig.2 仍是 R022 旧版 `Per-block SNR measurement → γ_blk → Fixed SNR threshold`。用户已手工微调现有 draw.io 连线，故本轮冻结“只改 Control path、不重建全图”。

**最小结构**：`Window power statistics` 进入 `CV < τ_CV?`；yes 直接形成 NDA command，otherwise 进入 `Blind ĥ_dsp / Effective SNR γ̂_eff` 组合块，再进入 `γ̂_eff < 13 dB?`，两层结果汇入 `Branch command` 后沿现有上行控制方向驱动 selector。外部 DA/NDA、raw spine、selected estimate、phase compensation、downstream DSP 与三背景带保持。

**验证门**：TDD 首先锁定用户现有非控制边签名并要求新两层节点/边；RED 后只修改 draw.io Control path。导出后检查正文两层术语、全部绑定正交边、无假 junction/穿字、目标 7.16 in 可读；独立 reviewer 通过后刷新 Fig.1 v5 thumbnail。

### 21. D022 实施与验证结果

- T001 已完成；报告曾写入 `projects/simulation/worker-tasks/fig2-two-layer-control-report.md`，验收证据汇总到 V011。
- RED 为 1 PASS / 4 FAIL；局部修改后 Fig.2 聚焦测试 5 PASS，最终与 Fig.1 资产/联动测试合计 23 PASS。
- Fig.2 为 49 cells / 17 bound orthogonal edges / 0 errors / 0 warnings；用户 9 条非控制边签名全部保持。
- 首次导出发现 branch→selector 竖轨穿过 downstream、控制标签重叠；只调整 Control path 局部路由后关闭，未移动上部估计器或中部 raw path。
- Fig.1 v5 已重新嵌入更新后的完整 Fig.2 thumbnail；两图 draw.io/SVG/PNG/PDF 均重新生成。独立语义/结构与目标尺寸视觉 reviewer 均 PASS，Critical/Important 为 0。

## 决策引用

- D016：Fig.1/Fig.2 从简单模块链重构为总览—局部层级与机制密度图（新建）。
- D017：形态板不作为最终设计基础；先以语义版 Fig.2 单原型过门，再迁移到 Fig.1（新建）。
- D018：Fig.1 改为端到端信号—扰动—时间尺度系统图，禁止无依据双偏振/器件链（新建）。
- D019：Fig.1 v5 保持外部架构不变，节点内部改用项目真实模型微型图（新建）。
- D020：否决在 CPR 节点内硬缩完整 Fig.2；该节点保留中性短标签与跨图引用（新建）。
- D021：用户覆盖 D020；中央公式改为真实受损星座+短标签，并恢复完整 Fig.2 thumbnail（新建）。
- D022：Fig.2 保留现有三泳道和用户连线微调，仅把 Control path 升级为 CV—blind-h/effective-SNR—13 dB 两层判决（新建）。
- D013：draw.io 编辑源、SVG/PDF 交付格式。
- R020/R021/R022：参考图型、候选架构、语义不变量与缩小验收门。

## 范围确认

- 本轮是否在 scope boundary 内：是。仍只处理 Fig.1/Fig.2 结构和视觉原型；不跑实验、不改正文、不做 Fig.3--5、不进入 LaTeX 投稿工程。

## 后续

- D022/T001 已完成并由 V011 验证；等待用户审阅两图成品。论文引用切换、caption 和最终编译由 CCISP 内容补强主控处理。
