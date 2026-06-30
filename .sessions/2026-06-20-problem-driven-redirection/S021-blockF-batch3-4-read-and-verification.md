# [S021] 块 F 判地专项执行第 2 对话——批 3 + 批 4 精读核查完成

> 2026-06-30 | 块 F 判地专项 | 状态：批 3/4 完成，三轴判读 + R002 三选一待续

## 目标

续接 H012，完成判地剩余批 3（调制/检测 8 篇）+ 批 4（AO+补充 7 篇）的精读核查，更新 R002 累计观察表。**本轮不下三选一结论**（守 H011 纪律 1 + 单对话 3 步上限），结论留下一对话冷静期再下。

## 记录

### 1. 报到 + H012 接收方验证（Trigger 5）

读 topic-index（不变量 8 条 + 当前位置）+ R002 工作文档（批 1/2 结果）+ profile.md（6 条画像）+ voice.md。H012 接收方验证清单 5 项核查全 PASS：

- 2.6 OPLL L619 sin 鉴相器失效：✅ PASS — `papers/doi/10.3390_photonics10121312/content.md` L619 原文真实（"the gain KD is related to the input signal level Ps... making the OPLL unstable" + "sin(θ)≈θ approximation"）
- 选样 36 篇池（28 已精读）：✅ PASS — `ls papers/_read_notes/*.md` = 28 篇真实
- 批 1+2 核查全 PASS：✅ PASS — R002 批 1/批 2 段标"全 PASS 无造假"，纠正点诚实记录
- 4.7 未精读文件：✅ PASS — `papers/doi/10.1088_1742-6596_2906_1_012002/content.md` 存在（125 行）
- depends_on stable：✅ PASS — `2026-06-19-4b1` closed + `framework-evolution` active

**Inflation check**：S### = 17 触发 ≥15 BLOCK 阈值。判地是 D013 既定决策延续非范围扩张，H011/H012 已标注，如实标注不阻断。

### 2. 派 3 subagent 并行执行

批 3/批 4 大部分是"读已有笔记提取判地三轴"（28 篇已精读复用），仅 4.7 是真全文精读。3 个 subagent 并发上限内：

- **批 3 subagent**：读 8 篇调制/检测笔记提取三轴
- **批 4 subagent**：读 6 篇 AO+补充笔记提取三轴（含 AO 维度单独标）
- **4.7 subagent**：全文精读 sat-ground 16QAM coherent

全部回传。4.7 subagent 发现 **paywall 截断**（content.md 仅摘要 L81-83，正文/图/数值全缺），诚实标注"全文未提及任何 dB"。

### 3. 主线 §7.2 grep 核查（5 个关键声称）

| 声称 | 核查结果 | 关键发现 |
|---|---|---|
| 3.3 OAM SNR↑10dB | ✅ PASS（L587/L606）| hybrid 全套（Bessel+Airy+OAM+AO+PSO+DCNN+DNFIS）非单一 DSP，baseline=MDM-FSO+DFE，仅仿真 |
| 3.5 SSB ~7dB | ✅ PASS（L221/L235）| **判读纠正**：baseline 不对称是三重的——DSB-ASK 地面 950m/850m vs SSB-QPSK 卫星 350-900km + coherent homodyne vs direct photodetection + 不同调制。7dB 本质是"相干 vs 直接检测"灵敏度差，非同场景 DSP 改进 |
| 4.3 AO+MDR 17-20dB | ✅ PASS（L145/L187）| 真实 + 协同机制清晰（强湍流 AO 把能量从高阶模重分配到前 6 模 + MDR 收 AO 残余）|
| 4.4 阵列 BER 10⁻²→10⁻⁵ | ✅ PASS（L381/L404）| 论文 L413 自承"PD quantum efficiency=1 + 理想角度匹配"假设偏强 |
| 4.2 分治够用 | ✅ PASS（L95/L189）| **漏报补录**：L189 "fading is to increase the minimal critical SNR...by approximately 5dB"——这是 baseline（纯 DPLL 无 AGC）失效 5dB 量化证据，subagent 归入"失效 dB"未点明是 baseline 失效 |

**核查结论：全 PASS，无造假。** 1 个判读纠正 + 1 个漏报补录，体现核查机制中性双向（S012 同构）。

### 4. 4 批判地累计核心发现（事实，非结论）

写入 `R002-blockF-judgment-sample-table.md` 批 3/4 段 + 4 批总观察表。核心：

**范围内 + 轴3 成立（够几 dB）的 4 个子地带**：
- 4.3 AO+MDR（GEO）：17-20dB 总增益，**剥离 AO 后 MDR 仍 9.1dB**——判地最强信号
- 3.3 OAM（星地上行）：+10dB SNR，但 hybrid 全套非单一 DSP，仅仿真
- 4.4 阵列检测器（星地）：BER 10⁻²→10⁻⁵，理想相位补偿假设偏强
- 3.7 OQAM single-PD（卫星）：1.25-2dB，B2B+self-coherent 未验证星地

**范围内 + 轴1 强有缝但轴3 失败的 3 个子地带**：
- 4.2 AO+DPLL 分治：5dB/2.3dB 失效但论文证明分治够用（典型"有缝但改进无增益"）
- 3.8 dual-pol self-coherent：两 PD 强失效（BER>0.1）但改进无 dB，vs coherent 负 penalty
- 3.1 PCS+Rs：Doppler baseline 真失效但增益是 Gbps 非 dB

**"有缝但改进无增益/不够格"是范围内主流形态。**

**AO 维度**（用户拍板分开标）：剥离 AO 后 4.3 MDR 仍成缝（最强），4.1/4.2 DSP 侧本无强缝。AO 维度不影响判地主结论。

## 决策引用

- 无决策（批 3/4 是过程性判读，判地结论要等 R002 三选一才到决策级）
- 引用 D013（重心转折转判地）、D005（务实路线轴3标准）、不对称判据（H011/H012 纪律 2）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（判地是 D013 既定下一步，不立 Q#、不补检索、AO 全判后分开标，均守 H011/H012 纪律）

## 后续

**下一对话执行 H013**：
1. 三轴判读（子地带 × 三轴汇总表，~36 篇全文层证据）
2. 不对称判据 A 三重防漏看核对（① 覆盖度：信道估计偏薄+综述偏薄须诚实标 ② 死轴已验批 2 ③ 综述受已落盘约束仅 1 篇真综述）
3. R002 三选一硬结论（A 真没缝 / B 有缝但选样错过 / C 窄缝可救）+ 置信度
4. 跟老师谈的证据包（如 A 或 B）：量化范围硬门砍了多少有缝候选 + 被砍子地带清单
5. 报用户拍板：三选一 + B/C 下一步建议

**预计**：三轴判读 + R002 结论约 1 对话（topic-index 悬置项 27 标注判地共 2-3 对话，本对话是第 2 对话，下一对话收尾）。
