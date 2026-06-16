# Handoff: R002 6 方向论文下载完成 + read-traceability 实战闭环跑通（待精读）

> **📌 状态更新（2026-06-16 下载完成）**：本 handoff 原为"下载准备就绪"，**当轮已在本机 WSL 执行完毕**。
> - **10/11 篇下载成功**，title_verify 全 match（含 2 篇人工核验修正 title_verify 误判）
> - **1 篇失败**：A2-SPIE `10.1117/12.3082273`（RNN 载波恢复）Firecrawl 超时，标 manual_required
> - **read-traceability 实战闭环首次跑通**：read-log 追加 10 篇溯源记录 + 2 个 title_verify 误判 case 发现
> - **下一轮任务变为：gw-read 精读**（不再是下载）。本 handoff 下半部"下一轮可执行步骤"已过时，参考本节"下载实战发现"+ 文末"精读起步"

> 来源: 本对话 2026-06-15（read-traceability 收尾）+ 2026-06-16（下载完成 + 实战闭环）
> 交接目标: 下一轮启动 gw-read 精读（10 篇已就绪）
> 文件名: H003-R002-download-ready.md
> 前置 handoff: H001（方向筛选）+ H002（read-traceability 验收，另一专题）

> **⚠️ 环境澄清（2026-06-16 实测，推翻初稿"跨机交接"前提）**：
> 初稿误判 win32 无 torch venv 为 blocker。实测后纠正：本机通过 **WSL（Ubuntu）** 访问 `/mnt/d/code/study/research-protocol`，WSL 内 `~/.venvs/torch/bin/python` 完整可用（含 requests/pymupdf/pymupdf4llm，DEPS_OK）。**调用方式 = `wsl -e bash -c "cd /mnt/d/code/study/research-protocol && ./tools/..."`**，所有 tools/ 工具均能在 WSL 内正常运行。早期出现的 bash 乱码是 cmd GBK codepage 解码 WSL UTF-8 输出导致，非功能故障。**下载在本机 WSL 完成，无需跨机**。

## 下载实战发现（2026-06-16，read-traceability 框架反馈素材）

### 发现 1：`try_firecrawl_scrape` 设计 gap（init 提交历史 bug，非 zcode 回归）

**症状**：`tools/download --doi <DOI>` 单篇模式对 OA 论文返回 `all_failed`，即使 Firecrawl API 本身能抓到论文。

**根因**（systematic-debugging Phase 1-3 定位）：
- `tools/litdownload/download_channels.py:35` 的 `try_firecrawl_scrape` 读 `paper.get("url") or paper.get("pdf_url")`
- `--doi` 单篇模式构造的 paper dict 只有 `{"doi": "..."}`，**没有 url 字段**
- 第 36-37 行 `if not url: return None` 静默跳过 → Firecrawl 通道形同虚设
- git blame 证实：从 `db6222f init: 初次提交`（2026-05-12）就存在，历史只 2 个 commit 碰过此文件，read-traceability 那次没动这函数

**为什么历史 165 篇能下**：之前走批量 JSON 模式（搜索结果带 url 字段），Firecrawl 通道正常。单篇 DOI 模式第一次真正用才暴露。

**变通方案（本轮用，未改源码）**：临时 wrapper 脚本给 paper dict 填 `url: https://doi.org/{doi}`，激活 Firecrawl 通道。**脚本用完即删，未提交**。

**正式修复建议**（超出 read-traceability/research-direction-exploration 范围，归 framework-evolution 或新专题）：`download_channels.py` 的 `try_firecrawl_scrape` 在 url 为空时，用 `https://doi.org/{doi}` 兜底（DOI 模式下 doi 一定有）。

### 发现 2：Firecrawl 通道对不同期刊的反爬表现

| 期刊 | Firecrawl 效果 | 原因 |
|---|---|---|
| MDPI（Aerospace） | ✅ 完整正文 | OA，无反爬 |
| Optica（Optics Letters/Express） | ✅ 完整正文 | OA，无反爬 |
| Scientific Reports | ✅ 完整正文 | OA，无反爬 |
| IEEE（Access/PTL/JLT/CL/ICSOS） | ❌ 只抓登录页/账户导航 | 反爬，需校园网 IP |
| SPIE | ❌ 超时 | 闭源 + 慢 |

