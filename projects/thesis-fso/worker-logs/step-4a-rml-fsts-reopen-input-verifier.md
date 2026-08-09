# RML-FSTS reopen-input independent verification

> 2026-08-09 | fresh-context read-only verification | authority: T022

## Verdict

**PASS。P0/P1/P2=`0/0/0`。**

本 PASS 只表示 D012 blocker-recovery Probe 的候选终态与证据边界可被独立接收：SC1 与 AB1 均未闭合，唯一 recovery terminal 为 `REOPEN_INPUTS_NOT_CLOSED`。它不表示 Q1 scientific success、performance correctness、novelty closure、Go/Kill/Resolved 或方法成立。D011/V007 的 scientific terminal `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED` 保持唯一有效。

## Control and scope

- task-control command：`python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions/2026-08-08-rml-fsts-groundwork/T022-step4a-reopen-input-independent-verifier.md --repo-root D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- result：`PASS`；binding=`epoch 37 / CP024 / NEW_TOPIC_RECOVERY`。该 PASS 只证明授权一致。
- Session Start：当前 topic 原始目标是验证 fixed-lag/`B_L` condition-dependence 能否经完整 Groundwork 成为 Ch4 方法入口；当前 scope 只允许 D012 source-config/action-before recovery。依赖 `2026-08-08-ch4-reference-method-extension` 为稳定 dormant，`conflicts_with=[]`；本专题 S 文件数为 5，未触发 inflation warning。
- RDL recovery route：本任务不创建、比较、晋级或写作方法；它只核验下一次合法 B0/B1/B2/O1 比较所需的输入是否恢复。两项输入均未闭合，故必须停止而不能转入 repair/grid/MVE。
- sim-preflight 阶段边界：当前属于 Groundwork，不进入 Execute 场景；未运行 estimator、performance grid、diagnostic structural run、C1 或 MVE，未修改 `common/`、`params.py`、合同、owner、receipt、论文或 protected logs。
- verifier 唯一写入本文件；未联网、未扩检索、未 commit、未 push。

## SC1 verification

### 有界检索面与声称边界

T020 ledger 明确覆盖三类独立 surface：publisher/DOI metadata、author identity/institutional、code/data repository，并在前两类只得到正文/身份、第三类完成后止损（`step-4a-rml-fsts-public-source-config-recovery.md:13-32`）。其 verdict 明确只是 bounded public-source exhaustion，不是全互联网不存在断言（同文件 `:5-9`）。未发现把零结果扩大成全称声称。

### Exact identity 与 canonical artifact

- fresh 全文核对：canonical IEEE HTML 顶部 PDF/document link 的 arnumber=`10097873`，期刊 issue link 的 isnumber=`10101698`，article sequence=`7302313`，DOI=`10.1109/JPHOT.2023.3265847`（shared canonical `content.md:11-13,65-73`）。因此 T020 的身份纠正成立，且不构成 executable config recovery（worker log `:94`）。
- fresh SHA-256/bytes：
  - `content.md`=`e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f` / `55349` bytes；
  - `metadata.json`=`b9236f0ff4fece29bf6b6df3358b8eb29e5e781d8f99e86556a0075cb123dce0` / `514` bytes。
  两项均与 T020 artifact ledger 一致（worker log `:35-49,104-113`）。
- canonical 目录 fresh listing 只有 `content.md`、`metadata.json`，没有 `source.pdf`、code、dataset 或 supplement。未要求 executor 伪造不存在的下载物。

### SC1 1–7 字段独立复核

| # | 字段 | fresh verdict | 一手本地证据与缺口 |
|---:|---|---|---|
| 1 | wavelength / input field / beam geometry | `NOT_FOUND` | Wang 仅给 Tx ECL linewidth/DP-IQ chain；全文未给 wavelength、waist、curvature、input complex field。 |
| 2 | phase-screen executable config | `RELATED_ONLY` | Wang 只给 Fourier phase-screen、10 km、`C_n^2` 两档及 inner/outer-scale 极限（canonical `:231-243`）；screen/grid/spacing/normalization/subharmonics/propagator均缺。 |
| 3 | aperture / SMF / branch lifecycle | `RELATED_ONLY` | 0.2 m aperture、SMF coupling、独立 branches与两档 mean coupling可确认（canonical `:241-243`）；mode overlap、joint law/covariance与 reset/continuity lifecycle均缺。 |
| 4 | received-power reference/accounting | `RELATED_ONLY` | Eq. (3)–(4)与图文使用 received/average optical power，但未定义 telescope/coupling 前后、per-pol/per-branch/total/MRC reference plane。 |
| 5 | coherent receiver noise terms | `RELATED_ONLY` | BPD、LO 15 dBm、responsivity 0.8 A/W、shot/thermal considered 可确认（canonical `:243`）；hybrid/TIA/temperature/load/background/dark/PSD/variance均缺。 |
| 6 | NEB/filter/sample/ADC convention | `RELATED_ONLY` | 10 GBaud、one sample/symbol推导与 ADC 存在可确认；NEB、filter/matched pulse、integration、ADC scale/bits/quantization均缺。 |
| 7 | unique `P_rx[dBm] -> E[|w[k]|^2]` | `NOT_FOUND` | Eq. (3)–(4)只把接收噪声记作 Gaussian `N_x,N_y`，第 5–6 项缺参使数值映射不唯一。 |

因此 `EXACT_CLOSED=0/7`。一般公式、相似平台、典型 1550 nm、moment-matched scalar GG、图像恢复或只给 mean coupling 均未被计为 exact closure。SC1 verdict=`SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED` 可接收。

## AB1 verification

### Wang structural causality 与 caller absence

- canonical 全文独立重读确认：`B_N/B_L` 先定义发端双偏振 FSTS block/symbol arrangement（`:103-107`），Eq. (7)–(11)才在接收端用相同结构做 coarse/fine FOE（`:183-215`）；simulation platform 又明确训练符号由 PRBS 生成、经 DAC/DP-IQ 调制后发入 channel（`:231-243`）。故 joint `(B_N,B_L)` 必须在 transmitter FSTS construction 前冻结。
- 对 `feedback|ACK|RSSI|common probe|previous-frame|frame cadence|action signaling|reconfiguration|receiver-power estimator` 的 fresh local grep 为 0 命中。正文 `:208,219` 的 buffer/periodic update只复用 receiver-side coarse CFO，不提供 transmitter structural-action feedback、previous-frame power caller或 lifecycle。
- Wang 仅称 `phi/eta/I` 相对 GHz symbol rate slow-varying（`:160`），不能补成跨帧 time-series、feedback freshness或 action-before observation。

### 两个选项

| 必需项 | previous-frame | common-probe | verifier conclusion |
|---|---|---|---|
| causal ordering | 可写 next-frame skeleton | 可写 probe-before-FSTS skeleton | 仅概念顺序，不等于 executable caller |
| action-invariant observation | 未定义固定 measurement region、reference与 normalization | probe原则上可不变，但 waveform/length/estimator未定义 | 任一缺失即不得 PASS |
| time-series/cadence | 无 frame cadence、trajectory、reset/continuity | 无 probe→selected-FSTS target trajectory | `NOT_CLOSED` |
| feedback/ACK/signaling | 无 caller、timestamp、CRC、ACK、reconfiguration | 同左 | `NOT_CLOSED` |
| latency/freshness | 无 processing/RTT与可执行 `T_valid` | 同左 | `NOT_CLOSED` |
| state/fallback | B1 fallback只能写规范草案，不能触发 | 同左 | `NOT_EXECUTABLE` |
| overhead | 缺 frame/control bit/latency参数 | 另缺 probe length/payload/duty-cycle | `NOT_CLOSED` |
| paired unit | 无 source-backed cross-frame latent trajectory | 无 probe/FSTS joint trajectory | 只能保留 conceptual contract |

### 相邻一手边界

- Valjus/sat.1553 `content.md:167` 给 atmospheric scintillation/pointing coherence通常 `>1 ms`，但同段明确不建模 coherence time而采用 quasi-static channel；只能支持短窗口慢变，不提供本系统跨帧 feedback freshness。
- WiSEE 2024 `content.md:50,92` 的 32768 symbols@32 GBd约 `1 us`、DSP overhead约 `7.75%`，只据 few-kHz scintillation声明**单 frame 内**静态；没有 receiver-to-transmitter structural-action feedback。
- JLT 2023 `content.md:155-171` 明确 earlier-frame CSI受 processing delay+round-trip约束；ground-to-ground强湍流边界约 10 km，LEO Greenwood time约 4 ms/最大约 60 km，并判 receiver-directed adaptive loading不适合该 satellite application。该文证明 feedback边界必须实算，不能被扩大为本系统现成协议。

### Provenance

T021 log 在首行明确：parent executor超出止损被中断；fresh child完成 Wang 455-line全文精读；最终 worker log由主控基于 delegated read和本地 primary line checks合成，且自称“not an independent verification”（`step-4a-rml-fsts-action-before-protocol.md:3`）。本 T022 已从 fresh context重读 Wang全文与三份相邻一手证据；未把该 master-synthesized log当作独立验证本身。

结论：两方案均有任一以上关键项缺失，frozen primary=`NONE`，applicable semantic tests PASS=`0`（worker log `:72-88,156-166`）；AB1=`AB1_NOT_CLOSED` 可接收。

## Reducer and scientific-terminal audit

- D012 reducer 唯一且 fail-closed：SC1 与 AB1 任一未闭合即 `REOPEN_INPUTS_NOT_CLOSED`；明示不存在“部分闭合先跑 diagnostic”出口（`decisions.md:445-452`）。本次两者都未闭合。
- D013 只关闭 recovery Probe：candidate=`REOPEN_INPUTS_NOT_CLOSED / PENDING_INDEPENDENT_VERIFICATION`；不取代 D011/V007 scientific terminal（`decisions.md:471-510`）。
- scientific disposition fresh parse：Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、contribution=`NONE`、object/package failure=`0/0`。
- execution fresh parse：grid=`NOT_RUN`、diagnostic=`NOT_RUN_TERMINAL_DISABLED`、MVE=`NOT_RUN`、scientific raw rows=`0`、paired delta/CI=`N/A (NOT_RUN)`；B0/B1/B2/O1/C1均=`N/A (NOT_RUN)`。
- ranking crossover与conditioned-lookup absorption均=`NOT_EVALUATED`；没有 residual/observability/actionability、Go/Kill/Resolved 或 C1 推断。
- strongest cheap comparator仍为 dev-frozen `(modulation, TS length, receiver-power bin) -> single structural lag/B_L` lookup（topic-index `:43`；literature owner `:38,89,161`）；未包装成方法。

## Owner/artifact/hash audit

### Owner/current-view consistency

topic-index `:15,53,70-81`、literature owner `:5,15,163-177`、master-state `:38-57`、registry current entry、D013、S005 `:3,31,43,51-54` 与 reopen receipt均一致写为：recovery pending V008、SC1/AB1未闭合、scientific terminal保持、全部 performance NOT_RUN。没有 owner提前写 V008 PASS。原 terminal receipt fresh parse仍为 `VERIFIED / D011_V007 / STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，且 `git status --short -- <terminal-receipt>`为空，未被改写。

