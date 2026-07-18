# batchB agent-B2 产出（B 维后半 6 素材源：够格线/答辩原则/否决索引/SNR约定/审计rubric/贡献定位）

## 提取统计
- 处理文件：6（B17/B18/B19/B20/B21/B22）
- 产出条目：B={18}
- 行号校准说明：
  - B17（S006 L142-157）：R002 指针精确，实读确认够格线对照表在 L142-155，结论在 L157
  - B18（defense-principles.md）：R002 标"行号待补"，已实读校准——开题本质(L8-16)、PPT 内容规则(L22-44)、时间分配(L47-56)、Q&A 防御(L60-99)、叙事弧清单(L103-113)、延续原则(L116-124)
  - B19（design-decisions.md R01-R16）：R002 标"613 行否决索引段"，实读确认否决索引表头在 L549，R01-R16 在 L551-566（紧凑表格式，非 613 行；613 是文件总行数）
  - B20（S019 D011 段+12-agent验证表）：R002 指针精确，实读确认 D011 决策在 L336-344，12-agent Batch1-4 在 L200-330，SNR 约定敏感性致命发现在 L139-153
  - B21（H025 13检查项+11维度压测）：R002 指针精确，实读确认 13 检查项分散在 L22-62 的 3 个文件审计表，11 维度压测 F1-F11 在 L145-186
  - B22（investigation-nmse L194-201）：R002 指针精确，实读确认贡献定位措辞在 L198-201

## B 维度

```yaml
id: B-501
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:142"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "够格线对照表——按 8 维度（章节体系/仿真器/baseline 数/实验组数/多 seed/消融/统计检验/仿真规模）量化当前项目 vs 同方向典型硕士论文，逐维判定远超/超出/达标"
original_quote: "章节体系|1个问题|3章独立问题|远超；仿真器|1个简化拓扑|3个从零搭建|远超；统计检验|通常不做|p<0.0001|超出"
is_covered: "否"
covered_by: "N/A"
new_dimension: "够格线对照自检 rubric（8 维量化对标，评估论文是否达到学位门槛）"
```

```yaml
id: B-502
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:155"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "论文定位自检——用已发表 SCI 论文（Shi 2024 用 14 节点 NSFNet、3 baseline、无消融无多 seed）作为最低够格锚点，当前项目任何单章超过它即可定位偏上"
original_quote: "Shi et al. 2024 用 14 节点 NSFNet、3 个 baseline、无消融、无多 seed，发了 SCI。当前项目任何单章都超过它"
is_covered: "否"
covered_by: "N/A"
new_dimension: "已发表对标锚点（用真实 SCI 论文作下限参照，避免自评无锚）"
```

```yaml
id: B-503
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:135"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "ML/GNN 方向审查特化维度——纯调参不是创新、套模型换数据集风险高、消融+多 seed+近 2-3 年 SOTA 对比是必须的实验严谨性、自建数据集开源代码是加分项"
original_quote: "纯调参不是创新；套模型换数据集风险高；消融实验、多 seed、近2-3年SOTA对比是必须的实验严谨性"
is_covered: "是"
covered_by: "8 维 R1-R8 自审 rubric（R2 论断依据：消融/多 seed 属实验严谨性）+ 基线公平性审查（SOTA 对比）"
new_dimension: "N/A"
```

```yaml
id: B-504
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题PPT/defense-principles.md:8"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "开题答辩三问框架——评审视角的'讲故事'逻辑：为什么做（背景→现状→空白→不解决后果）/怎么做（方案自圆其说）/为什么能做（基础+可行性）"
original_quote: "开题是讲故事：为什么做|怎么做|为什么能做；拟字是保护伞——承诺问题和方法，不是结果"
is_covered: "否"
covered_by: "N/A"
new_dimension: "答辩三问叙事框架（评审委员会视角的开题结构自检）"
```

```yaml
id: B-505
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题PPT/defense-principles.md:30"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "开题 PPT 内容红线——不放具体仿真结果数字（开题阶段数字可能变）、不写结论（写了被追问）、不写公式、不用禁忌词（首次/填补空白/显著鸿沟/oracle CSI）、不提已证伪方向"
original_quote: "不放具体仿真结果数字；不在PPT上写结论；不写公式；不用禁忌词：首次/填补空白/显著鸿沟"
is_covered: "是"
covered_by: "学术诚信'避免绝对化用语'（首次/填补空白禁忌）+ 已证伪清单（不提 TL-03/06/07 自适应/湍流感知）"
new_dimension: "N/A"
```

```yaml
id: B-506
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题PPT/defense-principles.md:47"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "答辩时间分配策略——文献综述多讲（4-5min，评委最能判断且认可）、创新点少讲（少给追问空间）、技术路线图为主快速过"
original_quote: "研究意义4-5分钟重点讲经得起问；创新点少讲少给追问空间；核心策略：文献综述多讲创新点少讲"
is_covered: "否"
covered_by: "N/A"
new_dimension: "答辩时间分配策略（强弱项暴露控制——强项多讲弱项少给空间）"
```

