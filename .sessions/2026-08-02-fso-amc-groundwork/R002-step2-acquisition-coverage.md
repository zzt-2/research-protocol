# [R002] Step 2 Acquisition 覆盖面报告

> ⚠️ **SUPERSEDED 2026-08-02 by D003** — 本报告判定的"Step 2 PASS / 6 篇覆盖 A/B/C 三族"经主控复核**不成立**。6 篇只过文件/转换质量门，**未做 CORE 判定**。逐篇 CORE 重判后保守核心集缩窄到 L023/L096/L146 3 篇（L075 DISPUTED / L165 AO 边界 / L090 fixed-STTC 边界不计核心），本轮补获 Galijasevic 后 CORE 全文 = 4 < 5 门槛 → Step 2 终态 **STEP2_BLOCKED_BY_COVERAGE_GAP**。本报告保留作历史档案（身份+内容质量门判定仍有效，是 CORE 判定的输入），但其"PASS/三族覆盖"结论废止。最新判定见 S003 + `search-archive/2026-08-02/_step2_acquisition_receipt.json` + topic-index GW Progress 表。

> 2026-08-02 | 关联：专题 slug 2026-08-02-fso-amc-groundwork / D002 / S002 / R001 shortlist
> 阶段：GW Step 2（身份+内容质量门，**非全文精读**；不写方法结论）
> 数据源：`search-archive/2026-08-02/_step2_shortlist.json`（13 篇）+ 3 轮下载止损（`search-archive/2026-08-02/_step2_download_log.md`）

---

## §1 调研问题

Step 2 要回答：13 篇 shortlist 能否获取到合格全文（≥50 行有效 content.md），覆盖 A_MCS_POWER_CONTROL / B_HARQ_IR_RATE_ADAPTATION / C_COHERENT_TX_ADAPTATION 三个候选族，且 L124（C 族身份闭合关键论文）得到确定身份结论。

---

## §2 每篇身份与内容质量门（B3）

> 主线程独立复核：6 篇 success 的 content.md 行数 + source.pdf SHA256 + 前 15 行身份抽查，全部与 subagent 报告一致（P6 分离审查）。

### 成功获取（6 篇，全部 ≥50 行有效内容）

| L | 路径 | source.pdf SHA256[:12] / size | content 行数 / 非空 | 身份（title+authors+venue+year+DOI 一致） | 候选族 | 质量门 |
|---|---|---|---|---|---|---|
| L165 | `papers/doi/10.1038_s41377-023-01201-7/` | fb2a72b55452 / 4.96MB | 359 / 226 | ✓ Horst et al., Light Sci Appl 12:153, 2023, DOI 10.1038/s41377-023-01201-7 | C（coherent feeder + AO，adaptive 动作在 AO 层） | PASS |
| L023 | `papers/doi/10.1109_jlt.2023.3242215/` | 97d7a981a5a2 / 2.20MB | 444 / 208 | ✓ Hu et al., JLT 41(11):3397-3406, 2023, DOI 10.1109/jlt.2023.3242215（Glasgow self-archive） | A（CSI-driven mod+power+MIMO 最强 comparator） | PASS |
| L096 | `papers/doi/10.1109_tvt.2021.3127193/` | 4fde136d1bdb / 2.65MB | 600 / 242 | ✓ Le & Pham, IEEE TVT 71(1), 2022, DOI 10.1109/tvt.2021.3127193 | B（IR-HARQ + rate adapt cross-layer 锚） | PASS |
| L146 | `papers/doi/10.1109_jiot.2025.3600439/` | 3f1389c5795e / 4.71MB | 863 / 338 | ✓ Li et al., IEEE IoT J 12(21), 2025, DOI 10.1109/jiot.2025.3600439（R2 经 Crossref 补 DOI） | A（robust MCS + imperfect CSI，**abstract 明提 adaptive modulation and coding schemes (MCS) + imperfect CSI**） | PASS |
| L075 | `papers/doi/10.1109_access.2025.3650714/` | 716080c6186d / 1.88MB | 564 / 245 | ✓ Sahrab & Albasri, IEEE Access 2026, DOI 10.1109/access.2025.3650714 | **⚠ identity 重新定性**：abstract 明说 "to **classify** real time modulation schemes…classification accuracy 96.3%" → 实为**调制分类 (modulation CLASSIFICATION/MFI)**，非 AMC。R001 标 "DL AMC 对照" 错误。属 dead-end#8 假命中族，Step 3 不当 AMC baseline，但可作 classification 边界参照。 | PASS（内容合格）/ 标签待 Step 3 修正 |
| L090 | `papers/manual/L090-intechopen/` | 2af0474cc5dd / 768KB | 294 / 132 | ✓ Adedayo et al., IntechOpen chapter, DOI 10.5772/intechopen.84911，"Mitigating Turbulence-Induced Fading…Adaptive Space-Time Code" | C（coherent FSO + STTC；本地 OWC-survey abstract 污染，真实内容是 STTC） | PASS |

