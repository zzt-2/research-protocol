# T008：B1 身份修复后的自适应相位窗方法生产包

> 来源：S001 / D001 / formal D013 / system D018 / mission CP007
> 执行环境：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> 基线提交：以本文件所在 clean HEAD 为准
> 当前 formal step：Groundwork Step 4a
> 产出：isolated B1 v2 代码、raw artifacts、synthesis、worker-log、单次 commit

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 12
  action_class: B1_IDENTITY_REPAIRED_METHOD_PACKAGE
  mission_checkpoint: CP007
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你是执行者，不是主控。在**一个 GLM 对话**内：

1. 修正 T007 的 baseline、required-SNR、oracle 与 observability 五个身份缺口；
2. 若 corrected oracle 相对合法 B* 仍存在预注册方法空间，立即实现并比较三个
   receiver-visible adaptive-window 方法；
3. 交付可包装的方法信号，或严格限定的 `METHOD_FAIL_WITH_SPACE` /
   `PACKAGING_BOUNDARY`。

不得只做审计、只补测试、只写下一轮计划。除 identity 无法闭合或 corrected oracle
空间确实消失外，本包必须进入方法实现和 fresh-seed paired comparison。

## 1. 起飞检查

### 1.1 控制与 formal owner

1. 确认 worktree、分支、HEAD、clean 状态，不得换主 worktree。
2. 完整读取本文件、同专题 `topic-index.md` 顶部控制块、`mission-log.md` 全表、
   `decisions.md#D001`。
3. 运行：

   ```powershell
   python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
     .sessions/2026-07-23-research-direction-lab-longitudinal-test/T008-b1-identity-repaired-method-production.md
   ```

   非 PASS 立即停止。
4. 读取：
   - `projects/thesis-fso/master-state.md` 当前控制面与 B1 行；
   - formal `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D013`；
   - 同专题 V001、S015；
   - T007、`projects/thesis-fso/worker-logs/step-007-*` 及 T007 新增源码/artifacts；
   - B1 source notes 与 `projects/thesis-fso/literature_notes.md` 对应条目；
   - `stages/groundwork.md`、`stages/gw-feasibility.md` Step 4a；
   - `thesis-lessons.md` 速查及 TL-20/22/23/26/27/30–33；
   - `code-quality.md` 与相关 VV/BPS/pilot-CPE/common 实现。
5. 本包是 GW Step 4a MVE，不进入 Step 5/Contract/Execute。`sim-preflight`
   v1.4 明确不拥有 MVE；以 `gw-feasibility.md` §D 为准。

若 formal carrier 不是 B1 Step 4a，停止为 `BLOCKED_STAGE_OWNER`；不得自行改 owner。

### 1.2 继承边界

T007 只作 diagnostic input，不继承其 Kill。必须复核而不是相信：

- oracle headroom 约 0.4–1.0 dB；
- 当前 receiver-visible features `|rho|<0.5`；
- T007 使用的 B*、SNR→dB 变换、oracle 集合、seed 纪律与 feature gate。

T006 的 B10/B12/channel helper 仍属 scientific-invalid，禁止导入。旧 T007 文件和
artifacts 全部只读；v2 写独立路径。

## 2. 正向方法合同

- `positive_method_target`：根据 receiver-visible block SNR 与 phase innovation，
  在有限 window grid 上因果选择相位估计窗。
- `minimal_construct`：
  - **P1 physics-ratio rule**：物理单调、有限网格、无训练标签回放；
  - **P2 validation lookup + hysteresis**：分箱查表并抑制 window chatter；
  - **P3 confidence-safe selector**：低置信度退回 B*，仅 ridge/logistic/shallow table。
- `fair_comparator`：
  - **B***：只在 validation 跨 registered conditions 选择并全 test 冻结的单一窗；
  - **B-cond**：每个 registered condition 仅用 validation 选的 fixed window；
  - validation-tuned conventional VV/BPS 或合法 pilot moving-average 作 robustness。
- `primary_packaging`：低复杂度 dual-pol FSO adaptive phase-window CPE。
- `fallback_packaging`：fixed-window regret、observability 与方法工作区边界。

## 3. 先冻结 v2 contract

在 `projects/simulation/explore/b1-adaptive-phase-window-v2/` 创建并在 primary 前冻结：

