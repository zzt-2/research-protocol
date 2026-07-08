# Handoff: 对话 5/6 — B5 路 2 同族精度改进重定位（范围优势已崩塌，重走 Step 4a）

> 来源: S005 + D002 + D003（对话 4 审计 + 判定）| 交接目标: 新对话执行路 2 重走 Step 4a
> 文件名: H006-conversation6-path2-reposition.md
> 日期: 2026-07-08

## 到哪了（状态）

**B5 原定位（范围优势够格）已崩塌，转路 2 同族精度改进重定位。不 Kill，因候选池整体偏弱+方向稀缺（用户原话"别的也一般般？有方向就可以试试，方向没那么多"）。**

### 审计结论（D002 + D003，3 决定性问题实测）

| 实验 | 结果 | 判定 |
|---|---|---|
| A（BER 根因）| AWGN 13dB BER=0（评估无 bug）。根因 B5 估噪 σ=6.8MHz >> fft_foe 0.05MHz，B5 粗估残频致 BER 退化 | BER fail 部分真实（B5 估噪大）|
| **B（公平范围对照）** | **fft_foe 配星历 19/19 = B5 19/19 持平，残留范围优势 1.00×（归零）**。fft_foe 残频 976kHz 比 B5 10.27MHz 好 10× | **Kill 级：范围优势是星历特权功劳** |
| C（同族 PSA 对照）| B5 σ=9.7MHz vs Vieira σ=28.7MHz，rel_diff=66%（V3 未触发，有真增量）。消融：同 n_fft=1024 下 B5 14.1 < Vieira 28.7 | **救命级：线性 Rp-n 比对数比好，同族内有增量** |

### "星历+FOE"不能水（用户直觉确认）
- Paillier JLT 2020 L17/L105 已发表此框架
- sat.1553 L464-466 已列
- 实验自证伪：fft_foe+星历比 B5+星历精度还高 10×

### 路 2 唯一活路
B5 线性归一化比 `(P+-P-)/(P++P-)` 比同族 Vieira 对数比 `ln(P+/P-)` 残频 σ 好 66%。但增量归因需拆清：纯算子改进（线性 vs 对数）贡献多少，1024×16 块结构降噪贡献多少。

## 下一步干什么（新对话 = 路 2 重走 Step 4a）

> **守 FR-22**：路 2 是新 M-C-A，必须重走 Step 3（精读 Vieira/Diniz）→ Step 4a（新 Go/No-Go）。不能直接跑 MVE。

### 第一步：重读同族（Step 3 补精读）

路 2 的新 M-C-A 需要 Vieira 2023 + Diniz 2011 的精读笔记（目前只有 B7 专题里 `_B7-gardner-ted-increment.md` 把 Vieira 当 baseline 提过，没独立精读）：
- **Vieira 2023**（`papers/doi/10.1109_access.2023.3287501/content.md`）：PSA coarse CFE 完整算法（L343-347 公式 / L375 参数 / L387 ±13GHz 范围）+ 两级 PSA+Mth-power 链路
- **Diniz 2011**（Opt. Express 19, B323，power-spectrum-imbalance 源头）：需下载精读（可能未落盘，查 papers/ 或用 tools/download）
- **B5 锚**（已精读）：Rp-n 线性归一化比机制

### 第二步：新 M-C-A + Step 4a Go/No-Go

路 2 的 M-C-A（初稿，新对话精读后修正）：
- **M（方法）**：B5 短时谱线性 Rp-n（`(P+-P-)/(P++P-)`）+ 星历预补 + 迭代
- **C（条件）**：LEO Doppler 星地相干（但注意：星历预补已证非 B5 独有，C 要聚焦"残频估计精度"而非"范围"）
- **A（失效）**：同族 Vieira PSA 对数比 `ln(P+/P-)` 在小残频处数值放大噪声（P+≈P- 时 ln 不稳定）
- **新 baseline**：Vieira 2023 PSA（同族，主对照）+ fft_foe（传统，参照）
- **新 fair gain 维度**：残频 σ（精度，不是范围）+ 同族增量 dB（如果上完整链路）

### 第三步：拆增量归因（Step 4a 维度 D 关键）

B5 vs Vieira 的 66% 残频 σ 改善来源：
- **假设 1**：线性 vs 对数算子（纯机制差）
- **假设 2**：1024×16 块均值滤波降噪（块结构差）
- **消融设计**（实验 C 已部分做）：同 n_fft=1024 同总样本下 B5 vs Vieira（已测：14.1 vs 28.7MHz）→ 拆出假设 2；再变 n_fft 看假设 1
- **判定**：假设 1 贡献 >30% → B5 算子有真贡献；假设 1 贡献 <10% → 主要靠块结构，算子增量弱

