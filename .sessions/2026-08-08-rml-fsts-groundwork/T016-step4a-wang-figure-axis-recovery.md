# Task Brief: Wang 2023 figure-axis recovery for Step 4a calibration

> 来源: S004 / V006 / T015 | 日期: 2026-08-09
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-wang-figure-axis.md`

## 任务

只恢复 Wang 2023 本地 canonical `content.md` 已直接引用的 Fig. 10–12（必要时 Fig. 8）的原图坐标轴、legend、power/`B_L` sweep values 与可辨 numeric anchors，用于判断 structural smoke 能否 source-calibrate。不得泛搜、不得修改论文库/代码/治理文件、不得跑仿真、不得下 Go/Kill。直接 IEEE mediastore figure URL 属原文一手附件，可在子 agent 中获取；若访问失败记录 HTTP/格式 blocker。最多 10 分钟。

## 必答

1. Fig. 10 四个 panel：横轴 `B_L` ticks、各曲线的 modulation/TS/power/legend、paper default 是否是图中 argmin、可读 MSE 数字/数量级。
2. Fig. 11–12：power-axis ticks/range、320-symbol panel 的 power points与 B0 qualitative trend；-43/-37 dBm anchor 的意义。
3. Fig. 8（仅必要时）：received-power legend 是否可读，outage threshold校准是否能绑定具体功率。
4. 每项标 `EXACT_READABLE / APPROX_FROM_PLOT / UNREADABLE`；禁止把像素估读写成精确值。
5. 保存临时图只可放系统 temp，不写 worktree；worker-log只写读数与 direct URL/hash/bytes（若可得）。

## 结论格式

`AXES_RECOVERED_FOR_CALIBRATION / PARTIAL_AXES_ONLY / FIGURE_ACCESS_BLOCKED`，并说明哪些值可进入 immutable contract，哪些只能做视觉 sanity check。
