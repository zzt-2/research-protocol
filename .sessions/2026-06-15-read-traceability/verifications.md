# Verifications — 2026-06-15-read-traceability

> V### 验证记录：实施验证、路线验证。每条关联 S### 或 D###。
> 结论必须是 PASS / FAIL / PARTIAL 三选一。

## V001: 精读溯源机制端到端 dry-run

- **关联**：S001（设计）+ 第 7 节实施
- **日期**：2026-06-15
- **结论**：**PARTIAL**（精读机制本身 PASS，但 dry-run 抓到数据层污染，使整体 PARTIAL）
- **执行**：executor（opus）精读 1 篇端到端跑新流程 + 主线程独立 grep 验证

### 验证对象

DOI `10.3390/photonics10080914`（index.json 标 "All-Digital OPLL for LEO Satellite"，主题看似关联 B1/A 组）。派子 agent 按 gw-read 新流程精读，产出全局笔记 + read-log。

### 机制验证（PASS）

| 验证项 | 结果 | 证据 |
|--------|------|------|
| 全局笔记产出 | ✅ | `papers/_read_notes/10.3390_photonics10080914.md`（72行，14字段齐全） |
| read-log 追加 | ✅ | `.sessions/2026-06-10-research-direction-exploration/read-log.md`（11行，7字段） |
| 源文件路径字段 | ✅ | 笔记填 `papers/doi/10.3390_photonics10080914/content.md`，路径正确 |
| 正向溯源（笔记→源文件） | ✅ | 源文件路径→content.md 文件存在 |
| 反向溯源（paper_id→笔记/log） | ✅ | paper_id 文件名→笔记存在；read-log grep 唯一命中 |
| paper_id 命名 | ✅ | `10.3390_photonics10080914`（doi 转义字面值），无歧义 |
| read-log 放置 | ✅ | 探索期放专题目录作无编号辅助文件，语义可接受 |

**结论**：精读溯源机制端到端可用，双向链路通。

### 🔴 致命发现（数据层，超精读机制范围）—— title↔content 错配

主线程独立 grep 验证（不轻信子 agent）：

- **content.md 正文实为**："Temporal Dynamics of an Asymmetrical Dielectric Nanodimer Wrapped with Graphene"（石墨烯纳米二聚体非线性动力学，line 193 真实标题）
- **metadata.json + index.json title 标**："All-Digital Optical Phase-Locked Loop for LEO Satellite Communication Terminals"，且 `download_status: success` / `content_quality: good`
- **grep 实证**：OPLL/同步词（OPLL|LEO satellite|Doppler|carrier sync|phase-locked）**0 命中**；石墨烯词（graphene|nanodimer|dimer|plasmon|dielectric）**71 命中**
- **根因**：title 数据源（检索 API / metadata.json）与 content 数据源（firecrawl 按 DOI 直抓）**不一致**。DOI `10.3390/photonics10080914` 真实指向石墨烯文章（content 抓对了），但 title 标成了 OPLL（错配源）

**系统性风险**：若 index.json 多篇 title↔content 错配，则 R002/S002 基于 title 的方向判断可能站不住（S002 粗筛留的 E1/B1/A3 等方向引用的论文 title 若错，方向可行性判断悬空）。

### 改进点清单（按优先级）

| # | 层 | 问题 | 建议 | 优先级 |
|---|----|------|------|--------|
| 1 | 数据 | title↔content 错配（系统性） | 定向审计 R002 留选方向关联论文 title；下载流水线加 title 一致性校验（用 content 真实标题回填） | **P0** |
| 2 | 流程 | gw-read 无内容身份校验 | 加 abort 协议：读 content 真实标题，与派遣 title 关键词 0 重叠则 abort 不产出 | P1 |
| 3 | 模板 | L01 "实现关键细节"字段 RL 强绑定（注解锁死奖励归一化/观测空间） | 泛化为"影响复现的工程细节（数值方法/归一化/初始化等）" | P2 |
| 4 | 模板 | "使用的 Baseline"+ 结构化 6 子表对纯理论/综述论文强加 | 按论文类型（RL/理论/实验/综述）差异化提取子集；门槛区分"有实验baseline空"vs"纯理论无baseline" | P2 |
| 5 | 流程 | content.md MDPI 导航噪声前缀（前~130-249行，8-14%） | 清洗子任务（已拆独立） | P2（已拆） |
| 6 | 机制 | paper_id 文件名可读性差（纯数字+下划线） | 笔记 frontmatter 加 title 字段，ls 能扫主题 | P3 |
| 7 | 机制 | read-log 生命周期模糊（项目锚定后删/留？多专题分散？） | 锚定后 .sessions 版本标 archived 不删；考虑全局 _index.md 总索引 | P3 |
| 8 | 模板 | "发表渠道"要求 venue 等级（SCI Q1/IF），content.md 无此信息 | venue 等级选填，或 acquire 阶段预填 metadata.json | P3 |

