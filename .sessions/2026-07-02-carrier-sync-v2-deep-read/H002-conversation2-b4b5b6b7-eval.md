# Handoff: 对话 2——B4/B5/B6/B7 评点 + B4/B6 cited-by 验证表

> 来源: S003 | 交接目标: 对话 2 评 B4/B5/B6/B7 四点 + B4/B6 补 cited-by 验证表
> 日期: 2026-07-03
> 文件名: H002-conversation2-b4b5b6b7-eval.md

## 到哪了（状态）

对话 1（S003）完成 v1 量级补料 + B1/B2/B3 评点。**本轮守 3 步上限用满**（补下 + 评点 + 写交接），B4-B7 交对话 2。

**补下收获（步骤 0）**：
- **8 篇新下成功**（IEEE 5 + IEICE/Chinese Opt Lett/OE 综述 3）
- **5 篇付费墙失败**（ol.42.002173 / ao.57.007915 / tcom.1974.1092337 / ao.434807 / lpt.2025.3644328）
- 当前全文 ~36 篇 + 3 篇摘要 = 39 篇，加用户手动下 6 篇付费墙 = 45 篇，**v1 量级 40-50 达成**
- **关键事实修正**：Optica JS 挑战分两类——真 OA（OE Vol.16）可抓直链，订阅论文（OL/AO 近年）被 Radware CAPTCHA 拦。OSAC 先例成功是因本身 OA，非 Playwright 能破订阅墙

**B1/B2/B3 评点收获（步骤 1）**：
- **7 个 Q# 候选**（B1×2 + B2×2 + B3×3），全部标注 D006/D005/范围
- **撞 D006：0 个**；**D005 倾向够格：4 个**（B1-Q1/B2-Q2/B3-Q1/B3-Q2）；**风险偏高/不够格：3 个**（B1-Q2/B2-Q1/B3-Q3）；**范围 out：1 个**（B3-Q1 光纤 DSCM）
- **sat.1553 L70 D006 复核结论**：H001 提示的"L70 撞 D006"**不是误判**——L70"湍流相位作为 pilot 先验"= 同物理假设第三种数学工具（前馈 Bayesian），撞 D006。已加注归档（不删原文，守 D018 中性）
- **三份增量笔记**：`papers/_read_notes/_B1-pilot-window-increment.md`（73 行）/ `_B2-deep-fade-freeze-increment.md`（76 行）/ `_B3-subsystem-coordination-increment.md`（101 行）
- **意外发现**：LCOMM.2026.3651445 在 B3 视角下高贴合 sat.1553 L790（一套 FPT 跨 FOE/CPE/RSOP 三子模块），原 A3 视角被低估——但场景是光纤 DSCM 非星地（B3-Q1 标 out 待迁移论证）

## 下一步干什么

**新对话打开后**（对话 2 = B4/B5/B6/B7 四点评点 + B4/B6 cited-by 验证表）：

### 步骤 1：报到（Trigger 1+5）
读 topic-index（不变量 9 条）+ S001 v2 + S002（cited-by 池+下载状态）+ **S003**（本轮 B1/B2/B3 评点 + 补下状态 + Q# 候选 7 个）+ 本 H002 + gw-read.md + 原专题 H020

### 步骤 2：B4/B5/B6/B7 评点（全文/素材齐后）

**素材盘点**：
- **B4 双反馈环**：Paillier 池 43（S003 §0.4 主线已列新增候选含 jlt.2023.3281082 / TWC.2026.3659523 / JLT.2025.3578005）+ Paillier 主线笔记 `papers/_read_notes/10.1016_j.optcom.2023.129312.md` + sat.1553 旧笔记
- **B5 短时谱粗频偏**：B5 全文失败（穷尽 11 源），靠 sat.1553 L558/L582 + [60]Leven（本轮有笔记素材）+ Paillier 池 + jlt.2023.3281082（S003 §0.4 新筛，数字域 Doppler 补偿 LEO FSO）评点，标"待全文"
- **B6 Z-ODPLL**：本轮素材大补——新下 5 篇 backward refs（Gardner TED 1986 / Pilot-Carrier LEO OPLL 2012 / OISL 2023 / MWP OPLL 2022 / Kazovsky 1992）+ 3 篇 OPLL（IEICE Z-domain Z-ODPLL 根基 / col202018 混合 OPLL / OE 2008 OPLL 综述）+ 已有 ofc.2026.w2a.62 + photonics10121312 旧笔记
- **B7 Gardner TED**：ofc.2026.w2a.62 backward 5 篇（含 Gardner TED 1986 原文）+ B7 锚笔记已有

**建议拆 2 子 agent 并发**（守 ≤3 并发 + ≤15 分钟）：
- 子 agent A：B4 + B5 合并（Paillier 池共用，B5 标"待全文"）
- 子 agent B：B6 + B7 合并（Gardner TED 1986 共用，B6 素材大补 B7 用 backward refs）

**每份笔记 gw-read 14 字段+7 项含 M-C-A**，每个 Q# 标"撞/不撞 D006"+"D005 够格判定"+"范围状态"。

### 步骤 3：B4/B6 补 cited-by 验证表（不重读全文）

- B4 用 S002 §2.2 候选 + S003 §0.4 新筛 Paillier 池候选
- B6 用 S002 §2.2 候选 + S003 §0.1 backward refs（Gardner TED 1986 / Z-domain OPLL 等）

### 步骤 4：主线 grep 核查 + 复用旧笔记删/标撞 D006 段

### 步骤 5：本轮不判 Go/Kill（D018 中性提取）

