# Task Brief: coherent FSO 共同平台参数 authority 提取

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 3
  action_class: GROUNDWORK_READ
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只读 T042 的 6 篇 qualified full texts，为共同 DP-(8,8)-16APSK+BICM/LDPC coherent FSO testbed 提取可引用、可实现的参数与边界表。重点读取：Paillier 2020、Bernini 2022、Vieira 2023、Faruk 2013、Roudas 2009、Kuschnerov 2009。输出不是方法 Q#，而是平台 authority：

- 单 tap 2×2 Jones/unitary/PDL 模型的公式、成立条件和与 PMD/FIR 的边界。
- 星地 Doppler/CFO、laser linewidth/phase noise、receiver filter 与 I/Q gain/phase/timing skew 的来源、量级、章节/公式定位。
- 每项分为 `SUPPORTED_ACTIVE`、`SUPPORTED_FIXED`、`CONDITIONAL`、`EXCLUDED`、`UNKNOWN`；说明 Ch3/Ch4/Ch5 谁承重、谁只固定。
- 给出一个“最小共同 smoke 配置”参数表和一个“后续开发矩阵可扫描维度”表；数值缺 authority 时写 UNKNOWN，不凭感觉填值。
- 明确 atmospheric polarization 全文缺口不进入主动 testbed/claim；光纤 PMD 不迁移到星地 FSO。

## 边界

- 不形成方法 Q#，不检索/下载，不做 Step 3.5/4a，不实现、不实验。
- 不改仿真/Skill/controller/论文正文；不把多个损伤叠加来人为制造 headroom。
- 只提交指定 parameter-authority 文件；如需引用 read note，只复用现有正文路径，不批量生成 gw-read 笔记。

## 验收

- 每个数值和模型假设都有 `paper path + section/equation/table/figure` 指针；无指针即 UNKNOWN。
- 输出冻结 memoryless 2×2 默认、finite FIR 条件分支、主动/固定/排除损伤，以及 Ch4→Ch5 接口字段。
- 最终回报 commit、可冻结参数数、UNKNOWN 数和唯一会阻塞 correctness smoke 的参数缺口。
