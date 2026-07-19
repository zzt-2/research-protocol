# [S074] Pilot Jones Step3.5 R2/R3 收敛纠偏

> 2026-07-17 | GW Step3.5 | 状态：待V031最终审查（原预留V030未落盘，V030后用于P03终验）

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
