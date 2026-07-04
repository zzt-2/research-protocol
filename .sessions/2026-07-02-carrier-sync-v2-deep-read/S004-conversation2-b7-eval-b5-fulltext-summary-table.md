# [S004] 对话 2：B7 评点 + B5 全文增量核验 + B1-B7 总表汇总

> 2026-07-04 | 精读沉淀补强·对话 2（评点收尾 B7 + 总表汇总）| 状态：B7 评点完成 + B5 全文核验完成 + B1-B7 总表落盘交用户排优先级
> 来源：H002（对话 2 任务）+ S003（B1-B6 已评 17 Q#）+ 用户 7-4 手动下 B5 全文

## 目标

执行 H002 三件事：①B7 Gardner TED 评点（派 1 子 agent）②B5 全文增量核验（主线直接做，升级 B5-Q1）③**B1-B7 总表汇总交用户排优先级**（中性，不判 Go/Kill）。守 3 步上限 + D018 中性提取 + FR-26 grep 核查 + 子 agent ≤15 分钟。

## 记录

### 报到验证（Trigger 1+5）

- **Trigger 1（Session Start）**：topic-index 不变量 9 条确认；active topic conflicts = none；depends_on（2026-06-20-problem-driven-redirection）输出已满足；profile 最近纠偏 2026-07-02 S030"急于推进"第 7 次；inflation check 本专题 3 S 文件（S001/S002/S003）远未到阈值。
- **Trigger 5（Handoff H002 接收）**：FR-26 主线独立 grep 核查 3 条关键事实全 PASS——
  - ① jlt.2023.3281082 落盘 PASS：`papers/doi/10.1109_jlt.2023.3281082/` 有 source.pdf(2,094,294 字节) + content.md（实际命名 `10138358.md`）
  - ② B4/B5/B6 三份增量笔记存在 PASS：三份笔记文件真实存在（13.6K/15.8K/14.1K 字节）
  - ③ B1-B6 总计 17 个 Q# PASS：B1×2 + B2×2 + B3×3 + B4×3 + B5×4 + B6×3 = 17 个 Q# 全在笔记中定义
- **额外核查（本轮素材）**：B5 全文落盘 PASS（source.pdf 2.9MB + content.md 252 行）+ B7 素材齐 PASS（旧笔记 + backward refs JSON + 锚全文 + Gardner TED 1986 原文）

### 步骤 1：B7 Gardner TED 评点（派 1 子 agent）

派 1 子 agent（general-purpose，≤15 分钟）读 B7 锚全文 + Gardner TED 1986 + B7 backward refs + 旧笔记（过时）+ B6 范例，写 `papers/_read_notes/_B7-gardner-ted-increment.md`。

**FR-26 主线独立核查 B7 产出**（读 B7 锚 content.md 行 21/49/65/69 + 笔记落盘）：

| 子 agent 报的关键 dB | content.md 原文核验 | 结论 |
|---|---|---|
| **0.6dB @ BER 2e-2**（receiver sensitivity，含 LPF2）| 行 65 "LPF2 improves receiver sensitivity by approximately 0.6 dB at a BER of 2×10⁻²" + 行 21 Abstract + 行 69 Conclusion | **PASS**（三处一致） |
| **1.9× 估计范围**（0–23GHz vs PSA FOE 0–12GHz）| 行 21 "1.9 times that of conventional algorithms" + 行 49 "nearly 1.9 times that of the PSA FOE, which fails beyond 12 GHz" + 行 69 | **PASS**（三处一致） |
| **OSNR 10dB 可解调**（常规失败点）| 行 21 "under a low optical signal-to-noise ratio of 10 dB" + 行 69 "OSNR of 10 dB, which is where conventional algorithms fail" | **PASS** |

**B7 评点收获（3 个 Q# 候选）**：
- **B7-Q1** Gardner TED 复用 FOE（核心）：TED 增益随符号净相位旋转量周期变化作 Doppler 指纹，扫频+双候选+TED2 判决。**撞 D006 否**（DSP 前馈，未把湍流纳入环路 TF）；**D005 边际够格**（0.6dB 偏小，1.9× 范围/OSNR 10dB 是结构性优势）；**范围 in**（星地 COSC）。
- **B7-Q2** TED 增益↔Doppler 映射的湍流鲁棒性：B7 仅无湍流验证，Ps 衰落致 S-curve 峰波动→估偏？**撞 D006 边界**（前馈归一化不撞；环路 TF 联合建模则撞，只标不砍）；**D005 待定量锚**（借 B6 0.42~0.66dB 参考）；**范围 in**。
- **B7-Q3** 双候选判决强噪声可靠性：TED2 标准差消歧，B7 未给错误率/置信度理论界。**撞 D006 否**；**D005 不够格**（鲁棒性证明非性能改进）；**范围 in**。

