# 切法地图定稿（B1-B5，对话 2 产出）

> 来源：B1-B5 切法地图草稿（`_cut-map-draft-b1-b5.md`）+ dB/复杂度全文核验（`_cut-b1b2b3-verify.md` + `_cut-b4b5-verify.md`）
> 日期：2026-07-05 | 状态：**定稿（B1-B5 范围）**，B6-B12 待对话 3 补
> 纪律：D018 中性提取扩展（只标模式不判"值得切/不值得"）+ profile 第 7 次"急于推进"防线（汇总只描述分布不推荐方向）+ FR-26（dB 数字带条件 + 口径统一警示）

---

## 0. 这份地图是什么（用户核心诉求对齐）

用户原话："别人都咋弄的？是怎么排列组合方法水一篇的？我也想水一篇该咋弄"+"看 cited-by 怎么从大点找到小点"。

这份地图回答 **"切的动作本身"**——别人怎么在引用网络里找到自己的小切口的。**定稿版相比草稿的升级**：dB 形态 + 实现复杂度从"abstract 粗档（30-40% 缺失）"升级到"全文细档（26 篇里 12 篇升级到细档）"，让 dB 维度可用于 D005"赢 baseline 几 dB"实操判断。

**这份地图不告诉你"该切哪一刀"**（那是 Step 4a 用户侧动作），只告诉你"别人是怎么切的 + 哪些切法能赢 baseline 几 dB"。

---

## 1. "被反复切的超级大点"分布（B1-B5 横切，核验后）

| 大点 | 池规模 | 被切的子点（按密度） | 主流切法角度 | 团队自切集中度 |
|---|---|---|---|---|
| **Spalvieri pilot-aided 相位估计**（B1 锚 sat.1553[57]） | 85 篇 | ① 信息率界（最密集）② Kalman carrier recovery ③ pilot-aided dual-stage ④ trellis demod | 性能极限 / 架构替换 / 参数调度 / 工具借用 | **极高**（~18+ 篇 Barletta/Magarini/Spalvieri 合著）|
| **Paillier 星地相干下行 ground receiver**（B4/B5 锚） | 43 篇 | ① 系统级参考架构 ② AO/波前校正 ③ 接收机硬件 ④ DPLL/OPLL 同步本体 | 场景迁移 / 硬件实现 / 架构替换 / 工具借用 | 中（L039 Paillier 自引延伸；B4/B5 同 BUPT 团队续作）|
| **传统 TS-FOE + Park 帧同步 + QPSK 分圈线**（B3 真正子大点）| ~4 篇 | FS+FOE 共享 TS / 共享 pilot / 分集合并 | 联合建模 / 工具借用 / 场景迁移 | 高（oe 是 jphot 同课题组续作；LCOMM 自前作 PTJ 续作）|
| **sat.1553 综述本身** | — | 综述自身即大点，**事后归并** L440/L558/L582/L790 切口 | 综述延伸 | — |

**核验后关键确认**：sat.1553 全文核验（content.md 1581 行）坐实——它是 OSL DSP 算法地图综述，通过 L440（pilot 窗口 open problem）+ L558/L582（fade 冻结）+ L790（子系统协同）**事后归并**出三个切口；池里 4 篇自己的大点锚各不相同（张思齐锚 QPSK 分圈经典 / LCOMM 锚自前作 PTJ / jphot 锚传统 TS+Park / oe 锚同课题组 jphot）。

---

## 2. 切法角度分布（B1-B5 横切，26 篇样本）

| 切法角度 | 篇数（粗估）| 典型代表 | 在"水一篇"里的角色 |
|---|---|---|---|
| **场景迁移** | ~9 | L009 PS-CPR / L027 短时谱搬星地 / Paillier 池 11 篇场景变体 | **Paillier 安全区**，拥挤但模板多 |
| **架构替换** | ~6 | L003 pilot+blind dual-stage / L008 双反馈环 / L036 ODPLL Z 域 / LCOMM 解耦 | 中等密度，**核验后确认有 dB 但多为内部对照/绝对指标** |
| **参数调度** | ~5 | L008 overhead 优化 / L005 PCS+符号率 / B1-Q1 自适应 N | 中等密度，**风险分化**（B1-Q1 待 MVE / L005 吞吐维度错位）|
| **硬件实现** | ~5 | L035 VLSI CMOS / L041 μICR 空间鉴定 / L003 SiPh / Paillier 池 10 篇 | **Paillier 安全区**，dB 维多无（绝对指标/pass-fail）|
| **工具借用** | ~4 | L053 CNN PN / L013 attention / L024 RL geometric / L036 Z 变换 | 独占区，**有 dB 空间**（L053 +2dB / L024 BER 量级）|
| **联合建模** | ~3 | L030 XPIC Kalman / jphot FS+FOE+MRC / 张思齐 FOE↔CPE | 独占区（B3 池主流），**有 dB 空间**（jphot +2-3dB / L030 vs PLL）|
| **性能极限 / 信息论界** | ~3 | L004 信息率界 / L010 coherent vs IM/DD IT / L019 OPLL 混沌 | 独占区，**无 dB 仅结构性** |
| **综述延伸** | ~3 | sat.1553 自报 / L001 综述+demo / L026 综述 | 套路占比较低（Spalvieri 池 ~10%）|

