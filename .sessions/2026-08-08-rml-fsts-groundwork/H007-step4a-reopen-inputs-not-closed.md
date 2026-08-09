# Handoff: RML-FSTS Step 4a 重开输入未闭合

> 来源: S005 / D013 / V008 | 交接目标: 仅在两类外部 executable input 同时新增后再 scope-change
> 文件名: H007-step4a-reopen-inputs-not-closed.md
> 日期: 2026-08-09

## 已完成边界

D012 的有界 blocker-recovery Probe 已完成。T020 对 publisher/DOI、author/institutional、code/data repository 三类 surface 止损后，SC1 fields 1–7 exact-closed=`0/7`；T021 对 previous-frame/common-probe 的因果审计均未得到 executable caller path。D013 reducer=`REOPEN_INPUTS_NOT_CLOSED`，V008 fresh-context 独立终验=`PASS, P0/P1/P2=0/0/0`。

这不取代 D011/V007 的 scientific terminal：Groundwork Step 4a 仍为 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`、object/package failure=`0/0`。performance grid、diagnostic structural run、bounded MVE 均未运行；scientific raw rows=`0`，B0/B1/B2/O1/C1与paired delta/CI均为 `N/A (NOT_RUN)`。

## 不要做什么

- 不把 public-source exhaustion 写成“材料不存在”，不以典型 1550 nm、一般 phase-screen、scalar Gamma-Gamma或结果拟合补 SC1。
- 不用当前 action-specific FSTS、truth power/SNR/`h`/turbulence label、per-action outcome决定当前 structural action。
- 不把 previous-frame/common-probe 纸面顺序当 executable protocol，不假设零反馈时延或用 generic `>1 ms` 自动证明 freshness。
- 不运行/恢复 T014、performance grid、diagnostic structural run、C1或MVE；不发 ranking/no-crossover、B2-absorbed、Go/Kill/Resolved 推断。
- 不把 conditioned single-lag lookup包装成方法；不进入 Step 5、Contract、Execute或论文写作。
- 不修改 `common/`、`params.py`、原 terminal receipt、旧 campaign或四个 `p05_run*.log`；不 push。

## 必读

1. `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md`（D011–D013）
2. `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md`（V007–V008）
3. `.sessions/2026-08-08-rml-fsts-groundwork/S005-step4a-reopen-input-recovery.md`
4. `.sessions/2026-08-08-rml-fsts-groundwork/T022-step4a-reopen-input-independent-verifier.md`
5. `projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-reopen-input-receipt.json`
6. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-public-source-config-recovery.md`
7. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-action-before-protocol.md`
8. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-reopen-input-verifier.md`

## 接口变更

```yaml
contracts:
  - id: RML-FSTS-STEP4A-C003
    type: evidence-recovery-receipt
    description: "Machine-readable blocker-recovery terminal; no scientific performance authority"
    location: "projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-reopen-input-receipt.json"
    change: "status=VERIFIED; recovery_terminal=REOPEN_INPUTS_NOT_CLOSED; recovery_authority=D013_V008"
    consumed_by: "topic/literature/master/registry current views"
    verification_result: PASS
    verified_by: V008
  - id: RML-FSTS-STEP4A-C004
    type: future-input-contract
    description: "Scientific reopen remains fail-closed on two simultaneous executable inputs"
    location: ".sessions/2026-08-08-rml-fsts-groundwork/decisions.md#D013"
    change: "Requires exact source backend plus feedback/time-series testbed; no partial diagnostic escape"
    consumed_by: "any future scope-change request"
    verification_result: PASS
    verified_by: V008
```

## 失败数据附录

### SC1

- Verdict：`SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`。
- Exact identity：IEEE document/arnumber=`10097873`；`10101698` 是 issue/media id；article sequence=`7302313`。
- Exact executable config fields=`0/7`。仍缺 wavelength/beam、phase-screen screens/grid/propagator、SMF overlap/joint lifecycle、received-power reference plane、BPD/TIA/NEB/filter/ADC 与唯一 `P_rx[dBm] -> E[|w[k]|^2]`。
- B0 consequence：`NOT_EXECUTABLE`；不是 B0 performance FAIL。

### AB1

- Verdict：`AB1_NOT_CLOSED`；frozen primary=`NONE`；applicable semantic tests PASS=`0`。
- Previous-frame缺 action-invariant measurement、frame cadence/time-series、feedback/freshness/cost；common-probe另缺 probe waveform/length/MDE，并同样缺 feedback/lifecycle/overhead。
- Wang只给 intra-frame structural FSTS；Valjus/WiSEE只支持短窗口慢变。JLT 2023直接表明 earlier-frame CSI受 processing+RTT/Greenwood边界约束，不能补成本系统协议。

### Scientific execution

- grid=`NOT_RUN`；diagnostic=`NOT_RUN_TERMINAL_DISABLED`；MVE=`NOT_RUN`；scientific raw rows=`0`。
- B0/B1/B2/O1/C1=`N/A (NOT_RUN)`；paired delta/CI=`N/A (NOT_RUN)`。
- ranking crossover=`NOT_EVALUATED`；conditioned lookup absorption=`NOT_EVALUATED`。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| executable source config | B0/source transfer须同一链可复现 | public recovery 0/7 exact closed | 作者/source backend给出 phase-screen/SMF与receiver-noise完整配置/代码/hash |
| action-before protocol | runtime action须因果、可观察、可审计 | previous-frame/common-probe均无caller | 可执行 feedback/time-series testbed给 observation、cadence、latency/freshness、overhead、state与B1 fallback |
| SSRN 6293357全文 | 不以缺全文声称novelty closure | 高风险债继续保留 | 取得qualified fulltext并完成action-level read |
| Wang figures/PDF | source numeric anchor须有轴/点 | direct figures 403 | 取得canonical PDF/原图；但单独恢复不解锁testbed |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| SC1 closure | exact source chain fields 1–7全闭合且无需典型值/拟合 | D012 | FAIL（0/1；0/7 fields） |
| AB1 closure | causal observation、feedback、freshness/state、overhead、fallback、caller与tests全闭合 | D012 | FAIL（0/1；tests 0 PASS） |
| Recovery reducer | 任一输入未闭合即唯一 `REOPEN_INPUTS_NOT_CLOSED` | D012-D013 | PASS（1/1） |
| Scientific boundary | D011 terminal不变；所有performance数字NOT_RUN；无Go/Kill/Resolved | D011/V007/V008 | PASS（2/2） |
| Mechanical integrity | log hashes、JSON/YAML/path、original receipt、protected logs与scope均一致 | T022/V008 | PASS（1/1） |

## 接收方验证（续接对话时必须完成）

- [x] 已读取 topic-index 的不变量段落（V008）
- [x] 已验证本文件中的至少 3 条关键事实声称
  - [x] 声称1：SC1 exact fields=`0/7`且bounded search非全称不存在 → V008 G1 PASS
  - [x] 声称2：previous-frame/common-probe均无executable caller path → V008 G2 PASS
  - [x] 声称3：recovery terminal不取代D011 scientific terminal，全部performance仍NOT_RUN → V008 G3 PASS
- [x] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with（V008；`conflicts_with=[]`）
- [x] 已确认当前范围未违反“明确不含”（V008）

## 下一轮

专题保持 dormant。只有外部新增输入同时满足 source backend与feedback/time-series testbed两门，才可显式 scope-change并重冻结 semantic-smoke 合同；单独补一门、恢复图像或纸面协议均不解锁性能执行。若要联系作者、发送邮件或提交外部请求，须用户另行明确授权。
