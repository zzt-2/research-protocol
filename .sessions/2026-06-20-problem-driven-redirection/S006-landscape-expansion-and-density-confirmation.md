# [S006] 地勘扩检索（137→430 主表）+ 死轴冷区结论加固

> 2026-06-22 | GW 重定方向 / 方法论验证 | 状态：执行完成，landscape.md v2 落盘，死轴冷区结论加固

## 目标

用户判断 S004 的 137 主表"太薄，根本没法体现什么"，要求扩到几百、IEEE 要足够多。本轮执行扩检索，核心验证一个问题：**S004 的"死轴冷区"结论是不是采样不足造成的统计假象？**

## 记录

### 步骤 1：用户决策锁定三参数（AskUserQuestion）

| 决策 | 用户选择 |
|------|---------|
| 扩到多少 | **~300**（每个主要子地带 30-50 条）|
| 扩检索怎么加词 | **加更多方法中性大背景词**（守 S003 不变量，不滑回模块锁死）|
| IEEE 多深 | **max=50 跑 5-6 条 query**（一个 session 搞定）|

### 步骤 2：设计互补词集（补第一轮盲区）

第一轮 6 词全是"星地泛指"，盲区：ISL（星间）/GEO/feeder/relay/终端/cubeSat/载荷/相干技术族/深空/网络级。

**精选 10 条 search API + 5 条 IEEE blit**（全过偏航检查 A，无模块词）：
- search: inter-satellite optical link / GEO optical communication / satellite optical feeder link / optical satellite relay / satellite optical terminal / cubeSat optical communication / optical satellite payload / coherent satellite optical communication / deep space optical communication / optical satellite network
- IEEE: inter-satellite optical link / GEO optical communication / satellite optical terminal / coherent satellite optical communication / deep space optical communication

### 步骤 3：派 3 子 agent 并行执行

- **Agent A（search 5 词）**：ISL/GEO/feeder/relay/terminal → 150 raw → ~78 主表（≥2019）
- **Agent B（search 5 词）**：cubeSat/payload/coherent/deep-space/network → 150 raw → 142 主表
- **Agent C（IEEE blit 5 词）**：ISL/GEO/terminal/coherent/deep-space → 125 raw（5×25，blit 实际单 query 上限 25 非 50）→ 56 主表

IEEE blit 通道健康（S005 修复后）：5/5 query 成功，3 条冷启动重试 1 次，quota ~7/50。发现 blit 单 query 硬顶 25 条（非 50，未触发分页）。

### 步骤 4：主线全量合并去重

24 个 JSON 源（round1 6 + round2 search 10 + round2 IEEE 5 + 诊断验证 3）全量合并：

| 指标 | 数值 |
|------|------|
| raw 总和 | 635 |
| 去重唯一 | 518 |
| 主表（≥2019） | **430** |
| <2019（附录） | 81 |
| unknown year | 7 |

**目标达成且超额**：用户要 ~300，实际 430（3.1 倍于 v1 的 137）。

### 步骤 5：子地带密度复评（核心验证）

**关键发现——死轴冷区结论加固**：

| 子地带 | v1(137条) | v2(430条) | 占比变化 |
|--------|-----------|-----------|---------|
| 载波同步 | 7 | **23** | 5.1% → 5.3%（仍冷）|
| 信道估计/均衡 | 2 | **13** | 1.5% → 3.0%（仍冷）|
| 网络层（热区）| 48 | **158** | 35% → 37% |
| 地面站（热区）| 65 | **155** | 47% → 36% |

载波同步从 7→23、信道估计从 2→13，绝对数涨了但**相对占比仍远低于热区**（5.3% vs 37%）。**这排除了"冷区是采样不足造成的统计假象"的质疑**——扩 3 倍后冷区还是冷，是结构性事实。

缝潜力分布：🟢 从 19 涨到 48，🟡 338，🔴 44。🟢 候选更充分。

### 步骤 6：落盘 landscape.md v2 + 偏航检查复跑

落盘 `projects/thesis-fso/landscape.md`（618 行，430 主表 + 5 项 🔴 必填 + 3 附录）。**偏航检查 A-E 复跑全过**：
- A：16 query 全方法中性 ✅
- B：518 全留自洽（430+81+7=518），5 项 🔴 必填全在，无臆造语言 ✅
- C：18 个子地带涌现（比 v1 的 13 个更丰富）✅
- D：本轮是评估停点，不选地 ✅
- E：🔴 标饱和不标难验证 ✅

### 步骤 7：质量评估