---

## 3. dB 增益形态分布（核验后，**关键升级**）

> **核验后 dB 形态分布是定稿版核心升级**。26 篇里 12 篇从 abstract 粗档升级到全文细档，dB 数字带条件 + 对照对象 + 口径警示。

### 3.1 dB 形态分布（核验后精确）

| dB 形态 | 篇数 | 典型代表 + 核验后精确数字 | D005 够格梯度含义 |
|---|---|---|---|
| **vs 传统 baseline（明确 SNR/BER dB）** | ~6 | **sat.1553 L440 pilot 在场景 4 比 VV+diff 好 1 dB**（@ BER 1e-3，4 场景准静态仿真）/ **jphot FSTS 4 支路 MRC 强湍 +2.09 dB（4-QAM 320 符号）/ +3.41 dB（16-QAM 320 符号）**（@ FEC=3.8e-3，FSO 相位屏 Cn²=1e-14，vs 传统 TS-FOE）/ **oe 4 支路 MRC 强湍 +1.78 dBm（QPSK）/ +2.46 dBm（16QAM）**（@ FEC=1.5e-3，Cn²=1e-14，**注意 dBm 灵敏度非 SNR penalty**）/ **张思齐 vs QPSK 分圈 +0.67/+0.76/+0.71 dB**（B2B/弱湍/强湍，纯仿真）/ **L053 DLAE 距 Genie gap 0.8 dB（256-QAM）/1.2 dB（1024/4096-QAM）+ PSAM gap > 3 dB → DLAE vs PSAM 实际差 ~2-3 dB**（@ BER 1e-6，5G-NR LDPC，AWGN 无线 backhaul）/ **Paillier 湍流 fading 致 2.3 dB BER penalty**（@ BER 1e-4，vs AWGN 理论，BPSK 10 GBaud）| **D005 第一梯队**（dB 量级明确 + 对照是传统 baseline）|
| **vs 内部对照（自报改进或前作对比）** | ~6 | **LCOMM LPT vs PTJ +0.9 dB Q-factor**（@ OSNR 25 dB，40 km SSMF）+ RSOP 100 Mrad/s + RMSE 4.47° vs 17.99° / **L008 B4 双环 MSE 2.0e-6 → 5.1e-7（4× 改善）+ ±920 MHz @ 0.5 dB 灵敏度代价 + 285 GHz/s + 0 dB 定点代价**（@ 2.5-GBaud PM-QPSK Arria 10 FPGA）/ **L013 attention 有效率 +58.4% / 可靠性 gain +34.2% / 最强 vs 最弱湍流慢衰落差 11 dB**（abstract 级未核）/ **L024 RL SCD vs DD BER ↓ 2 量级 / GS-SCD vs SCD BER ↓ 1 量级**（@ 20 Gbps PAM4，Cn²=1e-15~1e-13，纯仿真）/ **Matsuda +0.6 dB**（摘要级，vs 自身无 freeze baseline）/ **sat.1553 soft DQPSK penalty 2.5 dB / hard DQPSK 0.75 dB / soft vs hard FEC 2 dB** | **D005 边际够格**（dB 有但对照非传统 baseline）|
| **绝对指标无外部 dB 增量** | ~5 | **L027 B5 捕获范围 ±4.5 GHz + 残频 <140 MHz / <5 MHz + 灵敏度 −48 dBm**（核验后**确认无 vs baseline dB 增量**，B2B 实时 FPGA demo 无湍流信道）/ L005 +70~100 Gbps 吞吐（**维度错位**：吞吐非同步 dB）/ L041 μICR pass/fail / L008 严格说也在这一档（仅自报绝对值）| **D005 不够格**（无 vs baseline dB）|
| **无 dB 仅结构性** | ~3 | L004 信息率界 / sat.1553 三切口 / L035 硬件 penalty | 理论/结构维度，D005 不适用 |
| **稳定性裕度（非通信 BER dB）** | ~2 | **L036 ODPLL Z 域 Bode 裕度 16.8 dB / 55 dB 增益裕度 / 3 dB 截止 1.12 MHz / 时间常数 1.3 µs**（@ 419 km LEO，85 MHz/s Doppler，2 MBaud on 8 MHz carrier，**纯仿真 behavioral**）| 稳定性维度，**非 D005 够格标尺** |
| **信息不足（未落盘）** | ~6 | L003（OAM 错配，真 SiPh 未落盘）/ L001（DOI 待核）/ L010/L013/L019/L039（未落盘）+ Spalvieri 池 6 篇（L004/L003/L008/L030/L009/L035 未落盘）| 待全文核验 |

