# Handoff: AMC GW Step 2 PASS → Step 3 全文精读

> 来源: S002 | 交接目标: 下一个对话进 Step 3 全文精读
> 日期: 2026-08-02
> 文件名: H001-step2-to-step3.md

## 到哪了（状态）

GW Step 1 限定完整性修复完成（D002/V002，候选族 4→3 A/B/C，L124 bibliographic 级身份闭合，6 dup-abstract 抓取污染确认，provenance receipt 固化）。GW Step 2 acquisition **PASS**：6 篇合格 content.md（L165/L023/L096/L146/L075/L090，294–863 行，身份 title+DOI 一致），覆盖 A_MCS_POWER_CONTROL（L023/L146）/ B_HARQ_IR_RATE_ADAPTATION（L096）/ C_COHERENT_TX_ADAPTATION（L165/L090）三族，引用质量 0% 预印本。5 篇下载失败（L124 Optica 反爬 / L126/L073 MDPI 反爬 / L018 无 OA / L020 identity-uncertain）+ 2 篇中文 manual_required（L050/L206 CNKI 未索引）进入用户手动获取 blocker。**未进 Step 3/精读/方法设计/仿真**。

## 下一步干什么

**用户验收 Step 2 覆盖面后**，开新对话进 **GW Step 3 全文精读**：
1. 读 `stages/gw-read.md`（Step 3 职责文件，**进 Step 3 前必读**，FR-22）。
2. 精读池（6 篇 success + L124 待补全文）：L023（A 族最强 comparator）/ L096（B 族 IR-HARQ 锚）/ L146（A 族 robust MCS+imperfect CSI）/ L165（C 族 coherent feeder AO）/ L090（C 族 coherent STTC）/ **L124（C 族身份闭合关键，Optics Express 34(14):26128 DOI 10.1364/oe.595557，待用户补全文）**。
3. L075 **不计入 AMC 精读池**——它实为 modulation classification（MFI，dead-end#8 族），可作 classification 边界参照。R001 标 "DL AMC 对照" 错误，Step 3 修正标签。
4. Step 3 精读须在**子 agent** 中做（context-dense），主线程只接收结构化提取（gw-read 模板）。
5. Step 3 产出 `literature_notes.md`（AMC 专属），含 2-3 篇标杆论文写作架构提取 + 每篇适配性分析。

## 纪律（和下一步直接相关的约束）

- **FR-22 硬门控**：进 Step 3 前必读 `stages/gw-read.md`；Step 3 + Step 4a 是硬门，不可跳。不靠记忆判 "现在在哪步"，以 `projects/thesis-fso/master-state.md` GW Progress 表 + 本专题 topic-index GW Progress 表为准。
- **L124 全文是 Step 3 第一优先**：它是 C 族身份闭合关键——bibliographic 级已确认是真实 coherent-FSO AMC（physics-informed，modulation selection driven by [SNR, scintillation index, phase variance]），但 abstract 未提 Gamma-Gamma/satellite（terrestrial 取向）。全文须闭合 coding 标准 / CSI 估计 / 信道模型 / 场景，定性 C 族"星地 GG + coded chain"切片是否仍开放。用户补不到全文则 Step 3 据 abstract+Crossref 做有限定性。
- **L075 不当 AMC baseline**（classification，dead-end#8）。
- **不复活 dead-end #1-#9**（见 topic-index ledger）；候选族均"候选假设未过四判据"，Step 3-4a 逐门验证，不强造方向。
- **"直接竞品 0 已确认"已废止** → 用 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`（覆盖 caveat：Exa 透支/OpenAlex 0/S2 限速，alias query 32 命中 0 直接竞品）。不把搜索未命中解释成真实空白（FR-23）。
- **诚实边界**：coherent AMC 空间**部分被占**（L124 terrestrial physics-informed），星地 GG + coded chain 切片仍可能开放，Step 3 定性。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC ≠ receiver campaign / GW 流程强制 FR-22 / Go-Kill 标准分离 / 证据链强制 FR-26；9 条 dead-end ledger）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] L124 官方身份 = Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557（验证：`_step1_receipt.json` l124_identity_resolution 块）
  - [ ] 6 篇 success content.md 行数 ≥50（验证：`wc -l papers/doi/{10.1038_s41377-023-01201-7,10.1109_jlt.2023.3242215,10.1109_tvt.2021.3127193,10.1109_jiot.2025.3600439,10.1109_access.2025.3650714}/content.md papers/manual/L090-intechopen/content.md`）
  - [ ] 候选族修订为 3（A/B/C），非原 4（F1-F4）（验证：topic-index "其他结论" + D002）
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on（system D020 / longitudinal negatives / ch3 先验）和 conflicts_with（空）
- [ ] 已确认当前范围未违反"明确不含"（不进 Step 4a/不设计方法/不跑仿真/不改 Skill/不改 p05 log）

## 接口变更（如有代码改动）

无（本轮无源码改动；仅 papers/ 新增 6 篇 content.md + search-archive receipt + 治理文档）。

## 失败数据附录

- **L124 下载失败**：Optica Publishing HTTP 202 JS-challenge bot-block（gold OA 但反爬）。bibliographic 身份已闭合（Crossref+S2），全文未获。
- **L126/L073 下载失败**：MDPI HTTP 403 Access Denied（网络级 bot-block，非 header 可修），gold OA。
- **L018 下载失败**：2017 DLR elib 报告，无 DOI，无可发现 OA/API 副本。
- **L020 identity-uncertain**：无 DOI/venue，abstract 是污染的 OWC-survey（与 L038/L090 同 dup-abstract 组），目标无法可靠解析——不计入有效获取。
- **L050/L206 manual_required**：CNKI blit 搜不到（空间电子技术 2026 未被 CNKI 索引/覆盖），cookie/IP 受限。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| L124 全文未获 | Step 3 须全文精读 C 族身份 | bibliographic 级闭合，全文 coding/CSI 缺 | 用户手动获取 DOI 10.1364/oe.595557 全文 |
| L075 标签错误（classification 非 AMC） | R001 标 "DL AMC 对照" | Step 3 待修正，不当 AMC baseline | Step 3 精读时修正 |
| alias collision 覆盖 caveat | Exa 透支/OpenAlex 0/S2 限速 | 仅 SerpAPI Scholar live，32 命中 0 直接竞品 | Exa 充值后重跑 4 alias query（可选，不阻塞） |
| 中文检索 cookie/IP | CNKI/Wanfang 受限 | L050/L206 未获 | 校园网 IP + cookie 可用时 blit 重试 |

## 下一轮

1. 用户验收 Step 2 覆盖面（6 篇 success + L124 bibliographic 闭合是否足够进 Step 3）。
2. （推荐）用户手动获取 L124 全文（DOI 10.1364/oe.595557）放 `papers/doi/10.1364_oe.595557/source.pdf` 后 `bash tools/convert`。
3. 开新对话，读 `stages/gw-read.md`，进 Step 3 全文精读（子 agent 执行，精读池 L023/L096/L146/L165/L090/L124）。
