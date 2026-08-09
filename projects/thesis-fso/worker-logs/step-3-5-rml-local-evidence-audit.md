# Step 3.5 RML-FSTS 本地证据与 exact-action 预筛

> 2026-08-09 | 执行 T002 | 只读本地预筛；未联网、未运行新搜索、未进入 Step 4a

## 扫描范围与确定性命中数

### 扫描范围

- 全局索引：`search-archive/_index/all-papers.jsonl`，共 **21,806** 个 JSONL 行，其中 `year>=2019` 为 **17,625** 行。
- 本专题检索材料：`search-archive/2026-08-08/rml-fsts-step1-q1..q7*.json`、canonical ledger、Step 2 acquisition receipt。
- 本地论文材料：`papers/doi/`、`papers/_read_notes/`；对已有全文不重新逐篇精读，仅使用现成 read-note/worker-log 的动作级提取。
- 既有 worker-log：只用于定位本地已有身份、动作提取和引用种子；oversampled-sync 的终判没有移植到本 Q1。
- 未读取或修改 `projects/simulation/explore/cma-fade-divergence/p05_run*.log`。

### 计数口径与结果

1. 对 2019+ 索引行以 `lag / multi-lag / correlation distance / correlation window / window length / stepwise / multi-pilot / adaptive / variable / optimal` 做宽召回，共 **105 个 raw keyword hits**；大量命中属于路由、天气雷达、测距、流量预测等不同任务。
2. 再要求 carrier/frame synchronization、FOE/CFO、training/preamble、coherent optical/FSO 等任务语义，并按 DOI→规范化标题去重、人工检查 title/abstract 后，得到 **10 个 2019+ DOI 候选身份**；另有 **1 条无 DOI/年份且标题—摘要错配的 unresolved record**。
3. 10 个 DOI 候选的预筛分类：
   - confirmed exact collision：**0**；
   - conditioned single-lag lookup 等价：**0**；
   - generic multi-lag / multi-block correlation：**2**（Yu；Electronics 2021）；
   - offline parameter optimization：**2**（Wang；Enhanced）；
   - fixed-training/direct-task、未见 condition→lag：**3**（Cheng；Tang；TTQP）；
   - architecture adjacent：**3**（OE.505931；OE.448956；WiSEE）。
4. 现成 frozen query 的确定性补充：route-A direct 与 conditioned 两个 JSON 都是 `total=0`；route-B conditioned 仅 2 条，其中 2021 UAV range-estimation 已在 receipt 中标“排除”，2008 MIMO multiple-offset 不满足 2019+ 与 multi-lag 语义。证据：`search-archive/2026-08-08/rml-fsts-step1-q4-route-a-direct.json:1-8`、`...q5-route-a-conditioned.json:1-8`、`...q7-route-b-conditioned.json:1-48`。

这里的“0 exact”只表示**当前本地可承重全文/read-note 没有确认 exact action**，不是 novelty 终判；metadata/abstract 不能用来排除尚未取得全文的动作。

## 五项债务状态表

