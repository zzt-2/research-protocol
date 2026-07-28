# Step 022 — Q15 Groundwork Step 3 精读（含两项收据前置修复）

> Task: T022 (CANDIDATE_FORMALIZATION, CP020, control epoch 52)
> Date: 2026-07-28
> Status: `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35`
> mission_method_delta: `NONE`
> claim ceiling: Q15 四判据最终状态、novelty、cheap-alt closure 因 D1/C1/C4 全文缺失
> 保持 `PENDING_STEP35`——**不是 formal Go/Kill**，不宣称 problem survives conventional
> baseline。本包价值：完成 Q15 Step 3 精读（6 独立核心 + 2 补充）+ 两项收据前置修复。

## 0. Task boundary（纪律自检）

- 仅完成 Q15 的 **Step 3 精读** + **Phase A 收据前置修复**（IEEE 第三源 raw + 5 篇 blit
  canonical receipt）。
- **已读论文全文**（6 独立核心 + 2 补充的 method + experiment，子 agent 精读）。
- **未跑任何仿真 / seed / Probe / MVE**；未改 T020/T019 代码或 artifact。
- **未进入** Step 3.5 / Step 4a / Contract / Execute。
- **未宣称** novelty / `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` / Q15 四判据全过 / 论文方法胜利。
- **D1/C1/C4 全文仍缺** → 四判据 2（信息增量）+ cheap-alt closure 保持 `PENDING_STEP35`，
  进入 Step 3.5 mandatory debt（不做第四轮下载）。
- 论文全文仅用 `tools/blit.py`（Phase A1 搜索 raw）+ T021 已获取的 content.md（Phase B 精读）；
  **未用 webReader/ResearchGate/搜索页面冒充全文**。
- D3′/D4′ 按 task 规则 5 不计独立核心数（D3/D4 的早期/长版）。
- 仅提交授权路径，未 push；未更新 `.sessions` owner / mission-log / master-state /
  current YAML / formal decisions。

## 1. Preflight

- `python .agents/skills/research-direction-lab/scripts/validate_task_control.py
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T022-q15-step3-read-with-receipt-preflight.md`
  → **PASS**
- `git status --short`（worktree 起点）→ clean（无 modified）。

## 2. Phase A — 收据前置修复

### A1. IEEE 第三源结构化 raw

**命令**（`python tools/blit.py`，未用 WebSearch/webReader）：

```powershell
python tools/blit.py "radius directed multimodulus blind equalization QAM" `
  --source ieee --format json --max 20 `
  --output projects/thesis-fso/search-archive/2026-07-28/q15-ieee-radius-receipt.json
# → 0 hits（blit 仅在有结果时保存文件；故 radius-receipt.json 未生成）

python tools/blit.py "dual polarization 16QAM blind equalization coherent" `
  --source ieee --format json --max 20 `
  --output projects/thesis-fso/search-archive/2026-07-28/q15-ieee-dualpol-receipt.json
# → 2 hits，已保存
```

**结果**：
- `q15-ieee-radius-receipt.json`：未生成（0 hits）。
- `q15-ieee-dualpol-receipt.json`：2 hits，含可审计 title/venue/url：
  1. "Bootstrapping Blind Equalizer for Dual-Polarization Coherent FSO Systems via
     Modulus-Rings-Based Variational Autoencoder"（Qin et al., TCCN 2026, IEEE doc 11237129
     — 即既有 L-ML5/qin2025-vae-blind-equalizer）
  2. "Spectrally Efficient Quadrature Duobinary Coherent Systems With Symbol-Rate Digital
     Signal Processing"（Li et al., JLT 2011, IEEE doc 5686953, 50 citations）

**A1 通过条件**：task 要求"至少一份非空，含可审计 title/document-id/venue"——dualpol receipt
满足（2 hits 含 title/venue/url/document-id）。**两份均非空条件未全达（radius 为 0），但
"至少一份非空"已满足**。无 `BLOCKED_STEP1_SOURCE_RECEIPT`。

**source union 重算**：`129` 仍只代表 S2+OpenAlex merged unique（T021 §2.3）。IEEE/blit 第 3
源的 dualpol 2 hits 是 **独立 IEEE 源**，**未偷加进 129**（task 纪律：129 不含 IEEE hits）。
actual source union = 3（S2 + OpenAlex + IEEE/blit），与 T021 一致，未变。

### A2. 五篇 blit 全文 canonical receipt

**原文件未移动/删除**（task 要求）：`papers/downloads/2026-07-28/{9492010,9333378,1561206,
1493739,10251763}.{pdf,md,meta.json}` 保持原位。

