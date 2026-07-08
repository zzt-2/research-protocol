# Handoff: 对话 7 — B5 路 2 Step 4a sandbox 执行（2×2 消融 + 维度 A-D + Go/Conditional/Kill）

> 来源: S006（路 2 Step 3 补精读 + 新 M-C-A 构建）| 交接目标: 新对话执行 Step 4a sandbox + Go/Kill 判断
> 文件名: H007-conversation7-path2-step4a-sandbox.md
> 日期: 2026-07-08

## 到哪了（状态）

**B5 路 2 的 Step 3 补精读 + 新 M-C-A 构建完成。Step 4a sandbox + Go/Kill 判断留下一对话（守单对话 3 步上限 + profile"急于推进"防线）。**

### Step 3 精读结论（S006，推翻 H006 多项初稿）

| H006 初稿 | 精读修正（证据）|
|---|---|
| Vieira 公式 `α·ln(P+/P-)` | ⚠ **强推断非 verbatim**——L345 是图片（`picture intentionally omitted`，PDF→md 丢失）。基于 L347 文字推断 |
| Vieira α≈6.12e8 Hz（审计 JSON）| ⚠ **sandbox 自标定值**，**原文 α=17 GHz**（L349/L375，Vieira 自己 sequential search 重定，非继承 Diniz 21 GHz）|
| L387 ±13GHz 范围 | ⚠ **两阶段联合范围**（coarse PSA + fine Mth-power），**粗估单独 ~10 GHz** |
| 增量来自"线性 vs 对数算子" | ⚠ **未拆**：Vieira 无多块均值（单窗 1024 样本），B5 是 1024×16。σ 差可能主要来自块结构降噪 |
| Vieira 报 σ | ❌ Vieira **只报 BER penalty (dB)**，无 σ。B5 vs Vieira σ 是 sandbox 两边重标定后自算 |

**Diniz 2011（PSI 祖师爷）**：paywall 全锁（穷尽 6 源失败），仅 abstract 级。Eq.(1) 公式未知（log/线性比/arctan 无法确认），**不能据 Diniz 原文裁判 B5 vs Vieira**。

### 路 2 新 M-C-A（S006 §3）

- **M（baseline）**：Vieira 2023 PSA coarse CFE，算子 `α·ln(P₊/P₋)`（[推断]），单窗 FFT 1024 样本，α=17 GHz，无多块均值
- **C（场景）**：LEO 星地相干 FSO **残频估计**（星历预补后残频 ~MHz 级，**非原 ±4.5GHz 全量程**——D003 已证范围优势归零）
- **A（失效）**：Vieira 对数比在 P₊≈P₋（小残频）处数值放大噪声（ln 导数发散）——**假设待 Step 4a 验证，Vieira 原文未讨论此问题**
- **新方法**：B5 线性归一化比 `(P₊−P₋)/(P₊+P₋)` 替代对数比，小残频更稳（输出有界 [-1,1]）
- 四判据：✅ 全过（具体技术矛盾 / 有方法产出 / Vieira 2023 是 2019+ baseline / 能三方对照）

### 增量归因拆解设计（S006 §4，下一对话核心）

**2×2 消融矩阵**（公平条件：同星历预补 + 同采样率 + 同带限，守 D002 教训）：

| | 算子=线性 (B5) | 算子=对数 (Vieira) |
|---|---|---|
| **块=16 均值 (B5)** | A：B5 原配置（σ=9.7MHz，已测）| B：对数+16块（**待测**）|
| **块=单窗 (Vieira)** | C：线性+单窗（**待测**）| D：Vieira 配置（σ=28.7MHz，已测）|

**判定阈值**（前置门控，守 D003 + P5）：
- 算子贡献 > 30%（≥5.7 MHz）→ **Go 候选**
- 算子贡献 < 10%（≤1.9 MHz）→ **Conditional/Kill**（主要靠块结构）
- 10%–30% → 灰色区

## 下一步干什么（新对话 = Step 4a sandbox + Go/Kill）

### 第一步：补测 2×2 消融 B/C 格

