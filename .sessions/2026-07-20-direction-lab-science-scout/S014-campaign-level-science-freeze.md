# [S014] SCIENCE_FREEZE — campaign-level reconciliation 与 Pilot-Jones 链状态裁决

> 2026-07-22 | 阶段：campaign 收口（SCIENCE_FREEZE） | 状态：收口完成，待 commit

## 目标

用户触发整体反思（"经过了这么多轮，咱们是不是该整体想想？"）。本轮**只有两个目标**（SCIENCE_FREEZE）：
1. 收口 Direction Lab SCIENCE_SCOUT 的当前真相；
2. 核清现有 Pilot-Jones 正式 Groundwork 链的真实门控位置，形成下一轮主控决策材料。

**本轮禁止**：不跑 F2 collision check；不跑任何新仿真/Probe；不重测 F1/F3/F4；不实现 tracker/pilot/ML/testbed；不 WebSearch/webReader；不新开专题；不 push；不修改 protected STATUS.v1.md / project.v1.yaml / canonical-state / 历史 artifacts；不把局部负面包装成完整负面论文；不继续按"候选 FAIL 后自动轮转"推进。

## 记录

### §一 确定性状态审计（HEAD / branch / git status）

- HEAD = `7efbea37823de6814f0641fd877635ac9fc50d9c`（与提示词一致），branch = `codex/direction-lab-capability-atlas`，worktree 干净（本轮前无未提交改动）。
- 编号核验：topic 内 max D=D021 / max V=V011 / max S=S013 / max H=H014。本轮新建 D022 / V012 / S014 / H015，编号连续。

### §二 stale current-view 字段（继承 D020/H013 旧结论，本轮全部修正）

| 文件 | stale 字段 | 旧值（继承 D020/H013） | 本轮修正 |
|------|-----------|----------------------|---------|
| state/current.yaml | F1A_MODEL_PRIOR_ORACLE_HEADROOM validity | VALID | INVALIDATED_AS_PROBE_CONCLUSION（D021/D022） |
| state/current.yaml | F3A_HISTORY_INFORMATION_INCREMENT validity | VALID | INVALIDATED_AS_CONDITIONAL_MI（D021/D022） |
| state/current.yaml | next_action.mode | await_user_investment_decision（F1-B PASS 叙述） | SCIENCE_FREEZE（D022） |
| state/current.yaml | formal_goal | 直接可执行研究问题 | 降级为上层筛选目标（D022） |
| portfolio/current.yaml | SPARSE_PILOT_SEMIBLIND | 双条并存矛盾（NEXT_CANDIDATE_NEEDS_COLLISION + IDENTIFIED_NEEDS_DEDUP） | 单条 MERGED_INTO_PILOT_JONES_NO_PARALLEL_SCOUT |
| portfolio/current.yaml | TEMPORAL_MODEL_HISTORY | 双条并存矛盾（PROBE_RETRACTED + PROBE_PASS_SECONDARY） | 单条 UNRESOLVED |
| portfolio/current.yaml | next_action | F1-A0 FAIL → F2 collision check 待用户裁决 | SCIENCE_FREEZE（D022） |
| harvest/current.yaml | recovery_entry | H013 | H015 |
| harvest/current.yaml | F1A_..._POSITIVE_SIGNAL status | active（primary method candidate） | retracted_not_active |
| harvest/current.yaml | F3A_..._INCREMENT status | active（secondary） | retracted_not_active |
| harvest/current.yaml | current_valid_spines PRIMARY | F1-B 主线（probe-passed pending Scout） | WITHDRAWN（无 main-method spine） |
| harvest/current.yaml | current_valid_spines SECONDARY | F3-B 次级 | WITHDRAWN |
| harvest/current.yaml | next_action | present F1-B investment decision | SCIENCE_FREEZE（D022） |
| topic-index.md | 状态行 | active（F2 collision check 待裁决） | dormant（SCIENCE_FREEZE D022） |
| topic-index.md | 当前位置 | S012/D020/V009/H013（F1-A PASS / F1-B 首选） | S014/D022/V012/H015 |
| _registry.yaml | status | active | dormant |
| _registry.yaml | description | F1-A PASS / F1-B 首选 Scout | D021/D022 收口叙述（F1-A0 FAIL，无 main-method signal） |
| H013 | 作为 latest recovery | last_recovery_entry | 被 H015 取代（state/portfolio/harvest 已改指 H015） |

### §三 D022 campaign-level 裁决（核心 9 条）