### 3.2 核验后关键发现（**Paillier 安全区恰恰是 dB 最难出区结论仍坚挺**）

> B4/B5 子 agent 核验 5 篇落盘（L005/L008/L027/L036/L024）后明确报告：**5 篇落盘里 0 篇给出"vs 外部具名 baseline 改善 X dB BER/OSNR"**——L005 维度错位（吞吐）/ L008 自报绝对值（MSE+范围）/ L027 绝对指标无 baseline / L036 稳定性裕度非 BER / L024 BER 量级非 dB + 纯仿真。

**对"我也想水一篇"的含义（中性观察非推荐）**：
- 想做 D005 够格梯度（赢传统 baseline 几 dB）→ 切**架构替换 / 工具借用 / 联合建模**区（jphot +2-3 dB / L053 +2-3 dB / L030 vs PLL）
- 想做 demo/工程论文（无 dB 也毕业）→ 切**硬件实现 / 场景迁移**区（Paillier 池安全区，模板多但 dB 难出，B4/B5 自身都在这档）
- 想做理论论文（无 dB 仅结构性）→ 切**性能极限 / 信息率界**区

### 3.3 口径统一警示（定稿新增，FR-26）

> 核验后发现 5 个 dB 口径陷阱，主线引用时必须保留：

1. **jphot + oe 是灵敏度 dBm 非 SNR penalty dB**——单位差异，横向对比"赢 baseline 几 dB"时 dBm 灵敏度与 dB SNR penalty **不可直接相加**（`_cut-b1b2b3-verify.md` §篇 13/14）
2. **L053 DLAE "over 2 dB" 是间接计算**——实际是 (PSAM gap > 3 dB) − (DLAE gap 0.8~1.2 dB)，引用时标"DLAE 距 Genie 0.8/1.2 dB，PSAM 距 Genie > 3 dB"而非笼统"2 dB"
3. **sat.1553 L440 "pilot 比 VV+diff 好 1 dB" 不是 B1 切入点增量**——这是 pilot vs VV 的差，不是自适应 N vs 固定 N 的增量（B1 切入点增量 sat.1553 自承未量化）
4. **Paillier "湍流相位可忽略"条件性极强**——依赖 BPSK 单一调制 + 10 GBaud + 理想 timing + AGC 恒幅 + AO 校正后活塞慢（~1ms），引用时必须带条件不能简化为"分治够用"
5. **张思齐 dB/复杂度未对照原文核验**——B3 笔记数据标"论文原报未脑补"但原文不在 papers/ 下，引用具体百分比（13.8%/47.6% 等）需补 CNKI 全文核验

---

## 4. 动机叙事套路分布（B1-B5 横切）

| 叙事套路 | 占比 | 典型代表 | 套路结构 |
|---|---|---|---|
| **"X 已被研究但 Y 场景/维度未覆盖"** | ~35% | L005 / L008 / L027 / L013 / L024 / L030 / L009 | "Paillier/Spalvieri 已证 X 在 A 场景可行 → 但 B 场景未覆盖 → 本工作填 B" |
| **"既有方法失效/次优 → 提 Z"** | ~25% | L003 / L009 / L053 / L030 / B1-Q1 / sat.1553 | "blind 在 cycle-slip 失效" / "PS 损坏 BPS" / "PSAM 高阶+强 PN 失效" |
| **"前作有缺陷 → 改进"** | ~15% | LCOMM（PTJ 偏振衰落→解耦）/ oe（Park 侧峰→PRBS 消侧峰）/ L036（Paillier 经验式→Z 域建模）| "前作/经典方法有 X 缺陷 → 改进" |
| **"绕开而非赢"** | ~10% | L005（PCS+符号率绕开非对称滤波）/ L024（self-canceling 绕开相位噪声）| "不动 Paillier 同步本体，换一个维度绕" |
| **"借 ML/NN 工具到 FSO"** | ~10% | L013（attention）/ L024（RL）/ L032（NN）/ L053（CNN）/ L033（semantic）| "ML 在 Y 领域成功 → 借到 FSO 的 X 子环节" |
| **"open problem 自报 → 填空白"** | ~5% | sat.1553 L440/L790 自报 / B1 切入点 | 综述作者亲口说"未量化/未做"→ 直接填 |

