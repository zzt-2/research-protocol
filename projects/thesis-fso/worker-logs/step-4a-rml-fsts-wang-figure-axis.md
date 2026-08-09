# Wang 2023 figure-axis recovery

> 2026-08-09 | T016 | 仅恢复 Wang 2023 原图轴与正文锚点；未泛搜、未改论文库/代码/治理、未运行仿真

## Verdict

`FIGURE_ACCESS_BLOCKED`

本地 canonical `content.md` 给出的 Fig. 8、10、11、12 IEEE mediastore `large.gif` 直链均返回 HTTP 403；响应是 4141-byte HTML shut page（`IEEE Xplore - Temporarily Unavailable`），不是 GIF。因此，本报告只能冻结正文/图注中明确写出的值，不能恢复图面 ticks、legend、逐点曲线或从像素估读数值。本结论仅是 T016 的原图访问结论，不是 Step 4a 的 Go/Kill 或科学终态。

- canonical source：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`
- canonical source SHA-256：`e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f`
- 正文证据范围：`content.md:279-325`

## Direct figure access ledger

| Fig. | canonical direct URL | HTTP / type | response bytes | response SHA-256 | result |
|---|---|---:|---:|---|---|
| 8 | `https://ieeexplore.ieee.org/mediastore/IEEE/content/media/4563994/10101698/10097873/wang8-3265847-large.gif` | `403 / text/html` | 4141 | `3d8b074f6a8d7dd1d7bc7584eb91f566b9d4b5454846396ddc6beb4d749dca41` | `UNREADABLE` |
| 10 | `https://ieeexplore.ieee.org/mediastore/IEEE/content/media/4563994/10101698/10097873/wang10-3265847-large.gif` | `403 / text/html` | 4141 | `3d8b074f6a8d7dd1d7bc7584eb91f566b9d4b5454846396ddc6beb4d749dca41` | `UNREADABLE` |
| 11 | `https://ieeexplore.ieee.org/mediastore/IEEE/content/media/4563994/10101698/10097873/wang11-3265847-large.gif` | `403 / text/html` | 4141 | `3d8b074f6a8d7dd1d7bc7584eb91f566b9d4b5454846396ddc6beb4d749dca41` | `UNREADABLE` |
| 12 | `https://ieeexplore.ieee.org/mediastore/IEEE/content/media/4563994/10101698/10097873/wang12-3265847-large.gif` | `403 / text/html` | 4141 | `3d8b074f6a8d7dd1d7bc7584eb91f566b9d4b5454846396ddc6beb4d749dca41` | `UNREADABLE` |

上述 SHA-256 是四次相同 IEEE 403 响应体的哈希，**不是原图哈希**；原始 GIF 的 bytes/hash 均未取得。临时响应只保存在系统 temp，未写入 worktree。

状态解释：`EXACT_READABLE` 表示 canonical 正文/图注明确给出；`APPROX_FROM_PLOT` 本次为零项，因为原图不可见；必须读图才能得到的项目均标 `UNREADABLE`。

## Fig. 10 — four-panel `B_L` sweep

| 项目 | 状态 | 可恢复事实 / 限制 |
|---|---|---|
| panel 映射 | `EXACT_READABLE` | (a) 4-QAM、TS=320；(b) 16-QAM、TS=320；(c) 4-QAM、TS=960；(d) 16-QAM、TS=960（caption，`content.md:301-305`）。 |
| 横轴身份 | `EXACT_READABLE` | 横轴是 TS block length `B_L`（`content.md:299`）。 |
| `B_L` ticks / sweep values | `UNREADABLE` | 正文没有列出图中完整 action grid；原图 403。不能据 paper preset 反推整条横轴。 |
| modulation / TS 条件 | `EXACT_READABLE` | 由 panel 映射可精确绑定；见上。 |
| received-power 曲线值、legend 文本及线型/颜色 | `UNREADABLE` | 正文只说设计受 received power 影响，没有给 Fig. 10 每条曲线的功率值或 legend 映射。 |
| paper preset | `EXACT_READABLE` | 320-symbol 4-QAM：`(B_N,B_L)=(16,20)`；320-symbol 16-QAM：`(8,40)`；960-symbol 4-QAM：`(24,40)`；960-symbol 16-QAM：`(16,60)`（`content.md:299`）。 |
| preset 是否为每条图中曲线的 argmin | `UNREADABLE` | 正文用 “is designed as” 给出 preset，但没有声明它对每个 received-power curve 都是绘图 argmin；原图不可见，禁止补成精确结论。 |
| MSE qualitative shape | `EXACT_READABLE` | conventional TS 随 `B_L` 改变时 estimation accuracy 保持不变；proposed accuracy 随 `B_L` 先改善、到某值后可能下降。换成图中 normalized-MSE 语言，即 proposed MSE 先降、后可能升（`content.md:299`）。 |
| 逐点 MSE / 精确数量级 | `UNREADABLE` | Fig. 10 的正文没有给每个 `B_L × power` 点的数值；不得把 Fig. 9/11/12 的范围移植到 Fig. 10。 |

## Fig. 11–12 — received-power panels and anchors

### Panel/legend facts

