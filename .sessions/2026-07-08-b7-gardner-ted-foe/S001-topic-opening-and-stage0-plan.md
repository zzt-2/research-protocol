# [S001] 专题开题 + NDA-ML 混乱诊断 + 阶段 0 流程规划 + sim-preflight v1.3.0 补强

> 2026-07-08 | 阶段：B7 第二候选开题 + 流程规划前置 | 状态：专题开题 + 诊断 + skill 补强 + H001 交接完成

## 目标

NDA-ML 单载波候选卡 D-008~D-009（vs VV 持平陷阱 + 线宽选择 + 方法方向待定），用户决策同时跑 B7 分散风险。按用户要求"先规划流程防重蹈混乱"，诊断 NDA-ML 6 类混乱模式 → 补强 sim-preflight skill → 开 B7 新专题 + 写 H001 交接阶段 0 前置规约。

## 记录

### 起因：NDA-ML 卡住 + 用户要求先规划

用户在 step4a-mve-execution 专题经历 7/6-7/8 一周密集工作后反馈："并不是。而是在经过来回检查之后，感觉tmd这个在目前条件下，和vv没有差别？于是，不太知道咋办了。"

主线基于 D-008/D-009 最新事实回应：vs DA-ML 稳赢 +1.3~2.5dB 主结论不受影响，但 vs VV/BPS ablation 待 sandbox 重判（D-008 双 bug）+ 线宽 10kHz 疑似选错（D-009 Valjus 原文 0.1-1MHz）+ 方法方向 X/W/E/Z 待定。给三层选项（补强算法创新 / 重新定位贡献 / 转 B7）。

用户："那边现在乱的很，一会线宽不对一会没提升啥的，一直在折腾。所以，我打算同时跑第二个。但在那之前，需要先规划好整个流程，比如日志怎么记、怎么复用已有代码、怎么跑多种多样的验证、文件怎么组织、怎么防踩坑、出错了怎么自我验证等等。我觉得得先商量，防止和上次一样混乱以及出现低级错误。"

用户："你去改那个仿真相关的skill，然后给我新专题、交接文档，我去新对话做"

### NDA-ML 混乱诊断（派 Explore agent 深度诊断）

派 Explore agent 读 S002-S008 + decisions.md D001-D009，分类归纳 6 类混乱模式：

| 混乱类 | 具体事件 | 根因 |
|---|---|---|
| A. 参数反复 | 线宽 500kHz→10kHz→疑似 0.1-1MHz，全量重跑 3 轮 | D002 重定位只剥方法思想没清场景参数，参数散在 4 处抄写 |
| B. 算法 bug | D003 双 bug + D-008 双 bug（漏 ML 加权+升幂未归一）+ D-009 sandbox unwrap 伪 bug | 靠文字描述重建公式 / 两套独立实现开关不同步 |
| C. 验证失效 | consistency bit-exact 0.0000% PASS 但算法错（MVE 和 Formal 都漏同一加权）| 一致性锚点只查实现同步查不了算法对错 |
| D. 方向重定位 | B11 OFDM→单载波 / LMMSE 失败→VV/BPS / 方法方向 X/W 待定 | 架构性不等价没前置验清 |
| E. 文件混乱 | MVE 薄包装 + SPEC QPSK/NDA-ML 双套参数 + 两 results 目录 | 参数改后没同步清理下游引用 |
| F. 文献引用 | D-007 引 Valjus 位置没读原文数值 | 急于推进跳过原文核查 |

**做对的机制**（保留）：核查机制中性双向 + TL-20 偏离即查 + 用户附和性核查抓 bug + 用户拍 sandbox 先验证防白跑。

### sim-preflight v1.3.0 补强（6 条新规则）

基于 6 类混乱，补强 skill（commit 待提交）：

**新增 `rules/mve-validation.md`**（V1-V6 清单）：
- V1 公式来源逐项核对（禁靠文字重建，PDF→md 公式转 picture omitted 时标红不硬磕）
- V2 三方对照（消融 + 祖师爷，缺任一方归因不可信）
- V3 祖师爷持平警报（vs VV/Gardner 1986/BPS 持平即查数学同族性）
- V4 参数变更触发算法重审（参数选择和算法验证耦合）
- V5 子 agent 归因独立核查（只信原始数字不信归因）
- V6 FR-26 读原文数值（不只引位置）

**SKILL.md §1.6 新增 C6-C8**：公式核对 / 三方对照 / 祖师爷警报（跟 C1-C5 实验设计扎实性正交）

**interrupt.md 加第 10-12 条**：
- 10 vs 祖师爷方法持平警报
- 11 参数变更后未触发算法重审
- 12 MVE/sandbox 缺三方对照

