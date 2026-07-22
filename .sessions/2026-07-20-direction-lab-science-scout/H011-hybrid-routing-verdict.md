# Handoff: 混合盲均衡专家路由裁决 C + e15ae60 继承纠正

> 来源: S011 / D017 / D018 / V006 / V007 | 交接目标: 在干净状态上决定下一步（model-based tracker 或 harvest 收尾）
> 文件名: H011-hybrid-routing-verdict.md | 日期: 2026-07-22

## 已完成边界

- **e15ae60 继承纠正（D017/V006）**：commit e15ae60（C12/C14/C15/C16 + "5 轴穷尽"叙述）数值可复现，但 7 审计项全部 CONFIRM 科学语义失效/不足。H060 全域"信道属性/穷尽/不可提取求逆/可写完整负面/model-based 唯一剩余"5 宣称 **invalidated**，降级为 LOCAL_SLICE 弱断言。未重跑科学实验，未建 controller，未改 protected history。
- **混合路由 Macro A → VERDICT C（D018/V007）**：合法 FIR 专家（MMA 公平 μ + standalone cold-start DD-LMS）vs CMA，fresh disjoint test seeds [121-130]。oracle headroom = **0.0037** macro PI-SER，8× 低于实用阈值 0.03。机制=失效相关（MMA/DD-LMS 在 CMA 塌缩的同一 61/110 realizations 也塌缩）。原 C16 "26/37"确认为非法专家 + 污染 seeds 的伪象。独立 verifier 8/8 PASS。Macro B 不运行（无 headroom）。**关闭本具体 hybrid contract，不关闭算法选择家族。**
- 文件产物：`hybrid-routing-scout-v1/`（contract + dd_lms_equalizer.py + run_macro_a_oracle.py + test_hybrid_identity.py + result.v1.json + synthesis.v1.md）。治理：S011 / D017 / D018 / V006 / V007 / voice.md（2026-07-22 原话）/ topic-index / 4 个 current view 全部已同步。
- **本轮不产出毕业论文级"方法"**。产出：slice-level 负面 bound + 方法论教训。

## 不要做什么（Dead Ends）

- **不得复活"坍塌感知的合法 FIR 盲均衡专家路由（CMA↔MMA/DD-LMS）"**：机制=失效相关，headroom≈0.004。不得以"换 router""加 seeds""调阈值"复活——oracle 上界本身已证无 headroom（D018）。
- **不得用 C16 HOS 作 fallback 专家**：它是空间 2×2 非 FIR 的 task-mismatched 实现（D017 审计 5），不是合法能力对齐专家。
- **不得复用 seeds 71-80 作 held-out**：在 ≥6 批重复使用，已永久失去 held-out 资格（D017 审计 6）。
- **不得直接继承 e15ae60 的 5 条结论**（"5 轴穷尽"/"坍塌是信道本质属性"/"不可提取求逆信息"/"可写完整负面边界论文"/"model-based tracker 唯一剩余"）——全部 invalidated（D017）。
- **不得把 correlated-failure-mode 写成新机制贡献**：定性已知（Johnson 1998 / Qian 2002 / Kuncheva）。
- **不得为 ML 而 ML**：headroom < 阈值时停止 router 训练（frozen contract）。
- **不得删除 e15ae60 artifacts / 旧结论**：protected history，只追加 amendment/supersede/invalidate。

## 必读（≤8 个，按优先级）

1. `.sessions/2026-07-20-direction-lab-science-scout/S011-hybrid-routing-reconciliation-and-study.md`（本轮全部记录）
2. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 **D017 + D018**（核心裁决）
3. `.sessions/2026-07-20-direction-lab-science-scout/verifications.md` 的 **V006 + V007**（审计 + verifier）
4. `projects/thesis-fso/direction-lab/STATUS.v1.md`（一页式当前态）
5. `projects/thesis-fso/direction-lab/harvest/current.yaml` 的 **amended_2026_07_22** 段（当前有效 ceiling）
6. `.../hybrid-routing-scout-v1/synthesis.v1.md`（Macro A 结果 + 论文价值评估）
7. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（不变量 + 范围边界）

