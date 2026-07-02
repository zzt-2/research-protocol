# [S030] 载波同步 D015 v2（D017）判读层 B11/B12 + 拉总表（D018 新模式收尾）

> 2026-07-02 | 块 E Step 4a 载波同步 v2 判读层 | 状态：B11/B12 中性提取完成，**B 档 12 篇全摸完**，总表落盘交用户排优先级
> 来源：续接 H019（按 D018 新判读模式中性提取判 B 档剩 2 个 + 拉总表）

## 目标

执行 H019"下一步"：①按 **D018 新判读模式（中性提取）** 判 B 档最后 2 个（B11 NDA-ML STO+CPE / B12 频域 pilot 相位噪声）②2 个摸完后拉 **B 档 12 + C 档 4 + D 档星地候选** 总表给用户排优先级（用户 2026-07-02 拍"全部入总表"）。守 AGENTS.md 单对话 3 步上限（判 2 个 + 拉总表 = 收尾对话）。

## 记录

### 阶段 1：报到 + H019 接收验证（Trigger 1+5）

报到读：topic-index（不变量 8 条，D005 务实路线最高优先级）+ S029 + S028（含追加中性还原表）+ R004 + D018 + D017 + D006 + D005（decisions.md）+ voice.md（2026-07-02 段 4 条）+ profile.md + 本 H019。

**H019 接收方验证清单全过**（6 项核查全 PASS）：
- S029 B8/B9/B10 三篇中性提取 5 字段表（S029 L74-80）：**PASS**
- 主线 grep 核查 9 项关键声称全 PASS 无造假（S029 L56-69）：**PASS**
- B 档剩 2 个 B11/B12（S029 L106-108 + topic-index L133）：**PASS**
- 接口变更：无代码改动（H019:106）
- _registry depends_on/conflicts_with：none
- 范围未违反"明确不含"（不预设立 Q#、不改框架、不跑出星地激光通信大背景）

**Inflation check**：S### = 29（≥15 阈值）。本轮是 D017/D018 既定的载波同步 v2 判读层延续（H019 明确"下一步判 B11/B12"），非范围扩张，**如实标注不阻断**（与 S027/S028/S029 处理一致）。

**Profile 感应**：voice.md 2026-07-02 段无新增 profile 级纠偏模式（D018 第 6 次验证已在 profile 反映），不更新 profile。本轮守：①严格守 3 步上限（判 2 个 + 拉总表 = 收尾）②D018 中性提取不边摸边 Kill ③单 subagent 不看太多 ④总表范围 B12+C4+D星地候选（不只 B 档，防主线又收窄隐形排除 C/D）。

### 阶段 2：下载 B11/B12（blit IEEE 机制，2 篇全成功）

**预检查**：B11/B12 目录只有 metadata.json（download_status=failed，all_failed——urllib 不走代理 + IEEE paywall，S029 同款已知债务）。

**按 H019 纪律 5"下载失败穷尽途径再标失败"**，派 1 子 agent 穷尽降级源。

**子 agent 下载结果（2 篇全成功）**：

| 候选 | DOI | 降级源尝试链 | 成功路径 |
|---|---|---|---|
| **B11** | 10.1109/LPT.2024.3523478 | Unpaywall/OpenAlex/S2/Zenodo/arXiv 全无 OA → blit IEEE `--download` getPDF.jsp 触发 404 → curl getPDF.jsp=418 → **自写 Playwright 干净 session（先 goto IEEE 首页过 418 challenge，再请求 getPDF.jsp(arnumber=10816633)）✅**| papers/doi/10.1109_LPT.2024.3523478/source.pdf (1.78MB) + content.md (22KB) |
| **B12** | 10.1109/tcomm.2022.3171809 | 全无 OA → blit IEEE 标题搜索 0 条（IEEE 搜索排名）→ curl getPDF.jsp=418 → **直接用 arnumber 9766225 走自写 Playwright 干净 session ✅**| papers/doi/10.1109_TCOMM.2022.3171809/source.pdf (1.33MB) + content.md (63KB) |

