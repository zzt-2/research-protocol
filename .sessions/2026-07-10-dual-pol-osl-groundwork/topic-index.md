# Topic Index: 双偏振星地光通信 DSP — Groundwork Step 1 地勘

> slug: 2026-07-10-dual-pol-osl-groundwork
> status: active | created 2026-07-10 | last_updated 2026-07-23（S080/T003 完成：complex-Jones/PMD/PDL 模型充分性救活 → provisional verdict `PIVOT_MODEL_NOT_JUSTIFIED`，headroom 不随损伤强度增长，P1 不胜 task-matched B3。family 仍 UNRESOLVED，待主控验收，不进 Step 5。）

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
- **D042 方法层自主重开轨（当前）**：仅在软件 DSP/ML A-E+H 内自主排序、止损、换候选；每个新候选必须先形成 Q# 的 M-C-A，并从候选自己的 GW Step 1 开始，完整通过 Step 2/3/必要 3.5/Step 4a 后才可进入 MVE。
- **GW Step 1**（本轮）：双偏振 OSL 检索策略规划 → 执行检索 → 二轮定向 → 候选列表（守 D017 穷举门控）
- **GW Step 2**：下载 + 覆盖面缺口报告（待 Step 1 通过质量门槛）
- **GW Step 3**：正式晋级候选的精读 + 结构化提取；候选族探索阶段先共享轻量证据，不为每个微变体机械重复全文门
- **GW Step 3.5**：定向补充检索
- **GW Step 4a**：可行性 Go/No-Go
- **D063 complex-model salvage（当前）**：T002 只 Kill unitary-real-rotation M-C-A；当前一次完成物理充分性、complex Jones/PMD/PDL 隔离模型、task-matched baseline、正确 headroom 和条件式 MVE，止于 provisional verdict。

### 明确不含
- ❌ 不跳框架（地勘阶段不判方向 Go/Kill，穷举完 + 用户确认全景才推进——D017 红线 6）
- ❌ 不在检索阶段预设立 Q#（穷举完才立，D017）
- ❌ 不预设方向（§6 偏振解复用只是"回到桌面"的最大层，不是已选定方向）
- ❌ 不复活 9 次 Kill 当贡献（作思路素材重新进精读池，不变量1 仍守）
- ❌ 不推翻 9 次 Kill 的物理结论（那是事实）
- ❌ 不把 D056 豁免改写成 4 篇已全文精读；不用摘要冒充全文
- ❌ 不在 T003 后直接进入 Step 5/Contract/Execute；Step 4a verdict 必须由主控验收
- ❌ 不复活 dormant science-scout/P03，不建设通用基础设施或调度器

### 范围变更记录
- **[2026-07-13]** [D021]：将 GW Step 4a 维度 D 的当前执行范围明确细化为“统一合法 baseline 后重比”——包含 current-CMA、standard-CMA、ML-original、ML-aligned 的预注册 30-seed 对比。
  - 原因：D020 发现 PROMPT-013 的 CMA 梯度实现与 ML 交叉支路初始化存在两个独立混杂，D021 要求先解除混杂再判定方法层卖点。
  - 新范围：在不进入 Contract、不中途修改共享 `common/` 实现的前提下，完成 Prompt-015 的隔离脚本、三方/四方法对比、预注册统计判据和结果审计。
  - 影响的未决项：D019 盲 VAE A/B 选择继续挂起，直到本次 baseline Go/No-Go 结论落地。
- **[2026-07-14]** Inflation scope record（治理 BLOCK 处理）：专题 S### 文件数达 16（S001-S016），触发 session-governance inflation BLOCK（>=15）。确认非范围漂移——16 S 是 GW Step1（检索）→ Step2-3（下载/精读）→ Step4a（可行性评估 Q-DP1/2/3）→ Step4a 维度 D MVE（GG时间模型/发散扫描/ML对比/多轮基线审计 P011-P015）全流程的自然深度，所有 S 均在原始目标「GW Step 1-4a 完整流程」范围内。PROMPT-017 是 S016 已授权派出的 B 边前置厘清任务（Q-DP3 预测性检测物理可行性 + 与 D003 关系厘清），属 GW Step 4a 候选评估范畴，不引入新范围。允许继续执行并记 S017。后续若 S### 继续增长逼近 25，考虑将 MVE 执行段（S005-S015）拆分到独立「cma-fade-mve-execution」子专题。
- **[2026-07-15]** Inflation scope record（25 S + Contract 冻结）：专题 S### 文件数达 25（S001-S025）。S017-S025 是 Q-DP4 评估（S021-S024）+ 改动1 Kill（S024/D029）+ Contract S0-S5（S025-S026）的自然延续，全部在原始目标「GW Step 1-4a 完整流程 + Contract 冻结」范围内（Contract 冻结 = 形态定型最后一步）。非范围漂移。Contract 已冻结，专题使命（GW+Contract）基本达成，后续 Execute 转新专题或续接由用户定。
- **[2026-07-15]** Inflation scope record（27 S + 方法层解冻探索）：专题 S### 文件数达 27（S026-S027）。D030 用户解冻方法层重新探索后，S027 是 A 类（改 loss）GW Step 1 检索 + 横向 MVE，属 D030 授权的"方法层增强归类批量探索"范围（原始目标已含 Contract 冻结后形态定型，方法层解冻是用户明确的范围内延伸）。非范围漂移。S027 已完成 A 类 KILL（D031），下一 S 将是 C 类探索。S### 继续增长但每类探索 1 S 节奏可控，暂不拆子专题。
- **[2026-07-16]** 范围边界明确（S033，用户拍板）：S032 §C 8 机制中的 **F1（电控偏振跟踪，硬件层）和 G2（HARQ swap 段重传，协议层）排除**出本轮方法层再探索范围。原因：F1 撞车重（光纤 PMD 电控偏振跟踪成熟标配）+ 仿真器无 EPC 模型无法 MVE；G2 物理上对 D028 永久锁定 swap 无效（SOP 不变重传还错）+ 属协议层。聚焦软件方法层 A-E+H。未改原始目标（GW Step 1-4a + Contract 形态定型），只是细化方法层探索边界。
- **[2026-07-16]** [D042] Inflation scope record（37 S 文件 + 自主方法搜索重开轨）：创建 S036 后专题共有 37 个 `S###` 文件（含历史重复编号 S033 两份，编号债务不在本轮重命名）。S027-S035 与 S036 均属于 D030 解冻后的软件方法层探索及其治理复位，未改变原始双偏振 OSL/GW+Contract 目标。
  - 原因：专题已超过 >=15 的强制 inflation 门槛，且用户把协作方式从“两模型分工/主控给提示词”改为主控在现有范围内自主推进。
  - 新范围：软件 DSP/ML A-E+H 内可自主排序、止损和换候选；每个候选必须 Q#+GW 全链。F1 硬件和 G2 协议仍明确排除，不能借“自主换向”静默解禁。
  - 影响的未决项：strict equivariance/e2cnn 由 D043 A0 NO-GO；下一候选 residual cascade 从 GW Step 1 开始；Contract/feasibility/literature/briefing 的旧状态留下一批同步，当前不进 MVE/Execute。
- **[2026-07-19]** [D057] Inflation scope record（75 S 文件 + Direction Lab P03 closure）：S075 是 D045“深耕基点—候选族—批量排跑—晋级”工作流内的 residual-headroom Scout terminal closure，不是新研究方向，也未扩大 formal GW/Contract/Execute 范围。之所以新开 S075 而不追加 S074，是因为 S074 属 pilot-Jones Step3.5 文献门控，P03 属独立 Scout diagnostic，混写会破坏两条状态线。F1/G2 排除、formal FR-22 门和 S074 未决项均不变；本轮只记录 P03 A 出口及停止，不选择下一候选。
- **[2026-07-19]** [D058] Inflation scope record（76 S 文件 + claim-scope P0纠错）：S076 从 P03 科学 closure 转为推理范围与流程规范纠错，性质不同于 S075，故新开编号。它仍服务 D045 的候选族批量探索，不扩大 formal GW/Contract/Execute；只纠正局部证据越级，并为后续 Headroom Atlas 增加通用机器门。
- **[2026-07-19]** [D059] Inflation scope record（77 S 文件 + Headroom Atlas Stage A）：S077 是 D058 列为下一对话硬前置的 Atlas 阶段（唯一强门入口 + Stage A runnable 子域诊断），承接 S076 但性质不同（流程纠错 vs 实验+门实现），故新开编号而非追加 S076。仍服务 D045 候选族批量探索，不扩大 formal GW/Contract/Execute；runnable 子域 LOCAL_NEGATIVE 但不退候选/族。
- **[2026-07-19]** [D060] Inflation scope record（79 个 S 文件、78 个唯一 S 编号 + Portfolio Autopilot 目标设计）：S078 从 P03 单候选科学诊断转为 D045 批量探索的组合级长跑控制设计，性质不同于 S077，故新开编号。额外 1 个文件来自既有 S033 重号债务，本轮不重命名历史。它只定义未来 6批/3族 shadow 的调度、双审查和全局停机边界，不实现控制器、不运行实验、不扩大 formal GW/Contract/Execute。
- **[2026-07-23]** [D062] Inflation/scope record（用户显式授权 Pilot-Jones Step 4a 大包）：专题已远超 15 个 S 文件，但本次不是新方向或 topic 膨胀；它回到原始目标“GW Step 1–4a 完整流程”，只对 D056 的不可获取全文门作一次性带债豁免。允许新增 S079、Step 4a 专属 MVE 闭包与 worker-log；明确止于 provisional verdict，不进入 Step 5/Contract/Execute。
- **[2026-07-23]** [D063] Inflation/scope record：允许新增 S080 和 complex-model salvage 隔离闭包。原因是 T002 暴露 canonical model 不含所假设的物理结构；这是原 Pilot-Jones Step 4a 的模型充分性修复，不是新方向或新 topic。仍止于 provisional verdict。

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

9. **~~swap 是 SOP 累积旋转的物理现象，CMA 和 ML 都 swap~~（S034/D040 修正：此条错误，降级为债务）**
   - prompt030 双控扫描用了 `common/_cma.py` 的 CMAEqualizer2x2，该实现梯度更新 `eX = R2 - |z|²` **缺标准 Godard 1980 的 z 因子**（正确应为 `err = (R2 - |z|²)·z`），是有 bug 的 current-CMA
   - 执行 agent prompt032 三 CMA 实测：**standard-CMA（有 z）0/5 swap（fixed ~2e-4）**，current-CMA（无 z）5/5 swap，ML 5/5 swap
   - **修正后真相**：swap 是 **ML 固定权重 SOP 泛化失败**（D015），standard-CMA 在线跟踪 SOP 不 swap。执行 agent 原 TL-22"swap 载体=ML"是对的，prompt030 因用错 CMA 错误推翻了它
   - SOP_RATE 临界曲线对 ML 仍成立；对 standard-CMA 须重测（预期不 swap）。`common/_cma.py` 缺 z 因子是历史 bug，使用它的历史结论须审计
10. **PI-BER 对 swap 结构性失明，fixed-label BER 是 swap 真记分牌**（此条仍成立）：PI-BER 排列不变自动抹掉 swap 影响；fixed-label BER 才反映 swap 破坏（0.4996）。后续 swap 判定用 fixed-label + correlation 分类口径
11. **D022 的 ML 优势修正（S034 后）**：PI 口径 ML 优于 standard-CMA 29/30 成立。fixed 口径 standard-CMA ~2e-4（不 swap），ML ~0.5（swap）——**standard-CMA 在 fixed 口径远优于 ML**。H2 须重新定位：swap 是 ML 的标签泛化缺陷；D043 已否决“strict equivariance/e2cnn 直接恢复 fixed label”，当前只允许从带标签锚点的在线规范化或 standard-CMA 保标签后的残差改进入手，并重走候选 GW 链。

## 其他结论（普通技术决策）

