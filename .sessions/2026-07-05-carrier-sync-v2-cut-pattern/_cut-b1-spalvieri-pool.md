# 切法元数据：B1 综述线（sat.1553 + Spalvieri 85 池）

> 提取人：子 agent | 日期：2026-07-05 | 范围：B1 切入点（自适应 pilot 窗口）
> 纪律：D018 中性提取（只提取不判断）；FR-26 证据链（看不出信息标"信息不足"不脑补）；团队维度只标作者名不推断师承

---

## 1. sat.1553 综述自身的切法动作

> sat.1553 = Valjus, Wolf, Poliak（DLR 课题组）2025 综述，锚"相干光卫星链路(OSL)DSP 算法"。

1. **站在哪个大点上切的**：站在"地面光纤相干 DSP 算法"这个超级大点上切（Viterbi–Viterbi / BPS / Schmidl–Cox / CMA 等，全部从地面光纤搬来），通过"场景迁移"切到 OSL。同时引 Spalvieri[57] 作为 pilot vs decision-directed 理论锚。
2. **切的什么角度**：**算法地图 + 场景对比 + open problem 罗列**三合一。把整个相干接收机 DSP 流水线拆 3 大子系统（定时恢复 / 载波同步 / 均衡），每子系统罗列 state-of-the-art 算法清单，再用 4 场景仿真做横向 SNR-penalty 对比。最后 Section 4.2 末自报两个 open problem（自适应 pilot rate / 自适应 phase-estimation window）作为综述延伸切法。
3. **dB 真实性条件性**：**vs 内部对照**（4 场景下各算法互相对比，无统一"传统 baseline"），关键 dB 数字"pilot 在场景 4 比 VV+diff 好 1 dB"。条件性明确：dB 只在准静态 SNR 分布假设 + 单一 SNR 采样点评测下成立，自承未建模相干时间。
4. **横向多样性**：**综述型独占**——该综述是 OSL 场景下的最新（2025）DSP 算法地图，横向覆盖最广，但本身不深挖单一算法，给后续工作留"小切口"。
5. **动机叙事**：intro 收窄路径清晰——"地面光纤 DSP 为静态信道优化 → OSL 是动态低 SNR → 直接套用会出问题 → 需要场景定制"。挑战"光纤算法可直接搬"的常识。
6. **实现复杂度**：纯计算机仿真（未写工具），无 FPGA/ASIC。4 场景参数完整公开，Open Access，理论可复现。

---

## 2. B1 切入点（自适应 pilot 窗口）的切法动作

> B1 = 用户从 sat.1553 L440 自报 open problem 出发切的候选点。

1. **站在哪个大点上切的**：站在 **sat.1553 综述**（系统级算法地图）+ **[58] Martins osac.438524**（dual-stage pilot-BPS CPR，静态 pilot-rate×linewidth 优化）+ **[60] Leven lpt.2007.891893**（Mth-power CFO，给出"最优 N ∝ SNR/phase-noise 比值"理论锚）三个大点上。
2. **切的什么角度**：**参数调度 + 场景迁移**复合——把 [58]/[60] 给出的"最优窗口 N 随 SNR/linewidth 变"理论依据，从静态优化曲线（地面光纤 access）迁移到 OSL 上行强湍场景，并改为按当前 SNR 动态调度 N（参数调度，非算法重构）。机制上 ≠ D006（不纳入湍流相位建模，只调 filter 窗长）。
3. **dB 真实性条件性**：**信息不足（待 MVE）**——sat.1553 自承"potential gain 未量化"。背书信号是 sat.1553 L440 报"pilot 在场景 4 比 VV+diff 好 1 dB"，但这是 pilot vs VV 的差，不是自适应 N vs 固定 N 的增量。负向信号：sat.1553 自承"same pilot rate performs similarly for all scenarios"（暗示自适应 pilot rate 增益可能平缓）。
4. **横向多样性**：**独占风险中**——window-N 自适应这条路线在 Spalvieri 85 池里未见直接复刻（池里 pilot 工作多为静态 overhead 优化或架构替换，非动态 SNR-driven 窗调度）；但"自适应"概念在池里有 Kalman 自适应（L014/L030）、DL 自适应（L053）等共享角度。
5. **动机叙事**：从"sat.1553 自报 open problem 且作者亲口说'未量化'"出发收窄——理论依据 [60] 说最优 N 随 SNR 变 → OSL 场景 SNR 大幅波动 → 固定 N 必然次优 → 动态调 N 应有增益（增益量未知）。空白声明由综述作者亲口给出（非 agent 臆造）。
6. **实现复杂度**：**信息不足**——B1 切入点笔记未给实现方案细节。理论上 window-N 调度是 filter taps 数值参数调度，复杂度增量小（无新算法结构），但需 SNR 估计反馈环路（sat.1553 信道假设准静态，未提供 SNR 估计模块）。

