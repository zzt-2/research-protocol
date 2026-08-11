# [R001] D0 HMM / consumer-ledger canonical identity binding

> 2026-08-10 | 关联：2026-08-09-coded-decoder-feedback-groundwork / D015

## 调研问题

为关闭step-134剩余P1，确定`p_s/sigma` binary64 identity、HMM member/group/computation roots、consumer PK→ledger绑定与cache source的唯一可执行语义；特别回答`b2_hmm_grid_chunk.computation_ids_manifest_sha256`应绑定group aggregate、member computations还是二者分层。

## 发现

### 已有owner语义与真实缺口

owner已经冻结数学网格`{0}∪logspace(1e-7,1e-1,121)`、6项sigma、canonical JSON通则、HMM chunk PK与float-hex字段、clean/target/sentinel成员数`10/90/90`、trajectory先归一化后binary64 exact-sum、sentinel仅排除objective而不删receipt/cost、CACHE_READ source/content/materialized规则、controlled sentinel绑定clean source content、S2 off九行共享、BPS duplicate-N共享及logical/materialized HMM总量。

缺口是identity而非科学语义：122项binary64字节承诺、domain-separated payload/root、member canonical order、chunk→logical computation IDs、consumer PK→ledger公式、HMM ledger粒度、N100 exact source方向、cache chain规则与dual-pol accounting owner均未定义。当前`schemas.py`的opaque namespace hash与管道拼串不能关闭等量替换或same-phase exchange。

### 独立复算的binary64 commitments

生成规则仅用于建立literal authority：NumPy 2.4.3 `float64`，`[0.0] + logspace(-7,-1,121,endpoint=True,base=10)`；runtime authority是owner中122个canonical `float.hex()` literals及root，不重新依赖NumPy计算。

```text
p_s[0]=0x0.0p+0
p_s[1]=0x1.ad7f29abcaf48p-24
p_s[61]=0x1.a36e2eb1c432dp-14
p_s[121]=0x1.999999999999ap-4
p_s_grid_sha256=bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864
sigma_grid_sha256=0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca
combined_grid_sha256=0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf
```

Canonical bytes：UTF-8，`sort_keys=true`、`separators=(",",":")`、`ensure_ascii=false`、`allow_nan=false`、无尾换行；identity payload禁止JSON float，浮点只用canonical hex string，拒绝alternative spelling、`-0.0`、NaN/Inf、重复与非严格递增。

三个commitment的exact payload shape如下；`values`均按`index`升序，分别填入全部122项与6项literal，不使用省略项或运行时重算值：

```json
{
  "schema": "coded_decoder_feedback.d0.float64_grid.v1",
  "name": "p_s",
  "values": [{"index": 0, "float64_hex": "0x0.0p+0"}]
}
```

sigma payload与上式同构，`name="sigma_e2"`。combined payload把两份完整standalone payload原样嵌套：

```json
{
  "schema": "coded_decoder_feedback.d0.hmm_grid_commitment.v1",
  "p_s": {"schema": "coded_decoder_feedback.d0.float64_grid.v1", "name": "p_s", "values": []},
  "sigma_e2": {"schema": "coded_decoder_feedback.d0.float64_grid.v1", "name": "sigma_e2", "values": []}
}
```

上面两个空数组仅表示嵌套位置；实际commitment必须与standalone payload的完整`values`深等。该shape从历史原始工具记录恢复：`rollout-2026-08-10T15-58-54-019feaae-7543-72e0-a6fb-2b38dd214d0e.jsonl`，tool-call `2026-08-10T10:18:21.628Z`构造`combo={'schema':'coded_decoder_feedback.d0.hmm_grid_commitment.v1','p_s':po,'sigma_e2':so}`，紧随的`2026-08-10T10:18:22.378Z`输出对三个冻结root均为PASS。T102/step-148再次fresh复算三个root，结果仍为PASS；因此保留既有root，不生成新root。

### 分层HMM computation binding

选择“group envelope + ordered member logical computations”二层，但不新增cost-bearing group aggregate ledger row：

- `b2_hmm_grid_chunk`本身是group aggregate receipt。
- `member_key_manifest_sha256`绑定chunk consumer PK、按owner轴排序的10/90个typed raw-row PK与ordinal。
- `computation_ids_manifest_sha256`绑定chunk PK、p/sigma index+hex、pilot count、exact-sum algorithm、member count，以及每个member的logical computation ID/cache status/source ID。
- `content_sha256`在runtime另绑定computation manifest root、resolved member content hashes、exact numerator/denominator与member count；preexecution root不包含运行后才知道的content。
- HMM ledger粒度是一条per-pol trajectory的完整`122×6` grid logical computation，共22,800条；不建立16,689,600条parameter-pair ledger，也不另建263,520条group aggregate ledger。