**结论**：IEEE 必须走 blit（校园网 IP 机构认证），不能用 Firecrawl。H003 原路由判断正确。

### 发现 3：title_verify 有 2 类误判（content.md 实际正确）

| 论文 | title_verify 判定 | 实际 | 误判原因 |
|---|---|---|---|
| C2-Nasr `10.1109/ACCESS.2025.3535789` | mismatch 0.000 | ✅ content 正确 | pymupdf4llm 把作者行 `## YEGANEH NASR...` 标成 heading，title_verify 误提为标题 |
| E1-Ahmad `10.1038/s41598-026-40704-2` | unverifiable | ✅ content 正确 | 期刊 banner "orts Scientific Rep"（截断的 Scientific Reports）被误提为标题 |

**已处置**：人工核验 content.md 标题/摘要/正文完整后，修正 metadata.json 的 `title_check: match` + 加 `title_check_note` 字段记录误判原因。

**框架反馈**：title_verify 的 heading 提取启发式对"PDF 页眉 banner"和"作者行被误标 ##"两类 case 不鲁棒。归 read-traceability 后续改进（非本轮范围）。

### 发现 4：blit sidecar title_check 判定逻辑有 bug

`{arnumber}.meta.json` 里 `title_check: match` 但 `title_overlap: 0.167`（<0.4 阈值）——判定与阈值矛盾。但不影响下载流程，title_verify 会用 content.md 重新判定。归 read-traceability 后续。

### 发现 5：A3-Yang DOI 并非"张冠李戴"

初稿（H003 早期版本）称 index.json 的 `LCOMM.2026.3681606` 是 A3-Yang 张冠李戴。**实测纠正**：`3681606` 是另一篇真实存在的论文（"Spectrum Sharing... Multi-Satellite Multi-beam STINs"，卫星通信方向），index.json 记录正确。真正的问题是 A3-Yang `3651445` **根本不在索引**，本轮已新增。H003 已修正措辞。

## 下载结果总表（10 成功 + 1 失败）

| # | 方向 | paper_id | 方法 | title_check | content 行数 |
|---|---|---|---|---|---|
| 1 | E1 | 10.3390_aerospace12100869 | firecrawl | match 1.0 | 770 |
| 2 | E1 | 10.1038_s41598-026-40704-2 | unpaywall(旧) | match（人工核验）| 858 |
| 3 | E1补 | 10.1364_oe.555656 | firecrawl | match 1.0 | — |
| 4 | A3 | 10.1364_ol.596189 | firecrawl | match 1.0 | — |
| 5 | A3 | 10.1109_LCOMM.2026.3651445 | blit | match 1.0 | 225 |
| 6 | A2 | 10.1109_LPT.2025.3582338 | blit | match 0.857 | 157 |
| 7 | B1 | 10.1109_ICSOS66026.2025.11443174 | blit | match 1.0 | 397 |
| 8 | C2 | 10.1109_ACCESS.2025.3535789 | blit | match（人工核验）| 649 |
| 9 | C2 | 10.1109_JLT.2025.3533422 | blit | match 1.0 | 377 |
| 10 | D2 | 10.1109_LPT.2025.3647750 | blit | match 1.0 | 247 |
| ❌ | A2 | 10.1117/12.3082273 (SPIE) | — | — | manual_required（Firecrawl 超时）|

**bonus 相关文献**（blit 搜索附带下到，非 R002 主清单，convert 未完成，待评估）：
- `papers/manual/c2-nasrollahzadeh-ann-equalization-2026/`（ANN Equalization，C2 同作者）
- `papers/manual/c2-dsp-free-coherent-receiver-datacenter-2017/`（DSP-Free，C2 相关）

## 精读起步（下一轮任务）

10 篇已就绪，按 H001 第 83-88 行 Groundwork 前置流程精读：

