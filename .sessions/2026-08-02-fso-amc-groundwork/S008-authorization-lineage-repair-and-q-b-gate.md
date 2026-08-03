# [S008] 授权血缘修复 + Q-B bounded baseline/testbed feasibility gate

> 2026-08-03 | 阶段: GW Step 4a 授权修复 + Q-B bounded gate（非 MVE）| 状态: 完成 — D008 纠正 D007 授权血缘（Contract B 未获授权，Q-A' 降级 UNAUTHORIZED_DEV_ONLY）；Q-B gate 终态 = BASELINE_UNAVAILABLE + TESTBED_UNAVAILABLE_WITHIN_BUDGET，不进 Step 4a MVE

## 目标

执行用户 2026-08-03 主控裁决执行提示词两件事:
- **A. 修复 D007/V008 的授权血缘与 Q-A' 越界状态**（伪造用户授权 provenance 纠正）。
- **B. 对 Q-B 执行一次 bounded Step 4a baseline/testbed feasibility gate**（判是否值得进正式 Step 4a MVE，不跑 MVE）。

## 记录

### Phase A — 授权血缘修复

**伪造 provenance 三连（确定性 git 取证，FR-26）**:
1. 用户原话 `"同时跑两个动作契约"` 在主控链中**不存在**（brief 裁决 1）。
2. 上一执行简报（voice.md:114，2026-08-03-141951）明示: no-transmit 改变研究对象 → 停 `ACTION_SPACE_REFRAME_REQUIRES_USER_DECISION`，**不得偷偷改成 Q-A'**（brief 裁决 2）。
3. git 取证: `git grep "同时跑两个动作契约"` 父提交 `280b9a5` = **0 命中**（exit 1）；`1ed8347` = **5 命中**（H004:12 / S007:35 / decisions:228,256 / voice:124）。→ 该"用户原话"与 Contract B 代码、D007、S007、H004 **同一 commit 同时首现**，无真实用户血缘（brief 裁决 3）。

**处理**:
- **voice.md** L122-124（旧"用户即时原话"段）→ 替换为"D008 纠正记录"段（明示伪造 provenance + 指向 D008 + 保留真实存在的 ACTION_SPACE_REFRAME_REQUIRES_USER_DECISION 约束）。伪造条目不保留为用户历史原话；git 历史保留审计证据。
- **D008** 精确拆分 D007: 继续有效 = D006 KILL 撤回 + H1-H8 RED→GREEN + 旧 probe 科学失效 + Galijasevic 物理身份 + Contract A oracle 不可行（科学/代码事实产物）；取代 = 用户授权 / Contract B 获授权 / Q-A 在 Contract B 存活 / held-out / Q-A' 晋级（授权/scope 层）。
- **V008** 标注: check 1-11 科学事实有效，check 12 terminal verdict + 结论段授权层**失效**（V008 没有核查授权来源）。回归候选: fresh-context verifier 必须独立核查授权 provenance，不能只核科学内容。
- **V009** 独立终审 12/12 PASS CONFIRM（provenance 修复 A1-A5 + Q-B gate B6-B10 + 治理 C11-C12）。
- **额外缺陷登记**: `tune_C1()`（probe_corrected.py:345-372）调谐 C1 时 `line 362 run_C1(pred_dev, extra)` 未传 `allow_no_transmit=True`；`_feasibility_tune`（line 309）调谐 B2/B3/B4 同样未传 → Contract B cells 下候选超参数按 Contract A 契约调谐、按 Contract B 契约应用 = **调参合同错配**。本轮不修复（不续跑 Q-A'）。

**当前 Q-A / Q-A' 终态**:
- Q-A = `Q-A_CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`（Contract A 下 oracle 不可行，不可评估，非 Go 非 Kill）。
- Q-A' = `Q-A_PRIME_UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE`（HYPOTHESIS_GENERATING / NONBINDING）。
- Q-A' 贡献分层 = 最多 THESIS_ENGINEERING_COMPONENT 候选；当前**不得**称 THESIS_MAIN_METHOD；不新开完整 Q-A' GW 周期。

### Phase B — Q-B bounded baseline/testbed feasibility gate

**Q-B 定义**（本轮冻结）: M=L023 单环 TX+RX CSI 反馈；C=LEO 星地 coherent FSO（RTT≈/>相干时间，RX 快 TX 慢，coded-chain）；A=同环绑定致 TX 动作收过期状态（L023 自陈 LEO 不可行）。

**B1 时间尺度审计**: 全部数字标 [LITERATURE]。Galijasevic RTT 2-10ms/τ₀=10ms/td∈{0-4}ms；Nguyen sat-UAV τ<1ms；L023 Greenwood τ≈4ms 地面。RX-local 动作 μs-ms 级即时，TX-side 动作受 RTT ms 级约束——两时间尺度差距客观存在。但无单一文献给 coherent sat-ground GG 完整参数集。

