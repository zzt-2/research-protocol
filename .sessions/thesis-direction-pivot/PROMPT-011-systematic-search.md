# 对话提示词：框架合规系统检索（替代R004-R007）

> 产出文件: projects/thesis-fso/literature_notes.md（初版）+ search-archive/
> 优先级: 最高（后续所有步骤的基础）
> 预计耗时: 2-3小时

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，三章：Ch2信道估计 → Ch3信道均衡 → Ch4载波同步。

**之前的R004-R007检索全部未用项目工具，结论未经验证，不可靠。本次是正规检索。**

**已确认的技术路线**：
- 统一仿真方案：相干检测 + QPSK + GG大气湍流模型 + Python全栈
- 策略：传统方法主线，DL作为对比实验（不押注DL必须赢）
- Ch3做后均衡（不做预均衡）
- 本科代码：完整相干检测MATLAB仿真，有CMA均衡器和PLL载波同步

**已知的选题安全性**：
- 张岱2018国防科大论文已确认为AI幻觉（CNKI搜不到）
- Ch4的VV/BPS对比已被Liu 2023做过（R008确认存在）

## 框架要求

本次检索必须严格遵循 `stages/gw-search.md` 的流程。核心要求：

1. **必须用 `bash tools/search` 脚本检索**，不要用 WebSearch 或其他方式
2. 结果自动保存到 `search-archive/{date}/{slug}.json`
3. 每个方向 ≥3 组不同角度的搜索关键词
4. 多源搜索，每源 ≥15 条
5. AI候选审查：对每条标注 priority 和 priority_reason
6. 二轮定向检索：识别候选方向后做定向深搜验证空白
7. 中文文献用 `bash tools/blit --source cnki` 补充

**质量门槛**：
- 去重后 ≥20 条候选/方向
- 覆盖 ≥3 个搜索源
- "必读"类 ≥5 篇/方向
- 覆盖 ≥2 个不同子方向/技术路线
- 正式发表文献占比 ≥50%

## 操作步骤

### 第一阶段：初始化项目目录

```bash
cd /mnt/d/code/study/research-protocol
mkdir -p projects/thesis-fso
```

### 第二阶段：Ch2 信道估计检索（英文+中文）

```bash
# E2-1: FSO信道估计综述/方法
bash tools/search --query "free space optical channel estimation survey" --limit 20 --mode academic

# E2-2: DL信道估计FSO
bash tools/search --query "deep learning channel estimation free space optical Gamma-Gamma" --limit 20

# E2-3: LEO卫星光通信信道模型
bash tools/search --query "LEO satellite optical channel model atmospheric turbulence estimation" --limit 20

# E2-4: LS MMSE Kalman信道估计对比
bash tools/search --query "LS MMSE Kalman channel estimation comparison optical wireless" --limit 20

# C2-1: FSO信道估计（中文）
bash tools/blit --source cnki --query "自由空间光通信 信道估计" --limit 30

# C2-2: GG大气湍流（中文核心文献）
bash tools/blit --source cnki --query "Gamma-Gamma 大气湍流 信道" --limit 20

# C2-3: 星地激光信道（中文）
bash tools/blit --source cnki --query "星地激光 信道建模" --limit 20
```

### 第三阶段：Ch3 信道均衡检索

```bash
# E3-1: FSO均衡综述
bash tools/search --query "free space optical communication equalization survey" --limit 20

# E3-2: MMSE DFE FSO湍流
bash tools/search --query "MMSE DFE equalization FSO atmospheric turbulence coherent" --limit 20

# E3-3: DL均衡器FSO
bash tools/search --query "deep learning neural network equalizer free space optical" --limit 20

# E3-4: CMA均衡光通信
bash tools/search --query "CMA equalization coherent optical communication" --limit 20

# C3-1: 激光通信均衡（中文）
bash tools/blit --source cnki --query "激光通信 均衡算法" --limit 30

# C3-2: CMA自适应均衡（中文）
bash tools/blit --source cnki --query "CMA均衡 自适应 光通信" --limit 20

# C3-3: 大气湍流补偿（中文）
bash tools/blit --source cnki --query "大气湍流 光通信 补偿 均衡" --limit 20
```

### 第四阶段：Ch4 载波同步检索

