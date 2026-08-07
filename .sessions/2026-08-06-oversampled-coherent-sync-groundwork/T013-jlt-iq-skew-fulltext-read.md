# Task Brief: JLT 2025 IQ-skew 用户提供全文 acquire→read

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-jlt-iq-skew-fulltext-read.md`
> 日期: 2026-08-06
> 唯一文档: 执行方只需本任务文件与指定 canonical PDF/content/metadata

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 27
  action_class: USER_FULLTEXT_PROVISION
  mission_checkpoint: CP014
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

用户已提供此前缺失的 JLT 2025 IQ-skew 全文，canonical 文件位于：

- `papers/doi/10.1109_jlt.2025.3581618/source.pdf`
- `papers/doi/10.1109_jlt.2025.3581618/content.md`
- `papers/doi/10.1109_jlt.2025.3581618/metadata.json`

论文标题：**Preamble Design for Online IQ-Skew Estimation in Upstream 400G Coherent TFDM-PON**。

你的任务：全文精读，裁决它是否与 Q1 的 exact joint `(frame, fractional τ, CFO)` information/action/output
contract 碰撞，并提取可复用的完整 read note。

最高纪律：

1. 必须读 `content.md` 全文；不得只凭摘要、题名或本任务背景裁决。
2. 区分“同一 preamble 复用多个顺序 DSP 模块”与“单一 estimator/objective 联合输出三个参数”。
3. 不把 IQ-skew estimation、SOP、channel estimation 或 shared overhead 自动算作 Q1 exact action。
4. 不修改 canonical topic/decisions/literature notes；不进入 Step 4a、实现或仿真；不提交。

## 1. 背景

Q1 当前 canonical M/C/A：

- M：Le Bidan 2-sps 顺序 acquisition chain + Sun/Wang frame–FOE；
- C：RRC、≥2 sps coherent FSO，fractional timing、frame、CFO 同时未知；
- A：顺序 timing-first 处理在同时未知状态下可能传播误差或产生错误峰/误锁。

Q1 四判据已 PASS，是唯一 Step 3 survivor。Step 3.5 已收敛，但此前 JOCN 2026 与本篇 JLT 2025
全文缺失，禁止 exact-action novelty closure。本任务只关闭本篇的全文语义不确定性；JOCN 仍缺。

## 2. 任务详情

### 2.1 源文件身份门

- 核对 metadata、正文题名、DOI `10.1109/JLT.2025.3581618`、作者与出版信息；
- 报告 title overlap、source/content SHA256、行数；若 title mismatch 立即 ABORT。

### 2.2 标准全文条目（必须）

提取并写入 `papers/_read_notes/10.1109_jlt.2025.3581618.md`：DOI/来源、源文件路径、发表状态、
发表渠道/年份、核心贡献（≥2句）、方法概述、实验设置、baseline、关键结论、与 Q1 关系、实现关键
细节（带数值）、开源代码、验证状态。

### 2.3 结构化提取七子表（必须）

逐项给出：状态/输入信息空间、动作/输出空间、目标或估计公式、建模假设、算法/DSP 架构、适配性分析、
问题提取 M/C/A + canonical 四判据。非 ML 论文对 reward/network 字段明确写 N/A，不得省略。

### 2.4 实验完备性（必须，≤20行）

提取 claim+scope、重复次数/误差条、baseline matrix、消融、信道/系统模型、拓扑/场景多样性、复杂度、
VVUQ。保留具体数字、图表/公式/章节定位。

### 2.5 Exact-action collision 裁决（核心）

用表格逐字段回答：

| 字段 | 本文事实 | Q1 contract | 匹配？ | 正文证据位置 |
|---|---|---|---|---|
| receiver-visible input | | | | |
| preamble structure/resource | | | | |
| frame output | | | | |
| fractional timing output | | | | |
| CFO output | | | | |
| IQ-skew/SOP/channel output | | | | |
| objective/estimator coupling | | | | |
| execution order/timing | | | | |
| operating condition/modality | | | | |

最终 verdict 只能选：

- `CONFIRMED_EXACT_Q1_COLLISION`
- `NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`
- `PARTIAL_COLLISION_AMBIGUOUS`

必须说明该文是否只是 resource reuse、是否存在单一三参数 objective、timing recovery 与 frame/FOE 的
先后关系，以及它对最强 cheap comparator 的影响。

## 3. 已知陷阱

- 摘要中的 “simultaneously enables” 不等于 estimator 在数学上联合输出；必须沿 Fig. 2 与方法正文追踪。
- 共享 TS-A/TS-B、零额外开销与 action jointness 是三个不同命题。
- 本文 TFDM-PON/光纤 upstream 与 coherent FSO 的 modality 差异不能单独排除方法碰撞；应先裁动作，再裁 task fit。
- 不得因为本文还估计 IQ skew 就忽略其 frame/timing/CFO 子动作；也不得因模块共用 preamble 就宣称 exact collision。

## 4. 验收

- [ ] 身份、SHA、行数与全文标题一致；
- [ ] 标准条目与七子表字段完整；
- [ ] 实验完备性含具体数值和正文定位；
- [ ] collision 表逐字段闭合，verdict 来自正文而非摘要；
- [ ] worker log 与 read note 两份产物存在；
- [ ] 未修改 canonical、未提交。