---

## 3. Spalvieri 85 池筛出的切法多样样本（7 篇）

### 3.1 切法角度分布速览

| DOI / ID | 标题简 | 切的角度（一句话） | 团队 |
|---|---|---|---|
| 10.1109/jlt.2012.2187635 / L004 | Information rate through Wiener phase noise channel | **性能极限/信息论界**：把 Spalvieri 的 pilot-aided 相位估计迁到"信息率上下界"这个理论维度，pilot 当信道状态信息纳入界计算 | Barletta, Magarini, Spalvieri 等 |
| 10.1109/lpt.2012.2187439 / L003 | Pilot-symbols-aided CPR for 100-G PM-QPSK | **架构替换**：pilot 粗估 + blind 细估 dual-stage，替换 standalone blind，避免 cycle-slip 后 phase ambiguity | Magarini, Barletta, Spalvieri 等（含 Pfau/Gavioli） |
| 10.1364/oe.27.024654 / L008 | Overhead-optimization of pilot-based DSP | **参数调度**：用 achievable information rate 找 pilot overhead 最优点，证明最优 overhead 弱依赖传输距离 | Mazur, Schröder, Lorences-Riesgo, Yoshida, Karlsson, Andrekson 等 |
| 10.1109/lcomm.2016.2542798 / L030 | Joint phase recovery for XPIC using adaptive Kalman | **联合建模**：把 Spalvieri 的 Kalman carrier recovery 迁到 XPIC 双极化场景，参数按 Eb/N0 + XPD 自适应 | Vizziello, Savazzi, Borra 等 |
| 10.1109/jlt.2019.2959395 / L009 | Phase & frequency recovery for probabilistically shaped | **场景迁移**：把 pilot + BPS dual-stage 迁到概率成形(PS)场景，发现 PS 在中低 SNR 损坏 BPS，提出 detune PS factor 或 SNR-driven 开关 BPS | Barbosa, Rossi, Mello 等 |
| 10.1109/jlt.2020.2976166 / L035 | VLSI implementations of CPR for M-QAM | **硬件实现**：把 BPS 和 pilot-symbol-aided CPR 做成 22 nm CMOS 电路，给 pJ/bit 能效数字 | Börjeson, Fougstedt, Larsson-Edefors 等 |
| 10.1109/ICCWorkshops59551.2024.10615713 / L053 | Deep learning-assisted PN mitigation (DLAE) | **工具借用**：用 CNN 替换 PSAM 的 pilot 插值，利用 PN-induced 信号间互相关，pilot overhead 减少但 BER 增益 >2 dB | Neshaastegaran, Jian 等 |

> 注：池里大量 Spalvieri 自引（L014/L015/L016/L017/L020/L022/L023/L025/L033/L038/L039/L040/L042/L044/L062/L079/L080/L081 等）是同一团队对自己大点的连续切——切法偏理论（Kalman 界 / trellis demod / Wiener 滤波），未选入 7 篇以保持"切法多样性"目标。这些自引在 §4 横向多样性讨论中标"团队自切集中"。

### 3.2 逐篇 6 维元数据

#### 篇 1：10.1109/jlt.2012.2187635（L004）— The Information Rate Transferred Through the Discrete-Time Wiener's Phase Noise Channel

1. **大点锚**：Spalvieri 团队自己的 Wiener 相位噪声 + pilot-aided carrier recovery 大点（与 L014/L016 同源）。
2. **切的角度**：**性能极限/信息论界**——切的是"信息率"这个理论维度而非算法本身。pilot 在这里被当"信道状态信息源"纳入界计算，研究"pilot 占用符号率损失 vs 带来的信道状态增益"的平衡。
3. **dB 形态**：**无 dB 仅结构性**——给的是信息率上下界（bits）的收敛性，不是 SNR penalty dB。
4. **横向多样性**：**共享**——与 L010（Ghozlan & Kramer）、L013、L016、L074（Barletta & Kramer）同属"信息率界"角度，是池里最密集的子类之一。
5. **动机叙事**：abstract 看出动机——"pilot 一方面损失符号率一方面带来信道状态信息，二者平衡需要计算"。从工程权衡收窄到信息论量化。
6. **实现复杂度**：信息不足（abstract 未给算力/数据需求，提到 trellis + 量化 phase space，是计算密集型）。

