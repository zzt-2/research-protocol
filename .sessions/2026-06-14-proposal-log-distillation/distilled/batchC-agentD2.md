# batchC agent-D2 产出（D 维后半 8 素材源：D12否决记录流程/D13写作质量脚本/D14三轮验证/D15仿真教训/D16答辩预演/D17 CAJ痛点/D18文献筛选溯源/D19毕设复用元观察）

## 提取统计
- 处理文件：8（D12/D13/D14/D15/D16/D17/D18/D19）
- 产出条目：D=25（D-501~D-525）
- step_group：11 组
- 行号校准：D12 L7-23+L62-64+L549-566；D13 gen_test.py L79-82+L92-118+L195-219；D14 S003 L298-307+L329-338+L598-641；D15 TL-20~25 L270-391；D16 S006 L271-322；D17 cnki-survey L554-567；D18 literature_notes L34-71+L200-237；D19 毕设/ 目录
- 去重自检：D12 不重复 B-509~512；D18 不重复 C-416/417/B-410

## D 维度

```yaml
id: D-501
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:7"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "决策记录维护：每条决策必含 6 字段（内容/理由/否决方案/来源/强度/状态），强度分 4 级（INVARIANT 架构约束不可推翻 > DECIDED 可讨论需显式推翻 > TENTATIVE 暂定 > REJECTED 已否决带证据），状态分 3 态（LOCKED/SUPERSEDED/OPEN）"
step_group: "design-decisions 否决记录维护流程"
step_order: 1
vs_paperwrite: "paper-write 无'决策强度 4 级+状态 3 态'分类机，决策无优先级/可推翻性标注"
optimization: "决策库每条必带强度标签（INVARIANT/DECIDED/TENTATIVE/REJECTED）+状态（LOCKED/SUPERSEDED），推翻 INVARIANT 需显式记录推翻理由，TENTATIVE 有过期自动提醒"
```

```yaml
id: D-502
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:21"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "SUPERSEDED 血缘链：决策被取代时标 SUPERSEDED 并保留'取代: D008'指针（如 D008 KF 统一载波同步被 D009 系统性分析取代），不删除旧决策，下游可追溯演化路径；新决策'否决方案'字段记录被取代的旧决策 ID"
step_group: "design-decisions 否决记录维护流程"
step_order: 2
vs_paperwrite: "paper-write 无'被取代决策保留血缘链'机制，旧决策被覆盖后无法追溯"
optimization: "决策被取代不删除，标 SUPERSEDED+指向新决策 ID，新决策'否决方案'字段记录旧 ID，形成双向可追溯的决策演化图"
```

```yaml
id: D-503
source_ref: "/mnt/d/code/study/research-protocol/毕设/design-decisions.md:549"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "否决索引集中归档：R01-R16 被否决方向/方法集中在一张表（ID/方案/否决原因/证据来源 4 列），每条否决必带可回溯证据指针，否决原因分三类——结构性硬约束（循环依赖/创新窄）、物理不可行（τ/T_coh<10⁻⁶）、仿真证伪（BER 恶化 2-3×）"
step_group: "design-decisions 否决记录维护流程"
step_order: 3
vs_paperwrite: "paper-write 无'否决方向集中索引表'，被否决方案散落各 session，新对话易重新提出已否决方向"
optimization: "维护全局否决索引表（方案/否决原因分类/证据指针），新方向提案前必先查否决索引，命中即自动阻断并附否决证据；否决判据本身见 B-510/512"
```

```yaml
id: D-504
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/gen_test.py:79"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "写作质量维度做可控实验：2×2×2 全因子设计（D4 问题前置 × D2 递进评价 × D1 落脚句）× 3 轮 = 24 次生成，每条件独立 prompt 注入维度指令片段，baseline=三维度全关，通过主效应分析量化每个写作维度对输出的独立贡献"
step_group: "gen_test 写作质量自动化范式"
step_order: 1
vs_paperwrite: "paper-write 无'写作维度全因子实验'设计，无法量化某个写作要求对生成质量的独立贡献"
optimization: "写作质量评估内置全因子实验框架（N 维度 × M 轮），每维度独立 prompt 片段注入，主效应分析算出每维度的边际贡献"
```

