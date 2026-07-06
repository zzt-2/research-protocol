# [S001] 专题开题 + 仿真基建盘点 + 组织方案定稿

> 2026-07-06 | Step 4a 排优先级 + Go/Kill（上游专题续接）→ Step 4a 维度 D MVE 执行专题开题 | 状态：专题开题 + 基建盘点 + 组织方案 + H001 交接完成

## 目标

承接上游专题 2026-06-20-problem-driven-redirection S031（35 Q# 排优先级 + 前 5 名 Go/Kill 评估），按用户"去新对话试 + 哪些并行复用 + 想想之后咋组织"的诉求，开新专题 Step 4a 维度 D MVE 执行，盘点旧仿真基建，设计组织方案，写 H001 交接给新对话。

## 记录

### 起因：用户诉求演变

用户在切法地图专题定稿后（2026-07-05）说"水一篇会议就行"（voice.md），上游 S031 据此排了 35 Q# 优先级 + 对前 5 名判 Go/Kill（主线建议 B11/B3/B7 Conditional Go）。用户对前 5 名评估的反馈："我不知道。我想的是，这些各种条件，到时候多想想哪些能改？比如调制方式啥的...别人咋水我们也咋水（不是说严格对照，是体会他们的思想）...有点东西就可以试试。不过别忘了之前踩过的坑，尤其是仿真方面"。

第二轮主线回应：3 个 Go 候选的可改旋钮（B11 调制格式/信道/联合维度/pilot 开销 + B3 支路数/联合维度/信道 + B7 Doppler 范围/TED 算法/湍流鲁棒性）+ 别人咋水的思想体会（切法地图 §D 浓缩）+ 仿真坑防线 7 条（TL-22/26/27/20/23 + FR-18/12）+ 主线最稳试法（首选 B11-Q1 + 星地湍流迁移 + DVB-S2 调制，先算 oracle 上界再决定跑不跑 MVE）。

用户："我打算去新对话试？以及，它们哪些可以并行、复用？"——主线回应复用矩阵（信道+参数溯源+CRB 框架搭一次 3 候选共用）+ 并行矩阵（B11↔B7 机制正交可并行 / B3 单独序列）+ 新对话拆分建议（对话 1 基建+B11 oracle / 对话 2 B11 MVE 或 B7 / 对话 3 B3 架构）。

用户："可以，建议参考我旧的代码 projects/simulation/README.md，以及，想想之后咋组织这一大堆。不好好组织肯定会乱"——主线读旧仿真基建（README + common/ 7 模块 + params.py pydantic source_type + explore/ n1/mcs 模式）+ 设计组织方案（explore 每候选一子目录 + 增量扩 common + MVE 通过转 experiments + 关键规则 7 条防乱）。

### 治理 Trigger 3 阻断：MVE 执行撞切法地图专题 scope

用户："D:\code\study\research-protocol\.sessions\2026-07-05-carrier-sync-v2-cut-pattern 写这个专题吧"。

主线 session-governance Trigger 3（扩大范围检查）发现矛盾：切法地图专题 topic-index 明确写"不判 Go/Kill / 不拆方法配方 / 不排 Q# 优先级"（明确不含第 1/2/3 条），而 MVE 执行的本质就是判 Go/Kill + 拆方法配方。治理 skill 要求触"明确不含"需 explicit user confirmation + scope change record + D### 决策。

主线 AskUserQuestion 给 3 选项（A 开新专题 / B 重新激活切法地图扩 scope / C 切法地图下写 handoff 指向新专题）。**用户选 A 开新专题**。

### 新专题开题（治理 Trigger 1 + 2 流程）

**slug**：`2026-07-06-step4a-mve-execution`（日期+阶段定位，对齐项目惯例）