**关键发现**：
1. 旧笔记"下载失败/poster ROI 低"预期被全文推翻——实际含完整原理+实验+三组量化数字（0.6dB/1.9×/10dB），机制描述清晰（TED 增益周期相关）
2. baseline 是 **PSA FOE（Vieira 2023，数字谱不对称法）**，非 OPLL/PADE/V–V——B7 在"DSP 数字 FOE"赛道，与 B6（OPLL 鉴相器）/B4（PADE/V–V 级联）正交
3. 未涉湍流（NL-FT-DFB 三角波仅模拟频偏），初步看不撞 D006；边界在 Q2（湍流致 TED 增益波动是否纳入环路 TF）

### 步骤 2：B5 全文增量核验（主线直接做）

**触发**：用户 2026-07-04 手动下 B5 锚全文（source.pdf 2.9MB + content.md 252 行）。原 S003 §1.8 B5-Q1 标"待全文核验"现可升级。

**FR-26 主线读 252 行 content.md 提取关键信息**（不派子 agent，任务量小）：

| B5 全文核验项 | content.md 行号 | 核验结果 |
|---|---|---|
| 场景确证 | 行 29/47/143 | **星地 LEO 下行 in**（LEO 600km，1550nm，Doppler ±4.5GHz @ 56MHz/s）|
| 方法确证 | 行 71-87 | 分块 FFT + **正负功率谱面积比**（式 2-4，Rp-n）+ 星历预测调 LO；非"找谱峰"而是功率比积分量；盲估无 pilot 不依赖 MIMO DSP |
| 捕获范围 | 行 23/47/143/167 | **±4.5 GHz**（四处一致，覆盖 LEO Doppler 全量程）|
| 粗补偿残频 | 行 23/149 | **<140 MHz** 标准差，最大 250MHz（含激光 250MHz 抖动）|
| 精确补偿残频 | 行 149 | **<5 MHz** |
| 精估范围 | 行 57/149 | ±312.5 MHz（= B/8）|
| 灵敏度 | 行 149 | BER 1e-3 @ **−48 dBm** |
| 收敛 | 行 129-141 | 1GHz 频偏 8 点 FFT 第 4 次迭代 / 16 点 FFT 第 3 次收敛 |
| baseline | 行 33-45 | 4 类 FOE 算法（M-power/训练序列/改进传统/谱分析），B5 属第 4 类，首次搬到星地 LEO |
| 湍流建模 | 全文 | **无**（仅背景提"atmospheric turbulence...affect"，实验为 B2B 无湍流信道）|
| dB 增益对比 | 全文 | **无**（只给绝对指标，未 vs baseline 给"改善 X dB"）|

**B5-Q1 升级判定**（从"待全文核验"到明确三维）：
- **撞 D006**：**确证否**——前馈频域功率比 + 星历预测调 LO，非环路 TF 联合建模湍流相位；全文无湍流建模
- **D005 够格**：**dB 维度不够格 / 结构性优势维度有价值**——本体无 vs baseline dB 对比（硬伤），但 ±4.5GHz 覆盖 LEO Doppler + 残频落精估范围 + 收敛 3-4 次 + 盲估无 pilot 是工程可用性证据
- **范围**：**确证 in**（星地 LEO 下行）

**B5 关键机制辨析（追加发现）**：
- B5 核心 = **"正负功率谱面积比"而非单纯谱峰**（行 77-85 式 2-4）——积分量比谱峰更鲁棒（低 SNR 下谱峰不明显）
- B5 与 B7 机制互补：B5 用功率谱面积比（频域积分），B7 用 TED 增益周期相关（定时域指纹）；B5 粗估范围大 ±4.5GHz，B7 精估但需扫频
- B5 无湍流建模 = 潜在 Q# 延伸点（D006 边界，与 B6-Q2/B7-Q2 模式一致）：前馈归一化不撞，环路 TF 联合建模则撞

B5 增量笔记追加"全文增量核验段"落 `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md`，含 B5-Q1 升级表 + 更新后的 Q# 候选清单 + 4 条追加关键发现。

### 步骤 3：B1-B7 总表汇总（交用户排优先级）

