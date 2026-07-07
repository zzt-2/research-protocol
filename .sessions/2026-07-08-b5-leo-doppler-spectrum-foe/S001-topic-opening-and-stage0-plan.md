# [S001] 开题 + 阶段 0 六项规约设计 + 复用基建盘点

> 2026-07-08 | 阶段: 主控对话开题（B5-Q1 第四候选）| 状态: 完成，阶段 0 规约设计完成，交工作对话执行

## 目标

主控对话角色：核查 S031 候选池 + 开 B5-Q1 专题 + 设计阶段 0 六项规约 + 交接给工作对话。不自己执行精读/MVE（那是工作对话的事）。

## 记录

### 触发与决策（D001）

用户"再开另一个方向"（第二次）触发第四候选选择。主控对话先列 S031 剩余可开候选（B3-Q2 / B5-Q1 / D006 边界模式 7 次），用户选 **B5-Q1（LEO Doppler 范围）**。

主控对话派 Explore agent 查详情后发现关键特征：**B5-Q1 不是 dB 增量是范围优势**（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展），D005 "赢 baseline 几 dB" 标尺下不够格。亮给用户后用户选**"开，首验证够格路径"**。

D001 决策记录在 `decisions.md`。voice.md 登记 3 条原话。

### 关键核查发现：B5-Q1 不是 dB 增量是范围优势

**这是主控对话核查的核心价值**——S031 排优先级时把 B5-Q1 列第二档 #6 但没标"不是 dB 增量"。Explore agent 详查 `_cut-b4b5-verify.md:64-66` 发现"本体无'vs baseline 改善 X dB'对比，只给绝对残频/范围指标"。

→ B5-Q1 不是"稳够格"候选（D005 dB 标尺下不够格），但会议门槛放宽允许范围维度够格（BUPT Arria 10 FPGA demo 会议模板）。用户选"开，首验证够格路径"，遵守用户决策权。

**意外发现**：Explore agent 报告 B5-Q1 早在 S003 全文核验阶段就做过详评（`_B5-short-time-spectrum-cfo-increment.md:100-167` 全文增量核验段），S031 第二档 #6 是引用该详评的浓缩。但 S003 只判了 D006/D005/范围三维，**没判 A1 归属和代码复用**——这次详查的增量价值在 A1 + 复用两块。

### B5-Q1 基本面（Explore agent 核查结果）

| 维度 | B5-Q1 | 证据 |
|---|---|---|
| M-C-A | M=[60] Leven Mth-power 时域相位增量（QPSK 专用 M=4）/ C=星地 LEO 下行 Doppler ±4.5GHz @ 56MHz/s / A=M-power FPGA 资源大+M-PSK 专用+改进传统估计范围有限 | `_B5-short-time-spectrum-cfo-increment.md:55-60, 142-147` |
| dB/范围 | **范围优势不是 dB 增量**：±4.5GHz 覆盖 LEO Doppler 全量程 + 残频落 ±312.5MHz 精估范围 + 残频 σ<140MHz（最大 250MHz 含激光抖动）/ 精确补偿后 <5MHz / BER 1e-3 −48 dBm | `_cut-b4b5-verify.md:64-66` + `content.md:23, 29, 143, 147, 167, 149` |
| 范围 | in 星地 LEO 下行（600km 轨道 1550nm）| `content.md:29, 47, 143` |
| D006 | 不撞（前馈频域找谱峰+星历预测调 LO，非环路 TF 联合建模）。**边界残留**：湍流致功率波动归一化前馈合法 / 环路 TF 联合建模则撞 | `_B5-...-increment.md:145, 162` |
| 池类型 | 饱和池 §A（B1-B5），跟 B4 共锚 Paillier 星地相干下行 ground receiver（43 篇大池）| `_cut-map-final-b1-b12.md:19, 23-28` |
| A1 归属 | [Fan/Ju/Liu 等青岛大学+CETC 34 所，Optics Communications 572 (2024) 130981] **已发期刊非预印本**。B5 本身就是星地场景（非论文外改进），论文外可改进空间=加湍流+高阶调制+vs baseline dB | metadata.json + `content.md:1, 47` + `_cut-b4b5-paillier-pool.md:39-46` |

### LEO Doppler 主题跟现有候选的关系（机制正交，无撞车）

| 候选 | 机制 | 范围 | 主题 |
|---|---|---|---|
| **B5-Q1** | 频域正负功率谱面积比 | ±4.5GHz 粗估 | LEO Doppler |
| B7-Q1 | 定时域 TED 增益周期相关 | 0-23GHz 需扫频 | LEO Doppler |
| B4-Q1 | 双反馈环架构 | ±920MHz @ 0.5dB | LEO Doppler |

**三个候选是 LEO Doppler 大动态的三种正交解法**（B5 vs B7 vs B4 运算结构无共享，无数学同族陷阱路径）。B5 vs B7 无同族陷阱（B5 频域积分，B7 定时域周期相关）。

### 复用基建盘点（部分复用，需新增）

`projects/simulation/common/`：

