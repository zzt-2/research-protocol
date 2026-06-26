# Task Brief: 第三轮换维度检索（问题/失效词 + 诊断 + 综述金矿）

> 来源: S009（外部评审 + 主线 push back 后定案）| 产出位置: `projects/thesis-fso/landscape.md` v4
> 日期: 2026-06-22
> 唯一文档: 执行方只拿这一个文档 + 已有 landscape.md v3

## 0. TL;DR（执行方先读）

你在 research-protocol 项目，手上已有 landscape.md v3（509 主表，场景词 430 + 设备词 79）。

**你的任务**：做第三轮换维度检索，三个**性质不同**的动作：
- **动作 A（真·地勘，方法中性）**：问题/失效维度检索，召回"自陈失效/开放问题"的研究型论文。结果入主表
- **动作 B（受控诊断，不是地勘）**：方法+问题复合词，直接命中"某方法遇到某问题"。标诊断不地勘，产出只入诊断段
- **动作 C（综述金矿）**：综述/对比/自陈失效声明词。综述天然做对比、主动盘点 open problem，是找缝最强信号源。结果入主表

**产出**：landscape.md v4 = v3 + 动作 A 主表续段 + 动作 C 主表续段 + 动作 B 诊断段（物理隔离）。

**最高纪律**（按优先级）：
1. **三动作物理隔离**——A/C 入主表续段，B 入诊断段（单独、明示"诊断不是地勘"）。混在一起 = 方法论边界模糊（S007/S009 评审核心教训）
2. **动作 A/C 守方法中性不锁模块**——问题/失效大类词 + 综述大类词，**禁止** modulation/synchronization/equalization/channel-estimation/coding/detection 这些模块词（H002:24/67 明令）。带模块词 = 偏航 A 红线
3. **动作 B 必须明示"诊断不是地勘"**——用方法+问题复合词是**受控例外**，产出只入诊断段不入主表，不污染候选池。这个例外不侵蚀"地勘方法中性"原则，因为 B 根本不是地勘
4. **全留拉表**（H002 死规定）——三动作的所有结果都留，包括范围外入附录
5. **A/B 分离诊断是本轮核心价值**——动作 A/C 颗粒无收 = 物理约束成立该跟老师谈调范围；有信号 = 检索盲区成立继续

## 1. 背景（了解即可不对照评价）

### 1.1 为什么有这次任务

前两轮地勘（场景词 430 + 设备词 79 = 509 主表）共同盲区：**全在搜"是什么"**（什么场景/设备/模块），没有一个在搜"**出了什么问题**"。换到"问题/失效"维度可能召回自陈失效论文（跟判据 A 同构）。

S009 用户提出"多找几个角度切入"，主线做 A/B 分离诊断（A 检索盲区 vs B 物理约束）后认可换维度。外部对话评审挑出：
- 问题维度里**物理现象词（scintillation/turbulence/beam wander）跟已有维度重叠**，应砍
- 视角偏差：**工程师词（degradation/loss）偏"已解决"，研究者词（limitation/challenge/open）偏"未解决"**——要的是后者
- 综述论文是**找缝金矿**（作者主动盘点 open problem），是之前三轮都漏召的最强缝信号源

主线 push back 外部第 4 点"判据 A 同构=方法对比"——方法对比论文≠baseline 失效证据（可能只是"我比你好一点"），真正跟判据 A 同构的是独立诊断 baseline 失效的论文（标题常含 limitation of / failure of / when X fails）。最终融合为三动作方案。

### 1.2 范围边界（老师同意 + 非死轴）

- **背景锁死**：星地激光通信（satellite optical / satellite laser / FSO satellite）。跑出大背景不收
- **"处理技术"边界**（用户 2026-06-22 确认，见 voice.md 06-22 段）：
  - ✅ 算：调制/复用、检测（相干/自相干/外差/零差）、编码/FEC/交织、信道估计/均衡、同步、信道建模/湍流（信道处理）、AO/自适应光学算法（波前校正算法）
  - ❌ 不算（老师不同意）：ATP/指向（光学/控制工程）、网络层/路由/RWA、ISL/feeder/系统级、QKD/深空/在轨/硬件
