# Task Brief: 二次地勘（设备词补盲）+ 死轴冷区诊断验证

> 来源: S007（外部方法论评审 + 主线 push back 后定案）| 产出位置: `projects/thesis-fso/landscape.md` v3
> 日期: 2026-06-22
> 唯一文档: 执行方只拿这一个文档 + 已有 landscape.md v2

## 0. TL;DR（执行方先读）

你在 research-protocol 项目，手上已有 landscape.md v2（430 主表，16 个场景词检索产出）。

**你的任务**：做两个**性质完全不同的动作**，严格分开执行和产出：
- **动作 A（真·二次地勘）**：用**设备/系统词**（transceiver/modem/receiver）补一次地勘漏掉的背景维度，**延续 S003 方法中性不锁模块**，结果入主表
- **动作 B（诊断验证，不是地勘）**：用**模块词**（synchronization/channel-estimation/equalization）做死轴冷区占比对比，验证 S006 冷区结论是检索词偏差还是结构性事实。**动作 B 不产出候选，只产出对比表**

**产出**：landscape.md v3 = v2 + 动作 A 主表续段 + 动作 B 死轴诊断对比表（单独段，明确标"诊断不是地勘"）。

**最高纪律**（按优先级）：
1. **动作 A 和动作 B 物理隔离**——不同检索词集、不同产出段、不同方法论定位。混在一起 = 方法论边界模糊（S007 评审核心教训）
2. **动作 A 守 S003/H02 方法中性不锁模块**——只用设备/系统/拓扑词，**禁止** modulation/synchronization/equalization/channel-estimation/coding/detection 这些模块词（H002:24/67 明令）。带模块词 = 偏航 A 红线
3. **动作 B 必须明示"诊断不是地勘"**——用模块词是**受控例外**，产出只入诊断段不入主表，不污染候选池。这个例外不侵蚀"地勘方法中性"原则，因为 B 根本不是地勘
4. **全留拉表**（H002 死规定）——两个动作的所有结果都留，包括范围外入附录
5. **动作 B 判读区分"人数多"和"有缝"**——占比涨只说明做的人多，物理证据（中弱湍流 σ²_R<1 压死没缝）不变

## 1. 背景（了解即可不对照评价）

### 1.1 为什么有这次任务

一次地勘（S004/S006）的 16 个检索词**全是场景词**（inter-satellite/GEO/feeder/relay/terminal/cubeSat/payload/coherent/deep-space/network）。但仔细分类，**全是"链路/拓扑/任务"维度**，缺一个维度：**"设备/收发机"**（transceiver/modem/receiver/前端）。

S007 方法论评审发现：原 T001 草案想用**模块词**（modulation/synchronization 等）补地勘，但这违背 S003/H02 方法中性（H002:24/67 明令"不带模块词"）。所以本 T 拆成两动作：
- 动作 A 补**设备维度盲区**（跟一次地勘同方法论，无争议）
- 动作 B 用模块词做**诊断**（不是地勘，是验证 S006 冷区结论）

### 1.2 范围边界（老师同意 + 非死轴）

- **背景锁死**：星地激光通信（satellite optical / satellite laser / FSO satellite）。跑出大背景不收
- **"处理技术"边界**（用户 2026-06-22 确认，见 voice.md 06-22 段）：
  - ✅ 算：调制/复用、检测（相干/自相干/外差/零差）、编码/FEC/交织、信道估计/均衡、同步、信道建模/湍流（信道处理）、AO/自适应光学算法（波前校正算法）
  - ❌ 不算（老师不同意）：ATP/指向（光学/控制工程，非通信处理）、网络层/路由/RWA（跑题）、ISL/feeder/系统级（系统/网络）、QKD/深空/在轨/硬件（跑题或工程）
- **死轴**（5 次失败 + S003 决议 Kill）：载波同步（PLL/DPLL/Costas/Kalman 载波相位恢复）、信道估计（LS/LMS/RLS 自适应均衡）

### 1.3 不在本次任务范围

- ❌ 选方向（那是选地之后做批评汇总的事）
- ❌ 批评汇总（S002 已做）
- ❌ 改框架协议（S003 已决议"先测不改协议"）
- ❌ ATP/网络层/QKD/深空等跑题地带（涌现了入附录 C 注明范围外）
- ❌ 用模块词产出候选（动作 B 不入候选池）

## 2. 任务详情

### 2.1 动作 A：设备词补盲地勘（延续 S003 方法论）

#### 要回答的问题
用设备/收发机维度词补搜，能否涌现出一次地勘（链路/拓扑/任务词）没覆盖到的处理技术密集地带？

#### 检索词集（方法中性，设备/系统维度，**禁止模块词**）

