# Verifications — Coded decoder-feedback 方法主线 Groundwork

## V001: Step 1 terminal package 技术终验（语义映射待修）

> date: 2026-08-09
> 关联：S001 / D003–D004 / CP003–CP004 / T007–T010

### 验证项

- [x] 技术证据与 corpus：[由 fresh-context `/root/authority_terminal_verifier` 重跑 A/B] → mirror 28/28，93 raw→66 unique，50/66 published，must-read=6，sources=7，C1/C2 exact collision，replacement=0，P0/P1/P2=`0/0/0`
- [x] Git 与保护边界：[动态读取 HEAD receipt 和 HEAD T022，再与 fresh 文件比较] → `p05_run*.log` bytes/SHA 4/4 一致且一直 untracked/unstaged，无 forbidden scientific artifact 变更
- [ ] canonical problem 映射：[staged diff 独立审查对照 `stages/glossary.md` 与 `stages/gw-search.md`] → D003 的 `NO_VALID_PROBLEM` 未经 Step 3 M-C-A Q#，属于越级映射；已由 D004 修正，尚待 T011 fresh verification
- [ ] 治理收口：[检查 current owner、task snapshot、handoff checklist 与 V-template] → T009/H001/V001/report 已进入修复，尚待 T011 验证和 V002 接收

### 证据

`projects/thesis-fso/worker-logs/step-056-coded-decoder-authority-terminal-verification.md` 原始摘录：

```text
计数：P0=0 / P1=0 / P2=0。
四组 fresh-context 冻结检查均为 PASS。
integrated v2 输入为 8 个 C1 route、8 个 C2 route、1 个 reviewed mirror；raw=93、records=66
fresh 复算 published=50、must-read=6、sources=7、R2 C1/C2=2/2。
authority_result=HEAD_RECEIPT_T022_FRESH_MATCH_4_OF_4
```

同一日志暴露、后由 staged review 判为越级的原始接受行：

```text
terminal/canonical/adapter=STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM / false
```

D004 修正后的机器投影 fresh 读取：

```text
schema_version=coded-decoder-step1-integrated.v2.1
terminal=STEP1_NO_METHOD_ACTION_SURVIVOR
framework_disposition=STEP1_CANDIDATE_SET_EXHAUSTED
canonical_mapping=null
problem_disposition=NOT_EVALUATED_NO_Q_FORMED
```

验证链保留：T007/step-053=`FAIL 0/2/1` → T008/step-054 repair → T009/step-055=`FAIL 0/1/0`（`INVALID_TASK_CONTRACT`）→ T010/step-056 技术检查=`PASS 0/0/0`。T010 总耗时 `00:04:23.396`，小于 8 分钟。

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

已由 T011/V002 完成：D004 的语义层级、integrated v2.1、current owner 投影、T009 派发快照、H001 checklist、V001 模板以及保护边界均通过 fresh verification。V001 保持 PARTIAL 作为历史验证记录，不再单独支持终态关闭。

## V002: D004 语义/治理修正终验

> date: 2026-08-09
> 关联：S001 / D004 / CP004–CP005 / T011

### 验证项

- [x] Artifact 与定量收据：[fresh 解析 integrated v2.1 与 reviewed mirror，并独立复算] → 93 raw→66 unique、50 published、6 must-read、7 sources、93/93 provenance、R2 C1/C2=`2/2`、mirror 28/28 与 8/10/4/2/4 全一致
- [x] 语义层级：[fresh 对照 `stages/glossary.md` 和 `stages/gw-search.md`] → local=`STEP1_NO_METHOD_ACTION_SURVIVOR`、framework=`STEP1_CANDIDATE_SET_EXHAUSTED`、`canonical_mapping=null`、problem=`NOT_EVALUATED_NO_Q_FORMED` 合法；current owner 无越级 verdict
- [x] 治理与历史边界：[检查 registry/topic/master/S001/D004/mission/V001/H001/report/JSON、T009 EOF 与 V-template] → current 投影一致，旧 mapping 仅在显式 historical/superseded 位置保留，T009 快照、H checklist、V001 PARTIAL、v1 supersession 均合规
- [x] Git 与保护边界：[动态读取 HEAD receipt/T022、fresh 比较四个 p05 日志并审计 staging/status] → HEAD 正确，bytes/SHA 4/4 MATCH，四文件一直 untracked/unstaged，无 forbidden artifact 或 staging 漂移
- [x] 执行隔离与时限：[比较执行前后 cached/status 并记录计时] → verifier 唯一写入 step-057；最终复查 `00:04:08.356`，小于 8 分钟

### 证据

`projects/thesis-fso/worker-logs/step-057-coded-decoder-semantic-governance-verification.md` 原始输出：

```text
P0=0 / P1=0 / P2=0
A/B/C/D：全部通过
schema_version=coded-decoder-step1-integrated.v2.1
terminal=STEP1_NO_METHOD_ACTION_SURVIVOR
framework_disposition=STEP1_CANDIDATE_SET_EXHAUSTED
canonical_mapping=null
problem_disposition=NOT_EVALUATED_NO_Q_FORMED
raw_rows=93; records=66; published=50; must-read=6; source families=7
provenance=93/93; mirror=28/28; replacement.accepted=0
HEAD=1d76f917a89c719614aeefd7a165ab9819425978
p05 HEAD receipt/T022/fresh=4/4 MATCH
elapsed=00:03:34.523; final recheck total=00:04:08.356
verdict=PASS
```

