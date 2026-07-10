# [R001] 场景迁移方法论 + FSO 领域成功案例调研

> 2026-07-10 | 关联：专题 2026-07-10-scenario-transfer-pivot / 9 次 Kill 后转向评估
> 子 agent：A（方法论，agent_3c2d885d）/ B（FSO 领域，agent_9dd01686）

## 调研问题

9 次殊途同归（载波同步 4 候选 + A3/N1/③ + ISI 均衡 + AO-DSP 全 Kill 或凑不齐 baseline）后，**别人在类似困境下怎么做场景迁移找增量？星地 FSO 信号处理领域有哪些成功案例？**

## 发现

### 一、场景迁移怎么才算合法贡献（子 agent A）

**两条硬标准（审稿人/导师共识）**：
1. 搬运方法本身不算贡献，**必须回答"B 场景下 A 方法的哪个假设不成立了、要怎么改"**
2. 只换参数 = 凑数；**必须改算法结构/推导/建模 = 合法增量**

**饱和领域找增量的标准动作**：不是"换大方向"，是"换一个未解决的子问题或换一个边界条件"——把成熟方法应用到"约束更严/指标更极端"的子场景。

**成功案例论证套路**：
- OFDM 无线→光纤（Shieh 2006 OE）：贡献不在"搬 OFDM"，在"处理光纤特有约束（色散/PMD/Kerr 非线性/相位噪声/PAPR×光放大器）"
- MIMO 无线→FSO（Ren 2015 OL，202 引）：贡献不在"搬 MIMO"，在"湍流致模式串扰，无线 MIMO 信道模型不直接适用，需重建模"
- DL 图像→通信物理层（当前主流）：合法性来自"湍流信道动态非高斯，传统解析模型失效"

### 二、星地 FSO 信号处理成功案例（子 agent B）

**成功论文的共同套路**："不发明新算法，迁移成熟光纤 DSP + 刻画新物理场景下性能边界/失效点"

| 案例 | 方法 | 论证方式 | 发表 |
|---|---|---|---|
| 100Gbps 相干 FSO | 光纤商用 DSP 穿湍流 | 同波长/同调制/同 DSP→迁移合法；首次湍流+LEO 达 100Gbps + 性能边界 | Nat Sci Rep 2022（118 引）|
| LEO-LEO 星间 | 明言"leveraging maturity from fiber" | 迁移频偏补偿/数字相干 + 超密集星座场景 | IEEE 2023（44 引）|
| 相位偏置跟踪 | 光纤算法迁移 FSO | 复用相位估计内核 + 叠加大气相位噪声模型 | MDPI 2019 |

**近年活跃子方向（除载波同步/均衡）**：
- Model-free AO / AO×DSP 联合（Springer 2025/2026 综述 Selim）
- 数字波束合成 DBC（JLT 2026 Cardakli，8 引）
- 低功耗相干接收机架构（UCL/ICSOS 2022）
- FEC + 自适应调制格式（ISAE-SUPAERO / Kotake ICSO 2020）

**学位论文常见方向**：硕士高频 = "算法对比类" + "Gamma-Gamma 湍流下某方案性能仿真"；博士 = 相干 DSP / 湍流建模 / AO 大气补偿 / 接收机硬件平台

**工程痛点 → 可能方向**（DLR/ESA/ONERA/Cailabs）：
- LEO 多普勒频偏（Pech ICSOS 2025 Z 变换建模）
- 湍流快衰落/波前畸变（>1Gbps 强制缓解）
- OGS 站点分集应对云/可用率
- PAT 受 LEO 过境快动态约束

### 三、两子 agent 共同结论（交叉一致）

> **我们的困境源于一直在"信号处理层纯算法"找增量。窄场景的增量在"算法 × 湍流信道 × 工程约束"的交叉论证。**

可操作启发：
1. 不做"光纤 DSP 平移"，做"**锁定光纤方法在星地失效的物理点 + 刻画性能边界 + 给设计准则**"
2. 聚焦单一耦合机制窄而深——如多普勒-湍流双重时变下鲁棒性边界，或 LEO 过境非平稳信道参数调度

