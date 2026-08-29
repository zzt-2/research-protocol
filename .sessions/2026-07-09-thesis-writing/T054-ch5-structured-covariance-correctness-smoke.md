# Task Brief: Ch5 structured covariance implementation and correctness smoke

> 来源: S028 / D045 | 产出位置: `projects/simulation/explore/ch5-apsk-structured-covariance/` 与 `projects/simulation/tests/test_ch5_apsk_structured_covariance.py`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 7
  action_class: GW_STEP4A_D_IMPLEMENTATION_SMOKE
  mission_checkpoint: CP007
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在独立 explore seam 实现 Q-C5-1 candidate 与公平 covariance demapper arms，并运行 correctness/GMI-identity smoke。目标是证明估计式、Mahalanobis/log-det LLR、bit order、正定性、几何旋转和退化关系正确；合成 residual 只作算法测试，不证明目标平台存在 headroom。

## 必读与启动

1. 根 `AGENTS.md`、topic-index、D045、本 brief，先运行 task-control validator。
2. `sim-preflight` 全部规则、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、`reference/sim-template/{config.py,experiment.py,evaluate.py,verify.py}`。
3. `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-paper-feasibility.md`、T046/T049 的 read/supplement evidence，及 Layton full-covariance read note/fulltext。
4. 只读借鉴 `common/_modulation.py` APSK mapping、`soft_demap.py` bit partition/sign/clipping、`gmi.py` identity、`coded-decoder-feedback/codec.py` decoder接口。不得把硬编码 16QAM demapper 直接复用为 APSK。

## 冻结算法族

- B1：per-ring scalar covariance。
- B2（最强廉价替代）：per-ring radial/tangential hard pooling。
- B3（最强直接传统对手）：per-point full 2×2 real-IQ covariance + matched generic shrinkage/floor。
- C1 candidate：per-point radial/tangential local variance 向同 ring、同 polarization target 做 hierarchical shrinkage，`lambda_k = κ/(n_k+κ)`，`v_hat=(1-lambda_k)s_local²+lambda_k t_ring²`。κ 在本包仅取一个显式测试常数，不调优；cross-polarization sample pooling 关闭。
- 所有 arms 使用同一 mean rule、pilot samples、bit labeling、LLR clipping 与共享 numerical eigenvalue/variance floor；oracle covariance 只作 scoring identity，不是 deployable comparator。

## 接口与最小测试合同

建议新增 `contract.yaml`、`post_ch4_fixture.py`、`methods.py`、`codec_metrics.py`、`run_smoke.py`、`README.md` 与唯一 pytest 文件；不得修改 `common/`、`params.py` 或既有实验。

定义 `PostCh4Bundle`，至少含 `z/G_eff/Sigma_n/sample_phase/flags/constellation_id/labeling_id/pilot_mask/pilot_labels`。合成 fixture 必须显式标 `SYNTHETIC_CORRECTNESS_ONLY`。

必须测试：

1. APSK 4-bit labeling、bit partition、LLR sign 与 noiseless hard-decision roundtrip。
2. 所有估计 covariance 对称、有限、正定；B1/B2/B3/C1 共用 floor。
3. radial/tangential rotation 与 constellation 共同旋转时 equivariant；circular residual 下 B2/C1 正确退化为近 scalar，不制造增益。
4. `κ=0` 时 C1 退化为 point-local R/T；`κ→large` 时趋近 B2；同样本/同 ring target 下解析值一致。
5. Mahalanobis + logdet APSK LLR 与 brute-force reference 一致，且接口不读取 eval bits/TX residual truth。
6. paired fixtures/arms 共用 samples、pilots、labels 和 realization hash；train/eval residual 严格分开。
7. GMI identity 只验证 perfect/high-SNR LLR 优于符号翻转或零 LLR；不得比较 C1 与 B2/B3 的科学优劣。

## 交付与退出

- 运行 pytest 和最小 smoke，输出机器 receipt 与 README，显式写 `CORRECTNESS_ONLY / SYNTHETIC_RESIDUAL / NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL`。
- 不接 LDPC performance、不扫 SNR/pilot/κ、不为得到收益调整 anisotropy。
- `git diff --check`，只提交一次。
- 若 LLR sign/bit order、PD、退化测试或 truth firewall 无法通过，立即修正或 `BLOCKED`；不得用 clip/floor 掩盖公式错误。
- 最终只回报 commit、文件、测试/smoke 数字、解析退化结果和遗留 blocker；不声称 GMI/BER/FER 改善。
