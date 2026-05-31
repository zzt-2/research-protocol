# 对话提示词：Ch4 载波同步 — 系统文献检索

> 写入产出到: R007-ch4-literature-review.md

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，Ch4 做载波同步/相位恢复。

**已确认的技术路线**：
- 必须用相干检测（IM/DD不需要载波同步）
- 传统方法：VV(QPSK最优) / BPS(高阶调制鲁棒) / Pilot-aided(低SNR好)
- DL对比：RNN/GRU（可选，增益<1dB，不作为主线）
- 仿真平台：Python + OptiCommPy（有现成VV实现）
- 学生本科已有PLL载波同步框架，换鉴相器即得VV/BPS

**关键已知坑点**：
- 多普勒±4.6GHz必须LO预补偿，VV/BPS只处理残余频偏
- VV有4折相位模糊，需差分编码或导频解决
- 创新点偏弱——VV/BPS在光纤中已大量研究，FSO场景需找差异化

**最关键的问题**：创新点够不够？如果"VV/BPS/Pilot在FSO湍流下的对比"已经有人做了，Ch4还需要加什么？

## 检索步骤

### CNKI检索

```bash
cd /mnt/d/code/study/research-protocol

# R1: 载波同步 + 激光/光通信
bash tools/search --source cnki --query "载波同步 激光通信" --limit 30

# R2: 相位恢复 + 光通信
bash tools/search --source cnki --query "相位恢复 光通信" --limit 30

# R3: 卫星光通信同步
bash tools/search --source cnki --query "卫星光通信 同步" --limit 20

# R4: Viterbi算法 光通信
bash tools/search --source cnki --query "Viterbi 载波恢复 光" --limit 20

# R5: 星地链路多普勒补偿
bash tools/search --source cnki --query "星地 多普勒 光通信" --limit 20

# R6: 相干检测 + FSO
bash tools/search --source cnki --query "相干检测 自由空间光" --limit 20
```

### 英文检索

```bash
# R7: carrier phase recovery FSO
bash tools/search --query "carrier phase recovery free space optical" --limit 20

# R8: Viterbi-Viterbi BPS optical communication
bash tools/search --query "Viterbi-Viterbi BPS carrier recovery optical" --limit 20

# R9: satellite optical Doppler compensation
bash tools/search --query "satellite optical communication Doppler frequency compensation" --limit 20

# R10: carrier synchronization coherent FSO turbulence
bash tools/search --query "carrier synchronization coherent FSO atmospheric turbulence" --limit 20

# R11: pilot-aided carrier recovery optical
bash tools/search --query "pilot-aided carrier recovery optical communication" --limit 20
```

### 下载+分析

同PROMPT-005的流程。

## 重点关注

1. **创新点排查**：搜索"VV/BPS/Pilot在FSO湍流下的对比"是否已有论文做过。如果做了，我们的差异化在哪里？
2. **FSO vs 光纤的区别**：载波同步在FSO和光纤中的技术差异有哪些？湍流对载波同步的具体影响是什么？
3. **多普勒补偿方案**：LEO场景下多普勒频移的实际处理方案？轨道预测+LO预补偿的具体实现？
4. **DL载波同步的最新进展**：2024-2026年有没有突破性的DL载波同步方法？
5. **OptiCommPy生态**：有没有用OptiCommPy做FSO载波同步的先例？

## 创新点评估（最关键）

如果"方法对比"创新点不够，需要评估以下替代/补充创新点：
1. "湍流强度对VV/BPS性能的系统影响分析"——是否已有人做？
2. "联合频偏+相位噪声补偿方案"——有没有FSO场景的先例？
3. "自适应窗口长度的VV算法"——有没有改进空间？
4. "FSO场景下载波同步的参数优化指南"——工程贡献，有没有文献空白？

## 产出格式

同PROMPT-005结构，额外增加：

```markdown
## 创新点评估
| 候选创新点 | 是否已有先例 | 文献支撑 | 可行性 |
|-----------|------------|---------|--------|
| 方法对比(VV/BPS/Pilot) | | | |
| 湍流鲁棒性分析 | | | |
| 联合频偏+相位补偿 | | | |
| 自适应窗口VV | | | |
| DL对比(RNN/GRU) | | | |

## 推荐创新点
[基于文献检索结果，推荐Ch4应该采用的创新点]
```

产出文件：`.sessions/thesis-direction-pivot/R007-ch4-literature-review.md`