Fresh verifier：`/root/t011_semantic_verifier`。本轮未联网、未实验、未进入任何下游科学步骤，唯一仓库写入为 step-057。

### 结论

PASS

---

## V003: Step 3.5 完整链、检索 receipts 与物理边界独立验收

> date: 2026-08-10
> 关联：S001 / D009 / T036–T037

### 验证项

- [x] 完整链语义：[fresh-context verifier 独立抽核 6 篇本地全文并逐篇复建八字段] → bounded slice 内未确认 exact complete chain；OFC2017/2604/1704 三个高风险语义均与中央报告一致，P0/P1/P2=`0/0/0`
- [x] 未决全文与 Q1 上限：[核查 CSSC/CS-DC/U01/U02 metadata/content 状态及 Q1 措辞] → 全部正确 fail-closed；occurrence/observability/recoverability 保持 UNKNOWN，无 novelty/Step4a 事实越级
- [x] 检索充分性：[独立复算 R1 query matrix、双向引用链与 R2/R3 JSON] → R1=`70→63, 2/5`；citation=`58F/21B, 12 abstracts, 0/1`；R2=`101→97→91, 0/2`；R3=`82→79→72, 0/1`
- [x] Round 3 债务与终态：[按 DOI/arXiv/title 复核唯一新增 OFC2017 及全文] → `ROUND3_CAP_REACHED_WITH_NEW` 正确，唯一 SHOULD 已 `CLOSED_NO_EXACT / STRONG_NEIGHBOR`，没有第 4 轮
- [x] Physical/B2 transfer：[抽核 OFC2014、ICTON、PAPU、JLT2020 本地全文] → slip-rate/PCS、0.78%/per127/filter、FSO/AO/CFO/5dB/2.3dB 数字一致；JLT fading 未被误写为 slip 因果
- [x] 控制与保护：[fresh parse、topic/master/literature 状态、p05 SHA 与 Git staging] → 关键 JSON 6/6 parse；验证时仍 CP009/Step4a forbidden；p05 4/4 MATCH；staging=0

### 证据

`projects/thesis-fso/worker-logs/step-082-c1-step3_5-collision-verifier.md` 原始终态：

```text
verdict=PASS
P0=0 / P1=0 / P2=0
FULLTEXT_SPOTCHECK_COUNT=6
NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE
p05 SHA 4/4 MATCH
staging=0
```

同一 verifier 的三个承重语义核验：

```text
OFC2017 soft decision = pilot state probability; no decision feedback
2604 burst = Gilbert–Elliott Markov-modulated Wiener innovation variance; not discrete slip
1704 window = SC-LDPC code-graph decoding wave; not detected-slip local window
Q1 occurrence/observability/recoverability = UNKNOWN
```

`projects/thesis-fso/worker-logs/step-083-c1-step3_5-receipt-verifier.md` 原始复算：

```text
R1: 48 Crossref + 22 arXiv = 70; 70-7=63; MUST/SHOULD=2/5
citation: forward=58 (abstract=11); backward=21 (abstract=1); screened=12; new=0/1
R2: 80 Crossref + 20 arXiv + 1 S2 = 101; unique=97; metadata-new=91; new=0/2
R3: 80 Crossref + 2 arXiv = 82; unique=79; metadata-new=72; new=0/1
verdict=PASS; P0=0; P1=0; P2=0
JSON parse=6/6; p05=4/4 MATCH; staging=0
```

Physical transfer 原始接受边界：

```text
OFC2014: pre-FEC BER>1e-2 region slip rate>1e-3; synthetic slip=0.1*pre-FEC BER; pilots=1/2/3%
ICTON2016: synthetic P_CS=1e-3, sweep 2/3/4e-3
PAPU: pilot overhead=0.78%; one per 127 symbols; filters={4,8,16,20,32,48}
JLT2020: fading critical-SNR shift≈5dB; BER=1e-4 penalty=2.3dB; turbulent phase-noise effect after AO=negligible
transfer ceiling: these do not prove coherent-FSO turbulence causes discrete cycle slips
```

Fresh verifiers：`/root/step35_collision_verifier` 与 `/root/step35_receipt_verifier`。两者唯一仓库写入分别为 step-082 与 step-083；均未联网、实验、提交或修改中央 owner。

### 结论

PASS

---

## V004: A0 数值合同与 D0 进入边界独立验收

> date: 2026-08-10
> 关联：S001 / D010 / T042–T045 / CP010–CP011

### 验证项

