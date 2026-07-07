# Topic Index: B7 Gardner TED 复用 FOE 第二候选

> slug: 2026-07-08-b7-gardner-ted-foe
> status: active | created 2026-07-08 | last_updated: 2026-07-08（S001 专题开题 + 流程规划前置——NDA-ML 卡 D-008~D-009 期间，用户决策同时跑第二候选 B7 分散风险）

## 专题定位（一句话）

B7-Q1（Gardner TED 复用 FOE）第二候选 MVE 执行。与 NDA-ML 单载波候选（step4a-mve-execution 专题）并行，NDA-ML 卡 D-008 双 bug + D-009 线宽/vs VV 持平陷阱期间推进。**流程规划前置**（阶段 0 不写代码先定规约）防重蹈 NDA-ML 6 类混乱。

## 原始目标（冻结，不可修改）

对 B7-Q1 走 Step 4a 维度 D MVE，守 FR-21/TL-20/FR-18/FR-12 + D005 务实路线 + D006 红线 + **sim-preflight v1.3.0 新增 C6-C8**（公式核对/三方对照/祖师爷警报）。

**冻结边界**：
- 只做 B7-Q1（Gardner TED 复用 FOE 星地 COSC 迁移），不回头救 6 次 Kill
- 不跳框架（FR-22，当前在 Step 4a 维度 D）
- 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- 不改框架文件（守"先测不改协议"）

## 范围边界

### 原始目标（冻结）
对 B7-Q1 走 Step 4a 维度 D MVE。

### 当前范围
- **阶段 0 前置规约**（不写代码，先定 6 项规约，防 NDA-ML 6 类混乱）：
  0.1 锚论文公式完整性核查（OFC 2026 poster 全文 + 页码 + 公式编号 + 是否完整可实现）
  0.2 Gardner TED 数学同族性检查（跟 1986 原版 + VV + BPS 的数学关系）
  0.3 架构定性（前馈 vs 环路 TF，环路则撞 D006 必须前置决策）
  0.4 公平对照框架设计（B7 baseline PSA FOE 时域，fair gain 怎么定义，工作点 BER 2e-2 还是 HD-FEC）
  0.5 参数真相源前置（Doppler range / OSNR / LEO Doppler rate 一开始进 params.py 单字段）
  0.6 文件组织规约（`explore/b7-gardner-ted-foe/` 目录结构 + 命名规则）
- **阶段 1 sandbox 三方对照**（Gardner TED 改进版 / 1986 原版祖师爷 / PSA FOE baseline）
- **阶段 2 TL-20 理论预期表**（仿 N1-MVE-SPEC.md §2）
- **阶段 3 MVE + consistency**（守 sim-preflight v1.3.0 C6-C8 + V1-V6）

### 明确不含
- ❌ 不回头救 6 次 Kill
- ❌ 不判 NDA-ML 那边的线宽/方向决策（那是 step4a-mve-execution 专题的事，本专题只做 B7）
- ❌ 不改框架文件
- ❌ 不跳框架（FR-22，当前在 Step 4a 维度 D）
- ❌ 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- ❌ 不污染 common（explore 阶段探针不直接进 experiments，MVE 通过才转正）

### 范围变更记录
- 无（专题首 session）

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 降级为参考不当 Kill 门
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具
5. **切法地图是参照系不是答案**：B7 是稀池 1 细分独占赛道（OFC 2026 会议样本 + 75%"既有方法失效"叙事），引用模式不搬"切法地图说这个好"
6. **profile 第 9 次"急于推进"防线激活**：B7 流程规划阶段主线极易"阶段 0 太繁琐先跑起来再说"。**防线：阶段 0 六项规约必须全做完才进 sandbox，禁跳阶段 0 直接写代码**（NDA-ML 最大混乱就是阶段 0 没做）
7. **TL-26 参数溯源强制**：B7 每个关键参数（Doppler range / OSNR / LEO Doppler rate / 符号率 / 线宽）必须标文献来源（B7 OFC 2026 / Paillier / sat.1553 / Fernandes），禁拍参数。**且必须读原文数值不只引位置**（D-009 教训 5，FR-26 强化）
8. **TL-13 共用同一信道实现**：B7 必须从 `common/_channel.py` 导入，禁自建信道
9. **TL-20 先建理论预期**：MVE 跑之前必须写明理论预期表，仿 N1-MVE-SPEC.md §2
10. **核查机制中性双向**：子 agent 产出 + 主线独立 grep 核查，**子 agent 归因必须主线独立重算验证**（D-009 教训 6，只信原始数字不信归因）
11. **【B7 特殊·INVARIANT】Gardner TED 1986 数学同族性前置检查**：Gardner TED 是 40 年前祖师爷方法（比 VV 1983 还老），B7 锚方法（OFC 2026 Gardner TED 复用 FOE）跟它比，**如果数学同族就是 NDA-ML D-008 陷阱重演**（vs VV 持平被当合理接受）。**必须在阶段 0.2 做深度数学同族性检查**，并在 sandbox 阶段做三方对照（改进版/1986 原版/PSA FOE）验证非同族
12. **【B7 特殊·INVARIANT】架构定性前置（前馈 vs 环路 TF）**：B7 锚方法是反馈环（TED→loop filter→NCO），**如果我们的实现也走反馈环，环路 TF 联合建模则撞 D006**。必须在阶段 0.3 定死：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策）。**禁边跑边定架构**（NDA-ML D-002 B11 OFDM→单载波重定位教训）
13. **【B7 特殊·INVARIANT】锚论文公式完整性前置核查**：B7 OFC 2026 poster 只有 90 行（比 B11 PTL 2025 的 226 行薄很多），**靠文字描述重建公式风险高于 NDA-ML**（LMMSE #15 复现失败教训：PDF→md 把公式转 picture omitted）。必须在阶段 0.1 核查所有公式完整可实现，**公式不全直接标红不硬磕**，切降级方案（定性引用或换 baseline）

