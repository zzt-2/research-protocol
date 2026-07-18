# [S012] 批 1+2+3 全文核查审计日志

> 2026-06-23 | 阶段：方法论验证（GW Step 3 精读核查）| 状态：核查完成，Q#-A 重评待用户拍板
> 来源：PROMPT-005 §2 核查清单 + §7.2 三条加严硬规则（全文真实性 / 论文立场不可扭曲 / 孤证就是孤证）
> 执行方：本对话（新对话，接 PROMPT-005 开工）

## 目标

1. 独立 grep 核查批 1+2+3 全部 8 篇报告真实性，不凭信任接受前任（S011 主线）判断
2. 写审计日志逐篇给出 PASS/FAIL/INVALID 判定 + 证据
3. 核查完后诚实重评 Q#-A，给事实 + 选项让用户拍板

## 核查方法

按 PROMPT-005 §7.2 硬规则 11：每篇报告附**文件路径 + 关键论述位置（行号 / 章节 / 原文引用片段）**，报告前 grep 核实论述在文件里真实存在；全文没下载的禁止报"全文层"论述。

每篇核查维度：
- **文件存在性**（ls / find）
- **abstract / 标题真实性**（head + 关键词 grep）
- **batch 报告关键声称是否在全文真实存在**（grep + 原文引用）
- **batch 报告对论文立场的判读是否忠实**（receiving-code-review 纪律 + §7.2 硬规则 12）

---

## 论文 #444 qBeam（批 1）

- **文件路径**: `papers/downloads/2026-06-22/11443150.md`（44,974 字节，2026-06-22 下载）
- **核查方法**: head 看标题/abstract + grep `APD|burst|interleav|DVB|FEC|PER|fade|turbulen|failure|limit`
- **核查结果**: ✅ **PASS**（全文真实 + abstract 立场核实）
- **关键论述核实**:
  - 标题真实："Forward Error Correction Considerations for Optical Satellite Links"（IEEE ICSOS 2025）
  - 作者真实：Eugenio Estinto / Scott Allwine / Luca Estinto（**qBeam 公司全员**，厂商身份确认）
  - **abstract line 7 原文**："This paper will propose that **treating optical communications in the same manner as RF satellite links is usually not the best approach from a FEC-selection perspective**. This is due to the unique properties of optical detectors and the atmospheric turbulence effects"
  - **line 29 原文**："Conventional FEC techniques used for RF links are **not very effective** against optical fading scenarios, as they were mostly designed for the **additive white Gaussian noise (AWGN) channel**"
  - line 25: 空对地链路有大气湍流 fading
- **跟前任报告差异**: 无。批 1 报告"#444 qBeam 给四层失效机制 + 三方 APD 实测 + 第三方 modem PER 对比"——abstract 立场确实支持 Q#-A（RF-derived FEC 在 FSOC fade 场景不够）。**Q#-A 的真正来源就是这篇**。
- **诚实警告**: 厂商夸大动机——qBeam 在卖 fade-tolerant optical modem，"RF-derived FEC 不够"立场对其有利。**厂商论文不能单独采信**（§7.2 硬规则 13）。

## 论文 #516 Youssef（批 1）

- **文件路径**: `papers/doi/10.1186_s13638-023-02285-w/content.md`（55,403 字节）
- **核查方法**: head + grep `WBF|BWBF|RRWBF|baseline|oscillat|offline|threshold mismatch`
- **核查结果**: ✅ **PASS**（全文真实 + 立场核实）
- **关键论述核实**:
  - 期刊：EURASIP Journal on Wireless Communications and Networking（2023:78）—— **合法期刊非低质量**
  - 标题真实："Bootstrapped low complex iterative LDPC decoding algorithms for free-space optical communication links"
  - **line 191**：RRWBF + Implementation Efficient Reliability Ratio WBF = Algorithm (2)
  - **line 223**：oscillation phenomena（译码算法本身在迭代中的振荡现象）
  - **line 241**："A significant deficiency of the **Bootstrapped WBF (BWBF) algorithm**... determined the threshold value β **offline**... leads to massive complexity"——**BWBF 算法离线算阈值 β 复杂度高**
