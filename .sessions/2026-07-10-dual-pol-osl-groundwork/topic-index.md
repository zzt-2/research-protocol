# Topic Index: 双偏振星地光通信 DSP — Groundwork Step 1 地勘

> slug: 2026-07-10-dual-pol-osl-groundwork
> status: active | created 2026-07-10 | last_updated 2026-07-11（PROMPT-005 Step C 完成：ML vs CMA MVE PASS，Go 判定。Q-CMA-FADE 两层贡献全 PASS，方向确认可进 Contract/Execute）

## 专题定位（一句话）

scenario-transfer-pivot 方法论准备就绪后（D001 三维度调整 + D002 角度素材 schema + D003 双偏振空间解锁），**按 FR-22 从 GW Step 1 重走地勘**，搜索空间从单偏振扩到含双偏振 OSL（sat.1553 §6 偏振解复用层 + §3/4/5 双偏振下的变化）。不是本专题继续"评估路线"，是开 GW 流程找真问题。

## 原始目标（冻结，不可修改）

**在含双偏振的星地相干 FSO（intradyne 单孔径单链路 GG 湍流 LEO）场景下，走 GW Step 1-4a 完整流程，找到过四判据的真问题（baseline M 在条件 C 下因 A 失效）和对应的合法迁移适配贡献形态。**

冻结边界：
- 守 FR-22——Step 3 精读 + Step 4a 可行性 Go/No-Go 是硬门控不可跳过
- 守"颗粒无收好过凑数"（继承上游专题）
- 不预设答案（可能找到也可能颗粒无收，诚实走完）
- 不复活 9 次 Kill 当贡献（Kill 掉的作思路素材重新进精读池，见上游 D001 维度4）

## 范围边界

### 原始目标（冻结）
见上。

### 当前范围
- **GW Step 1**（本轮）：双偏振 OSL 检索策略规划 → 执行检索 → 二轮定向 → 候选列表（守 D017 穷举门控）
- **GW Step 2**：下载 + 覆盖面缺口报告（待 Step 1 通过质量门槛）
- **GW Step 3**：精读 + 结构化提取（试 D002 角度素材 schema，3-5 篇验证后决定进不进 gw-read.md）
- **GW Step 3.5**：定向补充检索
- **GW Step 4a**：可行性 Go/No-Go

### 明确不含
- ❌ 不跳框架（地勘阶段不判方向 Go/Kill，穷举完 + 用户确认全景才推进——D017 红线 6）
- ❌ 不在检索阶段预设立 Q#（穷举完才立，D017）
- ❌ 不预设方向（§6 偏振解复用只是"回到桌面"的最大层，不是已选定方向）
- ❌ 不复活 9 次 Kill 当贡献（作思路素材重新进精读池，不变量1 仍守）
- ❌ 不推翻 9 次 Kill 的物理结论（那是事实）

### 范围变更记录
- 无（专题刚成立）

## 不变量（动任何一条必须重新讨论）

**全部继承 scenario-transfer-pivot topic-index 的 7 条不变量**（来源：2026-07-10-scenario-transfer-pivot/topic-index.md），本专题是方法论准备就绪后的 GW 执行，不重述，查上游：

1. 9 次 Kill 是物理事实不是方法论错（Kill 掉的作思路素材重新进精读池，不变量1）
2. 场景迁移合法性两条硬标准（B 场景下 A 哪个假设不成立 + 只换参数=凑数）
3. 成功论文论证套路（迁移成熟 DSP + 刻画性能边界 + 给设计准则）
4. TL-05 解析贡献比算法贡献安全
5. 继承上游全部方法论产出（地勘前置/abstract 工具错位/§7.2 核查/D017 v2/D018/D009/adaptation-scan 6 类/profile 升级）
6. 守"颗粒无收好过凑数"
7. D005 务实路线 + 找方向方法论不问导师（唯一跟导师谈=具体选定方向 + 论文结构）

**本专题新增不变量**：

8. **SC-001 许可的双偏振放宽有效**：场景设定从"单偏振 intradyne"放宽到"含双偏振 PolMUX"。其余约束（单孔径/单链路/GG 湍流/LEO）不变。双偏振动 Ch3/Ch4 的许可来自用户"可以动"（上游 D003）

