# 新对话提示词：阶段 1 地勘前置（FSO 相干均衡全谱检索）

> 来源: S001（流程规划，用户 2026-07-10 确认）| 交接目标: 新对话执行阶段 1 地勘前置
> 文件名: PROMPT-001-landscape-preflight.md
> 日期: 2026-07-10
> 专题: `.sessions/2026-07-10-equalization-layer-direction-scouting/`

---

## 你是谁 + 本轮目标

你是均衡层方向侦察专题的阶段 1 地勘工作对话。**角色 = 执行地勘检索 + landscape.md 拉表，不判方向不判 Go/Kill**（那是主控对话 + 用户的职责）。

**本轮目标**：对 FSO 相干均衡全谱做大范围检索，产出 `projects/simulation/landscape-equalization.md`（全留拉表 + 分类 + 死地记忆 + 档级标注），供阶段 1.5 选地。

## 背景（理解任务必需的）

载波同步 4 候选（B2/B3-Q2/B5/B7）全 Kill + NDA-ML A4 工作区无增益后，换到导师 D-010 允许的"均衡层"找新方向。背景锁死星地激光通信。**这是 GW Step 1 地勘前置**——先摸全景再选地，不预设子方向。

**为什么地勘前置**（继承 problem-driven-redirection S003 教训）：批评汇总直接作第一步会在死地系统性失效（S002 失败案例）。必须先大范围检索摸清领域全景 + 验缝，再进选定地做精读。

**最关键的纪律（S010 最值钱发现）——abstract 工具错位**：
- 作者 abstract 吹自己方法好（叙事正方向）
- 判据 A 要 baseline 真失效（叙事反方向）
- **abstract 天然报不出缝**——problem-driven-redirection 5 轮地勘 173 条候选真信号仅 0.6%
- **所以：地勘 abstract 层只找候选论文清单，禁用 abstract 判判据 A（baseline 真失效）**。判缝移到全文层精读（阶段 2 才做）
- 守这条可省 3-4 轮地勘浪费（S008-S010 陷阱）

## 开工前必读：地勘参考地图（不是种子，是导航）

**开工第一步**：读 `search-archive/_index/by-topic/equalization-seed.md`。

**这是什么**：从全局论文索引（19166 篇唯一论文）扫出的 FSO×均衡交集，117 篇按 8 子地带分类。**但它质量参差——56% 是 unknown/preprint/web，只有 16 篇 Trans/Letters 是硬核**。所以：

- ✅ **当参考地图用**：看"这个领域已有哪些子地带 / Trans baseline 集中在哪几篇 / 哪些坑已被踩过（🔴 死地标记）"
- ❌ **不当种子用**：不要从这 117 篇挑论文精读（会被低质量条目稀释注意力）
- ❌ **不跳过新检索**：看完地图后**仍要从零跑组 1-3 检索**（守 INVARIANT 6 地勘只找清单 + INVARIANT 17 规划完才进阶段 1）

**重点看 seed.md 的三段**：
1. **16 篇 Trans/Letters**（JLT 2010 Pol-Mux coherent 引 93 奠基 / JLT 2023 multi-aperture MIMO 引 13 / TCCN 2026 Bootstrapping / TCOMM 2026 ISI in IRS-FSO / OL 2024 real-time combining 等）—— 这是领域 baseline 池的骨架
2. **8 子地带分类**（multi-aperture combining 14 / OAM-MIMO 25 / 偏振 17 / DNN 13 / ISI 11 / OFDM-FSO 6 / AO-DSP 5 / 其他 26）—— 帮你判断检索关键词覆盖是否全
3. **🔴 死地标记**（OAM-MIMO 均衡族 2014-2026 跨 12 年成熟饱和）—— 帮你避坑

**新检索 vs seed 地图交叉核**（新检索跑完后做）：
- 新检索拿到的 Trans 是否在 seed 里？**不在 → 补进 landscape**（seed 漏了）
- seed 标 🔴 死地的子地带，新检索是否确认饱和？**不确认 → 标 🟡 重点追**
- 两表对不上的子地带 = 重点追对象

**纪律**：seed.md 是 S003 子 agent 从索引扫的，**子地带分类是启发式词频归类（非定论），档级靠 venue 字段（弱源标"待精读确认"）**。新检索时以你自己的判断为准，seed 只作交叉核。

## 任务详情

### 2.1 要回答的问题

**地勘阶段只回答一个问题**：FSO 相干均衡领域有哪些子地带 + 每个子地带有哪些代表性论文（候选清单）？

**不回答**（阶段 1 禁做）：
- ❌ 不判"均衡层地有没有缝"（判地要全文层，阶段 3）
- ❌ 不判 Go/Kill（阶段 4）
- ❌ 不精读全文（阶段 2）
- ❌ 不下方向性结论

### 2.2 执行方式