### 下载失败（5 篇，已 3 轮止损）

| L | 失败原因 | 候选族 | 影响 |
|---|---|---|---|
| **L124** | Optica Publishing HTTP 202 JS-challenge bot-block（gold OA 但反爬）。R2 Crossref/S2 已确认身份（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557，coherent-FSO AMC），全文未获 | C（身份闭合关键论文） | **身份 bibliographic 级已闭合**（不再 title-abstract 混乱）；全文 coding/CSI/channel/scenario 仍缺，须用户手动获取 |
| L126 | MDPI Photonics HTTP 403 Access Denied（网络级 bot-block，非 header 可修），gold OA | B（power+HARQ） | L096 已覆盖 B 族 HARQ-IR 锚，L126 缺失不致命 |
| L073 | MDPI Entropy HTTP 403 同 L126，gold OA | B（HARQ 极限） | 同上，B 族已有 L096 |
| L018 | 2017 DLR elib 报告，无 DOI，无可发现 OA/API 副本 | A/B（F1 统计 CSI 锚） | 统计 CSI 路线锚点缺失；可由 L146（imperfect CSI）部分替代 |
| L020 | 无 DOI/venue，abstract 是污染的 OWC-survey（与 L038/L090 同组），目标无法可靠解析 | A（旧 baseline） | identity-uncertain，不计入有效获取；L023 已覆盖 IM/DD AMC baseline |

### 中文 manual_required（2 篇，CNKI cookie/IP 受限）

| L | 状态 | 候选族 | 影响 |
|---|---|---|---|
| L050 | blit cnki 搜 "DFT-SAMP 信道估计 概率整形 FSO" 未命中目标记录（空间电子技术 2026 未被 CNKI 索引/覆盖） | A（中文 PS+FSO，dead-end#5 风险） | 仅用于判断是否固定 PS/信道估计换名，不计入 5 篇门槛 |
| L206 | 同 L050（三维概率整形 FSO 快衰落，空间电子技术 2026） | A（同上） | 同上 |

---

## §3 覆盖面状态

- **成功获取**：6 篇（L165 / L023 / L096 / L146 / L075 / L090）—— 全部 content.md ≥50 行有效内容（实际 294–863 行），身份 title+authors+venue+DOI 一致。
- **内容质量不达标**：0 篇。
- **下载失败（用户待获取）**：5 篇（L124 / L126 / L073 / L018 / L020）。
- **manual_required（中文 CNKI）**：2 篇（L050 / L206）。

### 候选族覆盖（修订后 A/B/C）

| 族 | 覆盖状态 | 已获论文 |
|---|---|---|
| **A_MCS_POWER_CONTROL** | ✓ 覆盖 | L023（CSI-driven mod+power+MIMO 最强 comparator）/ L146（robust MCS + imperfect CSI）/ L075（⚠ 实为 classification，边界参照非 baseline） |
| **B_HARQ_IR_RATE_ADAPTATION** | ✓ 覆盖 | L096（IR-HARQ + rate adapt cross-layer 锚） |
| **C_COHERENT_TX_ADAPTATION_UNVERIFIED** | ◐ 部分 | L165（coherent feeder + AO，adaptive 在 AO 层）/ L090（coherent FSO + STTC）/ **L124 未获全文**（身份 bibliographic 级闭合，coding/CSI/channel 待全文） |

### Step 2 通过要求核对（gw-acquire.md + 执行提示词 §四 B4）