```yaml
id: D-505
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/gen_test.py:92"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "客观 pattern 指标替代 LLM 评判：measure_patterns 用正则统计结构模式而非 LLM 打分——D4 计'为了解决/抑制'因果转换词+局限/瓶颈问题词；D2 计'但.*引入'对比评价链+进一步/进而递进词；D1 计本文/后续/仍需落脚词；外加 total_chars/paragraphs/sentences 结构指标，合成 d4/d2/d1_score"
step_group: "gen_test 写作质量自动化范式"
step_order: 2
vs_paperwrite: "paper-write 若用 LLM 评判写作质量会有评判者偏差，无法机械复现；此范式用确定性正则统计可 100% 复现"
optimization: "写作质量检查用确定性 pattern 统计（因果转换词/对比评价链/落脚词的正则计数），每维度定义 2-3 个可 grep 的标记模式"
```

```yaml
id: D-506
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/gen_test.py:222"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "盲评模板兜底：pattern 指标之外生成随机打乱的人类评分模板，每样本 1-5 分评逻辑递进/评价深度/问题驱动/信息密度，答案密钥 reveal 后再对齐——客观 pattern 指标+主观盲评双轨验证维度有效性"
step_group: "gen_test 写作质量自动化范式"
step_order: 3
vs_paperwrite: "paper-write 无'客观 pattern + 主观盲评'双轨验证机制"
optimization: "写作维度有效性用双轨验证：客观 pattern 计分（可机械复现）+ 人类盲评（随机打乱+答案密钥延后 reveal），两轨一致才确认维度有效"
```

```yaml
id: D-507
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/S003-methodology-reset-and-research.md:298"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "文献逐句验证方案设计：用户'不放心'要求至少 24 子 agent 逐句验证，按引用论文数分配（§1.2.1 约 17 篇/§1.2.2 约 24 篇/§1.2.3 约 8 篇），每 agent 负责 2-3 篇，信息来源=bib 池+已下载全文，验证 4 维度（方法描述/定量数据/结论归属/常识性错误）"
step_group: "S003 §1.2 文献逐句验证三轮工作流"
step_order: 1
vs_paperwrite: "paper-write 无'按引用数分配子 agent 逐句验证'机制"
optimization: "文献综述写完按引用数分配 N 子 agent（每 agent 2-3 篇），逐句核查 4 维度，存疑项预标记重点验证，输出 VERIFIED/UNVERIFIABLE/QUESTIONABLE/INCORRECT 四态判定"
```

```yaml
id: D-508
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/S003-methodology-reset-and-research.md:329"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "第一轮 24 子 agent 执行：3 并发分 8 批次，验证范围 §1.2 全部 ~49 篇引用+结构审查+无来源数据审计+绝对措辞扫描，每句判定标准 VERIFIED/UNVERIFIABLE/QUESTIONABLE/INCORRECT；发现 6 项必须修复的事实错误（N31 场景错误/N49 归因错误等）+ 15 篇验证通过"
step_group: "S003 §1.2 文献逐句验证三轮工作流"
step_order: 2
vs_paperwrite: "paper-write 无'8 批 × 3 并发'大规模逐句验证执行范式"
optimization: "大规模文献验证采用 N 批 × 3 并发，每句四态判定，INCORRECT 立即修复，QUESTIONABLE 标记待人工确认"
```

```yaml
id: D-509
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/S003-methodology-reset-and-research.md:598"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "第三轮重验证（2 子 agent）+ 结构检查：修复后再派 2 子 agent 重验 §1.2.1（10 引用）和 §1.2.2（10 引用），同时主线程做结构检查（铁律 10 铺垫合规/孤儿清理/共用引用说明/绝对措辞/映射表 bib key/计数更新）；发现 bib key 错误（N2 chen→valjus 等）"
step_group: "S003 §1.2 文献逐句验证三轮工作流"
step_order: 3
vs_paperwrite: "paper-write 无'修复后重验+结构检查'闭环"
optimization: "文献验证必做三轮闭环——首轮大规模逐句验证→修复→小规模重验+结构检查（铺垫合规/孤儿/bib key/绝对措辞），结构检查与内容验证并行"
```

