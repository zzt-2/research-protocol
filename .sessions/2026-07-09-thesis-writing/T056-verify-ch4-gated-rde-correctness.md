# Task Brief: 独立复核 Ch4 gated-RDE correctness seam

> 来源: S028 / D045 / T053 | 产出位置: `projects/thesis-fso/apsk-front-end-groundwork/step4a-correctness-verification.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 7
  action_class: INDEPENDENT_CORRECTNESS_VERIFICATION
  mission_checkpoint: CP007
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

以 fresh context 独立审查 T053 提交的 Ch4 seam。重新推导并核对 canonical RDE 更新、2×2 pilot-LS、APSK mapping/ring score、hard gate 退化、truth firewall、paired realization 和机器 receipt；实际重跑目标 pytest 与 correctness smoke。只判断实现正确性与可复现性，不寻找增益、不调参、不跑性能网格、不形成科学 Go/Kill。

## 启动与证据

1. 读根 `AGENTS.md`、topic-index、D045、本 brief，先运行 task-control validator。
2. 按任务触发并完整读取 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md` 与相关测试模板；不得扩读无关治理历史。
3. 审查 `projects/simulation/explore/ch4-apsk-ring-gated-rde/` 全部文件及 `projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py`。
4. 直接核对本地 `papers/doi/10.1109_jlt.2009.2021961/source.pdf` 的论文页 3044、Eq. (9)–(10)，并交叉核对 Ready–Gooch RDE 本地全文/笔记。不能只相信代码 docstring 或实现者手算测试。

## 必验项目

1. 对约定 `z = W @ y` 独立做 Wirtinger/复数梯度推导，确认更新符号、`z`/`z*`、输入共轭与逐行 gate 放置；给出 PDF 页码/式号和本实现转写。
2. 核对 APSK label-index mapping 与公共调制资产逐点一致，ring identity、nearest-symbol distance 和 normalized ring residual 不读取 TX truth。
3. 核对 random `J` 真为 SU(2)，正交 pilot 与 LS 逆矩阵方向正确；identity/random-J 无噪误差应在数值精度。
4. 重新计算一步复数更新，不复用测试里的 expected；复核 all-one=plain、zero=W0、cheap=single-feature candidate。
5. 检查 deployable arms 的函数签名与调用链不接收 TX symbols、true Jones、true SNR、evaluation BER；oracle truth 不反流。
6. 检查所有 arms 共用 symbols/J/noise/W0/seed/hash；receipt 不把 30 dB correctness cell解释为性能信号。
7. 实际运行目标 pytest、`run_smoke.py` 和 `git diff --check`，记录命令、退出码、关键数字与 receipt hash。

## 判定与退出

- `PASS`：上述项目全部成立，允许主控考虑开放一个预注册 oracle/headroom cell；仍不代表方法有效。
- `FAIL_REPAIRABLE`：有具体公式、测试、接口或 receipt 缺陷；列出文件/行号、预期行为与最小修复，不自行修改代码。
- `BLOCKED_AUTHORITY`：本地原文无法支撑所用 canonical 更新，且不能通过独立推导消除歧义；停止，不以测试自洽替代权威。

只允许新增指定 verification report；不修改实现、测试、Skill/controller、论文正文、topic-index/decisions/verifications/voice、`papers/index.json` 或任何日志。报告必须区分 `IMPLEMENTATION_CORRECTNESS` 与 `SCIENTIFIC_METHOD_SIGNAL`，后者固定为 `NOT_TESTED`。只提交一次，不 push。最终回报 commit、verdict、公式核对、fresh tests/smoke 数字和唯一 blocker。