- [x] A0 全量合同：[step-090 fresh-context 审查理论/mapping/physical/truth/B2/four strata/statistics/budget/authorization] → B2 source contract、controlled exposure、strata 合取、symmetry、truth boundary 与 7.00 日预算均 CLOSED；残余计数为 P0/P1/P2=`0/2/1`
- [x] 残余 finding：[step-091 只复核 bootstrap/invalid replicate、S3 fusion 与 post-D0 safety 边界] → P1-1/P1-2/P2-1 全部 CLOSED，P0/P1/P2=`0/0/0`
- [x] 复刻性：[fresh YAML parse + 定向机器断言 + owner 初末 SHA] → 10,000-replicate PCG64 bootstrap、NA/9500/0.05 terminals、equal-cell macro、dev-only lexicographic fusion 与唯一 lambda 均可唯一执行
- [x] 授权边界：[对照 report/YAML/topic control] → step-091 PASS 本身未授权 D0；D010/CP011 只开放 D0，不开放 adapter、C1-ext、MVE、held-out 或论文声称
- [x] 保护边界：[检查 staging 与四个 p05 SHA] → staging empty；p05 4/4 MATCH；step-091 唯一 verifier 写入

### 证据

`projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md` 原始终态：

```text
PASS；P0/P1/P2=0/0/0
P1-1 — CLOSED
P1-2 — CLOSED
P2-1 — CLOSED
YAML yaml.safe_load: PASS
定向机器断言: 10/10 PASS
owner 开始/结束 SHA: 2/2 MATCH
p05 protected logs: 4/4 MATCH
staging: empty
D0_EXECUTION_AUTHORIZED=NO（治理转移前）
```

经验证的科学 owner 快照：

```text
step4a-a0-preflight.md SHA256=046bb45a95bde5672270a552828e2a5730987b48ac681c5fcad86f44b8755f27
d0-defect-smoke-contract.yaml SHA256=6c1e228f892ac1981fd22d7c7e89e0247df5c2cece9a69798e4387da2b003a4b
step-091 SHA256=13cd7e9c440e7b556d40fc78916f4f347eff7cca83e627bbcd3221e161b132df
```

step-090 保留为失败历史：`FAIL / P0/P1/P2=0/2/1`；不得用 step-091 覆盖其审计轨迹。D010/CP011 仅把上述已验证 scientific snapshot 的 control metadata 改为 D0 authorized，未改变 strata、阈值或 estimand。

### 结论

PASS

---

## V005: D0 v3 资产合同与 dev-freeze 闭合验收

> date: 2026-08-10
> 关联：S001 / D011 / T048–T057 / CP011–CP012

### 验证项

- [x] 失败血缘：[完整读取 step-101] → v2 明确保留 `FAIL / P0/P1/P2=0/2/0`；P1-1 为 HMM clean/controlled likelihood 权重不唯一，P1-2 为 BPS/B2 dev-freeze 缺具名 typed artifact；不是 scientific terminal
- [x] additive repair：[完整读取 step-102 与 v3 owner] → 只增加 typed artifact/estimand/chronology closure，不重开 population、seed、threshold、gate、baseline、strata 合取或 7 日预算
- [x] fresh reverification：[step-103 duplicate-key parse、hash、确定性算术、静态语义复核] → `PASS / P0/P1/P2=0/0/0`，P1-1/P1-2 均 CLOSED，定向静态断言 `94/94 PASS`
- [x] scientific no-drift：[step-103 按 family 对照 step-096/098/099/100/A0] → 抽核范围内 `SCIENTIFIC_FIELD_DRIFT=NONE_FOUND`；D0 仍 `NOT_RUN`，method signal 仍 `NONE`
- [x] 预算边界：[对照 logical/materialized/HMM 双账与 12 分钟门] → `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`，`>7D_HARD_BLOCKER=NOT_ESTABLISHED`；静态验收不冒充运行时预算 PASS
- [x] 保护边界：[step-103 初末检查] → p05 `4/4 MATCH`，staging=`0`，verifier 唯一写入为 step-103；未运行 D0/pytest/benchmark/science
- [x] 授权边界：[对照 step-103 terminal 与 D011] → verifier 只允许治理转交；D011/CP012 只开放 implementation/unit/non-scientific benchmark，`DEFECT_SMOKE`/S1–S4 仍关闭
- [x] CP012 owner 投影：[fresh parse control] → implementation/unit/engineering-benchmark/execution/science=`true/true/true/false/false`；status=`verified_frozen_for_d0_implementation_and_unit_test`

### 证据

```text
v3 pre-transfer owner SHA256=6924842c5696e80bcf8efa24bc63f005d7a78ba63f959c768e0183de85c81f54
asset report pre-transfer SHA256=e008c0f0b78772a80201d4969359ed34d655d79ed37614652746e911ebbc01f1
step-101 SHA256=d103a17dda0fbbe1c86c8b073e614bef36fee7ec4cfc008d6c164472f5cb0d20
step-102 SHA256=077d0b9337769a7185e665e8d05f4b448e6efb9cb5cdc179e90e2107a94a1a76
step-103 SHA256=6ad845f009a64c0a5d93671bf98354a17a1dd83cf3882aecaa43f5e7f73a5ab9
```

step-103 终态为 `ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER`，并明确 `IMPLEMENTATION_UNIT_BENCHMARK_SCIENCE_AUTHORIZED_BY_THIS_VERIFIER=NO`。上述 owner/report SHA 是 CP012 control metadata 写入前的接收快照；治理投影变更不得解释为 scientific-field 变更。

### 结论

PASS

验收上限：v3 可由 D011 限权进入实现、单测与后置非科学吞吐门；本验证不授权 `DEFECT_SMOKE`、S1–S4、adapter、MVE 或 held-out。

---

## V006: I06 T092 最终字节独立复验

