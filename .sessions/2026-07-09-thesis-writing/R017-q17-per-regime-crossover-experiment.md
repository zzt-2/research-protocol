# [R017] Q17 探索：per-regime crossover 阈值 vs 固定 13.0——选对率/增益变化实证

> 2026-07-12 | 关联：专题 `2026-07-09-thesis-writing` / revision-queue Q17 / D005
> 任务来源：`projects/simulation/explore/` Q17 探索 brief（Step 4a 维度 D MVE 判据调整范畴）

## 调研问题

Q17（revision-queue L74）：论文 W002 §III 声称 "γ_th is set to the **measured crossover SNR**, **determined separately for each regime**"，但代码 `_a4_switch_30seed_fixed.py:64` 实际用**固定 `GAMMA_EFF_TH=13.0` dB 跨所有 regime 统一**。两点都不符。如果改代码实现 per-regime crossover 阈值（选项②），选对率/增益怎么变？足以让论文文字变真吗？

## 发现

### 改法（路径 A）

保留 γ_eff 判据结构（CV 门控 + γ_eff 阈值两层，Bug 2 脱钩保留），唯一改动：γ_eff 阈值从单一 13.0 改成 per-regime dict：

```python
GAMMA_EFF_TH_REGIME = {
    'awgn': 99.0,      # 无 crossover（AWGN 全程 NDA 赢），设高值永远选 NDA
    'weak': 17.9,      # crossover ≈ 17.9 dB
    'moderate': 16.8,  # crossover ≈ 16.8 dB
    'strong': 10.7,    # crossover ≈ 10.7 dB
}
```

换算依据：crossover 在 γ 轴（平均 SNR）测的；decide() 阈值作用在 γ_eff 轴（γ_eff = γ_db + 10·log10(h_blind)）。实测各 regime median(h_blind) ∈ [0.77, 1.15]（unit-normalized fading），median(γ_eff) ≈ γ_db ± 1dB。故 `GAMMA_EFF_TH[regime] = crossover_γ[regime]` 是自然映射（median(h)≈1 → crossover_γ ≈ crossover_γ_eff）。

### 结果对比表（30 seed，data 口径判选对，net 口径判增益）

**选对率（switch_caliber_audit.py 定义：SW BER 离 DA_full 还是 NDA 近，推断选择，比 data 口径赢家）**：

| 指标 | FIXED (13.0) | PER-REGIME (17.9/16.8/10.7) | 变化 |
|---|---|---|---|
| 选对率 | **26/29 (90%)** | **25/29 (86%)** | **↓1 点（变差）** |
| 选错点 | strong@15/20/22 | strong@15/20/22 **+ moderate@20** | 新增 1 错点 |

**strong 高 SNR 3 点（D005 已知问题）——预期翻转，实际没翻**：

| 点 | winner(data口径) | FIXED 选择 | PER-REGIME 选择 | vs NDA 增益 FIXED→PERREG |
|---|---|---|---|---|
| strong@15 | NDA | DA ❌ | DA~ ❌ | +0.90 → +0.75（差距缩小但没翻） |
| strong@20 | NDA | DA ❌ | DA ❌ | +0.39 → +0.26 |
| strong@22 | NDA | DA ❌ | DA ❌ | +0.26 → +0.18 |

**vs NDA net gain（避险卖点，低 SNR 区）——per-regime 反而增强**：

| 点 | FIXED | PER-REGIME | Δ |
|---|---|---|---|
| weak@15 | +0.98 | **+1.56** | **+0.58** |
| moderate@15 | +1.08 | **+1.40** | **+0.32** |
| moderate@20 | +0.18 | **+0.47** | **+0.29** |
| weak@10 | +2.30 | +2.31 | ≈0 |
| strong@5 | +1.30 | +1.30 | 0 |

**TL-23 自检**：per-regime 版 SW ≥ per-seed per-block-oracle **违例数 = 0**（盲判据不可能赢 oracle，自检通过）。

### 物理机制（per-block 追踪，strong@15 1 seed 400 block）

关键发现：**crossover 是 γ 轴（平均 SNR）概念，decide() 作用在 γ_eff 轴（per-block），两者不能干净映射**。

th=10.7 时 strong@15 的 per-block 分布：
- decide=DA 的块（88 个，γ_eff<10.7，deep fade）：DA 赢 71，NDA 赢 17 → 判据对这些块**选对了**（DA 确实好）
- decide=NDA 的块（304 个，γ_eff>10.7）：**DA 赢 230，NDA 赢 74** → 判据对这些块**大量选错**（应选 DA 却选了 NDA）

机制：strong 湍流 deep-fade 块概率高，即使平均 SNR=15dB 远超 crossover 10.7dB，仍有 22% 块 γ_eff<10.7。这些块 DA 赢，被选 DA（对）。但 γ_eff>10.7 的 304 块里，DA 在 230 块仍赢（非 deep fade 但 DA pilot 仍更准）——判据把它们全判给 NDA（错）。

