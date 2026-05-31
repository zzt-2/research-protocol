# 对话提示词：选题撞车检查 + Ch4创新点验证

> 产出文件: R008-collision-and-ch4-verify.md
> 优先级: 最高（决定方向是否需要调整）

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，三章：信道估计→信道均衡→载波同步。

**上一轮检索（未用项目工具）报告了两个致命风险，必须验证：**

### 风险1: 选题撞车
张岱（国防科技大学，2018，硕士）论文标题"星地相干激光通信大气信道特征及信号处理技术研究"，与我们几乎完全重叠。如果连章节内容也重叠，导师必批。

### 风险2: Ch4创新点已被抢占
Liu 2023（Optics Communications, 15 cites）报告已做VV/BPS在星地相干激光通信中的载波恢复对比。如果属实，Ch4的"方法对比"创新点就不成立。

## 检索任务

### 任务A: 张岱论文验证

```bash
cd /mnt/d/code/study/research-protocol

# A1: 搜索张岱的论文
bash tools/search --source cnki --query "张岱 星地相干激光通信" --limit 10

# A2: 搜索近似标题的论文（看有没有其他人也做了类似的）
bash tools/search --source cnki --query "星地激光通信 信号处理" --limit 20 --doc-type master

# A3: 搜索近似标题的博士论文
bash tools/search --source cnki --query "星地激光通信 信号处理" --limit 20 --doc-type phd

# A4: 如果找到张岱论文，用 blit 下载全文或摘要
bash tools/blit --source cnki --download <论文ID或DOI>
```

**关键问题**：
1. 张岱论文的**章节结构**是什么？做了哪些具体内容？
2. 与我们的三章（信道估计+均衡+载波同步）重叠多少？
3. 如果高度重叠，我们的**差异化**在哪里？（DL方法？方法对比更系统？场景不同？）

### 任务B: Ch4创新点验证

```bash
cd /mnt/d/code/study/research-protocol

# B1: 搜索 Liu 2023 载波恢复星地论文
bash tools/search --query "carrier recovery satellite-to-ground coherent laser Liu 2023" --limit 10

# B2: 搜索 VV BPS FSO 对比论文
bash tools/search --query "Viterbi-Viterbi BPS comparison free space optical" --limit 20

# B3: 搜索湍流下载波恢复论文
bash tools/search --query "carrier phase recovery atmospheric turbulence FSO" --limit 20

# B4: 搜索湍流强度对载波同步影响
bash tools/search --query "turbulence intensity carrier synchronization optical" --limit 20

# B5: 搜索 FSO 载波同步 激光通信（中文）
bash tools/search --source cnki --query "载波恢复 相干 激光通信 湍流" --limit 20

# B6: 搜索星地相干光通信载波同步
bash tools/search --source cnki --query "星地 相干光通信 载波同步" --limit 20
```

**关键问题**：
1. Liu 2023 是否真的做了VV/BPS在星地链路的对比？具体结论是什么？
2. "大气湍流强度变化对VV/BPS/Pilot性能的系统性影响分析"是否有论文做过？
3. Ch4的最强创新点应该是什么？如果方法对比已被做，湍流鲁棒性分析能撑起一章吗？

### 任务C: 全局选题独特性检查

```bash
# C1: 搜索与我们标题高度匹配的论文
bash tools/search --source cnki --query "星地激光通信信号处理" --limit 20

# C2: 英文搜索
bash tools/search --query "satellite-to-ground laser communication signal processing" --limit 20
```

## 产出格式

```markdown
# [R008] 选题撞车检查 + Ch4创新点验证

## 任务A: 张岱论文验证
### 搜索结果
[原始搜索结果]

### 张岱论文分析
- 标题：
- 学校/年份：
- 章节结构：
- 与我们计划的重叠度：X/10
- 关键差异点：

### 结论：选题是否需要调整？

## 任务B: Ch4创新点验证
### Liu 2023验证
[搜索结果 + 内容确认]

### 湍流+CPR空白确认
[搜索结果]

### 结论：Ch4可行创新点是什么？

## 任务C: 全局独特性
[其他近似标题论文列表]

## 综合结论
1. 选题是否安全？
2. Ch4是否需要换方向？
3. 如果需要调整，推荐方案是什么？
```

## 约束

- **必须用项目工具**：`bash tools/search` 和 `bash tools/blit`，不要用 web search
- 从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/...`
- 如果 tools/search 不支持 --source cnki 或 --doc-type，改用 `bash tools/blit --source cnki`
- 中文输出
- 3000字以内
- 产出文件：`.sessions/thesis-direction-pivot/R008-collision-and-ch4-verify.md`
