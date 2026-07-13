# [R021] Fig.1 信息架构候选与综合 critic

> 2026-07-13 | 关联：2026-07-09-thesis-writing / D010 / S012 / R020

## 调研问题

在 R019 的样图语料和 R020 的视觉语法基础上，Fig.1 可以有哪些信息架构候选？每个候选如何承载连续业务数据流、测量/控制平面、并行 DA/NDA 估计器、固定阈值 selector 和公共后级？哪些差异必须交由用户确认，不能由样图自动推断？

## 发现

### 1. 所有候选共同的语义硬门

以下不是候选风格，而是必须同时满足的语义约束：

- raw sample 必须沿 receiver 前级→phase compensation→公共 decision/downstream 连续、单向、可追踪；测量、估计和控制从上/下方侧接入，不能吞掉业务数据。
- 同一输入进入并行 DA 与 NDA 候选；effective-SNR measurement→fixed-threshold comparison→单一 selector 一次性路由；不画成“DA 失败后再运行 NDA”的 early-exit 串级。
- DA/NDA 输出的相位估计量（\(\hat\theta_{DA}\)、\(\hat\theta_{NDA}\)）侧向注入 phase compensation；selector 不截断 raw path。
- 数据、测量、估计和控制至少使用两种独立视觉通道（线型、形状、空间位置、文字标签等），颜色只能辅助，黑白和缩小后仍要可读。
- 不放 crossover 数字、性能口号、参数表、训练流程、纯装饰频谱/星座/相位小图；旧 SVG 的标签级微调方案不再适用。

这些门分别由 R020 的 R1/R3、R4、T1/T2、C3/C4 和 R018 Fig.1 规格支持；R1/R3 为跨组高置信，T1/T2 为目标语义强特例，不能被解释成已有单图同构模板。

### 2. 候选 A：receiver-local“数据平面 + 控制平面”单图

**形态与阅读顺序**

只画 coherent receiver/CPR 局部。中部左→右为 raw sample 主链；上方或下方为 effective-SNR→fixed-threshold comparator→selector 控制平面；同一输入向 DA/NDA 并行候选分叉，估计量侧向回到 phase compensation，再进入公共后级。

**能承载什么**

- R1、R3、R4 和 T1/T2 最直接，数据线、估计线、控制线可以用冗余编码分开。
- 不需要 system→receiver 的跨尺度 callout，因此可以把 CPR 机制画到足够大；只保留 receiver-local 的公共 downstream 边界。
- 单栏局部图有机会通过目标字号/箭头检查；若附加 Tx—FSO—Rx 上下文，则会失去低密度优势并接近候选 B。

**优点**：语义最清楚、密度最低、最适合先验证 DA/NDA/selector 的真实执行关系。

**风险**：缺少 Tx—FSO/channel—coherent Rx 系统定位；R2/R6 不直接适用；若把上下文硬塞进去，容易退化为横向过长单面板。

**证据性质**：由 R1/R3、A1-08、A4-15、B3-01 组合出的候选；没有单张参考图完全同构，属于结构推断。

**需要用户确认**：Fig.1 是否允许只画 receiver-local；公共 downstream 画到 phase compensation 还是继续到 demapper/decision；raw input 采用 \(r_b\) 还是 \(r[k]\) 标签。

### 3. 候选 B：端到端总览 + receiver/CPR 嵌入式 zoom

**形态与阅读顺序**

同一画布先读 Tx→FSO/channel→coherent Rx→DSP/common downstream 粗链；在 Rx/CPR 处用一个明确父级 callout/inset 展开候选 A 的局部结构。主链与局部只通过父级模块名、编号或身份标记连接，不重复制造第二条业务流。

**能承载什么**

- R2/R6 的父子锚点、身份连续和最多两级局部展开最自然。
- 外层交代系统边界，局部解释 measurement/control、并行 DA/NDA、selector 和公共后级；频谱/星座不作为装饰补入。
- 完整图默认按双栏通宽验收；局部 inset 是否能单栏独立可读，需另做目标尺寸检查。

**优点**：兼顾系统定位和机制解释，最接近 B1-01/B1-02 的总览—局部层级语法；可把主图和局部的职责分开。

**风险**：父级与 zoom 的 raw anchor 若重复或不一致，会被读成两次处理；超过两级或做成等权拼贴会触发 R6/C4；局部文字可能在缩小后失读。

**证据性质**：B1-01/B1-02 提供总览—局部强特例，A1-08/A4-15 提供机制语义；把二者组合成 Fig.1 是合理推断，不是单图模板照搬。

**需要用户确认**：是否必须保留 Tx/FSO context；inset 放在 Rx 内部还是下方；外层是否只保留 4 个粗模块；哪些物理器件、参数和公共后级应删掉。

