# Step 021 — Q15 prefix-gated shell calibration Groundwork Step 1–2

> Task: T021 (CANDIDATE_FORMALIZATION, CP019, control epoch 51)
> Date: 2026-07-28
> Status: `AWAITING_DELEGATED_COVERAGE_GATE`
> mission_method_delta: `NONE`
> claim ceiling: Q15 仍是**暂定问题假说**，未过四判据，非 formal Go/Kill。
> 本包价值：决定 T020/M4 诊断信号能否合法继续（formal collision + cheap-alt coverage）。

## 0. Task boundary（纪律自检）

- 仅完成 Q15 的 Groundwork **Step 1 检索**与 **Step 2 公共全文获取 / coverage-gap report**。
- **未读论文全文**（只 title/abstract/metadata 初筛 + Step 2 的 title-identity/content 行数/SHA256 质量检查，未读 method/experiment）。
- **未写 Step 3 精读条目**；Q15 四判据全部保持 **UNKNOWN / NOT_ADJUDICATED**。
- **未跑任何仿真 / seed / Probe / MVE**；未改 T020 code/artifact，未补 gate receipt。
- **未把 T020 signal 写成 Q15 四判据 PASS / novelty / 论文方法胜利**。
- **未执行或修改 Q14/T018**；未进入 Step 3.5 / Step 4a / Contract / Execute。
- 论文全文仅用 `tools/download` / `tools/blit --download` / `tools/convert` 获取；**未用 webReader/ResearchGate/搜索页面冒充全文**。
- 三轮下载止损后，失败项进入 coverage gap；未绕过。
- 仅提交授权路径，未 push；未更新 `.sessions` owner / mission-log / master-state / current YAML / formal decisions。

## 1. Preflight

- `python .agents/skills/research-direction-lab/scripts/validate_task_control.py
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T021-q15-groundwork-step1-2.md`
  → **PASS**
- `git status --short`（worktree 起点）→ clean。

## 2. Phase A — Groundwork Step 1 检索

### 2.1 全仓去重结论

既有 `literature_notes.md` / `papers/` / `search-archive/_index/all-papers.jsonl`
对 Q15 四条检索线的覆盖**接近空白**（仅 Q14/S038 同族暂存 + L-DP8 JR-CMA 邻近 +
sat.1553§6 共识盲区 + L07 CMA/RDE 并行）。无既有 Q15 专属全文池。无已 Kill 的
exact construct 复用风险（T019 M3/M5 已被 V052 Kill 的 causality-leak 构造在本包
不复用；Q15 M1–M4 全部 prefix-only，已过 5/5 TDD）。

### 2.2 检索执行（11 query，2 轮）

- **工具**: `bash tools/search`（实际命中源 Semantic Scholar + OpenAlex）+ `bash
  tools/blit --source ieee`（Playwright IEEE Xplore，第 3 源）。
- **raw 文件**（13 个，路径见 candidate-map §0）：4 条线 × (broad + targeted)，每条
  线含 optical/coherent/dual-pol/16QAM 层与一般 digital comms 层。
- **未用主对话 WebSearch/webReader**（遵守 §2.2）。

### 2.3 Step 1 质量门（全部 PASS，详见 `search-archive/2026-07-28/q15-step1-candidate-map.md`）

| 门 | 阈值 | 实测 | 状态 |
|---|---|---|---|
| unique count | ≥20 | **129** | ✅ |
| source union | ≥3 | **3** (S2 + OpenAlex + IEEE/blit) | ✅ |
| 必读 | ≥5 | **11** | ✅ |
| published ratio | ≥50% | **93.8%** (121/129) | ✅ |
| 技术路线 | ≥2 | **4** (radius/MMA/shell；CMA singularity/restart/init；blind AGC/scale；distribution/quantile) | ✅ |

