# [S014] 高阶调制 CPR 组合方法重激活

> 2026-07-25 | GW Step 4a 载体切换 | 状态：T006_READY

## 目标

在 Pilot-Jones complex component rescue axis 被正式关闭后，恢复已有 B10/B12
Step 1–3 证据，以一个大包检验高阶调制 CPR 是否存在合法 headroom，并在门通过时直接
形成可包装的组合方法。

## 记录

Pilot-Jones T005 的 fixed/verified component primary 8 个 cells 全部低于 0.5 dB：
最大 point `0.0804126817 dB`，最大 95% CI upper `0.2371961896 dB`。主控进一步用
真正的 M3 酉矩阵精确逆重算 40 个 test realizations，BER 与原 MMSE-reference
40/40 一致，无噪恢复误差 `1.1310e-15`，因此该局部 Kill 不依赖原实现的正则化。

下一个载体不再从 Pilot-Jones 补丁延伸，而回到载波同步 Step 4a 已有证据池。B10
pilot-RLS 与 B12 frequency-domain pilot/MAP 已有全文/结构化精读、16/256-QAM
方法链和现成 CPR simulator 资产，且组合可形成明确输出动作。T006 采用
“问题/headroom 先行，门过则同包实现 cascade、confidence gate、adaptive forgetting”
的设计，避免只做分析，也避免在无 headroom 时建设方法。

## 决策引用

- D012：授权高阶调制 CPR 组合方法 Step 4a 大包（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。D012 显式把既有 B10/B12 Step 1–3 证据恢复为
  当前 carrier；仍停在 GW Step 4a，不进入 Contract/Execute。

## 后续

执行 live-test `T006-high-order-cpr-combination-method.md`。若合法 headroom 不存在，
按预注册门关闭当前 M-C-A；若存在，同一包完成三个务实方法与 paired test。
