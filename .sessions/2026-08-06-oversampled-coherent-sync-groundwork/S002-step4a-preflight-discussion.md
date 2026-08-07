# [S002] Q1 Step 4a preflight discussion

> 2026-08-07 | GW Step 4a preflight | closed

## 目标

只完成 Q1 的 A0 §0–§6、A′/A/B 分析和维度 D 的 ≤1 天 deterministic semantic smoke 设计；不运行
MVE/smoke/仿真，不建 testbed，不实现方法。

## 记录

### Session Start Confirmation

- 当前专题：`2026-08-06-oversampled-coherent-sync-groundwork`；原始目标见 topic-index `:14-18`。
- 旧范围止于 Step 3.5，旧明确不含 Step 4a；H003 与用户本轮指令共同构成受限重开授权，见 D009。
- 不变量：QPSK/16QAM、RRC、≥2 sps；物理参数须有星地/相干 FSO 文献；receiver-known preamble
  可用于部署但 payload truth 只用于评分。
- 依赖 RDL system 与 framework-evolution 均 active；`conflicts_with: []`；专题仅 2 个 S 文件，无 inflation。
- profile 无新稳定画像信号；本轮继续执行窄范围、证据链和防过早 Go/Kill。

### H003 接收验证

- JLT 2025 非 exact collision：PASS — T013 worker log `:20-40,62-68`。
- JOCN 停止获取但 claim limitation 保留：PASS — D008 `:304-322` 与 voice `:18-19`。
- 只允许 Step 4a preflight discussion：PASS — RDL D032 `:1123-1145`、control `:7-25`、
  master-state `:30-52`。
- registry 依赖/冲突与明确不含已检查；范围差异由 D009 显式处理。

### RDL recovery route check

本动作不创建或运行方法，只辨认 B0/B1/B2/C 的方法身份并冻结最小 semantic smoke。它是下一正向方法
动作的必要门，因为必须先证明 C 相对增强传统 baseline 有不可替代结构增量。当前 formal carrier 为 Q1、
same-axis/no-method streak 未触发 factory 或 rotation；在 smoke 证据出来前保持 formal preflight lane。

### 分析结论

- Q1 四判据 PASS，A0 §0 合法；不得再次要求“A 已被 MVE 证明”。
- evidence-faithful B0 已含 coarse CFO；A 必须针对 residual CFO/timing/frame 的顺序硬判决传播。
- 一般 joint likelihood 非可分，但 B1 若使用相同 global score 可与 C 在离散网格等价。
- 当前无性能间隙、稳定错误峰或 B1/B2 吸收率数字；四个空白零假设均未反驳。
- 唯一主要贡献维度冻结为 wrong-basin false-lock rate，`miss=N/A`；A0 专门负面证据搜索仍为
  `EVIDENCE_GAP`；最终 terminal=`STEP4A_PREFLIGHT_EVIDENCE_GAP`。
- 详细方法表、信号模型、FIM/Hessian/ambiguity 分析方案、竞争矩阵和 smoke 合同见
  `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md`。

## 决策引用

- D009：受限重开 Step 4a preflight discussion（新建）。
- D010：冻结 EVIDENCE_GAP terminal 与 semantic smoke 合同（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（旧边界由用户显式授权并按 D009 记录范围变更）。
- 未运行实验/仿真脚本、MVE 或 semantic smoke，未建 testbed，未改 `common/`、`params.py`、旧实验、Skill 或四个日志。

## 后续

等待用户审阅并决定是否授权执行 ≤1 天 deterministic semantic smoke。未获批准前无执行入口。
