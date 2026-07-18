# PROMPT-002: 载波同步 v2 精读沉淀 对话 4（B11/B12 评点 + literature_notes 并入）

> 专题：2026-07-02-carrier-sync-v2-deep-read
> 承接：S005 对话 3（B1-B10 总表 26 Q# 已落盘）
> 对话 4 目标：B11/B12 评点 + literature_notes 载波同步 v2 章节并入 + B1-B12 全 12 点总表最终合并

---

## 直接复制下面的提示词 ↓↓↓

你是载波同步 v2 精读沉淀专题的对话 4。承接 S005（B1-B10 总表 26 Q#）。

## 任务（3 件事，守 3 步上限）
1. B11 NDA-ML STO+CPE 评点（派 1 子 agent，写 `_B11-nda-ml-sto-cpe-increment.md`）
2. B12 频域 pilot 评点（派 1 子 agent，含**用户新下 MAP 全文 150 行**，写 `_B12-freq-domain-pilot-increment.md`）
3. literature_notes 载波同步 v2 章节并入（综合分析 + 研究问题清单，主线写可派子 agent 辅助）+ B1-B12 全 12 点总表最终合并

## 先报到（session-governance Trigger 1+5）
读 topic-index（不变量 9 条）+ H004 + S005 + S004 + S003 + gw-read.md + **templates.md literature_notes 模板（L248/L277/L295）**。报到时 FR-26 主线独立 grep 核查 H004 至少 3 条事实。

## 必读文件
1. `.sessions/2026-07-02-carrier-sync-v2-deep-read/topic-index.md`（不变量 9 条）
2. `.sessions/2026-07-02-carrier-sync-v2-deep-read/H004-conversation4-b11b12-eval-literature-notes.md`
3. `.sessions/2026-07-02-carrier-sync-v2-deep-read/S005-conversation3-b8b9b10-eval.md`（B1-B10 总表 26 Q#）
4. `.sessions/2026-07-02-carrier-sync-v2-deep-read/S004-conversation2-b7-eval-b5-fulltext-summary-table.md`（B1-B7 总表 20 Q#）
5. `stages/gw-read.md`（14 字段+7 项 + 综合分析 + 研究问题清单 [MUST]）
6. `templates.md`（L248 literature_notes 模板 / L277 综合分析 / L295 研究问题清单）
7. `stages/glossary.md`（问题四判据，研究问题清单逐条过）

## 🔴 防偏差纪律（历史踩坑换的，别再犯）
1. **守子 agent 强制委托**——🔴 对话 2 B5 主线自读全文违规已被用户纠偏（"你就派一个 subagent？不是计划至少二十个？"），对话 3 已纠正（3 子 agent 委托率 100%）。**对话 4 B11/B12 评点各派子 agent，主线不碰任何全文，委托率 100%**
2. **守 D018 中性提取**——Q# 只标 D006/D005/范围，禁出现"方向死了/值得做/Go/Kill"判断词。Go/Kill 是用户的，总表阶段排完优先级才做
3. **守 gw-read 14 字段+7 项**——不允许只写 5 字段中性表，第 7 项 M-C-A 必含 ≥1 Q# 或显式标"无 Q# 候选"。M=baseline+行号 / C=条件+参数 / A=不足
4. **守 FR-26 主线 grep 核查**——子 agent 每条声称必主线独立 grep，dB 必溯源原文，不准脑补
5. **守 3 步上限**——超 3 步主动建议分对话
6. **D006 红线 + 范围硬门**——撞 D006 只标不砍，ISL/feeder 出界标状态
7. **复用旧笔记不重写**——B11/B12 旧笔记查复用，写增量段
8. **literature_notes 综合分析必含研究问题清单**（gw-read [MUST]，过 glossary 四判据，未过标 ❌ 说明缺哪条）

## 当前状态（不必重查）
- 全文 46 篇落 v1 量级
- B1-B10 已评点 **26 个 Q#**（B1×2+B2×2+B3×3+B4×3+B5×4+B6×3+B7×3+B8 主判定+2+B9×3+B10×3）
- 撞 D006 明确撞 **0** / 边界 **5**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2）
- D005 倾向够格 **9**（含 B9-Q1 ~3dB 第一梯队）/ 边际够格 **3** / 待定量 **6** / 不够格不适用 **6**
- 范围 out **7** / in 倾向 **18**
- **D005 够格梯度**：第一梯队 B3-Q2 +2~3dB > B9-Q1 ~3dB（baseline 内部对照需注明）> B3-Q1 +0.9dB out > B1-Q1/B2-Q2 +1dB > B5-Q2 7dB penalty out；第二梯队 B7-Q1 0.6dB+范围 / B10-Q1 范围鲁棒性 / B5-Q1 范围覆盖 / B6-Q1 定性保锁
- **D006 边界模式 5 次**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2 都是"前馈/工具层不撞，环路 TF 联合建模则撞"）——潜在一致性研究方向，literature_notes 综合分析时点出
- **B8 特例**："载波同步冗余"（自相干绕过），literature_notes 并入时单独标
- 仍缺：ao.581648（B10-Q3 全文，Optica AO 订阅墙，标待全文核验）
- 用户新下到位：B5（252 行对话 2 用）/ B9 DRE apn.3.3.036007（440 行对话 3 用）/ **B12 MAP oecc-psc62146（150 行对话 4 用）**

## 产出
1. `_B11-nda-ml-sto-cpe-increment.md`（B11 增量笔记 gw-read 14 字段+7 项）
2. `_B12-freq-domain-pilot-increment.md`（B12 增量笔记，含 MAP 全文）
3. literature_notes 载波同步 v2 章节并入（综合分析 5 小节 + 研究问题清单过四判据）
4. B1-B12 全 12 点总表最终合并（26+B11/B12 新 Q#，交用户最终排优先级）
5. S006 + H005（如未完成 Go/Kill 判定交对话 5）
6. 结束 commit 一次 + 更新 topic-index/registry

## 关键提醒
1. **B11 锚极新 cited-by 仅 1**：LPT.2024.3523478（226 行）+ s25164906（边缘），B11 评点靠锚全文 + M-APSK/NDA ML 经典 Wu[11]/Hu[12]
2. **B12 用户新下 MAP 全文 150 行**：oecc-psc62146（MAP Phase Recovery 256-QAM），原 IEEE 订阅墙已解决。B12 锚 TCOMM.2022.3171809（590 行）+ cited-by 3 篇（COMST.2024.3443158 Phase Noise Survey 1288 行 / acp ipoc63121 频域 pilot tone 待核 / oecc-psc62146 已下）
3. **ao.581648 仍缺**：B10-Q3 4dB OSNR gain 仅摘要，对话 4 如用户继续尝试手动下可补，否则标待全文核验
4. **dB 量级参考**：第一梯队 B3-Q2/B9-Q1 +2~3dB；B1/B2 +1dB；B7 0.6dB+范围；B10 无统一 dB（范围鲁棒性）
5. **总表中性**：最终合并不判 Go/Kill，交用户最终排优先级后对前几名判 Go/Kill

一句话纪律：守子 agent 委托（主线不碰全文）+ D018 中性 + gw-read 14 字段+7 项 + FR-26 grep 核查 + 3 步上限 + literature_notes 综合分析必含研究问题清单。