## 纪律（和下一步直接相关的约束）

1. **FR-22 重走 Step 3**：路 2 是新 M-C-A，必须先精读 Vieira/Diniz（同族源头），不能直接跑 MVE
2. **公平对照强制**：路 2 所有对照必须给 baselines 同条件（星历/采样率/带限），不再给 B5 特权（D002/D003 教训）
3. **V3 同族对照**：祖师爷警报对照对象 = Vieira PSA（同族），不是 [60]Leven（不同族）。rel_diff <5% 才触发警报
4. **候选池约束**（用户 D003 原话）：方向稀缺，B5 增量改进也值得试。但"值得试"≠"强行 Go"——Step 4a 要诚实判，增量拆不清或太小仍可能 Conditional/Kill
5. **INVARIANT 11 实质失效**：范围优势已证伪，够格路径转为"同族精度增量"。新对话要更新 topic-index 不变量

## 接口变更（代码改动）

**本轮（对话 4）已完成**：
- `common/_recovery.py`：short_time_spectrum_foe + leven_mthpower_foe（转正保留，路 2 仍用）
- `explore/b5-leo-doppler-spectrum-foe/`：B5-MVE-SPEC.md / mve_b5_short_time_spectrum.py / _mve_results.json / _ephemeris_residual_sweep.json（MVE 记录，路 2 参照）
- `explore/b5-leo-doppler-spectrum-foe/_scope_advantage_audit.py` + `_scope_audit_results.json`（本轮审计，路 2 基础）

**路 2（新对话）将新增**：
- Vieira 2023 + Diniz 2011 精读笔记（`papers/_read_notes/`）
- 路 2 新 M-C-A 文档 + 新 sandbox（公平对照）+ 新 MVE（同族 PSA 对照）

## 失败数据附录（如涉及路线失败）

**B5 原定位（范围优势）路线失败**（D003 记录）：
- 核心失败机制：范围优势是星历预补特权功劳，非 B5 算法独有。fft_foe 配星历即持平（19/19）且精度反超 10×
- 排除的方向：不能再卖"范围扩展 14.4×"；不能卖"星历+FOE 架构"（Paillier/sat.1553 已发表）
- 可复用部分：B5 算法实现（common 转正保留）+ 实验C 同族对照数据（路 2 基础）+ sandbox 三方对照框架（公平化后复用）

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~范围优势结实度~~ | 需实测验证 | **✅ 已解决（D003）**：崩塌，转路 2 | — |
| V3 对照对象错误 | sim-preflight V3 要同族对照 | sandbox/MVE 选了 [60]Leven 不同族 | 路 2 新 MVE 改对照 Vieira PSA |
| 增量归因未拆 | 66% 改善来源不清（算子 vs 块结构）| 实验C 部分消融（同 n_fft 下 B5 仍优）| 路 2 Step 4a 拆清 |
| INVARIANT 11 实质失效 | 范围优势够格路径 | 已证伪 | 路 2 更新 topic-index 不变量 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ~~范围优势（原）~~ | ≥10× 公平对照 | INVARIANT 11 | **❌ FAIL（1.00×，D003）** |
| 同族 PSA 对照（路 2 新）| B5 vs Vieira rel_diff >5% | V3 同族 | ✅ 初测 66%（待 Step 4a 复核）|
| 增量归因拆清（路 2 新）| 算子贡献 >30% | D003 教训 | ⬜ 待拆（Step 4a）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条 + D002/D003 范围变更）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 范围优势归零（核查 `_scope_audit_results.json` experiment_B fft_foe_with_ephemeris 19/19 + range_advantage_remaining 1.00×）
  - [ ] 同族 PSA 增量（核查 experiment_C b5_vs_vieira_sigma rel_diff 0.663）
  - [ ] BER 根因（核查 experiment_A awgn_baseline ber_at_13db=0 + no_foffset_weak B5 0.26 vs fft 0.008）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围：路 2 重定位（不回头救范围优势 / 不卖星历+FOE 架构 / 重走 Step 3-4a）

## 下一轮

**新对话（路 2 重定位）**：
1. Step 3 补精读：Vieira 2023（已落盘）+ Diniz 2011（可能需下载）
2. 构建路 2 新 M-C-A（M=线性 Rp-n / C=同族 PSA 精度瓶颈 / A=对数比数值噪声）
3. Step 4a 维度 A-D：公平 sandbox（B5 vs Vieira 同条件）+ 增量归因拆解 + Go/No-Go
4. 守候选池约束（方向稀缺，增量改进也值得试，但诚实判）
