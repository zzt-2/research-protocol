# [S017] Q8 切入点深化 + 切入点 2 MVE FAIL Kill

> 2026-06-27 | 块 E Step 4a（Q8 深化）+ Step 4b（切入点 2 MVE）| 状态：本轮完成

## 目标

深化 Q8（PCS+Rs 治 Doppler，Fernandes 2023 增量）的切入点定义：查 4 候选切入点有无已做论文 → 选定切入点 → 进 Step 4b MVE 验证。

## 记录

### 1. H008 handoff 接收 + 框架文件重读

- H008 4 条事实核查**全 PASS**：D006 Q12 Kill（decisions.md:313）/ Q8 通过（feasibility_report.md:210）/ master-state Step 4a 🔄（master-state.md:47）/ advisor-brief line 9 确认"自适应载波同步"非泛指（advisor-brief.md:7）
- 注册表检查：depends_on（4b1-groundwork closed + framework-evolution active）满足，conflicts_with=[]
- 范围检查：本轮在块 E Step 4a/4b 内，未违反"明确不含"
- 框架文件重读：gw-feasibility.md 维度 D MVE 8 步 + FR-20 参数溯源 + FR-21 oracle 上界前置

### 2. Q8 切入点深化检索（4 候选 × 10 查询）

**用户拍板"全部 4 个都查"**（2026-06-27）。主线 tools/search 跑 10 组检索词存 search-archive/2026-06-27/（+10 JSON，零 WebSearch/webReader）：
- 切入点 1（指向×Doppler）：3 组
- 切入点 2（真实 SD-FEC）：3 组
- 切入点 3（DWDM）：2 组
- 切入点 4（湍流-Doppler 耦合）：2 组

2 子 agent 并行 digest（切入点 1+2 / 3+4），主线独立核查关键 DOI：
- OTFS (10.1109/LPT.2025.3545920) 确认 IM-DD 非 PCS，不撞 Q8 ✅
- NTN-UAV (10.1109/WiSEE57913.2025.11229841) 确认建模非处理 ✅
- staircase FSO (10.1109/ICSOS66026.2025.11443140) 确认非相干无 PS ✅

**4 切入点状态**：

| 切入点 | 状态 | 撞界 |
|---|---|---|
| 1. 指向×Doppler | 🟢 空白可做（限定信号处理侧） | ⚠️ 纯 pointing/ATP 撞 S007；"指向对 DSP 影响"不撞 |
| 2. 真实 SD-FEC | 🟡 方法论成熟+场景空白 | ✅ 不撞 |
| 3. DWDM | 🟡 增量绑定移植 | ✅ 不撞 |
| 4A. 湍流相位进同步 | 🔴 撞死 D006 | 🔴 |
| 4B. 湍流时变×Doppler 调度 | 🟢 空白可做 | ✅ 不撞 D006 |

核查中发现 3 个 nuance：TS-KF (10.1364/oe.553709) 被切入点 1 检索召回=Q1；Spectral Segmented CFOE（无 DOI）描述 Q8 场景替代方法；HCS polar-DMT (10.1109/LPT.2024.3434993) 切入点 2 相关但 polar 非主流。

### 3. 用户选定切入点 2 + Step 4b MVE 设计

用户选切入点 2（最硬）。进 Step 4b 前先读 gw-feasibility 维度 D + 判 FR-21。

下载辅助文献：Post-FEC BER (arxiv 1911.01585) ✅；Cho&Winzer 2019 + FPGA 2022 (IEEE DOI) fail（urllib 不走代理），blit IEEE 未命中目标 review。

子 agent 精读 Post-FEC BER 提取量化结论：
- coding gap = ASI 0.86 vs R_c 0.8 = 0.06 ASI 单位（§445）
- 比特映射效应所需 SNR 差 0.1-0.3 dB（§480）
- 论文未给"理想 vs 真实"整体 gap 单一数字，指向 cho_2019_jlt 作主源

### 4. 🔴 事实修正（FR-26）

精读笔记 L08 旧判读"FEC 假设理想（NGMI_th=R_FEC）"**不准确**。核对 Fernandes L189 原文：用 **NGMI=0.88** 作为"practical SD-FEC with 20% overhead"典型阈值（0.88 > R_FEC=5/6=0.833，已含 coding gap）。
切入点 2 剩余增量 = "通用 0.88 vs 码型特异精确阈值"散布，非"理想 vs 真实"全 gap。此修正降低增量预期。

### 5. Step 4b MVE 设计 + 执行（方案 2 反推）

Fernandes 式 10 公式图被 blit 省略（"==> picture intentionally omitted <=="），无法精确复现 NGMI-SNR-熵关系。改方案 2：反推 LEO 放大因子 K。

**反推**：Δ_fiber=0.1-0.3dB；达 0.5dB FR-21 需 K=1.67×-5×；达 2dB D005 需 K=6.67×-20×。

**K 物理判读（Kill 依据）**：Post-FEC BER 散布来源是比特映射 + SD-FEC 码型内部特性（L480），**跟信道时变无关**。LEO 时变信道影响 NGMI 绝对值（需 Rs 适配应对），不影响 NGMI 阈值散布宽度。**K≈1，LEO 不放大散布**。

**MVE 结果：FAIL**。Δ_LEO ≈ Δ_fiber = 0.1-0.3dB < 0.5dB ≪ 2dB。

### 6. Q8 切入点 2 Kill

Kill 理由：①MVE FAIL（K≈1 物理不成立）；②Fernandes 已用经验阈值；③FR-21 <0.5dB；④D005 需 2-4dB 差 7-40×。

**Q8 剩余可行切入点**：1（踩 S007 边界）/ 4B（不撞界）。

## 决策引用

- D005：务实路线 INVARIANT（Go=赢传统 baseline 几 dB）— 本轮 MVE 判据基准
- D006：Q12 Kill（湍流相位进同步算法已 Kill）— 切入点 4A 撞界依据
- 无新建 D###（切入点 2 Kill 记 feasibility_report，非架构决策级；如需正式 D### 下轮补）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（块 E Step 4a/4b 切入点深化 + MVE，未跑出星地激光大背景，未放水四判据）

## 后续

1. **Q8 剩余路径**：深化切入点 1（踩 S007 边界，需限定信号处理侧）或 4B（湍流时变×Doppler 调度，不撞界）
2. **或转评估 Q1**（TS-KF 两阶段解耦 Doppler，四判据全过无旧 Kill 史）作对比后选最优
3. **⚠️ 待决债务**：MVE Kill 依据"散布跟信道无关 K≈1"是物理推理未经独立文献验证。若要更硬证据：补检索"时变信道 NGMI 散布"文献；或接受物理判断（散布是 FEC 解码器特性跟信道无关是通信理论常识）
4. **至少 1 个 Q# Go 才进块 F**（Step 5-7）。目前 Q8 未 Go（切入点 2 Kill），其他 Q# 未评
5. **本轮做 D### 吗**：切入点 2 Kill 我倾向记 feasibility_report 不单独建 D###（非方向级 Kill，是切入点级 Kill，Q8 整体未死）。但下轮若 Q8 整体也 Kill（切入点 1/4B 都不行），需立 D### 记 Q8 整体 Kill
