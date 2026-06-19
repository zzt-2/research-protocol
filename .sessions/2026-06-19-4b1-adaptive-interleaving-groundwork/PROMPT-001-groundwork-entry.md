# PROMPT-001: 4b#1 信道感知自适应交织 — Groundwork 入口

> 新对话粘贴此提示词启动。本专题 = 执行专题（Groundwork 阶段），接续定方向专题 2026-06-17-thesis-method-redirection（已 closed）。
> 日期: 2026-06-19

---

## 怎么开始这个对话

你是 ZCode，正在帮用户做硕士论文方法方向的执行落地。上一个专题（定方向）刚 closed，方向已裁定为 **4b#1 信道感知自适应交织**。现在要进 Groundwork 阶段做 MVE 可行性验证 + 仿真链路搭建。

**第一步必须做的事（按优先级）**：

1. **报到**：调 session-governance skill（Trigger 1 Session Start），确认本专题范围边界
2. **读 H004 handoff**：`.sessions/2026-06-17-thesis-method-redirection/handoffs/H004-groundwork-entry-4b1-adaptive-interleaving.md` —— 这是上一个专题的收尾交接，含方向定位 + 关键约束 + 已知风险 + 下一步任务
3. **完成 H004 接收方验证**（H004 末尾的 checklist，验证 3 条关键事实声称）
4. **读必读文件**（见下）

## 必读文件（按优先级）

### 方向定位（必须读懂）
1. `.sessions/2026-06-17-thesis-method-redirection/decisions.md` 的 **D006**（方向裁定 + 关键约束 + 已知风险 + 排除方向）
2. `.sessions/2026-06-17-thesis-method-redirection/decisions.md` 的 **D005**（创新定位 = 增量改进，非填补空白）+ **D003**（策略 + FPGA 当验证章）

### 核心证据链（理解为什么定 4b#1）
3. `.sessions/2026-06-17-thesis-method-redirection/R001-survey-peer-master-theses.md` **§F16**（4b#1 撞车文献精读：唐承茂 L2053 缝隙干净，4 篇撞车全周边撞）
4. R001 **§F17**（创新核核查：GG-LCR/AFD→最优交织深度 B/D 解析推导无人做过，Moltchanov 2018 RF/Markov 最近邻，Le 2021 FSO LCR/AFD 上游）
5. R001 **§F19**（增量改进视角重评：4b#1 定位重写为"唐承茂静态交织的增量改进"）
6. R001 **§F20**（A3 非自适应核查排除，6 候选无一干净）

### baseline 一手细节（Groundwork 仿真起点）
7. `papers/downloads/2026-06-18-cnki-survey/空空激光通信链路抗突发错误交织编码技术的研究与实现_唐承茂.md`
   - **L440-468**：LCR/AFD/Markov 双状态框架（Gilbert 1960 + Rappaport）
   - **L1081-1088**：交织参数静态估算（Lburst≈800 反推 B=27）
   - **L2053**：自留"交织器开关"展望原话
   - **L1247**：卷积交织参数 B=27/D=38
   - **5.1 节**：FPGA RTL 架构（Virtex-7，编码 6.83Mbps / 译码 3.86Mbps）

### Groundwork 执行规范
8. `stages/groundwork.md`（Groundwork 阶段每步操作 + 检查点 + 通过条件）—— **[MUST] 转阶段必须先读**
9. `thesis-lessons.md`（教训速查 TL-20~29）+ `code-quality.md`（仿真规范）—— **[MUST] 仿真/训练前必读**
10. `reference/sim-template/`（config/env/model/train/reward/verify 代码模板）—— **[MUST] 搭仿真器前必读**

### 上游文献（解析推导起点）
11. Le 2021（IEEE Photonics J, DOI 10.1109/JPHOT.2021.3097363）：卫星-UAV FSO GG+指向误差 LCR/AFD 闭式 —— 用 tools/search 或 web 查（在子 agent 内执行）

## 本轮目标

**进 Groundwork §A0/A'/A 可行性预判 + §D MVE 验证 GG-LCR/AFD→B/D 解析可行性**。

具体任务（按 H004 下一轮）：
1. §A0/A'/A：FR-20 参数溯源（Cn²/仰角/Le 2021 参数标文献来源）+ FR-21 oracle 上界门控（先算"自适应 vs 静态"增益上界，<0.5dB Kill）+ 空白零假设（列 ≥3 个"自适应有必要"的结构性原因）
2. §D MVE：先验基线（唐承茂静态参数）+ 验 GG-Meijer-G 能否推出 B/D 闭式（推不出退半解析/数值优化，方向仍成立）+ pass 标准（自适应>静态>0.5dB BER/时延增益）
3. 仿真链路搭建（sim-template + wandb + early stopping）

## 关键约束（H004 纪律段，必须遵守）

1. **开环形态**（不撞 CSI 反馈延迟坑3）：仰角确定性排程 + 闪烁指数查表。**禁止闭环 CSI 反馈**（ρ(RTT) 强湍流<0.03 失效）
2. **TL-03 不迁移到交织层**（准静态是载波同步符号级，突发 µs-ms 是动态量）
3. **FPGA 当验证章**（非方法章）：方法章 = LCR/AFD 接入 + 自适应设计 + 仿真
4. **创新定位 = 增量改进**：baseline 是唐承茂，改进点是"静态→自适应+空空→星地"。**不要重新陷入"找空白"**（上一个专题的教训）
5. **解析推导是实现手段不是创新核**：GG-Meijer-G 推不出闭式不影响方向成立
6. **子 agent 强制委托**：论文精读/web search 在子 agent；主对话只接收结构化摘要
7. **主对话严禁 WebSearch/webReader**（用 tools/search 或子 agent）

## 上一个专题的教训（避免重蹈）

定方向专题 4 次"没核对就下空白判断"（C6/盲均衡/#2/C3-FEC）。**Groundwork 推荐任何"空白/baseline 不足"判断时，先核对前序筛子**（TL-03/04 + R005 + D 排除列）。不要凭"物理缝 PASS"就推方法形态——C3 就是只验物理缝没验方法形态导致判死。

## 开场怎么说

读完 H004 + 必读文件后，报到：
1. Session Start Confirmation（topic/范围/不变量/冲突/voice）
2. H004 接收方验证结果（3 条关键事实声称的 PASS/FAIL）
3. 本轮 Groundwork 计划（§A0/A'/A + §D MVE 的拆解）
4. 第一步具体做什么（建议从 FR-21 oracle 上界门控开始——<0.5dB 直接 Kill 不跑 MVE，省时间）

---

## 附：本专题基本信息

- **slug**: 2026-06-19-4b1-adaptive-interleaving-groundwork
- **title**: 4b#1 信道感知自适应交织 Groundwork 执行
- **depends_on**: 2026-06-17-thesis-method-redirection（已 closed，方向已定）
- **范围**: 只做 Groundwork 阶段（§A0/A'/A 可行性 + §D MVE + 仿真链路）。不做 Contract / Execute
- **明确不含**: 不重新定方向（已 D006 裁定）；不做完整训练（MVE 只验可行性）
