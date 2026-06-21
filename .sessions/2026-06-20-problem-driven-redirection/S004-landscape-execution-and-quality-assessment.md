# [S004] 地勘执行（IEEE blit 失败 + search API 落盘 landscape.md）+ 偏航检查 A-E + 质量评估

> 2026-06-21 | GW 重定方向 / 方法论验证 | 状态：执行完成，landscape.md 落盘，方法论地勘这步**过了**，但 IEEE 通道失败留下债务

## 目标

执行 H002 指定的下一步——派子 agent 做地勘式检索，产 landscape.md 全景表。**停点用户锁定**：只到 landscape.md 落盘 + 偏航检查 A-E + 质量评估，不选地、不进批评汇总。本轮根本目的仍是**验证地勘这步方法论能不能用**，不是推进论文。

## 记录：执行全过程原原本本

### 步骤 0：新对话报到 + handoff 接收（Trigger 1 + Trigger 5）

- 读 H002 + S003 + topic-index + voice.md + _registry.yaml + thesis-fso/master-state.md
- 验证 H002 的 4 条关键事实声称，**全部 PASS**：
  1. S003 确实把方法论从"批评汇总第一步"迭代为"地勘前置" ✅（S003 L101-110 + topic-index 范围变更记录）
  2. 范围确实从"物理层锁死"放开为"星地激光通信全谱" ✅（topic-index 当前范围 + 范围变更记录）
  3. 载波同步确实是 5 次失败核心子环节 ✅（S003 第三步表 N1 PCS / A3 CPE 均载波同步子环节 + master-state 历史教训锚点）
  4. depends_on 已稳定（4b1 closed + framework-evolution LOG-001 落盘）✅

### 步骤 1：修 master-state §8 一致性债务（handoff 接收本职）

H002 L121 已知债务表 + voice.md L26 跨对话点评"消除文件矛盾属于 handoff 接收本职不是越界——别积压"。master-state §8 原写"批评汇总先于精读"（旧方法论），与 S003 迭代后的"地勘先于批评汇总先于精读"冲突。

**修复**：
- §8 重写为 8 步执行表 + 方法论链路图（地勘→选地→批评汇总→四判据→FR-21 验缝→Q# 进 4a）
- §2 当前位置同步更新
- front-matter `direction` 行从"星地湍流激光通信…载波同步/信道估计/资源调度方向待精读后从问题清单浮出"改为"星地激光通信（FSO）——子地带由地勘全景表分类后选定，不预设"

### 步骤 2：EnterPlanMode 锁三决策（用户参与把关）

按 global-rules"先讨论先锁边界再执行"+ H002"派子 agent 前把检索词先列出来过目"，进 plan mode，派 2 个 Explore agent 并行探查 S002 派任务模式 + landscape schema + search-archive 现状。

**3 个决策点（AskUserQuestion）**：

| 决策 | 用户选择 |
|------|---------|
| IEEE 覆盖方式（用户偏好"ieee 为主"） | **blit 单 agent 串行补 IEEE**（而非纯 search） |
| 并发拆分维度 | **按检索词族并行（3 agent）** |
| 本轮停点 | **只到 landscape.md 落盘 + 偏航检查 + 质量评估**（不选地、不进批评汇总） |

检索词集（方法中性，全过偏航检查 A）：6 条 search + 5 条 blit IEEE，全不含 synchronization/estimation/modulation/coding/equalization 模块词。

### 步骤 3：派 3 个子 agent 并行执行（单消息 3 调用）

- **Agent 1（search·英文词族 A）**：`tools/search` × 3 query（satellite optical communication / satellite laser communication / LEO optical downlink）
- **Agent 2（search·英文词族 B）**：`tools/search` × 3 query（free-space optical satellite / space-to-ground optical link / satellite optical ground station）
- **Agent 3（blit·IEEE）**：`tools/blit --source ieee` 串行 × 5 query

