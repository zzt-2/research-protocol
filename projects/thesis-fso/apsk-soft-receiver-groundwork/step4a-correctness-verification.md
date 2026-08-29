# T057 Ch5 structured-covariance correctness 独立复核

> 2026-08-30 | independent correctness verifier | authority: D045 / CP007

## 裁决

- `IMPLEMENTATION_CORRECTNESS: PASS`
- `TARGET_RESIDUAL_OCCURRENCE: NOT_TESTED / NOT_AUTHORIZED`
- `SCIENTIFIC_METHOD_SIGNAL: NOT_TESTED / NOT_AUTHORIZED`
- 总裁决：`PASS`

本裁决只接收 T054 correctness seam 的公式、实现、接口、identity、退化和机器 receipt。它不授权 occurrence/headroom/performance，不把 synthetic radial/tangential residual 当成目标场景信号，也不表示 Ch5 方法已经成立。

## 1. 启动门与审查边界

- T057 task-control 正式命令：
  `python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-07-09-thesis-writing/T057-verify-ch5-structured-covariance-correctness.md`
  → exit `0`, `PASS`。
- 在正式命令前曾误把 control 文件作为第二个位置参数传入，CLI 以 `unrecognized arguments` 拒绝并 exit `1`；该次未进入验证逻辑。随后按单位置参数接口 fresh 重跑通过。
- topic-index 的 CP007 允许 `INDEPENDENT_CORRECTNESS_VERIFICATION`，禁止 `SCIENTIFIC_EXPERIMENT`、`PERFORMANCE_GRID` 和 `FORMAL_THESIS_PROSE`；D045 只开放 Step 4a-D correctness。
- 本轮未运行 occurrence、headroom、BER/GMI performance grid、LDPC performance 或参数 sweep；未修改实现、测试、Skill/controller、治理或论文正文。

## 2. Layton Eq. (10)–(12) 原文核对

核对对象：Kelvin J. Layton, Azam Mehboob, William G. Cowley, Gottfried Lechner, “Improved demapping for channels with data-dependent noise,” EURASIP JWCN, 2018:123, DOI `10.1186/s13638-018-1136-z`。

### 2.1 来源完整性

- 当前 worktree 的 `papers/doi/10.1186_s13638-018-1136-z/source.pdf` 实际为 63,257 字节纯文本，SHA-256 `9ba585ed46266a088ba1a1266e203fd3879c2d7457fbc6bb089a8cef2b88d07f`，并非 `%PDF`；`content.md` 又把公式图片省略，二者单独不足以做 C6 原式核对。
- 本地另一 worktree 保留同 DOI 的真实 12 页 PDF：`C:/Users/zzt/.codex/worktrees/72c5/research-protocol/papers/doi/10.1186_s13638-018-1136-z/source.pdf`，2,261,353 字节，SHA-256 `b53c96bd24de33c978febb65ea0f9e374e0420332a4d3aba8ec40ab0582b84df`。主线程实际渲染并查看第 4–5 页；题名、作者、DOI、公式与当前纯文本提取和 read note 一致。因此不触发 `BLOCKED_AUTHORITY`。

### 2.2 原式与实现关系

Layton Eq. (10)，PDF p.4：

\[
p(\mathbf y\mid \mathbf x_k)=
\frac{\exp\!\left[-\frac12(\mathbf y-\boldsymbol\mu_k)^T
\boldsymbol\Sigma_k^{-1}(\mathbf y-\boldsymbol\mu_k)\right]}
{2\pi\sqrt{|\boldsymbol\Sigma_k|}}.
\]

因此略去所有星座点共同的 `-log(2π)` 后，symbol score 必须为

\[
g_k(\mathbf y)=-\frac12\left[(\mathbf y-\boldsymbol\mu_k)^T
\boldsymbol\Sigma_k^{-1}(\mathbf y-\boldsymbol\mu_k)+
\log|\boldsymbol\Sigma_k|\right].
\]

`codec_metrics.py:52-89` 正确实现 Mahalanobis、`slogdet` 与 exact log-sum-exp。Layton Eq. (6) 的约定是 `log P(bit=0)/P(bit=1)`，正值表示 bit 0；项目冻结约定相反，代码计算 `log_one-log_zero`，所以 `L_project=-L_Layton`，正值表示 bit 1。这是显式 convention 反号，不是 likelihood 错误。

Layton Eq. (11)–(12)，PDF p.5：

\[
\boldsymbol\mu_k\approx\frac1N\sum_{i=1}^{N}\mathbf y_i,
\qquad
\boldsymbol\Sigma_k\approx\frac1{N-1}\sum_{i=1}^{N}
(\mathbf y_i-\boldsymbol\mu_k)(\mathbf y_i-\boldsymbol\mu_k)^T.
\]

紧邻正文要求先按第 `k` 个星座点分组 pilots；因此这里的 `N` 是该点组的样本数。`methods.py:73-93` 对每点先求 pilot mean 再去均值，`methods.py:207-225` 把同一个只读 mean 对象绑定给 B1/B2/B3/C1，demapper 消费的也是该 pilot-estimated mean，而不是真值星座中心。

## 3. 自由度与四臂独立算术

对每个点 `k` 先计算 `e_{ki}=y_{ki}-mean_k`。同环 pooling 的正确分母为

\[
\nu_r=\sum_{k\in r}(n_k-1),
\]

不是 `sum(n_k)-1`，也不是未经逐点去均值的总样本自由度。故：

- B2：每个 R/T 轴分别用 `sum ||e_axis||² / ν_r`；
- B1：二维总平方和再除以 `2ν_r` 得 scalar component variance；
- point-local：每点用 `n_k-1`；
- C1：`lambda_k=kappa/(n_k+kappa)`，`v_hat=(1-lambda_k)s_local²+lambda_k t_ring²`；
- B3：每点 full `2×2` unbiased sample covariance，再做 generic isotropic shrinkage 与共同 eigenvalue floor。

