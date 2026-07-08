# B3-Q2 场景真实性核查：星地光通信多孔径阵列接收（AO 校正后分集）

> 子任务：B3-Q2 第三候选 · SCENE-REALITY 文献核查（不是 Kill/Go 判定，判定属主线职责）
> 核查对象："星地光通信多孔径阵列接收 / 自适应光学（AO）校正后分集"是否为真实工程场景
> 核查日期：2026-07-08
> 方法论约束：仅给文献证据链；每条主张标注证据来源；web 主张须 Semantic Scholar/DOI 交叉验证，否则标"web 未完全交叉验证"；查不到即标"未查到"；严格区分"星地"与"地面 FSO"（核心判别）

---

## 结论速览（先给后证）

| 维度 | 判定 | 证据强度 |
|---|---|---|
| 场景 A（地面多望远镜阵列接收卫星**下行**，分集合并）是否真实 | **有文献支撑，但以仿真 + 架构提案为主，无确认的已部署多望远镜阵列 OGS 工程实例** | 中（≥1 篇星地下行分集仿真 + 1 篇面向星地的接收机架构提案） |
| 锚论文 dB 增益（+2~3dB 强湍流 4 支路 MRC）来源 | **来自地面 FSO 仿真（场景 D），非星地** | 高（锚论文全文 + 读笔证实） |
| AO + 多孔径分集的"校正后分集"组合 | **未查到星地侧的成熟工程实例；AO 与分集在文献中呈"互补/替代"关系而非"AO 校正后做分集"的固定链路** | 中低（AO 单孔径有实测；AO+多孔径分集多为讨论未落地） |
| Valjus 2025 sat.1553 综述是否提及星地分集接收 | **否——仅提及单孔径 aperture averaging，未讨论多孔径空间分集/MRC** | 高（综述全文 grep + 读笔证实） |

**给主线的一句话结论**（仅呈证据，不替主线下 Kill/Go）：B3-Q2 的"星地多孔径阵列"特长场景 **部分成立**——星地下行多孔径分集在文献中有仿真（Ma 2015 等）与接收机架构提案（Geisler 2016），但锚论文的 dB 增益来自地面 FSO 仿真，星地侧缺乏已部署工程实例；"AO 校正后分集"这一特定组合无成熟工程实例，迁移后增益存疑（可能显著低于锚论文报告值）。

---

## 第 1 节 · 多望远镜/多孔径阵列分集接收文献清单（含场景 A/B/C/D 判别）

> 场景判别码：
> - **A** = 地面站多望远镜接收卫星**下行**（最相关 B3-Q2）
> - **B** = 卫星/地面**上行**多孔径发射
> - **C** = 星上多孔径接收/发射
> - **D** = 纯地面 FSO（非星地）——**与 B3-Q2 判别核心**

| # | 文献（作者/年/出处） | 链路场景 | 仿真/工程 | 证据强度 | DOI/ID |
|---|---|---|---|---|---|
| 1 | **Ma, Li, Tan, Yu, Cao 2015, Applied Optics** — "Performance analysis of satellite-to-ground downlink coherent optical communications with spatial diversity over Gamma-Gamma atmospheric turbulence" | **A（星地下行，卫星单孔径发射 + 地面多孔径接收，MRC/SC，Gamma-Gamma）** | **纯仿真/解析** | 中高 | 10.1364/AO.54.007575 |
| 2 | **Geisler, Berardinelli, Campagnolo, Chandar, 2016, Optics Express** — "Multi-aperture digital coherent combining for free-space optical communication receivers" | **A 架构（MIT Lincoln Lab 地面接收终端：用多小口径廉价望远镜经相干探测+数字化做数字相干合并，目标面向卫星通信）；但实验验证链路 = 3.2 km 地面 FSO** | 架构提案 + 地面 FSO 实验验证（非星地实测） | 中 | 10.1364/OE.24.012661 |
| 3 | **Wang, Wang, Tang 2023, IEEE Photonics J.（B3-Q2 锚论文）** — "Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO" | **D（地面 FSO，z=10 km，相位屏 Cn²=1e-16/1e-14，分集支路 1/2/4/6 MRC）**——文中表述"偏星地/水平链路性质"但仿真链路是地面 FSO | 纯仿真 | 高（但场景判别为 D） | 10.1109/JPHOT.2023.3265847 |
| 4 | **Wang et al. 2024, Optics Express（oe.520452，锚论文姊妹篇）** — 20 km 空间光 10G PM-QAM 分集接收平台 | **D（20 km 地面 FSO）**——文中明写"20 KM space optical communication (FSO)" | 实验平台 + 仿真 | 高（但场景为 D） | 10.1364/OE.520452 |
| 5 | **Horst, Läppchen, Baeumker et al. 2023, Light: Science & Applications** — "Tbit/s line-rate satellite feeder links enabled by coherent modulation and full-adaptive optics" | **星地 feeder 链路场景（53.42 km 山顶-天文台，模拟星地），单孔径 + 全 AO 校正，无多孔径分集** | 工程/实验（地面长距模拟星地） | 中高（佐证：主流星地 feeder 方案是单孔径+AO，不是多孔径分集） | 10.1038/s41377-023-01201-7 |
| 6 | Bian et al. 2021, Optics Communications — GEO 卫星-地面混合分集（孔径分集 + 模式分集） | **A（GEO 星地下行，混合分集）** | 仿真 | **低（web 未完全交叉验证，未拿到稳定 DOI 全文确认）** | 待定 |