- **死轴**（5 次失败 + S003 决议 Kill）：载波同步（PLL/DPLL/Costas/Kalman 载波相位恢复）、信道估计（LS/LMS/RLS 自适应均衡）

### 1.3 不在本次任务范围

- ❌ 选方向（那是选地之后做批评汇总的事）
- ❌ 批评汇总（S002 已做）
- ❌ 改框架协议（S003 已决议"先测不改协议"）
- ❌ ATP/网络层/QKD/深空等跑题地带（涌现了入附录 C 注明范围外）
- ❌ 用方法+问题复合词（动作 B）产出候选入主表

## 2. 任务详情

### 2.1 动作 A：问题/失效维度地勘（方法中性，入主表）

#### 要回答的问题

用问题/失效维度词（研究者视角的"未解决"词），能否召回前两轮（场景词/设备词）没覆盖到的"自陈开放问题"型论文？

#### 检索词集（方法中性，研究者词，**禁止模块词**）

主集（必跑，研究者视角词——外部评审第 2 点）：
- `satellite optical performance limitation`
- `satellite optical open challenge`
- `satellite optical fundamental limit`
- `satellite optical capacity bound`
- `satellite optical bottleneck`
- `satellite optical Doppler impact`

结果型补集（跟已有维度重叠低，是结果度量不是物理现象）：
- `satellite optical SNR degradation`
- `satellite optical BER floor`

**砍掉的词**（外部评审第 1 点：跟已有场景词维度重叠）：scintillation / turbulence / beam wander / atmospheric impairment。这些在 v2/v3 主表里已是信道建模子地带（v2 47 条），跑了浪费。

**派子 agent 前过用户审**（用户原话"派子 agent 前把检索词先列出来过目"）。

**工具**：`tools/search` + `tools/blit --source ieee`。每 query max=50。

**偏航检查 A 单独验证**：动作 A 检索词 grep 一遍，确认零模块词（modulation/synchronization/equalization/channel-estimation/coding/detection）+ 零物理现象重叠词（scintillation/turbulence/beam wander/atmospheric impairment）。

#### 产出格式（动作 A）

`## 主表（续，第三轮动作 A 问题/失效维度检索，2026-06-22）` 段，格式同 v3 主表 7 字段（# / 年 / 子地带 / 做的事 / 湍流 / baseline 是谁 / 验证 / 缝潜力）。

**所有结果全留**，包括范围外（ATP/网络层）入附录 C 注明"范围外（动作 A 问题词检索涌现）"。

### 2.2 动作 B：方法+问题复合词诊断（不是地勘，入诊断段）

#### 要回答的问题

用方法+问题复合词（如 equalizer × Doppler / synchronization × turbulence）能否直接命中"某 baseline 方法在某失效模式下失效"的论文？这类论文是最强判据 A 证据。

#### 为什么动作 B 必须用模块词（且这不算违背方法中性）

判据 A 信号是"某 baseline 方法在常见条件下失效"。要直接命中这个信号，**必须**用方法名（equalizer/synchronization 等）+ 问题（Doppler/turbulence）复合词搜。但这**不是地勘动作**——是诊断验证。明确标"诊断不是地勘"，产出只入诊断段不入候选池，不侵蚀方法中性原则（S007/S008/S009 三轮已验证）。

#### 检索词集（方法+问题复合词，**仅动作 B**，禁止挪用到地勘）

8 个复合词（方法 × 问题）：
- `satellite optical equalizer Doppler`
- `satellite optical synchronization turbulence`
- `satellite optical modulation phase noise`
- `satellite optical equalization residual`
- `satellite optical detection mismatch`
- `satellite optical coding bursty`
- `satellite optical coding fading`
- `satellite optical modulation nonlinear`

**注意**：这些词是**为诊断服务**，不是为找候选。检索结果**只统计占比 + 抽取真缝候选**，不入主表。真缝候选入诊断段（单独的 E 类清单）。

