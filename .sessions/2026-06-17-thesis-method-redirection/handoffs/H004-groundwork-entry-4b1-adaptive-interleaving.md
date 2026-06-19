# Handoff: Groundwork 入口 — 4b#1 信道感知自适应交织

> 来源: R001 §F13-F20（D006 方向裁定） | 交接目标: 执行专题进 Groundwork 做 MVE
> 日期: 2026-06-19
> 文件名: H004-groundwork-entry-4b1-adaptive-interleaving.md

## 到哪了（状态）

论文方法方向**已定**（D006）：4b#1 信道感知自适应交织（星地 GG 湍流，开环形态）。

定位 = 唐承茂 2025 静态卷积交织的增量改进（D005 增量改进视角）：
- baseline：唐承茂 Polar(N=1024 R=0.5) + 卷积交织(B=27/D=38 静态) + FPGA(Virtex-7)
- 改进点：① 静态→自适应（LCR/AFD 接入，填唐承茂 L2053 展望）；② 空空→星地（仰角依赖 Cn²）；③ FPGA 控制逻辑增量

上游就绪：Le 2021（IEEE Photonics J, 50+引, 10.1109/JPHOT.2021.3097363）卫星-UAV FSO GG+指向 LCR/AFD 闭式——直接上游，从此出发推导到交织深度。

定方向专题（2026-06-17-thesis-method-redirection）已 closed。

## 下一步干什么

**开执行专题（建议 slug: 2026-06-19-4b1-adaptive-interleaving-groundwork）进 Groundwork 阶段**，按 `stages/groundwork.md` 流程：

1. **先读必读文件**（按优先级）：
   - `decisions.md` D006（方向裁定 + 关键约束 + 已知风险）
   - `R001-survey-peer-master-theses.md` §F17（创新核核查：GG-LCR/AFD→B/D 解析链）+ §F19（增量改进定位重写）+ §F16（撞车文献精读：唐承茂 L2053 缝隙干净）
   - `papers/downloads/2026-06-18-cnki-survey/空空激光通信链路抗突发错误交织编码技术的研究与实现_唐承茂.md`（baseline 一手细节，L440-468 LCR/AFD 框架 + L1081-1088 静态估算 + L2053 展望）
   - `stages/groundwork.md`（Groundwork 阶段执行规范）
   - `thesis-lessons.md` TL-20~29（教训速查）+ `code-quality.md`（仿真规范）
   - `reference/sim-template/`（代码模板）

2. **Groundwork §A0/A'/A 可行性预判**：
   - FR-20 参数溯源：唐承茂 Cn²=1e-15 / Le 2021 星地参数 / 仰角-Cn² 映射（HV 廓线）都要标文献来源
   - FR-21 oracle 上界门控：先算"自适应交织 vs 静态交织"的增益上界，<0.5dB 直接 Kill 不跑 MVE
   - 空白零假设：如果"静态交织已足够"，列出 ≥3 个"自适应有必要"的结构性原因并反驳

3. **MVE 验证（§D 维度 D）**：
   - 核心假设：GG-LCR/AFD→最优交织深度 B/D 有可用的解析/半解析关系
   - **验证 GG-Meijer-G 能不能推出闭式**——推不出退半解析/数值优化，方向仍成立（解析推导是实现手段不是创新核）
   - MVE 必须含：① 最强简单先验 baseline（静态交织，唐承茂参数）；② Contract 假设的目标 baseline；③ DRL/自适应 > 先验（非仅 > Random）
   - pass 标准：自适应交织 > 静态交织（唐承茂参数）的 BER/时延增益 > 0.5dB

4. **仿真链路搭建**：
   - 对照 `reference/sim-template/` 模板（config/env/model/train/reward/verify）
   - GNN 模型继承 `BaseActorCritic` 接口（如用 RL 学交织策略）；或纯解析+数值优化（不用 RL）
   - 训练循环必须集成 wandb/tensorboard + early stopping