```bash
# E4-1: 载波相位恢复FSO
bash tools/search --query "carrier phase recovery coherent free space optical communication" --limit 20

# E4-2: VV BPS载波恢复对比
bash tools/search --query "Viterbi-Viterbi BPS carrier recovery comparison optical" --limit 20

# E4-3: 湍流下载波同步
bash tools/search --query "carrier synchronization atmospheric turbulence optical communication" --limit 20

# E4-4: 多普勒补偿卫星光通信
bash tools/search --query "Doppler compensation satellite optical coherent communication" --limit 20

# C4-1: 载波同步激光通信（中文）
bash tools/blit --source cnki --query "载波同步 激光通信 相干" --limit 20

# C4-2: 相位恢复光通信（中文）
bash tools/blit --source cnki --query "相位恢复 相干光通信" --limit 20

# C4-3: 星地多普勒（中文）
bash tools/blit --source cnki --query "星地 多普勒 光通信 补偿" --limit 20
```

### 第五阶段：AI候选审查

对每轮搜索结果（search-archive JSON）执行AI审查：
1. 读取 JSON 文件
2. 对每条候选，综合 title + abstract + venue + year + citation_count，判断真实语义相关性
3. 标注 priority（必读/建议读/待确认/备选/排除）和 priority_reason
4. 输出统计：各优先级数量分布

### 第六阶段：二轮定向检索

基于一轮审查结果，识别候选研究方向和空白区域，构造定向关键词：
- 如果发现"GG湍流+相干PSK+均衡对比"确实空白 → 验证空白真实性
- 如果发现某个方法在FSO中已充分研究 → 标记为非创新方向
- 针对一轮中覆盖不足的方向补充搜索

### 第七阶段：参数提取

从搜索结果中提取以下参数的文献来源（这是MVE的关键输入）：

| 参数 | 需要提取的信息 | 关注哪些论文 |
|------|--------------|------------|
| GG湍流参数(α,β) | 弱/中/强三档的α,β值及对应Cn²范围 | Andrews & Phillips 2005, Khalighi 2014综述, 曹明华2020 |
| 星地链路距离 | LEO典型高度（500-2000km） | Xu 2025, Paillier 2020 |
| 波长 | 1550nm或其他标准波长 | 综述论文 |
| 符号速率 | 星地激光典型值 | 实验类论文 |
| SNR范围 | 实际星地链路SNR | 信道建模论文 |
| CMA参数 | 抽头数、步长典型值 | 佟欣2020, Almogahed 2022 |
| VV窗口长度 | 最优窗口和Δν·Rs关系 | Liu 2023, Shi 2025 |

## 产出格式

### 1. 搜索存档

自动保存到 `search-archive/2026-05-29/` 下。

### 2. literature_notes.md（初版）

```markdown
# 文献调研笔记 — 星地激光通信信号处理

## 步骤进度
| 步骤 | 状态 | 日期 | 备注 |
|------|------|------|------|
| Step 1 检索+初筛 | ✅ | 2026-05-29 | PROMPT-011 |
| Step 2 论文获取 | ⬜ | | |
| Step 3 精读 | ⬜ | | |
| Step 3.5 定向补充 | ⬜ | | |

## 候选论文列表

### Ch2 信道估计
| # | 标题 | 年份 | 期刊 | 引用 | 优先级 | 原因 |
|---|------|------|------|------|--------|------|
| ... | | | | | 必读/建议读/... | |

### Ch3 信道均衡
[同上]

### Ch4 载波同步
[同上]

## 研究空白汇总
[从搜索结果中识别的空白]

## 参数来源表
| 参数 | 值 | 来源论文 | 来源类型 |
|------|-----|---------|---------|
| GG弱湍流α,β | | | [实证]/[综述]/[理论] |
| ... | | | |

## 综合分析
### 领域概况
### 核心挑战
### 研究定位
```

### 3. 搜索统计报告

```
总检索轮次：XX
总检索条目数：XX
去重后条目数：XX
必读篇数/方向：Ch2=XX, Ch3=XX, Ch4=XX
搜索源覆盖：Semantic Scholar / Crossref / CNKI / ...
正式发表占比：XX%
覆盖子方向：[列出每个方向覆盖的技术路线]
```

## 约束

- **必须用项目工具**：`bash tools/search` 和 `bash tools/blit`，绝对不要用 WebSearch
- 从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/...`
- 搜索结果 JSON 保存在 search-archive/，不要挪到别处
- literature_notes.md 放在 `projects/thesis-fso/` 下
- 中文输出
- 如果 tools/search 参数不支持（如 --doc-type），改用 tools/blit
- 总耗时控制在 2-3 小时
