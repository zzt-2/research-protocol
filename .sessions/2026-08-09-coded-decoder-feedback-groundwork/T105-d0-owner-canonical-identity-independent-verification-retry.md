# Task Brief: D0 owner canonical identity contract — transport-corrected independent verification

> 来源: T104/step-150 INCOMPLETE + D015/R001/T103 authority review | 产出位置: `projects/thesis-fso/worker-logs/step-151-d0-owner-canonical-identity-independent-verification-retry.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Scope / corrected rule / terminal

- Fresh复验T104全部必跑项；只写step-151，不改owner/source/tests/session，不跑pytest/science/benchmark/MVE。
- T104因Windows code 206在Python启动前失败，所有checks NOT_RUN；step-150不是owner裁决。
- 权威审查确认：D015/R001/T103冻结解析值deep equality与canonical JSON/root，未禁止YAML alias；T104的“任何alias=P0”是自增规则，撤销。
- 当前owner只允许exact四个tokens：`&id001`定义p_s standalone、`&id002`定义sigma standalone、combined内`*id001/*id002`各一次；禁止任何额外/递归/chained alias。解析后的combined两payload必须与standalone深等并独立复算三root。schema/runtime仍须fresh materialize；owner文档不得原地变异。
- PASS terminal=`OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED`；不宣称I05完成或授权benchmark/science。
- 目标10分钟、12分钟硬停止；任何必跑项未执行即INCOMPLETE。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
old_owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
final_owner=9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d
step149=c69e974e860b5948f44307e51077f7b94ad783a07b4b103db1416af858ab70a8
step150=e54d130d7cc080dddc33616e159e2263324850278489d0ee871896120c458fe7
R001=679e437b052f5b664f2aae1a42f7268482612c396d9a613d6ea6c18e1d285a4d
decisions=376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0
verifications=16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step147=a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f
step148=c089a52190988b7695e6df66a153984ef1bf06f8ade98132a63145490eea31af
```

## Mandatory transport（先选定，不得再塞入命令行）

1. 用`apply_patch`创建step-151，先写完整独立verifier源码于：

````text
<!-- verifier:start -->
```python
...
```
<!-- verifier:end -->
````

2. PowerShell从step-151正则提取fence内容，经stdin pipe到`python.exe -B -`；源码不得出现在shell command参数。
3. 保存exit code、完整stdout与stdout SHA；再仅用`apply_patch`回填同一step-151。不得创建临时脚本或第三文件。

## Fresh verifier requirements

单进程只用stdlib/PyYAML/NumPy 2.4.3；禁止导入schemas/author helper、禁止用step-149 PASS数据当断言。assertions `>=240`。

### A. Parser / placement / projection / permission

- duplicate-key SafeLoader；token/event scan精确验证上面2 anchors+2 aliases且仅在指定路径；无额外/递归/chained alias。
- exact block一次、无leading `+`，位置`statistical_contract_repair < identity_binding_contract < strata`；13个top-level sections及header exact。
- raw删除identity block后bytes SHA=`c61c88e...de7d`，strict parsed projection与new doc pop后深等。
- epoch12/CP012/action、implementation/unit/engineering true、execution/scientific false、not_mve/not_c1_extension与science-change none均无漂移。此组漂移=P0。

### B. 128 literals / roots / schemas / placeholders

- 独立NumPy 2.4.3生成122+6 literal，128项逐项assert；index/keys/canonical lowercase hex/finite/strict increasing/no negative-zero/duplicate/JSON float/anchors。
- 独立构造standalone和combined，combined parsed payload深等；canonical规则exact；三个root exact。
- 所有payload domain/version/field order/typed atom、preexecution/runtime boundary、validator obligations exact。
- 递归拒绝placeholder/TODO/TBD/UNKNOWN/FILL_ME/OMITTED/PENDING/ellipsis/非法空值。

### C. Fresh goldens / mutations

- 从raw inputs自行重建owner全部8个golden classes：grid三个subvectors、clean10、target90、sentinel90→clean、M3_N100→M2 direct、S2 nine-to-one、BPS dual-pol、runtime exact-sum；不能只hash owner payload。
- 至少12/12 mutation：member replacement/order、group cell/role/grid、hex、runtime manifest/content、cache chain/source-content、logical-ID吞并、S2 swap/orphan/extra、X/Y charge；均改变root或被义务明确拒绝。

### D. Counts / protection / verdict

- 六式必须6/6：263520、22800、16689600、9600、7027200、13200；无group/pair ledger，X732/Y0，per trajectory732，EXECUTED-only，8344800旧owner交叉一致。
- begin/end owner SHA、HEAD/staging、全部frozen hashes、P05四值、cache `202/41/4`、diff-check=0。
- 必须记录assertions/literals/roots/goldens/mutations/counts/mismatch、permission/projection/alias/protection、P0/P1/P2。
- 仅`mismatch=0`、goldens全过、mutations>=12/12、counts6/6、P0/P1/P2=0/0/0可PASS；执行不全则INCOMPLETE。

## Environment / return

Windows Python 3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；不得install/commit/push/stage。返回terminal、数字、owner/step151 SHA与写入路径。