- **Q-DP1 共识缝 ≠ 可做方向**（TL-04 在双偏振空间验证）：5 篇独立静态 SOP 建模是真实共识缝，但"动态 SOP 致失效"因果链不成立（均衡器 300 krad/s 够用，SOP 真实来源是机械振动非湍流）。共识缝只是新颖性证据，须转译成 A 物理成立的 M-C-A 才是问题。
- **DSP 方向的 A0 适配**：A0 §2/§3/§4（ML 特性）不适用 DSP 方向，§1（性能间隙）/§5（负面证据）/§6（先验覆盖）对 DSP 反而更关键。
- **L-DP5/L-DP6 跨帧结论部分是预期性论述**：L-DP5 湍流未显式仿真，跨帧挂起是预期分析非实测。Q-DP3 进 MVE 前需用真实 GG 时间模型验证。
- **GG 时间域衰落模型是 Q-DP2/DP3 共享基建**：现有文献只给幅度 PDF，衰落持续时间/频率全篇缺失，需自建。
- **双口径是后续性能结论的强制口径（D018）**：fixed-label 与 PI-BER 必须并报；PI 需 pilot/帧头消歧。N=5M 的固定标签约 0.5 是交换而非信息丢失；N=2M 的 ML>CMA PI 优势只在已审计参数域内成立。
- **PROMPT-013 不形成机制贡献（D020）**：30 seeds 只确认 ML 优于 current scalar-error CMA；H_a 证伪，H_b 严格 unknown 且 freeze 主效应 0/3，standard CMA 在 2/3 高差 seed 上近乎消除差距。未统一 standard baseline 与初始化前，不得泛化为 ML 优于经典 CMA。
- **PROMPT-014 首轮不形成性能结论（D019）**：盲 VQ-VAE 实现和 11 个诊断 cells 可复用，但顺序不同 batch 的首末 loss 不能作为固定 probe 收敛证据；当前 SHA 的 30-cell 候选被拒，11/11 paired wins 不得外推。
- **PROMPT-015 统一合法 baseline 重比（D021/V005）**：standard-CMA 对 ML-original 与 ML-aligned 的超额 PI-BER 比较均为 ML 29/30 胜、exact p=1.1920928955078125e-6；预注册 overall gate=GO。初始化敏感性在本实验中近乎不影响均值，但不作因果或跨参数域结论。
- **PROMPT-016 N=2M 扩参数域反预期（S017）**：ML 相对 standard-CMA 的 PI-BER 优势在 N=2M 下**不普适**——6 唯一 cell（f_G 扫3+SNR扫3+16QAM，基准点去重）仅 2 cell 均值更优，配对胜场 fg30_snr20 4/5、fg100 3/5、fg1000 **1/5 反转**、snr15/10 各 2/5、16qam 2/5。根因=late_slice SOP 累积旋转量差异（陷阱3实证）：N=5M late SOP 漂移大→CMA 漂错解→ML 优势显著（P015 29/30）；N=2M late SOP 漂移小→standard-CMA 完美锁定（好 seed PI≈0）→ML 监督残余误差反更差。**D022 的"ML 优于 standard-CMA"卖点严格限于 N=5M/f_G=30 参数域，不能外推到 N=2M 或其他参数点**。新参数点（SNR扫/16QAM）用 N=2M 未独立审计适用性。改动1（物理发散判据触发 ML 重训练）新颖性 PASS 有真创新空间（FSO/广义通信均无先例）。
- **feasibility_report Q-DP3 帧时长数据错误（R006 发现的既有债务）**：feasibility_report L593 记 L-DP5 帧时长"~74µs（4160 sym/56GBaud）"，实际 4160/56e9=74**ns**（差 1000 倍）；L-DP6 记"~1µs（32768 sym/32GBd）"，实际 32768/32e9=1.024**ms**（差 1000 倍）。精读笔记（10.1109_ICSOS59710.2023.10490279.md）已确认 L-DP5 仿真帧=4160 sym。影响：feasibility_report"相干时间/帧时长比 13-1000 倍"的论证量级有误（实际 L-DP5: 1ms/74ns≈13500×；L-DP6: 1ms/1.024ms≈1× 即 L-DP6 帧长≈相干时间，跨帧论证可能不成立）。Q-DP3 进维度 A 正式评估前须回原文核实帧时长并修正 feasibility_report。R006 结论不依赖此数值（只用 τ_c≫block·t_s 已验证关系）。
- **Q-DP3 维度 A 竞争分解 Conditional Go（D025/S018）**：A0§1 "为什么没人做" 四解释无一致命——(a) 沉默 Kill 无证据（三篇均无负面措辞，sat.1553 L582 倾向主动）；(b) 物理可行≠工程值得中度风险（fade AFD=10.12µs 实测 20 seeds vs CMA 重收敛 40µs 比值 0.25，但压μ响应 40ns 比值 253 时间窗充足，R7 硬冻结无效但压μ未测）；(c) 社区小+问题新部分成立（"预测性 fade 触发 DSP 恢复"交叉切口确实小众，Le Bidan 2023 仅 3 引无人接续——这恰恰提供空白的结构性合理解释）；(d) RF/光纤迁移不成立（三条路径均未直达 DSP 块级，新颖性保留）。四判据全过，A' 先验覆盖度最低，FR-21 不触发。**Conditional 条件：压μ（非冻结）能否救 BER 是 MVE 生死前置**——R7 冻结无效阴影，若压μ也救不了 BER 则预测性检测没有载体（物理 Kill）。恢复动作必须限定为轻量响应（压μ/冻结/切换），不能是 CMA 重锁定（AFD/重收敛=0.25 物理死）。
- **Q-DP3 压μ MVE 生死验证 FAIL — 物理 Kill（D026/S019）**：压μ（非冻结，μ→μ/k）在 5 seeds 三对照中 **0/5 胜**，PI-BER 反而更差（0.0362 vs 0.0275），阈值扫描 h<0.2/0.3/0.5 三档全部 FAIL。根因=D014 SOP 极化串扰：压μ降 fade 期间权重漂移（drift∝μ）但 BER 恶化来自 SOP 持续旋转下恒模代价锁定跳变，两者正交。fixed BER 几乎不变（0.2262 vs 0.2261）证实 SOP swap 未被触及。压μ期间 SOP 漂移 mean 48.4° max 103.9°（R7 阴影证实）。恢复动作载体不存在（R7 冻结无效+压μ更差+CMA 重锁定物理死），Q-DP3 Kill 回路线 A 保底。
- **Q-DP4（SOP 驱动 lock swap 防跳变）A0+A'/A 三道分析门全过（S021）**：R007/R008 验证 B 类缝隙成立后，正式立 Q-DP4 并走 gw-feasibility A0§0-§6 + A' 竞争维度分解 + A 结构优势论证。**A0 通过（无致命）**——§0 四判据全过（不撞 D001/D016）；§1 性能间隙 1.9-7.9× BER 比值 [实证 D014]；§2 非必须 ML（形态2/3 可经典 DSP）；§5 无沉默 Kill；§6 主指标未被简单规则覆盖 ≥90%。**A' 通过**——竞争维度矩阵：Q-DP4 目标问题拆 D1 初始收敛（A 类饱和）/D2 连续跟踪（B'类饱和）/D3 收敛后防 swap（B 类=0 + 冻结/压μ/CA-CMA/ML 都不覆盖）；创新声称建在 D3（先验覆盖度低+改善空间≥10%），合法。**解 §6 张力**：D022 ML 是"换掉 CMA"非"防 CMA 跳变"，在 D3 先验覆盖度=低；D015 决定性证据——所有固定权重方法（含 ML）SOP 大漂移下同样失效（N=5M SOP 57° 时 ML BER=0.497 全崩），换掉 CMA 也不解决 D3。**A 通过**——结构优势建在 D3（代价地形多解+SOP 驱动漂移，4 个增强 baseline 都不覆盖，差距来自结构非参数）；FR-08 偏离主流（EKF 整体替换/B'类）理由=工程惯性（CMA 是 DSP 链路核心模块），标注最终说服力待 D MVE 兑现。**回应 §3 警告**：0 跨域先例经 A' 分解降级为"论证负担"非 Kill 信号（0 先例集中 D3，结构性空白有合理解释）。**满足进维度 D 前置条件**。风险1（改步长顺带缓解）机制预判=不能（R7 冻结+压μ佐证），须 MVE 证否=D 第一验证。进 D 前须定方法形态（形态1 检测+回滚/形态2 预防约束/形态3 混合补偿）。**不立 D###**（A0/A'/A 是门控更新非 Go/Kill）。
- **Q-DP4 形态2 预防性约束 Kill（S022/D027）**：PROMPT-020 维度 D MVE 三验证完成。**V1 PASS** — 6× PI-BER 差距来源分解（B0 standard-CMA 0.0210 / B1 identity重跟踪 0.0180 / B2 per-block LS最优 0.0025 / B3 frozen 0.0240 / oracle 0.0084）：B0/B2=8.3× 证明残余=swap相关权重漂移（CMA远离per-block最优），B1/oracle=2.2× 证明CMA跟踪能力够（从正确盆地跟踪SOP BER接近oracle），**定位B（防跳变同时降swap+漂移）成立**。**V2 PARTIAL** — 大μ(5e-3)确实降swap-prone seeds的SOP退化（f_G=30 ratio 4.9→1.3，物理合理=更快跟踪SOP），但不完全消除（ratio>1.0）+发散风险（D006临界区）。**V3 FAIL** — J_XCA（输出互相关惩罚）对clean swap完全无效（PI不变0.0393-0.0395，因clean swap输出互相关≈0梯度≈0，CA-CMA机制匹配错误）；diag约束（交叉FIR权重惩罚）最好仅1.24×（远<2×阈值），大α(0.5/1.0)反引发更多swap（5/5 vs baseline 2/5）。**根因**：swap不是交叉权重过大驱动，是恒模代价多解地形在SOP旋转下让权重跳盆地，约束权重分量不改变地形结构。**V3 FAIL触发预注册Kill标准**。但V1证实Q-DP4问题陈述（D3=收敛后防swap）真实（8.3×改善空间），只是形态2不是解。形态1（检测+回滚）/形态3（混合SOP补偿）未测。路线A保底不受影响。
- **Q-DP4 形态1 检测+回滚 Kill + Q-DP4 整体 Kill（S023/D028）**：PROMPT-021 维度 D MVE 第二轮。**V0 发现 swap 是一次性永久锁定**（非间歇反复跳变）：seed 1000/1003 swap 从 block 36698 持续到序列末尾（len=41426 blocks），late 段 100% swap 状态；clean seeds 1001/1002/1004 无 swap。swap 动态两阶段：①早期间歇期（block 21000-36000 ~1300个单block短暂swap CMA能自己跳回）②永久锁定（block 36698+ CMA无法自己跳回）。**V1 KILL**（3 snapshot_windows × 5 seeds 全 KILL）：回滚后 dwell time 中位 **11 块**（远<1000 Kill阈值），swap seeds n_rollbacks=888（late段几乎每11block回滚一次）。**深度物理诊断（TL-22）**：回滚到早期快照（swap前25000+块）dwell长（16083块）但BER从0.0176恶性爬升到0.1226（权重过时SOP旋转）——**不存在"既有长dwell又有好BER"的回滚点**。**根本死因**：SOP持续旋转+恒模代价多解地形的结构性矛盾，物理层面不可行。**三类响应式方法全FAIL**：R7冻结（响应fade D010）+ 压μ（响应fade D026）+ 回滚（响应swap 本轮）。**Q-DP4整体Kill**：问题陈述真实（8.3×改善空间）但三种方法形态（约束Kill/检测回滚Kill/混合补偿未测但物理覆盖）都无法解决。S021 §3 警告（0跨域先例）部分应验——不仅是结构性空白也指向"问题虽真但当前方法无法解决"。**GW Step4a 双偏振OSL三候选评估完成**：Q-DP1 Kill（D001）/ Q-DP3 Kill（D026）/ Q-DP4 Kill（D028）→ **路线A（Q-CMA-FADE D022+改动1）唯一存活方向**。
- **改动1（物理判据驱动 ML 重训练）KILL（S024/D029）**：PROMPT-022 验证1（N=5M, 5 seeds, f_G=30, SOP=4e-7, strong, 20dB, QPSK）。**所有 D 方法 PI-BER 精确等于 B（ML训练一次），无改善**。B PI=0.01028 ≈ oracle 0.00837（差距仅 0.00191）。**Kill 根因 1（最根本）**：改动1 前提（"ML训练一次失效需重训练"）在 PI 口径下不成立——D018 已确认 N=5M ML 是 clean swap（fixed≈0.5 但 PI≈0.005），ML 训练一次 PI 口径已接近 oracle，重训练无空间。D015"ML N=5M 全崩 BER=0.497"是 fixed-label 口径，改动1 基于错误口径设计。**Kill 根因 2**：物理判据检测不到 swap——预筛选证实 D013（swap 时 |w| 不发散→D1 权重范数判据 0% 触发）+ D027 V3a（clean swap J_CMA 不变→D2 恒模代价判据 0% 触发）；D3（权重漂移）唯一能触发但重训练无效。**Kill 根因 3**：C（固定周期重训练）PI=0.01626 反而比 B 0.01028 更差（每段用更少数据训练）。D015 Q3-B 报"PI=0.002"实为 fixed-label 4 旋转口径非 D018 PI 口径。**路线 A 方法层升级最后一张牌 Kill**：Q-CMA-FADE 方法层定型为"弱"（D022 窄域 29/30 + 无架构创新 + 无重训练机制）。**GW Step4a 全部候选 + 方法层升级评估完成**：Q-DP1/DP3/DP4/改动1 全 Kill，唯一存活 = Q-CMA-FADE 分析层（强）+ 方法层（弱 D022）。
- **A 类（改 loss）KILL（S027/D031）**：D030 方法层解冻后第一类横向 MVE。L1 SOP 不变性正则（4 档 λ × 5 seeds）甜点 λ=0.001 mean PI=0.01019（L0 0.01020，2/5 胜 p=0.75）KILL；L2 swap 对比学习甜点 λ=0.1 mean PI=0.01017（2/5 胜 p=0.75）KILL；消融 PASS（λ=0 退回 L0）。A3 VAE 盲损失 GW Step 1 检索硬撞车（Qin 组 2026 IEEE TCCN "Bootstrapping Blind Equalizer DP-coherent FSO via modulus-rings VAE" = 同作者组+同场景+同机制）defer 不跑。**核心失败机制 = floor 效应 + 时序正交**：3/5 clean seeds PI≈0 已 floor 无处改；swap 是 test 段 CMA 在线跳盆地（D027/D028），但 L1/L2 正则在训练段施加，训练段 SOP 漂移远小于 test late 段（57°），学到的"SOP 不变性"泛化不到。**与 D027 V3 同构**（训练阶段 loss/约束触及不到 test 段 swap）→ 火力重定向：排除整类训练阶段 loss 修改（A + 部分 C），转向 test 段在线机制（D 类 CMA+ML 混合 / E 类 pilot 前置）或架构（B 类）。L0 baseline 5-seed 复现 D022（PI=0.01020）。守 FR-22（GW Step 1 检索→MVE）+D030（归类批量+消融可验）+D018（双口径）+TL-20/22（假设先行+物理前提检查）。
- **C 类（改训练）KILL/defer（S028/D032）**：C1 周期 pilot-assisted 在线微调按预注册 `K=[1000,5000,10000] × lr=[1e-5,1e-4] × 5 seeds` 全部 0/5 胜、单侧精确 p=1.0；mean PI=`7.952e-5–8.128e-5`，不低于同初始化 L0=`7.936e-5`，lr=0 消融逐 seed 完全退回 L0。C2 SOP 数据增强/C3 curriculum 不触及 test 段，依 D031 时序正交 defer。检索发现 AdaNN 2020 与 JLT 2023 joint PMD tracking 强邻近在线适配先例，但无星地 FSO+GG+SOP lock-swap 同场景硬撞；数据已 Kill 当前化身。确定性训练下 L0 绝对值与 D031 差异大，故只采用同权重配对“无增量”结论，训练随机性列复现债务。
- **B 类（改架构）整体 defer（S029/D033）**：B1/B2/B3 四判据形式可构造，但均未通过 D031 test 段准入门，故不跑性能 MVE。B1 有 Optics Letters 2024 MIMO-CVNN/PDM 强邻近占点，复值结构保存相位/偏振关系但不等于未见 SOP 群等变；B2 无当前 SOP 角输入且两组检索无 rotation-equivariant optical equalization 支撑；B3 固定 X/Y 分支依赖坐标基，不能随 SOP 旋转基变化。`prompt026` JSON 固化筛选和若复活时的参数量匹配/消融合同。检索部分源限速，零结果不解释为绝对空白。
- **D 类历史注册域 MVE KILL（S030/D036；D034 REJECTED，D035 superseded）**：系统诊断确认 2/5→0/5 漂移来自 strong Gamma-Gamma 参数由 D022 的 `1.5/0.8` 变为当前 `4.2/1.4`；隔离脚本冻结历史输入后精确恢复 `{1000,1003}` 2/5 swap。D1/D2 mean PI=0.01505264，高于 L0=0.01043760，0/5 胜、p=1.0，KILL；触发集合断言和 forced-switch=L0 均 PASS。baseline drift 债务关闭，未改 common/params.py。
- **E 类 pilot 前置 DEFER（S031/D037）**：test 段 pilot 直接估 SOP/Jones 并前馈补偿，通过 D031。正确检索计数为首组混合源 10 条、其余 4 组 arXiv 0 条；2023 JLT `10.1109/JLT.2023.3253383` 已直接占据“插入 pilot 估信道+前馈补偿跟踪 fast SOP”，并有 2018/2023/2024/2026 pilot/data-aided SOP 链。FSO 是场景迁移但方法增量未证、关键全文/直接 FSO 覆盖仍缺，四判据保持 PASS/UNRESOLVED/PASS/UNRESOLVED，故不准入性能 MVE。`prompt028` gate 仅固化合同（`performance_mve_run=false`）。H013 C→B→D→E 扫描结束，无 Go；defer 不计 Kill。
- **strict equivariance/e2cnn fixed-label 路线 A0 NO-GO（S036/D043）**：e2cnn SO(2)/E(2) 的二维空间特征表示与 Jones U(2)/SU(2) 双复偏振作用不匹配；即使实现正确 Jones 等变，等变性也不提供绝对 X/Y 标签锚点，不能从盲观测消除排列/相位歧义。该结论只否决其 fixed-label 解法定位，不否决等变结构用于 PI-BER/残差任务。
- **P03 exact-slice 局部负面与范围纠错（S075–S076/D057–D058）**：精确 source closure 与10-cell零错误事实有效；历史coverage=1.0仅是v1零分母约定。claim-scope adjudication为cell无headroom、slice局部负面、domain未决、candidate/family开放。当前slice不训练ML，但P03需先做代表域Headroom Atlas才可候选级退出。
- **P03 Headroom Atlas Stage A（S077/D059/V033）**：建立唯一强门入口（TDD 19 tests + 独立对抗审查），跑 baseline-only Stage A 11 cells × 10 paired seeds（QPSK × SNR 5–25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192 × CSI_NONE × uncoded hard decision）。0/11 cells 达 MDE 0.005（max visible headroom 0.00039，比 MDE 低 ~13×），exit=`NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`，Stage B 不触发。但 16QAM/receiver-CSI/coded-output 三轴在 frozen closure 上 INFRASTRUCTURE_BLOCKED，历史反例（D008–D015/D023、U20 coded）恰好落在被阻轴上 → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。P03 当前 status 不变=`P03_DOMAIN_ADEQUACY_UNRESOLVED`；ML/B004/Queue/Registry 仍禁止。