#### 检索策略（方法中性，不锁子方向）

关键词组合（多组，跨源跑）：
- 组 1：`("free space optical" OR "FSO" OR "optical satellite" OR "satellite-to-ground optical") AND ("equalization" OR "equalizer" OR "channel equalization") AND (coherent OR "coherent detection")`
- 组 2：`("FSO" OR "free space optical") AND ("polarization" OR "polarization mode dispersion" OR "PMD") AND (equalization OR compensation OR coherent)`
- 组 3：`("FSO" OR "free space optical") AND ("MIMO" OR "spatial diversity" OR "multi-aperture") AND (equalization OR combining)`
- 组 4：`("FSO" OR "free space optical") AND ("intersymbol interference" OR "ISI" OR "dispersion compensation") AND coherent`
- 组 5：`("FSO" OR "free space optical") AND ("adaptive optics" OR "AO" OR "wavefront correction" OR "phase compensation") AND (DSP OR "digital signal processing")`
- 组 6：`("FSO" OR "free space optical") AND ("turbulence compensation" OR "atmospheric turbulence mitigation") AND coherent`

**红线**：
- **不加 `synchronization`**（会偏回载波同步，那是已 Kill 的方向）
- **不加具体子方向结论性词**（如 "polarization balanced" 等具体方法名）——子方向留给地勘结果揭示
- **不锁年份下限太严**——经典方法（如 AO 补偿祖师爷）也要，标档级和年份即可

#### 检索源

- `bash tools/search "<query>"`（S2/OpenAlex/SerpAPI/Exa 多源，从项目根目录调）
- `bash tools/blit --source ieee "<query>"`（IEEE 全文下，含 venue 字段）
- 详见 `tools-guide.md` §1-2

#### 跨对话分批

地勘预计 3-5 对话。本对话（PROMPT-001）= 第 1 批，先跑组 1-3（equalization 总览 + 偏振 + MIMO）。后续对话续接跑组 4-6 + 补检索。**每对话 ≤3 步**（AGENTS.md 单对话步数上限）。

### 2.3 产出格式（强制）

产出 `projects/simulation/landscape-equalization.md`（跟 `landscape.md` 平级，专门给均衡层地勘用），**每行一篇论文**，7 字段：

| 字段 | 内容 |
|---|---|
| 子地带 | 偏振均衡 / MIMO 均衡 / ISI 均衡 / AO-DSP 残余补偿 / 湍流信道均衡 / 其他（地勘结果揭示）|
| 做的事 | 方法一句话（中性描述，不评价）|
| **档级** | Trans（JLT/TCOM/TSP/OE/TVT/JPhoton 等）/ Letters（PTL/CL 等）/ 会议（OFC/OECC/SPIE 等）|
| 年份 | YYYY |
| 是否跟湍流强相关 | 是 / 否 / 部分 |
| baseline 是谁 | 该论文对照的方法（一句话，从 abstract 提取）|
| 缝潜力初判 | 🟢有缝潜力 / 🟡不确定 / 🔴死地（饱和）—— **基于 abstract 的粗判，不是判据 A（禁判 baseline 真失效）** |

**🔴死地记忆**：如果某子地带明显饱和（大量论文做同一件事且增益趋同），在表后单独列"🔴死地"段，标子地带名 + 饱和理由 + 代表论文。下次不重复撞墙。

**landscape-equalization.md 头部模板**：
```markdown
# FSO 相干均衡全谱地勘（landscape）

> 创建: YYYY-MM-DD | 专题: 2026-07-10-equalization-layer-direction-scouting
> 阶段: GW Step 1 地勘前置 | 产出供阶段 1.5 选地
> 纪律: abstract 层只找候选清单，禁判判据 A（baseline 真失效）。判缝移全文层。

## 检索覆盖度（诚实标注）
- 检索组数: N
- 检索源: tools/search（S2/OpenAlex/SerpAPI/Exa）+ tools/blit ieee
- 候选论文总数: N
- 子地带覆盖: 列出发现的子地带
- 未覆盖（诚实）: 列出没检索到的角度（如 paywall 锁的 / 工具召回不了的）

## 论文主表

| # | 子地带 | 做的事 | 档级 | 年份 | 跟湍流强相关? | baseline 是谁 | 缝潜力初判 |
|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... | 🟢/🟡/🔴 |

## 🔴 死地记忆（饱和子地带）

### [子地带名]
- 饱和理由：...
- 代表论文：...
```

## 已知陷阱（基于历史失败的具体案例）

### 陷阱 1: abstract 工具错位（S010 教训，最致命）
- **症状**：想用 abstract 判"这个方法 baseline 真失效吗"——abstract 天然报不出（作者吹自己好）
- **避免**：abstract 只提取"做什么 + baseline 是谁 + 档级年份"，缝潜力初判只标 🟢/🟡/🔴 三档粗判（🟢=多方法并存可能竞争 / 🟡=不确定 / 🔴=明显饱和），**不下"baseline 真失效"结论**

