# Step 182 — D0 I16 engineering benchmark manifest and slices

> 2026-08-11 | author implementation | DONE

## 边界

- 只新增 `projects/simulation/explore/coded-decoder-feedback/benchmark.py`、`projects/simulation/tests/test_d0_engineering_benchmark.py` 与本 worker log。
- 未运行真实 benchmark、D0 science、S1–S4、I05、seed 注册或 fit；未修改 `common/`、owner、session、P05 日志及其他 production/test 文件。
- 未 stage/commit/push，未使用 reset/restore/checkout。

## 实际代码

- 新增 engineering-only frozen manifest：class=`ENGINEERING_THROUGHPUT_V1`、root seed=`900000001`、显式 synthetic `ResolvedDevFreeze`、四种 decoder batch、六组 BPS、十个 B2 view 与四项 owner slice。
- 新增 fake-worker-friendly `run_engineering_benchmark(...)` 注入边界；I16 不提供 live worker/CLI，不会自行运行真实 720 秒 benchmark。
- decoder slice 强制 `{4,8,12,16}` 且每次 fresh restart；BPS 只构造一个 waveform 并对同一对象跑六组 `(B,Nw)`；B2 要求十个内容 hash 全唯一。
- HMM 保留 primitive binary64 scores，以 `Fraction.from_float` 的 integer/power-of-two exact aggregate 汇总；benchmark API 没有 ordinary-float aggregate 入口。
- representative rows 通过现有 `write_jsonl_atomic` 真正落盘，返回 landed bytes/rows/hash/directory-fsync receipt。

## RED → GREEN

- RED command：`C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest projects/simulation/tests/test_d0_engineering_benchmark.py -q -p no:cacheprovider`。
- RED：`6 errors in 2.76s`，shell stopwatch `3.9104904s`，exit `1`；六项均在 I16 module import 处得到预期 `ModuleNotFoundError: No module named 'benchmark'`，不是 syntax/fixture/path/dependency error。
- RED output SHA256：`2d402ac08fd1146123c3ea3072b4a62b178785983148bd2c10083d4d2c2b1478`。
- 首轮 GREEN：同命令 `6 passed in 2.61s`，shell stopwatch `3.5971551s`，exit `0`。
- GREEN output SHA256：`c103d1cb53683c115444621d5a8a10be2808b4d685a7987833e41ff179e762f7`。
- 最终 fresh：两个目标文件 in-memory `compile()` + EB01–EB06 整文件，`6 passed in 2.89s`，合并 stopwatch `4.0609578s`，exit `0`；未执行真实 benchmark。

## 接收证据

