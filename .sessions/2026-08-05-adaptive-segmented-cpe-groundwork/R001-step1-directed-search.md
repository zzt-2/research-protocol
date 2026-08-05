# [R001] C3 Step 1 定向检索与问题门裁决

> 2026-08-06 | 关联：2026-08-05-adaptive-segmented-cpe-groundwork / D001

## 调研问题

1. 是否存在 2019+ 顶刊、task-matched 的固定 block/window/segment NDA/blind CPE baseline？
2. 是否已有同 receiver-visible 信息、同 K/segment 动作粒度的 adaptive segmentation？
3. 主流 linewidth/SNR/turbulence 条件是否支持 C3，而不依赖拍参数？
4. 是否形成至少一个满足 `stages/glossary.md` 四判据的 Q#？

## 发现

### 查询、来源与计数

| Query | 路线 | 实际非零来源 | raw / query-dedup / final | 归档 |
|---|---|---|---:|---|
| Q1 `adaptive window length blind phase search carrier phase recovery coherent optical` | adaptive/variable window | S2 / OpenAlex / SerpAPI Scholar | 60 / 57 / 50 | `c3-q1-adaptive-window-blind-phase-search.json` |
| Q2 `variable block length non-data-aided carrier phase estimation Wiener phase noise coherent` | variable block NDA CPE | S2 / OpenAlex / SerpAPI Scholar | 35 / 35 / 30 | `c3-q2-variable-block-nda-cpe.json` |
| Q3 `fixed block window Viterbi-Viterbi blind carrier phase estimation coherent optical` | recent fixed baseline | S2 / OpenAlex / SerpAPI Scholar | 47 / 43 / 37 | `c3-q3-recent-fixed-block-cpe-baseline.json` |
| Q4 `laser linewidth SNR averaging window length phase noise tracking tradeoff carrier phase recovery` | PN-aware tradeoff | S2 / OpenAlex / SerpAPI Scholar | 45 / 44 / 34 | `c3-q4-linewidth-window-tradeoff.json` |

- 每组调用 S2、OpenAlex、arXiv、SerpAPI、Exa；arXiv 实际贡献 0，Exa 因 402 credits 实际贡献 0。
- 总计 raw=187，组内去重后=179，final records=151；跨组按 DOI/arXiv/title 去重=140。
- unique：published=77、unknown=63；必读=8、建议读=7、备选=20、待确认=36、排除=69。
- 检索前 `all-papers`=21,443 条，宽语义预扫命中 624；工具索引增量后=21,498（+55 unique）。

`gw-search` 数量/覆盖门：unique 140≥20、实际非零 API 源=3、必读=8≥5、正式发表下限
77/140=55.0%≥50%，且覆盖 adaptive/variable window 与 phase-noise-aware tradeoff 两条路线。形式门通过；
科学问题门仍须由四判据与历史 exact-action 反证裁决。

### 近期合法固定 baseline

| 论文 | Step 1 可支持的事实 | 角色 |
|---|---|---|
| JLT 2020, 10.1109/JLT.2020.2976166 | blind BPS；averaging-window type/size 影响实现 | 最强近期 task-matched fixed-window baseline |
| JLT 2021, 10.1109/JLT.2020.3027781 | 固定 mVV/BPS/PCPE 实现、设计参数与 SNR penalty | baseline 补强 |
| IEEE Photonics Journal 2024, 10.1109/JPHOT.2024.3415635 | Wiener PN 下 VV/LMMSE 与 memory/block-length effect | PN-aware baseline |
| Frontiers in Physics 2024, 10.3389/fphy.2024.1452087 | 固定 optimal block length=105 | near-task baseline |

这些论文与 C3 的 blind CPE 任务/估计器族匹配，但主要是 coherent fiber/system implementation，
不是 FSO-turbulence 场景 exact match。按本轮冻结的“task-matched”门，判据 3 PASS；其场景差异必须在
未来 Step 3 才能裁，不能在本轮升级为 FSO 物理证据。C3 不重复 P1 的 recent-baseline 缺位。

