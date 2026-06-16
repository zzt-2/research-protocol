# [R006] 大规模补盲扫描：按主导损伤重组 + 5 维度盲区补扫

> 2026-06-16 续 2 | 关联：S003 / D003 / D001 / R002 / R005 / PROMPT-003
> 状态：5 子 agent 全部撞 harness 600s 硬上限超时（PROMPT 设计 ≤900s）→ 转 salvage 路径（digest 10 已成 JSON + 主对话补 β1×2/β2×3）→ 15 JSON ~180 hits 消化 + E 三检验完成（TENTATIVE 摘要级）
> 置信度：摘要级 + abstract 初判（与 S002/R005 同级），进 Groundwork 精读后可能回升/推翻

## 调研问题

用户反馈"方向还是太少了"——B1 FAIL（D003）后干净候选仅 A3 + 2.2，离"2-3 个可行方向"原始目标还远。PROMPT-003 授权大规模补盲扫描：
- **A 轴（新视角）**：按 Paillier 2020 主导损伤（残余幅度闪烁 + 激光相位噪声）重组扫跨模块处理组合——之前按"模块"切可能漏掉"一个损伤跨多模块处理"的方向
- **B 轴**：补 5 盲区（β1 DSP 流水线 / β2 系统架构 / β3 信息论 / β4 跨领域 / β5 局部动态）
- **目标**：候选池扩到 15-20 个 + 粗筛分级表

## 执行实况（关键事件，治理记录）

**5 子 agent 并行全部超时**：
- Agent-α1/α2/β3：在撞 harness 硬上限（600000ms）前已写出 10 份检索 JSON（α1×2 / α2×6 / β3×2），但未完成"读结果→E 检验→结构化返回"阶段
- Agent-β1/β2：空手超时，无 JSON 落盘
- 这是 PROMPT-003 L95 设计的 escape hatch（"若某 agent 超时或需多轮检索，写 handoff 分对话"）

**Salvage 路径（避免再次空手重派）**：
1. 写 `_digest_blindspot_scan.py`（紧凑提取，abstract 截 300 字符，结构化非 HTML），把 10 份 JSON digest 成 71.8KB 可读 markdown
2. 主对话直接跑 `tools/search`（脚本，AGENTS.md 允许）补 β1×2（定时/均衡）+ β2×3（波长分集/容量中继/中继）共 5 JSON
3. 主对话消化全部 15 JSON ~180 hits，在主线程做 E 三检验 + TL-04 + 主导损伤相关性 + 去重

**检索 slug（15 份新 JSON，均落 `search-archive/2026-06-16/`）**：
- α1：`pilot-amplitude-fading-scintillation-deep-fade-coherent-fso` / `pilot-symbol-assisted-fading-amplitude-scintillation-deep-fa`
- α2：`pilot-aided-carrier-phase-estimation-satellite-optical-commu` / `pilot-aided-phase-estimation-satellite-optical-turbulence` / `laser-linewidth-tolerance-carrier-phase-estimation-bps-blind` / `linewidth-tolerant-cpe-bps-coherent-fso` / `differential-qpsk-dqpsk-detection-atmospheric-turbulence-fre` / `differential-dqpsk-detection-fso-turbulence-penalty`
- β3：`rf-satellite-coherent-communication-carrier-synchronization-` / `rf-satellite-coherent-carrier-sync-migration-fso`
- β1（主对话补）：`timing-recovery-gardner-godard-satellite-optical-fade` / `adaptive-equalization-cma-dd-lms-fso-deep-fade`
- β2（主对话补）：`wavelength-diversity-fso-coherent-satellite` / `coherent-fso-capacity-outage-gamma-gamma` / `coherent-fso-relay-df-af-satellite`
- 临时产物：`_digest_blindspot_scan.py` / `_digest_output.md`（合并对话可删）

---

## 发现（核心结论：本轮扫描的"负结果"性质）