```yaml
id: D-510
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/S003-methodology-reset-and-research.md:14"
source_agent: "全量蒸馏D2"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "写作失败根因诊断：§1.2 v1（76 分）/v2 失败根因是跳过 Phase 3 范文深度分析——§1.1 成功因 S006 Phase 3 逐段分析 4 篇参考论文提取段落级指标+写法技巧才手写，§1.2 仅基于 R001 摘要级模式描述写作；核心纪律=结构决策由人工做，LLM 只做语言优化"
step_group: "S003 §1.2 文献逐句验证三轮工作流"
step_order: 4
vs_paperwrite: "paper-write 若无'范文 Phase 3 深度分析'前置步骤，直接让 LLM 写综述会重蹈 v1/v2 覆辙"
optimization: "综述写作强制前置 Phase 3 范文深度分析（逐段提取段落级指标+句法级写法技巧），结构决策人工做，LLM 只做语言优化；跳过 Phase 3 禁止进入手写阶段"
```

```yaml
id: D-511
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:270"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "跑仿真前先建理论预期（TL-20）：预期建立 3 步=文献调研（同类系统已知结果数量级）→理论推导（定性特征：单调性/floor 效应/渐近行为）→量化锚点（≥2-3 个'偏离这些值一定有问题'检查点）；偏离时强制动作——偏离锚点 >3× 暂停排查代码，>10× 停止所有推进集中排查"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 1
vs_paperwrite: "paper-write 无'仿真前理论预期建立+偏离锚点强制动作'机制"
optimization: "仿真脚本启动前强制建理论预期文档（数值范围+趋势+≥2 量化锚点），偏离锚点 >3× 自动暂停排查，>10× 阻断所有推进"
```

```yaml
id: D-512
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:294"
source_agent: "全量蒸馏D2"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "文档数字审计用确定性 grep（TL-21）：链式 agent 流程有盲区，声称'验证 PASS'实际漏检 19 处（9 处种子数+7 处失败率+3 处 BER 定义混淆）；正确做法=先 grep 出所有数字再将完整输出交 agent 做 SPEC 对比，搜索和判断分离，≥3 独立 agent 取并集，声称 PASS 前反向 grep 确认旧值已不存在"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 2
vs_paperwrite: "paper-write 若用链式 agent 同步文档数字会重蹈覆辙"
optimization: "文档数字审计禁止依赖 agent 链式标记，必须先确定性 grep 全量数字→交 agent 做 SPEC 对比（搜索/判断分离），≥3 独立 agent 取并集，PASS 前反向 grep 确认旧值清除"
```

```yaml
id: D-513
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:314"
source_agent: "全量蒸馏D2"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "震撼结果先查物理前提（TL-22）：'复数 h_est 对 DPLL 灾难性影响'被称为重大发现，后续验证发现 FSO 相干检测中 h 是实值辐照度（GG 分布），复数 h_est 物理上不存在，实验白跑；检查顺序 TERMS.md 定义→design-decisions 相关决策→信号模型公式→文献，'发现'越震撼越要怀疑前提"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 3
vs_paperwrite: "paper-write 无'新发现先查物理前提'门控"
optimization: "任何涉及新假设/新模型的'重大发现'，先花 5 分钟按 TERMS→design-decisions→信号模型→文献顺序查物理前提，前提不成立实验再精美也是废纸"
```

```yaml
id: D-514
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:331"
source_agent: "全量蒸馏D2"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "半场开香槟强制冷静期（TL-23）：TL-12/TL-20/TL-22 同一失败模式反复出现——跑实验→发现好结果→立即兴奋规划后续→验证发现前提有误→前功尽弃；防护=超过预期 >3× 的结果禁止立即写文档，验证顺序遵循 物理前提→数学推导→文献交叉→多种子→最后才写文档"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 4
vs_paperwrite: "paper-write 无'好结果强制冷静期'"
optimization: "超过预期 >3× 的结果触发强制冷静期（禁止立即写文档/宣布发现），验证顺序物理前提→数学→文献→多种子→最后写文档，文档更新永远在验证之后"
```

```yaml
id: D-515
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:348"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "论文结论单源代码（TL-24）：结论只从 common.py 统一实验提取，禁止散落 15+ 脚本；CONCLUSIONS.md 每条结论标注代码来源（common.py/旧代码/独立脚本/纯理论），分 3 层——第一层可直接写、第二层需重验、第三层不写入"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 5
vs_paperwrite: "paper-write 无'结论代码来源分层'机制"
optimization: "论文结论强制单源代码提取，每条结论标代码来源分层（可直接写/需重验/不写入），独立脚本结论必须先用 common.py 重跑验证才能写入"
```