- `source-closure.yaml`
- `MVE-SPEC.md`
- `contract.yaml`
- `seed-census.yaml`

### 3.1 Fresh seed discipline

用确定性脚本盘点 T002–T007、Direction Lab、相关 simulation result 中所有已观察
seeds。T007 及历史 seed 不再作 held-out。冻结：

- validation seeds ≥10；
- test seeds ≥10，并在 contract 冻结确切数量；
- 两池彼此不交，且与全历史观察池 assert 不交；
- 每个 `(cell, seed)` 只生成一次 realization，所有方法共用。

validation 用于 B*/B-cond、feature mapping、threshold/hysteresis/confidence；
test 开始后任何参数、特征、bin、window grid 不得再改。

### 3.2 物理与 metric contract

- uniform 16QAM、canonical GG channel、同 pilot/data channel、同 energy/overhead、
  同 eval mask/denominator/latency；
- primary linewidth/SNR/湍流范围必须引用现有 source，不为救方法扩到非典型点；
- window grid 对所有 fixed/adaptive/oracle 完全相同；
- primary dB 指标只能由实际覆盖 FEC crossing 的 SNR sweep 插值得到；
- 不得使用固定 log-BER slope、BER ratio 常数映射或单点 proxy 冒充 dB；
- 若没有合法 crossing，报告 raw/log-BER 与 `UNRESOLVED_NO_CROSSING`，不造 dB；
- oracle per-block window 只作 Kill/headroom bound，不作 Go comparator。

## 4. 五个 REQUIRED identity smoke

以下全过才运行 primary：

1. **source/algorithm identity**：窗公式、phase sign、16QAM 固定 bias、合法 π/2
   ambiguity、linewidth→per-symbol variance 逐项闭合。
2. **signal/information identity**：pilot 与 data 走同一物理通道；deployable 方法
   不读 TX bits、true SNR/phase/channel、future block/test labels。
3. **baseline identity**：B* 是 validation 跨条件冻结的一个窗；禁止 per-seed、
   per-test、用 true bits 重选。B-cond 同样只读 validation。
4. **oracle/metric identity**：oracle 候选集合包含 B*；required-SNR 来自真实曲线；
   actual window、oracle label、feature target 对齐到同一 block/latency。
5. **observability identity**：validation 拟合、held-out test 同时报 Spearman、
   exact-window accuracy、top-2 accuracy、majority-fixed accuracy、regret；
   禁止用两个边际 `rho` 推翻所有 receiver-visible 信息。

另做：

- noiseless/known phase/Wiener direction tests；
- window 增大确实体现 averaging-vs-tracking tradeoff；
- block boundary、causal prefix、latency、polarization order；
- input 改变时 feature/method output 发生非退化变化；
- raw rows→aggregate/result 独立重算；
- deterministic subprocess、UTF-8、source hash。

一次有界修复后仍失败则 `BLOCKED_IDENTITY`，不得下方法或 family verdict。

## 5. Corrected space gate

identity 全过后，在 validation + fresh diagnostic slice 重算：

- B* 与 B-cond；
- oracle per-condition / per-block window；
- per-cell regret、median、20% trimmed mean、paired CI；
- out-of-work-region、collapse、single-seed dominance。

只有以下情况允许停止而不实现 P1–P3：

- oracle 相对合法 B* 的 primary working-region median 和 20% trimmed
  required-SNR gain 均 `<0.5 dB`（FR-21；低于方法自身 0.5 dB 门时不再运行）；或
- gain 只来自 BER `>=0.2` / no-crossing / outlier-dominated cells。

除此以外，即使当前 feature `rho` 较低，也必须进入 §6。observability 最终由
deployable method regret/performance 判定，不由单一相关系数提前 Kill。

## 6. 同包完成三个方法

### P1 physics-ratio rule

- receiver-visible `SNR_hat / phase_innovation_hat` 映射到有限 window grid；
- 映射方向符合“低 SNR→更长、phase innovation 大→更短”；
- 只用 validation 定标，带边界与 B* fallback。

### P2 validation lookup + hysteresis

- 用 validation 对 `(SNR_hat, phase_innovation_hat, 可选一个已证明增量的 trace)`
  做浅分箱；
- 相邻 block 跨过冻结边界才切换；
- 报告 switch rate、latency 与无 hysteresis 消融。

### P3 confidence-safe selector

