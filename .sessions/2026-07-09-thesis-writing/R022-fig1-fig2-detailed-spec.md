# [R022] Fig.1/2 两图详细规格：语义、版式与验收门

> 2026-07-13 | 关联：2026-07-09-thesis-writing / D011 / D012 / R018 / R021
> 2026-07-14 修订 | 关联：D022；Fig.2 控制带升级为正文一致的两层判决

## 调研问题

在 D011 确认“Fig.1 系统总览 + Fig.2 自适应 CPR 机制”后，分别冻结两张图的论点、可见标签、数据/控制流、层级、版式和验收门，避免在绘图阶段再次把系统上下文、估计器细节和结果解释混在一起。本文先写可执行规格；D012 已在规格审阅后选定 SVG，首版源文件与预览见 S013。

## 发现

### 1. 两图共用规格

#### 1.1 目标与边界

- 目标载体：论文/学位论文正文图，不是汇报页或海报；不使用标题横幅、结论式大字、性能口号、参数表或装饰性小图。
- D011 的职责边界：Fig.1 只回答“系统中 CPR 位于哪里”；Fig.2 只回答“自适应 CPR 如何由测量量驱动 DA/NDA 选择并完成补偿”。
- 两图不得各自画出会被误读为两次处理的完整 raw path。Fig.1 用一个 `Adaptive CPR (Expanded in Fig. 2)` 位置标记；Fig.2 再展开机制。
- 原 BER/crossover 图规划顺延为 Fig.3--5，但正文、脚本和文件名的编号联动不在本规格执行。

#### 1.2 共用冻结标签

仅允许从以下标签集取图内文字；长解释放 caption，不把代码变量或结果数字塞进框图。

- 系统标签：`Tx`、`FSO channel`、`Coherent Rx`、`Adaptive CPR`、`Common downstream DSP`。
- 机制标签：`r_k`、`Window power statistics`、`CV < τ_CV?`、`NDA if yes`、`otherwise`、`Blind ĥ_dsp`、`Effective SNR γ̂_eff`、`γ̂_eff < 13 dB?`、`DA if yes · NDA if no`、`Branch command`、`DA estimator`、`NDA estimator`、`Estimator selector`、`θ̂_DA`、`θ̂_NDA`、`Selected θ̂`、`Phase compensation`、`Common downstream DSP`。
- 说明性短标签：`Data path`、`Phase-estimate path`、`Control path`、`Expanded in Fig. 2`。若版面已经能由线型和位置自解释，则不重复放三个 lane 标题。

CV 边界函数、blind-power proxy 公式和 DA/NDA 估计器公式不放入主图；它们属于正文公式清单。图中只显示执行顺序、关键中间量和固定 `13 dB` 比较，避免把 13 dB 决策值误写成观测 crossover 数值。

#### 1.3 共用视觉编码

- **业务数据**：深蓝实线、较粗箭头；表示 `r_k` 的连续主路。
- **相位估计量**：绿色短虚线；表示 `θ̂_DA`、`θ̂_NDA` 和 `Selected θ̂`，只作为侧向补偿量。
- **测量/控制**：橙色点划线；表示 window statistics、CV gate、blind `ĥ_dsp`、effective SNR、固定 13 dB 比较和 branch command 到 selector 的控制关系。
- **判据/路由图元**：CV gate 与 13 dB 比较使用菱形；`Estimator selector` 使用独立六边形；`Branch command` 使用小型中性合流块；DA/NDA 保持同构模块。形状、线型和标签至少保留两种独立编码，颜色只作辅助。
- **容器**：低饱和浅色背景、细边框、无阴影和 3D；容器只表达层级，不承载箭头语义。
- **字体**：正文同族数学字体；目标尺寸下模块标签约 9--10 pt、线旁短标签约 8.5--9 pt；任何允许的单栏裁剪不得把可见文字压到约 7.5 pt 以下。
- **图例**：Fig.2 可放一个紧凑三项线型图例；Fig.1 若只有业务实线和 CPR 位置标记，则不另放大图例，由 caption 解释。

### 2. Fig.1 系统总览规格

#### 2.1 论点

Fig.1 让读者在一次左→右阅读中看到 `Tx → FSO channel → Coherent Rx → Adaptive CPR → Common downstream DSP` 的系统边界，并知道自适应 CPR 的详细机制见 Fig.2。它不解释 DA/NDA 的内部公式、阈值判据或性能结果。

