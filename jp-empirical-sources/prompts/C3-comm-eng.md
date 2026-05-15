# C3: 收集通信工程领域中文实证研究论文（30篇）

## 背景

本项目正在为实证研究型期刊论文设计约束体系。通信工程是重点应用领域，需要额外 30 篇中文实证研究论文作为素材。

通信工程领域"实证研究"的定义比社科更宽泛：包括基于仿真的性能评估、基于实测数据的验证、算法实验对比等，但必须有：
- 明确的研究问题/性能目标
- 实验设计（仿真参数、数据集、测试条件）
- 量化评估（指标、对比基线）
- 结果分析（不只是理论推导）

## 范围

- **语言**：仅中文
- **质量**：CSSCI、北大核心、EI 中文期刊
- **类型**：有实验/仿真/实测验证的通信工程论文
- **时间**：2020-2026 为主，允许少量高引用经典论文
- **数量**：30 篇
- **覆盖子领域**（每个 4-6 篇）：
  - 无线通信（5G/6G、调制编码、MIMO）
  - 卫星/空间通信（LEO、NTN、星地链路）
  - 网络与协议（路由、切换、资源分配）
  - 信号处理（检测、估计、滤波）
  - 天线与传播（天线设计、信道建模）
  - 通信安全/量子通信

## 目标期刊

### 核心（CSSCI/EI）
通信学报、电子学报、电子与信息学报、中国科学：信息科学、通信学报（英文版不收）

### 重要（EI/北大核心）
电波科学学报、微波学报、信号处理、电路与系统学报、西安电子科技大学学报、电子科技大学学报、北京邮电大学学报、浙江大学学报（工学版）、清华大学学报（自然科学版）

### 领域特刊
各学报的"6G""卫星通信""智能通信"等专题

## 工具使用

本项目有专用的文献检索工具链。**所有操作从项目根目录执行**：

```bash
cd /mnt/d/code/study/research-protocol
```

### 检索

```bash
# 广域检索（chinese_journal 模式，SerpAPI Scholar 源）
./tools/search "关键词1 关键词2 实验验证" --doc-types chinese_journal

# CNKI 检索 + 自动下载（首选！cookie 认证，--download 自动下载 PDF）
~/.venvs/torch/bin/python tools/cnki_login.py  # 首次获取 cookie
./tools/blit "关键词 仿真 实验" --source cnki
./tools/blit "关键词 仿真 实验" --source cnki --download jp-empirical-sources/papers/pdf/

# 单刊定向（cbpt，稳）
./tools/blit "关键词 仿真 实验" --source cbpt --journal {code}
# 常用 code：txxb（通信学报）、dianzixb（电子学报）、dzxxxb（电子与信息学报）

# 万方补充（≤10次/会话）
./tools/blit "关键词 性能评估" --source wanfang
```

### 中文查询规则

**关键词用空格分隔**：
```bash
./tools/search "低轨卫星 切换 性能仿真" --doc-types chinese_journal
```

## 检索策略

### 第一步：逐子领域检索（每个子领域 2-3 组关键词）

```bash
# 无线通信
./tools/search "5G 调制编码 性能仿真" --doc-types chinese_journal
./tools/search "MIMO 检测算法 实验对比" --doc-types chinese_journal
./tools/search "信道编码 误码率 仿真" --doc-types chinese_journal

# 卫星/空间通信
./tools/search "低轨卫星 切换 性能分析" --doc-types chinese_journal
./tools/search "星地链路 信道建模 仿真验证" --doc-types chinese_journal
./tools/search "NTN 非地面网络 资源分配" --doc-types chinese_journal

# 网络与协议
./tools/search "路由协议 性能评估 仿真" --doc-types chinese_journal
./tools/search "资源分配 算法 实验对比" --doc-types chinese_journal
./tools/search "网络切片 资源调度 仿真" --doc-types chinese_journal

# 信号处理
./tools/search "信号检测 算法 性能对比" --doc-types chinese_journal
./tools/search "信道估计 实验验证" --doc-types chinese_journal

# 天线与传播
./tools/search "天线设计 测试 验证" --doc-types chinese_journal
./tools/search "信道测量 传播模型" --doc-types chinese_journal

# 通信安全
./tools/search "物理层安全 实验验证" --doc-types chinese_journal
./tools/search "量子通信 实验 性能" --doc-types chinese_journal
```

