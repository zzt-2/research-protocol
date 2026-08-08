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
