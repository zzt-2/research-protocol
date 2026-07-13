# [R018] 改稿后图表规格与视觉规范

> 2026-07-12 起草；2026-07-13 续接 | 关联：专题 2026-07-09-thesis-writing / D009 / D011 / D012
> 状态：Fig.2--4 的原规格已由用户拍板并进入重画；D011 新增 Fig.1 系统总览与 Fig.2 自适应 CPR 机制两张独立图，原 BER/crossover 图计划顺延为 Fig.3--5，具体图号联动尚未执行。D012 已选定 SVG 为 Fig.1/Fig.2 可编辑图源；首版源文件与预览已生成，caption/正文联动仍未执行。

## 调研问题

改稿后 Fig.1--4 与 Table I 应分别承载什么论点，并采用怎样的论文级标题、坐标、字体、线型、图例和版面？

## 0. 本轮边界与先行发现

- 当前仍在 GW Step 4a 维度 D；本轮只读既有正文、样图、代码和数据，讨论 Fig.1--4 与 Table I 的信息分工。**不跑实验、不画新图、不改正文。**
- 原 4 图 + 1 表规划经 D011 调整为 **5 图 + 1 表**，仍处于 R010 对标集的 4--6 图、0--2 表范围内。D011 的新增两图职责已冻结；现有 BER/crossover 章节中的 Fig.2--4 编号属于重编号前记录，正文/脚本联动留待后续规格实施。
- **D007 硬约束**：AWGN/弱/中湍流的 naive 归零值 0.09/0.18/0.19 dB 不进入任何图、表、标题、图注或脚注。底层数据仍保留。
- **发现 F2-v2-1（Fig.1 局部过时）**：现有 SVG 仍含 “~13 dB”“Crossover ~13 dB”以及已被推翻的 “BER waterfall flattens” 注释。系统框图骨架可保留，但这些标签必须删除或改为中性标签。
- **发现 F2-v2-2（低 SNR 数字定义门）**：`_a4_switch_30seed_fixed.py:238-249` 中 `switch_vs_nda_db_mean` 的定义是
  \(10\log_{10}(P_{b,\mathrm{NDA}}/P_{b,\mathrm{switch}})\)。它是同一 SNR 点的 **BER 比值 dB 化**，不是达到同一 BER 所需的横向 SNR 差。故 Fig.3 若使用这组数，纵轴不得写 “net SNR gain”；W002 中 “1.3--2.3 dB net SNR gain” 也应在转 LaTeX 前单独过口径门。
- **发现 F2-v2-3（crossover 方向）**：可复现的当前曲线交点从 about 18.0 dB 降至 about 10.7 dB，表示 NDA 从更低 SNR 起占优，即 **NDA 优势区扩大**；W002 L38 的 “the SNR window in which the DA estimator is preferable widens” 方向相反。规格只冻结中性事实“crossover moves lower”，正文方向句需联动删除或修正。

## 1. 总体推荐组合

| 项 | 改稿后功能 | 推荐状态 | 与其他载体的分工 |
|---|---|---|---|
| Fig.1 | 系统总览：Tx—FSO/channel—coherent Rx—DSP | **首版 SVG 已生成**：源文件与预览待最终版式确认 | 只交代系统边界、CPR 所在位置和必要 raw 主链 |
| Fig.2 | 自适应 CPR 机制：measurement—threshold—DA/NDA—selector—compensation | **首版 SVG 已生成**：源文件与预览待最终版式确认 | 只展开 receiver-local 机制，不重复系统总览 |
| Fig.3（原 Fig.2） | 六场景 DA/NDA BER 全扫描 | **重画**：删全部卖点箭头，按论文版式收敛 | §IV-A 只读总体趋势；crossover 专项交给 Fig.5 |
| Fig.4（原 Fig.3） | 切换相对固定 NDA 的低 SNR BER reduction | **重画**：单面板三场景完整扫描 | 21 个点承载方法自身效果，避免与 Table I 重复 |
| Fig.5（原 Fig.4） | DA/NDA 优势区的场景依赖：观测 crossover 左移 | **重画**：删总标题、重 legend、HD-FEC 和大标记 | 图承载三个交点；正文摘趋势和至多两个锚点 |
| Table I | 强湍流/上行下 NDA 相对 DA 的净 SNR 增益 | 保留，改为单一口径结构化表 | 表承载三个场景全值；正文只报范围或 headline |

