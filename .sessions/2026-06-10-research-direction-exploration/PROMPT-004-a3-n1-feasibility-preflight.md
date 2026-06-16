# PROMPT-004: A3 / N1 物理可行性预检

> 新对话粘贴此文件全文启动。承接 S004（讨论收敛到"先验能做出来"）。
> 创建: 2026-06-16 续 3 | 专题: research-direction-exploration | 前置: S004 / D003 / D004 / R006

---

## 你是 ZCode，在 research-protocol 项目工作

工作目录: `D:\code\study\research-protocol`（win32，命令用 `wsl -e bash -lc "cd /mnt/d/code/study/research-protocol && ..."`，torch venv 在 `~/.venvs/torch/bin/python`）。

**本对话先调 session-governance skill**（续接 = Trigger 1，无 handoff 接收），再开工。

## 本轮目标（一句话）

**验 A3 和 N1 各自的物理可行性——会不会像 B1 那样倒在物理死锁上？** 派 2 子 agent 并行，带 D003 教训（不只看 E 三检验，看物理前提 + 主导损伤针对性）。验完才有资格谈"几个够、怎么互锁成三章"。

## 为什么做这个（背景，给新对话快速进入）

R006 大规模补盲扫描（三轮扫描最后一轮，15 JSON ~180 hits）证明**枚举式找方向已到边际**——净增仅 N1，强化 A3，干净候选 A3+2.2+N1=3。用户多轮讨论后（见 S004）收敛到一个判断：**"3 个互锁刚好够"这个方案依赖 A3/N1 能做出来，但两者的物理可行性到现在一个都没验过**——A3 的"三重障碍"在 Paillier 主导损伤结论下没重评，N1 的 PCS gain 数据没精读。B1 就是倒在这道关上的（D003 物理死锁）。所以**找更多方向不解决"做不出来"，先验"哪个能做出来"才是正确下一步**（D001 后续阶段链的 Groundwork §B 空白零假设前置）。

## 用户的核心关切（驱动本轮）

- 用户原话（2026-06-16 续 3）："'3 个互锁刚好够'很依赖于能做出来？" → **不能在未验证物理可行性前承诺"3 个够"**
- 若 3 个里只有 1 个能做出来，"刚好够"就变"根本不够"
- 用户已拦住两条歧路：❌ 排列组合全切法发散（=第五轮扫描翻车，"一大堆出不来"）❌ 派子 agent 无约束发散（漏教训）
- **本轮只验物理可行性，不找新方向，不锁叙事**

## 必读（严格按序，不可跳）

1. **`thesis-lessons.md`** 速查表 + **TL-03/04/05/22/26（建议）** —— 物理可行性检验的依据。TL-03（相干时间禁全局自适应）/ TL-04（湍流自适应载波同步物理无意义）/ TL-22（震撼结果先查物理前提）/ TL-26（E三检验全过≠值得做，主导损伤定位）
2. **`decisions.md` D001 + D002 + D003 + D004** —— D001 评判框架+后续阶段链（Groundwork §B 是当前步）；D003 是 B1 物理可行性预检 FAIL 的**方法论范本**（物理死锁机制 + 否决了什么 + 可复用部分 + 量级对比），**本轮对 A3/N1 做同类预检**；D004 是扫描边际+换角度（含路由红线）
3. **`S004-pivot-from-divergence-to-feasibility-preflight.md`** —— 完整讨论轨迹（4 轮反转），本轮的决策依据。**尤其"关键认知沉淀"段**：找更多方向不解决"做不出来"；互锁是结果非前提；保底骨架=2.2+不依赖未验证物理的方法
4. **`R006-large-scale-blindspot-scan.md`** —— A3/N1 的来源 + 负发现族（DL/AMC/多孔径/新分布BER/光纤CPE/光学硬件/RF迁移，新候选撞这些族直接砍）。**N1 的 cite=81 待验 gain 标注**
5. **`S003-b1-feasibility-precheck-fail-funnel-merge.md`** —— B1 预检 FAIL 的执行记录（PROMPT-001 的 Phase A/B/C 方法），**本轮照这个方法做 A3/N1**
6. **`papers/_read_notes/10.1002_sat.1553.md`**（Valjus 2025 综述）+ **`papers/arxiv/1911.11851/content.md`**（Paillier 2020）—— Paillier 主导损伤结论（残余幅度闪烁+激光相位噪声主导，湍流活塞相位 negligible）是本轮物理可行性的**判据基础**

