# [S005] A3/N1 物理可行性预检：A3 倾向 PASS（机制缺口）+ N1 存疑（锚点纠正 + gain 数据缺失）

> 2026-06-16 续 4 | 阶段: 方向探索（物理可行性预检）| 状态: 预检完成，两候选均"存疑"但性质不对称，需补检索后再判
> 来源: PROMPT-004（A3/N1 物理可行性预检）| 方法: 照 D003 Phase A/B/C

## 目标

验 A3 和 N1 各自的物理可行性——会不会像 B1 那样倒在物理死锁上。派 2 子 agent 并行（各 ≤600s，这次按 harness 实际上限切，未犯 R006 的 900s 错误），带 D003 教训（不只看 E 三检验，看物理前提 + 主导损伤针对性）。验完才有资格谈"几个够、怎么互锁成三章"。

## 记录

### 执行实况（治理记录）

- **2 子 agent 并行，均 ≤600s 内完成，无超时**（R006 教训已吸收——任务量按 harness 600s 切，每 agent 只验一个候选）
- Agent-A3：Phase A 足够（Paillier 正文 §IV-A/B/C 全部直接回答核心问题），Phase B 未启动
- Agent-N1：Phase B 必要——cite=81 closed access 下载失败，转 Semantic Scholar 拿 abstract + 下载替代论文 Elzanaty 2020（arXiv:2005.02129）精读
- **主对话交叉验证 3 条关键断言**（AGENTS.md 强制）：① cite=81 = TL-03 陷阱（Semantic Scholar abstract 直证）② Elzanaty 是 IM/DD（content.md line 43）③ Paillier AGC 机制（content.md line 177/186/200，AGC 放大信号也放大噪声，critical SNR +5dB，BER penalty 2.3dB）

### 预检结果 1：A3 = 存疑倾向 PASS（无物理死锁，机制定位需收窄）

**核心结论**：A3 不会像 B1 那样倒在物理死锁上。前馈导频机制无带宽矛盾，攻击的损伤是 Paillier §IV-A/B 量化的主导损伤（残余幅度闪烁）的相位副产物，而非 negligible 活塞相位。

**物理基础判定**：通过。A3 攻的"deep fade 相位跳变" = 幅度骤降→SNR 骤降→相位估计方差暴增（**幅度问题的相位副产物**，主导损伤相关），**不是**湍流活塞相位（Paillier §IV-C line 196 证 negligible）。这是 D003 要求厘清的关键区分，A3 物理基础比 B1 强。

**三重障碍逐一判定（全部工程量，无物理挡死）**：

| 障碍 | 判定 | 依据 |
|---|---|---|
| 多普勒时变 | 工程量 | 残频 100MHz 由数字 CFO 前馈估计 + ephemeris 预补偿；Yang 2026 频域导频 FOE 范围达 ±fs/2 全覆盖；导频间隔与多普勒时间尺度无矛盾 |
| deep fade 相位跳变 | 工程量（正是 A3 攻的目标） | Paillier 已证此问题"可被压"（AGC +5dB 容限即够）；前馈导频在 fade 期间天然不依赖环路稳定 |
| 单孔径无分集 | 不是障碍（D 不变） | Paillier 整篇单 50cm 孔径 AGC+DPLL 已工作；A3 是 DSP 域算法不引入接收阵列硬件，**不命中 D 排除列#2** |

**物理死锁检查（B1 对照）**：**A3 无物理死锁**。
- B1 死锁 = PLL 环路带宽被"窄看活塞 vs 宽跟多普勒"两个相反要求拉扯，单一标量无解
- A3 是**前馈导频相位估计**（Valjus 全 feedforward；Yang 直接算 Jones 矩阵无迭代；Paillier 结论 line 206 也推荐 open-loop）。前馈没有"被拉扯的带宽参数"——导频间隔和功率是两个独立自由度
- A3 自己的潜在矛盾点（已查，不构成死锁）：导频功率 PSR 要大（抗 fade）vs 要小（省数据功率预算）= **功率分配 trade-off，有连续可工作区间**（PSR=−15dB 是 Yang 实测甜点），非 B1 那种无可工作区间的硬矛盾