| 对象 | identity | metadata | content path | SHA / bytes | provenance blocker 与可修证据 |
|---|---|---|---|---|---|
| Cheng 2020, `10.1016/J.OPTCOM.2020.126046` | **PASS（index/metadata 层）**：题名、DOI、2020、摘要一致；index 支持 low-OSNR joint frame/frequency sync | 当前 worktree `metadata.json` 为 `download_status=failed`、`download_method=all_failed`、`content_file=""` | 无正文；仅 `papers/doi/10.1016_j.optcom.2020.126046/metadata.json` | 无 | blocker=没有合法全文与 source provenance；旧 receipt 明确要求 lawful author/publisher PDF + `tools/convert`。证据：`search-archive/_index/all-papers.jsonl:10857`；metadata `:4-11`；`search-archive/2026-08-08/rml-fsts-step2-acquisition-receipt.json:49`。 |
| OE.505931, `10.1364/OE.505931` | **PASS（index/metadata 层）**：2023 Optics Express 身份一致 | `failed/all_failed`，空 `content_file` | 无正文；仅 `papers/doi/10.1364_oe.505931/metadata.json` | 无 | blocker=abstract 只支持 CV-DD-LMS diversity combining+CPR，且无全文；不能据此判 lag action。可修证据是合法 Optica/author-copy PDF + source receipt。证据：`search-archive/_index/all-papers.jsonl:10853`；metadata `:4-11`；acquisition receipt `:52`。 |
| OE.448956, `10.1364/OE.448956` | **PASS（index/metadata 层）**：2022 Optics Express 身份一致 | `failed/all_failed`，空 `content_file` | 无正文；仅 `papers/doi/10.1364_oe.448956/metadata.json` | 无 | blocker=abstract 只支持 optimal branch block phase correction，且无全文；不能把 branch condition 邻接当 lag controller。可修证据同上。证据：`search-archive/_index/all-papers.jsonl:16291`；metadata `:4-11`；acquisition receipt `:53`。 |
| Tang 2022, `10.1109/JPHOT.2022.3161795` | **PASS（文件/receipt 层）**：title/DOI 与正文 identity 已检查 | metadata 仍为 `failed/all_failed`，空 `content_file`，与磁盘 PDF/content 冲突 | `papers/doi/10.1109_jphot.2022.3161795/content.md` 与 `source.pdf` 均存在 | content=`DB526B...FB69`, **36,071 B**；source=`E7D281...D1CE`, **2,413,149 B**；本轮重算与旧 receipt 一致 | blocker=下载来源链没有被 metadata/receipt 合法闭合，未修前不得承重；可修证据是现存 PDF magic/hash、content title/DOI/119 effective lines、index DOI identity，再写保留旧失败状态的新 provenance receipt。证据：metadata `:4-11`；acquisition receipt `:45`。 |
| WiSEE 2024, `10.1109/WiSEE61249.2024.10850117` | **PASS（旧 receipt/index 层）**：2024 conference identity 与 abstract 一致 | 旧 receipt 记录 metadata=`failed/all_failed`；当前 worktree 内 canonical 目录缺失，不能在本轮独立复核 metadata | receipt 指向主仓 `D:/code/study/research-protocol/papers/doi/10.1109_wisee61249.2024.10850117/content.md`；**不在当前 worktree** | receipt：content=`214343...14E`, **35,131 B**, 112 effective lines；source=`87222B...40CE`, **1,185,870 B** | blocker=“PDF/content 存在”与失败 metadata 的来源链矛盾，且当前 worktree 无文件；未修前不得承重。可修证据是回到 receipt 指向的 canonical 文件核验 PDF/content/hash/title/DOI 并补新 provenance receipt，不静默改旧 receipt。证据：`search-archive/_index/all-papers.jsonl:11554`；acquisition receipt `:46`。 |

## 候选动作分类表

Evidence level：`FT-note`=已有全文精读提取；`FT-blocked`=正文存在但 provenance 禁止承重；`ABS`=title/abstract/metadata 召回；`META`=仅身份 metadata。