#### 篇 2：10.1109/lpt.2012.2187439（L003）— Pilot-Symbols-Aided Carrier-Phase Recovery for 100-G PM-QPSK

1. **大点锚**：Spalvieri pilot-aided 相位估计大点 + blind BPS 大点（dual-stage 把二者嫁接）。
2. **切的角度**：**架构替换**——pilot 粗估（coarse，data-aided）+ blind 细估（fine，non-data-aided）双级，替换 standalone blind。卖点：cycle-slip 后避免 phase ambiguity。
3. **dB 形态**：**vs 传统 baseline**——"for homogeneous transmission, the proposed scheme outperforms blind carrier recovery with differential decoding"（abstract）。具体 dB 数字需查正文。
4. **横向多样性**：**共享**——dual-stage pilot+blind 是池里高频架构（L009 Barbosa、L005 Neves、L055 Guiomar、L035 Börjeson 都切 dual-stage），属主流切法。
5. **动机叙事**：动机清晰——"cycle slip 后 phase ambiguity 是问题 → pilot 帮忙解 ambiguity → 但 pilot overhead 高 → 用 dual-stage 兼顾"。从工程痛点收窄。
6. **实现复杂度**：信息不足（abstract 未明说，但 dual-stage 比单级多一级处理，复杂度增加）。

#### 篇 3：10.1364/oe.27.024654（L008）— Overhead-optimization of pilot-based DSP for flexible high SE transmission

1. **大点锚**：pilot-based DSP 大点（完全 pilot-based DSP chain，无 blind 兜底）。
2. **切的角度**：**参数调度**——用 achievable information rate(AIR) 找 pilot overhead 最优点，证明最优 overhead 弱依赖传输距离（"back-to-back optimization is sufficient"）。这是 overhead 这个数值参数的优化，非算法重构。
3. **dB 形态**：**vs 内部对照**——报 9.3/8.3 bits/s/Hz spectral efficiency 和 11.9/10.6 Tb/s 吞吐量（具体 dB penalty 在正文）。
4. **横向多样性**：**共享**——overhead 优化角度池里有 L041 Gävert（signal-to-pilot-power ratio）、L050/L060（URLLC pilot power vs overhead）。但 L008 是"用 AIR 当优化目标"的独占小变体。
5. **动机叙事**：动机清晰——"pilot 增性能但减吞吐 → 需找最优 overhead 平衡 → 用 AIR 当统一指标量化"。从 spectral efficiency 工程权衡收窄。
6. **实现复杂度**：**实测级**——51×24 Gbaud PM-64QAM superchannel 1000 km 传输实测，需要高速 DSP 平台（非纯仿真）。

#### 篇 4：10.1109/lcomm.2016.2542798（L030）— Joint Phase Recovery for XPIC System Exploiting Adaptive Kalman Filtering

1. **大点锚**：Spalvieri 的 Kalman carrier recovery 大点（L014/L015 同源），迁到 XPIC（cross-polar interference cancellation）场景。
2. **切的角度**：**联合建模**——把 Kalman 相位恢复从"单极化"扩到"双极化 joint"，用四状态/二状态模型 joint 估计 main + interfering 极化的相位与频偏。
3. **dB 形态**：**vs 传统 baseline**——"compared to a common PLL approach, the proposed Kalman-based algorithm directly adapts its parameters"（abstract）。具体 dB 数字需查正文。
4. **横向多样性**：**独占小变体**——"自适应参数 Kalman"角度池里独占（其他 Kalman 工作 L014/L015 是固定结构下界计算，不按 Eb/N0+XPD 自适应调度参数）。与 B1 切入点的"参数自适应"思路结构相似（但 B1 调的是 window N，这里调的是 Kalman 增益）。
5. **动机叙事**：动机清晰——"XPIC 双极化用两条独立 RF 链 → 各自 PLL 次优 → joint Kalman 更好且能按信道条件自适应"。从架构痛点收窄。
6. **实现复杂度**：信息不足（abstract 提仿真验证，未给算力数据；四状态模型比二状态复杂）。

#### 篇 5：10.1109/jlt.2019.2959395（L009）— Phase and Frequency Recovery Algorithms for Probabilistically Shaped Transmission

