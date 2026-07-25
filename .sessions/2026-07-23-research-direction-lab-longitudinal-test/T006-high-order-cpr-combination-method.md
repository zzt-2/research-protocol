# T006：高阶调制 CPR 组合方法大包

> 执行环境：`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`
> 当前 formal step：Groundwork Step 4a
> 权威决策：`.sessions/2026-07-06-step4a-mve-execution/decisions.md#D012`
> 前台控制：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`

## 任务目标

在**一个 GLM 对话**中完成高阶调制 CPR 的合法问题门、headroom 门，以及门通过后的
2–3 个务实组合方法比较。目标不是再写分析报告，而是尽可能形成一个可包装的方法；
只有物理/公平性门明确失败时才停止。

候选来源不是标题联想：复用已完成的 B10/B12 Step 1–3 证据，检验星地
Gamma-Gamma 湍流 + CFO/linewidth 条件下，pilot-RLS 与 MAP/pilot phase recovery
能否形成比单一组件和最强简单传统方法更好的组合。

## 开始前必须完整读取

1. 本文件与同目录 `topic-index.md` 的 `RDL-CONTROL`；
2. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` 的 D012；
3. `projects/thesis-fso/master-state.md`；
4. `projects/thesis-fso/literature_notes.md` 的 L20、L22、B10-Q1/Q2、B12-Q2/Q3；
5. 主仓库（不在 worktree 内）的
   `D:\code\study\research-protocol\papers\_read_notes\_B10-16qam-pilot-rls-increment.md`
   和
   `D:\code\study\research-protocol\papers\_read_notes\_B12-freq-domain-pilot-increment.md`；
6. `stages/groundwork.md`、`stages/gw-feasibility.md`；
7. `thesis-lessons.md` 速查表及 TL-20/TL-22/TL-23/TL-26/TL-27/TL-30–33；
8. `code-quality.md`、`.agents/skills/sim-preflight/SKILL.md`；
9. 现有实现资产：
   `projects/simulation/common/_recovery.py`、
   `projects/simulation/common/_dual_pol_channel.py`、
   `projects/simulation/simulator/run_bps_ablation.py`、
   `projects/simulation/experiments/test_qam16_multimethod.py`、
   `projects/simulation/explore/nda-awgn-tracking-sandbox/`。

如果主仓库 paper 路径存在但 worktree 内不存在，这是共享论文库布局，不得误报“全文缺失”。

## 授权边界

- 只在 GW Step 4a 内工作；不得进入 Step 5、Contract 或 Execute。
- 允许新建：
  - `projects/simulation/explore/high-order-cpr-combination/`
  - `projects/simulation/results/high-order-cpr-combination/`
  - `projects/simulation/tests/test_high_order_cpr_combination.py`
  - `projects/thesis-fso/worker-logs/step-006-high-order-cpr-combination-method.md`
- 优先复用现有 `common/`；不得为了方便改 shared generator、protected history、
  Direction Lab Skill/controller 或通用基础设施。
- 不获取新私有全文，不把摘要当全文，不恢复 P03/Science Scout。
- T005/Pilot-Jones 资产保持 immutable；本包不得继续修其方法或语义。
- 全部细节写文件，聊天只返回最后四行。

## 执行顺序

### A. Step 1–3 证据恢复与冻结契约

先从 B10/B12 笔记提取并写入 `source-closure.yaml`：

- B10 pilot-RLS 的观测、状态、CFO/phase-noise 更新、pilot→decision-directed 切换；
- B12 frequency-domain pilot 与 MAP phase recovery 的信息源、输出和限制；
- 哪些参数来自论文，哪些来自现有星地 simulator，哪些只是 validation-tuned；
- 明确组合方法相对两个 source component 的新增动作，而不只是并排调用。

在任何 primary test 前冻结 `contract.yaml`，至少包含：

- primary modulation = uniform 16-QAM；
- canonical star-ground GG link，主条件使用当前有来源参数；至少一个 clean/control、
  一个 operational turbulence、一个 adversarial 但仍有来源的条件；
- CFO/linewidth 不得直接照搬“10 GHz/1.45 MHz”而忽略当前前端与采样率。先做
  dimensional audit，再冻结一个现有 nominal 点和一个 B10 支持范围内且当前系统可表示的
  stress 点；
- 至少 3 个位于 HD-FEC waterfall 邻域的 SNR 点；只用 validation 定位，不用 test 调参；
- 所有方法使用相同 pilot overhead、总发射能量、data mask、realization 和有效 BER 分母；
- fresh disjoint validation seeds 至少 5、test seeds 至少 10，并与已有包 assert 不相交；
- primary metric = BER→Q² penalty/gain；同时报告 raw BER、paired wins、95% CI；
- 所有 source/contract SHA、Python/依赖版本和真实运行参数。

