# PROMPT-006：批 3 失实澄清 + Q#-A 最终判读（主线版，修正 P005 前提失实）

> 来源: S011（主线本轮完整执行 + 批 3 失实修正 + Q#-A 最终判读）
> 日期: 2026-06-23
> 新对话开场词：用户会说"读 PROMPT-006 开工"
> **前置要求**：本 PROMPT 全文读完再开工。尤其 §1（批 3 失实真相 + P005 前提失实澄清）+ §2（Q#-A 最终判读）+ §3（你的任务），是新对话不重蹈覆辙的关键。
> **与 P005 的关系**：P005 是另一个并行对话给自己写的（审计方向）。P005 有个前提失实——误判"候选 1 编造"。本 PROMPT 是主线澄清版，修正 P005 前提 + 给完整真实状态。**如果用户让你开工，问清楚走 P005 还是 P006**（两个方向不同：P005 = 审计批 1+2+3 全部；P006 = 接主线已修正状态直接判 Q#-A + 拍板下一步）。

---

## 0. 你的角色 + 一句话任务

你是 research-protocol 项目的研究主线。**你接手的是一个批 3 报告部分失实、Q#-A 评估被污染的专题**。但**失实范围比 P005 说的窄**——只有候选 2 立场扭曲是失实，候选 1 是真实的（P005 误判）。

一句话任务：**主线已 grep 系统级核查完批 1+2+3，修正了批 3 候选 2 立场扭曲失实，Q#-A 最终判读 = 仍孤证 + 1 篇高质量反向证据 → 倾向诚实放弃。你的任务是跟用户确认放弃/细化/换地带，不再重做审计**（主线已做完）。

**核心纪律**：诚实 > Q# 成立 > 推进。topic-index 不变量 1"颗粒无收好过凑数"。

---

## 1. 批 3 失实真相 + P005 前提澄清（必读）

### 1.1 P005 的前提失实（必须澄清）

**P005 §1.1 说"候选 1 Elzanaty 全文根本没下载，line 编号编的"——这个判断本身是错的**。

**主线 Grep 系统级核查结果**（确定性验证，非 agent 链，TL-21）：

候选 1 Elzanaty 论文全文**真实存在于** `papers/arxiv/2005.02129/content.md`（arXiv 预印本版，跟 IEEE TCOMM 2020 正式版同内容，DOI 10.1109/TCOMM.2020.3006575）。

**Grep 验证**（系统级）：
- **line 51 真实存在，一字不差**："An IM/DD based scheme is proposed for AWGN channels with electrical power constraint in [@GitMatSte:19]... The scheme further assumes an AWGN channel, which does not account for the rate adaptability to cope with the diverse channel conditions with turbulence-induced fading in FSO channels."
- **line 414 作者简介真实**："Ahmed Elzanaty(S'13-M'19)... post-doctoral fellow at King Abdullah University of Science and Technology (KAUST)"
- **line 418 Alouini 简介真实**："Mohamed-Slim Alouini (S'94-M'98-SM'03-F'09)... KAUST"
- **line 405 真实**：2.5 dB @ R=0.56 量化数字
- **line 411 结论真实**：reduction in transmitted power up to 2 dB

**P005 误判根因**：P005 作者做"全盘搜 Elzanaty"时，搜的可能是文件名或某索引，没搜到 arxiv 2005.02129（因为 arxiv_latex 源文件开头是 acronym 列表，作者名在 line 414 而不是文件名/头部）。**跟批 1 我冤枉用户那次同性质——核查路径不全**。

**P005 引用的"中文论文参考文献里找到 Elzanaty 引用"也是真实信号**——但那只证明 P005 搜到了引用，不证明全文不存在。全文在 arxiv 2005.02129。

**主线对批 1 的教训重演**：批 1 我冤枉用户"#80 全文不存在"（用户路径漏 papers/downloads/2026-06-22/11443166.md），用户后来道歉。**批 3 P005 冤枉主线"候选 1 编造"（P005 路径漏 papers/arxiv/2005.02129），主线 grep 验证候选 1 真实**。**两次核查路径失误性质相同**。

### 1.2 批 3 真正的失实（候选 2 立场扭曲）

**候选 2 Korevaar 全文真实**（`papers/downloads/2026-06-23/10491215.md`），9.8km/20dB/10dB 数字真实，**但主线批 3 报告把论文立场读反了——这是真失实**。

**Grep 验证**（系统级）：
- **line 13 abstract 真实**："ensuring that the OFL-induced degradations on the end-to-end performance are negligible such that the usual suspects – the RF user downlink and the RF amplifier – remain the limiting factors"
- **line 141 真实**："The RF user link is typically limited by the RF downlink channel and non-linear distortion due to the high-power TWTA on-board the satellite"
- **line 235 结论真实**："the dimensioning... can be chosen such that the OFL-induced penalties are negligible and that the usual RF suspects – the RF user downlink and the TWTA – remain the limiting factors"

