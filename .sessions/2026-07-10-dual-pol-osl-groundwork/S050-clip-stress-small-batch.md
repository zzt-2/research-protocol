# [S050] Clip 压力域 small batch

> 2026-07-16 | Batch 1 压力诊断 | PASS（observation only）

## 目标

在已有高步长失稳证据域（μ=1e-2）测试 gradient clipping 是否至少改变 divergence/update-tail 机制；不把结果直接升级为性能 Go。

## 记录

固定 D046 修复后的 generator：N=100000、seeds41–45、strong α=4.2/β=1.4、fG=30、SOP=4e-7、standard Godard-z。压力 pilot（seeds41–43） pooled update norm：P50=`0.0011734202`、P95=`0.0014604833857170827`、P99=`0.003110059353060399`、P99.9=`0.02866144`、max=`0.05504071`；所有 pilot seed 未发散、update finite。

冻结三臂：baseline、clip-P95、clip-P99；paired seeds41–45，共同 realization/mask/window/events。观察项：divergence、divergence_symbol、update clipping count、fixed/PI BER、swap/fade/recovery/censor。若 schema/mask/finite 失败立即停止；即使 clip 降低 divergence，也只记机制信号，待更大批和预注册判据后再作 Go/Kill。

## 决策引用

- D045：候选族批量排跑。
- D046：GG generator prefix-stable 修复。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

压力 small batch 已完成且独立审计 PASS；freeze 仍 DEFER。clip 是否进入更大 paired 批，需另立性能判据，当前不作 Go/Kill。