| 项目 | 状态 | 可恢复事实 / 限制 |
|---|---|---|
| Fig. 11 panel 映射 | `EXACT_READABLE` | 4-QAM；(a)/(c) 为 MSE vs frequency offset，TS=320/960；(b)/(d) 为 MSE vs average received optical power，TS=320/960（`content.md:309-315`）。 |
| Fig. 12 panel 映射 | `EXACT_READABLE` | 16-QAM；(a)/(c) 为 MSE vs frequency offset，TS=320/960；(b)/(d) 为 MSE vs average received optical power，TS=320/960（`content.md:319-325`）。 |
| algorithm identities | `EXACT_READABLE` | 相邻正文定义四类算法：4-QAM 使用 4th-power、4th-FFT、conventional TS、proposed；16-QAM 对应 QPSK-partition、4th-FFT、conventional TS、proposed（`content.md:289,309-319`）。原图中的缩写、颜色与 marker 映射仍不可读。 |
| power-axis ticks/range | `UNREADABLE` | Fig. 11(b)/(d)、Fig. 12(b)/(d) 的起止值、步长和全部 ticks 未在正文列出。 |
| 320-symbol power points | `UNREADABLE` | Fig. 11(b) 与 Fig. 12(b) 的离散 power points 无法从正文恢复；`-43/-37 dBm` 不是这些点表的已确认定义。 |

### B0/proposed qualitative trend

- `EXACT_READABLE`（4-QAM，Fig. 11(b)/(d) 整体文字趋势）：以项目语义 `B0 = paper proposed preset` 解读，低 received power 时 proposed 的 estimation accuracy 可能低于其他算法；随 received power 增大，其 accuracy 显著改善、趋于稳定并优于另外三种算法（`content.md:309`）。正文没有给转折/knee 所在功率，因此 knee 为 `UNREADABLE`。
- `UNREADABLE`（16-QAM power-panel 具体形状）：Fig. 12 正文没有逐段写出 (b)/(d) 的低功率转折、稳定区或交叉点；不能把 Fig. 11 的 4-QAM power curve 当作 Fig. 12 的精确读数。
- `EXACT_READABLE`（共同长度趋势）：正文明确说四种算法的 estimation performance 随 (training) symbol length 增加而改善（`content.md:319`）。这不是 power-axis 数值恢复。

### `-43/-37 dBm` anchors

| anchor | 状态 | 精确意义 |
|---|---|---|
| `-43 dBm` | `EXACT_READABLE` | 4-QAM Fig. 11(a)/(c) **frequency-offset sweep** 的固定 received optical power；对应 TS=320/960。它不是正文确认的 power-axis 下界、tick 或 Fig. 11(b) 的特定 power point（`content.md:309`）。 |
| `-37 dBm` | `EXACT_READABLE` | 16-QAM Fig. 12(a)/(c) **frequency-offset sweep** 的固定 received optical power；对应 TS=320/960。它不是正文确认的 power-axis 下界、tick 或 Fig. 12(b) 的特定 power point（`content.md:319`）。 |

在上述固定功率的 frequency-offset sweeps 中，正文给出的数量级锚点为：conventional TS 约 `10^-7`，proposed 约 `10^-8–10^-9`，即超过一个数量级改善（4-QAM：`content.md:309`；16-QAM：`content.md:319`）。这是 `EXACT_READABLE` 的正文数量级，不是逐点 digitization。power sweeps 对同一 received-power 点从 `(-1.1 GHz, 1.1 GHz)` 随机取 frequency offset，并对 800 次仿真求平均（`content.md:319`）；power ticks 仍未知。

## Fig. 8 — MSE-to-BER calibration limit

| 项目 | 状态 | 可恢复事实 / 限制 |
|---|---|---|
| panel 映射 | `EXACT_READABLE` | (a) 4-QAM；(b) 16-QAM（`content.md:279-283`）。 |
| received-power legend / 具体功率 | `UNREADABLE` | caption 只写 “different received optical powers”；正文未列 legend 数值，原图 403。 |
| BER 开始上升的 normalized-MSE threshold | `EXACT_READABLE` | 4-QAM：`2.5e-7`；16-QAM：`6.25e-8`（`content.md:279`）。 |
| BER 严重恶化的 normalized-MSE threshold | `EXACT_READABLE` | 4-QAM：`6.25e-6`；16-QAM：`2.25e-6`（`content.md:279`）。 |
| threshold 绑定具体 power | `UNREADABLE` | 只能绑定 modulation 与 normalized MSE，不能从正文绑定到某个 received-power bin；论文此处也未定义独立 outage event。 |

## Immutable-contract boundary

可进入 immutable source contract 的只有 canonical 正文/图注明示事实：

1. Fig. 10 四个 panel 的 modulation/TS 映射与四组 paper preset；
2. `B_L` 的定性 U-shape（以 MSE 表述）及 conventional TS 对 `B_L` 不变的正文趋势；
3. Fig. 11/12 panel 映射、`-43/-37 dBm` 作为 frequency-offset sweeps 的固定功率、`10^-7` vs `10^-8–10^-9` 的正文数量级、随机 CFO 区间与 800 次平均；
4. Fig. 8 的四个 modulation-specific normalized-MSE thresholds。

不得进入 immutable contract 的项目：Fig. 10 `B_L` grid/ticks、各 received-power legend、任一逐点 MSE、preset=per-curve argmin、Fig. 11/12 power-axis range/ticks/points、任何 power-specific threshold/outage 绑定。

本次没有 `APPROX_FROM_PLOT` 项：原图不可见，缺失轴值连视觉 sanity check 都不能做。正文定性趋势可作为 source-text sanity check，但不能替代图轴校准，也不能据此补造 action grid、power bins 或 crossover。
