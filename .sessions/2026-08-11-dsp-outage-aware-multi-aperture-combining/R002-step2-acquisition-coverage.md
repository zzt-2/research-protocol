# [R002] Step 2 acquisition 与 coverage gap

> 2026-08-11 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D002

## 调研问题

冻结优先池的全文是否可得、身份是否闭合、转换内容是否达到 Groundwork Step 2 质量门；特别是 2019 Optics Communications direct competitor 是否可以进入后续 fresh-context 精读。

## 发现

### 获取结果

- 成功复用或获取并通过内容质量门：4 篇。
  - Johst et al., WiSEE 2024（现有 canonical PDF + Markdown）。
  - Wang et al., IEEE Photonics Journal 2023（共享根现有 HTML-derived fulltext）。
  - Yang et al., ICCC 2022（本轮 IEEE 专用通道获取 PDF 并转换）。
  - Tu et al., IEEE Photonics Journal 2020（本轮 IEEE 专用通道获取 PDF 并转换）。
- 内容质量不达标：0 篇。JPHOT 2020 有 39 个局部公式字形替换符，但正文、标题、DOI、图注与论述连续，未形成大面积乱码，仍判 qualified。
- 全文不可得：5 篇。
  - Sun et al., Optics Communications 2019，DOI `10.1016/j.optcom.2019.03.069`（P0）。
  - Geisler et al., Optics Express 2016，DOI `10.1364/OE.24.012661`。
  - Johst et al., OFC 2024，DOI `10.1364/OFC.2024.W2A.31`。
  - Rao et al., IEEE Access 2020，DOI `10.1109/ACCESS.2020.3035748`。
  - Ju et al., Optics Letters 2024，DOI `10.1364/OL.511941`。

### 三轮获取事实

1. 先审计 worktree、共享根、downloads/manual 与 metadata：仅 WiSEE 2024、共享根 Wang 2023 可复用；参考文献命中不算全文。
2. `tools/download` DOI 首轮以及 Step 1 OA URL/标题检索第二轮：P0、Geisler、OFC、Access、OL 均未产生 source/content；P0 的 Semantic Scholar + OpenAlex 身份记录一致标注非 OA、无 arXiv/PDF URL。Geisler 虽被索引标为 OA，但 DOI/viewmedia 合法入口均 `all_failed`。
3. IEEE 第三轮：ICCC 2022 与 JPHOT 2020 成功；Access 2020 连续两次在已返回 `application/pdf` 后于 30 s 流式读取超时，未留下可验证文件。没有使用 webReader、ResearchGate 或绕过访问控制的通道。

### 覆盖面分析

- 冻结 optical CORE 定义为 P0/P1 中直接支撑 reference M、defect 或 direct/hard competitor 的五篇：OptCom 2019、WiSEE 2024、Wang 2023、Geisler 2016、OFC 2024。
- qualified optical CORE=`2/5`：WiSEE 2024、Wang 2023。
- 其余 qualified 资产：JPHOT 2020 是 optical strong neighbor；ICCC 2022 是 RF comparator/neighbor。二者不得替代 optical CORE。
- P0 是 Step 1 已识别的最近 direct competitor；其全文不可得，因此完整 action signature 与 exact-collision 问题均不能在本轮闭合。本句只描述覆盖缺口，不给 collision verdict。
- 四篇 qualified 全部为正式发表，预印本=`0/4`；来源为本地 PDF/Markdown、共享根既有全文与 IEEE 专用获取，不存在 arXiv-only 偏差。

## 结论

`STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`。

P0 不可得是独立关键阻塞；同时 optical CORE `2/5 < 5`。Step 3 保持 `NOT_AUTHORIZED`，不得精读、提取完整动作签名或判断 exact collision。

### 用户 coverage 选择

- 手动提供 P0 合法全文，放入 `papers/manual/{slug}/` 并补 metadata；随后只重跑 Step 2 identity/content gate。
- 或明确确认接受“P0 未精读、exact collision unresolved”的 claim limitation，并另行授权 Step 3；在确认前不得继续。

## 对决策的影响

D002 的 Step 2 scope 已执行完毕，但 coverage blocking gate 未解除。没有形成 Q#、Go/Kill、METHOD_SIGNAL 或方法贡献判断。