## 当前位置

**S080/T003：complex-Jones/PMD/PDL 模型充分性救活完成，provisional verdict = `PIVOT_MODEL_NOT_JUSTIFIED` — 2026-07-23**。

- D063/T003 已完成：物理证据 → M0–M4 模型梯（8/8 limiting-case tests PASS）→ task-matched B3（whitening/tapped）→ 正确 BER→Q² 口径 → headroom 门 → 双审查。
- **决定性结构发现**：在最 P-favorable 深衰落条件（α=2.0/β=1.0/17dB）下，B3-vs-oracle headroom **不随损伤强度增长**——PDL 0→9.5dB（cond 1→3.6）headroom 与 M0 deep-fade-only control 完全相同（delta=0.0）；PMD 40→160ps 不单调增长。残余 headroom 来自深衰落+噪声，非 PDL/PMD 结构。verified range（PDL 1dB/DGD 6ps）信道近酉/memoryless。
- P1（energy-weighted LS）全 cell 不胜 task-matched B3。formal MVE 未运行（gate 在 probe 阶段失败，结构性结论非统计性）。
- Integrity 独立重算 PASS（SHA 链/raw→aggregate bit-exact/seeds disjoint/13 tests PASS）；science critic 8 项攻击 survive。执行中发现并修复 oracle 只逆 J_b 不逆 SOP 旋转的 anomaly（TL-22），M4 联合模型 FDE oracle 因需联合求解器排除出 headroom 表（scope 限制非 confound）。
- T002 的 `UNITARY_REAL_ROTATION_MCA_KILLED` 扩展为：即便 richer（非酉/memory）Jones，B3 仍关闭 headroom。**Pilot-Jones family 仍 `UNRESOLVED`，不在本轴关闭**，等待真正新轴（verified DGD≫T_S 频选信道或 sub-symbol 块变 Jones）。provisional verdict 待主控验收；不进 Step 5/Contract/Execute，不新建 D064，不复活 Scout/P03，不改 protected/Skill/controller，未 push。
- 4 篇 D056 全文继续 BLOCKED；OE2021 一阶 PMD provenance 标 unverified 债务。

此前：**S079/T002/V036/V037/D063：unitary slice 局部 Kill 接收，complex-model salvage 已授权 — 2026-07-23**。

- D062/T002 已完成 A0/A′/A/B；formal D 未运行。V037 接收 real-rotation `cond≡1` 这一局部致命门，状态为 `UNITARY_REAL_ROTATION_MCA_KILLED`。
- 原第二条 FR-21 门不按正式证据采信：`B1/O=1.19` 是 BER ratio，未证明等价 `<0.5dB`；contract 仍有 0/7/3 stale count，真实 raw 为 0/6/4。
- V036 numeric/code integrity 由 V037 保留为 PASS，但 V036 的全量 integrity/claim-scope 修正为 PARTIAL；science critic 的 complex-Jones caveat 成为下一授权轴。
- Pilot-Jones family=`UNRESOLVED`；D063/T003 已授权模型充分性、task-matched baseline 和条件式方法 MVE，仍不进 Step 5/Contract/Execute。
- 历史 EMA09 15/15 provenance 断裂已记录（batch1_fade_methods.py SHA mismatch），仅作 diagnostic prior；它是 pilot-vs-blind 比较非 pilot-inversion 方法间比较，从不支持 B2-beating。
- 可复用沉淀：real-rotation OSL Jones 结构性良态负面材料；B0/B1/B2/P/O ladder + paired runner + fixed/PI metrics + 10 directed tests；5-min pre-MVE 滤波器（cond-distribution + B1-vs-oracle headroom probe，泛化 FR-21）。
- V037 发现 contract stale count（真实 0/6/4）和无依据 BER-ratio→dB 门；只接收 `UNITARY_REAL_ROTATION_MCA_KILLED`，不接收 family Kill。D063 已授权 T003 检验 complex Jones/PMD/PDL rescue，不改 shared canonical generator。

此前：**S074 续接/D062：Pilot-Jones Step 3.5 带债豁免，Step 4a 大包已授权 — 2026-07-23**（已由本 S079 执行完毕）。

- P03 exact-slice历史status=`P03_ANALYTIC_COVERAGE_GE_90`，当前candidate status=`P03_DOMAIN_ADEQUACY_UNRESOLVED`；10-cell visible headroom=0只关闭该slice。
- 下一步为baseline-only multi-domain Headroom Atlas；在代表域与统计灵敏度闭合前，不训练P03 ML，不创建B004/Queue/Registry，也不退休candidate/family。
- formal research 仍 BLOCKED；S074 pilot-Jones Step3.5 与 V029 backward-chain 债务不因 P03 改变。
- 本里程碑不选择下一候选；若后续继续，另轮回 BatchPlan 选择既有候选族。

此前：**S036 状态修复完成，进入新候选 GW Step 1（尚未跑实验）— 2026-07-16**。

- D042：主控获准在软件 DSP/ML A-E+H 内自主排序/止损/换候选；F1/G2 仍排除；每个候选必须先 Q#+GW 链，不能直接 MVE。
- D043：strict equivariance/e2cnn 作为 fixed-label 解法 A0 NO-GO。
- 三路线比较后，下一条仅选择 **standard-CMA 前端 + ML residual cascade** 进入 GW Step 1。当前没有 Go 结论、没有实验设计、没有新仿真数字。
- 下一动作：先盘点 CMA-fade/SOP lock-swap 候选族，统一代码接口与批量 MVE 设计；残差 cascade 按 D044 保留 DEFER。族级结果中胜出的少数候选再补完整 GW Step 1→4a。

此前：**S035 Tier 1 执行完成（D3 MMA KILL + E2 排列对称破缺 KILL）— 2026-07-16**。

承接 S033 §F 方法层 Tier 1 两独立方向（与 S034 E1/CMA+H1 并行）：
- **方向 2 D3 MMA KILL**（prompt032_d3_mma_mve.py，D040）：MMA vs standard-CMA 0/5 胜 p=0.5，无增量。MMA 轴分离打破的是相位旋转对称非 X/Y 排列对称（正交）。**附带重大发现**：standard-CMA（有 z 因子）在新域 4.2/1.4 下 5/5 不 swap（fixed≈2e-4），而 ML 5/5 clean-swap（fixed≈0.495）——**S033 不变量 9 "CMA 和 ML 都 swap" 部分是 current-CMA 无 z 因子 bug 的假象**，swap 主因是 ML 固定权重 SOP 泛化（D015 回归）。此债须主控复查
- **方向 1 E2 排列对称破缺 KILL**（prompt033_e2_perm_symmetry_break_mve.py，D041）：非对称锚点 + 排列敏感正则 λ=0.01（5/5）+ λ=0.1（2/2）全 clean-swap（fixed≈0.4996），与 L0 完全相同。smoke 验证标准 ButterflyCNN 精确排列等变（|zX(orig)-zY(swap)|=0），E2 成功破缺（=0.35）但 swap 不变

**关键结论（第四度同构）**：训练段修改（loss D031 / 约束 D027 V3 / CMA 变种 D040 / 架构对称 D041）四度证实触及不到 test 段 swap。swap 真因 = ML 固定权重 SOP 泛化失败（D015/D040）。火力须转向 **test 段在线机制**（CMA 在线跟踪 D015 N=8M 优势）或 **CSI-aided**（pilot 前置 D037 DEFER）或 **H 类**（接受 swap）。

**方法层 8 机制探索状态**（S032 §C）：A KILL（D031）/ C KILL（D032）/ B defer（D033）/ D KILL（D036）/ E defer（D037）/ Tier0 B2 KILL（D038）H1 trivial（D039）/ Tier1 E1 FAIL（S034）D3 KILL（D040）E2 KILL（D041）。**Tier 0-2 全部完成，无 Go**。D043 又在表示/可辨识性审计处否决 strict equivariance/e2cnn 的 fixed-label 定位。下一条只把 residual cascade 作为 GW Step 1 检索路线；E3/E4/H2-H3 均不因“尚未跑”自动获得准入。

**旧待办（已由 S036/D042/D043 取代）**：① standard-CMA z 因子债已由 D040 修正；② 不再直接“进 Execute 或开 Tier 3”，而是 residual cascade 候选重走 GW Step 1。此段以下为历史进展，不授权当前动作。

---

此前（**历史记录；其中 current-CMA swap/e2cnn 活路线叙事已被 D040/D043 取代**）：**S034 Tier 1 执行完成（E1 FAIL + CMA+H1 PASS 弱）— 2026-07-16**。

承接 S033 §F 方法层下一步两方向：
- **方向 1 E1 群等变 NN FAIL**（prompt031_e1_equivariant.py）：约束等变（soft equivariance，loss 惩罚 `‖f(R(θ)r)-R(θ)f(r)‖²`）在训练段施加，L0 fixed=0.49937 vs E1 λ=0.01/1.0 fixed=0.49939/0.49940，改善 1.0×。与 D031（A1 不变性正则 KILL）三度同构——训练段任何几何约束都触及不到 test late 57° SOP 旋转。要实现真等变需严格群卷积（e2cnn SO(2) 等变层重写架构，成本高）
- **方向 2 CMA+H1 组合 PASS 但弱于 ML+H1**（prompt031_cma_h1_combo.py）：CMA 5/5 swap（4 clean_swap + 1 degraded_swap），翻标签 fixed 0.484→0.0169（28.6× 改善）。但 ML+H1 5591× 更好（CMA degraded_swap seed1004 拖后腿：翻标签只救到 7.6e-2）。CMA+H1 是独立有效方法（≠ PI-BER trivial），但不构成方法层升级（弱于已有 ML+H1）

**关键结论**：训练段几何约束类方法（A1/A2/E1）全 FAIL，火力应转向**严格群卷积架构**（hard equivariance）或 **test 段在线机制**或 **H 类（接受 swap）**。

**方法层下一步（待主控决定）**：E2 排列等变（与 E1 同构风险高但机制不同）/ D3 MMA / H2-H3 / 严格群卷积（e2cnn）。

---

此前：**S033 swap 全貌诊断完成 + 8 机制方法层战场重新校准（2026-07-15，待 Tier 1 执行）**。

prompt030 双控扫描（2 域 × SOP_RATE×N × CMA/ML/oracle × 10 seeds，7656s）**推翻执行 agent 的 TL-22 结论**，坐实三条不变量（见上方不变量 9/10/11）：
- swap 是 SOP 累积旋转的物理现象（临界角 29°~114°），**CMA 和 ML 都 100% swap**——执行 agent"新域 CMA 不 swap"是 prompt029 检测器口径错误的假象
- PI-BER 对 swap 失明，fixed-label BER 是真记分牌
- D022 的 ML 优势仅在 PI 口径成立，fixed 口径无赢家