> date: 2026-08-10
> 关联：S001 / D012 / D013 / T092–T093 / step-138–139

### 验证项

- [x] 最终字节 fresh tests：三个 exact 节点 `3/3`、contract+waveform `22/22`、codec `7/7`、schemas `10/10`、aggregate 4 文件 `39/39`；零 fail/error/skip/xfail/warning
- [x] step-137 已知缺口：旧 9 个 bad accepts 全部 `9/9 CLOSED`
- [ ] fresh robustness：73 例中 10 个错误接受，聚为 stored correctness 篡改、opaque mutable built-ins、physical-noise alias、NumPy integer root 四项 P1
- [x] 物理与 receiver 派生量：四组 physical equations/sharing/双偏振 C_pre 独立复算均通过
- [x] 保护：source/tests/governance 无 verifier 修改；HEAD、staging、cache、P05 与冻结 hash 无漂移

### 证据

`projects/thesis-fso/worker-logs/step-139-d0-i06-final-independent-reverification.md`

```text
VERDICT=FAIL
P0/P1/P2=0/4/0
fresh_cases=73
old_bad_accepts=9/9 CLOSED
new_bad_accepts=10
aggregate=39/39 passed
step-139 SHA256=959fe9bffaa795633fcd4e0f9a72d08025f5573d67d631158e6128baa6a937b0
```

### 结论

FAIL

---

## V007: I06 closed-world receiver/truth boundary 最终独立验收

> date: 2026-08-10
> 关联：S001 / D012 / D013 / T094–T097 / step-140–143

### 验证项

- [x] strict TDD：T094 四个 exact节点在旧 production 上真实 `4 failed`，RED receipt先于 production修改；作者最终 exact `4/4`、aggregate `43/43`
- [x] fresh final-byte pytest：T097 exact `4/4`、aggregate `43/43`，0 fail/error/skip/xfail/warning
- [x] 独立合同矩阵：126 cases，correctness/metadata/Receiver keys/root/payload-contract-C_pre 五类均含 reject与accept controls，`mismatch=0`
- [x] 数值与因果边界：四组×两偏振 C_pre=`8/8`；物理方程、sharing、codec→coded→Gray→waveform chain与Receiver receipt truth-free均 PASS
- [x] 静态与保护：无 sys.path/legacy/global RNG/finalizer token、channel无I/O；`git diff --check=0`；final hashes、HEAD、staging、cache、P05全部保持
- [x] 失败血缘：T095因平台过滤无日志；T096取得 pytest GREEN但合同矩阵/物理 receipt未在时间盒内闭合，step-142准确 `INCOMPLETE`；二者未被当作 PASS

### 证据

`projects/thesis-fso/worker-logs/step-143-d0-i06-fresh-final-verifier.md`

```text
VERDICT=PASS
P0/P1/P2=0/0/0
exact=4/4 passed
aggregate=43/43 passed
contract_cases=126 mismatch=0
C_pre=8/8
step-143 SHA256=1470d822ee3570fdeb85fdba58360a7635c403985f1a3ebf72748cb72c181c1e
```

### 结论

PASS

验收上限：I06 receiver/truth boundary 已闭合，可继续 I05 实现单测；本验证不授权 engineering benchmark、DEFECT_SMOKE、S1–S4、adapter 或 method execution。

---

## V008: I05 FULL authority T098 独立复验

> date: 2026-08-10
> 关联：S001 / D014 / T098–T099 / step-144–145

### 验证项

- [x] fresh tests：exact `3/3`、schemas `13/13`、aggregate `46/46`，0 fail/error/skip/xfail/warning
- [x] 正常路径：88 authority cases `mismatch=0`；partial-only、direct FULL constructor、owner/extent/plan/table/projection/digest drift均在新鲜对象路径fail closed
- [ ] authority独立性：object-returning cached compiler共享canonical实例；改变缓存实例后，factory+validator接受digest不一致对象
- [x] scope ceiling：raw FULL positive=`NOT_RUN`；HMM/member与consumer-ledger binding仍OPEN；未越级声称I05 READY
- [x] 保护：source/tests/owner/HEAD/staging/cache/P05均无verifier漂移

### 证据

`projects/thesis-fso/worker-logs/step-145-d0-i05-full-authority-independent-verification.md`

```text
VERDICT=FAIL
P0/P1/P2=0/1/0
normal_cases=88 mismatch=0
shared_cached_canonical_consistency=FAIL
step-145 SHA256=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
```

### 结论

FAIL

---

## V009: I05 FULL fresh authority graph 独立验收

> date: 2026-08-10
> 关联：S001 / D014 / T100–T101 / step-146–147

### 验证项

- [x] fresh tests：exact `2/2`、schemas `15/15`、aggregate `48/48`，全部`-W error`且0 fail/error/skip/xfail/warning
- [x] step-145重放：authority SHA/table/nested projection三层改变对象均被拒；10轮后续compile保持canonical与独立digest一致
- [x] output graph isolation：FIRST/MAX×两套plans，700对递归nonprimitive对象共享0；cache返回树递归primitive-only，不依赖cache_clear
- [x] authority controls：56 cases（5 accept/51 reject）`mismatch=0`
- [x] scope ceiling：raw FULL positive、HMM/member、consumer-ledger仍OPEN；未声称I05 READY
- [x] static/保护：object-returning cache=0；source/tests/owner/HEAD/staging/cache/P05无verifier漂移

