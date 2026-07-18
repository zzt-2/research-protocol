# Decisions — CCISP 2026 论文内容补强

## D001: 正文词数下限调整为 3500

> status: active
> date: 2026-07-14
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-07-14 + 调研: R001（当前正文 2,219 词）

### 决策

将本专题的正文验收下限由 `CCE-CC-001` 提议的 2,500–2,900 词调整为至少 3,500 词；公式可作为候选补强手段，但每个新增公式必须通过 benchmark、argument、evidence 三门，并说明其对论证的实际职责。

### 理由

用户明确指出低于 3,500 词无法满足实际页数需要。当前正文为 2,219 词，因此后续合同必须规划至少约 1,281 词的净增量，而不能沿用原合同约 300–600 词的预算。

### 排除的替代方案

- 维持 2,500–2,900 词：不能满足用户明确的页数目标，否决。
- 仅靠放大图、增加参考文献或调整浮动体满足页数：违反原始目标中的“真实内容”约束，否决。
- 无代码或文献对应关系地增加公式：属于不可验证 filler，否决。
- 仅靠公式数量补足全部缺口：尚无 benchmark 与论证职责支持，不作为默认路线。

### 影响范围

- `CCE-CC-001` 保持 NOT APPROVED，不再作为可批准版本；需形成 `CCE-CC-002`。
- 重算 System Model、Method、Results 的内容预算和公式职责。
- 更新本专题 `topic-index.md`、S001 和后续研究记录。
- 不改变“批准前禁止 WRITE、不运行新仿真、不修改数据/JSON/算法”的不变量。

### 来源

用户纠正 / S001

## D003: CCE-CC-002 Batch A 因 switching 口径失败而暂停

> status: superseded
> date: 2026-07-14
> 取代：无
> 被取代：D004
> 依据：调研: R003 + 验证: V002

### 决策

`CCE-CC-002` 在 Batch A 停止，不进入正文扩写；在统一 switching 的 information-bit/throughput 比较口径或另行重签定位合同前，禁止使用当前 Fig.3 比值、26/29 或 1.9 dB 构造 switching 性能贡献。

### 核心失败机制

A4 fixed 结果将 NDA 的 1024 个信息位错误与 DA/switching 仅来自 768 个数据位的错误放在同一 1024 分母下，等效把 256 个 pilot 位置当成零错误信息位。该比值可复现但不是公平的标准 BER；现有汇总 JSON 又缺少离线统一重算所需的逐块信息。

### 否决了什么

- 否决在不重评的情况下把 Fig.3 称为 BER reduction 或 switching gain。
- 否决把 NDA-vs-DA 的约 1.9 dB 归给 switching。
- 否决无持久证据的 26/29。
- 否决用精确定义非标准 error-count ratio 的方式绕过公平性门。

### 可复用部分

- CCISP 官方 5–10 页和 double-blind 声明已核验。
- 四组真实引用元数据和逐句引用映射可复用。
- 8 组公式及实际两层 selector 信息流已通过静态代码审计。
- NDA-vs-DA 工作区数字和 crossover 观察可在新定位中复用，但不能代替 switching 性能验证。

### 具体数据

- NDA：1024 information bits/block。
- DA：768 decoded data bits/block；`da_full` 仍除以 1024。
- switching：选 DA 时沿用 768-data-bit error count，再除以 1024。
- 26/29：无持久字段。
- 1.9 dB：NDA-vs-DA strong-uplink 工作区结果，不是 switching。

### 影响范围

- 当前 phase 保持 WRITE / Batch A，但状态为暂停。
- 论文 `.tex`、BibTeX 和 `毕设/CONCLUSIONS.md` 暂不修改。
- 若授权统一口径重评，需先做 scope change；若不授权，需新 change contract 重定位论文。

### 来源

S001 / R003 / V002

## D004: 恢复历史最终 data-BER 口径并解除 WRITE 暂停

> status: active
> date: 2026-07-14
> 取代：D003
> 被取代：无
> 依据：验证: V003 + 调研: `.sessions/2026-07-09-thesis-writing/S007-switch-framing-caliber-audit.md` / `R008-switch-narrative-upgrade.md` + 用户原话: voice.md 2026-07-14

### 决策

撤销 D003 对 `CCE-CC-002` 的暂停。估计器选对率继续采用历史 D005 冻结的标准 data-BER 口径：NDA 为 `ne_n/1024`，DA 为 `ne_d/768`；现有 A4 fixed JSON 可确定性重算 26/29，不需要新仿真。WRITE 恢复，仍须保留 1.9 dB 归属 NDA-vs-DA、Fig.3 不称 equal-BER SNR gain、crossover 与固定 13 dB 阈值分离等独立事实修正。

### 理由

D003/V002/T009 只读取了早期 H005 和 A4 脚本的 full/net 口径，漏读了后续 D005/D006、S007、R008 及写作专题不变量 10。历史最终裁定已明确：`ne_d/1024` 会将未解码 pilot 位稀释为零错误，只适用于特定 net/full 对照；判断 DA/NDA 哪个估计器的标准 BER 更低时使用各自真实解码信息位分母。A4 fixed JSON 已持久化 `nda_ber_mean`、`da_ber_mean_data`、`da_ber_mean_full` 和 `switch_ber_mean`，无需旧临时脚本即可复算 26/29。

### 排除的替代方案

- 授权最小统一口径重评：既有 JSON 已足够复算，且 D006 明确冻结“不需回 Step 4a 跑新实验”，否决。
- 继续沿用 D003：与上游 active D005/D006 和 topic-index 不变量 10 冲突，否决。
- 删除 D003/V002：破坏误判血缘和教训追踪，否决；保留并标记被取代。
- 将 1.9 dB 重新归给 switching：历史口径纠正不改变该数字属于 NDA-vs-DA 的事实，否决。

### 影响范围

- `CCE-CC-002` 恢复 WRITE，无需扩大到新仿真。
- T009/R003/V002 的 Batch A 总体 FAIL 被 V003/D004 取代；官方约束、引用、公式门继续有效。
- 26/29 可按 data-BER 口径使用；Fig.3、1.9 dB、crossover 和 13 dB 阈值仍按各自已核验定义写作。

### 来源

用户纠正 / S001 / V003 / 上游 D005-D006

## D002: 外部论文只呈现有利且可证实的论证

> status: active
> date: 2026-07-14
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-07-14 + 调研: R001/R002 + 验证: V001

### 决策

内部继续完整记录冲突、证据债务和停止条件；对外论文只呈现有利且可证实的机制、比较和结果。无法闭合的声称直接删除或收窄，不把内部 `BLOCKED/GAP/EXCLUDED`、失败路线、弱场景说明、证据债务或自我否定措辞写进论文，也不增加 limitations/future-work 段削弱说服力。

### 理由

论文目的为说服审稿人，内部审计语言不承担外部论证职责。把“证据不足”“经验启发式”“并非最优”等内部判断原样写入正文，会主动降低贡献强度；但保留错误或扩大无证声称同样会在审稿时损害可信度。因此采用“内部严格、外部积极、声称收窄而不自曝债务”的分层呈现。

### 排除的替代方案

- 把内部风险表和证据债务翻译成 limitations：主动削弱论文，否决。
- 为显得严谨而逐项写“不是理论最优、不是无偏、缺少证据”：这些属于内部门控，不写入论文。
- 保留宽泛强声称，同时隐藏与其矛盾的事实：会构成误导并增加审稿风险，否决；正确做法是把声称收窄到已有证据支持的条件。
- 删除完整结果图中的合法数据：不改数据、不裁掉既有 sweep；只控制正文的代表锚点和解释重点。

### 影响范围

- `CCE-CC-002` 增加“外部呈现门”：内部术语与不利审计信息不得进入正文。
- CV 曲线、1.10 margin、blind-h proxy 和 13 dB 在内部按经验固定量审计；论文用 `pre-calibrated/fixed decision parameters` 等中性积极措辞，不声称理论最优。
- 1.9 dB、BER-ratio、26/29 等事实修正以“重写/删除/分离贡献”完成，不在论文中叙述曾经存在的错误。
- 不改变三门、事实一致性和“不编造”的不变量。

### 来源

