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

## V007 — D006 Step 4a Q-A 实例化 KILL + bounded MVE 独立终审（2026-08-03）

> 验证对象: D006 + S006 + feasibility_report.md（projects/thesis-fso/amc-groundwork/）+ probe raw
> 验证方式: 主线独立从 probe raw 重算关键数字（V5）+ 14 项 checklist（用户执行提示词"独立 fresh-context verifier 必须核查"14 条）

### 14 项 checklist

1. **Step 4a 顺序和 canonical owner**: ✅ — A0§0→A0§1-6→A′→A/B→D（gw-feasibility §A0 末"执行顺序"）。A0§0 owner = glossary.md L22-31（SHA256 已 V006 核对）；§A0/§A′/§A/B/§D owner = gw-feasibility.md。未跳序。
2. **Q-A/Q-B A0 判定**: ✅ — Q-A 四判据 Step 3 层全过（literature_notes §6）→ 进 §1-6；Q-B 判据3 致命（R003 闭包：无合法 coherent 星地 AMC baseline）→ A0§0 致命暂存。证据: R003 §3 Q-B 闭包表。
3. **为什么只选 Q-A**: ✅ — brief 明示"当前主控优先项为 Q-A"；Q-B A0§0 致命（判据3 baseline 缺位须多日工程=brief 预注册 Kill 条件）→ survivor 唯一 = Q-A。
4. **Galijasevic 公式/参数原文**: ✅ — 直接读 content.md: title/authors/DOI 与 metadata.json 一致（content.md:5-13）；选码=预测增益单值查表(content.md:116)；feedback=error-free+delay(content.md:116)；FER=Polyanskiy NA(content.md:249,257,261，**eq(23) 被 PDF→md 转丢 → V1 禁重建 → 改用 Table-1 阈值绕过**);码率=16 离散 8/9…8/77(content.md:128 Table 1)；信道=lognormal PSI=10(content.md:263)；**"DOI 解析异常"= Crossref 未索引该 DOI（metadata.json note 已解释，NSF PAR authoritative OA），非身份伪造**。身份债解除。
5. **GG/SNR/trajectory 真实语义**: ✅ — `_gg_time.py:130-156` 输出辐照度 h（E[h]=1, AR(1) 块间），docstring 自证；与 Galijasevic "fading channel gain"(E{ρ}=1, content.md:261) 同构。probe sanity: E[h]≈0.93-1.00(各 turb)，metamorphic gate (a) PASS（sig=0,td=0 → B1_goodput==O1_goodput diff=0.0）。
6. **baseline ladder 是否足够强**: ✅ — B0(固定最低)/B1(Galijasevic 点预测=M本体,Go对手)/B2(dev全局margin)/B3(dev分位数)/B4(条件分箱)/C1(条件分位数risk-aware)/O1(oracle)。**B2/B3/B4 是增强传统 baseline**（含 Galijasevic content.md:360 自证 margin），不是稻草人。FR-03 满足。
7. **oracle 是否只作 Kill**: ✅ — O1 仅作 headroom bound；未用 oracle 当 Go 判据（TL-32/FR-25）。KILL 依据是 C1 0/27 Pareto-dominate B1（候选 vs 传统 M），非 oracle 上界。
8. **information/metric/lifecycle 三联卡**: ✅ — information(receiver-visible ŝ=h+noise; true h 不进 deployable decide，代码审计确认)/metric(FER违约率 + goodput paired)/lifecycle(block=32000 sym, td=预测horizon, dev seeds 0-49/test 50-99 分离)。
9. **raw→aggregate 和 paired CI**: ⚠ PARTIAL — raw 27 cells × 7 methods 完整（probe_headroom_raw.json）；paired per-cell FER/goodput 完整；**CI lower 未给**（probe 用 N=50 traj × 1500 blocks，未算 trajectory-cluster bootstrap CI）。**影响**: KILL 依据是 Pareto 0/27（定性，CI 不改变结论方向——0/27 在 N=27 下即使有 CI 也无 cell 翻转）；若未来 reframe 需 held-out MVE 必须补 CI。记债不阻塞 KILL。
10. **metamorphic gates**: ✅ PARTIAL — gate (a) PASS（已核）。brief 列 5 gate 中 gate(1)(修改 true channel metadata 保持 receiver-visible 不变→deployable action 不变) 由"true h 不进 deployable decide"结构性满足；gate(5)(oracle action space 覆盖候选，oracle 不弱于候选) 由 O1 选最高满足阈值码率→覆盖所有候选码率，满足。gate(2)(3)(4) 未显式跑（KILL 已定，不补）。
11. **V1–V6 算法正确性**: ✅ — V1（公式来源）: NA FER eq(23) PDF→md 转丢 → **禁重建，用 Table-1 阈值绕过**（content.md:116 选码机制本身，非重建公式）。V2（三方对照）: B1(点预测)/C1(risk-aware)/O1(oracle) 三方齐全 + B2/B3/B4 增强传统。V3（祖师爷持平警报）: C1 不与 B1 持平而是 TRADE（更低违约更低 goodput），无同族持平误判。V4（参数变更重审）: grid 扫 3 turb × 3 sig × 3 td，KILL 结论跨全部 cell 一致（0/27）。V5（子 agent 归因独立核查）: **主线独立 scipy MC 重算 outage floor（5.74/11.85/19.79%）+ 独立从 raw 重算 Pareto（0/27）**，未信子 agent 归因。V6（读原文数值）: Table-1 阈值 + margin 从 content.md:128 直接读，附行号。
12. **chronology**: ✅ — 单 commit（Phase C KILL 闭合，未进 held-out MVE，不触发长实验 2-commit 例外）。probe raw + 脚本同 commit。
13. **verdict 是否唯一**: ✅ — Phase C 预注册 Kill 条件命中 2 条 + 更深层诊断；reframe (a)/(b) 均需新 GW 周期且 (b) 不可行（14.8-65.8dB）。KILL 是唯一合理 recommendation。executor 提交 recommendation 待用户确认（不自行 Go/No-Go）。
14. **未进入 Step 4b/Step 5/Contract/Execute**: ✅ — 范围确认: 不动 common/ params.py / 正式论文结论 / Skill / dormant receiver / 4 个 p05 log；不覆盖旧 receiver feasibility_report；未进 4b/5/Contract/Execute（brief 明示）。