### 证据

`projects/thesis-fso/worker-logs/step-147-d0-i05-fresh-authority-graph-reverification.md`

```text
VERDICT=PASS
P0/P1/P2=0/0/0
isolated_nonprimitive_pairs=700 shared=0
authority_cases=56 mismatch=0
step-147 SHA256=a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f
```

### 结论

PASS

验收上限：FULL authority seal已闭合；raw positive、HMM/member与consumer-ledger bindings仍须独立TDD/验证。

---

## V010: D015 owner canonical identity transfer 独立验收

> date: 2026-08-10
> 关联：S001 / D015 / D016 / T102–T105 / step-148–151

### 验证项

- [x] T103 author-side：prechange RED exit=23先于owner编辑；最终330 assertions、122+6 literals、3/3 roots、8/8 author goldens、6/6 counts、science drift none
- [x] T104操作失败诚实保留：Windows code 206在Python启动前发生，所有required checks NOT_RUN，step-150=`INCOMPLETE`，未用于裁决owner
- [x] T105 transport修正：verifier源码先落唯一step-151，再从fence经stdin送Python；无临时脚本或第三文件
- [x] T105 full checks：720 assertions、128/128 literals、3/3 roots、15/15 mutations、6/6 counts；projection/permission/指定2 anchors+2 aliases/protection全部PASS
- [ ] golden：8/10；S2/BPS logical IDs精确命中，但consumer-binding manifest roots因`binding_kind`未在owner inputs/projection冻结而不可独立复算
- [x] scope ceiling：未修改schemas/tests，未运行pytest/benchmark/science，未宣称I05 READY

### 证据

`projects/thesis-fso/worker-logs/step-151-d0-owner-canonical-identity-independent-verification-retry.md`

```text
VERDICT=FAIL
P0/P1/P2=0/2/0
assertions=720
literals=128/128 roots=3/3 goldens=8/10 mutations=15/15 counts=6/6
step-151 SHA256=c1b0f39ed0903735387d6d12aaf5963c6a400215da81fa649a4f0e9b9459e535
```

### 结论

FAIL

只开放D016 owner-only窄修；完整fresh verifier PASS前不得实施D015 schema bindings。

---

## V011: D015 owner canonical identity transfer 最终独立验收

> date: 2026-08-10
> 关联：S001 / D015 / D016 / T106–T107 / step-152–153

### 验证项

- [x] T106 strict RED：global+8 projections+2 golden inputs共11/11 authority位置缺失，exit=23，先于owner修改
- [x] repair exactness：11/11均为`LOGICAL_COMPUTATION_ID`；删除11行/11字段分别还原pre-repair raw/parsed owner
- [x] fresh independent full matrix：729 assertions、128/128 literals、3/3 roots、10/10 goldens、15/15 mutations、6/6 counts，mismatch=0
- [x] consumer manifests：S2/BPS builder只从owner保存inputs读取`binding_kind`，logical IDs与既有roots 2/2精确命中
- [x] drift/protection：旧owner整体投影、permission/science/count/grid-root、指定aliases、HEAD/staging/P05/cache/diff-check全部PASS
- [x] scope ceiling：只闭合D015 owner transfer；I05 raw positive与schema bindings仍OPEN，未运行pytest/benchmark/science

### 证据

`projects/thesis-fso/worker-logs/step-153-d0-owner-binding-kind-independent-reverification.md`

```text
VERDICT=OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED
P0/P1/P2=0/0/0
assertions=729 authority=11/11 literals=128/128 roots=3/3
goldens=10/10 mutations=15/15 counts=6/6 mismatch=0
owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
step-153 SHA256=39ded7d15e32bd43e625782b143406e45e8390ef451279d1c05ed239491b8443
```

### 结论

PASS

D015 owner transfer已闭合；允许进入I05 raw FULL positive oracle与HMM/member/consumer-ledger schema TDD。benchmark/science继续禁止。

---

## V012: D0 owner identity typed loader 独立验收

> date: 2026-08-10
> 关联：S001 / D015 / T108–T109 / step-154–155 / V007

### 验证项

- [x] strict RED：四个新增 public-loader nodes 在生产 API 缺失时 4/4 FAIL、exit=1，先于实现，stdout SHA=`56a07c407b8b...`
- [x] author GREEN：exact 4/4、16/16 owner mutations fail closed、contract+waveform 30/30；owner/schema/session/P05无漂移
- [x] fresh independent oracle：430 assertions、128 literals、3 roots、8 anchors；31/31 fresh mutations拒绝，wrong accept/reject=`0/0`
- [x] fresh pytest：exact 4/4、四文件全量52/52，0 fail/error/skip/xfail/warning
- [x] I06 additive regression：34 cases + 7 static，5 accept/29 reject、mismatch=0；D0Contract仍四字段，channel只接D0Contract
- [x] boundary：loader只在显式调用时I/O；integer anchors typed化而未放宽通用string-key freeze；未补猜ordinary phase/operation/kind
- [x] scope ceiling：I05 bindings仍OPEN；未运行benchmark/science/MVE

