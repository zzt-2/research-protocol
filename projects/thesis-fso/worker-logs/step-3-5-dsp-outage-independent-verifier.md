# Step 3.5 DSP-outage exact-action closure — independent verifier

> 2026-08-11 | T016 | fresh-context independent verification | no repair / no commit / no push

## Verdict

`PARTIAL`

- critical / major / minor = `0 / 1 / 2`
- 科学终态 `EVIDENCE_BLOCKED` 与现有一手证据边界相符；PARTIAL 来自最终控制面尚未闭合和两项可复现性/措辞问题，不是 collision verdict 反转。

## 逐项核验

### 1. 机械计数与收敛 — PASS（附 1 minor）

- Round 1：8 个 JSON receipt 均存在；JSON 实际保留行数为 `6+1+4+0+8+20+3+4=46`，按 DOI→arXiv→规范化标题复算为 `45 unique`。T011 表内 provider-raw 为 `20+3+21+0+20+34+12+5=115`；最后分类 `MUST/SHOULD/MAY/REJECT=0/0/5/40`，总数 45。
- citation：7 个 receipt 实际行数为 `20+19+19+24+14+30+8=134`；同一 key 规则复算 `121 unique`；raw records 中 abstract present/missing=`106/28`。
- Round 2：q01–q06 六个 receipt 实际保留 `0+0+0+3+1+0=4 unique`；T015 表内 provider-raw=`0+0+0+5+1+0=6`。Qiu 是 T012 已知 MUST，其余 3 个 REJECT，因此最后一轮 new MUST/SHOULD=`0/0`。
- 来源：Round 1 retained unique 的 S2/OpenAlex 贡献为 `17/28`；Round 2 只有 S2 实际贡献，OpenAlex 限流 0 贡献。R005 没有把 Round 2 的 0 贡献源虚报为贡献源；整体确有 S2+OpenAlex 两个实际贡献源。
- **minor-1**：`115` 与 `6` 是执行时 provider-raw stdout 计数，只保存在 worker table；保存的 JSON 分别只有 46 与 4 行，未保存 provider 原始返回或 stdout，故 verifier只能复算表内加总，不能从 raw artifact 独立重建 provider-raw。45/121/4 unique 与最终 0/0 均可从 receipt 独立复算。

### 2. Identity/content/acquisition — PASS

- Zhang：正文题名、作者和 DOI 在 `papers/downloads/2026-07-08/10301506.md:5-19` 一致；实测 418 行、SHA256=`AFCE9FB293BC12F5638239D03F3B31A76068B31D48B528C8E82BCD091DAD45CF`，与 T014/canonical note 一致。动作顺序由正文 `:115,145-223` 支持；Sun 引文片段与 identity 由 `:129,405` 支持。
- Sun/Xie/Chen/Qiu/Li 五个 canonical DOI 目录均无 `source.*`/`content.md`；metadata 都是 `failed/all_failed` 且 `content_file` 为空。Xie/Chen/Qiu/Li metadata SHA 与 T013 四行一致；Sun 本轮 metadata SHA=`87D8EF6D6F3F31D1AD8EA007447ED7912C5240EE1193394614E474C881C9035B`。R005 没有把 metadata、title 或后续引文冒充全文。
- Zhang canonical note 已存在但受 `papers/` ignore 规则影响，当前未被 Git 跟踪；统一 commit 必须显式 force-add。

### 3. 动作语义与 terminal — PASS

- Wang/Johst/SC-GSC/Tu/Yang/Liu/Zhang/Sun/Xie/Chen/Qiu/Li 的分类保持了已读一手与未知字段边界；Zhang 的 input/position/trigger/tap action/no-valid/state/output 可由全文定位复核，确属 estimator-changing neighbor，不是 Q001 exact collision。
- Johst 是测得 outage boundary 后提出的 hard-discard comparator，未被写成已验证 soft policy；Sun 仅闭合 modulus-normalized-cost fragment；Xie/Qiu 等 action 保持 unknown。
- 可读一手中无 confirmed exact collision，但 Xie/Qiu 等 task-matched direct identities 的承重 input-trigger-action-output 仍无 primary fulltext；因此 `EVIDENCE_BLOCKED` 符合 D005 的三选一合同。它没有被包装为 Kill、non-collision、novelty 或 METHOD_SIGNAL。

### 4. Scope — PASS

- R005/D006/topic/master/registry/H004 一致禁止 Step 4a；完整 post-all-FS/CE/CPE 仍 excluded/unresolved。
- 本轮目标 diff 没有实现、仿真或 b3/coded 文件修改；当前工作树中的 p05/coded logs、pycache、profile、`papers/index.json` 等均为必须排除的 unrelated dirty files。