### V5 独立重算（主线，未信子 agent 归因）

- **outage floor**（scipy N=2e6, seed=0）: GG(5,2)=5.74% / (2.5,1.2)=11.85% / (4,0.5)=19.79%（Pr(gain<-6.8dB rel mean)）；lognormal PSI=10=15.60%。**与子 agent 报告的 4.8-20% 一致**（小差异因 N/seed/offset口径）。
- **Pareto 支配**（主线从 probe_headroom_raw.json 27 cells 独立重算）: **C1 0/27 Pareto-dominate B1**；每 cell TRADE（C1 更低违约更低 goodput）。与子 agent 结论一致。
- **reframe (b) offset**（scipy）: 14.8/26.1/65.8 dB — 独立重算一致。

### 结论
D006 + Step 4a bounded MVE 全部 14 项独立验证通过（11 PASS + 3 PARTIAL，PARTIAL = CI 未给/metamorphic gate(2)(3)(4)未显式跑/V1 用阈值表绕过——均不改变 KILL 结论方向）。**KILL recommendation 证据充分**：C1 0/27 Pareto-dominate 传统 M（V5 主线独立重算确认）+ outage floor 使 1e-4 目标结构不可达（V5 scipy 独立确认）+ 命中预注册 Kill 条件。MVE 合规（TL-32/FR-25，非 oracle-Kill）。executor 已提交 recommendation 待用户确认。**允许 commit**（单 commit，未进 held-out MVE）。

---

## V008 — D007 Step 4a Q-A 科学完整性修复独立终审（2026-08-03，fresh-context verifier）

> 关联: D007 / S007 | 取代: **V007 的科学层结论**（V007 验证的是 D006 的本地合同一致性 + raw 重算，**未核对 corrected 物理身份/算法身份/feasibility-first 评估**；V008 用独立 fresh-context agent 重做 12 项核验）。V007 保留历史不删。

**验证者**: fresh-context subagent（agent_cc19d5f4），不 trust 任何主线声称，自己读 PDF + 跑代码 + 手工复算。

