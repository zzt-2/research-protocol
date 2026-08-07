# [S003] Q1 deterministic semantic smoke 执行

> 2026-08-07 | GW Step 4a 维度 D Probe | completed

## 目标

在 D010/H004 合同内执行 ≤1 天 deterministic semantic smoke，闭合 B1/C 等价性、廉价覆盖率、稳定
wrong-basin false-lock 区域与真实计算量四个缺口；不扩大为正式 MVE 或 testbed。

## 记录

### Session Start Confirmation

- 当前专题：`2026-08-06-oversampled-coherent-sync-groundwork`；原始目标与 RRC/≥2 sps、参数溯源、
  receiver-visible information 不变量不变。
- H004 三项事实核验 PASS：D010 合同存在且未执行；V007 PASS/blocker=0；B1/C 等价性与 gap 尚无数据。
- 依赖 RDL system 与 framework-evolution 均 active；`conflicts_with: []`；本专题 S 文件数=3，无 inflation。
- 用户“执行”构成显式 scope approval；D011 记录对旧“明确不含 semantic smoke”的受限变更。
- profile 无新稳定画像信号，不更新。

### RDL recovery route check

本动作比较 B0/B1/B2/C 的最小构造，但 Probe PASS 只允许判断是否值得进入正式 micro-MVE，不产生
METHOD_SIGNAL。它直接回答当前 active formal carrier 的唯一前置缺口；same-axis/no-method streak 未触发
factory 或 rotation。当前 mode=`PREPARING`，首个合法动作是冻结并验证 T015 control 后再派执行。

### 执行合同冻结

- 实施计划：`docs/superpowers/plans/2026-08-07-oversampled-sync-semantic-smoke.md`；
- 执行任务：T015；RDL control 绑定 epoch 30 / CP017；
- 本地负面证据核查仍未找到 exact Q1 headroom/失败/FIM 数字，只允许维持 `EVIDENCE_GAP` 起跑；
- 参数缺口以 diagnostic sentinel 显式处理：fixed-seed 64-symbol QPSK、RRC span、frame/tau grid 与 -6 dB
  noisy layer均不得外推为外场分布；
- operational B1 与 C-grid 使用同一完整候选集/score，exact equivalence 本身就是待验证的不可替代结构门，
  不另造更弱 B1 来制造 headroom。

### H004 接收验证

- “当前 terminal=EVIDENCE_GAP 且维度 D 未执行”：PASS — formal topic-index 与 D010。
- “B1 同 grid/score 可能与 C 数学等价”：PASS — preflight report §1.3/§4.4。
- “V007 fresh-context PASS、blocker=0”：PASS — verifications.md V007 与独立 verifier report。
- 接口变更：无；并行依赖：无未接收产物；registry dependencies active，conflicts none。

### Probe 执行与修复

- T015 task-control PASS；TDD 三段 RED→GREEN 后首轮 focused tests `24/24`，完成 180 cells / 720 method rows。
- 首轮 T016 为 FAIL（3 Important）：traversal visits/cache misses 混记、plot 未标 truth/top1、stress interaction
  可污染 primary reducer；另有 1 Minor 的历史 RED 证据等级问题。
- 执行 agent 用 4 个回归测试先得到 `4 failed, 24 passed`，随后最小修复至 `28 passed`，重跑 identity 与
  完整 grid；未改方法身份、grid 或阈值。
- T016 full re-verification PASS，blocker=`0`；semantic gates、artifact closure、B1/C independence、
  reducer、compute ledger、plot、provenance 与 protected boundary 全部闭合。

### 科学终态

- noiseless residual：B0/B1/B2/C 均 `0/75` false locks；
- minus6db diagnostic residual：B0/B2=`58/75`，B1/C=`59/75`，`G_C=-1.7241%`；
- stress_noiseless：四法均 `0/30`，不进入 primary；
- B1/C exact common-grid equivalence=`180/180`；B0 stable adjacent 2×2 wrong basin=`0`；
- 正式 terminal=`STEP4A_PREFLIGHT_KILL_OR_PIVOT`（D012）。

## 决策引用

- D011：用户批准执行受限 deterministic semantic smoke（新建）。
- D012：semantic smoke 触发硬退出，Q1 Step 4a Kill/Pivot（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（D011 与 topic-index scope-change 解除 semantic-smoke 执行禁令；
  正式 MVE/testbed/Contract/Execute 仍明确排除）。

## 后续

formal topic 关闭；不建 testbed、不进正式 MVE/Step 5。下一合法动作仅为用户决定归档 Q1，或显式授权把
latency/complexity 作为新的 M-C-A pivot 从前置步骤重新论证；不得沿用本 Q1 直接实施。