1. 读 `stages/gw-read.md` 完整流程（**步骤 0 abort 协议已实战验证有效**）
2. 按方向优先级精读：E1/B1/A3（留选）先于 A2/C2/D2（存疑）
3. 每篇精读产出 `papers/_read_notes/{paper_id}.md`（首篇创建该目录）+ read-log 更新"笔记路径"和"首读日期"字段
4. 精读目标：确认/推翻 D001 E 三检验（反例/非平凡/可比较）

**注意**：gw-read 要求子 agent 精读（AGENTS.md 子 agent 强制委托 #1），主对话只接收结构化摘要。

## 项目背景（接收方首次接触必读）

- **硕士论文**：星地湍流信道激光通信处理技术研究
- 当前位置：研究方向探索阶段，**R002 22 候选已粗筛到 6 方向（E1/B1/A3 留选 + A2/C2/D2 存疑）**
- 当前步骤（按 H001 第 79-90 行"下一轮"）：第 3 步 Groundwork 前置第一步——精读关键论文。**但 V002 审计发现 9 篇关键论文 0 篇下载**，所以实际下一步是**先下载**，再精读。
- **未进 Groundwork、未碰 MVE**（H001 明确警告：候选筛出 ≠ 可 MVE）

## 本对话（2026-06-15~16）已完成

1. **read-traceability H002 接收方验证全部 PASS**（5 条事实声称逐一核对）
2. **切到 research-direction-exploration 主线**（用户决策："切"；read-traceability 保持 active 不关，"后面兴许用得上"）
3. **从 R002 6 方向挑出 11 篇关键论文清单**（E1×2 + A3×2 + A2×2 + C2×2 + D2×1 + B1×1 + E1补OE 1篇 = 共11）
4. **子 agent 用 Crossref API 核实全部 DOI**（5 项查询全 FOUND，HIGH 置信度）—— 关键修正：A3-Yang 的 DOI `10.1109/LCOMM.2026.3651445` 是正确的；本地 index.json 里的 `LCOMM.2026.3681606` 是另一篇无关论文（卫星通信波束成形），**张冠李戴，需修正**
5. **重复检查**：11 篇中 1 篇（E1-Ahmad `10.1038/s41598-026-40704-2`）已在索引但 `title_backfill_rolled_back`，需重跑 title_verify
6. **环境 blocker 发现**：本机 win32 无 `~/.venvs/torch`，系统 Python 缺 pymupdf/pymupdf4llm，无法跑 `tools/download`

## 不要做什么（Dead Ends）

- **❌ 不要重新派 agent 搜索方向** —— 22 候选已在 R002，方向搜索阶段结束
- **❌ 不要在没有 torch venv 的机器上尝试 `tools/download`** —— pymupdf/pymupdf4llm 缺失，PDF→md 转换必失败。本机 win32 已实测 blocker
- **❌ 不要跳过 title_verify 直接进 gw-read** —— H002 已立"步骤 0 abort 协议"：精读前必须核 title↔content，mismatch 的不计入 ≥5 篇下限
- **❌ 不要现在做 sigma2_turb 推导**（B 任务）—— 等方向选定后视是否沿用同步框架再决定
- **❌ 不要碰论文写作** —— 用户明确"一时半会不推进"
- **❌ 不要重新讨论 D001 框架** —— DECIDED 状态，要推翻先读 decisions.md 的否决条件段

## 必读（按优先级）

1. `.sessions/2026-06-10-research-direction-exploration/H001-research-direction-screening.md` —— 上一轮方向筛选 handoff
2. `.sessions/2026-06-10-research-direction-exploration/decisions.md` —— **D001 评判框架** + **D002 创新点抛弃**
3. `.sessions/2026-06-10-research-direction-exploration/R002-extension-opportunity-scan.md` —— 22 候选方向（341 行）
4. `.sessions/2026-06-10-research-direction-exploration/topic-index.md` —— 专题全貌（进展/不变量/范围/未决项）
5. `.sessions/2026-06-15-read-traceability/H002-title-verify-landed-and-mainline-resume.md` —— read-traceability 验收 + 本 handoff 的姊妹篇（含 title_verify/gw-read 步骤 0 协议详情）
6. `stages/gw-read.md` —— 精读流程（**步骤 0：源文件 title 自检 abort 协议**，第 33/40/188 行）