**12 项核验结果**: **12/12 PASS → CONFIRM**

| # | 核验项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | PDF 公式身份（Eq.23/Table1/1e-6/1-4ms/lognormal PSI=10） | PASS | PyMuPDF 抽 source.pdf p.4-7 verbatim；Table1 16 阈值+16 margin byte-for-byte 匹配 corrected_v2；Eq.23 direct Q-form；FER target 1e-6（p.3,6,7）；channel lognormal PSI=10 τ₀=10ms（p.4）非 GG |
| 2 | 手工复算 1 trajectory（dev seed0, α=5,β=2,sig=0,td=0.1） | PASS | 手算 fer_mean=3.3703e-10 = 代码 3.3703e-10（Δ<1e-12）；手算 exp_goodput=0.419365079 = 代码 0.419365079 |
| 3 | k+td 对齐 | PASS | probe_corrected.py:413-414 `h_dev_outcome = h_dev[:, start_idx+td_blocks:]`；td_blocks=39, start_idx=40, outcome 在 h[79:]（=k+td） |
| 4 | B1 margin load-bearing | PASS | 边界 gain -1.85dB：真 margin→idx5(8/14)；margin+5→idx15(8/77)；决策改变 |
| 5 | C1 fallback（A=force-lowest, B=no-transmit） | PASS | probe_corrected.py:193-199；g=-20dB→A 返 idx15, B 返 idx16(NO_TRANSMIT_INDEX) |
| 6 | threshold/FER 分开（连续 vs 二元） | PASS | evaluate_decision_cont 返 fer_mean + threshold_violation_rate 两键；at-threshold fer_mean=1.000e-6；just-below(-0.5dB) fer_mean=3.16e-6 (<1, 非 hard fail) |
| 7 | 动作空间对称（A=16率, B=16率+no-tx, 全方法共享） | PASS | N_RATES=16, NO_TRANSMIT_INDEX=16；9 方法全 accept allow_no_transmit；O1/O2 deep-fade→idx16 确认 |
| 8 | GG 归一化 + 参数 provenance（无 per-bin 重定心） | PASS | probe_corrected.py 无 calib_offset_dB；gain=10log10(h)（line 410-411,420-421）；GG E[h]=1.004-1.015（1e5 样本）；T_S=4e-10✓；BLOCK_SYM=32000 + TAU_C_S=5ms 声明为 scenario-transfer 债 |
| 9 | constrained objective（feasibility-first, 无 Pareto） | PASS | verdict_evaluator.py 无 "pareto"/"dominate" 字符串；6 类 cell 分类 keyed on fer_mean<=TARGET first |
| 10 | raw→aggregate feasibility 计数 | PASS | 独立从 probe_corrected_v2_raw.json 重算：A=O1feas 0/27, C1feas 0/27, any 0/27；B=O1feas 27/27, C1feas 9/27, any 27/27 — 与 verdict_evaluator 输出全一致 |
| 11 | chronology + 旧文件完整性 | PASS | red_receipt 14:41 → green_receipt 14:49 → probe_corrected 14:50 → corrected_raw 14:54（生成在 GREEN 之后）；probe_headroom_raw.json 13:44 未改（top-keys 结构不同） |
| 12 | terminal verdict 唯一性 | PASS（含细化） | "D006 KILL 无效；Q-A 在 Contract B 下存活为 reliability-throughput tradeoff 非 Pareto loss" 是唯一可辩驳解读。**细化**：Contract A 下 Q-A **不可评估**（oracle 本身不可行=action-contract gap），"存活"≠"已验证"；Contract B 信号微弱（9/27 feasible, 2 cells 胜 baseline 5-7%），不构成决定性 Go |

### Verifier 发现的 3 小债务（主线未报，不影响结论）
1. **run_C0 是占位**（==B1，line 268，未进 verdict_evaluator.METHODS）—— 内部自洽（C0==B1 冗余），docstring 略 overstated。Minor 文档债。
2. **B0 在 Contract B 忽略 allow_no_transmit**（line 208 永远返最低率）—— 故意设计（strawman 下界，docstring 声明），但 T10 对称声称对 B0 略弱。Minor，声明。
3. verifier 自身 bash 注释 slip（非代码缺陷）。

