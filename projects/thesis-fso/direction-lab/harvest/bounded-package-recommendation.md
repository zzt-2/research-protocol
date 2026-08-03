# Bounded Package Recommendation — Gap-to-Package Map + Single Small Package

> **SUPERSEDED / PAUSED — D025→D026 (2026-08-03)：D024 小包执行已暂停；本文件不再授权统一鲁棒性表或正式 Ch4 写作，当前下一合法包见 D026。**

> 2026-08-03 | 关联: conference-to-thesis-map.md、asset-claim-matrix.yaml
> Phase E（gap-to-package map）+ 唯一小包推荐。**本轮只诊断不派实验**。任何执行需新合同 + 用户批准。

---

## Phase E — Gap-to-Package Map

所有缺口按五级分类。**本轮不派实验**，只标分级。

| Gap | 类别 | 现状 | 文件指针 | 价值（对 Ch4/Ch5） |
|---|---|---|---|---|
| headline G_C 复算（9 dB 三档） | **READY** | selector_a JSON raw 可一行确定性复算 0.8–1.5 dB | `results/ccisp_family1_selector_a_30seed.json` | Ch3 T1 表 |
| 三图（Fig.3/4/5）regeneration | **RECOMPUTE_ONLY** | raw READY，重画为 plotting pass | `figures/ccisp_fig{2,3,4}_*.pdf` 生成脚本 | Ch3 图 |
| P02 region retune 数字 | **READY** | D040 已闭合 +0.454/+0.358/−0.096 dB | longitudinal decisions.md D040 | Ch4 T2 行 |
| P04 continuous GG 数字 | **READY** | D042 已闭合 +0.146 dB CI[+0.083,+0.209] | longitudinal decisions.md D042 | Ch4 T2 行 |
| P11 strong-traditional 边界 | **READY（PARTIAL）** | 20 dB partial only | pilot-jones-step4a/ B0/B1/B2 | Ch4 T2 行（限定 20 dB） |
| branch-routing 990/990 bit-exact | **READY** | formal authority JSON（V015） | `results/ccisp_family1_branchrouted_b_30seed.json` | Ch5 F6 |
| P03 Q(8,6) identity 0/132000 | **READY** | phaseA_uniform.json | `results/p03_fixed_point_codesign/phaseA_uniform.json` | Ch5 T3 行 |
| **统一鲁棒性表（P01 adapter + P04 continuous GG）** | **SMALL_VALIDATION** | P01/P04 数据 READY，需统一口径合并 + 可能补连续 GG 网格 | P01/P04 现有 + 可能补连续 GG channel grid | **Ch4 核心（最高价值）** |
| **full-grid branch-compute timing（formal 口径）** | **RECOMPUTE_ONLY→SMALL_VALIDATION** | OLD-params 诊断 JSON 有 33-cell timing 但**无 authority**；formal B JSON **无 timing 字段** | `_a4_branchrouted_30step2.json`（诊断）/ `ccisp_..._b_30seed.json`（formal 无 timing） | Ch5 F7（中等价值，需 warm-up/重复/多条件） |
| **float-vs-Q BER（formal CCISP grid）** | **NEW_INFRASTRUCTURE（局部）** | 仅 Q-vs-oracle regret（FROZEN errors），float-vs-Q 绝对 BER 曲线不存在 | `_p03_fixed_point.py` 需扩 float path | Ch5 T3 补充（低-中价值，claim ceiling 仍是数值精度） |
| **coded chain freeze rerun** | **NEW_INFRASTRUCTURE** | PARTIAL，无 pre-test freeze receipt（D051） | `p08r2_chain.py` 需独立 freeze + rerun | Ch5 T4（低价值，coded 是通用设施非主线） |
| G1/P09 | **INVALIDATED** | D057/D053，禁晋级 | — | 仅 threats-to-validity/附录 |
| AMC | **INVALIDATED（packaging）** | D009 freeze，背景一句 | — | Ch6 未来工作一句（需用户授权新 GW） |

---

## 唯一推荐小包