## R002 6 方向 11 篇关键论文清单（DOI 已 Crossref 核实）

> DOI 全部 HIGH 置信度（Crossref 直接 lookup）。title 字段用 Crossref 返回的**正式完整 title**，非 R002 缩写版。

### 留选方向（E1/B1/A3，6 篇）

| # | 方向 | DOI | 正式 title（Crossref） | 期刊 | 路由 |
|---|---|---|---|---|---|
| 1 | **E1** | `10.3390/aerospace12100869` | End-to-End Performance Analysis of CCSDS O3K Optical Communication System Under Atmospheric Turbulence and Pointing Errors | Aerospace (MDPI) | **OA→tools/download --doi** |
| 2 | **E1** | `10.1038/s41598-026-40704-2` | Robust high-capacity free-space optical communication using OAM-based structured light and intelligent adaptive signal processing | Scientific Reports | ⚠️ **已下**，但 `title_backfill_rolled_back`，**需重跑 title_verify** |
| 3 | **A3** | `10.1109/LCOMM.2026.3651445` | Polarization-Fading-Free Phase Recovery and Robust RSOP Tracking Using Frequency-Domain Pilot Tones in Optical DSCM Systems | IEEE Communications Letters | **IEEE→blit --download**（校园网 IP） |
| 4 | **A3** | `10.1364/ol.596189` | Vibration Detection Based on DSP Frame Pilot Symbols Using Integrated Coherent Receivers | Optics Letters | **OA→tools/download --doi**（先试 Unpaywall/OA） |
| 5 | **B1** | `10.1109/ICSOS66026.2025.11443174` | Z-Transform Model of a Coherent Receiver for Satellite-to-Ground Laser Links Under High Doppler Rates | IEEE ICSOS 2025 | **IEEE→blit --download** |
| 6 | **E1补** | `10.1364/oe.555656` | Array detector systems for satellite-to-ground atmospheric coherent laser communications: performance evaluation | Optics Express | **OA→tools/download --doi** |

### 存疑方向（A2/C2/D2，5 篇）

| # | 方向 | DOI | 正式 title（Crossref） | 期刊 | 路由 |
|---|---|---|---|---|---|
| 7 | **A2** | `10.1109/LPT.2025.3582338` | Transparent Carrier Phase Recovery Based on an Artificial Neural Network | IEEE Photonics Technology Letters | **IEEE→blit --download** |
| 8 | **A2** | `10.1117/12.3082273` | Recurrent neural network enabled adaptive carrier phase recovery algorithm for high-speed coherent optical transmission systems | SPIE Artificial Intelligence in Photonics | **OA→tools/download --doi**（SPIE 多闭源，可能 manual_required） |
| 9 | **C2** | `10.1109/ACCESS.2025.3535789` | Dual-Polarization Self-Coherent Transceivers for FSO Communications in the Presence of Atmospheric Turbulence | IEEE Access | **IEEE→blit --download**（Access 多 OA，也可试 tools/download） |
| 10 | **C2** | `10.1109/JLT.2025.3533422` | Dual-Polarization Optical Costas Loop for DSP-Free Homodyne Short-Reach Links | Journal of Lightwave Technology | **IEEE→blit --download** |
| 11 | **D2** | `10.1109/LPT.2025.3647750` | Probabilistic Shaping and Residual Carrier Modulation for FSO Turbulent Channels | IEEE PTL | **IEEE→blit --download** |

### 路由统计

- **IEEE 闭源（blit --download，校园网 IP）**：6 篇（#3/5/7/9/10/11）
- **OA（tools/download --doi）**：5 篇（#1/4/6/8/9-备选）
- **已下需重跑 title_verify**：1 篇（#2）
- **本地 index.json 张冠李戴需修正**：A3-Yang DOI（详见"已知债务"）

## 接收方验证（续接对话时必须完成）

