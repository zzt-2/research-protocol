# [S002] Decision receipt、evidence gate 与四轮行为压力测试

> 2026-07-17 | 实施与验证 | COMPLETE（核心 gate PASS；完整性债务 PARTIAL）

## 目标

以 TDD 实现最小 decision receipt + evidence gate，并在一个主对话中连续完成正常、诱惑、stale/绕过和无历史上下文恢复四轮压力测试，最后交由独立 verifier 复核。

## 记录

### 收 H002 核验

- H002 声称当前仅有 `GovernanceController.check()` / `execute()`、没有 receipt/evidence gate：PASS；源码核验一致。
- H002 声称 V003 定向测试 22 项：PASS；本轮新鲜运行 `python -m pytest projects/simulation/tests/test_direction_lab_controller.py -q` 得到 `22 passed in 0.30s`。
- H002 声称未知 action、缺失 evidence、fingerprint stale 与 blocked execute 漏口已修复：PASS；源码和对应回归测试均存在。
- 注册表：`depends_on` 为 `framework-evolution` 与 `2026-06-12-simulation-foundation-rebuild`，两者均为 active；`conflicts_with: []`。R002 与 pilot 资产存在，依赖可用。
- 范围：本轮在当前 scope 内，未触及“明确不含”；专题仅 1 个既有 S 文件，无膨胀风险。

### 最小设计与实现计划

选择审计账本背书方案（D001），不选择不可恢复的纯内存 token，也不在 pilot 内建设签名系统。

1. RED：先写 receipt 字段、manifest hash、blocked receipt、受控 envelope 的失败测试；确认因接口缺失而失败。
2. GREEN：最小扩展 controller，让 `check()` 的每次允许/阻断都写 receipt 字段，让 `execute()` 返回结果 envelope。
3. RED：先写 evidence gate 对合法、orphan、伪造/不匹配 receipt 及三类目标的失败测试；确认因 gate 缺失而失败。
4. GREEN：实现只读审计核对与目标动作门；不可信结果返回 `ORPHAN/UNTRUSTED` 或 `UNTRUSTED`，不写任何目标 ledger。
5. 在隔离 pilot 运行目录连续跑 Round 1–3；Round 4 先写答案键，再派无历史子 agent 恢复并评分。
6. 派独立 verifier 复核行为、证据与复杂度；出现 bug 先补 RED 回归测试再修复，同类连续两轮漏拦则停止堆规则并退回设计。

### 前置门与负担字段

每轮固定记录：输入、预期门、实际动作、是否被拦、是否进入证据链、误拦、人工提醒次数、读取文件数、读取字段数、同类违规是否复发。P0 漏入证据链必须为 0；同类漏拦不得连续两轮。

### 独立复核与修复

- V004 独立 verifier 首次黑盒发现：合法 receipt 可承载替换后的 `result` 进入 ledger；仅 `check()` receipt 可拼出可验收 envelope；同一 receipt 可 replay。该轮结论 FAIL，原始运行目录 `runs/stage2-2026-07-17/` 保留。
- 按 TDD 新增三条 RED 回归，随后写入 execution audit event、`result_hash` 与同 destination replay 门；定向测试由 31 项增至 34 项并通过。
- 修复后在 `runs/stage2-2026-07-17-final/` 重跑 Round 1–3：R1 PASS（1 条 accepted ledger）；R2 PASS（诱惑全阻断，ledger 计数不变）；R3 PASS（旧结果 STALE，绕过三目标均 ORPHAN/UNTRUSTED）。
- 修复后再次派无历史 agent 做 R4，答案键语义评分 8/8（阈值 7/8）。V005 发现 final answer-key raw SHA256 与记录沿用了旧目录 hash（旧 `76EA...`，final `F950...`；canonical JSON hash `20ec...`），文本语义未变但字节规范未冻结，故 Round 4 provenance 记 PARTIAL，不静默改写为 PASS。
- V005 另记 destination path 由调用方注入、manifest 可整体伪造、JSONL 无签名/不可变 registry 等债务；这些不在本轮扩展范围内。

### 复杂度审计

- **必须保留**：`check()`/`execute()` 双入口；receipt 六字段；manifest/result hash 与 execution audit；STALE/replay；三类 destination 动作白名单；逐轮输入、门、误拦、证据链、负担和复发字段。
- **应合并**：`_recorded_receipt()` 与 `_recorded_execution()` 后续可统一成一次审计索引；`allowed/blocked` 可冻结一个规范字段、另一个派生；轮次重复字段可由统一汇总器生成。
- **应删除或延后**：本 pilot 未使用的 `VERIFIED_RUN`/`PAPER_READY` 晋级等级；不要在本轮增加签名、数据库、全部 schema 或新 skill。`REUSE_RESULT` 是否进入正式 schema 留给后续设计，不在本轮扩展。

## 决策引用

- D001：采用审计账本背书的最小 decision receipt 与 evidence gate（新建）
- D002：execute 结果必须有审计 execution 记录并防止 replay（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

- 核心 gate 已完成；保留 hash 表示、manifest 来源、JSONL 不可变性和 destination path 边界债务，不在 pilot 内扩展。