#### 2.2 模块与箭头

- 主链节点按左→右排列：`Tx`、`FSO channel`、`Coherent Rx`、`Adaptive CPR`、`Common downstream DSP`。
- 只保留一条深蓝实线业务链；`Adaptive CPR` 用浅蓝边框或轻量高亮标示，但不在其中嵌套 DA/NDA 方框。
- `FSO channel` 只作为信道边界，不放 Gamma--Gamma 参数、Doppler 数字、湍流等级或 BER 解释。
- 在 `Adaptive CPR` 旁放短标签 `Expanded in Fig. 2`，用细连接器或编号标记，不再画第二条数据链。
- 不显示 pilot insertion、mapper、crossover、`~13 dB`、`BER waterfall`、训练/推理泳道或仿真配置。

#### 2.3 布局与版式

- 首轮目标为低密度单栏宽度约 3.5 in 的紧凑横向图；若 `FSO channel` 或 `Common downstream DSP` 标签在目标尺寸下拥挤，再升级为双栏通宽约 7.16 in。是否升级由缩小检查决定，不凭画布余量决定。
- 画布保持约 2.4--3.0:1 的横向比例；模块间留白优先于增加子模块。
- 只使用一层容器，不做系统→receiver→unit 三级拼贴；父级—局部关系由 `Adaptive CPR` 与 `Expanded in Fig. 2` 连接表达。
- 阅读顺序只有一条：左→右主链，caption 解释 CPR 位置；不设置上下并列面板或反馈环。

#### 2.4 Fig.1 caption 分工

Caption 只说明：系统从 Tx 经 `FSO channel` 到 coherent receiver，再进入 adaptive CPR 和 common downstream DSP；CPR 内部机制在 Fig.2 展开。Caption 不解释阈值数值、crossover 或任何 BER 结果。

#### 2.5 Fig.1 验收门

- 缩小到约 3.5 in 时，五个主模块和主箭头仍一眼可读；否则改用双栏或缩短标签，不增加细节。
- 主链没有折返或跨越文字的箭头；`Adaptive CPR` 只出现一次，不含隐藏的第二套处理链。
- 读者不看 caption 也能识别系统边界；看 caption 后不会误以为 Fig.1 已经展示 selector 机制。

### 3. Fig.2 自适应 CPR 机制规格

#### 3.1 论点

Fig.2 解释同一接收输入如何同时支持两条候选估计路径，并由两层控制规则驱动一次性 selector：第一层以 window-power CV gate 直接产生 NDA 命令；其余窗口进入 blind `ĥ_dsp`、effective-SNR 与固定 13 dB 比较，产生 DA/NDA 命令。最后把选中的相位估计量侧向注入公共 phase compensation。业务数据本身不经过 selector，候选估计器仍为并行结构，不存在 DA 失败后再运行 NDA 的 early-exit 语义。

#### 3.2 三层信息结构

采用同一画布的三条语义带，不使用等权拼贴：

1. **中部主数据带**：`r_k` → `Phase compensation` → `Common downstream DSP`，深蓝实线连续贯通。
2. **上部估计器带**：同一 `r_k` 在显式分叉点复制到 `DA estimator` 与 `NDA estimator`；两者输出 `θ̂_DA`、`θ̂_NDA`，绿色短虚线汇入 `Estimator selector`。
3. **下部控制带**：从同一输入旁路到 `Window power statistics`，进入 `CV < τ_CV?` 第一层判据；yes 路径直接生成 NDA 命令，otherwise 路径依次进入 `Blind ĥ_dsp / Effective SNR γ̂_eff` 组合块和 `γ̂_eff < 13 dB?` 第二层判据。两层结果在 `Branch command` 合流后，以橙色点划线驱动 `Estimator selector`。外部仍只保留一条控制带输入和一条到 selector 的上行控制线。

`Estimator selector` 输出 `Selected θ̂`，以绿色短虚线从侧面进入 `Phase compensation`；深蓝 raw path 不在 selector 处断开。三条带应通过空间位置、线型和短标签共同表达，不能只靠颜色。

#### 3.3 具体布局