**B1 切入点用的"open problem 自报"套路在池里占比最低（~5%）但证据链最强**（综述作者亲口说"未量化"）。

---

## 5. 实现复杂度梯度（核验后精确档位）

> 核验后复杂度档位精确到 FPGA 型号 / 链路长度 / 湍流强度。

| 复杂度档 | 篇数 | 典型代表 + 核验后精确参数 | "水一篇"门槛 |
|---|---|---|---|
| **纯仿真/理论** | ~10 | **sat.1553**（4 场景准静态仿真，QPSK 10/28 GBaud，σp²=0.029~0.25，无硬件）/ **张思齐**（FOE 符号块 320/960/1024，CPE 符号块 64，B2B/弱湍/强湍三档）/ **jphot**（Schmidt 相位屏 Cn²=1e-16/1e-14，10 GBaud PM 4/16-QAM，耦合效率 67.3%/4.84%）/ **oe**（多相位屏 + 室内 B2B Cn²=6e-11）/ **L024**（20 Gbps PAM4 Gamma-Gamma + 高斯近似，Cn²=1e-17~1e-13）/ **L004/L010/L019**（理论）| **最低**（一台机器 + Python/MATLAB）|
| **仿真 behavioral model** | ~2 | **L036**（MATLAB-Simulink Z 域 TF，2 MBaud on 8 MHz carrier，419 km LEO 85 MHz/s Doppler，标未来 FPGA+photonic 集成已到货待实测）| 低 |
| **FPGA / 实验室硬件 demo** | ~8 | **B4 L008**（Intel Arria 10 FPGA 10ax066k3f40，12-bit 定点 9.1K+1.4K ALE，2.5-GBaud PM-QPSK 实时，**无湍流建模**）/ **B5 L027**（Intel Arria 10 FPGA + 5 GSa/s 8-bit ADC，2.5-GBaud PM-QPSK 实时 B2B，**无湍流信道**）/ **L035 VLSI**（22 nm CMOS）/ **L003 SiPh**（待核 DOI）/ **L013 attention**（10 m FSO 7 级湍流 demo，未落盘）/ **Matsuda**（FPGA 实时 4 Gbps，**型号/资源未给**，仅摘要）| 中（需 FPGA / 光学器件）|
| **实验室 + outdoor/野外实测** | ~3 | **L001**（42 m 48h outdoor，未落盘）/ **L039**（Jungfraujoch-Zimmerwald 瑞士野外，未落盘）/ **L005**（半物理 600 Gbps PCS-64QAM，AWG Keysight M8194A + LO 频偏物理模拟 Doppler ±15 GHz）| **高**（野外链路 / 长期实测）|

**梯度规律（核验后坐实）**：协同角度越宽/越靠近综述 open problem 端（张思齐、sat.1553），硬件实现越弱；协同角度越靠近工程痛点端（LCOMM、Matsuda、B4/B5），硬件实现越强。

---

## 6. 团队自切模式（中性观察，用户已纠正"不是同门"）

| 模式 | 案例 | 切法特征 |
|---|---|---|
| **同一团队连续切自己大点** | Spalvieri 团队（~18+ 篇）/ B4-B5 BUPT 团队（Na Liu/Cheng Ju/Jiamin Fan）/ jphot-oe 同课题组 | "自己切自己大点"形成连续轨迹，切法偏理论延伸 |
| **自前作续作** | LCOMM（自 PTJ +0.9 dB）/ oe（自 jphot FSTS + 同质改进）/ L039（Paillier 自引延伸）| "前作有缺陷 → 改进"叙事 |
| **跨团队接力** | L003 Spalvieri dual-stage → L009 Barbosa 迁 PS 场景 / B1 切入点接 sat.1553 open problem | 不同团队在不同维度接力切同一大点 |

---

## 7. B1-B5 切法地图一句话总结（中性，不判 Go/Kill）