priority 分布：必读 11 / 建议读 13 / 待确认 2 / 备选 16 / 排除 87。
未触发第 3 轮检索；**无 BLOCKED_STEP1_COVERAGE**。

### 2.4 直接碰撞 vs 廉价替代（分开，§2.3 强制）

**直接碰撞（direct collision）**——与 Q15 action（prefix-gated identity/quantile-shell
radius transport）+ information boundary（prefix-only）+ problem（fixed-μ CMA 内环
塌缩部分恢复）三者同时重叠的候选：

| ID | 论文 | 碰撞点 | 程度 |
|---|---|---|---|
| D1 | Shell-Partitioned MMA + Soft Switching (EUSIPCO 2007, 10.5281/zenodo.40308) | shell 分区 + soft switching（动作机制最接近 M4+M2/M3） | HIGH（但 always-on 抽头，无 prefix 因果边界） |
| D2 | Modified RDE for high-order QAM (ECOC 2015, 10.1109/ecoc.2015.7341620) | 概率 radius 更新（radius 重映射同族） | HIGH |
| D3 | A Novel Radius-Adjusted Approach (IEEE SPL 2006, 10.1109/lsp.2005.860544) | region-dependent（按输出 radius 分区）步长/权重切换 | HIGH（radius-gated 切换思想同源） |
| D4 | Likelihood-Based Selection RDE + pilot (JLT 2021, 10.1109/jlt.2021.3098220) | likelihood-based payload 盲 radius 分配 | MEDIUM-HIGH |
| D5 | Optimized blind eq for PS high-order QAM (COL 2022, 10.3788/col202220.080601) | peak-density K-means 跟踪 amplitude radius/distribution | MEDIUM |
| D6 | Time Reverse Eq for 16QAM PDM (Access 2021, 10.1109/access.2021.3073246) | 同场景（16QAM PDM），机制不同（改代价） | LOW-MEDIUM |

**碰撞小结**：Q15 action space **不是空白** —— D1/D3 已在 equalizer 层做过"按
radius/shell 分区切换"核心思想；D2/D4/D5 在 radius-directed / distribution-based
radius 跟踪有成熟先例。Q15 差异化必须落在：(a) **prefix-only 因果边界**（D1–D6 全
是 always-on 在线更新，无此边界）；(b) **identity fallback 健康零回归**（D1–D6 无
安全分支）；(c) **post-proc frozen map 而非 equalizer 抽头/代价修改**。是否构成
"同一 action+information+problem"直接碰撞，需 Step 2 全文 + Step 3 精读判断。

**廉价替代（cheap alternative）**——可能用更便宜的稳健 CMA/RDE/MMA/重启/初始化吸收
Q15 问题的候选：C1 Null-Space Init (PIERS 2019)、C2 Adaptive filters stable but
divergent (EURASIP 2015)、C3 MMA steady-state (Signal Processing 2014)、C4 Analytical
MMA (IJDMB 2010)、C5 Equalizer State Caching (JLT 2021)、C6 Blind Pol Demux temporal
corr (JLT 2023/2024)、C7 dual-mode switching (2006)、C8 智能 GA/正交初始化 (2008)。
存在**多条**可能吸收 Q15 问题的 cheaper 路径（初始化修复 / 换 MMA/RDE 代价 / state
caching / dual-mode switching）。Q15 post-proc prefix-gated frozen map 必须证明比这些
cheaper 替代多出"健康零回归 + receiver-visible collapse detect"的独特价值。

## 3. Phase B — Groundwork Step 2 公共全文获取

Step 1 门全过 → 执行 Step 2。按 §3.1 优先级（direct collision > robust/restart cheap
alt > radius/distribution mechanism > general background）选 **11 篇**，先查共享
`papers/` 是否已存在合法 content.md（Q15 候选均不存在），再 `--dry-run` → 三轮止损。

### 3.1 获取结果（11 attempted → 8 成功 + 1 质量不达标 + 5 失败进 gap）

