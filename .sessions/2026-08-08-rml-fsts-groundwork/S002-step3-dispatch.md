# [S002] RML-FSTS Groundwork Step 3 派发

> 2026-08-09 | Groundwork Step 3 | DISPATCH_READY

## 目标

在用户接受当前 5 篇合格 CORE 覆盖面后，完成范围变更并起草自包含 T001，只授权正式 GW Step 3 全文精读；到 Step 3 完成或阻塞状态停止。

## 记录

- 用户在 Step 2 覆盖面二选一确认关口回复“行”，接受当前 5 篇合格 CORE 作为 Step 3 输入边界并授权进入 Step 3。
- 该回复是有明确关口语境的有效范围确认，但原话本身属于零信息推进/应答；按 `session-governance` 的 `voice-quote.md` 不创建 `voice.md`。D003 的触发原话字段显式记录这一边界。
- D003 将专题当前范围从 Step 1–2 扩大到 **仅 Step 3**；Step 3.5、Step 4a、smoke、实现和仿真继续明确排除。
- T001 固定精读输入为 Wang 2023、Enhanced 2024、Morelli 2009、Paillier 2020、Yu 2023 五篇 CORE；要求 title preflight、标准 14+ 字段、7 个结构化子表、通信参数、五篇实验完备性、三篇写作架构、全局 read-notes/read-log、综合分析与 canonical Q#。
- Yu 2023 必须先闭合 `source.md` 到 canonical `content.md` 的字节一致路径适配与 title/DOI 证据；无法闭合则执行 title-abort，返回 Step 2，不得用口头例外凑足五篇。
- Step 3 四判据只允许使用 `stages/glossary.md` 的 canonical 四项；不得增加 `problem_truth`、`novelty`、`actionability` 或 `thesis_fit`。若无 Q# 全过，保持 Step 3 `BLOCKED/IN_PROGRESS` 并记录回 `gw-search` 的恢复路径，不自造 terminal、不进入 Step 3.5。

## 决策引用

- D003：用户确认当前 5 篇 CORE 后，将专题范围扩大到仅执行 Step 3，并在 Step 3 边界停止（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D003 与 topic-index 2026-08-09 范围变更记录）。

## 后续

在新对话完整读取并执行 `T001-rml-fsts-groundwork-step3-read.md`；本轮只完成派发准备，不执行论文精读。