当前证据分工：Fig.1 回答“系统在 Tx—FSO/channel—coherent Rx—DSP 中如何定位”，Fig.2 回答“自适应 CPR 的 measurement—threshold—DA/NDA—selector—compensation 机制”，Fig.3（原 Fig.2）回答“两种估计器在六场景下怎样”，Fig.4（原 Fig.3）回答“切换相对固定 NDA 在哪些 SNR 有效”，Fig.5（原 Fig.4）回答“二者优势边界怎样随场景变化”，Table I 回答“强湍流场景中的等 BER 横向 SNR 增益是多少”。各载体不得复述同一组三点。

> 编号联动说明：上表已按 D011 展示当前规划编号；下方 §3--§5 保留原 Fig.2--4 的历史规格标签，待后续转 LaTeX/脚本联动时统一重命名。

---

## 2. Fig.1/2 系统总览与自适应 CPR 机制（D011）

现有 `fig1_system_block.svg` 的布局骨架判定为不可沿用：它同时混入系统背景、参数、算法、结果解释和仿真配置，并存在 mapper/pilot insertion 数据流画错、\(\gamma_{blk}\) 控制流缺失、原始 \(r_b\) 未旁路进入 phase compensation 等语义问题。**“标签级微调保留”方案作废。**

用户已确认拆为两个独立编号图：Fig.1 负责 Tx—FSO/channel—coherent Rx—DSP 的系统上下文；Fig.2 负责 receiver-local 的自适应 CPR 机制。Fig.1 只交代 CPR 所在位置和必要的 raw 主链，Fig.2 才展开 effective-SNR measurement、fixed-threshold comparator、并行 DA/NDA、selector、估计量侧向注入 phase compensation/common downstream。两图的详细语义、标签、流向、版式和验收门已写入 R022；D012 已选 SVG 作为可编辑图源，首版实现见 S013，caption/正文联动仍待后续。

当前只冻结两条：

1. Fig.1/2 不在本规格旧图表重画批次中直接实施；原 BER/crossover 图号顺延尚未执行。
2. 新方案必须补齐真实的数据流、相位估计流和固定阈值控制流，且不在图内放总标题、参数表、性能口号或大图例。
3. Fig.1 与 Fig.2 不得各自画出会被误读为两次处理的重复 raw path；两图的接口身份和 caption 分工必须明确。

---

## 3. Fig.2 BER 主图

### 3.1 论点

在六个信道场景中完整展示 DA、NDA（及已定义的参考线）随平均 SNR 的 BER 变化，建立后续 crossover 与切换讨论的数据底座。

### 3.2 推荐画法

保留 `ccisp_fig2_ber.png` 的 3×2 六子图与对数 BER 纵轴，结构不大改；转正式图时做以下检查：

1. 场景顺序保持 AWGN、下行 weak/moderate/strong、上行 moderate/strong。
2. 保留 7% HD-FEC 水平线；纵轴下限继续标为 D003 待导师定，不为统一版式外推到无可靠数据区。
3. 删除当前 strong/uplink 子图中的全部 `NDA +XdB @...` 橙色点值注释。Fig.2 只让曲线、门限和图注说话。
4. 图例中的 `Oracle`、理论 AWGN 线和其他 baseline 必须按真实数据身份命名，不能把 oracle 与 AWGN theory 混称。最终保留哪些参考线，须与 §IV 设置段逐项一致。
5. 删除图内总标题；面板名统一为 `(a) AWGN`、`(b) Weak turbulence` 等短标签，\((\alpha,\beta)\) 放 caption。
6. 最终双栏宽约 7.16 in，高度控制在 8--8.5 in；只在底行显示横轴名、左列显示纵轴名。
7. 横轴统一为 `Average data-symbol SNR, $\bar{\gamma}_d$ (dB)`，纵轴为 `Bit error rate (BER)`；门限写 `HD-FEC threshold ($3.8\times10^{-3}$)`，不使用 `4e-03` 程序输出格式。
8. 插值只能改善视觉连续性，原始采样点保留 3--4 pt 小型标记；不得把插值曲线当新增仿真点。
9. 主线 1.1--1.5 pt，参考线 0.7--0.9 pt；轴名 9 pt，刻度/legend 8.5--9 pt；仅保留浅色 major grid。最终输出矢量 PDF，PNG 仅作预览且不低于 300 dpi。