1. **大点锚**：pilot + BPS dual-stage CPR 大点（与 L003 同源），迁到 probabilistic shaping(PS) 场景。
2. **切的角度**：**场景迁移**——把 dual-stage pilot+BPS 搬到 PS 传输场景，发现 PS 在中低 SNR 严重损坏 BPS 第二级。切法是"在新场景下重新评测既有架构 + 提出场景定制修复（detune PS factor 或 SNR-driven 开关 BPS）"。
3. **dB 形态**：**vs 内部对照 + vs 理论上界**——报的是 shaping gain 是否被 CPR 损坏（abstract 提"reducing or even eliminating the expected shaping gains"），无单一 dB 数字。
4. **横向多样性**：**独占**——PS 场景的 CPR 评测池里独占（L012/L032 Wakayama 是 geometric shaping 但角度不同）。"在不同 SNR 段切换 BPS 开关"与 B1 切入点的 SNR-driven 切换思路结构相似。
5. **动机叙事**：动机清晰——"PS 在 AWGN 接近容量 → 但损坏 receiver DSP 链 → 评估 CPR 在 PS 下表现 → 找修复"。从"PS 增益被 DSP 吃掉"的工程问题收窄。
6. **实现复杂度**：**实测级**——offline processing of experimental data with laser imperfections + additive noise loading，需要实验数据 + 长噪声拒绝窗（computational complexity 章节自承 undesirable）。

#### 篇 6：10.1109/jlt.2020.2976166（L035）— VLSI Implementations of Carrier Phase Recovery Algorithms for M-QAM Fiber-Optic Systems

1. **大点锚**：BPS CPR 大点 + pilot-symbol-aided CPR 大点（把两种算法做硬件）。
2. **切的角度**：**硬件实现**——切的是"VLSI/CMOS 电路实现"维度，不是算法本身。给出 22 nm CMOS 工艺下的 pJ/bit 能效、silicon area、三个关键设计参数（input word length / test phase 数 / averaging window）trade-off。
3. **dB 形态**：**vs 传统 baseline + 内部对照**——SNR penalty ≈0.25 dB @ BER 1e-2（BPS），pilot-aided 0.38/0.34 pJ/bit（16/256-QAM）。dB 是"硬件实现引入的 penalty"vs 理想算法。
4. **横向多样性**：**独占**——VLSI 实现角度池里独占（L064 Börjeson 是 FPGA 加速 cycle-slip 仿真，角度相近但不同）。
5. **动机叙事**：动机清晰——"BPS 算法虽好但硬件实现复杂度未量化 → 实现 VLSI → 给能效数字 + 找算法修改以适配电路"。从"算法到芯片"的工程落地收窄。
6. **实现复杂度**：**最高**——需要 22 nm CMOS 工艺流片/综合，给出 netlist 级实现。池里实现复杂度最高的切法。

#### 篇 7：10.1109/ICCWorkshops59551.2024.10615713（L053）— Deep Learning-Assisted Phase Noise Mitigation for High-Order Modulation with Minimal Overhead (DLAE)

1. **大点锚**：PSAM（Pilot-Symbol Assisted Modulation）大点（Spalvieri 池核心），用 DL 替换 PSAM 的 pilot 插值环节。
2. **切的角度**：**工具借用**——把 CNN 工具借到相位噪声估计，利用 PN-induced 信号间互相关，非迭代。卖点是"pilot overhead 减少但 BER 增益 >2 dB"。
3. **dB 形态**：**vs 传统 baseline**——"DLAE outperforms PSAM by over 2 dB at 10⁻⁶ level across 256/1024/4096-QAM"（abstract）。dB 量级大且明确。
4. **横向多样性**：**共享**——DL-for-PN 角度池里有 L054（Neshaastegaran 同团队 ETEL）、L058（ParamNet）。属池里"工具借用 DL"子类。
5. **动机叙事**：动机清晰——"PSAM 在高阶调制 + 强 PN 下 pilot 间距大时失效 → 用 CNN 借信号互相关 → overhead 减少增益还高"。从既有方法的失效边界收窄。
6. **实现复杂度**：**中等**——CNN size，复杂度独立于 constellation size（abstract 明说），但需要训练数据 + 推理硬件。

---

## 4. B1 综述线切法模式小结（中性，不判 Go/Kill）

- **大点分布**：Spalvieri 大点上集中了以下角度——①**信息率界**（L004/L010/L013/L016/L074，最密集子类，多为 Spalvieri 团队自切）；②**Kalman carrier recovery**（L014/L015/L030，团队自切 + XPIC 迁移）；③**pilot-aided dual-stage**（L003/L005/L009，主流架构切法）；④**trellis-based demod**（L017/L020/L023，团队自切）；⑤**硬件实现**（L035/L064，独占）；⑥**DL 工具借用**（L053/L054/L058，新兴）。重复出现：Spalvieri 团队自切集中度极高（约 18+ 篇是 Barletta/Magarini/Spalvieri 合著），形成"自己切自己大点"的连续轨迹。

