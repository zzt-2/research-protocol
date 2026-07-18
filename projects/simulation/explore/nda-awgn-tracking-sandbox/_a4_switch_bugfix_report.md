# 切换方法 bug 修复 + 重跑报告

> 日期: 2026-07-09
> 专题: .sessions/2026-07-06-step4a-mve-execution（S013 续）/ .sessions/2026-07-09-thesis-writing（D001）
> 代码: `_a4_switch_30seed_fixed.py`（新，原 `_a4_switch_30seed.py` 留作 bug 证据不改）
> 数据: `_a4_switch_30seed_fixed.json`（30 seed，net 口径）
> 纪律: TL-22（震撼结果先查物理前提）/ TL-23（NDA≥oracle 0 违例自检）/ TL-29（换口径先校准）

## 1. Bug 确认

| Bug | 是否成立 | 证据（代码行） |
|---|---|---|
| 1 混合分母 | ✅ **成立** | 原 `_a4_switch_30seed.py` L110: `b_n += Ns*BITS_PER_SYM`（NDA 全块 1024 bit）；同 L110: `b_d += int(np.sum(isd))*BITS_PER_SYM`（DA data 768 bit，去掉 64 pilot 位）；L112-113: SWITCH 混用两套分母（选 DA 块加 768，选 NDA 块加 1024）。→ NDA-BER / DA-BER / SW-BER 三者不同口径，互比不公平。 |
| 2 判据脱钩 | ⚠️ **部分成立，但非假增益驱动源** | L135: `decide(rx_raw,...)` 用 raw 信号算 cv/h；L129-132 候选用 `rxb`/`rxp`（均衡后）。脱钩属实。**但**：脱钩只 *损* SWITCH（判据信号 ≠ 候选输出 → 判错选错路），不 *帮* SWITCH，无法解释 +0.27-0.48dB 假增益。且 decide 必须在 raw 上做（接收端选估计器前不可能先均衡——均衡要 h，选估计器要判 h 大小，鸡生蛋）。**结论：判据用 raw 是合理的，Bug 2 不是 bug，保留原设计 + 文档说明。** |
| 3 事后对照 | ✅ **成立（假增益主因）** | 原 L152: `mx=[min(n,d) ...]` 取 NDA/DA **逐 seed 错误数最小值** = "每帧事后选赢家" = oracle 理想策略；L153: `switch_vs_max_db = 10·log10(min/sw)`。**盲判据不可能赢 oracle**，+0.27-0.48dB CI 下界全正是此 bug 产物。 |

**假增益归因**：Bug 1（分母混乱，DA 被高估）+ Bug 3（oracle 对照，SW 不可能输）共同造成。Bug 2 无关。

## 2. 修复方案

**Bug 1 — 统一全块 bit 口径（net 口径）**：
- NDA / DA / SWITCH BER 全部除以 `N_BLOCKS × N_DFT × BITS_PER_SYM`（=400×256×4，全块 bit）。
- DA 错误数仍在 data 位算（pilot 是已知插入符号不算信息错误，对齐主实验 `ber_da_awgn` 的 `is_data` 约定），但分母用全块 bit。
- **口径物理意义**：DA 的全块 BER = data 位 BER × (768/1024) = data 位 BER − 1.249 dB（= pilot overhead）。所以"全块口径"本质 = **已扣 pilot power penalty 的 net BER**，正是论文 net-gain 框架（R003）的口径。
- **同时存 gross 口径**（DA 错误数 / 768 data bit）作透明参考，不参与结论。
- 理由：这是主实验 net-gain 的标准对照口径——DA vs NDA 按 BER 比，pilot 能量代价在 net-gain 里单独扣（已在 fair_gain 做过），不在 per-bit BER 里重复扣。NDA 无 pilot，全块==data。

**Bug 2 — 保留 raw 判据 + 文档说明（不修）**：
- 见 §1 判定：decide 必须在 raw 上（接收端选估计器前没法均衡），判据估 γ_eff（交叉驱动量），raw 信号足够。
- decouple 只损不帮，非假增益源。原设计的"两层判据"（CV 门控 + γ_eff 门控）逻辑保留。

**Bug 3 — 删除 oracle max，改真实 baseline 对照**：
- 删除 `max(DA,NDA)`。
- 改报两个真实固定 baseline：`switch_vs_DA_net`（SW vs 固定 DA，net 口径，两边同分母）和 `switch_vs_NDA`（SW vs 固定 NDA，两边同分母）。
- **额外加 per-block oracle 上界**（Σ_b min(ne_n_b, ne_d_b)）= 任何选择器的可实现上界，作 TL-23 守门基准 + 论文"切换兑现了多少 oracle 空间"的诚实参考。