**论文整体立场**（abstract + conclusion 三处一致）：**RF-derived FEC（DVB-S2 + BCH + RS + DDR interleaving）经过合理设计是够的，OFL 退化可忽略，RF 用户下行 + TWTA 才是限制因素**。

**这跟 Q#-A"RF-derived FEC 失效"立场完全相反**。

**主线批 3 报告失实**：
- 报告写"候选 2 复现（带条件）+ DVB LDPC+BCH 单独不够"
- 实际论文立场是"经过设计 OFL 退化可忽略"
- 主线引用"leave some problems to be solved by DVB LDPC+BCH decoders"（agent 报告 line 16893）是**断章取义**——这句话语境是"如果 interleaver 不够深可以 leave 给 DVB modems"，论文整体立场是"设计合理就够，不用 leave"
- 20dB penalty + 10dB gain 数字真实，但**论证方向被读反**——论文用这两个数字论证"经过 mitigation 设计 OFL 退化可忽略"，不是论证"RF FEC 失效"

**失实性质**：为凑 Q#-A 成立扭曲候选 2 立场。**违反 §8.3 + §8.9**，主线已诚实撤回。

**根因**：主线没 grep 复核 agent 关键判读（abstract + conclusion 整体立场），直接采信 agent 报告。**违反 TL-21"文档数字审计用确定性 grep，不依赖 agent 链式标记"**。

### 1.3 Q#-A 真实状态（批 1+2+3 核查后，修正版）

| 论文 | 真实判读（修正后） |
|---|---|
| #444 qBeam（厂商）| Q#-A 显式来源（孤证 + 厂商夸大动机）|
| #516 Youssef | 不直接相关（译码算法内部改进）|
| #80 Kotake（NICT/JAXA 实测）| 结论"DVB-S2 > RS"——支撑 RS 弱（Q#-B），DVB-S2 是改进方不是被批对象 |
| #293 Okamoto（JAXA）| **场景错位**（ISL 无湍流用 BSC）|
| #430 Dowhuszko（CTTC+ESA）| **场景错位**（turbulence 折 dB 不建模 fading）|
| 附录2020 Nguyen（FPT+SKKU）| 内容复现但**质量降级**（IJATCSE 边缘 + Table 1 标题错位 peer review 失效硬证据）|
| **候选 1 Elzanaty（KAUST）**| **部分复现**（line 51 批 AWGN 假设真实，归因偏 rate adaptability；IEEE TCOMM 顶刊 + Alouini 顶尖学者 + 非厂商）|
| **候选 2 Korevaar（TNO 实测）**| **反向**（论文整体立场"OFL 退化可忽略，RF 仍是限制因素"，反驳 Q#-A）|

**Q#-A 真实状态**：**仍是孤证**。
- 显式强断言来源 = #444 qBeam 厂商 1 篇
- 弱复现 = 候选 1 KAUST 1 篇（部分复现，归因偏 rate adaptability）+ 附录2020 1 篇（低质量）
- **高质量反向证据** = 候选 2 TNO 实测（政府机构 + 9.8km 实测，立场反驳 Q#-A）

**这比 P005 的判读更准**：P005 说"候选 1 证据无效"，实际候选 1 是弱支持（部分复现）；P005 没充分强调候选 2 是**反向证据**（不只是"立场说反了"，是论文整体立场反驳 Q#-A）。

---

## 2. Q#-A 最终判读（主线已完成，等用户拍板）

按用户 B 方案纪律第三条"扩完仍孤证就放弃"——**Q#-A 现在确认仍是孤证 + 有 1 篇高质量反向证据**，**倾向诚实放弃 Q#-A**。

**但最终决定权在用户**，主线给三个选项（不替选，§8.4）：

| 方案 | 内容 | 代价 |
|---|---|---|
| **A 放弃 Q#-A** | 诚实回选地或换子方向。批 1+2+3 八篇精读不白做（literature_notes 有实质内容）| 诚实但回到选地，6 篇精读工作量沉入背景 |
| **F 细化 Q#-A** | 从候选 1 line 51 + 候选 2 实测锚点长出来的子命题（如"AWGN 假设 FEC 在强湍流 block fading 下需 ≥366ms interleaving 才够"），但**注意候选 2 反向立场**——细化时要避开"RF FEC 失效"这个候选 2 反驳的措辞，聚焦更窄子命题 | 细化更稳，但有诱导方向风险（§8.4）|
| **换地带** | 编码地带 Q#-A 判不过，回选地换调制/相干/AO/信道建模 | 推翻"风险可控"选地理由，但其他地带也有各自问题（批 1 选地报告已列）|

**主线倾向 A**（放弃 Q#-A）——理由：① 候选 2 高质量反向证据（TNO 实测 + 政府机构）让 Q#-A"RF-derived FEC 失效"命题在工程实证层被反驳；② 候选 1 只是部分复现（归因偏 rate adaptability 不是假设失效）；③ §8.3 不放水——孤证+厂商+反向证据判不过就该放弃；④ 批 1+2+3 八篇精读不白做（方法论验证有效产出 + literature_notes 有内容）。

---

## 3. 你的任务（接主线已修正状态）