## 其他结论（普通技术决策）

- **Q-DP1 共识缝 ≠ 可做方向**（TL-04 在双偏振空间验证）：5 篇独立静态 SOP 建模是真实共识缝，但"动态 SOP 致失效"因果链不成立（均衡器 300 krad/s 够用，SOP 真实来源是机械振动非湍流）。共识缝只是新颖性证据，须转译成 A 物理成立的 M-C-A 才是问题。
- **DSP 方向的 A0 适配**：A0 §2/§3/§4（ML 特性）不适用 DSP 方向，§1（性能间隙）/§5（负面证据）/§6（先验覆盖）对 DSP 反而更关键。
- **L-DP5/L-DP6 跨帧结论部分是预期性论述**：L-DP5 湍流未显式仿真，跨帧挂起是预期分析非实测。Q-DP3 进 MVE 前需用真实 GG 时间模型验证。
- **GG 时间域衰落模型是 Q-DP2/DP3 共享基建**：现有文献只给幅度 PDF，衰落持续时间/频率全篇缺失，需自建。

## 当前位置

**R1/R4/R5 分析层验证完成（2026-07-11）——⚠️ 发现重大方向风险**。第一批零风险后处理执行完毕，R4 直接反证"CMA 发散由深衰落触发"的核心叙事：57% 发散 trial 前窗口零深衰落事件，发散主要由高 μ 数值不稳定驱动。R1 半解析界趋势对（0.86）但量级差（R² 0.27）。R5 漂移 √n 律部分有效（r=0.74 但系数差 4×）。**方向核心叙事受挑战，第二批 R2/R7 紧迫性上升。**

- Step 1-3：完成（双偏振 9 篇 + ML 20 篇 = 29 篇精读）
- **Step 4a：完成**（Q-DP1/2/3 可行性评估）
- **R001/R002 调研：完成**（调制切换 Kill + ML 全谱）
- **D004 攒材料：完成**（20 篇精读 + 候选合并 D005）
- **D005 候选合并：完成**（Q-CMA-FADE 首选）
- **Step 4a 维度 D MVE（Q-CMA-FADE）**：
  - ✅ **Step A：完成**（GG 时间域衰落模型，PASS）
  - ✅ **Step B：完成**（CMA 发散概率扫描，PASS——发散由 μ 主导，条件判据已给）
  - ✅ **Step C：完成**（ML vs CMA MVE，PASS）→ 压力测试修正为 **Conditional Go（D008）**
  - ✅ **R003：完成**（12 个可出结果子问题穷举）
  - ✅ **R1/R4/R5：完成**（分析层验证）—— R1 趋势对量级差，R4 **反证深衰落触发**，R5 √n 律部分有效

下一步：**第二批 R2/R7 执行**（关键前置判断，紧迫性因 R4 发现而上升）。R4 暴露三个需排查的问题：(1) 5M 符号观测窗口太短（AFD 无法计算）；(2) Step B 用 250 krad/s SOP 可能掩盖深衰落作用；(3) 发散判据 threshold=10× 可能太松。

## 进展线索