**成功获取（8 篇，content ≥50 行，title identity PASS，SHA256 已记）**:

| ID | 标题 | 年/venue | DOI / 来源 | 路径 | 行数 | source | SHA256(source.pdf) 前12 |
|---|---|---|---|---|---|---|---|
| D2 | Modified radius directed equaliser for high order QAM | 2015 ECOC | 10.1109/ecoc.2015.7341620 | `papers/doi/10.1109_ecoc.2015.7341620/` | 102 | oa_pdf | 4d15edb2f675… |
| D5 | Optimized blind equalization for PS high-order QAM | 2022 COL | 10.3788/col202220.080601 | `papers/doi/10.3788_col202220.080601/` | 216 | oa_pdf | 53998b5f3af5… |
| C2 | Adaptive filters: stable but divergent | 2015 EURASIP | 10.1186/s13634-015-0289-8 | `papers/doi/10.1186_s13634-015-0289-8/` | 647 | oa_pdf | 591684fdd97f… |
| D4 | Likelihood-Based Selection RDE + pilot for PS-QAM | 2021 JLT | 10.1109/jlt.2021.3098220 | `papers/downloads/2026-07-28/9492010.{pdf,md}` | 418 | ieee/blit | 2d93cd006259… |
| D4′ | (ECOC 2020 早期版) Blind RDE likelihood selection PS/high-order QAM | 2020 ECOC | ieee 9333378 | `papers/downloads/2026-07-28/9333378.{pdf,md}` | 112 | ieee/blit | d5e3de4e3670… |
| D3 | A Novel Radius-Adjusted Approach for blind adaptive eq | 2006 SPL | 10.1109/lsp.2005.860544 | `papers/downloads/2026-07-28/1561206.{pdf,md}` | 682 | ieee/blit | 6c6dc69417a6… |
| D3′ | (ISCC 2005 长版) Hybrid Methods for Blind Adaptive Equalization | 2005 ISCC | ieee 1493739 | `papers/downloads/2026-07-28/1493739.{pdf,md}` | 299 | ieee/blit | 26e2f3f38631… |
| C6/L010 | Blind Polarization Demultiplexing of Shaped QAM (temporal corr) | 2024 JLT | 10.1109/jlt.2023.3315370 | `papers/downloads/2026-07-28/10251763.{pdf,md}` | 514 | ieee/blit | 0f2d3a9e6481… |

> 说明：blit 下载的 PDF `meta.json` `title_check=mismatch` 是因为 IEEE PDF 首行是
> 期刊刊头（如 "JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 42..."）而非文章标题——这是
> blit 的已知表现，**身份以 IEEE document ID ↔ DOI 解析 + 转换后 md 首个标题行双重
> 核验为准**（均 PASS，见 §3.3）。

**内容不达标（1 篇， watermark-only，未进精读池）**:
- `papers/downloads/2026-07-28/4458069.{pdf,md}`（FPGA configurable equalizer，bonus）
  → md 仅 8 行，全是 "Authorized licensed use limited to BEIJING INSTITUTE OF
  TECHNOLOGY... Restrictions apply" 水印，正文被 IEEE 反爬拦截。**丢弃，不计入成功**。

### 3.2 三轮止损执行记录

| 轮 | 通道 | 成功 | 失败 |
|---|---|---|---|
| 1 | `tools/download`（arXiv HTML/LaTeX/PDF, OA PDF, Unpaywall） | 3（D2/D5/C2，均 oa_pdf） | 8 |
| 2 | `tools/download --force`（重试 OA/Unpaywall；无 arxiv_id 可走 arXiv 通道） | 0 | 7（同上失败集，OA flag 但 PDF 解析/重定向失败） |
| 3 | `tools/blit --source ieee --download`（IEEE 校园网机构认证） | 4 目标 + 2 bonus = 6 PDF（5 内容达标：D4/D4′/D3/D3′/L010；1 仅水印弃） | D1/C1/C3/C4/L011（非 IEEE 或 blit 搜不到） |

