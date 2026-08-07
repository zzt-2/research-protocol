# [S017] CCISP 单分支执行架构权威协调与方法闭合

> 2026-08-07 | thesis harvest / authority reconciliation | 完成，待统一提交

## 目标

在不寻找新方向、不改变 CCISP 算法本体且不混入 fixed-point 的前提下，拆分历史 2B 复合 authority，
从 immutable T005 raw artifacts 确定性复算 scheduling-only 证据，并形成可直接进入 Ch5 的工程方法包。

## 记录

### Authority facts

- T005 合同与 V016 已明确：scheduling 可独立达到论文工程方法门，fixed-point 失败不能 Kill scheduling。
- D023 的有效判断是“动作已属于 CCISP，不得另立 2B 新 selector”；无效延伸是把 scheduling 本身一并
  压成 SUPPORTING_ONLY。
- D036 保留前者并取代后者：复合 2B 仍 SUPPORTING_ONLY，scheduling 以 CCISP 真实动作身份晋级。

### Deterministic recomputation

- raw source：commit `67970307a051dd8149e1a750498a20674dfcfe6f`，990 performance + 990 timing shards。
- 990=3 scenes×11 SNR×30 seeds；396,000=990×400 windows；304,128,000=396,000×768 bits。
- command mismatch=0/396,000；selected-output mismatch=0/396,000；A-F/B-F pooled BER 均为
  32,589,134/304,128,000=0.1071559804。
- BF/AF seed-cluster timing ratio mean=0.5424435602，单侧 95% t-CI upper=0.5472819332；平均每窗
  679.2102 μs→363.5087 μs。正式 before/after 污染门 1,980 样本均未判 contention。
- 分支调用 792,000→396,000（-50.00%）；复乘 -39.45%、复加 -46.87%、除法 -51.28%、FFT
  -36.44%；dispatch/mux 不变。

### Method and packaging

方法动作冻结为 `receiver-visible selector → branch command → only selected recovery branch → common
downstream detector`。已形成完整 M-C-A、伪代码、公平 comparator、等价性、复杂度/时延、边界、主图、
主表、消融和 contribution statement。Terminal 仅在 V020 fresh-context verifier 独立复算并检查 claim
ceiling 后接收为 `THESIS_ENGINEERING_METHOD_READY`。字段分账：canonical contribution tier=
`THESIS_ENGINEERING_COMPONENT`；本轮用户四选一 task-local terminal=`THESIS_ENGINEERING_METHOD_READY`。

### 迭代计数器

- 假设：历史 formal timing 字段足以闭合 scheduling-only 时延合同。
- 否决条件：raw timing 缺少合法 repetition/affinity/contamination 字段，或独立复算的 ratio 上界不低于 1。
- 结果：PASS；990/990 schema/repetition 合法，单侧上界 0.5473，故未运行 bounded timing rerun。
- 本方向迭代：1；没有算法或物理场景修改。

## 决策引用

- D036：拆分 2B 复合 authority 并接收 CCISP 先选后算工程方法（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（用户显式授权的 scope change；见 D036）

## 后续

将本方法包按 Ch5 写作语言整合入论文；若未来需要硬件结果，必须另冻结综合平台、资源与功耗合同，当前
软件证据不得外推。
