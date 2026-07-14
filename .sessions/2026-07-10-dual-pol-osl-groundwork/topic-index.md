# Topic Index: 双偏振星地光通信 DSP — Groundwork Step 1 地勘

> slug: 2026-07-10-dual-pol-osl-groundwork
> status: active | created 2026-07-10 | last_updated 2026-07-14（PROMPT-017 B 边完成 R006：Q-DP3 前置厘清——预测性 fade 检测物理可行/对 divergence 前兆存疑；R005 方向2⊂D003 子集；合并定义=预测性 fade 检测驱动跨帧 DSP 恢复；D003 Conditional Go 补第4条。A 边 PROMPT-016 待回传）

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
- **[2026-07-13]** [D021]：将 GW Step 4a 维度 D 的当前执行范围明确细化为“统一合法 baseline 后重比”——包含 current-CMA、standard-CMA、ML-original、ML-aligned 的预注册 30-seed 对比。
  - 原因：D020 发现 PROMPT-013 的 CMA 梯度实现与 ML 交叉支路初始化存在两个独立混杂，D021 要求先解除混杂再判定方法层卖点。
  - 新范围：在不进入 Contract、不中途修改共享 `common/` 实现的前提下，完成 Prompt-015 的隔离脚本、三方/四方法对比、预注册统计判据和结果审计。
  - 影响的未决项：D019 盲 VAE A/B 选择继续挂起，直到本次 baseline Go/No-Go 结论落地。
- **[2026-07-14]** Inflation scope record（治理 BLOCK 处理）：专题 S### 文件数达 16（S001-S016），触发 session-governance inflation BLOCK（>=15）。确认非范围漂移——16 S 是 GW Step1（检索）→ Step2-3（下载/精读）→ Step4a（可行性评估 Q-DP1/2/3）→ Step4a 维度 D MVE（GG时间模型/发散扫描/ML对比/多轮基线审计 P011-P015）全流程的自然深度，所有 S 均在原始目标「GW Step 1-4a 完整流程」范围内。PROMPT-017 是 S016 已授权派出的 B 边前置厘清任务（Q-DP3 预测性检测物理可行性 + 与 D003 关系厘清），属 GW Step 4a 候选评估范畴，不引入新范围。允许继续执行并记 S017。后续若 S### 继续增长逼近 25，考虑将 MVE 执行段（S005-S015）拆分到独立「cma-fade-mve-execution」子专题。

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
- **双口径是后续性能结论的强制口径（D018）**：fixed-label 与 PI-BER 必须并报；PI 需 pilot/帧头消歧。N=5M 的固定标签约 0.5 是交换而非信息丢失；N=2M 的 ML>CMA PI 优势只在已审计参数域内成立。
- **PROMPT-013 不形成机制贡献（D020）**：30 seeds 只确认 ML 优于 current scalar-error CMA；H_a 证伪，H_b 严格 unknown 且 freeze 主效应 0/3，standard CMA 在 2/3 高差 seed 上近乎消除差距。未统一 standard baseline 与初始化前，不得泛化为 ML 优于经典 CMA。
- **PROMPT-014 首轮不形成性能结论（D019）**：盲 VQ-VAE 实现和 11 个诊断 cells 可复用，但顺序不同 batch 的首末 loss 不能作为固定 probe 收敛证据；当前 SHA 的 30-cell 候选被拒，11/11 paired wins 不得外推。
- **PROMPT-015 统一合法 baseline 重比（D021/V005）**：standard-CMA 对 ML-original 与 ML-aligned 的超额 PI-BER 比较均为 ML 29/30 胜、exact p=1.1920928955078125e-6；预注册 overall gate=GO。初始化敏感性在本实验中近乎不影响均值，但不作因果或跨参数域结论。
- **feasibility_report Q-DP3 帧时长数据错误（R006 发现的既有债务）**：feasibility_report L593 记 L-DP5 帧时长"~74µs（4160 sym/56GBaud）"，实际 4160/56e9=74**ns**（差 1000 倍）；L-DP6 记"~1µs（32768 sym/32GBd）"，实际 32768/32e9=1.024**ms**（差 1000 倍）。精读笔记（10.1109_ICSOS59710.2023.10490279.md）已确认 L-DP5 仿真帧=4160 sym。影响：feasibility_report"相干时间/帧时长比 13-1000 倍"的论证量级有误（实际 L-DP5: 1ms/74ns≈13500×；L-DP6: 1ms/1.024ms≈1× 即 L-DP6 帧长≈相干时间，跨帧论证可能不成立）。Q-DP3 进维度 A 正式评估前须回原文核实帧时长并修正 feasibility_report。R006 结论不依赖此数值（只用 τ_c≫block·t_s 已验证关系）。

