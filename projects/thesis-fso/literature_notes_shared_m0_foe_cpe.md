# Literature Notes — Shared M0-Power FOE–CPE Groundwork

> Project: thesis-fso | 子方向: Ch5 工程方法候选 P1（Shared Raised-Power Compute Graph）
> 状态: GW Step 1–2 已完成并验收（T008，V002 PASS；Step 2 终态 = STEP2_ACCEPTED_READY_FOR_STEP3）| 最后更新: 2026-08-05
> **本轮只到 Step 2 覆盖面门；Step 3 精读条目待后续授权专题建立，本文件不得伪造精读内容。**

## 0. 研究对象（冻结，仅用于检索/获取）

- **M**：当前串行 NDA carrier recovery 先用 M0 次幂做 FOE，再对 CFO 补偿信号重做 M0 次幂做 CPE。
- **C**：资源受限的软件或硬件实现，要求与当前 receiver 输出/BER 匹配。
- **A**：用一个共享 M0-domain 表示同时驱动 FOE 与 CPE；升幂域 CFO 去除用
  `raised * exp(-j*M0*omega*k)`，原信号域补 `omega*k + phi`。

## 1. GW Step 进度表

| Step | 状态 | 完成日期 | commit | 关键产出 | 下游门控 |
| ---- | ---- | -------- | ------ | -------- | -------- |
| 1 search | ✅ | 2026-08-05 | — | search-archive/2026-08-05/ 4 `r1-*.json`（97 去重）+ 全局索引复用筛选；初筛矩阵见 `search-archive/2026-08-05/_p1-competitor-shortlist.md` | 进 Step 2 前 Step 1 必 ✅（已满足） |
| 2 acquire | ✅（已验收，V002 PASS） | 2026-08-05 | — | **12 篇合格全文**（`papers/doi/`，含 2 篇 HIGH★ 直接竞品）；receipt + coverage report 见 `shared-m0-foe-cpe-groundwork/step2-coverage-report.md`；terminal=`STEP2_ACCEPTED_READY_FOR_STEP3` | **进 Step 3 须用户新对话显式授权** |
| 3 read | ⬜ 未授权 | | | （本轮不得建精读条目） | — |
| 3.5 supplement | ⬜ 未授权 | | | | — |
| 4a feasibility | ⬜ 未授权 | | | | — |

> FR-22 跨 Step 硬门控：Step 2 覆盖面已验收（V002 PASS），但 Step 3 仍须用户新对话显式授权才可启动；禁止跳过授权进 Step 3/3.5/4a/MVE/Contract。

## 2. Step 1 候选初筛（metadata/abstract 级，非精读结论）

> 以下仅为 Step 1 metadata/abstract 级初筛，标注优先级；**不得当作 Step 3 精读后的方法/数据流/
> 竞品结论**。详细矩阵见 `search-archive/2026-08-05/_p1-competitor-shortlist.md`（Step 1 末产出）。

**检索质量门槛**（gw-search.md）：**raw=100 → dedup=97**（≥20 ✅）；实际贡献候选的 API 源 3 类
（Semantic Scholar / OpenAlex / SerpAPI-scholar，4 查询通道均调用但 Exa 贡献 0）（≥3 ✅）；
publication_status = published 59 / unknown 36 / preprint 2，**可直接证明的正式发表率下限 =
59/97 = 60.8%**（≥50% ✅，unknown 不计入分母）；3 语义类全覆盖（≥2 ✅）；必读 ≥12（≥5 ✅）。

**HIGH-RELEVANCE 直接对标（优先 Step 2 获取）**：
- udWDM-PON Simplified CR PSK（10.1109/JLT.2018.2831918）— abstract 明言 shares correlation within
  FOE and CPE blocks（implementation-level 最接近，但用 correlation 非 Mth-power）
- udWDM-PON LUT-Free CR DPSK（10.1109/jlt.2019.2892901）— 同族简化，FPGA 原型
- FOE+CPR via VV monomial（10.1109/CSNDSP.2014.6923933）— method-level 最接近（同 VV monomial 驱动 FOE+CPR）
- Low-complexity joint FOE+CPE QPSK-partition DP-16QAM（10.1364/OFC.2013.OTU3I.5）
- Joint CPE+FOE parallel DA-ML（10.1364/OE.25.005217）
- FSO inter-satellite noise-tolerant CPR（electronics 14020265）— "resource ↓ 64%" 成本对标
- sat-ground VV FF cascade double-feedback（2023, 22 cites）
- Low-complexity CPE space coherent（10.1117/12.3059522）— 避免 4th-power（同成本动机）

**metadata 级 Step 1 结论**（不当 Go/Kill）：文献空间存在（成熟活跃领域）；P1 数据流共享的具体 claim
在 metadata 级未被显式覆盖（最接近是 method-level，非 implementation-level 共享图）；是否构成可区分
工程 claim **必须由 Step 3 精读全文关闭**。

## 3. Step 2 获取状态

**12 篇合格全文**（identity/≥50 行/SHA256 全过），通道：OA/unpaywall 5 篇 + blit-ieee 校园网 7 篇。
含 2 篇最高优先直接竞品（已消除原 IEEE paywall 系统性偏差）：
- HIGH★ udWDM-PON 2018（10.1109/jlt.2018.2831918）— shares correlation within FOE+CPE blocks
- HIGH★ CSNDSP 2014（10.1109/CSNDSP.2014.6923933）— VV monomial 驱动 FOE+CPR

其余 HIGH：PTL 2016 multiplier-free CPE、ISCAS 2022 FPGA VV、CL 2026 prefix-sum CPR（面积↓51%）、
PhotonicsJ 2022 FSO CFO（avoid 4th-power）、TSP 2021 joint ML/MAP 理论上界、JLT 2019 LUT-Free DPSK。
完整 receipt 见 `search-archive/2026-08-05/_step2_receipt.json`，覆盖面报告见
`shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。

（全文语义结论属 Step 3，本文件不写）

## 4. 综合分析

（属 Step 3 精读产出；本轮不写。本轮不得出现"该论文共享了 X"等全文语义断言。）