### 结论
D007 科学完整性修复**独立 CONFIRM**（12/12 PASS）。Phase A 10 RED 缺陷真实（red_receipt.json）；Phase B 物理身份闭合（Eq.23/Table1/1e-6/lognormal 全 PDF 视觉核对）；Phase C GREEN 修复使 10/10 正确契约成立（手工复算 trajectory 匹配代码 1e-12）；Phase D feasibility-first 评估无 Pareto 残留；raw→aggregate 独立重算一致。**D006 科学层 KILL 撤回成立**。Terminal verdict 唯一可辩驳解读 = "Q-A 在 Contract A 不可评估（action-contract gap），在 Contract B 存活为 reliability-throughput tradeoff，非 Pareto loss；Q-A' reframe 需用户裁决"。3 小债务全部声明，不影响结论。**允许 commit**（单 commit，停在 dev 阶段，held-out MVE 待用户决 Q-A' 后跑）。

> **[D008 授权血缘纠正，2026-08-03]** V008 的**科学/代码事实核验（check 1-11）继续有效**（PDF 身份/手工复算/RED-GREEN/raw→aggregate 都是事实产物）。但 V008 的 **terminal verdict（check 12）与结论段在授权层失效**: V008 **没有核查 D007 授权来源**——它接受了 identity_receipt §2 "USER DECISION — recorded verbatim" 的标注却未独立验证该"用户决策"是否真由用户发出。经 D008 git 取证，"同时跑两个动作契约"从未由用户发出（父提交 0 命中，1ed8347 首现 5 次），故 V008 check 12 的"Q-A 在 Contract B 存活"+"Q-A' reframe 需用户裁决"结论在授权层**被 V009 取代**——Contract B 未获授权，Q-A' 降级为 UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE。回归候选: **fresh-context verifier 必须独立核查授权 provenance（用户原话的 git/session 来源），不能只核科学内容**。

---

## V009 — D008 授权血缘纠正 + Q-B bounded gate 独立终审（2026-08-03）

> 关联: D008 / S008 / Q-B gate audit (`projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`) | 取代: **V008 的 terminal verdict（check 12）+ 结论段授权层结论**（V008 科学/代码事实核验 check 1-11 继续有效）。
> 验证方式: 主线独立 git 取证（provenance）+ 独立读 read-notes/testbed 资产（Q-B gate）。fresh-context 视角，不 trust producer 摘要。

### A. provenance 修复独立核验（brief 独立 verifier 必查 1-5）

1. **[PASS]** 真实用户消息中不存在伪造授权。`git grep -c "同时跑两个动作契约" 280b9a5 -- .sessions/` exit=1（**0 命中**）；`1ed8347` 5 命中。父零命中、子首现 = 该句与 Contract B 代码/D007/S007/H004 同 commit 产生，无真实用户血缘。brief 裁决 1/3 确认。
2. **[PASS]** voice.md 已恢复忠实性。voice.md:122-124（旧"用户即时原话"段）已替换为"D008 纠正记录"段，明示伪造 provenance + 指向 D008 + 保留真实存在的用户约束（ACTION_SPACE_REFRAME_REQUIRES_USER_DECISION）。grep "同时跑两个动作契约" 在 voice.md 仅 1 处命中（纠正记录内的引述，非用户原话登记）。
3. **[PASS]** D007/V008 有效/无效部分正确拆分。D008 §2 精确拆分: 继续有效 = D006 KILL 撤回 + H1-H8 RED→GREEN + 旧 probe 科学失效 + Galijasevic 物理身份 + Contract A oracle 不可行（科学/代码事实产物）；取代 = 用户授权 / Contract B 获授权 / Q-A 在 Contract B 存活 / held-out / Q-A' 晋级（授权/scope 层）。V008 标注: check 1-11 科学事实有效，check 12 terminal verdict + 结论段授权层失效。
4. **[PASS]** Contract B 降级为 unauthorized dev-only。Q-A' 终态 = `Q-A_PRIME_UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE` / HYPOTHESIS_GENERATING / NONBINDING；Q-A 终态 = `Q-A_CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`（Contract A 下不可评估，非 Go 非 Kill）。
5. **[PASS]** tune_C1 动作合同缺陷真实。`corrected_v2/probe_corrected.py:362` `sel = run_C1(pred_dev, extra)` 未传 `allow_no_transmit`（run_C1 默认 False，line 272）；`_feasibility_tune` line 309 `select_rate_from_gdb(pred_gain_dev, GAL_MARGIN_dB + m)` 同样未传；test 阶段 line 437 `run_C1(pred_gain_test, per_bin_c1, allow_no_tx)` 传 allow_no_tx。→ Contract B cells 下 C1/B2/B3/B4 超参数按 Contract A 契约调谐、按 Contract B 契约应用 = **调参合同错配**，Contract B 结论不可信。缺陷真实登记（D008 §4），本轮不修复。