**🔴 本表守 D018 中性提取——只标 D006/D005/范围三维，不判 Go/Kill。Go/Kill 是用户的，排完优先级后对前几名做。**

汇总 B1-B7 七点共 **20 个 Q# 候选**（B1×2 + B2×2 + B3×3 + B4×3 + B5×4 + B6×3 + B7×3）：

#### B1-B7 总表（20 个 Q# 候选）

| B 点 | Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 | 关键 dB/量级 |
|------|-----|-----------|--------|----------|------|------------|
| **B1 pilot 窗口** | B1-Q1 | 自适应 phase-estimation window N（sat.1553 固定窗 + [60] 最优 N∝SNR 理论；LEO 强湍 σp²=0.25 SNR 波动；sat.1553 固定 N 单 SNR 点 + L440 自承"动态调整 gain 未量化"）| 不撞 | 倾向够格但有风险（sat.1553 pilot 场景4 比 VV+diff +1dB，自适应 N 增量待 MVE）| in | +1dB（sat.1553 pilot vs VV+diff）|
| | B1-Q2 | 自适应 pilot rate（sat.1553 固定 pilot rate + [58] 静态 pilot-rate×linewidth 优化；LEO 过顶 SNR 慢包络；[58] 静态未建模 SNR 动态）| 不撞 | 风险偏高倾向不够格（sat.1553 L440 自承"same pilot rate performs similarly"负面证据）| in | 0.5dB 阈值 |
| **B2 deep fade 冻结** | B2-Q1 | FOE freeze 自适应阈值/多估计器协同（[79] 静态功率阈值 gate FOE；上行强湍 deep fade；sat.1553 L582 自承"完全冻结在 SOP 漂移大时丢跟踪"）| 不撞（估计器 gating ≠ 相位建模）| ≥1dB 存疑待全文核验（**陷阱已规避**：0.6dB 是 [79] 相对无 freeze，非 B2-Q1 增量）| in | 0.6dB（[79] vs 无 freeze，非增量）|
| | B2-Q2 | FOE freeze + pilot-aided fallback 双模切换（[79] blind freeze；fade 恢复期需快速重捕获；blind 恢复收敛慢，sat.1553 L440 pilot 在 fade +1dB）| 不撞 | 倾向够格但增量未量化 | in | +1dB（sat.1553 pilot 在 fade）|
| **B3 子系统协同** | B3-Q1 | LCOMM B3 视角重抽（一套 FPT 跨 FOE+CPE+RSOP，CPE/解复用解耦，+0.9 dB Q / RMSE 4.47°）| 不撞 | 够格（+0.9dB / 持平 MIMO）| **out（光纤 DSCM，待迁移论证）** | +0.9dB Q |
| | B3-Q2 | jphot+oe 合并（一套 TS 同时 FS+两段 FOE+MRC，复杂度 17%~25%，强湍 4 支路）| 不撞 | 够格（+2~3 dB / 复杂度降 75%）| in（FSO，分集增益不可全迁）| +2~3 dB |
| | B3-Q3 | sat.1553 L790 + 张思齐空白（定时+均衡+载波恢复跨子系统共享 pilot + 依赖解耦联合协同，open problem 级）| 不撞（边界：若具体化为环路 TF 联合建模则撞，只标不砍）| 待定量锚（借 +0.9~3 dB 量级参考）| in | 借 +0.9~3 dB |
| **B4 双反馈环** | B4-Q1 | optcom.2023 双反馈环本体（外环 PADE 大动态 + 内环 V–V RFO 精补 + 前馈 V–V 相位）| 不撞（边界：若内环跟湍流相位则撞，只标不砍）| 部分（无外部 dB 增量，待锚点）| in（星地 LEO）| ±920 MHz @ 0.5 dB / 285 GHz/s / MSE 4× |
| | B4-Q2 | jlt.2023 PCS+符号率自适应（粗细接口量级参考，−15~+15 GHz 扫描）| 不撞 | 够格（维度错位：吞吐 vs 同步 dB）| in | +70~100 Gbps |
| | B4-Q3 | sat.1553 feedback latency/并行化 + L790 open problem（粗细双环分工工程动机背书）| 不撞 | 待定量锚 | in（含 ISL 边界）| 无直接实例 |
| **B5 短时谱粗频偏** | **B5-Q1** | B5 本体短时谱粗 CFO（**全文核验后升级**：分块 FFT + 正负功率谱面积比 + 星历预测，2.5-GBaud PM-QPSK 星地 LEO）| **否（全文确证）** | **不够格（dB 维度）/ 结构性优势（范围维度）**——无 vs baseline dB 对比；±4.5GHz 覆盖 LEO Doppler + 残频落精估范围 | **in（星地 LEO 下行，全文确证）** | ±4.5GHz / 残频 <140MHz / 灵敏度 −48dBm@BER 1e-3 |
| | B5-Q2 | [60] Leven Mth-power 理论锚（4 次方 + 500 样本和 + 相位除 4 前馈 FE）| 不撞 | 够格（赢 FLL/无 FE 几 dB）| **out（光纤 intradyne，待迁移论证）** | OSNR <9dB 与频偏无关 / 无 FE 7dB penalty |
| | B5-Q3 | sat.1553 L558 粗 CFO 精度边界（Δfm=fs/8N + 慢速平均）| 不撞 | 待定量锚 | in（OSL，含 ISL 边界）| 残频上限 10⁻³fs |
| | B5-Q4 | jlt.2023 频谱扫描 Doppler 视角参考（非 CFO 估计）| 不撞 | 够格（维度错位：吞吐 vs 同步 dB）| in（视角参考非本体）| +70~100 Gbps |
| **B6 Z-ODPLL** | B6-Q1 | atan2 鉴相器 KD 与 Ps 解耦（全湍流态保锁，容 30ns 延迟）| 不撞 | 边际够格（定性保锁非几 dB）| in | σ=2.6°/0.42dB / 容 30ns 延迟（sin 仅 6ns）|
| | B6-Q2 | Z-ODPLL H(z) 建模（固定 Kd 掩盖 Ps 波动）| **边界（只标不砍）** | 不够格（工具）| N/A | — |
| | B6-Q3 | sin 鉴相器幅度衰落鲁棒性跨论文空白（OIPLL 靠 AGC/LUT 部分缓解，均未评湍流深衰落）| 不撞 | 待定量锚 | in | 无 |
| **B7 Gardner TED** | **B7-Q1** | Gardner TED 复用 FOE（**本轮新评**：TED 增益随符号相位旋转周期变化作 Doppler 指纹，扫频+双候选+TED2 判决）| **否**（DSP 前馈，未把湍流纳入环路 TF）| **边际够格**（0.6dB 偏小，1.9× 范围/OSNR 10dB 是结构性优势）| **in（星地 COSC）** | 0.6dB @ BER 2e-2 / 1.9× 范围（0–23GHz）/ OSNR 10dB 可解调 |
| | B7-Q2 | TED 增益↔Doppler 映射的湍流鲁棒性（B7 仅无湍流验证，Ps 衰落致 S-curve 峰波动→估偏？）| **边界（只标不砍）**——前馈归一化不撞；环路 TF 联合建模则撞 | 待定量锚（借 B6 0.42~0.66dB 参考）| in（星地 COSC 湍流）| 借 0.42~0.66dB |
| | B7-Q3 | 双候选判决强噪声可靠性（TED2 标准差消歧，B7 未给错误率/置信度理论界）| 否 | 不够格（鲁棒性证明非性能改进）| in（星地 COSC 低 SNR）| 无 |