主集（必跑）：
- `satellite optical transceiver`
- `satellite optical modem`
- `satellite optical receiver`
- `satellite optical transmitter`
- `satellite optical frontend`
- `optical satellite payload transceiver`
- `satellite optical photonic receiver`
- `satellite optical DSP`（边界——DSP 算设备级还是模块级？倾向设备级，因为是"接收机里的 DSP 单元"，不是具体算法。执行方自检：如果觉得偏模块，砍掉换 `satellite optical digital processing unit`）

补集（可选）：
- `satellite optical coherent transceiver`
- `satellite optical balanced receiver`
- `satellite optical FPGA receiver`

**派子 agent 前过用户审**（用户原话"派子 agent 前把检索词先列出来过目"）。

**工具**：`tools/search` + `tools/blit --source ieee`。每 query max=50（blit 实际 25/query 也行）。

**偏航检查 A 单独验证**：动作 A 的检索词 grep 一遍，确认零模块词（modulation/synchronization/equalization/channel-estimation/coding/detection）。

#### 产出格式（动作 A）

`## 主表（续，二次地勘新增，设备词检索）` 段，格式同 v2 主表 7 字段（# / 年 / 子地带 / 做的事 / 湍流 / baseline 是谁 / 验证 / 缝潜力）。

**所有结果全留**，包括范围外（ATP/网络层）入附录 C 注明"范围外（动作 A 设备词检索涌现）"。

### 2.2 动作 B：死轴冷区诊断验证（不是地勘）

#### 要回答的问题

S006 场景词检索得出的死轴冷区（载波同步 5.3% / 信道估计 3.0%），在**模块词**检索下占比是否大涨？
- 如果还是低 → S006 冷区结论加固，5 次失败依据更硬，下一轮选地放心避开死轴
- 如果大涨 → 标注"S006 冷区可能部分是检索词偏差"，主线决定是否复议。**但占比涨只说明做的人多，物理证据不变**

#### 为什么动作 B 必须用模块词（且这不算违背方法中性）

死轴冷区是按**模块维度**（载波同步/信道估计）统计的。要测这个维度的占比，**必须**用模块词搜。但这**不是地勘动作**——是诊断验证，跟 S002 "Are PLLs dead" 候选验证同性质。明确标"诊断不是地勘"，产出只入诊断段不入候选池，不侵蚀方法中性原则。

#### 检索词集（模块词，**仅动作 B**，禁止挪用到地勘）

3 个死轴词 + 1 个对照：
- `satellite optical carrier synchronization`（死轴 1）
- `satellite optical channel estimation`（死轴 2）
- `satellite optical equalization`（死轴 3）
- `satellite optical modulation`（对照——非死轴热区，验证模块词检索本身有效）

**注意**：这些词是**为诊断服务**，不是为找候选。检索结果**只统计占比**，不入主表。

#### 产出格式（动作 B）

`## 死轴冷区诊断验证（诊断，不是地勘；S007 评审后定案）` 段，紧跟"子地带涌现分布"后。格式：

```markdown
## 死轴冷区诊断验证（诊断，不是地勘；S007 评审后定案）

> ⚠️ 本段是诊断验证，不是地勘。检索用了模块词（违背 S003 地勘方法中性），
> 但这是受控例外——产出只入本诊断段，不污染候选池，不侵蚀"地勘必须方法中性"原则。
> 动作 B 和动作 A 物理隔离。

### 诊断检索词（仅诊断用，禁止挪用到地勘）
- satellite optical carrier synchronization
- satellite optical channel estimation
- satellite optical equalization
- satellite optical modulation（对照）

### 死轴占比对比表

| 子地带 | v2 占比（场景词） | B 占比（模块词） | 判读 |
|--------|-----------------|-----------------|------|
| 载波同步 | 5.3% (23/430) | X% (M/总) | [加固/推翻/需复议] |
| 信道估计 | 3.0% (13/430) | X% | [加固/推翻/需复议] |
| 均衡 | (v2 未单列) | X% | [新增观察] |
| 对照：调制（热区）| 20% (86/430) | X% | [验证模块词检索本身有效] |

### 判读（按 S007 §2.4 标准）

[冷区是结构性事实 / 冷区是检索词偏差需复议 / 部分加固部分推翻]

**关键提醒**：占比涨只说明"做的人多"，物理证据（中弱湍流 σ²_R<1 压死没缝）不变。
```

### 2.3 死轴诊断判读标准（防误判）

| B 载波同步占比 | 判读 |
|---|---|
| <8%（接近 v2） | 冷区加固 |
| 8-15% | 部分修正，主线评估 |
| >15% | 推翻冷区结论（但物理证据不变，复议概率低）|

**注意**：即使占比大涨，物理证据（地被中弱湍流压死没缝）不会因为检索词变多而消失。判读时区分"人数多"和"有缝"。

### 2.4 执行方式（动作 A + 动作 B 派发）

