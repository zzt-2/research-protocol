# [S009] 计数纠正（chronology fail-closed）+ P09 重定向 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH

> 2026-08-01 | CAMPAIGN_EXPLORATION_DISPATCH / 计数纠正 + 有效科学大包 | 状态：进行中（A 计数纠正完成；B P09 端到端执行中）
> 来源: 用户纠正+重定向执行指令（同一对话完成两部分 A+B，不得在 A 或入口准备后停止）

## 目标

**A**：确定性纠正 campaign 当前计数 8→7（P08-R2 chronology 缺陷 fail-closed：单一 commit `a21fdba` 同时含 runner+dev+test raw 8000-8039+verifier+result+治理，`p08r2_run.py:99` 同进程无 immutable freeze，grep freeze/receipt/hash/test_started 零命中，V075 verifier 只验 seed 不相交未核 chronology 闭合）。新增 D/V 血缘纠正不删旧记录；D049/V075 保留历史但"恢复第 8 包"效力被取代；D050/V076 NDA-ML STRATEGIC_GATE 保留；纠正本身不计有效科学包。

**B**：端到端执行重定向 P09 = `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH`（换机制族，对象=`bps_cpr`(`:91-118`) 真实 B×N exhaustive search；M=16APSK full blind phase search / C=有限实时计算预算 / A=每 window 对全部相位候选计算星座距离存在 B×N 搜索开销 / 目标=相同 receiver-visible 信息+相同延迟+相同 BPS objective 下减少 distance/objective evaluations 同时保持 full BPS 性能）。过入口四门 + **独立 pre-test freeze receipt**（修复 chronology 缺陷，独立 Commit 1 在任何 held-out test 前）+ Phase A→B→C 门控 + 独立 verifier 11 项 + Commit 2。不 push。

## 记录

### Route check（三句）
1. 本轮 A 是计数纠正（chronology 缺陷 fail-closed，SCIENCE_INTEGRITY_REPAIR，不计有效包数，同 P07-R/D046、P08-R/D048、P08-R2/D049 修复模式）。
2. 本轮 B 是 campaign 第 8 有效科学大包的新入口（重定向 P09，换机制族：16APSK BPS search 复杂度优化；非 NDA-ML body 非 coded/interleaving 轴）。
3. 必须同一对话完成 A+B，不得在 A 或入口准备后停止（用户硬约束）。

### Part A：计数纠正（已完成 2026-08-01）

**chronology 缺陷证据**（主线程 git chronology + grep + Python JSON 核实，不信任 executor 自述）：

1. `git show --stat a21fdba`：单一 commit 22 文件 9722 insertions，含 runner（`p08r2_run.py` 391 行）+ dev workspace（`p08r2_dev_workspace.json` 327 行）+ **test raw（`p08r2_phaseA_raw_rows.json` 6642 行，seed range 8000-8039 实测）** + verifier（`p08r2_verify.py`）+ result（`p08r2_v075_result.json`）+ 治理文件。**无任何 freeze-only commit 在前**。
2. `p08r2_run.py:99 def main()`：同一 Python 进程顺序 Step 0（`:120` metamorphic 门）→1（`:130` AWGN sanity）→2（`:143` dev workspace scan）→3（`:168` freeze metric，**进程内步骤顺序**）→4（`:221` tune B1/B2 on dev_tune）→5（`:248` test on FRESH test seeds 8000-8039）→6（`:276` CI）→7（`:330` verdict）。**无跨进程/跨 commit immutable freeze point**。
3. grep `freeze|receipt|sha256|hashlib|test_started|prefreeze|pre_freeze|pre_test|pre-test` on 全部 `p08r2_*.py` = **零命中**。"freeze" 仅 docstring `:5,:168` 文字描述步骤顺序，非密码学 receipt/hash 落盘、非 `test_started=false→true` 状态机、非 commit 边界。
4. `p08r2_verify.py:332-335` check c = `not (dev_seeds & history) and not (test_seeds & history)` —— 只验 dev/test seeds 与 campaign history 不相交，**未核 pre-test receipt/source/contract hash 闭合**。V075 19/19 ACCEPT 是 H7/H8/H9 修复 + consistency，**非 chronology 闭合证明**（V075 盲区，consistency≠correctness 第四度重演，本次是 chronology consistency 维度）。

