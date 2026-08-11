# Step 091 — C1 A0 step-090 residual findings narrow verifier

> 2026-08-10 | T045 / CP010 / epoch 10 | narrow fresh verifier  
> control：`rdl.task-control.v2`、`control_ref`、epoch、`FEASIBILITY_A0` 与 CP010 对 topic owner 解析一致。  
> scope：只复核 step-090 的 P1-1、P1-2、P2-1；未重开任何 CLOSED 项。  
> snapshot：report SHA256=`046bb45a95bde5672270a552828e2a5730987b48ac681c5fcad86f44b8755f27`；YAML SHA256=`6c1e228f892ac1981fd22d7c7e89e0247df5c2cece9a69798e4387da2b003a4b`。  
> no-experiment receipt：仅静态读取 T045、控制 owner、step-090 与中央 report/YAML，并运行 YAML 解析、哈希和 Git staging 检查；未运行 web/search/download、仿真、defect smoke、adapter、MVE、held-out、科学实验、代码实现、commit 或 push。

## 1. Verdict

**PASS；P0/P1/P2=`0/0/0`。**

step-090 的三个 residual findings 均已唯一、fail-closed 地修复；在本次限定触及的修订段落内未发现足以导致相反科学裁决的新直接矛盾。

## 2. Residual-finding closure

### P1-1 — CLOSED

- raw-row contract 与 cluster：YAML `:226-249` 冻结必需字段、`cluster_key=seed`，每次抽中的 seed block 同时带入三 cells、双 target polarizations、九个 injected fixtures 及 cached no-jump twins；重复 seed 即重复完整 block。
- estimand 与聚合顺序：YAML `:250-254` 先由 pooled affected-CW counts 逐 cell 计算 damage/recoverability/coverage，再对三个 cells 等权 macro；coverage 又在 `:276-279` 明确重复该顺序，因此禁止 pooled-all-cells 和 mean-of-ratios 替代。
- bootstrap/CI：YAML `:255-262` 唯一冻结恰好 10,000 replicates、NumPy PCG64 seed `2026081001`、two-sided 95% percentile `2.5/97.5`；每 replicate 对十个 seed blocks 有放回采样，并重算 cell counts、cell estimands 与 equal-cell macro。
- invalid replicates：YAML `:263-275` 分别定义 recoverability/coverage 的 any-cell 非正分母；保留为 NA、禁止 impute 0/1，invalid fraction 上限 `0.05`、valid replicates 下限 `9500`，越限分别 terminal 为 `UNSTABLE_DAMAGE_DENOMINATOR` / `UNSTABLE_HEADROOM`，CI 只用通过上限检查后的 valid replicates。

### P1-2 — CLOSED

- score normalization：YAML `:329-337` 要求 pilot score 除以 pilot observations 数；decoder score 在每个 candidate 相同的 full-frame evaluated coded-bit support 上归一化，并显式禁止 raw touched-CW sums。report `:245` 与唯一 owner 一致。
- dev-only fusion：seed owner `:79` 将 `observability_fusion_dev` 冻结为 `8050–8059`；YAML `:321-347` 仅在该 dev slice 上逐 cell 计算 MRR/top1、再三 cells 等权。
- 唯一 lambda：YAML `:338-347` 冻结 lexicographic objective：先最大 fused macro MRR，再最大 fused macro top1，再选较小 lambda；test 前恰好输出一个 lambda。candidate-ranking tie-break `:348` 未被误当作 lambda tie-break。

### P2-1 — CLOSED

- D0 gate：report `:239,280` 将 D0 闭环项限定为 occurrence、coded damage/headroom、recoverability、B2 absorption、decoder-information increment、diagnostic identity/information/cost。
- post-D0 boundary：report `:247,280` 明确 D0 不定义 fallback/applied policy，clean false-action、fallback、goodput safety 仅属于 policy-freeze 后 post-D0；YAML `:361-374,389-397` 同样把 S4 固定为无 action 的 clean diagnostic，并把这些 policy/safety 项移到新决策之后。
- 审查历史：report `:286-288` 诚实登记 step-090 `FAIL / 0/2/1`、本轮三类精确修复、narrow re-verification 前 D0 仍禁止。

## 3. Determinism checks

- YAML `yaml.safe_load`：PASS（top-level mapping）。
- T045 task-control：PASS；epoch `10`、CP010、`FEASIBILITY_A0` 与 topic control 一致，且 action class 在 allowed actions 内。
- 定向机器断言：10/10 PASS，覆盖 bootstrap、invalid replicate、coverage aggregation、S3 normalization/fusion 与 post-D0 boundary。
- bootstrap：PASS；唯一 RNG、replicate 数、cluster resampling、CI 与重算顺序均已冻结。
- invalid replicate：PASS；定义、NA 处理、双阈值、双 terminal 与 valid-only CI denominator 均已冻结。
- S3 fusion：PASS；dev slice、逐 cell→equal-cell macro、lexicographic objective 与唯一输出均已冻结。
- report post-D0 boundary：PASS；report 与 YAML 无冲突。

## 4. Findings

无 OPEN finding，亦无本轮直接引入的新矛盾。P0/P1/P2=`0/0/0`。

## 5. Control disposition

本 PASS 仅允许主控另立 D/V/CP 考虑是否开放 D0；本日志不直接授权 D0。治理转移前继续维持 CP010/epoch10，`D0_EXECUTION_AUTHORIZED=NO`，adapter、C1-ext、MVE、held-out 与科学实验继续禁止。

## 6. Protection receipt

- owner 开始 SHA：report=`046bb45a95bde5672270a552828e2a5730987b48ac681c5fcad86f44b8755f27`；YAML=`6c1e228f892ac1981fd22d7c7e89e0247df5c2cece9a69798e4387da2b003a4b`。
- owner 结束 SHA：report=`046bb45a95bde5672270a552828e2a5730987b48ac681c5fcad86f44b8755f27`；YAML=`6c1e228f892ac1981fd22d7c7e89e0247df5c2cece9a69798e4387da2b003a4b`。
- protected logs：
  - `p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- staging：开始与结束 `git diff --cached --name-only` 均为空。
- 唯一写入：`projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`；未修改 owner、治理文件、源码或四个 protected logs。
- 禁止动作：无 web/search/download、commit/push、D0、adapter、C1-ext、MVE、held-out、仿真或科学实验。