## 当前位置

**A/B 两边并行推进（2026-07-14，D022 后；B 边 R006 完成）**。PROMPT-015 GO 后方法层卖点解冻（ML 优于 standard-CMA 30 seeds 显著），但创新性软（照搬 Qin + 机制说不清）。用户决策"两边同时推"+ "能不能动一点点让它好一点点"。主控诊断方法层 = 别人方法 + 新场景，提出用分析层发散判据驱动 ML 训练调度（改动1）作为可能的创新升级。seed 策略修正：中间验证 5 seeds 够，只有论文最终结论补 30。

- **A 边（PROMPT-016，已派出）**：5 seeds 扩参数域（f_G/SNR/16QAM）拿鲁棒性曲线 + 改动1（发散判据驱动 ML 训练调度）新颖性快查。低优先机械活。**待回传**。
- **B 边（PROMPT-017，R006 已完成）**：Q-DP3 两个前置问题厘清完成。**结论**：预测性 fade 检测物理可行（对 fade 可行，对 divergence 前兆存疑）；R005 方向2 ⊂ D003 Q-DP3（子集）；合并定义=预测性 fade 检测驱动的跨帧 DSP 恢复；D003 Conditional Go 仍有效但补第4条 Conditional（检测对象须 fade 非 divergence + 前兆可辨识性需 MVE 前最小验证）。Q-DP3 可进 step 4a 维度 A 正式竞争分解，致命风险=fade 前兆可辨识性未实证。
- D019 盲 VAE 仍挂起。R005 方向1（自适应步长）已 Kill（JR-CMA 占点）。

下一步：等 A 边回传 → 核验鲁棒性数据 + 改动1 创新判断；B 边据 R006 决定 Q-DP3 是否进 step 4a 维度 A。两边汇合后做方法层战略判断（Q-CMA-FADE 加固 vs Q-DP3 转向）。

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
  - ✅ **R2/R7/R4修正：完成**（第二批关键前置判断）—— CMMA 不降发散，冻结完全无效，R4修正确认 μ 主导+LCR 次级
  - ✅ **S009：完成**（用户选 B，LCR 机制 H1/H2 都不成立 + BER 影响验证，方法层重新定位 D011）
  - ✅ **R004：完成**（方向总规划 13 发散角度 + 3 批次 + 防坑清单）
  - ✅ **S010 批次 1：完成**（数据补完验证 PASS，D012）—— BER vs SNR / 16QAM / 发散可视化 / pilot overhead
  - ✅ **S011 批次 2：完成**（方法层加固验证 PASS，D013）—— CMA 瞬态/稳态分解（机制细化）+ CMMA BER（增强 baseline）
  - ✅ **S011 续 + D014：完成**（D013 机制误诊纠正）—— 主控独立深查证明真因是 SOP 驱动极化串扰（非相位漂移），SOP×f_G 矩阵证明 D011 跟踪滞后叙事大部分被推翻，论文主卖点改为 SOP 极化鲁棒性
  - ⚠️ **S012 + D016/V001：PROMPT-011 前提 FAIL**—— fixed-label 0.5 主要是 X/Y swap；旧 CMA 非标准更新。转 10+ seeds 基线合法性重审
  - ✅ **S013 + D018/V002：PROMPT-012 双口径重审 PASS**—— S005 阈值收紧；N=5M CMA/ML 均为交换主导；N=2M 的 ML PI 优势在三 f_G 保留
  - ⚠️ **S013 续 + D020/V004：PROMPT-013 机制验证 PARTIAL**——30-seed Q1 PASS（ML>CMA 30/30 p=1.86e-9，但 baseline=current scalar-error CMA）；H_a 证伪、H_b unknown；standard CMA 在 2/3 high-gap seed 消除差距 → "ML 优于经典 CMA"不可成立
  - ⚠️ **S014 + D019/V003：PROMPT-014 首轮 PARTIAL（deferred）**——盲 VQ-VAE 实现 PASS；11/30 cells loss gate 语义不合法被拒；A/B 二选一挂起等 D021
  - ✅ **S015 + D021/V005：统一合法 baseline 重比完成**——standard-CMA、ML-original、ML-aligned 的 30-seed 主比较均通过预注册 Go 判据；结果仅作参数域内结论，D019 仍挂起

