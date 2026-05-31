# 对话提示词：FPGA选题+全局风险验证

> 产出文件: 结论更新到 `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
> 优先级: 高
> 依赖: S002、S005
> 预计耗时: 20-30分钟

## 背景

硕士论文Ch5（半章，FPGA实现/验证）的选题，以及全局性风险排查。

本对话唯一任务：用 `tools/search` 检索回答以下2个问题，每条结论附论文引用。

## 前置条件

读取以下文件恢复上下文：
1. `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
2. `.sessions/thesis-direction-pivot/S002-systematic-search-and-direction-rethink.md` — 第六阶段FPGA部分

## 必须回答的问题

### Q7：哪个模块上FPGA有文献先例？

用户已有Verilog代码：CMA 16抽头、FFT+NCO、Gardner定时同步。

需要确认：
- 星地/空间激光通信的FPGA实现，有没有已发表的论文？做的哪些模块？
- "多普勒+湍流联合FPGA验证"是否真的没人做过？
- 如果只做接收端DSP链（Gardner+FOE+CPR），半章篇幅够不够？

检索：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "FPGA implementation carrier synchronization coherent optical satellite communication" --max 15 --source s2,openalex
bash tools/search --query "FPGA real-time DSP free space optical link carrier recovery" --max 15 --source s2,openalex
bash tools/search --query "FPGA 激光通信 载波同步 相干检测 实时" --max 10 --source cnki
bash tools/search --query "FPGA digital signal processing coherent optical receiver Doppler compensation" --max 15 --source s2,openalex
```

要回答：
- 已有的FPGA+光通信论文覆盖了哪些模块？
- "多普勒+湍流联合FPGA验证"作为创新点的文献空白是否真实？
- 接收端DSP链上FPGA的工作量是否在半章范围内？
- 用户的Verilog代码（CMA+FFT+NCO+Gardner）在这个方向上的复用率是多少？

### Q8：调制格式不确定性的全局影响

当前方案未确定QPSK还是DP-QPSK。这影响：
- Ch2：单偏振信道估计 vs 2×2 MIMO信道估计
- Ch3：单偏振预补偿 vs 偏振解复用+预补偿
- Ch4：单偏振CPR vs 偏振+相位联合恢复
- FPGA：1路 vs 2路处理

检索：
```bash
bash tools/search --query "dual polarization QPSK free space optical satellite coherent detection complexity" --max 15 --source s2,openalex
bash tools/search --query "single polarization vs dual polarization FSO coherent satellite tradeoff" --max 10 --source s2,openalex
```

要回答：
- 星地FSO论文中，QPSK和DP-QPSK哪种更常见？
- DP-QPSK带来的偏振解复用额外复杂度有多大？（CMA→2×2 MIMO CMA）
- 如果用QPSK（单偏振），三章仿真是否都能成立？
- 导师或领域惯例是否倾向于某种格式？

## 输出格式

每个问题：
```
### Q{n}: {问题}
- 结论：{一句话}
- 证据：{论文标题+年份+关键数据}
- 可信度：高/中/低
- 对选题的影响
```

最后给出综合判断：
- FPGA选题推荐：做哪个模块？故事怎么讲？
- 调制格式建议：QPSK还是DP-QPSK？理由
- 是否需要和导师确认

## 约束

- 必须用 `tools/search` 检索，禁止 WebSearch
- 每条结论必须有论文引用，不靠推理
- 不写代码、不做仿真
- 中文输出
- 检索结果存档到 `search-archive/2026-05-29/`
