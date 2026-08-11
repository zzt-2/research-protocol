# Handoff: I07/I08 已 GREEN，下一对话直接继续 D0 实现

> 来源: S001 | 交接目标: 一次合并快验后直接进入 I09/I11，不再回头审 I05
> 日期: 2026-08-11
> 文件名: H005-i07-i08-green-continue-implementation.md
> 当前 handoff: 是；取代 H004 的当前入口地位，H004 作为 CP012 初始实现入口保留

## 到哪了（状态）

I01–I06 已完成，其中 I05 由 V018 的唯一 fresh batch 以五文件 `71 passed / 686.12s`、118项负向、wrong accept/reject=`0/0`接收；FULL增量由重复编译修复前的364.1秒timeout降到`17.895242s`。I07作者侧已完成S1/S2/bootstrap与S3，SS01–11局部门`10/10`；I08作者侧AC01–06与窄回归共`19/19`，20项负向全拒。D0仍=`NOT_RUN`、method signal=`NONE`，没有BER/goodput或方法增益结论。

## 下一步干什么

新对话先对I07+I08最终字节做**一次**15分钟内的合并focused verifier；PASS后立即按implementation plan进入Batch 3a：I09 receiver与I11 ledger/S4并行实现。不得重跑I05的11分钟五文件链，除非新的具体P0/P1直接指向I05；不得在每片之间再插owner/schema/readiness review。

## 纪律（和下一步直接相关）

1. 每个工作包必须产生实际代码和真实RED→GREEN；纯准备、纯审查、纯状态协调不得形成独立常态包。
2. 一批实现后只做一次fresh合并验收；PASS即前进，只有新P0/P1才开最小修复，不做author→review→rereview链。
3. 子agent单次≤15分钟；同文件串行、独立文件最多三路并行。聊天每次只报代码、测试数、耗时、失败点。
4. 不运行science、S1–S4或FAIR_COMPARISON，直到剩余D0实现、独立代码审查、12分钟非科学吞吐门全部PASS并新立D/V/CP。
5. 不改`common/`，不动/暂存四个P05日志，不push；不使用reset/restore/checkout丢弃工作树。

## 接口变更

```yaml
contracts:
  - id: C-I05-RUNTIME
    type: interface-change
    description: typed decoder hard-output, ordinary provenance, HMM runtime and authenticated FULL authority
    location: projects/simulation/explore/coded-decoder-feedback/schemas.py
    change: populations 27487 ordinary + 22800 HMM = 50287 FULL; authority 6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484
    consumed_by: I11 ledger and later runner/verification
    verification_result: PASS_V018
    verified_by: projects/thesis-fso/worker-logs/step-171-d0-i05-fresh-batch-verification.md
  - id: C-I07-STATS
    type: interface-change
    description: pure S1/S2/S3 reducers and paired PCG64 bootstrap
    location: projects/simulation/explore/coded-decoder-feedback/statistics.py
    change: reduce_s1, reduce_s2, bootstrap_paired, select_s3_lambda, reduce_s3
    consumed_by: I10/I11 and later scientific runner after authorization
    verification_result: AUTHOR_GREEN_PENDING_ONE_BATCH_VERIFIER
    verified_by: projects/thesis-fso/worker-logs/step-172-d0-i07-s1-s2-bootstrap-kernels.md; projects/thesis-fso/worker-logs/step-174-d0-i07-s3-kernels.md
  - id: C-I08-ARTIFACTS
    type: interface-change
    description: canonical JSON/JSONL and immutable-generation atomic bundle with CURRENT pointer
    location: projects/simulation/explore/coded-decoder-feedback/artifacts.py
    change: canonical_json_bytes, canonical_jsonl_bytes, write_jsonl_atomic, write_bundle_atomic, validate_complete_bundle
    consumed_by: I11 and I10 finalized artifact boundary
    verification_result: AUTHOR_GREEN_PENDING_ONE_BATCH_VERIFIER
    verified_by: projects/thesis-fso/worker-logs/step-173-d0-i08-atomic-artifact-core.md
```

## 失败数据附录

### 过度复核路线

- 核心失败机制：把owner/schema readiness拆成多轮author/reviewer/re-review，实际功能代码没有同步增长，触发M4/M6。
- 具体数据：唯一I05全量五文件运行只需`686.12s`；全天级耗时主要不是计算，而是重复拆分和复核。
- 已排除方向：无新P0/P1时继续loader/owner/schema readiness review。
- 可复用部分：V018已接收的I05代码、71-test结果和118项负向矩阵，后续直接消费。

### FULL重复canonical recompilation

- 核心失败机制：ordinary graph在positive node、FULL build、FULL assert内共构建三遍。
- 具体数据：旧run `364.1s timeout`；修后ordinary重复深编译`2→0`，FULL增量`17.895242s`，authority不变。
- 已排除方向：重复全图深验；public deep verifier仅留给真正需要的独立批验。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| I07/I08尚无fresh独立batch verdict | 实现与审查分离 | author GREEN | 新对话第一包一次合并focused verifier |
| I09–I20尚未实现 | D0 deterministic/unit全部闭合后才可benchmark | PENDING | 按plan批次持续推进，不停在单任务 |
| tracked `tools/**/__pycache__`存在历史dirty | final commit不得夹带生成缓存 | 未清理 | 最终commit前用`git cat-file blob HEAD:path`逐文件恢复；禁止reset/restore/checkout |
| scientific S1–S4未运行 | 只有新D/V/CP可开放 | NOT_RUN/NONE | 全D0+独立code review+12分钟吞吐PASS后治理开放 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| I07+I08合并快验 | SS01–11 focused + AC01–06 +独立golden/负向，P0/P1=0；≤15分钟 | implementation plan / T126–T128 | author: I07 10/10，I08 19/19 |
| I05已关闭 | 不重跑；只有新直接交叉失败才重开 | V018/D021–D023 | 71/71，118 negatives |
| science权限 | 新D/V/CP存在前始终NOT_RUN | CP012 | 当前NONE |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少3条关键事实声称
  - 声称1：I05 V018=`71 passed` → 核对step-171
  - 声称2：I07 author=`10/10` → 核对step-172/174与final SHA
  - 声称3：I08 author=`19/19` → 核对step-173与final SHA
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

一次I07+I08合并focused verifier；PASS即并行实现I09/I11。除真实P0/P1或hard terminal外，自动继续后续D0批次，不停下来请求用户确认。
