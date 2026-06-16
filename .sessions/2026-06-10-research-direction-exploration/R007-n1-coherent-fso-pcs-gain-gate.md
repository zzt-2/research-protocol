# [R007] N1 相干 FSO PCS gain 数据门控——门控解除（Tian 2021 报 1.3-1.5 dB）

> 2026-06-16 续 5 | 关联：专题 slug 2026-06-10-research-direction-exploration / D005（gain 数据门控）/ H005 任务块 N1
> 阶段: 方向探索（N1 Groundwork 前置数据门控）| 状态: 门控解除，N1 可进 Groundwork

## 调研问题

D005 给 N1 加了一道数据门控：进 N1 Groundwork 前**必须补"相干 FSO（intradyne，非 IM/DD）下 PCS shaping gain 的 dB 数字"**。门控逻辑：
- 找到相干 FSO PCS gain ≥1dB（精读正文，非 abstract 推断）→ **门控解除**，N1 可进 Groundwork
- 找到 gain 但 <0.5dB 或无显著 gain → **N1 降级**（gain 太薄撑不起方法章，TL-05 算法贡献需 ≥1dB 且非薄增益）
- 找不到任何相干 FSO PCS gain 数据 → **N1 标"数据不足"降级**（不能在缺数据时外推 IM/DD gain，TL-22 红线）

Elzanaty 2020（arXiv:2005.02129，N1 当前合法化身锚点）全部 gain（1-2.5 dB）是 **IM/DD M-PAM**，相干 QAM 下 PCS gain 无任何论文直接验证（S005/D005 记录的缺口）。

## 发现

### 检索与精读（2026-06-16）

2 条 `tools/search` 查询（slug 加 `-n1-gain-preflight` 后缀避免覆盖）：
- `probabilistic constellation shaping coherent free-space optical QAM turbulence`（71 去重 → 30 篇）
- `Maxwell-Boltzmann probabilistic amplitude shaping coherent optical wireless turbulence gamma-gamma gain`（38 去重 → 30 篇）

JSON 存 `search-archive/2026-06-16/`。检索命中多篇直接针对"相干 FSO + 湍流 + PS"的论文（先前 D005 记录的"无任何论文"被推翻——检索能力差异）。

**下载并精读 4 篇关键论文**（子 agent 精读，主对话交叉验证 dB 数字）：

| 论文 | 检测 | 信道 | 相干 FSO PS gain（dB vs uniform） | ≥1dB? |
|---|---|---|---|---|
| **Tian 2021**（MDPI Appl. Sci., DOI 10.3390/app11219805, c=3）| **相干**（BPD+LO, 90° hybrid）| **FSO Gamma-Gamma**（weak→strong sweep）| **1.3 dB（post-FEC BER @ 1e-2）/ 1.5 dB（SER @ 4e-1）/ 0.3-0.4 dB（AIR @ 1.8 bit/sym）** | **是** |
| Zahr 2024（JSAC, DOI 10.1109/JSAC.2024.3365898, c=9）| 相干+IM/DD 对照 | FSO lognormal（moderate, S≈0.1）| 无 dB 数字；正文称 coherent shaping gains "limited" for low-order ASK | 否 |
| Deng 2026（LPT, DOI 10.1109/LPT.2025.3647750, c=0）| 相干（intradyne, 90° hybrid）| FSO Gamma-Gamma（实验+仿真）| gain 已声称（"best BER under all turbulence"）但正文 BER 曲线为图片，dB 数字不可从文本提取 | 无 dB |
| Rode 2023（cite=35, JLT, arXiv 2212.03839, c=21）| 相干（fiber）| **Fiber AWGN + Wiener 相位噪声**（非 FSO，无湍流）| ~0.1 bit/symbol BMI（非 dB）| 不适用（fiber）|

### 核心证据：Tian 2021 直证相干 FSO PS gain ≥1 dB

**这是 D005 门控的决定性证据。** Tian 等人 2021（长春光机所 Wu Zhiyong 组）正是 N1 假设的精确场景：相干 FSO + QAM + Gamma-Gamma 湍流 + 概率整形。正文 dB 数字（主对话 grep content.md 交叉验证，逐字引用）：