### dry-run 产出（待定删/留）

- `papers/_read_notes/10.3390_photonics10080914.md`（72行，石墨烯笔记 + 顶部元数据警示）
- `.sessions/2026-06-10-research-direction-exploration/read-log.md`（11行，1条记录，标记 dry-run）

**建议**：石墨烯笔记与 FSO 零相关，待 title 排查决策后处理（删笔记 / 留作警示案例）。

### dry-run 价值

**没花大力气进 Groundwork 就抓到数据污染**。若直接精读 6 方向，至少这一篇会精读错论文（石墨烯当 OPLL 读），浪费且误导方向判断。dry-run 覆盖了"机制可用性 + 数据可信度"两个维度，后者价值更高。

---

## V002: R002 留选方向论文 title 定向审计

- **关联**：V001（dry-run 发现 title 错配，触发本审计）
- **日期**：2026-06-15
- **结论**：**PARTIAL**（审计完成，但发现审计对象本身缺失——R002 论文未下载）

### 审计发现（反转预期）

R002 留选/存疑 6 方向（E1/B1/A3/A2/C2/D2）共 9 篇关键论文（7 有 DOI + 2 无 DOI）：

- **0 篇下载过**——papers/index.json（256条）和 papers/doi/（230目录）均无这 9 篇
- title↔content 错配审计对它们**无从谈起**（无 content 可比）
- R002 的 title 全来自 3-agent 广搜时检索 API 返回值，**未经任何独立验证**

### 已下载论文错配抽样

抽样 papers/ 里实际有 content.md 的 5 篇 FSO/coherent 主题论文：4 篇 title↔content 匹配，1 篇严重错配（photonics10080914 本身）。**错配率约 1/5（20%），样本极小仅供参考**。说明错配真实存在但属少数，非 100% 系统性失效。

### 对 S002 粗筛可信度的影响

- **无反证推翻 S002**：留选方向（E1/B1/A3）论文未下载，未发现错配
- **也无背书**：R002 title 来自检索 API 未验证，S002 的"TENTATIVE/摘要级/未精读"标注诚实，但事实基础（R002 title）零独立验证
- E1/B1/A3 是否真有论文支撑，**必须等下载+精读后才能确认/推翻**

### 决策结论

1. **不需要全量审计 index.json**——R002 方向论文没下载（审计不了），已下载错配是少数（20% 抽样）。全量审计是大工程收益低。
2. **治本**：下载流水线（tools/download / gw-acquire）加 title 一致性校验——下载后用 content.md 真实标题回填 index.json/metadata.json，校验 `download_status:success` 时 title 必须匹配 content。
3. **治标**：gw-read 加内容身份校验 abort 协议（V001 改进点 #2）——精读前读 content 真实标题，与派遣 title 关键词 0 重叠则 abort。
4. **精读流程修正**（research-direction-exploration）：6 方向精读启动时，第一步按 DOI 来源下载（**IEEE(`10.1109/`)/CNKI→`blit --download`**，arXiv/OA→`tools/download`；blit 不写 index.json 需手动追加）→ 第二步逐篇核 title↔content（abort 协议）→ 第三步才 gw-read 精读。**不能假设 download_status:success 等于内容正确**。

---

## V003: P0/P1 标题一致性校验落地 + 全量命中率实测

- **关联**：S001（溯源机制）+ V002 决策结论 #2/#3（治本 P0 + 治标 P1）
- **日期**：2026-06-15
- **结论**：**PASS**（photonics 回归 + 全量扫描实证 + 三类误报已修，残留 18 mismatch 绝大多数是真损坏）

