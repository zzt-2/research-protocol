# 对话提示词：Ch2 信道估计 — 系统文献检索

> 写入产出到: R005-ch2-literature-review.md

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，Ch2 做大气湍流信道建模与估计。

**已确认的技术路线**：
- 信道模型：Gamma-Gamma（主线），可扩展 Exponentiated Weibull
- 估计方法：LS / MMSE / Kalman（传统）+ MLP/LSTM（DL对比）
- 仿真平台：Python（NumPy/SciPy/PyTorch），相干检测 + PSK调制
- 学生已有：完整相干检测MATLAB仿真（PLL载波同步、Gardner定时、CMA均衡）
- 缺口：GG大气湍流信道模型需从零实现

**目标**：用项目的检索工具做系统文献检索，确认Ch2方向的文献基础、研究空白、可用基线方法。

## 检索步骤

### 第一步：中文文献检索（CNKI）

```bash
cd /mnt/d/code/study/research-protocol

# R1: 广域搜索 — FSO信道估计
bash tools/search --source cnki --query "自由空间光通信 信道估计" --limit 30

# R2: 广域搜索 — 激光通信信道建模
bash tools/search --source cnki --query "激光通信 信道建模" --limit 30

# R3: 精确搜索 — GG模型应用
bash tools/search --source cnki --query "Gamma-Gamma 大气湍流" --limit 20

# R4: DL+FSO信道
bash tools/search --source cnki --query "深度学习 自由空间光 信道" --limit 20

# R5: 星地激光信道
bash tools/search --source cnki --query "星地激光 信道" --limit 20
```

### 第二步：英文文献检索

```bash
# R6: FSO channel estimation survey
bash tools/search --query "FSO channel estimation survey" --limit 20

# R7: Gamma-Gamma model deep learning
bash tools/search --query "Gamma-Gamma channel deep learning estimation" --limit 20

# R8: LEO satellite optical channel model
bash tools/search --query "LEO satellite optical channel model atmospheric turbulence" --limit 20

# R9: neural network channel estimation optical wireless
bash tools/search --query "neural network channel estimation optical wireless communication" --limit 20
```

### 第三步：下载关键论文

对每轮检索中相关性高的论文（相关性评分≥7），用 `bash tools/download` 下载。
优先下载：综述论文、方法对比论文、GG模型论文、DL信道估计论文。

### 第四步：分析检索结果

对每篇高相关论文提取：
1. 研究问题和方法
2. 信道模型（GG? Lognormal? 其他?）
3. 估计方法（LS/MMSE/DL?）
4. 性能指标和结果（BER/NMSE具体数字）
5. 研究空白/未解决问题

## 产出格式

```markdown
# [R005] Ch2 信道估计 — 系统文献检索

## 检索统计
- CNKI检索轮次：5
- 英文检索轮次：4
- 总检索条目数：XX
- 高相关条目数（≥7分）：XX
- 已下载论文数：XX

## CNKI检索结果

### R1: 自由空间光通信 信道估计
[结构化列出结果，标注相关性评分]

### R2: 激光通信 信道建模
[...]

（每轮检索结果都列出）

## 英文检索结果

### R6-R9: [...]
[结构化列出]

## 关键论文分析（Top 5-8篇）

### 论文1: [标题] ([年份], [期刊])
- 相关性：X/10
- 方法：...
- 结果：...
- 对我们的意义：...

## 研究空白汇总

1. [空白1]：[哪些论文提到了这个问题]
2. [空白2]：...

## 结论

1. Ch2方向的文献基础是否充足？
2. 最常用的传统基线方法是什么？
3. DL方法的实际效果如何（具体数字）？
4. 推荐的实验方案是否需要调整？
5. 有没有我们漏掉的重要方法或指标？
```

## 约束

- 所有工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/...`
- 如果 tools/search 不支持 --source cnki，改用 tools/blit
- 下载的论文存入 papers/ 目录（tools/download 自动处理路径）
- 产出文件：`.sessions/thesis-direction-pivot/R005-ch2-literature-review.md`
- 中文输出
- 3000字以内
