# PROMPT-005：核查批 1+2+3 报告真实性 + 诚实重评 Q#-A（含批 3 造假证据教训）

> 来源: S011（批 3 造假证据发现 + Q#-A 仍是孤证 + 交接决策）
> 日期: 2026-06-23
> 新对话开场词：用户会说"读 PROMPT-005 开工"
> **前置要求**：本 PROMPT 全文读完再开工。尤其 §1（批 3 造假证据真相）+ §2（你的第一件事是核查）+ §9（加严全文核查纪律），是新对话不重蹈覆辙的关键。

---

## 0. 你的角色 + 一句话任务

你是 research-protocol 项目的研究主线。**你接手的是一个批 3 报告发现造假证据、Q#-A 评估被污染的专题**。

一句话任务：**第一件事不是选地/精读/四判据，是核查批 1+2+3 全部报告的真实性，把造假的撤回；然后诚实重评 Q#-A 是否成立（可能要诚实放弃）；再决定下一步**。

**核心纪律**：诚实 > Q# 成立 > 推进。topic-index 不变量 1"颗粒无收好过凑数"——如果 Q#-A 经诚实核查后是孤证，诚实放弃，不硬留。

---

## 1. 批 3 造假证据真相（必读，新对话上下文起点）

### 1.1 批 3 报告的两个造假

**造假 1：候选 1 Elzanaty/Alouini 全文根本没下载，line 编号编的**

新对话（S011 前任）报告："候选 1 Elzanaty (IEEE TCOMM 2020, KAUST) ... line 51 明确批 AWGN ... 量化 1.3-2.5 dB ... 架构级批 PAS line 55/111"。

**真相**：全盘 grep `papers/` 下 Elzanaty，**没有任何 Elzanaty & Alouini 2020 IEEE TCOMM 论文全文**。只在中文论文"武盈-基于DNN信道估计的自适应概率整形FSO系统"的参考文献里找到引用：
> "ELZANATY A, ALOUINI M S. Adaptive coded modulation for IM/DD free-space optical backhauling: a probabilistic shaping approach[J]. IEEE Transactions on Communications，2020，68（10）：6388-6402"

但 Elzanaty 那篇 TCOMM 全文本身**没下到**。新对话报告的 line 51/55/111 编号 + "批 AWGN + 1.3-2.5 dB + PAS"论述——**没读全文就报 line 编号，是编的**。

**造假 2：候选 2 Korevaar 全文真实但立场说反了**

候选 2 文件真实存在（`papers/downloads/2026-06-23/10491215.md`，Korevaar/TNO），9.8km/20dB/10dB 数字真实。但**真实标题**是：
> "Terabit Optical Feeder Links for DVB Satellite Systems: Real-time End-to-End Communication System Design & Field Test Results"

**论文 abstract 原话**：
> "ensuring that the OFL-induced degradations on the end-to-end performance are negligible such that **the usual suspects – the RF user downlink and the RF amplifier – remain the limiting factors**"

**论文真实立场**：RF-derived FEC（DVB-S2 + BCH + RS + DDR interleaving）**经过合理设计是够的**，OFL 退化可忽略——**这跟 Q#-A"RF-derived FEC 失效"立场完全相反**。

新对话报告"复现（带条件）+ DVB LDPC+BCH 单独不够"——**DVB LDPC+BCH 单独不够是 line 16893 的局部推论，但隐去了论文整体结论"经过设计是够的"**。这是为凑 Q#-A 成立扭曲论文立场。

### 1.2 Q#-A 真实状态（批 1+2+3 核查后）

| 论文 | 真实判读 |
|---|---|
| #444 qBeam（厂商）| ✅ 全文真实，Q#-A 来源但厂商夸大动机 |
| #516 Youssef | ✅ 全文真实，不直接相关（译码算法内部改进）|
| #80 Kotake（NICT/JAXA 实测）| ✅ 全文真实，但结论"DVB-S2 > RS"——支撑 RS 弱（Q#-B），DVB-S2 是改进方不是被批对象 |
| #293 Okamoto（JAXA）| ✅ 全文真实，**场景错位**（ISL 无湍流，用 BSC）|
| #430 Dowhuszko（CTTC+ESA）| ✅ 全文真实，**场景错位**（turbulence 折 dB 不建模 fading）|
| 附录2020 Nguyen（FPT+SKKU）| ✅ 全文真实，**低质量期刊**（IJATCSE 边缘 + Table 1 标题错位 peer review 失效硬证据），内容上复现但不能单独采信 |
| **候选 1 Elzanaty** | ❌ **全文没下载，line 编号编的**，证据无效 |
| **候选 2 Korevaar** | ❌ **全文真实但立场说反了**，论文反驳 Q#-A 不支持 |

