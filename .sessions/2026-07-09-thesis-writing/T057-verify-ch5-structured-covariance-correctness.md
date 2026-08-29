# Task Brief: 独立复核 Ch5 structured-covariance correctness seam

> 来源: S028 / D045 / T054 / T055 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-correctness-verification.md`
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

以 fresh context 独立审查 T054 提交的 Ch5 seam。重新推导并核对 B1/B2/B3/C1 估计式、pilot mean、逐点去均值后的自由度、Mahalanobis/log-det LLR、APSK bit identity、退化/旋转/正定性、truth firewall 与机器 receipt；实际重跑目标 pytest 和 correctness smoke。只判断实现正确性，不使用合成 residual 证明目标场景存在或方法有效。

## 启动与证据

1. 读根 `AGENTS.md`、topic-index、D045、本 brief，先运行 task-control validator。
2. 按任务触发并完整读取 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md` 与相关测试模板；不得扩读无关治理历史。
3. 审查 `projects/simulation/explore/ch5-apsk-structured-covariance/` 全部文件及 `projects/simulation/tests/test_ch5_apsk_structured_covariance.py`。
4. 直接核对 Layton 2018 本地全文/笔记 Eq. (10)–(12) 的二维 Gaussian likelihood、pilot 分组均值与 covariance；不能只相信实现者注释或测试。
5. 读取 `projects/thesis-fso/apsk-soft-receiver-groundwork/post-ch4-residual-authority.md`，确认当前科学 blocker 仍是 `NO_AUTHORIZED_TARGET_RESIDUAL`。

## 必验项目

1. B1/B2/B3/C1 必须从同一 pilot samples、同一每点 pilot-estimated means、同一 constellation identity 和同一 floor 产生；demapper 的实际消费路径使用这些 means，而非另取真值星座中心。
2. 每点先去均值再做 ring pooling 时，方差自由度应为 `sum_k(n_k-1)`；用独立小数组算术检查 B1/B2/C1 target，不复用实现辅助函数。
3. C1 的 `lambda_k=κ/(n_k+κ)` 与 `v_hat=(1-lambda)s_local²+lambda*t_ring²` 正确；`κ=0`、`κ→large` 和非等 `n_k` 退化成立。
4. B3 为 per-point full 2×2 real-IQ covariance + generic isotropic shrinkage/floor；不因 floor/clip 掩盖非正定或公式错误。
5. Mahalanobis+logdet exact-sum LLR 与独立 brute force 一致，positive LLR 表示 bit 1；公共 `m16apsk_mod` 生成的点、bit partition、constellation/labeling fingerprint 一致。
6. R/T covariance 在星座与样本共同旋转时 equivariant；circular residual 下 B2/C1 退化为 scalar，不凭合成 anisotropy 给方法排优劣。
7. train/eval fixture 分离，deployable estimator/demapper 不读取 eval bits、payload labels、TX residual truth 或 future samples；receipt 明确 `SYNTHETIC_RESIDUAL / NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL`。
8. 实际运行目标 pytest、`run_smoke.py` 与 `git diff --check`，记录命令、退出码、13 项测试、关键解析误差和 receipt hash。

## 判定与退出

- `PASS`：上述项目全部成立；只说明实现可进入真实 residual occurrence/headroom 准备，不代表科学方法成立。
- `FAIL_REPAIRABLE`：有具体公式、自由度、接口、identity、测试或 receipt 缺陷；列文件/行号、预期行为与最小修复，不自行改代码。
- `BLOCKED_AUTHORITY`：Layton 本地证据不足以支撑 likelihood/estimator 且独立推导无法消歧；停止。

只允许新增指定 verification report；不修改实现、测试、Skill/controller、论文正文、topic-index/decisions/verifications/voice、`papers/index.json` 或日志。报告必须分别写 `IMPLEMENTATION_CORRECTNESS`、`TARGET_RESIDUAL_OCCURRENCE`、`SCIENTIFIC_METHOD_SIGNAL`，后二者固定为 `NOT_TESTED/NOT_AUTHORIZED`。只提交一次，不 push。最终回报 commit、verdict、公式/自由度核对、fresh tests/smoke 数字和唯一 blocker。