```yaml
id: B-507
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题PPT/defense-principles.md:62"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "Q&A 防御策略——不主动暴露弱点（PPT 不写结论则评委只能问'打算怎么做'）、被追问用'拟'字挡、诚实但不自贬（专硕不要求新方法）、对标已发表论文定位"
original_quote: "不主动暴露弱点；被追问时用拟挡；诚实但不自贬；对标Han2022/Petkovic2023"
is_covered: "是"
covered_by: "导师硬底线 + 已发表对标（Han2022/Petkovic2023）"
new_dimension: "N/A"
```

```yaml
id: B-508
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题PPT/defense-principles.md:103"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "叙事弧检查清单——讲完后评委应能回答 6 问：课题为什么重要/别人做了什么还差什么/不解决会怎样/打算怎么做/凭什么能做/创新在哪"
original_quote: "评委应能回答：为什么重要？别人做了什么还差什么？不解决会怎样？打算怎么做？凭什么能做？创新在哪？"
is_covered: "否"
covered_by: "N/A"
new_dimension: "叙事弧闭环自检（6 问覆盖率检查，答辩完整性 rubric）"
```

```yaml
id: B-509
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:549"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "否决索引范式——R01-R16 每条 4 字段（ID/方案/否决原因/证据来源），否决记录必须带可回溯证据指针（S024§D2/S002§3.6/导师反馈等），本身是'否决记录该怎么写'的元范例"
original_quote: "R01|方向B(信道跟踪→预补偿闭环)|与Ch4循环依赖|方向评估；R09|湍流感知R矩阵作为贡献|B2+D3双重验证FAIL|S024§B2,§D3"
is_covered: "否"
covered_by: "N/A"
new_dimension: "否决记录范式（4 字段：ID/方案/否决原因/证据来源，每条必带可回溯指针）"
```

```yaml
id: B-510
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:551"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "方向否决判据 R01-R03——方向 B 因与 Ch4 循环依赖否决、方向 C 因创新空间窄否决、方向 E 因 τ/T_coh<10⁻⁶ 预测≡估计否决：方向选择必须有结构性/物理性硬约束作否决理由"
original_quote: "R01方向B|与Ch4循环依赖；R02方向C|创新空间窄；R03方向E|τ/T_coh<10⁻⁶预测≡估计"
is_covered: "否"
covered_by: "N/A"
new_dimension: "方向否决判据（循环依赖/创新空间窄/物理不可行三类硬约束）"
```

```yaml
id: B-511
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:558"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "声称否决判据 R08/R09/R14——KF 全湍流适用（强湍流差 1.4dB）、'湍流感知 R 矩阵'作为贡献（B2+D3 双重 FAIL）、VV CPR 在湍流信道使用（BER 恶化 2-3×）：声称必须经仿真证伪门控"
original_quote: "R08|KF全湍流适用声称|强湍流差1.4dB|S024§D1；R09|湍流感知R矩阵作为贡献|B2+D3双重FAIL；R14|VV CPR|BER恶化2-3×"
is_covered: "是"
covered_by: "压力测试 FAIL→结论证伪（pilot B-301）+ 已证伪清单（pilot B-207，X-01~X-09）"
new_dimension: "N/A"
```

```yaml
id: B-512
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:562"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "方法否决判据 R06/R07/R15/R16——Hu2025 erfc 法（已有闭合形式不需）、P_s/2 近似（median 误差 6%）、自适应 CPR 切换（湍流强度非合理判据物理站不住）、Wiener 最优 B_L∝√h（过于复杂线性 h 足够）：方法选择权衡收益 vs 复杂度/精度"
original_quote: "R06|Hu2025 erfc|已有闭合形式不需要；R07|P_s/2近似|median误差6.0%；R15|自适应CPR切换|湍流强度不是合理判据；R16|Wiener最优√h|线性h足够"
is_covered: "否"
covered_by: "N/A"
new_dimension: "方法选择否决判据（收益-复杂度-精度三维权衡，已有替代方案/误差超阈/物理判据错误即否决）"
```

```yaml
id: B-513
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S019-ch2-derivations-and-verification.md:139"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "SNR 约定敏感性致命发现——Ch2/Ch4 用 γ∝h²（IM/DD 约定）与 Ch3 用 γ∝h（相干检测约定）跨章不一致，相干检测物理上 γ∝h 正确，约定差异导致 N_opt∝h⁻⁴ vs h⁻²、E[1/h²] 收敛条件 min>2 vs min>1 等结论级影响"
original_quote: "跨章SNR约定不一致：Ch2链路预算γ∝h²|Ch4自适应γ∝h²→N_opt∝h⁻⁴|新Ch3 γ=γ̄·h；相干检测γ∝h正确，Ch2/Ch4的γ∝h²是IM/DD约定"
is_covered: "否"
covered_by: "N/A"
new_dimension: "约定/假设敏感性审查（同一物理量不同约定导致指数级结论差异，跨章约定一致性是致命级检查）"
```