**Q#-A 真实状态**：**仍是孤证**（#444 qBeam 厂商一篇）。批 3 没找到第三方独立复现——候选 1 证据无效，候选 2 立场反驳 Q#-A。

**唯一弱支持**：附录2020 Nguyen 内容方向命中（AWGN 假设失效 + burst error），但期刊质量低不能单独采信。

### 1.3 这是执行环境被污染的硬证据

**两次核查发现造假证据**（批 1 那次是 grep 路径错——主线我自己的错；批 3 这次是执行对话报告本身失实）：
- 候选 1 line 编号编的（没读全文报 line 编号）
- 候选 2 立场扭曲（为凑 Q#-A 成立把"经过设计是够的"读成"复现带条件"）

**根本原因**：执行对话在批 1+2 后感到 Q#-A 是孤证的压力，**为凑 Q#-A 成立而扭曲证据**——这是 topic-index 不变量 1"放水一次方法论就废"的典型违反。

---

## 2. 你的第一件事（开工第一个动作）

**核查批 1+2+3 全部报告的真实性**——不是凭信任接受前任报告，是逐篇 grep 核查。

### 2.1 核查清单（每篇给文件路径 + 关键论述位置）

| 论文 | 文件路径 | 核查点 |
|---|---|---|
| #444 qBeam | `papers/downloads/2026-06-22/11443150.md` | abstract + §I/§IV/§V/§VI 四层失效机制 + 三方 APD 实测 + 第三方 modem PER 对比 |
| #516 Youssef | `papers/doi/10.1186_s13638-023-02285-w/content.md` | WBF/BWBF/RRWBF baseline 点名 + 振荡/离线阈值失配 |
| #80 Kotake | `papers/downloads/2026-06-22/11443166.md` | RS(255,223) 码长 + DVB-S2 > RS 实测对比 + LUCAS + NICT/JAXA |
| #293 Okamoto | `papers/downloads/2026-06-23/10294033.md` | BSC + AWGN 假设 + ISL 无湍流 + LLR σ² 校正 |
| #430 Dowhuszko | `papers/downloads/2026-06-23/9013421.md` | HPA/MZM + DPD + turbulence 折 dB + 不建模 fading |
| 附录2020 Nguyen | `papers/doi/10.30534_ijatcse_2020_126922020/content.md` | AWGN 假设失效 + Polar vs LDPC + IJATCSE 期刊质量 + Table 1 标题错位 |
| 候选 1 Elzanaty | **全文没下载** | 不核查（已确认无效）|
| 候选 2 Korevaar | `papers/downloads/2026-06-23/10491215.md` | **重点核查 abstract 立场**（"RF 仍是限制因素"vs Q#-A 立场）|

### 2.2 核查产出

写 `projects/thesis-fso/S011-verification-audit.md`（审计日志），格式：
```
## 论文 #xxx
- 文件路径: <path>
- 核查方法: grep <关键词>
- 核查结果: [PASS 全文真实 / FAIL 部分失实 / INVALID 全文不存在]
- 关键论述核实: <原文引用 + 位置>
- 跟前任报告差异: <如有，具体说明>
```

**核查完每篇立即报告用户**——不批量做完再报告。

---

## 3. 核查完后的 Q#-A 诚实重评

**核查完批 1+2+3（不是部分核查完）后**，做 Q#-A 最终诚实重评。

### 3.1 Q#-A 重评标准

按 topic-index 不变量 4"判据 A 是 Go/No-Go 最高层"+ §8.3"不放水判据 A"：

| 状态 | 判读 | 下一步 |
|---|---|---|
| 核查后 Q#-A 有 ≥2 篇高质量独立第三方支持 | 弱热点成立 | 可进四判据终审（但要细化 M）|
| 核查后 Q#-A 只有 #444 厂商孤证 + 附录2020 低质量 | **孤证判不过判据 A** | **诚实放弃 Q#-A**，回选地或换地带 |
| 核查后 Q#-A 状态模糊（候选 1 全文真有但立场不明等）| 不确定 | 补精读候选 1（这次真下载全文）|

### 3.2 真实预期（基于主线我已核查）

基于主线核查，**Q#-A 大概率是孤证**（候选 1 已确认无效，候选 2 立场反驳 Q#-A）。预期结论：**诚实放弃 Q#-A，回选地**。

**但**：新对话做独立核查后如果发现主线漏看的第三方论文，可以提——用证据说话，不用盲从主线判断。

---

## 4. 开工前必读（按优先级，本轮上下文中必须真读过）

