agent_task: /root/audit_red_case1
fork_turns: none
skill_identity: git:53085bb5d1b7cc3e759e62af5c55397979402acc
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case1.md

## Raw adjudication

## 原始裁决

**选择：STOP / REDIRECT。不得扩 cells/seeds，不得冻结 `METHOD_SIGNAL`。**

- **Formal science disposition**：`G1_FORMAL_CONFIRM_NO_GO`。更严格地说，Gate 6 的正式证据链无效，不能把它解释为候选机制被科学否定。
- **Mission method delta**：`NONE`。
- **贡献层级**：仅保留 `BOUNDARY_RESULT + EVALUATION_INSIGHT`；可记录局部动作机制的诊断性正证据，但不是论文主方法贡献。
- **Claim ceiling**：`SLICE`，即该候选在当前 16QAM、7 cells、20 seeds、既定 CMA 后处理切片上的诊断结论；不得上升为 `CANDIDATE/FAMILY/DOMAIN` 方法主张。

### 事实与证据

实现确实执行了合同所称动作：

- 仅用 128-symbol calibration prefix 冻结 gate 和 scale，在独立 suffix 上评分。
- healthy 分支原样返回 CMA 输出；active 分支施加逐偏振 `sqrt(Ps/Pz_hat)`。
- 140 个 `(cell, seed)` 对、8 个方法形成 1120 条闭合记录。
- 20 个 recoverable-collapse 对中 gate 命中 19 个；29 个 healthy 对中 28 个走 identity、1 个误激活但未造成退化。
- G1 对 collapse 的 seed-cluster 平均 PI-SER 差为 `−0.55980`，CI `[−0.69471, −0.40640]`；healthy worst degradation 为 `0`。
- always-on scalars 的 healthy worst degradation 为 `0.015625–0.019531`，超过 MDE `0.005`；G1 相对 M4 的 collapse 差为 `−0.03546`，CI `[−0.04657, −0.02434]`。

这些数据支持一个局部诊断：**identity gate 能避免 always-on normalization 的健康区退化，而正确平方根缩放能恢复被标记的幅度塌缩。**

### 不允许冻结方法信号的原因

1. **Gate 6 的实现违反声明统计单位。**
   runner 在 `_balanced_accuracy_bootstrap` 中直接重采样 `(cell, seed)` 行，而合同明确规定 cluster 为 seed。由此得到的 `[0.8905, 1.0]` 不能作为预注册 Gate 6 的 PASS。

2. **事后修正本身没有闭合统计定义。**
   结果文件把单类 seed 的 per-seed balanced accuracy 固定为 `0.5`，但该处理未在合同中冻结；且其“仅 3 个 seed 同时含两类”的叙述与 raw CSV 不一致——实际有 5 个 seed 同时含 healthy 与 recoverable-collapse。因而不能把事后 `CI_lo=0.5` 当作已充分验证的科学负结论。合法结论是：**Gate 6 未被有效执行，正式确认失败。**

3. **D4 不是实际执行的任务匹配 comparator。**
   `d4_likelihood_gated_rde_apply` 直接原样返回已收敛 CMA suffix；raw CSV 中 D4 对全部 140 对均与 baseline 完全相同。代码没有运行 D4 的 tap-update 轨迹，因此 Gate 7 只能证明“identity 后处理不改善 CMA”，不能证明 G1 胜过或未被真实 D4/RDE comparator 吸收。

4. **“只在 collapse risk 时激活”超过证据。**
   Gate 还在 45 个 ambiguous 和 9 个 AWGN-dominated 对上激活；balanced-accuracy 计算排除了这 91 个非 healthy/recoverable 对。因此只能声称两类子集上的局部区分，不能声称全切片的 collapse-only activation。

5. **语义 smoke 未在终端结果中持久化。**
   `result.json` 的 `smoke_results` 为空；allowlist 内无法独立闭合 smoke 证据。

### 下一合法动作

关闭当前 workline，保留局部机制数据与以下收获：

- `BOUNDARY_RESULT`：G1 在当前切片呈现“collapse recovery / healthy zero-regression”权衡。
- `EVALUATION_INSIGHT`：分类指标的 cluster estimand 必须在合同中精确定义，不能以 pair bootstrap 或事后单类-seed 规则替代。

随后轮转到最佳合法 READY 候选。若以后重新研究 G1，必须作为新的授权 workline，预先冻结 seed-cluster balanced-accuracy estimand，并实现同阶段、同任务、同信息的 conventional comparator；不得作为当前合同的扩 seed/cell 救活包。

### 实际读取的 Skill 路径

- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/SKILL.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/core-loop.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/batch-and-atlas.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/baseline-adjudication.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/method-production.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/thesis-harvest.md`
- `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`（平台启动检查；文件中的 `SUBAGENT-STOP` 指示子 Agent 忽略，未作为裁决依据）

### 实际读取的证据路径

- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\contract.yaml`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\src\methods.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\src\run_g1_confirm.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\artifacts\result.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\artifacts\raw-rows.csv`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\scout\g1-safe-gated-normalization-confirm\artifacts\synthesis.md`
