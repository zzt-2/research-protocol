# Task Brief: CP011 / D010 / V004 D0 限权治理 verifier

> 来源: S001 / D010 / V004 / H003 | 产出位置: `projects/thesis-fso/worker-logs/step-092-cp011-d0-governance-verifier.md`
> 日期: 2026-08-10
> 唯一任务文档: 执行方按本 T046 核验治理转移，只读当前 owner 与 step-090/091

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR（执行方先读）

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，fresh-context 验证 A0 `PASS` 后从 CP010 到 CP011 的治理转移是否完整、无矛盾、只开放 D0。

**任务**：核验 D010/V004/CP011/H003、topic/master/registry/S001/mission/voice、report/YAML control metadata 与禁止边界。不要重审 step-090/091 已关闭的 scientific design；只检查治理投影是否诚实消费其结论。

**产出**：只写 `projects/thesis-fso/worker-logs/step-092-cp011-d0-governance-verifier.md`。

**时间纪律**：6–8 分钟目标，12 分钟硬上限；到限立即裁决。

**最高纪律**：

1. 禁止修改任何 owner/治理/源码/protected logs；禁止 D0 实现/测试/运行、web/search/download、仿真、adapter、MVE、commit/push。
2. PASS 必须 P0/P1/P2=`0/0/0`。发现矛盾只报告最小修复，不代改。
3. step-091 的科学快照 PASS 只允许 D/V/CP 开 D0；不得把 A0 写成 Step 4a Go、方法信号或贡献。

## 1. 背景与冻结事实

- step-090：`FAIL / 0/2/1`，大部分全量合同已 CLOSED。
- step-091：`PASS / 0/0/0`，P1-1/P1-2/P2-1 全部 CLOSED；旧科学快照 report=`046bb45a...f27`、YAML=`6c1e228f...a4b`。
- 本次只允许 control metadata/审查历史/授权投影变化；D0 的 strata、seeds、B2 tuples、estimands、thresholds、bootstrap、fusion、budget 与 post-D0 boundary 不得被治理转移改写。
- 当前方法信号必须仍为 NONE，D0 必须仍为 NOT_RUN。

本次治理快照 SHA256：

```text
report=0e335d1770402f5eab188801c1fc008e5abe0d3858d839b490736177daae4c4d
yaml=28ceabf78c1aa48925cfbf19131350024f4fcdcc7c2bd0cb0534d54e617a7e84
topic=37d795e2cd58283215b556f4a012ec73fbab2d967dd0e6829eb0bc15cd92a70d
decisions=c066b7f14d230b37026519a197c7c260b54551012e5a686432ced967daec29de
verifications=d4967104b0083101c946ff6165d367b3f8b3a27018c706ed4fecfed3cfc2ef5b
H003=059b7210b92f4bebe294b4231851b138da526775daf06b0052cc28f36d58dc28
S001=4ab523736c64591532647aa79bcf6c64dceef25a96f365ac9d2ac5b449992f19
mission=2369908292c26ef68464aac988162e52dbdd0ecc1ff41f19d5adbad76a098baf
master=46aeefaf2ee8f1cfa2e70cfd76d1d975746efe11cb26c3535c5f1b40ae0c342d
registry=1ef6ef6481dbb3ab2fd9cf3e22d4b2c7fefbf106853a65585ffb7a1a708aecdb
voice=852d152e5539d136607d4ade8572d9c82a908f9ab06e6a837d94a0e434c41209
```

## 2. 必审问题

1. T046 task-control 是否对 CP011/epoch11/`CONTRACT_STATIC_CHECK` PASS。
2. topic control、YAML control、report header/output、master bridge、mission CP011 是否一致为：
   - lane=`GROUNDWORK_STEP4A_D0_DEFECT_SMOKE`；
   - D0 authorized / NOT_RUN；
   - allowed 只含 D0 implementation/unit test/defect smoke/source/static check；
   - adapter/C1 policy/MVE/held-out/non-D0 experiment/Contract/Execute/thesis claim 禁止。
3. YAML 可 parse；control 恰为 epoch11/CP011/DEFECT_SMOKE/D010/V004/两个 authorization true；`purpose.not_mve=true`、`purpose.not_c1_extension=true`，其余 scientific contract 与 step-091 接受边界一致。
4. report 不再同时写 `execution_authorized=false` 或 re-verification pending；`D0_EXECUTION_AUTHORIZED=YES / D010+V004+CP011 ONLY`，同时明确 post-D0 safety 与最终 MVE/Step4a Go 仍未完成。
5. D010 是否含 status/date/取代/被取代/依据/决策/理由/排除方案/影响/触发原话/来源；是否与 D009 冲突；是否把任一 D0 gate 失败定为 C1 terminal，而非放宽门槛。
6. V004 是否按 V 模板、编号顺序 001→004，诚实保留 step-090 FAIL 和 step-091 PASS；历史 `D0_EXECUTION_AUTHORIZED=NO` 是否明确只指治理转移前。
7. H003 是否含 AGENTS 强制 anchors：已完成边界、不要做什么、必读、接口变更、失败数据、已知债务、验证阈值、接收方验证、下一轮；checkbox 必须未预勾。
8. S001、mission、master、registry、topic 当前状态/未决项/当前位置与 D010/V004/CP011 一致；voice 的三条 D010 原话必须能在用户原始合同中逐字找到。
9. scope 未扩大：仍在原始 3–7 日 C1 reference-extension/D0 范围；不新建平行专题，不修改 `common/`，p05 仍受保护。
10. `git diff --check` 无错误；staging empty；治理 owner 初末 SHA 11/11 不漂移；p05 4/4 正确。

## 3. 产出格式（强制）

```markdown
# Step 092 — CP011 D0 governance verifier

> control / scope / no-experiment receipt

## 1. Verdict
PASS/FAIL；P0/P1/P2=x/y/z。

## 2. Control projection matrix
topic/YAML/report/master/mission/registry。

## 3. D/V/H/session governance checks
D010、V004、H003、S001、voice、编号/anchors。

## 4. Scientific-ceiling and authorization checks
A0 ceiling、D0 NOT_RUN、method NONE、post-D0/MVE forbidden。

## 5. Findings
行号+影响+最小修正；无则明确0。

## 6. Disposition
允许主控进入 D0 preflight/implementation，或维持 CP011 修复；本日志不运行 D0。

## 7. Protection receipt
11 owner 初末 SHA、p05 4 SHA、staging、唯一写入、禁止动作。
```

## 4. 已知陷阱

1. V004 引用的 `D0_EXECUTION_AUTHORIZED=NO` 是 step-091 在治理转移前的原始证据，不是当前投影；不能因此误判当前矛盾。
2. report/YAML 当前 hash 与 step-091 旧快照不同是预期的 control metadata 变更；重点是 scientific contract 不漂移。
3. D0 是受控 scientific diagnostic，但不是 MVE、C1-ext 或 held-out；不要用“scientific experiment authorized=true”扩大成非 D0 实验。
4. 历史 CP010/D009/step-091 文本可保留在明确 history/evidence 位置，不得要求抹除审计历史。

## 5. 验收

- [ ] task-control PASS，YAML parse，control projection 无矛盾。
- [ ] D/V/H/session/master/registry 完整；V 顺序正确、H anchors齐全。
- [ ] A0 ceiling 与 D0/post-D0/MVE 边界无越级。
- [ ] PASS 时 P0/P1/P2=`0/0/0`。
- [ ] 11 owner SHA、p05 4/4、staging empty、唯一新写 step-092。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-092-cp011-d0-governance-verifier.md`