### 实施清单（5 文件）

| # | 文件 | 改动 |
|---|------|------|
| 1 | `tools/litdownload/title_verify.py`（新） | 纯函数模块：`extract_real_title`/`classify_mismatch`/`title_overlap`/`verify_pdf_title` + CLI（`python -m litdownload.title_verify <path>`） |
| 2 | `tools/litdownload/download_output.py` | `_save_metadata` 加 `real_title`/`title_check`/`title_overlap` 三字段（向后兼容） |
| 3 | `tools/litdownload/download_pipeline.py` | 新增 `_compute_title_check`；batch + single 两路下载后调用，metadata.json + index.json 双写 `title_check` |
| 4 | `tools/blit.py` | IEEE/CNKI 下载后 `verify_pdf_title`，结果写 `{pdf_stem}.meta.json` sidecar（复用 title_overlap，不接 index.json） |
| 5 | `stages/gw-read.md` | 操作段加"步骤 0：源文件 title 自检（abort 协议）"；派遣清单加 #7 派遣标题 [MUST]；质量门槛加 title-mismatch 不计入 ≥5 篇 |

### 回归验证

**photonics 案例（V001/V002 的原始触发点）**：CLI 重跑 → `mismatch, overlap=0.000`，真标题正确提取为"Temporal Dynamics of an Asymmetrical Dielectric Nanodimer Wrapped with Graphene"。**PASS**。

**全量扫描（237 篇 success 下载，非 dry-run）**：

| 状态 | 数量 | 占比 |
|------|------|------|
| match | 109 | 46.0% |
| mismatch | 18 | 7.6% |
| unverifiable | 110 | 46.4% |

- **unverifiable 110 篇（46.4%）**：arxiv_latex（pandoc 丢 \title{}，按计划跳过）+ arXiv 单篇下载 title 字段为 URL + manual 论文 title 为 slug + 垃圾/极短 content.md。这些不是损坏，是基准不可信——正确归类。
- **mismatch 18 篇逐篇分类**：
  - **真损坏（约 14 篇）**：firecrawl 抓到 bot 墙（"Let's confirm you are human" ×3）、paywall/block 页（"wiley.scienceconnect.io is blocked"/"Access to this work was provided by"）、抓错期刊（"Results in Optics"/"Physical Communication"/"SCIENCE CHINA"）、抓错论文（photonics/electronics14122367 real=完全不同主题）、content 截断（"Data availability"/"Article contents"）。**全部是真下载损坏，校验正确捕获。**
  - **提取器边缘（约 4 篇）**：real 提到了公式行（"vi,j,k=..."）、算法标题（"Algorithm 1 WGS..."）、正文片段（"beamforming gain, massive antenna arrays"）。content.md 可能没问题但提取器抓错位置 → 标 mismatch 触发人工复核，保守可接受。

### 实施中发现并修复的 3 类误报

首轮全量扫描 32 mismatch，修复后降到 18：

| 类 | 问题 | 修复 | 解决数 |
|----|------|------|--------|
| B | MDPI 论文 firecrawl 输出无 H1 论文标题，提取器抓到 `## 2. Section` 正文小节标题 | `_is_nav_heading` 加编号小节模式（`N.`/`N.M`/`Section N`/罗马数字） | ~6 |
| C | slug 检测漏掉 `network-00015`（只 1 个连字符，旧规则要求 ≥3 段） | 改为"无空格+连字符+数字"即判 slug | ~4 |
| D | 合法标题变体 overlap 0.33-0.36（GraphVNE/Dueling DDQN）被误判 | 加"首词挽救"：首词 ≥4 字符且在 real 标题中出现则判 match | ~4 |

### blit 路验证

- `verify_pdf_title` 在无 pymupdf 环境下返回 `unverifiable` 不崩溃（PASS，graceful degradation）
- blit.py import OK，`_TITLE_VERIFY_AVAILABLE=True`，`_save_title_meta` 可调用
- **未做实下载验证**：papers/downloads/ 不存在（R002 9篇未下载），需等实际 blit --download 时验证 sidecar 写入。记为已知未验证项。

