# [S018] 2A region-calibration authority reconciliation

> 2026-08-07 | authority reconciliation | 已完成

## 目标

完成且只完成一次 2A 受限 authority reconciliation：分开裁决 P01 receiver-visible pilot-SNR adapter、
P02 weak/low-SNR retune 与 T004 online estimated-SNR calibration map，并闭合到用户冻结的唯一 terminal。

## 记录

- foreground 从 epoch 32 / CP019 / D036 切换到 epoch 33 / CP020 / D037。
- 授权来源按转述记录：完整受限方案由主控提出，用户回复“行”；不把主控提案伪造成用户逐字原话。
- 证据复用优先。先确定性遍历 P01/P02 raw rows、审计真实 caller 和 region identity；只有语义门通过且缺合法 confirmation 时才运行一次 bounded held-out。
- T004 commit `1140134e89e8b0571274944cb44471ab6403481f` 的 REJECT 与“无合法 held-out 正结果”冻结，不因本次 reconciliation 改写。
- caller/raw 复算确认 P02 runtime 无 region 输入，实际只有全域 `ref=11`；六项语义门仅 truth-not-in-decide
  PASS，因此未触发 sim-preflight 或新 held-out。
- P01 恢复 4/5 harm cells，nominal-safety material failure 1/15；P02 weakretune-adapter
  `+0.45387 dB`，cluster CI `[+0.43404,+0.47370]`，cand_rank-weakretune `-0.09609 dB`，
  cluster CI `[-0.10275,-0.08942]`。P02 30-seed 汇总不是 pristine one-shot。
- 完成 authority artifact、Ch4 不升格包、original/global/region dev-only 表与流程图；D038/CP021
  terminal=`SUPPORTING_ONLY`。fresh-context V021 PASS（P0/P1/P2=0/0/0）。

## 决策引用

- D037：受限解冻 2A region-calibration authority reconciliation（新建）
- D038：2A region-calibrated CCISP 方法身份失败记录（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D037 scope change record）

## 后续

无。2A 已闭合，不得补跑或改名恢复；D036 Ch5 scheduling authority 与本终态分账。
