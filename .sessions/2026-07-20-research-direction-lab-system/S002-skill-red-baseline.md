# [S002] Research Direction Lab Skill RED 基线

> 2026-07-20 | Skill 实施前压力测试 | 完成

## 目标

在不存在新 `research-direction-lab` Skill 的条件下，用盲测压力场景观察模型是否会复现历史上的四类偏差：围绕单一 blocker 继续补丁、把局部负面外推为方法族失败、把修复错误 baseline 的漂亮数字当作论文正信号、把研究时间耗在通用控制器上。

## 记录

四名 fresh agent 只收到各自场景，没有读取本专题蓝图或未来 Skill。完整原始回答保存在 `.superpowers/sdd/red-scenario-a.md` 至 `red-scenario-d.md`；以下保留与判定直接相关的原句。

| 场景 | 观察到的下一动作 | scope / harvest 行为 | RED 结果 |
|---|---|---|---|
| A：一个 action candidate 缺真实状态/动作可观测性，另有两个 ready 候选 | “今晚立即停止继续补 A……主线切换到 B；B 完成后，只要尚有时间且 C 的 preflight 通过，就继续做 C” | 明确把 A 标成工程阻断而非科学失败，并要求记录合同、结果、时间账和组合裁定 | 未复现目标失败 |
| B：QPSK、CSI_NONE、hard-decision 的 11-cell 局部负面，三个关键轴受基础设施阻断 | “关闭已测试的……分支……但不作候选级科学否证，更不关闭 residual-aware 方法族” | 区分 cell、已测子域、候选和方法族；提出边界结果、热图、证据范围立方体和负面表 | 未复现目标失败 |
| C：pilot-Jones 对错误 current-CMA 得到 15/15 正信号，合法 standard-CMA 已接近 oracle | “立即停止 Pilot-Jones 的科学扩展……撤销其基于 current-CMA 的族级 promotion” | 把结果降为 diagnostic-only，保留 runner、指标、负面结果和 baseline 合法性教训 | 未复现目标失败 |
| D：控制器有两个 bug 和 37 个旧失败，同时存在 runnable、small-adapter、provenance-blocked 与概念候选 | “我不会把这 4 小时投入通用 campaign controller 的修复” | 优先运行 C1、并行闭合 B1、保留 A1 provenance 缺口和两族候选卡，最后形成证据化 handoff | 未复现目标失败 |

本轮没有得到一个可诚实称为 RED 的行为失败。按 `writing-skills` 的要求，不能为了证明新 Skill 必要而继续放宽场景或把合格回答判成失败，也不能把上述模型已经稳定具备的科学判断重写成大量硬规则。

因此，Task 2 的 GREEN 范围收窄为：提供稳定触发入口、恢复顺序、单一长期循环、文件归位、证据/claim 边界、harvest 与一页状态的路由；具体候选排序、换路和科学解释保留为 AI 判断。历史案例只作为回归材料，不复制成逐案 if/then 规则。

## 决策引用

- D001：继续采用 `Skill-first, code-guarded`；本次基线进一步证明 Skill 应主要补跨上下文组织与恢复，而不是把正常科学判断编码成 scheduler。

## 范围确认

- 本轮是否在 scope boundary 内：是。
- 未创建正式 Skill，未修改控制器、campaign core、仿真器、baseline、历史 scientific artifact 或运行授权。

## 后续

先完成 U01–U15 的独立溯源审查整改；随后用官方 initializer 建立精简 Skill，只为尚未被基线证明冗余的职责编写指导，并用结构测试和跨域隔离测试验证。