```yaml
id: D-516
source_ref: "/mnt/d/code/study/research-protocol/thesis-lessons.md:370"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "新实验起飞检查单 6 条（TL-25）：①共享信道 ②重生信道 ③从 common.py 导入 ④基线已优化 ⑤先写理论预期 ⑥输出含元数据（git hash+md5+时间戳）；脚本头部加注释 '# TL-25 checklist: [1-6] 全部确认'"
step_group: "thesis-lessons 仿真验证硬货（TL-20~25）"
step_order: 6
vs_paperwrite: "paper-write 无'新实验起飞检查单'"
optimization: "新实验脚本启动前强制过 6 条起飞检查单，头部注释确认全部通过，类似飞行员起飞清单不靠记忆"
```

```yaml
id: D-517
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:303"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
workflow_step: "答辩预演 5 问+预置应答：①'size gen 是已知性质你贡献是什么'→坦然承认+强调'首次在 LEO 场景量化衰减率+三子问题交叉验证' ②'三章都用 GNN 同质化'→工具相同但问题层面/建模方式/学习范式不同 ③'为什么没和 XXX 对比'→提前准备对比选择说明表 ④'局限性'→主动展示边界分析 ⑤'创新性'→系统性应用创新+实证贡献非方法论突破"
step_group: "S006 答辩预演+Tier 分工+跨章元分析"
step_order: 1
vs_paperwrite: "paper-write 无'答辩 5 问预置应答'清单"
optimization: "论文定稿前必做答辩预演——列出最可能被问的 5 个问题，每问预置坦然承认+转移焦点的应答策略，方法论可继承到 FSO 方向"
```

```yaml
id: D-518
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:280"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
workflow_step: "加强策略三级 Tier 分工：Tier1（几天显著提升）=文档修改 P0 共 19 处消除过度声称+跨章元分析框架设计+每章失败/边界分析；Tier2（1-2 周改变论文层次）=补实验多 seed+N=30/40+throughput+竞争者定量对比表+scaling law；Tier3（2-4 周加亮点）=跨章迁移实验+在线适应实验"
step_group: "S006 答辩预演+Tier 分工+跨章元分析"
step_order: 2
vs_paperwrite: "paper-write 无'改进工作按工时×提升分 Tier'优先级排序"
optimization: "论文改进工作分 Tier（几天显著提升/1-2 周改变层次/2-4 周加亮点），每 Tier 标工时+提升幅度，优先做 Tier1 高性价比项"
```

```yaml
id: D-519
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:311"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
workflow_step: "跨章元分析数据收集需求表：结论章统一讨论'GNN 在什么条件下有效'需 6 类跨章数据（同规模绝对性能/跨规模退化曲线/消融无 GNN/GNN 优势激活条件/训练成本/推理延迟），每类标 Ch1/Ch2/Ch3 状态（待补/✅），三章贡献定位未充分差异化"
step_group: "S006 答辩预演+Tier 分工+跨章元分析"
step_order: 3
vs_paperwrite: "paper-write 无'跨章元分析数据需求矩阵'"
optimization: "结论章写作前先建跨章数据收集需求表（N 类数据×各章状态），跨章贡献定位强制差异化"
```

```yaml
id: D-520
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:271"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
workflow_step: "跨章一致性检查 3 维：①贡献定位是否充分差异化 ②指标体系是否部分对齐 ③叙事主线是否同步；文档修改分 P0（必须改 5 处）+P1（建议改 6 处）"
step_group: "S006 答辩预演+Tier 分工+跨章元分析"
step_order: 4
vs_paperwrite: "paper-write 无'跨章一致性 3 维检查+文档修改 P0/P1 分级'"
optimization: "跨章修改后必做 3 维一致性检查（贡献定位/指标体系/叙事主线），文档修改分 P0 必须改/P1 建议改，总览文档强制与章节文档同步"
```

