# Step 023 — Q15 终局 Step 3.5 + 条件式 Step 4a 归一化审判

> Task: T023 (CANDIDATE_FORMALIZATION, CP021, control epoch 53)
> Date: 2026-07-28
> Status: `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO` | mission_method_delta: `NONE`
> claim ceiling: Q15 被 conventional normalization 吸收；可靠负面 + evaluator/normalization
> 方法论教训；非方法进展。**本包后无第四个 Q15 repair/factory 包**。
> Artifacts: `projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/`

## 0. Task boundary（纪律自检）

- 仅完成 Q15 的 **Groundwork Step 3.5**（D1 纳入 + 定向检索 + 综合修正）+ **条件式
  Step 4a**（A0/A′/A/B/D + correct-normalization 终局审判）。
- **旧 T020 代码/raw/result/synthesis 只读复用**（import，未修改）；新审判在隔离目录
  `q15-step4a-normalization-adjudication/` 实现。
- **M2/M4 只称 monotone quantile/radius calibration**，不称已证明的 optimal transport。
- **D1 官方全文已公开获取**（EURASIP），不再列"不可得 mandatory debt"。
- **未跑** Step 5 / Contract / Execute / 任何 Q15 repair/factory 第四包；**未 push**。
- **未改** `.sessions/**`（owner/mission/log/decisions/master-state/current YAML）、
  T020/T019/B01-R/C11 artifacts、common/、params.py、cb1_evaluator.py、cb1_cell_runner.py。
- 全文精读（D1）、引用链批筛、web 结果消化**全部委托子 agent**；主对话未直接
  WebSearch/webReader。

## 1. Preflight

- `python .agents/skills/research-direction-lab/scripts/validate_task_control.py
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T023-q15-terminal-step35-step4a-adjudication.md`
  → **PASS**
- `git status --short`（worktree 起点）→ clean（无 modified）。

## 2. 理论预期写入新 contract + M1/evaluator audit

理论预期（写入 `contract.yaml` 顶部 THEORETICAL EXPECTATION 段，**先于任何 seed**）：

```text
若 z 的 prefix 功率估计为 Pz、公开 16QAM 目标功率为 Ps，
正确的复振幅乘子 a 满足 |a|² Pz = Ps，
因此 a = sqrt(Ps/Pz)，不是 Ps/Pz。
```

**caller/callee audit**（确定性核查，证据指针）：

| 项 | 实际 | 证据 |
|---|---|---|
| M1 公式 | `scale = E_ABS2 / trimmed_mean(|z_prefix|²)`（= Ps/Pz） | `preformal-method-factory-sprint-002/src/methods.py:69` |
| M1 应用 | `scale * z`（复数乘，功率比当振幅因子） | methods.py:85 (`m1_prefix_scalar_apply_continuous`) |
| 正确公式 | `a = sqrt(Ps/Pz)`；`|a|² Pz = Ps` | contract.yaml 理论预期 |
| M1/M2/M4 送入 evaluator | `*_apply_continuous` 返回连续 z，evaluator 自己 hard-decision + 8-way 搜索 | run_factory.py:240-275 |
| evaluator 恢复尺度？ | **否**。`evaluate_dual_16qam` 8-way = `{+1,+j,-1,-j}` × 流置换，rotation 均 unit-modulus，无法补偿任意幅度尺度 | cb1_evaluator.py:75 (`ROTATIONS_16QAM=[1,j,-1,-j]`), :172-237 |
| information access | M1/M2/M3/M4 freeze 只读 prefix `z[eval_start:calibration_end]`；apply 读 suffix `z[calibration_end:eval_end]`，suffix 不进 freeze/gate/scale | methods.py docstring; run_factory.py:232-235 |
| metric signature | PI-SER（置换不变）+ fixed_label_ser + pi_ber，dual 报 | cb1_evaluator.py:229-237 |
| state lifecycle | prefix-only frozen（无在线状态）；suffix 无反馈 | methods.py |

**audit 单测**（确定性验证）：synthetic z=c·s，c=0.45 时 correct sqrt SER=0.0，M1 wrong
SER=0.759（过校正 1/c=2.22×）。→ M1 公式错误 + evaluator 不恢复尺度 = M4 收益可能只是
补常规归一化。