- owner SHA256：`f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`。
- `benchmark.py` SHA256：`0303b63490884add20c41d44a9a9250a3e7d959a748a5b54a09c9ba70524e1ef`。
- `test_d0_engineering_benchmark.py` SHA256：`4654a3cdb2fb7e49b471dad91222904a7e73a4ffb504b73b68dd7a1a11237a95`。
- 静态负向扫描：`fit_|raw_s[1-4]|estimand|gate_conjunction|scientific_verdict|defect_smoke|message_state|warm_state` 在 `benchmark.py` 为 `0 hits`。
- 动态负向：EB01 证明 seed `900000001` 被 frozen registry 明确拒绝，并断言 5 个 scientific/schema 字段不存在；wrong accept/reject=`0/0`。
- 环境：Windows Python 3.11 固定解释器；`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、`-B`、`-p no:cacheprovider`。

## 裁决

- I16 author gate：EB01–EB06=`6/6 GREEN`；P0/P1=`0/0`。这不是独立验收，也不授权真实 benchmark 或 science。
- D0 science 保持 `NOT_RUN`，method signal 保持 `NONE`。
- 下一接口：I16 final bytes 进入本批唯一合并独立验收；PASS 后按 plan 继续 I17 watchdog/full-work projection/no-science receipt 的真实代码 TDD。

## I17 continuation — watchdog, full-work projection and no-science receipt

> 2026-08-11 | same-file serial author implementation | DONE

### 实际代码

- 新增 fake-clock `watchdog_call`：`elapsed >= 720s` 一律 `INCOMPLETE`，丢弃 partial value；`write_benchmark_receipt` 拒绝覆盖 incomplete receipt，旧证据保持原字节。
- 新增 `FullWorkProjection`：冻结 logical=`69,360 / 1,032,000 / 20,640,000` 与 HMM=`8,344,800 / 16,689,600 / 7,027,200` 六轴，缺轴/改数均拒绝；四种 allowed adjustment 只能改变 materialized counts，logical keys/count/hash 不变，message-state reuse 无合法入口。
- 新增 `BenchmarkReceipt`、canonical receipt document 与 atomic JSONL writer；完整性门同时检查四项 I16 slices、owner 八项 runtime record、六个 D0 line-item completed/remaining partition 与 watchdog。
- 预算公式逐字实现：`projected_D0_days=consumed+remaining`；`contingency_consumed=max(0,projected_D0_days-4.50)`；`required_remaining_contingency=0.50-contingency_consumed`；`projected_mission=consumed+remaining+2.00+required_remaining_contingency`。`required_remaining_contingency<0` 或 mission `>7.00` 才是 `GREATER_THAN_7D_HARD_BLOCKER`；缺 slice/record/partition/timeout 优先 `INCOMPLETE`。
- 新增冻结 CLI parser：只接受 I20 命令的 class/root-seed/720s/synthetic-freeze/output；默认没有 real runner，因而 I17 不会意外执行真实 benchmark。

### RED → GREEN

- RED：EB01–EB06 保持通过，EB07–EB11 因五个目标 API 缺失得到 `5 failed / 6 passed in 5.31s`，shell stopwatch `6.6972149s`，exit `1`。
- RED output SHA256：`4cd280163290655f00fa2e92bf260564c07bb76fa013ec24aeeab320f6e8d30e`。
- GREEN：同一整文件命令 `11 passed in 3.34s`，shell stopwatch `4.3841667s`，exit `0`。
- GREEN output SHA256：`f77e03afc1050fe8510fc0185dd99a495dff50766284aca4da1a088124c2f348`。
- 最终 fresh：两个目标文件 in-memory `compile()` + EB01–EB11 整文件，`11 passed in 3.45s`，合并 stopwatch `4.4322316s`，exit `0`。

### 接收证据与负向

- final `benchmark.py` SHA256：`d3879a1a7484600c82e0b42e3e9fc007c76b36fb905f46293f14f005c800da17`。
- final `test_d0_engineering_benchmark.py` SHA256：`cb23feb9dc8cf677266f564be84668a11ed10a1fe6ddefe4f523e4ff8c315916`。
- 负向动态 5 类：`721s timeout`、full-work 缺轴、forbidden state-reuse adjustment、`5.1d` negative remaining contingency、owner record 缺字段；错收/错拒=`0/0`。
- 静态禁止词 `fit_|raw_s[1-4]|estimand|gate_conjunction|scientific_verdict|defect_smoke|message_state|warm_state` 在 final `benchmark.py` 为 `0 hits`。
- 未运行真实 benchmark/science/I05，未改其他文件、common/session/owner/P05，未 stage/commit/push。

### 裁决

- I17 author gate：EB01–EB11=`11/11 GREEN`；P0/P1=`0/0`。D0 science 仍 `NOT_RUN`，method signal 仍 `NONE`。
- 下一接口：I16+I17 final bytes 进入本批唯一独立合并验收；PASS 后由 plan I17A 绑定真实 cross-component truth/freeze/no-fit seal，不得提前运行 I20。

## Batch 6 P1 fix — strict owner record and projection binding

> 2026-08-11 | reviewer-directed minimal TDD repair | DONE

### Root cause 与修复

- Root cause：`build_benchmark_receipt` 仅比较八个 owner record key，未验证 value type/finite/nonnegative；`projected_full_D0_time` 也未与六个 line-item 的 `consumed + remaining` 绑定，因此 `100*86400`、NaN、negative/bool 等值仍可进入 PASS。
- 最小修复：新增 strict record validator。`device` 必须 non-empty exact string；`dependency_versions` 必须 non-empty string→string mapping；四个计数字段必须 exact nonnegative int（bool 拒绝）；`wall_time/projected_full_D0_time` 必须 exact int/float、finite、nonnegative。
- projection binding：`projected_full_D0_time == projected_D0_days * 86400`，其中 `projected_D0_days = consumed_engineering_days + projected_remaining_D0_days`；不再把已耗时间重复放入 remaining。字段完整但数值非法=`INVALID_OWNER_RECORD/INCOMPLETE`；projection 与 line-item 不一致=`PROJECTED_FULL_D0_TIME_MISMATCH/INCOMPLETE`；一致且 `required_remaining_contingency_days<0` 仍为 hard blocker。exact 7.00d 保持 PASS。

### RED → GREEN

- RED：EB01–EB09/EB11 保持通过；原实现错收 projection mismatch 与 17 个非法 owner values，得到 `18 failed / 10 passed in 5.01s`，shell stopwatch `5.7008067s`，exit `1`。
- RED output SHA256：`b8de2e162e81e0e527bae2f2f4f73c83faaa430093ece67ec36abfb1243e116c`。
- GREEN：EB01–EB11 参数化整文件 `28 passed in 4.75s`，shell stopwatch `5.4061634s`，exit `0`。
- GREEN output SHA256：`225175c312b60dc924acf527f126a0fd867bb34e7465fdfbcafaca8d2cea54bf`。
- final fresh：两个目标文件 in-memory compile + 整文件 `28 passed in 4.70s`，shell stopwatch `5.3565178s`，exit `0`。

### 负向与 hashes

- 新增 18 项负向：projection mismatch 1；empty/wrong device 2；dependency mapping/wrong value 2；negative/bool/wrong-type integer fields 6；NaN/Inf/bool/negative numeric fields 7。最终 wrong accept/reject=`0/0`。
- exact 4.50d 与 exact 5.00d/7.00 mission 保持 PASS；5.10d 且 projection 一致保持 `GREATER_THAN_7D_HARD_BLOCKER`；缺字段保持 `INCOMPLETE`。
- final `benchmark.py` SHA256：`87b752553529a814ab7515644526bf756b9de72dc643fd3bb33e143eef6f477f`。
- final `test_d0_engineering_benchmark.py` SHA256：`d79f2899460ce27fc36123a12538eefe3b00d14961d0a950c552c2772212253c`。
- 禁止词扫描仍为 `0 hits`；未运行真实 benchmark/I05/science，未改其他文件/common/session/owner/P05，未 stage/commit/push。

### 裁决

- Batch 6 P1 CLOSED；author P0/P1=`0/0`。下一接口仍是受影响 benchmark shard 的唯一 fresh 独立合并验收，未授权 I20/science。

## Batch 6 exact-binding P1 fix

> 2026-08-11 | reviewer-directed one-line production repair | DONE

- Root cause：`PROJECTED_FULL_D0_TIME` binding 使用 `math.isclose(..., abs_tol=1e-6)`，因此 owner record=`expected + 5e-7` 被错收。
- RED：新增 binary64 微扰负向后 focused EB10=`1 failed in 0.52s`，shell stopwatch `1.1767667s`，exit `1`；output SHA256=`7dc77363a3b18ad038b253aaf44ac1793d68ec44535bf410735dc41da5722a65`。
- 最小修复：两侧都按 `float(...).hex()` 规范化后 exact equality；删除全部容差，不改预算、状态或其他 validation 逻辑。
- focused GREEN：`1 passed in 0.44s`，shell stopwatch `1.0780104s`，output SHA256=`9b02778cb61c4d7ef3caacf0ec35ddbaafd17d7639685d1455f4c565adfd0c88`。
- final fresh：in-memory compile + EB01–EB11 参数化整文件=`28 passed in 4.85s`，shell stopwatch `5.6502239s`，output SHA256=`d18fc0ea9b524db260abad66d28b6f98081dd5b26eeee5e2fcb1ed8a0e1b8b79`。
- 该微扰负向最终错收/错拒=`0/0`；P0/P1=`0/0`（author gate）。
- final `benchmark.py` SHA256=`d1cd43038d8604f233092266be683a62b37a5dbd8ab331daa126dc5334ea74c8`；test SHA256=`cb852c61f63572e09186f9e8472ca77b76a294cd35a3cee7c82cb98c1b174815`。
- 未改其他逻辑/文件，未运行 real benchmark/I05/science，未 stage/commit，未触碰 P05。