### B. 先做合法问题门与 headroom 门

建立 baseline ladder：

- `B*`：当前任务下 validation-tuned 的最强简单传统 CPR，至少覆盖现有 BPS/4OPM
  或仓库里更强且合法的 conventional baseline；
- `B10`：pilot-RLS standalone；
- `B12`：MAP/pilot phase recovery standalone；
- `O`：使用 true CFO/phase 的 truth-assisted reference，只作 FR-21 Kill bound，
  不作 Go 对手。

必须先通过 semantic smoke：

- 无噪/零 CFO/零 phase noise 的恢复；
- CFO 与 phase sign、单位和 block boundary；
- pilot/data mask、pilot overhead 与能量公平；
- receiver-visible 输入无 future/TX-truth 泄漏；
- 固定标签或显式 PI/ambiguity resolution 口径；
- B10/B12 单体确实消费各自声称的信息，不能退化成同一估计器别名。

用 paired validation/test 计算 `B*→O` 合法 headroom。若所有 primary cells 的
point estimate 与 95% CI 上界都 `<0.5 dB`，立即裁决
`KILL_NO_LEGAL_HEADROOM`，不实现三个组合方法；但仍需完成 raw rows、测试、综合报告和
worker-log。

### C. headroom 存活时，同包实现三个有界方法

1. `P1 cascade`：B10 pilot-RLS 负责 coarse CFO/phase state，B12/MAP 只优化
   residual phase；必须证明 residual 输入与 standalone B12 不同。
2. `P2 confidence gate`：由 RLS innovation、residual likelihood 或 receiver-visible
   confidence 在 B10/P1/B12 之间切换；阈值只用 validation。
3. `P3 adaptive forgetting`：RLS forgetting factor 由 innovation/confidence 调整；
   必须有限幅、可复现，并与固定 forgetting 的 B10 standalone 对照。

先做小型 mechanism slice，排除退化/符号错误后，直接完成 primary paired test。
不为失败方法建设框架，不另开第二个执行包修小毛病；在本对话内定位并修复会改变结论的
bug，且保留 anomaly 记录。

### D. 预注册裁决

- `GO_METHOD`：至少一个 P 在 primary test 上相对 `B*` **且**相对 B10/B12 两个
  standalone component 的最强者取得 `>=0.3 dB` Q² gain，95% CI 下界 `>0`，
  paired wins `>=7/10`，clean/control 退化不超过 `0.1 dB`，并通过复杂度/开销公平审计。
- `COMPONENT_REPRO_ONLY`：只赢 `B*`，但不赢最强 standalone component；不得包装成组合方法。
- `PROBLEM_SURVIVES_METHODS_FAIL`：`B*→O >=0.5 dB`，但 P1–P3 均未达到方法门；
  保留真问题与失败机制，下一轮再决定是否换机制。
- `KILL_NO_LEGAL_HEADROOM`：问题门失败，停止本族当前 M-C-A。
- semantic/oracle/baseline 身份未闭合时，禁止给科学 PASS；状态最高 `PARTIAL`。

## 证据与测试要求

至少落盘：

- `source-closure.yaml`
- `contract.yaml`
- runner、baseline/method source
- validation/test raw rows
- aggregate/result JSON
- `synthesis.md`
- worker-log
- source/contract hashes

测试至少覆盖：

- noiseless/known-offset recovery；
- CFO/phase sign 与单位；
- pilot mask、data mask、equal overhead/energy；
- no future leakage / no TX-truth in deployable methods；
- B10/B12/P1/P2/P3 身份不退化；
- raw→aggregate bit-identical；
- seed split 与跨进程 deterministic fingerprint；
- source/contract SHA closure；
- verdict boundary tests。

测试在 Windows 默认 locale 和 `PYTHONUTF8=1` 下都必须通过；所有读写显式
`encoding="utf-8"`。

若当前 GLM 支持独立 critic/verifier，必须使用分离上下文做 scientific critic 与
integrity verifier；若不支持，完成同样的自查但最终 `status` 最高只能为 `PARTIAL`。

## 收尾

- 本对话只做一次 consolidated commit，不 push。
- `git diff --check`、全部定向 tests、YAML/JSON parse、raw recomputation、protected diff、
  `git status` clean 都要在 worker-log 记录真实输出。
- 不更新 formal owner、live control 或 master-state；这些由主控接收后更新。

最终聊天只返回：

```text
status: PASS|PARTIAL|BLOCKED|FAIL
commit: <40-char SHA>
worker_log: projects/thesis-fso/worker-logs/step-006-high-order-cpr-combination-method.md
anomaly: <NONE or one concise anomaly>
```
