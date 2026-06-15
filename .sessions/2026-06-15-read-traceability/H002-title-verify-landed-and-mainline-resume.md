# Handoff: P0/P1 标题一致性校验全部落地 + 回填 + API 交叉验证 + 回主线精读

> 来源: S002(read-traceability) + V003/V003b/V003c | 交接目标: research-direction-exploration（R002 9篇下载+精读，H001 路径 B）
> 文件名: H002-title-verify-landed-and-mainline-resume.md

## 已完成边界（本轮全部完成）

**P0 治本 + P1 治标（5 文件，V003 PASS）**：

| 文件 | 改动 |
|---|---|
| `tools/litdownload/title_verify.py`（**新**） | 纯函数：`extract_real_title`/`classify_mismatch`/`title_overlap`/`verify_pdf_title` + CLI `python -m litdownload.title_verify <path>`。按 download_method 分派（arxiv_html 锚 .ltx_title_document / 其余通用 heading / arxiv_latex 跳过）|
| `tools/litdownload/download_output.py` | `_save_metadata` 加 `real_title`/`title_check`/`title_overlap` 三字段（向后兼容）|
| `tools/litdownload/download_pipeline.py` | 新增 `_compute_title_check`；batch + single 两路下载后调用，metadata.json + index.json 双写。**mismatch 只标记不阻断下载** |
| `tools/blit.py` | IEEE/CNKI 下载后调 `verify_pdf_title`，写 `{pdf_stem}.meta.json` sidecar。import 失败静默降级 |
| `stages/gw-read.md` | 操作段加"步骤 0：源文件 title 自检（abort 协议）"；派遣清单加 #7 派遣标题 [MUST]；质量门槛加 title-mismatch 不计入 ≥5 篇 |

**回填（V003b）+ API 交叉验证（V003c）**：

- `tools/backfill_titles.py`（dry-run + 审计日志 + 双重守卫）：回填 metadata.json 的空/URL/slug title。安全边界 6 条：① 只动 unverifiable/None ② metadata title 必须无效 ③ extract high 置信 ④ 非垃圾 ⑤ **method=all_failed 禁回填** ⑥ `_looks_like_non_title` 二次校验
- 回填 81 篇 → 子 agent API 交叉验证（67 篇：arxiv 44 + DOI 23）→ **抓出 4 篇抓错页面的回填** → 回滚 3 篇（清空）+ 清理 1 篇（剥 OPEN 前缀）→ 加双重守卫防止复发

**最终全量（237 篇，回滚后）**：

| 状态 | 数量 | 占比 |
|---|---|---|
| match | 172 | 72.6% |
| **mismatch** | **18** | **7.6%（全程不变，真损坏未被掩盖）** |
| unverifiable | 47 | 19.8%（arxiv_latex 28 + 真提取不到 12 + 垃圾 5 + banner 1 + 回滚 3）|

- **photonics 回归 PASS**（overlap=0.000）
- arxiv 回填集 API 验证 **44/44 = 100%** 准确；DOI 集 19/23 准确，4 篇抓错已回滚
- 18 mismatch 逐篇：~14 真损坏（bot墙×3/paywall×2/抓错期刊×3/抓错论文×2/截断×3）+ ~4 公式算法误提（保守触发复核）

## 不要做什么

1. **不要回写历史 256 篇 metadata.json**（V002 决策 #1 + V003 重申）——按需 `python -m litdownload.title_verify <path>` 手动跑，V003 给出 18 mismatch 列表供选择性修复
2. **不要把 blit sidecar 接入 papers/index.json**——架构扩张超范围；blit 平铺下载是既定设计
3. **不要假设 blit 下载的论文能直接触发 gw-read abort**——blit 下的是 `{arnumber}.pdf` 平铺布局，需先 `tools/convert` 转 content.md 放进 `papers/doi/{id}/` 才进 gw-read 流程
4. **不要在本专题做 R002 9篇实下载精读**——那是 research-direction-exploration 主线（H001 路径 B）
5. **不要 trust method=all_failed 的 content.md**——V003c 证实其 content 本就残缺，任何"标题"都是期刊名/页眉/正文片段

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段（read-traceability scope = 溯源机制 + title 校验 + 回填；content.md 清洗/doi 补转不在内）
- [ ] 验证本 handoff ≥3 关键事实：
  - `python -m litdownload.title_verify papers/doi/10.3390_photonics10080914` → mismatch overlap≈0.000
  - `grep _compute_title_check tools/litdownload/download_pipeline.py` 命中
  - `stages/gw-read.md` 含"步骤 0"abort 协议
  - 抽查回填论文 `papers/arxiv/2404.12633/metadata.json` 的 title 是 "FlagVNE:..." 且有 `title_backfilled_at`
  - 抽查回滚论文 `papers/doi/10.1016_j.ast.2026.112361/metadata.json` 的 title 为空 + `title_backfill_rolled_back` 字段存在
- [ ] 检查 `_registry.yaml`：read-traceability active，depends_on research-direction-exploration
- [ ] 确认范围未违反"明确不含"

## 接口变更（代码改动）

