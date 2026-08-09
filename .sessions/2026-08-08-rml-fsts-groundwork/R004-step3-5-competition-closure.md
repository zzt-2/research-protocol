# [R004] RML-FSTS mandatory Step 3.5 竞争闭包

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
| R1 新增 should T006 | 2（ICAIT 2025、JLT 2021） | 1（Optics Communications 130981） | 两篇 qualified 均为 architecture adjacent；130981 的 STFT/window action `UNKNOWN` |

四篇本轮 qualified 新全文均记录 title/DOI/path/SHA/bytes/action/information source/granularity：

- Tang 2022：固定 `[A,B,A*,B*]` training block 做 frame localization→FOE；无 condition selector。
- WiSEE 2024：固定 header/pilot spacing 做 frame/CFO/equalization/CPE；损伤条件只作评测轴。
- ICAIT 2025：固定 training-spectrum coarse+fine FOE，training length 离线扫描后固定 960；无 lag/`B_L` action。
- JLT 2021：FO sweep+spectral correlation 做 OSNR/FOE，`ΔF/Th/q` 离线统一优化后固定；不是 time-lag family，也不是 conditioned lookup。

完整 identity/action 证据分别见 T004/T006 worker-log 与 receipts；两篇新增 IEEE read-notes 位于 `papers/_read_notes/10.1109_icait66450.2025.11353316.md`、`papers/_read_notes/10.1109_jlt.2021.3063251.md`。

### 竞争动作分类

| 类别 | 已确认对象 | 对 Q1 的影响 |
|---|---|---|
| exact action collision | **0（仅限 qualified fulltext evidence）** | 不能据此宣布 novelty；8 项关键全文债务仍可隐藏 collision |
| generic multi-lag prior art | Morelli 2009、Yu 2023；Dong 2009 仅 identity/abstract debt | 宽泛“multi-lag/weighted correlation”主张已被占用 |
| offline parameter optimization | Wang 2023、Enhanced 2024；JLT 2021 有固定参数离线优化子特征 | 只证明 fixed design/curve sweep，不等于 online condition controller |
| conditioned single-lag lookup equivalent | **0 confirmed** | 最强廉价替代仍必须保留；“未找到”不等于不存在 |
| architecture adjacent | Tang、WiSEE、ICAIT、JLT 2021；两篇 Optica 摘要级邻接 | TS/FFT/STFT/CPR/combining/phase correction 的信息源或动作对象不同 |

### 未关闭的一手证据债务

以下 8 项经过项目下载通道、官方 DOI/API、OpenAlex/Unpaywall 或 bounded author/institutional search 后仍无 qualified fulltext：Cheng 2020、OE.505931、OE.448956、Dong 2009、OE.561252、ACP/IPOC 10809664、SSRN 6293357、Optics Communications 130981。尤其 Cheng、ACP short-block、SSRN low-power 与 130981 的动作粒度不能由 metadata/abstract 诚实裁决；两篇 Optica虽摘要显示 CPR/branch-phase 邻接，也不能用摘要排除正文 lag/window 细节。

### Conditioned single-lag 廉价替代

dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 没有被 qualified fulltext 确认为已有等价实现，也没有被证明无效。它与“在线 receiver-visible reliability controller”必须继续分开：前者按开发集/粗 bin 冻结单一 lag，后者在运行时用 turbulence/branch/phase reliability 改变 lag/weight。二者的数值胜负、fixed-lag failure 与 headroom 仍属于 Step 4a；本轮不比较。

## 结论

canonical terminal = **证据阻塞**。

理由不是“搜不到所以新颖”，而是：已完成关键词矩阵、三类真实来源、Wang/Enhanced 双向引用链与三轮止损；qualified evidence 中未确认 exact collision 或 conditioned-lookup 等价，但 8 项关键一手全文仍不可得，且 R3 源限定补查超时达到轮次上限。因此竞争边界无法诚实闭合为“Q1 存活”，也没有证据支持“Q1 被碰撞/廉价方法关闭”。

Q1 保持 Step 3 的合法问题候选身份；**当前没有 Step 4a 入口**。下一合法动作只是在获得上述关键一手全文后做 action-level read/receipt，并重新裁决 Step 3.5；不得直接进入实验或方法设计。

## 对决策的影响

新建 D007：把 Step 3.5 终态登记为证据阻塞，保持 Q1 未被确认碰撞、也未完成 novelty closure；Step 4a 继续禁止，object/package failure 计数保持 `0/0`。