**关键发现（S029 B8 结论延伸）**：代理 7897 对 IEEE paywall 有效，但 **blit 自带 `--download` 通道不稳**（B11 getPDF 触发 404 / B12 搜索找不到）。起作用的是"**Playwright 浏览器先访问 IEEE 首页建立 session（过 418 反爬 challenge）→ 再请求 getPDF.jsp**"。curl/urllib 直连 getPDF 一律 418。**tools/download --doi 全 fail 根因不变**（urllib 不走代理）。子 agent 自写 Playwright 脚本是更可靠的 IEEE 下载通道（用 arnumber 直请 getPDF.jsp）。

**标题核验**：
- B11 首页 "Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems"（DOI 一致）
- B12 首页 "Estimation of Phase Noise Based on In-Band and Out-of-Band Frequency Domain Pilots"（Björn Gävert & Thomas Eriksson, Ericsson/Chalmers，DOI 一致）

### 阶段 3：子 agent 中性提取（D018 新格式，守禁做项）

派同一子 agent 对 2 篇落盘全文做中性信息提取，填 5 字段表（做了什么/报了啥增量/撞 D006/星地关系/备注）。

**子 agent 守 D018 禁做项**：①不用 A2/A3 硬门槛提前砍 ②不判 Go/Kill ③不下领域级结论。每条关键声称 grep content.md 标 line 号（FR-26 + §7.2）。

### 阶段 4：主线 grep 独立核查（§7.2 防造假 + 核查机制中性双向）

**逐项 grep 核查子 agent 关键声称（全 PASS 无造假）**：

| 候选 | 声称 | 核查 | 结果 |
|---|---|---|---|
| B11 | L33"atmospheric turbulence...totally compensated"（不撞 D006）| sed L33 逐字命中"Assuming that the atmospheric turbulence effect, pointing error, Doppler shift and CFO have been totally compensated" | **PASS** |
| B11 | M-APSK + fiber+FSO 双适用（L9/L29）| sed L9/L29 摘要 + intro 逐字命中 | **PASS** |
| B11 | 2dB SNR gain vs DA ML @ (8,8)-16APSK 7% HD-FEC（L181/L191）| grep "2 dB" 命中 L181"DA ML method exhibits a 2 dB SNR drop compared to our approach at the 7% HD-FEC threshold for (8,8)16APSK" + L191"2 dB SNR gain" | **PASS** |
| B11 | satellite/downlink/LEO 关键词全未命中 | grep "satellite\|downlink\|geostation\|LEO" 全文 0 命中（场景是 FSO 但非星地）| **PASS** |
| B11 | turbulence 仅 L15 背景 + L33 假设已补偿 | grep "turbulence\|atmospheric" 命中 L15（背景物理来源）+ L33（假设已补偿）| **PASS** |
| B12 | turbulence/satellite/FSO/atmospheric 全文零命中 | grep 全文 0 命中（L545 引用文献 [11] 标题含 transmission 不算）| **PASS** |
| B12 | wireless 主场景（L11/L15）| grep "wireless" 命中 L11 Index + L15 intro + L533 ref | **PASS** |
| B12 | Wiener 相噪模型（L117-121）| grep "wiener\|random walk" 命中 L29/L117/L573 | **PASS** |
| B12 | 无系统级 dB/BER 增量 vs baseline | grep "dB gain\|BER improvement\|SNR gain\|sensitivity gain" 全文 0 命中 | **PASS**（确为纯理论方法论文）|

**核查机制中性双向第 4 次验证有效**（S012/S028/S029/S030 同构）：子 agent 9 项关键声称全部 grep 命中真实，**无 S011 式造假**。无诚实标注技术限制类（B11/B12 文字陈述的关键声称都 grep 到了，图表数值是子 agent 已诚实标"图中数值未提取需 MinerU 重转"）。

### 阶段 5：B11/B12 中性提取汇总表