### 3.3 已拍板方案

保留 3×2 六子图；不删上行场景，不保留任何卖点箭头。若最终排版高度仍超限，只调面板间距和共享标签，不把数据场景砍成 4 个。

### 3.4 图文关系

§IV-A 采用“引图 + 一条总体趋势”，不逐场景读曲线。crossover 三个数不在 Fig.2 段重复列全，交给 Fig.4；正文可只说各估计器在不同 SNR 区域占优。

### 3.5 对标集对齐

- R010 §4.1：BER vs SNR 主图、2--6 子图、HD-FEC 线、纵轴不硬凑 10^-5。
- R015 维度 3/惯例 3：全扫描进图，正文不逐点复述；比较基准同图叠加。

### 3.6 数据来源

- 30-seed 主数据：`projects/simulation/results/sc_nda_ml_main_30seed/_main_experiment_30seed.json`
- 5-seed 已有延伸数据：`projects/simulation/results/sc_nda_ml_ber_ext_5seed/_ber_ext_5seed.json`、`_ber_ext2_5seed.json`
- 样图脚本：`projects/simulation/figures/plot_fig2_ber.py`

### 3.7 待拍板点

- **卡导师 D003**：纵轴下限及 strong/uplink 是否统一到 10^-4。
- Oracle/理论线身份仍须与正文逐项一致；本轮只改视觉，不擅自换 baseline。

---

## 4. Fig.3 低 SNR BER reduction（已拍板）

### 4.1 论点

固定 NDA 在低 SNR 下 BER 较高；逐块切换在该区域选择 DA，从而降低 BER，并在 SNR 升高后逐渐回到固定 NDA 的性能。该图表达的是**切换方法自身的低 SNR 避险作用**，不再重复 Table I 的强湍流净 SNR 增益。

### 4.2 推荐画法

将旧 Fig.3 完全改为单面板三条完整扫描曲线：weak / moderate / strong，各 7 个 SNR 点，共 21 点。

- 横轴：`Average data-symbol SNR, $\bar{\gamma}_d$ (dB)`。
- 纵轴：`BER reduction relative to fixed NDA (dB)`。
- 定义：\(10\log_{10}(P_{b,\mathrm{NDA}}/P_{b,\mathrm{sw}})\)；正值表示切换 BER 更低。完整公式放 caption，轴名保持短。
- 三场景颜色与 Fig.4 一致，并叠加 circle/square/triangle 小型 marker，保证黑白可读。
- 画细的 \(y=0\) 参考线；不画 CI、阴影、\(\gamma_{th}\) 竖线、数值箭头或图内总标题。
- caption 必须写明这是**同一 SNR 下 BER 比值的 dB 化**，不是等 BER 横向 SNR gain；正文只能称 BER reduction。

这组数据与 D007 禁止的 HD-FEC naive 归零值不是同一指标；图中仍不得出现 0.09/0.18/0.19 dB。

### 4.3 排除的方案

- 1×3 raw BER：信息量足够，但重复 Fig.2 的 BER 视觉语法且需双栏。
- 三场景柱状图：与 Table I 三行完全重复。
- 加 AWGN 填密度：破坏三档湍流受控比较。

### 4.4 图文关系

§IV-B 先用一句引图并给定性趋势：“Fig. 3 shows that switching lowers the BER relative to a fixed NDA estimator in the low-SNR region and converges to it as SNR increases.” 正文不逐场景列所有点。若保留代表点，只摘一个；`1.3--2.3 dB` 在口径名称修正前不作为 net SNR gain 复述。

### 4.5 对标集对齐

- R010 §4.3：真实 baseline 同图比较；不另设 baseline 对比节。
- R015 维度 3/5、惯例 1/3：全扫描进图，正文只摘代表点；Fig.3 与 Table I 分别承担不同功能。

### 4.6 数据来源

- 修复后的 30-seed 数据：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.json`
- 生成定义：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py:238-269`
- 已核验低 SNR 点：weak@5/10、moderate@5/10、strong@5/10；只使用现有数据，不补跑。
- 旧样图 `ccisp_fig3_gain.png` 仅复用颜色、字体和版式风格，不复用论点或数据映射。