```yaml
新增模块:
  - tools/litdownload/title_verify.py
    public_api:
      - extract_real_title(content_md_path, method) -> {real_title, confidence, reason}
      - classify_mismatch(metadata_title, real_title_info) -> {status, overlap, real_title, reason}
      - title_overlap(t1, t2) -> float  # Jaccard，去停用词
      - verify_pdf_title(pdf_path, expected_title) -> dict  # blit 用
    cli: "python -m litdownload.title_verify <content.md|dir> [--method M] [--metadata-title T]"
    constants: {MISMATCH_THRESHOLD: 0.4}
  - tools/backfill_titles.py
    public_api: [_looks_like_non_title, main]
    cli: "python tools/backfill_titles.py [--dry-run]"
    guards: [all_failed 禁回填, _looks_like_non_title 二次校验]

签名变更:
  - file: tools/litdownload/download_output.py
    function: _save_metadata
    old: (paper, result, dest) -> None
    new: (paper, result, dest, title_check=None) -> None
  - file: tools/blit.py
    function: _ieee_download_paper
    old: (ctx, arnumber, save_dir) -> Path | None
    new: (ctx, arnumber, save_dir, expected_title="") -> Path | None
```

## 失败数据附录

**P0 误报修复（首轮 32 mismatch → 修后 18）**：
- B. MDPI section 误提（real="2. Topological Analysis"）→ `_is_nav_heading` 加编号小节模式
- C. slug 漏检（`network-00015`）→ 改"无空格+连字符+数字"判 slug
- D. 合法变体（GraphVNE overlap 0.36）→ 加"首词挽救"

**V003c 回填交叉验证发现的 4 篇抓错（已回滚）**：

| paper_id | 回填的（错）| 官方标题 | method |
|---|---|---|---|
| 10.1016/j.ast.2026.112361 | Aerospace Science and Technology | GNN-ASSSP... LEO Satellite | all_failed |
| 10.1038/s41598-026-40704-2 | orts Scientific Rep | Robust high-capacity FSO using OAM... | unpaywall |
| 10.1109/taes.2026.3652971 | 60%. Compared with the baseline... | A Service-Oriented Multipath Routing... | all_failed |
| 10.1038/s41598-025-17852-y | OPEN Secure and energy-efficient... | Secure and energy-efficient transmission... | all_failed（仅剥前缀，核心对）|

**根因教训**：① 自己验证自己是循环论证（V003b 只自检 high 置信就回填，没独立 API 验证）② method=all_failed 是危险信号 ③ "看起来正确"比"明确缺失"更危险。

## 已知债务

| 债务 | 当前状态 | 触发解决 |
|---|---|---|
| **14 篇 manual 论文回填未 API 验证** | 无 arxiv_id/DOI，V003c 跳过。`jang-etri-2026` 回填值 `O R I G I N A L A R T I C L E` 疑似 banner 已标 unverifiable，余 13 篇待抽检 | 实战精读时人工抽检 content.md |
| blit 未做实下载验证 | 只验证 graceful degradation，未验证 sidecar 实写入 | R002 实下载时（H001 路径 B）顺带验证 |
| 18 mismatch 的人工修复 | V003 列表已出，多为真损坏 | 按需删/重下/标弃 |

## 验证阈值（校验体系）

| 验证项 | PASS 标准 | 历史通过率 |
|---|---|---|
| mismatch | Jaccard <0.4 且无首词挽救 | 18/237 = 7.6%（回填前后不变）|
| match | Jaccard ≥0.4 或首词挽救 | 172/237 = 72.6%（回填+回滚后）|
| unverifiable | 提取失败/低置信/title 无效/arxiv_latex/all_failed | 47/237 = 19.8% |

## 下一轮建议（新对话首选）

### research-direction-exploration 主线（H001 路径 B）

R002 9 篇论文下载 + 精读，确认/推翻 E1/B1/A3 三检验。**这是 Groundwork 前置第一步**，不是 MVE。
1. 按来源下载（IEEE `10.1109/`→`blit --download`，自动写 `{arnumber}.meta.json`；OA/arXiv→`tools/download`，自动写 metadata.json title_check）
2. 逐篇核 title↔content（abort 协议 + `python -m litdownload.title_verify <path>`）
3. gw-read 精读产出 `papers/_read_notes/{paper_id}.md` + read-log

read-traceability 专题至此**机制 + 工具 + 数据清洗 + 交叉验证全部完成**，可 close（待方向探索实战精读跑通后正式 close）。

## 关键文件索引

- 代码：`tools/litdownload/title_verify.py`（主）、`download_output.py`、`download_pipeline.py`、`tools/blit.py`、`tools/backfill_titles.py`（回填+守卫）
- 框架：`stages/gw-read.md`（abort 协议在"操作"节步骤 0）
- 验证：`.sessions/2026-06-15-read-traceability/verifications.md` V003 + V003b + V003c
- 回填审计：`.sessions/2026-06-15-read-traceability/backfill-log.md`（81 篇 old→new）
- 用法：`python -m litdownload.title_verify papers/doi/<id>`（自动读 metadata.json 取 method+title）