**为何只判"倾向 PASS"而非无条件 PASS（机制定位缺口）**：
- Paillier 已证 **AGC 补偿**就能把幅度问题压住（PLL 1.4ms 收敛，+5dB 容限，但 BER penalty 2.3dB 残留 + critical SNR 抬升 +5dB）
- A3 用导频补，**必须回答"导频比 AGC 强在哪"**——否则是 AGC 的替代品非增量
- **关键增量论点（物理上成立，需数值验证）**：AGC 放大信号也放大噪声（Paillier line 177），deep fade 瞬态 SNR 不改善，PLL 仍可能跌破 critical SNR 失锁；**前馈导频 CPE 无环路稳定性约束，无 critical SNR 失锁风险**。这是 A3 真正的增量价值，非冗余
- **进 Groundwork 前必须收窄的定义**：A3 = "导频做前馈 CPE 替代 VV/AGC 的相位估计角色"（增量清晰，PASS）；**不是**"导频补幅度衰减本身"（与 AGC 冗余）。这个边界必须在 Groundwork 第一步显式锁定

**A3 唯一数据缺口**（非物理可行性缺口，是工程验证缺口）：星地湍流场景下导频抗 fade 增益未被任何已读论文直接测量。Yang 2026 是光纤 DSCM（无湍流），Valjus pilot+1dB 是符号导频非频域连续音。**建议 Phase B 补检索**：`frequency-domain pilot tone + free-space optical + turbulence` 查有无先例。若确认"频域导频音从未在湍流信道验证过"，迁移非平凡性反而增强（更适合硕士论文），物理可行性不受影响（前馈机制无死锁）。

### 预检结果 2：N1 = 存疑（锚点纠正 + gain 数据缺失）

**核心结论**：N1 物理上无死锁（不像 B1），TL-03 边界可厘清，主导损伤针对性强。但 **R006 把 cite=81 当 N1 关键论文是误判**（cite=81 踩 TL-03 + 场景偏离），N1 的合法化身必须重新锚定到 Elzanaty blind 模式；且**相干 FSO 下 PCS gain 数据完全缺失**（Elzanaty 全是 IM/DD），进 Groundwork 前必须补此数据。

**重大发现：cite=81 是 R006 误判（触发 D005 锚点纠正）**：
- cite=81 = Guiomar et al. 2020, JLT, DOI 10.1109/JLT.2020.3012737（Semantic Scholar 确认，closed access 无 OA）
- **Semantic Scholar abstract 直证 TL-03 陷阱**："a simple moving average channel estimator... 400G+ transmission over a seamless fiber-FSO **55-m link**... continuous measurement over 3 hours, including **raining periods**"
- 即：cite=81 是**按瞬时 SNR 帧级自适应**（moving average channel estimation 驱动 PCS 分布变化）= **跨 RTT = TL-03 砍**。且场景是 55m 短距 fiber-FSO + rain memory，**非 N1 假设的强湍流 GG 分布 deep fade**
- R006 对 cite=81 的"PCS-FSO 强湍流 deep fade gain"假设**缺乏正文支持**。cite=81 实属 R005 已砍的"2.1 链路自适应（TL-03 反馈延迟陷阱）"族，不是 N1

**N1 的合法化身 = Elzanaty 2020 (arXiv:2005.02129) blind 模式**（已下载精读）：
- Elzanaty 是真正针对 FSO turbulence 的 PCS 论文，Gamma-Gamma 湍流，Rytov σ²_R∈{0.1,...}
- **blind 模式**（CSI only at RX，发射端分布按湍流长期 CDF 的 outage 分位点离线设计）= **不随瞬时 SNR 变化，不跨 RTT = TL-03 安全**。这正是 N1 声称的"离线静态"
- gain（IM/DD, blind）：**1 dB (R=1.5, σ_R=0.5) vs uniform** / 2 dB (R=0.5) / 2.5 dB (CSI-aware, GG, R=0.56)
- **关键限制**：Elzanaty 全文是 **IM/DD M-PAM**（content.md line 43 "IM/DD is preferable over coherent"），**不是相干检测**

**gain 稀释分析**：Elzanaty blind 模式 1-2 dB gain 在 σ_R=0.5（中等湍流）实测成立 → **证明 gain 未被 SNR 方差稀释到 <0.5dB**（blind 正是对"瞬时 SNR 远低于平均"的回答：按 outage 分位点离线设计）。但强湍流 σ_R>1 时 blind gain 衰减程度 Elzanaty 未单列具体 dB（曲线未读数）。