### 4.7 已拍板点

- 单面板三条 BER-reduction 曲线；不再称 net SNR gain。

---

## 5. Fig.4 crossover 场景依赖

### 5.1 论点

DA 与 NDA 的相对优势具有场景依赖性：随下行湍流增强，观测到的 BER crossover 向更低平均 SNR 移动，说明 NDA 优势区从更低 SNR 开始。该图是数据观察，不是 \(\gamma_{th}\) 的标定图，也不解释左移原因。

### 5.2 推荐画法

基于 `ccisp_fig4_crossover.png` 保留单图 6 条曲线：weak/moderate/strong 三色，DA 实线、NDA 虚线。

1. 图内不放总标题；caption 使用中性表述，例如 `Observed DA/NDA BER crossovers across turbulence regimes`，不写 “switching threshold shifts”。
2. 曲线、交点计算和标记统一使用原始点间 log-BER 线性插值；当前可复现值为 18.013/16.866/10.703 dB，图中按一位小数标为 **about 18.0 / 16.9 / 10.7 dB**。
3. 删除大叉号与箭头，交点改为小型空心标记；图例不使用 \(\gamma_{th}\) 符号。
4. 删除 HD-FEC 线，它不参与 crossover 论点。
5. legend 拆成两套编码：颜色表示 Weak/Moderate/Strong，线型表示 DA/NDA；不列 6 个场景×方法组合。
6. 横轴和纵轴与 Fig.2 完全一致；尺寸约 7.16×3.6--4.2 in，字体/线宽遵循全局视觉规范。

### 5.3 已拍板方案

独立保留 Fig.4；不并入 Fig.2，不改画热图或 switching/fixed BER。

### 5.4 图文关系

§IV-A 推荐只写“一条趋势 + 至多两个端点锚点”，例如从 weak 的 about 18.0 dB 降至 strong 的 about 10.7 dB；moderate 的 16.9 dB 留在图中。删除 W002 当前对三点的第二次重复，并删除/修正 “DA advantage window widens”。不能写 “\(\gamma_{th}\) moves” 或 “below/above \(\gamma_{th}\) 两法必然谁优”，因为 \(\gamma_{th}\) 是固定判据而非这三个观测交点。

### 5.5 对标集对齐

- R010 §4.1/§4.3：多估计器同图比较，crossover 在图中自然呈现。
- R015 维度 5/惯例 3：图承载三个交点，文字只摘端点或一个代表点，不逐值复述。

### 5.6 数据来源

- 30-seed 主数据与已有 5-seed 延伸数据，同 Fig.2。
- 交点算法：`projects/simulation/figures/plot_fig4_crossover.py` 的原始点间 log-BER 线性插值；显示曲线使用同一插值，避免“画法与计算法不一致”。
- 当前源 JSON 可复现值：weak 18.013 dB、moderate 16.866 dB、strong 10.703 dB；显示为 about 18.0/16.9/10.7 dB。R012 的 17.9/16.8/10.7 保留为历史版本，不再硬编码到新图。

### 5.7 待拍板点

- 正文最终摘 weak/strong 两端，还是只摘 strong 10.7 dB，留到转 LaTeX 时处理。

---

## 6. Fig.2--4 全局视觉规范

| 元素 | 冻结规格 |
|---|---|
| 图内总标题 | 不使用；论点由 caption 承担 |
| 字体 | Times New Roman/Times；数学字体与正文同族并嵌入 PDF |
| 轴名 | 9 pt |
| 刻度/legend | 8.5--9 pt |
| 主曲线 | 1.1--1.5 pt |
| 参考线 | 0.7--0.9 pt |
| 原始点 marker | 3--4 pt，小型且黑白可辨 |
| Grid | 仅浅色 major grid；minor 关闭或极淡 |
| 颜色 | 场景颜色跨 Fig.3/Fig.4 保持一致；颜色之外必须有线型/marker 冗余编码 |
| 标注 | 不使用卖点箭头、大文本框、粗体结论或程序输出格式数字 |
| 输出 | 矢量 PDF 为正式稿；PNG 只作预览且不低于 300 dpi |