用户纠正 / S001
## D005: 三项实现真实性冲突闭合前暂停投稿级交付

> status: active
> date: 2026-07-14
> 取代：无
> 被取代：无
> 依据：验证: V004 + critic: S001 独立专业性审计 + 上游 `.sessions/2026-07-09-thesis-writing/S010-logic-chain-controlled-attribution.md` / `S017-fig1-fig2-structural-redesign.md`

### 决策

保留已通过独立验证的五条短图题修改，但在三项实现真实性冲突闭合前，暂停将当前稿件判为投稿级完成：NDA 的 genie-assisted 相位模糊消解未披露；26/29 与 Fig. 5 的 BER-ratio 数字来自不同分母口径；湍流 selector 每 256 样本重启相位 realization，而正文声称跨 DSP 窗连续。

### 理由

三项均由当前源码、生成脚本和历史记录交叉确认，分别影响信息可用性、指标含义和模型/实现一致性。它们属于 G4 事实冲突，不能通过标题润色或只报喜政策掩盖。D004 对 26/29 的 data-BER 判定仍然有效，但不等于替 Fig. 5 的 full-block 归一化或其余两项真实性问题背书。

### 排除的替代方案

- 仅改标题后继续宣称投稿就绪：标题不能修复指标和实现冲突，否决。
- 把三项内部审计原样写成 limitations：违反 D002，否决；应先决定删除、收窄还是另行修复实验链。
- 未经用户授权直接重跑仿真或修改算法：超出 CCE-CC-002 和本专题明确不含，否决。
- 用 D004 把 26/29 与 2.3/2.0/1.3 dB 视为同一 data-BER 口径：历史 D005/D006 和 A4 fixed 脚本明确否定，否决。

### 影响范围

- `projects/simulation/paper/ccisp2026/` 暂不进入 DELIVER/投稿就绪结论。
- 标题层级可继续作为 L1 独立批次讨论；不得借此绕过三项 G4。
- 后续需要用户选择：仅按现有实现收窄正文/删除受影响声称，或另开仿真修复范围。

### 来源

S001 / V004
## D006: 采用现有实现对齐路线修复非引用项

> status: active（Fig.5 分名 full-block-normalized error ratio 部分已被 D011 取代；ambiguity-resolved 披露、相位连续性收窄、术语统一三项仍 active）
> date: 2026-07-14
> 取代：无
> 被取代：D011（仅 Fig.5 分名 full-block-normalized error ratio 部分）
> 依据：用户原话: voice.md 2026-07-14 + 验证: V005

### 决策

参考文献补充由其他工作流处理；本专题在不运行新仿真、不修改算法/数据/JSON/图资产的边界内，将论文正文对齐现有实现：披露 transmitted-bit-assisted ambiguity-resolved evaluation，分离 26/29 data-BER 与 Fig.5 full-block-normalized error ratio，收窄相位连续性到单个 256-sample window，并统一标题、符号、oracle 和 processing-window 术语。

> **2026-07-15 更新（D011）**：其中"Fig.5 分名 full-block-normalized error ratio 即已闭合"的部分已被 D011 取代——R004 证明只分名不够，分支 population 必须统一到 common-768（768-bit 冻结数据位总体）。Fig.5 改用 common-data-payload BER 口径 + 全 9 点 + 避险递减叙事。本决策其余三项不变。

### 理由

用户明确要求参考文献先不管、其余问题修复。现有三项 G4 中，正文真实性可以通过准确限定闭合；改仿真或图资产分别超出当前合同和用户先前的跨对话职责边界。

### 排除的替代方案

- 本轮新增参考文献：用户明确排除。
- 未经授权重跑仿真或实现在线相位模糊消解：超出范围，排除。
- 为保持旧 Fig.5 轴名而继续把 full-block 指标称为 BER：与实现真实性冲突，排除。
- 由论文主控直接修改 Fig.5 图资产：违反图线程职责边界，排除。

### 影响范围

- 修改 `projects/simulation/paper/ccisp2026/main.tex` 与 6 个 section 源，fresh build 生成 `main.pdf/main.log`。
- Fig.5 图内纵轴旧标签仍由图线程修复；在新资产返回前整体验证保持 PARTIAL。
- Skill 是否改造另行讨论，不由本决策授权实施。

### 来源

用户指令 / S001 / V005

## D007: 实施双 Skill 实现真实性三联卡门禁

> status: active
> date: 2026-07-14
> 取代：无
> 被取代：无
> 依据：用户批准 + Skill RED 审计 + 验证: V006

### 决策

在 `paper-writing` 与 `sim-preflight` 中同步加入实现真实性三联卡：`information_access`、`metric_signature`、`state_lifecycle`。论文写作/投稿前必须提供 `paper line -> caller -> callee -> metric/state` 证据链；任一字段缺失、调用链未追到底层实现，或论文声称强于实现，均标记 `BLOCKED`。

固定三类阻断锚点：blind 声称下读取发送端真值、不同分母/误差总体共用同一指标名、逐窗重置却声称跨窗连续。自动脚本只验证结构契约未回退；行为有效性必须由独立上下文压力测试验证，不得以关键词检查代替。

### 理由

V004 暴露的三项冲突并非缺少宽泛原则，而是诊断/数字搬运模板没有强制槽位，且此前审查未追 caller/callee 与外层循环。双 Skill 同步改造可同时堵住上游仿真数字转移和下游论文验证的漏口；单改论文 Skill 仍会保留上游污染，另建第三个 Skill 则会重复职责。

### 排除的替代方案

- 仅增加提醒文字：不能形成缺项即阻断的门禁，否决。
- 只改 `paper-writing`：不能阻止错误口径从仿真写作卡进入论文，否决。
- 新建独立 truth-audit Skill：增加触发和职责重叠，当前没有必要，否决。
- 把 token-presence 脚本宣称为行为测试：独立 reviewer 已证明可被 token 附录绕过，否决。

### 影响范围

- 修改全局 `paper-writing` 的 diagnosis/communication/verification 参考规范并增加结构契约夹具。
- 修改项目 `sim-preflight` 的 C4、场景 C 数字转移卡、技术规则与 changelog，并增加结构契约夹具。
- 不修改论文、参考文献、仿真、数据、图资产。

### 来源

用户批准 / Skill RED 审计 / V006

## D008: 将 26/29 降为结果部分的聚合对齐辅助证据

> status: superseded
> date: 2026-07-15
> 取代：无
> 被取代：D018
> 依据：验证: V007 + 用户原话: voice.md 2026-07-15

### 决策

保留 `26/29`，但只在 Results 中出现一次，并准确命名为 aggregate selected-output alignment；不写成 `26/26`，不称 selector accuracy、correct selection 或 recovery of the better estimator，也不在 Abstract、Introduction 或 Conclusion 中反复放大。结果定义须说明该对齐由聚合 selected-output error ratio 与固定分支结果的接近关系推断，主论证仍由 DA/NDA 互补工作区和规范化后的 selected-output 性能证据承担。

### 理由

V007 已确认 `26/29` 不是直接保存的逐点 selector branch-decision accuracy，而是由聚合曲线接近度反推。完全删除会削弱“互补工作区到选择器效果”的中间证据；继续称准确率或恢复较优估计器则强于现有数据。降级为一次聚合对齐辅助证据，可保留有利数字，同时使声称与证据形态一致。无 rebuttal 的会议审稿中，避免需要额外解释才能成立的 headline 更有利于降低静默拒稿风险。

### 排除的替代方案

- 写成 `26/26` 并不提另外三个预设评价点：三点没有独立、事先冻结的排除标准，属于选择性删样本，排除。
- 在 Abstract/Introduction/Conclusion 中继续称 `26/29` 为选择准确率或 estimator recovery：现有 JSON 未保存直接分支决策，声称强于证据，排除。
- 完全删除该计数：会损失一项有利的辅助诊断；在准确降级命名可成立时不采用。
- 通过新仿真补直接分支统计：超出当前“不运行新仿真”的范围，不由本决策授权。

### 影响范围

- 后续最小真实性改稿合同中的 `26/29` 项按本决策执行。
- 影响 `projects/simulation/paper/ccisp2026/sections/results.tex` 及 Abstract/Introduction/Conclusion 中现有相关表述；具体 WRITE 仍须与其余 V007 修复项形成获批批次。
- 不改变算法、数据、JSON、图资产或参考文献。