## 3. Phase A：Groundwork Step 3.5

### A1. D1 正式纳入（EURASIP 官方公开 PDF）

DOI `10.5281/zenodo.40308` 经 `tools/download` FAIL（与 T021 一致）。EURASIP 官方 PDF
公开获取：`https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a4p-h07.pdf`
→ `papers/downloads/2026-07-28/` → `tools/pdf_convert.py`（fast/pymupdf4llm）转 md →
canonical `papers/manual/eurasip-2007-d1-shell-partitioned-mma/`。

**身份 receipt**：

| 字段 | 值 |
|---|---|
| verified title | Joint Blind Adaptive Equalization Based on Shell Partitioned Multi-Modulus with Soft Switching and Orthogonal Basis for 256 and 1024 QAM |
| authors | Grzegorz Haza, Ryszard Makowski（Wroclaw U. of Tech.） |
| venue | EUSIPCO 2007, Poznan |
| SHA256(source.pdf) | `0e104edda9c418d4…`（5,293,869 bytes, %PDF-1.6） |
| content.md 行数 | 271 |
| title_check | PASS（Jaccard=1.0） |
| metadata.json | expected/verified title, venue, DOI, EURASIP url, sha, source=eurasip_official_pdf |

**D1 精读**（子 agent 全文，逐项 + 章节/公式指针）：

1. Shell = **1-D PAM 级幅度子集**（非 2-D |y|² 环）；Q=√M/2/轴；半径 R²_R;k=E[|a_R|²|subset]（§1.2）。
2. ShMMA = **抽头更新代价**（eq.5→6→24），非 post-proc 输出 remap。
3. Soft switching = **Edge-MSE 估计器**（eq.10，指数窗 λ_E=0.98）驱动，**always-on 在线**
   用整个 running eval 流，**非 prefix-frozen，无因果隔离**。
4. **无 identity passthrough 分支**；两分支恒更新抽头；soft switch 连续混合永不零修改。
5. 目标 **256/1024-QAM SISO**；不涉及 16QAM、dual-pol、内环 collapse。

**D1 与 Q15 碰撞裁决**：**NONE**。

| Q15 维度 | D1 覆盖？ | 证据 |
|---|---|---|
| (a) prefix-only 因果边界 | NO | Edge-MSE/switch 用整个 running eval 流 |
| (b) identity fallback | NO | 无 identity 分支；两分支恒更新 |
| (c) post-proc frozen 输出 remap | NO | 抽头更新代价，非输出变换 |
| (d) dual-pol 16QAM collapse 恢复 | NO | 256/1024-QAM SISO；不涉及 |
| (e) gain/constellation normalization | PARTIAL | ShMMA 半径隐式每 shell 目标功率，但织入抽头代价 |

### A2. 定向检索（12 query / 2 源 / 收敛）

矩阵 = 方法轴（AGC/normalization、radius/shell MMA、regional/sliced、dual-mode gated、
post-eq radial）× 问题轴（dp-16QAM collapse、receiver prefix scale ambiguity、CMA
inner-ring collapse、post-eq radial quantile、monotone radius output、post-CMA identity
fallback）。结构化源 = Semantic Scholar + OpenAlex。结果存
`projects/thesis-fso/search-archive/2026-07-28/q15-step35-{slug}.json`（12 文件）。

| 关键 query | hits |
|---|---|
| p6 dual polarization 16QAM collapse singularity | **0** |
| p9 post equalization radial quantile calibration | **0** |
| a2 monotone radius calibration receiver output transform | **0** |
| a3 post CMA identity fallback zero regression safety | **0** |
| 其余 8 query | 1-6（generic AGC/DSP，多 off-topic） |

**收敛**：4 条最 Q15-specific 吸收威胁轴 query 全 0 命中；新增必读 = **0**。满足
gw-supplement 收敛判据。

**D1 引用链（双向）**：前向被引 **0**（S2 citationCount=0 + OpenAlex 交叉验证，未被引
叶节点）；后向 11 条，最相关 foundation：Lee 2000 ShCMA（10.1109/30.846661，D1 的 [4]
源头）、Yang 2002 MMA（10.1109/jsac.2002.1007381）、Godard 1980 CMA。