| # | 切入点 | 做了啥 | 报了啥增量 | 撞 D006 | 跟星地湍流载波同步什么关系 | 备注 |
|---|---|---|---|---|---|---|
| **B11** | NDA-ML STO+CPE 联估 M-APSK（PTL 2025 Du/Yu/Wang/Kam，UIC/ZJUT/CUHK-SZ）| CO-OFDM 下 M-APSK 调制，**非数据辅助** ML 联合估计 STO+CPE。升 M₀ 次幂去调制相位→化为"单复正弦频率+相位估计"→套 [13] 闭式 ML 解（L29/L119-127）。推导 CRLB（L133-151）。**信号模型假设湍流+CFO+Doppler 都已被外部补偿**（L33）| **2dB SNR gain @ (8,8)-16APSK 7% HD-FEC vs DA ML [10]**（L181/L191）；CLW 容忍度超 DA ML 2 倍（PN 方差，L183）；"1dB SNR 代价"超 DA ML CLW 容忍（L191）；MSE 收敛 CRLB（L157/L191）；复杂度低于"CPE+定时同步"组合（Table II）。⚠️ 图表数值 fast md 占位符需重转 | **不撞**。L33 明确"湍流效应、指向误差、Doppler、CFO 已被完全补偿"——**湍流在算法外假设已消除**。估计器内 θ(n) 只建模 Wiener PN（L51，σ²p=2πΔνTs 驱动），**无湍流相位项/环路/KF 状态扩展** | **场景=CO-OFDM FSO**（摘要明确 fiber+FSO 双适用，L9/L29/L191），**但全文无 satellite/星地/下行/LEO 关键词**（仅 FSO 泛指）。M-APSK 跟卫星通信常用 16/32-APSK 调制同源，物理相关性强。**算法层不触及湍流诱导相位** | 落盘✅ blit IEEE(arnumber 10816633) 干净 session。依赖 **genie-aided 相位解缠绕**（L113-131，作者承认为性能上界条件）。图表数值需 MinerU 重转 |
| **B12** | In/Out-of-Band 频域 pilot 相位噪声估计理论（TCOMM 2022 Gävert & Eriksson，Ericsson/Chalmers）| CW pilot（连续波导频音）相位噪声估计的**理论+方法基础**。比较 BLUE/ML/improved 三估计器（L133/L199/L277），推导**最优信号-导频功率比（SPR/β）**（L343-409，使 SNDR 最大）。相噪=离散 Wiener 过程（L117-121）| **改进估计器归一化 MSE 大范围接近 CRLB**（L451/L457）；最优 SPR 随相噪↓而↑、随热噪↑而↑（L485/L521）；in-band 需更高导频功率（L491/L509）。**无 BER/dB-SNR 系统级增益 vs 某 baseline**（纯理论方法论文，记"未量化系统 dB"）。与实测 [11][13] 对齐（OSNR 18-19dB，L493-505）| **不撞**。全文**零 turbulence/satellite/atmospheric/FSO 关键词**（grep 确认）。相噪唯一建模为 Wiener（来源=收发振荡器 θn(Tx)+θn(Rx)，L65/L79），**无湍流相位项/大气信道建模**。信道=memoryless AWGN+相噪+CW 导频 | **场景=纯无线/射频**（Index "Wireless communication"，L11/L15 主场景，作者 Ericsson 背景微波/毫米波 beyond-5G/6G + 分布式 MIMO）。**光学仅在引用文献与脚注 5 OSNR 比对出现，非主场景**。**完全不涉及湍流信道**，与"星地湍流载波同步"物理场景不对口。CW 导频相位估计框架原理可迁移但论文本身未触及湍流/星地 | 落盘✅ blit IEEE(arnumber 9766225) 干净 session。**纯理论+仿真方法论文**，无硬件实验。改进估计器假设近似 MVU 未严格证明（L333/L405 脚注 4）。图表+公式需重转 |

**两篇都不撞 D006**（B11 湍流算法外假设已补偿 / B12 纯无线 Wiener 振荡器相噪零湍流）。

### 中性观察（非 Go/Kill 结论，供总表排优先级用）

- **D006 归属一致**：B11/B12 都**不撞 D006**，且机制相似——估计器内相位噪声只建模 Wiener 过程（振荡器/激光线宽驱动），湍流要么被假设已补偿（B11 L33），要么完全不在信道模型（B12 零湍流关键词）。两者都未把湍流相位建模进载波同步算法。
- **场景对口度梯度**：B11（CO-OFDM FSO + M-APSK，M-APSK 与卫星通信调制同源）**场景对口度高于** B12（纯无线/射频 CW 导频理论，光学仅作引用对照）。**两篇都无 satellite/星地链路关键词**。
- **B11 是 B 档 12 篇中少数有可核查 dB 级增量的**（2dB vs DA ML @ (8,8)-16APSK），但依赖 genie-aided 解缠绕（作者承认为上界条件），且场景是 FSO 泛指非星地。
- **B12 是纯理论方法论文**，定量验证需重转图（图表占位符），且主场景无线跟星地不对口——可迁移性最弱。
- 两篇图表数值 fast 转 md 均为占位符，**若进入总表前排优先级，建议先做 standard 质量 MinerU 重转**（S029 B10 同款诚实标注）。