> "At the post-FEC BER of 1×10⁻², the proposed PS scheme with H=3.7964 (resp. H=3.9451) obtains nearly a **1.3 dB (resp. 0.5 dB)** gain over the uniform QAM."

> "the PS scheme with H=3.7964 achieves about **1.5 dB gains** over the uniform distribution at an SER of 4×10⁻¹"

> "An approximately **1.3 dB shaping gain** was achieved by PS with H=3.7964, which proves the effectiveness of the proposed scheme in a **coherent FSO** system."

**条件**：PS-16QAM（CCDM + DVB-S2 LDPC），Maxwell-Boltzmann 分布（启发式 PSO 优化 PMF），Gamma-Gamma 湍流 weak→strong sweep，baseline = uniform 16-QAM。

### 关键限制（门控解除但不无条件 PASS）

1. **gain 随 SNR 递减**：Tian 正文明确"With the increase of the SNR, the shaping gain between the optimized PS and the uniform distribution decreases gradually. Eventually, the PMF approaches the uniform distribution." → **高 SNR（弱湍流）gain 趋零**。这是 MB 分布的本质（高 SNR 下 capacity-achieving 分布趋于均匀）。**N1 的 gain 主要在低-中 SNR（中-强湍流）区**，这与 Elzanaty blind 模式按 outage 分位点设计的逻辑一致
2. **AIR gain（0.3-0.4 dB）远低于 SER/post-FEC BER gain（1.3-1.5 dB）**：AIR（achievable information rate）是信息论指标，SER/BER 是工程指标。1.3-1.5 dB 的工程 gain 含 FEC + 编码增益协同，纯整形的信息论增量更小。**N1 若做方法章，应报 SER/post-FEC BER gain（1.3 dB），而非 AIR**
3. **强湍流（σ²_R > 1）gain 未单独列表**：Tian sweep weak→strong 但未按 σ²_R 数值隔离 gain。文本暗示弱湍流 gain 更大（"under weak turbulence, optimized PS closer to Shannon limit"），但与"gain 随 SNR 递减"结合看，实际是**中湍流（中 SNR）gain 最大**——弱湍流 SNR 高 gain 趋零，强湍流 SNR 低但分布 shaping 空间大。这点需 N1 Groundwork 数值复核
4. **Tian 是单一组（长春光机所）的单篇**：Wu Zhiyong 组在 FSO 相干检测 + PS 方向有持续工作（Deng 2026 也是该方向但 dB 未提取）。单一来源的 1.3 dB 需 N1 Groundwork 内用 Elzanaty blind 框架独立复现验证

### cite=35（Rode 2023）适用性

**不适用 FSO 门控**。Rode 是 fiber AWGN + Wiener 相位噪声，无湍流，gain 报为 ~0.1 bit/symbol BMI（非 dB）。相干检测 ✓ 但信道不兼容 Gamma-Gamma FSO。**cite=35 从 N1 关键论文列表降级为"PCS+CPE 联合优化方法参考"**（其 differentiable BPS + GeoPCS 方法论可迁移，但 gain 数字不能用于 N1 的 FSO 门控）。

### 其他相关论文（检索命中但未精读）

- **L8/L9 "Impact of Super-Gaussian Distribution on Shaping Gain of PS 64QAM in coherent FSO + turbulence"**（DOI 10.1109/ACP/IPOC63121.2024.10809965, c=1）：abstract 报"4% maximum transmission distance improvement vs MB distribution"（≈0.17 dB，**小**）——这是 PS 分布族（super-Gaussian vs MB）的内部对比，不是 PS vs uniform。印证 Tian 的"gain 随设计精细化提升空间有限"
- **L13 Zahr 2024 JSAC**：相干 vs IM/DD 信息论对照，shaping gain 在 coherent 低阶 ASK 上"limited"。**重要负证据**：coherent 低阶调制下 PS gain 确实小，Tian 的 1.3 dB 依赖 16-QAM（中阶）+ FEC 协同
- **L4/L11 OFC 2024 Th3C.5 "Tailoring rate and latency with PCS + interleaving in strong turbulence"**（DOI 10.1364/ofc.2024.th3c.5）：强湍流 65dB link-loss，未精读（abstract 无 dB），N1 Groundwork Phase B 可补