**复制为 canonical manual artifacts**（`papers/manual/{slug}/{source.pdf,content.md,metadata.json}`）：

| slug | 原 IEEE doc | SHA256(source.pdf) | content.md 行数 | title Jaccard | title_check |
|---|---|---|---|---|---|
| ieee-9492010-likelihood-rde | 9492010 | 2d93cd006259… | 418 | 1.0 | pass |
| ieee-9333378-blind-rde-likelihood | 9333378 | d5e3de4e3670… | 112 | 1.0 | pass |
| ieee-1561206-radius-adjusted-equalization | 1561206 | 6c6dc69417a6… | 682 | 1.0 | pass |
| ieee-1493739-hybrid-blind-equalization | 1493739 | 26e2f3f38631… | 299 | 1.0 | pass |
| ieee-10251763-temporal-correlation-demux | 10251763 | 0f2d3a9e6481… | 514 | 1.0 | pass |

逐篇核对：canonical `content.md ≥50` 行（全过）；SHA 与原 PDF 相同（全过）；title Jaccard=1.0
（全过，observed title 取 content.md 首个 H1，跳过 IEEE 期刊 banner 行）。**无身份不明，无
abort**。blit meta.json 的 `title_check=mismatch`（9492010/1561206/10251763）因 IEEE PDF 首行
是期刊刊头非文章标题——身份以 IEEE doc id ↔ DOI + content.md H1 双重核验为准（均 PASS）。

**metadata.json** 每篇含：expected_title、verified_title、IEEE document id、DOI（有则填）、
original_path、source=`ieee_blit`、source_pdf_sha256、title_check、title_jaccard。

**index.json 合并**：`papers/index.json` 追加 5 条 `ieee-doc:{id}` success receipt（**未覆盖
既有 11 条**，其中 3 success + 8 failed 由 T021 tools/download dry-run 生成）。

> **FR-26/TL-33 证据链纠正**：T021 worker log §6 注脚称"papers/index.json 当前为空文件"——
> **实际非空**：本包启动时 index.json 已含 4386 字节 / 11 条记录（3 success: D2/D5/C2 +
> 8 failed）。T021 该注脚是事实错误（凭记忆非证据），本包以实际 `wc -c`=4386 + `python -m
> json.tool` VALID + 11 条记录的 Read 证据纠正。本包在既有 11 条基础上追加 5 条，共 16 条。

**index/canonical receipt 表**（最终）：

| key | status | source | role |
|---|---|---|---|
| doi:10.5281/zenodo.40308 | failed | tools/download | D1 (gap) |
| doi:10.1109/ecoc.2015.7341620 | success | oa_pdf | D2 |
| doi:10.1109/lsp.2005.860544 | failed | tools/download | D3 (实际经 blit 获取，见下) |
| doi:10.1109/jlt.2021.3098220 | failed | tools/download | D4 (实际经 blit 获取，见下) |
| doi:10.3788/col202220.080601 | success | oa_pdf | D5 |
| doi:10.1109/piers-fall48861.2019.9021839 | failed | tools/download | C1 (gap) |
| doi:10.1186/s13634-015-0289-8 | success | oa_pdf | C2 |
| doi:10.1016/j.sigpro.2014.10.020 | failed | tools/download | C3 (gap) |
| doi:10.1155/2010/307927 | failed | tools/download | C4 (gap) |
| doi:10.1109/jlt.2023.3315370 | failed | tools/download | C6 (实际经 blit 获取，见下) |
| doi:10.1109/access.2021.3073246 | failed | tools/download | L011 (gap) |
| **ieee-doc:9492010** | **success** | **ieee_blit** | **D4** (本包追加) |
| **ieee-doc:9333378** | **success** | **ieee_blit** | **D4′** (本包追加, 补充) |
| **ieee-doc:1561206** | **success** | **ieee_blit** | **D3** (本包追加) |
| **ieee-doc:1493739** | **success** | **ieee_blit** | **D3′** (本包追加, 补充) |
| **ieee-doc:10251763** | **success** | **ieee_blit** | **C6/L010** (本包追加) |

**Phase A 终态**：两项收据债修复完成。无 `BLOCKED_TITLE_OR_SOURCE_IDENTITY`。进入 Phase B。

## 3. Phase B — Groundwork Step 3 精读

### B1-B2. 8 篇精读（6 独立核心 + 2 补充）

