# Verifications — Ch4 参考方法扩展

## V001: 防偏合同与 Skill 最小补丁独立验收

> date: 2026-08-08
> 关联：S001 / D001 / 旧专题 D041
> 结论：PASS

### 验证范围

Fresh-context verifier 独立检查 12 项：Skill 最小补丁、supporting leftovers 禁止重包装、cheap alternative 比较纪律、基础设施预算门、每对象两包与两对象停机条件、旧专题 dormant 且无 S020、新专题治理结构、H001 恢复边界、registry 血缘、p05 日志隔离、Skill repo/user 同步及 `git diff --check`。

### 结果

- 12/12 PASS；P0/P1/P2 = 0/0/0。
- Skill 完整回归：`116 passed, 1 skipped`。
- repo/user Skill：104/104 个非缓存文件 SHA256 byte-identical。
- 旧 system 专题 S### 数量保持 19；不存在 S020。
- registry YAML 可解析；旧专题 `dormant`、新专题 `active`，依赖 slug 均存在。
- 下一轮被限制为最多 3 个对象、至多 1 个推荐，不检索、不进入 GW、不实现、不仿真。
- 四个既有 `p05_run*.log` 未跟踪、未暂存、未进入 diff；因其从未受 Git 跟踪，Git 只能直接证明本补丁未纳入它们。
- `git diff --check` exit 0；仅有 Windows 行尾提示。

### 裁决

防偏合同、恢复入口与 Skill 三条通用规则可以进入使用；无修复项。

## V002: reference-method 入口选择独立验收

> date: 2026-08-08
> 关联：R001 / D002 / T001

### 验证项

- [x] 恢复与范围：[fresh-context verifier 重读 T001、topic、D001、registry] → dormant/active、依赖、授权与防偏边界一致。
- [x] 候选与入口门：[逐候选核 G1–G7、旧 K01/D027 与本地 runner] → 2 个机制不同候选；C1 G3/G7 FAIL，C2 G3 FAIL；无 survivor、无第三候选。
- [x] 防重包装：[对照旧 K01 包与 D027] → 初稿 exact 复活 K01，初审 `REJECT`；修正稿将其记为历史 collision，不再晋级。
- [x] 终态一致性：[确定性 `rg`] → R001、D002、topic-index、registry、H002 均为 `NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`，无旧 selected terminal 残留。
- [x] 范围纪律：[Git 状态与产物审阅] → 未检索、下载、实现、仿真或进入 Groundwork；无科学代码/结果变更。
- [x] Git 与受保护日志：[status/cached diff/diff-check] → cached diff 为空，`git diff --check` exit 0；四个 `p05_run*.log` 未跟踪、未暂存、未进入 diff。

### 证据

```text
git rev-parse HEAD
cb1f5c60a0160aab02a76eceab734589d689f788

git diff --cached --name-only
[empty]

git diff --check
exit 0

rg -n 'ONE_REFERENCE_METHOD_ENTRY_SELECTED_FOR_GW_STEP1|SELECTED_FOR_GW_STEP1' R001 decisions.md topic-index.md .sessions/_registry.yaml H002
NO_MATCH

rg -n 'NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED' R001 decisions.md topic-index.md .sessions/_registry.yaml H002
R001 / decisions.md / topic-index.md / _registry.yaml / H002 均命中

rg -n 'G3 FAIL|G7 FAIL|exact K01|D027|block-GG|不进入 Groundwork' R001 decisions.md topic-index.md H002
C1 G3/G7 FAIL、旧 K01/D027、runner 边界及停止纪律均命中

git status --short --untracked-files=all -- projects/simulation/explore/cma-fade-divergence/p05_run*.log
?? p05_run.log
?? p05_run2.log
?? p05_run3.log
?? p05_run4.log
```

Fresh-context verifier 初审：`REJECT`，P0/P1/P2=`1/2/0`；修正项为撤销 exact K01 晋级、修正 runner 时序边界、删除未来 V002 预证。修正稿复核：`ACCEPT`，P0/P1/P2=`0/0/0`。

### 结论

PASS

## V003: reference-source expansion 与 defect-reproduction 入口独立验收

> date: 2026-08-08
> 关联：S001 / R002 / D004 / T002

### 验证项

- [x] 恢复与计数：[重读 T002、topic、D001–D004、R001/H002 与 method-production lane] → D002 supersession 边界正确；T001/T002 均为 entry screening，object/package failure=`0/0`。
- [x] 检索 receipt：[核四个 cache JSON、sidecar、SHA256 与 mtime] → 本地优先、4/4 query、requested/actual/error/raw/dedup/kept 与缓存路径齐全；修复未重跑 query。
- [x] 候选与 E1–E8：[逐项核 RML-FSTS/BUM-CMA、共享论文全文/精读笔记、历史 collision] → 两个机制不同候选；C1 八门全过，C2 E2/E4/E7/E8 FAIL。
- [x] 廉价替代与 claim ceiling：[初审提出 P1/P2 后复核] → conditioned single-lag lookup 是最强 cheap comparator，且它仍失败才可 smoke PASS；Yu et al. TVT 2023 identity 补齐，prior art 只限缩 claim。
- [x] 范围纪律：[核 R002/D004/H003/current views 与 Git diff] → terminal 仅为 GW Step 1 defect-reproduction 入口；未写成 defect/Q#/Go/METHOD_SIGNAL/方法，未实现、仿真、运行 smoke 或进入 GW。
- [x] 受保护日志：[SHA256/length/mtime 与启动基线逐项比对] → 四个 `p05_run*.log` 完全一致、未暂存、未进入 diff。

### 证据

Fresh-context verifier 初审：

```text
结论=PARTIAL
P0/P1/P2=0/1/2
P1: global fixed lag 不是最强廉价替代，C1 E4/E7 暂不成立
P2: raw/dedup/source-error receipt 未持久化
P2: external multi-lag prior-art claim 缺 identity
```

修复后同一 verifier fresh-context 复核：

```text
结论=PASS
P0/P1/P2=0/0/0
remaining_findings=none
terminal=ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1 accepted
unique_entry=RML-FSTS accepted
object/package failure=0/0
```

确定性 receipt 复核：

```text
receipt_json_and_cache_hashes=PASS
Q1 sha256=5D93B30A... kept=0
Q2 sha256=DF29DBC3... kept=7
Q3 sha256=55D58532... kept=1
Q4 sha256=9C131227... kept=12
query_rerun=false
```

Git 与日志复核：

```text
git diff --check -> exit 0
git diff --cached --name-only -> [empty]
R001/H002 historical diff -> exit 0
p05_run.log  length=641  sha256=7843B048... mtime=2026-07-30T13:53:16.1107978Z
p05_run2.log length=2417 sha256=735E4650... mtime=2026-07-30T14:08:08.3977355Z
p05_run3.log length=929  sha256=C76887C6... mtime=2026-07-30T14:21:41.1167560Z
p05_run4.log length=1430 sha256=95A1D184... mtime=2026-07-30T14:39:58.3099005Z
```

### 结论

PASS。P0/P1/P2=`0/0/0`。接受 terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1` 与唯一 RML-FSTS 入口；该入口不是 defect、Q#、Go、METHOD_SIGNAL 或方法，下一动作只能从 GW Step 1 开始。
