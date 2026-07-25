# [S015] T006 拒收与 B1 自适应相位窗激活

> 2026-07-25 | GW Step 4a 接收/载体切换 | 状态：T007_READY

## 目标

独立接收 T006，区分实现产出与科学结论；在不陷入 B10/B12 长修复的前提下，选择
已有 Step 1–3 证据、能在一个执行对话内形成方法的下一 carrier。

## 记录

T006 完成了大量代码、raw rows 和测试，但其科学结论不能成立。B10 没有实现论文的
128-pilot training→DD 语义，B12 在关键公式缺失时自行重构 MAP，pilot 与 data 又经过
不同物理通道。更直接地，B10 在纯 CFO + AWGN 的 source-native 小探针中也无法恢复；
因此 9–20 dB 退化首先是实现身份失败。

原 headroom survivor 也不稳健。adversarial|14 dB 的 mean 0.6059 dB 几乎全部来自
一个 near-random collapse seed；median 0.0447 dB，删去最大值后 mean 0.0560 dB。
所以不接受“问题存活、三个方法失败”，但保留 T006 为工程和方法论负面资产。

候选比较后选择 B1 自适应相位估计窗，而非 B9 DRE 或 T006 修复。B1 有明确来源问题：
固定窗无法同时处理 SNR 波动与 phase-noise drift，sat.1553 明确要求进一步研究动态窗。
现有 VV/pilot CPE 可复用，方法只需 receiver-visible 条件估计、有限窗集合和滞回，
可以在一个大包内完成 problem gate、三策略和 paired test。

## 决策引用

- D013：拒收 T006 科学裁决，激活 B1 自适应相位窗（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。B1 已有 Step 1–3 证据且在本专题校准后的
  Step 4a 候选范围内；只切换 carrier，不进入 Step 5/Contract/Execute。

## 后续

执行 live-test `T007-b1-adaptive-phase-window-method.md`。先过“最优窗随条件变化且
不存在普适固定窗”的结构门；失败即 Kill，成功则同包完成三种方法和正式 test。
