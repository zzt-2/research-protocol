# 对话提示词：Ch4选题验证检索

> 产出文件: 结论更新到 `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
> 优先级: 高
> 依赖: S002、S005、literature_notes.md Ch4部分
> 预计耗时: 30-40分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"Ch4载波同步选题讨论。

当前默认方案："湍流×CPR算法(VV/BPS/Pilot)系统性鲁棒性分析"——纯对比，创新偏弱。

提议升级为方案A：自适应CPR切换策略。但**未经任何正规检索验证**。

本对话唯一任务：用 `tools/search` 检索回答以下3个问题，每条结论附论文引用。

## 前置条件

读取以下文件恢复上下文：
1. `.sessions/thesis-direction-pivot/S005-overall-feasibility-review.md`
2. `projects/thesis-fso/literature_notes.md` — Ch4部分（第131-177行）

## 必须回答的问题

### Q1：自适应CPR/VV-BPS切换是否已有人做过？

检索策略：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "adaptive carrier phase recovery switching Viterbi BPS QPSK optical" --max 20 --source s2,openalex
bash tools/search --query "turbulence aware carrier phase recovery free space optical" --max 20 --source s2,openalex
bash tools/search --query "adaptive modulation carrier recovery FSO atmospheric turbulence" --max 15 --source s2,openalex
```

要回答：
- 光纤通信中是否有人做过VV/BPS/Pilot之间的自适应切换？
- FSO场景下是否有人做过湍流感知的CPR？
- 如果已有人做：我们的方案和他有什么区别？还是创新性归零？

### Q2：不同湍流强度下VV/BPS/Pilot性能差异有多大？

从literature_notes Ch4必读论文中交叉验证：
- Yang 2025 (#1): VV vs BPS对比结论和具体数字
- Zhang & Shu 2021 (#19): 窗口/线宽/复杂度系统对比
- Zhang 2023 (#21): VV/NVV/BPS实验对比

补充检索：
```bash
bash tools/search --query "Viterbi Viterbi BPS pilot carrier phase recovery comparison turbulence optical" --max 15 --source s2,openalex
bash tools/search --query "carrier phase recovery algorithm performance scintillation atmospheric turbulence" --max 15 --source s2,openalex
```

要回答：
- 三种算法在不同湍流/不同SNR下的BER差异具体是多少dB？
- 如果弱/中湍流下差异<1dB，切换策略没有实际价值
- 哪种算法在什么条件下明显优于其他？

### Q3：湍流强度作为CPR切换判据物理上是否合理？

关键物理问题：GG湍流主要产生幅度闪烁(scintillation)，相位起伏是波前畸变的二阶效应。
CPR算法性能主要受SNR波动影响还是相位噪声影响？

检索：
```bash
bash tools/search --query "atmospheric turbulence phase fluctuation coherent optical communication" --max 15 --source s2,openalex
bash tools/search --query "wavefront distortion phase screen FSO coherent detection carrier" --max 15 --source s2,openalex
```

要回答：
- 星地FSO中湍流引起的相位起伏量级是多少？
- 这个量级是否足以区分VV/BPS/Pilot的性能？
- 切换判据应该是湍流强度、SNR、还是其他？

## 输出格式

每个问题：
```
### Q{n}: {问题}
- 结论：{一句话}
- 证据：{论文标题+年份+关键数据}
- 可信度：高/中/低（基于几篇论文、是否矛盾）
```

最后给出 Ch4选题综合判断：
- 方案A（自适应CPR）：Go / No-Go / 有条件Go
- 如果No-Go或条件Go：推荐替代方向

## 约束

- 必须用 `tools/search` 检索，禁止 WebSearch
- 每条结论必须有论文引用，不靠推理
- 不写代码、不做仿真
- 中文输出
- 检索结果存档到 `search-archive/2026-05-29/`