### 第二步：单刊定向补充

如果广域检索某个子领域不足，用 cbpt 定向检索通信学报、电子学报：

```bash
./tools/blit "低轨卫星 切换 仿真" --source cbpt --journal txxb
./tools/blit "MIMO 检测 性能" --source cbpt --journal dianzixb
```

### 第三步：筛选

对搜索结果逐篇检查：
1. **期刊级别**：CSSCI / 北大核心 / EI
2. **实证要素**：
   - 有仿真/实验/实测数据（非纯理论推导）
   - 有量化指标（误码率、吞吐量、时延、频谱效率等）
   - 有对比基线（与其他方案/算法的对比）
3. **完整性**：实验条件描述是否充分（参数设置、仿真平台、数据集）

### 第四步：下载与转换

1. **CNKI 自动下载**（首选）：
   ```bash
   ./tools/blit "关键词 仿真 实验" --source cnki --download jp-empirical-sources/papers/pdf/
   ```
2. **自动下载**：`./tools/download search-archive/{date}/{file}.json`（有 URL 时自动尝试 Firecrawl Scrape）
3. **Firecrawl 单篇抓取**（对以上两种方式都失败的论文）：
   ```bash
   # 方法 A：用 tools/download 单篇重试
   ./tools/download --doi {DOI}

   # 方法 B：用 webReader 抓取 CNKI/期刊网站全文页面
   # 在 Claude Code 中用 mcp__web_reader__webReader 工具，传入论文 URL
   # CNKI 开放获取论文通常可产出 43-82KB markdown

   # 方法 C：Firecrawl MCP 工具直接抓取
   ```
   通信工程论文多在 IEEE/EI，付费墙比例高。CNKI 开放获取部分用 Firecrawl Scrape 可抓取。IEEE OA 论文也可尝试。
3. 记录仍然无法获取的论文到 `jp-empirical-sources/papers/pending-download.md`

### 第五步：结构化输出

## 输出格式

### 文件命名

`comm-{subdomain}-{author_last_name}-{year}.md`
- subdomain: wireless / satellite / network / signal / antenna / security
- 例：`comm-satellite-li-2023.md`、`comm-wireless-zhang-2022.md`

### 全文格式

```markdown
---
category: papers
source: {期刊名}
year: {发表年份}
domain: comm
subdomain: {wireless|satellite|network|signal|antenna|security}
language: zh
url: {原文链接}
doi: {DOI（如有）}
quality_tier: CSSCI | 北大核心 | EI
research_type: simulation | experiment | measurement | mixed
simulation_platform: {MATLAB|NS3|自研|实测|未知}
---

# {论文标题}

## 摘要
{完整摘要}

## 研究问题/性能目标
{论文要解决的具体问题或要优化的性能指标}

## 方法
{算法/方案描述，关键公式可保留 LaTeX}

## 实验设计
{仿真参数、数据集、测试条件、对比基线、评估指标}

## 结果
{关键性能数据，保留具体数值、图表描述}

## 结论
{核心结论和性能提升幅度}

## 参考文献
{完整参考文献列表}
```

### 仅摘要格式

同 C1/C2 格式，`full_text: false`。

### 汇总清单

写入 `jp-empirical-sources/papers/_index-C3.md`：

```markdown
# C3 论文索引（通信工程，30篇）

## 无线通信
| # | 标题 | 期刊 | 年份 | 方法 | 平台 | 全文 | 文件 |
|---|------|------|------|------|------|------|------|

## 卫星/空间通信
| # | 标题 | 期刊 | 年份 | 方法 | 平台 | 全文 | 文件 |
|---|------|------|------|------|------|------|------|

## 网络与协议
...

## 信号处理
...

## 天线与传播
...

## 通信安全
...

## 待手动下载
- [ ] {标题} — {期刊} {年份} — {URL}
```

## 完成标准

1. 总数 ≥30 篇，覆盖 ≥5 个子领域（每个 ≥4 篇）
2. 每篇确认：期刊级别 + 有实验/仿真验证
3. 每篇有完整 YAML 元数据（含 subdomain 和 simulation_platform）
4. 全文获取率 ≥50%（通信论文付费墙比例高，可以接受）
5. _index-C3.md 汇总清单完整
6. 如单次对话无法完成 30 篇，写到 pending-download.md 并说明剩余数量和已用关键词，供续接对话使用