### 总览：本轮**未达成 PROMPT-003 "扩到 15-20 个"目标**，但产出净增 1 个真新候选 + 若干候选的 refinement + 一组强化性负发现

诚实地报告：15 JSON ~180 hits 经筛子（E≥2 + TL-04 + 主导损伤相关性 + D 排除 + 去重）后，**几乎全部命中都坍缩回已有候选族或已被证伪的失败模式**。这本身是一个**有价值的负发现**——它强化了 S003 的"出井没有明显更好方向"判断，但**反向回答了用户"方向太少"的诉求**：方向少不是扫描不充分，是该物理问题的可行解空间本来就窄。

**筛子筛掉的命中分布（模式化，重要）**：
| 命中模式 | 出现的轴 | 为何砍 | 关联教训 |
|---|---|---|---|
| DL/BiGRU/CNN 信道估计均衡 | α1/α2/β1/β3 反复出现 | "DL 检测器套湍流"=教科书反例；导频 MMSE 在 GG 下已接近完美 | R005 维度4 + TL-05/TL-10 + Amirabadi 自述 |
| AMC/HARQ/自适应速率反馈类 | α1（AGC+编码）/β2 | 星地 RTT~10ms ≫ 湍流相干 2-10ms，反馈物理不可行 | R005 维度5 + TL-03 |
| 多孔径/MIMO-CMA/OAM/模分复用 | β1/β2 | 需专用接收阵列硬件 | D001 D 排除列#2 + S001 |
| 新湍流分布（IGGG/IGG/Málaga）BER 闭合解 | β2 容量/中继 | 换分布重做 BER = 常识重做 | R005 维度3 3.2 + E 反例检验 |
| 光纤 CPE 算法（BPS/two-stage/NFT）迁 FSO | α2 主力 | R002 B 组已扫，且多数论文不建模湍流 | R002 B组 |
| 光学硬件方案（OPC/相位共轭/全光匹配滤波/OPLL） | α2/β3 | 专用光电硬件 | D001 D 排除列#2 |
| 差分 DQPSK 性能比较 | α2 | 全 IM/DD 调制对比，无相干湍流创新 | E1 常识重做 |
| RF 卫星同步迁移 | β3 | RF 与 FSO 波长差 5-6 个数量级，迁移变常识或物理无意义 | TL-04 |
| 调制比较（OOK/PPM/BPSK/DPSK in turbulence） | α1/α2 | 重复多年对比 | E1 常识重做 |

### 留下的候选

#### 新候选（1 个 net-new）

**N1. 静态概率星座整形（PCS）适配湍流 SNR 分布的相干 FSO**
- **来源轴**：α2（激光相位噪声 + 高阶调制 CPE 容忍）+ β3 间接（PCS-FSO cite=81 启发）
- **思路**：PCS（Probabilistic Constellation Shaping，Maxwell-Boltzmann 分布匹配）按湍流 SNR 分布**离线优化**星座点概率分布（非实时反馈——发射端固定一套适配 GG 统计的 PCS 分布），在 deep fade 统计上获得 shaping gain。**关键：无需跨 RTT 反馈**（PCS 分布是离线按长期 SNR 统计设计的，非每帧自适应）→ 避开 TL-03 反馈陷阱
- **关键论文**：
  - "Adaptive probabilistic shaped modulation for high-capacity free-space optical links" (2020, cite=81) — **abstract 已验证，PCS-FSO 早期工作**
  - "End-to-end optimization of constellation shaping for Wiener phase noise channels with a differentiable blind phase search" (2023, cite=35) — PCS + 激光相位噪声联合（光纤，待迁移）
