# [S002] Step 1 限定完整性修复（Phase A）+ Step 2 acquisition（Phase B）

> 2026-08-02 | 阶段: Groundwork Step 1 修复 → Step 2 | 状态: Phase A 完成（D002/V002 PASS）+ Phase B 完成（Step 2 PASS，6 篇合格 content.md，待用户验收覆盖面）

## 目标

一个对话内完成：Phase A（Step 1 科学完整性限定修复：计数重算 / title-abstract identity 审计 / 候选族修订 / provenance receipt / 治理修正），Phase A PASS 后立即 Phase B（Step 2 全文获取：4 批身份清洗→直接竞品→最强 comparator→邻近边界，3 轮下载止损，≥5 篇合格 content.md 或停在 STEP2_BLOCKED）。

## 记录

### Phase A — Step 1 限定完整性修复（已完成）

#### A1 重新计算检索事实（确定性，`tools/amc_step1_recompute.py`）

从 raw JSON 重算（排除 alias repair 文件，alias 单独记）：

| 指标 | 原口径（R001/S001/V001） | 真值（重算） |
|---|---|---|
| raw JSON 文件 | "16 queries" / manifest 32 file | **32 文件 = 17 unique query**（每个 query 双存：slug-archived + named-output，内容相同） |
| 非零结果 query | — | **16**（1 个 query "mcs-fer-goodput-coherent" openalex+arxiv 返 0，双存为 2 个 240B json） |
| requested source union | "5 sources" | **4 API**：openalex/exa/serpapi/arxiv（arxiv 被 request 2 次返 0） |
| result-bearing source（result-level source_api） | 混入 "5 sources" | **openalex(286) / serpapi_scholar(124) / cnki(38)** + 2 条 openalex+openalex。exa 在 171 条 source_set 出现但 result-level 未单独打标（wrapper provenance 漏洞）。故真值=4 数据通道产结果（含 cnki），非"5" |
| unique candidates | 209 | **209**（_alldigest.json，不变） |
| published | manifest 153(73%) / R001 115(55%) | **115/209 = 55.0%**（manifest 153 是 r1-digest 重复计数；_alldigest 真值 115） |
| priority 分布 | 必读10/建议读17/待确认4/备选57/排除121 | **同**（从 R001 triage 行重解析一致） |
| 0-byte 文件 | "1 个 0-byte CNKI 文件" | **纠正**：唯一 0-byte 是 `_cnki-r2-linkadapt.txt`（辅助 .txt，非 CNKI .json）；2 个 240B json 是合法空结果 query |

#### A2 title-abstract identity 审计（`_alldigest.json` normalized-abstract 分组）

6 个 normalized-abstract 重复组（len≥40）覆盖 **18 条 hit**。根因：**Exa/SerpAPI abstract 抓取污染**——少数通用 survey 摘要被反复注入不同标题条目。

| 组 | 摘要类型 | 条目数 | 受影响 shortlist/flagged |
|---|---|---|---|
| 1 | OWC-survey（"optical wireless communication refers to…"） | 7 | **L020 / L038 / L090**（+ L064/L127/L134/L091） |
| 2 | SATCOM-survey | 3 | — |
| 3 | ISAC-survey | 2 | — |
| 4 | FSO-enabling-tech-survey | 2 | L135/L176（dup fam） |
| 5 | 6G-roadmap（"6G and beyond will fulfill…"） | 2 | **L124**（+ L005） |
| 6 | IRS-survey | 2 | — |

**L124 官方身份**（Semantic Scholar + Crossref 双源，OpenAlex 429 不可用）：
- Optics Express **34(14):26128**, 2026, **DOI 10.1364/oe.595557**，作者 Xiao/Li/Liu/Zhang/Zhang/Xie。
- 真实 abstract（Crossref）："Coherent FSO suffer from coupled amplitude fading and phase distortion. Conventional **AMC** relying solely on SNR cannot capture phase dynamics…**physics-informed AMC framework** that extracts scintillation index σ²I and phase variance σ²ϕ from pilots…modulation selection…"——**是真实的 coherent-FSO AMC 论文，AMC action 真实**（modulation selection driven by [SNR, scintillation index, phase variance]）。
- 本地 abstract 是 6G-roadmap（与 L005 同），错配确认。
- pre-fix 状态 `UNVERIFIED_BIBLIOGRAPHIC_HIT`（身份 bibliographic 级闭合，全文 coding/CSI/channel/scenario 待 Step 2）。
- abstract 未提 Gamma-Gamma/satellite，是 terrestrial coherent FSO 取向。