### 来源

用户拍板 / S001 / V007

## D009: 采用双坐标解释并以总能量等效优势作为主结果

> status: superseded
> date: 2026-07-15
> 取代：无
> 被取代：D018
> 依据：验证: V007 + 30-seed JSON `workregion_grand_mean_db` + 用户批准

### 决策

将 1.3/1.2/1.9 dB 准确表述为 strong downlink、moderate uplink、strong uplink 的 data-symbol-SNR 差值；首次出现时说明加入 DA 的 (10\log_{10}(4/3)=1.249\) dB 导频能量项后，对应 total-energy-equivalent advantages 为 2.5/2.4/3.1 dB。Abstract 使用最高 3.1 dB 作为 headline，并同时注明其由 1.9 dB data-symbol-SNR gap 与约 1.25 dB pilot-energy term 构成；后文统一使用 2.5/2.4/3.1 dB 总能量坐标。

### 理由

V007 确认当前稿将两种坐标的语义写反。现有 30-seed 结果直接支持总能量等效值 2.509/2.443/3.101 dB，减去 1.249 dB 后得到约 1.260/1.194/1.852 dB 的 data-symbol-SNR 差值。双坐标只解释一次，既保留更强的总能量结果，又清楚交代增益构成，避免把导频能量记账误写为算法本身的全部优势。

### 排除的替代方案

- 继续将 1.3/1.2/1.9 dB 称为已计入 pilot offset 的 total-energy 结果：与计算方向相反，排除。
- 只报 1.3/1.2/1.9 dB：合法但舍弃已有总能量比较优势，外部说服力较弱，排除。
- 只报 2.5/2.4/3.1 dB 而不解释 1.249 dB 导频项：容易把能量记账误解为纯算法增益，排除。
- 使用 `naive`、`corrected error` 等内部纠错措辞：违反 D002 的外部呈现边界，排除。

### 影响范围

- 影响 Abstract、Introduction、Results 和 Conclusion 中相关 SNR 数字与坐标说明。
- 不改变仿真、数据、JSON、算法、图资产或参考文献。
- 具体 WRITE 与 D008、Fig.5/calibration 项合并成最小真实性修复批次后执行。

### 来源

用户批准 / S001 / V007

## D010: 批准 CCE-CC-003A 独立真实性修复批次

> status: active
> date: 2026-07-15
> 取代：无
> 被取代：无
> 依据：验证: V007 + 决策: D008/D009 + 用户批准

### 决策

批准 `CCE-CC-003A` 进入 WRITE：在不等待 Fig.5 专项审计的前提下，先实施与其独立的 SNR 双坐标和 calibration 来源/冻结边界修复；同时按 D008 从 Abstract、Introduction、Conclusion 移除 `26/29` recovery headline，并从这些门面段移除 Fig.5 的 2.3/2.0/1.3 dB。Results 中 26/29 的精确定义、Fig.5 公式/数字/解释、caption 和图资产保持不动，等待 T010/R004。

### 理由

D009 的 fixed-estimator SNR 坐标与 calibration 来源均有独立代码/数据证据，不依赖 Fig.5 指标裁定。先修复这些项可消除当前确定的错误语义和模糊来源，同时避免在 R004 回传前提前决定 Fig.5 的最终命运。门面段移除尚待专项审计的 selector 指标，可防止当前弱证据继续承担 headline。

### 排除的替代方案

- 等 R004 后再处理所有项：会不必要地阻塞已独立拍板的 D009 与 calibration 修复，排除。
- 本批次同时修改 Results 中 26/29/Fig.5：精确定义仍在 T010 审计，超出已锁边界，排除。
- 继续使用 `pre-calibrated` 而不写来源：无法说明参数从何而来，排除。
- 声称 independent holdout、optimized threshold 或 sensitivity robustness：现有证据不支持，排除。

### 影响范围

- 修改 `sections/abstract.tex`、`introduction.tex`、`method.tex`、`results.tex`、`conclusion.tex`。
- 不修改参考文献、Fig.5 资产、其他图资产、仿真、代码、数据或 JSON。
- 本批次验证只能判局部 PASS/PARTIAL；整稿仍等待 R004。

### 来源

用户批准 / S001

## D011: Fig.5 改用 common-768 口径，全 9 点保留，避险增益随湍流递减叙事

> status: superseded
> date: 2026-07-15
> 取代：D006 中"Fig.5 分名 full-block-normalized error ratio 即已闭合"的部分（R004 证明分名不够，分母 population 必须统一到 768）；D006 的其余三项（ambiguity-resolved evaluation 披露、相位连续性收窄、术语统一）仍 active 不动
> 被取代：D012
> 依据：调研: R004（端到端口径审计，病态退化证明机械白送最多 1.249 dB）+ 验证: R005（30seed × 9 点 common-768 验证，全 9 点 CI95 下界为正，`_a4_switch_common768_30seed.json`）+ 用户原话: voice.md 2026-07-15（拍板方案 B）
> 触发原话: 用户拍板方案 B（详见 voice.md 2026-07-15）

### 决策

Fig.5 采用 **common-data-payload BER** 口径（common-768）：NDA 和 selector 输出都在同一冻结的 768-bit 数据位总体上评 BER——即每 256 样本窗中 192 个非 pilot symbol 的 4×192 = 768 bit，与 DA 的评分位一致，NDA 亦裁到这 768 位上评。全 9 点（weak/moderate/strong × {5,10,15} dB）保留不删不藏。正文叙事为"selector 避险增益随湍流增强递减，strong 区收窄至接近零"。

common-768 增益定稿数字（30seed，dB，CI95 下界全为正）：weak {5:+0.698 / 10:+1.256 / 15:+0.542}；moderate {5:+0.470 / 10:+0.867 / 15:+0.472}；strong {5:+0.074 / 10:+0.138 / 15:+0.101}。weak/moderate 真实避险增益约 0.5–1.3 dB；strong 三点绝对值接近零但统计显著（CI 下界 +0.053~+0.098）。

### 理由

R004 做了端到端调用链审计（paper claim → caller → callee → metric/state），证明 Fig.5 原 mixed 口径的 `switch_ber_mean` 选 DA 窗时累计 768-bit population 的 `ne_da`、选 NDA 窗时累计 1024-bit population 的 `ne_nda`，两边都除 1024 但分母只统一标度不统一统计总体——实际是 branch-dependent decoded-error-count ratio，不是公平 BER，并给出病态退化证明：即使 selector 毫无本事、全选 DA，也会机械白送 10·log10(4/3)=1.249 dB。R005 的 30seed 验证坐实该退化（strong@5 mixed +1.298 dB ≈ 病态地板，扣到 common-768 只剩 +0.074 dB）。

公平 common-768 口径下全 9 点 CI95 下界为正，证明 selector 不是废物（weak/moderate 低 SNR 区 NDA 升幂崩溃，selector 切 DA 避险有真实 +0.5–1.3 dB 增益），也不是性能明星（strong 区接近零，反映 deep fade 下两估计器均受限）。用户选方案 B 的理由：不藏数据守诚实底线 + 完整递减曲线物理自洽 + 审稿人看到完整 9 点比藏 strong 更觉严谨；递减叙事把 strong 接近零从"不利数字"转化为"避险增益随湍流递减"这一完整物理叙事的一部分，而非被动暴露缺陷。

### 排除的替代方案

- 删 Fig.5（方案 C）：会丢掉 weak/moderate 低 SNR 区 +0.5–1.3 dB 的真实避险增益证据——这是 selector 唯一能正当声称的性能贡献，删了就真没 selector 性能证据了，否决。
- 只画 6 点、藏 strong（方案 A）：在已实测 strong 接近零的情况下选择性删除三个点，属 cherry-pick 嫌疑，审稿人若知全 9 点会质疑为何藏，否决。
- 维持 mixed 口径：R004 已证明病态退化（机械白送最多 1.249 dB），指标不诚实，否决。
- 强行把 strong 区写成"selector 有效"：与数据矛盾（绝对值接近零），违反 D002 声称收窄原则，否决。

### 影响范围

