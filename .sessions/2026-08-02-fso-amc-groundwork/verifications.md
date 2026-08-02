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