- [ ] 已读 `topic-index.md` 不变量段（含 D001 评判框架 + 跳步 dead end）
- [ ] 已读 `decisions.md` D001（四轴筛选）+ D002（创新点抛弃）
- [ ] 已读 H001（上一轮方向筛选）"不要做什么" + "下一轮"
- [ ] 已读 `stages/gw-read.md` 步骤 0 abort 协议（第 33/40/188 行）
- [ ] 已验证 ≥3 条关键事实：①11 篇 DOI 在本文件表 ②D001 是 active DECIDED ③本机/目标机有 torch venv（无则二次 blocker）
- [ ] 已确认 `_registry.yaml` 中 `research-direction-exploration` status=active、depends_on 无冲突
- [ ] 已确认范围未违反"明确不含"（不改仿真代码/开题报告/做实验）

## 下一轮（具体可执行，按顺序）

### 步骤 1：环境就绪检查（已验证 PASS）

本机 WSL 已实测（2026-06-16）：

```bash
wsl -e bash -c "ls ~/.venvs/torch/bin/python && ~/.venvs/torch/bin/python -c 'import requests, pymupdf, pymupdf4llm; print(\"DEPS_OK\")'"
```

✅ torch venv 存在，所有依赖齐全。`./tools/download --help` 正常输出。**直接进步骤 2**。

后续所有 tools/ 调用都用统一入口 `wsl -e bash -c "cd /mnt/d/code/study/research-protocol && ..."`。

### 步骤 2：批量下载（按路由分组）

**A 组：OA 论文（5 篇）—— tools/download**
```bash
# 串行，每篇间隔避免被限速
./tools/download --doi 10.3390/aerospace12100869     # E1-CCSDS
./tools/download --doi 10.1364/ol.596189             # A3-Vibration
./tools/download --doi 10.1364/oe.555656             # E1补-Array detector
./tools/download --doi 10.1117/12.3082273            # A2-RNN（SPIE 可能失败，记 manual_required）
./tools/download --doi 10.1109/ACCESS.2025.3535789   # C2-DualPol（先试 OA，失败转 blit）
```

**B 组：IEEE 闭源（6 篇）—— blit --download**
```bash
# 校园网 IP 必需，blit 50 次/会话限制，6 篇 OK
mkdir -p papers/downloads/2026-06-16-r002/
# 注意：blit 按关键词搜，不按 DOI 下。需先用 title 搜到论文，再 --download
./tools/blit "Polarization-Fading-Free Phase Recovery RSOP Frequency-Domain Pilot Tones" --source ieee --download papers/downloads/2026-06-16-r002/
./tools/blit "Z-Transform Model Coherent Receiver Satellite-to-Ground Laser High Doppler" --source ieee --download papers/downloads/2026-06-16-r002/
./tools/blit "Transparent Carrier Phase Recovery Artificial Neural Network" --source ieee --download papers/downloads/2026-06-16-r002/
./tools/blit "Dual-Polarization Self-Coherent Transceivers FSO Atmospheric Turbulence" --source ieee --download papers/downloads/2026-06-16-r002/
./tools/blit "Dual-Polarization Optical Costas Loop DSP-Free Homodyne" --source ieee --download papers/downloads/2026-06-16-r002/
./tools/blit "Probabilistic Shaping Residual Carrier Modulation FSO Turbulent" --source ieee --download papers/downloads/2026-06-16-r002/
```

**blit 下载后必做**（tools-guide §3）：手动 convert + 手动追加 index.json
```bash
./tools/convert papers/downloads/2026-06-16-r002/*.pdf --batch --quality fast
# 然后手动追加到 papers/index.json（blit 不自动写）
```

### 步骤 3：read-traceability 实战闭环（顺带做，零额外成本）

对每篇下载成功的论文跑 title_verify（含已下的 #2）：
```bash
# 每篇一次，串行
./tools/download --doi 10.3390/aerospace12100869  # 已含 _compute_title_check 自动跑
# 或手动复核：
cd tools && python -m litdownload.title_verify ../papers/doi/10.3390_aerospace12100869
```

