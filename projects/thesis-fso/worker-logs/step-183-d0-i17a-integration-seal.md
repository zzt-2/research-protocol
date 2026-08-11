# Step 183 — D0 I17A real integration seal

> 2026-08-11 | author implementation | DONE

## 边界

- 只实现 I17A 的真实 cross-component truth/freeze/no-fit seal；未运行真实 benchmark、D0 science、S1–S4、I05 或 action。
- 修改 `verify.py`、`benchmark.py`、CV/DF 两个测试文件；`freeze.py` 仅补足 owner/plan 点名但此前缺失的真实 `fit_b2_tuple` binding。
- 未改 `common/`、owner/session/P05，未 stage/commit/push，未使用 reset/restore/checkout。

## 实际代码

- `verify.DeploymentBoundary.seal(...)` 对 receiver/B0/B1/B2/scorer/artifact/evaluator/benchmark 八个真实 production callable 做 exact identity、module presence、callability 与递归 signature/annotation/closure/nested-type 检查；缺 phase、缺 callable、空 registry、missing module 一律 fail closed。
- seal 使用真实 `receiver.run_common_bps` 和 `estimate_post_bps_residual`，输出 BPS 选择、score、output SHA、canonical receipt bytes/hash；evaluator 只能经 `evaluate_after_seal` 在 seal 后使用 `TruthView`。
- `benchmark.bind_resolved_freeze(...)` 把 benchmark freeze SHA 与 S1/S2/S3_DEV/S3_TEST/S4 五阶段的同一个 `ResolvedDevFreeze` 绑定，receipt 对输入顺序 canonical；缺阶段、错阶段、错 hash、wrong freeze 均拒绝。
- `freeze.fit_b2_tuple(...)` 是现有 `select_b2_tuple(...)` 的真实具名 fit boundary，使三类 fit API 能被 call-graph/runtime tripwire 完整枚举；不新增算法、schema、row、estimand 或 scientific runner。
- DF11 对真实 `contract.finalize_truth_view` 与 `benchmark.py` 同时做 AST 与 runtime tripwire；`fit_common_bps`、`fit_b2_statistics`、`fit_b2_tuple` 均不可达，并拒绝 `importlib/__import__/eval/exec` 绕过。

## RED → GREEN

- RED：CV06–CV08、DF11 focused=`4 failed / 46 deselected in 1.97s`，shell `2.689509s`，exit `1`；失败点分别是缺 `DeploymentBoundary/deployment_callable_registry`、缺 benchmark freeze binding、缺 `fit_b2_tuple`，均为目标 seam 缺失。
- RED output SHA256：`5654d79a765f98b30e6e34a15c85b9d0b41ee9ca3fa4818be07c5b5d2c1f81ef`。
- focused GREEN：同四项=`4 passed / 46 deselected in 2.03s`，shell `2.690332s`，exit `0`；output SHA256=`aa6ef54b416de349a101e428582b044dbefc2ec55c94fe7adc87367ca3df3dd6`。
- fresh 受影响回归：CV+DF+EB 三文件=`78 passed in 37.32s`，shell `37.991864s`，exit `0`；output SHA256=`fb441a6eca484d5850d794c80248e9f8c8a816d5f024c05d7ed7fb4a55ec3ed5`。

## Receipt、负向与 hashes

- real resolved freeze SHA256：`e8a2b25c8124ed4cdb7cf344b8a5441fdb7e27b7078eda5460547157405cb32a`。
- benchmark freeze-binding receipt：198 bytes，SHA256=`dabe8f90fd1da9bc965f72cb3b283f2a27b3c3fa0a58b8f4c742a06a05c4cacf`。
- 新增显式负向 14 类：nested annotation/closure truth leak 2；phase/freeze 4；phase/registry/callable/module 5；三 fit runtime tripwire 3。错收/错拒=`0/0`。
- final SHA256：`verify.py=6c9c3693b7753e2558b7c8d925c83f9e85062ca912fdc1309e5000106535b842`；`benchmark.py=82b9e91c68d85a200c99a67cd15862f288dd2a514034a17c264079c71baa8a1d`；`freeze.py=6425836a744d37963f97d3f6df2346f375bb2e78c1889264f3cffb37f882fe49`；`test_d0_contract_views.py=8dfd50fb16d816e5f0da619355011c991f2c9962cae1d73ac2f772a7c3f327f7`；`test_d0_dev_freeze.py=356a4bc749756026b09bf4910b6f582edfff594aee19a8414f2ef898ed010248`。
- 五个目标文件均通过 fresh in-memory `compile()`；P05 四日志仍仅为原 untracked 状态。