## 结论

**回答调研问题**：

1. 场景迁移合法 → 必须锁定"B 场景下 A 方法失效的物理点"，不能纯平移
2. FSO 领域成功案例套路 = "迁移成熟 DSP + 刻画性能边界 + 给设计准则"（非发明算法）
3. **我们 9 次 Kill 的共同根因可能是"找错了贡献类型"——找的是"算法 dB 增量"，但这个场景给的是"边界/准则/包络"型贡献**。这与 TL-05（解析贡献比算法贡献安全）一致

## 对决策的影响

**需新建评估**：基于 R001 框架重新扫哪些光纤 DSP 模块在星地 GG+LEO 多普勒下有"非平凡失效点"，评估"性能边界刻画"路线能否凑齐 D-010 + 四判据。详见 PROMPT-001。

**⚠ 待跟导师确认**：如果"性能边界刻画"路线的增量不是"dB"而是"准则/包络"，导师 D-010 标准 1-5 是否认可这类贡献（D-010 标准原文是"赢传统 baseline 几 dB"，边界刻画可能不是这个形态）

## 来源

### 子 agent A（方法论）
- [Academia SE: saturated field future directions](https://academia.stackexchange.com/questions/86863)
- [IFERA: Four Ways Scholars Move Knowledge Forward](https://ifera.org/the-art-of-crafting-contributions-the-four-ways-scholars-move-knowledge-forward/)
- [Evolution of Optical OFDM (IEEE CST 2021)](https://strathprints.strath.ac.uk/79260/1/Zhang_etal_IEEE_CST_2021_The_evolution_of_optical.pdf)
- [Shieh: CO-OFDM (OE 2006)](https://opg.optica.org/oe/fulltext.cfm?uri=oe-16-2-841)
- [Ren 2015: FSO OAM+MIMO (OL)](https://opg.optica.org/ol/abstract.cfm?uri=ol-40-18-4210)

### 子 agent B（FSO 领域）
- [100Gbps Coherent FSO (Nat Sci Rep 2022)](https://www.nature.com/articles/s41598-022-22027-0)
- [LEO-LEO Optical ISL (IEEE 2023)](https://ieeexplore.ieee.org/iel7/6287639/10005208/10155111.pdf)
- [Phase Offset Tracking FSO (MDPI 2019)](https://www.mdpi.com/2076-3417/9/5/836)
- [Model-Free AO Survey (Springer 2025)](https://link.springer.com/article/10.1007/s12596-025-03011-z)
- [DBC FSO (JLT 2026)](https://opg.optica.org/jlt/abstract.cfm?uri=jlt-44-3-903)
- [Valjus 2025 DSP Review (Wiley, = sat.1553)](https://onlinelibrary.wiley.com/doi/10.1002/sat.1553)
- [Pech ICSOS 2025 Z-transform Doppler](https://hal.science/hal-05410631v1/file/Pech_Destic_Dion_Rissons_ICSOS2025_hyperref_101025.pdf)
- [DLR Giggenbach LEO-to-Ground (ICSO 2016)](https://elib.dlr.de/107778/1/ICSO-2016_%2523025_Giggenbach.pdf)
- [Cailabs: space-to-ground challenges](https://www.cailabs.com/blog/aerospace-and-defense/space-optical-communications-why-are-space-to-ground-links-taking-time-to-develop/)
- 学位论文：[UCL homodyne PhD](https://discovery.ucl.ac.uk/10197325/) / [TUM AO PhD](https://mediatum.ub.tum.de/doc/980518/) / [Chalmers receiver PhD](https://research.chalmers.se/publication/542251/) / [DTU DSP PhD](https://orbit.dtu.dk/files/9853846/PhD_th)

**诚实声明**：CNKI 中文学位论文未取证（"别人硕士做什么"由英文博论/会议论文推断）；Valjus 2025 正文未打开（= sat.1553，已落盘另读）；子 agent A 未找到专门讨论"硕士论文场景迁移套路"的中文经验帖。