依据：Johst Fig.3/5/6、Le Bidan Fig.10--12、Panasiewicz Fig.4--6、OECC Fig.1--2、Paillier Fig.3--6 的本地 PDF 实图核查。五篇共同模式是图内无结论式总标题、短量名加括号单位、颜色/线型/小 marker 区分方法、全扫描交给曲线而不是卖点注释。

## 7. Table I 强湍流净增益汇总

### 7.1 论点

以结构化方式给出三个有利强湍流/上行场景中，NDA 相对 DA 的净 SNR 增益；该表量化的是估计器架构差异，不把全部增益归因于切换判据本身。

### 7.2 推荐画法

只保留 strong downlink、uplink moderate、uplink strong 三行。推荐列为：

| Regime | Link direction | \((\alpha,\beta)\) | Approx. net SNR gain of NDA over DA (dB) |
|---|---|---:|---:|
| Strong | Downlink | (1.5, 0.8) | 1.3 |
| Moderate | Uplink | (1.2, 0.9) | 1.2 |
| Strong | Uplink | (1.0, 0.7) | 1.9 |

表头或 caption 统一说明 “values are rounded to 0.1 dB”；单元格不重复写 `about`。精确底层值 1.260/1.194/1.852 仅留在来源记录，不进入正式表。

推荐采用**单一口径列**，而不是 naive/fair 双列：

- 导师定 **naive**：使用上表，删除 fair 列；caption 定义为扣除 1.249 dB pilot power penalty 后的净值。
- 导师定 **fair**：将最后一列整体替换为 fair 数值约 2.5/2.4/3.1 dB，并改 caption 为 including pilot power penalty；不要与 naive 同表并列。

三行不等于信息量不足：增加 \((\alpha,\beta)\) 与 link direction 后，表承担“场景条件 → 结果”的查询功能；这比把另一个口径或低 SNR 指标塞进同表更清晰。

### 7.3 备选方案与利弊

- **备选 A：naive + fair 双列。** 透明展示口径关系；但两个口径同表会增加解释负担，与 R015 “单一结果口径/不混角色”相悖，并把 Q3 的导师选择变成读者负担。
- **备选 B：增加 low-SNR avoidance 列。** 可增加数值密度；但该列来自不同场景区间、不同计算定义（且当前是 BER ratio dB），会把两类声称混在一起，不推荐。
- **备选 C：删除 Table I，正文只报 headline。** 可省版面；失去唯一的结构化场景映射，且三个 \((\alpha,\beta)\) 条件无处集中呈现。

推荐单一口径表；Q3 由导师决定“替换哪一列”，而不是决定“是否再叠一列”。

### 7.4 图文关系与 Q8

Table I 承载三个场景的完整值，§IV-B 不再逐项复述 1.3/1.2/1.9。正文推荐写法是：先报范围或 headline（如 “about 1.2--1.9 dB, as summarized in Table I” 或 “up to about 1.9 dB”），再解释该结果的条件与口径。这样表不是正文数字的重复汇总。

Table I 不加入弱湍流行，不加弱湍流脚注，不写“其他场景接近零”。

### 7.5 对标集对齐

- R010 §4.2：1 张增益汇总表作为增量亮点，主报单一口径。
- R015 维度 2/5、惯例 1/4：表承担结构化映射，正文不逐值复述；结果用一位小数和近似标记。

### 7.6 数据来源

- `projects/simulation/results/sc_nda_ml_main_30seed/_fair_gain_summary_30seed.json`
- 计算定义：`projects/simulation/simulator/fair_comparison.py:120-136` 在工作区按相同 BER 求横向等效 SNR 差；因此这组三场景数可称 SNR gain，与 Fig.3 的同 SNR 点 BER ratio dB 不同。
- 口径关系：`projects/simulation/simulator/fair_comparison.py:109`，fair = naive + 1.249 dB。
- 参数：R012 参数表；strong (1.5,0.8)、uplink moderate (1.2,0.9)、uplink strong (1.0,0.7)。
- naive 精确底层值：1.260/1.194/1.852 dB；fair 精确底层值：2.509/2.443/3.101 dB。

### 7.7 待拍板点

- **卡导师 Q3/Q4**：主报 naive（当前推荐）还是 fair。规格建议二选一替换单列，不并列。
- **卡用户**：正文保留范围 `about 1.2--1.9 dB`，还是只留 headline `up to about 1.9 dB`。

---

## 8. 图文关系联动清单（转 LaTeX 时执行，本轮不改正文）

