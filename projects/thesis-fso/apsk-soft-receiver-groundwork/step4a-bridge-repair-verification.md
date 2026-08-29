# Ch5 residual bridge repair 独立复验

> 2026-08-30 | T065 | independent scientific verifier
> 当前 HEAD `c304791` | T063 修复提交 `e141cc6`

## 裁决

- **PASS**。
- T061 的两项 P1 与随附 P2 均已关闭：完整 frozen Ch4 arm 数值快照真实进入 runner、deployable bundle、`bundle_hash` 与 required audit；Ch4 acquisition preamble 和 observation 真实共享一条连续 scalar→Jones→AWGN realization。
- 旧 firewall 全部成立：offline truth、future observation、polarization swap 与 8 个 APSK rotation 均通过独立突变/等变 probe。
- **允许主控按 D047 另派唯一一格 occurrence。** 本轮没有运行 occurrence、性能、调参，也不判断 C5-1 方法信号。

## Fresh 验证

1. Task-control：
   `python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-07-09-thesis-writing/T065-verify-ch5-residual-bridge-repair.md` → `PASS`。
2. 为避免测试内置 receipt 写入污染仓库，将当前 `projects/simulation/` 逐字复制到临时目录后执行：
   `python -m pytest tests/test_ch5_apsk_structured_covariance.py tests/test_ch5_post_ch4_ch3_bridge.py -q` → **33 passed in 3.24s**，exit 0。
3. 同一临时镜像执行 `python explore/ch5-apsk-structured-covariance/run_occurrence_smoke.py --mode correctness` → exit 0；`truth_firewall/eight_rotation/polarization_swap/covariance_identity=PASS`，`realization_hash=ae581a28e62c92c9932f88ee9ab64bc2c48cdfc878ec576d187cae7d9f5dadab`，`bundle_hash=cdeec988502fd25b8224373f28f2ecc5d36e8b5329170a6b8bf8d7b4164e79bd`。
4. 同一临时镜像执行 `--mode occurrence` → argparse `invalid choice`，**exit 2**；没有进入运行路径。
5. 一次性只读独立 probe → exit 0；未落实现、测试或结果文件。

## 独立 probe 数字

### Frozen-arm snapshot 与 hash

基础 candidate arm 的独立结果：

- `bundle_hash=d842448011dfe92bbb368afb9fcdd36bbefde68821415ce31b43817912869962`
- `realization_hash=68a10f8f7c9ef69d9aca1fee27a78495ba62f0ce7ae564e69eb57c6752d44187`
- snapshot 与实际 runner 入参、`ch4_summary.frozen_arm_snapshot` 三者逐字段一致；plain arm 的 `ring_threshold`、`decision_threshold` 两个键均显式存在且为 `null`。
- 独立按数组形状、dtype、bytes 和 metadata 重算两类 SHA-256，分别与上述 `realization_hash`、`bundle_hash` 完全一致；不是读取 receipt 布尔值。

| 单项突变（同一 receiver realization、同一 arm_id） | 新 `bundle_hash` | `bundle_hash` 变化 | `realization_hash` 保持 |
|---|---|---:|---:|
| `mu` | `3f6e7dd5e9e827087a431951df542aaffa2c25d4d47b23ec6755225e922497e2` | 是 | 是 |
| `ring_threshold` | `c2b271489605481e15acd48e1bd50bad2e6ab1a3f445d44d8b25a3aa5442a09d` | 是 | 是 |
| `decision_threshold` | `4991ef81a0669efe64bdee9919daeb21847b7321aca5e04a6c91a1cd2edd0f51` | 是 | 是 |

Required-field audit 使用两个独立来源：contract 的 expected set 与 `deployable_dict()` 的 observed key set。结果为 bundle required `25/25`、observed fields `26`、missing `0`；snapshot required/observed `5/5`、missing `0`；offline-only 字段进入 exported bundle 的数量为 `0`。因此 audit 没有把 expected set 自身冒充 observed set。

### 连续 scalar 时序

在同 seed、identity Jones、noiseless 控制下，仅把 GG/CFO/ramp/Wiener 设为非零，独立比较 impaired 与 identity-scalar control：

| 量 | 最大变化/误差 |
|---|---:|
| acquisition `ch4_pilot_rx` 最大变化 | `0.14622001045332056` |
| observation `rx` 最大变化 | `1.2526005520831716` |
| Ch4 `W` 最大变化 | `0.11485031706054694` |
| preamble 用同一完整 scalar trace 重建误差 | `0.0` |
| observation 用同一完整 scalar trace 重建误差 | `0.0` |
| offline full phase trace 重建误差 | `0.0` |

完整 trace 长度为 `176=16+160`；审计边界为 preamble `[0,16)`、observation `[16,176)`，`realization_timing` 与该切分完全一致。边界相邻样本的 phase increment 为 `-0.004251659376215321 rad`，amplitude ratio 为 `1.4334282101272378`。这证明两段来自同一次完整 trace 后切分，不是各自重置生成。

### Firewall 与等变性

- 同时突变全部 offline truth：`payload_labels/payload_bits/true_jones/true_phase/true_snr`，`ResidualBridgeBundle` **全部 dataclass 字段逐项不变**。
- 突变 `observation_stop` 之后全部 future observation，bundle 全部字段逐项不变。
- polarization swap 的 `z/x/e`、labels、两级 counts、known mask、phase/frequency、ambiguity、gate counts 与 `W'=PWP` 共 13 项全部通过；`W` 最大误差 `2.2204463139480933e-16`。
- 8 个 APSK rotation 为 **8/8** 正确唯一恢复；最大恢复误差 `3.1401849173675503e-16`，最小 best-vs-second SSE margin `9.372583002030474`。

## Diff firewall

T063 提交 `e141cc6` 只修改 brief allowlist 内 7 个文件：必要 usage log、README、bridge correctness receipt、occurrence contract、bridge 实现、correctness runner、bridge test。没有修改 `common/`、`params.py`、Ch4 core、Ch5 estimator、Skill/controller 或论文正文，也没有生成 occurrence/performance artifact。

当前实现、contract、README、runner 和 test 与该修复提交一致；receipt 仅被后续 correctness-only 重跑刷新 `_meta.git_commit/timestamp`，科学内容与 hash 不变。验证开始时工作树 clean，本轮 fresh 动作只写临时镜像。

## 问题严重度

- P0：0
- P1：0
- P2：0

没有发现阻断 occurrence 的 correctness、provenance 或可移植性缺口。

## 唯一下一动作

由主控按 D047 **另派唯一一格 occurrence**；保持其余 occurrence/performance grid、调参和方法信号判断冻结。
