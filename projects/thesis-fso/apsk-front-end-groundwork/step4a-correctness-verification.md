# Ch4 gated-RDE 独立正确性验证

> 任务：T056 | 日期：2026-08-30 | 范围：correctness seam only

## 0. 总裁决（修复后）

- `IMPLEMENTATION_CORRECTNESS`: **PASS**
- `SCIENTIFIC_METHOD_SIGNAL`: **NOT_TESTED**
- 唯一 blocker：**无**。首次验证发现的 update-target 语义缺陷已由 `9f51caf` 修复，并经本报告 §7 独立复验关闭。

§1–§6 保留首次验证时的 `FAIL_REPAIRABLE` 事实快照；当前有效裁决以本节和 §7 为准。修复后，更新式符号/共轭、canonical nearest-radius target、APSK mapping、SU(2)、pilot-LS、gate 语义、truth firewall、paired realization 与 receipt 边界均通过独立检查。允许主控在既有 authority 下开放**预注册的 development/headroom cell**；该授权只代表 correctness gate 已关闭，不构成方法有效性、性能改善或科学 Go/Kill。

## 1. 启动、权限与证据边界

首个项目动作运行：

```text
python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-07-09-thesis-writing/T056-verify-ch4-gated-rde-correctness.md
```

退出码 `0`，结果 `PASS`。当前 checkpoint 为 `CP007`，仅授权独立 correctness verification；本次未运行性能网格、未调参、未形成科学 Go/Kill，也未修改实现、测试、治理、论文正文或既有 receipt。

按 brief 读取了 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、相关 verify 模板，以及 seam 全部文件和唯一目标测试；没有扩读无关治理历史。

## 2. 公式权威与独立推导

### 2.1 本地原文核对

指定路径 `papers/doi/10.1109_jlt.2009.2021961/source.pdf` 实际是 43,925-byte 的纯文本提取物，不含 `%PDF`、xref 或 trailer；其论文页 3044、Eq. (9)–(10) 位置存在，但公式字形为空，因此不能充当“可视原 PDF”权威。

没有因此降低证据标准。只读核对了以下两份未复制、未提交的完整本地原 PDF：

- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\papers\manual\ieee-9492010-likelihood-rde\source.pdf`：Di Rosa–Richter, JLT 2021，PDF 1.4，1,197,987 bytes。印刷页 6108，Section II-A，Eq. (1)–(3) 给出 butterfly 输出、四行 SGD 抽头更新以及 `epsilon=R_k^2-|x_out|^2`；正文明确 `R_k^2` 是距输出平方模最近的 constellation ring 半径平方。
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\papers\manual\ieee-9333378-blind-rde-likelihood\source.pdf`：ECOC 2020，PDF 1.7，387,203 bytes。其 likelihood/hard-selection 更新只允许高可信 ring assignment 进入更新，支持 gate 只乘更新项而不改变 base SGD。

Ready–Gooch 本地全文/图像进一步交叉确认 `w(n+1)=w(n)+2 mu x*(n)e(n)` 与 radius-directed error；常数 2 可吸收入步长。上述完整原 PDF、Ready–Gooch 和下述独立推导共同消除了符号与共轭歧义，故坏下载不是 authority blocker。

### 2.2 row convention 独立推导

约定单支路 `z_i=w_i y`，其中 `w_i` 是 `W` 的行，代价

```text
J_i = 1/2 (|z_i|^2 - R_i^2)^2 .
```

Wirtinger 导数为

```text
dJ_i/dw_i* = (|z_i|^2 - R_i^2) z_i y^H .
```

因此负梯度更新为

```text
w_i+ = w_i + mu g_i z_i (R_i^2 - |z_i|^2) y^H .
```

这与 `core.py:123-125` 的 `z * (R^2-|z|^2)`、`outer(..., conj(y))` 在符号、`z`/`z*`、输入共轭和逐行 gate 位置上完全一致。问题不在 `canonical_rde_step`，而在调用者给它选择了错误的 `R_i`。

### 2.3 update-target 语义缺陷

Canonical RDE 应按

```text
R_i^2 = argmin_{r in {r1,r2}} ||z_i|^2-r^2|
```

选择更新半径。`nearest_apsk` 在 `core.py:56-63` 却先按二维欧氏距离选择最近 constellation point，再把该点所属 ring 写入 `scores["radii"]`；`_run_rde` 在 `core.py:158-166` 将这一半径直接传给所有 arm 的 `canonical_rde_step`。

两者并不恒等。对当前 `(8,8)-16APSK`，`r1=0.5128238844547685`、`r2=1.3179573830487548`，取 `z=0.9+0j`：