**别人怎么从大点切小点的**（B1-B5 横切 26 篇样本，核验后）：
1. **切哪个大点**：Spalvieri 85 池 / Paillier 43 池是饱和安全区（团队自切密集），TS-FOE+Park+QPSK 分圈线是未饱和子大点（独占空间大）
2. **切什么角度**：8 类角度，**拥挤区在场景迁移+硬件实现（Paillier 池过半）**，**有 dB 空间区在架构替换+工具借用+联合建模**
3. **dB 怎么报（核验后精确）**：D005 第一梯队（vs 传统 baseline 明确 dB）= sat.1553 pilot 比 VV+diff 1 dB / jphot 4 支路 MRC 强湍 +2-3 dB / L053 DLAE vs PSAM ~2-3 dB / Paillier 湍流 2.3 dB penalty / 张思齐 vs QPSK 分圈 +0.67-0.76 dB；**Paillier 安全区（场景迁移+硬件实现）5 篇落盘 0 篇给出 vs 外部 baseline dB**
4. **intro 怎么讲**：5 套路，"X 已被研究但 Y 未覆盖"绝对主流（~35%），"open problem 自报"占比最低（~5%）但证据链最强
5. **实现多复杂（核验后精确档）**：纯仿真（最低门槛，sat.1553/张思齐/jphot/oe/L024/L036）→ FPGA demo（B4/B5 同 Arria 10 模板）→ outdoor 实测

**给"我也想水一篇"的尺子（中性参照系，不推荐方向）**：
- 选**切法角度** = 选"D05 够格难度"：架构替换/工具借用/联合建模有 dB（核验后 jphot +2-3 dB / L053 +2-3 dB 是样本）；场景迁移/硬件实现无 dB（Paillier 安全区 5 篇落盘 0 篇出 dB）；性能极限/综述延伸理论维度
- 选**大点** = 选"独占切口空间"：饱和大点参考多但切口少；未饱和子大点切口多但参考少
- 选**叙事套路** = 选"intro 立得住的证据链强度"：open problem 自报最强但稀少；X 已被研究但 Y 未覆盖最通用
- 选**复杂度档** = 选"毕业门槛"：纯仿真最低（B4/B5 同 Arria 10 是 FPGA demo 模板）

---

## 8. 待补 + 已知债务

- **样本局限**：B6-B12 七点未提取（稀池/天然稀，B6 仅 2 / B7 空 / B10-B11 各 1，切法样本密度可能不够画分布）——对话 3 待用户拍是否补
- **未落盘 14 篇**（Spalvieri 池 6 + Paillier 池 8）dB/复杂度保持粗档，其中 **L030 XPIC Kalman / L035 VLSI / L010 IT / L013 attention / L039 feeder 实测** 是高价值补下候选（abstract 已带 dB 数字或独占角度）
- **DOI 错配 2 处**（定稿新增债务）：
  - L003 `s41598-026-40704-2` 实为 OAM 结构光论文非 SiPh 论文（真 SiPh 论文 DOI 待核）
  - L001 Guiomar 综述 DOI `10.1109/jlt.2022.3164736` 在 papers/ 下不存在（真 DOI 待核）
- **张思齐学位论文原文未在 papers/ 下**（B3 笔记数据未对照原文核验，引用具体百分比需补 CNKI 全文）
- **B5 锚 paywall 已破**（用户 2026-07-04 手动下全文 252 行已落盘，核验后确认无 dB 增量）

---

## 9. 自评（定稿诚实度）

- **核验后 dB 形态分布的实操可用性**：从草稿"abstract 粗档 30-40% 缺失"升级到定稿"12/26 篇细档 + 5 个口径警示"，**dB 维度现在可用于 D005'赢 baseline 几 dB'实操判断**（草稿做不到）
- **关键定稿升级**：①Paillier 安全区恰恰是 dB 最难出区结论核验后坚挺（5 篇落盘 0 篇出 dB）②口径统一 5 警示（dBm vs dB / L053 间接计算 / sat.1553 条件性区分 / Paillier 条件性 / 张思齐未核原文）③复杂度档精确到 FPGA 型号 + 链路长度 + 湍流强度
- **守纪律**：定稿只描述分布不推荐方向（D018 中性提取扩展 + profile 第 7 次防线）；每条 dB 数字带条件 + 对照对象（FR-26）；DOI 错配诚实标出（FR-26）；团队维度只标作者名不推断师承（用户纠正"不是同门"）
- **局限诚实标**：B6-B12 未补是已知债务（对话 3 待用户拍），14 篇未落盘保持粗档不强填
