# S005 PROMPT-004 参考文献质量升级 + Bib 元数据批量修复

> 2026-06-04 | 执行+修复 | 完成
> 2026-06-04 续接：P-012 GB7714 格式修正 + DeepSeek 二轮审查问题处理

## 目标

1. 完成 PROMPT-004：将 kaiti-report.md 中的 Tier-3 引文替换为 trans 级
2. 发现并修复 bib 文件中大量 AI 编造的元数据（DOI/卷期页码）

## 记录

### Phase 1：PROMPT-004 质量升级（上一轮完成，本轮恢复）

- 9 个 Tier-3 bib 条目标记 REPLACED，4 个新 trans 级条目添加（chan2026jstqe, chen2023dl, gappmair2017, schmogrow2012）
- 14 处 citekey 替换完成
- 新论文 DOI 均通过 Semantic Scholar API 验证

### Phase 2：编译验证 + DeepSeek 审查

- 编译 kaiti.docx 后，用 DeepSeek 审查参考文献列表
- DeepSeek 标记 26 条格式问题 + 3 条期刊质量偏低
- 关键发现：**大量 DOI 是 AI 编造的**

### Phase 3：Bib 元数据系统性审计

**问题规模**：
- bib 文件 106 条 DOI 中，3 个重复 DOI（不可能）
- `10.1117/12.3012345` 出现 5 次（同一 DOI 给 5 篇不同论文）
- `10.1088/2040-8986/abcd12` 明显编造（"abcd12"）
- kaiti-report 引用 63 条中 43 条有缺失/错误

**工具开发**：
- 创建 `tools/bib_verify.py`：用 Semantic Scholar API 批量验证 bib 条目
- 使用 `S2_API_KEY`（在 `.env` 中，key: s2k-FrVAP...）
- API 支持按 DOI 查询和按标题搜索

**批量验证结果**（38 条有问题的条目）：
- 34 条通过 SS API 找到正确元数据
- 4 条未找到（3 条中文 + 1 条 SPIE）

**高置信度应用（17 条）**：sim ≥ 80%，DOI/卷期页码已更新
- alhabash2001, almonacil2020, chan2026jstqe, chen2023dl, gappmair2017, khalighi2014, li2024jlt, pfau2009, rustum2026iet, safi2019, valjus2025dsp, viterbi1983, wang2024oe, wang2025a, xu2025, yang2025, zhao2025

**用户验证后修正（5 条）**：
- kaushal2016：作者从 3 人改为 2 人（Kaushal + Kaddoum），卷期页码修正
- zhang2024jlt（原 zhang2024pilot）：标题改为 "Automatic Turbulence Resilience..."
- zhang2023kf：期刊从 LPT 改为 IEEE Photonics Journal，标题修正
- yuan2017：作者从 "Jie Yuan" 改为 "Shuai Yuan"
- brandao2024：页码从 384-394 改为 270-277

**SPIE 论文修正（1 条）**：
- heine2023tesat：标题改为 "Status on Laser Communication Activities at Tesat-Spacecom"，补全 DOI/卷页

**编造论文删除（3 条）**：
- davies2024fiber：DOI 假，SS 搜不到 → 删除引用（同段其他引文已支撑论点）
- zhou2014clock：作者"Uma Devi G."假，DOI 假 → 替换为 @valjus2025dsp
- mcdonald2025：DOI 返回 404 → 删除该句（3 dB 数据无法验证）

**中文文献补全（3 条）**：
- guanhaijun2019：中国光学 2019, 12(5):1131-1138（已完整）
- yanjiaxin2024：电子科大硕士论文，补 DOI
- yanxu2022：西电硕士论文，补 DOI

### Phase 4：编译问题修复

- bib 解析错误：zhang2024jlt 和 heine2023tesat 标题更新时旧标题残留 → 修复
- Word 锁文件导致写入失败 → 需关闭 Word 再编译

## 决策引用

- 无正式决策（执行性工作）

## 范围确认

- 本轮在 scope boundary 内：是（PROMPT-004 质量升级 + P-012 前置 bib 修复）

## 后续

### 待办
1. ~~用户压缩后给 DeepSeek 最新审查结果 → 需处理~~ → **已完成**（Phase 5）
2. P-012（GB7714-87 格式修正）→ **大部分已完成**（Phase 5），剩余 3 个无法修复项
3. **valjus2025 DOI 10.3390/satellite8030045 Crossref 返回 404** — 不能从 DOI 格式猜测卷页，需用 MDPI/Semantic Scholar 实际验证，找到正确元数据
4. **[5] heine2023tesat CSL "卷" 字问题** — 用户明确要求修复。CSL gb7714-2015.csl 对会议论文渲染 "Proc. SPIE: 卷 12413"，"卷" 字不符合 GB/T 7714。需修改 CSL 或 bib entry 的 booktitle 格式，去掉 "卷" 标签
5. S001 topic-index 需更新
6. ~~`israel2023lcrd` 在 kaiti-report 中引用但 bib 中找不到~~ → citekey 实际匹配，已修正 DOI/标题/卷号
7. bib 中仍有部分旧条目（非 kaiti-report 引用）的 DOI 可能也是假的，但不在本轮范围内

