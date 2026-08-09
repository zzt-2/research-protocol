# [R004] RML-FSTS mandatory Step 3.5 竞争闭包

> **D008 主控接收修订**：本报告的检索、引用链、qualified-fulltext 分类与三轮止损事实保留；“8 项关键全文全部不可得 → `EVIDENCE_BLOCKED` / Step 4a NO ENTRY”被撤回。共享 canonical 已存在 Optics Communications 130981 全文，且余下缺件并非同等强度的 exact-action blocker。当前终态见 D008/V005/H005。

> 2026-08-09 | 关联：2026-08-08-rml-fsts-groundwork / D006-D007

## 调研问题

2019 年至今的 FSTS、training-aided FOE、multi-lag CFO estimation 与 coherent-FSO carrier recovery 文献，是否已经实现或实质吸收 Q1 的 exact action：receiver-visible condition → 在线/分区选择 lag、`B_L`、correlation distance，或 condition-aware multi-lag weighting？最强廉价替代 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 是否已有文献等价实现？

## 发现

### 检索矩阵、来源与引用链

- R1 按 4 个方法变体 × 2 个场景/条件组执行 **8/8 query**，得到 27 条；实际 retained source family 为 SerpAPI、OpenAlex、Semantic Scholar 三类。原始路径与 SHA256 见 `search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json`。
- Wang 2023 与 Enhanced 2024 均完成 forward/backward citation chain：四链 63 条，跨链按 DOI/title 去重为 51 条，全部筛查；OpenAlex 为严格主链，`S2-only=0`。
- R1 新增 must/should=`3/3`，因此未停。R2 用新术语跑 4 个冻结 query：Q1-Q3 共 63 条，known hit 15 次、48 个新标题全部排除，new must/should=`0/0`；Q4 在 120 s 超时，不能记为 0。R3 仅用 S2+OpenAlex 重试 Q4，仍在 120 s 超时；`round_limit_reached=true`，禁止 R4。
- 因 R2/R3 的 Q4 超时，检索轮次按三轮上限合法停止，但不能声称“最后一轮完整收敛”。

### Fulltext/provenance 结果

| 组别 | qualified fulltext | unavailable / unresolved | 动作级结论 |
|---|---:|---:|---|
| 旧直接债务 T004/T007 | 2（Tang 2022、WiSEE 2024） | 4（Cheng 2020、OE.505931、OE.448956、Dong 2009） | Tang/WiSEE 均为固定 training/header DSP；无 condition→lag/`B_L` |
| R1 新增 must T005 | 0 | 3（OE.561252、ACP/IPOC 10809664、SSRN 6293357） | 三篇 exact/cheap-lookup 均 `UNKNOWN`，不能用标题/摘要排除或确认 |
| R1 新增 should T006 | 3（ICAIT 2025、JLT 2021、Optics Communications 130981） | 0 | 三篇均为 architecture adjacent；130981 共享 canonical 全文证明固定 STFT/FFT 参数与评测轴，不含 condition→lag/`B_L`/window 选择 |

五篇本轮 qualified 新全文均记录 title/DOI/path/SHA/bytes/action/information source/granularity：

- Tang 2022：固定 `[A,B,A*,B*]` training block 做 frame localization→FOE；无 condition selector。
- WiSEE 2024：固定 header/pilot spacing 做 frame/CFO/equalization/CPE；损伤条件只作评测轴。
- ICAIT 2025：固定 training-spectrum coarse+fine FOE，training length 离线扫描后固定 960；无 lag/`B_L` action。
- JLT 2021：FO sweep+spectral correlation 做 OSNR/FOE，`ΔF/Th/q` 离线统一优化后固定；不是 time-lag family，也不是 conditioned lookup。
- Optics Communications 2024（130981）：固定分块 FFT、1024×16-point mean spectrum、正负谱功率比与星历辅助；received power/FFT points 仅为评测或离线设计轴，非 runtime condition→lag/`B_L`/window selector。