- **跟前任报告差异**: 无。批 1 报告"#516 给 WBF 振荡"正确。**PROMPT §1.1 表格"#516 不直接相关（译码算法内部改进）"判断也对**——论文主题是 LDPC **译码算法内部改进**（WBF/BWBF 振荡 + 阈值离线复杂度），不是"baseline FEC 在大气湍流下失效"。
- **对 Q#-A 影响**: **不直接支持 Q#-A**。Q#-A 是"RF-derived FEC（DVB-S2/BCH/RS/interleaving）在 FSOC fade 场景不够"，#516 是"LDPC **译码算法** WBF/BWBF 在 FSO 信道下的振荡 + 阈值复杂度"——不同角度。

## 论文 #80 Kotake（批 1）

- **文件路径**: `papers/downloads/2026-06-22/11443166.md`（33,374 字节）
- **核查方法**: head + grep `RS\(255|DVB-S2|LUCAS|NICT|JAXA|Reed-Solomon`
- **核查结果**: ✅ **PASS**（全文真实 + 立场核实）
- **关键论述核实**:
  - 标题真实："Experimental Demonstration of Next-Generation FEC-Coded Data Transmission for GEO Satellite-to-Ground Laser Link Using LUCAS Onboard the Optical Data Relay Satellite"（IEEE ICSOS 2025）
  - 作者：NICT（Wireless Networks Research Center）+ JAXA + Nagoya Institute of Technology——**三方独立机构**（非厂商）
  - **abstract line 31 原文**："**DVB-S2 and 5G NR LDPC** codes have been employed as next-generation FEC schemes, both with interleaving. For comparison, a conventional **Reed Solomon (RS) code** with interleaving has also been utilized. The experimental results have demonstrated that **both codes successfully corrected burst errors caused by fades due to atmospheric turbulence**, thereby improving BER performance, **in comparison with RS code**. Among both codes, **DVB-S2 exhibited stronger error correction capability** than 5G NR LDPC"
  - 场景：**GEO-to-ground**（LUCAS onboard 光数据中继卫星）—— 大气湍流场景
- **跟前任报告差异**: 无。批 1 报告"#80 给 RS 弱"正确。PROMPT §1.1 表格"#80 结论 'DVB-S2 > RS'——支撑 RS 弱（Q#-B），DVB-S2 是改进方不是被批对象"判断**完全正确**。
- **对 Q#-A 影响**: **不直接支持 Q#-A**。#80 显示 **DVB-S2 + interleaving 在 GEO-to-ground 大气湍流下成功纠正 burst errors**，且强于 RS——这恰恰**反驳** Q#-A"DVB-S2 这套 RF-derived FEC 在 FSOC fade 场景失效"。**#80 支持 Q#-B（RS 弱），不支持 Q#-A（DVB-S2/RF-derived 失效）**。

## 论文 #293 Okamoto（批 2）

- **文件路径**: `papers/downloads/2026-06-23/10294033.md`（30,836 字节）
- **核查方法**: head + grep `BSC|binary symmetric|inter-satellite|AWGN|LLR|variance`
- **核查结果**: ✅ **PASS**（全文真实 + 立场核实 + **场景错位确认**）
- **关键论述核实**:
  - 标题真实："Performance Comparison of Channel Coding Methods for Optical Satellite Data Relay System"
  - 作者：Nagoya Institute of Technology + JAXA
  - **line 55 原文**："The optical **intersatellite link** is assumed to be a **binary symmetric channel (BSC)** with an error probability p"
  - **line 89 原文**："Note that the results of Condition 1 are **not limited to optical links**, but are **generally applicable to relay transmission in BSC and AWGN channels**"
  - 论文用 Polar / LDPC / DVB-S2 / Turbo / BCH 在 **BSC + AWGN** 信道上对比
- **跟前任报告差异**: 无。PROMPT §1.1 表格"#293 Okamoto 场景错位（ISL 无湍流，用 BSC）"判断**完全正确**。**这是 JAXA 光数据中继系统研究，ISL = LEO→GEO 无湍流 BSC，Ka-band feeder = AWGN——完全不在 atmospheric turbulence fading 场景**。
- **对 Q#-A 影响**: **场景错位，不构成 Q#-A 证据**。

## 论文 #430 Dowhuszko（批 2）