#### 总表统计（中性，不判 Go/Kill）

| 维度 | 计数 | Q# 编号 |
|------|------|---------|
| **总 Q# 数** | **20** | B1×2 + B2×2 + B3×3 + B4×3 + B5×4 + B6×3 + B7×3 |
| **撞 D006 明确撞** | **0** | （sat.1553 L70 旧扩展方向撞已加注归档，不计入）|
| **撞 D006 边界（只标不砍）** | **3** | B3-Q3（若环路 TF 联合建模）/ B6-Q2（Z 域建模纳入湍流）/ B7-Q2（TED 增益纳入环路 TF）|
| **D005 倾向够格** | **8** | B1-Q1 / B2-Q2 / B3-Q1 / B3-Q2 / B4-Q2 / B5-Q2 / B5-Q4 / B6-Q1 |
| **D005 边际够格** | **2** | B7-Q1（0.6dB 偏小但范围/鲁棒性结构性优势）/ B5-Q1（无 dB 对比但范围覆盖结构性优势，全文核验后升级）|
| **D005 待定量锚** | **5** | B2-Q1（0.6dB 陷阱规避后存疑）/ B3-Q3 / B4-Q1（部分）/ B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 |
| **D005 风险偏高/不够格** | **4** | B1-Q2（自承负面证据）/ B5-Q1 dB 维度不够格（结构性优势另计）/ B6-Q2（工具）/ B7-Q3（鲁棒性证明非性能改进）|
| **范围 out** | **3** | B3-Q1（光纤 DSCM）/ B5-Q2（光纤 intradyne）/ B6-Q2（N/A 工具）|
| **范围 in** | **17** | 其余全部（含 ISL 边界标注 B4-Q3/B5-Q3）|