## 决策引用

- D018：判读模式中性提取（本轮收尾，守"不边摸边 Kill"+"全摸完排优先级"）
- D017：D015 v2 扫描/判读两层（本轮判读层收尾）
- D006：联合建模红线（C3 核查用，B11/B12 全不撞）
- D005：务实路线（中性提取不判 Go/Kill，A3 增量量级留总表阶段）
- D009：靠谱方向 checklist（降级为前几名深度评估时用，本轮不用）
- **无新建 D###**（本轮是判读层中性提取收尾 + 拉总表，未到方向决策级；用户排完优先级后对前几名做 D009 深度评估时才到决策级）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（载波同步 v2 判读层 B11/B12 是 H019 既定下一步；中性提取不预设方向，不立 Q#；拉总表是 D018 核心交付）
- 守 3 步上限成功（profile 第 6 次验证防线）：本轮判 B11/B12（2 篇）+ 拉总表 = 2-3 步，收尾对话没贪多

## 后续

### 判读层闭环（B 档 12 篇全摸完）

**B 档 12 个全摸完**（D018 中性模式）：
- B1/B2/B3 综述背书（S028 追加中性还原表）
- B4/B5/B6/B7 CFO 子环节（S027 旧判 A3 FAIL / 下载失败）
- B8/B9/B10 自相干+16-QAM（S029 中性提取）
- **B11/B12 本轮中性提取**（NDA-ML STO+CPE / 频域 pilot 相位噪声理论）

### 拉总表（D018 核心交付，本对话内完成）

**🔴 总表范围 = B 档 12 + C 档 4 + D 档有星地潜力个别候选**（用户 2026-07-02 拍"全部入总表"，主线不能只盯 B 档隐形排除 C/D）。

总表已落盘（见本对话主线输出 + topic-index 当前位置段），交用户排优先级。

### 决策点（报用户拍板，不自作主张）

1. 用户看全貌（B+C+D）后排优先级
2. **前几名才用 D009 checklist 做深度评估**（D018 核心：全摸完才排优先级，排完前几名才深度评估）
3. B4/B6/B7 旧判 A3 FAIL 是否还原中性——总表阶段统一处理（S027 旧判相对扎实 B4/B6 子 agent 全文精读，B5/B7 下载失败可 blit 补）
4. **B5/B7 下载失败债务** + **[58][60][79] 三篇 sat.1553 核心引文未落盘债务** + **B10/B11/B12 图表数值需 MinerU 重转债务**——若前几名涉及，下对话穷尽降级源 + MinerU 重转

## 核心教训（本轮）

1. **D018 新模式第 2 次执行（首次收尾）成功**：B11/B12 从头用中性提取（不混合旧 Go/Kill），守"不边摸边 Kill"+"全摸完排优先级"。profile 第 6 次验证防线（守 3 步上限）有效——只判 2 个 + 拉总表就交接，没贪多。
2. **核查机制中性双向第 4 次验证有效**（S012/S028/S029/S030 同构）：子 agent 9 项关键声称全部 grep 命中真实，无 S011 式造假。
3. **blit IEEE 干净 session 是比 blit `--download` 更可靠的 IEEE 下载通道**：S029 B8 用 blit `--download` 成功，但本轮 B11/B12 blit `--download` 失败（404/搜不到）。起作用的是"Playwright 先访问 IEEE 首页建立 session 过 418 challenge → 再请求 getPDF.jsp(arnumber)"。子 agent 自写脚本用 arnumber 直请更稳。
4. **B 档 12 篇全摸完仍未出现"够格点"**：abstract 层 A 档=0（R004 扫描层结论）+ 判读层 B 档 12 篇中性提取后**没有一篇明确"星地光+载波同步+≥2dB 灵敏度增量 vs 传统 baseline"**。但有若干中性观察点（B8 BER 量级/B9 DRE 3-1-0.5dB/B11 2dB vs DA ML/B10 16-QAM 对口 D011 种子）——这些是排优先级的素材，不是 Go/Kill 结论。载波同步领域够格点的真实判断要等总表阶段用户排完优先级 + 前几名 D009 深度评估。