### 已知边界（声明，不解决）

1. **blit sidecar 不触发 gw-read abort**：blit 下的 PDF 是平铺布局（`{arnumber}.pdf`），不在 `papers/{type}/{id}/content.md`。gw-read abort 协议对 blit 论文需先 `tools/convert` 转 content.md 放进 papers/doi/ 才生效。这是 H001 路径 B 既定流程，不在本专题扩张。
2. **unverifiable 110 篇无校验**：arxiv_latex（28）+ URL/slug title 的论文靠 arxiv_id/paper_id 做权威 key，title 错配风险本就低，按计划跳过。
3. **公式/算法误提（4 篇）**：提取器在 firecrawl 输出无 H1 时回退到"第一个非 nav 行"，偶尔抓到公式。保守标 mismatch 触发复核，不阻塞。

### 对决策的影响

- **V002 决策 #2（治本 P0）落实**：下载流水线已加 title 校验，后续下载自动标 mismatch。
- **V002 决策 #3（治标 P1）落实**：gw-read abort 协议已写入框架文件。
- **V002 决策 #4（精读流程修正）仍待执行**：本专题只造工具，R002 9 篇实下载 + 精读是 research-direction-exploration 主线工作（H001 路径 B），不在本专题。
- **回溯校验历史 256 篇**：按 V002 决策 #1 不全量回写 metadata.json，但 `python -m litdownload.title_verify <path>` 可按需手动跑（本 V003 的 18 mismatch 列表即此方式产出，供人工选择性修复）。

### 后续：81 篇 unverifiable 回填（V003b，同日追加）

unverifiable 110 篇里**65+ 篇是"可救"的**——metadata title 是空/URL/slug（基准无效），但 content.md 明明提取到 high 置信真标题。写了 `tools/backfill_titles.py`（带 dry-run + 审计日志），安全边界四条全满足才回填：

1. 当前 `title_check ∈ {unverifiable, None}`（绝不碰 match/mismatch）
2. metadata title 是 empty/url/slug（绝不覆盖已有真标题）
3. `extract_real_title` 返回 `confidence == 'high'`
4. 非垃圾 content.md（垃圾检测在 extract 内已挡）

**实测回填 81 篇**（比预估 65 多，因放宽到 None 也回填）：80 篇 → match（overlap=1.0，因回填后 title==real_title），1 篇 → unverifiable（`'O R I G I N A L A R T I C L E'`，提取到期刊 banner 而非论文标题，正确标 unverifiable 不掩盖）。

**回填后全量验证（安全 PASS）**：

| 状态 | 回填前 | 回填后 | 变化 |
|---|---|---|---|
| match | 109 (46.0%) | **173 (73.0%)** | +64 |
| **mismatch** | **18 (7.6%)** | **18 (7.6%)** | **0（真损坏一个没被掩盖）** |
| unverifiable | 110 (46.4%) | **46 (19.4%)** | -64 |

18 个 mismatch 逐篇与回填前一致（photonics/electronics14122367/bot墙/paywall 全在，overlap 数字一字不差）。残留 46 unverifiable = arxiv_latex 28（pandoc 丢标题，跳过）+ 真提取不到标题 12 + 垃圾/反爬 5 + banner 误提 1。

审计日志：`.sessions/2026-06-15-read-traceability/backfill-log.md`（81 篇逐条 old→new）。

**结论**：回填只动了 unverifiable 里的"基准无效"类，没碰任何 mismatch，安全。回填后 metadata.json 的 title 字段是真标题，下游（literature_notes/gw-read 派遣标题/index.json 检索）可直接用，不再依赖 arxiv_id 间接定位。

---

## V003c: 回填标题 API 交叉验证 + 4 篇回滚

- **关联**：V003b（回填）+ 用户质疑"别弄到乱七八糟的"
- **日期**：2026-06-15
- **结论**：**PARTIAL → 修复后 PASS**（回填主力集可信，但抓出 4 篇系统性回填错误并已回滚）

### 触发