#### D005 够格梯度（中性排序，供用户排优先级参考，不判 Go/Kill）

> 本梯度只按"D005 够格"程度的客观证据强度排，**不判 Go/Kill**。Go/Kill 是用户的，排完优先级后对前几名做。

**第一梯队（有明确 dB 增益 + 范围 in）**：
- **B3-Q2**（+2~3 dB 强湍 4 支路，复杂度降 75%）—— dB 最高，范围 in
- **B3-Q1**（+0.9 dB Q）—— dB 次高，但 **范围 out（光纤 DSCM 待迁移论证）**
- **B1-Q1**（+1dB pilot vs VV+diff）—— 有理论锚 [60] 背书
- **B2-Q2**（+1dB pilot 在 fade）—— 作者亲口指出 [79] 冻结局限 = 改进空间
- **B5-Q2**（OSNR <9dB 与频偏无关 vs 无 FE 7dB penalty）—— **范围 out（光纤 intradyne 待迁移）**

**第二梯队（结构性优势，dB 偏小或维度错位）**：
- **B7-Q1**（0.6dB @ BER 2e-2 + 1.9× 范围 0–23GHz + OSNR 10dB 极限）—— 0.6dB 偏小但范围/鲁棒性是结构性优势，baseline PSA FOE 明确
- **B4-Q2**（+70~100 Gbps 吞吐 vs 同步 dB 维度错位）—— 够格但维度错位
- **B5-Q4**（+70~100 Gbps 同 B4-Q2）—— 视角参考非本体
- **B5-Q1**（全文核验后：±4.5GHz 覆盖 LEO Doppler + 残频落精估范围 + 盲估无 pilot）—— dB 维度不够格但范围覆盖结构性优势
- **B6-Q1**（σ=2.6°/0.42dB + 容 30ns 延迟 vs sin 仅 6ns）—— 定性保锁（失锁→保锁）非几 dB

**第三梯队（待定量锚 / open problem 级）**：
- B2-Q1（0.6dB 陷阱规避后存疑待全文核验 [79] 正文）/ B3-Q3（open problem 级借 +0.9~3dB）/ B4-Q1（±920MHz @ 0.5dB 但无外部增量）/ B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2（湍流鲁棒性借 B6 0.42~0.66dB）

**第四梯队（风险偏高/不够格）**：
- B1-Q2（sat.1553 自承"same pilot rate performs similarly"负面证据）/ B6-Q2（工具 N/A）/ B7-Q3（鲁棒性证明非性能改进）

#### 关键观察（中性，辅助排优先级）

1. **撞 D006 明确撞 0 个**——B1-B7 七点 20 个 Q# 没有一个明确撞 D006 红线（B3-Q3/B6-Q2/B7-Q2 是边界只标不砍）。D006 不是 B 档的主要杀手。
2. **范围 out 3 个**是硬筛选——B3-Q1（光纤 DSCM）/ B5-Q2（光纤 intradyne）/ B6-Q2（N/A 工具）天然排低优先级（除非迁移论证成立）。
3. **dB 增益集中区**：B3（+0.9~3dB）> B1/B2（+1dB）> B7（0.6dB + 范围优势）。B3 范围 out 风险最大（光纤 DSCM），B1/B2 in 范围但 dB 量级中等，B7 dB 偏小但范围/鲁棒性结构性优势 + baseline 明确（PSA FOE）。
4. **"D006 边界"模式重复出现**（B3-Q3/B6-Q2/B7-Q2）——三者都是"前馈/工具层不撞，若纳入环路 TF 联合建模则撞"。这是潜在的一致性研究方向（跨 B 点的湍流相位建模边界），但 Go/Kill 留用户判。
5. **B5/B7 全文核验后升级**（本轮）——B5-Q1 从"待全文"升级为"dB 不够格但范围结构性优势 in"；B7-Q1 新评为"边际够格（0.6dB + 1.9× 范围）"。两者都是"DSP 数字 FOE"赛道，机制互补（B5 功率比频域积分 / B7 TED 增益定时域指纹）。
6. **dB 量级 vs 同门学位论文**：同门 2-4dB 区间，本表第一梯队 B3-Q2 +2~3dB 达标，B1-Q1/B2-Q2/B3-Q1 +0.9~1dB 偏下沿，B7-Q1 0.6dB 偏低。**0.5dB 阈值**（D008 FR-21 参考）下，B1-Q2/B6-Q1/B7-Q1 的 0.6dB 级刚过线。