- 默认按双栏通宽约 7.16 in 验收；画布比例约 2.0--2.5:1。单栏版本不是当前主图目标，只有在裁剪后仍满足字号/箭头门时才可作为局部复用。
- `r_k` 和主数据带位于垂直中心；上部估计器带左右对齐，DA/NDA 两块同宽同高；下部控制带与 selector 垂直对齐，避免长折返线。
- `Phase compensation` 是主链唯一接受 `Selected θ̂` 的公共补偿模块；`Common downstream DSP` 只接收补偿后的业务数据，不再重复画 DA/NDA。
- 第二层判据明确标 `γ̂_eff < 13 dB?`；13 dB 是接收机固定决策参数，不是 10.7/16.9/18.0 dB 的观测 crossover。图中不列 CV 系数、margin、proxy floor 或完整公式。
- 不加入频谱、星座、相位轨迹、训练过程、硬件存储或参数表；若需要说明 pilot/非 pilot 语义，放 caption 或正文，不扩展图内节点。

#### 3.4 Fig.2 caption 分工

Caption 必须解释三种线型/职责：深蓝实线是 raw data path，绿色虚线是 phase estimate，橙色点划线是 measurement/control。Caption 说明控制器先执行 CV gate；其余窗口再计算 blind `ĥ_dsp` 与 `γ̂_eff` 并使用固定 13 dB 比较，最终选择 `θ̂_DA` 或 `θ̂_NDA`；同时明确 raw data bypass selector 进入 phase compensation。Caption 不写 crossover 观测值、不承诺“局部最优”或任何性能增益。

#### 3.5 Fig.2 验收门

- 从 `r_k` 到 `Common downstream DSP` 的深蓝主链可连续追踪；selector 只出现在估计量侧路。
- DA/NDA 两个候选必须共享同一输入分叉点，且输出各自可追踪到 selector；不能画成串联 exit/continue。
- `Window power statistics → CV gate → {direct NDA / blind ĥ_dsp → γ̂_eff → 13 dB comparison} → Branch command → Estimator selector` 的控制方向单向、独立于 raw 主链；两个判据、合流命令、selector 和候选模块职责可区分。
- 缩小到约 7.16 in 目标宽度时，模块标签、`θ̂`、`CV`、`ĥ_dsp`、`γ̂_eff`、`13 dB` 和三类线型仍可读；若不可读，先删解释性 caption-like 标签，不删两层判决节点、不增加独立面板。
- 黑白打印/去色后仍能凭线型、形状和位置区分三类关系；图例不能成为唯一语义来源。

### 4. 两图之间的接口与编号

- Fig.1 的 `Adaptive CPR` 是 Fig.2 的唯一入口；Fig.2 的 `Common downstream DSP` 与 Fig.1 的同名终端模块语义对应，但两图不复制完整内部链。
- 两图 caption 分工：Fig.1 讲系统边界，Fig.2 讲机制；正文首次引 Fig.2 时说明它是 Fig.1 中 CPR 模块的展开。
- 原 BER/crossover 图整体顺延为 Fig.3--5；编号、脚本、文件名和正文引用在后续联动批次统一处理，本规格不改它们。

## 结论

R022 将 D011 的两图拆分转成可执行规格：Fig.1 是低密度系统总览，Fig.2 是双栏优先的 receiver-local 自适应 CPR 机制图。两图共享 raw-data/estimate/control 的冗余编码和“不重复 raw path”门槛，但不共享内部细节。D022 根据当前 CCISP 正文和实现，把 Fig.2 的旧单层 `γ_blk → γ_th` 控制链升级为 CV gate 与 blind-`ĥ_dsp`/effective-SNR/13 dB 两层判决；三泳道、并行候选、raw bypass 与 selected-estimate 侧向注入保持不变。D013 已确定 draw.io 为编辑源，SVG/PDF 为交付，PNG 仅作预览；最终 caption/正文联动仍待后续。

## 对决策的影响

D022 取代本文件旧的 Fig.2 单层控制条款，不改变 D011 的两图职责、D017 的语义图元门或 D013 的 draw.io 交付合同。旧 `projects/simulation/figures/fig1_system_block.svg` 保持不改。Fig.2 更新后必须刷新 Fig.1 v5 内嵌的完整 Fig.2 thumbnail；caption、正文图号联动和最终落版仍由 CCISP 主控另行处理。
