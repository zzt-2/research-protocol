# [S074] Pilot Jones Step3.5 R2/R3 收敛纠偏

> 2026-07-17 | GW Step3.5 | 状态：待V031最终审查（原预留V030未落盘，V030后用于P03终验）
> 2026-07-22 续接 | D061/V035：战略切换激活 Pilot-Jones 为 formal GW 线；backward-chain 终验 PASS（V035）；4 篇直接竞品全文获取 BLOCKED；Step 3.5 维持 PARTIAL 不进 4a；纠正 170c00c 审计错误

## 目标

按独立V028指出的硬缺口完成Step3.5收敛：补R3、修正最高引用核心竞品双向引用链，并保留全文/provenance纠错。

## 记录

R1满足6/6矩阵、42 raw→41 unique、OpenAlex+Semantic Scholar两源，但新增4篇必读+1篇建议读，不能以重复簇主观宣称收敛。OE 2021此前被误报为失败获取，主控复核发现`papers/doi/10.1364_oe.419574/content.md`为54KB、metadata=`success/good`的完整HTML全文；已由子agent按gw-read完成L013精读。其余4篇仍为摘要级证据。

R2严格按5种方法变体×2类场景检索，31 raw→25 unique；汇总相对全归档判new=0，但独立V028指出JLT 2023 PDL/FPT仍应视为R2新增直接竞品，存在去重全集口径差异，故不采信“已收敛”作为门控结论。V028结论PARTIAL，禁止进入Step4a。

R3仅围绕JLT 2023 PDL/FPT同族补检，50 raw→37 unique，新增必读/建议读=0。最高引用直接竞品为JLT 2022（citation_count=36，高于OE 2021的19）：Semantic Scholar前向链25篇；原backward wrapper因空query/HTTP429失败，不能当真实0。随后通过Crossref publisher metadata补得21条references，并在子agent中批量筛出7篇方法相关，全部为已知候选、新增0。双向链已按“前向citing papers + 后向references metadata”语义透明闭合，待V031独立复核。

## 决策引用

- D056：直接竞品必须在Step4a前检查。
- V028：Step3.5 PARTIAL；R3和最高引用双向引用链为硬后续。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

V029在Crossref补链前判PARTIAL；后续独立复核编号改为V031。只有V031 PASS才进入Step4a。

---

## 2026-07-22 续接记录（D061/V035 战略切换 + 审计纠正 + acquisition BLOCK）

### 纠正 170c00c（science-scout SCIENCE_FREEZE 轮）的审计错误

用户指出 H015/S014/D022（170c00c）中关于 Pilot-Jones Step 3.5 的表述有事实错误。逐条用真实文件复核（FR-26 证据链 / TL-33 自欺式核查防护）：

1. **"LCOMM 2026 仅 abstract" 错误**：S069（专篇精读）+ S071（列为已精读第1篇）证明 LCOMM 2026 `papers/doi/10.1109_LCOMM.2026.3651445/content.md` **已完成全文精读**（FPT 频域 pilot→4 路 FPT→2×2 Jones 直接补偿，光纤场景，无时域 LS+EMA）。H015 写"JLT2022-23/TCOMM2025/LCOMM2026 仅 abstract"是**把联想当证据**（TL-33），未查 read-log。
2. **"真正缺全文的四篇"**：以 D056/S072 的 DOI/title 为准，真正缺全文闭合的是：
   - TCOMM `10.1109/TCOMM.2024.3522036`（Time-Domain ML Est. Ultra-Fast RSOP；S072 称"TCOMM 2025"，DOI 实为 2024）
   - JLT `10.1109/JLT.2025.3640695`（Joint Preamble/DSP Burst-Mode Coherent PON；S072 称"JLT 2026 短 preamble"）
   - JLT `10.1109/JLT.2022.3224805`（HW-Efficient Polarization/Carrier Phase Tracking, FPT DSCM）
   - JLT `10.1109/JLT.2023.3284489`（HW-Efficient Robust DSP, DSCM TX IQ Impairments）
   - 已全文精读：OE 2021 `10.1364/oe.419574`（L08/L013）+ LCOMM 2026（S069）。
3. **"JLT 2022 backward chain 尚未获取"错误**：S074 本体 line 15 已记录 Crossref references=21、screened=7、new=0。**缺的是对该现成补链的独立终验**（V029 标 UNAVAILABLE 后的缺失终审），不是重新抓取。本轮已完成该终验（见下 V035）。

### backward-chain 独立终验（V035 = PASS）

