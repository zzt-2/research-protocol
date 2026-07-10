# Topic Index: 双偏振星地光通信 DSP — Groundwork Step 1 地勘

> slug: 2026-07-10-dual-pol-osl-groundwork
> status: active | created 2026-07-10 | last_updated 2026-07-10（Step 4a 可行性评估完成：Q-DP1 Kill / Q-DP2/DP3 Conditional Go，交用户确认）

## 专题定位（一句话）

scenario-transfer-pivot 方法论准备就绪后（D001 三维度调整 + D002 角度素材 schema + D003 双偏振空间解锁），**按 FR-22 从 GW Step 1 重走地勘**，搜索空间从单偏振扩到含双偏振 OSL（sat.1553 §6 偏振解复用层 + §3/4/5 双偏振下的变化）。不是本专题继续"评估路线"，是开 GW 流程找真问题。

## 原始目标（冻结，不可修改）

**在含双偏振的星地相干 FSO（intradyne 单孔径单链路 GG 湍流 LEO）场景下，走 GW Step 1-4a 完整流程，找到过四判据的真问题（baseline M 在条件 C 下因 A 失效）和对应的合法迁移适配贡献形态。**

冻结边界：
- 守 FR-22——Step 3 精读 + Step 4a 可行性 Go/No-Go 是硬门控不可跳过
- 守"颗粒无收好过凑数"（继承上游专题）
- 不预设答案（可能找到也可能颗粒无收，诚实走完）
- 不复活 9 次 Kill 当贡献（Kill 掉的作思路素材重新进精读池，见上游 D001 维度4）

## 范围边界

### 原始目标（冻结）
见上。

### 当前范围
- **GW Step 1**（本轮）：双偏振 OSL 检索策略规划 → 执行检索 → 二轮定向 → 候选列表（守 D017 穷举门控）
- **GW Step 2**：下载 + 覆盖面缺口报告（待 Step 1 通过质量门槛）
- **GW Step 3**：精读 + 结构化提取（试 D002 角度素材 schema，3-5 篇验证后决定进不进 gw-read.md）
- **GW Step 3.5**：定向补充检索
- **GW Step 4a**：可行性 Go/No-Go

### 明确不含
- ❌ 不跳框架（地勘阶段不判方向 Go/Kill，穷举完 + 用户确认全景才推进——D017 红线 6）
- ❌ 不在检索阶段预设立 Q#（穷举完才立，D017）
- ❌ 不预设方向（§6 偏振解复用只是"回到桌面"的最大层，不是已选定方向）
- ❌ 不复活 9 次 Kill 当贡献（作思路素材重新进精读池，不变量1 仍守）
- ❌ 不推翻 9 次 Kill 的物理结论（那是事实）

### 范围变更记录
- 无（专题刚成立）

## 不变量（动任何一条必须重新讨论）

**全部继承 scenario-transfer-pivot topic-index 的 7 条不变量**（来源：2026-07-10-scenario-transfer-pivot/topic-index.md），本专题是方法论准备就绪后的 GW 执行，不重述，查上游：

1. 9 次 Kill 是物理事实不是方法论错（Kill 掉的作思路素材重新进精读池，不变量1）
2. 场景迁移合法性两条硬标准（B 场景下 A 哪个假设不成立 + 只换参数=凑数）
3. 成功论文论证套路（迁移成熟 DSP + 刻画性能边界 + 给设计准则）
4. TL-05 解析贡献比算法贡献安全
5. 继承上游全部方法论产出（地勘前置/abstract 工具错位/§7.2 核查/D017 v2/D018/D009/adaptation-scan 6 类/profile 升级）
6. 守"颗粒无收好过凑数"
7. D005 务实路线 + 找方向方法论不问导师（唯一跟导师谈=具体选定方向 + 论文结构）

**本专题新增不变量**：

8. **SC-001 许可的双偏振放宽有效**：场景设定从"单偏振 intradyne"放宽到"含双偏振 PolMUX"。其余约束（单孔径/单链路/GG 湍流/LEO）不变。双偏振动 Ch3/Ch4 的许可来自用户"可以动"（上游 D003）