| title / DOI / year | evidence level | action | information source | granularity | classification | exact? | evidence pointer |
|---|---|---|---|---|---|---|---|
| Carrier FOE Scheme Based on FSTS / `10.1109/JPHOT.2023.3265847` / 2023 | FT-note | 固定 FSTS，coarse+fine FOE；`B_L/B_N` 由 modulation/TS 设置与离线扫描给定 | 已知 FSTS、接收复样值、双偏振/分支信息 | 每帧执行固定计算图；参数按实验/设计冻结 | **offline parameter optimization / source baseline** | **否**：无 receiver condition→在线/分区 lag 选择 | `papers/_read_notes/10.1109_jphot.2023.3265847.md:10-19,93-94` |
| Enhanced Frame Synchronization and Carrier Recovery / `10.1364/OE.520452` / 2024 | FT-note | mixed TS、FS、两级 FOE；扫描 QPSK 总长与内部 block length 后使用固定工作点 | PRBS/QPSK TS、接收 samples、双偏振 | 每帧固定链；长度离线确定 | **offline parameter optimization** | **否**：read-note 明示无 conditioned single-lag lookup/lag-ranking experiment | `papers/_read_notes/10.1364_oe.520452.md:10-19,93-104` |
| Joint Physical Layer Frame Optimization and Carrier Synchronization / `10.1109/TVT.2022.3218937` / 2023（online 2022） | FT-note | 固定 stepwise `AC1→AC2→multi-block CC` residual refinements；frame geometry 另行离线优化 | 已知 pilots、AC/CC statistics | 每帧执行固定多 separation 计算图 | **generic multi-lag / stepwise correlation** | **否**：无 condition-dependent lag ranking 或 conditioned lookup | `papers/_read_notes/10.1109_tvt.2022.3218937.md:179-193` |
| An Efficient Carrier Synchronization Scheme for Demodulation Systems / `10.3390/electronics10232942` / 2021 | ABS | RLR CFR + PA CPR；multi-pilot-block autocorrelation values superimposed | pilot blocks、received samples | per-frame fixed/reconfigurable estimator；condition→lag rule 未见 | **generic multi-block correlation**（全文待裁） | **未证实** | `search-archive/_index/all-papers.jsonl:19109` |
| Training-Aided Joint Frame and Frequency Synchronization...Low OSNR / `10.1016/J.OPTCOM.2020.126046` / 2020 | ABS+META | low-OSNR joint FFS；摘要只支持 noise-tolerant joint frame/CFO | training sequence、low-OSNR received signal | per-frame；lag/window/`B_L` 机制未知 | **fixed-training/direct-task，lag status unresolved** | **未证实**，需全文 | `search-archive/_index/all-papers.jsonl:10857`; metadata `papers/doi/10.1016_j.optcom.2020.126046/metadata.json:4-11` |
| Symmetric Training Sequence-Based FOE / `10.1109/JPHOT.2022.3161795` / 2022 | FT-blocked | STSB frame temporal-position identification + FOE；已有 read-note 指向固定训练链 | symmetric TS、received samples | per-frame fixed training action | **fixed-training/direct-task** | **不得终判**：provenance 未修；现有抽取未显示 condition→lag | `search-archive/2026-08-08/rml-fsts-step2-acquisition-receipt.json:45`; `papers/_read_notes/10.1109_jphot.2022.3161795.md:123-133` |
| Low Complexity Parallel FOE Based on TTQP / `10.3390/photonics11090885` / 2024 | ABS | time-tagged QPSK partition + modified Mth-power parallel FOE | signal-point time tags、received samples | per-frame fixed FOE | **fixed-training/direct-task / architecture adjacent** | **未证实**；abstract 无 lag selection | `search-archive/_index/all-papers.jsonl:10850` |
| Real-Time Low-Complexity Diversity Combining... / `10.1364/OE.505931` / 2023 | ABS+META | CV-DD-LMS 同时做 diversity combining 与 CPR | decision-directed error、多支路 samples | online adaptive weights（但动作是 combining/CPR） | **architecture adjacent** | **否于摘要层的动作对象**：不是 lag/`B_L` selector；全文仍缺 | `search-archive/_index/all-papers.jsonl:10853`; metadata `papers/doi/10.1364_oe.505931/metadata.json:4-11` |
| Spatial Diversity...Optimal Branch Block Phase Correction / `10.1364/OE.448956` / 2022 | ABS+META | branch block phase correction | branch relative phase / received blocks | block-level phase correction | **architecture adjacent** | **否于摘要层的动作对象**：修 phase，不选 lag | `search-archive/_index/all-papers.jsonl:16291`; metadata `papers/doi/10.1364_oe.448956/metadata.json:4-11` |
| Data-Aided Multi-Format DSP... / `10.1109/WiSEE61249.2024.10850117` / 2024 | ABS + provenance-blocked receipt | custom multi-format data-aided equalizer，支持 spatial diversity/post-DSP combining | training/data-aided equalizer inputs | equalizer update granularity；当前证据不足以细化 | **architecture adjacent** | **不得终判**；abstract 无 lag/`B_L` selector | `search-archive/_index/all-papers.jsonl:11554`; acquisition receipt `:46` |
| *Joint frame synchronization and frequency offset estimation...under low received optical power* / DOI/year unknown | corrupted local record | 题名看似 condition-specific joint FS+FOE，但记录 abstract 实为通用 FSO survey | 不可确定 | 不可确定 | **identity/content collision；不计 2019+ DOI 候选** | **不可判** | `search-archive/2026-08-08/rml-fsts-step1-q1-fixed-lag.json:113-129`; canonical ledger `:294-311` |

### 历史但非 2019+ 的必要去重边界

Morelli 2009 已有固定多 lag、相关幅度/lag 几何加权的 closed-form residual CFO refinement；它不满足 2019+ recent baseline，但会占用“generic weighted multi-lag fusion”这一宽泛主张。证据：`papers/_read_notes/10.1155_2009_821819.md:89-101,120-125`。Dong 2009 `10.1109/CHINACOM.2009.5339877` 仍只有 exact-title identity、无全文，不能动作终判（acquisition receipt `:50`）。

## Wang/Enhanced backward seeds

### Wang 2023