### Hash/parse/path

- recovery logs fresh SHA-256 2/2与 candidate receipt一致：
  - source-config=`44b0d098b3ae0debf02dd85c34ca612008fbba1f60aff02d10652c554451ed87`；
  - action-before=`57c07b80cde22c2f66b02235a63cfb8e91fc130ee0514b02da18aaa4ff80196d`。
- original terminal receipt与 candidate reopen receipt均 fresh JSON parse PASS；`.sessions/_registry.yaml` fresh YAML parse PASS。
- candidate receipt中的两份 evidence log、原 terminal receipt均存在；V008 verifier path在本文件写入后存在。receipt reducer、authority、NOT_RUN数字与 owners逐项一致。

### Git/scope/protected logs

- pre-write HEAD=`4fd6d348b9eda09ecaa022d274cc2eddd5d5f763`，branch=`codex/rdl-method-production-v2`；staged diff为空；branch无 upstream。`git diff --check` exit 0。
- tracked changed names仅 D012/D013 recovery owners：decisions/topic/voice/registry/literature/master；untracked任务资产仅 S005、T020–T022、candidate receipt与两份 recovery logs，另含四个既有 protected logs。无 `common/`、`params.py`、旧 campaign代码、正式论文或原 terminal receipt diff。
- 四个既有 untracked/unstaged protected logs fresh `(bytes, SHA-256, mtime +08:00)`：
  - `p05_run.log`: `641`, `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`, `2026-07-30 21:53:16`；
  - `p05_run2.log`: `2417`, `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`, `2026-07-30 22:08:08`；
  - `p05_run3.log`: `929`, `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`, `2026-07-30 22:21:41`；
  - `p05_run4.log`: `1430`, `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`, `2026-07-30 22:39:58`。

