# Handoff: RML-FSTS Step 4a Inconclusive testbed terminal

> 来源: S004 / D011 / V007 | 交接目标: 仅在重开输入齐备且显式 scope change 后恢复 Step 4a
> 文件名: H006-step4a-inconclusive-testbed.md
> 日期: 2026-08-09

## 已完成边界

D010 已在 V006 pre-run 审查后保持 `rejected`；T015–T017 进一步确认 scientific performance 起飞门被三类 hard blocker 阻断。D011/V007 已将唯一终态确认并独立验证为 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，verdict=`PASS, P0/P1/P2=0/0/0`。performance grid、diagnostic structural run 与 bounded MVE 均未运行；没有 scientific raw rows、paired delta/CI 或可报告 performance 数字。

## 不要做什么

- 不运行/恢复 T014 performance grid、diagnostic structural run 或 MVE；不构造 C1。
- 不把门控阻断写成“实验完成”或“跑了但无结果”，不发 Kill/Resolved/Go。
- 不把 Gu scalar-GG/无量纲 SNR 冒充 Wang phase-screen/SMF/dBm source calibration。
- 不把 V007 PASS 解释成性能或方法成立；不改 voice 或四个 `p05_run*.log`。
- 不进入 Step 5、Contract、Execute 或论文写作；不关闭 SSRN 6293357 全文债，不删除 strongest cheap comparator。

## 必读

1. `.sessions/2026-08-08-rml-fsts-groundwork/T019-step4a-independent-terminal-verification.md`
2. `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md`（D009–D011）
3. `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md`（V006）
4. `.sessions/2026-08-08-rml-fsts-groundwork/S004-step4a-feasibility.md`
5. `projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json`
6. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md`
7. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-physical-transfer.md`
8. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-wang-figure-axis.md`

## 接口变更

```yaml
contracts:
  - id: RML-FSTS-STEP4A-C001
    type: interface-change
    description: "Rejected semantic-smoke contract is explicitly non-authoritative"
    location: "projects/simulation/explore/rml-fsts-step4a/contract.json"
    change: "status=REJECTED_PRE_RUN; terminal_authority=NONE; verification_pointer=V006"
    consumed_by: "V007 independent terminal verifier"
    verification_result: PASS
    verified_by: V007
  - id: RML-FSTS-STEP4A-C002
    type: interface-change
    description: "Machine-readable verified Step 4a terminal receipt"
    location: "projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json"
    change: "Records verified terminal, NOT_RUN numerics, blockers, source/verifier hashes, claim ceiling and reopen inputs"
    consumed_by: "V007 and owner consistency checks"
    verification_result: PASS
    verified_by: V007
```

## 失败数据附录

### D010 pre-run contract

- 核心失败机制：off-default receiver-lag adapter 无权代表原 structural `(B_N,B_L)` action；未验证 SNR/transfer channel 无 source calibration。
- 独立审查：V006=`FAIL`，P0/P1/P2=`2/5/2`。
- performance 数据：B0/B1/B2/O1/C1=`N/A (NOT_RUN)`；scientific raw rows=`0`；paired delta/CI=`N/A (NOT_RUN)`。
- 已排除方向：用 D010 contract 发 Q1 terminal、用 synthetic SNR/GG 下 Kill/Resolved/Go、在 B2 前构造 C1。
- 可复用部分：公式 identity、structural action ledger、paired-exogenous-latent diagnostic contract；只能作 `DIAGNOSTIC_ONLY / TERMINAL_DISABLED`，本轮未运行。

### Hard blocker 与 recoverable gap

- hard blockers：structural action-before causality；source channel non-equivalence；dBm→discrete-noise non-identifiability；其结果是 B0 numeric calibration gate 不可执行。
- recoverable gap：Wang Fig. 8/10/11/12 direct image HTTP 403。恢复图可补 axes/ticks/部分 numeric targets，但不能自动关闭 hard blockers。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| SSRN 6293357 高风险全文 | 不用缺全文声称 novelty closure | 未关闭，继续保留 | 取得 qualified fulltext 并完成 action-level read |
| Wang figures/PDF | B0 calibration target 应有 source axes/points | direct figures 403，只有正文锚点 | 取得 canonical PDF/原图并预登记 digitization |
| receiver/channel source config | dBm、noise、phase-screen/SMF 必须可复现 | 不可辨识/不等价 | 取得 authors/source executable config 或后端标定接口 |
| action-before protocol | runtime action 必须因果可得 | 当前 FSTS power estimate为 action-after | 显式 scope-change，定义 probe/previous-frame、feedback、lifecycle、overhead与 fallback |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| Terminal semantics | 所有 owner/receipt 写唯一 terminal 5 与 V007 PASS，且无 Kill/Resolved/Go | D009 terminal 5 + V007 | PASS（1/1） |
| NOT_RUN integrity | grid/MVE/diagnostic 均 NOT_RUN；B0–C1 全为 `N/A (NOT_RUN)`；raw rows=0 | T015–T019 | PASS（1/1） |
| Blocker classification | 三类 hard blocker与 B0 gate 独立于 Fig. 403 recoverable gap | T015–T019 | PASS（1/1） |
| Machine integrity | contract/receipt JSON 可解析；六份 source hash 匹配；Markdown 引用存在 | T018/V007 | PASS（1/1） |
| Protected scope | voice/四个 `p05_run*.log` 未修改，excluded science paths无 diff | T018/V007 | PASS（1/1） |

## 接收方验证（续接对话时必须完成）

- [x] 已读取 topic-index 的不变量段落（V007）
- [x] 已验证本文件中的至少 3 条关键事实声称
  - [x] 声称1：performance grid/MVE 未运行，所有 performance 数字 N/A → V007 PASS
  - [x] 声称2：三类 hard blocker 独立于 Fig. 403 recoverable gap → V007 PASS
  - [x] 声称3：D010 contract 无 terminal authority，D011 terminal 5 唯一合法 → V007 PASS
- [x] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with（V007；`conflicts_with=[]`）
- [x] 已确认当前范围未违反“明确不含”（V007）

## 下一轮

专题保持 dormant。科学重开须先取得 H006“已知债务”中的 source config/action-before inputs，并显式记录 scope change；在此之前不得恢复 performance grid、diagnostic structural run、MVE 或下游阶段。