- 改 `projects/simulation/paper/ccisp2026/sections/results.tex` §IV-C（L36–53）：公式分母 1024→768、符号 G_FB → G_C768、加 common-data-payload 定义句、3 个正文锚点换成 common-768 数字并改递减叙事、caption 描述句与 Fig.5 caption 改名。
- 改 `projects/simulation/figures/plot_fig3_gain.py`：数据源从 `_a4_switch_30seed_fixed.json` 的 `switch_vs_nda_db_mean`（mixed）→ `_a4_switch_common768_30seed.json` 的 common-768 gain；纵轴 label 改 common-data-payload BER reduction；重新生成 `figures/ccisp_fig3_gain.pdf`。
- **不动**：算法/判据/参数/§IV-B（NDA-vs-DA 1.9/3.1 dB）/§IV-A/其他 section/参考文献/26/29 定义（26/29 仍用 branch-specific data-BER 分母，与 G_C768 不同口径，已在正文区分）。
- D006 中 Fig.5 分名部分由本决策取代；D006 顶注追加指向 D011。V008 的"Fig.5 error population 与轴名未闭合"未决项随之闭合。

### 来源

用户拍板（方案 B）/ R004 / R005 / S001

## D012: 冻结 Fig.5 权威证据链并拆分数据、图、文执行

> status: superseded
> date: 2026-07-15
> 取代：D011
> 被取代：D013
> 依据：调研: R004 + 验证输入: R005/`_a4_switch_common768_30seed.json` + critic: S001 对 D011/当前工作区的独立复核 + 用户原话: voice.md 2026-07-15
> 触发原话: “我刚刚用这个跑了一下（另一个对话给的方案）。但它感觉考虑的十分不周到。还得看你的？你整理一下吧”

### 决策

保留 D011 中“common-768 公平总体、全 9 点、不隐藏 strong”的方向，但在继续改稿前增加权威数据门，并把执行拆成数据证据闭环、Fig.5 图资产、论文文字三个独立任务。论文与图的唯一外部统计量冻结为逐 seed 配对对数 BER 比的均值及 95% t 置信区间：

\[
G_{\mathcal C}^{(s)}=10\log_{10}\!\left(P_{b,\mathcal C,\mathrm{NDA}}^{(s)}/P_{b,\mathcal C,\mathrm{SW}}^{(s)}\right),\qquad
\bar G_{\mathcal C}=30^{-1}\sum_{s=1}^{30}G_{\mathcal C}^{(s)}.
\]

其中 \(\mathcal C\) 是每个 256-symbol DSP window 中共同的 192 个非 pilot symbol，即 768 bit。`ratio of pooled counts` 只可作内部验算，不得与上述点估计或 CI 混作一个统计对象。

strong 三点应表述为 **0.08--0.14 dB 的小幅正改善**或“benefit narrows under strong turbulence”，不得写“收窄至零/趋近零”。当前数据只支持状态依赖现象，不足以把 deep fade 写成已验证的因果机制。

### 理由

当前 D011 和半成品实现存在四个会让上下游分叉的问题：一是正文表中点估计使用逐 seed dB gain 均值，而绘图脚本读取 pooled-count ratio，中心值最多相差约 0.006 dB；二是 Fig.5 尚未画与点估计同口径的 95% CI；三是 D011 把三个显著为正的 strong 点写成“趋近零”，并加入未由本探针单独证明的 deep-fade 因果；四是正文仍把 26/29 称为 recovery，违反 D008。先冻结权威 JSON 契约，再让图、文对话只消费同一摘要字段，可以防止再次出现公式、图和正文各用一套数字。

### 排除的替代方案

- 直接接受当前 D011 和半成品：统计中心、CI、因果和 26/29 语义仍不一致，排除。
- 只修绘图脚本、不补证据溯源：无法证明最终图对应哪版代码/参数，排除。
- 只改 Results、不改 Abstract/Introduction/Conclusion：论文标题以 selector 为核心，但门面段仍没有规范 selector 性能结果，论证闭环偏弱，排除。
- 继续把数据、图、文和提交塞进一个对话：上游契约未锁定时下游会自行解释字段，已实际导致口径分叉，排除。
- 隐藏 strong 三点或删 Fig.5：分别有事后筛选风险或会丢失 selector 唯一的直接输出性能图，维持 D011 的否决。

### 影响范围

