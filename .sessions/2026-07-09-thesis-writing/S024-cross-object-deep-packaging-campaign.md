# [S024] 跨技术对象方法深挖包装

> 2026-08-13 | 战略讨论后的只读深挖 | COMPLETE

## 目标

在 D032 的硕士级 recipe 标准和 D034 的跨技术对象约束下，分别把 P11、P05、P08-R2 沿本地证据追到章级包装终态，或确认存在真实性上的硬阻断。

## 记录

第一批三个彼此独立的技术对象：

1. T029：P11 少导频 complex-LS 双偏振 Butterfly FIR；
2. T030：P05 强湍流/SOP 下固定流标签在线 CMA 均衡；
3. T031：P08-R2 prefix-calibrated、decoder-tuned coded-FSO receiver。

首轮只读：允许深读已有代码、raw result、worker log、D/V/harvest 与 git 历史；不运行实验/复算脚本，不联网检索/下载论文，不补 Groundwork，不创造候选，不修改研究资产。每条不能以“经典方法、廉价替代、旧 terminal、差别小、未击败强邻居”停止；只能交付完整方法章 dossier，或指出违反真实性底线/缺少 baseline 改善/没有实际动作链等硬阻断。

若首轮仅发现一个可补的小证据缺口，执行方必须给出最小补证、时间上限与失败后去向，但不得自行开跑。主线程收到后可继续在同一独立对话追问，直到 `PACKAGEABLE_NOW / PACKAGEABLE_AFTER_ONE_BOUNDED_STEP / CANNOT_PACKAGE_HONESTLY` 三态之一稳定。

### 回传与复审

三项首轮均给出 `PACKAGEABLE_AFTER_ONE_BOUNDED_STEP`，理由分别是双偏振/payload-only 评分、独立 seeds、三点曲线/pristine confirmation。主线程按 D032 追问“缺少该补证是否会使现有有限命题为假或不公平”，三项均在第二轮改判为 `PACKAGEABLE_NOW_WITH_LIMITS`：

- P11：现有动作真实；只将结果限定为固定 20 dB、X 输出、runner-defined BER 和 pilot-adjusted goodput proxy。
- P05：15-epoch 正式 baseline 合法；两个 cell、3 paired seeds 限制外推，不破坏现有约 0.5 fixed-label delta。
- P08-R2：单工作点和 chronology debt 限制标题；n=40 paired、CI 下界为正足以支持 operating-point alpha/offset method。

三项章级 dossier 与横向判断见 R026。

## 决策引用

- D032：具体 recipe 优先，完整相同才构成碰撞。
- D034：CCISP 是会议代号；核心方法须尽量跨技术对象。
- D035：跨对象深挖到包装或硬阻断（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。用户明确授权开多个新对话深挖；首轮仍保持只读停机边界。

## 后续

T029–T031 深挖完成。等待用户讨论 P05/P11 二选一的均衡章身份以及 P08-R2 是否作为独立 coded-receiver 小方法；不自动恢复执行。