- **E 三检验**：反例 ✓（PCS for 湍流相干检测非教科书，需分布匹配 + CPE 容忍联合设计）/ 非平凡 ✓（GG 分布匹配 + 线宽容忍 CPE 耦合不显然）/ 可比较 ✓（vs uniform QAM + vs AMC-2.1 有明确 baseline）→ **3/3**
- **TL-04**：技术障碍（PCS 在相干 FSO + 湍流下未充分探索；与激光相位噪声 CPE 的耦合是 open），非物理无意义 → 可突破
- **主导损伤相关性**：✓ 针对幅度闪烁（SNR 分布 shaping）+ ✓ 兼顾激光相位噪声（与线宽容忍 CPE 联合）
- **D 排除列**：不命中（纯 DSP + 仿真）
- **与已有候选去重**：**新**。与 R005 2.1（ML 预测 AMC）区别——2.1 是**实时预测自适应**（跨 RTT，TL-03 风险），N1 是**离线静态 PCS**（不跨 RTT）。与 R005 2.2（频谱效率闭合解）区别——2.2 纯解析，N1 是 DSP 实现 + 可配解析性能界
- **风险/待验证**：PCS gain 在强湍流 deep fade 下是否被 SNR 方差稀释（需精读 cite=81 验证 gain 数据）；线宽容忍 CPE 与 PCS 的耦合设计

#### Refinement 候选（强化已有候选的基线/对照，非新方向）

**R-A3. A3（导频抗 deep fade）的 CPE 基线资产 + 物理基础再确认**
- α2 命中"Low-complexity CPE for space coherent optical communication"（DOI 10.1117/12.3059522）+ "Pilot-Assisted Phase Recovery with Robust Locally Weighted Interpolation"——为 A3 提供 **CPE 对照基线论文**（A3 是导频抗 fade，CPE 是相位估计，二者在载波恢复模块内互补）
- α1 命中"Field demonstration of turbulence-resilient self-coherent FSO with pilot-assisted scheme"（2025, cite=10）——**A3 思路的实验验证（自相干版）**，强化 A3 物理基础
- **结论**：A3 作为井内首选的地位**进一步强化**（更多基线 + 实验证据 + 主导损伤针对性）

**R-2.2. 2.2（自适应频谱效率闭合解）的相干容量变体**
- β2 容量命中全部是 RIS/UAV/新分布 BER，但**反向提示**：相干 FSO（非 IM/DD）在 GG 下的**容量界/outage 容量**仍是相对空白（多数容量论文是 IM/DD）。2.2 可扩展为"相干检测 h·γ̄ 模型的 outage 容量闭合解"——但**与 2.2 核心重合**，作为 2.2 的一个解析分支，非独立新方向
- **结论**：2.2 解析保底地位不变，可深化为相干容量分支

#### 强化性负发现（对决策有实质影响）

**F1. 激光相位噪声（α2）的"跨模块组合"视角未产出新方向**
- 激光相位噪声处理空间（线宽容忍 CPE / 导频相位 / 差分 / OPLL / 多级 CPE）的命中**绝大多数是光纤 CPE 算法**（R002 B 组已扫），且多数论文**不建模湍流**
- 差分 DQPSK 命中全是 IM/DD 调制比较
- **含义**：α2 轴没有发现"跨模块组合处理激光相位噪声"的新切入点。激光相位噪声作为主导损伤，其处理已被光纤 DSP 社区充分覆盖，迁移到 FSO 是 R002 B 组的既定路线（非新方向）。**但**——这为 D001 D 排除补充一条观察：激光相位噪声方向的高质量 baseline 充足（光纤 CPE 可直接复用为对照）

**F2. β4 跨领域迁移物理可行性差**
- RF 卫星同步迁移：RF 波长（cm-m）与 FSO（μm）差 5-6 数量级，多普勒/CFO 量级、信道模型完全不同，迁移要么变常识（换介质套公式）要么物理无意义
- 水下/VLC：本轮未专门检索（β3 子 agent 超时前只完成 RF），但物理介质差异更大
- **含义**：β4 跨领域迁移**整体低产出**，与 R002 漏斗判断一致——FSO 内部信号处理自洽，外部迁移收益低