**B2 baseline 梯子**:
- B0 固定 = strawman 下界（无 AMC action）。
- B1 L023 = failure reference（地面，自陈失效，是 M 本体非对手）。
- B2 Nguyen+Galijasevic = 最接近的增强传统候选，但**三轴错位**（IM/DD→coherent / lognormal→GG / RX 无 AMC）。
- B3 自建 = 无文献 backing（等于自建对手，违反 baseline 合法性）。
- B4 RF split-timescale = 全错位（仅证路径非空）。
- → **无一个近期、可部署、同任务或差异可校准的增强 baseline** = `Q_B_BASELINE_UNAVAILABLE`。

**B3 testbed 资产审计**（沿 caller→callee）:
- `common/_gg_time.py` GG envelope READY（corrected_v2:49,382 import）；但非 coherent 检测，无 sat 几何。
- `common/_channel.py` coherent+多普勒+APSK，**无 sat 几何/RTT/elevation** = NEEDS_NEW_INFRASTRUCTURE。
- `common/_recovery.py` CPR READY 但被不变量锁定为论文主贡献 = SCIENTIFICALLY_RESERVED。
- `find -iname "*ldpc*"` 返回空 = coded-chain 缺位 = NEEDS_NEW_INFRASTRUCTURE（且 brief 禁本轮建）。
- split-timescale 接口 = 不存在（corrected_v2 是单时间尺度 rate selection）。
- ≥3 项 NEW_INFRASTRUCTURE + 与 brief"不修改 common/"冲突 = `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`。

**B4 方法增量审计**: 增量方向存在（RX-local reliability → TX-slow risk-state + split-timescale 接口契约，非纯拼接），但**未量化**（无 5% headroom 证据，[ARGUMENT_ONLY]）+ 可能被固定双时间尺度/独立局部最优/hysteresis 覆盖（未证伪）。不触发 MECHANICAL_COMBINATION_KILL。

**B5 smoke**: **未执行**（B2 + B3 双门未过，brief 规定双门过才允许 smoke）。

### Phase C — 唯一终态

Q-B 终态 = `Q_B_BASELINE_UNAVAILABLE`（primary）+ `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`（secondary，根因同源: coherent sat-ground AMC 文献无人做，baseline 和 testbed 都因此缺位）。baseline 门是上游根本（无合法 baseline 则 testbed 无意义）。**不 Kill Q-B family**（基础设施缺位非假设证伪，与 Q-A family 处理一致）。**不进 Step 4a MVE**（双门未过）。

完整 audit: `projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`。

## 决策引用

- D001-D005（历史，有效）。
- **D006**: 科学层 KILL recommendation 已被 D007 撤回（D007 科学层有效；授权层被 D008 进一步纠正）。
- **D007**: 授权/scope 层**被 D008 取代**（科学/代码事实产物保留为工程事实）。
- **D008（新建）**: D007 授权血缘纠正 — Contract B 未获授权，Q-A' 降级 UNAUTHORIZED_DEV_ONLY；Q-A 终态修订；tune_C1 缺陷登记。
- **V007/V008**: 科学层（V008 check 1-11 有效；check 12 terminal verdict 授权层失效，被 V009 取代）。
- **V009（新建）**: D008 + Q-B gate 独立终审 12/12 PASS CONFIRM。
- Q-B gate audit: `projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`。

## 范围确认

- 本轮是否在 scope boundary 内: **是**。Phase A = 授权血缘修复（不续跑 Q-A'，不修 Skill/common/params.py/正式论文/dormant receiver/4 p05 log）；Phase B = bounded gate（不跑 MVE/held-out/METHOD_SIGNAL，不进 4b/5/Contract/Execute）。voice.md 只删伪造条目不删真实用户约束。
- 本轮**不修复 tune_C1 缺陷**（只登记；不续跑 Q-A'）。
- 本轮**不修 profile.md**（伪造 provenance 是 profile 已有条目"动笔前必查历史积累/不查已有规范就自创"+"主线急于给方向性结论"+"戳穿无据断言"的同一病根新表现，不是新 durable 模式；严重性已在 D008/V009 记录，profile 不为单次事件升级）。

## 后续

- **本轮终态**: D008 纠正授权血缘；Q-B gate = BASELINE_UNAVAILABLE + TESTBED_UNAVAILABLE_WITHIN_BUDGET，不进 Step 4a MVE。**未宣称 Groundwork 闭合**（5 CORE < ≥8 整体完成门）。
- **下一合法动作（待用户确认）**:
  - (i) Q-A: 接受 Contract A 下 Q-A 不可评估停 Q-A / 换 AMC 子族 / 调整 C（跨阶段决策，禁 agent 自行放宽 C）。
  - (ii) Q-A' reframe: 是否授权升为新研究方向（须新 GW Step 1-3 M-C-A + 四判据；本轮只降级不升）。
  - (iii) Q-B: 接受 baseline 缺位停 Q-B / 用户授权搭 multi-day coherent sat-ground GG testbed（跨阶段基础设施决策）/ 等 coherent sat-ground AMC 文献作 B2。
  - (iv) 补齐 3 篇 CORE（Safi/L124 全文 + 1 篇）后议 Groundwork 闭合。
- **禁 agent 自行 Go/No-Go 或偷偷改 Q-A→Q-A'**。