#### 产出格式（动作 B）

`## 诊断段（v4 动作 B 方法+问题复合词诊断，不是地勘，受控例外，2026-06-22）` 段，明示标"不是地勘"。格式同 v3 附录 E：
- 死轴/方法层失效占比 + 真缝密度对照表
- 真·方法论缝候选清单（严判，待精读验证，不作为 Go/No-Go 依据）
- 判读（区分"人数多"和"有缝"）

### 2.3 动作 C：综述/对比/自陈失效声明词（方法中性，入主表）

#### 要回答的问题

综述论文天然做对比、主动盘点 open problem——这是前两轮（场景词/设备词）完全漏召的最强缝信号源。用综述/对比词能否召回这批金矿？

#### 检索词集（综述/对比词，方法中性，**禁止模块词**）

主集（必跑）：
- `satellite optical communication survey`
- `satellite optical communication review`
- `satellite optical communication tutorial`
- `satellite optical communication existing methods`（召回"compared with existing methods"的对比论文）
- `satellite optical communication limitations of`（召回"limitations of prior work"的缝声明）

补集（可选）：
- `free space optical satellite survey`
- `satellite laser communication overview`

**派子 agent 前过用户审**（同动作 A）。

**偏航检查 A 单独验证**：动作 C 检索词 grep 一遍，确认零模块词。

#### 产出格式（动作 C）

`## 主表（续，第三轮动作 C 综述/对比词检索，2026-06-22）` 段，格式同动作 A。

**特别注意**：综述论文要单独标记 `综述` 子类（在子地带字段或缝潜力字段加标记），因为综述是高价值精读对象——精读阶段优先级高于普通论文。

### 2.4 三动作执行方式

- **派子 agent 前过用户审**：执行方拿到本 T 后，**先把动作 A/B/C 检索词集分别列给用户过目**，用户确认方法中性定位（A/C 中性、B 是诊断）才派子 agent 跑
- **三动作分别派 agent**（不混在一个 agent），避免方法论混淆
- **工具**：tools/search + tools/blit --source ieee
- **派发**：动作 A 8 词可拆 2 agent（search 4 词 + IEEE 4 词），动作 B 8 词单 agent，动作 C 5-7 词可拆 2 agent。单 agent ≤15 分钟
- **主线合并去重**：动作 A/C 结果和 v3 合并入主表续段；动作 B 结果单独统计，不入主表
- **偏航检查 A-E**：A 方法中性（A/C 验问题词+综述词零模块词、B 明示诊断例外）/ B 全留+🔴必填+无臆造 / C 不滑回开题线索 / D 每步说清为什么 / E 跑完停一步看方法论

### 2.5 A/B 分离诊断判读（本轮核心价值）

**这是第三轮检索的真正目的——不只是补候选，是 A/B 分离诊断**：

| 三动作产出 | 判读 | 后续 |
|---|---|---|
| 动作 A/C 涌现新方法层缝信号 | A 成立（之前是检索盲区），地有缝 | 继续：精读验证候选 |
| 动作 A/C 颗粒无收（只有信道建模/物理分析） | B 成立（物理约束），地真没缝 | **该跟老师谈调范围**（S007 结构性矛盾） |
| 动作 A/C 有部分信号但不强 | 不确定，需精读 + 可能要第四轮 | 精读后再判 |

**关键提醒**：动作 A/C 颗粒无收不代表本轮失败——**这本身就是有价值的诊断结论**（证明物理约束成立），据此可以诚实跟老师谈调范围。颗粒无收好过凑数。

## 3. 已知陷阱（基于历史失败的具体案例）

### 3.1 动作 A 滑回"先有方法"（偏航检查 A 红线）

**反面案例**：S002 批评汇总 PLL 验证里用 `pll-or-costas`。动作 A/C **禁止**模块词。

**正确做法**：A/C 只用问题大类词 + 综述大类词，让"做什么"从结果涌现。

### 3.2 动作 A 用物理现象词（外部评审第 1 点）

