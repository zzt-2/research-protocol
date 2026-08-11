# DSP 失效感知的多孔径相干 FSO 可靠合并

> 状态：dormant | 当前阶段：Groundwork Step 3.5 `EVIDENCE_BLOCKED`

## 范围边界

### 原始目标

基于现有仓库、已下载一手材料和 reference baseline，判断 post-DSP multi-aperture MRC 在支路 DSP-outage/lock 异质条件下是否存在值得进入 Groundwork 的 reference-method extension 入口。

### 当前范围

仅执行 GW Step 3.5：围绕冻结 Q001 做矩阵化补检索、核心竞品双向引用链、Sun 2019 合法动作证据闭合、新高相关全文 acquire/read 与统一 exact-action collision 裁决。最多三轮，最后一轮 new must/should 必须为 0。

### 明确不含

- 不进入 Step 4a 及以后；只允许 Step 3.5 合法检索、获取与精读。
- 不实现、不仿真、不运行 smoke、不修 b3 代码。
- 不把固定 SNR 阈值 branch-drop、SC/GSC 或 Johst 2024 已给出的 discard rule 当新方法。
- 不重开 coded decoder-feedback C1；decoder/FEC flag 只可列为可选 receiver-visible feature。
- 不输出 Go/Kill、METHOD_SIGNAL、方法成立或论文贡献。

### 范围变更记录

- 2026-08-11，D001：主控验收 K1 后授权新专题仅执行 GW Step 1；原因是 coded C1 科学关闭后需寻找不同算法研究对象。
- **[2026-08-11] D002**：当前范围由 Step 1 扩展到 Step 2 acquisition。
  - 原因：V001 接受 Step 1，主控显式确认进入 acquisition。
  - 新范围：相关性筛选→资产复用→合法获取/转换→identity/content quality→coverage gap。
  - 影响的未决项：2019 P0 只判全文可得性；完整动作签名留给未授权 Step 3。
- **[2026-08-11] D003**：撤销“2019 P0 缺失=绝对 hard blocker”，开放 Step 2 narrow repair + Step 3。
  - 原因：共享根已有更晚、更强且可读的 JLT 2023 estimator-changing competitor；用户不接受继续把全部工作停在 coverage 行政门。
  - 新范围：JLT 2023 CORE binding → Step 2 accepted with limitation → 五篇全文精读与 Q# 裁决。
  - 影响的未决项：2019 缺失降为 claim limitation；仅当 Step 3 窄 Q# 存活时移交 Step 3.5。
- **[2026-08-11] D005**：当前范围由 Step 3 扩展到 Step 3.5 exact-action closure。
  - 原因：V003 接受 Q001 branch-local 4/4，但 Sun 2019 exact action 与定向 collision landscape 未闭合；主控显式授权。
  - 新范围：query matrix → 核心竞品双向引用链 → Sun 2019/新高相关一手证据 → 统一动作签名 → 三选一 terminal。
  - 影响的未决项：Step 4a 继续禁止；完整 post-all-FS/CE/CPE 版本仍 excluded/unresolved。

## 进展线索

- S001 / D001：注册表去重通过；冻结 M-C-A hypothesis、Step 1 检索合同与越界禁止项。
- T001–T002：两路摘要/元数据级语义初筛完成；27-entry matrix、24 formal、8 must-read。
- R001：hard route 已归 comparator；宽泛 soft weighting 有 RF 先例；2019 optical direct competitor collision 未闭合，provisional terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。
- T003 首验：`FAIL 0/1/1`；计数/scope PASS，identity/provenance binding 与 26→27 残字需窄修。`step1-provenance-receipt.md` 已绑定既有全局索引的 2019/Geisler S2+OpenAlex 条目，等待第二次 fresh 终验。
- V001 / H001：第二个 fresh verifier `PASS 0/0/0`；terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`，Step 2=`NOT_AUTHORIZED`。
- S002 / D002：主控确认 Step 2；开始 acquisition，Step 3=`NOT_AUTHORIZED`。
- R002/R003：九篇冻结池中 4 篇 fulltext qualified；optical CORE=`2/5`。2019 P0 非 OA、无 arXiv/PDF URL且合法三轮获取失败，terminal=`STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`。
- V002/H002：fresh verifier=`PASS 0/0/0`；coverage blocking terminal 被接受并交接主控，Step 3 仍未授权。
- S003/D003：JLT 2023 source/content 身份、SHA、行数闭合；Step 2 修为 `STEP2_ACCEPTED_WITH_2019_FULLTEXT_LIMITATION`，Step 3 已授权并开始。
- T007–T010/R004/D004/V003/H003：五篇全文完成；首验 PARTIAL 0/2/0 后，Q001 收窄到 Wang 真实 branch-local FS/phase-correction→MRC 边界并修 read-note 持久化链；终验 PASS 0/0/0。
- S004/D005：主控授权 Step 3.5；H003 接收核验 PASS，开始 exact-action closure。
- T011–T016/R005/D006/V004/H004：两轮检索最后一轮 new MUST/SHOULD=0/0；Zhang 2023 为 estimator-changing neighbor；Sun/Xie/Qiu 等承重动作仍无一手全文。fresh verifier 首验 PARTIAL 0/1/2，bounded repair 后 final PASS 0/0/0；terminal=`EVIDENCE_BLOCKED`，无 Step 4a 入口。

## 已确认结论

### 不变量

1. Johst 2024 的 outage-branch discard 只支持 defect 形状；固定阈值丢支路是 mandatory comparator，不是本专题方法。
2. 只有 receiver-visible multi-source DSP validity 驱动的 soft shrinkage/abstention，或有明确时序物理前提的 hysteretic admission，才可作为潜在 extension 检索对象。
3. Step 1 只能产生检索终态；没有 Step 2 授权，不得下载、精读、实现或仿真。

### 其他结论

1. 历史 b3 multi-aperture caller path 可作未来资产，但 truth-h 信息边界与 RNG/offset 是未来 Step 4a 债务，不在本轮修复。
2. Q001 仅在 branch-local FS/alignment+phase-correction→MRC 边界通过 Step 3 四判据；完整 post-all-FS/CE/CPE 位置仍未闭合。
3. `STEP3_Q_SURVIVES_READY_FOR_STEP3_5` 只表示问题候选存活，不等于方法有效、新颖性闭合或论文贡献。
4. Step 3.5 身份检索已收敛，但 direct-action evidence 不充分；`EVIDENCE_BLOCKED` 不是 exact collision 或 scientific Kill。

## 未决项

1. Sun/Xie/Qiu 的承重 primary fulltext 或等价后续一手完整动作证据能否取得。

## 当前位置

`GROUNDWORK_STEP3_5_EVIDENCE_BLOCKED`：D006 已截断；Step 4a=`NOT_AUTHORIZED`。等待新的承重一手证据，不重复搜索。