### 4. 候选 C：两面板职责拆分

**形态与阅读顺序**

面板 (a) 只画 Tx—FSO—coherent Rx 粗链、raw 主路和必要的 quality/control 旁路；面板 (b) 只展开 receiver-local CPR：同一输入→并行 DA/NDA→criterion→selector→估计量→公共 phase compensation。两面板用 Rx/CPR 编号或同一 raw identity anchor 连接，每个面板内部保持左→右。

**能承载什么**

- (a) 保留系统边界，(b) 保留机制细节；面板 (b) 可作为独立 local 图复用。
- 两面板不超过 C4 的“>3 面板”门，但必须避免两面板各自画一条看似独立的 raw path。
- 整体按双栏通宽验收；(b) 单栏独立引用需过缩小检查，(a)+(b) 不宜在单栏并排压缩。

**优点**：比候选 B 少跨层叠线，caption 可以明确分担 panel 语义；系统图和机制图职责边界清楚。

**风险**：面板间接口若靠读者脑补，会破坏 R1；重复输入/输出可能被误解为两个连续算法阶段；连接器过多会把一张图拆散成两张互不相干的图。

**证据性质**：由 B1-01/B1-02、A1-08、A4-15 与 R1/R3/R5/R6 组合出的推断候选，现有样本没有完全同构的双面板。

**需要用户确认**：面板上下堆叠还是左右排列；是否允许 (b) 独立引用；(a) 是否保留公共 downstream；两个 panel 的 caption 是否分别解释“系统上下文”和“局部实现”。

### 5. 候选通用验收清单（批次 D-D2）

**INVARIANT（语义硬门）**

- raw sample 连续主路；估计量是旁路控制/补偿量，不替代业务数据。
- 数据/测量/估计/控制至少两种独立编码，颜色仅辅助。
- DA/NDA 是同一输入的并行候选→selector→common downstream，禁止 early-exit。

**DECIDED（当前可执行门）**

- 完整/高密度组合先按双栏通宽验收；receiver-local 可单栏，但必须做目标尺寸缩小检查。
- 超过 3 个面板必须由单一论点统领、保持单向阅读，并通过约 3.5 in 单栏/约 7.16 in 双栏检查。
- 多尺度必须有父级锚点/编号/身份连续；局部暂不超过两级；caption 不能挽救图内不可追踪的箭头。
- 不放结果数字、crossover、性能口号、参数表、训练态或纯装饰小图。

**TENTATIVE（结构条件）**

- 候选 B 最完整地承载 R2/R6，但双栏和 zoom 缩放风险最高。
- 候选 A 语义最简洁、最容易通过单栏，但牺牲系统边界。
- 候选 C 可分离系统与机制密度，但面板接口身份连续性是主要风险。

### 6. 用户确认后的两图配对架构（D011）

用户已确认采用两个独立编号图，而不是继续在一张图内纠结总览、zoom 和机制细节的取舍。当前配对方向为：

- **Fig.1 系统总览**：Tx→FSO/channel→coherent Rx→DSP/common downstream 的粗粒度上下文；只标出 CPR 所在位置和必要的 raw sample 主链，不展开 DA/NDA 内部判据。
- **Fig.2 自适应 CPR 机制**：receiver-local 细粒度图；完整表达 raw sample 连续主路、effective-SNR measurement、fixed-threshold comparator、并行 DA/NDA、单一 selector、\(\hat\theta\) 侧向注入 phase compensation/common downstream。

R021 的候选 A/B/C 不删除：A 主要作为 Fig.2 的低密度机制参考，B 的父级—局部层级语法可供 Fig.1/机制之间的身份连接参考，C 的职责拆分作为两图 caption/接口设计的对照。它们不再是“单张 Fig.1 三选一”的互斥方案。

**图号影响**：原 BER/crossover 图整体顺延为 Fig.3--5，Table I 保持独立；具体正文、脚本和文件名的图号联动尚未执行。

## 结论

批次 D 先把 R020 的证据转成三个单图候选；用户随后确认采用两张独立编号图，因而形成“Fig.1 系统总览 + Fig.2 自适应 CPR 机制”的配对架构。这个决定解决了系统定位与机制细节的层级冲突。随后按 R022 的验收门完成首版 SVG 源文件与预览，最终 caption/正文图号联动仍待后续。

## 对决策的影响

已记录 D011；D012 随后选定 SVG 作为两图可编辑图源，PNG 仅作预览，且旧 `fig1_system_block.svg` 保持不变。R021 仍冻结“两图职责分工”和每张图的语义边界；最终单双栏落版、caption/正文图号联动尚未执行。两图的可执行详细规格见 `R022-fig1-fig2-detailed-spec.md`，首版实现与视觉验收记录见 S013。
