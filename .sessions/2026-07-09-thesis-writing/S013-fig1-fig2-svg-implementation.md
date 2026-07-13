# [S013] Fig.1/Fig.2 SVG 首版实现与视觉验收

> 2026-07-13 | 实施与验收阶段 | 进行中

## 目标

将 R022 冻结的两图语义落成可编辑论文图源，并在目标尺寸与黑白条件下检查数据流、估计流、控制流、文字和线型是否可读；不修改旧 `fig1_system_block.svg`，不进入正文图号联动。

## 记录

### 1. 实施选择

- 依据 D012，采用两份独立 SVG 源文件：
  - `projects/simulation/figures/fig1_system_overview.svg`
  - `projects/simulation/figures/fig2_adaptive_cpr.svg`
- 同步生成矢量 PDF 和 PNG 预览；PNG 只用于视觉验收，不作为正式图源。
- 旧 `projects/simulation/figures/fig1_system_block.svg` 未修改。

### 2. Fig.1 事实检查

- 主链为 `Tx → FSO channel → Coherent Rx → Adaptive CPR → Common downstream DSP`，只有一条深蓝业务实线。
- `Expanded in Fig. 2` 作为 CPR 局部展开提示，不嵌入第二套处理链。
- 在约 3.5 in 目标宽度预览中，五个模块、箭头和短标签仍可辨；没有参数、BER、crossover 或训练文字。

### 3. Fig.2 事实检查

- `r_k` 深蓝主路连续经过 `Phase compensation` 到 `Common downstream DSP`，不经过 selector。
- DA/NDA 从同一 raw 输入并行分叉，分别输出 `θ̂_DA`/`θ̂_NDA`，再由 `Estimator selector` 产生 `Selected θ̂`。
- 下部控制路为 `Per-block SNR measurement → γ_blk → Fixed SNR threshold γ_th → Estimator selector`，与 raw 主路独立。
- 线型同时表达三类关系：深蓝实线 data、绿色虚线 phase estimate、橙色点划线 control；去色预览仍可区分。
- 数学符号改为可控的路径/分文本渲染，避免帽号和下标在转换器中变成方块或字面下划线。

### 4. 视觉验收

- 使用 Edge 3.125×无头渲染检查颜色版与黑白版，并用 CairoSVG 导出矢量 PDF；最新 PNG 约为 300 dpi（Fig.1 1050×419、Fig.2 2150×1094），箭头、虚线/点划线和公共后级接口可追踪。
- Fig.2 阈值菱形已放大，`γ_blk` 移到 measurement 输出连接器上方，避免与菱形文字重叠。
- 尚未做最终 caption、正文图号和投稿版面联动；这些不在本轮首版实现中。

## 决策引用

- D011：Fig.1 系统总览 + Fig.2 自适应 CPR 机制两张独立编号图。
- D012：采用 SVG 作为可编辑图源，PNG 仅作预览（新建）。
- R022：两图语义、标签、线型与缩小验收门。

## 范围确认

- 本轮是否在 scope boundary 内：是。属于写作专题的图表准备与视觉验收；未跑实验、未进 Contract、未写正式论文章节、未改旧 SVG。

## 后续

- 由独立 verifier 复核源文件标签、数据/控制流、旧 SVG 未改、专题记录同步和预览存在性。
- verifier 通过后，再处理 caption、正文图号联动和是否需要最终双栏落版；本轮不决定 Fig.3--5 的脚本/编号联动。
