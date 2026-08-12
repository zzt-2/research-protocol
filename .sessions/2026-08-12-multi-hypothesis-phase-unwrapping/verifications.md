# Verifications — 有界多假设固定滞后相位解缠 Groundwork

## V001: scope reconciliation 与 GW Step 1 独立验收

> date: 2026-08-12
> 关联：上游 R004/D007；本专题 S001/R001–R003/D001–D002/H001

### 初审（保留）

`PARTIAL`，Critical/Major/Minor=`0/3/1`。

- formal 合并口径未冻结且旧数字不可稳定复现；要求明确 duplicate-title 的 priority/status 聚合规则。
- current views 预声明 V001 PASS/VERIFIED；初审 PARTIAL 时不得保留。
- 两个专题产物使用非法无编号文件名；要求迁为 R002/R003 并补 research-note anchors。
- 最终提交必须显式 allowlist，不纳入 profile、papers index/read-note、pycache、p05/coded/Q001 artifacts。

### 修复状态

- 已由 R002 冻结确定性聚合：同规范化 title 取最高 priority，任一同身份 published 即 formal；复算 278→242→138、formal=98/138=`71.01%`、must=12。
- 旧无编号文件已迁为 R002/R003，全部引用同步中。
- current view 暂降为 `REVIEW_PARTIAL / REPAIR_COMPLETE_PENDING_FRESH_RECHECK`；等待第二个 fresh verifier。

### 当前结论

初审 PARTIAL 已保留；第二个 verifier 因未完成独立 JSON 复算仍为 PARTIAL 0/1/0，不用于恢复状态。第三个限定清单的 fresh verifier 完成全量确定性复算与语义/治理核验，结果如下：

```text
final fresh verifier: PASS — P0/P1/P2=0/0/0
files/raw/groups/keep/formal/must=11/278/242/138/98/12
priority_nonempty=278/278
priority_reason_nonempty=278/278
sources=semantic_scholar,openalex,serpapi_scholar
topic_files=9
illegal_topic_filenames=0
legacy_filename_hits=0
legacy_96_69.57_hits=0
D1_D2_required_fields=8/8
TCOM_verdict=FULL_GENERAL_SUPERSET / MANDATORY_COMPARATOR
step2=NOT_AUTHORIZED
registry_dependencies=2/2
conflicts_with=[]
source_owner_decisions_diff=+34/-0 (D006 untouched; D007 append only)
git_diff_check=0
```

### 结论

PASS。P0/P1/P2=`0/0/0`。允许恢复 Step 1 `VERIFIED` 与唯一 terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`；该 terminal 仍不是 Q#、Go、方法、METHOD_SIGNAL 或论文贡献，Step 2 保持 `NOT_AUTHORIZED`。

## V002: Groundwork Step 2 acquisition 独立验收

> date: 2026-08-12
> 关联：D003/S002/R004/H002/machine receipt

### 初审（保留）

`PARTIAL`，P0/P1/P2=`0/2/2`。

- P1：topic/master/registry 预声明 V002/H002，但当时 V002 与 H002 尚未落盘。
- P1：全 worktree diff 含 profile、JLT read-note、papers index、pycache 与 p05/coded logs；必须用精确 allowlist 暂存，不能把它们并入本轮 commit。
- P2：C12 receipt 作者使用检索元数据变体，与 source 首页不一致。
- P2：topic 顶部 last-update 与 S002 状态仍停在 Step 1/进行中。

### 修复与复核

- 已补本 V002 与 H002，消除 current-view 前置引用。
- C12 作者按 source PDF 首页修为 `Chunyuan Hu / Ruolin Yang`。
- topic 顶部更新为 V002/Step 2，S002 更新为“完成，等待 coverage confirmation”。
- commit 使用显式 allowlist；profile、JLT read-note、papers index、pycache、p05/coded/Q001 artifacts 不暂存。
- fresh verifier 复算 machine receipt：12 selected / 9 qualified / 8 CORE；formal=12/12，2019+=10/12，preprint-source=C02+C08=`2/9=22.22%`。9/9 qualified 的 canonical/source/content bytes、SHA 与有效行数一致（153–634 行）；A/B/C qualified coverage=`3/1/6`；C06/C07/C13 为 metadata-only、0 fulltext，未计 qualified。

### 结论

PASS。P0/P1/P2=`0/0/0`。terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；只确认全文/身份/内容质量/coverage，不构成 collision、Q#、Go、方法、METHOD_SIGNAL 或论文贡献，Step 3 保持 `NOT_AUTHORIZED`。

## V003: Groundwork Step 3 fulltext read 独立验收

> date: 2026-08-12
> 关联：D004–D005/S003/R005/owner/canonical read notes/read-log

### 初审与有界修复（保留）

初审 `PARTIAL`：科学/source spot-check PASS，但 owner 的辅助七表未使用 gw-read canonical schema，实验完备性与写作架构过度压缩，且 current view 预声明 VERIFIED。按同一 Step 3 范围完成一次 bounded documentation repair：

- 新增 9/9 `状态空间/动作空间/奖励函数/建模假设/网络架构/适配性/问题提取` 横向七表；
- 新增 9/9 communication parameter/source 四列表；
- 扩展 5 篇实验完备性并给 aggregate；扩展 C01/C02/C12 写作架构 A–H；
- 将验证状态恢复为 pending，并清理 topic 已裁未决项。

### Final fresh verifier

```text
PASS, P0/P1/P2=0/0/0
HEAD=5a1ef98
owner paper sections/title gates=9/9
gw-read canonical tables=7 × 9 rows
communication parameter rows=9
experiment completeness=5 papers + aggregate
writing architecture=3 papers × A-H = 24 items
canonical read notes=9/9
read-log Step3 rows=9
tracked simulation diff=0
```

Source spot checks PASS：C01 suffix propagation/failed-run discard；C02 decoder soft+forward/backward+L=1/2/3 且 source TeX 无 fixed-lag；C09 `δ`+suffix correction；C10 every-m+adaptive-Q；C12 feedback/feedforward+N64+4K/67K。Q001 四判据与 C02 “primitive full-general / task-contract neighbor”措辞均有界；D2 只作 motivation/component-level absorption，不称 exact collision。

### 结论

PASS。P0/P1/P2=`0/0/0`。允许 terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`；只表示存在 Step 3.5 exact-action/claim closure 入口，不授权 Step 3.5/4a/实现/仿真，不构成 Go、方法、METHOD_SIGNAL 或论文贡献。
