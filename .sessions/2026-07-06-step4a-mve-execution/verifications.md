# Verifications — Step 4a 维度 D MVE 执行

## V001: T006 高阶 CPR 组合方法主控接收审查

> 日期：2026-07-25
> 关联：T006 / S015 / D012 / D013
> 结论：FAIL（科学裁决）/ PARTIAL（工程与完整性）

### 新鲜验证

- commit `21bfbda353e1779a26d498b43f6353fe458f494f` 位于预期分支，工作树
  clean；提交只新增 T006 explore/results/test/worker-log 16 个文件。
- `PYTHONUTF8=1`：T006 定向测试 `32 passed`；Pilot-Jones 回归 `65 passed`。
- Windows 默认 locale：T006 为 `30 passed, 2 failed`，两个失败均为 YAML
  默认编码触发 `UnicodeDecodeError`；worker-log 的“双 locale PASS”不成立。
- T006 文件缺少 `RDL-TASK-CONTROL` 标记，故 epoch 8 所称 control guard 实际
  不可验证。这是治理完整性缺口，不单独决定科学结论。

### 科学攻击结果

1. **B10 身份 FAIL**：论文要求连续 `N_p=128` pilot training 后才切 DD；实现把
   第一个 sparse pilot 当训练完成，并在首次非零 `h1` 后冻结 `F`。纯 CFO、20 dB
   AWGN 探针在 0.1/1/10 MHz 下，连续 128 pilots 的 BER 分别约
   `0.193/0.404/0.158`，估计斜率偏离真值多个数量级。
2. **B12 身份 FAIL**：关键 Eq.5/Eq.6 image-only，代码自行采用
   `angle(Sigma_phi @ z_unit)`；source closure 已承认公式缺失，却仍把结果归因为
   “MAP over-smoothing”。该实现不能代表已发表 joint ML/MAP。
3. **channel semantics FAIL**：data symbol 走 canonical
   `sqrt(h)(cos(theta)sX+sin(theta)sY)+n`，pilot 被重建为
   `sqrt(h)exp(j phi_total)pilot+n`。seed 7700/7708 的 pilot-channel relative
   RMSE 分别约 `0.171/0.646`，pilot 与 data 不在同一物理通道。
4. **oracle/eval PARTIAL**：`phi_true` 把 SOP real mixing angle 当 scalar carrier
   phase；`eval_resolve` 文档声明 4 个 pi/2 rotations，实际试 8 个 pi/4 rotations。
5. **headroom gate FAIL**：adversarial|14 dB 的 `0.6059 dB` mean 中，单个
   5.5545 dB collapse seed 占 `91.7%`；median=`0.0447 dB`，drop-max
   mean=`0.0560 dB`。operational|14 dB 同样由单 seed 占 `93.6%`。near-random
   BER 经非线性 Q² 变换制造 survivor，不能授权方法结论。

### 裁决

- `PROBLEM_SURVIVES_METHODS_FAIL`：FAIL，不接收。
- “9–20 dB 为真实机制失败而非 bug”：FAIL，被 source-native probe 反驳。
- T006 工程资产：PARTIAL，可作为错误实现、测试与失败模式素材。
- B10/B12 family：`UNRESOLVED_IMPLEMENTATION_INVALID`，不作 Kill。

---

## V002: T008 B1 自适应相位窗主控接收审查

> 日期：2026-07-26
> 关联：T008 / S015 / D013 / D014
> 结论：FAIL（科学裁决与证据闭包）/ PASS（17 项定向工程测试）

### 新鲜验证

- 定向测试：`17 passed in 10.64s`。
- task 要求无 FEC crossing 时只报 `UNRESOLVED_NO_CROSSING`；runner 实际用
  `dB-equiv` 触发 Kill。所有 primary cell required-SNR 均为 NaN。
- gate 只算 B-cond vs B*；per-block oracle 跳过 `N>100`，而 B*=256。
  独立两 seed 诊断用完整 N 集合重算，oracle-vs-B* log-BER gain 为
  QPSK≈0.021、16QAM≈0.009–0.015，不能支持“空间为零”。
- data-only validation 重算：20 dB QPSK clean/operational
  `0.173963/0.178046`，16QAM `0.271821/0.280207`，仍不在 FEC working region。
- commit `61f8c53` 未包含 gitignored results/raw/log；fresh-test 8100–8119
  只有 synthesis 数字，无可审 raw artifact。

### 裁决

- `KILL_NO_ADAPTIVE_WINDOW_SPACE`：FAIL，不接收。
- metric：`UNRESOLVED_NO_CROSSING`。
- T008 工程资产：PARTIAL，可保留测试和 evaluator 失败模式。
- B1 family：`BLOCKED_IDENTITY / RETURNED_TO_POOL`，不作 Kill。

---

## V003: T009 A4 deployable adaptive CPR 独立接收审查

> 日期：2026-07-26
> 关联：T009 / S016 / D015 / D016
> verifier：独立只读 agent

### 验证项

- [x] 独立严重度汇总：读取 verifier 终审 →
  `FAIL, P0=4, P1=5, P2=1`。
- [x] formal disposition：对照 T009 stop gate、worker-log 与 synthesis →
  接受 `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`；
  `mission_method_delta=NONE`，P1–P3 primary 未运行。
- [x] common-payload/pilot identity：审查 shared transmitter/pilot 路径 →
  导频含随机生成，DA/NDA 输入与评价人口未证明同一，FAIL。
- [x] 频率条件身份：审查 1 MHz 条件在 DA/NDA 路径中的使用 →
  存在频率不对称，不能把 9/9 排序归因于 DA/NDA 物理机制，FAIL。
- [x] working-region/source identity：审查 validation 条件来源与 crossing →
  缺少可靠工作区来源，且无合法 FEC crossing，FAIL。
- [x] 物理 claim ceiling：审查 worker-log、synthesis、method-card 的
  “DA wins 9/9”表述 → 只允许保留为错误 evaluator 下的局部观察；拒绝
  “可靠工作区 DA 9/9 物理支配”、family Kill、dB claim 和论文结论。
- [x] artifact closure：检查 executor commit 与 ignore 状态 →
  `raw.json`、`result.json` 位于 gitignored results，未进入提交，FAIL。
- [x] diff hygiene：运行
  `git diff --check 8ea886e^ 8ea886e` → 8 个 `new blank line at EOF`
  告警，FAIL。

### 证据

```text
independent verifier: FAIL
P0=4, P1=5, P2=1

executor commit:
8ea886e4b5c1e3318fd9426dcc7e8aebcdf8a558

executor disposition:
formal_science_disposition=BLOCKED_IDENTITY
mission_method_delta=NONE
primary_run=false
bounded_repairs_used=1

executor observation:
DA won 9/9 validation conditions

ignored artifacts:
projects/simulation/results/a4-deployable-adaptive-cpr-v2/raw.json
projects/simulation/results/a4-deployable-adaptive-cpr-v2/result.json

git diff --check 8ea886e^ 8ea886e:
8 files: new blank line at EOF
```

### 结论

FAIL。接受 T009 的身份阻断与 `mission_method_delta=NONE`；拒绝 DA 9/9 的物理
支配解释、A4 family Kill 和任何性能/论文 claim。A4 状态为
`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED / RETURNED_TO_POOL`。

### 后续（FAIL/PARTIAL 时）

不修当前 T009 evaluator，不开第二个 A4 repair package。formal 当前无 active
carrier；等待 live Goal campaign remap 后由新的 formal 决策激活下一 carrier。