### 证据

`projects/thesis-fso/worker-logs/step-154-d0-owner-identity-typed-loader.md`

`projects/thesis-fso/worker-logs/step-155-d0-owner-identity-loader-independent-verification.md`

```text
VERDICT=OWNER_IDENTITY_TYPED_LOADER_INDEPENDENTLY_VERIFIED
P0/P1/P2=0/0/0
assertions=430 literals=128 roots=3 anchors=8 mutations=31/31
pytest_exact=4/4 pytest_full=52/52 I06_cases=34+7 mismatch=0
contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
step-155 SHA256=ce5edec6a9e8102bea6840abfff028bf8d36ca73d75e3dd9e6bab8078dfdfde9
```

### 结论

PASS

Typed loader结构与当前owner seal已接收，I06 additive regression重新封印。后续D017 owner identity completion将有意改变owner/identity seal，届时必须刷新并再次独立验证；本V不授权跳过该revalidation，也不开放benchmark/science。

---

## V013: D017 ordinary identity completion 独立验收

> date: 2026-08-10
> 关联：S001 / D017 / T110–T111 / step-156–157

### 验证项

- [x] pre-edit RED：41个D017 shape gaps，exit=23；旧128 literals、3 roots、10 goldens、6 counts与science/permission均不漂移
- [x] author gate：208 assertions、18/18 mutations、descriptors=`32/41/49`、ordinary/HMM=`7/1`、phase-operation signatures=8
- [x] fresh independent oracle：920 assertions，不读取author helper；58/58 mutations，wrong accept/reject=`0/0`
- [x] ordinary authority：bindings/logical IDs=`42,967/27,487`；S2 method、S3 split、B2 kind、S4 exact七项均唯一
- [x] HMM authority：logical/chunk roots=`22,800/263,520`；chunk reference独立于consumer-binding manifest
- [x] ledger/accounting：ledger identities=50,287、6/6 counts、10/10旧goldens，mismatch=0
- [x] drift/protection：owner/science/permission/grid/count/golden none；HEAD/staging/P05/cache/diff-check全过
- [x] scope ceiling：仅接收owner bytes；loader seal、I05 compiler/raw positive仍OPEN，未跑pytest/benchmark/science

### 证据

`projects/thesis-fso/worker-logs/step-156-d0-owner-ordinary-identity-completion.md`

`projects/thesis-fso/worker-logs/step-157-d0-owner-ordinary-identity-independent-verification.md`

```text
VERDICT=OWNER_ORDINARY_IDENTITY_COMPLETION_INDEPENDENTLY_VERIFIED
P0/P1/P2=0/0/0 assertions=920 mutations=58/58 goldens=10/10 counts=6/6 mismatch=0
owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
step-157 SHA256=bfab0aac3434a9aae22adb7b5e0d5e3963b2b5c534d3fb18ef85db7311057b78
```

### 结论

PASS

D017 final owner bytes已接收。下一步只允许刷新typed loader exact owner/identity seals并独立回归；完成前不得把新owner交给schema compiler。benchmark/science继续禁止。

---

## V014: D017 typed owner loader final-seal 独立复核

> date: 2026-08-10
> 关联：S001 / D017 / T112–T113 / step-158–159 / V007 / V013

### 验证项

- [x] source inverse proof：final owner/identity 两个 seal 各唯一替回旧值后精确命中 pre-contract SHA；D0Contract仍四字段、loader仅显式I/O、channel边界未漂移
- [x] fresh canonical oracle：1107 assertions；128/128 literals、3/3 roots、8/8 anchors、descriptors=`32/41/49`、8/8 signatures、S4=`7/7`
- [x] fresh mutations：48/48（40 YAML + 8 dataclass）全部拒绝，wrong accept/reject=`0/0`
- [x] I06 additive matrix：35 cases（6 legal / 29 illegal），mismatch=`0`
- [x] pytest：exact=`4/4`、mutation=`1/1`、显式四文件=`53/53`；0 fail/error/skip/xfail/warning
- [x] protection：HEAD/staging/P05/cache/frozen artifacts均无漂移；verifier只写step-159
- [x] scope ceiling：未运行benchmark/science/MVE；本V只开放final owner给schema identity compiler

### 证据

`projects/thesis-fso/worker-logs/step-158-d0-owner-identity-loader-seal-refresh.md`

`projects/thesis-fso/worker-logs/step-159-d0-owner-identity-loader-seal-independent-verification.md`

```text
VERDICT=D017_OWNER_IDENTITY_LOADER_SEAL_INDEPENDENTLY_VERIFIED
P0/P1/P2=0/0/0 assertions=1107 mutations=48/48 I06=35 mismatch=0
pytest=4+1+53 all_pass
step-159 SHA256=9821f06edf897412cac04ed8db69389b5ce20e7e4985120295f9d04fb701d762
```

### 结论

PASS

D017 final owner typed authority已可交给 additive schema identity compiler。I05 FULL/provenance/HMM/raw positive仍OPEN；benchmark/science继续禁止。

---

## V015: T114 ordinary identity compiler authority 验收

> date: 2026-08-10
> 关联：S001 / D018–D019 / T114–T115 / step-160–161

### 验证项

