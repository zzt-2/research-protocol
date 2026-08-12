# [R002] Step 1 检索回执

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D001

## 调研问题

Step 1 的 query、候选计数、来源、正式发表比例与 AI 语义初筛能否由 11 个原始 JSON 确定性复算，并满足质量门？

## 发现

### Query 矩阵

| Route / Round | Query | 返回 |
|---|---|---:|
| unwrap R1 | phase unwrapping error propagation cycle slip carrier phase estimation | 35 |
| unwrap R1 | multi hypothesis phase unwrapping MAP ML Wiener phase noise frequency offset | 45 |
| mixture R1 | Tikhonov mixture fixed lag sequence phase tracker pruning merging phase noise | 30 |
| unwrap R2 | coherent optical carrier phase recovery cycle slip mitigation low complexity pilot phase unwrapping | 27 |
| unwrap R2 | Joint ML MAP estimation frequency phase single sinusoid Wiener phase noise phase unwrapping | 26 |
| mixture R2 | Message Passing Algorithms Phase Noise Tracking Tikhonov Mixtures order 2 order 3 | 19 |
| optical R1 | coherent optical residual carrier frequency offset Wiener phase noise low complexity carrier phase estimation | 28 |
| optical R1 | coherent optical low complexity phase noise tracking fixed lag sequence phase estimator | 10 |
| optical R1 | free space optical coherent residual frequency offset phase noise cycle slip carrier recovery | 17 |
| optical R2 | inter-satellite coherent optical carrier phase recovery cycle slip pilot aided low complexity | 20 |
| optical R2 | coherent optical joint residual frequency offset phase noise estimation pilot Wiener 2020 2021 2022 2023 2024 | 21 |

### 确定性归并规则

1. 规范化 title：Unicode lowercase 后移除所有非字母/数字/下划线字符；按该键聚组。
2. priority 统一顺序：`MUST/必读 < SHOULD/建议读 < 待确认 < MAY < 备选 < BACKGROUND < 排除/DROP/EXCLUDE`；同标题组取最高优先级，最高优先级为排除才丢弃。
3. formal 身份：保留组内任一记录 `publication_status=published` 即计 formal；unknown 不单独计 formal。
4. must-read：保留组的最高优先级为 `MUST/必读` 即计一篇。
5. contributing source：只有对至少一个保留候选有实际结果的 `source_api` 才计贡献。

### 复算结果

- 11 JSON 合计 278 records；规范化 title 去重 242。
- 依上述最高 priority 规则保留 138 semantic candidates。
- 任一同身份记录确认 published 的 formal=98/138=`71.01%`；unknown 不计 formal。
- `MUST/必读` 归一后 12；三条技术路线均有 must/should 与 2019+ 正式 baseline。
- 实际贡献源：Semantic Scholar、OpenAlex、SerpAPI Scholar，共 3。arXiv 0 贡献；Exa 额度耗尽无贡献，不计来源门。
- 每个结果 JSON 的每条记录均含 `priority` 与 `priority_reason`；中英文标签来自两个独立 semantic worker，`relevance_score` 未作为分类替代。

### 结果文件

- `search-archive/2026-08-12/k2-unwrap-error-propagation-r1.json`
- `search-archive/2026-08-12/k2-unwrap-multihypothesis-r1.json`
- `search-archive/2026-08-12/k2-mixture-fixedlag-r1.json`
- `search-archive/2026-08-12/k2-unwrap-optical-cycle-slip-r2.json`
- `search-archive/2026-08-12/k2-unwrap-wang-directed-r2.json`
- `search-archive/2026-08-12/k2-mixture-tikhonov-directed-r2.json`
- `search-archive/2026-08-12/k2-optical-carrier-estimation.json`
- `search-archive/2026-08-12/k2-optical-fixed-lag.json`
- `search-archive/2026-08-12/k2-optical-fso-cycle-slip.json`
- `search-archive/2026-08-12/k2-optical-r2-intersatellite.json`
- `search-archive/2026-08-12/k2-optical-r2-joint-cfo-pn.json`

## 结论

检索质量门通过：242 unique≥20、3 contributing sources、98/138 formal=`71.01%`≥50%、12 must-read≥5、3 routes。Step 1 只基于 title/abstract/metadata 与已有本地一手锚；2024/2026 closest CPR 的动作仍须 Step 2/3 闭合。

## 对决策的影响

支持 D002 的 corpus 质量门，不支持 exact/non-exact novelty verdict。第一轮 verifier 对旧回执的 formal 合并口径给出 PARTIAL；本 R002 冻结确定性规则并取代旧无编号回执。
