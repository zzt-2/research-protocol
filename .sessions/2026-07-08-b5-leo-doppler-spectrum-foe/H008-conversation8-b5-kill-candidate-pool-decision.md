# Handoff: B5-Q1 Kill 收尾 + 候选池下一步决策（交用户）

> 来源: S007（路 2 Step 4a sandbox → Kill）+ D004 + V001 | 交接目标: 用户决定候选池下一步
> 文件名: H008-conversation8-b5-kill-candidate-pool-decision.md
> 日期: 2026-07-08

## 到哪了（状态）

**🔴 B5-Q1 Kill（D004/S007）。两条够格路径双证伪，B5 不再推进。**

### Kill 证据（2×2 消融，主线 V5 独立重算可复现）

路 2 Step 4a 维度 A0+C 双 FAIL：

| 维度 | 结果 |
|---|---|
| **A0 致命缺陷** | M-C-A 的 A（对数比小残频不稳）**证伪**：B/A σ 比=1.00 <1.30，linear-log 相关 0.994。两算子在 P+≈P- 处信息等价 |
| **C 信号强度** | 算子贡献 **−1%**（<10% Conditional-Kill 阈值）。66% σ 差全部来自 FFT 分辨率（n_fft=16 vs 1024）|

**四格 σ（MHz）**：A 线性 n16=11.369 / B 对数 n16=11.372 / C 线性 n1024=28.957 / D 对数 n1024=28.709

**贡献分解**（主线 V5 重算）：算子贡献 −0.123 MHz（−0.7%），FFT 分辨率贡献 +17.46 MHz（101%）。总差 17.34 MHz。

**无 salvage**：B5 相对 Vieira 既无算子贡献（−1%），n_fft=16 参数选择也是公开工程参数（B5 锚 content.md L87，Vieira 可同样采用）→ 不构成独占贡献。

### B5-Q1 两条够格路径回顾（都证伪）

1. ~~**范围优势**（±4.5GHz vs ±312.5MHz，15×）~~ → **D003 证伪**：fft_foe 配星历即 19/19 持平，残留 1.00×。范围优势是星历预补特权功劳
2. ~~**同族精度增量**（B5 线性比 vs Vieira 对数比，σ 好 66%）~~ → **D004 证伪**：算子贡献 −1%，66% 全来自 FFT 分辨率参数

### 新发现：experiment_C α 标定 bug（影响 S005 旧归因，不影响 Kill）

`_scope_advantage_audit.py` L421-422：grid C（B5@n_fft=1024）用锚 α=6e8（n_fft=16 标定值）未为 n_fft=1024 重标 → σ 被压到 14.1MHz（重标后真实 29.0MHz）。这解释了为何 S005/D003 初看"B5 n_fft=1024 下 σ=14.1 仍优于 Vieira 28.7"——其实是 α 没重标导致 B5 被人为压低。**教训**：跨 n_fft 对照必须每格独立 α 标定（D004 教训 2）。

## 下一步干什么（用户决策点）

**B5 Kill 后，候选池现状**：

| 候选 | 状态 | 阻塞/进展 |
|---|---|---|
| NDA-ML (B11-Q1) | dormant | 卡 D-008 双 bug + D-009 线宽选择，待用户拍板方法方向 |
| B7 Gardner TED | active | 阶段 0 完成，S006 smoke test PASS，进对话 7 正式 MVE 跑数 + Go/Kill |
| B3-Q2 联合估计 | active | 阶段 0 进行中（S001/S002），首验证 4 支路迁移 |
| B2 fade-freeze | closed | Killed（D004/K001，闭环版救援三 Go 全 FAIL）|
| **B5 短时谱** | **closed（本轮 Kill）** | 两条够格路径双证伪 |

**用户可选项**（H008 不替用户拍板，列选项）：
1. **推 B7 出 MVE 结果**（B7 是当前最活跃候选，smoke test 已 PASS，离 Go/Kill 最近）
2. **等 B3-Q2 阶段 0**（B3-Q2 +2~3dB 是候选池最高 dB，但 4 支路迁移+A1 归属风险未解）
3. **回拍 NDA-ML 方法方向**（D-008/D-009 待用户决定线宽 + vs VV 持平怎么处理）
4. **开新候选**（候选池持续收缩，但 D005 务实路线允许继续试）
5. **回看 thesis-method-redirection 的种子**（如 16-QAM CPR 扩展，Q2 自承仅 QPSK 未扩展）

**主线建议**（仅供参考，用户决策）：B7 离 Go/Kill 最近（smoke test PASS），优先推 B7 出结果最划算。但用户最了解自己节奏和导师偏好。

## 纪律（和下一步相关的约束）