## 结论

**门控判定：解除（RELEASE）。** 相干 FSO PCS gain ≥1 dB 在文献中存在且经正文精读交叉验证——**Tian 2021 报 1.3 dB（post-FEC BER）/ 1.5 dB（SER）vs uniform 16-QAM，coherent 检测，Gamma-Gamma 湍流**，过 D005 门控阈值（≥1 dB）。

N1 **可进 Groundwork**（锚 Elzanaty blind 框架迁移到相干，参照 Tian 2021 的 1.3 dB 作为量级锚点）。

**但门控解除不等于无条件 PASS**——四个限制（gain 随 SNR 递减 / AIR 远低于 BER gain / 强湍流未隔离 / 单一来源）是 N1 Groundwork §B 必须复核的点，写进 R007 作为 Groundwork 的前置约束。

## 对决策的影响

- **D005 门控**：**解除**。D005 否决条件第 1 条满足（"补检索确认存在相干 FSO PCS gain 论文 ≥1 dB → N1 数据门控解除，可进 Groundwork"）。**不新建 D006**（D006 预留给"降级"路径，本轮走"解除"路径）
- **N1 候选状态升级**：从 S005/D005 的"存疑（数据门控）"→ "**倾向 PASS（门控解除，可进 Groundwork）**"。与 A3（S005 倾向 PASS）对称——两候选现在都倾向 PASS，各有 Groundwork 内可闭合的缺口
- **对 D004 互锁三章主轴**：A3+N1+2.2 三章互锁的物理可行性基础**增强**——A3 无死锁（S005）+ N1 gain 数据确认存在（R007）+ 2.2 纯解析保底。但"互锁"是结果非前提（S004 教训），仍需各自 Groundwork §B 通过
- **对 Elzanaty 锚点**：Elzanaty blind 框架（离线按湍流 CDF outage 分位点设计 MB 分布）仍是 N1 的方法来源，但其 IM/DD gain（1-2 dB）现在有相干对照（Tian 1.3 dB）支撑迁移合理性。N1 Groundwork 应同时引用 Elzanaty（方法框架）+ Tian（相干 gain 量级锚点）
- **对 cite=35**：从"N1 关键论文"降级为"PCS+CPE 方法参考"（D005 已疑，R007 确认 fiber 非 FSO）

### 下一步（N1 进 Groundwork，非本轮）

1. 读 `stages/groundwork.md` + `gw-feasibility.md §B`（框架文件规则）
2. N1 §B 空白零假设：对照 Tian 2021（已证 gain 存在）+ Elzanaty blind（方法框架）做 N1 的增量定位——N1 比 Tian 强在哪？（Tian 是启发式 PSO 全搜索 + 单一 MB 分布；N1 若锚 Elzanaty blind 离线设计 + 仰角确定性排程（D004 切法③）= 增量）
3. 复核 R007 四个限制（gain 随 SNR 递减 / AIR vs BER / 强湍流隔离 / 单一来源）在 N1 的 Groundwork 数值验证中是否闭合
4. **未到 MVE**（D001 后续阶段链不变）

### 不要做

- ❌ 把 Tian 的 1.3 dB 当 N1 的既得 gain 直接写进结论（Tian 是他人工作，N1 需独立增量；1.3 dB 是"领域已证 gain 存在"的锚点，不是 N1 的贡献）
- ❌ 忽略"gain 随 SNR 递减"——N1 若报高 SNR（弱湍流）场景的 gain 会得到 <0.5 dB 的错误结论
- ❌ 用 cite=35 的 fiber gain（~0.1 bit/sym）作 N1 的 FSO gain 锚点（信道不兼容）
- ❌ 在 N1 Groundwork §B 未过前锁"互锁三章"叙事（S004 教训）