- [x] author TDD：RED 4/4真实失败；GREEN 4/4；counts=`42967/27487`、24/24 mutations、fresh sharing=0、旧四文件53/53
- [x] fresh verifier先核authority source而非复用author PASS
- [x] 可复现错误接受：同一owner/seals下等基数替换模块`CANDIDATES`，public build仍产生精确总数但包含1080个未授权candidate identities；同一global下public assert接受
- [x] 同类静态缺口：aliases、B/Nw、S2-off method来自代码globals/literals而非authenticated owner view
- [x] hard-stop：首个P1后未用后续pytest/mutation掩盖authority失败；仅写step-161，无禁跑项

### 证据

`projects/thesis-fso/worker-logs/step-160-d0-ordinary-canonical-identity-compiler.md`

`projects/thesis-fso/worker-logs/step-161-d0-ordinary-canonical-identity-independent-verification.md`

```text
VERDICT=FAIL — D0_ORDINARY_CANONICAL_IDENTITY_COMPILER_AUTHORITY_GAP
P0/P1/P2=0/1/0
baseline_counts=42967/27487 unauthorized_candidate_identities=1080
step-161 SHA256=8014dbbcdd93bbfdc63b7f2c5a3afff50fbfcf4eb725ffc3deab7683e2e80071
```

### 结论

FAIL

T114代码保留为待修实现，不接收为I05增量。只开放D019/T116 authenticated ordinary-domain projection与compiler rewiring；通过T117前不得继续provenance/HMM/FULL。

---

## V016: ordinary domain authority repair 最终独立验收

> date: 2026-08-10
> 关联：S001 / D019 / T116–T117 / step-162–163 / V015

### 验证项

- [x] author strict RED 4/4真实失败；final exact 4/4、contract+ordinary 22/22、旧四文件54/54全绿
- [x] raw-owner independent projection：15个domain字段逐项匹配typed view，canonical seal=`15c88476...`精确命中；owner/science/identity三旧seal与D0Contract四字段不变
- [x] runtime global/shadow attacks 9/9：CANDIDATES/S2_METHODS/FIXTURES/POL/TUPLES/S4_CHECK_IDS及alias/B/Nw等基数替换均不改变build/assert
- [x] fresh domain/seal mutations 22/22全部拒绝，wrong accept/reject=`0/0`
- [x] full independent identity oracle：438,313 assertions；bindings/computations=`42967/27487`逐条命中，7 projection counts、S2/BPS goldens、grouping、fresh nonalias全过
- [x] static boundary：ordinary compiler无parallel globals/domain literals、无import-time I/O；旧FULL/provenance/HMM路径无语义改动
- [x] protection：HEAD/staging/P05/cache/frozen artifacts/diff-check均通过；未运行benchmark/science/MVE

### 证据

`projects/thesis-fso/worker-logs/step-162-d0-ordinary-domain-authority-repair.md`

`projects/thesis-fso/worker-logs/step-163-d0-ordinary-domain-authority-independent-verification.md`

```text
VERDICT=D0_ORDINARY_DOMAIN_AUTHORITY_REPAIR_INDEPENDENTLY_VERIFIED
P0/P1/P2=0/0/0 assertions=438313 globals=9/9 mutations=22/22
identity=42967/27487 pytest=22/22+54/54
step-163 SHA256=1e0c25214e4fb2d69862dfb5da858492c788831430de01def21ec994779a31fa
```

### 结论

PASS

V015 的 module-global authority gap已关闭；ordinary canonical identity/binding compiler正式接收。I05 provenance/HMM/raw FULL仍OPEN，benchmark/science继续禁止。

---

## V017: D020 runtime-content owner 独立限时复核

> date: 2026-08-10
> 关联：S001 / D020–D021 / T118–T119 / step-164–165

### 验证项

- [x] final owner/identity/scientific seal精确命中；反向删除新增identity区域复原pre-owner `02d471a...`
- [x] 2个hard-output与8个ordinary provenance golden由独立local encoder重算，`10/10`命中
- [x] 新增11个version baseline全命中、11/11逐项mutation拒绝；已知`decoder_hard_output.version`错误接受判定为author oracle漏检，不是final-owner缺陷
- [x] wrong accept/reject=`0/0`，P0/P1=`0/0`
- [ ] 任务要求的`>=50`完整mutation只完成`11`；旧128 literals/3 grids/10 goldens/6 HMM counts、全保护矩阵未在硬停前完成

### 证据

`projects/thesis-fso/worker-logs/step-164-d0-ordinary-runtime-content-owner-transfer.md`

`projects/thesis-fso/worker-logs/step-165-d0-ordinary-runtime-content-owner-independent-verification.md`

```text
VERDICT=INCOMPLETE_D0_ORDINARY_RUNTIME_CONTENT_OWNER_INDEPENDENT_VERIFICATION_TIMEBOX
P0/P1/P2=0/0/1 new_goldens=10/10 version_mutations=11/11 wrong_accept/reject=0/0
step-165 SHA256=a0346cef7f4a5189501f35a3b174d20a2c802e973f624e8b5c91dea0cbbe747b
```

### 结论

PARTIAL

final owner未发现语义缺陷，但不得称独立PASS。按D021，遗留owner矩阵必须在下一次fresh loader final-byte verifier中一次完成；该verifier PASS前runtime sidecar继续冻结。