**裁决**（confirmatory evidence fail-closed）：P08-R2 物理归因（coded loss 主导突发深衰落）**可能正确**，但其作为"有效科学包"的 chronology 证据链有缺陷 → 降 PARTIAL diagnostic + engineering asset，不计有效包。campaign `accepted_valid_packages` **8→7**，G 族 = **STOPPED_WITH_PARTIAL_ASSET**（D049/V075 corrected-chain engineering asset 维持：receiver-visible σ²_pre prefix-LS + γ_vis MMSE + metamorphic 门 Δ=0.0 + AST 递归 + 先验 MDE + 去 min(B1,B2)；本地诊断证据保留 PARTIAL diagnostic）。不允许 P08-R3，禁 coded/interleaving 换名重开（TL-30）。D050/V076 NDA-ML STRATEGIC_GATE 维持不动（不触发 `NDA_ML_BODY_REOPEN`）。

**治理产物**：D051（计数纠正，取代 D049/V075"恢复第 8 包"效力，engineering asset 维持）/ V077（chronology 缺陷独立复核 11/11 PASS）/ CP042（mission-log checkpoint）/ topic-index 控制块 epoch 77→78、authority D050→D051、mission_checkpoint CP041→CP042、accepted_valid 8→7、G 族 STOPPED_WITH_PARTIAL_ASSET / _registry.yaml last_updated 更新 / voice.md 收录用户纠正+重定向原话。

### Part B：P09 入口准备（进行中）

（见下方 §P09 执行记录，持续追加）

## 决策引用

- D051（新建）：计数纠正（chronology fail-closed）— P08-R2 缺独立 pre-test freeze receipt，"恢复第 8 包"效力被取代，campaign 8→7，G 族 STOPPED_WITH_PARTIAL_ASSET。
- V077（新建）：计数纠正独立复核 11/11 PASS。
- D050/V076（引用）：NDA-ML STRATEGIC_GATE 维持不动。
- D049/V075（引用）：corrected-chain engineering asset 维持作 PARTIAL reusable asset。
- 无其他新决策（P09 入口门 + 实验结论待 B 部分完成后记入 D052/V078）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。A 是科学完整性纠正（chronology 缺陷 fail-closed，D039 campaign 授权范围内）；B 是 campaign 第 8 有效包新入口（换机制族 16APSK BPS search，非 NDA-ML body 非 coded/interleaving 轴，D047 coded-chain scope 不动）。未重开任何 forbidden axis（NDA_ML_BODY_REOPEN / 已关闭 A/E/F/G 族均未触碰）。未做 protected owner/formal/Skill/thesis framework 改动。

## 后续

- A 已完成（D051/V077/CP042 + 治理同步）。
- B 端到端执行 P09 `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH`：入口门四门（file:line）→ 16APSK BPS adapter → **独立 Commit 1（计数纠正 + frozen contract + receipt，任何 held-out test 前）** → Phase A（full BPS 性能+搜索成本）→ Phase B（fixed coarse/two-stage）→ Phase C（条件：候选 C1/C2/C3）→ 独立 verifier 11 项 → Commit 2 → 五项汇报。不 push。
- **chronology 闭合强制**（V077 教训）：P09 sprint 必须 pre-test freeze receipt 含 contract SHA256 + source hash + `test_started=false`，独立 Commit 1 在任何 held-out seed 读取前；runner 校验 hash 一致后才 `test_started=true`，hash 不一致即 EXECUTION_INVALID；held-out seed 如在现有 artifacts/ledger 出现过立即更换。