**执行 agent Tier 0 结论修正（基于全貌）：**
- D038 B2 非对称功率 KILL：仍成立（机制错配），但当时只测 ML swap，CMA 重测优先级低
- D039 H1 翻转标签 trivial Go：仍成立（=PI-BER），但**只测了 ML+H1，CMA+H1 未测是新方向**
- 检索批次 1（5 方向 0 撞车）仍有效

**方法层下一步（Tier 1，按依赖关系，可并行）**：
1. **E1 群等变**（攻 SOP 泛化，prompt030 坐实 ML 在 N=8M/SOP=1e-6 崩塌）— 优先
2. **CMA+H1 组合重测**（执行 agent 只测 ML+H1，CMA 在线跟踪+事后翻转可能是独立有效方法）— 新方向
3. **E2 排列等变 / D3 MMA** — 独立方向可并行（D3 须对冲 2015 Kalman 邻近点）
4. 后置：B1（同构风险高）/ H2-H3（价值未明）/ A 系列 pilot（撞车高）

**范围边界（D030 + S033）**：分析层 7 项不动。F1/G2 排除。方法层聚焦软件 DSP/ML。Contract S0-S3 字段保留，待方法层收敛后增量更新 H2。

**守纪律**：守 FR-22（不跳框架，每个新方法先 GW Step 1 检索防撞车）+ D030（拼也行+试了再说+消融可验）+ D018（fixed/PI 双口径）+ S033 不变量 9/10/11。

---

此前：S032 方法层 8 机制全景 + 统一规划（A-H ~40 思路）。执行 agent 跑完 Tier 0（B2 KILL/H1 trivial/检索 0 撞车）。

---

此前：**S032 方法层再探索 8 机制全景规划完成（2026-07-15，待执行）**。承接夜间 A-E 全类 KILL/defer 后用户质疑"不可能一点方法没有"。

**S032 核心发现（战场扩大依据）：**
1. **参数域审计**：夜间"参数漂移"误判澄清——4.2/1.4 是用户刚改的正确新参数（Gu 2022）。逐脚本核对：C 类 prompt025 用新参数，swap 5/5 正常触发，**不是假 Kill**；D 类 D036 引用旧域 1.5/0.8 frozen run（域不一致债，但 D 信息论注定 Kill）
2. **oracle 上界关键发现**：fixed-label BER 0.4996→3.5e-5（oracle，4 个数量级可恢复空间，前提 CSI）；PI-BER 仅 2×（**对 swap 结构性失明**）。夜间全类 MVE 用错记分牌（Go 判据用 PI-BER）
3. **信息论边界**：盲方法（A/C/D）注定碰不到 fixed-label BER（排列模糊，无参考帧）。只有 CSI-aided 或打破对称性的方法能解
4. **8 机制全景**（A 注入CSI / 🔥B 内生不对称 / C 时间维 / D 换范式 / 🔥E ML范式 / F 硬件 / G 跨层 / 🔥H 换问题）共 ~40 思路。富矿带=B/E/H，撞车重灾=A/D/F
5. **检索缺口**：夜间已覆盖 A1/A2/A3/C1/D2/E1；机制 B 全 5 个 + H 全 3 个 + 5 散点共 13 个真空白

**待用户拍板 3 点**：① F1/G2 范围（倾向排除）② Tier 0 先行（B2+H1）③ 检索批次 1（5 个：B2/B1/H1/E2/D3）立即并行？

**MVE 执行图**（按依赖分 tier，详见 S032 §F）：Tier 0（B2 非对称功率 + H1 CRC 翻转，物理前提，最快）→ Tier 1（B 成立后激活 D2/B1/E2）→ Tier 2（独立并行 E1/D3/C1）→ Tier 3（依赖殿后）

---

此前：**H013 C→B→D→E 全类扫描已结束（2026-07-16，D037）**。D 类历史注册域 KILL；E 类因 coherent-optical 同机制强占点且 FSO 方法增量未证而 DEFER，不启动性能 MVE。

**范围限定**：分析层 7 项稳结论不动（硬贡献：发散 μ 主导/SOP 串扰真因/CMMA 不降发散/冻结无效/LCR 伪相关/GG 时间模型/swap 永久锁定）。Contract S0-S3 字段保留有效（假设 H1 分析层 / H2 方法层 / baseline / 指标 FR-17 调整 / 参数溯源），待方法层探索收敛后增量更新 H2。

**方法层增强候选地图**（**已从 5 类扩展为 8 机制，见 S032**。原 5 类 D030 归类如下，仅供参考；当前以 S032 8 机制全景为准）：
- ~~**A 改 loss**~~（**KILL D031**）：L1 SOP 不变性正则 / L2 swap 对比 4 档 λ 全 KILL；L3 VAE 盲损失撞车 defer。失败根因：loss 正则在训练段，swap 发生在 test 段，时序正交（同 D027 V3 同构）
- ~~**B 改架构**~~（**整体 defer，D033**）：复值网络/SOP attention/双分支均未证明固定前馈可对未见 SOP 旋转等变
- ~~**C 改训练**~~（**C1 KILL、C2/C3 defer，D032**）：在线微调六档 0/5 胜；SOP 数据增强/课程学习按 D031 时序正交 defer
- ~~**D CMA+ML 混合**~~（**历史注册域 MVE KILL，D036；D034 rejected，D035 superseded**）：恢复历史 2/5 触发后仍 0/5 胜于 L0；baseline drift 已关闭
- ~~**E pilot 前置**~~（**DEFER，D037**）：插 pilot 估 SOP→补偿→均衡在 coherent fiber/PON 已有强同机制占点；FSO 场景迁移的方法增量未证

**执行顺序**（H013 扫描完成）：~~A~~ → ~~C~~ → ~~B~~ → ~~D~~ → ~~E（DEFER）~~。

**准入原则（D030 放宽，仍守）**：拼也行（A 机制+B 场景=合法迁移）+ 可能存在优化就可试（试了没用再说，不要求机制预判成立）+ 唯一硬防线=每类 GW Step 1 检索一次防撞车 + 消融可验（拿掉加的模块性能得退）。

**软退出判据**：一轮穷举扫描（A-E 全类过 GW Step 1+四判据+能跑的 MVE）做满后看全貌，全 Kill 或只剩窄域增强 → 接受当前形态进 Execute。不设硬时限。

**下一步：H013 全类扫描已结束；E 类保持 DEFER，待补关键全文、直接 FSO 覆盖及超出既有 pilot/feed-forward 链的方法增量后，再决定是否启动 PROMPT-028 性能 MVE（D037）。** baseline drift 已由 D036 定位并关闭。

此前：Contract S0-S5 全过冻结（S026）。Contract S0-S3 + prompt023 补 D014 债务（S025）。GW Step 4a 全候选 Kill（Q-DP1/DP3/DP4/改动1），唯一存活 Q-CMA-FADE 分析层强 7 项 + 方法层弱 D022 窄域 29/30。主控 reframe：D014 SOP 真因 + D022 ML PI 优势焊一起。

不立 Q# 不判 Go/Kill（守 FR-22）——注：D029 是改动1 方法 Kill，Q-CMA-FADE 方向本身不变量仍守。

此前：R008 排除风险2/3 占点（CA-CMA 静态+A类不占 / NPCA 整体替换不可移植不占），B 类缝隙在排除最危险两项后加固：
- **CA-CMA 2025（风险2）不占 B 类**：1500 测量全静态（采集内信道冻结），80% 无效收敛是 A 类初始收敛 singularity（非动态收敛后跳变）；CA-CMA 自承 J_XCA 引噪声不适合持续运行，预收敛后切换常规 CMA——切换后 SOP 持续旋转是否跳变论文未验证（R007 DEBT 解除 + B 类形态2 创新空间）
- **Yi NPCA（风险3）不占 B 类**：N-1 结构整体替换 CMA 偏振解复用（NPCA 1-tap 2×2 BSS filter），非保留 CMA 加约束；失效 A+C 类非 B 类；约束不可移植（BSS kurtosis 代价与恒模代价数学结构不兼容）
- R007 最危险占点排序前两位（Yi NPCA > CA-CMA 2025）确认非占点，**"0 篇 B 类专题论文"经最严格排查仍成立**

不立 Q# 不判 Go/Kill（守 FR-22）。

**主控须决定的下一步（Q-DP4 A0 已过，3 选项）**：
- **选项A（推荐）**：Q-DP4 进维度 A'（竞争维度分解，解 §6 张力——"保留 CMA 的增量 vs 整体替换"）+ A（结构优势论证，回应 §3 警告——"为什么保留 CMA 攻跳变可行"）。A'/A 无致命后进维度 D MVE，第一验证=风险1（改步长 SOP×f_G 矩阵换大步长是否消除 1.9-7.9× 退化，机制预判不能）
- 选项B：接受 A0 结论但暂缓——先确认 §3 警告（0 跨域先例）是否需补检索（扩中文术语万方/IEEE 中文标题、查 RF MIMO BSS 收敛后 jump 文献），再进 A'/A
- 选项C：接受低天花板保底（路线 A：Q-CMA-FADE D022 窄域 ML 优势 + 改动1 + 分析层），Q-DP4 挂起

**Q-DP4 的关键不确定性**（须 MVE 阶段解决）：
1. 风险1 改步长是否顺带缓解（机制预判不能，须实证）
2. SOP 旋转速率实测数据缺失（FR-20 参数溯源缺口）——sop_rate=4e-7 是 sat.1553 §6.3 仿真值，真实机械振动/热漂移致 SOP 实测速率缺失（D001/现有债务）
3. 方法形态选择（形态1/2/3）——A'/A 阶段需进一步收敛，影响 §3 先例论证 + §4 MDP 判断

**方法层系统复盘背景（2026-07-14，S020）**。压缩后按 H009 任务做四问复盘，核心结论：

1. **"治错病"判断成立**：所有方法层方向治发散/fade/跟踪滞后，但 D014 证明 BER 真因=SOP极化串扰。三个现象正交（发散=μ爆炸/fade=h→0/SOP串扰=恒模多解跳变），D014 SOP×f_G 矩阵铁证（SOP=0 时 CMA=oracle ratio=1.0）。例外：ML窄域优势（D022）误打误撞碰对病（固定权重交换后残余误差小）。
2. **D014 SOP串扰方法层空间被间接评估过但角度偏**：PROMPT-011 查通用恒模多解（D016 Kill）+ D001 Pivot 查机械振动SOP（占点）。**"FSO SOP极化锁定跳变针对性方法"这个精确角度没被专门查过**。
3. **Q-ML3/Q-ML4 不值得重评**：载波恢复跟SOP串扰正交，双频补偿无关。
4. **分析层不够单独交差**：导师约束①"不能只分析得加方法"硬卡。方法层是"强弱"问题不是"要不要"。当前最低版本=分析层硬+方法层弱（D022+改动1），唯一升级空间=SOP缝隙。

**SOP缝隙初步检索（子agent）**：B类（动态SOP下CMA收敛点跳变针对性方法）未检索到专题论文=疑似空白。A类（静态singularity解法）成熟（two-stage/CA-CMA/singularity-avoidance/VAE bootstrap）。**风险**：EKF/Kalman文献把动态跳变当整体替换动机，缝隙可能是"机制命名空白"非"方法空白"，需新对话系统验证。

**下一步**：用户确认派新对话系统验证SOP缝隙（纯文献tools/search，不跑实验）。缝隙真空白→新方向过GW Step4a四判据（守FR-22不开跑）；被占满→接受低天花板保底进Contract/写作。

**更新（D024，主控 fade 前兆验证）**：主控派两个子 agent + 独立核验，确认 fade 前兆可辨识（55-60% 事件 p<0.05 趋势显著）+ 预警提前量充足（85% 事件 ≥2µs，中位 9µs；子agent#1 悲观结论被推翻）。R006 致命风险（前兆未实证）解除，D024 落库。用户判断"B 看起来这么好却没人做，感觉危险"。

**PROMPT-018 已派出（Q-DP3 维度 A 竞争分解）**：核心是 A0§1 反向论证"为什么没人做"——四解释（沉默Kill/物理不值得/社区小/RF迁移）逐一查证，默认立场找死因不找活路。Go 则进维度 D MVE，Kill 则回 A 保底或重选。

**PROMPT-018 完成（S018/D025）**：Q-DP3 维度 A 竞争分解完成，**Conditional Go 进维度 D MVE**。A0§1 核心担忧"为什么没人做"已解除——(c) 提供结构性合理解释（交叉切口小众+问题新，Le Bidan 2023 仅 3 引无人接续），(a) 无沉默 Kill，(d) 非简单迁移。四判据全过，A' 先验覆盖度最低，FR-21 不触发。**但 (b) 压μ能否救 BER 是 MVE 生死前置**——R7 硬冻结无效已证，压μ（非冻结）从未测过，若压μ也救不了 BER 则预测性检测没有载体（物理 Kill）。恢复动作必须限定为轻量响应（AFD/压μ响应=253 时间窗充足），不能是 CMA 重锁定（AFD/重收敛=0.25 物理死）。

**PROMPT-019 已派出（Q-DP3 维度 D MVE 生死验证）**：压μ能否救 BER——三对照（常规μ/fade 期间压μ/oracle）+ 双口径（fixed/PI）+ 5 seeds→30 seeds if PASS。压μ PASS → Q-DP3 有恢复载体，进预测性增量验证；压μ FAIL → Q-DP3 物理 Kill，回路线 A 保底。默认立场"找死因"（继承 PROMPT-018），最可能死因=D014 SOP 极化串扰（压μ期间 SOP 同样不跟，R7 阴影 1774° 漂移）。