复用 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_scope_advantage_audit.py`（sandbox 框架已建，experiment_C 同族对照代码在此）。**注意实际路径**：H006 写的 `explore/b5-...` 是错的，真实在 `projects/simulation/explore/b5-...`。

补测：
1. **B 格**：对数算子（Vieira `α·ln(P+/P-)`）+ 16 块均值（B5 块结构）
2. **C 格**：线性算子（B5 `(P+-P-)/(P++P-)`）+ 单窗（Vieira 块结构）
3. **α 选择**：跑两版——原文 Vieira α=17 GHz + sandbox 重标定 α=6.12e8，看是否影响结论

### 第二步：拆增量归因 + 维度 A-D 全过

- 算子贡献 = (B−D) 或 (A−C)；块结构贡献 = (C−A) 或 (D−B)
- 维度 A0（致命缺陷：对数比小残频不稳是否成立）/ A（Vieira 同族对手合法）/ B（复现性）/ C（算子贡献信号强度 >30%?）/ D（FR-21 降级参考）
- 守 FR-25（Go 标准=赢传统 baseline，Kill 标准=oracle 上界<0.5dB 或 MVE FAIL）+ D003（诚实判，增量拆不清或太小仍 Conditional/Kill）

### 第三步：Go/Conditional/Kill 判断 + 交 H008

- 算子贡献 >30% 且 A0 成立 → Go，进 Contract 准备
- 算子贡献 <10% 或 A0 不成立 → Conditional（看块结构是否独立可叙事）/ Kill
- 灰色区 → Conditional，列补救方案

## 纪律（和下一步直接相关的约束）

1. **FR-22 不跳维度**：Step 4a 维度 A-D **全过**才判 Go，不因算子贡献看起来>30% 跳 A0/B 验证。守 profile 第 7 次"急于推进"防线
2. **公平对照强制**（D002 教训）：B5 和 Vieira **同星历预补 + 同采样率 + 同带限**，无特权。给 Vieira 配 α=17 GHz（原文）为主，6.12e8（自标定）作辅
3. **V3 同族对照**（D002 教训）：对照对象 = **Vieira PSA**（同族机制最近），**不是 [60]Leven**（不同族）
4. **诚实判**（D003 候选池约束）：方向稀缺，增量改进值得试，但"值得试"≠"强行 Go"——算子贡献太小或拆不清仍 Conditional/Kill。**不能拿"方向少"当强行 Go 理由**
5. **FR-26 证据链债务**（已知，Step 4a 不解决但记录）：B5 锚全文失败（算子定义是重建非 verbatim）/ Vieira L345 图片（α·ln 是推断）/ Diniz paywall 锁。若 Step 4a Go 进 Contract 需补全文核验

## 接口变更（代码改动）

**本轮（对话 6）无代码改动**（只读精读 + 文档）。

**下一对话（Step 4a）将改动**：
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_scope_advantage_audit.py`：补 B/C 两格消融实验代码
- 新结果 JSON：`_ablation_2x2_results.json`（2×2 消融数据 + 算子/块结构贡献分解）

## 失败数据附录（如涉及路线失败）

无新失败数据（本轮无实验）。历史失败数据见 H006 §失败数据附录（B5 原范围优势路线 D003）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B5 锚全文失败 | FR-26 证据链 | optcom.2024.130981 paywall（11 源穷尽），算子定义是 content.md 重建非 verbatim | 若 Step 4a Go 进 Contract，需机构权限下载全文核 |
| Vieira 公式 L345 图片 | FR-26 | α·ln 是基于 L347 文字的推断，非 verbatim | 回原 PDF 核 Eq.(14) 附近 |
| Diniz 2011 Eq.(1) 未知 | FR-26 | paywall 锁，abstract 级，公式形式无法确认 | 同上（机构权限）|
| sandbox Vieira α 自标定 | 公平对照 | 审计 JSON 用 6.12e8（自标定）非原文 17 GHz | Step 4a 跑两版 α 对照 |
| V3 对照对象曾选错 | sim-preflight V3 | S005 选 [60]Leven 不同族（D002 已纠）| Step 4a 改 Vieira 同族 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 算子贡献（路 2 核心）| >30%（≥5.7 MHz）| S006 §4 判定阈值 | ⬜ 待测（2×2 消融）|
| A0 对数比小残频不稳 | 实测验证成立 | S006 §3 M-C-A 的 A | ⬜ 待验证 |
| 同族 PSA 对照（V3）| B5 vs Vieira rel_diff >5% | V3 同族 | ✅ 初测 66%（待 Step 4a 复核）|
| ~~范围优势（原）~~ | ≥10× 公平对照 | ~~INVARIANT 11~~ | ❌ FAIL（1.00×，D003）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，注意 INVARIANT 11 已 D003+S006 重写）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] Vieira α=17 GHz 是原文值（核查 `papers/doi/10.1109_access.2023.3287501/content.md` L349/L375）
  - [ ] Vieira 无多块均值（核查 L375 "FFT window of 1024 samples"，全文无跨块平均）
  - [ ] ±13 GHz 是联合范围（核查 L387 "combination with the coarse CFE stage raises... to at least 13 GHz"）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定：problem-driven-redirection / cut-pattern / deep-read / step4a-mve-execution）
- [ ] 已确认当前范围：路 2 Step 4a sandbox（不回头救范围优势 / 不卖星历+FOE 架构 / 不跳 Step 3 已完成）

## 下一轮

**新对话（Step 4a sandbox 执行）**：
1. 补测 2×2 消融 B/C 格（对数+16块 / 线性+单窗）+ 两版 α 对照
2. 拆算子贡献 vs 块结构贡献，判是否 >30%
3. 维度 A-D 全过（守 FR-22 不跳维度）
4. Go/Conditional/Kill 判断
5. 交 H008（若 Go 进 Contract 准备 / 若 Kill 列 salvage）