独立 verifier 子 agent 读 `search-archive/2026-07-17/step35-r3-jlt2022-{crossref,backward,backward-screened}.json` 真实文件，6 项 claim 全 PASS：
- Crossref `reference_count=21`、`has_references=true`、`len(references)=21`、DOI match `10.1109/jlt.2022.3224805`；
- `screened_relevant`=7（含 OE 2021 = 直接前作 ref8）；
- `new_must_read=[]`、`new_suggested=[]`；
- 7 篇全部在 `search-archive/_index/all-papers.jsonl`（count≥1）+ 部分在 `papers/doi/` —— 全已知无新增；
- backward 语义正确（`chain_type:"backward references metadata"`，forward 25 citers ∩ backward 21 refs = ∅）；
- provenance 真实（Crossref REST + timestamp；两个 failed S2 尝试 total=0 保留为失败证据）。
- **gw-supplement 判据 #3（双向引用链已分析）现满足**。V029 的 UNAVAILABLE 由 Crossref 补链闭合。

### 4 篇直接竞品全文获取 = BLOCKED

- `tools/download --doi` 对 4 篇均 `all_failed`（non-OA IEEE paywalled；降级链 arXiv→OA PDF→Unpaywall 全失败）。
- OA scout 子 agent（Semantic Scholar `openAccessPdf` + Unpaywall `is_oa` + OpenAlex + arXiv 标题/作者检索）四源交叉：**4 篇均 closed / is_oa=false / 无 arXiv 预印本 / 无 green-OA**。
- 按 gw-read.md（浅读不计入精读门槛）+ 用户提示 §五（不得用 abstract 冒充全文）+ TL-33：**4 篇全文 BLOCKED，记 BLOCKED_NO_FULLTEXT，不强过 Step 3.5**。

### Step 3.5 最终裁决：PARTIAL/BLOCKED（不进 Step 4a）

- backward-chain 门：PASS（V035）。
- 收敛门（判据 #4 最后一轮 new=0）：R3 已 new=0（V029 确认）。
- **D056 全文门：FAIL/BLOCKED**——4 篇直接竞品全文无法获取，只有 OE 2021 + LCOMM 2026 两篇全文精读。
- **结论：Step 3.5 维持 PARTIAL/BLOCKED，不进入 Step 4a**（FR-22 硬门 + D056）。4 篇全文获取阻塞交主控/用户裁决获取路径（机构 VPN / 作者邮件 / 等待 OA / 是否以 2 篇全文 + V035 backward 证据 + 摘要级证据作"带债推进"由用户显式豁免——但本轮不豁免）。

### Q2 当前 M-C-A（基于已读全文 OE 2021 + LCOMM 2026 + V035 backward 证据）

- **M**：传统 block/frame pilot Jones inversion（短 pilot LS 估计 2×2 Jones + inverse derotation）—— OE 2021（3 pilot tones 逐 block RSOP 矩阵+inverse）+ LCOMM 2026（FPT→4 路→Jones 补偿）均属此族。
- **C**：dual-pol OSL 的 GG 湍流 + 高速 SOP + ≤10% pilot 预算。已读全文均**非 OSL 场景**（OE 2021 光纤短距 SCM；LCOMM 2026 光纤 DP-16QAM），且 OE 2021 自述短 block 噪声 penalty + 长 block 动态失配 + 矩阵退化/定点溢出风险（content.md L178-344）。
- **A**：fixed-label 恢复不稳定（短 pilot 估计抖动/病态）。**关键不确定性**：是否 OSL GG 深衰落引入 OE 2021/LCOMM 2026 未处理的结构性新失效（改变算法结构），还是仅场景替换/EMA 参数差异（→ Kill）。
- **裁决门**（D055/D056）：若只是 OSL 场景替换或 EMA=.9 参数差异 → Kill；若存在既有方法未处理的结构性 GG/低 pilot 病态且需改变算法结构 → 允许进 Step 4a。**当前 4 篇直接竞品全文未读，无法判定 A 是否真的不同** → Step 3.5 PARTIAL 的根因。

## 决策引用

- D056：直接竞品必须在Step4a前检查。
- V028：Step3.5 PARTIAL；R3和最高引用双向引用链为硬后续。
- D061：**新建**——战略切换控制面（P03 暂停选项① + Pilot-Jones 激活）；Step 3.5 backward PASS 但 4 篇 BLOCKED → 维持 PARTIAL 不进 4a。
- V035：**新建**——JLT 2022 backward-chain 独立终验 PASS。

## 范围确认

- 本轮是否在 scope boundary 内：是（GW Step 3.5 文献门控 + 控制面切换，均在原始目标"GW Step 1-4a 完整流程"内）。

## 后续（更新）

Step 3.5 维持 PARTIAL/BLOCKED。下一轮由用户裁决 4 篇全文获取路径：
- (a) 机构 VPN/proxy 获取 IEEE 全文后精读（最完整）；
- (b) 邮件联系通讯作者（Shuai Liu / Yiyang Feng / Linsheng Fan×2）求全文；
- (c) 以 2 篇全文（OE 2021 + LCOMM 2026）+ V035 backward 证据（7 篇已知 backward refs）+ 4 篇摘要级证据"带债推进"Step 4a（需用户显式豁免 D056 全文门，并把 backward 未独立精读列为阻断性债务）；
- (d) 等 OA / 换近似竞品。
**本轮不豁免、不进 Step 4a。**
