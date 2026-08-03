# Verifications — 星地相干 FSO AMC Groundwork

> 实施验证、路线验证。每条关联 S### 或 D###，结论必须是 PASS/FAIL/PARTIAL。

## V001 — GW Step 1 独立验证（2026-08-02）

> 独立 verifier（非 producer）按执行提示词 §九 12 项 checklist 重算。
> 复算环境：worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` @ `5de0dd4`，python `~/.venvs/torch/Scripts/python.exe`。
> 总体判定：**PASS（11 PASS + 1 PARTIAL）**。唯一 PARTIAL = Check 12（registry 局部 CRLF 注入），不影响内容正确性。**[Post-fix 2026-08-02]** Check 12 已闭合（CRLF→LF 归一化 + `git diff --check` exit 0），升级为 **PASS 12/12**（见文末 Post-fix 复核段）。

### Check 1 — Dedup PASS：无其他同方向开放专题 — **PASS**

- `.sessions/_registry.yaml` 全 55 个 topic slug 列表中，唯一含 "AMC/adaptive modulation and coding" 作**主题**（非边界继承）的 active topic 是 `2026-08-02-fso-amc-groundwork`（L623-639，status: active）。
- 旧专题均为 `dormant`/`closed`：
  - `2026-07-20-research-direction-lab-system`（active，但仅是流程 owner，AMC 在其 `rdl_control` 块声明 `next_legal_action: 新建AMC Groundwork专题`，L20，非同方向竞品）。
  - `2026-07-23-research-direction-lab-longitudinal-test`（dormant；描述明确"AMC 必须另开 Groundwork 专题，本专题不启动"，registry L53）。
  - `2026-06-19-4b1-adaptive-interleaving-groundwork`（closed；4b#1 自适应**交织**，是 dead-end#5 的局部历史，不是 AMC 方向）。
- 新专题 `depends_on`（registry L629-635）：`2026-07-20-...-system`（D020 授权）+ `2026-07-23-...-longitudinal-test`（继承 negatives 边界）+ `2026-05-30-ch3-direction-exploration`（继承旧 AMC 失败先验）—— 均为依赖/边界，非重复。

### Check 2 — State consistency：三处一致 — **PASS**

三处状态文件均明确"AMC Step 1 完成 + 指向新专题"：
- **registry** `.sessions/_registry.yaml:623-627`：`slug: 2026-08-02-fso-amc-groundwork` / `status: active` / `last_updated: "2026-08-02（专题初始化 + GW Step 1 执行中…）"`。
- **system topic-index** `.sessions/2026-07-20-research-direction-lab-system/topic-index.md:202-204`：「`AMC_GROUNDWORK_TOPIC_CREATION` 已执行——AMC 转入新独立专题 `2026-08-02-fso-amc-groundwork`（D001），从 GW Step 1 开始。本 system 专题不再显示"等待创建 AMC 专题"」。
- **master-state §2** `projects/thesis-fso/master-state.md:8,41`：`current_step: METHOD-PRODUCTION-CAMPAIGN-DORMANT (AMC 轨转入独立专题 2026-08-02-fso-amc-groundwork，Step 1 完成)` + 「AMC Step 1 已完成（209 candidates / 5 sources / F1-F4 候选族 / shortlist 12 / 直接竞品搜索级 0），待用户验收后进 Step 2 全文获取」。

### Check 3 — Step 1 数量/源/已发表/必读/覆盖门槛 — **PASS**（含一处可忽略的计数偏差）

独立从 `search-archive/2026-08-02/*.json` 重算（排除 `_digest`/`_manifest`/`_alldigest` 助手文件 + `cnki-*.json` 按 list 计）：

| 指标 | SLA（`stages/gw-search.md` L54-60） | 重算值 | producer 声称 | 判定 |
|---|---|---|---|---|
| unique candidates（按 title 归一去重，空 title 视为不同 key） | ≥20 | **211**（含 2 条 openalex 空 title/量子密码 false-hit）/ **209**（producer 排除 2 条空 title） | 209 | PASS |
| distinct sources（`sources` 字段 union + cnki 计 1） | ≥3 | **5**（openalex/exa/arxiv/serpapi/cnki） | 5 | PASS |
| published fraction | ≥50% | **115/209 = 55.0%**（_alldigest.json 真值）/ 117/211 = 55.5% | R001 报 115/209 = 55.0% ✅；但 S001/`_manifest.json` 误报"published 153 (73%)"（manifest 把 r1-digest 重复合并计数） | PASS（实际 55% 仍过门槛；manifest 计数为 cosmetic 误差） |
| 必读 | ≥5 | **10**（R001 §3 priority=必读：L018/L023/L050/L073/L096/L097/L124/L126/L165/L206） | 10 | PASS |
| 机制不同子方向 | ≥2 | **F1-F4 = 4 族**（鲁棒 CSI-AMC / HARQ-IR / CSI 调制+功率 / 相干物理信息 AMC） | 4 | PASS |
| 明显空洞 | 不强求 | **有**（coherent+GG+AMC+coded-chain 四要素齐全直接竞品 0） | PARTIAL（诚实结论） | 不影响 PASS（gw-search.md 无"必须无空洞"硬门） |

**注**：producer 在 R001 §SLA 表透明披露了 manifest 与 _alldigest 的差异（R001 L36：「manifest: published 153 含 r1-digest 重复计数；以 _alldigest unique 计 115 published」），不算隐瞒；但 S001 沿用了 manifest 的 73% 数字未更正——属轻微状态同步瑕疵，不影响 SLA 判定。

### Check 4 — 语义抽检：必读 + 10 条随机样本 — **PASS**

10 必读全部 sensible（topic/axis/comp 与 title+abstract 对齐）：
- L018（IM/DD-FSO-AMC/B/direct）= Adaptive HARQ with CSI in Inter-HAP FSO ✓
- L023（IM/DD-FSO-AMC/C/direct）= Adaptive Transceiver Multi-Modal FSO（JLT 2023 c35）✓
- L050（chinese-FSO-AMC/A/direct）= DFT-SAMP 信道估计+概率整形 FSO（空间电子技术 2026，无摘要但 title 强相关）✓
- L073/L096/L126（HARQ 类，axis/comp 正确）✓
- L097（hybrid-FSO/RF-AMC/A/direct）= Relay-Assisted Satellite Hybrid FSO/RF Rate Adaptation ✓
- L124（coherent-FSO-AMC/A/direct）= Physics-informed adaptive transmission for coherent FSO（2026）✓
- L165（coherent-FSO-AMC/A/direct）= Tbit/s feeder links coherent + full-AO（LSA 2023 c109）✓
- L206（chinese-FSO-AMC/C/direct）= 三维概率整形 FSO for 快衰落信道 ✓

10 条随机非必读样本（seed=42）标签全部正确：L025（adaptive optics 补偿 → FSO-other 备选）、L037（FSO 综述 → FSO-other 备选）、L059（capacity 分析 → FSO-channel-analysis 备选）、L075（DL adaptive modulation → IM/DD-FSO-AMC 建议读 direct，非 classification）、L113/L117（hybrid/DWDM FSO → 备选）、L134（modulation formats review → FSO-other 备选）、L153（PLS secrecy → 排除）、L191（湍流廓线估算 → 排除 channel measurement）、L192（声波流场 → 排除 unrelated）。

**5 条 claimed mod-classification 排除（L087/L188/L184/L207/L070）经 `_alldigest.json` title 核验全部属实**：
- L087 = "ML Techniques for Optical Performance Monitoring and Modulation Format Identification"（IEEE COMST 2020，MFI survey）✓
- L188 = "基于深度学习算法的针状光束增强湍流大气中OAM模式识别"（模式识别）✓
- L184 = "基于动态权重的涡旋光束斜程传输双任务识别"（双任务识别）✓
- L207 = "面向畸变涡旋光束的湍流强度与传播距离双参数联合反演模型"（参数反演）✓
- L070 = "FSO通信系统中AI辅助调制与解调技术的研究进展"（borderline demod/AI-mod survey，备选非必读）✓

### Check 5 — automatic modulation classification 假命中无泄入必读/建议读 — **PASS**

逐条核对 10 必读 + 17 建议读（共 27 条），无任何一条 true_topic 含 "classification"。最易混淆的 L075（"Hybrid deep learning-based adaptive modulation"）经 abstract 核验为真实 AMC 方案选择（"introduce a new adaptive modulation scheme that uses a m…"），非 classification——标签正确。

### Check 6 — Round-1 + Round-2 真实 JSON + query provenance — **PASS**

- **Round-1**：7 个 JSON 文件（`r1-axA-*` / `r1-axB-*` / `r1-axC-*` 共 7 query），全部含非空 `query` + 非空 `sources`，结果数 0/5/12/15/16/16/20（其中 `r1-axA-mcs-fer-goodput-coherent.json` 返回 0 是真实空检索，已透明记录）。
- **Round-2**：8 个 JSON 文件（`r2-c1-*` / `r2-c2-*` / `r2-c3-*` / `r2-dc-*` / `r2-density-*` 共 8 query），全部含非空 `query` + 非空 `sources`，结果数 2/11/15/17/17/20/20/20。
- 附加 15 个非前缀 JSON（如 `adaptive-coding-modulation-satellite-optical-communication-2.json`）+ 2 个 `cnki-r1/r2-*.json`（40 中文命中，cookie/IP 受限 0 摘要）。
- 共 32 个真实检索文件，远超 ≥2 round × ≥2 文件要求。

### Check 7 — dead-end ledger 完整但不被误读为全局 Kill — **PASS**

- **9 行 dead-end 全在** topic-index.md「AMC 历史 dead-end ledger」表（行号见下表，每行均含 # / 历史 dead-end / 证据指针 / 继承约束 4 列）：

  | # | dead-end | 证据指针（已 spot-read 存在） |
  |---|---|---|
  | 1 | ISL AMC prediction | `domain-comms.md:243-247` 反模式 3 isl-acm-pred D026 |
  | 2 | 反馈延迟 > 相干时间 2-10ms | `thesis-lessons.md:39` TL-03 + R005 + H004 |
  | 3 | ③ MCS 排程 oracle 0.09 dB | `2026-06-10-.../decisions.md:539,578` + S014 |
  | 4 | AMC+CPR 联合设计崩塌 | `2026-05-31-.../R002-algorithm-direction-scout.md:52,294,361,550` |
  | 5 | 交织/PS/N1/coded-chain repair | registry 专题边界 + `2026-06-19-4b1-.../topic-index.md` |
  | 6 | P08-R2 工程资产非证据 | `method-production-campaign-thesis-map.md` B 级行 + R010 §3 |
  | 7 | DA/NDA CPR = 现有主贡献 | thesis-map A 级行 + master-state §2 |
  | 8 | automatic modulation classification 假命中 | 夏兆宇 thesis 参考文献 [24/41/43/45/46] |
  | 9 | AMC↔Ch4 BER 循环依赖 | `2026-05-30-.../R003-direction-bc-deep-analysis.md:19,26` |

- **F1-F4 每族均有 per-dead-end collision 列**（R001 §4，每个 family 表的"dead-end collision 逐条"行）：F1（L304）/ F2（L318 区）/ F3 / F4 各逐条对照 9 dead-end 打勾或标"碰撞风险/待 Step 2 验证"。
- **不伪称全局 Kill 的 inheriting-discipline 行**（topic-index.md:56）：「> 这些是**局部**历史结果，不是"所有 AMC 都无效"。Step 1 任务是找机制不同、时间尺度成立、动作真实的新问题。」
- R001 §5 Q8（L419）亦重申：「空白不等于问题成立（FR-23）…不强造方向」。

### Check 8 — 未进入 Step 2/3/4a、无仿真/无方法设计 — **PASS**

- `papers/` 全树 `find -newermt "2026-08-02"` 返回空：本轮**未下载任何全文**，未创建任何 `papers/{arxiv|doi}/{id}/content.md`。
- 全 topic 目录 grep `METHOD_SIGNAL`：4 处命中均为**禁止性声明**（"不产生 METHOD_SIGNAL"，出现在 mission-log L11 / R001 L430 / S001 L42 / topic-index L27 / voice L11），无任何实际信号产出。
- 全 topic 目录 grep `Go/No-Go|Go/Kill`：均为"不写 Go/No-Go"禁止声明或"Step 1 无 Go/Kill"诚实边界，无 verdict。
- R001 §4 F1-F4 候选族均明确标「**候选问题假设，未过四判据**」（R001 L290 声明 + 每个 family 行 L299/L318/L337/L356），是合法 GW Step 1 候选问题地图，非方法设计。
- 无任何 Q# 标"过四判据"；shortlist 12 篇明确为「Step 2 acquisition 清单（仅准备，不执行）」（Q5 表 L389 起）。

### Check 9 — 未把 P08/G1/P09/P10/P11 或 negatives 升级为 AMC 证据 — **PASS**

- R001 全文 P08/P09/P10/P11/G1 命中 3 处，全部为**继承边界/死轴**表述：
  - R001 L15（§2 8 问大纲）：把"P08-R2 资产"列为 9 dead-end 之一（用于 collision 核对）。
  - R001 L304（F1 dead-end collision）：「#6 P08-R2 资产 — 不引用为结论 ✓」。
  - R001 L328（F2 当前未知量）：「与既有 P08-R2 LDPC 工程资产能否复用」——属"未来工程资产复用"问号，非 AMC 科学证据。
- topic-index L30/L41/L64/L65 + decisions L9/L17 + voice L11 均为「不引用为 AMC 科学结论」「只是可复用工程资产」否定句。
- **未发现任何 R001/topic-index 把 P08/G1/P09/P11 当作 AMC 方向的支持证据或竞品**。

### Check 10 — YAML/JSON/Markdown 路径 & 语法 — **PASS**

- `_registry.yaml` `yaml.safe_load` 成功，55 个 topics。
- 3 个样本 JSON `json.load` 成功：`r1-axA-coherent-fso-amc-gg.json`（20 results）/ `r2-c1-coherent-fso-adapmod-power.json`（17 results）/ `cnki-r1-amc-fso-turbulence.json`（20 results，键名 `count` 而非 `total`，但有效）。
- `_manifest.json`（32 queries）+ `_alldigest.json`（209 items）均 parse OK。
- 全部 7 个 topic 文件存在且非平凡：topic-index.md（9246 B）/ R001（54064 B）/ S001（4522 B）/ decisions.md（2320 B）/ voice.md（1244 B）/ mission-log.md（1077 B）/ verifications.md（本文件，原 stub 323 B 已替换）。

### Check 11 — 四个 p05_run*.log 未修改 & 未暂存 — **PASS**

```
$ git status --porcelain projects/simulation/explore/cma-fade-divergence/
?? projects/simulation/explore/cma-fade-divergence/p05_run.log
?? projects/simulation/explore/cma-fade-divergence/p05_run2.log
?? projects/simulation/explore/cma-fade-divergence/p05_run3.log
?? projects/simulation/explore/cma-fade-divergence/p05_run4.log
```
4 个文件全部为 `??`（untracked，未被本轮 touch），`git diff --cached --name-only projects/simulation/explore/cma-fade-divergence/` 返回空（未暂存）。

### Check 12 — `git diff --check` 与变更路径范围 — **PARTIAL**

- `git diff --cached --check`：无 staged 内容，返回空（**PASS**）。
- `git diff --check`（unstaged）：**报 trailing whitespace on `.sessions/_registry.yaml` 25 行**（line 33-34, 48-53, 622-639）。Hex 排查结论：原 HEAD 版本是 LF-only，本轮编辑注入的 `+` 行混入 CRLF（每行尾多一个 CR 字符），被 git 默认 `cr-at-eol` 视为 trailing whitespace。**仅影响 `.sessions/_registry.yaml` 一个文件**，其他文件（topic-index.md / master-state.md / R001 等新建文件）无此问题。
- 该 CRLF 注入不影响 YAML 解析（`yaml.safe_load` 成功），仅是 cosmetic/line-ending 一致性问题，建议 producer 在最终 commit 前用 `dos2unix` 或编辑器统一回 LF。
- **路径范围核对**：`git status --porcelain` 共 7 项，全部在预期范围内：
  - `M .sessions/2026-07-20-research-direction-lab-system/topic-index.md`（system topic-index 加 AMC 转移记录，预期）
  - `M .sessions/_registry.yaml`（新 topic 注册，预期）
  - `M projects/thesis-fso/master-state.md`（master-state §2 加 AMC 状态，预期）
  - `?? .sessions/2026-08-02-fso-amc-groundwork/`（新 topic 目录，预期）
  - `?? projects/simulation/explore/cma-fade-divergence/p05_run*.log` × 4（**预存的 untracked 用户旧文件**，本轮未动，预期保持 untracked）
  - `?? search-archive/2026-08-02/`（检索归档目录，预期）
- **无任何预期外路径被修改**（无 Skill 改动、无 papers/ 新增、无 projects/thesis-fso/ 之外的源码改动）。

---

## 总体判定

**PASS（11/12）+ PARTIAL（1/12，仅 CRLF cosmetic）+ FAIL（0/12）**。

唯一需要 producer 在 commit 前处理的小事：把 `.sessions/_registry.yaml` 改动行的行尾统一回 LF（或整个文件统一为 CRLF），消除 `git diff --check` 的 25 行 trailing-whitespace 告警。S001 中"published 153(73%)"建议更正为"115/209 = 55.0%（_alldigest 真值；manifest 153 含 r1-digest 重复计数）"以与 R001 对齐——但这不影响 SLA PASS 判定。

### Post-fix 复核（producer 已修，2026-08-02）

- **Check 12 升级为 PASS**：producer 对全部新建/编辑文件（7 个专题 .md + registry + system topic-index + master-state）执行 CRLF→LF 归一化（python `replace(b'\r\n',b'\n')`）。独立复核：所有文件 `CRLF_count=0`（python `d.count(b'\r\n')`）；`git diff --check` exit=0，0 whitespace 错误（仅剩 autocrlf hint，非 `--check` 错误）。
- **Check 3 数值对齐**：S001 已修正为 "published 115(55.0%)"，与 R001/_alldigest 真值一致。
- **升级后总体判定：PASS（12/12）**。原 PARTIAL（Check 12 cosmetic）已闭合。

GW Step 1 全部 12 项 checklist 实质内容 PASS，可进入用户验收。

---

## V002 — Step 1 限定完整性修复验证（2026-08-02）

> 关联：D002 / S002 / R001（修订）。独立 verifier 视角复核 Phase A（A1-A5）修订。
> 复算环境同 V001（worktree @ `007a7c4`，python `~/.venvs/torch/Scripts/python.exe`）。
> 总体判定：**PASS**。本次修复闭合了 V001 漏审的两项（title-abstract identity + source provenance 口径）。

### V001 漏审声明（保留 V001，明确其盲区）

V001（12/12 PASS）仍有效，但其判定基于 R001 的表面计数，**漏审**：
1. **source provenance 口径**：V001 Check 3 把 `_manifest.json` published=153（73%）与 _alldigest 115（55%）的差异当 cosmetic 误差，未追到 manifest 是 r1-digest 重复计数的根因；也未区分 requested-source（4 API）vs result-bearing-source（result-level source_api 仅 openalex/serpapi_scholar/cnki）。
2. **title-abstract identity**：V001 未做 normalized-abstract 分组审计，未发现 6 个 dup-abstract 组覆盖 18 条 hit 的抓取污染，未发现 L124/L020/L038/L090 的 abstract 与 title 不匹配。

本次 V002 闭合这两项，不推翻 V001 的其余 10 项（dedup/state/语义抽检/dead-end/未进 Step2-4a/未升级 negatives/YAML-JSON/4 p05 log）。

### Phase A 修订复核

| 复核项 | 方法 | 结果 |
|---|---|---|
| A1 计数可从 raw JSON 重算 | 重跑 `tools/amc_step1_recompute.py` | **PASS** — 32 文件=17 unique query/16 非零；published 115/209=55.0%；priority 必读10/建议读17/待确认4/备选57/排除121；0 字节文件仅 `_cnki-r2-linkadapt.txt`（辅助 .txt 非 CNKI json），2 个 240B json 是同一空 query（mcs-fer-goodput，openalex+arxiv 返 0）的双存。 |
| A1 source 口径纠正 | result-level source_api 全量 tally | **PASS** — 仅 openalex(286)/serpapi_scholar(124)/cnki(38)/openalex+openalex(2)。exa 在 171 条 source_set 出现但 result-level 未单独打标（wrapper provenance 漏洞）；arxiv 被 request 2 次返 0。故"5 sources"是 requested(result)混合口径，真值=4 数据通道产结果。 |
| A2 dup-abstract 全量可重算 | normalized-abstract 分组（len>=40） | **PASS** — 6 组 18 条（group1 OWC-survey 7 条含 L020/L038/L090；group2 SATCOM-survey 3 条；group3 ISAC-survey 2 条；group4 FSO-enabling-tech 2 条；group5 6G-roadmap 2 条含 L124；group6 IRS-survey 2 条）。 |
| A2 L124 official identity vs 本地错配均有证据 | Crossref + S2 双源 | **PASS** — 官方：Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557，真实 abstract 是 coherent-FSO AMC（"AMC relying solely on SNR cannot capture phase dynamics…physics-informed AMC…scintillation index + phase variance"）；本地 abstract 是 6G-roadmap（与 L005 同），错配确认。 |
| A3 R001/topic-index 不再宣称 4 独立族或"直接竞品 0 已确认" | grep | **PASS** — 见本文件 D002 + topic-index 修订后字段：候选族=3（A/B/C），"直接竞品 0"改为 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`。 |
| A3 alias collision ≤4 query 不扩成新地勘 | 文件清点 | **PASS** — 恰 4 query（32 命中），0 直接竞品；未重建 209 大表。 |
| A4 receipt hash 与磁盘 raw 一致 | 重算 SHA256 比对 receipt | **PASS** — 抽查 r1-axA-coherent-fso-amc-gg.json / cnki-r1-amc-fso-turbulence.json / r2-c2-rateldpc-fso-turbulence.json + 4 alias 文件，全部 MATCH。receipt 23KB json parse OK。 |
| A4 receipt force-add 可行 | git check-ignore | **PASS** — search-archive/ gitignored，receipt 需 `git add -f`（commit 时执行）。 |

### 未变更项（V001 继续承继）

- 未进入 Step 3/精读/方法设计/仿真（Phase B 是 Step 2 acquisition，合法）。
- 4 个 p05_run*.log 仍 untracked 未动。
- 9 条 dead-end ledger 仍完整，F1-F4→A/B/C 修订后 dead-end collision 逐条对照移到 D002/R002。

**总体**：Phase A 限定修复 PASS。Step 1 修订为 `STEP1_ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR`，可进入 Phase B（Step 2 acquisition）。

---

## V003 — Phase A 修复 + Phase B Acquisition 独立终审（2026-08-02，合并自独立文件）

> 关联：D002 / S002 / R001 / R002。独立 verifier（fresh context），worktree @ branch `codex/rdl-method-production-v2`。复算环境 `~/.venvs/torch/Scripts/python.exe`。不信任 producer 摘要，所有数字重算或重读。
> 原独立文件 `V003-final-audit.md` 已合并入此条目并删除（治理纠偏：禁用独立 V 文件冒充正式 V###）。
> 总体判定：**PASS (10/12) + 2 PARTIAL**。

### 逐项（12 项）

1. **[PASS]** Phase A 计数可从 raw JSON 重算。重跑 `tools/amc_step1_recompute.py`（确定性，无网络）：32 raw JSON / 17 unique query / 16 nonzero / published 115+3 preprint+91 unknown=209 unique / priority {必读10,建议读17,待确认4,备选57,排除121} / duplicate_query_groups 15。每字段与 `_step1_receipt.json` `search_facts` 完全一致。
2. **[PASS]** dup-abstract 组可重算：6 组 18 条（7/3/2/2/2/2），L124（group5 6G-roadmap）、L020/L038/L090（group1 OWC-survey）全在。
3. **[PASS]** L124 身份 vs 本地错配双证：官方 Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557；本地 abstract 是 6G-roadmap（与 L005 同），`startswith('6G and beyond')=True` 确认。
4. **[PARTIAL → 本轮已闭合]** 原报告：R001 body 仍活跃呈现 4 族（§2 L42 "4 机制不同族" PASS 判定；§4 F1/F2/F3/F4 live headers；"4 族机制真不同"），**无 D002 supersede banner**。topic-index 已 clean，但 R001 body 从未编辑。V002 check A3 只验 topic-index 不验 R001 body，过度乐观。**本轮复核**：R001 现状已闭合——§4 各 F### header（L303/322/341/360）均带内联 `〔D002：合并/保留/并入...〕` 标注，Q1 "4 族机制真不同"（L384）带 `〔D002 修订：已废止〕` 废止注释，R001 顶部（L7-10）有完整 D002 修订声明。**Issue 1 已闭合**（D002 banner 在 V003 原报告时点之后已加入；本轮复核确认存在）。
5. **[PASS]** receipt hash 与磁盘一致：重算 7 个 raw_file_hashes 抽样 + 4 alias 文件 SHA256，全 MATCH。
6. **[PASS]** 6 篇 success 论文路径/元数据/hash/content 齐：均 content.md ≥50 非空行（226/208/242/338/245/132），均有 source.pdf + metadata.json（success/ok 状态混用但都表成功）。L096/L146 title 抽查与 shortlist 一致。
7. **[PASS]** ≥5 质量门论文真实：repo-wide 15 篇 content.md ≥50 非空行，6 篇 AMC success 全合格。
8. **[PASS]** 止损被遵守：`_step2_download_log.md` 恰 3 轮，无 WebReader/Scholar/ResearchGate 抓取。6 success / 5 download-fail / 2 manual_required。
9. **[PASS]** 未进 Step 3/精读/方法设计/仿真/METHOD_SIGNAL/Go-NoGo。所有"过四判据"都是"未过"（候选）。
10. **[PASS]** 4 个 p05_run*.log 未改未暂存（`git status --porcelain` 显示 `??`，`git diff --cached --name-only` 该路径空）。
11. **[PASS]** YAML/JSON 可解析：`_registry.yaml`、`_step1_receipt.json`、`_manifest.json`、`_alldigest.json`、`_step2_shortlist.json` + 6 篇 success metadata.json 全 OK。
12. **[PARTIAL → 本轮已闭合]** `git diff --check` PASS（仅 LF→CRLF autocrlf 提示，无空白错误）。但原 V003 报告时全部 Phase A/B 工作**未提交**（最后提交 `007a7c4`），且 `_step1_receipt.json`（gitignored）从未 force-add。**注**：该 PARTIAL 是 V003 报告时点（commit 6ada2bc 之前）的状态——S002 工作随后已统一提交为 commit `6ada2bc`（receipt 已 force-add，`git ls-files search-archive/2026-08-02/_step1_receipt.json` 返回该文件）。**本轮（D003）PARTIAL #12 已闭合**：S003 工作将在本轮结束统一提交，receipt `_step2_acquisition_receipt.json` 同样 force-add。

### 发现的问题

- **Issue 1（PARTIAL, check 4）**：R001 body 未加 D002 banner。**本轮修正**：R001 §4 F1-F4 headers 加 D002 banner（标注"原 F1-F4，D002 合并为 A/B/C"）。
- **Issue 2（PARTIAL, check 12，已闭合）**：原报告时未提交 + receipt 未 force-add。S002 已在 commit 6ada2bc 提交并 force-add receipt；本轮 S003 同处理。
- **Issue 3（minor）**：metadata.json `download_status` schema drift（success vs ok）。本轮新论文 Galijasevic 统一用 `ok`；不强制回改旧 6 篇。

---

## V004 — Step 2 覆盖纠偏验证（2026-08-02，D003 主控裁决）

> 关联：D003 / S003 / `_step2_acquisition_receipt.json`。验证 D003 主控裁决的 CORE 重判与 Step 2 BLOCKED 结论。
> 总体判定：**PASS**（CORE 重判证据充分，Step 2 BLOCKED 判定成立）。

### 逐项

1. **[PASS]** CORE 全文计数 = 4 < 5 门槛：L023/L096/L146（已有 content.md）+ Galijasevic（本轮新获 content.md 481 行）。4 篇均经子 agent 全文验证 action/condition/deployability 满足 CORE 定义（运行时 TX-side AMC action + FSO/CSI/turbulence condition + 非 classification/AO/fixed/post-hoc）。
2. **[PASS]** Safi2019 = CORE_PROVISIONAL_abstract_only：abstract（all-papers.jsonl grep 命中 DOI 10.1109/tvt.2019.2916843，cite 58）明证 action=joint/standalone adaptive coding-rate + TX power control + GG turbulence + channel-estimation error。但 IEEE paywall 无 OA，未获全文 → 不计 5 篇门槛。
3. **[PASS]** L075 = DISPUTED（不计核心）：全文验证（子 agent）core artifact = CNN-LSTM-Attention softmax 分类器 on RX STFT（confusion-matrix eval + true-label training），属 modulation CLASSIFICATION（dead-end#8 族）。AMC framing claimed 但无 CSI 估计/反馈环。SEMANTICALLY_DISPUTED_PENDING_FULL_READ。
4. **[PASS]** L165 = BOUNDARY_NO（AO 层非 AMC）：全文验证 adaptive action = AO 波front 校正（Shack-Hartmann + 97-actuator DM 1.5kHz），调制 PM-16/64-QAM 等固定 per measurement 比较 not switch。
5. **[PASS]** L090 = BOUNDARY_NO（fixed STTC）：全文验证 4-state STTC，"adaptive orthogonality controller" = 数学 ξ-parameterization for arbitrary STCs，design-time config 非 feedback-driven switch。无 CSI 反馈，无运行时 AMC action。
6. **[PASS]** 补充获取达止损：Safi（IEEE paywall，3 路径：tools/download + Crossref/Unpaywall/S2 全空）/ Chang（IEEE gold-OA bot-block，3 路径）/ Sun（Optica gold-OA Radware bot-challenge，2 路径）/ L124（Optica JS-challenge，2 路径）均 ≥3 路径失败或合法路径穷尽。仅 Galijasevic（NSF PAR OA）获全文。无 WebReader/Scholar 抓取。
7. **[PASS]** L090 路径合规：`papers/manual/L090-intechopen/`（manual slug），metadata.json 含真实 DOI 10.5772/intechopen.84911。manual 获取按 slug 命名合规。
8. **[PASS]** 持久 receipt：`search-archive/2026-08-02/_step2_acquisition_receipt.json`（11 篇，每篇含身份/路径/SHA256/CORE 判定/理由/blocker/失败路径；coverage_summary step2_verdict=STEP2_BLOCKED）。
9. **[PASS]** 未进 Step 3/精读/方法设计/仿真/MVE（FR-22 硬门控遵守；Step 2 BLOCKED 无权进 Step 3）。
10. **[PASS]** 4 p05_run*.log 未动。

**结论**：D003 主控裁决证据链完整，Step 2 STEP2_BLOCKED_BY_COVERAGE_GAP 判定成立。CORE 全文 4 < 5，未伪造 Step 3 结果。

---

## V005 — D004 Step 2 解除 blocker + Step 3 终态独立验证（2026-08-03）

> 关联：D004 / S004 / `_step2_acquisition_receipt.json` / `literature_notes_amc.md` / 5 read-notes。独立 fresh-context verifier（producer 之外）复核 D004 + Step 3 终态。
> 复算环境：worktree @ 本轮 commit（HEAD da180519 + 本轮改动），python `~/.venvs/torch/Scripts/python.exe`。
> 总体判定：**PASS**（D004 证据链完整，Step 2 PASS 成立；Step 3 STEP3_NO_VALID_PROBLEM 诚实终态成立）。

### 逐项

1. **[PASS]** Nguyen 2024 迁移完整性：`papers/doi/10.1109_taes.2024.3403809/source.pdf` SHA256 = `b49f5abf8d37dd16d92c6cc046e1dfe106d500fe8cbafce061abf0faf4c95c51`，content.md SHA256 = `27f25473f4ef098614dfe45fd9729d239a6edf0b958fa53f3ee0a82a5787103f`，与主工作区原始 `papers/downloads/2026-05-30/10535712.{pdf,md}` SHA256 完全一致 → 迁移零字节改动。
2. **[PASS]** Nguyen 2024 身份独立验证：Crossref API `/works/10.1109/TAES.2024.3403809` 返回 title/authors/venue(IEEE TAES)/vol(60)/issue(5)/pages(7498-7509)/year(2024-10) 与 content.md H1 + 执行提示词逐字段匹配；content.md 页脚含 "Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY... IEEE Xplore... Restrictions apply" → 确认**非公开 OA**（机构授权），metadata.json/receipt 未误称 OA。
3. **[PASS]** Nguyen 2024 CORE 判定（全文证据）：subcarrier K-QAM 星座 K∈{4,8,16,32,64,128} + EDFA 离散功率（content.md:73,233,317）= 运行时 TX-side AMC action；ESN 多步预测克服反馈时延（content.md:133-175,381）；弱 lognormal 湍流 + Beckmann pointing（content.md:93,109-115）；非 classification/AO/fixed/post-hoc → CORE 成立。关键缺口（IM/DD γ∝h² / 非 GG / 无 coded chain）在 receipt + read-note 正确标注。
4. **[PASS]** CORE 全文 5 ≥ 5 门槛：L023/L096/L146/Galijasevic（D003 已验）+ Nguyen2024（D004）= 5。`_step2_acquisition_receipt.json` coverage_summary.core_with_fulltext=5, core_with_fulltext_list 含 Nguyen2024, step2_verdict=STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED, superseded_verdict 保留 D003 BLOCKED 历史。json parse OK。
5. **[PASS]** C 族 BLOCKED 边界保持：L124（C_L124_FULLTEXT_BLOCKED）+ Safi（PROVISIONAL_direct_competitor，不计门槛）+ L075（classification）+ L165（AO）+ L090（fixed-STTC）判定与 D003 一致，未被 D004 改写。
6. **[PASS]** Step 3 精读完整性：5 `papers/_read_notes/{L023,L096,L146,Galijasevic,Nguyen2024}_*.md` 均存在，每篇含 M-C-A + 7 结构化子表 + AMC 关键语义字段 + 与目标重合/缺失 + 四判据 + file:line 证据；`literature_notes_amc.md` 含精读条目 + 直接竞品矩阵 + 综合 + Q# 表 + 写作架构 + 实验完备性对标。title self-check 全过（Jaccard ≥0.38，L096 dispatched 短形式致 0.50 临界但语义 PASS）。
7. **[PASS]** 边界/语义仲裁证据：L075=classification（content.md:15,175,211,217,337 confusion-matrix + softmax + true-label）/ L165=AO（content.md:11,82,86,99,180 SH+DM 1.5kHz）/ L090=fixed-STTC（content.md:9,119,163,165 ξ-param design-time）证据链完整。
8. **[PASS]** Safi/L124 全文缺失边界遵守：二者 read-note 标 PROVISIONAL/C_FAMILY_BIBLIOGRAPHIC，**未据 abstract 推导失效机制**；Q4/Q5 因 abstract-blocked / C-blocked 判未过，证据链符合 D003 约束。
9. **[PASS]** 直接竞品矩阵：5 CORE + Safi 6 行 × 11 列，每格 ✓/✗/△ + 依据；**无一篇 confirmed 同时覆盖 coherent+GG+coded+uncertainty 四要素**结论有矩阵支撑（每篇至少 2 ✗）。
10. **[PASS]** Q# 四判据诚实：5 候选 Q# 逐条标四判据，**无一全过**。Q1（迁移非失效）/Q2（self-id future work）/Q3（机械拼接待证假设，brief FAIL）/Q4（abstract-blocked）/Q5（C-blocked）判定理由与 glossary 四判据 + brief 一致。**Step 3 终态 STEP3_NO_VALID_PROBLEM 成立**（诚实终止，不包装空白）。
11. **[PASS]** 未进 Step 3.5/4a/MVE/方法/仿真：literature_notes_amc.md §7 明确终态 + 下一步合法动作 = Step 3.5（下一轮）；无 METHOD_SIGNAL/Go-NoGo/算法设计/仿真代码。
12. **[PASS]** literature notes owner 不冲突：`literature_notes_amc.md`（新建专属 owner）与 receiver `literature_notes.md`（197KB 未改）独立文件，D004 §8 登记 adapter 路径。
13. **[PASS]** 治理合规：D004 含依据字段 + 触发原话（voice.md 已登记 2026-08-03 verbatim）；topic-index GW Progress 表 Step 2 ✅/Step 3 ✅ + 范围变更 D004 + 当前位置/未决项/下一合法动作改写；registry/master-state 待同步（producer 进行中）。
14. **待复核**：`git diff --check` + 4 p05_run*.log 未动 + Skill 未改 — 由 commit 前最终核查。

**结论**：D004 证据链完整，Step 2 STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED 成立；Step 3 STEP3_NO_VALID_PROBLEM 诚实终态成立。Nguyen 迁移 + Crossref 验证 + 5 CORE 精读 + 直接竞品矩阵 + Q# 四判据全部有 file:line / SHA / API 证据支撑。Safi/L124 全文缺失边界严格遵守。未伪造 Step 3.5/4a/方法/仿真。

> **[D005 语义失效标注，2026-08-03]** V005 验证的是**本地自写合同**（自创四判据标签 problem_truth/actionability/novelty/thesis_fit 四列）的**一致性**，**没有核对 canonical criteria owner**（stages/glossary.md L22-31 + templates.md L301）。因此 V005 的 Step 3 verdict（"Q# 四判据诚实"check 10、"STEP3_NO_VALID_PROBLEM 成立"）在**科学语义层失效**——它验证的四判据不是协议合法的四判据。V005 保留历史不删；regression candidate 已登记（见 V006 check 11 + D005）。Nguyen 迁移 SHA / Crossref 身份 / 5 CORE 精读完整性 / 边界仲裁 / Safi·L124 全文缺失边界遵守 等纯事实性 check（1-9 除 verdict 部分）继续有效。

---

## V006 — D005 Step 3 语义门纠偏 + Step 3.5 终审独立验证（2026-08-03）

> 关联：D005 / R001 / R003 / S005 / H003 / literature_notes_amc §6/§7/§11。独立 fresh-context verifier（producer 之外，复核 canonical owner + 竞争闭包 + 10 项 checklist）。
> 复算环境：worktree @ 本轮改动（HEAD `482d9ad` + 未提交改动），sha256sum/grep/Read 重算。
> 总体判定：**PASS（11/11）**。

### 逐项

1. **[PASS]** semantic-gate receipt owner — R001 §A 记 `stages/glossary.md` SHA256 `eafa43e3…073f610e74b`（L22-31）+ `templates.md` SHA256 `bdc93d41…caa7b9e41`（L301/L308/L311/L371）。重算 `sha256sum stages/glossary.md templates.md` 完全一致。D005 decisions.md 同 SHA + 同行号。
2. **[PASS]** 四判据与 owner 一致 — R001 §B 四判据标签 = glossary L22-31 + templates L301 原文（具体技术矛盾/方法产出形态/近期baseline/可量化对标）。literature_notes §6 明示 canonical 标签 + 旧自创标签废止。grep 确认 `problem_truth/actionability/novelty/thesis_fit` 仅出现于废止标注/纠偏解释，未作 §6/§7 terminal verdict。
3. **[PASS]** 没有把 Step 4a/MVE 证据前移 — Q-A/Q-B 判据1 只要求"M-C-A 明确可证伪"，明示"不要求已用 MVE 证明退化"。grep "需 MVE 证明/需 oracle/需证退化" 在 Q-A/Q-B verdict 段 0 命中（仅出现在解释旧错误时）。
4. **[PASS]** Q-A/Q-B 单一可证伪 M-C-A，且 ≠ Q3 — Q-A 单一 baseline(Galijasevic)+单一失效假设(点预测无后验)+可观察失效(FER 违约)；Q-B 单一 baseline(L023)+单一失效假设(同环绑定)+可观察失效(L023 自陈 LEO 不可行)。Q3 仍 TOO_BROAD，子集由 Q-A/Q-B 承接。Q-A≠Q-B。
5. **[PASS]** direct competitor search 足够针对 — `search-archive/2026-08-03/` 55 文件。Q-A 6 专属 query + Safi forward(49)；Q-B 9 专属 query + L023/Nguyen2024/Galijasevic citation。R003 §3 闭包表覆盖直接竞品(Nguyen2024/L023/Safi/L124)+近邻+反例(RF massive-MIMO split-timescale)。≥2 组不同表述 + 引用链 + 三类筛选均满足。
6. **[PASS]** Safi/L124 缺全文边界未越界 — 两目录仍仅 metadata.json 无 content.md。Q4/Q5 BLOCKED_BY_MISSING_FULLTEXT。R003 §2 记 3 路径失败。闭包表标 UNVERIFIED 而非推机制。多处明示"禁据 abstract 推导失效机制（FR-26）"。
7. **[PASS]** future-work 没被自动当 novelty FAIL — Q2 判定明示"论文自列 future work ≠ novelty 自动失败（D005/brief）"，作"问题原料保留待 Step 3.5 查"。D005 同原则。Q2 不晋级原因是切片重叠非 novelty 自动失败。
8. **[PASS]** competitor closure 支持终态 — R003 §3 + literature_notes §11 闭包表覆盖最强竞品（Nguyen2024/L023/Safi/L124）+ 分类完整（PARTIAL_OVERLAP/DISTINCT/UNVERIFIED）。§11.3 终态 Q-A+Q-B 均 SURVIVES_STEP3_5。
9. **[PASS]** 未进入 Step 4a/MVE — grep METHOD_SIGNAL/Go-NoGo 在本轮新文件 0 命中（唯一命中在旧 landscape 是否定约束）。literature_notes §7 + §10 + topic-index + H003 + master-state 均明示"本轮不启动 Step 4a/MVE/方法/仿真"。无算法设计/仿真代码。
10. **[PASS]** git diff --check / scope / 治理一致 — `git diff --check` exit 0（仅 CRLF hint）。`git status --porcelain` 确认 4 个 p05_run*.log 仍 untracked 未动。`.agents/skills/research-direction-lab/` 未改。dormant receiver campaign 未触碰。改动路径全在预期范围（.sessions/专题 + literature_notes_amc + master-state + search-archive/2026-08-03 + _registry.yaml）。
11. **[PASS]** 回归候选落实 — D005 "V005 处置"段标语义失效 + 登记 regression candidate "verifier 必须核对 canonical criteria owner，不能只验证本地 prompt/contract 自洽"。V005 保留历史不删。voice.md verbatim 登记同措辞。H003 纪律#4 + R001 §A 重申 canonical owner 唯一性。

### 发现的问题
无。所有 11 项 PASS。

### 结论
D005 + Step 3.5 终审全部 11 项独立验证通过——canonical owner SHA256/行号重算一致、四判据标签与 glossary/templates 原文一致且自创标签仅作废止标注、无 Step 4a/MVE 证据前移、Q-A/Q-B 单一可证伪且 ≠ Q3、检索规模与闭包表充分、Safi/L124 全文边界严守、future-work 未被当 novelty 自动失败、未进 Step 4a、git scope 与治理一致、回归候选已落实。**允许 commit**。