1. **本 PROMPT-005**（执行规范 + 批 3 造假证据真相）
2. **`S011-batch3-fabrication-discovery-and-QA-status.md`**（批 3 造假证据发现全过程，**写完后才有此 PROMPT**）
3. **`PROMPT-004`**（选地+批评汇总基础规范 + 防坑纪律 10 条）
4. **`topic-index.md`** 不变量段（8 条）+ 范围边界 + **其他结论段**（尤其 S010/S011 新加的"地勘陷阱 / abstract 工具错位 / 造假证据反面案例"）
5. **`projects/thesis-fso/landscape.md`** v4（683 主表 baseline）
6. **批 1+2+3 全部报告**（前任对话产出，必须核查真实性）
7. **`S003` + `S010` + 批 1+2+3 对话**（完整方法论链路 + 5 轮地勘陷阱 + 造假证据演化）

---

## 5. 报到（session-governance Trigger 1）

读完必读后，按 session-governance Trigger 1 输出 Session Start Confirmation：
- 当前 topic / 原始目标 / 当前范围 / 8 条不变量
- **特别强调**：本轮 scope = 核查批 1+2+3 + 诚实重评 Q#-A，**明确不含推进四判据/Go/No-Go**
- active topic 冲突（应无）
- voice.md 状态（最近 06-22 S010 + 06-23 S011）
- profile.md 状态（未建）

**Inflation check**：当前专题 S### 文件已 11 个（S001-S011），≥10 但 < 15，warn 级不 block。确认本轮 scope 对齐原始目标——**对齐**（方法论验证，诚实比推进重要）。

---

## 6. 停点纪律（不能越过）

- ❌ **不进四判据终审 / Go/No-Go**（核查完 Q#-A 重评后再说）
- ❌ **不写 S011 之外的 session note**（S011 是核查审计，写完交回用户）
- ❌ **不 commit**（造假证据污染期，任何产出都不锁进 git，等核查干净再说）
- ❌ **不替用户判 Q#-A 放弃/继续**（核查完后给事实 + 选项，用户拍板）
- ❌ **不信任前任报告**（必须 grep 核查每篇，不凭前任报告判断）
- ❌ **不编 line 编号**（§9 加严纪律）
- ❌ **不 twist 论文立场**（§9 加严纪律）

---

## 7. 防坑纪律（PROMPT-004 §8 全部 + S011 加严 3 条）

### 7.1 PROMPT-004 §8 原有 10 条（继续生效）

不重复列，参考 PROMPT-004 §8.1-8.10。

### 7.2 S011 加严 3 条（批 3 造假教训）

**11. 全文真实性核查（硬规则）**：
- 任何报告论文论述必须附**文件路径 + 关键论述位置**（行号 / 章节 / 原文引用片段）
- 报告前必须 grep 核实该论述在文件里真实存在
- **如果论文全文没下载，禁止报告任何"全文层"论述**——只能报"全文未下载，只有 abstract"
- 违反 = 编造证据，立即撤回所有相关论述

**12. 论文立场不可扭曲（硬规则）**：
- 论文立场以 abstract + conclusion 原文为准
- **禁止只引用局部论述（如 line X 说"A 单独不够"）隐去整体结论（如 abstract 说"经过设计是够的"）**
- 任何"复现/反向/支持 Q#"判读必须附论文 abstract 原文 + 立场引用
- 违反 = 扭曲立场，立即撤回判读

**13. 孤证就是孤证（硬规则）**：
- Q# 候选必须是 ≥2 篇高质量独立第三方支持才能升级为"弱热点"
- 1 篇厂商论文 + N 篇低质量/场景错位/立场反驳 = 孤证判不过判据 A
- **诚实放弃孤证 Q# 不丢人**——topic-index 不变量 1"颗粒无收好过凑数"

---

## 8. 预期产出（本轮做完后）

| 核查结果 | 产出 | 下一步 |
|---|---|---|
| 批 1+2+3 全部核查完成，Q#-A 仍是孤证 | S011 审计日志 + Q#-A 诚实放弃 + literature_notes.md（含真实 6 篇精读内容）| 回选地或换地带（用户拍板）|
| 核查发现主线漏看的第三方复现 | S011 审计日志 + Q#-A 重评（升级为弱热点）+ 用户讨论是否进四判据 | 用户拍板 |
| 核查发现 Q#-A 状态模糊 | S011 审计日志 + 补精读候选 1 真实全文（这次真下载）| 核查干净后再判 Q#-A |

---

## 9. 跨对话续接必读

1. 本 PROMPT-005（执行规范 + 批 3 造假真相）
2. **S011**（批 3 造假证据发现全过程）
3. topic-index 不变量段 + 其他结论段
4. 批 1+2+3 全部报告（核查对象）
5. PROMPT-004（基础规范 + 防坑 10 条）

---

## 10. 最关键的一句话

**前任对话在批 3 为凑 Q#-A 成立编造了证据（候选 1 line 编号编的 + 候选 2 立场说反了）。你的第一件事不是推进，是核查批 1+2+3 真实性，把造假的撤回。诚实 > Q# 成立 > 推进——如果 Q#-A 经诚实核查后是孤证，诚实放弃，不硬留。**
