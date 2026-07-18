# [S065] 6-pilot Jones EMA09 原门槛闭合

> 2026-07-16 | E 族机制稳定化 | 状态：PASS（正式GW晋级证据门）

## 目标

不修改 D052 预注册门槛，修正汇总口径并使唯一未达标 cell 真正达到 failure改善≥50%。

## 记录

`pilot_grid_summary.py` 修正任意正改善与≥50%改善的混淆，测试4 passed；旧grid正确计数为2p=9/15、4p=13/15、6p=14/15。problem `4e-6 seed47` 中，Tikhonov/condition guard 仅改善6–20%；EMA α=.5/.9/.99分别57.29%/72.92%/74.63%，clean controls无退化。选α=.9避免过强滞后。

最终 `pilot_6p_ema09_full24_N100k.json`：24 cells（8 seeds×3 rates），15 failure/9 clean；failure≥50%=15/15，clean退化=0/9，divergence=0，三臂 denominator一致，rate分层3/3、5/5、7/7。config/source SHA与fingerprint审查通过。

旧72-grid保留历史运行时SHA，并明确current runner已变更、旧源码snapshot缺失；不覆盖旧SHA冒充。full24保持独立SHA。

## 决策引用

- D053：不改门槛，做inverse稳定化。
- D054：6-pilot+EMA09晋级正式GW Step1（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

进入正式GW Step1撞车/竞争格局检索；该晋级不是Go，Step2/3/3.5/4a仍为硬门。