**派遣**：3 个子 agent 并行（Group1: D2/D3/D3′；Group2: D4/D4′/D5；Group3: C2/C6），各
≤15 分钟。主对话仅接收结构化提取并集成。**未用主对话 WebSearch/webReader**。

**逐篇 title/hash/line/read-note receipt**：

| ID | expected title | observed title (content.md H1) | Jaccard | verdict | SHA256(source.pdf) 前12 | 行数 | 笔记路径 |
|---|---|---|---|---|---|---|---|
| D2 | Modified radius directed equaliser for high order QAM | 同 expected (L1) | 1.0 | PASS | 4d15edb2f675 | 102 | papers/_read_notes/10.1109_ecoc.2015.7341620.md |
| D3 | A Novel Radius-Adjusted Approach for Blind Adaptive Equalization | 同 expected (L5) | 1.0 | PASS | 6c6dc69417a6 | 682 | papers/_read_notes/ieee-1561206-radius-adjusted-equalization.md |
| D3′ | Hybrid Methods for Blind Adaptive Equalization: New Results and Comparisons | 同 expected (L1) | 1.0 | PASS | 26e2f3f38631 | 299 | papers/_read_notes/ieee-1493739-hybrid-blind-equalization.md |
| D4 | Likelihood-Based Selection Radius Directed Equalizer With Time-Multiplexed Pilot Symbols for Probabilistically Shaped QAM | 同 expected (L5) | 1.0 | PASS | 2d93cd006259 | 418 | papers/_read_notes/ieee-9492010-likelihood-rde.md |
| D4′ | Blind Radius Directed Equalizer with Likelihood-based Selection for Probabilistically Shaped and High Order QAM | 同 expected (L1) | 1.0 | PASS | d5e3de4e3670 | 112 | papers/_read_notes/ieee-9333378-blind-rde-likelihood.md |
| D5 | Optimized blind equalization for probabilistically shaped high-order QAM signals | 同 expected (L5) | 1.0 | PASS | 53998b5f3af5 | 216 | papers/_read_notes/10.3788_col202220.080601.md |
| C2 | Adaptive filters: stable but divergent | 同 expected (L7) | 1.0 | PASS | 591684fdd97f | 647 | papers/_read_notes/10.1186_s13634-015-0289-8.md |
| C6 | Blind Polarization Demultiplexing of Shaped QAM Signals Assisted by Temporal Correlations | 同 expected (L5) | 1.0 | PASS | 0f2d3a9e6481 | 514 | papers/_read_notes/ieee-10251763-temporal-correlation-demux.md |

**完成矩阵**：8/8 精读合格（6 独立核心 + 2 补充）。独立核心 6 ≥ 5（gw-read 单步门槛 PASS）。
无 ABORT_TITLE_MISMATCH。每篇含 15 标准字段 + 7 结构化子表。D3/D4/C6 含写作架构提取；
D2/D3/D4/D5/C6 含实验完备性 benchmark。

### B3. Q15 综合分析

已写入 `projects/thesis-fso/literature_notes.md` 的 "Q15 Step 3 精读 + 综合分析" 节，回答
task §3 的 11 个问题。要点：

1. **机制分类**：5 类（equalizer-internal switching / output remap / distribution-aware
   radius / temporal-correlation alternative / divergence theory）。D2/D3/D4/D5 与 Q15 **动作
   族同源但信息边界不同、问题部分重叠**（详见 lit notes §1）。
2. **已知局限**：6 条原文证据（详见 lit notes §2）。
3. **趋势**：3 条方向性观察（2021+ 仅 3 篇，标 `INSUFFICIENT_EVIDENCE` 对全面趋势）。
4. **背景时间线 + Q15 定位**：Q15 在 receiver-only post-proc 层（D2-D5 在 equalizer 内，
   C6 在 TX+RX）。
5. **三差异化信息增量**：prefix-only 因果边界 / identity fallback / post-proc frozen map
   相对 D2-D5/C6 **各有真实增量**（详见 lit notes §5）——但 D1 全文缺失是关键未知。
6. **cheap-alt 吸收判断**：已获取论文中无一条能完整吸收（详见 lit notes §6）；C1/C3/C4/C5
   全文缺失 → cheap-alt closure `PENDING_STEP35`。
7. **baseline 矩阵 + comparator 候选**：fixed-µ CMA / STD-RDE / CMA-MMA（FR-25 Go
   comparator）；FDA-RDE 只作 Kill 工具。
8. **D3/D4/C6 写作架构 + 叙述骨架**：D4 独立 System Model+Algorithm Design 模式最适 Q15
   期刊论文。