### 5. 控制面 — PARTIAL（1 major，1 minor）

- topic-index、master-state、registry、R005、D006 与 H004 一致为 dormant / `GROUNDWORK_STEP3_5_EVIDENCE_BLOCKED` / 无 Step4a 入口。
- D004 已写 `被取代：D006`；D006 明确只取代 D004 的 READY 暂态，D005 继续作为 active scope contract，血缘成立。
- H004 包含已完成边界、不要做、必读、接口、失败数据、债务、阈值、接收验证和下一轮，模板完整。
- **major-1**：`verifications.md` 当前没有 V004；H004 scope 行也明确为“待 V004 独立终验”。T016 要求核验的最终控制面尚未形成，因此当前不能给最终 PASS。主线需依据本 verifier 记录 V004=`PARTIAL 0/1/2`，完成窄修后再做 fresh final check，或若治理约定 V004 只能在 verifier 后生成，则至少不得在生成前声称 Step 3.5 完整终验 PASS。
- **minor-2**：literature owner `:55` 仍写“Step 3 不授权公式”，当前应指 Step 3.5；`:71` 仍称 exact novelty 仅受 Sun 缺失限制，漏列本轮已成为 terminal 原因的 Xie/Qiu bearing debts。`:89-93` 的最终 disposition 正确，但前段存在陈旧措辞。

### 6. Git / 暂存边界 — PASS（当前尚未暂存）

- `git diff --check` exit 0，仅有 CRLF conversion warnings，无 whitespace error。
- 应提交（tracked/new）：H003、S004、R005、T011–T016、decisions、topic-index、H004、最终 `verifications.md`/V004、registry、master-state、literature owner、read-log、五份 Step3.5 worker logs、本 verifier log。
- 应 force-add（ignored evidence）：Zhang canonical note；Round1 q01–q08、citation 7 份、Round2 q01–q06 raw JSON receipts；Sun/Xie/Chen/Qiu/Li 五份 acquisition metadata。
- 必须排除：`.sessions/profile.md`、`papers/_read_notes/10.1109_jlt.2020.3003561.md`、`papers/index.json`、全部 `tools/**/__pycache__`、p05 logs、coded-decoder-feedback artifacts；Round2 q07/q08 不是 T015 六个完成 query receipt，也不应纳入本任务。

## 结论

科学证据支持 `EVIDENCE_BLOCKED`，没有 critical scientific defect。当前 PARTIAL 的唯一 major 是 V004/最终控制面未闭合；修复应严格限于 V004 集成与两处 owner 措辞/receipt 可复现性说明，不得重开搜索、改变 terminal 或进入 Step 4a。

## Final check

> 2026-08-11 | bounded-repair follow-up | verifier did not repair files

Final verdict: `PASS`

- critical / major / minor = `0 / 0 / 0`
- V004 已创建，完整保留初验 `PARTIAL 0/1/2`、三项 bounded repair 和待本 follow-up 的血缘；本 final check 可由主线写回其 Final check 段，未掩盖首次缺陷。
- H004 scope 行准确记录“初验 PARTIAL、bounded repair 后待 final check”；收到本结论后只需机械更新为 final `PASS 0/0/0`，不需要改变 terminal 或科学内容。
- R005 已新增 provider-raw 可复现性限制：明确 `115/6` 是 stdout-only，持久 JSON 可独立复算 retained=`46/4`、unique=`45/4`、citation=`134/121` 和最后一轮 `0/0`；未再把 provider raw 冒充 raw artifact。
- literature owner 两处陈旧措辞已修：方法设计禁止明确属于 Step 3.5；collision boundary 明确列出 Sun/Xie/Qiu bearing debts，并写清 Q001 当前不能进入 Step 4a。
- topic-index、master-state、registry、D006、R005、owner、H004 的 terminal/scope 一致为 `EVIDENCE_BLOCKED`、dormant、Step 4a=`NOT_AUTHORIZED`；broader post-all-FS/CE/CPE 继续 excluded/unresolved。
- fresh `git diff --check` exit 0，仅有 CRLF conversion warnings。工作树未新增实现/仿真/b3/coded 目标改动；profile/index/JLT note/pycache/p05/coded artifacts 仍清楚可辨，必须继续从提交中排除。

结论：bounded repair 关闭了初验 `0/1/2` 的全部问题；Step 3.5 最终验证为 `PASS 0/0/0`。这只接受 `EVIDENCE_BLOCKED` 证据与治理闭合，不授权 Step 4a，也不产生 collision/non-collision、novelty、Kill 或 METHOD_SIGNAL。