Wang 的当前 canonical HTML 在 References 处明确 unavailable，因此只能把**编号+正文赋予的角色**交给 citation-chain 子任务，不补造身份：

- `[10]` time-domain 4th-power FOE；`[11]` QPSK-partition FOE；`[15]` 4th-FFT；`[18]` conventional TS-based FOE；`[19]` TS-based joint frame/frequency synchronization；`[22]` Park timing metric；`[23]` turbulence slow-variation / diversity-branch phase correction。证据：`projects/thesis-fso/worker-logs/step-3-rml-fsts-l01-reader.md:335-346`。
- 可确定性对齐的直接种子只有 `[19]` Cheng 2020（DOI `10.1016/J.OPTCOM.2020.126046`，由 Enhanced references/index 交叉身份）与 `[22]` Park et al. 2003；其余保持 `IDENTITY_PENDING`。Wang reader 对 reference unavailability 的证据边界见 `...l01-reader.md:111-113,337`。

### Enhanced 2024

Enhanced reader 已从正文 references 提取出可直接进入 backward-chain 的种子：

1. Schmidl & Cox 1997（Ref.9）；Minn/Zeng/Bhargava 2000（Ref.10）；Park et al. 2003（Ref.11）；Ren et al. 2005（Ref.13）——基础 timing/preamble lineage。
2. Cheng et al. 2020，low-OSNR training-aided joint frame/frequency synchronization（Ref.19，DOI `10.1016/J.OPTCOM.2020.126046`）——直接 task seed。
3. Wu et al. 2022，QPSK-TS joint OSNR/FO monitoring（Ref.21）——直接 FOE/training seed，当前本地仅角色/作者年份，完整 DOI/title 仍需 citation-chain identity closure。
4. Wang et al. 2023 FSTS（Ref.24，DOI `10.1109/JPHOT.2023.3265847`）——已知 anchor lineage，不应作为“新 competitor”重复计数。

证据：`projects/thesis-fso/worker-logs/step-3-rml-fsts-l02-reader.md:268-276`。其中 Cheng、Wu、Park 是本 Q1 最直接的 backward seeds；基础 OFDM timing 文献只作 lineage，不自动升级为 lag-controller competitor。

## 对关键词矩阵的去重建议

这里只指出现有覆盖与重复，不新增 query 或方法论：

1. `q1 fixed-lag` 已覆盖 Wang、Tang、TTQP 与“低接收功率”错配记录；后续相同 title/DOI 应复用 canonical identity key，不重复计候选。
2. `q2 multi-lag` 已覆盖 Dong 2009 标题与大量跨域噪声；Morelli 2009/Yu 2023 已有全文 read-note，重复命中应直接落入 historical/generic prior-art bucket。
3. `q3 FSO-transfer` 已覆盖 Enhanced、OE.505931、OE.448956、WiSEE、TTQP；这些条目再次因 turbulence/diversity/low-SNR 命中时，应按 DOI 去重并保留 architecture-adjacent 标签。
4. `q4/q5` 现有归档均 `total=0`；`q7` 两条均已排除。它们只能证明 frozen query 的本轮召回事实，不能证明领域无 exact action。
5. Cheng 在 Wang baseline、Enhanced Ref.19、旧 sync search 和 all-papers 中重复出现，应合并为 DOI `10.1016/j.optcom.2020.126046` 一个 identity；Tang/WiSEE 应按 DOI 合并“index identity”和“provenance debt”，不能把正文存在与 metadata 失败拆成两篇。
6. “Joint frame synchronization...under low received optical power”必须保留 alias collision key `alias:satellite-low-power-title-collision`，在身份修复前不得与 TTQP、Wang 或其他 Wang-group 条目按标题联想合并。

## 结论边界

- 本地可确认：已有 fixed/offline `B_L`/block-length tuning、固定 stepwise multi-separation correlation、固定 multi-block correlation，以及若干 condition-source/CPR/combining 邻接动作。
- 本地**没有可承重证据确认** receiver-visible condition → 在线/分区选择 lag、`B_L` 或 correlation distance，并输出 condition-to-lag rule/curve family；也没有确认 dev-frozen conditioned single-lag lookup 的文献等价实现。
- Cheng、两篇 Optica 缺全文；Tang/WiSEE provenance 未修；标题—摘要错配条目身份未闭合。因此本报告只交付 candidate list 与证据债务，不作 Step 3.5 terminal、novelty、Go/Kill、数值胜负或 Step 4a 声称。
