# [R001] §1.2.2 载波同步文献分类

> 2026-05-31 | 关联：2026-05-31-thesis-writing, H007 Phase 1

## 调研问题

§1.2.2（低轨卫星激光通信载波同步研究现状）应引用哪些文献？如何按叙事逻辑组织？目标 1500 字、15-20 处引用。

## 数据来源

- `material-chapter-literature.md`：Ch1(#9-12,#16,#19-20,#23-25) + Ch4(#1-18)
- `R007-ch4-literature-review.md`：~200 条检索去重后 20 高相关论文
- `H007-section-1.2-handoff.md`：分类框架

## 去重论文池（21 篇）

| # | 论文 | 作者(年份) | 引用 | 状态 | 核心贡献 |
|---|------|-----------|------|------|----------|
| 1 | Carrier-phase recovery for coherent optical systems: Algorithms, challenges and... | Neves (2023) | 39 | ⬚ | CPR算法综述，VV/BPS/Pilot全覆盖 |
| 2 | 星地相干激光通信系统中信号处理与补偿技术研究 | 闫旭 (2022) | 1 | ⬚ | 星地+相干+信号处理+补偿 |
| 3 | Space-Ground Coherent Optical Links: Ground Receiver Performance With AO | Paillier (2020), JLT | 35 | ✅全文 | 星地DPLL+AO，FOE捕获1.4ms，湍流BER惩罚2.3dB |
| 4 | Carrier recovery for satellite-to-ground coherent laser communication systems | Liu (2023), OC | 15 | ⬚ | VV/BPS星地链路载波恢复对比 |
| 5 | Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links | Wang (2025), ACP | 0 | ✅全文 | FPGA LEO多普勒实时跟踪±8GHz |
| 6 | Joint Doppler and Phase Noise Compensation for Inter-Satellite Coherent Laser | Zhao (2025), ICCSN | 0 | ✅全文 | 联合多普勒+相位噪声，<0.5dB损失 |
| 7 | Digitally mitigating Doppler shift in high-capacity coherent FSO LEO-to-Earth links | Fernandes (2023), JLT | 31 | ✅ | LEO多普勒数字补偿标杆 |
| 8 | Digital Pre-Compensation of Doppler Frequency Shift in Coherent Optical Satellite | Almonacil (2020), ECOC | 6 | ⬚ | 发射端数字预补偿±10GHz |
| 9 | Enhanced frame synchronization and carrier recovery in coherent FSO communication | Wang (2024), OE | 2 | ⬚ | FSO湍流帧同步+载波恢复联合 |
| 10 | A noise-tolerant carrier phase recovery method for inter-satellite coherent optical | Hu (2025), Electronics | 3 | ⬚ | 噪声容忍型CPR，二阶反馈+前馈混合 |
| 11 | A low-complexity joint compensation scheme of carrier recovery for coherent FSO | Tang (2023), Photonics | 7 | ⬚ | 联合载波恢复(频偏+相位)低复杂度 |
| 12 | Low-complexity carrier phase estimation algorithms for space coherent optical communication | Yang (2025), SPIE | 0 | ⬚ | VV vs BPS空间场景直接对比 |
| 13 | Recurrent neural network enabled adaptive carrier phase recovery | Shi (2025), SPIE | 0 | ⬚ | RNN自适应CPR，DL-based最新 |
| 14 | Transparent Carrier Phase Recovery Based on ANN | Blatter (2025) | 0 | ❌ | ANN载波相位恢复 |
| 15 | Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links | (2025), Int. J. Satellite | 4 | ⬚ | 星地相干光链路DSP算法综述 |
| 16 | 相干光通信载波相位恢复算法研究 | 徐文婧等 (2021) | 10 | ❌ | 中文CPR综述 |
| 17 | 基于数字相位恢复算法的QPSK自由空间相干光通信系统 | 管海军等 (2019) | 8 | ❌ | QPSK+FSO+数字相位恢复 |
| 18 | 空间相干光通信中基于DSP的多普勒频移补偿技术 | 向劲松等 (2011) | 3 | ❌ | 多普勒频移补偿经典中文 |
| 19 | Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO | Wang (2023), IEEE PJ | 8 | ⬚ | 空间分集FSO载波频偏估计 |
| 20 | Real-time FPGA prototyping of Doppler frequency shift compensation using DSP-assisted AFC | (2024), Optics Letters | 1 | ⬚ | FPGA AFC多普勒补偿 |
| 21 | Digital Estimation and Compensation of Doppler Shift for Coherent Optical Satellite | Yan (2026) | 0 | ⬚ | 最新多普勒数字估计+补偿 |

注：Ch1 #24(低轨时频联合同步 2026)和 #25(朱勇 2003 多普勒影响)因质量/年代原因降为 P2 备选，未纳入主池。

## 叙事分类（D4 问题前置 + D2 递进评价）

### 结构逻辑

```
光纤成熟方法 → LEO多普勒挑战(已有解决方案) → CPR在FSO适配(部分解决) → 湍流影响(明确空白) → DL新兴方法(空白)
```

每段先说已有方案及其局限（D4），再引出下一层的未解决问题。

### A. 载波同步基本架构与光纤中的成熟方法（开段，2-3 句，2-3 篇引用）

| # | 论文 | 叙事角色 |
|---|------|----------|
| 1 | Neves 2023 (39 cites) | CPR算法全景综述——VV/BPS/Pilot在光纤中成熟，确立技术基线 |
| 15 | Review DSP 2025 | 星地相干DSP综述，补充系统视角 |
| 16 | 徐文婧 2021 | 中文CPR综述，补充国内研究背景 |

**D4 锚点**：以上方法均在光纤/实验室条件下验证，LEO星地链路引入多普勒和大气湍流两个新挑战。

### B. LEO 多普勒频偏挑战与补偿方案（~400 字，6-7 篇引用）

| # | 论文 | 叙事角色 |
|---|------|----------|
| 7 | Fernandes 2023 (31 cites) | LEO多普勒数字补偿标杆方案——频偏±8GHz下的数字域补偿 |
| 8 | Almonacil 2020 (6 cites) | 发射端数字预补偿——从源头消除多普勒 |
| 6 | Zhao 2025 | 联合多普勒+相位噪声补偿——QPSK下<0.5dB损失 |
| 21 | Yan 2026 | 最新多普勒数字估计+补偿方案 |
| 5 | Wang 2025 | FPGA实时跟踪实现——证明可行性 |
| 18 | 向劲松 2011 | 多普勒补偿中文经典，引入问题 |
| 20 | FPGA AFC 2024 | FPGA AFC实现补充 |

**D4 锚点**：多普勒频偏通过星历预补偿+数字跟踪已基本解决（Fernandes 2023, Almonacil 2020）。残余频偏通常在 CPR 容忍范围内。但大气湍流引起的相位波动尚无系统解决方案。

### C. 载波相位恢复在星地/FSO 场景的适配（~500 字，5-6 篇引用）

| # | 论文 | 叙事角色 |
|---|------|----------|
| 17 | 管海军 2019 (8 cites) | QPSK+FSO+数字相位恢复——光纤方法迁移到FSO的早期尝试 |
| 4 | Liu 2023 (15 cites) | **核心对照**：VV/BPS在星地链路载波恢复对比——VV适合QPSK，BPS适合高阶调制 |
| 12 | Yang 2025 | VV vs BPS空间场景直接对比——低复杂度CPR |
| 10 | Hu 2025 (3 cites) | 噪声容忍型CPR——前馈+反馈混合，抗噪声 |
| 3 | Paillier 2020 (35 cites) | 星地DPLL+AO方案——光学锁相环替代数字CPR |
| 11 | Tang 2023 (7 cites) | 联合载波恢复(频偏+相位)低复杂度——FSO场景 |
| 19 | Wang 2023 FOE (8 cites) | 空间分集FSO频偏估计——分集辅助 |

**D4 锚点**：以上方案在 AWGN/弱湍流下表现良好，但均未系统建模湍流强度（弱/中/强）对不同 CPR 算法性能的影响。Liu 2023 做了星地对比但未考虑湍流；Paillier 2020 考虑了湍流但重点是 AO 而非 CPR 算法对比。

### D. 大气湍流对载波同步的影响——明确研究空白（~200 字，2-3 篇引用）

| # | 论文 | 叙事角色 |
|---|------|----------|
| 3 | Paillier 2020 (35 cites) | 已发现湍流BER惩罚2.3dB，但未系统分析CPR算法在湍流下的性能差异 |
| 9 | Wang 2024 (2 cites) | FSO湍流帧同步+载波恢复联合——仅单一方案，未做算法对比 |

**D2 递进评价**：Paillier 2020 揭示了湍流对相干接收的惩罚，Wang 2024 在湍流下实现了载波恢复，但**两者均未系统分析不同湍流强度下 VV/BPS/Pilot 三种算法的性能差异**。这是 §1.2.2 的核心空白，直接支撑创新点(2)。

### E. DL 辅助载波同步——新兴方向（~150 字，2 篇引用）

| # | 论文 | 叙事角色 |
|---|------|----------|
| 13 | Shi 2025 | RNN自适应CPR——DL-based CPR在光纤场景的首次成功 |
| 14 | Blatter 2025 | ANN载波相位恢复——透明调制格式 |

**D4 锚点**：Shi 2025 和 Blatter 2025 均仅在光纤场景验证，FSO 湍流场景下 DL 辅助载波同步完全空白。

## 引用精选（推荐 18 篇，目标 15-20）

按叙事优先级排序：

| 优先级 | 论文 | 理由 |
|--------|------|------|
| **必引** | Neves 2023 | CPR综述基线 |
| **必引** | Liu 2023 | 核心对照论文（VV/BPS星地对比） |
| **必引** | Paillier 2020 | 唯一涉及湍流+相干接收+CPR的论文 |
| **必引** | Fernandes 2023 | LEO多普勒补偿标杆 |
| **必引** | Wang 2024 | 湍流+载波恢复，直接指向空白 |
| P1 | Zhao 2025 | 联合补偿最新 |
| P1 | Yang 2025 | VV/BPS空间场景补充 |
| P1 | Hu 2025 | 噪声容忍CPR最新 |
| P1 | Almonacil 2020 | 预补偿方案 |
| P1 | 管海军 2019 | 中文FSO相位恢复参考 |
| P1 | Shi 2025 | DL-CPR代表 |
| P2 | Review DSP 2025 | 系统综述补充 |
| P2 | Tang 2023 | 联合载波恢复 |
| P2 | Wang 2025 | FPGA实现参考 |
| P2 | Yan 2026 | 多普勒最新 |
| P2 | 徐文婧 2021 | 中文综述 |
| P2 | 向劲松 2011 | 中文经典 |
| P3 | Blatter 2025 | DL-CPR第二篇 |

## 写作约束提醒

- §1.2.2 目标 ~1500 字，15-20 处引用
- 不出现论文结论级内容（VV方差公式、EKF结构等）
- 每段先说局限（D4），再做递进评价（D2）
- 末尾需自然引出"湍流对CPR算法性能的系统分析缺失"→创新点(2)
- §1.2.1→§1.2.2 过渡桥梁：信道估计精度→残余估计误差→载波同步鲁棒性需求

## 范文写法分析

### 董凡 §1.2.2 载波恢复算法研究现状（直接相关，质量 3/5）

**结构**：FOE→CPR 两段式，每段内按算法族递进排列。

**递进评价模式（D2）执行良好**：
- Mth 算法[21] → "精度有限" → Fatadin 改进[22] → "只有 50% 星座点可用" → D.Huang 两级 Mth[23] → "均方误差减少两个数量级"
- VVPE[33] → "噪声放大 M 倍" → Gao 低复杂度 VVPE+ML[34] → Valery Filter-CPE[36] → Pfau BPS[39,40] → Xiang QA-BPS[41]

**开段**：一句话说明主题重要性 + 分类依据（前馈 vs 反馈）。

**收段**："载波恢复算法大多应用于光纤通信中，对于存在弱湍流影响下算法性能的研究较少。"——仅一句话，缺口声明偏弱。

**字数**：~2000 字。无公式，纯定性。

**对我们的启示**：
1. FOE→CPR 分类逻辑可直接参考
2. 递进评价（每篇论文→局限→下一篇改进局限）的执行模式可作为 D2 范例
3. 缺口声明太弱——我们需要更强的过渡引出 §1.2.3
4. 董凡未考虑湍流（方向是 FPGA 实现），正好是我们的差异化切入点

### 夏兆宇 §1.2.4 现状总结与启示（质量 5/5，缺口写法标杆）

**结构**：一句总述 → 3 个编号缺口段 → 过渡到 §1.3。

**每个缺口段的固定模式**：
1. "现有X技术面临A与B的双重困境/挑战/局限"（断言句）
2. 当前方法做了什么（肯定）
3. "然而"（转折→局限）
4. 局限的具体后果
5. "这导致..."（收束句）

**关键特征**：
- 每个缺口 1:1 映射一个章节/创新点
- 断言式语气，不 tentative
- 每段 ~150 字，信息密度高

### 写法决策

| 方面 | 采用 | 来源 |
|------|------|------|
| 内部分类逻辑 | FOE→CPR + 多普勒 + DL | 董凡结构 + R007 空白分析 |
| 递进评价模式 | 每篇→局限→下一篇改进局限 | 董凡 D2 执行模式 |
| 缺口声明 | §1.2.2 末尾 2-3 句过渡，不在 §1.2.2 内做独立缺口段 | §1.2.3 有独立缺口节，§1.2.2 只做过渡 |
| 引用位置 | 句中（"Mth算法[21]"），不句首堆叠 | 董凡模式 |
| 字数目标 | ~1500 字 | H007 规格 |

## 对决策的影响

无新决策。确认 R007 的创新点评估结论：湍流对CPR的系统性影响分析是§1.2.2的核心空白点，创新点(2)"载波同步缺乏湍流自适应机制"的文献支撑充分。