**陷阱**：scintillation/turbulence/beam wander 跟 v2/v3 场景词维度重叠（信道建模已是 v2 最大子地带 47 条），跑了浪费。

**做法**：A 组只用研究者视角的失效/限制词（limitation/challenge/bottleneck/bound）+ 少量结果度量词（SNR degradation/BER floor），砍纯物理现象词。

### 3.3 三动作混淆（S007/S009 评审核心教训）

**陷阱**：把动作 B 方法+问题复合词结果并入主表 → 方法论边界模糊 → "方法中性"原则被侵蚀。

**做法**：A/C 入主表续段，B 入诊断段（单独、明确标"不是地勘"）。三段物理隔离。

### 3.4 把综述当低质量剔除

**陷阱**：综述论文常被当作"二手资料"忽略。但综述是**找缝金矿**（外部评审第 4 点）——作者主动盘点哪些方法在哪些场景失效，是最强缝信号源。

**做法**：综述论文入主表（合法地勘对象），单独标记 `综述`，精读阶段优先级高于普通论文。

### 3.5 动作 A/C 被信道建模污染（外部评审第 3 点）

**陷阱**：问题/失效词可能召回大量信道建模论文（建模天然研究湍流/损伤）——这类是物理层分析型研究，不是方法层缝。

**做法**：检索阶段**接受污染**（宁多召回靠精读筛，S004 定的原则），但在产出里**单独标记**：
- 方法层缝（判据 A 直接可用，候选池）
- 物理层分析缝（判据 A 间接，分析型研究）
- 信道建模（纯物理分析，不入候选池）

精读阶段做这个区分。

### 3.6 动作 B 复合词命中"我解决了 X 问题"

**陷阱**：`equalizer Doppler` 可能召回"我提出了抗 Doppler 均衡器"（已解决），不是"Doppler 让均衡器失效"（开放问题）。

**做法**：动作 B 抽真缝候选时严判——abstract 要含"baseline 失效/限制"信号，不能只是"我提出 X 方法"。

### 3.7 IEEE 债务（S008 经验）

IEEE blit 可能被实时反爬+累积风险分限流。search API 增量价值够时（≥200 raw），留债务不卷用户手动下。

## 4. 验收（主线拿到产出后怎么检查）

执行方回传 landscape.md v4 后，主线按此清单验收：

- [ ] 三动作物理隔离（A/C 入主表续段、B 入诊断段，不同段、不同方法论标注）
- [ ] 动作 A 检索词 grep 验证零模块词 + 零物理现象重叠词
- [ ] 动作 C 检索词 grep 验证零模块词
- [ ] 动作 B 诊断段明确标"诊断不是地勘"，检索词列表明示方法+问题复合词
- [ ] 动作 B 结果**没**并入主表（并了 = FAIL）
- [ ] 综述论文单独标记 `综述` 子类
- [ ] 动作 A/C 产出区分了方法层缝 vs 物理层分析缝 vs 信道建模
- [ ] **A/B 分离诊断判读存在**（动作 A/C 颗粒无收 → B 成立该谈调范围 / 有信号 → A 成立继续 / 不确定 → 精读后再判）
- [ ] 偏航检查 A-E 全过

**验收 FAIL 的情况**（必须返工）：
- 动作 A/C 检索词带模块词 → 偏航 A 红线
- 动作 B 结果并入主表续段 → 方法论边界模糊
- A/B 分离诊断判读缺失 → 本轮核心价值丢失
- 综述被当低质量剔除 → 金矿丢失

## 附：产出回传位置

- 主产出：`projects/thesis-fso/landscape.md`（v3 → v4）
- 检索原始数据：`search-archive/2026-06-22/landscape3-a-*.json`（动作 A）+ `landscape3-c-*.json`（动作 C）+ `diag2-*.json`（动作 B，前缀区分）
- 操作日志：`.sessions/2026-06-20-problem-driven-redirection/S010-third-landscape-execution.md`（S### 编号取当前最大+1，执行前先扫目录确认）

**完成后在 topic-index 进展线索加 S010 条目，悬而未决 #6/#9 更新**。