1. **Kill 是终判，不再救 B5**：两条够格路径双证伪，无 salvage。禁以"再试试看"重启 B5（除非用户明确要求且能指出新角度）
2. **候选池约束（D003）依然适用**：方向稀缺，但"值得试≠强行 Go"。下一个候选同样要诚实判
3. **B5 Kill 不连坐其他候选**：B5 死是 B5 自身问题（范围优势是特权 + 算子无贡献），不影响 B7/B3/NDA-ML 的独立判断
4. **复用资产保留**：B5 代码（common 的 short_time_spectrum_foe + leven_mthpower_foe + explore 全部脚本 + _ablation_2x2_results.json）作 baseline 库扩展 + 教训素材，不删

## 接口变更（代码改动）

**本轮（对话 7）新增**：
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_ablation_2x2_results.json`：2×2 消融实测数据（Kill 证据）
- （子 agent 可能新建了 `_ablation_2x2.py` 或改了 `_scope_advantage_audit.py` 加 experiment_D——以实际文件为准）

**common 不变**：short_time_spectrum_foe + leven_mthpower_foe 留 common（算法实现正确，consistency PASS，作 baseline 库）

## 失败数据附录（B5-Q1 完整失败链）

**B5-Q1 两条够格路径失败数据**：

1. **范围优势失败（D003）**：`_scope_audit_results.json` experiment_B——fft_foe 配星历 19/19 = B5 19/19，残留 1.00×；fft_foe 残频 976kHz 比 B5 10.27MHz 好 10×。核心机制：范围优势是星历预补特权功劳
2. **同族精度增量失败（D004/S007）**：`_ablation_2x2_results.json`——算子贡献 −1%（四格 σ：A=11.369 / B=11.372 / C=28.957 / D=28.709 MHz）。核心机制：线性比 vs 对数比在 P+≈P- 处信息等价（相关 0.994），算子无贡献；66% σ 差全来自 FFT 分辨率参数（n_fft=16 公开工程参数，非独占）

**被排除的方向**（B5 内部，禁重启）：
- 卖范围优势（星历预补特权，非独有）
- 卖星历+FOE 架构（Paillier/sat.1553 已发表）
- 卖线性比对数比算子差异（证伪，相关 0.994）
- 卖 n_fft=16 参数选择（公开工程参数，Vieira 可同样用）

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B5 锚全文失败 | FR-26 证据链 | optcom.2024.130981 paywall（11 源穷尽）| **B5 Kill，不再需要补**（债务随 Kill 注销）|
| Vieira 公式 L345 图片 | FR-26 | α·ln 是推断 | 同上，B5 Kill 后无需 verbatim 核 |
| Diniz 2011 Eq.(1) 未知 | FR-26 | paywall 锁 | 同上 |
| experiment_C α 标定 bug | 公平对照 | grid C 未重标 α（已记录 D004 教训 2）| B5 Kill，bug 影响已说明（不影响 Kill 结论）|

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 结果 |
|--------|----------|------|
| ~~范围优势~~ | ≥10× 公平对照 | ❌ FAIL 1.00×（D003）|
| ~~同族 PSA 对照（V3）~~ | B5 vs Vieira rel_diff >5% | ⚠ 初测 66% 但**归因错**（D004：66% 是 FFT 分辨率非算子）|
| ~~算子贡献（路 2 核心）~~ | >30% | ❌ FAIL −1%（D004）|
| ~~A0 对数比小残频不稳~~ | 实测成立 | ❌ FAIL B/A=1.00（D004）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（INVARIANT 11 已终判 Kill）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 算子贡献 −1%（核查 `_ablation_2x2_results.json` operator_contribution.operator_share_of_total ≈ −0.007）
  - [ ] 四格 σ（核查 sigma_2x2_mhz.1.0GHz：A≈11.37 / B≈11.37 / C≈28.96 / D≈28.71）
  - [ ] B5 锚 n_fft=16 是论文定（核查 params.py FFT_POINTS_B5 source "content.md L87 16-point FFT"）
- [ ] 已检查 _registry.yaml：B5 depends_on 4 项仍稳定（Kill 不影响依赖专题）
- [ ] 已确认范围：B5 Kill 终判，不再推进 B5（除非用户明确要求新角度）

## 下一轮

**用户决策**（H008 不替用户拍板）：
- 推 B7 / 等 B3-Q2 / 拍 NDA-ML / 开新候选 / 回看种子——选一个
- 主线建议（仅供参考）：B7 离 Go/Kill 最近，优先推

**专题去向**：B5 Kill 后，待用户确认无复盘需求则专题转 closed（本轮先 active 留此 H008 交接）。