D022 裁决（详见 decisions.md D022）：
1. candidate rotation 暂停；
2. formal goal 降级为上层筛选目标（不再直接可执行）；
3. **当前没有合法 main-method signal**（本轮权威当前事实）；
4. F1=TESTBED_BLOCKED / F3=UNRESOLVED / F4=INFRASTRUCTURE_BLOCKED（不关闭 family，分别标状态）；
5. 不授权 F1 testbed 重建；
6. 不启动新 F2 Scout（collision check 本轮不执行）；
7. F2 lineage 合并入已有 Pilot-Jones 正式 Groundwork（不建平行链）；
8. 负面材料只进 harvest/limitations，不 pivot 完整负面论文；
9. campaign 收口置 dormant，恢复条件 = formal candidate 明确需要新 Scout。

protected 文件角色在 D022/H015 中明确标记（**不修改**文件）：
- STATUS.v1.md = STALE_PROTECTED（不是当前科学事实源；其头部仍写 F1-B 首选，已被 D021 撤回）；
- project.v1.yaml = historical read-only-preview adapter（不是当前授权 owner）；
- 当前可信事实源 = 修正后的 state/current.yaml + D022/H015。

### §四 Pilot-Jones 正式链真实门控（Explore agent 只读审计，file:line 证据）

> 本节回答提示词 §四 的 8 个问题。Explore agent 读 dual-pol-osl-groundwork 专题 S060-S074 / D052-D056 / V020-V029 + master-state.md，未补搜/下载/精读新论文。

1. **当前准确 GW Step**：Pilot-Jones 在 **Step 3.5（🔄 in progress）**，非 Step 4a。master-state.md:96 "Pilot Jones Step3.5 supplement | 🔄 待V030"；"Step4a仍封锁"。
2. **Step 3.5 已完成**：三轮 R1/R2/R3（S072/S073/S074 / D056 / V028/V029）。R1 加 4+1 must-read；R2 surface JLT2023 PDL/FPT；R3 new=0 收敛于 volume，但 backward 引用链 UNAVAILABLE。OE2021 全文精读完成（L08/L013）；JLT2022-23/TCOMM2025/LCOMM2026 仅 abstract。
3. **V030 ownership**：**V030 属 P03 非 Pilot-Jones**（verifications.md:782 "P03 residual-headroom Scout 最终独立终验"，关联 S075/D057）。Pilot-Jones Step 3.5 门控是 V028（verifications.md:639）+ V029（verifications.md:743），**均 PARTIAL**，且显式封锁 Step 4a（V028:669 "不能把 Step3.5 标为完成，也不能直接进入 Step4a"；V029:774-776 "不能按正常 PASS 门控进入 Step4a"）。**无任何 Pilot-Jones 专属终审 PASS V###**。
4. **缺的独立 verification**：缺一个独立终审 V### 完成 highest-citation 直接竞品 JLT2022 的 backward 引用链（V029:778-780 / S074:28）。S074 的 Crossref 补链未被独立复核（V029 在其之前跑，标 backward UNAVAILABLE）。
5. **Step 4a 缺维度**：master-state.md:96 确认 "Step4a仍封锁"。D056（decisions.md:2929-2931）block = 直接竞品 OE2021/TCOMM2025/JLT2022-23 须全文精读对比；当前仅 OE2021 全文。**Pilot-Jones Step 4a 的 A0/A/B/D 维度零起步**。
6. **generic pilot→Jones 撞车后剩余窄问题（M-C-A）**（S066:13/S066:17/decisions.md:2911）：
   - **M**：传统 block/frame pilot Jones inversion（短 pilot LS 估计）；
   - **C**：dual-pol OSL GG 湍流 + 高速 SOP + ≤10% pilot budget → 短 pilot 估计抖动/病态；
   - **A**：fixed-label 恢复不稳定；研究目标 = 量化/稳定 "pilot overhead — Jones estimate stability — fixed-label recovery" tradeoff。
   - 收窄 candidate_key（decisions.md:2889）：per-64-symbol 6 dual-pol QPSK pilots（9.375% overhead）+ per-block LS 2×2 Jones + EMA α=.9 + pinv derotation + standard-CMA。
7. **EMA09 15/15 + clean 0/9 的 claim ceiling 与 provenance 债**（S065:13/V023:725-727）：
   - 数字：EMA09 full24 = 24 cells（8 seeds×3 rates），failure≥50% 改善 = **15/15**，clean 退化 = **0/9**，divergence=0。
   - claim ceiling = **family-level promotion 到正式 GW Step 1，非 Go**（master-state.md:91 "晋级正式GW Step1，非Go"；S065:28 "该晋级不是Go"；decisions.md:2893 "晋级只说明值得投入正式证据链"）。
   - provenance/实现债：V022 PARTIAL（2p 公平性失败）被 EMA09 V023 修；fixed-label 定义修正（S065:10，old failure_improved 混淆 any-positive vs ≥50%）；old 72-grid 历史 SHA 保留但 "current runner 已变化、exact snapshot 缺失"（S065:16/V024:741）；formal promotion 依赖 EMA09 full24 独立 SHA，不依赖 old grid 可重放。EMA α=.9 选取避免 over-lag（decisions.md:2917 "不允许把没搜到同样 α=.9 当新颖性"）。
