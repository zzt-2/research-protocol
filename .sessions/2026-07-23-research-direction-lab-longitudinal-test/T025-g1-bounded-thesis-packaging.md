# Task Brief: G1 有边界毕业方法包装

> 来源: S002 / live D032 / formal D041 / V060
> 产出位置: `projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md`
> 日期: 2026-07-29
> 唯一文档: 执行方只拿到本 T；可读取本文列出的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 56
  action_class: THESIS_METHOD_PACKAGING
  mission_checkpoint: CP023
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

G1 是一个 receiver-visible、prefix-only 的门控幅度归一化组件：固定步长 CMA
输出正常时保持恒等；检测到塌缩风险时，按双偏振各自的稳健功率估计施加正确的
平方根幅度缩放。它在当前局部测试切片上显示了强塌缩恢复和零健康样本最坏退化，
但 Groundwork 证据闭包与直接竞品实现不合格，因此不是 formal Go。

**你的任务只做写作包装**：把既有算法动作、可信局部数字、适用边界、图表方案和
证据债整理成一个可供主控/论文后续选用的方法包。不得补实验、补检索、补全文、
修 T024、改科学代码或晋级正式主线。

最终只新增：

1. `projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md`
2. `projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md`

除上述两文件外不得修改任何文件；不得 push。

## 1. 启动与证据源

依次读取：

1. `AGENTS.md`
2. `.agents/skills/research-direction-lab/SKILL.md`
3. `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
4. `.agents/skills/research-direction-lab/references/thesis-harvest.md`
5. `thesis-lessons.md` 速查表、TL-20、TL-22、TL-23、TL-30–TL-33
6. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
7. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md`
   的 V060
8. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md`
   的 D032
9. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/src/methods.py`
10. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/artifacts/result.json`
11. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/artifacts/raw-rows.csv`
12. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/artifacts/prefix-receipt.csv`
13. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/artifacts/synthesis.md`
14. `projects/thesis-fso/worker-logs/step-024-g1-safe-gated-normalization.md`

启动：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T025-g1-bounded-thesis-packaging.md
git status --short
```

validator 非 PASS 或起点不 clean，立即返回
`BLOCKED_CONTROL_OR_DIRTY_START`，不得写文件。

## 2. 冻结事实

### 2.1 算法定义

必须直接按 `methods.py` 核对并用规范符号重写：

- 输入是 tuned fixed-μ CMA 后的双偏振复数流；
- 只读取 128 symbols calibration prefix，scored suffix 与 prefix 不重叠；
- 门控时先拼接双偏振前缀
  \(z_{\rm prefix}=[z_{x,\rm prefix};z_{y,\rm prefix}]\)，再统一计算共享特征：
  - \(m_2=\operatorname{mean}(|z_{\rm prefix}|^2)\)；
  - \(c_v=\operatorname{std}(|z_{\rm prefix}|)/
    (\operatorname{mean}(|z_{\rm prefix}|)+10^{-9})\)；
- 当 \(m_2\ge 0.6\) 且 \(c_v\ge 0.1\) 时保持恒等；其余情况启用缩放；
- 对每个偏振 \(p\in\{x,y\}\)，以 10% trimmed mean 估计
  \(\widehat P_p=\operatorname{trimmean}(|z_{{\rm prefix},p}|^2)\)；
- 归一化 16QAM 目标功率为 1，故
  \(a_p=\sqrt{1/\widehat P_p}\)，并对 suffix 使用
  \(z'_p=a_p z_p\)；
- 无 TX truth、oracle、future suffix 或 suffix feedback 作为在线输入；
- 复杂度表述限于 prefix 上的幅值、均值/标准差、排序型 trimmed mean 和
  suffix 上逐样本复数标量乘法；不得无依据给出精确 FLOP 或硬件时延。

### 2.2 可使用的局部证据

以下数字以 V060 独立复核为准：

| 项目 | 可用数字 | 正确表述 |
|---|---:|---|
| 门控 eligible pairs | 49 | 当前任务定义的 local slice |
| 混淆矩阵 | TP/FP/FN/TN = 19/1/1/28 | receiver-visible gate 对离线类别的诊断 |
| point balanced accuracy | 0.957759 | 诊断统计，不是领域泛化精度 |
| seed-cluster pooled bootstrap 95% CI | 约 [0.885, 1.000] | 正确聚类单位下 Gate6 PASS |
| G1−tuned CMA，collapse stratum | −0.559796 PI-SER | CI 约 [−0.6947, −0.4064]；help/hurt=12/0 |
| healthy worst pair degradation | 0 | 当前 local slice |
| healthy cluster mean | −0.0028409 | 若报告 CI，必须从 artifact 核对后再写 |
| false activation | 1/29 | 该次 false activation 未造成退化 |
| G1−M4，collapse stratum | −0.035457 PI-SER | CI 约 [−0.0466, −0.0243]；只作 lineage ablation |

“collapse stratum”是条件子集，不得偷换成全样本平均收益。M4 是派生非线性
策略消融，不是合法 recent direct competitor。

### 2.3 必须公开的证据上限

- T024 `result.json` 中把 Gate6 报成 CI `[0.50, 0.6579]` 是错误统计实现；
  正确 seed-cluster pooled bootstrap 约为 `[0.885, 1.000]`。
- Phase-A 的 G1 search/citation/read-note 没有形成可提交闭包，不能声称四判据、
  novelty 或 collision 已正式关闭。
- 所谓 D4 comparator 的 apply 是 post-CMA 恒等映射，不能声称已赢直接竞品。
- 当前结论是
  `G1_GROUNDWORK_EVIDENCE_INCOMPLETE / PHASE_B_NONBINDING_DIAGNOSTIC`。

## 3. 唯一产物：方法包装文档

创建
`projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md`，
至少包含以下结构。

### 3.1 总判断

先用普通中文给出三档判断：

1. **强独立主方法**：当前不可这样包，原因是 novelty/collision 与直接竞品
   闭合不足；
2. **推荐包装**：低复杂度、塌缩感知的接收机安全归一化层，可作为毕业论文
   的小方法、主方法安全组件或正向补充实验；
3. **保守包装**：作为“何时应启动幅度校正”的运行边界与评估洞察。

明确推荐第 2 档，并说明它比单纯负面分析更接近可写方法，但证据强度仍是
`LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。