**注册表登记**（_registry.yaml 新增条目）：
- status: active
- depends_on: 2026-06-20-problem-driven-redirection（继承 S031 排优先级 + D005/D006 + 5 口径警示）+ 2026-07-05-carrier-sync-v2-cut-pattern（切法地图参照系）+ 2026-07-02-carrier-sync-v2-deep-read（35 Q# 总表 + 12 份 B 点笔记）
- conflicts_with: []

**topic-index.md 建立**（10 条不变量 + 范围边界 + 组织方案 + 基建盘点）：
- 不变量 10 条（继承上游 9 条 + profile 第 8 次"急于推进"防线激活）
- 明确不含 6 条（不回头救 6 次 Kill / 不判 B9/B1 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）
- 组织方案（目录结构 + 关键规则 7 条防乱）

**voice.md 建立**（3 条原话登记）。

### 仿真基建盘点（S001 确立）

**已有**（projects/simulation/，成熟，TL-24/TL-13 已制度化）：
- `common/` 7 模块：`_channel/_modulation/_recovery/_kf/_equalizer/_experiment/_config`
- 信道：`gg_block`（Gamma-Gamma 块衰落）+ `doppler_phase`（Doppler+phase noise）+ `generate_shared_realization`
- 调制：QPSK / 16-QAM + Gray 映射 + `ber_eval`
- 载波恢复：VV / BPS / DPLL / KF（4 方法）
- params.py：pydantic + source_type + audit_flag（TL-26 已制度化，每个参数标来源）
- explore/ 模式：`*-MVE-SPEC.md` 契约 + 脚本 + results.json（n1/mcs 两个先例）
- archive/：旧代码禁用（TL-24）
- SPEC.md / DESIGN-modular-split.md / CAPABILITY_AUDIT.md 文档齐

**缺口**（本轮扩）：
- `_modulation.py` 缺 M-APSK（B11+B3 需要 8PSK / (8,8)-16APSK / 32APSK）
- `_recovery.py` 缺 DA ML（B11 baseline + B3 CPE 子组件）/ NDA-ML（B11 方法）/ Gardner TED（B7 方法 + B3 FOE 子组件）/ FOE（B7 baseline PSA FOE）
- params.py 缺 B11/B7/B3 参数族（CLW 500kHz / 7% HD-FEC / LEO Doppler rate / 多孔径阵列配置）

**最大工程红利**：搭一次共享基建（M-APSK + ML 估计器 + 星地湍流扩展），3 候选共用。DA ML 跨 B11+B3 复用，Gardner TED 跨 B7+B3 复用。

### 组织方案定稿（S001 确立）

**目录结构**（见 topic-index 当前范围段）：
- common/ 增量扩充（M-APSK / ML 估计器 / 信道扩展）
- params.py 加 B11/B7/B3 参数族
- explore/ 三个新子目录（b11-nda-ml-sto-cpe / b7-gardner-ted-foe / b3-subsystem-coordination）
- experiments/ MVE 通过后转正

**关键规则 7 条防乱**：TL-24 不引用旧代码 / TL-13 共用信道 / TL-26 参数溯源 / TL-27+FR-21 oracle 上界前置 / TL-20 先建理论预期 / FR-18 竞争格局 / explore 隔离不污染 experiments。

### 复用矩阵（S001 确立）

| 组件 | B11 | B3 | B7 | 复用方式 |
|---|---|---|---|---|
| 星地湍流信道（GG+Wiener+Doppler）| ✅ | ✅ | ✅ | 共享 common/_channel.py（TL-13）|
| 参数溯源库 | ✅ | ✅ | ✅ | 共享 params.py（TL-26）|
| DVB-S2 调制格式集 | ✅ 核心 | ✅ M-APSK | ⚠️ QPSK/16QAM | 共享 common/_modulation.py |
| oracle CRB 推导框架 | ✅ 频域 ML CRB | ✅ 联合 CRB | ✅ 时域 TED CRB | 同一框架不同应用 |
| DA ML baseline | ✅ | ✅ CPE 子组件 | — | 跨候选复用 |
| Gardner TED | — | ✅ FOE 子组件 | ✅ 方法 | 跨候选复用 |