**TL-29 校准**：换口径后先校准——DA 全块口径 BER 应 = DA data 口径 BER × 0.75。实测一致（见下表 strong@24: DAnet=3.55e-2, DAdata=4.73e-2, 比值=0.751 ✓）。

**TL-23 守门（自检通过）**：SW 是盲判据，逐 seed SW BER 必须 ≥ 逐 seed per-block-oracle BER。30 seed 实测 **违例数 = 0**。SW *可以* 赢 frame-level min(NDA,DA)——那是合法 per-block 选择收益，不是 bug（曾误把 frame-min 当边界，4 个"违例"实为合法）。

## 3. 重跑结果（修复后，30 seed，net 口径）

> 增益正 = SWITCH BER 更低（SWITCH 赢）。CI = 95% t-分布。

| 场景 | SNR | 切换 vs 固定DA(net) | [CI95] | 切换 vs 固定NDA | [CI95] | 切换赢两边？ |
|---|---|---|---|---|---|---|
| **awgn** | 5 | **−0.17** | [−0.2,−0.1] | +0.09 | [+0.1,+0.1] | ❌ 输 DA 赢 NDA |
| | 8 | **−0.72** | [−0.8,−0.7] | +0.15 | [+0.1,+0.2] | ❌ 输 DA 赢 NDA |
| | 10 | **−0.92** | [−1.0,−0.9] | +0.09 | [+0.1,+0.1] | ❌ 输 DA 赢 NDA |
| | 12 | **−1.09** | [−1.1,−1.1] | +0.06 | [+0.0,+0.1] | ❌ 输 DA 持平 NDA |
| | 14 | **−1.19** | [−1.2,−1.2] | +0.00 | — | ❌ 输 DA |
| | 16 | **−1.14** | [−1.2,−1.1] | +0.00 | — | ❌ 输 DA |
| | 18(HD-FEC) | **−1.04** | [−1.1,−1.0] | +0.00 | — | ❌ 输 DA |
| | 20 | **−0.84** | [−0.9,−0.8] | +0.00 | — | ❌ 输 DA |
| **weak** | 5 | **−0.28** | [−0.3,−0.3] | **+1.81** | [+1.8,+1.8] | ❌ 输 DA 赢 NDA |
| | 10 | **−0.45** | [−0.5,−0.4] | **+2.30** | [+2.3,+2.3] | ❌ 输 DA 赢 NDA |
| | 15 | **−0.75** | [−0.8,−0.7] | **+0.98** | [+0.9,+1.1] | ❌ 输 DA 赢 NDA |
| | 20 | **−0.90** | [−1.0,−0.8] | +0.03 | [−0.0,+0.1] | ❌ 输 DA |
| | 22-26 | −0.94~−1.07 | — | ≈0 | — | ❌ 输 DA |
| **moderate** | 5 | **−0.14** | [−0.2,−0.1] | **+1.65** | [+1.6,+1.7] | ❌ 输 DA 赢 NDA |
| | 10 | **−0.22** | [−0.2,−0.2] | **+1.98** | [+1.9,+2.0] | ❌ 输 DA 赢 NDA |
| | 15 | **−0.43** | [−0.5,−0.4] | **+1.08** | [+1.0,+1.2] | ❌ 输 DA 赢 NDA |
| | 20 | **−0.62** | [−0.8,−0.5] | **+0.18** | [+0.1,+0.2] | ❌ 输 DA 赢 NDA |
| | 22 | −0.68 | [−0.9,−0.5] | +0.05 | [−0.0,+0.1] | ❌ 输 DA |
| | 24-26 | ≈−0.5 | — | ≈0 | — | ❌ 输 DA |
| **strong** | 5 | −0.04 | [−0.1,−0.0] | **+1.30** | [+1.3,+1.3] | 持平 DA 赢 NDA |
| | 10 | −0.02 | [−0.0,−0.0] | **+1.29** | [+1.2,+1.3] | 持平 DA 赢 NDA |
| | 15 | +0.02 | [−0.0,+0.1] | **+0.90** | [+0.8,+0.9] | 持平 DA 赢 NDA |
| | 20 | **+0.06** | [+0.0,+0.1] | **+0.39** | [+0.3,+0.4] | 持平 DA 赢 NDA |
| | 22 | **+0.05** | [−0.0,+0.1] | **+0.26** | [+0.2,+0.3] | 持平 DA 赢 NDA |
| | 24 | **+0.20** | [+0.1,+0.3] | **+0.15** | [+0.1,+0.2] | ✅ **两边都赢** |
| | 26 | **+0.15** | [+0.0,+0.3] | +0.09 | [+0.0,+0.1] | 持平 DA 持平 NDA |