**止损触发**：三轮后仍失败的进入 coverage gap（§4）。**未尝试第四轮，未用 webReader/ResearchGate 冒充全文**。

### 3.3 身份与质量检查（§3 step 5，逐篇）

每篇检查：title identity（DOI/IEEE doc id + 转换后 md 首个标题行双重核验）、metadata
来源、content.md 有效行数 ≥50、SHA256。8 篇成功项全部 PASS（见上表行数 + §3.1 SHA256）。
**未读 method/experiment 内容**（只做质量检查，不进精读）。

## 4. 文献覆盖面状态（§3.1 强制暂停门）

### 4.1 成功获取（8 篇）
见 §3.1 表。覆盖：direct collision D2/D3/D4/D5（4 篇核心 radius/shell 碰撞 + D4′/D3′
两个早期/长版）+ cheap-alt C2（发散理论）+ C6/L010（PCS-QAM 盲均衡机制）。

### 4.2 内容不达标（1 篇）
- 4458069 FPGA configurable equalizer（bonus）→ IEEE 反爬 watermark-only，8 行，弃。

### 4.3 下载失败（5 篇进 coverage gap）

| ID | 标题 | DOI | 为什么重要 | 三轮失败原因 |
|---|---|---|---|---|
| **D1** | Shell-Partitioned MMA + Soft Switching (256/1024 QAM) | 10.5281/zenodo.40308 | **最直接的 shell 分区 + soft switching 碰撞**（M4 gated + M2/M3 shell transport 的动作机制最近邻） | Zenodo OA flag 但 tools/download 解析失败；非 IEEE，blit 不可用 |
| C1 | Null Space Init for CMA (MIMO) | 10.1109/PIERS-Fall48861.2019.9021839 | cheap-alt（初始化修复 CMA singularity） | IEEE PIERS 但 blit 标题搜不到；IEEE paywall |
| C3 | Steady-state performance of MMA | 10.1016/j.sigpro.2014.10.020 | cheap-alt（MMA 稳态 EMSE 解析，对标"换 MMA 代价"） | Elsevier OA flag 但解析失败；非 IEEE |
| C4 | Analytical MMA (time-varying MIMO) | 10.1155/2010/307927 | cheap-alt（analytical MMA，比 MMA 更低残差） | Hindawi OA pdf_url 但 tools/download 解析失败；非 IEEE |
| L011 | Time Reverse Eq 16QAM PDM | 10.1109/access.2021.3073246 | direct collision D6（同场景 16QAM PDM） | IEEE Access 但 blit 标题搜返回 0；IEEE paywall |

### 4.4 source / venue / 年份 / 正式发表覆盖

- **正式发表**: 8/8 成功项全部正式发表（ECOC/COL/EURASIP/JLT×3/SPL/ISCC）。published
  ratio 100%。
- **venue 覆盖**: JLT Q1 ×2（D4/L010）+ ECOC ×2（D2/D4′）+ SPL（D3）+ EURASIP（C2）+
  COL（D5）+ ISCC（D3′）。**缺**: IEEE Trans（TWC/TCOM/JLT 之外的）、Elsevier Signal
  Processing（C3 fail）。
- **年份**: 2005–2024，覆盖经典（D3 SPL 2006 radius-adjusted 思想源头）到近期（L010
  JLT 2024 PCS-QAM）。

### 4.5 direct collision 覆盖

- **已覆盖**: D2（modified RDE）/ D3（radius-adjusted SPL，思想源头）/ D4（likelihood
  RDE JLT）/ D5（PS-QAM K-means radius）+ D4′/D3′ 早期版。**4 个核心 direct collision
  全文已获取**。
