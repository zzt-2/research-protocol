# Decisions — 问题驱动方法论首次实战验证

> 本专题决策记录。D### 按编号排列，旧决策 superseded 不删。

## D001: Kill Xie et al. 独立性假设候选（验证为孤立建模改进）

> status: active
> date: 2026-06-21
> 取代：无
> 被取代：无
> 依据: 验证 `projects/thesis-fso/worker-tasks/verify-xie-independence.md`（全文 Grep 精确验证 + 636 行 content.md 读完）+ 调研 `projects/thesis-fso/worker-tasks/criticism-aggregation-en.md`（批评汇总层 3 时效检查）
> 触发原话: 无（技术推导，候选验证失败）

### 决策

Xie et al. "Revisiting the Independence Assumption in LEO Satellite-to-Ground Optical Links" (arXiv 2605.09892) 作为 Q# 候选种子被否决，不进入精读做假设审计。

### 核心失败机制

论文判为 (b) 孤立建模改进，不是 (a) 真裂缝：
- **全篇零 DSP 术语**（Grep 精确验证）——不触及估计/均衡/同步任何环节
- "design" 仅指 tip-tilt 角校正因子 η_tt（光机指向抑制参数），不是 DSP 设计准则
- 性能指标只测 outage（**无 BER/capacity**），与 5 次失败同构（信道建模 + 目标=outage 三轴锁死）
- 14 篇引用无 2024+ state-coupled 同类框架——"无人补"成立，但是**信道建模层的无人补，不是 DSP 层的无人补**

### 否决了什么

- 否决"Xie 独立性假设失效"作为 Q# 种子候选
- 否决"从信道建模改进反推 DSP 问题"的路径——建模改进不等于 DSP 假设失效
- 间接否决"凡是被批+无人补的洞就是 Q#"——必须是 DSP 链路相关、产出形态合法、有 baseline 的洞才是 Q#

### 可复用部分

- **baseline 信息可复用**：Ninos 2023 CL / Spirito 2025 JSAC / Helsdingen 2025 JOCN 都是 2019+ 顶刊复合衰落模型，可作为后续"信道建模"相关 baseline 引用
- **方法论教训可复用**：批评汇总的"无人补"信号需要区分"哪一层的无人补"——信道建模层的无人补对 DSP 链路 Q# 无价值。下次做时效检查时必须问"这个洞补不补对 DSP 有没有影响"
- **验证产出可复用**：`papers/arxiv/2605.09892/content.md`（全文已下载）可作为后续信道建模相关引用源

### 具体数据

- 性能偏差：ε=25° 处 BL-dom 2.85×10⁻² / FA-dom 3.30×10⁻² vs 独立假设 1.0×10⁻²（~3×）；ε=30° 处达 ~58×
- 14 篇引用里 2024+ state-coupled 同类工作 = 0 篇
- 全文 DSP 相关术语 Grep 命中 = 0（"channel estimation"/"equalization"/"synchronization"/"carrier recovery" 全 0 命中）

### 影响范围

- 本专题 Q# 候选池：从 2 个（Xie + "Are PLLs dead?"）减为 1 个（"Are PLLs dead?"）
- 精读对象选择：Xie 不进精读
- 方法论层面：批评汇总层 3 时效检查需补"哪一层无人补"维度（记入 S002 方法论迭代待办）

### 来源

S002 步骤 8.1 + 子 agent 验证报告 `verify-xie-independence.md`
