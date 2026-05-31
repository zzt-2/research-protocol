# 对话提示词：Ch4方向广搜 + 调制格式全局评估 + 三章仿真坑排查

> 产出文件: 结论更新到 `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
> 优先级: 高（Ch4方向未定，调制格式影响全局）
> 依赖: S005、R012/R013/R014（已完成检索）
> 预计耗时: 45-60分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。三章框架已基本确认，但有两个全局性问题未解决：

1. **Ch4方向未定**：R012确认"自适应CPR切换"No-Go，但Ch4到底做什么还没有定。导师原话是"同步算法（载波同步等）"，这个"等"字留了空间。不能假设Ch4一定是CPR。
2. **调制格式影响全局**：R014建议SP-QPSK，但需要确认这个选择对三章所有方法是否都合适。
3. **仿真坑**：之前只考虑了"能不能跑"，没有逐章排查每个方法的仿真陷阱。

## 前置条件

读取以下文件恢复上下文：
1. `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md` — 当前状态和已有结论
2. `.sessions/thesis-direction-pivot/R012-ch4-adaptive-cpr-verification.md` — Q1-Q3结论
3. `.sessions/thesis-direction-pivot/R013-ch3-precompensation-simulation-verification.md` — Q4-Q6结论
4. `.sessions/thesis-direction-pivot/R014-fpga-global-risk-verification.md` — Q7-Q8结论

## 必须回答的问题

### A. Ch4方向广搜（不预设CPR）

导师框架："同步算法（载波同步等）"。本科毕设已有PLL载波同步+Gardner定时同步。
需要广泛搜索，找出最适合做硕士论文Ch4的方向。

检索策略（第一轮，广泛撒网）：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "synchronization satellite free space optical coherent QPSK algorithm" --max 20 --source s2,openalex
bash tools/search --query "timing recovery clock synchronization atmospheric turbulence optical communication" --max 20 --source s2,openalex
bash tools/search --query "frequency offset estimation Doppler LEO satellite optical coherent compensation" --max 20 --source s2,openalex
bash tools/search --query "frame synchronization carrier recovery joint FSO turbulent channel" --max 15 --source s2,openalex
```

第二轮（基于第一轮结果定向）：
- 对第一轮中发现的有前景方向，做针对性深搜

对每个候选方向，回答：
1. 文献基础是否充分？（有≥5篇直接相关论文？）
2. 创新空间有多大？（已有人做到什么程度？还剩什么空白？）
3. 仿真难度如何？（需要什么模型？Python能做吗？工作量几天？）
4. 已知仿真坑有哪些？
5. 与Ch2(信道估计)+Ch3(预补偿)的联动是否自然？
6. FPGA可实现性？（Ch5要验证这个方向）

候选方向（不限于）：
- 载波相位恢复（VV/BPS/Pilot/Kalman）
- 联合频偏+相位恢复（FOE+CPR两阶段）
- 定时同步（Gardner等在湍流下）
- 帧同步+载波联合
- 偏振跟踪（需DP-QPSK）
- 其他第一轮检索中发现的方向

### B. 调制格式对三章方法的全局影响

已建议SP-QPSK（R014）。需要确认：

检索：
```bash
bash tools/search --query "QPSK coherent FSO satellite channel estimation equalization synchronization simulation" --max 15 --source s2,openalex
bash tools/search --query "single polarization QPSK vs dual polarization FSO coherent complexity comparison" --max 10 --source s2,openalex
```

逐章检查：

**Ch2 信道估计**：
- SP-QPSK下LS/MMSE信道估计怎么实现？估计的是标量h还是复数h？
- 相干检测下信道估计和IM/DD下的区别是什么？（IM/DD估计实值，相干估计复值）
- DL估计（MLP/LSTM）在SP-QPSK下输入是什么？（接收信号y=hx+n中的y？）

**Ch3 预补偿**：
- SP-QPSK下功率自适应预补偿是否有文献用SP-QPSK做？
- 反馈延迟建模是否受调制格式影响？

**Ch4（待定方向）**：
- SP-QPSK对Ch4各候选方向的适配性？
- 是否有方法只在DP-QPSK下才有意义（如偏振跟踪）？

### C. 三章仿真坑逐一排查

对以下每个方法，检索其仿真实现中的已知问题：

**Ch2 方法**：
```bash
bash tools/search --query "LS MMSE channel estimation Gamma-Gamma turbulence coherent optical implementation pitfalls" --max 10 --source s2,openalex
```
- LS估计在低SNR下是否数值不稳定？
- MMSE需要信道统计先验（α,β），如果估计不准会怎样？
- DL训练数据怎么生成？需要多少样本？过拟合风险？
- BER曲线收敛需要多少Monte Carlo符号数？

**Ch3 方法**：
```bash
bash tools/search --query "adaptive power control FSO turbulence feedback delay simulation outage probability" --max 10 --source s2,openalex
```
- 反馈延迟怎么建模？固定延迟？随机延迟？
- 功率约束（最大发射功率）怎么设？
- 中断概率和平均BER的计算有什么坑？
- GG信道的时变特性怎么仿真？自相关时间是多少？

**Ch4 方法**（对第一轮筛选出的方向）：
- 各方法的具体仿真参数怎么选？（VV窗口、BPS测试相位数、训练序列长度等）
- Monte Carlo BER计算的符号数需求？
- 有没有常见但容易忽略的仿真错误？（如相位模糊、判决区域错误等）

**全局仿真问题**：
- 三章是否可以用统一的仿真框架？（信号生成→GG信道→处理→BER）
- GG信道模型的边缘case（α≈β≈1强湍流时采样稳定性？）
- SNR范围怎么选？步进多少？每个SNR点跑多少符号？

## 输出格式

### A. Ch4方向对比

| 方向 | 文献基础 | 创新空间 | 仿真难度 | 与Ch2/Ch3联动 | FPGA | 推荐度 |
|------|---------|---------|---------|-------------|------|--------|
| 载波相位恢复(VV/BPS) | ... | ... | ... | ... | ... | ★★★ |
| 联合FOE+CPR | ... | ... | ... | ... | ... | ★★★ |
| 定时同步 | ... | ... | ... | ... | ... | ★★★ |
| [其他方向] | ... | ... | ... | ... | ... | ★★★ |

**最终推荐**：Ch4应做[方向X]，理由：...

### B. 调制格式确认

| 章 | SP-QPSK适配性 | 是否需要DP-QPSK | 理由 |
|---|-------------|---------------|------|
| Ch2 | ... | ... | ... |
| Ch3 | ... | ... | ... |
| Ch4 | ... | ... | ... |

**建议**：[SP-QPSK / DP-QPSK]，理由：...

### C. 仿真坑清单

| 章 | 方法 | 已知仿真坑 | 应对方案 | 文献来源 |
|---|------|----------|---------|---------|
| Ch2 | LS估计 | ... | ... | ... |
| Ch2 | MMSE估计 | ... | ... | ... |
| ... | ... | ... | ... | ... |

## 约束

- 必须用 `tools/search` 检索，禁止 WebSearch
- 每条结论必须有论文引用，不靠推理
- 不写代码、不做仿真
- 中文输出
- 检索结果存档到 `search-archive/2026-05-29/`
- 如果45分钟内做不完A+B+C，优先完成A（Ch4方向），B和C的初步结论也一并给出