9. **D2/D3/D4/D5/C6 实验完备性 benchmark**：U 普遍弱（无 CI/检验）；D4 baseline 矩阵最完整。
10. **Q15 problem table**：M-C-A 形式过判据 1/3/4；判据 2（信息增量）partial；综合
    `PENDING_STEP35`。**不记为四判据全过 Q#**。
11. **D1/C1/C4 缺失影响 + Step 3.5 targets**：D1 决定 collision 闭合；C1/C3/C4 决定
    cheap-alt closure。Step 3.5 mandatory query/citation targets 已列（lit notes §11）。

## 4. direct collision 与 cheap-alt 矩阵

### direct collision（基于已获取 6 核心；D1 全文缺失为关键未知）

| ID | 与 Q15 重叠点 | 动作族 | 信息边界 | 问题 | 碰撞程度 |
|---|---|---|---|---|---|
| D2 | 概率半径 P(r) 标量乘误差项 | 同（半径键控更新调制） | 不同（always-on 全窗） | 不同（高阶 QAM 跟踪非 collapse） | HIGH（机制）；无 identity fallback/prefix |
| D3 | region-dependent µ_i/λ_i 联合切换 | 同（radius-keyed switch） | 不同（always-on 逐符号） | 不同（性能优化非安全） | HIGH（思想源头）；无 detector/fallback |
| D4 | likelihood α-gated payload 更新 | 同（gating policy 雏形） | 部分（pilot+payload 但在线非 prefix-frozen） | 不同（PMD/SOP 非 collapse） | MEDIUM-HIGH；α 是借鉴 detector 信号 |
| D5 | peak-density K-means 估半径/分布 | 同（分布感知半径） | 不同（batch 全块） | 不同（解固定归一化半，无 detector） | MEDIUM；解 fixed-normalization 但假设内环保靠 |
| C6 | pr-MMA 概率加权 + temporal corr | 不同（TX+RX 非 post-proc） | 不同（TX+RX 非 prefix） | 部分同（CMA shaped QAM ~50% 崩） | LOW-MEDIUM（机制不同但现象佐证） |
| **D1 (gap)** | shell 分区 + soft switching | **未知（全文缺失）** | **未知** | **未知** | **最关键未知** |

**碰撞结论**：Q15 action space **不是空白**（D2-D5 在 equalizer 层有 radius/shell-键控先例）；
三差异化（prefix-only + identity fallback + post-proc frozen map）相对已获取 6 核心各有增量；
**但 D1 全文缺失使 collision 评估未闭合** → 保持 `PENDING_STEP35`。

### cheap alternative（已获取论文；C1/C3/C4/C5 gap）

| 候选 | 来源 | 吸收 Q15 问题？ |
|---|---|---|
| robust CMA (JR-CMA) | L-DP8 | 部分（AGC+重置防深衰落发散，但无 detector/fallback） |
| 换 MMA/RDE 代价 | D2/D4 | 部分（PRDE 对 16QAM 无增益[D2 显式]；LBS-RDE 解 PMD 非 collapse） |
| radius-adjusted switching | D3 | 部分（服务性能非安全，假设健康轨迹） |
| temporal-correlation pr-MMA | C6 | 否（需 TX 端，非 receiver-only） |
| l2-stability 步长界 | C2 | 否（分析框架非方法） |
| C1 null-space init / C3 MMA steady-state / C4 analytical MMA / C5 state caching | gap | **未知（全文缺失）** |

**cheap-alt 结论**：已获取论文无一条完整吸收；C1/C3/C4/C5 全文缺失 → closure
`PENDING_STEP35`。

## 5. Q15 Q# 四判据表

| 判据 | 状态 | 理由 |
|---|---|---|
| 1 具体技术矛盾（M-C-A） | ✅ 形式过 | M/C/A 三要素明确，句子级可解 |
| 2 方法产出形态 | ⚠️ partial（UNKNOWN→partial） | prefix-gated policy 有 T020 diagnostic 支撑；信息增量相对 D2-D5/C6 有（§5），但 D1 未知 |
| 3 近期 baseline 可对标 | ✅ 精读确认 | fixed-µ CMA / STD-RDE / CMA-MMA 是 2019+ 顶刊 comparator |
| 4 能做可量化对标 | ✅ 框架确认 | PI-SER/BER/NGMI vs fixed-µ CMA 可量化（D4 NGMI 框架可借鉴） |
| **综合** | **PENDING_STEP35** | 判据 2 依赖 D1；cheap-alt closure 依赖 C1/C3/C4/C5 |