### 并行矩阵（S001 确立）

- **B11 ↔ B7 机制正交可并行**：B11 频域 NDA-ML 盲估计（前馈闭式）vs B7 时域 Gardner TED 反馈环。CRB 推导可派 2 子 agent 同时，MVE 独立跑
- **B11/B7 内部强依赖**：oracle 上界 → MVE（TL-27/FR-21 硬门控）+ 信道模型实现（基建先搭）
- **B3 单独序列不并行**：4 支路→星地迁移架构假设需先决（多孔径阵列 vs 单链路）+ 信道模型需扩多孔径阵列版本 + A1 归属（jphot+oe 已做联合）前置工作量大

### 对话拆分（S001 确立）

- **对话 1**（H001）：基建增量扩充（M-APSK + DA ML/NDA-ML/Gardner TED/FOE + params 参数族）+ B11 oracle CRB 推导（<0.5dB 降为参考不卡死 / ≥0.5dB 写 B11-MVE-SPEC）
- **对话 2**（视对话 1）：B11 MVE（若 CRB 过）或 B7 全流程（若 B11 Kill）
- **对话 3**（最后）：B3 架构决策 + 视情况 MVE

### 标准校准（S001 后半段，用户质疑触发）

**触发**：用户两连问——"这么多东西推完了，啥也弄不出来的可能性大吗"+"但这几十个Q，最后难道都不行吗？...也能想想可能是哪里考虑不周？"

**主线诊断**（自我诊断 + 概率重估）：
- **最可能考虑不周的地方**：S031 评估时用了期刊级标准判会议候选（FR-21<0.5dB 砍 B1 + A1 严查 B7 + 主题锁载波同步判 B9 偏题）——是 profile"急于给方向性结论"的新表现，这次是"急于用严标准砍"
- **概率重估**：严守 S031 标准 → 30-40% 颗粒无收；校准到会议+大论文支撑+同门范式标准 → **10-15%**
- **校准依据**：同门范式（夏兆宇/王培森/李兀祺）在这个领域发了学位论文，证明物理上有可发的增量——若推完不行而同门行了，更可能是标准差而非物理差

**校准 3 点**（写入 topic-index 不变量 11/12/13 + 标准校准段）：
1. **B1-Q1 不预设 Kill**：FR-21 oracle 上界 <0.5dB 不直接砍，降级为联合判断（sat.1553 L440 open problem 自报证据链 ~5% 最强 + [60] Leven 理论锚 +1dB），用户拍板
2. **B9-Q1 不锁"载波同步改进"主题**：放开 S007 处理技术宽义，DRE（TX 侧量化噪声整形）+ 自相干绕开载波同步是合法处理改进；A1 归属用同门范式对标（搬星地+加湍林是合法场景迁移）
3. **D006 边界 7 次升优先级**：从"单独评估"升为"潜在大论文一致性研究方向"——7 次重复是文献实证强（非孤证）+ 块 A/B/C/D 延续 + **其他候选都是单点，这 7 个连起来是大论文一章的叙事骨架**。B11/B7 单点 MVE 跑完立刻评估

**校准后范围扩大**：B1-Q1 / B9-Q1 / D006 边界 7 次都进 MVE 评估范围（原本只 B11/B3/B7 三个）。校准不是违反不变量，是修正 S031 评估时过严的标准。

## 决策引用

