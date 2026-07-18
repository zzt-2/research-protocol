# [R007] 自适应 CPR 定位、参数溯源与精炼边界

> 2026-07-15 | 关联：2026-07-14-ccisp-content-expansion / R006

## 调研问题

1. 是否可将“两阶段控制 + DA/NDA 分支”作为完整的自适应 CPR 方法，而不是以 estimator selector 作为论文身份？
2. 五组 Gamma--Gamma \((\alpha,\beta)\) 是否存在既有直接来源？
3. 导师所说“整段无意义”在全文中对应哪些可安全精炼项，预计可减多少？

## 发现

### 1. 方法身份

- 当前实现的数据流为：原始接收功率统计 → CV 一级门 → 盲功率代理与有效 SNR 二级门 → DA/NDA 分支 → 统一载波校正序列。该完整链可被定义为 `received-power-aware adaptive CPR scheme/method`。
- DA phase--time LS 与 NDA eighth-power recovery 是既有 component branches；控制器不直接产生新的相位估计公式。因此不得把 controller 或整套方案说成“new estimator”。
- 本地相近论文支持将多阶段/多部件完整处理链作为 CPR method/scheme/algorithm 的贡献主语；机制最接近的 adaptive detection 文献也将 switching 放在 framework 内部，而非放在标题主语。
- 推荐层级：`adaptive CPR scheme/method`（外层方法身份）→ `two-stage received-power-aware branch controller`（核心内部机制）→ existing DA/NDA branches。
- `two-stage` 若对外使用，必须限定为 two-stage control，避免被理解为两个相位估计阶段串联。

### 2. 五组参数来源

| 参数对 | 追溯结果 | 可对外支持的性质 |
|---|---|---|
| \((4.0,3.0)\) | 2026-05-30 首次入库时只有数值；后写材料出现无题名/DOI/页码的 “Trinh 2017” 标签；本地论文库未命中同一数值对 | `UNRESOLVED`：项目采用的弱湍流档位，无可核验直接数值来源 |
| \((2.5,1.8)\) | 同上 | `UNRESOLVED`：项目采用的中湍流档位，无可核验直接数值来源 |
| \((1.5,0.8)\) | 同上；现有记录只支持其代表更强闪烁，不能支持由 Andrews/Rytov 映射得到 | `UNRESOLVED` |
| \((1.2,0.9)\) | `params.py` 明确标为 `assumption`；sat.1553 只给 lognormal 场景的 \(\sigma_p^2=0.15\)，没有 GG 数值对 | 项目设计假设，不是文献直接值或推导值 |
| \((1.0,0.7)\) | `params.py` 明确标为 `assumption`；sat.1553 只给 \(\sigma_p^2=0.25\)，没有 GG 数值对 | 项目设计假设，不是文献直接值或推导值 |

关键证据：

- `projects/thesis-figures/simulation/sim_ch3_ber_bounds.py:23-25`：下行三组最早可定位数值记录，无来源字段。
- `projects/simulation/params.py:97-152`：下行三组虽标 `literature`，但只有泛化场景标签且审计为 WARNING。
- `projects/simulation/params.py:157-199`：上行两组明确为务实选取和 `assumption`。
- `papers/doi/10.1002_sat.1553/content.md:141-157`：只给 \(\sigma_p^2\)，未给本文 GG 数值对。
- `projects/simulation/ADVISOR_BRIEFING_2026-07-09_v2_ccisp.md:157`：既有记录已承认未完成 Rytov 标定且两套参数对不上。

### 3. 精炼边界

最高置信项：

- `sections/system_model.tex:27`：只删除末句无职责的 `Unlike ... not assumed ...`；不是整段删除。
- `sections/system_model.tex:31`：公式逐项复述可删；共享 realization 的公平性事实必须移至公式近处或比较定义处。
- `sections/method.tex:77`：第三次逐项复述 CV→proxy→13 dB→branch，是最明确的整段删除候选。
- `sections/method.tex:83`：保留参数来源、冻结和无 per-regime retuning；后半流程复述可压缩。
- `sections/method.tex:85`：不输入 turbulence label/realized gain 是必要真实性边界，只能与 `:83` 合并去重。
- `sections/introduction.tex:7` 与 `sections/conclusion.tex:4`：方法步骤和两套结果数字重复，可收束但不能删除贡献/结论职责。
- `sections/results.tex:47`：CI 包含零不等于证明“无性能惩罚”，该统计推断应收窄。

不应判为废话：

- `system_model.tex:12,29,35-37` 的幅度/辐照度、相位状态生命周期、100/256 分区和共享 realization。
- `method.tex:25` 的 LS slope/intercept 含义与统一输出接口；可逐句压缩，但不能整段按重复删除。
- `method.tex:39,81,83,85` 的 transmitted-bit-assisted ambiguity、信息访问、参数冻结和无场景标签输入。
- `results.tex:18,20,39-49` 的 BER 分母、oracle 边界、common-payload/CI 及 26/29 非选择准确率边界。

独立复核后，将可安全删减预算从初审的 430--560 词收窄为约 **250--350 词**；是否减少实际页数取决于浮动体与参考文献布局，不作保证。仓库最新 V009 对应 PDF 为 8 页且末页稀疏，用户所见 7 页可能是上一构建版本。

## 结论

- 方法定位：`PASS WITH BOUNDARY`。推荐将整体定义为接收功率感知的自适应 CPR scheme/method；selection 降为核心内部机制，不冒充新 estimator。
- 参数来源：`PARTIAL`。上行两组已闭合为设计假设；下行三组仍无可核验直接数值来源，禁止编造或用泛化场景标签冒充出处。
- 精炼合同：`PARTIAL`。已形成约 250--350 词的保守高置信删减边界；逐句合同尚待用户批准，未修改论文。

## 对决策的影响

- 暂不新建决策。推荐定位仍为待用户拍板方案；参数事实仍有未决来源；精炼仅为下一轮 change contract 输入。
- 未修改论文、图片、Skill、仿真代码或数据。