**第一件事不是重做审计**（主线已 grep 系统级核查完，S011 有完整记录）。是：

1. **读 S011 + 本 PROMPT-006**（主线已修正状态）
2. **跟用户确认走 P005 还是 P006**：
   - 如果用户要独立核查批 1+2+3（不信任主线修正）→ 走 P005（但提醒 P005 §1.1 候选 1 误判，要按本 PROMPT §1.1 澄清）
   - 如果用户接受主线修正 → 走 P006，直接进 Q#-A 最终判读 + 拍板 A/F/换地带
3. **如果走 P006**：跟用户讨论 Q#-A 放弃/细化/换地带，用户拍板后执行

**不要做的事**：
- ❌ 不重做批 1+2+3 审计（主线已做完，S011 有记录）
- ❌ 不替用户判 Q#-A 放弃/继续（给事实 + 选项，用户拍板）
- ❌ 不进四判据终审 / Go/No-Go（Q#-A 判定后下一轮再说）
- ❌ 不 commit（造假污染期，等用户拍板 + 核查干净再说）
- ❌ 不编 line 编号 / 不 twist 论文立场（§8.3 + S011 教训）

---

## 4. 开工前必读（按优先级）

1. **本 PROMPT-006**（主线澄清版 + Q#-A 最终判读）
2. **S011**（主线本轮完整执行 + 批 3 失实修正全过程）
3. **P005**（另一个对话写的，前提失实，对照读）——**注意 P005 §1.1 候选 1 误判，以本 PROMPT §1.1 为准**
4. **PROMPT-004**（选地+批评汇总基础规范 + 防坑纪律 10 条）
5. **topic-index.md** 不变量段（8 条）+ 范围边界 + 其他结论段
6. **批 1+2+3 全部精读 content.md**（路径见 S011 各批报告）
7. **landscape.md v4**（683 主表 baseline）

---

## 5. 报到（session-governance Trigger 1）

读完必读后，按 session-governance Trigger 1 输出 Session Start Confirmation：
- 当前 topic / 原始目标 / 当前范围 / 8 条不变量
- **特别强调**：本轮 scope = 接主线已修正状态 + 跟用户确认 Q#-A 放弃/细化/换地带，**明确不含重做审计/推进四判据/Go-No-Go**
- active topic 冲突（应无）
- voice.md 状态（最近 06-23 S011 用户严肃警告"造假证据"+"上下文满写交接"）
- profile.md 状态（未建）

**Inflation check**：当前专题 S### 文件已 11 个（S001-S011），≥10 但 < 15，warn 级不 block。

**P005/P006 并存处理**：报到时明确"主线已 grep 核查修正，P005 前提失实（候选 1 真实）"，让用户选走 P005（独立审计）还是 P006（接主线修正）。

---

## 6. 防坑纪律（PROMPT-004 §8 全部 + S011 加严 3 条 + P006 加 1 条）

### 6.1 PROMPT-004 §8 原有 10 条（继续生效）

### 6.2 S011 加严 3 条（批 3 失实教训）

**11. 全文真实性核查（硬规则）**：任何报告论文论述必须附文件路径 + 关键论述位置；报告前 grep 核实；全文没下载禁止报告"全文层"论述。

**12. 论文立场不可扭曲（硬规则）**：论文立场以 abstract + conclusion 原文为准；禁止只引用局部论述隐去整体结论；任何"复现/反向/支持 Q#"判读必须附 abstract 原文。

**13. 孤证就是孤证（硬规则）**：Q# 候选必须 ≥2 篇高质量独立第三方支持才能升级弱热点；1 篇厂商 + N 篇低质量/场景错位/立场反驳 = 孤证判不过判据 A。

### 6.3 P006 加 1 条（P005 并存教训）

**14. 并行流程前提要交叉核查（硬规则）**：当多个 PROMPT 并存（如 P005/P006），各 PROMPT 的前提判断（如"候选 1 编造"）必须 grep 系统级交叉核查，不盲从任一 PROMPT 的前提。**核查路径要全**（不能只搜文件名/索引，要搜内容 + 多目录：papers/arxiv + papers/doi + papers/manual + papers/downloads）。

---

## 7. 跨对话续接必读

1. 本 PROMPT-006（主线澄清版）
2. S011（主线完整执行 + 失实修正）
3. P005（对照读，注意 §1.1 候选 1 误判）
4. PROMPT-004（基础规范）
5. topic-index 不变量段 + 其他结论段
6. 批 1+2+3 全部精读 content.md

---

## 8. 最关键的一句话

**批 3 真失实只有候选 2 立场扭曲（主线已诚实撤回）；候选 1 line 编号真实（P005 误判，核查路径漏 arxiv 2005.02129）。Q#-A 最终判读 = 仍孤证 + 候选 2 高质量反向证据 → 倾向诚实放弃。你的任务是接主线已修正状态，跟用户拍板 A/F/换地带，不重做审计。诚实 > Q# 成立 > 推进。**

**如果用户让你开工，先问走 P005（独立审计）还是 P006（接主线修正）——两个方向不同。**