用户指出："之前经常发现后来 doi 和实际对不上，或者作者不对"。V003b 回填只验证了"提取出 high 置信标题"，**没验证这个标题真的是 metadata 里 arxiv_id/DOI 所指那篇论文的标题**。如果 content.md 当初就抓错了页面，回填的是**另一篇论文的标题**，比空标题更危险（看起来正确了）。

### 验证方法（不信任 content.md，不自己验证自己）

派子 agent 对 67 篇可 API 验证的回填论文（46 arxiv + 21 DOI，14 manual 跳过）：
- arxiv_id → arxiv API（`id_list` 批量查）官方标题
- DOI → Semantic Scholar API 官方标题
- 官方标题 vs 回填标题 token Jaccard ≥0.6 = 吻合

### 结果

| 类别 | 验证 | 吻合 | 不吻合 |
|---|---|---|---|
| arxiv（44 篇 API 成功）| 44 | **44 (100%)** | 0 |
| DOI（23 篇 API 成功）| 23 | 19 (83%) | **4** |
| manual（14 篇）| 跳过 | — | — |

**4 篇不吻合（全部 content.md 抓错页面）**：

| paper_id | 回填标题 | 官方标题 | 判断 |
|---|---|---|---|
| `10.1016/j.ast.2026.112361` | Aerospace Science and Technology | GNN-ASSSP... LEO Satellite | 期刊名，method=all_failed |
| `10.1038/s41598-026-40704-2` | orts Scientific Rep | Robust high-capacity FSO using OAM... | 页眉碎片，method=unpaywall |
| `10.1109/taes.2026.3652971` | 60%. Compared with the baseline... | A Service-Oriented Multipath Routing... | 正文段落，method=all_failed |
| `10.1038/s41598-025-17852-y` | OPEN Secure and energy-efficient... | Secure and energy-efficient transmission... | OPEN 前缀泄漏，核心标题对 |

**根因**：4 篇里 3 篇 method=`all_failed`（firecrawl/unpaywall 全失败，content.md 本就残缺），1 篇 method=`unpaywall` 也抓到残缺页。`all_failed` 是问题充分条件。

### 修复

1. **回滚 3 篇**（ast.2026 / s41598-026-40704-2 / taes.2026）：清空 title + 标 unverifiable + 加 `title_backfill_rolled_back` 字段记原因
2. **清理 1 篇**（s41598-025-17852-y）：剥 `OPEN ` 前缀，核心标题保留
3. **backfill_titles.py 加双重守卫**：
   - 边界 0：`method=all_failed` 直接禁回填（主力防线）
   - 边界 5：`_looks_like_non_title` 启发式二次校验（捕获期刊名/页眉碎片/正文段落/词数过少），作为 method guard 的补充
4. 守卫实测：4 类失败模式全部被捕获（3 method guard + 1 heuristic），4 个真标题不被误拒

### 回滚后最终全量

| 状态 | 回填前 | V003b 回填后 | V003c 回滚后 |
|---|---|---|---|
| match | 109 (46.0%) | 173 (73.0%) | **172 (72.6%)** |
| mismatch | 18 (7.6%) | 18 (7.6%) | **18 (7.6%, 不变)** |
| unverifiable | 110 (46.4%) | 46 (19.4%) | **47 (19.8%)** |

回滚后 match 减 1（173→172，因 3 篇清空 + 1 篇清理后仍 match 净变化 -1），mismatch 仍 18 不变。

### 教训（写入 code-quality.md 候选）

- **自己验证自己是循环论证**：V003b 只用 extract_real_title 自检 high 置信就回填，没用独立权威源交叉验证。子 agent API 验证才发现 4 篇系统性错误。
- **method=all_failed 是危险信号**：content.md 来源不可靠时，再"自信"的提取也是垃圾进垃圾出。
- **"看起来正确"比"明确缺失"更危险**：空标题下游知道要补；错标题（期刊名当论文标题）下游会直接用，污染 literature_notes/gw-read 派遣。

### 残留未验证

- **14 篇 manual 论文**：无 arxiv_id/DOI，无法 API 验证。其中 `jang-etri-2026` 回填值是 `O R I G I N A L A R T I C L E`（字母带空格，强烈疑似期刊 banner），已标 unverifiable。其余 13 篇需人工抽检 content.md 确认（新对话或实战精读时做）。