**Q# 候选**：Q15 可形成 *暂定* Q# 候选（判据 1/3/4 过，判据 2 partial）。**不记为四判据全过
Q#**，不进 Contract Step 1 假设引用。

## 6. D1/C1/C4 Step 3.5 debt

| 缺失 | 改变哪项结论 | Step 3.5 mandatory target |
|---|---|---|
| **D1**（shell-partitioned MMA + soft switching, EUSIPCO 2007, 10.5281/zenodo.40308） | **最关键**。决定 Q15 shell-transport + gated action 是否被等价覆盖（判据 2、collision 闭合） | 必须获取全文。query: "shell partitioned MMA soft switching identity fallback"；citation: EUSIPCO 2007 Poznan proceedings |
| **C1**（null-space init CMA, PIERS 2019） | cheap-alt closure（初始化修复能否吸收） | 获取全文。query: "null space initialization CMA singularity dual polarization" |
| **C4**（analytical MMA, IJDMB 2010） | cheap-alt closure（换更聪明 MMA 代价能否吸收） | 获取全文。query: "analytical multimodulus algorithm blind demodulation time-varying MIMO" |
| (附带) C3（MMA steady-state, Signal Processing 2014） | cheap-alt（MMA 稳态对标） | 获取全文 |

**不做第四轮 D1/C1/C4 下载**（task 纪律 6）。进入 Step 3.5 mandatory query/citation targets，
由主控/用户裁决获取路径。

## 7. changed files、验证命令、commit SHA

### changed files（本包产出）

**gitignored（保留 worktree，不提交）**：
```text
papers/manual/ieee-9492010-likelihood-rde/{source.pdf,content.md,metadata.json}
papers/manual/ieee-9333378-blind-rde-likelihood/{source.pdf,content.md,metadata.json}
papers/manual/ieee-1561206-radius-adjusted-equalization/{source.pdf,content.md,metadata.json}
papers/manual/ieee-1493739-hybrid-blind-equalization/{source.pdf,content.md,metadata.json}
papers/manual/ieee-10251763-temporal-correlation-demux/{source.pdf,content.md,metadata.json}
papers/index.json                                              (追加 5 条 ieee-doc receipt)
papers/_read_notes/{8 篇}.md                                    (D2/D3/D3'/D4/D4'/D5/C2/C6)
projects/thesis-fso/search-archive/2026-07-28/q15-ieee-dualpol-receipt.json   (A1 blit raw)
```

**tracked（提交）**：
```text
projects/thesis-fso/literature_notes.md   (新增 "Q15 Step 3 精读 + 综合分析" 节)
projects/thesis-fso/read-log.md           (追加 8 条精读记录)
projects/thesis-fso/worker-logs/step-022-q15-step3-read.md  (本文件)
```

### 验证命令（全过）

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T022-q15-step3-read-with-receipt-preflight.md
# → PASS

python -m json.tool papers/index.json > $null
# → VALID JSON

git diff --check
# → (no whitespace errors)
```

### commit SHA
`3555f615f9ffa03db6a6b2fbc9aae69b8651ef1c`（分支 `codex/rdl-method-production-v2`，未 push）

## 8. 终态

- **status**: `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35`（6 独立核心精读合格 ≥5 门槛；
  综合分析完整；暂定 Q# 候选形成但判据 2 + cheap-alt closure pending D1/C1/C4）
- **mission_method_delta**: `NONE`（GW Step 3 精读是 formal 必经步骤，不冒充新方法进展）
- **未进入**: Step 3.5 / Step 4a / Contract / Execute / 任何实验
- **未宣称**: novelty / problem survives conventional baseline / Q15 四判据全过
- **未修改**: `.sessions/**`（owner/mission/log/decisions/master-state/current YAML）、
  T020/T019/B01-R/C11 artifacts、common/、params.py、simulator、任何实验代码
- **允许修改的文件全部落在授权路径**（§7 清单），未 push。

## 9. 验收 checklist（task §4）

- [x] Phase A 原始命令、source-union 重算、index/canonical receipt 表（§2）
- [x] 逐篇 title/hash/line/read-note receipt（§3 B1-B2 表）
- [x] 六篇核心 + 两篇补充完成矩阵（§3，6 独立核心 + 2 补充，全 PASS）
- [x] direct collision 与 cheap-alt 矩阵（§4）
- [x] Q15 Q# 四判据表（§5）
- [x] D1/C1/C4 Step 3.5 debt（§6）
- [x] changed files、验证命令、commit SHA（§7）
- [x] 只提交授权路径，未 push（§7 清单）