Member order：clean=`seed`；target/sentinel=`seed→fixture owner legal order`。Outer envelope包含完整group/grid identity，禁止相同member list跨grid/role/cell迁移。

### Cache/source与计数

新增direct-to-executed规则：

1. N100 canonical materialization owner是legal-order较早的`M2_N100`。
2. `M3_N100` HMM trajectory logical IDs保留，但CACHE_READ直接指向相同physical-content key的`M2_N100` executed computation。
3. sentinel先规范化到同seed/cell/row-pol的clean content，再做N100规范化；`M3_N100 sentinel`直接指向`M2_N100 clean`。
4. source必须是EXECUTED根，禁止cache chain；logical ID不得被source ID替代。
5. physical-content key排除M、logical tuple label和sentinel fixture；保留N/seed/cell/row-pol，controlled target另保留target-pol与fixture。此复用仅限HMM/BPS等content-identical路径，禁止跨M复用downstream B2 decode。

```text
chunks=5*122*6*3*12*2=263,520
logical trajectory-grid ledger rows=5*10*12*2*(1+9+9)=22,800
logical primitive scores=22,800*732=16,689,600
executed trajectory-grid rows=4*10*12*2*(1+9)=9,600
materialized primitive scores=9,600*732=7,027,200
cache trajectory rows=13,200
```

Dual-pol accounting由X作为pair-charge owner：每对X行记732 dual-pol scores、Y行记0；每条logical trajectory行均记732 primitive scores，materialized总量只汇总EXECUTED。由此`11,400*732=8,344,800`。

### Consumer-PK→ledger

普通consumer plan必须冻结`(table, exact typed PK)→logical computation ID`：S2 off省略fixture并由B04 canonical owner实现nine-to-one；S2 on保留fixture/method；S3保留split/seed/cell/target/fixture/candidate；BPS省略polarization；B2 clean省略polarization；B2 controlled省略row polarization；HMM绑定chunk PK→computation manifest root；S4保持显式standalone plan。Validator同时检查正向binding、ledger identity/source/content与reverse coverage，same-phase ID交换必须拒绝。

`consumer_binding_manifest.binding_kind`是hash-bearing字段，所有上述consumer→logical-computation绑定统一冻结为exact literal `LOGICAL_COMPUTATION_ID`。该值必须同时出现在projection authority与每个golden raw inputs中，不能只隐含在author脚本。以该literal复算S2 off nine-to-one与BPS dual-pol两个既有golden，roots分别精确命中`ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6`与`51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f`。

## 结论

`computation_ids_manifest_sha256`不能只绑定单个group ID，也不能只绑定无group envelope的member IDs。采用分层payload与22,800条trajectory-grid ledger既能完整表达10/90成员、cache provenance和logical exposure，又保持ledger规模有界并精确复现owner总量。

## 对决策的影响

需要D015 additive identity closure，并在schema实现前把完整payload/schema/cache/accounting规则写入唯一owner `d0-defect-smoke-contract.yaml`。这是implementation-contract closure：scientific population/seed/grid数学值/gate/estimand/exposure totals不变；raw FULL positive与运行时content仍须后续TDD/独立验证。

## 2026-08-10 续接：compiler-readiness gap

T108–T109先把owner identity变为可重验证的typed immutable view：strict RED 4/4后，独立验收为430 assertions、31/31 mutations、四文件52/52与I06 mismatch=0。该结果证明loader边界闭合，但不证明owner每个projection已能唯一生成logical ID。

两路后续只读审查逐字段发现：ordinary S2_on/S3/B2_clean/B2_controlled/S4没有owner-owned `work_key.kind`，phase/operation只在实现代码；S2_off/BPS也仅由历史golden verifier隐含完整三元组。更进一步，typed consumer PK的atom types未逐projection冻结。HMM则是另一种引用：raw chunk字段持有`computation_ids_manifest_sha256`，不能用字段名为`logical_computation_id`的consumer-binding payload解释。

因此D017补齐七类ordinary projection的consumer PK/work-key typed descriptors与phase/operation规则，并把HMM单列为manifest reference。静态规模锚点为：ordinary projections=7、HMM reference=1、work descriptors=32、consumer-PK descriptors=41/49、unique phase-operation signatures=8、ordinary bindings/logical IDs=`42,967/27,487`、HMM logical/chunk roots=`22,800/263,520`、ledger total=`50,287`。现有S2_off/BPS/HMM roots均不得漂移；不新增golden root，完整枚举由后续independent FULL oracle关闭。

该补充只改变identity authority bytes，不改变scientific population/seed/grid/gate/estimand、22,800 ledger粒度、logical/materialized totals或CP012权限。
