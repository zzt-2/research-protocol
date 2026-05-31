# 对话提示词：Ch3 信道均衡 — 系统文献检索

> 写入产出到: R006-ch3-literature-review.md

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，Ch3 做信道均衡。

**已确认的技术路线**：
- 做后均衡（不做预均衡——CSI反馈延迟是根本瓶颈，R002已确认）
- 传统方法：CMA（学生本科已实现）/ MMSE / DFE / LMS自适应
- DL对比：CNN/LSTM均衡器
- 仿真平台：Python，相干检测 + PSK调制 + GG湍流信道
- 关键条件：DL均衡器仅在中强湍流(σ²_I≥1)下优于MMSE

**关键已知坑点**：
- FSO用IM/DD时信号是实值，不能直接搬RF复值均衡代码（但我们用相干检测，是复值信号）
- 均衡前需先做符号定时同步（可假设理想同步）
- 弱湍流下DL无增益，必须设计中强湍流场景

## 检索步骤

### CNKI检索

```bash
cd /mnt/d/code/study/research-protocol

# R1: FSO均衡
bash tools/search --source cnki --query "自由空间光通信 均衡" --limit 30

# R2: 激光通信均衡
bash tools/search --source cnki --query "激光通信 均衡算法" --limit 30

# R3: 大气湍流补偿
bash tools/search --source cnki --query "大气湍流 光通信 补偿" --limit 20

# R4: DL均衡+光通信
bash tools/search --source cnki --query "深度学习 光通信 均衡" --limit 20

# R5: CMA/DFE在FSO中的应用
bash tools/search --source cnki --query "CMA均衡 自由空间光" --limit 20
bash tools/search --source cnki --query "判决反馈均衡 光通信" --limit 20
```

### 英文检索

```bash
# R6: FSO equalization survey
bash tools/search --query "free space optical communication equalization survey" --limit 20

# R7: deep learning equalizer FSO
bash tools/search --query "deep learning equalizer free space optical" --limit 20

# R8: MMSE DFE FSO turbulence
bash tools/search --query "MMSE DFE equalization FSO atmospheric turbulence" --limit 20

# R9: adaptive equalization optical wireless
bash tools/search --query "adaptive equalization optical wireless LMS RLS" --limit 20
```

### 下载+分析

同PROMPT-005的流程。对高相关论文下载并提取结构化信息。

## 重点关注

1. **后均衡在FSO中的具体实现**：有哪些论文实际做了MMSE/DFE均衡并给出了BER数字？
2. **DL均衡器在FSO中的效果**：具体提升多少BER？在什么湍流条件下有效？
3. **均衡和信道估计的耦合**：Ch3均衡器的输入来自Ch2信道估计——这种联合设计有没有文献先例？
4. **CMA在FSO中的适用性**：学生本科CMA均衡器能不能直接用到GG湍流信道？有没有文献做过？
5. **创新点确认**："FSO湍流信道下的均衡方法对比"是否已有人做过？如果做过，我们还能做什么差异？

## 产出格式

同PROMPT-005的结构，但额外增加：

```markdown
## 预均衡相关发现
[虽然不做预均衡，但需要了解这个方向的文献，以备导师追问]

## CMA在FSO中的适用性
[评估学生本科CMA代码能否直接用于GG信道]

## 均衡+信道估计联合设计
[是否有先例支持Ch2→Ch3的数据流设计]
```

产出文件：`.sessions/thesis-direction-pivot/R006-ch3-literature-review.md`