### A3. 综合结论修正（写入 literature_notes.md）

1. **D3 collision 修正**：`R_n=|z_n−ŝ_n|` 是 **decision-error radius**（z 到其
   hard-decision 的距离），非星座 shell radius。regions 是绕星座点同心圆（MSE 阶段
   代理），非 |z| 功率环。机制仍是抽头更新。collision 从 "HIGH 思想源头/shell radius"
   下修为 "decision-error-radius region switching（抽头更新层）"。
2. D1 不再列"全文缺失"（已精读，collision=NONE）。
3. Q15 判据 1 = PASS（句子级 M-C-A 成立 + 检索尽 + D1 零碰撞；主控授权宽松解读：
   C 直接发表证据缺失由 T020 diagnostic + C6 现象佐证，进 Step 4a 实证闭合）。
4. 判据 2 = PARTIAL（D1 零碰撞解除等价覆盖威胁；但须 Phase B correct-normalization
   实证；prefix-only/identity/post-proc 结构差异不自动当信息增量）。
5. 判据 3/4 = PASS（comparator 存在 / 可量化）。

### A4. Phase A 硬门

- Step 3.5 检索充分性达标（12 query / 2 源 / 收敛）。
- D1 已精读且**非 exact collision**（NONE）。
- Q15 四判据：1/3/4 PASS，2 PARTIAL（**判据 2 由 Phase B 实证闭合**——主控授权：
  Step 3.5 已尽检索义务 + D1 零碰撞 + M-C-A 句子级成立，进 Phase B 用 correct
  normalization 实证裁决吸收，而非纯文献 NO-GO）。
- conventional normalization 确定为 Phase B 必测强简单先验。
- literature_notes.md 已更新，evidence pointer 可核。
- **进入 Phase B**。

## 4. Phase B：条件式 Groundwork Step 4a

隔离目录 `projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/`，
含 `contract.yaml`、`src/{methods.py,run_adjudication.py}`、`tests/test_semantic_smoke.py`、
`artifacts/{raw-rows.csv,result.json,run.log}`、`synthesis.md`。

### B0. 起飞硬门（先于 seed）

写入 `feasibility_report.md` 的 Q15 Step 4a 段：A0 §0（Q# + 四判据）、A0 §1 性能间隙
[FR-02]、§2 问题结构（Q15 非 ML，N/A）、§3 跨域先例、§4 MDP（N/A）、§5 负面证据、
§6 先验覆盖（correct normalization 是否覆盖 = 维度 D）；维度 A′ 竞争维度分解、维度 A
结构优势、维度 B 新颖性-可行性 + 空白零假设（4 个）。**A0/A′/A/B 无致命信号**。

**seed 前冻结**（contract.yaml）：FR-11 架构摘要、FR-20 每参数溯源（全继承 T020/B01-R，
不为 Q15 改场景）、FR-21 oracle affine 只作 Kill（不作 Go 对手）、FR-18 testbed 简化对
所有 comparator 等价影响、FR-12 MVE=formal 架构（Q15 是 per-prefix frozen policy，无
架构差异）、FR-14/15 最强简单先验 + 贡献目标 comparator 清单。

### B1. 必备三方及消融（9 方法，全 prefix-only frozen）

1. fixed-μ CMA μ=0.03（baseline，Q15 的 M）
2. blind_affine（z-only 2×2）
3. C11_legal_causal（CMA+DD one-pass）
4. oracle_affine_bound（**Kill-only**，FR-21/FR-25，TX-truth）
5. M1_prefix_scalar_T020（**保留错误公式作透明对照**）
6. M2_quantile_transport_T020（monotone radius map，read-only reuse）
7. M4_gated_policy_T020（候选，gate + M2/M3 map，read-only reuse）
8. **correct_pooled_sqrt_rms**（NEW：a=sqrt(Ps/pooled robust_mean(|z|²))）
9. **correct_per_pol_sqrt_rms**（NEW：per-pol a=sqrt(Ps/robust_mean(|z|²))）
10. **gated_scalar_ablation**（NEW：M4 gate + correct scale，隔离 gate vs map）
11. **robust_scalar**（NEW：a=sqrt(Ps/median(|z|²)) per-pol）