**PROMPT-019 完成（S019/D026）**：压μ MVE 生死验证 **FAIL，Q-DP3 物理 Kill**。5 seeds 三对照压μ **0/5 胜**，PI-BER 反而更差（0.0362 vs 0.0275），阈值扫描 h<0.2/0.3/0.5 三档全部 FAIL。根因=D014 SOP 极化串扰：压μ降 fade 期间权重漂移（drift∝μ）但 BER 恶化来自 SOP 持续旋转下恒模代价锁定跳变，两者正交。fixed BER 几乎不变（0.2262 vs 0.2261）证实 SOP swap 未被触及。压μ期间 SOP 漂移 mean 48.4° max 103.9°（R7 阴影证实）。恢复动作载体不存在（R7 冻结无效+压μ更差+CMA 重锁定物理死=AFD/重收敛 0.25）。Q-DP3 Kill 回路线 A（Q-CMA-FADE+改动1）保底。分析层全部不受影响。
- **SOP lock swap 方法缝隙成立（R007，B 类真方法空白；R008 排除最危险两项风险后加固）**：S020 复盘确认 BER 真因=D014 SOP 驱动 polarization lock swap 后，R007 系统验证"保留 CMA、专攻收敛后 SOP 驱动跳变"的精确缝隙。7 英文查询（singularity/dynamic/SOP/lock swap/tributary/migration/saddle point 术语全覆盖）117 唯一命中，B 类精确判据 **0 篇专题论文**。邻近文献全绕开 B 类：整体替换 CMA（EKF/Kalman 10+VAE 2+Stokes 3）/ 攻跟踪速度不提跳变（Suzuki 2022/Qiu 2026 AS-CMA/Cojocaru 2026 软判MCMA，明确不提 convergence migration/lock swap）/ 攻静态奇异点（A 类 8 篇，PROMPT-011 已确认成熟）。非机制命名空白——B'类解的是连续跟踪滞后（不同机制）。**R008 全文精读排除最危险两项风险**：风险2（CA-CMA 2025）确认全静态测试+A 类初始收敛+不持续运行，不占 B 类；风险3（Yi NPCA）确认整体替换 CMA+BSS 代价不可移植，不占 B 类。剩余风险1（B'类改步长顺带缓解）须 MVE 证否，预期不能（跳变是恒模多解驱动非步长）。中文 CNKI 0 有效（CMA=气象局术语歧义，债务）。**不立 Q# 不判 Go/Kill 守 FR-22**。

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
- **S017**（2026-07-14）：PROMPT-016 A 边执行（扩参数域鲁棒性 5 seeds + 改动1 新颖性快查）。**段1 N=2M/6 唯一 cell/5 seeds 核心反预期**：ML 相对 standard-CMA 的 PI-BER 优势在 N=2M 下不普适——6 cell 仅 2 cell 均值更优（fg30_snr20 4/5、fg100 3/5、fg1000 **1/5 反转**、snr15 2/5、snr10 2/5、16qam 2/5）。跨 cell ML excess 均值 0.073 vs stdCMA 0.044。根因=late_slice SOP 累积旋转量差异（陷阱3实证）：同 seeds/f_G=30/QPSK/20dB，N=5M(P015) ML 5/5 赢 excess 0.00005-0.031，N=2M(本扫) ML 4/5 赜 seed1004 翻转 excess 0.0001-0.16；N=5M late SOP 漂移大→CMA 漂错解→ML 优，N=2M late SOP 漂移小→stdCMA 完美锁定→ML 监督残余误差反更差。current-CMA 全 6 cell 最差（sanity OK）。**段2 改动1 新颖性 PASS 有真创新空间**：物理发散判据触发 ML 重训练在 FSO/广义通信均无先例（Qin/Kulmer/Li 冻结训练，Nasr 固定网格预训练非触发，Freire-TL 光纤非 FSO，B2/JR-CMA 物理阈值 gate 经典 DSP 非ML）；须守触发频率二难边界 + 写作区分"信道状态触发"vs Nasr"固定网格"。守 PROMPT-016 §0 不写 D### 回传主控。详见 `S017-prompt016-param-sweep-and-novelty.md` + `projects/simulation/explore/cma-fade-divergence/PROMPT_016_REPORT.md`
- **S018**（2026-07-14）：PROMPT-018 Q-DP3 维度 A 竞争分解执行。3 子 agent 并行（全文精读 A0§1a + GG 时间模型 AFD 实测 A0§1b + web 调研 A0§1c/d）+ 主控集成。**A0§1 四解释无一致命**：(a) 沉默 Kill 无证据（L-DP5/L-DP6/sat.1553 均无负面措辞，sat.1553 L582 倾向主动 + L764 主动提名动态步长）；(b) 物理可行≠工程值得中度风险（fade AFD=10.12µs 实测 20 seeds vs CMA 重收敛 40µs 比值 0.25 → CMA 重锁定物理死，但压μ响应 40ns 比值 253 时间窗充足，R7 硬冻结无效但压μ未测）；(c) 社区小+问题新部分成立（"预测性 fade 触发 DSP 恢复"交叉切口确实小众，Le Bidan 2023 仅 3 引无人接续——提供结构性合理解释）；(d) RF/光纤迁移不成立（三条路径均未直达 DSP 块级）。四判据全过，A' 先验覆盖度最低，FR-21 不触发。**D025 Conditional Go 进维度 D MVE**，压μ能否救 BER 为生死前置（第一优先验证）。恢复动作必须限定为轻量响应（非 CMA 重锁定）。详见 `S018-prompt018-qdp3-dimension-a-competition.md` + `PROMPT_018_REPORT.md`
- **S019**（2026-07-14）：PROMPT-019 压μ MVE 生死验证执行。主控直接执行（代码 MVE 属中任务）。新建 `prompt019_mu_compress_mve.py`（StandardCMA2x2 含 Godard 1980 z 因子 + 压μ逻辑）。5 seeds × 3 对照（A 常规μ / B 压μ / C oracle）× 双口径。**压μ 0/5 胜**，PI-BER 反而更差（0.0362 vs 0.0275），阈值扫描 h<0.2/0.3/0.5 三档全 FAIL。根因=D014 SOP 极化串扰（压μ降 drift∝μ 但不解决 SOP 串扰，两者正交；fixed BER 几乎不变 0.2262 vs 0.2261 证实 SOP swap 未被触及；压μ期间 SOP 漂移 mean 48.4° max 103.9° R7 阴影证实）。**D026 Q-DP3 物理 Kill**——恢复动作载体不存在（R7 冻结无效+压μ更差+CMA 重锁定物理死），回路线 A 保底。分析层全部不受影响。详见 `S019-prompt019-mu-compress-mve-fail.md` + `PROMPT_019_REPORT.md`
- **S020**（2026-07-14）：压缩后系统复盘（H009 任务）。四问：(1)"治错病"成立——所有方法层治发散/fade/跟踪滞后但D014证明BER真因=SOP串扰；(2)D014 SOP串扰方法层空间被间接评估过但角度偏（PROMPT-011查通用恒模多解/D001 Pivot查机械振动SOP），"FSO SOP极化锁定跳变针对性方法"精确角度未专门查；(3)Q-ML3/Q-ML4不值得重评（载波恢复跟SOP正交）；(4)分析层不够单独交差（导师约束①"得加方法"），方法层是强弱问题。子agent初步检索SOP缝隙：B类（动态SOP收敛点跳变针对性方法）疑似空白，A类（静态singularity解法）成熟，风险=可能是机制命名空白非方法空白。用户确认派新对话系统验证。详见 `S020-post-compaction-method-layer-postmortem.md`
- **R007**（2026-07-14）：SOP lock swap 方法缝隙系统验证（S020 下一步选项1，纯文献 tools/search）。7 英文查询（继承 S020 子agent 5 + 补 lock-swap/migration 2）+ 2 中文 CNKI（0 有效，CMA=气象局术语歧义）= 117 唯一命中。**核心结论：B 类缝隙成立——"保留 CMA、专攻收敛后 SOP 驱动 polarization lock swap"是真方法空白非机制命名空白**。B 类精确判据（收敛后跳变针对性方法）0 篇专题论文。去重预分类：B'=3（保留 CMA 攻跟踪速度不提跳变：Suzuki 2022/Qiu 2026/Cojocaru 2026）/ 边界=22（整体替换 15+混合 2+分析 5）/ A=8（静态歧义，PROMPT-011 已确认）/ 无关≈84。深查 5 篇关键论文（S2 API abstract）：无一篇"保留 CMA 攻收敛后跳变"。带 3 项风险：①改步长可能顺带缓解②CA-CMA 2025 动态测试条件 DEBT③Yi NPCA 约束可移植性。最危险占点 Yi NPCA>CA-CMA 2025>B'类>EKF 主流。方法 3 形态列举（跳变检测+回滚/预防性约束/混合 SOP 补偿，均无直接先例）。**不立 Q# 不判 Go/Kill 守 FR-22**。详见 `R007-sop-lock-swap-method-gap-verification.md`
- **R008**（2026-07-14）：R007 风险2/3 占点排除（全文精读 CA-CMA 2025 + Yi NPCA 2021，gw-read 规范聚焦 5 问题）。DOI 下载失败（IEEE paywall）转 blit campus IP 成功，tools/convert 转 content.md。**核心结论：风险2/3 均排除，B 类缝隙在排除最危险两项后仍成立**。CA-CMA（风险2）不占 B 类：①测试条件全静态（1500 测量=15 OSNR×100 信道状态，每次 10μs 采集内信道冻结，MPC 只在采集间调）②失效 A 类初始收敛 singularity（两路同源，非收敛后跳变）③CA-CMA 自承 J_XCA 引噪声不适合持续运行，方案是预收敛 1.5×10⁵ 符号后切换常规 CMA——切换后 SOP 持续旋转是否重新跳变论文未验证（R007 DEBT 解除 + B 类形态2 创新空间）。Yi NPCA（风险3）不占 B 类：①N-1 结构整体替换 CMA 偏振解复用（前段两 N-tap polarization-independent M-CMA 只补偿色散，后段 1-tap 2×2 NPCA BSS filter 做偏振解复用）非保留 CMA 加约束 ②失效 A+C 类（静态 singularity + 跟踪速度）非 B 类 ③约束不可移植（NPCA 是 BSS 分离器非约束项，kurtosis 代价与恒模代价数学结构不兼容）。R007 最危险占点排序前两位确认非占点，"0 篇 B 类专题论文"经最严格排查仍成立。**唯一剩余风险1（B'类改步长顺带缓解）须 MVE 证否**（SOP×f_G 矩阵换大步长，预期不能因跳变是恒模多解驱动非步长）。精读新发现两个 B 类创新空间开放点：CA-CMA J_XCA 持续运行噪声是公开未解问题 / NPCA 的 BSS 思想未用于收敛后跳变。两篇精读笔记存 papers/_read_notes/，read-log 已登记。**不立 Q# 不判 Go/Kill 守 FR-22**。详见 `R008-cacma-npca-occupancy-verification.md`
- **S021**（2026-07-14）：Q-DP4（SOP 驱动 polarization lock swap 防跳变）A0 预检（主控派出的 GW Step 4a 维度 A0 子对话）。R007/R008 验证 B 类缝隙成立后正式立 Q-DP4 并走 gw-feasibility A0§0-§6 + glossary 四判据。**核心结论：A0 通过（无致命），Q-DP4 正式立项**。§0 四判据全过——显式区分不撞 D001（Q-DP1 SOP 跟踪失效：均衡器够用所以 SOP 不是问题；Q-DP4 均衡器够用但恒模代价让已收敛权重跳错解，D014 SOP×f_G 矩阵 SOP=0 时 ratio=1.0/SOP=4e-7 时 1.9-7.9× 证明）+ 不撞 D016（通用恒模多解静态解法复测；Q-DP4 是收敛后动态跳变针对性方法非静态复测）。§1 性能间隙 1.9-7.9× BER 比值 [实证 D014]；§2 有时变+泛化特性但**诚实标注非必须 ML**（形态2/3 可经典 DSP）；§3 **0 跨域直接先例=最高风险警告**（但证据指向结构性空白非方法不匹配：CA-CMA 自承放弃持续运行）；§4 ML 形态非平凡/经典 N/A；§5 无沉默 Kill+(c) 结构性合理解释；§6 主指标未被简单规则覆盖 ≥90%（D022 ML 是换掉 CMA 非防跳变，与"保留 CMA 攻跳变"正交）。风险1（改步长顺带缓解）**机制预判=不能**（跳变是恒模多解驱动离散事件非步长可消除连续漂移，R7 冻结+压μ两个极端都佐证），须 MVE 实证证否=进维度 D 第一验证。**不立 D###**（A0 只到"进 A'/A"，Go/Kill 在维度 D 后）。守 FR-22（A0 纯分析不跑代码 MVE）+ FR-23/TL-04（M-C-A 过四判据非空白即机会）+ FR-25（§1 用传统 baseline 不用 oracle 当 Go 判据）+ FR-26（§1 数字标来源类型）。feasibility_report Q-DP4 章节 + literature_notes Q-DP4 条目已写。详见 `S021-qdp4-a0-assessment.md`
- **S022**（2026-07-14）：PROMPT-020 Q-DP4 维度 D MVE 执行（主控派出）。三验证完成，新建 `prompt020_qdp4_mve.py`（复用 prompt019 StandardCMA2x2 + ml_long_seq_failure + prompt012 evaluate_outputs，隔离原则不改 common/）。**V1 PASS**（6× PI-BER 差距分解，5 seeds）：B0 standard-CMA PI 0.0210 / B1 identity重跟踪 0.0180 / B2 per-block LS最优 0.0025 / B3 frozen 0.0240 / oracle 0.0084。B0/B2=8.3× 证明残余=swap相关权重漂移（CMA远离per-block最优），B1/oracle=2.2× 证明CMA跟踪能力够（从正确盆地跟踪SOP BER接近oracle）。**定位B（防跳变同时降swap+漂移）成立**——swap仅seed 1000/1002发生，B2在swap seeds也极低(0.0014/0.0112)=swap不损失信息是CMA权重没找到最优。**V2 PARTIAL**（改步长证否，SOP×f_G×μ矩阵）：大μ(5e-3)确实降swap-prone seeds的SOP退化（f_G=30 seed1000 ratio 4.9→1.3，seed1002 1.9→1.1，物理合理=更快跟踪SOP），但不完全消除（ratio仍>1.0）+发散风险（D006临界区μ≥5e-3）。f_G=1000时大μ ratio→1.04但信道本身变化快。**V3 FAIL**（形态2预防性约束）：V3a J_XCA（输出互相关惩罚）对clean swap**完全无效**（PI不变0.0393-0.0395）——clean swap时zX=sY/zY=sX仍独立QPSK输出互相关≈0梯度≈0，CA-CMA机制匹配错误（J_XCA为静态same-source singularity高互相关设计）；V3b diag约束（交叉FIR权重惩罚）最好α=0.1仅**1.24×**（远<2×阈值），大α(0.5/1.0)**反引发更多swap**（5/5 vs baseline 2/5）——swap不是交叉权重过大驱动是恒模代价多解地形在SOP旋转下让权重跳盆地，约束权重分量不改变地形结构。**D027新建：Q-DP4形态2 Kill**（V3 FAIL触发预注册Kill标准）。但V1证实Q-DP4问题陈述（D3=收敛后防swap）真实（8.3×改善空间），形态1（检测+回滚）/形态3（混合SOP补偿）未测。路线A保底不受影响。守FR-22+FR-11~15（架构摘要见S022）+FR-20（sop_rate=4e-7标sat.1553§6.3）+D018（双口径fixed/PI并报）+TL-20（理论预期先行）+TL-22（J_XCA无效查物理前提=clean swap互相关≈0）。详见 `S022-prompt020-qdp4-d-mve.md` + `projects/simulation/results/cma-fade-divergence/prompt020_qdp4_mve.json`
- **S023**（2026-07-15）：PROMPT-021 Q-DP4 形态1（检测+回滚）维度 D MVE 第二轮执行（主控派出）。新建 `prompt021_qdp4_form1_mve.py`（复用 prompt019 StandardCMA2x2 + prompt012 evaluate_outputs/_abs_corr，新增 block 级 swap 检测 compute_block_corr_series + detect_swap_events + Form1CMA 权重回滚类，隔离原则不改 common/）。**V0 发现 swap 是一次性永久锁定**（非设计预期的间歇反复跳变）：seed 1000/1003 swap 从 block 36698（sym 2.35M SOP~47°）持续到序列末尾（len=41426 blocks），late 段 swap_frac=1.0；clean seeds 1001/1002/1004 无 swap。swap 动态两阶段：①早期间歇期（block 21000-36000 ~1300个单block短暂swap CMA能自己跳回）②永久锁定（block 36698+ CMA无法自己跳回）。swap 间隔概念不适用（单次永久事件）→ 形式上 V0 PASS 继续 V1。**V1 KILL**（3 snapshot_windows {100,500,1000} × 5 seeds × threshold=0.5 全 KILL）：回滚后 dwell time 中位 **11 块**（704 sym=282ns，远<1000块Kill阈值），swap seeds n_rollbacks=888（late段几乎每11block回滚一次）。三 snapshot_window 无差异。FAIL 根因：swap 永久锁定后检测时（late段），最近100-1000块快照都已在swap盆地（swap已持续30000+block），回滚到swap盆地内快照=仍在swap盆地→立即再检测→循环回滚。**深度物理诊断（TL-22触发）**：回滚到早期快照（swap前25000+块）dwell长（block5000快照dwell=16083块）但BER从0.0176→0.0321→0.0589→**0.1226**恶性爬升（权重过时SOP旋转CMA跟踪不上）→ **不存在"既有长dwell又有好BER"的回滚点**。根本死因=SOP持续旋转+恒模代价多解地形的结构性矛盾（物理层面不可行非参数调优可解）。**三类响应式方法全FAIL统一证据链**：R7冻结（响应fade D010 ΔP_div=0全24组合）+ 压μ（响应fade D026 0/5胜PI更差）+ 回滚（响应swap 本轮 dwell=11）。**D028新建：Q-DP4形态1 Kill + Q-DP4整体Kill**。问题陈述真实（8.3×改善空间）但三种方法形态（约束Kill/检测回滚Kill/混合补偿未测但物理覆盖）都无法解决。S021 §3 警告（0跨域先例）部分应验。**GW Step4a 双偏振OSL三候选评估完成**：Q-DP1 Kill（D001）/ Q-DP3 Kill（D026）/ Q-DP4 Kill（D028）→ **路线A（Q-CMA-FADE D022+改动1）唯一存活方向**。守FR-22+FR-25（Go/Kill分离不用oracle当Go判据）+FR-20（sop_rate=4e-7标sat.1553§6.3）+D018（双口径fixed/PI并报）+TL-20（理论预期先行）+TL-22（深度诊断回滚早期快照BER爬升）。详见 `S023-prompt021-qdp4-form1-mve.md` + `projects/simulation/results/cma-fade-divergence/prompt021_qdp4_form1_mve.json`
- **S024**（2026-07-15）：PROMPT-022 改动1（物理判据驱动 ML 重训练）MVE 执行（主控派出，路线 A 方法层升级验证）。新建 `prompt022_modification1_mve.py`（复用 prompt019 StandardCMA2x2 + ml_long_seq_failure gen_channel/ML + prompt012 evaluate_outputs，新增 MonitoredStandardCMA 块级物理量监控 + run_ml_criterion_retrain 物理判据触发重训练，隔离原则不改 common/）。**预筛选（TL-22 单 seed CMA 物理量分析）**：D1（|w|>5×init）0% 触发（D013 swap 时 |w| 不发散）+ D2（J_CMA>5×baseline）0% 触发（D027 clean swap 恒模）→ D1/D2 物理上检测不到 swap；D3（Δw 漂移）唯一有效（0.3=21.7%/0.5=10.3% 触发率）。**验证1 KILL**（N=5M, 5 seeds, f_G=30, SOP=4e-7, strong, 20dB, QPSK, A/B/C/D1/D2/D3 双口径）：所有 D 方法 PI=0.01028 精确等于 B（ML训练一次）无改善。B PI=0.01028 ≈ oracle 0.00837（差距仅 0.00191）。**Kill 根因 1（最根本）**：改动1 前提（ML训练一次失效需重训练）在 PI 口径下不成立——D018 已确认 N=5M ML 是 clean swap（fixed≈0.5 但 PI≈0.005），ML 训练一次 PI 口径已接近 oracle，重训练无空间。D015"ML N=5M 全崩 BER=0.497"是 fixed-label 口径，改动1 基于错误口径设计。**Kill 根因 2**：物理判据检测不到 swap（D013/D027 推论经预筛选+MVE确认）。**Kill 根因 3**：C（固定周期重训练）PI=0.01626 反比 B 0.01028 差（每段用更少数据训练）。D015 Q3-B 报"PI=0.002"实为 fixed-label 4 旋转口径非 D018 PI 口径。**D029新建：改动1 KILL**。路线 A 方法层升级最后一张牌 Kill，Q-CMA-FADE 方法层定型为"弱"（D022 窄域 29/30 + 无架构创新 + 无重训练机制）。**GW Step4a 全部候选 + 方法层升级评估完成**：Q-DP1/DP3/DP4/改动1 全 Kill，唯一存活 = Q-CMA-FADE 分析层（强）+ 方法层（弱 D022）。守FR-22+FR-25（Go/Kill分离）+D018（双口径）+TL-20（理论预期先行D1/D2无效预期被证实）+TL-22（预筛选物理前提检查省大量无效计算）+TL-26（判据阈值标来源）。详见 `S024-prompt022-modification1-mve.md` + `projects/simulation/results/cma-fade-divergence/prompt022_modification1_mve.json`
- **S025**（2026-07-15）：Contract 阶段 S0-S3 执行（GW Step 4a → Contract 转阶段）。收 H010 handoff（Trigger 5 验证 3 事实：D022 PASS / D014 SOP=0 FAIL 无独立JSON / D029 PASS）。读 stages/contract.md 全文守 FR-22。**S0 PASS**（复用 GW 29 篇，reframe 后增量定位冻结：分析层 7 项 Qin/Nasr 全空白 + 方法层窄域，不换皮）。**S1 PASS**（瓶颈=恒模多解 SOP 跳变，引用 D014，SOP=0 时 CMA=oracle 证明非架构瓶颈）。**S2 PASS**（FR-17 子 agent 抽查 8 篇 67 去重：PI-BER 首选率 0% → 主指标改 fixed-label BER 75%，PI-BER 降辅指标；FR-19 模型假设记录；D018 双口径强制保留）。**S3 PASS**（全 [ASSUMPTION] 消除，SOP_RATE 仿真值债务标注；**D014 SOP=0 矩阵债务补 PASS**：子 agent 建 prompt023_sop0_matrix.py 隔离脚本，30 runs 428s，复现 SOP=0 ratio=1.00-1.01 / SOP=4e-7 ratio=1.12-6.93，方向一致强化 D014 核心声称）。contract.md draft 创建（`projects/thesis-fso/contract.md`，含 Problem Reference/H1+H2 Hypothesis/Success-Failure Signal/B1-B4 Baselines/M1-M4 Metrics FR-17调整/F1-F5 Fairness/A1-A5 Ablation/E1-E8 Experiments/Simulation Config/数据集设计/Parameter Provenance全标来源/C1-C5声称证据映射）。守 FR-22（转阶段读 contract.md）+FR-17（指标首选率审计）+FR-19（模型假设敏感性）+FR-20（参数溯源）+FR-25（Go/Kill 对手分离）+D018（双口径）+TL-21（文档审计用确定性证据）。详见 `S025-contract-s0-s3.md`
- **S026**（2026-07-15）：Contract S4-S5 + 冻结执行（Contract 收尾）。续 S025。**S4 PASS** — data-flow.md 创建（`projects/thesis-fso/data-flow.md`）：8 步 DSP 信号流推演适配网络路由模板（信道配置→信号生成→均衡器输入→处理→输出→BER 计算→评估指标→跨参数泛化），每步标真实代码来源（`ml_long_seq_failure.py:154` gen_channel / `_cma.py` CMAEqualizer2x2 / `_ml_equalizer.py` ButterflyCNNEqualizer2x2 / `prompt012_longseq_audit.py:98` evaluate_outputs）。FR-13 均衡能力表达力审计适配 DSP（非 RL 动作空间→均衡能力）：B1 standard-CMA 可比（ML<CMA 跟踪能力但 ML>CMA swap 免疫，窄域 D023 已标）/ B2 CMMA ≥（16QAM）/ B3 oracle <（预期 FR-25 不做判据）。FR-16 架构信息增量审计：训练前后输出不同（信息增量真实），但增量来源是监督学习数据非架构创新（F4 标注）。**S5 PASS** — experiment_completeness_checklist.md 创建：5 问压力测试无致命风险（分析层独立成立 + 方法层窄域量级优势 9×）；反模式 4 项 3 pass + 1 注意（反模式 3 确定性信道+DL 强行优越已诚实标注 D023 非致命）；Tier 1 六项全 pass（T1-4 逐模块消融适配 DSP 单组件场景：D022 ML-original vs ML-aligned 初始化消融是组件级等价性验证）。**Step 6 冻结**：用户确认 FR-17 主指标调整（fixed-label BER 主 / PI-BER 辅）后 contract.md status: draft → frozen。H011 交 Execute。守 FR-22（S4/S5 读 contract.md Step 4/5 段）+FR-13/FR-16（两项审计适配 DSP）+D018（双口径）+FR-25（Go/Kill 分离）。详见 `S026-contract-s4-s5-freeze.md`
- **S027**（2026-07-15）：D030 方法层解冻后 A 类（改 loss）GW Step 1 检索 + 横向 MVE 执行（主控派出，本轮）。新建 `prompt024_a_class_loss_variants.py`（隔离脚本，复用 ButterflyCNNEqualizer2x2 + gen_channel/oracle_equalize/evaluate_outputs，自定义训练循环支持 L0/L1/L2 三 loss）。**阶段 1 GW Step 1 检索**：3 方向各 2 组关键词（tools/search s2+openalex）+ 子 agent 撞车评估。A1 SOP 不变性正则 = NO（无人在均衡 loss 加 SOP/旋转不变性正则，都跟踪/估计 SOP）；A2 swap 对比 = NO（零对比学习偏振解复用）；**A3 VAE 盲损失 = YES 硬撞车**（Qin 组 2026 IEEE TCCN "Bootstrapping Blind Equalizer DP-coherent FSO via modulus-rings VAE" = 同作者组+同场景+同机制）→ A3 defer 不跑。**阶段 2-3 横向 MVE**（9 config × 5 seeds + 10 消融 = 55 runs, 6388s）：L1（SOP 不变性正则，λ=0.001 甜点）mean PI=0.01019 vs L0=0.01020，2/5 胜 p=0.75 → KILL；L2（swap 对比学习，λ=0.1 甜点）mean PI=0.01017，2/5 胜 p=0.75 → KILL；消融 PASS（λ=0 退回 L0）。L0 baseline 5-seed mean PI=0.01020 复现 D022。**A 类整体 KILL**。核心失败机制 = floor 效应（3/5 clean seeds PI≈0）+ 时序正交（loss 正则在训练段，swap 在 test 段）+ 与 D027 V3 同构（训练阶段修改触及不到 test 段 swap）。**D031 新建**：A 类 KILL + 火力重定向（排除训练阶段 loss 修改类，转向 test 段在线机制 D/E 或架构 B）。守 FR-22（GW Step 1 检索→MVE）+D030（归类批量+消融可验+检索防撞车）+D018（双口径 evaluate_outputs）+TL-20/22（假设先行+物理前提检查）。详见 `S027-prompt024-a-class-loss-mve.md` + `results/cma-fade-divergence/prompt024_a_class_loss.json`
- **S028**（2026-07-16，夜间 H013 C 类）：C1 周期 pilot-assisted 在线微调 `K=[1000,5000,10000]×lr=[1e-5,1e-4]` 六档全 0/5 胜 p=1.0，mean PI `7.952e-5–8.128e-5` 不低于 L0 `7.936e-5`，lr=0 消融逐 seed 退回 L0。**C 类整体 KILL/defer**（D032）：C1 KILL，C2 SOP 数据增强/C3 课程学习按 D031 时序正交 defer。检索 AdaNN 2020 + JLT 2023 joint PMD tracking 强邻近但无 FSO+GG+SOP lock-swap 硬撞。详见 `S028-*` + `prompt025_c1_online_finetune.json`
- **S029**（2026-07-16，夜间 H013 B 类）：B1/B2/B3 四判据形式可构造但均未过 D031 test 段准入门，**B 类整体 defer**（D033）不跑性能 MVE。B1 有 Optics Letters 2024 MIMO-CVNN/PDM 强邻近占点。`prompt026` 固化筛选合同。详见 `S029-*`
- **S030**（2026-07-16，夜间 H013 D 类）：D 类历史注册域 MVE KILL（D036；D034 REJECTED，D035 superseded）。strong GG 参数由 D022 的 1.5/0.8 漂移为 4.2/1.4 致 2/5→0/5；冻结历史输入后精确恢复 {1000,1003} 2/5 swap。D1/D2 mean PI=0.01505264 高于 L0=0.01043760，0/5 胜 p=1.0 KILL。baseline drift 债务关闭，未改 params.py。详见 `S030-*`
- **S031**（2026-07-16，夜间 H013 E 类）：E 类 pilot 前置 DEFER（D037）。test 段 pilot 估 SOP/Jones 前馈补偿过 D031，但 2023 JLT `10.1109/JLT.2023.3253383` 直接占"插入 pilot 估信道+前馈补偿跟踪 fast SOP"，FSO 迁移增量未证。四判据 PASS/UNRESOLVED/PASS/UNRESOLVED，不准入性能 MVE。`prompt028` 仅固化合同。详见 `S031-*`
- **S032**（2026-07-15）：方法层再探索 8 机制全景 + 统一规划。承接夜间 A-E 全类 KILL/defer 后用户质疑"不可能一点方法没有"。**参数域审计**澄清 4.2/1.4 是用户刚改的正确新参数（非漂移）。**oracle 上界关键发现**：fixed-label BER 0.4996→3.5e-5（4 数量级），PI-BER 仅 2×（对 swap 失明）。**8 机制全景**（A 注入CSI/B 内生不对称🔥/C 时间维/D 换范式/E ML范式🔥/F 硬件/G 跨层/H 换问题🔥）~40 思路。**MVE 执行图** Tier 0（B2+H1 物理前提）→ Tier 1（B 成立后 D2/B1/E2）→ Tier 2（E1/D3/C1）。待用户拍板 F1/G2 + Tier 0 顺序 + 检索批次。详见 `S032-method-layer-8-mechanism-plan.md`
- **S033**（2026-07-16）：S032 §F 执行图 Tier 0 物理前提 MVE + 检索批次 1 执行（执行 agent 本轮）。新建 `prompt029_b2_asymmetric_power.py`（5 功率比 × ML/CMA/oracle 三对照，非对称功率信道）+ `prompt029_h1_crc_flip_label.py`（ML fixed-weight 翻标签诊断 + block 级 swap 两阶段检测）。**关键事实校正（TL-22）**：swap 载体=ML fixed-weight（D015/D018），CMA standard 在新参数域 strong=4.2/1.4 下 5/5 clean（0 swap）；D028 的 2/5 swap 是旧域 1.5/0.8。H1/B2 smoke 初版误用 CMA（得 5/5 clean），修正为 ML fixed-weight 后才观察 5/5 clean-swap。**Tier 0-B2 KILL（D038）**：5 功率比 × 5 seeds，ML swap_rate=100% 恒定（SOP 泛化与功率对称正交），CMA 本域不 swap，极端比例伤 BER（oracle 3.5e-5→0.036）。机制 B 整体倾向 KILL。**Tier 0-H1 trivial Go（D039）**：5/5 clean-swap 翻标签恢复 5591×（0.4996→8.9e-5≈oracle），但=PI-BER（D018 已证）非新方法；0 degraded-swap。**检索批次 1（5 方向 B2/B1/H1/E2/D3）0 硬撞车**，注意 Le Bidan 2023（H1 强邻近须区分）+ 2015 Kalman（D3 定性 MMA=CMA singularity 须对冲）。范围拍板：F1/G2 排除（用户）。**火力重定向信号**：A 类（D031）+ D027 V3 + B2（D038）三度同构失败→"swap 是 test 段 ML SOP 泛化，训练段 loss/约束/对称性触及不到"，最有希望剩余=E 类架构（攻 SOP 泛化）+ H 类。守 FR-22+D030+D018+TL-22。详见 `S033-tier0-b2-h1-mve.md` + `results/cma-fade-divergence/prompt029_b2_asymmetric_power.json` + `prompt029_h1_crc_flip_label.json`
- **S034**（2026-07-16）：S033 §F 方法层 Tier 1 两方向执行（本轮）。**方向 1 E1 群等变 NN FAIL**（`prompt031_e1_equivariant.py`）：约束等变（soft equivariance，训练 loss 加 `‖f(R(θ)r)-R(θ)f(r)‖²`，θ~U[0,2π]）。seed=1000 完整三 λ：L0 fixed=0.49937 / E1 λ=0.01 fixed=0.49939 / E1 λ=1.0 fixed=0.49940，全 clean_swap，改善 1.0×。与 D031（A1 SOP 不变性正则 KILL + A2 swap 对比 KILL）三度同构——**训练段任何几何约束（不变性/对比/等变）都触及不到 test late 57° SOP 旋转**。约束等变（soft）≠ 严格等变（hard，需 e2cnn SO(2) 群卷积重写架构）。**方向 2 CMA+H1 组合 PASS 但弱于 ML+H1**（`prompt031_cma_h1_combo.py`）：5 seeds 完整，CMA 5/5 swap（4 clean_swap + 1 degraded_swap seed1004），翻标签 fixed 0.484→flip 0.0169（28.6× 改善）。ML+H1 对照 flip 8.25e-5（5591×）更好。CMA degraded_swap seed1004 翻标签只救到 7.6e-2（CMA 在线输出质量差）拖后腿。CMA+H1 ≠ PI-BER trivial（CMA 在线输出随 SOP 持续演化，翻标签是 post-hoc 翻"CMA 锁错"），但不构成方法层升级（弱于已有 ML+H1）。GW Step 1 E1 检索复核：夜间 2 组 rotation-equivariant 查询 40 命中全邻近领域（遥感/光纤传感/diffractive NN/PolSK），**0 硬撞车**（最强相关 Nasr 2026 ANN-FSO 已知 baseline + Chen 2023 QNN-PolSK 无线非光）。守 FR-22（E1 GW Step 1 复核）+ D030（消融可验 λ=0 退回 L0）+ D018（fixed/PI 双口径）+ S033 不变量 9/10/11（correlation 口径 classify_swap + fixed-label Go 判据 + cma_equalize 用 prompt030 口径）。详见 `S034-tier1-e1-cma-h1-mve.md` + `results/cma-fade-divergence/prompt031_e1_equivariant.json` + `prompt031_cma_h1_combo.json`
- **S035**（2026-07-16）：S033 §F 方法层 Tier 1 两独立方向执行（与 S034 并行，本轮）。**方向 2 D3 MMA KILL**（D040，`prompt032_d3_mma_mve.py`）：MMA（Yang 2002 多模，实/虚部模值分离 R²_R=R²_I=0.5）vs standard-CMA 0/5 胜 p=0.5，mean fixed MMA=0.0112 vs standard-CMA=0.0002，无增量。MMA 打破相位旋转对称非 X/Y 排列对称（正交）。消融 SOP=0 两者都正常 PASS。**附带重大发现（S033 不变量 9 部分修正债）**：standard-CMA（有 z 因子 Godard 1980）在新域 4.2/1.4 下 5/5 不 swap（fixed≈2e-4），ML 5/5 clean-swap（fixed≈0.495），current-CMA（无 z 因子 common/_cma.py）5/5 swap——**S033 不变量 9 "CMA 和 ML 都 swap" 部分是 current-CMA 无 z 因子 bug 假象**，swap 主因是 ML 固定权重 SOP 泛化（D015 回归）。GW Step 1 检索 0 硬撞车（邻近=光纤色散 MMA-singularity 线 Yang 2002/Vgenis 2010/Kikuchi 2011；2015 Kalman 邻近点未定位疑似误标注）。**方向 1 E2 排列对称破缺 KILL**（D041，`prompt033_e2_perm_symmetry_break_mve.py`）：非对称锚点（gX≠gY 可学习门）+ 排列敏感正则。smoke 验证标准 ButterflyCNN 精确排列等变（|zX(orig)-zY(swap)|=0），E2 成功破缺（=0.35）。但 λ=0.01（5/5）+ λ=0.1（2/2）全 clean-swap（fixed≈0.4996）与 L0 完全相同，λ=1.0 待 checkpoint 补。第四度同构证实"训练段修改触及不到 test 段 swap"（D031→D027 V3→D040→D041）。GW Step 1 检索 0 硬撞车（邻近=音频 BSS Audioslots arXiv 2305.05591 非光学；Pan 2026 OE 盲 CMA-DNN 仍困 swap 证实空白）。**Tier 1+2 全部完成无 Go**（E1 FAIL/D3 KILL/E2 KILL）。守 FR-22（两方向 GW Step 1 检索）+ D030（消融可验）+ D018（双口径 evaluate_outputs）+ S033 不变量 + 铁律 #2/#3（fixed-label Go + correlation 分类）。详见 `S035-tier1-d3-mma-e2-perm-mve.md` + `results/cma-fade-divergence/prompt032_d3_mma_mve.json` + `prompt033_ckpt.json`（E2 λ=1.0 待补）
- **S036**（2026-07-16）：接收用户自主推进授权并完成方法层状态复位。D042 冻结自主权边界（软件 DSP/ML A-E+H；F1/G2 仍排除；每候选必须 Q#+GW 全链）；D043 将 strict equivariance/e2cnn 作为 fixed-label 解法在 A0 NO-GO。三路线比较后仅选择 standard-CMA 前端 + ML residual cascade 进入候选 GW Step 1，尚未形成 Go、尚未设计或运行实验。详见 `S036-autonomous-method-search-reset.md`
- **S037–S039**（2026-07-16）：residual cascade 完成 Step 2 获取（5 篇全文）与 Step 3 精读（S038，5/5；无直接 additive-residual 先例）；Q14 四判据第 2 条 UNKNOWN，按 gw-feasibility §0 在 Step 4a 前置门控 PIVOT/DEFER（D044），未进入 A0 §1–§6、未运行 MVE。下一候选需重走 Step 1。
- **S040/D045**（2026-07-16）：用户按时间线纠正“协议生硬化”问题，明确回到已有 CMA-fade/SOP lock-swap 基点，先列全候选族、归类、统一规划，再分批排跑；完整 GW/Contract 门控改为正式晋级少数胜者时执行，不再对每个微变体机械重复。
- **S041**（2026-07-16）：完成 6 类方法族、约 30 个变体的候选地图和 Batch 0–5 执行计划；统一 fixed/PI/swap/fade 诊断、paired seeds、消融和晋级阈值。独立前向测试确认 `method-family-batch-exploration` 能复现该工作流。
- **S042–S044**（2026-07-16）：Batch 0 基线审计 PARTIAL；确认 30 paired seeds 与 standard/current-CMA 差异，但 `CRITICAL=4` 且事件字段不足。Batch 0.5 进一步判现有 `r7`/`prompt030`/`prompt015` 均不得原样进入 Batch 1：参数硬编码、非 canonical shared generator、缺统一 first-swap/recovery、部分单流/终态口径。下一步以 prompt015 caller 骨架新建统一 Batch runner，不分别缝补历史脚本。
- **S045/V006**（2026-07-16）：隔离 worktree 中以 TDD 建立统一 Batch 配置签名、单 canonical shared realization、真实 prompt013 standard-CMA adapter、统一窗口 fixed/PI/swap/fade/divergence/recovery/censor、正式保存与 legacy 同 seed 等价门；端到端 N=512 smoke + 定向回归 99 PASS，独立逐条审查判 Batch 0.5 PASS。准入 Batch 1 首个短序列/少 seed 小批，不等于长跑放行。
- **S046/V007**（2026-07-16）：Batch 1 首个 Fade 单轴 smoke 完成：baseline/fade-freeze/gradient-clip 三变体共享 standard Godard-z 核心；baseline 与 prompt013 allclose，2×512 seed smoke 共同 valid_samples=480，freeze/clip 各触发 15 blocks，定向回归 102 PASS。仅判 smoke PASS，不作性能 Go/Kill。
- **S047/V008**（2026-07-16）：真实参数 small batch 的 schema/provenance 审计 PASS，但数值生成于 D046 RNG 修复前，现标 stale；只保留管线证据，禁止作物理/性能结论，需用修复后 generator 重跑。
- **H015**（2026-07-16）：交接至下一轮性能判断；明确不把 small batch 当 Go/Kill，下一步先决定是否扩大 paired seeds。
- **S048/V009**（2026-07-16）：定位并修复 GG big/small 共享 RNG 导致的 N-dependent prefix；修复后 5M seeds41–43 两种 block 均 `h<0.1=0`、prefix exact。旧 54.14% low-h 数字作废；freeze threshold=0.1 低信息/DEFER，clip 保留。
- **S049/V010**（2026-07-16）：用修复后 generator 重跑 S047；5 seeds×4臂 schema/provenance/finite 审计 PASS，freeze/fade仍全0，clip P99/P95仅seed42触发106/858 blocks；仅观察记录，不作性能结论。
- **S050/V011**（2026-07-16）：μ=1e-2 压力域 clip small batch 去重后审计 PASS；seeds41–45三臂均 valid=99968、无 divergence/swap/fade，P95/P99均有不同触发计数；仍仅 observation，不作 Go/Kill。
- **S051**（2026-07-16）：μ=1e-2、N=5M 性能筛选仅完成 seed41/P99 单臂 smoke（fixed/PI=0、无 divergence）；多臂同进程因内存被杀，标 PARTIAL，后续需流式/分臂执行。
- **S052/V012**（2026-07-16）：明确标注 N=1M fallback 压力批，5 seeds×3臂合同审计 PASS；全 BER=0、无 divergence/swap/fade，P95/P99 仅触发计数不同，判 observation-only/inconclusive。
- **S053/V013**（2026-07-16）：Batch2 fG=30/100/1000 事件 pilot，9 cells 全无 BER/swap/div/fade，审计 PASS；转为无事件对照，不盲目扩展。
- **S054/V014**（2026-07-16）：Batch2 SOP-rate pilot，`1e-5` 在 2/3 seed 出现 BER tracking failure（0.00400/0.00608），但全无 swap/div/fade；审计 PASS，依据 D047 转高速 SOP failure detector/recovery 侦察，不作 lock-swap Go。
- **S055/V015/D048**（2026-07-16）：高速 SOP 盲 detector scout；三种基础统计量对 2 个 oracle failure 提前召回 0/2，控制组有误报；JSON 算术一致但 evaluator 未入源码/SHA，证据 FAIL。先固化 evaluator+warm-up，再决定重跑或换 H/状态跟踪族。
- **S056/V016**（2026-07-16）：补齐 evaluator 源码、control-only calibration、warm-up、persistence、oracle post-hoc 和 TDD；2 tests passed，独立审查 PASS。synthetic smoke 仅证明 evaluator 逻辑，不改写真实 scout FAIL。
- **S057/V017/D049**（2026-07-16）：evaluator 接入可复现 N=100k 短 scout，旧 summary 缺 trace 时明确拒绝；4 tests、SHA、TX-free trace 审查 PASS。三基础统计量仍 recall=0/2，正式关闭该支线，转接收端几何特征侦察。
- **S058/V018/D050**（2026-07-16）：geometry scout 独立审查 PASS；Stokes-like ratio recall=2/2、control false alarm=0/3，准入短 pilot；cov-eigen 仅作敏感性臂，cross-correlation 降级。
- **S059/V019/D051**（2026-07-16）：Stokes short pilot 18 cells；control 新 seed 出现 oracle events，control-only 阈值前提失效，raw recall/FA 不可作有效 detector 证据。停止该支线，优先转 E pilot-assisted。
- **S060**（2026-07-16）：接口盘点确认 E 族需新增 dual pilot 注入器/data mask/2×2 SOP estimator；旧单偏振 pilot 和整段监督接口不可直接冒充。H 暂为 oracle 标注，不进长 recovery。
- **S061**（2026-07-16）：dual pilot seam + N=100k 短集成完成，6.25%开销、theta P95约0.05–0.08 rad；naive pilot injection 的 BER 未优于 baseline，且尚未消费 Jones estimate，待 V020 后进入真正 pilot-informed derotation/初始化消融。
- **S062**（2026-07-16）：pilot Jones derotation 三臂短跑初现正信号：seed41/43 baseline BER .00399/.00611，derotation 均为0，clean seed42不退化；naive pilot略差。待 V021 公平性/泄漏审查后扩展。
- **S062/V021/D052**（2026-07-16）：三臂公平性、same-realization、shared data mask、TX-free部署估计器审查 PASS；pilot Jones derotation 短集成 feasible，准入新 seed/rate/pilot-count 扩展，仍非性能 Go。
- **S063**（2026-07-16）：预注册 N=100k、8 seeds×3 rates×2/4/6 pilots 扩展；failure改善≥50%、clean不退化、overhead≤10% 才晋级。运行中，先主臂checkpoint再敏感性。
- **S064**（2026-07-16）：72-cell 扩展初步显示2p灾难性失败；4p改善14/15、clean退化0/9；6p改善15/15、clean退化0/9、均值改善89.37%。待 V022 后决定正式GW晋级。
- **S064/V022/D053**（2026-07-16）：72-cell 数据/provenance通过，但原汇总把任意正改善误作≥50%。正确为2p 9/15、4p 13/15、6p 14/15；2p另有发散分母不公平。暂不晋级，不改门槛，转Jones inverse稳定化单轴。
- **S065/D054**（2026-07-16）：EMA09 full24 在原门槛下 failure≥50%=15/15、clean退化0/9、无发散/同分母；6-pilot+EMA09冻结为正式GW Step1候选。旧grid历史SHA语义显式保留，不伪造快照。
- **S066/D055**（2026-07-16）：正式Step1主体检索确认generic pilot-assisted Jones/SOP tracking已撞车；Tavily补齐第三有效来源14条并强化邻近竞争证据。候选收窄为dual-pol OSL低pilot预算下Jones估计稳定性与fixed-label恢复权衡，待V025质量审查后进Step2。
- **S067**（2026-07-16）：Step2获取5篇完成状态审计：LCOMM2026全文已存在且success；其余4篇all_failed元数据留档，未冒充已读。Step1分类标注仍待补。
- **S068**（2026-07-16）：82条候选逐条priority/direct/adjacent/formal/narrow字段补齐，统计与S066对齐；待V026后闭合Step1质量门。
- **S068修订/V026b待审**（2026-07-16）：分类加入82/82唯一candidate_key与top-level stats；必读6、formal56、direct5/adjacent26/none51，修正Optics Communications formal和宽direct误标。
- **V026b闭合**（2026-07-16）：Step1质量门 PASS（82候选、3源、必读6、formal68.3%、两路线覆盖）；进入Step2/3，仍保留generic机制撞车和窄问题边界。
- **S069**（2026-07-16）：LCOMM 2026全文精读完成；确认方法族直接撞车，但其FPT光纤机制不等同OSL GG稀疏时域pilot+EMA，不能跳过后续Step3/3.5/4a。
- **S070**（2026-07-16）：4篇失败DOI补检仍无作者稿/arXiv，失败metadata与search-archive留档；转共享papers库的可核查邻近全文，明确不替代失败条目。
- **S071**（2026-07-16）：完成LCOMM+4篇共享库邻近全文结构化精读，均附content/meta/行号；待V027审查后闭合Step3五篇质量门。
- **S072/D056**（2026-07-16）：Step3.5 6组矩阵+LCOMM双向引用链完成，发现OE2021/TCOM2025/JLT2022-23更直接block-pilot Jones竞品；强制获取/精读后再4a。
- **S073**（2026-07-17）：Step3.5 41篇canonical结果与5篇direct浅读已集成；主控provenance复核纠正“5篇均无全文”的错误回报——OE2021已有完整HTML全文并转正式精读，其余4篇维持摘要级债务。V028待精读集成后执行，未提前进入4a。
- **S074/V028**（2026-07-17）：独立门控发现R1新增4必读+1建议未收敛、R2存在JLT2023 PDL/FPT直接竞品去重口径争议，且LCOMM(0 citations)不满足最高引用双向链要求；V028=PARTIAL，R3与JLT2022/OE2021引用链补检执行中，Step4a继续封锁。
- **S075/D057/V030**（2026-07-19）：一轮有限 archaeology 找回 `_gg_time.py` 精确 SHA `92eaa6…` 并固化为 raw Git blob；historical z-window `3d99d4…` exact equal。10-cell P03 probe 的 fixed/PI BER、SER 全0、visible headroom=0，按预注册 zero-headroom rule 触发 A；P03停止且不训练ML。独立终验43/43定向测试、7/7 runtime blobs、三次probe 6/6 SHA exact PASS。
- **S076/D058/V031–V032**（2026-07-19）：保留S075运行事实并纠正其候选级停止解释；首轮绕过审查FAIL后，补齐结构化decision class、DOMAIN以上scope certificate、真实证据/hash、独立复核、统计灵敏度与内容寻址receipt。第二轮独立终验PASS；Atlas receipt consumer仍是运行前硬前置。
- **S077/D059/V033**（2026-07-19）：建立唯一 Headroom Atlas 强门入口 `headroom-atlas/atlas_gate.py`（TDD 11 functional + 8 独立对抗测试 = 19 passed；不信任 PASS receipt 本身，对实时 assessment 字节重跑 validator；append-only 审计；token 类型分离 CELL_RUN/CLOSEOUT）。跑 baseline-only Stage A 11 cells × 10 paired seeds，覆盖 QPSK × SNR 5/10/15/20/25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192 × CSI_NONE × uncoded hard decision。0/11 cells 达 MDE 0.005（max visible headroom 0.00039，比 MDE 低 ~13×）；6/11 灵敏度受限（零错误但 rule-of-three UB > MDE），4/11 测得 negative（oracle affine 不胜 nearest on PI-SER）。exit=`NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`；Stage B 不触发。3 轴 INFRASTRUCTURE_BLOCKED（16QAM/receiver-CSI/coded-output），历史反例（D008–D015/D023、U20 coded）恰好落在被阻轴上 → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。独立 verifier 子 agent 5 区全 PASS（B001–B003/canonical 未触、B004 不存在、gate SHA binding 一致、3 cells 重算逐位一致含 P03 v1 anchor 零错误精确复现、aggregation 自洽）。P03 当前 status 不变=`P03_DOMAIN_ADEQUACY_UNRESOLVED`；ML/B004/Queue/Registry 仍禁止。下一步用户决策：① P03 暂停回候选池；② 建一条干净 closure（最有杠杆 16QAM）扩域重跑 Stage A；③ 换候选族（U36 等）。
- **S078/D060/V034**（2026-07-19）：完成 Direction Lab Portfolio Autopilot 目标设计。根因定位为单候选状态机和组合级停机权缺失；采用最小 `campaign.yaml + events.jsonl + reducer-built state.yaml + batch thin summary + campaignctl`，复用现有 CandidateMap/BatchPlan/EvidenceGate/claim-scope/canonical owners。首轮 shadow 要求至少 6 个有效批次、至少 3 个证据型机制族，每 2 批重排；达到下限前局部失败、阻断、critic FAIL 和正信号不触发用户方向拍板。独立审查首轮 PARTIAL，修复 scope/预算早停、刷批次、critic 独立性和生产停机漏洞后第二轮 PASS；当前可进入实现计划，尚未实现或运行。
- **S079/T002/V036**（2026-07-23）：执行 D062 带债豁免的 Pilot-Jones Step 4a 大包（A0→A′→A/B→D）。新建当前 worktree 自包含最小闭包（source-closure.yaml/metrics.py/pilot_jones_methods.py/run_pilot_jones_mve.py/mve-contract.yaml/test_pilot_jones_step4a.py 10 directed tests/result.json）。A0/A′/A/B 完成；D 性能 MVE **未运行**——两条独立 Kill 门在 semantic-smoke + bounded headroom 阶段触发：(1) A0 §1 致命 + FR-01 先验覆盖致命——real-rotation 信道 cond≡1 使假设失效 A（病态）结构缺席，固定 EMA09 把主指标覆盖到 oracle；(2) FR-21 headroom Kill——B1→oracle headroom 可忽略（预注册 B1/O=1.19，亚一个数量级，多 seed bit-equal）。历史 15/15 provenance 断裂已记录（batch1_fade_methods.py SHA mismatch），仅作 diagnostic prior，且为 pilot-vs-blind 比较非方法间比较。独立 integrity verifier V036=PASS（11 项结构性全 PASS；headroom 公式+contract stale 数字分歧已修复）；独立 science critic=KILL_WITH_CAVEAT（唯一 rescue 出包范围：升级 canonical 信道为 complex Jones/PMD/PDL）。**Provisional verdict=KILL，scope 限于 unitary real-rotation 实例化，不重构为杀方向本身**；待主控+用户确认，不进 Step 5/Contract/Execute。
- **S079 主控接收/V037/D063/T003**（2026-07-23）：fresh pytest 10/10；raw 重算 0/6/4。V037 修正 V036 漏审：contract 仍残留 0/7/3，且 2×BER 未证明等价 0.5dB。正式结论收窄为 unitary-real-rotation M-C-A Kill，family unresolved；T003 已授权物理模型充分性 + complex-Jones/PMD/PDL + task-matched baseline + 条件式 MVE。
- **S080/T003**（2026-07-23）：执行 D063 complex-Jones/PMD/PDL 模型充分性救活大包。物理证据（DGD≤6ps=1.5%T_S memoryless；component PDL<1dB cond<1.12；RSOP≤600krad/s 块内恒定；PMD/PDL 是 component/fiber 非大气）→ M0–M4 模型梯（`complex_jones_channel.py` 块常数叠加在 canonical generator 上，保留 shared-noise 契约）8/8 limiting-case tests PASS → task-matched B3（whitening/tapped）+ 正确 BER→Q² 口径（修复 T002 的 BER ratio≠dB 缺陷）→ headroom 门。**决定性结构发现：在最 P-favorable 深衰落（α=2.0/β=1.0/17dB）下，B3-vs-oracle headroom 不随损伤强度增长**——PDL 0→9.5dB（cond 1→3.6）headroom 与 M0 deep-fade-only control 完全相同（delta=0.0），PMD 40→160ps 不单调增长 → 残余 headroom 来自深衰落+噪声非 PDL/PMD 结构。P1（energy-weighted LS）全 cell 不胜 B3。formal MVE 未运行（gate 在 probe 阶段失败，结构性结论）。Integrity 独立重算 PASS（SHA 链/raw→aggregate bit-exact/seeds disjoint/13 directed tests PASS/protected byte-unchanged）；science critic 8 项攻击 survive。执行中修 TL-22 anomaly：oracle 只逆 J_b 不逆 SOP 旋转 R(theta) 致反常差于 B3，component-level trace 定位+修复+回归测试；M4 联合模型 FDE oracle 因需联合求解器排除出 headroom 表（scope 限制非 confound）。**Provisional verdict=`PIVOT_MODEL_NOT_JUSTIFIED`**（允许枚举）：complex-Jones/PMD/PDL 升级不在 2.5GBaud/64–100sym block 下重新产生方法级 Pilot-Jones gap，B3 关闭 headroom。T002 `UNITARY_REAL_ROTATION_MCA_KILLED` 扩展为即便 richer Jones B3 仍关闭。Pilot-Jones family 仍 `UNRESOLVED` 不在本轴关闭，待真正新轴（verified DGD≫T_S 频选或 sub-symbol 块变 Jones）。待主控验收；不进 Step 5/Contract/Execute，不新建 D064，不复活 Scout/P03，不改 protected/Skill/controller，未 push。详见 `projects/simulation/explore/pilot-jones-complex-salvage/synthesis.md`。
