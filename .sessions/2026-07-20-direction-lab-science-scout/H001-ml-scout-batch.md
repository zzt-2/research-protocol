# Handoff: CB1 16QAM headroom found — design and run ML Scout batch

> **SUPERSEDED by D005 / H002. Do not execute this handoff.** The headroom is diagnostic until a defensible task-appropriate conventional baseline and convergence check show that the problem survives.

> 来源: S001 + S002 | 交接目标: 在新对话设计并运行针对 inner-ring-collapse 的 ML Scout batch
> 文件名: H001-ml-scout-batch.md
> 日期: 2026-07-20

## 到哪了（状态）

CB1 modulation-generic closure **已实施并独立验证**。baseline-only Atlas 在 16QAM 代表域发现 **10/11 cells 有 headroom ≥ MDE 0.005**（max 0.333 at snr=25，66× MDE）。QPSK 回归 PASS（P03 v1 anchor PI-SER=0.0 字节复现）。

**核心机制发现**：standard-CMA Godard-with-z（R²=1.32）在 16QAM 上 SNR≥15 dB 时约 50% seeds 坍缩到内环（|z|²→0.2），per-seed PI-SER≈0.67-0.78；oracle affine 能恢复坍缩 seeds 到 PI-SER=0.0。headroom 主要来自这个 bimodal collapse。snr=5 dB 是 LOCAL_NEGATIVE（AWGN 主导）。

**独立验证 CONFIRM**（clean-room verifier 用 canonical prompt013 only）：QPSK 回归 PASS；snr=20/25/5 三 cell 数字 MATCH；collapse 模式真实；headroom 定义正确（oracle = Kill tool FR-21，nearest = Go baseline FR-25）。

本轮授权（campaign-contract.v1.yaml）**包含 `batch_ML_scout_conditional_on_headroom`**，下一对话不需要用户重新授权 ML Scout。

worktree：`.worktrees/direction-lab-capability-atlas`，分支 `codex/direction-lab-capability-atlas`，从 `65db4ef`。本轮末尾做单次 consolidated commit，不 push。

## 下一步干什么

**在新对话**（context 干净）设计并运行针对 inner-ring-collapse 的 ML Scout batch：