**判别要点**：
- 锚论文（#3）与其姊妹篇（#4）**均属场景 D（地面 FSO）**，不是星地。这是 B3-Q2 "dB 增益能否迁移到星地"质疑的根源。
- 场景 A 真实存在的证据主要来自 **Ma 2015（纯仿真）** + **Geisler 2016（架构提案 + 地面 FSO 验证）**。二者均**非已部署星地工程**。
- 主流星地 feeder 工程方案（Horst 2023）走的是**单孔径 + 全 AO** 路线，**不是多孔径分集**。

---

## 第 2 节 · AO 校正后多孔径分集——工程实例 / AO 与分集关系

**2.1 是否有"AO 校正后做分集"的工程实例？**
- **未查到**明确的"星地链路 AO 校正 + 多孔径分集合并"已部署工程实例。
- **Horst 2023（s41377-023-01201-7，本地全文）**：Tbit/s 星地 feeder 演示用的是**单孔径 + 全自适应光学（full AO）**，明言"adaptive optics does not distort the reception of coherent modulation formats"。这是一条**单孔径 AO**的强工程证据，但**不含多孔径分集**。[证据来源：本地全文 grep + 摘要]
- **Geisler 2016** 的多孔径数字相干合并架构面向卫星通信，但**未与 AO 组合**，验证链路是地面 FSO。[证据来源：Optica 摘要 + 锚论文姊妹篇对其引用]

**2.2 AO 与分集是互补还是冲突？**
- **主流观点：互补/替代关系，而非"AO 校正后做分集"的标准链路。**
  - 大口径单望远镜：**AO** 校正波前畸变（提升单孔径相干接收耦合效率），是**单孔径**技术。
  - 多小口径望远镜阵列：靠**分集合并（MRC/DCC）**抗衰落，**无需 AO**（每孔径小，波前畸变小）——这是 Geisler 2016 的核心动机（用多个廉价小孔径替代单个昂贵大孔径 + AO）。
  - Valjus 2025 综述（见第 4 节）把 **AO 完全划在 DSP 综述范围之外（光域）**，且只提单孔径 aperture averaging。
- **潜在冲突点（web 未完全交叉验证，标记推断）**：AO 校正会提升单孔径相干长度/耦合效率，理论上可能**降低多孔径间的衰落独立性**（AO 把波前"抹平"后，各孔径接收趋于相关，分集增益下降）。此关系在部分大气光通信教材/综述中有讨论，但本核查时间预算内未拿到可引用的 DOI 全文交叉验证，**标"web 未完全交叉验证"**，不作为定论。

**2.3 小结**：B3-Q2 设想的"AO 校正后分集"在文献中**不是标准链路配置**，更像两种独立抗湍流手段的组合假设。工程上主流是二选一（大孔径+AO 或 多小孔径+分集），而非叠加。

---

## 第 3 节 · 真实 OGS 多望远镜阵列配置（ESA / JPL / NICT / 中科院）

> 本节为"是否真有多望远镜阵列 OGS"的实证。诚实标注未查到项。