- **无新建 D###**（专题开题 + 基建盘点 + 组织方案定稿 + 标准校准，非架构决策；MVE Go/Kill 决策留对话 1-3 用户拍板时立）
- **标准校准**（S001 后半段，用户质疑触发）：S031 评估时用了期刊级标准（FR-21<0.5dB 砍 + A1 严查 + 主题锁载波同步）判会议级候选，是 profile"急于给方向性结论"的新表现——这次是"急于用严标准砍"。校准 3 点写入 topic-index 不变量 11/12/13 + 标准校准段：
  - **不变量 11**：B1-Q1 不预设 Kill（FR-21 <0.5dB 降为参考不卡死，联合 sat.1553 open problem 证据链 + [60] Leven 理论锚综合判断，用户拍板）
  - **不变量 12**：B9-Q1 不锁"载波同步改进"主题（放开 S007 处理技术宽义，DRE + 自相干绕开载波同步是合法处理改进）
  - **不变量 13**：D006 边界 7 次升优先级为"潜在大论文一致性研究方向"（B11/B7 单点 MVE 跑完立刻评估 7 个联合叙事）
- 引用既有：D005（务实路线 Go 判据 + 会议门槛放宽）/ D006（前馈不撞/环路 TF 联合建模则撞）/ D009（靠谱方向 checklist）/ D017（饱和池/稀池判读框架）/ D018（中性提取扩展，本专题判 Go/Kill 是用户授权的 Step 4a 维度 D 动作）/ **S007 处理技术边界（不变量 12 校准依据）**

## 范围确认

- 本轮是否在 scope boundary 内：**是**（专题开题 + 基建盘点 + 组织方案 + H001 交接，都是 S001 启动动作）
- **守 3 步上限**：本轮实际超出 3 步（上游 S031 3 步 + 旋钮/思想/坑防线 + 基建盘点 + 新专题开题 5 文件），但都是同一逻辑链（上游 Go/Kill → 旋钮细化 → 基建盘点 → 专题开题 → 交接），且用户明确推动"去新对话试"+ "想想咋组织"。**主线认错**：上游 S031 之后用户反馈的旋钮/思想/坑防线 + 基建盘点 + 新专题开题应整体视作"S031 续接 + 新专题 S001 开题"两段，每段各自 3 步。后续严格守 3 步上限
- **守 profile 第 8 次"急于推进"防线**：本对话未跑任何 MVE，只开题+盘点+组织+交接，Go/Kill 决策留新对话用户拍板
- **守切法地图是参照系不是答案**：组织方案和 H001 引用切法地图模式（B11 稀池 1 独占赛道 / B7 OFC 会议样本 / B3 饱和池联合建模），但不搬"切法地图说这个好"
- **守治理 Trigger 3**：MVE 执行撞切法地图 scope 时主线阻断 + AskUserQuestion 给选项 + 用户选 A 开新专题，scope change record + D### 不需要（开新专题非扩旧专题 scope）

## 后续

### 已完成（本对话）

1. 上游 S031 落盘（35 Q# 优先级 + 前 5 名 Go/Kill + 旋钮 + 思想 + 坑防线）
2. 切法地图专题转 closed（使命已达，待步骤 6 执行）
3. 新专题 2026-07-06-step4a-mve-execution 开题：
   - 注册表登记（depends_on 3 个）
   - topic-index.md（10 不变量 + 范围边界 + 组织方案 + 基建盘点）
   - voice.md（3 条原话）
   - H001（对话 1 三步详述 + 接口变更 + 验证阈值 + 接收方验证）
   - S001（本文件）

### 下一步（新对话执行 H001）

新对话报到后按 H001 三步：
1. 报到 + 框架文件重读
2. 基建增量扩充（子 agent A 扩 _modulation+_recovery / 子 agent B 扩 params / 主线扩 _channel）
3. B11 oracle CRB 推导（子 agent ≤15 分钟）+ 判定（<0.5dB Kill 转 B7 / ≥0.5dB 写 B11-MVE-SPEC 进对话 2）

### 待办（本对话收尾）

- 步骤 6：切法地图专题 topic-index + registry 转 closed
- 步骤 7：上游专题 voice.md/S031 补记录"转新专题"
- 自动提交规则：对话末统一 commit（如用户要求提前提交则执行）