**统一鲁棒性表（P01 SNR-adapter + P04 continuous GG）= 唯一推荐下一执行包**。

### 为什么是这个包

按 brief 的 8 条推荐包标准逐项核：

| 标准 | 是否满足 | 证据 |
|---|---|---|
| 直接增强 Ch4 或 Ch5 | **Ch4** | 填 Ch4 统一鲁棒性表（T2） |
| 复用现有正式 CCISP anchor | 是 | 被检验对象 = CCISP 两阶段 selector（A01） |
| 不开新方向 | 是 | P01/P04 是 selector 鲁棒性，非新算法 |
| 不需要新 channel/coded infrastructure | 是 | P01 SNR-adapter + P04 continuous GG 用现有 GG 信道组件（common/_channel.py） |
| 有传统 comparator | 是 | region retune（P02）= 传统重调 comparator；fixed-NDA = 主对手 |
| 有预注册 PASS/FAIL | 是 | 见下 |
| 失败仍能写成边界 | 是 | P01 终态本就是 `NO_DIAGNOSTIC_SIGNAL`，P04 是 `ABSENT_ON_CONTINUOUS_GG`——都是边界，失败即边界 |
| 不制造第二个算法 | 是 | 仅合并鲁棒性证据，无新机制 |

### 预注册 PASS/FAIL（执行前必须冻结）

**目标**：在统一口径下验证 CCISP 两阶段 selector 在 (a) SNR 失配 + (b) 连续 GG 下的鲁棒性，合并成 Ch4 一张表。

**PASS 标准**：
- (a) P01：5 个 substantial-harm cell 的 adapter 恢复 ≥4/5（复现 D040 既有结论）。
- (b) P04：连续 GG held-out pooled regret 仍 < MDE 0.15 dB（复现 D042 既有结论）。
- 合并表口径统一（相同 SNR 网格、相同 seed 协议、相同 metric 签名）。

**FAIL 标准**：
- (a) adapter 恢复 <4/5，或 (b) 连续 GG pooled regret ≥ MDE 且 OOD-specific（regret 在 strong-side 反而上升）。
- FAIL → Ch4 写成"selector 在 X 条件下退化，边界为 Y"（仍是合规边界章节）。

**执行范围**：
- 数据 READY 部分：P01 5-cell + adapter（step-028）、P04 held-out pooled（D042）—— **确定性复算，无新仿真**。
- 可能补：连续 GG 在 formal CCISP 三档 σ²_R（0.2/1.6/3.5）邻近的连续插值网格（若 D042 的连续 GG 网格与 formal 三档不完全对齐）—— **≤半天小验证**。

### 不推荐的包（本轮）

| 候选 | 不推荐原因 |
|---|---|
| full-grid branch-compute timing | 需 warm-up/重复/多条件新跑；74.6% 已明确单条件不可写；价值中等但 Ch5 已有 990/990 bit-exact 支撑"先选后跑"，timing 是锦上添花 |
| float-vs-Q BER | claim ceiling 仍是数值精度（非 FPGA）；P03 Q-vs-oracle regret 已够 Ch5 T3；新跑 float path 价值低 |
| coded freeze rerun | coded 是通用验证设施非主线；PARTIAL 不影响 Ch3/Ch4；价值最低 |
| 统一 figure/table regeneration | 纯 RECOMPUTE_ONLY，不是"小验证"，归入 Ch3 正常写作流程而非独立包 |

---

## 执行纪律（若用户批准）

1. **本轮不执行**——只诊断 + 包装合同。任何执行需新对话 + 新合同（T###）+ 用户批准。
2. 执行时守 FR-22（不跳框架：Ch4 鲁棒性是 GW Step 4a 维度 D 的延伸，不进 Contract/Execute 跑新算法）。
3. 守 D040/D042（A/C-family 已封顶/首包）：不 rename-reopen P01/P02/P04 轴，只合并既有结论。
4. 守 sim-preflight（参数溯源 + 三方对照 + 公式核对）。
5. 失败仍写边界（PASS/FAIL 都合规）。