- **派子 agent 前过用户审**：执行方拿到本 T 后，**先把动作 A + 动作 B 的检索词集分别列给用户过目**，用户确认方法中性定位（A 中性、B 是诊断）才派子 agent 跑
- **动作 A 和动作 B 分别派 agent**（不混在一个 agent 里），避免方法论混淆
- **工具**：tools/search（API 多源）+ tools/blit --source ieee
- **派发**：参考 S006，动作 A 可拆 2 agent（search + IEEE），动作 B 单 agent（3-4 词），单 agent ≤15 分钟
- **主线合并去重**：动作 A 的结果和 v2 合并入主表续段；动作 B 的结果单独统计占比，不入主表
- **偏航检查 A-E**：A 方法中性（A 动作验设备词、B 动作明示诊断例外）/ B 全留+🔴必填+无臆造 / C 不滑回开题线索 / D 每步说清为什么 / E 跑完停一步看方法论

## 3. 已知陷阱（基于历史失败的具体案例）

### 3.1 动作 A 滑回"先有方法"（偏航检查 A 红线）

**反面案例**：S002 批评汇总的 PLL 验证里，检索词带 `pll-or-costas` / `kalman-filter-carrier-synchronization`——带具体方法名。动作 A **禁止**这种词。

**正确做法**：动作 A 只用设备/系统词（transceiver/modem/receiver），让"做什么"从结果涌现。

### 3.2 动作 A 和动作 B 混淆（S007 评审核心教训）

**陷阱**：把模块词检索结果并入地勘主表 → 方法论边界模糊 → 下一轮第三次地勘"方法中性"原则已被破开。

**做法**：动作 A 入主表续段，动作 B 入诊断段（单独、明确标"不是地勘"）。两个段物理隔离。

### 3.3 把 S002 诊断探针当本 T 动作

**陷阱**：`search-archive/2026-06-21/` 有 `kalman-filter-carrier-synchronization` / `satellite-fso-equalization-assumption` / `channel-estimation-assumption` 等——这些是 S002 批评汇总的诊断探针（带批评词 assumption/suboptimal + 具体方法名），**不是本 T 动作 B**。不要并入。

**区分**：文件名带 `assumption`/`suboptimal`/`limitation`/`pll`/`costas`/`kalman` = S002 探针，不是本 T。

### 3.4 范围外地带当候选

**陷阱**：动作 A 设备词检索可能涌出 ATP（光机控制）/ 网络层 / QKD 等跑题地带。

**做法**：范围外入附录 C，标"❌ 范围外，老师不同意"。不剔除（H002 全留），但不计入有效候选池。

### 3.5 动作 B 死轴占比大涨直接复议 PLL

**陷阱**：动作 B 载波同步占比大涨 → 直接说"死轴结论推翻，复议 PLL"。

**正确**：占比涨只说明做的人多，物理证据不变。判读分开"人数多"和"有缝"。

### 3.6 IEEE 无 abstract 信号噪声

IEEE blit 无 abstract，baseline/验证方式默认"未明确(IEEE无abstract)"，缝潜力默认 🟡 待精读。不要因此把 IEEE 条目剔除。

## 4. 验收（主线拿到产出后怎么检查）

执行方回传 landscape.md v3 后，主线（本对话或新对话）按此清单验收：

- [ ] 动作 A 和动作 B 物理隔离（不同段、不同方法论标注）
- [ ] 动作 A 元数据段齐全，主表续段格式与 v2 一致
- [ ] 动作 A 检索词 grep 验证零模块词（偏航检查 A）
- [ ] 动作 B 诊断段明确标"诊断不是地勘"，检索词列表明示模块词
- [ ] 动作 B 死轴占比对比表存在，v2 vs B 占比填齐，判读明确
- [ ] 动作 B 判读区分了"人数多"和"有缝"
- [ ] 动作 B 结果**没**并入主表（如果并了 = FAIL）
- [ ] 没把 S002 诊断探针（带 assumption/suboptimal/具体方法的）并入
- [ ] 范围外条目入附录 C 注明
- [ ] 偏航检查 A-E 全过

**验收 FAIL 的情况**（必须返工）：
- 动作 A 检索词带模块词 → 偏航 A 红线
- 动作 B 结果并入主表续段 → 方法论边界模糊
- 把 S002 诊断探针并入 → 重复 + 视角混淆
- 动作 B 判读只给占比不给"人数多 vs 有缝"区分

## 附：产出回传位置

- 主产出：`projects/thesis-fso/landscape.md`（v2 → v3）
- 检索原始数据：`search-archive/2026-06-22/landscape2-*.json`（动作 A）+ `search-archive/2026-06-22/diag-*.json`（动作 B，文件名前缀 `diag-` 与地勘 `landscape-`/`landscape2-` 区分）
- 操作日志：`.sessions/2026-06-20-problem-driven-redirection/S008-second-landscape-and-diag.md`（S### 编号取当前最大+1，执行前先扫目录确认当前最大 S 编号）

**完成后在 topic-index 进展线索加 S008 条目，悬而未决 #6（地勘方法对不对）+ #7（判据 A 怎么验）更新**。