**F3. 局部动态（β5）几乎全部坍缩到 TL-03 或硬件**
- deep fade 瞬态检测 → 若反馈式 = TL-03 砍；若前端处理 = 多与 A3 重合
- 跟踪-失锁-重捕 → cycle slip 恢复，命中少且偏光纤
- **含义**：β5 局部动态**没有产出独立新方向**，但确认了"参数区间内局部动态"的可行处理都收敛到 A3（导频抗 fade）族

---

## 候选池总览（R006 合并后）

| # | 方向 | 来源 | 状态（R006 后）| 物理前提 |
|---|---|---|---|---|
| **A3** | 导频抗 deep fade（幅度鲁棒）| R002/S003 | **首选（强化）**— R006 加 CPE 基线 + 实验证据 | 追主导损伤（幅度）|
| **2.2** | 自干 FSO 自适应频谱效率闭合解（解析保底）| R005 | **保底（可深化相干容量分支）**| 不受物理波动影响 |
| **N1** | 静态 PCS 适配湍流 SNR 分布 | R006 新 | **新候选（待精读 cite=81 验证 gain）**| 离线 PCS 不跨 RTT，避 TL-03 |
| 1.1 | 预测驱动自适应 LDPC | R005 | 留（需 §B 预测器跨 RTT）| TL-03 风险 |
| 2.1 | ML 信道预测 AMC | R005 | 留（同 1.1）| TL-03 风险 |
| 1.3 | DTAT-FSO | R005 | 次优先 | 偏信源信道编码 |
| E1 | 湍流时间相关性→载波跟踪 | R002 | 高风险（需过 Paillier 对照）| 与 B1 同前提 |
| B1 | PLL 联合建模 | R002 | **FAIL（D003）** | 物理死锁 |
| B2/A2/C2/D2 | 存疑 | S002 | 存疑 | — |

**R006 后干净候选**：A3（强化）+ 2.2（保底）+ **N1（新）= 3 个**（仍未达"2-3 个可行方向"上限，但 N1 是实质新增）。带 §B 待检的 1.1/2.1 仍可作为井外备选。

---

## 关键观察（对决策有影响）

### 1. 本轮扫描的"负结果"实质：方向少 ≠ 扫描不充分

PROMPT-003 假设"按主导损伤重组 + 补盲区能扩候选池"。**执行后发现**：新视角（按损伤切）确实照亮了跨模块组合的可能性，但**几乎所有跨模块组合都坍缩回已有候选族或已被证伪的失败模式**。这**强化**了 S003 的判断："载波同步井不是采样偏差，是物理确有需求的少数问题"——本轮把"井外"也扫透了，结论是**井外没有明显更好的，且井内"幅度鲁棒"类（A3）持续被强化**。

**对用户"方向太少"诉求的诚实回答**：方向少**不是扫描不充分**（本轮 15 JSON ~180 hits 覆盖 5 盲区 + 2 损伤轴），**是该物理问题的可行解空间本来就窄**。继续扫的边际收益递减。N1（PCS）是本轮唯一净增，且需精读验证。

### 2. A3 的地位从"井内首选"升级为"跨扫描共识首选"

三轮扫描（R002 载波同步井 / R005 出井 / R006 按损伤重组 + 盲区）**都指向 A3 或 A3 族**：
- R002：A3 导频抗 fade（载波恢复模块内）
- R005：1.1/2.1 幅度/预测问题（井外，但共享 TL-03 风险）
- R006：α1 幅度闪烁处理全部坍缩到 A3 族；β5 局部动态可行处理收敛到 A3；F1 确认激光相位噪声有充足 baseline
- **物理基础**：Paillier 2020 "残余幅度闪烁是主导损伤" → A3 追主导损伤，针对性最强

**含义**：A3 不是"因为别的都失败了所以选 A3"，而是"三轮独立视角都收敛到 A3"。这是**更强的支持**，但仍需 Groundwork §B（A3 三重障碍在 Paillier 主导损伤结论下的重评）。

### 3. N1（PCS）是"非反馈式自适应"的可行代表，值得精读