| 判据 | 内环 | 外环 | 选择 |
|---|---:|---:|---|
| `||z|^2-r^2|` | 0.5470116635 | 0.9270116635 | 内环（canonical RDE） |
| 到最近 ring point 的平方距离 | 0.2201708533 | 0.1746883740 | 外环（当前代码） |

于是 `z(r^2-|z|^2)` 应为 `-0.4923104972`，当前代码却给 `+0.8343104972`，梯度方向相反。因此：

- T052 §4.1 允许 candidate gate 使用“nearest constellation point 所属 ring residual”；该特征可以保留。
- T052 §4.1 step 5 要求 gate 乘在 canonical RDE 更新上；plain/cheap comparator 也必须复用 canonical nearest-radius 更新目标。当前四个 arm 均不满足这一点。

## 3. 独立数值复算与其边界

不导入测试 expected，独立复算 `W0=I`、`y=[0.5+0.25j,-0.75+0.5j]`、`R=[1,1.5]`、`mu=0.1`、`g=[1,1]`：

```text
z                         = [0.5+0.25j, -0.75+0.5j]
R^2-|z|^2                = [0.6875, 1.4375]
z(R^2-|z|^2)             = [0.34375+0.171875j, -1.078125+0.71875j]
mu * outer(error, y*)    = [[ 0.021484375+0j,
                              -0.0171875-0.030078125j],
                             [-0.0359375+0.062890625j,
                               0.116796875+0j]]
W+                        = [[ 1.021484375+0j,
                              -0.0171875-0.030078125j],
                             [-0.0359375+0.062890625j,
                               1.116796875+0j]]
```

结果与测试 expected 相同，证明 primitive 在显式给定正确半径时成立；该测试没有验证运行链是否按 nearest-radius 产生半径，故不能排除本次缺陷。

## 4. 其余必验项

- **APSK mapping 与 receiver-visible scores**：`core.py` 的 gamma `2.57`、能量归一化、内环 `pi/8+k*pi/4`、外环 `k*pi/4`、reflected Gray-8PSK 标签顺序与 `common/_modulation.py` 逐点一致。nearest-symbol label、point distance 和 point-ring residual 只读取 `z` 与固定星座，不读取 TX truth。
- **SU(2) 与 pilot-LS**：归一化四元数构造满足 `J^H J=I`、`det J=1`；独立数值最大 unitary 误差 `1.1107840558453256e-16`，determinant 为 `1+5.551115123125783e-17j`。正交 pilot 满足 `XX^H=nI`，LS 使用 `W=XY^H(YY^H)^-1`，方向正确；random-J 无噪 `max|WJ-I|=5.56501278935197e-16`，identity 为 `0`。
- **退化关系**：按当前实现，all-one candidate 与 plain 完全一致，zero gate 保持 `W0`，`decision_threshold=inf` 时 candidate 与 cheap 完全一致。它们只能证明 gate wiring 一致，不能证明共享的 update target 正确。
- **truth firewall**：deployable signatures 和 `_run_rde` 调用链不接收 TX symbols、true Jones、true SNR 或 evaluation BER。truth 仅进入 oracle gate和 `_attach_seam` 的离线评估量；未发现回流到 deployable adaptation。
- **paired realization**：四个 arm 共用同一 symbols/J/noise/W0/payload/seed/hash；fresh smoke 中四个 arm 的 unique hash 数为 `1`。
- **receipt 语义**：30 dB cell 仅记录 correctness 与 accepted updates，receipt 明确 `CORRECTNESS_ONLY / NO_METHOD_SIGNAL`，没有 BER/性能裁决。既有 receipt 的 formula blocker 文本未在本任务中修改。

## 5. Fresh 执行证据

### 5.1 目标 pytest

```text
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py -q
```

退出码 `0`：`6 passed in 0.37s`。

### 5.2 correctness smoke

Fresh 调用原 `run_smoke.py::main()`；仅在进程内把 receipt 指向 repo 内临时目录，运行后删除临时文件，以遵守“只新增本报告”的写入边界。

```text
exit code                         0
internal pytest                   6 passed in 0.34s
identity/noiseless LS max error   0
random-J/noiseless LS max error   2.289170737184863e-16
accepted updates                  candidate=506, cheap=506,
                                  oracle=512, plain=512
paired unique hashes              1
realization hash                  815ed95330f7452a1863168514cd520ca0596ae92bad558e259769f6583b879a
receipt verdict                   CORRECTNESS_ONLY
method signal                     NO_METHOD_SIGNAL
```

这些通过数字是可复现性证据，不是 method signal；由于 smoke 没有构造 nearest-point ring 与 nearest-radius 分叉的样本断言，它同样未捕获 update-target 缺陷。

## 6. 精确 repair scope