完整 identity/action 证据分别见 T004/T006 worker-log 与 receipts；两篇新增 IEEE read-notes 位于 `papers/_read_notes/10.1109_icait66450.2025.11353316.md`、`papers/_read_notes/10.1109_jlt.2021.3063251.md`。

### 竞争动作分类

| 类别 | 已确认对象 | 对 Q1 的影响 |
|---|---|---|
| exact action collision | **0（仅限 qualified fulltext evidence）** | 不能据此宣布 novelty；执行阶段所列 8 项已由 D008 重分层，仅 SSRN 6293357 保留为高风险 action-level UNKNOWN |
| generic multi-lag prior art | Morelli 2009、Yu 2023；Dong 2009 仅 identity/abstract debt | 宽泛“multi-lag/weighted correlation”主张已被占用 |
| offline parameter optimization | Wang 2023、Enhanced 2024；JLT 2021 有固定参数离线优化子特征 | 只证明 fixed design/curve sweep，不等于 online condition controller |
| conditioned single-lag lookup equivalent | **0 confirmed** | 最强廉价替代仍必须保留；“未找到”不等于不存在 |
| architecture adjacent | Tang、WiSEE、ICAIT、JLT 2021；两篇 Optica 摘要级邻接 | TS/FFT/STFT/CPR/combining/phase correction 的信息源或动作对象不同 |

### 未关闭的一手证据债务

执行阶段把 8 项统一列为缺全文债务，其中 Optics Communications 130981 是 stale false negative：完整 PDF/content 早已位于共享 canonical，PDF SHA256=`2a5728193de8fac0ffbd1c55f60847fe44b9d462c70e13c8325c798c84feefc2`，content SHA256=`67fa0ea9f1c8b8c37b48bc87474c4a7d7b565b2ebe3f0c12b44cca9d8aa66ecb`。正文显示固定分块 FFT、1024×16-point mean spectrum、正负谱功率比与星历辅助；received power/FFT points 是评测或离线选择轴，不是运行时 condition→lag/`B_L`/window 选择。

余下 7 项分层为：SSRN 6293357 是唯一高风险 action-level UNKNOWN；ACP/IPOC 10809664 是次级直接 comparator 债；Cheng 2020、OE.561252 是高相关任务/条件邻近但现有摘要不支持 exact action；OE.505931、OE.448956 与 Dong 2009 分别属于 diversity/phase-correction 邻接和历史 generic multi-lag 边界。缺全文限制 novelty/首次措辞，但不构成 blanket Step 4a blocker。

### Conditioned single-lag 廉价替代

dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 没有被 qualified fulltext 确认为已有等价实现，也没有被证明无效。它与“在线 receiver-visible reliability controller”必须继续分开：前者按开发集/粗 bin 冻结单一 lag，后者在运行时用 turbulence/branch/phase reliability 改变 lag/weight。二者的数值胜负、fixed-lag failure 与 headroom 仍属于 Step 4a；本轮不比较。

## 结论

执行阶段 terminal=`证据阻塞` 已由 D008 撤回。修订后的 Step 3.5 terminal 为 **`STEP3_5_COMPLETE_Q1_PROVISIONAL_SURVIVOR_WITH_FULLTEXT_LIMITATIONS`**。

理由是：关键词矩阵、三类真实来源、Wang/Enhanced 双向引用链与三轮止损已经满足 `gw-supplement.md` 的停止规则；qualified evidence 未确认 exact collision 或 conditioned-lookup 等价；R2 三个完成 query 新 must/should=`0/0`。Q4/R3 timeout 继续作为 coverage caveat，不能算零结果，也不能反向当作碰撞存在。

Q1 作为 provisional survivor 获得 Step 4a 讨论入口；这不等于首次、新颖性闭合、target defect 已证或方法成立。Step 4a 必须保留 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 作为最强廉价 comparator。SSRN/ACP及其他缺件获得后仍需回填 action-level 边界，但不再作为启动 Step 4a 的先决条件。

## 对决策的影响

D007 的检索事实保留、terminal 被 D008 取代。object/package failure 计数保持 `0/0`；下一合法动作是用户授权后新对话只执行 Step 4a feasibility，不在本轮运行。