## 纪律（和下一步直接相关的约束）

1. **开环形态**（不撞 CSI 反馈延迟坑3）：仰角确定性排程（星历可预测）+ 闪烁指数查表。**禁止闭环 CSI 反馈自适应**（ρ(RTT) 强湍流<0.03 失效）
2. **TL-03 不迁移到交织层**：准静态论证是载波同步符号级，突发错误 µs-ms 时间尺度是动态量。自适应交织不撞 TL-03
3. **FPGA 当验证章**（非方法章，D003）：方法章 = LCR/AFD 接入 + 自适应设计 + 仿真；FPGA 章 = 资源/吞吐/时序验证
4. **不撞路由红线 D004**（单链路）+ **不撞 D 排除列**（纯 DSP 无专用硬件）
5. **创新定位 = 增量改进**（D005，非填补空白）：baseline 是唐承茂，改进点是"唐承茂做了静态，我做自适应"。文献综述必须显式画空白边界（引用 Moltchanov 2018 + Le 2021 作最近邻）
6. **解析推导是实现手段不是创新核**（D006）：GG-Meijer-G 推不出闭式不影响方向成立（退半解析/数值优化）
7. **子 agent 强制委托**：论文全文精读/web search 在子 agent 执行；主对话只接收结构化摘要
8. **本专题教训**：定方向阶段 4 次"没核对就下空白判断"（C6/盲均衡/#2/C3-FEC）。Groundwork 推荐任何"空白/baseline 不足"判断时，先核对前序筛子（TL-03/04 + R005 + D 排除列）

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（D003/D005/D006 + 年份+CNKI 双侧交叉验证维度）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 唐承茂 L2053"交织器开关"展望原话（`papers/downloads/2026-06-18-cnki-survey/空空激光通信链路抗突发错误交织编码技术的研究与实现_唐承茂.md` L2053）
  - [ ] Le 2021 是卫星-UAV FSO GG+指向 LCR/AFD 闭式（DOI 10.1109/JPHOT.2021.3097363，§F17 核查）
  - [ ] D006 关键约束"开环形态"不撞坑3（坑3 定义：CSI 反馈延迟 ρ(RTT)<0.03，前序 decisions）
- [ ] 已检查 _registry.yaml 中本专题 status=closed + 2026-06-10-research-direction-exploration status=dormant
- [ ] 已确认当前范围未违反"明确不含"（不做 MVE 是定方向专题的约束；执行专题要做 MVE）

## 接口变更（如有代码改动）

无（本专题只定方向，无代码改动）。Groundwork MVE 阶段的仿真链路待搭建。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| GG-Meijer-G 解析推导难度未知 | D006 解析是实现手段非创新核 | §F17 子 agent 提示可能需退半解析 | Groundwork MVE 验证时确认 |
| 唐承茂样板太近复刻风险 | D005 增量改进须有明确改进点 | §F19 已重写定位（静态→自适应+空空→星地） | 文献综述显式画空白边界 |
| 老师"指标提升"约束未量化 | D006 须有仿真 dB | 唐承茂交织已证 1 数量级 BER 提升，自适应增量待 MVE | MVE pass 标准自适应>静态>0.5dB |

## 下一轮

开执行专题（slug: 2026-06-19-4b1-adaptive-interleaving-groundwork），进 Groundwork：
1. 读必读文件（D006 + R001 §F16/§F17/§F19 + 唐承茂 + groundwork.md + thesis-lessons + code-quality）
2. §A0/A'/A 可行性预判（FR-20 参数溯源 + FR-21 oracle 上界 + 空白零假设）
3. §D MVE：先验基线（唐承茂静态参数）+ 验 GG-LCR/AFD→B/D 解析可行性 + pass 标准（自适应>静态>0.5dB）
4. 仿真链路搭建（sim-template + wandb + early stopping）