本任务不实施修复。最小修复边界是：

1. 在 `projects/simulation/explore/ch4-apsk-ring-gated-rde/core.py` 中把两个概念显式分离：
   - gate feature 可继续使用 nearest-symbol point、该点所属 ring residual 和 decision distance；
   - update target 必须独立按 `argmin ||z|^2-r_m^2|` 选择 canonical nearest radius。
2. `_run_rde` 对 plain、cheap、candidate、oracle 四个 arm 一律把 canonical nearest-radius 结果传给 `canonical_rde_step`；不要改变 gate 的 truth boundary，也不要让 candidate 的 point-ring feature替代 update target。
3. 在 `projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py` 增加显式分叉回归点（例如 `z=0.9+0j`），固定“gate 特征可指向外环，但更新目标必须为内环”，并对 plain/cheap/candidate/oracle 的更新目标分别断言。保留现有手算、退化、firewall 和 paired tests。
4. 重跑目标 pytest、correctness smoke 并刷新其机器 receipt；在此修复验证通过前，不得开放 oracle/headroom cell。

无需改公共 modulation、pilot-LS、SU(2)、scientific parameters、性能网格、论文正文或治理文件。若另行要求 cheap gate 的分数本身改为 canonical native-RDE residual，那是 gate/comparator 合同的额外澄清，不属于修复本次“更新目标耦合”的必要最小范围。

## 7. 修复后复验

### 7.1 整合边界

只读审阅 executor commit `9f51caf`，并以本地 cherry-pick commit `1a14a88` 整合到 verifier worktree。该提交只改 T056 repair scope 内的 6 个 Ch4 文件；verifier 未再修改实现、测试或 receipt。

实现已显式分离三种语义：

- `nearest_apsk(...)["radii"/"ring_score"]`：candidate 使用的 nearest-point 所属 ring 与 point-ring residual；
- `canonical_nearest_radius(...)`：按 `argmin ||z|^2-r_m^2|` 选择 canonical RDE update radius，并产生 native-ring residual；
- `_run_rde`：四个 arm 一律把 canonical radius 传入 `canonical_rde_step`；cheap gate 使用 native-ring residual，candidate gate 保持 point-ring residual + decision distance。

### 7.2 `z=0.9+0j` 分叉与四 arm

独立 fresh 探针得到：

```text
inner radius                         0.5128238844547683
outer radius                         1.3179573830487550
nearest-point ring radius            1.3179573830487548  (outer)
canonical nearest radius             0.5128238844547685  (inner)
candidate point-ring score           0.5336818876894426
cheap native-ring score              2.0799844999999997
canonical error                      -0.4923104971794502
```

在 `mu=0.1`、`W0=I`、all-one update 下，plain、cheap、candidate、oracle 四个 arm 均得到 `W[0,0]=0.9556920552538495`，与显式内环 canonical step 一致。阈值取 `1.0` 时，candidate point-ring gate 为 `True`，cheap native-ring gate 为 `False`，证明 gate 特征没有被错误合并。deployable signatures 及调用链的 TX/Jones/SNR/BER truth firewall 复验为 `PASS`。

### 7.3 Fresh pytest、smoke 与 receipt

目标 pytest fresh 运行：

```text
python -m pytest projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py -q
exit code: 0
7 passed in 0.37s
```

原 `run_smoke.py::main()` 使用 repo 内自动清理的临时 receipt 路径 fresh 运行，外层退出码 `0`：

```text
internal pytest                   7 passed in 0.37s
identity/noiseless LS max error   0
random-J/noiseless LS max error   2.289170737184863e-16
accepted updates                  candidate=506, cheap=506,
                                  oracle=512, plain=512
paired unique hashes              1
realization hash                  815ed95330f7452a1863168514cd520ca0596ae92bad558e259769f6583b879a
formula authority status          VERIFIED_BY_T056
receipt blockers                  []
receipt verdict                   CORRECTNESS_ONLY
method signal                     NO_METHOD_SIGNAL
```

Fresh receipt 与已提交 receipt 的算法、测试、hash、authority、blocker 和边界字段一致；临时 receipt 未保留，避免 verifier 改写 executor 的机器产物。

### 7.4 修复后裁决

`IMPLEMENTATION_CORRECTNESS = PASS`。首次发现的唯一 blocker 已关闭；主控可以开放预注册 development/headroom cell，但必须继续保持 paired design、truth firewall、独立 tuning budget 和 correctness/performance 分栏。`SCIENTIFIC_METHOD_SIGNAL` 仍固定为 `NOT_TESTED`；本次 PASS 不证明 gated-RDE 有增益，也不授权把 30 dB correctness cell 写成方法结果。