- **dB 形态分布**（基于筛选 7 篇 + 池速览）：
  - **vs 传统 baseline**：约 3/7（L003 vs blind+diff，L030 vs PLL，L053 vs PSAM）—— dB 数字最明确，量级 1-2+ dB。
  - **vs 内部对照**：约 2/7（L008 AIR 对比，L009 shaping gain 损坏评估）—— dB 形态偏结构性。
  - **vs 理论上界**：约 1/7（L009 部分）。
  - **无 dB 仅结构性**：约 1/7（L004 信息率界）。
  - **vs 硬件实现 penalty**：约 1/7（L035，独占形态）。
  - 注：池里相当一部分 abstract 无 dB 数字（标信息不足），尤其 Spalvieri 团队理论自切和 conference paper。

- **横向多样性**：角度集中度**中高**——信息率界 + dual-stage pilot 是两大主流，占池约 30-40%。独占角度有：VLSI 实现（L035）、PS 场景 CPR（L009）、XPIC 自适应 Kalman（L030）、DLAE CNN（L053）。整体看 Spalvieri 大点的"切口已被切得很密"，剩余独占小切口偏硬件/新场景/新工具三向。

- **动机叙事常见套路**：
  - **"X 既有方法在 Y 场景失效/次优 → 提 Z"**（约 50%）：L003（blind 在 cycle-slip 失效）、L009（PS 损坏 BPS）、L053（PSAM 高阶+强 PN 失效）、L030（PLL 双极化次优）。
  - **"X 性能未量化 → 量化 X"**（约 25%）：L004（信息率界）、L035（VLSI 能效）、L008（overhead 最优）。
  - **"X 已被广泛研究但 Y 维度未覆盖"**（约 15%）：L030（XPIC 场景）、L009（PS 场景）。
  - **"open problem 自报 → 填空白"**（约 10%）：sat.1553 自报 / B1 切入点属此类。
  - 提示：B1 切入点用的"open problem 自报"套路在池里**占比较低**（池里更常见的是"既有方法失效"套路）。

- **实现复杂度梯度**：
  - **纯仿真/理论**：约 50%（L004 信息率界、L030 Kalman 仿真、Spalvieri 团队多数理论自切）。
  - **FPGA 加速仿真**：约 5%（L064 Börjeson）。
  - **VLSI/CMOS 流片**：约 3%（L035 Börjeson，独占最高复杂度）。
  - **实测（实验数据 offline processing）**：约 25%（L008 superchannel 实测、L009 PS 实验、L012 Wakayama、L028 Yang）。
  - **训练 + 推理（DL）**：约 5%（L053/L054）。
  - **信息不足**：约 12%（conference paper 无 abstract）。
  - 提示：B1 切入点若做最简 MVE 属"纯仿真"档，复杂度门槛低；若要做实测需 OSL 硬件（sat.1553 仿真假设可复用）。

---

## 5. 自评

- **6 维信息缺失率（诚实标）**：
  - **大点锚**：缺失率 ~5%（abstract 都能看出引哪个大点）。
  - **切的角度**：缺失率 ~5%（abstract 都能分类）。
  - **dB 形态**：缺失率 ~30%（约 1/3 篇 abstract 无 dB 数字，需查正文；尤其 Spalvieri 团队理论自切和 conference paper）。
  - **横向多样性**：缺失率 ~10%（依赖池整体扫描，conference paper 无 abstract 时难判）。
  - **动机叙事**：缺失率 ~15%（多数 abstract 能看出 intro 收窄路径，少数纯方法 abstract 看不出）。
  - **实现复杂度**：缺失率 ~25%（abstract 经常不写算力/数据/硬件需求）。
  - **整体最高缺失维**：dB 形态 + 实现复杂度（abstract 限制），主线汇总时这两维需查正文补全。

- **降维建议**：
  - 建议主线汇总时**保留 6 维但降权 dB 形态 + 实现复杂度**——这两维 abstract 缺失率高，强行填会脑补。可改用"标 √/× 是否有 dB 数字"+"标 仿真/实测/VLSI/DL 档位"的轻量分类，不做完整描述。
  - **大点锚 + 切的角度 + 动机叙事**三维信息密度最高、缺失率最低，建议作为切法地图主结构。
  - **横向多样性**维度对"看别人怎么找小切口"最有价值，建议保留但需配合池整体扫描（单篇看不出横向）。