#### A3 修订候选地图（4 族 → 3 族 A/B/C）

**关键修订**：原 F4（相干物理信息 AMC，锚 L124）**不再算机制不同的第 4 族**——L124 官方身份确认它是真实的 coherent-FSO AMC（A 族的一个相干相位实例），不是独立机制族。

1. **A_MCS_POWER_CONTROL** = instantaneous-CSI 分支（原 F3）+ delayed/statistical/uncertain-CSI 分支（原 F1）合并，因真实 action 相同（调制阶数/码率/功率切换）。
2. **B_HARQ_IR_RATE_ADAPTATION** = 原 F2，真实独立 action（IR-HARQ 重传+速率+功率），文献密集，当前更像 ENGINEERING_COMPONENT 候选。
3. **C_COHERENT_TX_ADAPTATION_UNVERIFIED** = 原 F4（L124 + L165），L124 全文身份闭合前不算正式候选族。

**必须纠正（D002）**：
- F1 headroom：**并非完全避开** dead-end#3 的 0.09 dB MCS 天花板；与旧路线共享长时间尺度信息驱动 MCS/码率切换，新增点只是"不确定信息约束"，headroom **未证**，须 Step 4a 维度 D oracle 上界核算。
- "直接竞品 0 篇确认"→ `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`。
- L038 标签 `chinese-FSO-AMC` 错误（英文标题 + T&F DOI 10.1080/24751839.2026.2637258）→ 应标 `IM/DD-FSO-AMC`，abstract 同样污染。
- L070 文字声称属"mod-classification 排除"但 pri=备选（未排除）→ 文字改为"borderline demod/AI-mod survey，pri=备选（保留观察）"与 pri 一致。

**Alias collision query（≤4，bounded Step 1 修复，不扩成新地勘）**：
| query | 命中 | 直接竞品 |
|---|---|---|
| coherent FSO ACM ModCod satellite | 9 | 0（EHF/RF-sat survey；near-miss L003 EHF-FSO 2018 survey） |
| optical feeder link variable-rate FEC | 7 | 0（全 RF，无光学） |
| FSO rate-compatible LDPC puncturing | 1 | 0（off-topic URLLC review） |
| satellite optical DVB-S2X ACM | 15 | 0（RF Q/V/Ka-band） |

共 32 命中，**0 直接竞品**。覆盖 caveat：Exa 402 透支 + OpenAlex 0 + S2 限速，仅 SerpAPI Scholar live。near-miss L003（Softwarization/Virtualization EHF-FSO 2018）待 Step 2 评估。

#### A4 持久 provenance receipt

`search-archive/2026-08-02/_step1_receipt.json`（23KB，json parse OK，需 `git add -f`）。含：search_facts（17 query/16 非零/published 115(55%)/source 口径纠正）/ duplicate_abstract_groups（6 组 18 条）/ alias_collision_repair（4 query SHA256）/ l124_identity_resolution（Optics Express 官方身份）/ shortlist_provenance（12 篇 DOI/URL）/ raw_file_hashes（32 原始文件 SHA256，全 MATCH）/ replay（确定性重放命令）。

#### A5 治理修正

- Step 1 状态：`STEP1_DONE` → `STEP1_ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR`。
- D002（候选族修订 + identity 审计 + receipt 血缘）+ V002（修复验证 PASS）写入；保留 V001 并明确其漏审（identity + source provenance）。
- topic-index 更新：GW Progress commit 字段 / 候选族 4→3 / source 口径 / L124 身份 / "直接竞品"措辞 / 范围变更记录（D002 打通 Step1→Step2）。
- mission-log CP002 / registry last_updated / master-state §2 AMC 指针 同步。

### Phase B — Step 2 acquisition（已完成）

#### B1 获取顺序（身份清洗→直接竞品→最强 comparator→邻近边界，4 批）

shortlist 13 篇按 R001 Q5 + L124 官方 DOI 修正后入 `search-archive/2026-08-02/_step2_shortlist.json`。L124 的本地 DOI（None）覆盖为官方 `10.1364/oe.595557`（Optics Express gold OA）。

