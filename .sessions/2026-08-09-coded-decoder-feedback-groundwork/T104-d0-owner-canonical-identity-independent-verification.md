# Task Brief: D0 owner canonical identity contract — independent verification

> 来源: T103 final bytes / D015 / R001 | 产出位置: `projects/thesis-fso/worker-logs/step-150-d0-owner-canonical-identity-independent-verification.md`
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

## Independence / scope / terminal

- Fresh独立验收最终owner字节；禁止导入`schemas.py`、author helper或把step-149结论当证据。
- 只允许创建step-150；owner/source/tests/session均只读，不跑pytest/science/benchmark/MVE。
- PASS仅为`OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED`；不宣称I05完成或授权science。
- 目标10分钟、12分钟硬停止；任一必跑检查未完成即INCOMPLETE。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
old_owner_sha256=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
final_owner_sha256=9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d
step-149=c69e974e860b5948f44307e51077f7b94ad783a07b4b103db1416af858ab70a8
R001=679e437b052f5b664f2aae1a42f7268482612c396d9a613d6ea6c18e1d285a4d
decisions=376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0
verifications=16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f
step-148=c089a52190988b7695e6df66a153984ef1bf06f8ade98132a63145490eea31af
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
test_schemas=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step-147=a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f
```

## One fresh verifier program

用单个独立Python程序从YAML/raw owner输入复算；只可用stdlib、PyYAML和NumPy 2.4.3。不得读取step-149里的PASS数字驱动断言。总assertions `>=240`，记录命令、exit code、stdout SHA、分组数字。

### A. Parser / placement / old projection / permission（任一漂移=P0）

1. SafeLoader在`flatten_mapping`后逐键拒绝duplicate；YAML event扫描拒绝alias。
2. 文本恰有一个exact `identity_binding_contract:`，且`statistical_contract_repair < identity_binding_contract < strata`；禁止`+identity_binding_contract`。
3. header exact：schema v1、D015、science change none；13个top-level identity sections精确为当前owner定义，不许未知额外项。
4. 从raw新owner删除identity block，所得bytes SHA须等于old owner `c61c88e...de7d`；其strict parse与`deepcopy(new_doc).pop(...)`深等。
5. epoch/checkpoint/action、implementation/unit/engineering=true、execution/scientific=false、not_mve/not_c1_extension与statistical science-change=none全部保持。

### B. 128 literals / three roots

- 独立以NumPy 2.4.3 float64生成`[0]+logspace(-7,-1,121)`及`[0,1e-5,1e-4,1e-3,1e-2,1e-1]`；128项逐项单独计assertion。
- 精确检查index、entry keys、canonical lowercase `float.hex()`、finite、strict increasing、无negative-zero/duplicate/JSON float及四anchors。
- 独立构造两份standalone payload；combined必须嵌套二者深等。canonical UTF-8 JSON规则exact，无尾换行。
- roots精确为`bfc3...78864`、`0f37...01ca`、`0cdb...99fdf`。

### C. Payload schemas / obligations

- 对consumer PK、typed work key、HMM group/member/computation、logical computation、computation manifest、consumer binding manifest、runtime aggregate逐项冻结exact domain/version与field-order，字段无重复且payload keys一一对应。
- typed atom仅`str/int/bool/none/float64_hex`，bool不能冒充int，none仅null；preexecution禁止runtime content，runtime必须绑定manifest、ordered content、exact numerator/denominator/member count。
- 递归拒绝TODO/TBD/UNKNOWN/PLACEHOLDER/FILL_ME/OMITTED/EXAMPLE_ONLY/PENDING、ellipsis、`<...>`、`{placeholder}`与非法空schema/version/field-order/golden。
- validator obligations必须显式覆盖literal/root/field-order/type/domain/version/count/direct source/content/logical/materialized/reverse及所有冻结mutation。

### D. Fresh golden recomputation（不能只hash owner payload）

从每个golden的raw inputs自行重建payload、canonical JSON与SHA，检查：三个grid sub-vectors、clean10、target90、sentinel90→clean、M3_N100→M2 direct、S2 off nine-to-one、BPS dual-pol shared、runtime clean10 exact-sum。要求owner的8个golden classes全部通过且上述subcases无遗漏。

至少12个fresh mutation：等量member替换、ordinal/member顺序交换、group cell/role/grid迁移、hex交换、runtime manifest/content篡改、intermediate source chain、source/content不等、logical ID吞并、S2 same-phase swap/orphan/extra、X/Y charge owner交换；每项必须改变root或被明确拒绝。

### E. Counts / accounting

独立复算并与旧owner交叉：

```text
5*122*6*3*12*2=263520
5*10*12*2*(1+9+9)=22800
22800*122*6=16689600
4*10*12*2*(1+9)=9600
9600*122*6=7027200
22800-9600=13200
```

另断言无cost group row、无pair ledger；X=732/Y=0；per logical trajectory=732；materialized仅EXECUTED；`11400*732=8344800`与旧owner一致。

### F. Protection / verdict

- 开始与结束final owner SHA相同；HEAD/staging/frozen hashes/P05四值/cache census=`202/41/4`不变；`git diff --check=0`。
- owner并发变化→`INCOMPLETE_CONCURRENT_OWNER_CHANGE`。
- golden全部、mutations至少12/12、counts 6/6、mismatch=0且P0/P1/P2=0/0/0才PASS。
- P0：parser/old projection/science permission/HEAD/staging/P05漂移；P1：identity、root、schema、golden、binding、cache、count、accounting、placeholder任一缺口；P2：日志缺命令/exit/stdout SHA/分项/final SHA。

## Environment / writes

Windows Python 3.11；`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`。只写step-150；不得install/commit/push/stage。

## Return

verdict、P0/P1/P2、assertions、literal/root/golden/mutation/count/drift/protection数字、final owner与step-150 SHA。