- **S001**（2026-07-10）：双偏振 OSL 检索策略规划 → 执行（用户"一直往下做"授权）→ 15 查询穷举 + 综述补搜 + AI 候选审查 + 覆盖度评估 → Step 2 下载（tools/download + blit IEEE 两轮）→ 9 篇成功+sat.1553 → Step 3 精读（3 批 9 篇 + sat.1553§6补读 + D002 schema 试用）→ 综合分析 + 3 Q#(Q-DP1/2/3)。核心候选 43 篇 8 子方向。守 D017 穷举门控 + D018 中性提取。详见 `S001-search-strategy-dual-pol-osl.md` + `projects/thesis-fso/literature_notes.md` 双偏振 OSL 沉淀节
- **S002**（2026-07-10）：GW Step 4a 可行性评估。收 H002（Trigger 5 验证全 PASS）→ 读 gw-feasibility/glossary/TL-30/32/27 → 维度 A' 竞争分解 → 2 子 agent 物理量级核查（SOP 速率 + 衰落统计）→ Q-DP1 Kill（A0 §1 致命 D001）/ Q-DP2 Conditional Go（D002）/ Q-DP3 Conditional Go 首选（D003）→ feasibility_report.md 追加双偏振章节。守 D018 全评完才排 + FR-25 Go/Kill 分离 + TL-27 量级核算。详见 `S002-step4a-feasibility-evaluation.md` + `projects/thesis-fso/feasibility_report.md` 双偏振 OSL 节
- **R001**（2026-07-10）：PROMPT-002 并行开放调研——ML/LSTM 自适应调制切换在光通信现状。两轮检索（英 search 6 查询 + 中 CNKI 7 查询，3 子 agent 消化）。结论：广义"ML for 光通信"成熟大方向（S2 命中 2472），精确"ML 驱动光通信调制切换"小众新兴（2022-2026 引用<40，大半是识别/分配非切换）；LSTM 在切换方向极少（英文 2 篇做检测非切换，中文 0 篇）；用户"见过 LSTM 调制切换学位论文"印象未获标题层佐证（7 中文查询 0 篇，疑印象来自 RF-ACM）；双偏振星地 FSO+ML 调制切换=空白。**不立 Q# 不判 Go/Kill**（守 FR-22）。详见 `R001-ml-modulation-switching-survey.md`
- **R002**（2026-07-10）：用户追问"ML 在星地激光湍流有啥可行方向"，R001 只查了调制切换一个点，扩到全谱。两轮检索（英 search 11 查询 + 中 CNKI 5 查询，3 子 agent 消化）。结论：ML 有 9 类应用点全不窄（用户直觉正确）；跟物理层 DSP 对口的 3 个点（衰落预测/ML载波恢复/ML均衡）**在湍流场景几乎全空白**（均衡仅 Qin/Nasr 3 篇全 0 引，载波恢复湍流无人，衰落预测喂 DSP 参数无人）→ 有切入空间；中文"星地激光+湍流+ML"学位论文完全空白。**推翻主线对话内口头判断"ML 大概率也窄"**（③ oracle 只封调制切换不封 DSP 模块 ML，外推过度=急于收敛 profile 第 N 次）。修正：ML 做 DSP 模块不受调制切换天花板约束。与 Q-DP3 跨帧恢复有自然结合点（LSTM 衰落预测→fade 前瞻→恢复触发，无人接起来）。不立 Q# 不判 Go/Kill（守 FR-22）。详见 `R002-ml-in-satellite-fso-turbulence.md`
- **S003**（2026-07-10）：R001+R002 两轮 ML 调研 + 讨论三个调制相关口子（识别/分配/切换均不合适）+ 讨论 Q-DP2/DP3 纯 DSP 不带 ML。**用户确立攒材料策略（D004）**：不急进任何一个，全部推到 MVE 前大量精读攒材料。候选池 5 个（Q-DP2/Q-DP3 + ML 衰落预测/载波恢复/均衡）。守 FR-22 全程不立 Q# 不判 Go/Kill。修正主线口头判断"ML 大概率窄"（急于收敛）。详见 `S003-ml-survey-and-material-accumulation-strategy.md`
- **续 S003**（2026-07-10~11）：D004 攒材料执行——ML 方向 20 篇精读完成（3 批子 agent，含 Chen2022 标题错配 abort 后补正），全部 gw-read 规范笔记存 papers/_read_notes/ + literature_notes ML 章节（L-ML1~20 + 4 Q-ML# + 综合分析 + 7 可迁移范式 + Freire2022 6 陷阱 checklist）。候选合并（D005）：Q-DP2+Q-ML1 → Q-CMA-FADE（CMA 深衰落发散：分析+ML缓解），四判据全过最强，增量定位补 Qin/Nasr 实验缺口不换皮。候选池收缩为 Q-CMA-FADE（首选）> Q-DP3（备选）> Q-ML4（种子）。用户"和别人接近才好"偏好记 voice.md
- **S004**（2026-07-11）：PROMPT-003 Step A 执行——GG 时间域衰落模型建好验证 PASS，补 FR-20 缺口（D002 Conditional 风险 1）。2 子 agent 查证物理参数（本地论文全块衰落/准静态，外部教材交叉验证 Greenwood 1977 f_G + Conan 1995 τ_c=1/(2πf_G)）。新建 common/_gg_time.py（gg_time_envelope，块内恒定块间 AR(1)，gar/lognormal 两法）+ params.py GGTimeParams（10 字段全标来源）+ 验证脚本（边缘 PDF GAR KS<0.006 / log-ACF 误差 0% / τ_c 落文献 1-100ms）。formulas-master F33b（Greenwood+τ_c），发现 F3.28/F3.29 AR(1) 已存在同构。物理发现：τ_c≫block·t_s（ρ>0.9999），单帧准静态，Step B 需长序列≥10⁷ 符号。详见 `S004-stepA-gg-time-domain-model.md`
- **S005**（2026-07-11）：PROMPT-004 Step B 执行——CMA 发散概率扫描 PASS，补 sat.1553§6.3 L778 空白。新建 common/_cma.py（2×2 蝶形 + 1×1 退化，Godard 1980 公式溯源 Eq.28/48/50）+ explore/cma-fade-divergence/cma_divergence_scan.py。384 trials (4 湍流×4 f_G×4 μ×2 tap×3 seeds) × 5M 符号。TL-20 理论预期 + TL-22 物理前提检查。核心发现：发散由 μ 主导（μ≤1e-3 安全区/μ≥1e-2 危险区），f_G 第二驱动，湍流深度影响弱（深衰落 h→0 时 r≈n 梯度与 h 无关）。发散条件判据已给出。D006 新建。详见 `S005-stepB-cma-divergence-scan.md`
- **S006**（2026-07-11）：PROMPT-005 Step C 执行——ML vs CMA MVE PASS，Go 判定。新建 common/_ml_equalizer.py（8 实值 1D-CNN 蝶形, Qin 2025 L275/283 架构 + MSE 监督, 不照搬 VAE 损失）+ explore/cma-fade-divergence/mve_cma_vs_ml.py。5 场景 × 5 trials × 500K 符号, 三方对照（CMA/ML/oracle MMSE）。TL-20 理论预期验证：ML 零发散 vs CMA 危险区 P_div=0.40-0.60。SOP 速率修正（250→1 krad/s, sat.1553 §6.3 真实值）。C6-C8 自检全 PASS（C8 未触发: 安全区 ML≈CMA 是预期非同族性）。D007 新建（Go 判定）。Q-CMA-FADE 两层贡献完整, 方向确认。详见 `S006-stepC-ml-vs-cma-mve.md`
- **S006 续**（2026-07-11）：压力测试修正 Go→Conditional Go（D008）。Sup-1 16QAM CMA modulus mismatch 安全区就 BER 差。Sup-2 QPSK μ=1e-3 够用（方向弱），16QAM 安全步长也差（结构性缺陷）。Sup-3 ML SOP 容忍≤20°。3 子 agent 调研发现：(1) CMMA 修不好深衰落梯度发散（仍是盲 CMA 类），CMMA 在 GG 深衰落下无人测过；(2) 当前"监督 ML vs 盲 CMA"不公平，应改盲 vs 盲，但 Qin 已做 VAE vs CMA，需叠方法增量；(3) "CMA 发散后不可恢复 = Q-DP3 的 hang-up"是未被提出的因果桥，L-DP5/JR-CMA/sat.1553 三种深衰落对策全没在真实动态湍流下测过。用户"扩吧"+"出结果不容易先记下来"→ R003 穷举 12 个可出结果子问题
- **S007**（2026-07-11）：H006 第一批零风险后处理 R1/R4/R5 执行。3 子 agent 并行。R1 半解析界：drift=μ·R²·σ_n·√(AFD/(block·T_S))，P_div=1-(1-P_single)^{N_events}，趋势一致性 0.86 但 R² 仅 0.27（单 κ 无法吸收自放大动力学）。R4 相关性：μ 主导（r=0.749），LCR 仅高 μ 下弱相关（r=0.46），**⚠️ 深衰落触发模型被直接反证**——57% 发散前零深衰落事件，30% 发散在前 10%，diverged trial min_h 反而更高。R5 漂移模型：√n 律 r=0.74 R²=0.55 但系数差 3.9×（块平均梯度+自平衡负反馈）。综合：发散是高 μ 数值不稳定驱动，深衰落是加剧因素非必要触发。方向核心叙事受挑战，分析层贡献需重新定位。详见 `S007-r1r4r5-analytical-layer-validation.md`
