# 对话提示词：Ch4 方向侦察 — 多候选方向快速文献摸底

> 产出文件: `.sessions/thesis-direction-pivot/S009-ch4-direction-scout.md`
> 优先级: 高
> 依赖: S008(A0检查v5), S007(Ch4+Ch5精读)
> 预计耗时: 30-40分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。四章结构：Ch2(GG信道建模+DL信道估计) → Ch3(功率自适应预补偿) → Ch4(载波同步) → Ch5(FPGA验证)。

**Ch4 当前状态**：A0 检查未通过——核心假设（湍流下自适应FOE参数 > 固定参数）零实证数据。创新空间（零文献做过湍流对FOE的影响）经精读确认真实，但创新空间 ≠ 性能改善空间。仿真可能发现增益 <5%。

**问题**：Ch4 是否应该换方向？当前 FOE+CPR 自适应参数方向可能太窄，需要探索其他同步方向。

## 前置条件

读取以下文件恢复上下文：

1. `.sessions/thesis-direction-pivot/S008-a0-and-gap-analysis.md` — A0 检查结果（重点关注 Ch4 部分）
2. `.sessions/thesis-direction-pivot/S007-ch4-ch5-deep-review.md` — Ch4/Ch5 精读结果

## 用户背景

用户做过以下同步相关工作：
- 载波同步（当前 Ch4 方向）
- 位同步
- 帧同步（用户自评"没啥好写的"）
- CMA（用户自评"也没啥好写的"）

## 候选方向

对以下每个方向做快速文献摸底（不精读，判断空白和证据强度）：

### 方向 A：LEO Doppler + 载波同步联合

- **核心问题**：LEO Doppler 偏移 ~±10 GHz，变化率 ~MHz/s，与 GG 湍流联合影响载波恢复
- **独特性**：Doppler 是 LEO 星地链路独有挑战（地面 FSO 和星间 FSO 都没有这么大的 Doppler）
- **搜索关键词**：
  - "LEO satellite free space optical Doppler carrier recovery"
  - "LEO FSO frequency offset estimation"
  - "satellite optical communication Doppler compensation"
  - "low earth orbit laser communication carrier synchronization"
  - "星地激光通信 多普勒 载波同步"
- **判断标准**：是否有 ≥2 篇做过 LEO FSO Doppler 补偿？如果有，他们的方法是否考虑了湍流？

### 方向 B：当前方向（FOE+CPR 自适应参数，保留）

- 已有 S007 精读结果，重点补充搜索：
  - "turbulence carrier recovery QPSK" 
  - "atmospheric turbulence frequency offset estimation"
  - "adaptive FFT window length carrier recovery"
- **判断标准**：是否有任何论文做过湍流下的 FOE 参数优化？

### 方向 C：位同步 / Symbol Timing Recovery

- **核心问题**：湍流导致幅度闪烁 → Gardner/Early-Late 定时恢复性能退化
- **搜索关键词**：
  - "symbol timing recovery free space optical turbulence"
  - "clock recovery fading channel optical"
  - "timing synchronization atmospheric turbulence"
- **判断标准**：是否有论文研究过湍流对定时恢复的影响？增量空间多大？

### 方向 D：联合同步（Doppler + 载波 + 位同步统一框架）

- **核心问题**：将多个同步任务统一在一个框架中
- **搜索关键词**：
  - "joint synchronization LEO optical communication"
  - "unified carrier timing recovery satellite FSO"
- **判断标准**：是否有人做过？复杂度是否可控？

## 每个方向的评估维度

对每个方向，回答以下问题（基于搜索结果，不要求精读）：

1. **文献空白度**：零文献 / 少量(<5篇) / 充足(≥5篇) / 拥挤
2. **问题显著性**：物理上是否是硬约束？（Doppler 是硬约束，参数微调可能不是）
3. **与 Ch2/Ch3 衔接度**：是否共享 GG 湍流模型和 SP-QPSK 假设？
4. **仿真可行性**：能否在 1-2 个月内完成有意义的仿真？
5. **创新点强度**：可能的创新点是什么？是性能创新还是方法论创新？
6. **致命风险**：是否存在"做了才发现增益 <5%"的风险？

## 输出格式

```markdown
# [S009] Ch4 方向侦察

## 方向评估总览

| 方向 | 文献空白度 | 问题显著性 | Ch2/3衔接 | 仿真可行性 | 创新点强度 | 致命风险 | 推荐 |
|------|----------|----------|----------|----------|----------|---------|------|
| A Doppler+载波 | ... | ... | ... | ... | ... | ... | ★/☆ |
| B FOE+CPR自适应 | ... | ... | ... | ... | ... | ... | ... |
| C 位同步 | ... | ... | ... | ... | ... | ... | ... |
| D 联合同步 | ... | ... | ... | ... | ... | ... | ... |

## 方向 A 详情
### 搜索结果
### 文献空白分析
### 创新点
### 风险
### 结论

（B/C/D 同理）

## 推荐
### 首选方向及理由
### 备选方向
### 需要导师确认的决策点
```

## 约束

- 每个方向搜索 3-5 组关键词，每组读前 5 条结果摘要即可
- 不下载全文、不精读，仅从标题/摘要判断
- 如果某个方向搜索结果 <3 条 → 标记为"文献极少"，可能是空白也可能是无人关注（需区分）
- 中文输出
- 30 分钟内完成
- 搜索工具：用 `tools/search` 脚本，不用 WebSearch（主对话禁止 WebSearch）
- 如果需要 WebSearch，必须在子 agent 中执行