**CHANGELOG v1.3.0**：记录 6 条触发证据（D-008 双 bug / consistency 假 PASS / 参数掩盖 bug / sandbox 缺三方 / 子 agent 归因错 / FR-26 引位置没读数值）

### B7 新专题开题

**slug**：`2026-07-08-b7-gardner-ted-foe`

**registry 登记**：depends_on 4 个（上游 + 切法地图 + 精读沉淀 + step4a-mve-execution NDA-ML 教训）。step4a-mve-execution 转 dormant（NDA-ML 卡 D-008~D-009 期间）。

**topic-index 13 条不变量**：
- 继承上游 9 条 + D005 务实路线 + FR-22 + FR-25 + 切法地图参照系 + profile 第 9 次防线 + TL-26 + TL-13 + TL-20 + 核查机制
- **B7 特殊 3 条**（INVARIANT 11/12/13）：
  - 11 Gardner TED 1986 数学同族性前置检查（祖师爷警报最严，B7 锚方法跟 40 年经典比）
  - 12 架构定性前置（前馈 vs 环路 TF，反馈环可能撞 D006）
  - 13 锚论文公式完整性前置核查（OFC 2026 poster 90 行很薄，靠文字重建风险高于 NDA-ML）

### B7 流程规划（阶段 0 前置规约，不写代码）

**阶段 0 六项规约**（防 6 类混乱）：
- 0.1 锚论文公式完整性核查（防 B 算法 bug + LMMSE 复现失败教训）
- 0.2 Gardner TED 数学同族性检查（防 C 验证失效 + D-008 祖师爷警报）
- 0.3 架构定性前馈 vs 环路（防 D 方向重定位 + D006）
- 0.4 公平对照框架设计（baseline PSA FOE 时域，不能照搬 NDA-ML DA ML pilot overhead）
- 0.5 参数真相源前置（防 A 参数反复 + sim-preflight v1.2.0）
- 0.6 文件组织规约（防 E 文件混乱 + D-007 教训 2 下游引用同步）

**对话拆分**：
- 对话 1 = 阶段 0 六项规约（本 H001）
- 对话 2 = sandbox 三方对照
- 对话 3 = MVE + consistency

## 决策引用

- **无新建 D###**（专题开题 + 流程规划 + skill 补强，非架构决策；B7 Go/Kill 决策留对话 1-3 用户拍板时立）
- 引用既有：D005（务实路线）/ D006（前馈不撞/环路 TF 联合建模则撞）/ D009（靠谱 checklist）/ step4a-mve-execution D-007~D-009（NDA-ML 教训）/ sim-preflight v1.3.0 C6-C8 + V1-V6 + interrupt 10-12

## 范围确认

- 本轮是否在 scope boundary 内：**是**（专题开题 + NDA-ML 诊断 + skill 补强 + H001 交接，都是 S001 启动动作）
- **守 3 步上限**：本轮实际 3 步（①NDA-ML 诊断 + skill 补强 ②B7 专题开题 4 文件 ③H001 + S001 交接）
- **守 profile 第 9 次"急于推进"防线**：本对话未跑任何 B7 代码，只开题+诊断+skill 补强+阶段 0 规约，sandbox/MVE 留新对话
- **守治理 Trigger 3**：B7 是上游 S031 已排出的候选（Conditional Go），开新专题不撞任何"明确不含"，scope 合规
- **step4a-mve-execution 转 dormant 合规**：NDA-ML 卡 D-008~D-009 期间转 dormant，等 B7 出结果或 NDA-ML 线宽/方向拍板后回来，不关闭（主结论 vs DA-ML 稳赢不受影响）

## 后续

### 已完成（本对话）

1. NDA-ML 6 类混乱诊断（派 Explore agent）
2. sim-preflight v1.3.0 补强（rules/mve-validation.md V1-V6 + SKILL §1.6 C6-C8 + interrupt 10-12 + CHANGELOG）
3. B7 新专题 2026-07-08-b7-gardner-ted-foe 开题（topic-index 13 不变量 + voice + registry + H001 + S001）
4. step4a-mve-execution 转 dormant（registry 更新）

### 下一步（新对话执行 H001）

新对话报到后按 H001 三步：
1. 报到 + 框架文件重读（含 sim-preflight v1.3.0 新增）
2. 阶段 0.1 + 0.2（公式完整性 + 数学同族性，派子 agent）
3. 阶段 0.3 + 0.4 + 0.5 + 0.6（架构/公平对照/参数/文件，主线定）

**最大风险**：0.2 数学同族性检查发现 B7 跟 Gardner TED 1986 同族 → 红线警报（NDA-ML D-008 陷阱重演），需重新定位贡献或放弃 B7。

### 待办（本对话收尾）

- commit（sim-preflight skill + B7 新专题 + registry 更新）
- 总结给用户