每个 agent 收到自包含 brief：TL;DR + 背景（标"了解即可不对照评价"）+ 执行方式（完整命令）+ 6 字段产出格式 + 已知陷阱（基于 S002 失败经验）+ 验收 checklist + 5 条最高纪律。

### 步骤 4：3 agent 回传——2 成功 1 失败

#### 4.1 Agent 3（blit IEEE）失败 ❌

**子 agent 诊断**：IEEE HTTP 418（IP 封锁），未跑任何 query（0/50 quota 消耗），按纪律停止。报告 3 个阻塞：① IEEE 主动封锁 IP（HTTP 418）；② 平台假设错误（实际 MINGW64 非 WSL）；③ 只读 agent 无法写文件。

**主线独立验证（不自审自验）**：
```bash
curl -s -o /dev/null -w "IEEE HTTP: %{http_code}\n" --max-time 10 https://ieeexplore.ieee.org/
→ IEEE HTTP: 418
```
**主线复测确认 418 属实**——校园网 IP 不在本机生效，IEEE 通道本轮放弃正确。不浪费用户时间硬试。按风险预案 1：仅靠 search API 6 条覆盖。

**遗留债务**：换校园网环境后可补 blit（见 decisions.md / topic-index 债务段）。API 已命中 33/165 条 IEEE venue，覆盖度暂可接受。

#### 4.2 Agent 1 + Agent 2（search API）成功 ✅

- Agent 1：3 query × 30 = 90 raw → 73 去重（61 主表 + 12 noise）
- Agent 2：3 query × 30 = 90 raw → 86 去重（70 主表 + 16 noise）
- 检索障碍：SerpAPI 全程报 `google-search-results not installed, skipped`（6 query 均失败）；S2 + OpenAlex + Exa 正常

### 步骤 5：主线跨 agent 合并去重 + 落盘 landscape.md

用 Python 脚本（`tools/_gen_landscape.py`）做规范化标题去重合并：

| 指标 | 数值 |
|------|------|
| 6 query raw | 180 |
| 跨 query dups | 15 |
| 去重唯一 | 165 |
| ≥2019（主表） | 137 |
| <2019（附录 A） | 21 |
| unknown year（附录 B） | 7 |

**年份分布（deduped）**：2019=12, 2020=5, 2021=14, 2022=16, 2023=17, 2024=18, 2025=42（最密）, 2026=13, ?=7。近 3 年（2023-2026）占主体。

**来源分布**：S2=109, Exa=52, 混合=4；OpenAlex 在 total 计数但 source_api 未标注。

**缝潜力分布（137 主表）**：🟢=19, 🟡=96, 🔴=22（🔴 含 5 项必填预置，其余 17 是 abstract 自陈成熟/广泛采用）。

**落盘**：`projects/thesis-fso/landscape.md`（252 行，137 主表行 + 5 项 🔴 必填 + 3 个附录）。

### 步骤 6：偏航检查 A-E（H002 清单逐条对照，主线独立验证）

| 检查项 | 结果 | 证据 |
|--------|------|------|
| **A.1** 检索词方法中性不锁模块 | ✅ PASS | grep 6 query 全无 synchronization/estimation/modulation/coding/equalization/sync/carrier/phase/frequency offset |
| **A.2** 有没有"我觉得 X 地带值得做"绕开全景表 | ✅ PASS | 本轮没选地，停点就是评估 |
| **B.1** landscape.md 全留 | ✅ PASS | 137(主) + 21(<2019) + 7(unknown) = 165 = total_deduped |
| **B.2** 🔴 死地 5 项必填标进去 | ✅ PASS | 载波同步/自适应交织/GG-LLR/MCS排程/信道估计LS-LMS-RLS 5 项均在表 |
| **B.3** 缝潜力凭证据不臆造 | ✅ PASS | grep 无"应该算有缝/我觉得/感觉/可能算/大概有"；🟢 全部带"abstract 自陈"理由 |
| **C** 种子从全景表涌现不预设 | ✅ PASS | 13 个子地带从 abstract keyword 涌现，无预设候选 |
| **D** 先评估质量再选地 | ✅ PASS | 本轮就是评估，没跳到选地 |
| **E** 难度≠否决（🔴 标饱和不标难验证） | ✅ PASS | 5 项 🔴 理由全是"物理天花板/0dB/oracle 0.09dB/拥挤赛道"，无"难验证" |