下一步：**由主控决定是否在 GW Step 4a 维度 D 内扩大参数域或进入下一门控**；PROMPT-015 已完成，结论暂限于注册合同。若进入 Contract，必须按对应阶段框架重新检查门控；D019 盲 VAE 继续挂起。

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
- **S008**（2026-07-11）：第二批关键前置判断 R2/R7/R4修正执行。3 子 agent 并行。R2 CMMA：P_div 与 CMA **逐点相同**（32/32 组合差异=0），多模修星座失配但完全修不好高 μ 发散。R7 冻结：**ΔP_div=0 全 24 组合**（冻结完全无效），即使冻结 53% 的块 P_div 仍 0.33，SOP 累计漂移 1774°/trial，sat.1553 [79] Matsuda 2020"停 CMA 更新"直觉被证伪。R4 修正（1krad/s SOP + 10M 符号）：μ 仍主导 r=0.70，LCR 从 +0.17→+0.42（固定 μ=1e-3 后 r=+0.88），深衰落触发仍被拒（Mann-Whitney p=0.9998），AFD 10M 下可计算。完整证据链：发散 = 高 μ 数值不稳定（主因）+ LCR（次因），深衰落是加剧因素非必要触发。分析层故事完整可发表，方法层价值减弱。详见 `S008-r2r7r4corrected-second-batch.md`
- **S009**（2026-07-12）：用户选 B，先验证 LCR 机制再定方法层。2 子 agent 并行。LCR 机制：**H1（重收敛累积）和 H2（边沿梯度突变）都不成立**——发散 100% 在正常区，距最近 up-cross 中位 2530 block，<100 block 占 0%。LCR~P_div r=0.96 是伪相关（代理变量：高 f_G → 短 τ_c → 块间 h 波动大 → 梯度方差大 → 数值不稳定）。BER 影响：**方法层真价值出现**——CMA 安全 μ（不发散）下 BER 仍比 oracle 差 2.9-2266×（跟踪滞后惩罚），ML 全 6 f_G 优于 CMA（1.8-数百倍），2 个 f_G 达到 oracle。方法层从"ML 不发散（trivial）"重新定位为"ML 避免 CMA 跟踪滞后惩罚（非 trivial）"。详见 `S009-lcr-mechanism-and-ber-validation.md`
- **S010**（2026-07-12）：批次 1 数据补完（R004 批次 1）执行回传后主控独立验证集成。4 任务全 PASS：① BER vs SNR（4 f_G×13 SNR×5 seeds）CMA 高 SNR 跟踪滞后 floor 0.03-0.10 vs ML/oracle→0 直接验证 D011；② 16QAM BER 确认 modulus mismatch（CMA~0.27 vs QPSK~0.10）但 ML/CMA gap **反预期小于 QPSK**（高阶星座同时伤 ML/oracle，诚实记录）；③ 发散概率可视化；④ pilot overhead 连续传输下<<1%（债务(1) 缓解）。**新发现 seed-bias 债务**：`gg_time_envelope` h_mean 跨 seed CV≈1.0（20 seeds 实测，N=10M 仅降到 0.90），根因是 AR(1) ρ≈0.97 强相关非代码 bug，Step A 只查 PDF 未查样本均值的既有盲点。影响判定：**不影响 D011 相对比较**（同 seed 同 h，比率免疫）+ 影响**绝对 BER 跨 seed 平均**（须写 limitations + 加 seed 数）。D012 新建。详见 `S010-batch1-data-completion-integration.md`
- **S011**（2026-07-12）：批次 2 方法层加固（R004 批次 2）执行回传后主控独立 P6 验证。2 任务：① 任务1 CMA 瞬态/稳态分解（3 f_G×20 seeds×N=5M）**反预期但经主控4步独立复现验证为真实物理现象**——稳态BER~0.32几乎不依赖f_G（预期f_G=30≈oracle被否证），窗口BER"高→下降→缓慢爬升至0.5"。主控4步验证：排除BER bug(3方法一致)+排除seed scheme偏置(N=2M task1更优)+决定性复现(N=2M late~0.14 vs N=5M late~0.5)+机制定位(|w|稳定1.4142→1.4166未发散但LS相位0°→-172.6°漂移)。机制=2×2蝶形CMA长序列次优锁定不稳定/相位漂移。**D011机制从"跟踪滞后"细化为"长序列锁定不稳定"**（D013新建），结论方向不变ML价值更强。② 任务2 CMMA BER（6 f_G×20 seeds×QPSK+16QAM）——QPSK CMMA=CMA精确相同(逐seed max diff=0.00实现验证PASS)，16QAM CMMA仅优CMA 0.4-0.9%(modulus mismatch非主因，CMMA非强baseline)。**r_lcr/批次1的N=2M整段BER掩盖early/late分化需补说明**。D013新建。详见 `S011-batch2-method-reinforcement.md`
- **S012**（2026-07-13）：PROMPT-011 先调研再最小验证。文献确认 DD/酉约束/两级 CMA 已成熟；机制审计发现连续酉多解表述错误、D014 未区分 swap/同源、旧 `_cma.py` 缺标准 CMA 输出因子。3 shared seeds：current fixed `0.4741±0.0201`→PI `0.0306±0.0253`、swap 3/3；standard PI `0.0349±0.0268`。D016 暂停新方法，转基线重审；V001 PARTIAL（阻断证据充分，正式数字待≥10 seeds）。详见 `S012-prompt011-cma-root-diagnostic.md`
- **S013**（2026-07-13）：PROMPT-012 双口径历史重审完成，并续接 PROMPT-013。P012 确立 fixed/PI 强制口径；P013 在 30 seeds 上确认 ML 相对 current CMA 30/30 更优，但 H_a 证伪、H_b unknown，standard CMA 在两个高差 seed 近乎消除差距，故 D020 拒绝机制贡献泛化，V004 PARTIAL。详见 `S013-dual-metric-historical-reaudit.md`、`PROMPT_012_REPORT.md` 与 `PROMPT_013_REPORT.md`
- **S014**（2026-07-13）：PROMPT-014 盲 VQ-VAE 公平比较首轮执行。Qin 原文核对修正固定星座码本/Eq.15，完成 1-sps 线性 2×2 complex-FIR VQ-VAE、共享 DP 信道、严格签名/分片/合并与 48 项回归；正式 11/30 cells 时 seed1004 触发 loss sanity，独立复算确认首末来自不同 batch、当前 gate 无固定 probe 语义。D019 拒绝当前结果候选，V003 PARTIAL；不判方法优劣。详见 `S014-prompt014-blind-vqvae-partial.md` 与 `PROMPT_014_REPORT.md`
- **S015**（2026-07-13）：PROMPT-013 回传后的主控独立核验 + 集成，并完成 PROMPT-015 统一合法 baseline 重比。Q1 独立重算（30/30, p=1.86e-9, CMA超额0.0147 vs ML0.00115，数字真实）；Q2 standard CMA 在 high-gap seed 1006/1017 降 752×/688×，seed 1011 无效；H_a 证伪/H_b unknown/H_c 排除但发现 ML 交叉支路初始化混杂。PROMPT-015 30 seeds 上 standard-CMA vs ML-original/aligned 均为 ML 29/30 胜，exact p=1.1920928955078125e-6，两条预注册主判据通过，GO 但仅限注册参数域。D019 继续挂起。详见 `S015-prompt013-reaudit-and-baseline-decision.md` 与 `projects/simulation/explore/cma-fade-divergence/PROMPT_015_REPORT.md`
- **R005**（2026-07-13）：方法层困境后两个出口方向的文献新颖性调研（用户"要方法层"，S015 诊断方向1 自适应步长 CMA + 方向2 发散检测响应）。4 英文检索（tools/search，Exa credits 耗尽降级 S2+OpenAlex+SerpAPI）+ 3 中文检索（CNKI blit 0 条/cookie 问题，tools/search chinese 命中4条仅1条RF卫星非光通信）+ 2 子 agent 深查（方向1 三篇关键论文摘要交叉验证 + 方向2 三问题 WebSearch 8 查询）。**结论：方向1 不支持继续评估**——JR-CMA (L-DP8, ACP 2025) 已在同场景（FSO+深衰落）占点三机制（AGC+误差阈值重置+自适应步长），是我们精读笔记自评"经典套路新颖性有限"的论文，是 PROMPT-011 教训（DD-CMA 翻车）的精确复现形态；双重否定（文献 JR-CMA 占点 + 自有分析层 R7 冻结无效/R4 深衰落非触发反向证伪自适应 μ 假设）。**方向2 有条件支持**——FSO/卫星光算法层无先例（hang-up recovery 刚被 Le Bidan 2023 列为开放问题），ML 预测衰落→触发 ACM 有邻近范式（Galijasevic 2025），与 Qin 区分清晰；但致命风险是须做出预测性检测（非响应性重置，否则退化成 JR-CMA 阈值重置或被判工程优化），且与 Q-DP3（D003 跨帧恢复）机制相邻须先厘清子集/独立。两个方向都受 D021 冻结约束，评估时序排在统一 baseline 重比之后。**不立 Q# 不判 Go/Kill**（守 FR-22 + 任务书最高纪律）。详见 `R005-method-direction-novelty-survey.md`
- **R006**（2026-07-14）：PROMPT-017 Q-DP3 两个前置问题厘清（B 边，文献+机制分析，3 子 agent：2 读精读笔记/结果JSON + 1 web 检索）。**前置1 预测性检测物理可行性**：对 **GG fade** 预测性可行（AR(1) ρ≈0.99997，h 下降趋势在 fade 前 0.16-0.5ms 可观测≫响应延迟），对 **CMA divergence** 前兆证据不足（J_CM(t)/h(t) 前兆轨迹从未测过；R4 修正版"前窗口零深衰落"从 57% 降到 32%）。Q-DP3 检测对象须锁定 fade 非 divergence。文献空白确认：光通信 hang-up recovery 全响应性/算法层规避，光 fade 预测全统计级喂链路层，符号级 fade 预测喂物理层 DSP = 空白；RF 有成熟预测范式可借鉴（信道级非环路级）。**前置2 与 D003 关系**：子集关系——R005 方向2 ⊂ D003 Q-DP3（D003 原始定义已含"fade 检测+状态管理+重锁定"完整链，R005 是检测环节具体化+预测性约束；L-DP5=Le Bidan 2023 同源 A 相同）。合并后 Q-DP3 精确定义：M=预测性 fade 检测驱动的跨帧 DSP 恢复（前兆检测→触发→恢复动作→性能指标），检测对象=fade，预测性是硬约束，ML=fade 预测器（可选）非均衡器。D003 Conditional Go 仍有效但补第4条 Conditional（检测对象须 fade 非 divergence + 前兆可辨识性需 MVE 前最小验证）。**不立 Q# 不判 Go/Kill**（守 FR-22）。详见 `R006-qdp3-prerequisite-clarification.md`