**Q1 信噪比**：635 raw → 518 deduped → 430 主表。noise ~90 条（新闻/产品/成像载荷/通用 FSO 无卫星上下文/百科视频），占 raw ~14%。`optical satellite payload` query 拉入大量 EO 成像载荷误命中（高光谱/多光谱），是本轮主要 noise 源。信噪比合格。

**Q2 摸清谁在做什么**：18 个子地带涌现，比 v1 的 13 个更全。新增涌现：ISL(125)/feeder(92)/深空(44)/放大器载荷(62)——这些在 v1 里几乎没覆盖。**领域全景更完整**。

**Q3 字段填得实不实**：IEEE 无 abstract 的 ~111 条 baseline/验证方式默认"未明确(IEEE无abstract)"，缝潜力默认 🟡——诚实但不臆造。search API 有 abstract 的按字面证据填。整体偏保守，符合"初判不是结论"。

**Q4 方法要不要改**：**不要**。扩检索方法（方法中性大背景词 + 全留 + IEEE 补）验证有效。死轴冷区结论加固后，下一轮选地时应避开载波同步/信道估计两轴（H002 🔴 必填已标记）。

### 步骤 8：本轮明确不做（停点遵守）

- ❌ 没选地（没做 🟢/🟡/🔴 分类，只更新了缝潜力初判字段）
- ❌ 没进批评汇总
- ❌ 没继续 "Are PLLs dead?" 候选

## 决策引用

- 本轮无新建 D###（执行性工作非方向决策）。引用 D001/D002（🔴 必填来源）。

## 范围确认

- 本轮在 scope boundary 内：执行地勘扩检索（用户明确要求），不越界。
- 未碰"明确不含"项。

## 后续

### 下一轮（用户决策后）的可执行接口

landscape.md v2（430 主表）已就绪。下一轮（新对话）：
1. 读 landscape.md v2 + S006 + topic-index 不变量段
2. 主线做 🟢/🟡/🔴 三分（H002 L42-48 判据）
3. 看哪块 🟢 最值得进批评汇总——🟢 48 条候选，集中在：
   - **信道建模/湍流**（111 条总数，多条 abstract 自陈模型失效：lognormal 误用/beam-wander 局限/Málaga 场景）
   - **ATP/指向**（105 条，tip-tilt 退化源/PAT 延迟被忽略/point-ahead 问题）
   - **调制/复用**（86 条，PAM4 灵敏度 vs DP-QPSK/OAM 抗湍流退化）
   - **网络层/路由**（158 条，波长受限/拓扑低效/链路可用度不确定性）
   - **相干检测**（58 条，接收复杂度/相位恢复/外差实时）
4. 选一块地进批评汇总（框法乙找 Q#）→ 四判据 → FR-21 验缝 → Q# 进 4a

### 关键观察供下一轮

- **死轴冷区加固**：载波同步 23/430=5.3%、信道估计 13/430=3.0%，扩 3 倍后仍冷。**结构性地避开这两轴**。
- **热区候选密度排序**：网络层(158) > 地面站(155) > 链路预算(128) > ISL(125) > 在轨演示(117) > 信道建模(111) > ATP(105) > feeder(92) > 调制复用(86)。
- **🟢 48 条是初步信号**，需批评汇总验证 baseline 真失效。密度高 ≠ 有缝。
- **IEEE 贡献**：125 raw 去重后贡献显著（ISL/相干/深空/GEO/终端 IEEE 专属内容），S005 修复有效。

### 遗留债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| IEEE 单 query 上限 25（非 50） | 想要更深 IEEE 覆盖 | blit 未实现分页 | 如需 IEEE 第 2/3 页，改 blit.py 加分页逻辑 |
| SPIE 部分页反爬拦截 | abstract 完整性 | 标 🟡 待精读 | 精读阶段用 DOI 直接查 |
| abstract baseline 信息密度低 | 找缝要看 baseline | 430 主表大量"baseline 未明确" | 选地进批评汇总时精读补 |
| `optical satellite payload` 拉入大量 EO 成像载荷 | 检索精度 | noise 进附录已记录 | 非阻塞 |

## 跨对话续接必读

1. 本文件 S006
2. **`projects/thesis-fso/landscape.md`（v2，430 主表）**
3. topic-index 不变量段（8 条）
4. S004（v1 地勘执行，本轮是它的扩检索）
5. S005（IEEE blit 修复）
6. H002（偏航检查 A-E + landscape.md schema）
7. `stages/glossary.md`（四判据，下一轮选地要用）