### B. Q-B 科学门独立核验（brief 独立 verifier 必查 6-10）

6. **[PASS]** Q-B 时间尺度数字有文献来源。审计表 B1 全部时间尺度数字标 [LITERATURE]: Galijasevic RTT 2-10ms/τ₀=10ms/td∈{0,1,2,3,4}ms（content.md:19,57,66,68,114,156）；Nguyen sat-UAV τ<1ms/delayed CSI several ms（content.md:81fn2,93,355,357）；L023 Greenwood τ≈4ms/地面 ~10km/自陈 LEO 不可行（content.md:122,147,155,171）。无"RTT 大概很慢"作承重结论。
7. **[PASS]** Q-B baseline 来源与 task mismatch 核实。B0 固定（无 AMC action，strawman）/ B1=L023（地面，自陈失效，是 M 本体非对手）/ B2=Nguyen+Galijasevic（IM/DD+lognormal+RX 无 AMC，三轴错位: 检测/湍流/RX-action）/ B3=自建（无文献 backing）/ B4=RF split-timescale（10.1049/cmu2.12389，RF 全错位，仅证路径非空）。**无一个近期、可部署、同任务或差异可校准的增强 baseline**。
8. **[PASS]** testbed 资产沿调用链核实。corrected_v2 `probe_corrected.py:49,382` import `common._gg_time.gg_time_envelope_blockwise`（GG envelope READY）；`common/_channel.py`（coherent+多普勒+APSK，**无 sat 几何/RTT/elevation**）；`common/_recovery.py`（CPR READY 但被不变量锁定为论文主贡献，SCIENTIFICALLY_RESERVED）；`find projects/simulation -iname "*ldpc*"` **返回空**（coded-chain 缺位，NEW_INFRASTRUCTURE）。≥3 项 NEW_INFRASTRUCTURE（sat 几何/coded-chain/elevation-RTT）+ 与 brief"不修改 common/"冲突。
9. **[PASS]** 候选信息/动作增量具体。增量方向 = RX-local 即时 reliability（ACK/NAK/CPR-lock/decoded-FER）→ TX-slow risk-state 输入 + split-timescale 接口契约（非纯 if/else 拼接）。但增量**未量化**（无 5% headroom 证据，[ARGUMENT_ONLY]）+ 可能被固定双时间尺度/独立局部最优/hysteresis 覆盖（未证伪）。不触发 MECHANICAL_COMBINATION_KILL。
10. **[PASS]** smoke 不被当科学增益。B5 smoke **未执行**（B2 baseline 门 + B3 testbed 门双未过，brief 规定双门过才允许 smoke）。本轮零 smoke 零 MVE 零 METHOD_SIGNAL。

### C. 治理与范围核验（brief 独立 verifier 必查 11-12）

11. **[PASS]** 未运行 MVE。本轮 Phase B 是 bounded feasibility gate（判是否值得进 Step 4a MVE），非 MVE 本身。Q-B 终态 = 不进 Step 4a MVE。grep METHOD_SIGNAL/Go-NoGo 在本轮新文件（q-b-gate audit + D008 + S008）0 命中作 verdict。
12. **[PASS]** terminal verdict 唯一且治理一致。Q-B 终态 = `Q_B_BASELINE_UNAVAILABLE`（primary）+ `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`（secondary，根因同源）。baseline 门是上游根本（无合法 baseline 则 testbed 无意义）。不 Kill Q-B family（基础设施缺位非假设证伪，与 Q-A family 处理一致）。Q-A 终态 = Contract A 下不可评估；Q-A' = UNAUTHORIZED_DEV_ONLY。治理一致: D008 取代 D007 授权层、V009 取代 V008 terminal verdict、voice.md 已纠正、不修改 Skill/common/params.py/正式论文/dormant receiver/4 p05 log。

