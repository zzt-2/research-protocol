# [S001] Campaign 启动：授权迁移、隔离 worktree、protected history 核验

> 2026-07-20 | SCIENCE_SCOUT campaign 启动 | 状态: 进行中

## 目标

完成首轮 SCIENCE_SCOUT campaign 的启动准备：
1. 恢复 STATUS、anchor、canonical-state、portfolio、harvest 和最新 projection；
2. 核验 protected history（B001–B003、P03 Atlas、B004 不存在、canonical baseline hash）；
3. 创建隔离 worktree（不在 integration worktree 实施科学代码）；
4. 登记新专题并迁移授权状态（READ_ONLY_MIGRATION_PREVIEW → 本轮 SCIENCE_SCOUT）；
5. 进入 Portfolio Refresh 和 Capability Leverage Atlas（实质推进，不停在规划）。

## 记录

### 已完成

**地基恢复**（来源均在 `projects/thesis-fso/direction-lab/` 与 `.sessions/2026-07-17-direction-lab-governance-pilot/`）：

- `STATUS.v1.md`：formal_goal = "identify legal ML information increment in the complete dual-pol ground-to-satellite OSL receiver chain"；formal_status = BLOCKED；migration mode = READ_ONLY_MIGRATION_PREVIEW；science mode = AWAITING_STRATEGY。
- `anchor.yaml`：anchor_id = `anchor.dual-pol-osl.2026-07-17`；canonical_baseline.mutable=false；3 个 open/contained 冲突已登记（master-state drift、runner-not-in-main-tree、scope-governance resolved）。
- `canonical-state.yaml`：baseline = `baseline.standard_cma.godard_z`（SHA `9282ecb5…`，已核验 PASS）；metric_contract = `{fixed_label_ber, permutation_invariant_ber}`；sandbox_state = BOARD_READY；last_completed_batch = B003（COMPLETED_SANDBOX_VERIFIED）。
- `portfolio/current.v1.yaml`：P03/U19 OPEN（claim_ceiling=SLICE，P03_DOMAIN_ADEQUACY_UNRESOLVED）；P01/U25 DEFERRED_ARCHITECTURE；P02/U10 NOT_RUNNABLE；U24/B003 HISTORICAL_SANDBOX_COMPLETE_NO_PROMOTION；U36 RETAINED_NOT_SELECTED。6 个 blocked_axes 已登记。
- `harvest/ledger.v1.yaml`：H001–H009 已 HARVESTED/VERIFIED/OPEN，含 FAILURE_MECHANISM（CMA-swap）、LOCAL_NEGATIVE（P03 Stage A 0/11 cells at MDE）、INFRASTRUCTURE_GAP（16QAM/receiver-CSI/coded-output 三轴 blocked）、REUSABLE_ASSET（Atlas gate + cell runner + driver + contract）。
- P03 Stage A synthesis：在 QPSK × SNR sweep × dynamics sweep × short/long × CSI_NONE × uncoded hard-decision 的 runnable representative sub-domain，0/11 cells 达到 MDE 0.005；最大 visible headroom 0.00039（13× below MDE）；exit = `NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`；3 个 axis 仍 INFRASTRUCTURE_BLOCKED（16QAM、receiver-estimated CSI、soft/coded output）。

**Protected history 核验**：

- B004 不存在（在 integration worktree 和新 capability-atlas worktree 均确认）。
- B001/B002/B003 目录存在且字节受保护（本轮不修改）。
- canonical baseline SHA `9282ecb5…`（`prompt013_swap_mechanism_q2.py`）在 `unified-batch-runner` worktree 核验 PASS。
- `_dual_pol_channel.py` SHA 偏差已诊断：canonical-state 声明 `537dce98`（main 工作树 CRLF）vs worktree 实际 `3d02eaa3`（LF）；纯行尾差异，内容相同；source closure 实际绑定 commit `65db35bb` + `_gg_time.py` git_blob_oid `9155de05`，与本专题工作无关。登记为 stale-checksum 债务，用新 projection 解决，不回写历史。

