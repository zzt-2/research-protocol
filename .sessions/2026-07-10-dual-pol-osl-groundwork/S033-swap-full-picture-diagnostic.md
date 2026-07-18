# [S033] swap 全貌诊断（prompt030 双控扫描）— 推翻 TL-22 假象，swap 是 SOP 物理现象

> 2026-07-15 | GW 方法层诊断 | 状态：诊断完成，结论已定
> （承接 S032 规划 + 执行 agent Tier 0 报告。核心矛盾：执行 agent TL-22 说"新域 CMA 不 swap"，与 prompt012 旧域 CMA 8/10 swap 冲突）

## 目标

用参数域双控扫描（新域 4.2/1.4 vs 旧域 1.5/0.8 × CMA/ML/oracle × seeds × SOP_RATE × N）摸清 swap 全貌：谁的病、什么条件下出现，为方法层定位提供硬事实。

## 记录

### A. 实验设计（prompt030_domain_swap_audit.py）

三阶段扫描，所有 alpha/beta 显式传入（不读 params.py，杜绝漂移争议），swap 分类用 prompt012 标准口径（main-correlation threshold 0.5），双口径 BER（fixed + PI）：

- **Phase 1**：域 {旧 1.5/0.8, 新 4.2/1.4} × {CMA, ML, oracle} × 10 seeds，固定 N=5M/SOP=4e-7
- **Phase 2**：新域 × SOP_RATE {0, 1e-8, 1e-7, 4e-7, 1e-6} × 10 seeds，固定 N=5M
- **Phase 3**：新域 × N {2M, 5M, 8M} × 5 seeds，固定 SOP=4e-7

总耗时 7656s（2.1h），结果 `results/cma-fade-divergence/prompt030_domain_swap_audit.json`。

### B. Phase 1 核心结论：CMA 和 ML 两域都 100% swap

| 域 | CMA swap | CMA mean fixed_ber | ML swap | ML mean fixed_ber |
|---|---|---|---|---|
| 旧 1.5/0.8 | **10/10** | 0.477 | **10/10** | 0.497 |
| 新 4.2/1.4 | **10/10** | 0.488 | **10/10** | 0.500 |

**推翻执行 agent TL-22 结论**。执行 agent 说"新域 CMA 5/5 clean 0 swap，swap 载体=ML fixed-weight"——这是 **prompt029 的 divergence trigger 检测器口径错误**（该检测器在 SOP=4e-7 新域失灵，之前 D036 已发现过同样问题）。标准分类口径下两域两均衡器都 100% swap。

旧域 CMA（10/10）与 prompt012（8/10 clean-swap + 2/10 degraded-swap，10 seeds）一致，确认 prompt030 分类逻辑正确。

### C. Phase 2 核心结论：swap 临界点在 SOP 累积旋转 29°~114°

| SOP_RATE | 累积旋转@5M late | CMA swap | ML swap |
|---|---|---|---|
| 0 | 0° | 0/10 | 0/10 |
| 1e-8 | 2.9° | 0/10 | 0/10 |
| 1e-7 | 29° | 0/10 | 0/10 |
| **4e-7** | **114°** | **10/10** | **10/10** |
| 1e-6 | 286° | **10/10** | **0/10**（见 D 段异常解析）|

**swap 是 SOP 累积旋转超过临界角的物理必然**。D014 机制坐实：旋转角大到恒模代价"正确盆地/交换盆地"势能反转，CMA 在线更新也跟着跳盆地（不是 ML 独有缺陷）。

### D. 反直觉数据解析（TL-22 物理前提检查，非 bug）

**SOP=1e-6 ML 0/10 swap——实为训练崩塌，非"不 swap"**：
- ML fixed_ber 全在 0.01~0.12（degraded/normal），不是 0.5（swap）也不是 0（clean）
- 原因：SOP 旋转 286° 过快，训练段（前 50%）与 test 段 SOP 角差距过大，ML 滤波器失效，**崩塌方式是整体性能退化而非 swap**
- 结论：ML 在极端旋转下崩得"连 swap 都不是"，是泛化失败更严重的形式

**N=8M CMA 0/5 swap（4/5 normal）——CMA 在线跟踪在长序列上重新锁住**：
- N=8M late [7M,8M) 累积旋转 182°，但 CMA fixed_ber ~1e-4（normal）
- 原因：足够长序列让 CMA 在线更新追上 SOP 漂移，重新锁定正确盆地
- 而 ML 固定权重在 8M 时 3/5 degraded_swap + 2/5 degraded——彻底跟不上
- 结论：**长序列下 CMA 在线跟踪优势显现**，ML 固定权重崩