## Findings by severity

- **P0: 0。** 无错误恢复、terminal authority覆盖、performance/方法声称冒充或下游越权。
- **P1: 0。** SC1/AB1证据边界、reducer、owner/receipt、hash/path与protected scope均闭合。
- **P2: 0。** `PENDING V008` 是 verifier 写入前的正确候选状态；T021 provenance已显式降级并由本轮 fresh read独立复核，不构成遗漏。

## Final gate matrix

| Gate | Result | Evidence replay | Accepted conclusion |
|---|---|---|---|
| G1 SC1 source-config | `PASS` | 三类 surface ledger+止损边界；canonical identity/hash；字段1–7独立全文复核=`0/7` exact | `SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`；非全网不存在、非 executable recovery |
| G2 AB1 causal/executable protocol | `PASS` | Wang structural pre-TX action；caller关键词0命中；previous-frame/common-probe逐项缺口；Valjus/WiSEE/JLT边界；provenance复核 | `AB1_NOT_CLOSED`；primary=`NONE`，tests PASS=`0` |
| G3 reducer/scientific terminal | `PASS` | D012 fail-closed reducer；D013/receipt；D011/V007 terminal；NOT_RUN/0/0/cheap comparator | recovery=`REOPEN_INPUTS_NOT_CLOSED`；scientific terminal不变 |
| G4 owner/artifact/mechanical | `PASS` | owners pending一致；2/2 recovery hash；JSON/YAML/path；original receipt clean；protected logs 4/4；diff/staging/scope audit | recovery terminal/artifact可独立接收；verifier无越权写入 |

## Conclusion

**PASS，P0/P1/P2=`0/0/0`。** 接收 D013 recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`：SC1=`SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`，AB1=`AB1_NOT_CLOSED`。D011/V007 scientific terminal `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`、Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献=`NONE`、failure=`0/0` 与所有 `N/A (NOT_RUN)` 数字继续有效。

下一合法动作仍需外部新增输入：同一 executable phase-screen/SMF/receiver-noise source backend，以及可执行 feedback/time-series testbed；联系作者或提交外部请求必须另获用户授权。在此之前不得运行 performance grid、diagnostic structural run、bounded MVE、C1、Contract、Execute 或论文写作。
