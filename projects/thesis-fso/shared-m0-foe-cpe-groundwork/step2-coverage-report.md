# Step 2 Coverage Report — Shared M0-Power FOE–CPE Groundwork

> 生成: 2026-08-05（初版）| 修订: 2026-08-05（blit 第三轮通道补取 7 篇 IEEE 全文后）
> 阶段: GW Step 2 获取/覆盖面门 | 终态: **STEP2_READY_FOR_USER_CONFIRMATION**
> 任务: T008 Phase C | 依据: `stages/gw-acquire.md`

> **修订说明**（2026-08-05）：初版误判 `tools/blit` "不支持单 DOI 故跳过第三轮"。用户纠正后实测：
> blit 是 query 驱动（`--download DIR` + query 关键词），在校园网代理（`127.0.0.1:7897`）下是 IEEE
> 付费墙论文的有效获取通道。补跑后取回 7 篇高优先 IEEE 全文，含 2 篇最高优先直接竞品。本轮教训
> 已记（凭 `--help` 推断跳过实测 = TL-33 自欺式核查）。

## 0. 覆盖面 terminal（唯一）

**`STEP2_READY_FOR_USER_CONFIRMATION`**（12 篇身份+内容质量合格全文，含 2 篇最高优先直接竞品；
仍列出剩余高优先级获取失败项，等用户确认；**不得自动进 Step 3**）。

---

## 1. 成功获取（身份 + 内容质量合格，共 12 篇）

| # | DOI | 标题（简） | 年/venue | content.md 行数 | PDF SHA256（前12） | 通道 | P1 相关度 |
|---|---|---|---|---|---|---|---|
| 1 | 10.1109/jlt.2018.2831918 | Simplified CR for Intradyne Optical PSK Receivers in udWDM-PON | 2018 JLT | 262 | 0aa071170ba3 | blit-ieee | **HIGH★**（abstract 明言 shares correlation within FOE and CPE blocks）|
| 2 | 10.1109/CSNDSP.2014.6923933 | FOE and CPR for high-order QAM using VV monomial estimator | 2014 CSNDSP | 267 | bf6e2c61a8e6 | blit-ieee | **HIGH★**（method-level 最接近：VV monomial 驱动 FOE+CPR）|
| 3 | 10.1109/lpt.2016.2586076 | Multiplier-Free CPE for Optical Coherent Systems | 2016 PTL | 177 | 4b4a834c4d8b | blit-ieee | HIGH（V&V Mth-power 复杂度高，去乘法器近似）|
| 4 | 10.1109/ISCAS48785.2022.9937906 | Low-latency CPR Hardware (FPGA VV 4th-power) | 2022 ISCAS | 267 | a6e5c2e1f0ca | blit-ieee | HIGH（CPR hw 延迟对标，22-cycle）|
| 5 | 10.1109/LCOMM.2026.3653195 | Low-Complexity CPR Architecture Prefix-Sum+CT-MLE | 2026 CL | 238 | 00ed1876248d | blit-ieee | HIGH（面积↓51% 功耗↓39%，最新 hw CPR 成本数字）|
| 6 | 10.1109/jphot.2022.3161795 | Symmetric TS-Based CFO Estimation coherent FSO | 2022 Photonics J | 278 | e7d281a30fc1 | blit-ieee | HIGH（FSO，明言 avoid time-consuming 4th-power）|
| 7 | 10.1109/TSP.2021.3137966 | Joint ML/MAP Estimation Frequency+Phase Wiener CPN | 2021 TSP | 598 | b75bf346fe76 | blit-ieee | HIGH（joint freq+phase 理论上界，CRLB/BCRLB）|
| 8 | 10.1109/jlt.2019.2892901 | LUT-Free CR for Intradyne Optical DPSK udWDM-PON | 2019 JLT | 201 | cc4e7db37b86 | oa_pdf | HIGH（同族简化 FOE+CPE，FPGA 原型）|
| 9 | 10.1109/JLT.2009.2024963 | DSP for Coherent Single-Carrier Receivers | 2009 JLT | 984 | e520e263d650 | oa_pdf | MEDIUM（canonical FF FOE/CPE DSP 综述，必引基础）|
| 10 | 10.3389/fphy.2023.1099867 | Two-stage freq compensation Doppler BPSK FSO | 2023 Frontiers Phys. | 415 | f5473b9c38b4 | unpaywall | MEDIUM（FSO 两阶段 FOE + 资源节省）|
| 11 | 10.2991/icmmita-16.2016.71 | Low Complexity CPE for 16-QAM Systems | 2016 ICMMITA | 137 | 84c2d5f49f7a | unpaywall | MEDIUM（16-QAM 低复杂度 CPE）|
| 12 | 10.1186/s43593-025-00082-0 | Free-space terabit/s coherent via platicon microcombs | 2025 eLight | 434 | e3002461851a | unpaywall | LOW（FSO coherent 16-QAM context）|

**身份核对**：12 篇 content.md 首部标题/作者/venue 与下载对象一致（blit 的 mismatch 警告均为首页
提取到期刊 header，论文本身正确，已逐篇核验 content.md 首行）；无反爬/登录/目录页。