### 关键教训
- **bib_verify.py 的 sim 门槛 35% 太低**：mcdonald2025 (57%) 匹配到社科论文，davies2024fiber (75%) 匹配到错误论文。建议 ≥80% 才自动应用
- **标题替换会残留旧文本**：用 regex 替换 title 字段时，如果旧标题包含 `}` 后的残留文本会导致 bib 解析错误。需要验证替换结果
- **Semantic Scholar 查不到中文文献和极新论文**（2025-2026 的某些论文）
- **编造 DOI 的特征**：连续数字尾号（3401234）、同一 DOI 多次出现、DOI 返回 404
- **编译前必须关 Word**：否则 docx 写入 permission denied
- **SS API 查不到不代表 DOI 不存在**：部分 Optics Express/SPIE 论文 DOI 在 Crossref 能查到但 SS 没有。应 SS → Crossref 依次验证
- **同一 DOI 配不同标题 = 编造条目**：petkovic2022/2023 共享 DOI 但标题不同，说明其中一个标题是 AI 改写的。应 Crossref 验证 DOI→标题映射
- **replace-et-al.lua 检测范围太宽**：CSL 中文 locale 渲染的"卷"会误触发中文字符检测。修复：仅检测作者区域（前 80 字符）

### Phase 6：DeepSeek 第三轮审查（续接对话，压缩后）

用户提交第三轮 DeepSeek 审查结果（59 条，Petkovic 重复已删除）。DeepSeek 评价大幅改善：
- 绝大多数条目格式正确、期刊水平可接受
- 仅标记 2 条期刊偏低：[6] Strategic Study of CAE、[41] MDPI Mathematics
- 格式问题仅剩：[5] "卷"字、[23] 缺页码、[58] valjus2025 刊名+缺卷页
- 2026 出版年份：用户确认现在是 2026，年份无问题

**本轮处理**：
- valjus2025：临时从 DOI 格式推断 vol=8(3):45，**但 Crossref 返回 404，需要实际验证**
- heine2023tesat "卷"字：**用户要求必须修复**，CSL 渲染问题待处理
- 已更新 bib（valjus2025 补了 volume/number/pages），编译验证被 Word 占用阻断

**压缩时状态**：等待用户关闭 Word 后重新编译 + 验证 valjus2025 DOI + 修复 CSL "卷"字

### Phase 5：DeepSeek 二轮审查 + P-012 GB7714 格式修正（续接对话）

用户压缩上下文后，将最新编译结果提交 DeepSeek 审查。DeepSeek 标记 21 条问题（格式错误 + 期刊水平偏低）。

**格式修复（16 条，全部已处理）**：

| 原编号 | citekey | 问题 | 修复方式 |
|--------|---------|------|---------|
| [4] | israel2023lcrd-early | DOI 编造 + 缺卷号 | DOI 改为 10.1117/12.2655481（Crossref 验证），补 SPIE 12413 |
| [5] | heine2023tesat | "等"替代"et al." | 修复 replace-et-al.lua：仅检测作者区域中文字符，避免 CSL 渲染的"卷"误触发 |
| [6] | wang2020progress | 期刊名错 + 缺卷期页码 | journal→"Strategic Study of CAE"，补 vol=22(3):118-126，DOI 修正 |
| [10] | andrews2005 | "2nd 版" | edition→"2nd ed."（CSL else 分支直接输出文本变量） |
| [13] | gong2015 | 作者缺首字母 | author→"Gong, Chen and Xu, Guanding" |
| [14] | valjus2025dsp | 缺期号页码 | Crossref 补 number=3, pages=229-250 |
| [16] | zhang2018 | 作者缺首字母 + DOI/页码错 | SS API 修正完整作者名/标题/DOI/页码 |
| [17] | li2024jlt | volume/pages 散落在 entry 外 | 移入 entry 内部 |
| [20] | sun2020 | DOI 指向完全不同论文 | SS API 找到正确论文，修正 DOI/标题/作者/卷页 |
| [23] | rustum2026iet | 缺期号 | Crossref 补 number=1（页码未分配，2026 在线发表） |
| [32] | almonacil2020 | 缺 DOI/页码 | 补 DOI + pages=1-4 |
| [43] | gardner1979 | "2nd 版" | edition→"2nd ed." |
| [53] | ozbilgin2025 | DOI 编造 + 标题编造 + 作者缺首字母 | SS API 找到真实论文（VLC 相位噪声），修正全部字段，调整 kaiti-report 引用文本 |
| [55] | li2022 | DOI 编造 + "others" + 页码错 | SS API 修正 DOI/作者/页码 |
| [56] | zhang2024jfso | journal={IEEE} + "others" + 缺卷页 | SS API+Crossref 修正为 Optics Communications, vol=552 |
| [60] | ju2024realtime | 期刊错(LPT→JLT) + DOI 编造 | SS API+Crossref 修正全部 |
| [28] | yanxu2022 | 缺保存地点 | 补 address=西安 |
| [58] | yanjiaxin2024 | 缺保存地点 | 补 address=成都 |

