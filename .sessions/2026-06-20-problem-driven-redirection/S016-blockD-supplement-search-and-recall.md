# [S016] 块 D Step 3.5 定向补检索 + 旧 B1 资产召回

> 2026-06-27 | GW Step 3.5 | 状态：检索+召回完成，下载精读债务

## 目标

执行块 D（Step 3.5）定向补检索，填补块 C 综合分析识别的盲区 A（星地 LEO + 湍流 + Doppler 三者联合）和盲区 B（竞品共同引用的基础文献）。接收 H006 交接。

## 记录

### 执行序列

1. **接收方验证（Trigger 5）**：H006 三条事实声称全核查 PASS（Q# 数=10、Step 3 ✅ 2026-06-26、S015 落盘）。盲区 B 引证核实（新2 笔记 8 处引用 Diniz[50]）。

2. **检索方案设计（过用户审）**：
   - 盲区 A：A1-A4 四条场景词（方法中性，无模块词）
   - 盲区 B：B1-B3 三条基础文献按名定向
   - 用户决策：①只用 tools/search 不碰 IEEE（S008 债务原则）②盲区 C 不做（聚焦 A/B）③A1-A4 全跑不改

3. **派 2 个子 agent 并行执行检索**：盲区 A + 盲区 B 各一批。全部用 `bash tools/search`，0 条 WebSearch/webReader。

4. **主线独立核查（S011/S012 教训）**：核心 DOI（Pech 2025 / Paillier 2020 JLT / Rustum 2026 / Viterbi 1983）全部在 JSON 中真实存在，abstract 与子 agent 转述一致。Yokomura 2025 标题/abstract 错配判断正确。**发现并修正了我自己核查脚本的 bug**（第一次 grep 命中 thesis 而非 JLT，break 太早）。

### 🔴 重大发现：H004 选样漏召旧 B1 资产（S013/S014 同型问题复发）

核查下载需求时发现 **Pech 2025 + Valjus 2025 + Paillier 2019 conf 三篇早在 2026-06-16 已下载并完整精读**（papers/doi/ 有 content.md + papers/_read_notes/ 有 73-84 行笔记），标注方向 B1（OPLL 联合建模）。

- **根因**：B1 方向后被 Kill（thesis-direction-pivot 时期），H004 块 A/B 选样时因"路径依赖"把旧 B1 标签论文排除，没召回本轮 10 篇 Q# 清单。违反 D003"多候选发现"原则——候选池不该因历史方向标签过滤。
- **严重性**：literature_notes.md 第 130 行自己都写了"本批没有星地 LEO+湍流+Doppler 联合"，但块 C 综合分析时没召回已下载的 Pech/Valjus。盲区 A 的"缺口"判断**字面成立但实质部分不成立**——不是"GW 没覆盖"，是"已有资产被遗忘"。
- **性质修正**：盲区 A 不是蓝海，是**"分治架构成熟但联合建模空白"的稀疏前沿**。Paillier 系列（AO 管湍流 + DPLL 管多普勒分治）是代表 baseline，Valjus 2025 综述给"没有任何算法联合处理二者"的综述级强证据。

### 用户决策（voice.md 已登记）

- 召回 Pech/Valjus 入本轮 Q# 清单 + D005 务实标准重评
- 剩余 5 篇全下（Paillier2020JLT/Rustum2026/Mosnier2025/Tang2024/Viterbi1983）

### 召回整合（Q11/Q12/Q13 入 Q# 清单）

基于已有笔记 + D005 务实标准重新评估：

- **Q11（Pech 2025 Z 变换 ODPLL）**：部分过 D⚠️（baseline 自身量化弱，仅 XOR 误差清零无数值 BER）。M=固定参数 ODPLL 只建模多普勒 φ_D，C=星地 LEO+湍流+Doppler，A=环路 H(z) 不含湍流相位 φ_T（用正弦近似衰落）。旧 B1 时期判"勉强>常识重做"是作创新点评估，D005 下作 baseline 合格。
- **Q12（Paillier 2019 conf 分治架构）**：**全过 + E 三检验 3/3**。M=分治架构（AO 光域管湍流 + DPLL 数字域管多普勒，环路不含湍流相位），A=分治假设 AO 完全校正+AGC 恒幅。是盲区 A 联合建模 gap 的**最强 baseline 端证据**（分治范本）。
- **Q13（Valjus 2025 综述）**：支撑型，非独立 Go 候选。给 gap 综述级强证据 + 算法地图基线（timing/carrier/equalization/polarization 全 DSP 链 + 4 场景 SNR penalty 全量化）。

三者共同指向同一 gap：**星地 LEO + 湍流 + Doppler 联合 DSP 建模缺失**。

### 下载债务（未完成）

5 篇缺失论文下载遇 IEEE/SPIE 难点（urllib 不走代理 fail + blit 走 Playwright 慢/限流），子 agent 后台运行中未产出 content.md。作为债务记录，不阻塞 Step 3.5 主线（检索+召回已完成）。

### 偏航检查 A-E（全过）

- A 方法中性 ✅（A1-A4 场景词无模块词，B1-B3 按名定向）。⚠️ 召回 Q11-Q13 有滑回 B1 风险，已用 D005 重评+标注"旧 B1 方向"，块 E 需警惕"B1 换皮"
- B 全留无臆造 ✅（search-archive 全留，死地噪声标记）
- C 种子从综合分析诊断出 ✅（非开题线索）
- D 每步说 why ✅（检索→核查→发现遗漏→召回，每步可溯源）
- E 不把难度当否决 ✅（Q11 标 D⚠️ 是 baseline 量化弱客观原因）

## 决策引用

- 无新 D###（本轮是执行+召回，未产生架构决策）。依赖 D003（多候选）、D005（务实路线）、D004-a（对手标准）。
- voice.md 已登记本轮 6 条用户决策（检索源/盲区C/A检索词/下载范围/盲区B处理/已有资产召回）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。块 D Step 3.5 是 groundwork.md:33 强制必做步骤，未跑 MVE/未判 Go/未改框架。召回是 H004 漏召的纠正，非扩范围。

## 后续

1. **下载债务清完**：5 篇论文（Paillier2020JLT/Rustum2026/Tang2024/Mosnier2025/Viterbi1983）下到后精读，Rustum 2026（DL 独立路径）和 Tang 2024（核对是否[50]）是精读重点，可能产生 Q14/Q15
2. **块 E 启动**：Step 4a 可行性 Go/No-Go。对 Q1-Q13 每个 Q# 走 gw-feasibility A0/A'/A/B/D。**重点 Q12（分治→联合建模）**，但需警惕 B1 换皮（D005 标准：赢传统 baseline 几 dB 即可，但要诚实判创新增量）
3. **PS N1 同构核查**（块 E 必做）：Q8/Q9/Q10 的 PS 增益是否依赖时变信道