- **文件路径**: `papers/downloads/2026-06-23/9013421.md`（35,879 字节）
- **核查方法**: head + grep `HPA|MZM|DPD|predistortion|turbulence.*dB|fade|fading channel`
- **核查结果**: ✅ **PASS**（全文真实 + 立场核实 + **场景错位确认**）
- **关键论述核实**:
  - 标题真实："Total degradation of a DVB-S2 satellite system with analog transparent optical feeder link"
  - 作者：CTTC（Barcelona）+ ESTEC/ESA——**ESA 项目**
  - **abstract line 11 原文**：研究 HTS 系统用 transparent optical feeder link 传 DVB-S2 信号，**主要非线源是 optical MZM（gateway）+ HPA（satellite）**
  - **line 117 原文**："we tackle this issue by **reserving few dBs of the optical feeder link budget as system losses**, to address the effect of turbulence on the optical signal"——**turbulence 只是预算中预留 dB 数，不建模 fading**
- **跟前任报告差异**: 无。PROMPT §1.1 表格"#430 Dowhuszko 场景错位（turbulence 折 dB 不建模 fading）"判断**完全正确**。论文重点 = MZM + HPA 非线性失真 + DPD 补偿，**不在 fading 场景**。
- **对 Q#-A 影响**: **场景错位，不构成 Q#-A 证据**。

## 论文 附录2020 Nguyen（批 2）

- **文件路径**: `papers/doi/10.30534_ijatcse_2020_126922020/content.md`（30,663 字节）
- **核查方法**: head + grep `AWGN|Polar|LDPC|IJATCSE|Table 1|burst`
- **核查结果**: ✅ **PASS**（全文真实 + 立场核实 + **低质量期刊确认 + 内容方向部分命中**）
- **关键论述核实**:
  - 期刊：**International Journal of Advanced Trends in Computer Science and Engineering (IJATCSE)**, 9(2), 2020, ISSN 2278-3091——**低质量期刊**（warse.org，predatorial 嫌疑）
  - 作者：Vietnam 多机构 + FPT University + SKKU + Kookmin——**非主流机构**
  - **line 3-23 原文**：Polar codes vs LDPC codes 在 OSC（optical satellite communication）信道对比
  - **line 33 原文**："A conventional error correction codes (ECC) is **not suitable** for overcoming the large size of burst error"
  - **abstract line 23 原文**："the conventional form of both codes **cannot overcome the fading noise due to atmospheric turbulence**. Therefore, **interleaving is applied**... The gain is **2 dB** at the BER of 10⁻³"
- **跟前任报告差异**: 无。PROMPT §1.1 表格"附录2020 低质量期刊（IJATCSE 边缘 + Table 1 标题错位 peer review 失效硬证据），内容上复现但不能单独采信"判断**完全正确**。
- **对 Q#-A 影响**: **内容方向部分命中但低质量，不能单独采信**。Nguyen 重点是"Polar vs LDPC 对比 + interleaving 增益 2dB"，**不是直接判 DVB-S2/RF-derived FEC 失效**——角度有重合但不完全同 Q#-A。

---

## 候选 1 Elzanaty（批 3）— **核心核查发现：PROMPT-005 §1.1 判断部分错误**

- **文件路径**: ⚠️ **PROMPT-005 §1.1 称"全文没下载"——这是错的**。文件真实存在：
  - `papers/arxiv/2005.02129/content.md`（105,062 字节，2026-06-16 下载）
  - arxiv_id: 2005.02129
  - **作者真实**：Ahmed Elzanaty + Mohamed-Slim Alouini（**都在 KAUST**）—— 完全匹配 PROMPT §1.1 引用的"ELZANATY A, ALOUINI M S. Adaptive coded modulation for IM/DD free-space optical backhauling: a probabilistic shaping approach[J]. IEEE Transactions on Communications，2020，68（10）：6388-6402"
  - **arxiv 2005.02129 就是 IEEE TCOMM 2020 那篇的 arxiv 预印本**
- **核查方法**: head + grep `elzanaty|alouini|probabilistic shaping|IM/DD|backhaul` + sed 看具体行号
- **核查结果**: ⚠️ **PARTIAL FAIL**（PROMPT §1.1 "全文没下载" 判断错；批 3 报告 line 编号真实但**数字部分失实**）
- **关键论述核实（修正后）**:
  - **line 51 真实存在**，末段原文："The scheme further assumes an AWGN channel, **which does not account for the rate adaptability to cope with the diverse channel conditions with turbulence-induced fading** in FSO channels" —— **Elzanaty 自己批了 AWGN 假设**
  - **line 55 真实存在**：fiber-optical 的 PAS scheme 不能直接扩展到 IM/DD（"the PAS can not be directly extended to IM/DD in FSO channels, as the constellation symbols are constrained to be non-negative"）
  - **line 111 真实存在**：unipolar MPAM 信号没已知高效 PS 方案
  - ❌ **"量化 1.3-2.5 dB" 数字部分失实**——全文 grep `[0-9]+\.?[0-9]*\s*dB` 找不到 1.3-2.5 区间。论文实际数字：line 51 "around 1 dB"（other 工作 uniform signaling 增益）+ line 340 "up to 2 dB"（PS 相比 uniform 节省发射功率）
