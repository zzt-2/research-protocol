# 对话提示词：锚点论文检索与分析

## 背景

你在为一个北京理工大学硕士论文"星地激光通信信号处理关键技术研究"做锚点论文检索。

论文计划三章内容（统一用相干检测 + QPSK/APSK）：
- Ch2: 大气湍流信道建模与估计（GG模型 + MMSE/LS/DL对比）
- Ch3: 信道均衡（CMA/DFE/MMSE/DL对比）
- Ch4: 载波同步（VV/BPS/Pilot对比）

学生本科毕设已有完整的相干检测MATLAB仿真（PSK/APSK调制、Gardner定时同步、CMA均衡、PLL载波同步、LDPC编码、帧同步）。

**目标**：找到3-5篇与上述方向高度接近的中文硕士/博士论文，作为"锚点"——确认我们计划的深度和结构是合理的。

## 任务

### 第一步：用blit工具检索CNKI

**重要：所有检索必须用 `bash tools/blit` 或 `bash tools/search`，从项目根目录调用。**

```bash
cd /mnt/d/code/study/research-protocol

# 检索1：激光通信 + 信号处理（硕士论文，985高校）
bash tools/search --source cnki --query "激光通信 信号处理" --doc-type master --limit 30

# 检索2：自由空间光通信 + 均衡（硕士+博士）
bash tools/search --source cnki --query "自由空间光通信 均衡" --limit 20

# 检索3：激光通信 载波同步（硕士+博士）
bash tools/search --source cnki --query "激光通信 载波同步" --limit 20

# 检索4：卫星光通信 信道估计（硕士+博士）
bash tools/search --source cnki --query "卫星光通信 信道估计" --limit 20

# 检索5：空间激光通信 深度学习（看看有没有类似方向）
bash tools/search --source cnki --query "空间激光通信 深度学习" --limit 20

# 检索6：星地激光通信（更精确的搜索）
bash tools/search --source cnki --query "星地激光通信" --limit 20
```

如果 tools/search 不支持 `--doc-type`，用 tools/blit：
```bash
bash tools/blit --source cnki --query "激光通信 信号处理 硕士" --limit 30
```

如果工具报错，用 WebSearch 在子agent中搜索CNKI：
- 在子agent中搜索 "site:cnki.net 激光通信 信号处理 硕士论文 985"
- 搜索 "site:cnki.net 自由空间光通信 均衡 硕士论文"
- 搜索 "site:cnki.net 星地激光通信 载波同步 论文"

### 第二步：筛选985高校论文

从检索结果中，**优先筛选以下高校的论文**：
- 北京理工大学、北京邮电大学、清华大学、北京大学
- 哈尔滨工业大学、上海交通大学、西安电子科技大学、电子科技大学
- 中国科学院大学、华中科技大学、武汉大学、国防科技大学
- 南京大学、东南大学、浙江大学

**筛选标准**（按优先级）：
1. 方向高度匹配：做的是激光/FSO通信的信号处理（信道估计/均衡/同步）
2. 方法有重叠：用了传统方法对比，或传统+DL混合
3. 系统模型相似：相干检测、PSK/QAM调制、大气湍流信道
4. 985高校优先

### 第三步：下载并分析3-5篇锚点论文

对筛选出的论文，用 `bash tools/download` 下载（或告诉用户哪些需要手动下载）。

对每篇论文，分析：
1. **章节结构**：几章主体？每章做什么？怎么串联？
2. **每章深度**：对比了几个方法？出了几张图？多少页？
3. **创新点**：宣称的创新是什么？实际是什么级别的贡献？
4. **实验设计**：仿真参数？对比基线？评价指标？
5. **和我们的差距**：它做了什么我们没计划做的？我们做了什么它没做的？

### 第四步：产出锚点分析报告

写入 `.sessions/thesis-direction-pivot/R004-anchor-papers-analysis.md`，格式：

```markdown
# [R004] 锚点论文检索与分析

## 检索结果统计
- 总检索条目数
- 985高校论文数
- 方向高度匹配的论文数

## 锚点论文详细分析

### 论文1：[标题]（[学校]，[年份]，[硕士/博士]）
- 方向匹配度：高/中/低
- 章节结构：...
- 每章深度：...
- 创新点：...
- 和我们计划的对比：...

（重复3-5篇）

## 综合结论

1. 我们的计划在深度上是否达标？
2. 我们计划的方法对比数量是否足够？
3. 我们计划的工作量（每章2-3天仿真）是否现实？
4. 有没有我们漏掉的内容是这些论文都做了的？
5. 最终建议：我们的计划需要调整什么？
```

## 约束

- 检索工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/search ...`
- 如果工具出错，在子agent中用WebSearch搜索CNKI
- 产出文件：`.sessions/thesis-direction-pivot/R004-anchor-papers-analysis.md`
- 中文输出
- 总长度3000字以内
- 如果找不到足够多的985论文，放宽到211高校也可以