### 3.2 方法定义

用对外写作语言写清：

- 问题：盲均衡输出可能发生幅度/星座塌缩；always-on 归一化会伤害本已正常的
  输出；
- 核心思想：先用接收端前缀判别是否需要干预，再只在风险状态执行物理正确的
  平方根幅度恢复；
- 输入、输出、因果边界；
- 公式；
- 8–15 行伪代码；
- 复杂度和实现位置；
- 与“始终归一化”和“非线性半径重映射”的机制区别。

正文不得使用 G1、T024、V060、D032、Gate6 等内部控制代号。它们只允许出现在
文末 provenance appendix。

### 3.3 论文叙事

给出：

- 3 个规范中文方法名/小节标题；
- 1 段“问题—机制—收益—边界”中文摘要；
- 3 条候选贡献，每条均注明当前可写强度；
- 2 句可直接放入英文摘要/贡献列表的克制英文；
- 推荐放置位置：
  1. 独立小方法；
  2. 更大接收机方法中的 safety component；
  3. 负面路线后的 positive salvage。

不得写“首次”“显著优于现有方法”“state of the art”“普遍适用”“已验证可部署”
或“解决了盲均衡问题”。

### 3.4 证据矩阵与图表计划

做 claim–evidence–scope–debt 四列表；每个数字都附仓库路径。

规划但不生成图片：

- 方法流程图：CMA 输出 → prefix features → identity/scale gate →
  per-pol sqrt scaling → suffix；
- 一张 collapse/healthy 分层结果表；
- 一张风险—收益图或 confusion + degradation 组合图；
- 每张图写清横纵轴、统计单位、caption 要披露的 local-slice 限制。

### 3.5 不可声称项与补强清单

单列“目前不能写进论文的说法”。随后给出未来若要升级成正式主方法所需的最小
证据，限于：

1. 重新闭合 direct-collision / cheap-alternative 文献链；
2. 实现真实直接竞品而非恒等占位；
3. 在预注册、多信道/多长度/多调制切片上复核 gate 与健康保护；
4. 报告整体分布、失败案例、参数敏感性与计算代价。

这里只列债，不执行。

### 3.6 Provenance appendix

内部附录必须列出：

- V060、D032、formal D041；
- `methods.py`、`raw-rows.csv`、`prefix-receipt.csv`、`result.json`；
- 错误 Gate6 字段为何禁用；
- D4 为何禁作竞品证据；
- 每条外部正文数字对应的精确来源。

## 4. Worker log 与独立审查

创建
`projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md`，
记录：

- 启动门与 clean 起点；
- 实际读取的证据；
- package 文件路径；
- 使用/拒绝的全部数字；
- 主张边界检查；
- changed files；
- 独立 reviewer 的结论和 P0/P1/P2。

必须委托一个独立 reviewer 只读审查 package：

1. 算法公式是否与 `methods.py` 一致；
2. 数字是否与 V060/raw 一致；
3. 是否把 conditional result 写成 overall result；
4. 是否暗示 formal Go、novelty closure 或 direct-competitor victory；
5. 对外正文是否去掉内部治理语言；
6. 是否只新增两个授权文件。

P0/P1 必须为 0；否则修改后复审。

## 5. 验证、提交与回执

至少运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T025-g1-bounded-thesis-packaging.md
git diff --check
git status --short
```

确认只新增两个授权文件。每个对话只做一个 consolidated commit，commit message
概括 G1 bounded thesis packaging；不 push。

允许的终态：

- `PACKAGING_BOUNDARY_READY_FOR_MASTER_REVIEW`
- `PACKAGING_BLOCKED_EVIDENCE_CONFLICT`
- `BLOCKED_CONTROL_OR_DIRTY_START`

成功时：

```text
status: PACKAGING_BOUNDARY_READY_FOR_MASTER_REVIEW
mission_method_delta: PACKAGING_BOUNDARY
commit: <sha>
worker_log: projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md
package: projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md
one_line_result: <一句普通中文，说明包装强度、核心局部信号和正式证据边界>
```

其余终态 `mission_method_delta: NONE`。不要返回长篇过程，不要 push。
