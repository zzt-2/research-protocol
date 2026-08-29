# Ch5 Q-C5-1 GW Step 3.5 exact-recipe closure

> T049｜2026-08-30｜只完成 Q-C5-1 Step 3.5；未进入 Step 4a、实现、实验或论文正文。
> 控制校验：`validate_task_control.py` = `PASS`（epoch 4 / CP004 / `TARGETED_SUPPLEMENT_SEARCH`）。

## 1. 固定目标与 collision 门

目标完整 recipe 为：

`已知 APSK ring/angle + 当前/过去 pilot residual`
`→ radial/tangential covariance parameterization`
`→ 同环点/跨偏振统计强度 shrinkage pooling`
`→ positive-definite structured covariance`
`→ Mahalanobis/log-det bit LLR`。

只有 receiver-visible input、pilot-only causal sample budget、structured estimator、pooling/shrinkage action 和 APSK LLR output 全部相同才记 `EXACT_RECIPE_COLLISION`。Mahalanobis、full covariance、generic shrinkage、polar noise 或其他场景的单原子重合只记邻居。

## 2. 轮次、计数与收敛

| 轮次 | 动作 | raw / unique | 新增 MUST | 新增 SHOULD | 终态 |
|---|---|---:|---:|---:|---|
| Round 1 | 预注册 6/6 query matrix | 28 / 25（跨 query） | 0 | 2 | 两个摘要级邻居进入 action 筛查 |
| Round 2 | Layton 2018 双向 citation-chain + alias/action 筛查 | forward 1 + backward 37 | 0 | 0 | 收敛 |
| Round 3 | 未启动 | 0 / 0 | 0 | 0 | Round 2 已满足 zero-new stop |

两轮合计 66 archive rows，按 DOI、否则按题名跨 archive 去重为 63 条。receipt 与 8 个 archive 的 SHA-256 见 `search-archive/2026-08-30/t049-ch5-structured-covariance-step3-5-receipt.json`。

## 3. exact-action ledger

| 对象与证据层 | receiver-visible input | estimator/action | pooling / PD | output | verdict |
|---|---|---|---|---|---|
| Layton et al. 2018，既有全文 | 已知 pilot labels 与每点接收样本；亦讨论 blind GMM | 每星座点独立 sample mean + unstructured full 2×2 covariance | 仅一般建议跨 frame 或 biased shrinkage；没有 APSK 几何/跨偏振 pooling，也未给目标结构化 PD recipe | Mahalanobis + determinant-normalized bit LLR | `STRONG_PRIMITIVE_COLLISION`；最强邻居，非完整 recipe collision |
| Schäfer–Strimmer 2005，Layton backward reference/摘要 | 通用小样本高维数据 | analytic covariance shrinkage | 正定/良态 covariance 是其核心 | 无通信 demapper/LLR | `PRIMITIVE_COLLISION`（generic shrinkage/PD） |
| Bello et al. 2024，Round 1 摘要 | DFT-s-OFDM、Gaussian phase-noise model | model-derived polar detector | 无 pilot-residual covariance shrinkage/pooling | detector metric；非 APSK structured-covariance LLR recipe | `STRONG_NEIGHBOR`（polar likelihood，任务不匹配） |
| *Orbital Detection* 2026，Round 1 摘要 | MIMO message-passing beliefs + constellation ring prior | radial discrete / phase-continuous orbital denoisers | 无 pilot covariance estimator 或 shrinkage pooling | posterior denoiser/detector | `STRONG_NEIGHBOR`（ring-aware primitive，动作不匹配） |
| Xie et al. 2012，Layton backward reference/摘要 | APSK/product-label received symbols | low-complexity simplified soft demapper | 无 data-dependent covariance 或 pooling | APSK soft metric | `STRONG_NEIGHBOR`（APSK demapping primitive） |
| Dzieciol et al. 2020，Layton forward citation/摘要 | optical-fiber phase-noise samples | geometric shaping with mismatched channel model | 无 pilot-limited structured covariance estimator | GMI / post-FEC BER | `NEIGHBOR_ONLY`；不是 estimator recipe |

Layton 全文的承重指针为 `papers/doi/10.1186_s13638-018-1136-z/content.md:115`（covariance LLR）、`:139`–`:151`（pilot sample covariance、低 pilot shrinkage 建议、blind GMM）、`:269`–`:283`（pilot sweep）及 `papers/_read_notes/10.1186_s13638-018-1136-z.md`。这些证据确认“full covariance + Mahalanobis/log-det”原子已碰撞，也确认目标的 radial/tangential parameterization 与跨环/跨偏振 pooling 未由该文给出。

## 4. fulltext / abstract 边界

- **全文级**：仅复用已取得并已精读的 Layton 2018；它是唯一同时接近 estimator input、covariance action 与 LLR output 的对象。
- **摘要级**：本轮新增对象均在摘要已显示任务或核心动作不匹配；摘要只用于排除其成为“已确认完整碰撞”，不用于声称领域不存在同 recipe。
- **新全文 0 篇 / 新 read note 0 篇**：没有新增对象达到“可能同完整 recipe”的下载门，故依 brief 不为一般邻居扩大 acquisition。
- **工具覆盖限制**：OpenAlex 提供主要召回；Semantic Scholar 参与 forward citation union，但多次 rate-limit；SerpAPI/Exa 无 key。此限制禁止“首次”“SOTA”或领域穷尽性声称。

## 5. 裁决

**`Q-C5-1 SURVIVES`**。

在本次 bounded 6-query + Layton 双向引用链切片中，未确认同时满足以下五项的已发表 recipe：

1. APSK ring/angle 与 current/past pilot residual；
2. pilot-only causal sample budget；
3. radial/tangential structured covariance estimator；
4. 同环点/跨偏振 shrinkage pooling 并输出正定 covariance；
5. Mahalanobis/log-det APSK bit LLR。

最强邻居仍是 Layton 2018：它完整占用 full-covariance likelihood 原子，并提到 generic shrinkage，因此目标不得声称 covariance demapping、Mahalanobis/log-det 或 shrinkage 原子首次；可保留的最窄差别仅是 **pilot-limited APSK 几何结构化 estimator + matched-budget pooling recipe**。

本 verdict 只保留 Step 4a 的讨论入口，不是 Go、方法信号或科学可行性证明，也不授权自动进入 Step 4a。

## 6. blocker

- Step 3.5 内唯一 blocker：`NONE`。
- claim blocker：外部召回受 SerpAPI/Exa 无 key和 S2 限速影响，不能做首次/SOTA/穷尽性声称；该限制不构成 D032 完整 recipe 碰撞。
