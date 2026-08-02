# Research Direction Lab 长程真实运行测试

> 状态：dormant
> 当前纪元：85
> 最后更新：2026-08-02
> 权威决策：D058
> 权威验证：V084
> 最新 checkpoint：CP049

## 范围边界

### 原始目标

在用户只中转任务路径和极短回执的条件下，稳定推进真实研究并积累可用方法材料。

### 当前范围

- 保留长程运行审计、科学包血缘、论文资产分级和恢复条件。
- campaign 已收口为 `SATURATED_NO_ACTIVE_CARRIER / DORMANT`；本专题不再自动生产科学包。
- 下一对话只允许做 Research Direction Lab Skill 最小 patch 与历史回归，不启动新科学方向。

### 明确不含

- 不为凑满 10 包重开 P08/P09/P10/P11/G1 或任何已关闭轴。
- 不运行新仿真，不修复旧实验，不把 partial/invalid/negative 升格为方法贡献。
- 不在本专题启动 AMC。AMC 属于新系统层级，若获授权必须另开 Groundwork 专题并从 Step 1 开始。
- 不修改正式论文结论、protected history、旧 D/V、worker-log 或 raw artifact。

### 范围变更记录

- 2026-07-30，D039：启动“10 个有效包”探索 campaign；该固定数量是当时的执行合同。
- 2026-08-01，D057：一次性重开 G1 promotion 并纠正 P11；G1 终态为尺度伪影。
- 2026-08-02，D058：停止把 10 包当自动目标；7 包是最终有效计数，campaign 转 dormant。

## 不变量

1. 科学正确性优先于 receipt/hash/复算一致性；`consistency != correctness`。
2. `METHOD_SIGNAL=0`，`active_carrier=0`；负面包、工程资产和写作资产不得折算方法进度。
3. P01–P07-R 共 7 个有效科学包；P07 被 P07-R 替换后只计一次。
4. P08 系列 chronology 无效，P09 execution invalid，P10 evidence insufficient，P11 partial，G1 scale artifact，均不计有效包。
5. P11 四个标签为 9/11/13/15 dB，但 caller 未把 gamma 传入 generator；实际均使用默认 `GAMMA_BAR=100`，即 20 dB。
6. 旧记录与 raw 只保留血缘，不删除、不反向改写。
7. 恢复 campaign 必须出现新物理自由度、新系统层级或用户明确 scope change，且先过可执行语义门。

## 当前控制面

```yaml
status: SATURATED_NO_ACTIVE_CARRIER
topic_lifecycle: DORMANT
accepted_valid_packages: 7
fixed_target_10_is_execution_goal: false
remaining_valid_packages: null
mission_method_signal_count: 0
active_carrier_count: 0
current_package: null
active_lane: CAMPAIGN_CLOSEOUT
authority_pointer: D058
verification_pointer: V084
mission_checkpoint: CP049
next_action: SKILL_MINIMAL_PATCH_AND_HISTORICAL_REGRESSION
allowed_actions:
  - RECOVER
  - AUDIT
  - SKILL_PATCH_HANDOFF
forbidden_actions:
  - SCIENCE_EXPERIMENT
  - CLOSED_AXIS_REOPEN
  - FIXED_COUNT_PACKAGE_FILLING
  - AMC_GROUNDWORK_IN_THIS_TOPIC
```

## 科学包终态

| 包 | 机制族 | 终态 | 是否计数 | 可复用上限 |
|---|---|---|---:|---|
| P01 | CPR/SNR 失配 | `NO_DIAGNOSTIC_SIGNAL` | 1 | local negative |
| P02 | candidate rank | `PROBLEM_RESOLVED_BY_REGION_RETUNING` | 1 | retuning boundary |
| P03 | 定点协同 | `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION` | 1 | bit-true engineering |
| P04 | 连续 GG OOD | `PROBLEM_ABSENT_ON_CONTINUOUS_GG` | 1 | local negative |
| P05 | ML 均衡 OOD | `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER` | 1 | corrected CMA boundary |
| P06 | 因果跨帧历史 | `NO_CAUSAL_HISTORY_INCREMENT` | 1 | observability boundary |
| P07-R | AGC/ADC | `PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION` | 1 | gain-aware engineering |
| P08/R/R2 | coded LLR | `STOPPED_WITH_PARTIAL_ASSET` | 0 | coded-chain/prefix-LS/AST partial |
| P09 | 16APSK BPS | `EXECUTION_INVALID / KILL_C3` | 0 | methodology counterexample |
| P10 | ML/CMA router | `EVIDENCE_INSUFFICIENT` | 0 | two-cell local probe |
| P11 | pilot-efficient FIR | `PARTIAL_LOCAL_20DB_BASELINE_ASSET` | 0 | 20 dB local baseline only |
| G1 | gated normalization | `G1_SIGNAL_INVALID_SCALE_ARTIFACT` | 0 | bounded writing artifact only |

## 已确认结论

### 不变量

- 7/10 表示七个被接收的局部负面或边界包，不表示七项贡献，也不表示必须补齐三包。
- 本模型和当前授权下的 method-bearing 入口已经饱和；这不是数学完备性声明。
- A 级论文资产只有既有 DA/NDA 自适应 CPR；本 campaign 没有新增主方法。

### 其他结论

- B 级资产：bit-true 定点、coded-chain/prefix-LS/信息边界、强传统 comparator 边界。
- C 级资产：P01–P07-R 边界集、G1/P09 反例、metric/oracle/lifecycle 审计纪律。
- 过程根因与三项 Skill patch 见 R010；论文落点与两条 thesis spine 见 harvest map。

## 进展线索

- S001–S010：专题讨论与运行记录；不再新增 S，以避免控制面继续膨胀。
- R002：长程运行复盘；R003：轻量协议设计；R009：方法生产效果审计。
- R010：最终效果、根因、用户负担与 Skill patch brief。
- D039：固定 10 包历史合同；D057：G1/P11 纠偏；D058：campaign 收口。
- V071–V083：历史验证与撤回链；V084：最终 12 项独立验证。
- `mission-log.md`：完整 CP001–CP049 时间线。
- `projects/thesis-fso/direction-lab/harvest/method-production-campaign-thesis-map.md`：论文资产地图。
- H003：下一对话只做 Skill 最小 patch 与历史回归。

## 当前位置

专题已 dormant。下一步只读取 H003，修改 Skill 的三类最小规则并做历史回归；不运行 AMC，不创建 P12，不改科学资产等级。
