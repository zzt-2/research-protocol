# Task Brief: C4-1 scaled-unitary 冻结配方 fresh confirmation

> 来源: S028 / D050 / T069 / V025 | 产出位置: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/` 与 `projects/thesis-fso/polarization-demux-groundwork/step4a-c4-1-fresh-confirmation.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 12
  action_class: C4_SCALED_UNITARY_FRESH_CONFIRMATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 T069 的 `C4_STRUCTURED_SIGNAL / PROVISIONAL_A` 做且只做一次全新 seeds、零调参的 confirmation。复用已经接收的实现与四格场景，固定 B1/B2 参数和全部统计规则，判断 scaled-unitary C4 相对最强廉价 B2 的短导频 BER 信号能否成为 Ch4 的可写硕士方法证据。不得改 development 配方、尝试救场或扩展为完整论文实验。

## 启动门与只读前提

1. 先运行 task-control validator；完整读取 D050、T069、V025、development manifest/raw/aggregate/receipt、correctness receipt、实现/tests，以及适用 sim-preflight、TDD、systematic-debugging 与 verification 规范。
2. Fresh 运行 T069 的 13 项目标 tests；从现有 development raw 独立 reducer 重算 terminal/hash。任一不一致先定位 correctness/provenance，最多一轮局部修复；禁止以重新运行 development BER 覆盖旧 raw。
3. `development_manifest.json`、`development_raw.json`、`development_aggregate.json`、`development_receipt.json` 与 `correctness_receipt.json` 均只读。confirmation 必须使用独立命名的 manifest/raw/aggregate/receipt，不得覆写 development 证据。
4. 只允许修改本 seam 的 confirmation runner/tests/artifacts、指定 Groundwork 报告、worker log 与必要 usage log；不改 `common/`、`params.py`、Ch3/Ch5、Skill/controller 或论文正文。

## 冻结配方

- 场景、IAO、星座、Gamma–Gamma、AWGN、payload 长度和 arms 与 T069 完全相同：DP-(8,8)-16APSK，static random `Q∈U(2)`，`alpha=4.0,beta=1.9` 公共标量 fading，equal-branch circular AWGN，payload=`4096 symbols/pol/window`；无 PDL/PMD/FIR/IQ、时变 SOP、CFO/CPR、LDPC。
- 四格仍为 `14/18 dB × Np=2/4`；每格 64 个全部用于 confirmation 的 windows。四格 seed bases 按 T069 同一 cell 顺序固定为 `7000/7100/7200/7300`，每格 seeds=`base+0..63`，与 development 无重叠。
- arms 固定为 B0 plain LS、B1 normalized ridge、B2 SV-floor、C4 scaled-unitary mean-singular projection、O1 true inverse oracle。
- B1 参数逐格固定为 T069 tune winner：`0.01/0.001/0.001/0.01`；B2 四格固定 `tau=1.0`。confirmation 禁止 tuning、候选参数搜索或根据结果切换 strongest comparator；primary comparator 固定为 B2。
- 所有 arms 在每个 window 共用同一 `Q/g/noise/pilots/payload`；deployable arms 不得读取 `H_true` 或 payload truth 作动作。
- primary 为 payload BER 与 C4−B2 paired window bootstrap 95% CI；bootstrap 固定 PCG64 seed=`2026083004`、2000 resamples。另算两个 `Np=2` cell 合并后的 paired bootstrap CI。secondary 为 B0/B1/B2/C4/O1 BER、channel NMSE、inverse residual、oracle headroom、runtime；secondary 不改变 terminal。

## 冻结终态

1. `C4_CONFIRMED_STRUCTURED_SIGNAL`：两个 `Np=2` cell 的 C4−B2 mean 均 `<0`；合并 Np2 paired CI upper `<0`；至少一个 individual Np2 CI upper `<0`；两个 `Np=4` cell 均无 CI lower `>0` 的显著退化；全部 correctness/finiteness/provenance 门 PASS。
2. `C4_CONFIRMATION_LOCAL_ONLY`：不满足上项，但至少一个 `Np=2` individual CI upper `<0` 或合并 Np2 CI upper `<0`，且没有 correctness/provenance 失败。只保留有限局部支持，不增格、不改 seeds、不重调参数。
3. `C4_NOT_CONFIRMED`：无上述局部信号、出现显著反向结果，或科学统计门失败。关闭本次 confirmation；不得追加第二 confirmation。
4. correctness/provenance 不能闭合则 `INVALID_CONFIRMATION_ARTIFACT`，只允许报告阻塞；不得用 BER 终态掩盖。

## 交付与验证

1. 新增 `confirmation_manifest.json`、`confirmation_raw.json`、`confirmation_aggregate.json`、`confirmation_receipt.json` 与最小 runner/tests；文件必须包含冻结 development artifact hashes、seed arithmetic、paired realization/observation hashes、arm parameters、bootstrap config 和 terminal inputs。
2. 报告 facts-first：列四格各臂 BER、C4−B2 CI、合并 Np2 CI、oracle headroom、development/confirmation 方向一致性、终态、claim ceiling 与唯一下一步。明确 B2 cheap winner 和“共同尺度估计而非新旋转”的身份。
3. 运行 task-control validator、全部相关 tests、raw-only reducer、hash/split/firewall/finiteness 审计与 `git diff --check`。不要由实现对话宣布 `THESIS_METHOD_READY`；只回报 frozen terminal，等待另一上下文独立 raw 复算。
4. 单任务最大墙钟 60 分钟；若运行明显超过预期，先保存已完成 evidence 并查 correctness/复杂度，不扩规模。一次 commit、不 push。