| OGS | 运营方 | 望远镜配置 | 多望远镜阵列？ | 证据来源/状态 |
|---|---|---|---|---|
| **ESA OGS（Tenerife, Izaña）** | ESA | 单 1 m Zeiss 望远镜（主） | **否（单主镜）** | web 检索；未拿到官方配置页 DOI，标"web 未完全交叉验证" |
| **JPL Table Mountain / OGS** | NASA JPL | 单 0.6 m（TMF）等 | **否（单主镜，多站址非同站多镜）** | web 检索；标"web 未完全交叉验证" |
| **NICT OGS** | 日本 NICT | **单 1.5 m 望远镜（1988 建）**；另有可搬运 OGS（Saito 2021） | **否（单主镜 + 可搬运单镜站，非同站阵列）** | web 检索交叉验证 |
| **中科院（长春光机所 / 相关单位 OGS）** | CAS | 未查到明确的"同站多望远镜阵列"公开配置 | **未查到** | 本地 + web 均未确认；标"未查到" |

**关键发现**：上述主流 OGS **均未查到"同址多望远镜阵列分集接收"的已部署配置**。真实 OGS 普遍是**单台大口径望远镜**（常配 AO）。这与第 2 节"主流星地方案 = 单孔径 + AO"相互印证。

**注意区分**："多站址地面分集"（spatial site diversity，不同地面站接收以规避云遮挡）是另一回事——那是站间分集抗天气，**不是同址多望远镜孔径分集抗湍流**。本核查关注后者（孔径分集），前者不属 B3-Q2 场景。

---

## 第 4 节 · Valjus 2025 sat.1553 综述是否提及星地分集接收

**结论：否。**

**证据（本地全文 grep + 读笔双重确认）**：
- 综述全篇 grep `diversity / aperture / telescope / MRC / multi`：
  - **仅出现 `aperture averaging`（第 149 行附近）**——这是**单孔径**技术（增大单孔径面积以降低闪烁指数），**不是多孔径分集**。
  - `combining` 仅出现在 **DSP 域**（第 424 行合并导频估计、第 507 行合并 preamble），**不是空间分集合并**。
  - **无 spatial diversity、无 MRC、无 multi-telescope、无 multi-aperture array reception。**
- 读笔（`papers/_read_notes/10.1002_sat.1553.md`）L33 明确："AO 完全不在 DSP 综述范围内（光域，本文不讨论）"；L59："湍流 → 没有独立 DSP 模块。仅作为信道 SNR 分布"。

**含义**：2025 年最新的 OSL DSP 综述给出的算法地图里，**多孔径空间分集接收不是默认配置、不是主流讨论对象**。这间接支撑"B3-Q2 星地多孔径阵列"属较边缘场景的判断。

---

## 方法论与局限

1. **本地覆盖有限**：仅精读 3 篇锚论文（jphot.2023.3265847、oe.520452、sat.1553）+ grep 本地 doi/arxiv 目录。本地库中星地多孔径分集的专门论文仅靠锚论文姊妹篇的引用链触达 Geisler 2016。
2. **交叉验证状态**：
   - **Ma 2015 Applied Optics**：✅ 交叉验证（Semantic Scholar API：paperId 63f96e0e...，95 citations，作者 Jing Ma/Kangning Li/L. Tan/Siyuan Yu/Yubin Cao，venue Applied Optics 2015；PubMed PMID 26368880 摘要确认"satellite-to-ground downlink ... spatial diversity ... Gamma-Gamma"）。Optica 全文页有 captcha 拦截未直读，但 API+PubMed 双源一致。
   - **Geisler 2016**：✅ 交叉验证（Optica 摘要 + 锚论文姊妹篇对其作为 ref[1] 的明确引用 + Semantic Scholar）。
   - **Horst 2023**：✅ 本地全文（s41377-023-01201-7），grep 确认单孔径+全 AO。
   - **Bian 2021**：⚠ web 未完全交叉验证（未拿到稳定 DOI 全文，仅标题级检索）。
   - **ESA/JPL/CAS OGS 多望远镜配置**：⚠ web 未完全交叉验证 / 未查到（无官方配置 DOI 全文）。
   - **NICT OGS**：✅ web 检索确认单 1.5 m 主镜（1988）+ 可搬运 OGS。
3. **时间预算**：控制在 ≤15 分钟内完成；星地侧深挖（如逐篇核查 DLR/ESA/TOPTAL/GSOTA 演示任务的接收终端配置）未展开，标"未查到"而非臆断。
4. **场景判别的诚实性**：锚论文 dB 增益来自地面 FSO 仿真这一事实，是从本地全文（jphot L15"z=10 km"+ 读笔 L56）确认的，非 web 推断。
5. **本文件职责边界**：仅提供场景真实性的文献证据链。**Kill/Go 判定不属本子任务**，交由主线综合所有候选后裁决。
