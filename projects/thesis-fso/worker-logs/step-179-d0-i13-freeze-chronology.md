# Step 179 — D0 I13 freeze chronology

> 2026-08-11 | D0 implementation | DONE

## 范围

- 仅修改 `freeze.py` 与 `test_d0_dev_freeze.py`，实现 implementation plan I13 的 DF07–DF10、DF12。
- DF11 未创建；未实现 benchmark/evaluator 绑定，未运行 science、I05 或 benchmark。
- 未修改 `common/`，未触碰四个 `p05_run*.log`，未 stage/commit/push。

## 实际代码

- 新增三条 dev-only fit API：`fit_common_bps`、`fit_b2_statistics`、`select_b2_tuple`。三者均把输入限制为 exact dev seed `8000–8009`；HMM aggregate 通过显式 `member_seeds` 绑定成员 seed 域。
- 新增 `validate_b2_tuple_rows`：验证 clean=`1200`，controlled=`21600=10800 target+10800 sentinel`，每 fixture 两个 polarization row，affected counts 只允许出现在 target row。
- 新增 final tuple exact selector：combined macro net-goodput → periodic pilot fraction → controlled-target affected CWER → lower M → owner legal order。
- 新增 immutable five+five+one freeze：五个 BPS winner、五个 statistic winner、一个 final tuple；每一类保存全部被评估 candidate 的 exact rational objective、完整 lexicographic key 与对应 raw SHA256。
- 新增 `resolve_dev_freeze`、canonical one-write `write_resolved_freeze`、canonical `load_resolved_freeze` 与 `assert_phase_freeze_chronology`；S1/S2/S3-dev/S3-test/S4 必须反向绑定同一 `dev_freeze_sha256`。

## RED → GREEN

### RED 1

```text
14 passed, 8 failed in 21.48s
elapsed=22.498s
```

八个失败均为预期缺口：`validate_b2_tuple_rows`、`B2TupleSelection`、三个 fit/resolve/write/load/chronology API 尚不存在；既有 DF01–DF06 保持 GREEN。

### RED 2（新发现 malformed-seed fail-open 异常类型）

```text
1 failed, 22 deselected in 1.40s
```

`seed=None` 原会在排序时报 `TypeError`，不能按 fit boundary fail closed。加入 negative 后先复现，再以 `_observed_row_seeds` 最小修复为 `FreezeError(dev-only)`。

### Fresh GREEN

```text
23 passed in 21.72s
pytest+py_compile elapsed=23.047s
pytest exit=0; py_compile exit=0
```

- 展开后的显式拒绝检查：32 项，其中 DF10 对 5 类非法 seed × 3 fit API = 15 项。
- `git diff --check`：PASS。
- DF11/static benchmark no-fit test：不存在，符合 I13 延后约束。

## Hashes

- `freeze.py`: `a2a1083ecc34c54250f3ad320e2e0e804e902e775cded401b4b030d445e3e47d`
- `test_d0_dev_freeze.py`: `ce448054615719b90a29b1fa08890474cb7acb62f952768f984ce17be3be4a18`
- DF12 canonical synthetic resolved freeze: `e789d08a030f1f3d051756a9e6e78ce794d30e8dadb1b603b315b0e14ffa9341`

## 结论与下一接口

- 作者门：GREEN；P0=0，P1=0。
- D0 science 仍 `NOT_RUN`，method signal 仍 `NONE`；本任务不产生 BER/goodput/方法增益结论。
- 下一接口：I15 可消费 `ResolvedDevFreeze` 与每 tuple B2 statistic；I17A 才新增 DF11，把真实 evaluator/benchmark call graph 绑定到本 freeze 并证明三条 fit API 不可达。

## P1 最小修复追加 receipt（2026-08-11）

### Root cause

`resolved_freeze_from_document` 只验证 top-level/schema/raw-hash 形状，没有在 immutable load boundary 重验 fit 输出；因此空的 `common_bps=[]`、`b2_statistics=[]`、`b2_tuple_candidates=[]` 和 `final_b2_tuple={}` 也能构造 `ResolvedDevFreeze`。原 DF12 正向 fixture 恰好使用这一非法空结构，掩盖了 owner 的 exactly five BPS + five statistic + one final tuple 约束。

### RED

把 DF12 正向 fixture 改为真实合法 five+five+one canonical document，并加入缺、空、多、重复、wrong-final-binding、candidate raw-hash drift、candidate exact-key drift 七类变体：

```text
1 passed, 7 failed, 22 deselected in 8.46s
elapsed=9.778s
```

七类非法文档均被旧 `resolved_freeze_from_document` 错收，稳定复现该 P1。

### 修复

- loader 复用 fit 阶段 exact rational、owner tuple order/grid、candidate key 与 raw SHA 约束，闭世界验证五个 unique BPS tuple entries、五个 unique statistic tuple entries、五个 legal tuple candidates。
- BPS 每 tuple 必须保存六个 owner-grid candidates；statistic candidate set 必须非空且 `(p_s_index,sigma_e2_index)` 无重复。
- 每个 winner 必须等于其 candidate set 的 exact lexicographic minimum；`final_b2_tuple` 必须等于五个 tuple candidate 的 exact minimum。
- `resolved_freeze_from_document` 与真实 canonical-file `load_resolved_freeze` 共用同一 validator，single-freeze hash chronology 未改变。

### Fresh GREEN

```text
affected DF12: 8 passed, 22 deselected in 5.86s
full file: 30 passed in 22.69s
combined elapsed=30.265s
```

- 新增负向：7 类 × 2 个实际入口（resolve/load）=`14`；wrong accept/reject=`0/0`。
- `git diff --check`：PASS；DF11 count=`0`。
- P0=`0`，P1=`0`（本轮 P1 已关闭）。

### 修复后 hashes

- `freeze.py`: `b1523d7d90d55b28d9b3fbb59d65e77ffe2cd5477c92bdec81844ced673cab03`
- `test_d0_dev_freeze.py`: `d7599e68ecaf76a1114b6ec29f6e127eda0b40f1f651f2b71af6dcd9fff59f22`
- 合法 DF12 five+five+one freeze: `e8a2b25c8124ed4cdb7cf344b8a5441fdb7e27b7078eda5460547157405cb32a`
- 上一节空结构 synthetic hash `e789d08a...` 现被 loader 正确拒绝，不再是合法 freeze evidence。
