# Task Brief: Ch4 production-evidence 设计与正确性预检

> 来源: S028 / D060 / V035 / T080 | 产出位置: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/production-evidence-{design,plan}.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 22
  action_class: CH4_PRODUCTION_EVIDENCE_DESIGN_AND_PREFLIGHT
  mission_checkpoint: CP022
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

把 Ch4 从旧四格 confirmation 扩展为完整方法章所需的 production-evidence 设计和可执行计划，并完成只读 seam 审计。当前只允许读代码、构造确定性反例、写设计/计划/治理文档和做独立预审；不得运行仿真网格或产生新 BER 数字。

## 北极星

最终 Ch4 必须形成完整闭环：目标星地双偏振接收问题 → receiver-visible scaled-unitary 动作 → 公平 baseline/cheap comparator → 全 BER–SNR 工作区 → 导频效率 → NMSE/residual 机制 → turbulence/structure-mismatch 边界 → 复杂度 → Ch3 CPR 接口。

不得退化为“再补几个 SNR 点”，也不得为了图好看改变物理定义或遗漏已知廉价替代。

## 开始前强制读取

1. active topic-index CP022、D060/V035、S028 最新批次、master-state 当前 authority；
2. 既有 Ch4 `fact-matrix.md`、`chapter-blueprint.md`、`claim-and-citation-ledger.md`、独立审查和 T068–T073 证据链；
3. Ch4 simulator 的 `development.py`、`scaled_unitary.py`、confirmation runner/reducer/manifest/tests；
4. 公共 16APSK modulation 实现及其调用链；
5. 已接受 Ch3 camera-ready 配置、SNR 语义、Gamma–Gamma 参数和图形风格。

## 必答预检问题

1. 旧 BER 差异是否依赖一个不符合全局欧氏最近邻合同的 demapper？给出可复现的单点反例或 PASS 证明。
2. 旧 seed/RNG 是否允许 SNR/Np 曲线做严格 paired 解释？若不允许，冻结新 substream/latent 设计。
3. B2 与 C4 的动作差异是什么？同信息预算的最强廉价标量替代如何定义并进入主对照？
4. 哪些 axes 进入正式 production，哪些只做紧凑 slice，避免无意义全笛卡尔积？
5. Ch3 与 Ch4 哪些配置必须统一，哪些只能做清楚的章间接口而不能假装已联合验证？
6. 哪个结果足以继续、哪个结果强制停止，而不是用新损伤或调参救图？

## 交付与验证

- 主设计：`production-evidence-design.md`；
- 逐任务计划：`production-evidence-plan.md`；
- 独立 reviewer 必须核对科学门、可执行性、TDD 顺序、历史资产保护、scope 和 stop rules；
- 运行 task-control validator、路径/占位符检查、`git diff --check`；
- terminal 仅允许：
  - `CH4_PRODUCTION_PREFLIGHT_READY`；
  - `CH4_PRODUCTION_PREFLIGHT_NEEDS_REPAIR`；
  - `CH4_PRODUCTION_BLOCKED`。

本任务通过只表示可以另开 demapper correctness repair；不授权仿真、production 或论文正文写作。