### 陷阱 2: 地勘过度轮次（S008-S010 浪费 6 文件）
- **症状**：一轮地勘信号弱就换维度重检索，跑了 4-5 轮
- **避免**：本对话跑组 1-3，下一对话跑组 4-6 + 补检索，**最多 2 轮**（信噪比合格即停）。信噪比合格 = 子地带覆盖 ≥3 个不同 + 候选总数够

### 陷阱 3: 偏回载波同步（本专题红线）
- **症状**：检索词带 synchronization，结果全是载波恢复论文（已 Kill 方向）
- **避免**：检索词不加 synchronization；如果结果混入载波同步论文，标"偏载波同步，排除"不拉进主表

### 陷阱 4: 造假（S011 教训，§7.2 三硬规则）
- **症状**：候选论文没下载却报 line 编号 / 论文立场被扭曲（abstract 说 A 被报成 B）
- **避免**：§7.2 三硬规则——①全文真实性核查（abstract 也要从真实检索结果提取，不编）②论文立场不可扭曲（abstract 明说啥就写啥）③孤证就是孤证（某子地带只有 1 篇，标"孤证"不当主流）

### 陷阱 5: 主对话禁 WebSearch / webReader（AGENTS.md 强制）
- **症状**：主对话直接 WebSearch 灌入大量 HTML 致上下文爆炸
- **避免**：本对话所有检索走 `tools/search` + `tools/blit`（结构化可控）；web 查询必须子 agent 消化返回 ≤500 词摘要

## 验收（主线拿到产出后怎么检查）

阶段 1 地勘产出交回主控对话后，主线检查：
- [ ] `landscape-equalization.md` 存在 + 7 字段齐全 + 档级标注完整
- [ ] 检索覆盖度段诚实（列了未覆盖的）
- [ ] 子地带覆盖 ≥3 个不同（信噪比合格判据）
- [ ] 无载波同步论文混入（偏题检查）
- [ ] §7.2 核查：随机抽 3 篇，核查 abstract 提取是否真实（不编 line/不扭曲立场）
- [ ] 🔴死地记忆段（若有饱和子地带）标了理由 + 代表论文
- [ ] **没有判据 A 结论**（没下"baseline 真失效"判断，只标 🟢/🟡/🔴 粗判）

**验收不过 → 补检索或修造假，不进阶段 1.5 选地**。

## 必读（新对话开始时按优先级读）

1. `.sessions/2026-07-10-equalization-layer-direction-scouting/topic-index.md` —— 20 不变量（重点 INVARIANT 5 地勘前置 / 6 abstract 工具错位 / 7 §7.2 核查 / 18 背景锁死星地）
2. `.sessions/2026-07-10-equalization-layer-direction-scouting/S001-process-review-and-planning.md` —— 流程规划（阶段 1 设计在 §4）
3. `tools-guide.md` §1-2 —— tools/search + tools/blit 用法
4. `.sessions/2026-06-20-problem-driven-redirection/topic-index.md` —— 地勘前置方法论（不变量 5 地勘前置 + landscape.md schema）

## 纪律（和本任务直接相关的约束）

1. **abstract 工具错位（INVARIANT 6）**：地勘 abstract 只找候选清单，禁判判据 A
2. **方法中性检索（INVARIANT 5）**：不锁子方向，关键词不含具体方法名
3. **§7.2 三硬规则（INVARIANT 7）**：全文真实性 / 立场不可扭曲 / 孤证就是孤证 + 主线独立 grep 核查
4. **不偏回载波同步（本专题红线）**：检索词不加 synchronization
5. **主对话禁 WebSearch**：走 tools/search + tools/blit，web 查询子 agent 消化
6. **单对话 ≤3 步**：本对话跑组 1-3，不超发
7. **档级标注（INVARIANT 19）**：每行标 Trans/Letters/会议，供阶段 2 精读分层
8. **颗粒无收好过凑数**：如果某子地带真没论文，标"未召回"不硬凑

## 接口变更（代码改动）

无（地勘不写代码，只产 .md）

## 下一轮

**本对话（阶段 1 第 1 批）产出**：`landscape-equalization.md` 初版（组 1-3 结果）+ 写 S002 session note + H001 交接

**阶段 1 第 2 批（下一对话）**：跑组 4-6 + 补检索 + 信噪比合格判定 → 阶段 1 收尾 → 进阶段 1.5 选地（交主控对话 + 用户拍板）

**不在本对话做**：
- 不精读（阶段 2）
- 不判 Go/Kill（阶段 4）
- 不下"均衡层地有没有缝"结论（阶段 3）
- 不建均衡器代码（基建阶段 5 MVE 后才建）