**判定规则**（gw-read.md 步骤 0 abort 协议）：
- `match`（overlap ≥0.4）→ 可进 gw-read 精读
- `mismatch`（overlap <0.4）→ **abort**，不计入 ≥5 篇下限，metadata 标 `title_backfill_rolled_back`
- `unverifiable`（content.md 不存在）→ 下载失败，重下或 manual_required

**首次跑通 read-log 闭环**：首篇 match 论文在 `papers/_read_notes/{paper_id}.md` 建笔记，并在 `.sessions/2026-06-10-research-direction-exploration/read-log.md` 追加一行（7 字段格式，见 read-log.md 表头）。这同时是 read-traceability 专题的实战闭环验证（V003 待办）。

### 步骤 4：失败论文处置

预期失败模式（按 tools-guide §3.5 + V002 审计）：
- SPIE #8（A2-RNN）：闭源概率高 → `manual_required`，用户手动获取
- IEEE 部分（#3/5/7/9/10/11）：若不在校园网订阅范围 → `manual_required`
- title_verify mismatch：按 abort 协议，标 `title_backfill_rolled_back`，不勉强精读

**失败 ≠ 方向死**。某方向关键论文全失败 → 在 decisions.md 记 D### 方向降级（但不立刻砍，先看有无替代论文）。

### 步骤 5：精读（下载全部完成后，下一轮）

按 gw-read.md 完整流程精读，每个留选方向至少 1 篇 match 论文。精读目标：确认/推翻 D001 E 三检验（反例/非平凡/可比较）。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| A3-Yang DOI 张冠李戴 | index.json 准确性 | 本地索引存 `LCOMM.2026.3681606`（实为卫星通信无关论文），正确应为 `3651445` | 步骤 2 下到正确论文后，修 index.json |
| E1-Ahmad 论文 title 错配保护 | title_verify 必跑 | `title_backfill_rolled_back`，content.md 存在但未验证 title | 步骤 3 重跑 title_verify 判定 |
| ~~win32 无 torch venv~~ | ~~AGENTS.md 环境约定~~ | **初稿误判，已澄清**：本机 WSL torch venv 完整可用（2026-06-16 实测） | 已解决 |
| sigma2_turb 推导悬置 | 参数溯源 | D002 后等方向选定 | 选定方向沿用同步框架时做 |
| Ch3/Ch4 框架"很不充分" | 开题宽壳未填实 | topic-index 标注 | 选定方向后重评 |
| 凑创新点(1)(2) 悬置 | D002 作废为锚 | innovation-points.md 标"凑的待重评" | 方向选定后重写 |

## 验证阈值（read-traceability 实战闭环 PASS 标准）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| title_verify 状态 | match（overlap ≥0.4） | gw-read.md 步骤 0 + title_verify.py | 新机制，0 次实战 |
| mismatch abort | mismatch 论文不计入 ≥5 篇下限，metadata 标 rolled_back | gw-read.md 第 188 行 | 新机制 |
| read-log 首条 | 首篇 match 论文在 read-log.md 追加 7 字段行 | read-traceability V003 待办 | 新机制 |
| _read_notes 创建 | 首篇 match 论文在 papers/_read_notes/{paper_id}.md 建笔记 | gw-read.md | 新机制 |

## 用户/导师 voice（本轮关键原话，已追加 voice.md）

- "切"（从 read-traceability 切到 research-direction-exploration 主线）
- "我不知道，最好是"（授权我自主读 R002 挑清单）
- "专题不急着关？后面兴许用得上"（read-traceability 保持 active，不正式 close）
- 决策"先子 agent 补查全部 DOI（推荐）"+"11 篇全下"+"串行下载"
- ~~决策"回到原来那个 Linux/WSL 机器跳"~~（**推翻**：2026-06-16 实测本机 WSL 可用，改本机执行）
- "我之前是 wsl 里开 /mnt/d/code/xxx 去这个工作区。因此环境是 wsl 里的。现在换 zcode，好像没办法这么干了？"（用户指出环境认知错误，触发本澄清）→ 本机 WSL 直接下