## 两个预检对象的具体待验点（核心）

### 预检对象 1：A3（导频抗 deep fade，幅度鲁棒）

**A3 是什么**（来自 R002/S003）：在 intradyne 相干接收的载波恢复模块内，用频域导频音/pilot 符号在 deep fade 期间维持相位跟踪 + 抗幅度闪烁。关键论文 Yang 2026（频域导频音 FOE+CPE+RSOP，DOI 10.1109/LCOMM.2026.3651445）+ Zhou 2026（DSP 帧导频振动检测，DOI 10.1364/ol.596189）。

**待验的具体物理问题**（S003/R004 指出的"三重障碍"，本轮在 Paillier 主导损伤结论下重评）：
1. **多普勒时变**：A3 的导频跟踪能否在 LEO 大多普勒残频（Paillier 30-300MHz）下工作？导频间隔/功率够不够？
2. **deep fade 相位跳变**：deep fade 期间的相位跳变——**这是不是 Paillier 说的主导损伤（幅度闪烁）的直接表现？** 如果是，A3 针对的就是主导损伤（物理基础强）；如果相位跳变其实是湍流活塞相位（negligible），那 A3 针对的就是非主导损伤（物理基础弱，重蹈 B1）
3. **单孔径无分集**：A3 在单孔径下（D 排除多孔径硬件），导频抗 fade 的增益够不够？还是必须靠多孔径分集？

**预检要回答**：
- A3 针对的损伤（deep fade 幅度闪烁）是不是 Paillier 定位的主导损伤？→ 决定物理基础
- 三重障碍中，哪个是真障碍（物理上挡死），哪个是工程量（可克服）？
- A3 有没有 B1 那种"物理死锁"（两个物理要求矛盾，无可工作参数区间）？**重点查这个**

### 预检对象 2：N1（静态 PCS 适配湍流 SNR 分布）

**N1 是什么**（来自 R006）：概率星座整形（PCS，Maxwell-Boltzmann 分布匹配）按湍流 SNR 分布**离线优化**星座点概率分布，在 deep fade 统计上获 shaping gain。关键：离线 PCS 不跨 RTT → 避开 TL-03 反馈陷阱。关键论文"Adaptive probabilistic shaped modulation for high-capacity FSO links"（2020, cite=81，**abstract 已读，gain 数据待精读**）+ "End-to-end optimization of constellation shaping for Wiener phase noise"（2023, cite=35）。

**待验的具体物理问题**：
1. **gain 数据**（R006 挂着的）：cite=81 的 PCS-FSO 在强湍流（GG 分布）deep fade 下的 shaping gain 到底多少 dB？**必须精读正文拿数字**，不能停在 abstract
2. **gain 稀释**：deep fade 的 SNR 方差很大，PCS 按"平均 SNR 分布"优化的分布，在 deep fade 瞬态（SNR 远低于平均）是否还有效？gain 会不会被方差稀释到不值得做？
3. **与激光相位噪声 CPE 的耦合**：PCS（高阶调制）需要线宽容忍 CPE，激光相位噪声是 Paillier 说的主导损伤之一——PCS + 线宽容忍 CPE 在湍流下能联合工作吗？有没有参数冲突（类似 B1 带宽死锁）？
4. **TL-03 边界确认**：N1 的 PCS 是"离线按长期 SNR 统计设计"（不跨 RTT，TL-03 安全）还是隐含"每帧按瞬时 SNR 自适应"（跨 RTT，TL-03 砍）？**必须厘清这条边界**，否则 N1 可能偷偷踩 TL-03

**预检要回答**：
- N1 的 gain 在 deep fade 下是否值得做（≥1dB？还是被稀释到 <0.5dB）？
- N1 有没有物理死锁（PCS + CPE + 湍流的参数冲突）？
- N1 是真"离线静态"还是隐含跨 RTT 自适应？

