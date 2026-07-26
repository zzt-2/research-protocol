# [R004] T013 后 B9 覆盖修复与轮换比较

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D016

## 调研问题

T013 被独立接收为 `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE` 后，
是否值得在 B9 同轴再做一次有界 Step 1 覆盖修复；若值得，它为什么比 C15、B1、
A4 更可能最终产生 `METHOD_SIGNAL`？

## 发现

### T013 新事实

- 七个 archive 共 `61` 条 raw、`58` 条去重、`21` 条非排除、`8` 条必读；
  `21/21` 非排除候选为正式发表。
- 本轮实际返回源只有 OpenAlex；Semantic Scholar 被限流，未配置源没有返回。
- Route A 有 `8` 条非排除，但定向 deep 结果为 `0`；Route B 有 `17` 条非排除，
  其中两条 deep 只是一般 FSO task-fit/adjacent context，不支持 self-coherent、
  virtual-carrier、CSPR 或 phase-reconstruction。
- EFNS 已构成 DRE 的直接廉价竞争者；原始 DRE canonical 仍需 citation chase。
- 证据不足以支持星地低比特自相干的剩余问题，但“未搜到”也不能当不存在。

### 四个候选的六维比较

| 候选 | 方法形态 | 预期增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **B9 一次覆盖修复** | 低比特 self-coherent FSO 的 DRE/CSPR 状态选择或预配置，保留 fixed-DRE/RO 回退 | 若 Step 1–3 支持，目标是低 PNOB 下复杂度—稳健性适配；当前没有 method delta | “星地低比特 DAC 自相干链路的数字分辨率增强与稳健适配” | 仅 Step 1 repair-ready；有 JLT 2023 全文正向锚、21 条非排除和 EFNS 直接 comparator，仍非 active carrier | 用 IEEE、arXiv、S2 做一次真实多源与 mechanism-deep 补召；不下载、不精读、不实现 | 若仍不足三源，或两条 route 都无 mechanism-deep 支撑，B9 返回池；不得第三个 Step 1 包 |
| **C15 重启** | 归一化/降阶星座盲均衡代价函数 | 可能修复 19× gradient-scale 不公平后形成低复杂度 cost adaptation | “面向星地盲均衡的尺度公平降阶代价函数” | 仅 formalization candidate；T011 coverage blocked，T012 未执行科学内容且已消耗两包 | 重建 task，恢复多源、metadata、三篇 canonical，再进 acquire/read | 新任务仍卡接口/来源即轮换；不得把 task failure 当 science negative |
| **B1 新契约** | condition-dependent adaptive phase window | 若 evaluator 重建后存在可靠 FEC crossing，可形成窗口选择方法 | “按链路状态调节 CPR 窗口以折中噪声与动态跟踪” | 有历史 Step 1–3/4a，但 T007/T008 evaluator、oracle、population 均失真；当前实现禁止再修 | 从 working-region、per-block oracle、真实候选集重建 evaluator，实质是第三次 evaluator 路线 | 身份门再失败即保持池中，不再同轴 |
| **A4 新契约** | deployable DA/NDA/CPR 条件切换 | 可能在低 SNR 避险、强湍流高 SNR 微增益形成 robustness method | “可部署链路指标驱动的载波恢复模式切换” | 有 30-seed 历史资产，但 T009 暴露 TX/pilot、frequency-stage、working-region、raw closure 四类 P0/P1 | 第二次 identity rebuild，且需重做公平 waveform 与可部署输入 | 身份门再失败即退出；现有 no-second-repair 边界不应破坏 |

### 为什么选择 B9 修复

所有候选**下一包立即产生 `METHOD_SIGNAL` 的概率都为 0**：B9/C15 仍在
Groundwork Step 1，B1/A4 又没有合法 evaluator。比较的是完成最小债务后最终进入
方法比较的主控判断，不是频率学概率：

- B9 一次覆盖修复：主观 `15%–25%`；
- C15、B1、A4 中的最佳替代：主观 `5%–15%`。

B9 高于至少两个替代项的原因是：它已经有 source-native 正向锚、21 条非排除、
8 条必读和一个真实 EFNS 直接 comparator；当前缺口集中在“真实多源 + deep
mechanism support”，可由一次只读检索包直接裁决。C15 已连续两包仍未开始科学
内容；B1 需要被明确禁止的第三次 evaluator rebuild；A4 需要第二次多层 identity
重建。B9 修复不保证方法，只是目前最便宜、最可逆、最可能恢复合法方法载体的包。

## 结论

授权一次且仅一次的 B9 Step 1 多源/mechanism-deep 覆盖修复。它继续不是 active
scientific carrier，`minimal_construct` 仍不得冻结。若修复后实际 source
families 仍少于 3，或两条 route 都没有非 OpenAlex 的 mechanism-specific deep
证据支撑剩余问题，则接收 `BLOCKED_SEARCH_COVERAGE` 或
`STEP1_NO_DISTINCT_PROBLEM_FOUND`，B9 返回池并立即轮换；不得再派第三个 B9
Step 1 包。

## 对决策的影响

需要 live D016、formal D027、CP013 与 T014。该动作只延续 Groundwork Step 1，
不扩大到下载、精读、Step 4a、实现或实验。