## 其他结论（普通技术决策）

### B7 特殊风险（vs NDA-ML 的差异点，决定流程重点）

| 风险 | B7 情况 | NDA-ML 对照 | 流程对策 |
|---|---|---|---|
| 锚论文薄 | OFC 2026 poster 90 行 | B11 PTL 2025 226 行 | 阶段 0.1 公式完整性核查最严 |
| 祖师爷警报 | Gardner TED 1986（40 年经典）| VV 1983（NDA-ML 已踩陷阱）| 阶段 0.2 数学同族性检查 + sandbox 三方对照 |
| 架构定性 | 反馈环（TED→loop filter→NCO）| 前馈闭式（不撞 D006）| 阶段 0.3 前馈化 vs 环路决策 |
| 公平对照 | baseline PSA FOE 时域 | DA ML pilot overhead | 阶段 0.4 fair gain 框架重新设计 |

### NDA-ML 6 类混乱 + B7 防御措施（S001 确立）

| 混乱类 | NDA-ML 教训 | B7 防御措施 |
|---|---|---|
| A. 参数反复 | 线宽 500kHz→10kHz→疑似 0.1-1MHz，全量重跑 3 轮 | 阶段 0.5 参数真相源前置 + sim-preflight v1.2.0 param-source.md |
| B. 算法 bug | D003 双 bug + D-008 双 bug（漏 ML 加权+升幂未归一）| 阶段 0.1 公式完整性核查 + V1 公式逐项核对（v1.3.0）|
| C. 验证失效 | consistency PASS 但算法错（两套都漏同一 bug）| V2 三方对照 + V3 祖师爷警报（v1.3.0 C7-C8）|
| D. 方向重定位 | B11 OFDM→单载波 / LMMSE 失败→VV/BPS | 阶段 0.3 架构定性前置（前馈 vs 环路）|
| E. 文件混乱 | MVE 薄包装 + 双套参数共存 + 两 results 目录 | 阶段 0.6 文件组织规约 + 下游引用同步清单 |
| F. 文献引用 | D-007 引 Valjus 位置没读原文数值 | V6 FR-26 读原文数值（v1.3.0）|

## 已确认决策

- 无新建 D###（首 session，专题开题 + 流程规划，非架构决策）

## 悬而未决

1. **B7 锚论文 OFC 2026 poster 是否已落盘**：需阶段 0.1 核查（`papers/` 下找 ofc.2026.w2a.62 或 DOI 10.1364/ofc.2026.w2a.62），未落盘则需先下载
2. **Gardner TED 1986 数学同族性结论**：阶段 0.2 子 agent 深度检查后定（跟 B7 锚方法的关系）
3. **架构定性结论**：阶段 0.3 定死前馈化 vs 环路（影响是否撞 D006）
4. **公平对照框架**：阶段 0.4 设计（fair gain @ BER 2e-2 还是 HD-FEC，PSA FOE 怎么公平对照）

## 当前位置

**🟢 S001 专题开题 + 流程规划前置（2026-07-08）**：NDA-ML 单载波候选卡 D-008 双 bug + D-009 线宽/vs VV 持平陷阱，用户决策同时跑 B7 分散风险。本专题承接上游 S031 B7-Q1 Conditional Go + step4a-mve-execution NDA-ML 教训。**流程规划前置**：阶段 0 六项规约（公式完整性/数学同族性/架构定性/公平对照框架/参数真相源/文件组织）不写代码先定，防重蹈 NDA-ML 6 类混乱。sim-preflight v1.3.0 已补 C6-C8 + interrupt 10-12 条。下一步=新对话执行 H001（阶段 0 六项规约）。

## 进展线索

- **S001** 专题开题 + 流程规划前置 + H001 交接（2026-07-08，本对话产出）