**内容质量判定（gw-acquire 4 条）**：
1. Step 1 已按 metadata/abstract 列入必读/建议读 ✅
2. 标题/作者/venue/DOI 身份与下载对象一致 ✅（逐篇核验 content.md 首行）
3. content.md ≥50 行、正文非空、非反爬/登录/目录页 ✅（最低 137 行，最高 984 行）
4. provenance 与 SHA256 可审计 ✅（见 `_step2_receipt.json`）

> **本报告不填写 method/dataflow/competitor 的全文语义结论**（属 Step 3）。上述"P1 相关度"列仅
> 复述 Step 1 metadata 级初筛标注 + 首行 abstract 关键短语，非精读结论。

## 2. 内容质量不达标

无（12 篇全部 ≥50 行）。

## 3. 下载失败（用户待获取）

> 修订后：原 14 项失败中，7 篇高优先 IEEE 已由 blit 第三轮补取（见上表 #1-7）。剩余失败项以
> Optica/SPIE/MDPI 为主，P1 相关度中等或偏低。

| 优先 | DOI | 标题 | 年/venue | 与 P1 关系 | 失败原因 |
|---|---|---|---|---|---|
| 中 | 10.1364/OE.25.005217 | Joint CPE+FOE parallel DA-ML DP receiver | 2017 Opt. Express | joint CPE+FOE（DA-ML 非 Mth-power） | Optica OA 链失败，blit 不覆盖 Optica |
| 中 | 10.1364/oe.26.004853 | CFO estimator 16/32-QAM hw perspective | 2018 Opt. Express | FOE hw 分支对标 | Optica OA 链失败 |
| 中 | 10.3390/photonics11090885 | Low Complexity Parallel CFO FSO QPSK-partition | 2024 Photonics(MDPI) | FSO + modified Mth-power FOE | MDPI OA 链失败 |
| 中 | 10.3390/electronics14020265 | noise-tolerant CPR inter-satellite coherent | 2025 Electronics(MDPI) | "resource ↓ 64%" 成本对标 | MDPI OA 链失败 |
| 中 | 10.1117/12.3059522 | Low-complexity CPE space coherent optical | 2025 SPIE | 避免 4th-power | SPIE paywall |
| 低 | 10.1109/jlt.2017.2784804 | Hardware-Efficient Adaptive EQ and CPR 100G WDM-PON | 2018 JLT | "halve redundant compute" | IEEE paywall（blit 未取，可后续补）|
| 低 | 10.23919/saiee.2019.8864145 | Simplified ML-Based CFO+PN | 2019 SAIEE | joint CFO+PN | IEEE paywall |
| 低 | 10.1364/oe.505931 / 10.1364/oe.520452 | Real-time FSO diversity / Enhanced frame sync+CR FSO | 2023/24 Opt. Express | FSO context | Optica |

**失败原因汇总**：Optica/SPIE/MDPI 为主；blit 第三轮已补取所有高优先 IEEE 失败项（7 篇）。
剩余项 P1 相关度中等或偏低，且类别（joint/hw/FSO）已有合格全文覆盖。

## 4. 覆盖面分析

- **精读池结构**：12 篇中，2 篇 HIGH★ 直接竞品（udWDM-PON 2018 implementation-level、CSNDSP 2014
  method-level）+ 6 篇 HIGH（hw/成本/joint/FSO）+ 3 篇 MEDIUM + 1 篇 LOW context。
- **关键未知覆盖**：原"2 篇最高优先直接竞品在 IEEE paywall 后"的系统性偏差**已由 blit 第三轮消除**
  ——Step 3 精读现在能直接读这 2 篇全文，关闭"共享图是否已被传统实现吸收"。
- **技术路线覆盖**：3 语义类（VV/Mth-power/FF-joint、hw-efficient CR、FSO coherent CR）均有 ≥2 篇
  合格全文。
- **下载通道**：OA/unpaywall（5 篇）+ blit-ieee 校园网（7 篇）双通道，IEEE paywall 已打通。

## 5. 引用质量分析

- 正式发表：**12/12 = 100%**。
- 预印本：0 篇。
- 预印本占比：0%。

## 6. 用户行动项

- [ ] **确认覆盖面**：12 篇合格全文（含 2 篇最高优先直接竞品）是否可作为 Step 3 精读起点；
- [ ] 视需要补取剩余 Optica/SPIE/MDPI 中等优先项（非阻塞，类别已有覆盖）；
- [ ] 可选：blit 补取 10.1109/jlt.2017.2784804（"halve redundant compute"）等剩余 IEEE 项。

## 7. Receipt 索引

- 完整 receipt（12 篇 SHA256/bytes/identity）：`search-archive/2026-08-05/_step2_receipt.json`
- blit 第三轮记录：`search-archive/2026-08-05/_blit-r3-csndsp2014.json` / `_blit-r3-udwdm2018.json`
- Step 1 初筛矩阵：`search-archive/2026-08-05/_p1-competitor-shortlist.md`
- 搜索 JSON（4 查询 + 合并）：`search-archive/2026-08-05/r1-*.json` + `_r1_merged_shortlist.json`

> **纪律重申**：本报告未做全文语义精读（Step 3）；所有"与 P1 关系"列复用 Step 1 metadata 标注
> + 首行 abstract 关键短语。Step 3 未授权前不得读全文下方法/数据流/竞品结论。