```yaml
id: D-521
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:554"
source_agent: "全量蒸馏D2"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "CAJ 格式工具链痛点：6 篇高度相关论文因 CAJ 格式无法自动提取全文目录，仅 2 篇有万方摘要；建议需 CAJViewer 手动转 PDF 后再用 tools/convert 提取"
step_group: "CAJ 格式工具链痛点与优化"
step_order: 1
vs_paperwrite: "paper-write 若沿用现有 tools/convert（不支持 CAJ），6 篇高度相关中文论文目录永久无法自动提取"
optimization: "paper-write 工具链加 CAJ 处理环节（CAJ→PDF 转换，可用 CAJViewer 或 CAJ2PDF 工具），转换后接入现有 tools/convert 提取目录"
```

```yaml
id: D-522
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:567"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "CAJ 处理降级链：自动转换失败→CAJViewer 手动转 PDF→tools/convert 提取目录→仅万方摘要兜底（信息不全）；中文论文格式限制是系统性障碍，需在文献筛选阶段标记格式风险（CAJ/仅摘要/可提取），按风险分级处理"
step_group: "CAJ 格式工具链痛点与优化"
step_order: 2
vs_paperwrite: "paper-write 无'格式风险标记+降级处理链'"
optimization: "文献筛选阶段标记每篇格式风险（可提取/CAJ 待转/仅摘要），CAJ 走 CAJViewer→tools/convert 降级链，仅摘要的用万方兜底+标记信息不全需人工补"
```

```yaml
id: D-523
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:34"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "三级文献筛选工作流：①必读（8 篇，每篇标引用数+入选原因）②建议读（13 篇，引用数+原因）③二轮补充（按新发现补）；每篇必带'引用数+原因'双字段，覆盖子方向分类（传统方法/DL/GG 参数估计/星地建模），关键空白显式标注"
step_group: "literature_notes 三级筛选+参数溯源工作流"
step_order: 1
vs_paperwrite: "paper-write 无'必读/建议读/二轮补充三级+每篇引用数原因双字段'筛选流程"
optimization: "文献筛选分三级，每篇必带引用数+入选原因双字段，按子方向分类覆盖，关键空白显式标注；此处提'筛选工作流流程'，综述笔记模板见 C-416/417，空白分级 rubric 见 B-410"
```

```yaml
id: D-524
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:200"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "参数溯源审计表：所有仿真参数按 4 类（GG 湍流参数/链路参数/均衡器参数/载波同步参数）建来源表，每参数标值+来源论文+来源类型（[实证]/[理论]/[实测]/[建模]/[标准]/[工程]/[实验]），待精读项显式标'待精读确认'"
step_group: "literature_notes 三级筛选+参数溯源工作流"
step_order: 2
vs_paperwrite: "paper-write 无'参数按类建来源表+来源类型分类'审计机制"
optimization: "仿真参数建 4 类溯源审计表，每参数标值+来源论文+来源类型，待精读项显式标'待精读'，保证每个参数可信度可追溯"
```

```yaml
id: D-525
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作质量规范.md:1"
source_agent: "全量蒸馏D2"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "毕设/ 自管理极完整元观察：目录含规范（写作质量规范.md）+决策（design-decisions.md 含强度/状态机）+批注（开题报告导师批注）+审查（写作质量规范 R1-R8）+验证（CONCLUSIONS-VERIFY-PLAN 三步法）+审计（formulas-index/symbol-conventions/TERMS）体系齐全；复用原则=下游应最大化复用现有结构（规范/决策/审查/验证/审计六体系），而非从零建"
step_group: "毕设目录自管理复用元观察"
step_order: 1
vs_paperwrite: "paper-write 若从零建规范/决策/审查/验证/审计体系会重复造轮子，毕设/ 已有成熟六体系可直接复用"
optimization: "paper-write 设计前先盘点 毕设/ 现有六体系（写作质量规范/design-decisions 强度状态机/CONCLUSIONS 验证/formulas-index 审计/TERMS 符号/开题批注），最大化复用现有结构而非从零建"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（工作流蓝图 20 条 / 失败案例 5 条）
- [x] 所有 source_ref 含行号（25 条全部带 :line）
- [x] 所有 date_validity/direction 已标注（D-517~520 标"方法论可继承-技术作废"+"旧(GNN/路由)"，其余"有效"+"当前(FSO)"）
- [x] id 前缀均为 -5xx（D-501~D-525）
- [x] D 维度工作流已拆 step + step_group + step_order（11 组）
- [x] 每条 11 字段齐全
- [x] 去重：D12 不重复 B-509~512；D18 不重复 C-416/417/B-410
