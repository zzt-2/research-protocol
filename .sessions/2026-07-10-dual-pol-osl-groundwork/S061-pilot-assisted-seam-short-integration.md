# [S061] E 族 dual pilot seam 与短集成

> 2026-07-16 | E 族最小实现 | 状态：进行中（待 V020 独立审查）

## 目标

建立 dual canonical 的稀疏 pilot 注入、data mask 与 2×2 SOP/Jones 估计 seam，并与无 pilot standard-CMA 同 realization 对照。

## 记录

`pilot_assisted.py` 实现每 64 symbols 前 4 pilots（约6.25%，≤10%），注入阶段读取 `sX/sY/h/theta` 只用于 noise-preserving 物理重建；部署估计器只读 `rX/rY/pilot_mask/pilot_symbols`。测试 2 passed。结果 `pilot_assisted_short_N100k_rate1e-5_seeds41-43.json`：6252 pilot、93748 data。

- seed41 theta mean/P95=.03245/.08035 rad；baseline data BER=.0039853，pilot-injected=.0043027。
- seed42 theta mean/P95=.02029/.05024；两者 BER=0。
- seed43 theta mean/P95=.03185/.07931；baseline=.006106，pilot=.006490。
- 均无 divergence；assignment block 估计噪声较大（约1229 xy/334 yx）。

该批只验证 seam 与估计信息质量；简单“注入 pilot 后仍跑原 CMA”没有利用 Jones estimate，不能当 pilot-assisted recovery 方法。

## 决策引用

- D051：优先 E pilot-assisted，先做最小 seam。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

待 V020。若审计通过，下一最小候选必须实际消费 Jones estimate（data derotation/初始化/relock），并与 naive injection、baseline 同批消融。