Step 3.5 认定 nearest-shell/regional MMA/RDE 未在已获取论文中作 receiver-only output
transform（D2-D5 在 equalizer 层，C6 在 TX+RX）；D1 是 SISO 抽头更新；Step 3.5 检索无新
target-matched comparator。**correct normalization 是最强 conventional direct/cheap-alt
comparator**（吸收威胁轴）。无 `Q15_BLOCKED_TARGET_COMPARATOR_NO_GO`。

### B2. 公平性与 seeds

- 共享 realization；同 (cell,seed) 生成一次；7 T020 cells 不变；M4 gate 参数完全继承
  T020 dev freeze {collapse=0.6, spread=0.1}（不重看 test）。
- old slice 201-220（post-hoc mechanism adjudication：加 correct-normalization 到既有
  信号）；**fresh slice 241-260**（token-collision 检查：0 命中，确认 disjoint）。
- 新 baseline 不以新 test 调参（仅公式确定的 robust estimator）。
- seed-cluster 统计单位；primary PI-SER；MDE=0.005；10k bootstrap 95% CI。
- 逐 (cell,seed,method) raw + gate + prefix features + scale/map 参数 + offline 4 分类
  保存 `artifacts/raw-rows.csv`（7×40×11=3080 rows）。smoke receipt 未被 compare 覆盖。

### B3. 语义 smoke（先于 compare，TDD）

`tests/test_semantic_smoke.py` 8 测试（pytest 9.1.1，python 3.11.9，与 T020 一致）：

| 测试 | 结果 |
|---|---|
| correct sqrt 恢复 amplitude（SER=0 all c）；M1 wrong 过校正 c=0.45 SER>0.3 单调 | PASS |
| per-pol/pooled identity unbiased（mean a≈1.0）+ finite-sample 内 | PASS |
| prefix freeze invariance（suffix 扰动不改 scale/gate） | PASS |
| QPSK identity regression | PASS |
| information increment（不同输入不同输出） | PASS |
| clean stream 不被 identity 分支退化 | PASS |
| collapsed prefix 开 gate | PASS |

**8/8 PASS**。run_adjudication.py inline smoke（同物理容差）亦 PASS。无
`Q15_BASELINE_OR_EVALUATOR_IDENTITY_BLOCKED_NO_GO`。

### B4. 终局判据 + 结果

**seed-cluster mean PI-SER（10k bootstrap 95% CI，MDE=0.005）**：

| slice | baseline | M4 | correct_pooled | correct_per_pol | gated_scalar | **robust_scalar(最强)** | M4 vs robust |
|---|---|---|---|---|---|---|---|
| old 201-220 | 0.3143 | 0.2317 [−0.138,−0.032] 7/0/13 | 0.2234 | 0.2239 | 0.2269 | **0.2232** | M4 输 **+0.0085**（>MDE） |
| fresh 241-260 | 0.4150 | 0.2830 [−0.189,−0.078] 13/0/7 | 0.2696 | 0.2700 | 0.2758 | **0.2686** | M4 输 **+0.0144**（>MDE） |

**M4 在两 slice 都输给最强 correct normalization（robust_scalar）**，方向稳定（无符号翻转）。
gated_scalar_ablation（M4 gate + correct scale）≈ M4（overall 0.2513 vs 0.2574）→ map
无 gate+scale 外增量。correct scalar healthy 退化 0.016-0.027 < MDE（可用 conventional
comparator）；M4 healthy-worst=0.0（gate 安全）但 raw recovery 输。

**吸收机制**：collapse 是纯幅度尺度（z=c·s）；correct sqrt audit 精确恢复（SER=0 all c）。
M4 非线性 monotone radius map 无法 beat 精确标量恢复，quantile 锚引入轻微畸变致略输。
T020 M1 的"信号"只是补 M1 缺失的正确归一化。