| 组件 | 复用情况 |
|---|---|
| 信道（gg_block + doppler_phase + generate_shared_realization_apsk）| ✅ **完全复用**（TL-13）|
| `fft_foe`（4 次幂 blind QPSK）/ `fft_foe_m0_omega`（M0 升幂找谱峰）| ⚠️ **可作起点骨架**（分块 FFT 复用），但"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"核心算法需新写 |
| `B7Params`（params.py:611-628，DOPPLER_RANGE 0-23GHz + LEO_DOPPLER_RATE）| ✅ **参数族模板可参考**，B5 需扩 params.py 加 B5Params（DOPPLER_RANGE=±4.5GHz / DOPPLER_RATE=56MHz/s / BAUD_B5=2.5Gbaud / 精估范围 ±312.5MHz）|

**新增需求**：`short_time_spectrum_foe`（B5 核心算法）+ 星历预测调 LO 组件（若完整复现 B5 链路）

### 阶段 0 六项规约设计（B5 特殊版）

| 阶段 | 内容 | B5 特殊重点 | 守 |
|---|---|---|---|
| 0.1 | **够格路径验证** | 范围优势在 D005 会议门槛下能不能当 Go 判据（不是 dB 增量），对标 BUPT Arria 10 FPGA demo 会议模板 | INVARIANT 11（B5 特殊）|
| 0.2 | dB/范围溯源核查 | ±4.5GHz 出处 + 残频指标全读原文数值（σ<140MHz / <5MHz / ±312.5MHz）| INVARIANT 12（B5 特殊）+ V6 FR-26 |
| 0.3 | 架构定性 | 湍流致功率波动归一化走前馈路径（合法不撞 D006），禁环路 TF 联合建模 | INVARIANT 13（B5 特殊）+ D006 |
| 0.4 | 公平对照框架 | baseline [60] Leven 还是传统 FFT FOE？范围 fair gain 怎么定义？BER 1e-3 还是 HD-FEC？LEO Doppler 主题差异化（B5 频域 vs B7 定时域 vs B4 双环）| INVARIANT 14（B5 特殊）|
| 0.5 | 参数真相源前置 | Doppler ±4.5GHz / 56MHz/s / 2.5GBaud / 1550nm / 600km / ±312.5MHz，全标 source + 读原文数值 | TL-26 + FR-26 |
| 0.6 | 文件组织规约 | `explore/b5-leo-doppler-spectrum-foe/` 目录 + 命名 + short_time_spectrum_foe 接口定义 | NDA-ML D-007 教训 2 |

### B5 特殊风险（vs NDA-ML/B7/B2 的差异点）

| 风险 | B5-Q1 | 流程对策 |
|---|---|---|
| 够格路径 | 不是 dB 是范围优势 | **阶段 0.1 够格路径首验证**（最高优先）|
| 饱和池竞争 | Paillier 43 篇大池 | 阶段 0.1 BUPT Arria 10 FPGA demo 会议模板对标 |
| D006 边界 | 湍流致功率波动归一化 | 阶段 0.3 前馈归一化定死 |
| 代码新增需求 | short_time_spectrum_foe 需新写 | 阶段 0.6 文件组织 + fft_foe_m0_omega 作起点骨架 |
| A1 归属 | 论文外改进空间窄 | A1 风险中等 |
| 主题撞车 | LEO Doppler 跟 B7/B4 | 阶段 0.4 叙事定位（机制正交）|

## 决策引用

- **D001**（新建）：开 B5-Q1 专题 + 首验证够格路径策略
- 无其他新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**（主控对话开题 + 阶段 0 规约设计，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约全做完才进 sandbox，本对话只设计规约不执行
- **守 3 步上限**：本轮 2 步（①核查 S031 + 派 Explore agent 查 B5-Q1 详情 ②开专题 + 阶段 0 规约设计 + 写 S001/H001）
- **守主控对话角色**：不自己精读/不跑 MVE，核查工作对话产出（Explore agent）+ 亮关键特征给用户

## 后续

### 交工作对话执行

1. **阶段 0.1 够格路径验证**（工作对话核心）：验证范围优势在 D005 会议门槛下能不能当 Go 判据。输出 `explore/b5-leo-doppler-spectrum-foe/_qualification_path_validation.md`
2. **阶段 0.2 dB/范围溯源核查**：±4.5GHz + 残频指标全读原文数值
3. **阶段 0.3-0.6**：架构定性 / 公平对照 / 参数真相源 / 文件组织

### 主控对话跟进点

- 核查工作对话阶段 0.1 的够格路径验证是否真对标了 BUPT Arria 10 FPGA demo 会议模板（不是绕过）
- 核查阶段 0.2 的 dB/范围溯源是否全读原文数值
- B5-Q1 跟 B7 的交叉：B5 够格路径验证结果对 B7 方向决策有交叉验证价值（都是 LEO Doppler 主题）

### 已知风险（交工作对话）

- **够格路径可能崩塌**：如果阶段 0.1 验证后范围优势无法走会议够格路径（BUPT Arria 10 FPGA demo 模板不适用 + 补 dB 对比不真实），B5-Q1 转 Kill
- **饱和池竞争激烈**：Paillier 43 篇大池，B5 走范围维度能否绕开"饱和池是 dB 最难出区"警示需验证
- **代码新增需求成本**：short_time_spectrum_foe 需新写，跟 B2（4 估计器全有）比新增成本高