- **未覆盖（gap）**: **D1（shell-partitioned MMA + soft switching，EUSIPCO 2007）**——
  这是与 Q15 M4+M2/M3 动作机制**最近邻**的碰撞，摘要仅 1 行（"Publication in the
  conference proceedings of EUSIPCO, Poznan, Poland, 2007"），无方法细节。**D1 全文
  会显著改变 direct-collision 判断**（若 D1 的 shell 分区 + soft switching 已等价于
  Q15 的 gated identity/transport，则 Q15 novelty 大幅缩水）。

### 4.6 cheap alternative 覆盖

- **已覆盖**: C2（CMA 发散理论）/ C6（PCS-QAM 盲均衡 temporal corr）。
- **未覆盖（gap）**: C1（null-space init）/ C3（MMA steady-state）/ C4（analytical
  MMA）—— 这三条是"换初始化 / 换 MMA 代价" cheaper 路径的代表。**C1/C3/C4 全文会改
  变 cheap-alt 吸收判断**（若这些方法已能在 dual-pol 16QAM 内环塌缩场景稳定收敛，
  则 Q15 问题被吸收，无需 post-proc）。

### 4.7 哪些失败全文会改变判断

1. **D1（shell-partitioned MMA + soft switching）** —— **最关键**。决定 Q15 的
   shell-transport + gated action 是否已被等价做过。摘要无方法细节，必须全文。
2. **C1（null-space init）/ C3（MMA steady-state）/ C4（analytical MMA）** —— 决定
   "更便宜的 CMA 初始化/MMA 代价修复"能否吸收 Q15 问题。三者均 cheap-alt 代表。
3. L011（time-reverse 16QAM PDM）—— 同场景碰撞 D6，影响小（机制不同）。

### 4.8 建议 coverage gate

**建议: `PARTIAL`**

理由（事实）:
- ✅ Step 1 门全过（unique 129 / source 3 / 必读 11 / published 93.8% / 4 路线），
  无 Step 1 阻塞。
- ✅ 4 个核心 direct collision（D2/D3/D4/D5）全文已获取，足以判断 Q15 action space
  **不是空白**（radius/shell 分区切换在 equalizer 层有成熟先例）。
- ✅ cheap-alt 的理论侧（C2 发散理论）+ 机制侧（C6 PCS-QAM）已覆盖。
- ⚠️ **关键缺口**: D1（shell-partitioned MMA + soft switching，与 Q15 动作机制最近邻）
  全文未获取，摘要仅 1 行无方法细节 → **无法确认 Q15 gated identity/transport 是否
  已被 D1 等价覆盖**。
- ⚠️ cheap-alt 的方法侧（C1/C3/C4）未获取 → **无法确认 cheaper 初始化/MMA 代价修复
  能否吸收 Q15 问题**。

**不下 `PASS`**：D1 是 direct-collision 判断的最关键未知，其全文缺失使 collision
评估无法闭合。**不下 `FAIL`**：4 个核心 direct collision 已获取，Step 1 门全过，
不是系统性覆盖失败。**`PARTIAL`**：主控可据此裁决（a) 接受带 D1/C1/C3/C4 债务进
Step 3 精读已获取的 8 篇；(b) 要求用户手动获取 D1/C1/C3/C4 后再进 Step 3；(c) 因
D1 碰撞风险判 BLOCKED_DIRECT_COLLISION。

## 5. 终态

- **status**: `AWAITING_DELEGATED_COVERAGE_GATE`（Phase B 完成，停在 gate，等主控验收）
- **mission_method_delta**: `NONE`（formal Groundwork 必经步骤，不冒充新方法进展；
  CP019 已记录 T020 METHOD_SIGNAL，本包价值是决定该信号能否合法继续）
- **未进入**: Step 3 精读 / Step 3.5 / Step 4a / Contract / Execute / 任何实验
- **未修改**: `.sessions/**`（owner/mission/log/decisions/master-state/current YAML）、
  T020/T019/B01-R/C11 artifacts、common/、params.py、simulator、任何实验代码