1. **必读优先级**（按顺序）：
   - `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（不变量 + 范围）
   - `projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/campaign-contract.v1.yaml`（授权 + 禁止）
   - `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/baseline-atlas/artifacts/cb1-baseline-atlas-v1-synthesis.md`（headroom 详情）
   - `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/baseline-atlas/cb1_evaluator.py` 和 `cb1_cell_runner.py`（复用 runner/evaluator）
   - `.sessions/2026-07-20-direction-lab-science-scout/S002-cb1-baseline-atlas-headroom.md` §后续（ML Scout 设计要点）

2. **设计 ML Scout batch**（参 campaign-contract.v1.yaml step_8_conditional_ml_scout）：
   - shared input contract：causal CMA trace features（output_power, weight_norm, |z|²/R² ratio, update_norm）— 这些是 receiver-visible，CSI_NONE 合法
   - mechanism-different candidates（不是 model-name 排列组合）：
     - 监督式 collapse classifier（label = per-seed collapse ground truth from oracle affine disagreement）
     - 自监督 anomaly detector（causal mask + reconstruction on control-rate traces，避免 B001 oracle-filtered 重蹈）
     - 学习型 re-init / fallback trigger（输出 abstain 或 reset action）
   - 必须包含：no-change baseline (identity)，strongest simple comparator (blind affine)，必要 ablation
   - 禁止：oracle-supervised 方法当贡献；pilot-only mechanism variants；model-name 排列组合当多样性

3. **legal comparator 纪律**：
   - **Go baseline = nearest-16QAM**（strongest legal non-ML）—— ML 必须在这个上赢
   - **oracle affine = Kill tool only (FR-21)**，不当 Go baseline (FR-25)
   - 同信息量：所有 candidates 和 baseline 用相同 receiver-visible 信息（CMA trace features）

4. **claim ceiling = SLICE**。即使 ML 赢 nearest-16QAM，不自动晋级 DOMAIN（receiver-CSI / soft-coded axes 仍 blocked）。

5. **独立验证（P6 分离审查）**：必须有独立子 agent 复核 ML 结果（不能自审自验）。复核至少：公式/参数/identity gate / comparator 信息量一致 / no oracle leakage / claim ceiling。

6. **harvest**：完成后至少一条 harvest（POSITIVE_MECHANISM_SIGNAL if ML wins; LOCAL_NEGATIVE if ML doesn't beat nearest-16QAM; SCOPED_NEGATIVE if ML only beats on some cells）。

## 纪律（和下一步直接相关的约束）

- **standard-CMA identity gate**：每个 cell/seed 必须验证 `gradient == 'Godard-with-z'`。注意 `_cma.py:CMAEqualizer2x2` 是 **scalar-error** 不是 Godard-with-z（H013 债务）；用 CB1 的 `cb1_cell_runner.standard_cma_godard_with_z` 或直接调 `prompt013.run_cma_diagnostic(mode='standard')`。
- **不修改 protected history**：canonical-state / portfolio/current.v1 / STATUS.v1 / B001-B003 / P03 Atlas / harvest/ledger.v1 / receipts 字节不变。新结果只进 `campaigns/science-scout-2026-07-20/` 和 `scout/cb1-.../ml-scout-batch/`。
- **不创建 legacy B004**：新 batch 用 B005+ ID。
- **主对话严禁 WebSearch/webReader**；论文精读/web 查询必须子 agent。
- **single consolidated commit at session end, no push**。
- **claim 诚实**：headroom found ≠ ML 会赢。oracle affine 是上界工具，不是 baseline。profile.md "警惕主线急于给方向性结论"。
- **公式/参数 provenance**：新公式/参数进入实现前必须更新 `formula-symbol-parameter-provenance.yaml`。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（canonical baseline / metric contract / protected history / no auto-promotion / no WebSearch）
- [ ] 已验证本 handoff 中至少 3 条关键事实声称：
  - [ ] CB1 closure QPSK 路径字节不变（验：跑 `tests/test_dual_pol_shared_channel.py` + `scout/cb1-.../tests/test_cb1_closure.py`）
  - [ ] 16QAM snr=25 headroom=0.333（验：重跑 `run_baseline_atlas.py` 一个 cell 或读 `artifacts/cb1-baseline-atlas-v1.json`）
  - [ ] `_cma.py:CMAEqualizer2x2.equalize` 是 scalar-error（验：读 `_cma.py:163-166` 对比 `prompt013` standard delta）
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on（governance-pilot / system / groundwork）—— 都是 dormant/active/closed，无 conflicts
- [ ] 已确认当前范围未违反"明确不含"（不修改 protected history、不创建 B004、不自动晋级、不 push）

## 接口变更（CB1 代码改动）

```yaml
# generate_shared_realization_dp 新增 modulation kwarg
type: signature_change
function: projects/simulation/common/_dual_pol_channel.py::generate_shared_realization_dp
old_signature: "generate_shared_realization_dp(N, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None, t_s=None, method=None)"
new_signature: "generate_shared_realization_dp(N, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None, t_s=None, method=None, modulation='qpsk')"
backward_compatible: true  # modulation defaults to 'qpsk'; QPSK path byte-identical
new_return_fields: [modulation, bits_per_symbol]
new_return_field_shapes: {modulation: "str in {'qpsk','qam16'}", bits_per_symbol: "int (2 for qpsk, 4 for qam16)"}
qpsk_regression: PASS  # tests/test_dual_pol_shared_channel.py 6/6 PASS; cb1 closure tests 11/11 PASS
```

## 失败数据附录

无路线失败。本轮所有步骤都产出。pre-existing failure（与本轮无关）：`test_p03_claim_scope_receipt_binds_exact_assessment_and_validator` 在 base commit `65db4ef` 上就 FAIL —— P03 receipt SHA 与 assessment SHA 不匹配，须专门治理任务修复。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| `_cma.py:CMAEqualizer2x2` scalar-error 与 docstring "Godard-with-z" 不一致 | canonical baseline 身份严格 (anchor.yaml mutable=false) | OPEN_ACKNOWLEDGED (H013) | 任何 DOMAIN 级 claim 或 formal 晋级前必须解决（rename 或加 GodardWithZ 变体 + 改 docstring） |
| `canonical-state.yaml::simulator.sha256=537dce98` vs worktree `3d02eaa3` | source closure hash 准确 | RESOLVED_IN_PROJECTION（行尾差异；authorization-projection.v1.yaml 绑 worktree SHA） | canonical-state 重绑或迁移到 git-attributes LF 强制时 |
| 16QAM R²=1.32 未 canonical 化 | baseline identity 完整 | DEFINED_IN_CB1_CLOSURE_ONLY（formula-symbol-parameter-provenance.yaml 已记录 DERIVED_IN_PROJECT） | 16QAM 正式晋级时须进 canonical baseline identity |
| P03 claim-scope receipt SHA 不匹配 | receipt hash-binding 严格 | PRE_EXISTING_FAIL_AT_BASE_COMMIT | 专门治理任务修复 receipt 或重发 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| CB1 closure QPSK 字节不变 | `test_dual_pol_shared_channel.py` 6/6 PASS | P03 source-equivalence contract | 6/6 this round |
| CB1 closure 16QAM smoke | `test_cb1_closure.py` 11/11 PASS | CB1 build plan step 5/6 | 11/11 this round |
| R²_16QAM = 1.32 | abs(R² - 1.32) < 1e-12 on exact 16-point constellation | analytical derivation | PASS this round |
| QPSK anchor PI-SER=0.0 | == 0.0 on P03 v1 cell | P03 v1 LOCAL_NEGATIVE | PASS this round (independently verified) |
| 16QAM headroom ≥ MDE | ≥ 0.005 on majority of cells | campaign-contract MDE 0.005 | 10/11 cells this round (independently verified) |

## 下一轮

在新对话（context 干净）：
1. 读 handoff 必读清单（topic-index → campaign-contract → baseline-atlas synthesis → S002 §后续）
2. 完成接收方验证清单
3. 设计 ML Scout batch（参 S002 §后续 8 点设计要点）
4. 运行 + 独立验证 + harvest
5. 单次 consolidated commit，不 push
