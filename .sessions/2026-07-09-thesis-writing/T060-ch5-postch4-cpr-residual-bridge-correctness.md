# Task Brief: Ch5 post-Ch4→per-pol Ch3 residual bridge correctness

> 来源: S028 / D046 / T047 / T051 / T054–T055 / T057 | 产出位置: `projects/simulation/explore/ch5-apsk-structured-covariance/` 与唯一对应测试
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 8
  action_class: TARGET_RESIDUAL_BRIDGE_CORRECTNESS
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

实现一个最小、可审计的 receiver-visible residual bridge，固定真实物理顺序 `DP-(8,8)-16APSK → shared scalar GG/CFO/Wiener phase → unitary Jones → circular AWGN → Ch4 demux/RDE → per-polarization Ch3 DA CPR → pilot-only ambiguity resolution → known-pilot residual`。本任务只做 correctness，不运行 natural occurrence、不比较 Ch5 性能。

## 启动与边界

1. 完整读取本 brief、topic-index、D046、T055、T057、Ch4/Ch5 seam 与所复用 common 函数；先运行 task-control validator。
2. 本任务触发 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md` 与测试模板。不得改 `common/`、`params.py`、Ch4 算法、Ch5 estimator、Skill/controller 或论文正文。
3. T055 §4.1 的文字链顺序有误；以本 brief 为准：**先 Ch4 demux，再每偏振 Ch3 CPR**。不得实现为 Ch3→Ch4。
4. 禁止 IQ/filter/FIR、PDL/PMD/CD、synthetic anisotropy、payload-truth ambiguity、NDA payload resolve、LDPC performance 和 occurrence cell。

## 可复用接口

- Ch4 `core.py`：`m16apsk_constellation_by_label`、`random_su2`、`orthogonal_pilots`、`pilot_ls_demux` 与冻结 arm runner。
- Common `_channel.py`：`gg_block`、`doppler_phase`；common `_recovery.py:da_ml_recovery`，必须逐偏振调用。
- Ch5 `methods.py` / `codec_metrics.py`：仅用于对 bridge bundle 运行有限性/正定 identity，不做 method ranking。

建议最小新增文件：`post_ch4_ch3_bridge.py`、`run_occurrence_smoke.py`（本任务只允许 correctness mode）、`occurrence_contract.yaml`、对应 test；更新 README 和独立 correctness receipt。允许等价命名，但不得建新公共框架。

## Receiver-visible bundle

至少保存：`z_pilot`、`x_pilot`、`e=z_pilot-x_pilot`、pilot indices、point/ring labels、per-pol/per-point counts、known mask、`cpr_mode=DA`、estimated phase/frequency、8-fold ambiguity index、Ch4 arm/W/gate summary、cell/seed/window/config/source identifiers 与 realization hash。

truth-only 字段可单列 offline diagnostics，但绝不能进入 estimator、gate、ambiguity resolution 或 deployable bundle。禁止 TX payload labels/bits、true Jones、true phase、true SNR 回流。

## Pilot-only ambiguity

只允许从 8 个 APSK-compatible rotations 中选 known-pilot SSE 最小者；不得读取 payload bits/labels。修改隐藏 payload truth 后，bridge 输出、ambiguity index、Ch4/CPR state、bundle hash 必须完全不变。

## 必须测试

1. identity/noiseless：bridge residual 为 0；
2. 8 个旋转逐一可由 known pilots 唯一恢复；
3. payload truth mutation invariance；
4. polarization swap equivariance；
5. 调用顺序与数据依赖确为 Ch4→逐偏振 DA CPR；
6. `e`、point/ring labels、counts 与 known mask 精确；
7. train/eval 或观察窗口因果隔离，不跨偏振 pooling；
8. GG、linewidth、frequency ramp sentinels 能证明路径被消费，但 truth 不进入输出；
9. 将 bundle 喂入 B1/B2/B3/C1 时 covariance 有限、对称、正定，circular control 正确退化；
10. 同配置/seed hash 稳定，改变 receiver-visible 输入时 hash 改变。

## 交付与退出

- correctness receipt 必须写 `BRIDGE_CORRECTNESS_ONLY / TARGET_OCCURRENCE_NOT_RUN / NO_METHOD_SIGNAL`。
- 报告只回答 bridge 是否正确、truth firewall 是否关闭、future occurrence 所需字段是否完整；不得报告 natural R/T anisotropy、NLL/GMI/BER/FER gain。
- Ch4 arm/参数尚未由 T059 冻结，因此本任务不得自行选择“最好 arm”或运行 occurrence；只通过可注入的 frozen-arm/config 接口做 correctness fixtures。
- fresh 运行 validator、目标 tests、correctness smoke 与 `git diff --check`。一次 commit、不 push；回报 commit、测试数、hash、唯一 blocker。