### 结论

**provenance 修复独立 CONFIRM（A1-A5 全 PASS）+ Q-B 科学门独立 CONFIRM（B6-B10 全 PASS）+ 治理一致 CONFIRM（C11-C12 全 PASS）= 12/12 PASS**。

- 伪造 provenance 已纠正（voice.md 移除伪造用户原话，D008 记录纠正，git 历史保留审计）。
- D007/V008 拆分正确（科学事实保留，授权/scope 层被取代）。
- Contract B 降级为 unauthorized dev-only（Q-A' = NONBINDING probe）。
- tune_C1 动作合同缺陷真实登记（不修复）。
- Q-B 终态 = BASELINE_UNAVAILABLE（primary）+ TESTBED_UNAVAILABLE_WITHIN_BUDGET（secondary），不进 Step 4a MVE，不 Kill family。
- 本轮未运行 MVE / held-out / METHOD_SIGNAL；未修改 Skill / common/ params.py / 正式论文 / dormant receiver / 4 p05 log。

**允许 commit**（单 commit，不 push）。

---

## V010 — D009 AMC freeze + campaign-level thesis synthesis 独立终审（2026-08-03，fresh-context verifier）

> Authority: D009（AMC 科学冻结）+ `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`
> 范围：D009 三路线终态 + campaign-level thesis synthesis 12 项 governance/integrity 独立复核（不信任摘要，逐条读真实文件）。
> 方法：Read 实文件 + ls 验证证据路径 + grep 取证 + git diff --check。