---

## V018: I05 runtime-content/FULL 唯一 fresh batch 验收

> date: 2026-08-11
> 关联：S001 / D020–D023 / T120–T125 / step-166–171 / V017

### 验证项

- [x] 显式五文件 final regression：`71 passed / 0 failed`，pytest `686.12s`，wall `689.024s`
- [x] ordinary/HMM/FULL populations=`27487/22800/50287`；FULL incremental=`17.895242s`；重复深编译调用=`0`
- [x] FULL authority=`6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484`
- [x] loader、hard-output、ordinary provenance、HMM/FULL 共118项fresh负向全部拒绝，wrong accept/reject=`0/0`
- [x] owner/contract/schemas/codec/五tests/step-170/P05 hashes exact；HEAD不变、staging=0、无新simulation cache
- [x] 只关闭CP012 I05 implementation/unit；未运行benchmark/science/MVE，D0=`NOT_RUN`、method signal=`NONE`

### 证据

`projects/thesis-fso/worker-logs/step-166-d0-owner-loader-d020-seal-refresh.md`

`projects/thesis-fso/worker-logs/step-167-d0-hard-output-write-anchor.md`

`projects/thesis-fso/worker-logs/step-168-d0-ordinary-provenance-runtime-bundle.md`

`projects/thesis-fso/worker-logs/step-170-d0-full-positive-recompile-hotpath-repair.md`

`projects/thesis-fso/worker-logs/step-171-d0-i05-fresh-batch-verification.md`

```text
VERDICT=D0_I05_FRESH_BATCH_VERIFIED
P0/P1/P2=0/0/0 pytest=71_passed_in_686.12s
negatives=118 wrong_accept/reject=0/0 FULL_incremental=17.895242s
step-171 SHA256=896834e8d269276b934af0dc53cdb3b2ad9736184a81b13514b51757cb04c9bc
```

### 结论

PASS

V017剩余覆盖债由T120 loader矩阵与T125 final batch一并关闭；I05 implementation/unit正式接收。下一步只进入I07/I08 deterministic/unit实现，不开放吞吐门或科学运行。

---

## V019: D0 implementation、独立代码审查与正式 I20 工程终态验收

> date: 2026-08-11
> 关联：S001 / D011 / D024 / CP012–CP013 / step-175–200

### 验证项

- [x] I07+I08 唯一 fresh 合并快验：`25 passed / 1.89s`，P0/P1=`0/0`
- [x] 后续实现与修复均有真实 RED→GREEN；I18 aggregate=`133 passed / 30s`，I19D final integration=`189 passed / 488.73s`，最终 P0/P1=`0/0`
- [x] 四类允许调整均实际执行或证实 N/A：vectorization、batch size、checkpoint chunk 输出与 scalar `max_abs_error=0`；exact-content cache 无重复 owner content，reads=`0`、真实 miss units=`4`
- [x] EB final regression：`36 passed / 74.05s`
- [x] 正式 I20 只运行一次：shell wall=`25.7s`、runner elapsed=`11.26600000000326s`、exit=`1`、`incomplete_reasons=[]`
- [x] 官方 artifact：`benchmark-receipt.jsonl` 1 条、`engineering-slices.jsonl` 25 条；decoder/BPS/B2/HMM/adjustment=`4/6/10/1/4`，receipt/slice SHA 与 stdout 一致
- [x] 冻结预算复算：`4.0 + 6.8194509317398575 = 10.819450931739858d > 7.0d`；science、BER、goodput、method gain 均未运行/未声称

### 证据

```text
I07_I08_FRESH=25 passed in 1.89s
I18_DETERMINISTIC_INTEGRATION=133 passed
I19D_FINAL_INTEGRATION=189 passed in 488.73s; P0/P1=0/0
EB_FINAL=36 passed in 74.05s
FORMAL_I20_EXIT=1 WALL=25.7s RUNNER=11.26600000000326s
STATUS=GREATER_THAN_7D_HARD_BLOCKER
INCOMPLETE_REASONS=[]
PROJECTED_D0_DAYS=10.819450931739858
PROJECTED_MISSION_DAYS=7.0
RECEIPT_SHA256=236e1c17bedbf59b90e1b085b176d70377277e2c19a866e12c1e1ff63d72fddd
SLICES_SHA256=2795428ba4a45acf952a7254d66c82201ea7688980d90ced91ddc190312065f4
```

证据文件：

- `projects/thesis-fso/worker-logs/step-191-d0-i19d-final-integration-review.md`
- `projects/thesis-fso/worker-logs/step-198-d0-i20-allowed-adjustments-independent-verification.md`
- `projects/thesis-fso/worker-logs/step-199-d0-i20-cache-unit-accounting-repair.md`
- `projects/thesis-fso/worker-logs/step-200-d0-i20-formal-engineering-throughput-terminal.md`
- `projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput/benchmark-receipt.jsonl`
- `projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput/engineering-slices.jsonl`

### 结论

PASS

正式 I20 是完整、可复算的 `GREATER_THAN_7D_HARD_BLOCKER`，不是 INCOMPLETE。D024/CP013 可据此关闭专题；S1–S4 与 FAIR_COMPARISON_RUN 保持 NOT_RUN。