## 执行方案（2 子 agent 并行，每个 ≤600s）

**⚠️ harness 硬上限是 600s（10分钟），不是 AGENTS.md 写的 900s（15分钟）。R006 的 5 agent 全部因按 900s 设计而撞 600s 超时。本轮任务量必须按 ≤600s 切**。

| Agent | 任务 | 时间预算 | 预期产出 |
|---|---|---|---|
| **Agent-A3** | A3 物理可行性预检：三重障碍在 Paillier 主导损伤结论下重评 + 查物理死锁 | ≤600s | A3 PASS/FAIL/存疑 + 量级对比 + 死锁检查 + 可复用部分 |
| **Agent-N1** | N1 物理可行性预检：精读 cite=81 拿 gain 数据 + gain 稀释数值核对 + PCS×CPE×湍流参数冲突检查 + TL-03 边界确认 | ≤600s | N1 PASS/FAIL/存疑 + gain 数字 + 死锁检查 + TL-03 边界判定 |

**子 agent 调用规范**（AGENTS.md）：
- 用 `tools/search`（脚本）做检索，结果存 `search-archive/2026-06-16/`（注意别覆盖现有 22 份 JSON，slug 加 `-preflight` 后缀）
- 论文功能/贡献断言 → Semantic Scholar API（bash curl）交叉验证 abstract，不支持的标"AI 推断未验证"
- **cite=81 精读**：Agent-N1 必须先确认论文是否已下载（查 `papers/` 下有无对应 DOI/arxiv 目录），未下载则用 `tools/download` 下，用 `tools/convert` 转 md，再精读拿 gain 数字
- 实在需 web → 子 agent 内部用 WebSearch，**返回 ≤500 词摘要**，主对话不接收 HTML
- **主对话严禁 WebSearch/webReader**（AGENTS.md 强制）

**若子 agent 超 600s**（R006 教训）：转 salvage——检查子 agent 死前写了什么 JSON/笔记，主对话用 digest 脚本提取 + 补检索。但**本轮任务量已按 ≤600s 切（每 agent 只验一个候选），超时概率应低于 R006**。

## 预检方法（照 S003/PROMPT-001 的 Phase A/B/C，D003 的格式）

**Phase A**：从已读论文（Paillier 2020 / Valjus 2025 / R004 的 5 篇精读）提取 A3/N1 相关参数（主导损伤量级、deep fade 统计、PCS gain、CPE 线宽容限）
**Phase B**：派子 agent 查证缺失参数（A3 的 deep fade 相位跳变量级 / N1 的 cite=81 gain 正文数据）
**Phase C**：量级比较 + 物理死锁检查 + 主导损伤针对性判定 → PASS/FAIL/存疑

**输出格式（照 D003）**：
- 核心结论（PASS/FAIL/存疑）
- 若 FAIL：物理死锁机制（不只"没意义"）+ 否决了什么 + 可复用部分
- 若 PASS：物理基础确认 + 三重障碍/gain稀释的真实严重度 + 进 Groundwork 的前置条件
- 若存疑：缺什么数据才能判 + 建议补检索

## PASS/FAIL 映射到下一步（本轮产出后主对话判断）

| A3 | N1 | 下一步 |
|---|---|---|
| PASS | PASS | 互锁三章成立（A3方法 + 2.2解析 + N1扩展）→ 进 A3 的 Groundwork 剩余 |
| PASS | FAIL | 保底骨架（2.2 + A3）→ 进 A3 Groundwork，N1 可复用部分归档 |
| FAIL | PASS | 保底骨架（2.2 + N1）→ 进 N1 Groundwork |
| FAIL | FAIL | **必须真找新方向**，但概率低（都针对主导损伤）；此时才回 D004 切法 ⑦(AO残差不确定性)/⑧(反向问题)深挖，**不是回扫描** |
| 任一存疑 | — | 补检索后再判，不强行定 |

## 筛子与红线（不可违反）