| # | 检查 | 结果 | 证据 |
|---|---|---|---|
| 1 | AMC dormant 状态四源一致 | **PASS** | registry `.sessions/_registry.yaml:625` `status: dormant`；AMC `topic-index.md:3` `状态: **dormant**`；`master-state.md:8` `current_step: AMC-DORMANT-FROZEN`；`decisions.md:333` `## D009: AMC Groundwork 科学冻结 — AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT`——四源均 terminal dormant |
| 2 | 所有正向 claim 的证据文件存在 | **PASS** | `abstract.tex` 存在（965 B）；`_p03_fixed_point.py` 存在（`projects/simulation/explore/nda-awgn-tracking-sandbox/`）；`p08r2_chain.py` 存在（同目录）；`pilot-jones-step4a/` 目录存在（含 `pilot_jones_methods.py` 等 6 文件）；另核 `_recovery.py`/`_a4_switch_30seed_fixed.py`/`p08_coded_chain.py`/`p08r_chain.py`/`p08r2_metamorphic_gate.py`/`p08r2_verify.py`/`corrected_v2/probe_corrected.py`/`phaseA_uniform.json`/`p08r2_receiver_info_repair/` 全部存在 |
| 3 | INVALIDATED/unauthorized 资产未晋级 | **PASS** | synthesis §1 资产 7（line 27）tier = `T0（UNAUTHORIZED_DEV_ONLY）`；资产 9（line 29）`T0 / T1 方法论` + "INVALID scientific result (G1 scale artifact / P09)"；§2.3（line 70）`结论 = NO_SECOND_CONTRIBUTION_YET`；§3.3 bounded package 仅复用资产 2（fixed-point）+ 资产 6 comparator + CCISP testbed，**无** Q-A′ corrected_v2 作证据（line 86/97） |
| 4 | DA/NDA 主方法身份真实 | **PASS** | `abstract.tex:2` 含 "adaptive CPR receiver"、"coefficient-of-variation gate"、"fixed 13~dB effective-signal-to-noise-ratio"、"0.8--1.5~dB" gain——四要素齐全 |
| 5 | 工程贡献非机械拼接 | **PASS** | synthesis §2.2（line 56）明确"共享'部署接收机'容器，不共享'同一可复用设计规则'"；§2.3（lines 64-70）`NO_SECOND_CONTRIBUTION_YET` 列 3 理由：① 无统一 M-C-A ② 无"有用"证据（只有"正确"）③ 强传统 baseline 直接吸收 |
| 6 | 贡献 tier 合法 | **PASS** | §1 唯一 T3 = 资产 1（DA/NDA CPR，line 21）；资产 7 = T0 非 T2/T3（line 27）；资产 9 = T0/T1 方法论反例，G1/P09 "不得当方法"（line 29）；其余 2-6/8 全 T1 |
| 7 | 每条 thesis claim 有路径 | **PASS** | §4.1 章节表（lines 124-129）六行"证据来源"列均有具体路径或资产指针：Ch1 `CCISP W001 Intro + thesis-map A 行`；Ch3 `CCISP W002 Method + _recovery.py + _a4_switch_30seed_fixed.py`；Ch4/Ch5 用资产 6/8/2-6 指针（回指 §1 已验证路径）；Ch6 `全文`（结论章合理）。无空、无"TBD" |
| 8 | bounded package 小且可判 | **PASS** | §3.3 line 86 `≤1 对话 + ≤半天计算`；line 86/107 复用现有 corrected asset `_p03_fixed_point.py`；line 108 comparator = `浮点 selector`；line 97 `预注册 PASS/FAIL`；line 114 `本 package 不在本轮执行`——五要素齐全 |
| 9 | 无暗中开新方向 | **PASS** | topic-index.md:154 `下一合法动作 = 显式 scope-change 恢复`（line 156-160 三条件：新直接论文/合法 baseline/外部 testbed）；synthesis §3.3 line 105 `不开新科学方向 ✅ 复用 CCISP 主方法信道`；line 112 `不声称产生第二个主算法 ✅`；全文无 METHOD_SIGNAL claim |
| 10 | thesis spine 单一推荐（非选项堆） | **PASS** | §4.1 line 120 标题 `唯一推荐章节结构`（一张表）；§4.2 line 131 标题 `保守 fallback（工程贡献证据最终不足时）`——明确 fallback 条件触发，非第二并行推荐 |
| 11 | registry/session 治理正确 | **PASS** | registry `.sessions/_registry.yaml:625` `status: dormant` + line 627 `last_updated` 含 `D009 科学冻结`；thesis-writing `topic-index.md:43` 范围变更记录 `[2026-08-03] ...承接 AMC 冻结（D009）后的 campaign-level thesis contribution synthesis`；`H006-amc-dormant-closure.md` 存在（6281 B，AMC dir）；`mission-log.md:76` `## CP008: 2026-08-03 D009 AMC 科学冻结 + campaign-level thesis synthesis` |
| 12 | git diff --check 干净 | **PASS** | `git diff --check` EXIT_CODE=0；仅 6 条 LF→CRLF 警告（Windows 行尾正常提示，非 whitespace error）；无 trailing whitespace / 无 conflict marker / 无 mixed indent error |

**D009 AMC freeze + campaign-level thesis synthesis 独立 CONFIRM（12/12 PASS）**。AMC 三路线终态四源一致（registry/topic-index/master-state/decisions 全 dormant）；synthesis 9 项 inventory 证据路径全部 ls 通过；INVALIDATED（G1/P09）与 unauthorized（Q-A′）资产均未晋级、未作 bounded package 证据；DA/NDA 主方法 abstract 身份真实（adaptive CPR + CV gate + 13 dB + 0.8--1.5 dB）；工程贡献判定为 NO_SECOND_CONTRIBUTION_YET（3 理由，非机械拼接）；唯一 T3 = DA/NDA CPR；§4.1 单一推荐 spine + §4.2 标签化 fallback；bounded package 小（≤1 对话≤半天）+ 传统浮点 comparator + 预注册 PASS/FAIL + 不在本轮执行；无新方向/METHOD_SIGNAL 暗开；registry/thesis-writing/H006/CP008 治理记录齐全；git diff --check 干净。本轮未跑仿真、未修 Skill/common/params.py/正式论文/dormant receiver/4 p05 log、未进 Contract/Execute。

**允许 commit**（单 commit，不 push）。