**PCS×CPE×湍流 参数冲突检查**：**无 B1 式物理死锁**。PCS 是发射端固定符号概率分布（不涉环路带宽），CPE 是接收端相位估计，两者工作在不同域无共享参数需矛盾取值。唯一耦合点（高阶 PCS 对 CPE 残余相位噪声更敏感）是**工程耦合（联合设计）非物理死锁**。

**TL-03 边界判定**：
- N1 若按 cite=81（time-adaptive）做 → **FAIL（TL-03 砍）**
- N1 若按 Elzanaty blind（offline static）做 → **PASS（TL-03 安全）**
- **判决：N1 必须重新锚定到 Elzanaty blind 范式，抛弃 cite=81 作关键论文**（→ D005）

**主导损伤针对性**：强（确认）。N1 针对幅度闪烁（SNR 分布 shaping）+ 激光相位噪声（高阶 PCS 需 CPE 联合），两者都是 Paillier §IV-C 主导损伤。针对性比 B1 强。

**为何 N1 不能无条件 PASS（gain 数据缺口）**：
- Elzanaty 全部 gain 是 IM/DD，N1 假设相干 QAM。**Maxwell-Boltzmann PCS 在相干 AWGN 下光纤经典 gain 0.5-1.5 dB**（TL-22 红线参考范围），但**湍流 GG 分布 + 相干检测的联合 gain 无任何论文直接验证**
- 若 gain 是 IM/DD 外推（1-2 dB）→ 撑不起方法章（TL-05 算法贡献需 ≥1dB 且非薄增益）
- 进 Groundwork 前必须补"相干 FSO PCS gain"数据（否则 TL-22 红线）。补不到则 N1 应标"数据不足"降级，不强行 PASS

### 量级对比表（两候选合并，关键数字）

| 量 | 数值 | 来源 | 置信度 |
|---|---|---|---|
| Paillier 主导损伤 | 残余幅度闪烁（非活塞相位） | arXiv:1911.11851 §IV-C line 196 | **高**（正文） |
| 活塞相位影响 | negligible（曲线重合） | 同上 line 196 | **高** |
| Fade 引起 critical SNR 抬升 | +5 dB | 同上 line 200 | **高** |
| Fade 引起 BER penalty | 2.3 dB @ BER=1e-4 | 同上 line 204 | **高** |
| AGC 机制 | 补幅度归一化，**信号+噪声等比放大**（SNR 不改善） | 同上 line 177 | **高** |
| DPLL 收敛时间 | 1.4ms（fade 下仍成立） | 同上 line 186 | **高** |
| 导频 PSR（Yang） | −15dB（占功率 3.16%） | Yang 2026 笔记 | **高** |
| Pilot vs VV+差分增益 | +1 dB（深衰落场景 4） | Valjus 笔记 line 48 | **高** |
| 单孔径 scintillation σ²_I | 0.684 | Paillier Table 1 | **高** |
| N1 gain（IM/DD, blind, σ_R=0.5, R=1.5）| **1 dB vs uniform** | Elzanaty 2020 §7 Fig.9 | **高**（正文） |
| N1 gain（IM/DD, blind, R=0.5）| 2 dB vs uniform | Elzanaty 2020 §7 | **高** |
| N1 gain（CSI-aware, GG, R=0.56）| 2.5 dB | Elzanaty Fig.8 | **高** |
| **相干 FSO 下 PCS gain** | **无任何论文数据** | — | **缺失（决定性）** |
| A3 星地场景导频抗 fade 增益 | 未直接测量 | 无 | **数据不足** |

## 决策引用

- **D005（新建，本轮）**：N1 锚点纠正——cite=81 是 R006 误判（踩 TL-03 + 场景偏离），N1 合法化身重新锚定到 Elzanaty blind 范式；进 Groundwork 前必须补"相干 FSO PCS gain"数据。**不否决 N1 方向**（物理可行），只纠正锚点 + 补数据门控
- D003：参照（B1 物理可行性预检 FAIL 范本，本轮照做）
- D001：执行（后续阶段链 Groundwork §B）
- D004：参照（A3+2.2+N1 互锁三章主轴；本轮验 A3/N1 能否做出来）
- R006：**部分被纠正**（cite=81 作 N1 关键论文误判，D005 记录）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。物理可行性预检是 D001 后续阶段链的 §B 空白零假设前置筛选，属"系统性扫描找方向"原始目标。未进 Groundwork/MVE/Contract/Execute，未改仿真代码/开题报告
- **范围变更**：无新增。预检本身在 S004 已记的"先做物理可行性预检"范围内