**N=2M CMA 1/5 swap——累积旋转不足临界角**：
- N=2M late 累积旋转 ~46°，多数未过临界点，swap 率低
- 与 SOP 曲线一致：swap 概率由 SOP 累积旋转量决定，N 和 SOP_RATE 是同一物理量的两个因子

### E. 完整对比格局（CMA vs ML，跨 SOP×N）

| 条件 | CMA | ML | 含义 |
|---|---|---|---|
| SOP≤1e-7（旋转<29°） | clean | clean | 两者都正常，无 swap |
| SOP=4e-7, N=5M（旋转114°） | **swap** | **swap** | 两败俱伤（D022 域）|
| SOP=1e-6（旋转286°） | swap | **degraded/崩塌** | CMA swap，ML 崩得更惨 |
| N=8M（旋转182°，慢）| **clean（重新锁）** | degraded_swap/degraded | CMA 长序列在线跟踪优势 |

**核心张力**：ML PI-BER 优于 CMA（D022，排列不变口径），但 fixed-label 口径两者都 swap（0.5），且 ML 在极端条件（N=8M/SOP=1e-6）下崩塌更严重。**D022 优势只在 PI-BER（对 swap 失明），fixed 口径无赢家**。

### F. 对方法层定位的影响

1. **swap 是真研究问题**（SOP 物理现象，非 ML 设计缺陷）。H2 卖点不能讲"ML 比 CMA 好"（fixed 口径没赢家）；应讲"诊断 swap 临界角 + 提出 swap-aware 方法"
2. **方法层战场回到 S032 的 8 机制**，但优先级因全貌调整（见 S032 §F 更新）
3. **D022 状态**：PI-BER 优势仍成立（29/30），但须明确标注"仅 PI-BER 口径，fixed 口径两者都 swap"。H2 须重新定位
4. **执行 agent D038（B2 KILL）**：当时只测 ML swap。既然 CMA 也 swap，B2 理论上应用 CMA 重测——但 B2 机制错配（恒模盆地对功率比不敏感），大概率仍 KILL，优先级低
5. **执行 agent D039（H1 trivial Go）**：当时测 ML+H1（=PI-BER trivial）。CMA+H1 没测过，是新方向——CMA 在线跟踪 + 事后翻转标签可能是独立有效方法

## 决策引用

- D014：SOP 极化串扰是 BER 真因（prompt030 坐实 swap 临界点 29°~114°）
- D018：双口径强制——本轮证明 PI-BER 对 swap 失明，fixed 才是 swap 真记分牌
- D022：ML PI-BER 优于 standard-CMA——本轮确认仅 PI 口径成立，fixed 口径无赢家
- D027/D028：swap 是 test 段 CMA 在线跳盆地，永久锁定——prompt030 补充：N=8M 时 CMA 可重新锁住
- D031：A 类 KILL（floor+时序正交）——E1 等变网络攻其泛化痛点，prompt030 坐实 ML 泛化失败（N=8M/SOP=1e-6 崩塌）
- D038：B2 非对称功率 KILL——本轮指出应 CMA 重测但优先级低（机制错配）
- D039：H1 trivial Go——本轮指出 CMA+H1 未测是新方向
- 无新建决策（本轮是诊断，定位结论进 topic-index 不变量段，方法层方向进 todo）

## 范围确认

- 本轮是否在 scope boundary 内：是（S032 规划的诊断步骤，摸清全貌以避免跳方向）
- 无范围变更

## 后续

**关键不变量更新（进 topic-index）**：
- swap 是 SOP 累积旋转的物理现象，临界点 29°~114°，CMA 和 ML 都 swap
- PI-BER 对 swap 失明，fixed-label BER 是 swap 真记分牌
- D022 的 ML 优势仅在 PI-BER 口径成立

**方法层下一步（按依赖关系，详见 todo + S032 §F 更新）**：
1. E1 群等变（攻 SOP 泛化，prompt030 坐实）— Tier 1 优先
2. CMA+H1 组合重测（执行 agent 只测了 ML+H1）— 新方向
3. E2 排列等变 / D3 MMA — 独立方向可并行
4. B2 用 CMA 重测 — 低优先级（机制错配大概率仍 KILL）

**债务**：
- prompt029/030 检测器口径不一致已记录（divergence trigger vs correlation 分类），后续所有 swap 判定统一用 correlation 分类口径
- D036 旧域 frozen run 域不一致债仍在（D 类信息论注定 Kill，重跑意义低）