**触发 `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`**：
- M4 未同时达 mean ΔPI-SER ≤ −0.005、CI upper<0、help>hurt **且** beat 最强 correct
  normalization（FR-15 FAIL）；
- 原 T020 信号主要被 correct/gated scalar 解释；
- fresh slice 方向稳定（M4 一致输）；
- clean/healthy 无 >MDE 灾难退化（M4 0.0；correct scalar 0.016-0.027）。

## 5. formal science disposition 与 mission_method_delta

- **formal_science_disposition**: `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`
  （判据 2 实证 FAIL；M4 不 survive 最强 correct conventional normalization；"problem
  survives conventional baseline" 状态未达）。
- **mission_method_delta**: `NONE`（可靠负面 + evaluator/normalization 方法论教训；非方法
  进展，非 PACKAGING_BOUNDARY）。

## 6. changed files、验证命令、commit receipt

### changed files（本包产出）

**gitignored（保留 worktree，不提交）**：
```text
papers/downloads/2026-07-28/eurasip-a4p-h07-d1-shell-mma.{pdf,md}   (.gitignore: papers/)
papers/manual/eurasip-2007-d1-shell-partitioned-mma/{source.pdf,content.md,metadata.json}
projects/thesis-fso/search-archive/2026-07-28/q15-step35-*.json (12 文件)
```

**tracked（提交，与 T020 sprint-002 目录同 convention：scout 工作目录入库）**：
```text
projects/thesis-fso/literature_notes.md   (新增 "Q15 Step 3.5" + "Q15 Step 4a 终局" 节)
projects/thesis-fso/feasibility_report.md (新增 "Q15 Step 4a" A0/A'/A/B/D + 决策段)
projects/thesis-fso/decision_log.md       (新建，记录 Q15 Kill)
projects/thesis-fso/worker-logs/step-023-q15-terminal-adjudication.md  (本文件)
projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/  (隔离目录全量：
  contract.yaml, src/{methods.py,run_adjudication.py}, tests/test_semantic_smoke.py,
  artifacts/{raw-rows.csv,result.json,run.log}, synthesis.md)
  — 不含 __pycache__/.pytest_cache（gitignore）
```

### 验证命令（全过）

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T023-q15-terminal-step35-step4a-adjudication.md
# → PASS

python -m pytest projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/tests/test_semantic_smoke.py -v
# → 8 passed

python -m json.tool projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/artifacts/result.json > $null
# → VALID JSON

git diff --check
# → (no whitespace errors)
```

### commit receipt

`EXTERNAL_RECEIPT_REQUIRED`

（Git commit SHA 由包含 worker log 在内的树计算，不能在同一 commit 内自包含自己的最终
SHA。禁止为追逐自引用 SHA 反复 amend。主控随后把真实 HEAD SHA 写入接收记录。）

## 7. 终态

- **status**: `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`
- **mission_method_delta**: `NONE`
- **未进入**: Step 5 / Contract / Execute / 论文声称
- **未给**: Step 4a recommendation / thesis-facing method card
- **未改**: `.sessions/**`、master-state、current YAML、T020/T019/B01-R/C11 artifacts、
  common/、params.py、cb1_evaluator.py、cb1_cell_runner.py
- **允许修改的文件全部落在授权路径**（§6 清单），未 push。
- **本包后无第四个 Q15 repair/factory 包**——Q15 退出。

## 8. 验收 checklist（task §4）

- [x] Step 3.5 coverage/convergence 与 D1 receipt（§3 A1/A2）
- [x] D3、D1、Q15 四判据修正（§3 A3；literature_notes）
- [x] Phase A gate（§3 A4）
- [x] Phase B 公式单测（§4 B3，8/8 PASS）、方法表（§4 B1，11 方法）、raw closure
  （artifacts/raw-rows.csv 3080 rows）、旧/fresh 两套 paired 数字（§4 B4）、strongest
  comparator（robust_scalar）、机制消融（gated_scalar≈M4）、clean safety（healthy<MDE）
- [x] formal science disposition 与 mission_method_delta（§5）
- [x] changed files、验证命令、commit receipt（§6）
- [x] 明确"本包后无 Q15 repair"（§7）