## 裁决

- I17A author gate：CV01–CV09、DF01–DF12 与受影响 EB 回归合计 `78/78 GREEN`；P0/P1=`0/0`。
- D0 science 保持 `NOT_RUN`，method signal 保持 `NONE`；该 author gate 不是独立接收，也不授权 I20 或 science。
- 下一接口：I17A final bytes 进入 Batch 7/I18 fresh deterministic/unit integration；之后按 plan 进入 I19A–D 独立代码审查，均 PASS 前不得运行 12 分钟真实 benchmark。

## P1 fix — authenticated seal-gated evaluator

> 2026-08-11 | reviewer-directed minimal TDD repair | DONE

### Root cause 与最小修复

- Root cause 1：registry 的 evaluator 角色直接指向 `contract.finalize_truth_view`，因此调用方可以不经过 deployment seal 就消费 truth。
- Root cause 2：`DeploymentSeal` 是公开可构造 dataclass，`evaluate_after_seal` 只检查 exact type；公开构造、`object.__new__` 伪造或 `object.__setattr__` 篡改均没有签发身份验证。
- 最小修复只改 `verify.py`：registry evaluator 改为保留真实 evaluator 角色的 `_gated_evaluator`，必须先消费 authenticated `DeploymentSeal`；`DeploymentSeal` 改为 controlled construction，`seal()` 用 weakref-backed issuance registry 签发，并在 evaluator 前验证 object identity、完整字段 fingerprint、canonical receipt bytes/hash、八 callable 与 freeze binding。
- truth 仍只在 `evaluate_after_seal` 后进入 `contract.finalize_truth_view`；不进入 deployable BPS/output/score/receipt 路径。

### RED → GREEN

- RED-A：公开构造伪 seal 被旧代码错收，focused=`1 failed / 20 deselected in 2.43s`，shell `3.279663s`，SHA256=`c3caf3dfacc054c4f7d66b91d97884a84bd8db268e9f8af7e06233849bc818a6`。
- RED-B：pre-seal registry evaluator 直接调用被旧代码错收，focused=`1 failed / 20 deselected in 2.14s`，shell `2.959388s`，SHA256=`bbc042ac180b445464dbf6d123daf2ece9507bf4cd60d5e58014a9936101eed1`。
- focused GREEN：两项=`2 passed / 19 deselected in 2.07s`，shell `2.921675s`，SHA256=`2e2e00735fef9b909e36b5d765d5ed3b5082d0118afb5c8af11af1caae299893`。
- 首轮 CV+DF+EB：`80 passed in 40.61s`，shell `41.402015s`，SHA256=`b197f8db315f03b22ea3c2934128c9f533b5ed1f9adb2a49e4090b69b7fa7639`。
- 将签发逻辑收回 `seal()` 内部、删除独立签发 helper 后，final fresh CV+DF+EB=`80 passed in 40.19s`，shell `41.020823s`，SHA256=`2d84bad566457e86ad9eb3ce058018adfd6e1e2c858b31372971063a699ac9db`。

### 负向、receipt 与裁决

- 新增四类负向：pre-seal evaluator、公开构造、`object.__new__` exact-field forgery、issued-object field tamper；最终错收/错拒=`0/0`。
- authenticated seal receipt：747 bytes，8 callable，SHA256=`37677406cb414b956098043259b2ab6449def5eb76a7af24dbdb37a4f22c4db1`。
- final SHA256：`verify.py=0a174c90147266eb2994e25dcca80294427d8383181c02771add71350d717a7e`；`test_d0_contract_views.py=3bf19c6968449cad1fbc6f135c58c4533158e088d6d6ae5ec7117bcb5583cf5d`。
- P0/P1=`0/0`（author gate）；D0 science=`NOT_RUN`、method signal=`NONE`。未改其他 production/test 文件、common/session/P05，未运行 I05/science/real benchmark，未 stage/commit/push。