```yaml
id: B-514
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S019-ch2-derivations-and-verification.md:200"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "12-agent 多维并行验证流程——数学正确性/文献交叉验证/物理一致性三视角并行，物理一致性 agent 发现 SNR 约定致命不一致；文献验证分 4 批（物理模型根基/Ch2/Ch3/Ch4+仿真）逐步收敛"
original_quote: "三agent并行验证：Agent1数学正确性21/21PASS；Agent2文献交叉验证；Agent3物理一致性致命发现跨章SNR约定不一致"
is_covered: "否"
covered_by: "N/A"
new_dimension: "多维并行验证流程（数学/文献/物理三视角并行，单一视角无法发现约定级问题）"
```

```yaml
id: B-515
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S019-ch2-derivations-and-verification.md:306"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "约定选择权衡矩阵——三方案（A h=辐照度/B h=幅度/Agent12 h=等效基带系数）按物理严谨性/论证强度/代码改动/答辩风险四维量化对比，选物理严谨性最高方案 A（D011）"
original_quote: "方案A物理严谨性最高论证弱化代码改动大答辩风险低；方案B物理中论证最强代码无改动风险中；选A理由：文献主流+Ch3无需改+物理透明"
is_covered: "否"
covered_by: "N/A"
new_dimension: "约定选择权衡矩阵（物理严谨性/论证强度/代码改动/答辩风险四维量化决策）"
```

```yaml
id: B-516
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/H025-ch3-audit-result.md:8"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "审计 rubric 范式——13 检查项分 5 类（信号模型 A1-A3/参数 B4-B6/评估方法 C7-C8/数值验证 D9-D10/代码质量 E11-E13），每项给 PASS/FAIL/WARNING/FATAL 四级量化结论 + 证据行号"
original_quote: "审计13检查项：信号模型A1-A3|参数B4-B6|评估方法C7-C8|数值验证D9-D10|代码质量E11-E13；FATAL:0 FAIL:0 WARNING:4 PASS:9"
is_covered: "否"
covered_by: "N/A"
new_dimension: "审计 rubric 范式（5 类检查项 + PASS/FAIL/WARNING/FATAL 四级量化 + 证据行号）"
```

```yaml
id: B-517
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/H025-ch3-audit-result.md:145"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "11 维度压力测试 F1-F11——Meijer-G 稳定性/Fourier 收敛/闭合解 vs MC 全扫描/BER floor 大 σ/中断概率二分查找/SNR 惩罚湍流无关性等，按必须做/高优先/中低优先分级，每维给 PASS 标准 + 失败数 + 根因 + 是否需修复"
original_quote: "F1 Meijer-G稳定性FAIL73根因SNR=30dB未收敛阈值过严否；F6 P_s/2近似偏差FAIL66弱湍流+高SNR偏差>10%是；F10 SNR惩罚湍流无关PASS0"
is_covered: "否"
covered_by: "N/A"
new_dimension: "压力测试 rubric（11 维分级 + PASS 标准/失败数/根因/是否修复四字段，区分公式错误 vs 阈值过严 vs MC 限制）"
```

```yaml
id: B-518
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/verification/investigation-nmse-literature-review.md:198"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "贡献定位精确化——贡献不是'发现信道估计误差不影响 BER'（这在特定条件下已知），而是'量化了影响程度(<0.3dB)+发现 h 对消机制+区分路径 A/B'：贡献声称必须精确到不被误读为已知结论复述"
original_quote: "贡献不是'发现信道估计误差不影响BER'，而是：量化了FSO湍流信道下h估计误差通过载波恢复路径对BER的具体影响程度(<0.3dB)；发现了h对消机制；区分了路径A和路径B"
is_covered: "否"
covered_by: "N/A"
new_dimension: "贡献定位精确化（声称须区分'已知现象复述' vs '本工作增量'，量化程度+机制发现+路径区分三维定位）"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（审查rubric×7、规则清单×5、失败案例×6）
- [x] 所有 source_ref 含行号（18 条均带 :Lxx，WSL 路径 /mnt/d/...）
- [x] 所有 date_validity/direction 已标注（B17/B501-503 标"方法论可继承-技术作废"+"旧(NTN/DRL)"；B18-22/B504-518 标"有效"+"当前(FSO)"）
- [x] id 前缀均为 -5xx（B-501~518）
- [x] is_covered 判定与 pilot + agent-B1 的 B 条目一致（已有 rubric 不重复造 new_dimension）
- [x] 同形态字段结构与其他 agent 一致（B 维 11 字段顺序与 scan-template.md FROZEN schema 完全一致）