### 直接竞品与 tradeoff 证据

- 10.3390/photonics9100719（Photonics 2022）最接近 adaptive-window：blind EKF-PC，按 SNR 联合
  离线优化 noise-rejection window；它更换 estimator，且不是 current-window receiver-visible K selection。
- 10.1109/access.2019.2922313（IEEE Access 2019）对 Wiener PN 下 VV/MP 的对称 observation
  window 与 LMMSE 权重做理论优化；动作是权重设计，不是在线 segmentation。
- 10.1049/CP.2015.0121（IET 2015）明确 optimum averaging window 随 SNR/linewidth 改变，支持一般
  偏差—方差冲突，但不是 2019+ baseline。
- 10.1109/JLT.2010.2048198（JLT 2010）是 DA adaptive receiver，输入/估计器身份不同，且本轮只有
  metadata/abstract 级证据，保留为待确认 near-miss。

未发现 2019+ 外部论文实现“同 receiver-visible 信息 + 同 K/segment 动作粒度”的 adaptive
segmentation，故不触发 `EXISTING_ACTION_COLLISION`。

### 物理前提与历史 exact-action 反证

本地 inventory 的 `a1_adaptive_segmented_cpe` 与 C3 action signature 相同：
`current-window amplitude/SNR/phase proxy → choose K from 8/16/32 → segmented NDA CPE`。
历史 D-011 的量化结果为：

- adaptive-J4 退化为 always-K16，aggregate gain=0.000 dB，0/8 点显著胜 K16；
- 35 点中 K16 在 71% 场景持平 oracle，最强 receiver-visible proxy `|rho|=0.361`；
- tuned VV `Nw=16` 在 200/500 kHz 分别反超 NDA-segmented 14%/68%；
- 实测/演示型星地 FSO 主流 ECL 为 10–80 kHz；唯一显著 oracle 点集中在 1000 kHz 非主流极端条件。

inventory 的 reopen condition 要求同时出现：新的 receiver-visible 信息源、文献支持的主流工况，
以及相对 tuned VV 超过 MDE 的预先证据。本轮文献只支持一般 window tradeoff，没有提供新信息源，
也没有把 ≥200 kHz/1000 kHz 变成主流实测条件，不能满足 reopen condition。

### Abstract / identity 验证边界

- JLT 2020/JLT 2021/JPHOT 2024 的 DOI/year/venue 由 Crossref 独立确认，功能断言来自
  `tools/search` 的 Semantic Scholar abstract；S2 follow-up endpoint 本轮返回 429，未升级到全文证据。
- MDPI/Frontiers 条目的 DOI identity 与功能摘要由 Crossref 再核实。
- Step 1 不把 abstract 结论冒充全文数据流裁决；未进入 Step 2/3。

## 结论

| 四判据 | 预判 | 原因 |
|---|---|---|
| 1. 具体 M-C-A | 表面 PASS | 固定粒度 CPE、Wiener PN/工况、receiver-visible 选 K 均明确 |
| 2. 方法产出形态 | FAIL | 与已否决 exact action 相同，且无新信息源/可实现增量 |
| 3. 近期 baseline | PASS | JLT 2020 fixed-window blind BPS + JLT 2021 补强 |
| 4. 可量化对标 | PASS | BER/SNR penalty/window or memory length 可量化 |

没有形成四判据全 PASS 的 Q#。唯一 terminal：**`PHYSICAL_PREMISE_UNSUPPORTED`**。
C3 在当前冻结物理条件与 receiver-visible 信息下停止；不得进入 Step 2。

## 对决策的影响

新建 D002 记录 terminal。Step 2 合格全文=0、下载失败项=0；这是 Step 1 gate stop，不是获取失败。
返回 RDL 候选池时必须选择机制不同、已有近期合法 baseline、且不复用 adaptive-K action signature 的候选。