独立构造 `n_k=[3,4,5,...]` 的 16 点小数组，直接用中心化矩阵平方和计算期望，不调用实现内部 helper；两环 `ν_r` 分别为 `23`、`24`。与公开 API 比较：

| 核对项 | 最大绝对误差 |
|---|---:|
| B1 scalar ring covariance | `4.336808689942018e-19` |
| B2 hard-pooled R/T covariance | `1.3010426069826053e-18` |
| B3 full covariance + isotropic shrinkage | `5.204170427930421e-18` |
| C1 hierarchical shrinkage | `3.903127820947816e-18` |
| shared pilot mean value | `0.0` |

B3 的独立 pre-floor 最小特征值为 `5.54824538737388e-05`，实现结果为 `5.5482453873738745e-05`，远高于本次 `1e-14` floor；这次公式匹配不是由 floor/clip 漂白非正定或错误公式。所有臂使用同一 floor 路径，输出对称且正定。

退化关系成立：

- `kappa=0`：C1 与 point-local R/T covariance 的最大误差 `0.0`；
- `kappa=1e15`：C1 与 B2 最大误差 `3.144186300207963e-18`；
- 非等 `n_k`：每点 lambda 随自己的 count 变化，公开 API 与独立闭式一致；
- circular residual：B2 scalar gap `2.3468894485873016e-19`，C1 scalar gap `2.3455919207502133e-19`；
- 星座与样本共同旋转：B1/B2/B3/C1 最大 equivariance 误差 `1.951563910473908e-18`。

## 4. LLR、APSK identity 与 truth firewall

- 独立 brute-force `inverse + quadratic + logdet + bit-subset logsumexp` 与 `mahalanobis_logdet_llr` 最大误差 `9.094947017729282e-13`。
- `common._modulation.m16apsk_mod` 直接生成表与 seam 表最大符号误差 `0.0`；constellation/labeling table SHA-256 为 `684fa7045c351f816e77eb1480784b013d8c100b3939b63d71b05b3b9b8ed879`。
- 四个 bit partition 均为 `8 zeros / 8 ones`；无噪 symbol roundtrip 在“正值=bit 1”约定下有 `0` bit errors。
- B1/B2/B3/C1 的 `GaussianArm.means` 是同一个只读对象；其值与从同一 train pilots 独立计算的每点 mean 完全一致。实际 LLR 调用传入 `model.means` 和对应 `model.covariances`。
- estimator API 只接收 `pilot_z/pilot_labels/constellation/floor/kappa/b3_shrinkage`；LLR API 只接收 `z/means/covariances/clip`。API 和 bundle 中均无 `evaluation_bits`、`payload_labels`、`transmitted_residual_truth` 或 `future_samples`。
- train/eval 使用独立 spawned RNG，数组不共享内存；eval `pilot_mask` 全 false、`pilot_labels` 全为 `-1`。deployable estimator 只读 train pilots；eval 隐藏 symbol indices 未写入 bundle。
- synthetic fixture 与 receipt 明示 `CORRECTNESS_ONLY / SYNTHETIC_RESIDUAL / NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL`；合成 anisotropy 仅用于 identity/correctness，不参与方法排序或科学裁决。

## 5. Fresh 执行证据

### 5.1 pytest

命令：

`python -m pytest projects/simulation/tests/test_ch5_apsk_structured_covariance.py -q`

结果：exit `0`，`13 passed in 2.50s`。

### 5.2 correctness smoke

为遵守“只新增本报告”，实际执行 `run_smoke.py` 的 `__main__`，但把 `save_results` 输出重定向到系统临时文件，未覆盖 canonical receipt。两次先行 wrapper 分别因 `runpy` 不自动注入 simulation root / seam 路径而在 import 阶段 exit `1`；均未进入算法、未生成 receipt。双路径 import probe 通过后，fresh smoke exit `0`。

fresh receipt：

- SHA-256：`9853b283bac6539efb5c2032239daea6fcdec10386a81e6eb3da806e92a2e39b`；
- realization hash：`63d3f7f29f36563ed67e1edef6cdb3992885472bbcacbe86dead2cc492b5c6d0`；
- minimum covariance eigenvalue：`4.515432790811458e-05`；
- label roundtrip bit errors：`0`；
- GMI identity：correct `3.9999999881055355`，zero `0.0`，flipped `0.0`；
- `scientific_verdict=NOT_AUTHORIZED`，`target_occurrence=NOT_TESTED`，`method_signal=NOT_TESTED`；
- 除 `_meta.git_commit/timestamp` 外，fresh scientific payload 与 canonical receipt 完全相同。

### 5.3 仓库保护检查

- `git diff --check`：exit `0`。
- smoke 临时 receipt 与 PDF 渲染页均已删除。
- 提交前最终 diff 只允许本报告。

## 6. 唯一 blocker

唯一科学 blocker 仍为 `NO_AUTHORIZED_TARGET_RESIDUAL`：缺少带完整 config/hash、只含 receiver-visible 信息的 post-Ch3 + post-Ch4 known-pilot residual artifact，因此 natural covariance geometry 与实际 pilot sample budget 尚不可审计。

这不影响本次 `IMPLEMENTATION_CORRECTNESS: PASS`，但在 blocker 关闭前，`TARGET_RESIDUAL_OCCURRENCE` 与 `SCIENTIFIC_METHOD_SIGNAL` 必须保持 `NOT_TESTED / NOT_AUTHORIZED`，不得开放 occurrence/headroom/performance 或把 synthetic residual 当方法信号。