## 决策引用

- **无新建 D###**（本对话是评点 + 全文核验 + 总表汇总，Q# 候选留总表阶段用户排完优先级后判 Go/Kill，符合 D018 中性提取）
- 引用既有：D017（D015 v2 步骤 4 每点 ≤5 篇验证）/ D018（中性提取不判 Go/Kill）/ D006（红线保留，3 个边界只标不砍）/ D005（务实路线，Q# 标够格判定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（B7 评点 + B5 全文核验 + B1-B7 总表汇总都是 S001 v2"对话 2"动作；Q# 候选只提取不判 Go/Kill）
- **守 3 步上限**：本轮 3 步（①报到 ②B7 评点 + B5 全文核验 ③总表汇总 + 写 S004/H003）
- 守子 agent ≤15 分钟：1 子 agent（B7 评点），PASS（duration 123.6s ≈ 2 分钟）
- **守 D018 中性提取**：本轮 B7 新增 3 Q# + B5 升级 1 Q# + 总表 20 Q# 全标 D006/D005/范围三维，不判 Go/Kill（profile 第 7 次"急于推进"防线——总表只排梯度不判 Go/Kill）

## 后续

### 交对话 3（B8/B9/B10 评点 + literature_notes 并入准备）

**对话 3 必读**：
1. 本 S004（B7 评点 + B5 全文核验 + **B1-B7 总表 20 Q#**）
2. S003（B1-B6 评点 17 Q#）+ S002（cited-by 池 + 下载状态）
3. topic-index 不变量 9 条 + S001 v2 规划
4. H003（本轮 handoff，下一步具体任务）
5. gw-read.md（14 字段+7 项结构化提取标准）
6. 原专题 H020（总表 + 排优先级辅助信息）

**对话 3 任务**（B8/B9/B10 评点 + B11/B12 预登记）：
- **B8 RL+GS 自相干自消除**：锚 jocn.468220（603 行）+ cited-by 3 篇（photonics10050493 直击切入点 / lcomm GS 主题 IM/DD / jocn.503484 DRL FSO）
- **B9 虚拟载波自相干+DRE**：锚 jlt.2023.3270673（306 行）+ **用户新下 apn.3.3.036007 B9 DRE 全文 440 行**（Gold OA 反爬失败已解决）+ cited-by 4 篇
- **B10 16-QAM pilot-RLS**：锚 s11107-024-01019-2（318 行）+ cited-by 1 篇（**ao.581648 PS-64QAM KRLS 仍缺全文**，Optica AO 订阅墙，靠摘要 + 原 B10 锚 s11107）
- **B11/B12 预登记**（用户新下 oecc-psc62146 B12 MAP 全文 150 行到位）：B11 锚 LPT.2024.3523478（226 行）+ B12 锚 TCOMM.2022.3171809（590 行）+ B12 MAP 全文

### 关键提醒给对话 3

1. **B1-B7 总表已落盘**（本 S004 §步骤 3）：对话 3 评完 B8-B10 后续总表 B8-B12，对话 4 最终合并全 12 点总表
2. **B5/B9/B12 全文用户 7-4 已下到位**：B5（252 行本轮已用）/ B9 DRE apn.3.3.036007（440 行对话 3 用）/ B12 MAP oecc-psc62146（150 行对话 4 用）
3. **ao.581648 仍缺**（B10 高相关 PS-64QAM KRLS Optica AO 订阅墙）：B10 评点靠摘要 + 原 B10 锚 s11107，或用户继续尝试手动下
4. **B7 旧笔记过时**（本轮已更新）：旧笔记 `10.1364_ofc.2026.w2a.62.md` 写于下载失败时，实际 S002 已下全文。对话 3+ 看 B7 用 `_B7-gardner-ted-increment.md`
5. **D006 边界模式**（B3-Q3/B6-Q2/B7-Q2）：三者都是"前馈/工具层不撞，环路 TF 联合建模则撞"——对话 4 literature_notes 并入时这是潜在一致性研究方向
6. **dB 量级参考**（同门 2-4dB）：对话 3/4 评 B8-B12 时用本表第一梯队（B3 +2~3dB）作量级锚