- 限定 frozen ridge/logistic/shallow table；
- 低置信度退回 B*；
- 与 majority-fixed、P1/P2 和直接 oracle-label replay 防泄漏检查比较；
- 不建设深度学习或通用训练框架。

先做 mechanism slice，确认至少两个有来源条件选择不同窗、P2 减少 chatter、P3
真实 fallback；随后直接跑完整 paired test，不另开“方法实现下一轮”。

## 7. 指标与裁决

主指标：

- FEC-crossing required-SNR gain（仅真实曲线）；
- paired raw/log-BER、PI-SER；
- median、20% trimmed mean、95% CI、wins；
- oracle regret closure、clean degradation、worst-decile/cycle-slip、switch rate。

`METHOD_SIGNAL`：

- 至少一个 P 相对 B* 在至少两个 non-stress primary conditions 的合法
  required-SNR gain `>=0.5 dB`；
- paired-bootstrap 95% CI lower `>0`，且 paired win fraction `>=0.70`
  （按 contract 冻结的 test seed 分母计算）；
- 相对 B-cond 不为负，clean degradation `<=0.1 dB`；
- 关闭 oracle regret 至少 50%，且单 seed/cell 贡献不超过 40%。

`PROMOTION_READY`：METHOD_SIGNAL + 对 B-cond/传统 estimator 稳健 + 消融支持
具体组件 + 独立 verifier 重算一致。

`ROBUSTNESS_OR_PACKAGING_BOUNDARY`：未达 0.5 dB，但显著降低 worst-decile、
cycle-slip 或扩大 FEC-working coverage；只能作次级方法/边界。

`METHOD_FAIL_WITH_SPACE`：corrected oracle 空间存在，但 P1–P3 均不能稳定关闭；
只否定本包构造。

`KILL_NO_ADAPTIVE_WINDOW_SPACE`：仅在 §5 的 corrected、robust、working-region
headroom 门失败时成立；不得从 feature `rho` 单独推出。

任何正面结果必须做物理前提、cheap alternative、outlier、evaluator 与 test-leak
攻击；验证完成前不更新论文或宣称重大结果。

## 8. 文件边界

允许新建/修改：

- `projects/simulation/explore/b1-adaptive-phase-window-v2/**`
- `projects/simulation/results/b1-adaptive-phase-window-v2/**`
- `projects/simulation/tests/test_b1_adaptive_phase_window_v2.py`
- `projects/thesis-fso/worker-logs/step-008-b1-adaptive-phase-window-v2.md`

禁止修改：

- T007 及所有旧源码/artifacts/worker logs；
- `projects/simulation/common/**`、`params.py`、formulas-master；
- portfolio/state/harvest/master-state、formal decisions/verifications；
- live topic、mission-log、Skill/controller、protected history；
- Pilot-Jones、T006、C15、论文正文。

必须改 shared common 才能继续时，停止为 `BLOCKED_SHARED_CHANGE_REQUIRED`。

## 9. 验收与回传

必须落盘：

- source closure、theory expectation、frozen contract、seed census、source hashes；
- v2 implementation + tests；
- raw validation/test rows、selection manifest、aggregate/result；
- method card（输入、动作、复杂度、comparators、机制、工作区、主/备包装）；
- synthesis；
- worker-log，分别写 `formal_science_disposition` 与 `mission_method_delta`。

验证至少覆盖：task guard、五类 identity、no-truth/no-future、seed isolation、paired
realization、真实 crossing、raw→aggregate、deterministic rerun、YAML/JSON parse、
forbidden-path diff、`git diff --check`。

实现与 verifier 分离；若无法独立验证，最终最高 `PARTIAL`。本对话只做一次
consolidated commit，不 push，commit 后 worktree clean。

总投入硬上限 `<=1 day`；不得建设新框架或通用基础设施。单次 primary run 超过
30 分钟先缩到预注册代表 slice 查性能瓶颈；完整 primary 最多重跑 2 次。预计无法
在 1 天内闭合时停止为 `PARTIAL_BUDGET`，保留已完成 construct 与 raw evidence，
不得用无限调参拖延裁决。

最终聊天只返回：

```text
status: PASS|PARTIAL|BLOCKED|FAIL
commit: <40-char SHA>
worker_log: projects/thesis-fso/worker-logs/step-008-b1-adaptive-phase-window-v2.md
anomaly: <NONE or one concise anomaly>
```
