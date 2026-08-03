# Task Brief: 全项目历史方法内核盘点

> 来源: S018 | 产出位置: 回传主线程结构化摘要（主线程写 `internal-method-kernel-inventory.yaml`）
> 日期: 2026-08-03
> 唯一文档: 执行方只需本 brief 与 `projects/thesis-fso/`、`projects/simulation/`、相关 `.sessions/` 证据

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。
**你的任务**：从全部历史资产中找 deployable method kernel，不只看最终 METHOD_SIGNAL，并严格区分方法、工程组件、支持材料与 invalidated 结果。
**产出**：结构化核查摘要，回传主线程；不要修改任何文件。

**最高纪律**：

1. 每个数字、状态、claim ceiling 给真实文件指针；invalidated/unauthorized 结果绝不作正证据。
2. 方法必须有统一输入→动作→输出、传统 baseline 和可部署 action；参数值、测试、verifier、bugfix 本身不算方法。
3. CCISP 主方法保留；重点审 P01/P02/branch routing/P03/coded-prefix-LS/Q-A′/P05–P07-R/G1/P09。
4. 不跑代码、不跑实验、不使用 WebSearch、不修改仓库；单次不超过 15 分钟。

## 1. 必查内核

1. CCISP adaptive CPR：CV gate、fixed 13 dB effective-SNR gate、先选后执行 DA/NDA。
2. P01 receiver-visible SNR adapter：pilot-SNR estimation、selector 工作点校准、4/5 恢复。
3. P02 weak-region retuning：ref 9→11 dB、区域阈值、校准规则可能性。
4. branch-routed implementation：route A 双分支后选、route B 先判只跑一支、990/990 identity、成本证据。
5. P03 fixed-point selector：Q(8,6)、字长、uniform/mixed precision、resource proxy。
6. coded/prefix-LS receiver：prefix noise/channel estimation、coded metric、是否有新 action。
7. Q-A′：no-transmit/outage、risk-aware rate selection，unauthorized dev data 只作未来形态线索。
8. P05–P07-R、G1、P09：只收仍有效 kernel，invalidated 只说明不可行包装。

## 2. 产出格式（强制）

```markdown
## Evidence Map
| kernel | best evidence pointers | invalidated/unauthorized boundaries |

## Kernel Table
| kernel | M-C-A | deployable action | information source | baseline | existing evidence | missing evidence | method-like? | chapter-capable? | claim ceiling |

## Chapter-Capability Checklist
每个 kernel 给 8 项 true/false+证据：name/frame/steps/ablation/baseline/main figure/unified I-A-O/not parameter-or-bugfix。

## Candidate 2A–2D Preliminary Grade
每项从 THESIS_METHOD_READY / NEEDS_ONE_BOUNDED_PACKAGE / NEEDS_NEW_GW / SUPPORTING_ONLY / REJECT 选五选一并说明证据。

## Invalidated Claims Not To Revive
- claim + pointer + 可保留的失败教训。
```

## 3. 验收

- [ ] 8 类内核全部覆盖。
- [ ] 每个 method-like=yes 都同时有 action 与 baseline。
- [ ] 每个 chapter-capable=yes 都通过 8 项能力门。
- [ ] unauthorized/invalidated 没有变成正证据。
- [ ] 不修改文件。