8. **下一轮建议**：**仅完成 Step 3.5 终审 + Step 4a，不是新 F2 collision search**。证据：master-state.md:96 自指 V028-V029 → Step 4a（封锁）；V029:778-780 "不需要第四轮关键词泛搜" 只需完成 backward 链；S074:28 + D056 完成剩余竞品全文 + 独立复核 backward 链（新 V###）即可。
   - **重要 caveat**：当前授权控制面入口是 P03/Headroom-Atlas 决策点（master-state.md:25-32），**非 Pilot-Jones**（master-state.md:26 "旧 Pilot-Jones Step 3.5/4a 链也未成为当前授权入口"）。若用户激活 Pilot-Jones，下一具体动作 = 完成 V029 backward-chain 终审 + D056 竞品全文，非新 F2 search。

### §五 当前仍有效的科学结论（收口后保留）

- **H060_COLLAPSE_LOCAL_SLICE_WEAK**：Godard-cost CMA inner-ring collapse 在 11-cell atlas slice 存在（LOCAL_SLICE 弱断言）；全域"信道属性/5 轴穷尽"宣称 INVALIDATED（D017）。
- **C11_LEGAL_VERDICT**：合法因果 per-symbol DD-LMS 无收益（macro +0.01445 worse）。
- **TRUTH_ASSISTED_AFFINE_LOCAL_BOUND**：TX-truth affine gap ~0.05575 是特权诊断 bound，非 learnable target。
- **BLIND_AFFINE_LOCALLY_HARMFUL**：blind_affine 局部净有害（gain -0.00837）。
- **HYBRID_BLIND_EXPERT_ROUTING_LOCAL_NEGATIVE**：合法 CMA/MMA/DD-LMS 间 oracle headroom 仅 0.003693（D018）。
- **DETECTOR_CONVENTIONAL_CEILING**：传统 min_z2 detector 在 long cells AUROC=1.000，lead time ≤0。
- **F4A_SOFT_GMI_BOUNDARY_SCALE_ARTIFACT**：corrected analytic GMI +0.0089（smoothing-fragile）+ histogram-MI 复现 C12 scale-artifact；F4-B coded-chain BLOCKED。
- **CB1_INNER_RING_COLLAPSE_SURVIVES_FAIR_TREATMENT**：collapse 存活 fair tuning + per-symbol + DD-LMS cascade。

**当前没有 main-method spine 的证据**：F1-A headroom 0.133 是 genie gap（D021）；F1-A0 FAIL（binomial p~0.38）；F3 非 conditional MI；F4 coded-chain blocked；D018 hybrid-router 0.0037。全部信息源族 Probe 无一产生可授权主方法的正面 signal。

### §六 范围与纪律确认

本轮严守 SCIENCE_FREEZE 边界：未跑 F2 collision check / 未跑仿真或 Probe / 未重测 F1/F3/F4 / 未实现 tracker/pilot/ML/testbed / 未 WebSearch/webReader / 未新开专题 / 未 push / 未改 protected 文件 / 未把局部负面包装成完整负面论文 / 未按自动轮转推进。Explore agent 仅只读审计已有文件。

## 决策引用

- D022：SCIENCE_FREEZE campaign-level 裁决（**新建**）——暂停 rotation、无 main-method signal、F1/F3/F4 分别标状态、F2 合并入 Pilot-Jones、负面只进 harvest、置 dormant。
- D021：F1-A 科学语义纠偏（amends D020，本轮引用不新建）。
- V012：本轮独立 verifier（**新建**，见 verifications.md）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。SCIENCE_FREEZE + campaign-level reconciliation + Pilot-Jones 链状态裁决，全部在 topic-index 范围内（"启动首轮正式 SCIENCE_SCOUT campaign ... synthesis → harvest → 自动轮换"的收口阶段）。

## 后续

- **下一轮唯一建议**：完成 Pilot-Jones Step 3.5 终审 + Step 4a prerequisites（见 H015），不是新 F2 collision search。
- 未决项（不在本轮范围，记录给主控）：STATUS.v1.md "protected unchanged" vs bf620b3 +9/-4 diff 矛盾（D021 gap #10）；canonical project.v1 vs SCIENCE_SCOUT projection controller ownership 冲突（D021 gap #11）；这两个矛盾本轮仅记录不裁决，交主控。
- 恢复条件：本专题 dormant，待 formal candidate（Pilot-Jones Step 3.5/4a 闭合后）明确需要新 Scout 时再恢复。
