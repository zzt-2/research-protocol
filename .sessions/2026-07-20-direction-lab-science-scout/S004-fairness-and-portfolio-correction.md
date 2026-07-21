# [S004] Baseline 公平性与候选全貌纠正

> 2026-07-21 | SCIENCE_SCOUT 方法纠正 | 状态: 完成，等待下一对话执行 H004

## 目标

审计 S003/D006 后续是否会在 baseline 标准不一致和候选过窄的情况下直接进入 C01，并把已确认纠正写回科学专题。

## 记录

- 独立方法论审计确认：MMA 选择有文献和机制依据，但同 `mu`、`N=32768`、block-end 因果和 oracle recoverability 的解释均写得超过证据。
- 独立候选血缘审计确认：C01 最接近可运行但仅能先验证 observability；C02/C04 需新 adapter/合同；C03 因缺 state snapshot/action hook 为 `INFRASTRUCTURE_BLOCKED`。
- system topic D011 已把主 Skill 修订为共同系统锚点 + 任务专属 comparator、相当调参机会和有界机制级候选扩图；fresh-agent GREEN 与独立 verifier PASS。
- 科学专题据此将 D006 晋级撤回 `DIAGNOSTIC/SLICE`，保留所有 raw evidence 和 harvest；新入口 H004 要求先扩图、纠正 readiness、做有界公平修复，再立即批跑。

## 决策引用

- D007：新建——baseline 公平性未闭合；先扩机制全貌并做有界公平修复。

## 范围确认

- 本轮是否在 scope boundary 内：是。只纠正科学解释和后续入口；未运行实验、未修改 protected history、未创建 B004。

## 后续

- 下一对话接收 H004，在三个宏阶段内完成恢复/扩图、准备与运行、综合与收获；局部 blocker 不停，自动轮转。