| 正文位置 | 当前问题 | 推荐联动 |
|---|---|---|
| §III / Fig.1 | 固定阈值与 crossover 容易混称 | 只称 fixed \(\gamma_{th}\)，不报具体值；Fig.1 不出现 crossover 标签 |
| §IV-A / Fig.2 | 六场景全扫描已有图载体 | 正文只引图并给总体趋势，不逐场景读数 |
| §IV-A / Fig.4 | 三个 crossover 在同段列了两遍；DA 优势区方向写反 | 正文只留趋势 + 至多两个端点；删除反向窗口句；不把 crossover 写成 \(\gamma_{th}\) |
| §IV-B / Fig.3 | 1.3--2.3 dB 被称为 net SNR gain，但生成式是 BER ratio dB | Fig.3 明确画 BER reduction；正文称谓在转 LaTeX 前同步改 |
| §IV-B / Table I | 正文与表逐项重复 1.3/1.2/1.9 | 正文改范围/headline + `as summarized in Table I`，三场景全值只留表内 |

图文统一句式建议遵循：“Fig./Table X shows/summarizes ... [定性趋势]. For example, ... [至多一个或两个代表锚点].” 禁止按曲线或表格逐项复述。

## 9. 待用户/导师拍板清单

1. **Fig.1/2（R022）**：两图职责、标签、流向、版式假设和验收门已写；D012 已选定 SVG，S013 已完成首版源文件与视觉预览，caption/正文联动和最终落版仍待处理。
2. **Fig.3 正文称谓**：图已冻结为 BER reduction；W002 现有 net SNR gain 说法转 LaTeX 前联动修正。
3. **Table I 口径（卡导师 Q3/Q4）**：naive 或 fair；推荐只保留所选单列。
4. **Table I 正文锚点（卡用户）**：保留范围 about 1.2--1.9 dB，或只留 up to about 1.9 dB。
5. **Fig.4 正文摘值（卡用户）**：摘 weak/strong 两端，或只摘 strong 一个代表点。
7. **Fig.2 纵轴（卡导师 D003）**：strong/uplink 的最终下限。
8. **Fig.1/2 参考材料**：R019 的 97 张候选、R020 的视觉语法和 R021 的架构 critic 已完成；不再继续扩样，除非用户审阅后出现类型缺口。

## 10. 供主控审阅的总结

本轮将 F001 的改稿前 F2 规格更新为讨论版 v2，并完成三项核心联动：

- **Fig.3**：原“强/弱净增益对比”在 D007 后失去论点，且与 Table I 重复；已拍板改为切换相对固定 NDA 的三场景 BER-reduction 全扫描。旧柱状/双线净增益方案不再使用。
- **Fig.4**：从“\(\gamma_{th}\) 自动左移”改为“观测 crossover 随场景移至更低 SNR”；固定阈值与 crossover 严格分离，不附归因。
- **Table I**：完全删除弱湍流及脚注；通过 \((\alpha,\beta)\)+link direction 增加结构化信息；正文只报范围/headline，表承载三行全值；naive/fair 由导师二选一，不建议双列。

新增两项必须处理的口径/图文门：低 SNR 的 1.3--2.3 dB 是 BER ratio dB 而非横向 SNR gain；crossover 左移扩大的是 NDA 而非 DA 优势区。原 Fig.2--4 图规格按 D009 重画，D011 新增的 Fig.1/2 架构图另行规格化，编号与正文联动留到后续批次。

## 结论

原 Fig.2--4 的论点与视觉规范已冻结，可在不跑新实验的前提下基于既有 JSON 重画。D011 已确定新增 Fig.1 系统总览与 Fig.2 自适应 CPR 机制；R022 已完成两图详细规格，现有旧 SVG 不可沿用，S013 已按 D012 完成两份新 SVG 首版，具体 caption/正文联动与最终落版仍待处理。

## 对决策的影响

形成 D009：原 Fig.2--4 进入重画；形成 D011：架构图拆为 Fig.1 系统总览 + Fig.2 自适应 CPR 机制；D012 随后选定 SVG 作为两图可编辑图源。本文取代 F001/F2 中关于旧 Fig.1 微调、Fig.3 双线净增益、Fig.4 重标注的旧规格，但不修改 D003/D004/D007/D008。