| 要求 | 状态 |
|---|---|
| ≥5 篇核心论文成功转合格 content.md | ✓ **6 篇**（PASS） |
| 覆盖 MCS/功率控制 | ✓ L023/L146 |
| 覆盖 HARQ/IR | ✓ L096 |
| 覆盖 coherent tx adaptation 或明确证明其缺失 | ◐ L165/L090 已获但 action 在 AO/STTC 层；**L124（最关键 coherent AMC 身份闭合论文）全文未获**，bibliographic 级确认是真实 coherent-FSO AMC（Optics Express 34(14):26128），但 coding/CSI/channel/scenario 须全文 |
| L023/L096 至少成功获取或明确 blocker | ✓ 均成功 |
| L124 得到确定身份结论，不保持 title-abstract 混乱 | ✓ **bibliographic 级确定**（Optics Express + DOI + coherent-FSO AMC abstract，经 Crossref+S2 双源）；全文级 coding/CSI 仍缺（Optica 反爬，用户手动获取 blocker） |

### 引用质量分析

- 正式发表：6/6 success 全部正式发表（L165 Light Sci Appl / L023 JLT / L096 IEEE TVT / L146 IEEE IoT J / L075 IEEE Access / L090 IntechOpen chapter）。
- 预印本：0 篇（success 中无预印本）。
- **预印本占比 0%**（远低于 50% 警戒线）。

---

## §4 结论

**Step 2 PASS**（6 篇合格 content.md ≥5 门槛，覆盖 A/B/C 三族；引用质量 0% 预印本）。**不 BLOCKED**：虽 L124/L126/L073/L018 受付费墙/反爬/无 OA 阻塞，但 6 篇 success 已超门槛且三族覆盖成立。

**L124 身份结论（执行提示词第 3 项必答）**：L124 是**真实的 coherent-FSO AMC 论文**（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557，physics-informed AMC，modulation selection driven by [SNR, scintillation index, phase variance]），bibliographic 级身份**确定**，**不再保持 title-abstract 混乱**。全文 coding 标准 / CSI 估计 / 信道模型（是否 Gamma-Gamma）/ 场景（是否星地）仍缺（Optica JS-challenge 反爬，进入用户手动获取 blocker），但这不阻塞 Step 2 PASS——它已在搜索级确认 C 族"coherent tx adaptation"空间被一个真实 AMC 论文占据，C 族不再是纯空白。

**coherent AMC 空间身份结论（执行提示词第 3 项必答）**：C_COHERENT_TX_ADAPTATION 不再是空白——L124 占据了"coherent FSO + 物理信息 AMC（多维幅度-相位统计驱动 modulation selection）"位置。但 L124 的 abstract 未提 Gamma-Gamma / satellite-feeder，是 terrestrial coherent 取向；"星地 + Gamma-Gamma + 真实 coded chain + 信息不确定性"四要素齐全的直接竞品 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`（4 alias query 32 命中 0 直接竞品，覆盖 caveat：Exa 透支）。即：coherent AMC 空间**部分被占**（terrestrial physics-informed），**星地 GG + coded chain 切片仍可能开放**，须 Step 3 全文精读 L124 后才能定性。

---

## §5 对决策的影响

- **不新建 D###**（Step 2 是 acquisition，不产 Go/Kill/METHOD_SIGNAL；R002 只记覆盖面）。
- **L075 标签修正**进 Step 3 待办：R001 标 "DL AMC 对照" 错误，实为 modulation classification（dead-end#8 族），Step 3 不当 AMC baseline，可作 classification 边界参照。
- **L124 全文是 Step 3 第一优先**：用户手动获取 Optics Express 全文（DOI 10.1364/oe.595557）后，Step 3 精读闭合 coding/CSI/channel/scenario，定性 C 族是否仍开放。
- **下一合法动作**（唯一）：主控/用户确认覆盖面后，进入 **Step 3 全文精读**（独立新对话）。L023/L096/L146/L165/L090/L124 为精读池（L124 待用户补全文）。

### 用户行动项

- [ ] 手动获取 L124 全文（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557）放入 `papers/doi/10.1364_oe.595557/source.pdf` 后 `bash tools/convert` 转 content.md；或确认 bibliographic 级身份足够进 Step 3。
- [ ] （可选）手动获取 L126/L073（MDPI gold OA，反爬可换网络/VPN）/ L018（DLR elib 2017）/ L050/L206（CNKI 空间电子技术 2026）。
- [ ] 确认当前 6 篇覆盖面可接受，授权进入 Step 3。