## 其他结论（普通技术决策）

- **Q-DP1 共识缝 ≠ 可做方向**（TL-04 在双偏振空间验证）：5 篇独立静态 SOP 建模是真实共识缝，但"动态 SOP 致失效"因果链不成立（均衡器 300 krad/s 够用，SOP 真实来源是机械振动非湍流）。共识缝只是新颖性证据，须转译成 A 物理成立的 M-C-A 才是问题。
- **DSP 方向的 A0 适配**：A0 §2/§3/§4（ML 特性）不适用 DSP 方向，§1（性能间隙）/§5（负面证据）/§6（先验覆盖）对 DSP 反而更关键。
- **L-DP5/L-DP6 跨帧结论部分是预期性论述**：L-DP5 湍流未显式仿真，跨帧挂起是预期分析非实测。Q-DP3 进 MVE 前需用真实 GG 时间模型验证。
- **GG 时间域衰落模型是 Q-DP2/DP3 共享基建**：现有文献只给幅度 PDF，衰落持续时间/频率全篇缺失，需自建。

## 当前位置

**GW Step 4a 可行性评估完成（双偏振 OSL 子方向，Q-DP1/2/3）**。交用户确认 Go/No-Go。

- Step 1-3：完成（见 S001）
- **Step 4a：完成**——对 Q-DP1/2/3 走 gw-feasibility A0/A'/A/B/D，2 子 agent 物理量级核查 + FR-20 参数溯源
  - **Q-DP1（动态 SOP 跟踪）：No-Go（Kill）**——A0 §1 致命，均衡器 300 krad/s 高出湍流致 SOP 1-2 数量级，A 物理基础不足（D001）
  - **Q-DP2（CMA fade 发散）：Conditional Go**——空白真实（sat.1553 自认），需自建 GG 时间模型（D002）
  - **Q-DP3（跨帧恢复）：Conditional Go（首选）**——物理基础最扎实（跨帧+挂起+恢复 open 三点文献支撑），先验覆盖最低（D003）
- 优先级：Q-DP3（首选）> Q-DP2（备选）> Q-DP1（No-Go）

下一步：**交用户确认**（Q-DP1 Kill / Q-DP3 首选 / Q-DP2 备选）→ 如认可 Q-DP3，新对话进维度 D MVE（先补 FR-20 大气湍流时间模型参数）。

## 进展线索

- **S001**（2026-07-10）：双偏振 OSL 检索策略规划 → 执行（用户"一直往下做"授权）→ 15 查询穷举 + 综述补搜 + AI 候选审查 + 覆盖度评估 → Step 2 下载（tools/download + blit IEEE 两轮）→ 9 篇成功+sat.1553 → Step 3 精读（3 批 9 篇 + sat.1553§6补读 + D002 schema 试用）→ 综合分析 + 3 Q#(Q-DP1/2/3)。核心候选 43 篇 8 子方向。守 D017 穷举门控 + D018 中性提取。详见 `S001-search-strategy-dual-pol-osl.md` + `projects/thesis-fso/literature_notes.md` 双偏振 OSL 沉淀节
- **S002**（2026-07-10）：GW Step 4a 可行性评估。收 H002（Trigger 5 验证全 PASS）→ 读 gw-feasibility/glossary/TL-30/32/27 → 维度 A' 竞争分解 → 2 子 agent 物理量级核查（SOP 速率 + 衰落统计）→ Q-DP1 Kill（A0 §1 致命 D001）/ Q-DP2 Conditional Go（D002）/ Q-DP3 Conditional Go 首选（D003）→ feasibility_report.md 追加双偏振章节。守 D018 全评完才排 + FR-25 Go/Kill 分离 + TL-27 量级核算。详见 `S002-step4a-feasibility-evaluation.md` + `projects/thesis-fso/feasibility_report.md` 双偏振 OSL 节