## 后续

### 决策矩阵应用（PROMPT-004 L99-107）

矩阵规定"任一存疑 → 补检索后再判，不强行定"。本轮两候选均"存疑"但**性质不对称**：

| 候选 | 存疑性质 | 缺口类型 | 闭合难度 |
|---|---|---|---|
| **A3** | 倾向 PASS | 工程验证缺口（星地导频增益缺直接测量） | **低**——前馈机制无死锁已证，缺的是仿真验证（Groundwork 可做） |
| **N1** | 条件性 PASS | ① 锚点纠正（cite=81 误判）② gain 数据缺失（相干 FSO PCS） | **中**——需补检索确认相干 FSO PCS gain 是否存在，否则 gain 是 IM/DD 外推（TL-22 红线） |

### 当前可下结论（不等补检索即成立）

1. **两个候选都没有 B1 式物理死锁**——不会像 B1 那样整体倒在物理前提自相矛盾上。这点已确认
2. **保底骨架（2.2）依然成立**：S004 的"保底骨架=2.2+不依赖未验证物理的方法"判断不变。2.2 是纯解析，不受本轮预检影响
3. **A3 物理基础比 N1 干净**：A3 的缺口是"增量价值需数值验证"（Groundwork 内可做），N1 的缺口是"基础 gain 数据缺失"（需先确认相干 FSO PCS gain 存在才能谈 Groundwork）

### 下一步（建议，等用户拍板）

- **路径 A（推荐，先闭合 A3）**：A3 进 Groundwork §B。第一步收窄定义（前馈 pilot CPE vs AGC 增量）+ 补 Phase B 检索（频域导频音 + 湍流有无先例）。A3 物理可行已基本确认，缺口可在 Groundwork 内闭合
- **路径 B（N1 补数据门控）**：派子 agent 补检索"相干 FSO PCS gain"（`probabilistic constellation shaping coherent free-space optical QAM turbulence`）+ 精读 cite=35（PCS + Wiener phase noise）。补到相干 gain 数据 → N1 可进 Groundwork（锚 Elzanaty blind）；补不到 → N1 标"数据不足"降级
- **路径 C（先补 N1 数据再并行推 A3）**：两路径可并行——A3 进 Groundwork（已基本可行），N1 同时补数据门控
- **未到 MVE**：D001 后续阶段链不变

### 关键认知沉淀（防止下个对话重走老路）

- **物理可行性预检 ≠ 只查"有没有死锁"**：A3/N1 都无死锁，但 A3 的"增量 vs 冗余"问题和 N1 的"基础数据缺失"问题都是预检暴露的真实障碍，不能因为"无死锁"就判 PASS
- **R006 的摘要级判断有误判风险**（cite=81 = TL-03 陷阱）：再次印证 thesis-lessons 的教训——abstract 级判断（R006 全部是 abstract 级）需正文精读才能定。本轮 cite=81 的纠正证明"待精读 cite=81 验证 gain"（R006 未决项）的正确做法不是去精读拿 gain，而是先验它是否是 N1（结果它根本不是）
- **保底骨架思想再次验证有效**：S004 的"保底骨架=2.2"判断在本轮预检后依然成立——即便 A3/N1 都需补数据，2.2 仍站得住

### 不要做

- ❌ 在 N1 补到相干 FSO PCS gain 数据前进 N1 的 Groundwork（TL-22 红线，gain 是 IM/DD 外推）
- ❌ 把 cite=81 当 N1 关键论文（D005 已纠正，踩 TL-03 + 场景偏离）
- ❌ 跳过"机制定位收窄"直接进 A3 Groundwork（A3 必须先锁"前馈 pilot CPE vs AGC 增量"边界）
- ❌ 找第 4/5 方向（用户已拦，不解决"做不出来"）
- ❌ 锁"互锁三章"叙事（A3/N1 未完全 PASS，依赖未验证前提）