**偏航检查全部 PASS。**

### 步骤 7：质量评估（H002"再评估 landscape.md 质量"4 问）

#### Q1：信噪比如何？

- 6 query × 30 = 180 → 165 去重 → 137 主表（2019+）
- noise 占比：Agent 1 附录 12 + Agent 2 附录 16 = 28 条新闻稿/营销/视频/百科/无人机-地面（占 raw 的 ~17%）
- **信噪比合格**——去除商业 noise 后 137 条研究产出是实质内容，不是水。新闻稿/产品页占比高反映该领域处于工程化阶段（TBIRD/OSIRIS/LCRD 等在轨任务密集）。

#### Q2：摸清"谁在做什么"了吗？

**子地带涌现分布（核心发现）**：

```
  65  地面站/OGS/硬件/终端
  48  网络层/路由/调度
  47  信道建模/闪烁/湍流
  46  ATP/指向/PAT/捕获
  35  在轨演示/任务 (TBIRD/OSIRIS/LCRD/DSOC)
  27  调制/复用 (OAM/WDM/PDM/OFDM/PAM4/PPM)
  18  QKD/量子
  15  AO/自适应光学/波前
  10  相干/自相干检测
   7  语义/AI/DL/ML
   7  载波同步/恢复  ← 5 次失败死轴，地勘里几乎不涌现
   7  编码/FEC/交织
   2  信道估计/均衡   ← 另一死轴，极度稀疏
```

**摸清了，且照出了一个关键事实**：之前 5 次撞死的轴（载波同步 7 条 / 信道估计 2 条）在整个领域其实是**冷区**。热区在地面站/网络层/ATP/调制复用。

**这是地勘这步的方法论价值所在**——如果不做地勘，S002 的"批评汇总"会继续在死轴里找（因为批评信息集中在历史撞过的地方）；地勘照出了"死轴本就是窄冷区"这个结构性事实。

#### Q3：字段填得实不实？

- baseline 是谁：大量"未明确"（abstract 不提 baseline 就不填，不臆造）——诚实但信息密度低。这反映 abstract 本身很少显式 baseline。
- 增益怎么验证：仿真/实测/解析/综述四类标注，基于 abstract 字面——可靠。
- 缝潜力初判：🟢 全部带"abstract 自陈"具体引用句，🟡 分"abstract 无缝信号"和"abstract 自陈达成增益"两亚类——可追溯。
- **诚实但偏保守**——宁可标 🟡 待精读也不臆造缝潜力，符合 H002"初判不是结论"。

#### Q4：地勘这步方法本身要不要改？

**方法论评估**：
- ✅ **方法可用**——产出了结构化全景表，照出了死轴 vs 热区的结构性对照，这正是 H002 想要的。
- ✅ **没滑回先有方法**——13 子地带涌现，无预设。
- ⚠️ **IEEE 通道失败是债务不是方法问题**——换校园网环境就能补，不否定地勘方法本身。
- ⚠️ **abstract baseline 信息密度低**——137 主表大量"baseline 未明确"，这影响后续批评汇总阶段（找缝要看 baseline）。但这不是地勘这步的问题，是 abstract 本身的限制。下一轮选地进批评汇总时，精读补 baseline。
- ⚠️ **🟢 只有 19 条（14%）**——比例偏低。但符合预期：地勘是全景不是找缝，🟢 应该稀疏（初判保守）。真正找缝是下一轮批评汇总的事。

**结论**：地勘这步方法**过了**。产出质量够支撑下一步（看分类、选地进批评汇总）。不需要迭代地勘方法本身。IEEE 通道失败记为债务，换环境补。