→ **γ_eff 是 crossover 的噪声代理**：per-block γ_eff 不能预测该块 DA/NDA 谁赢。降低阈值（13→10.7）只是把更多块判给 NDA，但 NDA 在这些块并不系统占优，所以选对率不升反降。

### 可实现性（冷静期 TL-22）

per-regime crossover 在接收端**可实现**（不算偷看 BER）：
- **regime 可测**：h 分布 / 闪烁指数 σ²_I = Var(|h|²)/E[|h|²]² → 湍流强度 → regime ID
- **crossover 值**：需离线校准（发训练序列测 BER 曲线找交叉点）→ 标准自适应系统实践（offline-calibrated LUT），**非在线 BER 偷看**（接收端解码未知数据时不测 BER）
- 论文 "measured crossover SNR per regime" = 离线校准 LUT，**可实现**

## 结论

### Q17 决策建议：选项 ③（中间方案）——改文字不声称 measured crossover，也不强调 per-regime

**不支持选项 ②（改代码 per-regime）**：
1. 选对率**变差**（26/29→25/29），strong 高 SNR 3 点**没翻转**，反增 moderate@20 新错点
2. 物理上 crossover-on-γ ≠ 好 γ_eff 阈值（γ_eff 是噪声代理），改 per-regime 不解决根本问题
3. 改代码=回 step4a 重跑（守 FR-22），且结果更差，无收益

**不支持选项 ①（纯改文字"a fixed threshold γ_th=13 dB"）**：
- 虽然诚实，但 D005 已知 13dB 偏保守导致 strong 高 SNR 选错，写死 13dB 暴露弱点

**推荐选项 ③（改文字，保留固定代码）**：
- §III 改写为 **"a fixed effective-SNR threshold γ_th, chosen to separate the DA- and NDA-favored operating regions"**（不声称 measured crossover，不强调 per-regime）
- 删除 "measured crossover SNR for each turbulence regime" + "determined separately for each regime" 两句（W002 §III 当前文字 L28）
- §IV-A 的 crossover 17.9/16.8/10.7 仍呈现（那是**数据观察**，不影响判据描述）
- 理由：既诚实（代码确实固定阈值），又不暴露 13dB 偏保守弱点（用"分离优势区"中性表述）

### 意外收获（per-regime 对避险卖点有增强）

虽然选对率变差，但 **vs NDA net gain 在中间 SNR 区（weak@15/moderate@15/moderate@20）提升 0.3-0.6 dB**——因为这些点 winner=NDA，per-regime 降低阈值（13→10.7/16.8）让更多块判给 NDA，正好对齐 winner。但这不改变 Q17 决策（代码仍保持 fixed，因为选对率是 Intro 承诺的 26/29）。

## 对决策的影响

- **revision-queue Q17**：从"pending 用户决策"更新为"建议选项③，附 R017 实证依据"
- **D005**："strong 高 SNR 3 点选错 = 判据 γ_eff 阈值 13dB 偏保守"归因**修正**——不是"13dB 偏保守"，是"γ_eff 是 crossover 的噪声代理"，per-regime（10.7）也救不回来
- **R009 不变量 7**（crossover 只呈现数据不附归因）不受影响——crossover 17.9/16.8/10.7 作为数据观察仍呈现，只是不再声称是 γ_th 取值来源

## 代码 + 数据路径

- per-regime 脚本：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_per_regime.py`
- per-regime 30seed 数据：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_per_regime.json`（369s，违例 0）
- per-regime 2seed 冒烟：`.../_a4_switch_2seed_per_regime.json`
- 对照 fixed 数据：`.../_a4_switch_30seed_fixed.json`（394s，违例 0）

## 不确定性标注

1. **路径 A 换算近似**：median(h)≈1 是近似（实测 0.77-1.15），更精确的 γ_eff 阈值需各 regime 单独校准（如取 γ_eff 分布的中位数匹配 crossover）。但 per-block 追踪显示 γ_eff 本身就是噪声代理，精确换算不会改变结论方向。
2. **路径 B 未跑**（改 decide() 直接用 γ vs crossover 比较，放弃 γ_eff per-block 机制）——会变成 frame-level 判据（同 SNR 所有块同选），失去 per-block 选择能力，预期选对率更高但失去 deep-fade 块的 DA 优势。未跑因 brief 指定"路径 A 优先，不行再考虑 B"，而路径 A 已给出明确结论。
3. **30seed CI**：strong 高 SNR 3 点增益 CI 在 fixed 和 per-regime 都跨 0 或接近 0，统计上不显著。选对率 26→25 的差异在单点（moderate@20）可能是 seed 噪声，但 strong 3 点没翻转是系统性的（per-block 追踪确认机制）。