N1 的价值：它是**唯一一个既针对主导损伤（幅度闪烁 SNR 分布）又避开 TL-03 反馈陷阱（离线 PCS 不跨 RTT）的新候选**。这填补了"1.1/2.1 依赖跨 RTT 预测（TL-03 风险）"和"2.2 纯解析（无 DSP 实现）"之间的空档。但增益数据待 cite=81 精读验证。

### 4. 教训：harness 600s 硬上限 vs PROMPT 900s 设计不匹配

5 子 agent 全超时的根因：PROMPT-003 按 AGENTS.md "单子 agent ≤15 分钟（900s）"设计，但**harness 硬上限是 600s**。Salvage 路径（digest + 主对话补检索）成功挽回，但暴露**框架假设与运行时约束的脱节**。建议归 doc-steward：PROMPT 设计的子 agent 任务量须按 ≤600s 切分（而非 900s），或主对话分担部分检索。

---

## 对决策的影响

### 不新建 D###（本轮是扩候选池 + 负发现，非架构决策）

- **不修订 D001**：框架正常执行（N1 过 E 3/3 + C1 + 非 D 排除），A3 强化是候选重排非框架改
- **不修订 D003**：B1 仍永久排除；R006 未触碰相位联合建模
- **强化 S003 候选总览**：A3 从"井内首选"升级为"跨扫描共识首选"；新增 N1；2.2 可深化相干容量分支
- **F1/F2/F3 负发现**：归 doc-steward 沉淀为"FSO 方向探索可行解空间窄"的元教训（候选 D004 或 thesis-lessons 条目，待用户定夺是否升级为正式决策）

### 对后续 Groundwork 的影响

若用户倾向推进：
1. **A3 优先**（三轮共识 + 物理基础最强）：进 Groundwork §B 做"A3 三重障碍（多普勒时变/deep fade 相位跳变/单孔径）在 Paillier 主导损伤结论下的重评"
2. **N1 次优先**（新候选）：先精读 cite=81（PCS-FSO）验证 deep fade 下 gain 数据，再决定是否进 Groundwork
3. **2.2 保底**：纯解析，可并行推进相干容量分支
4. **未到 MVE**：D001 后续阶段链不变

### 待合并清单

- [ ] R006 结论并入 topic-index 进展线索（新增 R006 一行：大规模补盲 +1 net-new N1 + 强化 A3 + 负发现"可行解空间窄"）
- [ ] N1 关键论文 DOI（cite=81 PCS-FSO + cite=35 PCS-线宽）待查 Crossref 核实后并入 read-log（若进 Groundwork）
- [ ] **超时教训**（harness 600s vs PROMPT 900s）归 doc-steward 沉淀
- [ ] **F1/F2/F3 负发现**待用户定夺是否升级为 D004（"FSO 方向可行解空间窄"元教训）或 thesis-lessons 条目

### 不要做什么

- 不在本轮进 Groundwork/MVE（D001 后续阶段链，筛完≠MVE）
- 不改仿真代码/开题报告（范围外）
- 不强行凑到 15-20（D002 已废"凑"，宁少不烂）
- 不再无差别扩扫（边际收益递减，已扫透；若用户仍要扩，需换策略如"深挖 N1/A3 的细分"而非"再开新维度"）

---

## 置信度声明

- 所有候选判断为**摘要级 + abstract 初判**，TENTATIVE（与 S002/R005 同级）
- N1 的 cite=81 abstract 已读，gain 数据待精读正文
- α2/β3 的子 agent 未返回结构化 E 检验，主对话从 digest 的 abstract 做的初判——**对"砍掉"的命中置信度高（模式化失败），对 N1 的 E 3/3 判定需精读确认**
- 未做 Semantic Scholar abstract 交叉验证（主对话禁 WebSearch；N1 的 cite=81 abstract 来自检索 JSON，应视为待验证）——**进 Groundwork 前必须补**
