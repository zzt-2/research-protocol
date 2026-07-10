# Handoff: Step 2 下载完成 → Step 3 精读（10 篇 + D002 角度素材 schema 试用）

> 来源: S001 | 交接目标: 新对话执行 GW Step 3 精读
> 文件名: H001-step2-done-step3-read.md
> 日期: 2026-07-10

## 已完成边界

**GW Step 1 地勘 + Step 2 下载全部完成**：

1. **Step 1 检索穷举**：15 查询 + 综述补搜 4 查询，去重 43 核心候选（必读 16 + 建议读 27）+ 备选 32，8 子方向聚类。质量门槛全通过（≥20条/≥3源/必读≥5/≥2子方向/正式发表100%）。D017 穷举门控 A 经用户确认（"随你便，进吧"）。
2. **Step 2 下载**：两轮（tools/download 4 篇 + blit IEEE 5 篇转换成功）。**9 篇成功 + sat.1553 = 10 篇可用于精读**。1 篇登录页外壳（ANN Access），6 篇付费墙未获取（Optica 3 + Elsevier 1 + SAGE 1 + JLT 2025 登录页 1）。
3. **环境补强**：torch venv 新建（Python 3.14 + requests/serpapi/tavily/jieba/playwright/pymupdf4llm）；tools/search、download、blit、convert 四个 wrapper 加 `Scripts/python.exe` Windows 兼容。

**综述锚**：sat.1553（Valjus 2025，已落盘 `papers/doi/10.1002_sat.1553/content.md`，1581 行），§6 偏振解复用 227 行全书最大。

**8 子方向聚类**：A 多孔径MIMO均衡(12) / B CMA(6) / C Stokes(5) / D SOP跟踪(8) / E PDL/PMD(3) / F 双偏振FSO系统(21) / G 神经网络盲均衡(3) / H 迁移源(12)。详见 S001 全景表。

## 不要做什么

1. **不跳 Step 3 直接试方法/判方向**（TL-30/FR-22）—— Step 3 精读 + Step 4a 可行性是硬门控
2. **不在精读阶段判 Go/Kill 或排优先级**（D018 中性提取——全摸完才排）
3. **不直接改 gw-read.md**（D002 角度素材 schema 守"先测不改协议"，3-5 篇验证有效再进框架）
4. **不用 web reader 抓论文全文**（撑爆上下文，已守 gw-acquire.md 止损）
5. **不复活 9 次 Kill 当贡献**（作思路素材重新进精读池，不变量1 仍守）
6. **主对话禁 WebSearch**（用 tools/search + tools/blit）

## 必读

按优先级：
1. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（不变量 8 条 + 当前位置）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/S001-search-strategy-dual-pol-osl.md`（全景表 8 子方向 + 下载状态 + 覆盖面缺口报告）
3. `stages/gw-read.md`（精读流程 + 7 子表结构化提取 + 步骤 0 title 自检）
4. `.sessions/2026-07-10-scenario-transfer-pivot/decisions.md` D001/D002/D003（方法论三维度 + 角度素材 schema + 双偏振空间解锁）
5. `.sessions/2026-06-20-problem-driven-redirection/decisions.md` D017/D018（穷举门控 + 中性提取）
6. `papers/doi/10.1002_sat.1553/content.md` §6（偏振解复用层，227 行）

## 接口变更

无代码接口变更。环境层：
- **torch venv 新建**：`$HOME/.venvs/torch`（Python 3.14），Windows 下 python 在 `Scripts/python.exe`
- **4 个 wrapper 已修 Windows 兼容**（search/download/blit/convert 加 Scripts/python.exe 检测）
- **新增依赖**：playwright + chromium（blit 依赖）、pymupdf4llm（convert 依赖）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 6 篇付费墙论文未获取 | gw-acquire 覆盖面 | Optica 3 + Elsevier 1 + SAGE 1 + JLT2025 登录页 1 | 用户手动获取（机构VPN/作者主页），或确认当前 10 篇覆盖面可接受 |
| ANN Access 登录页外壳 | content.md ≥50 行 | 40 行 IEEE 登录页 | 机构订阅覆盖后重下，或确认不阻塞（G 类有 Bootstrapping VAE 可用） |
| 建议读 27 篇未下载 | Step 2 只下必读 16 | 建议读在 search-archive JSON 里标注了 priority | Step 3 精读时如必读不够再按子方向补下 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条，尤其不变量1 九次Kill是物理事实 + 不变量7 方法论不问导师 + 不变量8 双偏振放宽有效）
- [ ] 已验证至少 3 条关键事实声称：
  - sat.1553 §6 是全书最大层（核查 `papers/doi/10.1002_sat.1553/content.md` §6 L561-787 = 227 行 vs §3/4/5）
  - 10 篇精读论文 content.md 全 ≥50 行（核查 `wc -l papers/doi/{doi_path}/content.md`）
  - 必读 16 篇去重后子方向覆盖 A/B/F/G（核查 S001 全景表）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（scenario-transfer-pivot dormant + problem-driven-redirection active）
- [ ] 已确认当前范围未违反"明确不含"（不跳框架/不预设方向/不复活Kill当贡献）

## 下一轮

**GW Step 3 精读**（gw-read.md）：
1. 读 `stages/gw-read.md`（精读流程 + 派遣强制清单 6 项 + 步骤 0 title 自检）
2. 对 10 篇（9 必读 + sat.1553）派精读子 agent：每篇读 content.md method+experiment，按 gw-read 14 字段 + 7 子表结构化提取（含问题提取 M/C/A + 四判据）
3. **D002 角度素材 schema 试用**：前 3-5 篇精读时加试"角度素材"段（6 类来源 + 半结构化字段 + 通信大类通用词表），验证有效性。schema 设计在 `scenario-transfer-pivot/R002-angle-material-schema-design.md`
4. 精读产出写入 `papers/_read_notes/{paper_id}.md`（全局）+ literature_notes.md（项目级，需建 `projects/thesis-fso/literature_notes.md`）
5. 守步骤 0 title 自检（abort 协议）—— content.md 标题与派遣标题重叠 <0.4 则 abort
6. 全部精读完后做综合分析（方法分类/已知局限/趋势/研究问题清单过四判据）
