# 对话提示词：Ch3预补偿+仿真关键不确定项验证

> 产出文件: 结论更新到 `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
> 优先级: 高
> 依赖: S002、S005、literature_notes.md
> 预计耗时: 30-40分钟

## 背景

硕士论文Ch3"信道预补偿"和仿真系统的关键不确定项。以下问题目前只有旧文档中的推理，没有任何正规检索验证。

本对话唯一任务：用 `tools/search` 检索回答以下3个问题，每条结论附论文引用。

## 前置条件

读取以下文件恢复上下文：
1. `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
2. `.sessions/thesis-direction-pivot/S002-systematic-search-and-direction-rethink.md` — 第五、六阶段
3. `projects/thesis-fso/literature_notes.md`

## 必须回答的问题

### Q4：星地FSO信道互易性假设是否有文献支撑？

Ch3计划做"发射端自适应预补偿"——在发射端基于估计的CSI做功率/符号率调整。这要求上下行信道具有互易性。

检索：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "channel reciprocity free space optical satellite uplink downlink" --max 15 --source s2,openalex
bash tools/search --query "digital pre-compensation transmitter FSO satellite coherent optical" --max 15 --source s2,openalex
bash tools/search --query "星地激光通信 信道互易性 上行预补偿" --max 10 --source cnki
```

要回答：
- 星地FSO上下行信道互易性是否成立？在什么条件下成立/不成立？
- 如果不互易，预补偿方案的物理基础是否存在？
- Fernandes 2023 (JLT, 31引) 的Doppler预补偿方案是否依赖互易性？
- 有没有论文专门讨论或质疑星地FSO的互易性假设？

### Q5：湍流相位闪烁怎么建模？

当前仿真用GG模型只产生幅度衰落。但Ch4载波同步关心的是相位变化。这是仿真的关键缺口。

检索：
```bash
bash tools/search --query "atmospheric turbulence phase screen simulation coherent optical communication" --max 15 --source s2,openalex
bash tools/search --query "Gamma-Gamma turbulence phase model coherent detection carrier synchronization" --max 15 --source s2,openalex
bash tools/search --query "turbulence induced phase noise FSO coherent receiver simulation" --max 15 --source s2,openalex
```

要回答：
- 星地FSO中湍流引起的相位起伏如何建模？（Zernike？相位屏？统计模型？）
- GG模型能否扩展到相位域？还是需要单独的相位模型？
- 这个相位起伏的量级（rad）是多少？和激光线宽引起的相位噪声相比如何？
- 如果湍流相位起伏很小（<激光线宽），Ch4的"湍流鲁棒性分析"就没有意义

### Q6：预补偿"功率+符号率自适应"在GG湍流下是否真的有增益？

S002第六阶段调研推荐的Ch3方向。但导师原始框架只说"预补偿"，具体技术路线待定。
关键质疑：如果GG湍流是慢变的（相干时间ms级），简单的固定功率就够了，自适应是否有额外增益？

检索：
```bash
bash tools/search --query "adaptive power allocation FSO turbulence Gamma-Gamma satellite" --max 15 --source s2,openalex
bash tools/search --query "symbol rate adaptation free space optical atmospheric turbulence" --max 10 --source s2,openalex
bash tools/search --query "pre-compensation FSO link margin optimization turbulence intensity" --max 15 --source s2,openalex
bash tools/search --query "自适应功率分配 星地激光通信 湍流 预补偿" --max 10 --source cnki
```

要回答：
- 功率自适应在GG湍流下的增益具体是多少dB？有没有论文给出量化结果？
- 符号率自适应（改变符号速率适应信道条件）在FSO中是否有人做过？效果如何？
- 是否有论文指出"慢变信道下自适应无增益"或类似的结论？
- 如果增益很小（<2dB），Ch3需要换方向

## 输出格式

每个问题：
```
### Q{n}: {问题}
- 结论：{一句话}
- 证据：{论文标题+年份+关键数据}
- 可信度：高/中/低
- 对选题的影响：{如果结论是负面的，Ch3/仿真需要怎么调整}
```

最后给出Ch3+仿真综合判断：
- Ch3预补偿方案：物理基础是否成立？
- 仿真系统：相位建模缺口有多大？需要额外多少工作量？
- 是否需要和导师确认Ch3技术路线？

## 约束

- 必须用 `tools/search` 检索，禁止 WebSearch
- 每条结论必须有论文引用，不靠推理
- 不写代码、不做仿真
- 中文输出
- 检索结果存档到 `search-archive/2026-05-29/`