- **E≥2 不降**（D001）
- **路由红线**（D004）：A3/N1 都是单链路物理层，不碰多节点/资源调度。预检中若发现某候选隐含多节点，立即标红线
- **TL-03/04**：全局自适应/反馈类禁。N1 必须确认是离线静态非跨 RTT
- **D003 主导损伤定位**：A3/N1 针对的损伤必须是 Paillier 主导损伤（幅度闪烁/激光相位噪声），针对 negligible 湍流相位的直接 FAIL
- **D 排除列 5 类**：需实测/专用硬件/超算/实时物理闭环/数月实测
- **TL-22**：任何"震撼结论"（如 N1 gain 极高 / A3 完美无障碍）先查物理前提

## 不要做什么（Dead Ends）

- ❌ 找第 4/5 方向（不解决"做不出来"，用户已拦）
- ❌ 排列组合全切法发散（第五轮扫描翻车风险）
- ❌ 锁"互锁三章"叙事（依赖未验证前提，本轮就是来验的）
- ❌ 在未过预检前进 Groundwork/MVE（D001 后续阶段链）
- ❌ 改仿真代码/开题报告（范围外）
- ❌ 主对话 WebSearch（AGENTS.md 强制）
- ❌ 子 agent 按 900s 设计任务（harness 实际 600s，R006 教训）

## 单对话步骤上限

2 子 agent 派遣 + 结果汇总判断 = 2 步。若某 agent 超时需 salvage，可能到 3 步，写 handoff 分对话。**目标本轮收尾产出 A3/N1 各自的 PASS/FAIL/存疑 + 下一步映射**。

## 治理要求

- 改 `.sessions/2026-06-10-research-direction-exploration/` 下任何文件前，重读 session-governance 对应 Trigger
- 本轮产出新 S###（如 S005-a3-n1-feasibility-preflight）记录预检结果
- **若某候选 FAIL → 新建 D###**（参照 D003 格式：物理死锁机制 + 否决了什么 + 可复用部分 + 对其他候选影响）。若两都 PASS 不新建 D###（只是确认，非决策）
- **不修订 D001/D004**（框架正常执行）
- handoff（如本轮写）含 receiver verification checklist

## 接收方验证清单（启动时执行）

- [ ] 读 thesis-lessons TL-03/04/05/22（+TL-26 建议）
- [ ] 读 D001 + D002 + D003 + D004（D003 是预检方法论范本，D004 是扫描边际+路由红线）
- [ ] 读 S004（完整讨论轨迹，尤其"关键认知沉淀"——为什么先验而非发散）
- [ ] 读 R006（A3/N1 来源 + 负发现族 + N1 cite=81 待验标注）
- [ ] 读 S003（B1 预检 FAIL 的 Phase A/B/C 执行记录，本轮照做）
- [ ] 读 Paillier 2020（arXiv:1911.11851）主导损伤结论 + Valjus 2025 综述笔记
- [ ] 验证 S004 ≥3 条事实（4 轮反转轨迹 / 互锁依赖未验证 / 保底骨架思想）
- [ ] 确认 _registry.yaml research-direction-exploration status=active
- [ ] 确认 harness 600s 约束（查 R006 超时记录），任务按 ≤600s 切

---

## 一句话背景（给新对话快速进入）

硕士论文做"星地湍流信道激光通信处理"。三轮扫描（R002/R005/R006）证明枚举式找方向到边际，干净候选 A3（导频抗 deep fade，跨扫描共识首选）+ 2.2（自适应频谱效率闭合解，解析保底）+ N1（静态 PCS 适配湍流 SNR 分布，R006 净增）= 3 个。但"3 个互锁刚好够"依赖 A3/N1 能做出来——**两者物理可行性一个都没验过**（A3 三重障碍未在 Paillier 主导损伤结论下重评，N1 的 PCS gain 数据没精读），B1 就是倒在这道关的（D003 物理死锁）。本轮派 2 子 agent 并行验 A3/N1 物理可行性（照 D003 方法），验完才有资格谈"几个够、怎么互锁"。**用户不替细分技术拍板，靠 agent 用物理量级和文献证据判断。已拦住两条歧路：不发散找新方向，不锁未验证叙事。**
