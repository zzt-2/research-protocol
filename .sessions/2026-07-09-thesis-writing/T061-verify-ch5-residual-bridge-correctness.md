# Task Brief: 独立验证 Ch5 receiver-residual bridge correctness

> 来源: S028 / D046 / T055 / T057 / T060 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-bridge-correctness-verification.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 8
  action_class: INDEPENDENT_SCIENTIFIC_VERIFICATION
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 T060 已集成的 Ch5 receiver-visible residual bridge 做独立科学验证。只审 correctness；不得修改实现，不得运行 natural occurrence、性能比较、调参或新损伤，不得挑选 Ch4 最优 arm。

## 必读与启动门

1. 先运行 task-control validator；读取本 brief、D046、T055、T057、T060。
2. 读取 `post_ch4_ch3_bridge.py`、`run_occurrence_smoke.py`、`occurrence_contract.yaml`、对应 tests，以及所调用的 Ch4 core、`common/_channel.py`、`common/_recovery.py`。
3. 本任务触发 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`verification-before-completion`。只读审查，不写使用日志以外的实现文件；验证报告是唯一允许新增的研究产物。

## 必须独立回答

1. 数据依赖是否真实为 `shared scalar GG/CFO/Wiener -> unitary Jones -> AWGN -> Ch4 -> per-pol Ch3 DA CPR -> pilot-only 8-fold resolve -> residual`，而非只在文字或 mock call-order 中成立。
2. Ch4 acquisition pilots 与 observation samples 的 scalar/Jones/noise 语义是否足以支持上述链；特别审查 fixture 中 `ch4_pilot_rx` 是否绕过 shared scalar，这会不会使 correctness 或未来 occurrence 失真。若只是 occurrence 生成器待补条件，明确降为条件性 PASS；若破坏本 bridge correctness，判 FAIL。
3. `da_ml_recovery` 的输入、pilot index、符号、phase/frequency 输出与 16APSK mode 是否调用正确且逐偏振独立。
4. 8 个旋转的索引、补偿符号和唯一性测试是否无正负号/索引错误。
5. payload truth mutation、future-window mutation、receiver-visible mutation、polarization swap 是否真正覆盖 firewall/因果/等变性，而非只比较未受影响字段。
6. deployable bundle、realization hash、bundle hash 是否包含所有 receiver-visible 承重字段并排除 offline truth；改变 frozen-arm 数值参数但保留 arm_id 时，hash 是否仍能区分配置。若不能，判 correctness blocker。
7. covariance identity 仅能证明 B1/B2/B3/C1 可消费 bundle，不得解释为 occurrence 或 method signal。

## Fresh 验证

- 运行 T060 task-control validator。
- fresh 跑原 Ch5 correctness tests + bridge tests。
- 只运行 `run_occurrence_smoke.py --mode correctness`；证明 argparse 不存在 occurrence 路径。
- 必要时允许写一次性只读 Python probe，不得落新实现文件。
- `git diff --check`，并确认工作树没有被验证动作新增研究实现。

## 判定与交付

- `PASS`：上述 correctness 和信息边界全部成立；仅保留“Ch4 arm 未冻结、occurrence 未运行”的科学 blocker。
- `PARTIAL`：bridge API/顺序正确，但 fixture 或 hash 契约存在会在 occurrence 前必须修复的局部缺口；逐项给最小修复，不得自行修。
- `FAIL`：truth 泄漏、顺序错误、消歧错误、跨偏振 pooling、错误物理链或不可审计 hash。

验证报告必须给出：结论、逐条证据（文件/行号或 fresh 命令输出）、发现的问题按严重度排序、是否允许进入一次 occurrence smoke、唯一下一动作。一次 commit、不 push；commit 只能包含验证报告和必要 sim-preflight 使用日志。