- **允许修改的文件全部落在授权路径**（§4 清单），未 push。

## 6. 授权路径文件清单（本包产出）

```text
projects/thesis-fso/search-archive/2026-07-28/q15-t1-broad-agc-scale.json
projects/thesis-fso/search-archive/2026-07-28/q15-t1b-broad-blind-agc-optical.json
projects/thesis-fso/search-archive/2026-07-28/q15-t2-broad-radius-mma.json
projects/thesis-fso/search-archive/2026-07-28/q15-t2-dir-radius-dp-optical.json
projects/thesis-fso/search-archive/2026-07-28/q15-t3-broad-cma-singularity-restart.json
projects/thesis-fso/search-archive/2026-07-28/q15-t3b-broad-cma-restart-multistart.json
projects/thesis-fso/search-archive/2026-07-28/q15-t3-dir-singularity-twostage.json
projects/thesis-fso/search-archive/2026-07-28/q15-t4-broad-distmatch-histogram.json
projects/thesis-fso/search-archive/2026-07-28/q15-t4b-broad-histogram-postproc.json
projects/thesis-fso/search-archive/2026-07-28/q15-t4-dir-ps-qam-radius.json
projects/thesis-fso/search-archive/2026-07-28/q15-t1-dir-dd-mma-scaled.json
projects/thesis-fso/search-archive/2026-07-28/q15-merged-unique.json
projects/thesis-fso/search-archive/2026-07-28/q15-merged-annotated.json
projects/thesis-fso/search-archive/2026-07-28/q15-step1-candidate-map.md
projects/thesis-fso/search-archive/2026-07-28/q15-step2-download-input.json
projects/thesis-fso/search-archive/2026-07-28/q15-step2-round2-input.json
projects/thesis-fso/literature_notes.md                                    (仅新增 Q15 Step 1–2 pending 小节)
projects/thesis-fso/worker-logs/step-021-q15-groundwork-step1-2.md         (本文件)
```

**共享 `papers/` 仅新增合法 paper artifact（未修改既有文件）**:
```text
papers/doi/10.1109_ecoc.2015.7341620/{source.pdf,content.md,metadata.json}        (D2, OA, tools/download)
papers/doi/10.3788_col202220.080601/{source.pdf,content.md,metadata.json}         (D5, OA, tools/download)
papers/doi/10.1186_s13634-015-0289-8/{source.pdf,content.md,metadata.json}        (C2, OA, tools/download)
papers/downloads/2026-07-28/{9492010,9333378,10251763,1561206,1493739,4458069}.{pdf,md,meta.json}  (blit IEEE; 4458069 watermark-only 弃)
```

> `papers/downloads/2026-07-28/` 是 blit 下载目录（tools-guide §3 约定），与共享权威根
> `papers/{arxiv|doi|manual}/` 并行；blit 下载按 gw-acquire 规则需手动 convert（已做）+
> 手动追加 index.json（**本包未追加 papers/index.json —— papers/index.json 当前为空文件，
> 且任务 §4 授权路径未列 papers/index.json，故不动**；若主控要进 Step 3，需先补 index.json）。

## 7. 验收 checklist（§5）

- [x] ≥8 query 且两轮检索完成，raw 路径可复现（11 query，2 轮，13 raw 文件）
- [x] Step 1 数量/来源/路线/正式发表门均有数字（129 / 3源 / 4路线 / 93.8%）
- [x] direct collision 与 cheap alternative 分开（§2.4 + candidate-map §6/§7）
- [x] 8–12 篇选择与每篇 title/path/hash/line count 可审计（§3.1，11 attempted → 8 成功）
- [x] coverage report 完整并停在 gate（§4，status AWAITING_DELEGATED_COVERAGE_GATE）
- [x] 未读全文、未实验、未进入 Step 3+（§0 纪律自检）
- [x] 只提交授权路径，未 push（§6 清单）