**per-block oracle vs SWITCH（可实现上界差距，SWITCH 离 oracle 多远）**：
- AWGN: +0.94~+1.75 dB（oracle 空间大，SWITCH 兑现少）
- weak: +0.33~+1.30 dB
- moderate: +0.21~+1.32 dB
- strong: +0.15~+1.09 dB（strong 高 SNR SWITCH 兑现最好，+0.15~+0.42 在低 SNR）

## 4. 核心结论

- **切换 vs 固定导频（DA）**：**整体输了**。AWGN/weak/moderate 全 SNR、strong 低 SNR 区 SWITCH 显著输给固定 DA（−0.1~−1.2 dB，CI 上界多为负）。**唯一赢区 = strong 湍流高 SNR（15-26 dB），增益 +0.02~+0.20 dB（net 口径），且只有 strong@24 一个点 CI 下界 >0 显著**。物理上合理：只有强湍流高 SNR 区同时存在 deep-fade 块（DA 强）和非 fade 块（NDA 省 pilot overhead），per-block 选择才有真实空间。
- **切换 vs 固定盲（NDA）**：**低 SNR 区稳定赢**。weak/moderate/strong 的低 SNR 段（5-10/15 dB）SWITCH 显著赢 NDA **+1.3~+2.3 dB（CI 下界全正）**。物理：低 SNR 区 NDA 升幂噪声灾难（M₀=8），切换判据选 DA 避险——这是切换的**真实且显著的避险价值**。高 SNR 区持平（切换判据此时选 NDA，跟固定 NDA 一样）。
- **切换方法真实价值**：**不是"全面赢两个固定方法"，是"低 SNR 避 NDA 崩溃 + 强湍流高 SNR 微赢 DA"的条件性增益**。
  - **不存在原报告宣称的 +0.27~+0.48dB 全场景增益**（那是 Bug 3 oracle 对照的产物，已 TL-22 验证：盲判据不可能全面赢）。
  - 真实价值 = **鲁棒性/避险**：在 NDA 会崩的低 SNR 区，切换切到 DA 保命（+1.3~+2.3dB vs NDA）。代价 = 在 DA 本就够好的区域（AWGN/weak 全段），切换判据误选 NDA 反而输给固定 DA 0.1~1.2dB。
  - **唯一同时不输两边的工作区 = strong 湍流高 SNR（BER<<HD-FEC，~15-26dB）**，但即便那里 vs DA 的净增益也只有 +0.02~+0.20dB（net），多数点 CI 跨 0 不显著。唯一显著两边赢 = strong@24 一个点。
  - **对论文定位的影响（关键）**：切换方法**不应**作为独立卖点/核心贡献（原简报 v3 把它当 +1.2dB net gain 的"兑现机制"，现在看切换本身净增益微弱且条件性强）。切换的真实角色 = **NDA-ML 方法在低 SNR 区的鲁棒性补丁**（避免 NDA 在低 SNR 崩，让 NDA-ML 的"全工作区可用"叙述站住）。强湍流/上行的净增益 +1.2-1.8dB（主实验标准 BER）**仍成立且是主卖点**，不依赖切换。

**TL-22 复核**：修复后没有"全面赢"的震撼结果（用户预判命中——盲判据不可能全面赢固定方法）。低 SNR 输 DA 是正常的（AWGN 无 fade，DA pilot 稳赢；切换判据错选 NDA）。物理自洽。

## 5. 数据位置

- 修复后脚本：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py`
- 修复后 30seed 数据：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.json`
- 修复后 2seed 冒烟数据：`.../_a4_switch_2seed_fixed.json`（TL-23 自检验证用）
- 原 buggy 脚本/数据：`_a4_switch_30seed.py` / `_a4_switch_30seed.json`（留作 bug 证据，不改不删）
- 本报告：`.../_a4_switch_bugfix_report.md`

## 6. 给主线/写作专题的硬约束

1. **切换增益具体数字全部更新**：简报/论文禁用旧 +0.27~+0.48dB（不变量 8）。可用新数字：vs NDA 低 SNR +1.3~+2.3dB（避险）、vs DA 仅 strong 高 SNR +0.02~+0.20dB（弱）。
2. **切换不作为核心卖点**：主卖点维持强湍流/上行净增益 +1.2-1.8dB（主实验标准 BER，不受切换 bug 影响）。切换降级为"NDA-ML 低 SNR 鲁棒性补丁"。
3. **net 口径声明**：论文报 vs DA 增益必须用 net 口径（全块 bit），并脚注说明 pilot overhead 已在 BER 口径内扣除（DA 全块 = data BER − 1.25dB）。gross 口径（DA data BER）作附录透明参考。