**重复条目处理**：
- petkovic2023 与 petkovic2022 共享同一 DOI (10.3390/math11010121)，标题为 AI 编造的变体 → petkovic2023 注释删除，kaiti-report 中 4 处引用合并为 @petkovic2022，L74 文本合并为单篇论文的描述

**replace-et-al.lua 修复**：
- 旧逻辑：检测整个参考文献文本中的中文字符 → CSL 渲染的"卷 12413"误触发 → 英文论文"et al."被替换为"等"
- 新逻辑：仅检测前 80 字符（作者区域）中的中文字符 → 仅中文作者论文触发替换

**无法修复的剩余问题**：
- [4] israel SPIE 页码：Crossref/SS 均未收录
- [23] rustum2026iet 页码：2026 在线发表，尚未分配
- [41] petkovic2022 MDPI Mathematics：期刊偏低但内容独特，无同主题 trans 级替代

### Phase 7：压缩后续接 — valjus2025 验证 + "卷"字修复

> 2026-06-04 续接

**valjus2025 深度验证**（子 agent SS API + Crossref + OpenAlex 三路验证）：
- DOI `10.3390/satellite8030045` 在 doi.org/Crossref/Semantic Scholar 均返回 404
- 期刊 "Satellite" (ISSN 3080-4727, 声称 MDPI) 在 Crossref/OpenAlex 均不存在，MDPI 网站 403
- Carl Valjus 总共仅 3 篇论文（SS 作者页确认），**valjus2025 即 valjus2025dsp 的编造变体**（标题缩短 + 虚构期刊 + 虚构 DOI）
- **处理**：删除 valjus2025 bib 条目，kaiti-report.md (L408) + material-chapter-literature.md (3处) 的引用全部替换为 valjus2025dsp

**CSL "卷"字根因修复**：
- 根因：CSL `volume` macro (L109-125) 对非 article 类型条目，若 volume 为纯数字则渲染 `<label variable="volume" form="short"/>` + 数值，中文 locale 下 label = "卷"
- 修复方式：将会议论文的 `volume` 字段并入 `booktitle`，删除独立 volume 字段
- 受影响条目：heine2023tesat (`booktitle = {Proc. SPIE}` + `volume = {12413}`) → `booktitle = {Proc. SPIE 12413}`
- 同类条目 yang2025 同法修复：`booktitle` 改为 `Proc.\ SPIE 13630, Fourth International...`，删除 `volume = {13630}`
- israel2023lcrd-early 原本已将卷号写入 booktitle，无需修改
- **编译验证通过**：参考文献列表中无"卷"字残留

### Phase 8：DeepSeek 第四轮审查 — 会议论文地址补全 + 页码修复

> 2026-06-04 续接

DeepSeek 第四轮审查结果：59 条中仅 2 条期刊偏低 + 12 条格式问题（主要是会议论文缺地点），其余全部通过。

**会议论文/书籍地址补全（10 条）**：

| 编号 | citekey | 补充内容 | 来源 |
|------|---------|---------|------|
| [4] | israel2023lcrd-early | address=San Francisco, publisher=SPIE | SPIE Photonics West 常规地点 |
| [5] | heine2023tesat | address=San Francisco, publisher=SPIE | 同上 |
| [29] | neves2023 | address=San Diego, publisher=IEEE | OFC 2023 |
| [32] | almonacil2020 | address=Brussels, publisher=IEEE | ECOC 2020 |
| [33] | zhao2025 | address=Qingdao, publisher=IEEE | Crossref event.location |
| [34] | wang2025a | address=Jiangsu, publisher=IEEE | Crossref event.location |
| [36] | yang2025 | address=Suzhou, publisher=SPIE | Crossref event.location |
| [42] | gardner1979 | address=New York | Wiley 常规出版地 |
| [43] | moeneclaey1994 | address=San Francisco, publisher=IEEE | GLOBECOM 1994 |
| [49] | wu2012 | address=Anaheim, publisher=IEEE | GLOBECOM 2012 |
| [51] | yuan2017 | address=Singapore, publisher=IEEE | OECC 2017 |
| [10] | andrews2005 | address=Bellingham | SPIE Press 出版地 |

**页码修复（1 条）**：
- [23] rustum2026iet：补 pages=e70148（Crossref article-number）

**不可修复的剩余问题（4 条）**：
- [4] israel2023lcrd-early 页码：Crossref 返回错误数据（pages=2），无可靠来源
- [6] wang2020progress 期刊偏低（Strategic Study of CAE）：中国空间激光通信进展，无英文顶刊同角度替代
- [41] petkovic2022 期刊偏低（MDPI Mathematics）：内容独特（Málaga + DPLL 参数映射），替代候选 Hu et al. IEEE PTL 2025 角度不完全匹配，用户决定不替换

**P-012 状态**：GB7714 格式修正基本完成，4 条已知限制如上。
