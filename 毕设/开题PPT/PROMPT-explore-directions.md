# PROMPT: 探索 Ch4 后续可扩展研究方向

## 背景

我的硕士开题课题是"星地激光通信信号处理关键技术研究"，以 Gamma-Gamma 湍流信道为统一模型，研究：

- **Ch2**：系统建模与信道分析（QPSK 相干检测，GG 湍流参数体系）
- **Ch3**：信道估计误差对接收性能的影响 → 面向同步的精度设计方法
- **Ch4**：湍流下载波同步方法分析 → 分湍流条件的方法选择与参数设计方法 + 探索方向（跨模块联合处理、编码辅助载波恢复等）
- **Ch5**：FPGA 实现与验证

开题答辩 PPT 有一页"创新点"（在 3.4 后面），我想在创新点右侧加一个轻量面板，列出"可扩展方向"——展示研究思路的纵深，但**不是硬承诺**。

## 任务

探索除当前已有方向外，还有哪些值得列出的研究方向。要求：

1. **从当前工作自然延伸**，不是完全换领域
2. **有文献支撑**（不是凭空想象）
3. **每个方向用一句话描述"做什么"和"为什么有价值"**
4. **区分层次**：紧邻延伸（现有成果直接展开）/ 中等距离（需新建模或方法）/ 远期（有前景但需要更多前提）

## 已有方向（不要重复）

以下方向已在报告或 PPT 中提到，不要重复：

- 定时同步、均衡（物理上影响有限，仅列作扩展）
- 编码辅助载波恢复（Turbo/FEC + CPR 迭代）
- 多源相位噪声联合建模（激光线宽 + 多普勒残余 + 湍流相位）
- 自适应调制（根据湍流条件切换 QPSK/16-QAM）— 用户新增考虑

## 执行方式

开多个子 agent 并行探索以下方向，每个子 agent 负责一个领域：

### Agent 1：链路自适应与资源分配

搜索：FSO 湍流下自适应调制编码（AMC）、功率自适应、链路自适应相关文献。
回答：
- 有哪些已发表的湍流下链路自适应方案？
- 从"分湍流条件的方法选择"延伸到"链路自适应"的gap在哪里？
- 这个方向和当前Ch4的"参数设计方法"如何递进？

### Agent 2：光学域+数字域联合补偿

搜索：AO (Adaptive Optics) + DSP co-design for FSO turbulence、光学预补偿+数字后处理联合方案。
回答：
- AO+DSP 联合方案的研究现状？
- 从"数字域载波同步参数设计"延伸到"光+数联合"的自然路径？
- 这个方向对开题阶段的硕士是否过于庞大？

### Agent 3：空间分集与多孔径接收

搜索：FSO spatial diversity、MIMO FSO、multi-aperture coherent receiver、selection combining / MRC in FSO turbulence。
回答：
- 多孔径接收在湍流下的信号处理有什么特殊挑战？
- 和当前"单孔径载波同步"的关系？（是否是自然的多通道扩展？）
- 代表性文献有哪些？

### Agent 4：深度学习在 FSO 信号处理中的应用

搜索：deep learning carrier phase recovery FSO、DL channel estimation turbulence、neural network equalizer optical communication。
回答：
- DL 在 FSO 湍流 CE/CPR 中的最新进展（2024-2026）？
- 当前课题不用 DL（泛化性未验证），但 DL 作为"可扩展方向"是否值得列入？
- 有哪些具体的 DL+物理模型融合的方案？

### Agent 5：湍流信道预测与前馈补偿

搜索：FSO turbulence prediction、channel reciprocity、proactive compensation、time-series prediction optical turbulence。
回答：
- 湍流信道的时间可预测性如何？（相干时间 2-10ms，是否足够做预测？）
- 前馈补偿（基于预测的预补偿）和当前"参数设计方法"的关联？
- 有文献做过湍流预测+信号处理联合吗？

### Agent 6：混合 RF/FSO 与链路可靠性

搜索：hybrid RF-FSO、FSO fallback、reliability analysis turbulence、soft switching RF optical。
回答：
- 混合 RF/FSO 切换的触发条件研究现状？
- 和当前"分湍流条件的参数设计"有没有自然延伸？
- 这个方向是否偏离"信号处理"太远？

## 输出格式

每个 agent 返回：

```
## [方向名称]

### 一句话描述
[做什么]

### 为什么有价值
[从当前工作如何自然延伸，解决什么新问题]

### 文献支撑
[2-3 篇代表性文献，含年份和简要贡献]

### 层次判断
[紧邻延伸 / 中等距离 / 远期]

### 放入 PPT 的建议文字（≤15 字）
[精简版]
```

最后，主 agent 汇总所有结果，按以下标准筛选适合放入 PPT 右侧面板的方向（最多 4-5 条）：
1. 和当前工作有清晰的递进关系
2. 有文献支撑（不是空想）
3. 开题答辩场景下不会被评委质疑"为什么不一起做"
4. 每条 ≤15 字

不适合的说明原因。

## 关键文件

- 开题报告：`毕设/开题报告/kaiti-report.md`（了解当前研究内容细节）
- PPT 内容定稿：`毕设/开题PPT/ppt-content-decisions.md`（了解 PPT 结构和措辞规范）
- 创新点定义：`毕设/innovation-points.md`
- PPT 生成技能：`.omc/skills/ppt-generation.md`
- Python 环境：`~/.venvs/torch/bin/python`