#### B2 下载纪律（3 轮止损，`search-archive/2026-08-02/_step2_download_log.md`）

- **Round 1**（`tools/download` 批量，arXiv/OA/Unpaywall）：成功 L165（unpaywall）/ L023（unpaywall，Glasgow self-archive）。
- **Round 2**（R1 失败论文找 arXiv/OA 正式版，经 Crossref/S2 补 DOI）：成功 L090（IntechOpen OA，DOI 10.5772/intechopen.84911）；补出 L146 DOI 10.1109/jiot.2025.3600439、L075 DOI 10.1109/access.2025.3650714。
- **Round 3**（IEEE/CNKI `tools/blit --download` + 手动 `tools/convert`）：成功 L096/L146/L075（IEEE blit 浏览器自动化）；L050/L206 CNKI 搜不到目标（空间电子技术 2026 未被索引），manual_required。
- **3 轮后停止**：L124（Optica HTTP 202 JS 反爬）/ L126/L073（MDPI HTTP 403 网络级反爬，gold OA 但 bot-block）/ L018（DLR elib 2017 无 OA）/ L020（identity-uncertain，abstract 污染）列失败清单，进入用户手动获取 blocker。
- **未用 WebReader/ResearchGate/Scholar 抓全文**（遵守 gw-acquire.md 禁令）。

#### B3 每篇身份与内容质量门（主线程独立复核 6 篇 success）

6 篇 success 全部：content.md 294–863 行（132–338 非空，≥50 行有效）；source.pdf SHA256 与 subagent 报告一致；title+authors+venue+year+DOI 抽查一致。

| L | 候选族 | 身份 | 质量门 |
|---|---|---|---|
| L165 | C | ✓ Light Sci Appl 2023 | PASS |
| L023 | A（最强 comparator） | ✓ JLT 41(11):3397, 2023 | PASS |
| L096 | B（锚） | ✓ IEEE TVT 71(1), 2022 | PASS |
| L146 | A（robust MCS + imperfect CSI） | ✓ IEEE IoT J 12(21), 2025 | PASS |
| L075 | **⚠ 实为 classification（MFI）非 AMC** | ✓ IEEE Access 2026 | PASS（内容）/ 标签待 Step 3 修正 |
| L090 | C（coherent + STTC） | ✓ IntechOpen DOI 10.5772/intechopen.84911 | PASS |

**关键身份再定性（Step 3 待办）**：L075 abstract 明说 "to **classify** real time modulation schemes…classification accuracy 96.3%" → 是**调制分类**（dead-end#8 假命中族），R001 标 "DL AMC 对照" 错误。Step 3 不当 AMC baseline，可作 classification 边界参照。

#### B4 Step 2 通过判定

- ≥5 篇合格 content.md：✓ **6 篇**。
- 覆盖 A（L023/L146）/ B（L096）/ C（L165/L090）三族：✓。
- L023/L096 成功获取：✓。
- L124 身份确定不保持 title-abstract 混乱：✓ **bibliographic 级确定**（Optics Express 34(14):26128, DOI 10.1364/oe.595557，coherent-FSO AMC；全文 coding/CSI 仍缺，Optica 反爬用户手动获取 blocker）。
- **Step 2 PASS**（不 BLOCKED）。详见 R002。

**用户行动项**：手动获取 L124 全文（DOI 10.1364/oe.595557）后 `tools/convert` 转 content.md；确认 6 篇覆盖面可接受后授权进 Step 3。

## 决策引用

- D001：新系统层范围与旧轴边界。
- D002：Step 1 科学完整性限定修复 — 候选族 4→3（A/B/C）+ identity 审计 + provenance receipt（新建）。
- V001：Step 1 原 12 项 checklist（PASS 12/12，漏审已声明）。
- V002：Step 1 限定完整性修复验证（PASS）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（Phase A 限定修复 + Phase B Step 2 acquisition；不动 Step 3-4a/Skill/p05 log/不抓全文/不设计方法）。

## 后续

- Phase B 完成后：主控/用户确认覆盖面 → Step 3 全文精读（独立新对话）。
- 未决：CNKI cookie/IP 可用性（Phase B 第四批）；L124 全文 coding/CSI/channel/scenario 闭合。