## 接口变更（如有代码改动）

- 新增 `hybrid-routing-scout-v1/src/dd_lms_equalizer.py`：legal cold-start DD-LMS 专家（`dd_lms_cold_start(rX, rY, *, n_tap=11, mu, block_size=64) -> {zX,zY,diverged,divergence_symbol,final_w_norm,...}`，已修 weight-norm L2 bug）。
- 新增 `hybrid-routing-scout-v1/src/run_macro_a_oracle.py`：Macro A runner（per-expert μ tuning on val seeds + oracle complementarity on test seeds）。
- 无对 common/ 或 params.py 的改动。无 protected history 改动。

## 失败数据附录

- Macro A（fresh seeds 121-130, 110 realizations）：macro PI-SER CMA=0.3972 / MMA=0.5031 / DD-LMS=0.4319 / oracle=0.2196。
- oracle selector all3 macro=0.3935 → headroom=**0.0037**（阈值 0.03 的 12%）。
- complementarity: MMA better 5.5%/worse 58%；DD-LMS better 21%/worse 35%；collapse 子集（n=61）MMA/DD-LMS 各仅 5/61 更好。
- 仅 2/110 realizations 有任何专家超 CMA >0.03。per-realization headroom median=0（76/110 exact tie），SE=0.00067。
- DD-LMS weight-norm bug 已修（旧 L1-of-magnitudes → L2）；test 数据 0 divergence，impact nil。
- tune_mu 单 seed（101）vs contract 承诺 5 seed：impact 0.00003，caveat 记录。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| tune_mu 单 seed | contract 承诺 [101-105] | 已记录，impact 0.00003 | 若重启专家路由用 5-seed |
| seeds 71-80 失效 | held-out 必须新鲜 | 永久失效 | 任何 confirmatory test 用新 seeds |
| C16 HOS 非法专家 | fallback 须能力对齐 | 标记 task-mismatched | 若用 HOS 须先建 FIR 版本 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（oracle=Kill bound / metric contract / protected history）
- [ ] 已验证 H011 至少 3 条关键事实：（1）headroom=0.0037（读 result.v1.json aggregate）；（2）seeds 121-130 disjoint（grep）；（3）DD-LMS 5/5 身份门（跑 test_hybrid_identity.py）
- [ ] 已检查 `_registry.yaml` 本专题 depends_on（governance-pilot / dual-pol-osl-groundwork）
- [ ] 已确认当前范围不含 formal promotion / push / protected history 改动

## 下一轮（唯一第一动作）

读 S011 + D017 + D018 后，向用户确认战略选择（无自动合法路径可推进）：
- **(a)** 投资 ~1 day 建 receiver-only model-based GG+SOP tracker（唯一剩余 positive-potential 维度，信道 MODEL 先验非 pilot/modulus）→ 若 Go，进新一轮 SCIENCE_SCOUT 或转 formal Groundwork。
- **(b)** harvest 收尾：把 D017/D018 负面 + LOCAL_SLICE Godard-collapse + C11/MMA/blind-affine 负面整理成可毕业的负面/boundary 论文材料，决定 thesis spine。
- **(c)** 改 formal goal/contribution line。

## 用户态度（verbatim，见 voice.md 2026-07-22）

- "本轮不是只写计划。请连续推进到混合均衡路线得到一个有证据的 A/B/C/D 裁决，并完成交接。"
- "不得直接继承 e15ae60 的以下结论：'五个机制轴已经穷尽'…"
- "oracle 只作 Kill/headroom bound，不能作 Go comparator。"
- "如果简单阈值已经达到 ceiling，记录'ML 无必要'，不要为了 ML 而 ML。"

## git 状态

- worktree: `.worktrees/direction-lab-capability-atlas` | branch: `codex/direction-lab-capability-atlas`
- 本轮起点 HEAD: e15ae60 | 本轮结束：未提交（待统一 consolidated commit）
- 未 push、未 merge。protected history（B001-B003/P03/canonical/旧 batch artifacts）全未改。