- **跟前任报告差异**:
  - 批 3 报告称"line 51 批 AWGN + 量化 1.3-2.5 dB + PAS line 55/111" → **line 51/55/111 真实存在方向正确，但 "1.3-2.5 dB" 是两个不同来源数字的合并 + 编造区间**
  - PROMPT-005 §1.1 称"全文没下载，line 编号编的" → **错**。全文真实存在（`papers/arxiv/2005.02129/`），line 编号方向正确（但数字部分批 3 报告自己编造）
- **对 Q#-A 影响（这是核查的关键转折点）**:
  - **Elzanaty 主题是 IM/DD + PAS（probabilistic shaping）for FSO backhauling**，**不是 DVB-S2/BCH/RS/interleaving 这套 RF-derived FEC**
  - Elzanaty 批的是"先前工作假设 AWGN（无湍流）" + "PAS 不能直接用于 IM/DD"，**提出的方法是 PAS + CCDM + FEC encoder 组合**（新方法，不是批 RF-derived FEC）
  - **Elzanaty 立场跟 Q#-A"RF-derived FEC（DVB-S2/BCH/RS/interleaving）在 FSOC fade 场景失效"不同构** —— Elzanaty 是"现有 PS 方案在 IM/DD 不行"，Q#-A 是"RF-derived FEC 在 fade 场景不行"
  - **弱相关**：Elzanaty 也提到"现有 scheme 假设 AWGN 不 cope with turbulence-induced fading"——这点跟 Q#-A 信号方向同构，但不是同一个 baseline，不是同一套方法
  - **不构成 Q#-A 的第三方独立复现**（不是 RF-derived FEC 失效证据，是 PS 在 IM/DD 受限证据）

---

## 候选 2 Korevaar（批 3）— **PROMPT-005 §1.1 造假 2 判断正确**

- **文件路径**: `papers/downloads/2026-06-23/10491215.md`（39,799 字节）
- **核查方法**: head + grep `limiting factor|remain.*limit|negligible|RF user|amplifier`
- **核查结果**: ✅ **PASS**（全文真实 + **立场反驳 Q#-A 确认**）+ §1.1 造假 2 判断正确
- **关键论述核实**:
  - 标题真实："Terabit Optical Feeder Links for DVB Satellite Systems: Real-time End-to-End Communication System Design & Field Test Results"（IEEE ICSOS 2023）
  - 作者：TNO（Netherlands Organisation for Applied Scientific Research）+ Celestia STS——**非厂商研究机构**
  - **abstract line 13 原文**："4. ensuring that the OFL-induced degradations on the end-to-end performance are **negligible** such that **the usual suspects – the RF user downlink and the RF amplifier – remain the limiting factors**"
  - **line 235 conclusion 再次确认**："the OFL-induced penalties are negligible and that the usual RF suspects... remain the limiting factors"
  - 9.8km ground-to-ground 实测：20 dB fading penalty → 通过 DVB-S2 + DDR interleaving + 16APSK + 28Gbps 取得 10 dB coding & diversity gain
- **跟前任报告差异**:
  - 批 3 报告称"复现带条件 + DVB LDPC+BCH 单独不够" → **立场扭曲确认**：line 16893 局部"DVB LDPC+BCH 单独不够"是子段推论，但 abstract + conclusion 整体立场是"**经过合理设计 RF-derived FEC（DVB-S2 + DDR interleaving）是够的**，OFL 退化可忽略"
  - PROMPT-005 §1.1 造假 2 判断**完全正确**（§7.2 硬规则 12：禁止只引用局部论述隐去整体结论）
- **对 Q#-A 影响**: **立场反驳 Q#-A**。Korevaar 是**经验性证据**：经过设计 RF-derived FEC（DVB-S2 + DDR interleaving）在 OFL（feeder link）场景下能取得 10 dB coding gain，OFL 退化可忽略——**反驳 Q#-A"RF-derived FEC 在 FSOC fade 场景失效"**。
- **场景补充（诚实警告）**:
  - Korevaar 场景是 **OFL feeder link**（ground-to-ground 9.8km 模拟 GEO feeder），**不是 #444 的 LEO-to-ground 场景**
  - 严格说 Korevaar 反驳 Q#-A 也有场景偏差（feeder link 不等于 user link）
  - **但**：Korevaar 比 #444 厂商论文独立性强（TNO 非厂商 + ESA 合作），实测数据硬，仍是 Q#-A 的强力反证

