# [S002] 旧检索资产盘库：撤销"价值有限"误判 + 复用方案

> 2026-07-10 | GW Step 1 前置 / 地勘种子盘库 | 状态：完成（盘库结论供用户拍板复用机制）
> 续接：S001（同日，压缩恢复后续接）

## 目标

回应用户原话："我之前不是每次都会检索一大堆吗？总感觉每次检索完了就扔那了，后面再也没看过？你觉得有办法再给它利用起来吗？"

压缩恢复后，**先核查再发言**（守 6 次状态认知滞后教训）。S001 里我对此问题给过一个含糊的"价值有限、待阶段 1 后再说"的判断——**那是没看数据的臆测**。本轮用确定性数据撤销那个判断。

## 记录

### 1. 旧检索资产实测（确定性数据，非估算）

| 指标 | 数字 | 备注 |
|---|---|---|
| search-archive 日期目录 | 46 个 | 2026-05-07 ~ 2026-07-09 |
| JSON 检索结果文件总数 | 2084 | 每文件含 query + 多源（S2/OpenAlex/SerpAPI/Exa）+ results 数组 |
| 累计论文条目（去重前）| **36823** | 平均 18 条/文件 |
| 空 results 文件 | 147 | 失败检索（占比 7%，正常）|
| papers/doi 已落盘论文目录 | 331 | 真正下全文的少数 |

**结构根因**：`tools/search` 脚本只有 `_auto_save` 落盘 JSON，**没有任何可重读索引/digest 层**。3.6 万条目全部沉默躺在按日期分的目录里——这就是"扔那不看"的制度性根因，不是记忆问题。

### 2. 与均衡层专题的相关度（撤销"价值有限"误判）

按 PROMPT-001 关键词组扫了 3.6 万条：

| 关键词组 | 命中条目（去重前）| 命中文件 |
|---|---|---|
| equalization | 1867 | 568 |
| polarization | 2375 | 690 |
| MIMO | 2025 | 802 |
| adaptive-optics | 1101 | 477 |
| coherent-detection | 3690 | 727 |
| FSO | 7569 | 996 |
| **FSO × 均衡 交集（唯一论文）** | **142** | 81 有 DOI |

**142 篇 FSO×均衡唯一论文**——远超一次新地勘第 1 批的产出。含顶刊黄金区：

- **JLT 2010** Polarization-Multiplexed Optical Wireless Transmission With Coherent Detection（领域奠基）
- **JLT 2020** OAM CNN 大气湍流补偿
- **JLT 2023** Multi-aperture MIMO 2N×2 adaptive equalizer（multi-aperture combining 主流族）
- **JLT 2025** End-to-end multi-band autoencoder
- **OL 2024** Real-time two-aperture coherent digital combining
- **Opt Express 2025** Spatiotemporal feature 大气湍流均衡
- **TCCN 2026** Bootstrapping blind equalizer DP-FSO（极新）
- **sat.1553 (2025)** DSP for coherent optical satellite links review（Valjus，综述）
- **PTL 2014** MDPSK Nonequalization OFDM coherent FSO（早期 baseline）

完整覆盖 **OAM-MIMO 均衡族**（2014-2026 跨度 12 年）+ **multi-aperture coherent combining 族**（2016-2026）+ **DNN 均衡族**（2020-2026）。

### 3. 这批命中集中在哪里（不是均匀分布）

| 日期 | FSO×均衡命中 | 当日查询主题 |
|---|---|---|
| 2026-05-29 | **172 条** | thesis-fso 早期全景检索，**54 个均衡/MIMO/CMA/偏振查询**（CMA blind equalization DP-QPSK / CMA equalizer PolDemux FSO MIMO 2x2 / FSO equalization survey）|
| 2026-05-31 | 87 | 载波同步专题检索（但带出均衡论文）|
| 2026-06-10 | 64 | 同上 |
| 2026-06-22 | 59 | 同上 |

**关键**：2026-05-29 那 54 个均衡相关查询是 thesis-fso 转向载波同步前做的早期全景检索——**当时因为方向变了，这批就被冷藏**。它就是均衡层专题的天然种子库。

### 4. 已落盘率暴露第二个问题

142 篇 FSO×均衡有 DOI 的 81 篇里，**只有 3 篇落盘到 papers/doi**（落盘率 3.7%）。

这不是"扔那不看"——这是"检索到、评估了、但没下全文"。验证：papers/doi 共 331 个目录，集中在载波同步相关的 VV/BPS/NDA-ML 等少数方法。**FSO×均衡 81 个 DOI 是即用的"待下载清单"**，不是空中楼阁。

### 5. 复用方案（三档，供用户拍板）

**档 A（最小，推荐先做）**：把 142 篇 FSO×均衡 + 1867 篇 equalization 核心层导出成 `search-archive/_index/equalization-seed.md`，按子地带（multi-aperture MIMO / OAM / 偏振 / DNN / ISI / AO-DSP）分类，每条标档级+年份+是否 FSO+DOI。**地勘第 1 批第 1 组（equalization 总览）用这个起步，省 1 个对话。**

**档 B（中等）**：在档 A 基础上加 `_digest.md` 索引层——每个查询主题一行摘要（如"2026-05-29 CMA FSO: 16 篇，3 篇核心 multi-aperture combining"）。需要派子 agent 跑 1-2 小时。

**档 C（系统化）**：给 `tools/search` 加 `--digest` 后处理（落盘后自动跑摘要索引到 `_index/`），治本。但这是框架改进，超出均衡层专题范围，建议进 framework-evolution 专题。

### 6. 与 PROMPT-001 的衔接

如果用户选档 A，PROMPT-001 阶段 1 第 1 批的组 1（equalization 总览）改为：
- **先用 `_index/equalization-seed.md` 起步**（已盘库的 142 篇）
- 再补 1-2 个新查询覆盖 2026 下半年的最新论文
- 不从零检索

如果用户不选：保持 PROMPT-001 原样，从零检索，142 篇作为"二次交叉验证池"用。

## 决策引用

- 无新建 D###（复用方案待用户拍板，可能产出 D002）
- 引用既有：D001 开专题 / INVARIANT 17 规划门控 / 6 次状态认知滞后教训（先核查再发言）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（盘库是为阶段 1 地勘做准备，INVARIANT 17 允许）
- 未触发 Trigger 3（扩大范围）——盘库本身不扩大专题范围，只优化种子来源
- 档 C（系统化）若做会超出均衡层专题，建议进 framework-evolution

## 后续

**待用户拍板**：
1. 档 A / B / C 选哪个？（推荐档 A）
2. 若选档 A，是否同意 PROMPT-001 组 1 改为"种子起步 + 补新"？

**本轮（S002）已完成**：撤销 S001 含糊判断 + 给出有数据支撑的复用方案三档