- 数据闭环：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py/.json`，仅补指标持久化、同总体 oracle、自检和 provenance，不改算法、门限、参数或场景。
- 图资产：`projects/simulation/figures/plot_fig3_gain.py` 与 `ccisp_fig3_gain.pdf/.png`。
- 论文文字：`abstract.tex`、`introduction.tex`、`results.tex`、`conclusion.tex`；`system_model.tex`、`method.tex`、标题、Fig.1/Fig.2 和参考文献不动。
- Results 同批修复 D008：26/29 只称 aggregate selected-output alignment，不称 recovery/accuracy/correct selection。
- 最终提交在权威 JSON、图、文、fresh build、数值审计和独立验证全部通过后由主控统一完成；各执行对话不得自行提交。

### 来源

S001 / 用户纠正 / R004 / R005

## D013: Fig.5 扩展为 5--25 dB 双数间隔网格并统一定量图 SNR 轴

> status: superseded
> date: 2026-07-15
> 取代：D012 中 Fig.5 仅覆盖 5/10/15 dB 九点的范围合同；D012 的 common-768、paired-seed mean+t-CI、数据/图/文分离执行和 26/29 降级约束继续继承
> 被取代：D018（网格与统计口径继续继承，旧参数数据及其 hash 失效）
> 依据：用户原话: voice.md 2026-07-15 + 同领域图轴对照: Du 2025/Johst 2024/Paillier 2020/Du 2021/Martins 2021 + 候选验证数据: `_a4_switch_common768_30seed_snr5_25_step2.json`
> 触发原话: “那就5-25，然后2db间隔吧？然后，得看看别人的这符号都用的啥，别自己拍脑袋”

### 决策

Fig.5 的 common-768 性能网格扩展为 weak/moderate/strong 三种下行湍流、5--25 dB、2 dB 间隔，即每条曲线 11 点、共 33 个场景点；每点继续使用 30 个 paired seeds 和 400 个 DSP windows。扩展只改变采样网格，不改变 selector 算法、两层判据、13 dB 门限、信道参数、seed 集、窗口数或 common-768 统计总体。

三张定量图的横轴统一采用 `Data-symbol $E_s/N_0$ [dB]`。正文保留 $\bar\gamma=E_s/N_0$ 作为计算简写，不再在图轴使用正文未定义的 $\bar\gamma_d$。Fig.5 纵轴与正文符号闭合为 common-payload BER-ratio reduction $G_{\mathcal C}$（dB）。

外部叙事按扩展数据收窄为：低中 SNR 区提供避险增益；正常工作区内随 selector 回到 NDA，增益趋近 0，且未观察到统计可分辨的惩罚。不得把高 SNR 跨零 CI 写成显著正增益。

### 理由

论文已把 $\gamma_{\mathrm{tot}}\ge15$ dB 定义为正常工作区，而原 5/10/15 dB 网格仅在端点触及该区，且 weak/moderate 的固定估计器交叉点分别为 18.0/16.9 dB。5,7,...,25 dB 网格既以 2 dB 分辨率覆盖交叉过渡，也包含 15--25 dB 的正常工作区，可直接检查 selector 是否无可辨代价地退化到固定 NDA。

候选 990 seed-point 结果中，5/15 dB 六个旧锚点的 mean/CI 与 D012 权威数据严格一致，common-oracle 和分支计数违例为 0；weak 在 23/25 dB 完全选择 NDA，moderate/strong 高 SNR 点的微小正负均值置信区间跨 0。因此扩展增加的是正常工作区安全退化证据，而不是人为放大高 SNR 增益。

同领域原始论文对照显示，SNR 图轴常用 `SNR (dB)`、`$E_s/N_0$ [dB]` 或在正文定义后的 $\gamma$ (dB)；本稿为复基带符号能量口径，不是 OSNR。直接写 $E_s/N_0$ 比继续使用未定义的 $\bar\gamma_d$ 更透明，并与 Paillier 2020 的同类 FSO 载波恢复图轴一致。

### 排除的替代方案

- 维持 5/10/15 dB：不能完整覆盖 16.9/18.0 dB 交叉区，且正常工作区证据过少，排除。
- 仅扩到 15 dB 并用 1 dB 加密：分辨率高但截断 weak/moderate 的关键过渡，排除。
- 5--26 dB 每 1 dB：高端主要增加近零平台，运行和版面成本更高，对主张增量有限，排除。
- 继续用 $\bar\gamma_d$：正文未定义该符号，符号体系不闭合，排除。
- 改用 OSNR：当前仿真量是复基带 $E_s/N_0$，不是 0.1-nm 光学测量带宽下的 OSNR，排除。

### 影响范围

- 数据：将候选 `_a4_switch_common768_30seed_snr5_25_step2.json` 经独立验证后提升为 Fig.5 权威输入；保留 provenance 和旧权威数据的可追溯性。
- 图：`plot_fig3_gain.py`、`ccisp_fig3_gain.pdf/.png`；三张定量图绘图脚本的 SNR 横轴统一为 $E_s/N_0$。
- 文：`system_model.tex`、`method.tex`、`results.tex` 中网格范围、符号定义、代表数字和高 SNR 叙事。
- Fig.2 的 $\hat\gamma_{\mathrm{eff}}<13$ dB 与正文 $\hat\gamma_{\mathrm{eff,dB}}$ 不一致，另交图资产权威源修订；论文主控不直接修改 draw.io/PDF。
- 不改算法、判据、参数、参考文献、Fig.1 语义、§IV-B 固定估计器主结果或 D008 的 26/29 定义。

### 来源

用户拍板 / 同领域图轴专项对照 / 5--25 dB 候选扩展验证

## D014: 以自适应 CPR 方法作为论文身份

> status: active
> date: 2026-07-15
> 取代：无
> 被取代：无
> 依据：调研: R007 + critic: R007 独立复核 + 用户原话: voice.md 2026-07-15

### 决策

论文的方法身份采用 `received-power-aware adaptive CPR scheme/method`；两阶段 received-power-aware selection 是该方法的核心内部控制机制，DA phase--time LS 与 NDA eighth-power recovery 是既有 component branches。不得把控制器或完整方案称为新的 adaptive phase estimator；`two-stage` 若对外使用，必须限定为 two-stage control。

### 理由

当前实现形成原始功率统计、两阶段控制、DA/NDA 分支和统一载波校正输出的完整端到端处理链，本地相近论文允许以 CPR method/scheme 作为复合处理链的贡献主语。该层级回应导师“题目不能落在估计器的选择上，应该是估计算法”，同时不把既有 DA/NDA 公式冒充本文新估计器。

### 排除的替代方案

- 继续以 estimator selector/selection 作为标题和贡献主语：与导师反馈冲突，排除。
- 称 `adaptive phase estimator` 或 `new estimation algorithm`：控制器不直接产生新的相位估计公式，存在过度声称，排除。
- 把 selection 完全降为无关实现细节：它仍是本文方法的核心控制机制，排除。
- 在标题中无定义地使用 `two-stage estimation`：易被理解为两个估计阶段串联，排除。

### 影响范围

- 下一轮 change contract 可据此审计标题、摘要、引言、Method 一级/二级标题、贡献句和结论的贡献主语。
- 本决策不授权修改论文；不改变算法、判据、参数、数据、图或既有 DA/NDA 实现。

### 来源

R007 / 用户确认

## D015: selected-output 实现缺口阻断换名与 Fig.2 局部修路线

> status: superseded
> date: 2026-07-15
> 取代：无
> 被取代：D016
> 依据：调研: R011 + 验证: V010
> 触发原话: 无（技术推导）

### 决策

当前权威实现只在 common-768 错误计数上执行 branch mux，未实现 selected phase 或统一 carrier-corrected complex-sequence mux。因此否决“仅把 selector 换名为 adaptive CPR 并对 Fig.2 做局部文字/避让修复”的路线；D014 作为目标定位保留，但 R009 定位 Batch 与 R010 图合同在真实性路线重新拍板前保持 BLOCKED。

### 核心失败机制

DA/NDA recovery 分别产生复数序列，但权威 caller 丢弃两路 `phi_est`，将两路输出立即解调为错误数；selector 在两路处理完成后才执行，只选择累加哪一路错误数。Fig.2 却画出两路相位估计进入 selector、所选相位再进入 phase compensation 和共同 downstream DSP，语义强于实现。common-768 BER 的后验数值等价还依赖真实 `tx_bits` 消除 NDA 八重模糊，不能升级为可部署在线输出。

### 否决了什么

- 否决不追实现就直接执行 D014 的机械换名。
- 否决 `CCE-FIG2-001` 仅改 dB 符号、挪 edge label 而冻结当前 selected-phase 语义。
- 禁止声称只执行所选分支、存在计算节省、已经物化统一复数输出或可复用 downstream interface。

### 可复用部分

- D014 的方法层级目标仍可用于重新评估；两阶段 `decide()` 判据与信息访问边界真实。
- R009 的 307--338 词精炼 Batch 独立有效，但涉及方法身份/统一输出的句子须等待路线拍板。
- R010 的 dB 域符号、局部碰撞事实、17 条 edge 清单和 final-size QA 可作为后续重做图合同的输入，不能直接执行。

### 具体数据

- `per_block()` 同时调用两路 recovery 后只返回 3 个错误计数整数。
- `phi_est` 两处均由 `_` 丢弃；无 `selected_phi` 或 selected complex output。
- selector 后续操作仅为 `e_s_c768 += ne_d` / `+= ne_n_c768`。
- Fig.2 明示 `theta_da/theta_nda -> selector -> Selected theta -> phase compensation`，与 caller 不一致。

### 影响范围

- `R009/CCE-CC-004 v2` 定位 Batch BLOCKED；纯精炼子集仍可作为后续独立合同。
- `R010/CCE-FIG2-001` 标记 rejected，不得派图线程执行。
- 下一步需用户在“收窄为 branch-decision + post-hoc selected-BER evaluation”与“另开仿真实现真实 selected output”之间选择；前者是否足以满足导师“估计算法”需单独判断。

### 来源

R011 / V010

## D016: 采用 branch-routed adaptive CPR 与 A1+ 参数证据路线

> status: superseded
> date: 2026-07-15
> 取代：D015
> 被取代：D017
> 依据：调研: R008b + 调研: R013 + 验证: V011 + 用户原话: voice.md 2026-07-15

### 决策

论文目标运行架构采用路线 B：两阶段控制器先逐窗决策，只执行被选 DA 或 NDA CPR 分支，并输出统一复数序列。五档 Gamma--Gamma 参数采用强证据 A1+ 路线：下行使用文献锚定的 Family 1；上行按明确几何与大气剖面，经 spherical-wave Rytov 积分和 Al-Habash 公式复算，不采用为满足“上行更强”叙事而指定的 A2/A3 数值。

本决策当前只授权 T016 的候选参数复算与诊断性小切片；未授权修改正式 `params.py`、全量 30-seed 重跑、图文数字回填或论文 WRITE。

### 理由

V011 在旧参数网格上确认路线 B 的 selector 端结果与 A 版 990/990 bit-exact，且真实物化 selected complex output；因此 D015 的实现真实性阻断已有可行修复路径。R008b 同时证明现有五组参数均无可靠来源，A2/A3 又会为了预设叙事拍取超出文献锚点的强度，违反 FR-20/TL-26。A1+ 将“证据强”落实为可复算物理条件，而不是把湍流数值取得更大。

### 排除的替代方案

- 路线 A（双分支全跑后 post-hoc complex mux）：可修复输出接口，但不能支撑真实先选后跑与 branch compute 节省，排除为目标架构；保留为离线评估 runner。
- 路线 C（non-genie 在线 ambiguity resolver）：属于新增算法范围，需 Groundwork/Contract 与新实验，本轮不进入。
- 参数 A2（如 3.5/6.0）和 A3（如 4.0/6.0）：为满足“上行数值必须强于下行”而超出当前文献锚点，排除。
- 直接把 Osborn plane-wave 数值称为精确上行标定：wave model 不一致，排除；只能先复现其环境锚点，再按上行 spherical-wave 公式推导。
- 立即全量重跑：候选参数、selector 冻结边界和方向性尚未小切片检查，可能造成二次重跑，排除。

### 影响范围

- D015 的 BLOCKED 状态由本决策取代；其失败事实仍保留为历史证据。
- D014 的 adaptive CPR 方法身份继续有效，但对外不得称新 phase estimator；NDA 的 transmitted-bit-assisted ambiguity resolution 仍是 post-hoc 评估边界。
- 旧参数下的 990/990 等价性可作代码路径回归证据；74.6% 仅是一个条件下相对双分支 evaluator 的 branch-compute 实测，不是完整接收机总复杂度结论。
- 一旦五档正式参数被替换，旧 26/29、1.3/1.2/1.9 dB、2.5/2.4/3.1 dB、上行 +2.48/+3.07 dB、Fig.3--5 和旧权威 JSON/hash 均不得继续作为终稿证据。
- T016 只产出候选参数与小切片方向诊断；全量 A 评估 runner、B receiver runner、图文同步需 T016 返回后另立 change contract。

### 来源

S001 / R008b / R013 / V011 / 用户拍板

## D017: 路线 B 不变，先用三档新下行参数筛选论文范围

> status: superseded
> date: 2026-07-15
> 取代：D016
> 被取代：D018
> 依据：调研: R008b 修正版 + 验证: V011 + 调研: R014 + 用户原话: voice.md 2026-07-15

### 决策

保留 D016 的 branch-routed adaptive CPR 路线 B；参数执行顺序改为 downlink-first。T017 直接用三档 Family 1 下行候选做 old-vs-new 诊断小切片，不等待上行 P0。若三档下行仍保留 DA/NDA 互补性、selector 方向与 B/A bit-exact，则下一轮拟将两档 uplink simulation regimes 从 CCISP 论文评估范围删除；若不满足，只返回重议，不自动恢复旧上行参数或启用 A2/A3。

本决策只授权 T017 diagnostic probe；不授权正式修改 `params.py`、30-seed 权威重跑、删除论文上行文字/图线、回填数字或提交最终改稿。

### 理由

当前 selector 的直接 common-payload 证据、crossover 和 29-point diagnostic 本来只覆盖 AWGN 与三档下行；两档 uplink 仅贡献 fixed-estimator headline，且不存在通行的纯 GG `uplink moderate/strong` 固定分档。先验证三档文献锚定下行能否独立支撑方法，可避免为保留非核心上行场景继续扩大 spherical-wave/beam-wander 建模范围。

R014 的 P0 停止发生于文献未落盘，而非数值或算法失败。当前 Osborn 与 Kaushal 已归档，但 Al-Habash/Ghassemlooy/Sandalidis 仍缺本地一手证据；该缺口阻止正式参数 WRITE 和论文引用，不阻止明确标记为 non-authoritative 的三档方向性 probe。

### 排除的替代方案

- 继续等待五档 A1+ 全部闭合后才看下行：上行不是 selector 核心证据，等待成本与论文收益不匹配，暂不采用。
- 立即删除 uplink 并改论文：三档新参数下的方法方向尚未验证，排除。
- 三档不理想就自动加回旧 uplink：旧两档无来源，禁止回流。
- 用 A2/A3 强行制造上行更强：D016 已因证据不足排除，继续排除。
- 用 3-seed 小切片产生 headline 或显著性结论：probe 只作 full-run Go/No-Go 输入，排除。

### 影响范围

- D016 整体被本决策取代；其中路线 B、A/B 分工、non-genie 边界和旧结果失效规则继续由 D017 继承。
- T016 不再继续执行；R014 保留为证据管道断裂记录。
- T017 只新增 probe/verifier/R015，不触碰原 A/B runner、旧 JSON、论文、图、正式参数源。
- 若 T017 判 `DOWNLINK_ONLY_PROMISING`，下一轮另立正式三档参数落库、A evaluator + B receiver 全量重跑、删除 uplink 场景和图文一次性闭环合同。

### 来源

S001 / R008b 修正版 / R014 / 用户拍板

## D018: 三档下行 route-B adaptive CPR 正式全流程闭环

> status: active
> date: 2026-07-15
> 取代：D017；同时取代 D008 的 26/29 代理证据、D009 的旧参数数值主结果、D013 的旧参数权威数据
> 被取代：无
> 依据：调研: R015 + 验证: V012 + critic: formal_pipeline_audit / paper_endtoend_audit / task_contract_critic + 用户原话: voice.md 2026-07-15

### 决策

1. 进入三档下行正式闭环。CCISP 的评估矩阵冻结为 AWGN 加 weak/moderate/strong 三档 downlink Family-1 Gamma--Gamma；两档 uplink simulation regimes 从本论文评估、图和结果叙事中删除，但不删除全局 `params.py` 兼容字段、历史脚本或历史结果。
2. 方法身份继续采用 D014 的 `received-power-aware adaptive CPR receiver/method`。路线 B 是运行时实现：逐 256-symbol window 先决策、只执行被选 DA/NDA CPR 分支、输出统一复数序列；路线 A 仅作同 realization 的离线 fixed-branch、selected、paired statistics 和下界评估，绝不冒充运行时输出。
3. 正式三档参数的唯一真相源是 `projects/simulation/params.py`。在修改它之前，必须把 Al-Habash 映射公式和三档 \(\sigma_R^2=0.2,1.6,3.5\) 的可引用来源落成本地可审计原文，并给出式号/页码或 exact line、5% 内独立复算和 derivation。只有 DOI、搜索摘要、子 Agent 转述或“典型值”不算闭合；上行/Sandalidis 不再是本合同门。
4. 保留 `projects/simulation/common/_channel.py` 的末尾可选 `turb_params=None` 与专项测试。该接口是无副作用的诊断/敏感性注入口，不是算法修改；正式 runner 必须从 `params.py` 读取，且结果元数据要断言 override 为 `None` 或与真相源逐位一致，禁止长期在 probe 内硬编码 tuple。
5. 一个持续的新对话按三个宏阶段完成：证据与冻结；正式运行与独立验证；论文 WRITE、构建与终验。普通代码、环境、构建和长任务故障由执行对话自行排查并持续推进；只有下述科学/证据硬门失败时停止有利叙事，仍须完成 BLOCKED 报告和可复用产物。
6. 路线 B 已提供真实 selected output 后，旧 `26/29` aggregate proximity 代理从论文删除，不用新参数复刻。所有旧参数下的 1.2/1.3/1.9/2.4/2.5/3.1 dB、crossovers、Fig.3--5、extension、JSON/hash 和 uplink headline 全部失效；3-seed R015 只作正式开跑依据，不能进入论文。

### 正式运行冻结与硬门

- selector/CV/1.10 margin/13 dB/CPR/消歧/seed/window/metric 不得根据新结果调参；R015 的 15/15 改善不是正式结果必须复现的目标。
- fixed-estimator 正式数据覆盖 AWGN 与三档 downlink，核心点 30 seeds × 400 windows；若保留高 SNR extension，则相应三档必须全重跑并单独标明 5-seed 层，否则从图文删除。
- selector 层固定为 3 scenes × 11 SNR（5--25 dB，步长 2 dB）× 30 seeds × 400 windows。A/B 必须同 realization，并对 990 个 scene-SNR-seed 单元逐项核对 selected errors、DA/NDA 选择数、seed 范围、realization digest 和 selected output；目标为 990/990 exact。
- seed 是置信区间独立单位，400 windows 不是 \(n\)。paired common-768 gain 及 95% Student-\(t\) CI 只从 A 的同 realization 离线评估产生；B 的 fixed-NDA/oracle/gain 必须是 `null`/absent，而不是 0 或不完整数值。
- A 中 `min(ne_DA,ne_NDA)` 只能称 per-window lower-count bound，不能称 true-channel oracle；NDA 的 `tx_bits` 八重消歧继续明确为 post-hoc BER evaluation，不得称 blind online deployable receiver。
- Al-Habash/Family-1 证据未闭合、common 默认路径回归失败、A/B 非 exact、参数 fingerprint/realization 不一致、实现真相三联卡失败，均阻断论文 WRITE。
- 正式方向若相对 R015 反转，触发 TL-20 信号熔断：先做根因审计和独立复算，不调参、不删点、不强写利好。只有正式 JSON 被独立 verifier 从原始记录重算 PASS 后，才进入论文 WRITE。

### 论文与图的闭环边界

- 全文统一 adaptive CPR 方法层级，selection 只作为内部 two-stage control；不称新 phase estimator。
- 删除 uplink 场景、曲线、数字和“both downlink and uplink/five Gamma--Gamma/six conditions”等叙事；参数来源、B/A 角色和真实 selected complex output 必须靠近相应定义说明。
- 三张定量图只消费新正式 JSON，必须带 parameter fingerprint/path 自检且禁止静默 fallback 到旧 JSON。Fig.2 视为用户所有的当前资产：先查 diff并保留用户修改，只集成和最终尺寸验收，不覆盖其独立设计。
- 精炼优先删除无论证职责的公式复述、重复接口说明和 26/29 代理；不得机械执行 R012 的 307--338 词全量删除。fresh `texcount` 正文必须不少于 3500 词，内容不得为守词数而灌水。
- fresh build 必须满足官方 5--10 页、undefined/overfull 为 0，并逐页、逐图按最终双栏尺寸验视；独立 Agent 核对 `source -> params -> JSON -> figure -> prose`。
- 74.6% 只是一条件下的 branch-compute 计时。除非补齐 warm-up、重复、多条件和端到端边界，不进入论文，更不得称总接收机节省。

### 工作树与提交

当前工作树有大量用户/其他对话改动。执行前记录 `git status`、in-scope 文件 hash/diff 和明确 allowlist；禁止 reset/restore、`git add -A` 或目录级 staging。只 stage allowlist，提交前验证 cached path 集合精确相等；整个执行对话最多一次提交。预存的 common/test diff 经本决策批准保留，但不得声称由新对话原创。

### 排除的替代方案

- 为保留 uplink headline 继续寻找或拍取两档上行 GG 数值：非核心且证据成本过高，排除。
- 正式 runner 继续靠 probe 内显式 tuple 而不更新 `params.py`：制造双真相源，排除。
- 用 3-seed probe、旧 JSON 或旧 extension 回填论文：非权威或参数不一致，排除。
- 看到正式结果后调 13 dB、CV、margin、参数或选择性删点：事后过拟合，排除。
- 为“一次做完”跨过证据、独立 verifier 或 fresh render 门：排除；持续推进不等于绕开科学硬门。

### 来源

R015 / V012 / 三路独立只读审计 / 用户条件式批准与本轮执行意图

## D019: 三档下行 Gamma--Gamma 参数与引用方式定死，证据门解除

> status: active
> date: 2026-07-16
> 取代：D018 第3条中"Family-1 σ²_R=0.2/1.6/3.5 必须落成本地可审计原文并给式号/页码"的硬门（R017 证明该门严于领域惯例）
> 被取代：无
> 依据：调研: R017 + 用户原话: voice.md 2026-07-16 + Al-Habash 2001 本地归档 PDF (`papers/doi/10.1117_1.1386641/source.pdf`+`content.md`)
> 触发原话：用户原话: voice.md 2026-07-16（"别人咋声称这几组，我们就咋声称…""这块定死了之后别动了，太折腾了"）

### 决策

1. **三档下行 Gamma--Gamma 参数冻结**，正式闭环唯一参数集（plane-wave）：
   - weak：σ²_R=0.2 → (α,β)=(11.6, 10.1)
   - moderate：σ²_R=1.6 → (α,β)=(4.0, 1.9)
   - strong：σ²_R=3.5 → (α,β)=(4.2, 1.4)
   精确 Al-Habash 映射值与上述冻结四舍五入值的六项相对偏差最大为 2.775%，全部小于原 5% 门；闪烁指数严格有序且每档落在 Andrews regime 区间。冻结后不得再改数值。

2. **证据门解除条件**（修订 D018 第3条）：
   - Al-Habash 公式来源：**已闭合**（`papers/doi/10.1117_1.1386641/` 有 source.pdf + content.md）。
   - Family-1 三锚来源：**按领域惯例等效闭合**——以 Gu 2022（*Appl. Sci.* 12(7):3331，卫星下行）为代表的领域惯例为"著作级引用 Ghassemlooy CRC 教材 2019，不标具体表/页"。本项目照搬该惯例，**不要求**取得教材全文。无 CRC 订阅，不再尝试获取。

3. **引用方式冻结**（论文写作唯一允许的声称形式）：
   > "Following the Gamma-Gamma plane-wave turbulence model, we adopt (α, β; σ²_R) = (11.6, 10.1; 0.2), (4.0, 1.9; 1.6), and (4.2, 1.4; 3.5) for weak, moderate, and strong turbulence, respectively, as given in [Ghassemlooy2019]."
   - [Ghassemlooy2019] = Ghassemlooy, Popoola, Rajbhandari, *Optical Wireless Communications: System and Channel Modelling with MATLAB*, 2nd ed., CRC Press, 2019, ISBN 9781498742696。
   - 可选补引 Al-Habash 2001 作 GG 模型公式来源。
   - **禁止**声称这些值是某张标准表的"典型三档"或"文献标准值"；按惯例只说"as given in [教材]"。**禁止**重新质疑这组值或再开"找出处"的对话（用户要求定死）。

4. 上行两档维持 D018 删除状态（不在本论文评估）；Sandalidis/uplink 不再是任何门。

### 理由

Al-Habash 原典全文已落盘并确认 GG 映射公式（Eq.14/18-19）。子 Agent 全文提取证实，使用 Family-1 三档的领域论文（Gu 2022 卫星下行、Jaiswal 2017 等）**全部采用著作级引用、无一标到具体表/页**——D018 要求的"式号/页码"严于领域实际惯例。用户无 CRC 订阅，强行获取教材全文性价比低且非惯例所需。三档值物理合理（R016 复算 + Andrews 区间）、有可比卫星论文（Gu 2022）使用同一组合过审稿，继续悬而未决只会拖延。用户明确要求"定死别动"。

### 排除的替代方案

- 继续找 Ghassemlooy 教材全文：用户无订阅，领域惯例不要求，排除。
- 把 0.2/1.6/3.5 声称为"文献标准三档"：Al-Habash 原典证实无此标准组合，过度声称，排除。
- 改用其它 σ²_R 值或 Ansari 球面波族：现值已物理合理且复算一致，无必要再折腾，排除（用户定死）。
- 维持 D018 原硬门不变：严于领域惯例、阻塞重跑，排除。

### 影响范围

- T018 宏阶段一证据门**解除**，可进入宏阶段二（改 `params.py`、30-seed formal 重跑、图文同步、终验）。
- 论文引用按本决策第3条的唯一形式写。
- 不改算法、判据、selector、13 dB、seed、窗口数、common-768 统计总体。
- 本决策冻结三档值与引用方式；后续对话不得以"再找更权威来源"为由重开。

### 来源

R017 / 用户定死 / Al-Habash 本地归档 / Gu 2022 惯例子 Agent 提取

## D020: 授权主控修正 Fig.2 route-B 控制流并解除资产边界

> status: active
> date: 2026-07-16
> 取代：D018 中“Fig.2 只集成验收、不覆盖”的本轮资产边界
> 被取代：无
> 依据：验证: V015 + 用户原话: voice.md 2026-07-16

### 决策

用户授权当前主控直接修改 Fig.2 编辑源。修改仅把信息流修正为 `branch command -> branch router -> 单一 DA/NDA 分支 -> selected phase -> common compensation/DSP`，不修改 selector、CV、1.10 margin、13 dB、CPR、参数、seed/window/metric 或正式结果。

### 理由

T018 的唯一终验阻断是旧 Fig.2 仍表达“双路先运行、后选择”，与已经通过 990/990 exact 验证的 route-B 先选后跑实现不一致。用户明确撤销了本轮不得覆盖该资产的限制，因此可以做最小语义修复并重新构建、视觉 QA 和独立终验。

### 排除的替代方案

- 继续保留 BLOCKED 等待外部资产维护方：用户已授权主控修改，排除。
- 改 route-B 实现或重新跑正式结果来迁就旧图：会破坏已冻结算法与数据，排除。
- 仅改 caption 而保留错误箭头：不能闭合实现真实性，排除。

### 影响范围

`projects/simulation/figures/fig2_adaptive_cpr.{drawio,pdf,png,svg}`、Fig.2 结构测试、论文嵌入宽度、fresh build，以及 V015/T018 最终状态。

### 来源

S001 / 用户授权 / V015 原 Fig.2 语义阻断

## D021: Fig.3 fixed 横轴统一为 5--35 dB、2 dB 步长

> status: active
> date: 2026-07-16
> 取代：D018 中 fixed-estimator 的旧代表点网格（仅网格，不取代 A/B adaptive 网格）
> 被取代：无
> 依据：用户原话: voice.md 2026-07-16 + 验证: fixed-grid contract tests

### 决策

Fig.3 所消费的正式 fixed DA/NDA/oracle 数据，AWGN、weak、moderate、strong 四个场景统一使用 5, 7, ..., 35 dB（16 点）；保持 30 seeds、400 windows、既有算法、参数、统计口径不变。A/B adaptive 仍保持冻结的 5--25 dB、2 dB 步长和 990/990 exact 契约。

### 理由

旧 fixed 网格在不同场景分别为 5--20 dB 和不规则的 5--26 dB，导致 Fig.3 横轴范围不一致，也无法比较高 SNR 的低 BER 区域。统一网格是图表可比性修正，不是依据结果调整 selector、参数或指标。

### 排除的替代方案

- 只在绘图层把旧曲线外推到 35 dB：会把未运行点伪装成正式结果，排除。
- 修改 A/B adaptive 5--25 dB 网格：与已冻结的 selector 990/990 契约冲突，排除。
- 看到新曲线后调整算法、阈值或删除不利点：违反正式闭环纪律，排除。

### 影响范围

更新 `params.py` 的 fixed 专用网格、fixed runner、fixed verifier/tests、Fig.3/交叉图、Results 中 fixed 网格描述和由新正式曲线计算的 crossover 数字；不改 A/B JSON、selector/CV/1.10 margin/13 dB/CPR/seed/window/metric。

### 来源

用户原话 / fixed-grid contract tests / T018 正式闭环

## D022: CCISP 论文治理收口为一个活动专题

> status: active
> date: 2026-07-16
> 取代：独立 `2026-07-16-ccisp-fig1-layout` 专题安排
> 被取代：无
> 依据：用户原话: voice.md 2026-07-16 + registry/目录只读审计

### 决策

以 `2026-07-14-ccisp-content-expansion` 为 CCISP 论文唯一 active/canonical 专题，并更名为“CCISP 2026 论文整稿闭环”。`2026-07-13-ccisp-submission-prep` 与 `2026-07-14-ccisp-figure-typography` 只保留为关闭的历史档案；刚创建且尚未执行的 Fig.1 专题撤销，其设计与任务合同迁为本专题 S002/T019。后续同一论文的单图、排版、文字和投稿修订默认追加到本专题，不再拆新专题。

### 理由

同一论文被拆成投稿、内容、字体和单图多个入口，已经增加查找与恢复成本，也让用户难以判断当前主线。历史专题若物理搬迁，会造成 S/D/V 编号冲突和大量引用断裂；因此采用“一个活动入口 + 关闭历史档案”的最小破坏收口。

### 排除的替代方案

- 排除把所有历史文件强行搬进同一目录：会产生编号冲突并破坏既有证据指针。
- 排除继续保留独立 Fig.1 活动专题：任务尚未执行，迁回总专题成本最低。
- 排除删除投稿和字体历史：其验证证据仍需可追溯。
- 排除今后每个单图或局部修改都建专题：粒度过细；只有独立长期生命周期且用户明确批准时才可例外。

### 影响范围

更新 `_registry.yaml`、本专题 topic-index/S002/T019/decisions/voice，以及投稿骨架专题的关闭状态；不修改论文、图片、仿真、数据或历史验证内容。

### 来源

S002 / 用户治理纠正 / 独立只读审计

## D023: 论文引用删减按质量与职责双门执行

> status: active
> date: 2026-07-16
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-07-16 + 调研: 当前 aux/HEAD aux 引用集合审计

### 决策

CCISP 论文删除或替换引用时，必须同时检查正文职责与来源质量；在职责可由多篇文献承担时，优先保留 IEEE Transactions、JLT、PTL 等高质量且直接相关来源，优先删除低质量、弱相关或超出当前 downlink scope 的来源。不得仅为压页或减少参考文献数量而移除已经归档并承担论证职责的高质量文献。

### 理由

当前 PDF 的实际引用由 24 条降为 18 条，其中消失集合包含 TSP、JLT、TCCN、TCOM 等高质量来源；多数并非从 `references.bib` 删除，而是在压缩 Introduction 时失去正文挂接。只按文字长度删引用会破坏此前投入建立的证据链，也不符合 comparable-paper 的 related-work 组织要求。

### 排除的替代方案

- 为控制页数按引用数量机械删减：引用质量和论证职责比条目数量更重要，排除。
- 无差别恢复全部旧引用：Conroy uplink 与当前 downlink scope 不贴合，Martins OSA Continuum 相关性和质量优先级较低，不要求恢复。
- 保留高质量文献但把多篇堆在无职责句尾：仍属于引用罗列，排除；恢复必须绑定具体论证职责。

### 影响范围

后续修改 `sections/introduction.tex`、`sections/system_model.tex`、`sections/method.tex` 与 `references.bib` 时适用；不改变正式参数、算法、结果或指标。

### 来源

用户纠正 / Introduction 与引用集合独立审计

## D024: 导师批注驱动的 Skill 门禁升级与论文统一修订

> status: active
> date: 2026-07-17
> 取代：S003 中“只做提取和规划、暂不修改”的阶段边界
> 被取代：无
> 依据：用户原话: voice.md 2026-07-17 + S003 + Skill RED/GREEN 压力测试 + 21 项论文现状审计

### 决策

批准先升级 `paper-writing` 与 `external-output` 的导师/审稿反馈处理门禁，再按一个统一批次修改 CCISP 论文。统一批次采用 `INTAKE -> DIAGNOSE -> PROPOSE -> WRITE -> VERIFY -> DELIVER`，以逐条反馈账本为唯一核销入口；每项局部批注必须同时执行全文同类问题扫描。论文修改顺序固定为论证结构与术语、公式/符号职责、图表、引用、作者元数据、精确五页版式，最后 fresh build、逐页视觉 QA 和独立 reviewer 终验。

### 项目硬门

- 终稿必须恰为 5 页，并占用到第 5 页最后允许行；参考文献末页双栏视觉平衡。
- 作者为张哲铜、吴浩；吴浩为通信作者，邮箱 `wuhao@bit.edu.cn`；单位只用仓库既有正式证据，不猜测。
- Fig.3--5 图例位于图面/坐标轴内且统一；Fig.4 不用约等号，标注不遮挡；HD-FEC 若无独立职责即从图中移除。
- DA/NDA 定义为两类 CPR 算法/方法，不以“互补”定义，不把论文身份退回估计器选择。
- 会议引用按论证职责与来源质量压缩；不机械删除高质量 Transactions/JLT/PTL。
- 明确删除线内容不得以同义改写回流；局部删除必须扩展到同类防御性、元话语和内部验证语言扫描。

### 冻结边界

不修改 selector、CV 门限、1.10 margin、13 dB、CPR、三档参数、seed/window/metric、正式数据和结果；不覆盖用户维护的 Fig.1/Fig.2 drawio。禁止用 filler、弱引用、不可读缩图、负间距或删除有效性边界凑到五页。

### 排除的替代方案

- 排除只逐条改批注位置而不扫描全文同类问题：会重复出现同源缺陷。
- 排除先调字号/间距再改内容：结构变化会推翻排版且掩盖论证问题。
- 排除把所有导师局部意见机械升级成通用禁令：须区分项目合同与可复用规则。
- 排除以引用数量或文献类型机械删减：必须保留不可替代的直接证据。

### 来源

S003 / 用户批准 / paper-writing RED-GREEN / 独立 21 项 feedback ledger