---

## Q#-A 重评（基于核查后事实）

### Q#-A 原定义（批 1 报告）

"RF-derived FEC（DVB-S2 / BCH / RS / interleaving）在 FSOC atmospheric turbulence fade 场景下失效/不够，需要新的 fade-tolerant FEC"

### 核查后事实矩阵

| 论文 | 真实性 | 立场 | 对 Q#-A |
|---|---|---|---|
| #444 qBeam | ✅ 真实 | 厂商立场：RF-derived FEC 在 FSOC fade 不够 | **支持但厂商夸大动机**（孤证） |
| #516 Youssef | ✅ 真实 | LDPC 译码算法内部改进（WBF 振荡） | **不直接支持**（角度不同） |
| #80 Kotake | ✅ 真实 | DVB-S2 + interleaving **成功**纠正 burst errors，强于 RS | **反驳 Q#-A**（DVB-S2 在 GEO-to-ground 够） |
| #293 Okamoto | ✅ 真实 | ISL = BSC + AWGN，无湍流场景 | **场景错位**（不构成证据） |
| #430 Dowhuszko | ✅ 真实 | MZM + HPA 非线性 + turbulence 折 dB | **场景错位**（不构成证据） |
| 附录2020 Nguyen | ✅ 真实 | Polar vs LDPC + interleaving 2dB 增益 | **内容方向部分命中但低质量**（不能单独采信） |
| **候选 1 Elzanaty** | ⚠️ PROMPT §1.1 误判（全文真实存在） | **IM/DD + PAS 主题，不是 RF-derived FEC**；批 AWGN 假设但角度不同 | **不构成 Q#-A 第三方复现**（角度不同构） |
| **候选 2 Korevaar** | ✅ 真实 | **经过设计 RF-derived FEC 够用**（OFL 退化可忽略） | **反驳 Q#-A**（强力反证，TNO 非厂商 + 实测） |

### Q#-A 真实状态（核查后）

**Q#-A = 仍是孤证**，且**比 PROMPT-005 §1.1 判断更弱**：

- **唯一支持**：#444 qBeam 厂商论文（夸大动机）
- **弱支持**：附录2020 Nguyen（低质量，内容方向部分命中）
- **反驳证据**：#80 Kotake（DVB-S2 够用）+ 候选 2 Korevaar（RF-derived FEC 够用，TNO 非厂商实测）
- **场景错位**：#293 / #430
- **角度不同构**：#516（译码算法）/ 候选 1 Elzanaty（IM/DD PAS）

**PROMPT-005 §3.2 预期结论"Q#-A 大概率孤证" → 核查后确认**：Q#-A 是孤证，且**有 2 篇独立反驳证据**（#80 Kotake + 候选 2 Korevaar），比预期更严重。

### 按 PROMPT §3.1 重评标准

| 状态 | 判读 | 下一步 |
|---|---|---|
| 核查后 Q#-A 有 ≥2 篇高质量独立第三方支持 | 弱热点成立 | ❌ 不满足（0 篇独立支持）|
| 核查后 Q#-A 只有 #444 厂商孤证 + 附录2020 低质量 | **孤证判不过判据 A** | ✅ **满足此状态** |
| 核查后 Q#-A 状态模糊 | 不确定 | ❌ 不满足（清晰是孤证）|

**Q#-A 判读：孤证判不过判据 A，诚实放弃**（§7.2 硬规则 13：孤证就是孤证）。

---

## 核查方法论价值（S001 验证标准反馈）

| 阶段 | 看方法论什么 | 本轮表现 |
|---|---|---|
| PROMPT-005 §1.1 是否准确 | 交接文档事实准确性 | **部分错**——候选 1 Elzanaty "全文没下载" 判断错（全文真实存在 `papers/arxiv/2005.02129/`）。说明**即使是主线写的交接 PROMPT 也必须独立 grep 核查**，不能凭信任接受 |
| §7.2 硬规则 11 是否有效 | 全文真实性核查纪律抓造假 | **有效**——独立 grep 抓出 PROMPT §1.1 自己的误判（Elzanaty 全文真实存在），同时确认批 3 报告的 line 编号方向真实但数字部分编造 |
| §7.2 硬规则 12 是否有效 | 论文立场不可扭曲纪律 | **有效**——Korevaar 立场核查确认 abstract 原文"RF 仍是限制因素"反驳 Q#-A，批 3 报告扭曲立场确认 |
| §7.2 硬规则 13 是否有效 | 孤证就是孤证纪律 | **有效**——Q#-A 经核查确认是孤证（#444 厂商）+ 反驳证据 2 篇（#80 + Korevaar），不硬留 |