**产出**：B4/B5/B6/B7 各 1 份 gw-read 增量笔记（14 字段+7 项含 M-C-A）+ B4/B6 cited-by 验证表 + 每点 ≤5 篇支撑表

**守 3 步上限提醒**：步骤 1 报到 + 步骤 2 评点 + 步骤 3 cited-by 验证表 + 步骤 4-5 核查收尾会超 3 步。建议对话 2 先只做 B4/B5/B6/B7 评点（步骤 1-2-4-5 合并为评点阶段），B4/B6 cited-by 验证表（步骤 3）如时间紧交对话 3 头部。

## 纪律（和下一步直接相关的约束）

1. **🔴 gw-read 14 字段 + 7 项结构化提取是硬要求**（B6 范例 84 行 + S003 B3 范例 101 行）：不允许只写 5 字段中性表——本轮继续补 D017 步骤 4 + gw-read 沉淀
2. **🔴 每篇笔记第 7 项"问题提取"含 ≥1 个 M-C-A 候选 或 显式标"本篇无 Q# 候选"**——S003 已有 7 个 Q# 范例（B1-Q1/Q2/B2-Q1/Q2/B3-Q1/Q2/Q3），照格式写
3. **🔴 守 D018 中性提取**：笔记写 M-C-A 问题提取但不判 Go/Kill（S003 守住，对话 2 继续）
4. **🔴 D006 红线 + 范围硬门保留**：笔记 M-C-A 提取时标撞/不撞（只标不砍）；B3-Q1 光纤 DSCM 标 out 是范例
5. **守 3 步上限**（profile 第 6 次验证防线）：对话 2 ≤3 步
6. **子 agent ≤15 分钟**：B4+B5 合并 1 子 agent + B6+B7 合并 1 子 agent 并发
7. **主线 grep 核查每条关键声称**（§7.2，S003 已范例：核查 4 组磁盘证据全 PASS）
8. **D005 务实路线**：笔记 Q# 候选按 D005 标准（赢传统 baseline 几 dB），不预设严苛"真缝"
9. **B5 全文失败不脑补**：标"待全文"，靠 sat.1553 + [60]Leven + Paillier 池 + jlt.2023.3281082 评点

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| **B5 Elsevier paywall 全文失败**（穷尽 11 源）| 判读层需全文 | optcom.2024.130981 仅 metadata.json | 对话 2 评 B5 时标"待全文"，靠 sat.1553 L558/L582 + [60]Leven + Paillier 池 + jlt.2023.3281082 评点；或机构 VPN/邮件作者 Jiamin Fan（青岛大学）|
| **5 篇付费墙未下**（ol.42.002173 / ao.57.007915 / tcom.1974.1092337 / ao.434807 / lpt.2025.3644328）| B6/D5 全文 | 本轮穷尽失败 | 对话 2 B6 评点靠 IEICE Z-domain + col202018 + OE 2008 替代；D5 候选标"待全文"|
| **Gardner TED 1986 + Kazovsky 1992 转换质量差**（扫描 PDF md 14/26 行正文不可检索）| B7/B6 理论锚需读正文 | PDF 有但 md 占位符 | 如必须读正文用 docling/MinerU VLM OCR；或直接读 PDF 图像；**对话 2 评 B7/B6 时这两篇理论锚已知核心结论（Gardner TED 算法/Kazovsky QPSK 联合建模），可不重读全文**|
| **Optica JS 挑战订阅墙不可破**（OL/AO 近年）| OL/AO 候选全文 | Playwright 仅对真 OA 有效 | 用户手动下或馆际互借 |
| **[79] Matsuda SPIE 仅摘要**（穷尽 7 源）| B2 增量核验需全文 | 10.1117/12.2544050 仅 abstract | **摘要已坐实 sat.1553 L582 FO 估计器冻结机制**（S003 对话 1 评 B2 够用）；正文图表走馆际互借 |
| B10/B11/B12 图表数值 fast md 占位符 | 笔记量化段需读图 | 未处理（可后置） | 对话 3（B8-B10）/ 对话 2（B11/B12）涉及前用 `tools/convert --quality standard` 重转 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（9 条，D018 中性提取 + D006 红线 + 范围硬门 + D005 务实路线 + 3 步上限）
- [ ] 已验证本文件至少 3 条关键事实声称（建议验证：①S003 §0.1 磁盘核查 8 篇新下状态 ②S003 §1.2-1.4 三份增量笔记 Q# 候选真实存在 ③S003 §1.1 sat.1553 L70 D006 加注真实写入）
- [ ] 已检查 _registry.yaml depends_on（2026-06-20-problem-driven-redirection）和 conflicts_with（none）
- [ ] 已确认范围未违反"明确不含"（不判 Go/Kill / 不预设 Q# / 不改框架 / 不出星地激光通信大背景）

## 接口变更（如有代码改动）

无代码改动。

## 下一轮

**对话 2 执行（本轮 handoff 后）**：
1. 报到（读 topic-index/S001 v2/S002/S003/本 H002/gw-read.md/原专题 H020）
2. B4/B5/B6/B7 评点（派 2 子 agent 并发：B4+B5 合并 + B6+B7 合并，各写 gw-read 增量笔记 14 字段+7 项含 M-C-A）
3. B4/B6 补 cited-by 验证表（如时间紧交对话 3）
4. 主线 grep 核查 + 复用旧笔记删/标撞 D006 段
5. 产出 S004 + H003 交对话 3（B8/B9/B10 + B11/B12 评点 + literature_notes 并入）