**隔离 worktree 建立**：

- `git worktree add .worktrees/direction-lab-capability-atlas -b codex/direction-lab-capability-atlas 65db4ef`：成功；git status clean；HEAD = `65db4ef`；B004 不存在；B001–B003 present；全局 Skill 和项目 Skill 可发现。

**专题登记**：

- 新专题 `2026-07-20-direction-lab-science-scout` 已加入 `_registry.yaml`（depends_on = system/governance-pilot/groundwork；conflicts_with = []；status = active）。
- `topic-index.md` 已建（范围边界、不变量、明确不含完整）。
- `voice.md` 已建（本轮授权原话 7 条）。

### 授权迁移设计（进行中）

本轮授权是 **新增 SCIENCE_SCOUT 模式叠加在 BLOCKED formal 之上**，不是解除 formal BLOCKED。formal Groundwork/Contract/Execute/论文晋级继续阻断；本轮只能在 sandbox/Scout 层进行合法 ML 信息增量探索。

迁移策略（不回写历史）：

1. 不修改 `canonical-state.yaml` / `portfolio/current.v1.yaml` / `STATUS.v1.md`（这些是 V007-DEPLOYED 的 protected history）。
2. 新建 `campaigns/science-scout-2026-07-20/campaign-contract.v1.yaml`，声明本轮 SCIENCE_SCOUT 的 scope、allowed/forbidden actions、claim ceiling、退出条件。
3. 新建 `campaigns/science-scout-2026-07-20/authorization-projection.v1.yaml`，作为本轮的状态投影（叠加在 canonical-state 之上，引用 protected history hashes，不回写）。
4. 显式登记 stale-checksum 债务（`_dual_pol_channel.py` 行尾差异）在新 projection 的 `known_debts` 段。

### Portfolio Refresh 与 Capability Leverage Atlas（即将开始）

按用户提示词 §五和 §六推进。将调度子 agent 并行做：
- 子 agent A：审计已有论文库 / search-archive / literature_notes / competitor_notes，产出 baseline-source-matrix 和 unresolved-source-gaps。
- 子 agent B：审计现有代码资产（common/、explore/、tools/、scout/），产出 capability-asset-inventory。
- 主对话：综合产出 candidate-universe.v3（12 维展开）、capability-leverage-atlas.v1（5 能力包评估）。

## 决策引用

- 无 D### 新建（授权迁移和专题登记是 campaign setup，不是架构决策；本轮首批 D### 将在 Portfolio Refresh / Capability Atlas 阶段产生）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。授权迁移、隔离 worktree、protected history 核验、专题登记均在本专题"原始目标"和"当前范围"内。

## 后续

立即推进（不停下问用户）：
1. 建 campaign contract + authorization projection（完成授权迁移）；
2. 派 2 个并行子 agent 审计已有论文库和代码资产；
3. 主对话综合产出 candidate-universe.v3 + capability-leverage-atlas.v1；
4. 建 `formula-symbol-parameter-provenance.yaml` 硬门骨架；
5. 拍板首个共享能力（先验：modulation-generic closure）；
6. 实现共享能力 → baseline Atlas → 视 headroom 决定是否触发 ML Scout。

**债务清单（须用新 projection 解决，不回写历史）**：
- stale `_dual_pol_channel.py` checksum（行尾差异，内容相同；canonical-state 的 SHA 是 main 工作树 CRLF 版本）。
- stale internal checksum 和 last_completed_batch pointer 须在新 projection 中重新绑定。
- 历史 raw artifacts（B001/B002/B003 的 raw batch 数据）在新 worktree 中缺失（与 governance-pilot 已登记的 `raw_artifact_available_in_checkout: false` 一致），继续标记，不假装 self-contained。