**核心教训（新增）**：

1. **核查机制必须应用到所有层级**——不仅核查执行对话报告，也要核查主线写的 PROMPT。本次核查发现 PROMPT-005 §1.1 自己也对候选 1 Elzanaty 做了误判（"全文没下载"），如果没有 §7.2 硬规则 11 强制独立 grep，会照 PROMPT 走而漏掉真相。
2. **核查发现的真相不一定有利于"放弃 Q#-A"**——Elzanaty 全文真实存在但**主题角度跟 Q#-A 不同构**（IM/DD PAS 不是 RF-derived FEC），所以即使纠正了 PROMPT 误判，Q#-A 仍是孤证。**核查是中性的——发现造假要纠正，发现"被冤枉的造假"也要纠正**。
3. **批 3 报告部分真实部分失实**——line 51/55/111 真实存在方向正确（Elzanaty 确实批了 AWGN 假设），但"1.3-2.5 dB" 数字部分编造（论文只有 "1 dB" + "2 dB" 两个不同来源数字）。**部分真实不等于整体可信**——必须逐项核查。

---

## 决策引用

- **topic-index 不变量 1**（方法论验证优先 / 颗粒无收好过凑数）
- **topic-index 不变量 4**（判据 A 是 Go/No-Go 最高层）
- **PROMPT-005 §7.2 硬规则 11/12/13**（全文真实性 / 论文立场不可扭曲 / 孤证就是孤证）
- **receiving-code-review 纪律**：不盲从主线/PROMPT/前任判断，独立 grep 核实

## 范围确认

- 本轮在 scope boundary 内：核查批 1+2+3 + 诚实重评 Q#-A = GW Step 3 精读阶段的质量门控（PROMPT §5 明确范围）
- 没有扩大范围：核查 + 重评不涉及选地/换地/进四判据，是 Step 3 内部质量保证

## 后续

### 给用户的选项（Q#-A 重评后）

按 PROMPT §6 停点纪律"不替用户判 Q#-A 放弃/继续"——给事实 + 选项让用户拍板：

**事实**：Q#-A 经独立核查确认 = 孤证（#444 厂商）+ 2 篇独立反驳证据（#80 Kotake GEO-to-ground DVB-S2 够用 + Korevaar TNO OFL RF-derived FEC 够用）+ 2 篇场景错位 + 2 篇角度不同构。**判不过判据 A**。

**选项**（建议按推荐序）：
- **A（推荐）：诚实放弃 Q#-A，回选地或换子地带**——按 §7.2 硬规则 13 + 不变量 1（颗粒无收好过凑数）
- **B：先跟导师沟通 RF-derived FEC 这个角度**——如果导师有"在 LEO-to-ground 强湍流场景 RF-derived FEC 失效"的领域知识，可能补一个角度。但用户之前明确"老师不会同意"边界已锁，这条不建议
- **C：继续精读 #444 qBeam 全文（除 abstract 外的 §I/§IV/§V/§VI 四层失效机制 + APD 实测 + 第三方 modem PER 对比）**——看厂商论文里有没有引用第三方独立复现。**但厂商论文引用本身就是利益相关，不值得作为补孤证手段**

### 不在本轮范围（防顺手扩）

- ❌ 不进四判据终审 / Go/No-Go（Q#-A 重评后由用户决定）
- ❌ 不写 S012 之外的 session note（S012 是核查审计，本文件）
- ❌ 不 commit（PROMPT §6 停点：核查期任何产出都不锁进 git）
- ❌ 不替用户判 Q#-A 放弃/继续（核查完后给事实 + 选项，用户拍板）

## 跨对话续接必读

1. 本文件 S012（核查审计完整记录）
2. PROMPT-005（执行规范，但 §1.1 候选 1 Elzanaty 判断需修正为"全文真实存在"）
3. topic-index 不变量段 + 其他结论段
4. 批 1+2+3 全部报告（核查对象，已在 S012 内重新核实）