### 步骤 8：本轮明确不做（用户锁定停点遵守）

- ❌ 没选地（没标 🟢/🟡/🔴 分类——只填了缝潜力初判字段，分类是下一轮事）
- ❌ 没进批评汇总
- ❌ 没继续 "Are PLLs dead?" 候选（H002 L103 Kill）
- ❌ 没擅自扩大范围（11 条 query 锁定，不临时加）

## 决策引用

- D001：Kill Xie 独立性假设（S002，引用，本轮无新建）
- D002：Kill GG-LLR 译码（S003，引用，本轮 🔴 必填项用到）
- **本轮无新建 D###**——landscape.md 落盘 + 偏航检查 + 质量评估是执行性工作，不是方向决策。IEEE 通道失败记为债务（topic-index 已知债务段），不立 D（不涉及方向选择，只是工具可用性）。

## 范围确认

- 本轮在 scope boundary 内：执行地勘（H002 指定的下一步），正是本专题核心。未越界。
- IEEE blit 失败转纯 API 覆盖是执行中的工具调整，不是 scope change（在不变量 6"背景锁死星地激光通信"内，只换检索通道）。
- 没碰"明确不含"项（开题 4 线索当种子、继续 "Are PLLs dead?" 候选）。

## 后续

### 下一轮（用户决策后）的可执行接口

本轮产出 `projects/thesis-fso/landscape.md` 已落盘，可复用。下一轮（新对话）按 H002 §"拉完表后分类"做：

1. **读 landscape.md + 本 S004**——重点看子地带涌现分布 + 死轴冷区发现
2. **主线做分类（🟢/🟡/🔴 三分，按缝潜力）**——H002 L42-48 已给分类判据
3. **看哪块 🟢 最值得进批评汇总**——初步看候选：调制/复用（27 条，含 OAM/WDM/OFDM 多条 🟢）、ATP/指向（46 条，多条 abstract 自陈失效）、网络层/调度（48 条）、信道建模（47 条）
4. **选一块地进批评汇总**（框法乙找 Q#）→ 四判据 → FR-21 验缝 → Q# 进 4a

### 关键观察供下一轮参考

- **死轴冷区发现**：载波同步 7 条 / 信道估计 2 条，地勘照出这俩是领域冷区。下一轮选地时应避开这两轴（H002 🔴 必填已标记）。
- **热区候选**：地面站/网络层/ATP/调制复用四簇最密。但密度高 ≠ 有缝——需要进批评汇总看 baseline 失效证据。
- **🟢 19 条集中在**：信道建模（lognormal 误用、beam-wander 模型局限）、ATP（tip-tilt 退化源、PAT 延迟被忽略）、调制（PAM4 灵敏度 vs DP-QPSK）、网络层（链路可用度不确定性首建模）、接收（SNSPD 延迟限制动态范围）。这些是初步信号，需批评汇总验证。

### 遗留债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| IEEE blit 通道失败（HTTP 418） | IEEE 是用户偏好主力源 | 本轮纯 API 覆盖（33/165 IEEE venue） | 换校园网环境后补 blit，或主线在校园网机器重跑 |
| abstract baseline 信息密度低 | 找缝要看 baseline | 137 主表大量"baseline 未明确" | 选地进批评汇总时精读补 |
| SerpAPI 全程失败 | 多源覆盖 | S2+OpenAlex+Exa 已够 | 非阻塞，记录即可 |

## 跨对话续接必读

1. 本文件 S004（本轮完整执行日志）
2. **`projects/thesis-fso/landscape.md`**（本轮核心产出，137 主表 + 5 项 🔴 必填）
3. topic-index 不变量段（8 条，S003 更新版）
4. S003（方法论迭代完整脉络）
5. H002（偏航检查清单 A-E + landscape.md schema）
6. `stages/glossary.md`（四判据，下一轮选地过判据要用）
