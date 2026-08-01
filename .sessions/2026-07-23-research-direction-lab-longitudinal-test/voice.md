# Voice — Research Direction Lab 长程真实运行测试

> 用户原话档案，按日期。除零信息推进/应答外都收，不去重。

## 2026-07-23

- "是。但由于并没有那么紧急，所以我建议还是先追求找方法，哪怕是包装出的方法，也比分析强很多。或者说，方法其实很好包装，只看怎么包？因此等我们做的够多了，我们挑挑拣拣也能包点出来？" → D012
- ⟶ "别搞得太重（我没看你写的，只是习惯性提一下）。然后，得想好之后用的时候会咋用，怎么开一个个新对话，它们做什么？比如之前咱们遇到的那些情况，都该怎么处理？我理想的情况就是，我啥也不管，你给我提示词我开glm对话，做完了给你反馈，你再给我提示词，我中间啥也不看，然后跑着又稳又快，产出能用的东西。这是最好的。" → S001 被 2026-07-26 推翻
- "是。不过有个问题你得知道，你的上下文满的太快了，因此互相之间的交互字数要少，内容主要放到文件里（因为codex的压缩机制，我要是一直给你搬，那压缩之后也会占很多上下文），我复制粘贴的，只有文件索引以及关键信息（重要）。还有就是，咱们得考虑和sessions专题的配合，比如什么时候新开一个专题，比如你是不是最好专门弄一个日志记录关键流程，用来速查、防偏啥的？" → S001
- "但这样的话，具体工作细节就丢了。我希望有长程稳定日志和各自工作也有日志并不冲突" → S001
- "是。不过没必要急匆匆就去这么做。不然我很担心拍脑袋弄出个没用的，或者太重了。我更想咱们好好分析刚才的情况，仔细设计一个好的，然后直接就去用（我会fork当前对话）。等跑一段时间，再让你看看情况" → S001
- "你不觉得，这干的太少了吗？" → S001
- [转述]"同意按大包带债推进" → D062
- "随便，多做点" → D063
- "随便，反正现在算是在测试。这波做一阵之后我会回去让看看情况，总结一下，看看哪里控的不对" → D064

## 2026-07-26

- "纵向 live test 已运行到 T007，现在停止继续派 T008，做只读阶段审计。" → system D018
- "以及，是不是最好让它每轮分析结果之后，强制它去回顾最初以及整个链条（得有一个专门文件，简短记录，我记得有来着？），想想偏没偏？有没有连续多次在小范围打转或者工作量太少之类？" → system D018
- "也就是三层？一个简单的，一个相对详细的，一层每次单独的？这样的话，前两个是不是最好别加Sxxx？直接固定文件名，以后别的专题都在这？" → system D018
- "然后，目前我好像额度用不完，要重置了，打算之后gpt开个新对话去开goal模式一直做" → D002 / H002
- "当前无 active scientific carrier；campaign remap 完成前不得运行新实验、修 T008/B1 或派 T009。" → D003
- "首轮比较至少三个合法 carrier；不足三个时逐项证明其他候选为何不满足 formal readiness。" → R001
- "选择下一包前，明确说明它为什么比至少两个替代项更可能产生 METHOD_SIGNAL。" → D003
- "完成一个 T 不等于 Goal 完成。每包必须记录 method delta、no-method/repair/same-axis streak 和 drift；继续自动推进下一决策。" → D003
- "不把测试 PASS、治理 PASS、negative result 或 evaluator 修复冒充方法产出。" → D003
- ⟶ "你要不告诉我goal咋改？我想让你这个对话一直做下去。我现在不太想分glm让它做。希望你自己昨完全部" 推翻 2026-07-23 → D004

## 2026-07-28

- "让goal跑了十几个小时，效果不是很好啊？" → S002
- "按你推荐" → D026
- ⟶ "你不急着验证。你先写个日志记录1情况。然后你再更新skill，然后再给我新的提示词（这次不是goal了，是glm）" 推翻 2026-07-26 → D026

## 2026-07-29

- "这玩意能包吗？我最近一直没看。你先说说，顺便给我提示词" → T025
- "不过我得说一下，基本每次交互都会发生压缩。这很难受。咱们目前把控的咋样？" → R009 / D034
- "行，改完之后咱们继续？" → D034
- "停止中转当前 T027。做一次最小入口纠偏，不运行科学实验，不开新专题" → D035 / V061
  （附长指令：列出 T027 的四项绑定缺陷——信道源码无频域物理自由度、comparator 非已确认传统同信息对象、
  control_epoch 59≠60、action_class 与正文语义不一致；要求 method-factory 入口补"problem-bearing
  testbed preflight"四门、每门 file:line、禁"未测族/REOPENED/testbed 曾产 signal"放行；
  只审判一个替代入口（CB1 逐符号/更新粒度族），判放宽 identity parity 是否科学合法；
  四门全过则原位修订 T027 不建 T028，否则记 STRATEGIC_GATE 不生成新科学任务；明确边界不跑 seed/
  不实现/不新建 testbed/不改 protected history 与 formal owners/Skill 只补入口门不扩 controller）
- ⟶ "在一个对话内完成'T027 最终纠偏 → 科学执行 → 独立验证 → 主控接收'，不要在任务准备后停下来等用户。" → D036 / V062
  （附四项确定性纠偏长指令：①门2 证据等级——sprint-001"块末更新几何是结构性吸引子原因"已在
  CP018/D026/V052 被拒收，不得继续写成已确认机制，正确表述=块末更新是 source-backed 值得验证的
  疑似作用点、T027 正是检验其因果性的诊断 sprint；②冻结 comparator 身份——传统 comparator=
  tuned per-symbol standard CMA，必须用 canonical Godard-with-z 梯度 Δw∝(R²−|z|²)·z·r*，
  `_cma.py` scalar-error 缺 z 只能证明 block_size 是真旋钮不得冒充 comparator，provenance 指向
  canonical cb1_cell_runner 实现/公式并单独 dev 调谐 μ；③修正执行授权——action_class 改
  PREFORMAL_METHOD_FACTORY，foreground 显式允许本次 bounded factory，不再用
  METHOD_FACTORY_TASK_PREPARATION 掩盖实验，更新 control epoch 重跑 validate_task_control.py，
  授权只覆盖本次 diagnostic sprint 不授权 formal MVE/Step 5/论文 claim/protected owner 修改；
  ④增加传统 comparator 裁决终态——tuned per-symbol CMA 已消除 block-64 问题而新构造没稳定超过
  必须判 PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR，不是 METHOD_SIGNAL 也不形成 active carrier。
  Phase 1 由独立 executor 跑 3-5 个更新粒度构造（含 inherited block-64、tuned per-symbol comparator、
  ≥2 个可部署候选，block size/μ/更新预算分别公平调谐，dev 冻结后跑 fresh held-out，paired/seed-cluster/
  raw/prefix-only/identity-semantic smoke 全闭合，block size×μ/更新预算消融，禁用 seeds 71-80，
  不改 common/params/protected owner、不 push），terminal verdict 五选一；Phase 2 独立 verifier
  核 Godard-z 公式/provenance、信息公平、dev-test 隔离、μ 与更新预算公平、raw→aggregate 可复算、
  归因不越界、verdict 符合五选一，verifier 不过只允许一次包内确定性修复不另开第二修复对话，无法
  修复则 EXECUTION_INVALID；主控更新 mission-log/topic-index/D/V 与必要 owner，有 signal 只登记待
  promotion 不冒充 formal method，统一一次 commit working tree clean；聊天只回 verdict+关键数字+
  是否 signal+verifier 结论+worker-log/artifact/commit SHA）
  [用户原话明确：本轮端到端完成，中间不参与技术判断]

## 2026-07-30

- "接收 CP027/T027 为可靠局部负面，立即轮换，不修复、不追加 CB1 实验。…… 本轮目标：在 CB1
  collapse 家族之外，从既有资产中选择一个真正 problem-bearing 的新 testbed，并在同一对话直接
  完成一次新 method-factory sprint。入口比较最多三个候选，必须逐项满足：1.有明确 M-C-A … 2.源码
  证明候选动作可作用的物理/算法自由度确实存在 3.开跑前已命名传统、同任务、同信息、可独立调谐的
  comparator 4.有当前有效的 runnable testbed … 5.能形成明确的毕业论文 primary/fallback packaging
  6.每项均给当前有效 evidence 的 file:line；rejected、invalidated 或 privileged 证据不得重新洗成
  PASS。…… 入口通过后不要先写一个 T 再停。由独立 executor 立即：构造并运行 3–5 个机制不同的最小
  方法 …… terminal verdict 至少区分 … DIAGNOSTIC_METHOD_SIGNAL / NO_DIAGNOSTIC_SIGNAL /
  PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR / BLOCKED_SHARED_TESTBED / EXECUTION_INVALID。
  只 有新候选稳定超过调谐后的传统 comparator … 才能形成 METHOD_SIGNAL。再由独立 verifier 重算并
  审查。主控完成接收、mission-log/topic/D/V 更新和一次统一 commit。若三个入口均过不了前置门，
  不得制造第四个弱候选；直接输出 STRATEGIC_GATE，具体说明缺的是 testbed、comparator、物理问题
  还是论文范围授权。" → D037 / V063
  [绑定结论：CB1 z-only 后处理和更新粒度两条 factory 线均已跑完；tuned per-symbol CMA 只救活 1/7
  cell；block-8 相对 per-symbol ΔPI-SER=-0.00293，CI 跨0；不再运行 CB1 collapse-recovery 的
  block-size、μ、更新调度、频域/子带、z-only、初始化或 cost 变体；这是局部关闭，不外推为整个盲均衡
  或接收机方向 Kill；当前 active carrier 仍为 0]

- "用户授权方案 1：用一个端到端大包完成"物理可信的 channel 扩展 → problem-bearing testbed →
  conventional baseline adjudication → 条件式 method factory"。预算约一天，不在选择入口或建设
  基础设施后停下来等待用户。…… 一、物理入口筛选：由独立文献/物理 subagent 从以下候选中最多比较
  三个：complex time-varying Jones / differential phase coupling；physically justified PDL；PMD、
  色散或其他具有跨符号记忆的 coherent dual-pol FSO impairment。不得假定这些现象在 LEO/星地 FSO
  中成立。每个候选必须过六门 … 1.与当前 coherent dual-pol 星地 FSO 论文范围直接相关 … 2.至少两篇
  可访问 primary/fulltext 来源支持其存在、模型和参数范围；3.用真实参数做量级核算 … 差三个数量级
  以上直接 Kill；4.明确传统、同任务、同信息、可调谐的 conventional comparator；5.能写成具体 M-C-A，
  而不是"增加复杂信道看看有没有增益"；6.预计可在约一天内完成隔离实现、验证和小批诊断。所有门必须给
  全文或源码 file:line。oracle gap 不能作 Go 依据。若三个候选均失败，直接终止为
  PHYSICS_BACKED_TESTBED_UNAVAILABLE 并建议转论文范围/新子问题，不继续制造第四个 impairment。
  二、只扩一个 channel 自由度：若且仅若一个候选六门全过——只实现排名第一的单一 impairment；新模块/
  显式 mode 隔离，旧 channel 默认路径必须 byte-identical；不为让方法有用而扩大参数；参数全部绑定
  文献范围；建理论预期、单位测试、极限退化测试、seed 可复现和旧模型 regression；独立 verifier 先确认
  模型公式、单位、时间尺度和实现一致。testbed 未通过物理/身份验证，不得进入方法实验。三、conventional
  baseline adjudication：在新 testbed 上先运行——原有 shared anchor；一个任务匹配、receiver-visible、
  充分调谐的传统 comparator；一个明显廉价扩展（如适用）；paired realization、dev freeze、fresh held-out、
  raw rows、CI。只有记录 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE 才允许进入 method factory。若传统
  comparator 已解决问题，终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR，不包装成新方法。四、条件式
  method factory：若问题仍存，同一对话立即由独立 executor 构造并运行 3–5 个机制不同的最小方法，不再
  返回用户等待授权。要求：每个方法只用 deployable receiver-visible 信息；单独 dev 调谐，fresh held-out；
  与 tuned conventional comparator 比较；raw rows、paired CI、help/hurt/tie、语义 smoke、消融和复杂度
  记录齐全；只有新候选稳定超过 comparator，且排除额外信息、调参预算和实现伪影，才能判
  DIAGNOSTIC_METHOD_SIGNAL；signal 同时给 primary packaging 和 fallback packaging。五、独立验证和接收：
  至少分离——物理模型/source verifier；实现与数值 verifier；主控最终科学裁决。允许一次包内确定性修复，
  不开第二个修复对话。最后统一更新 topic-index、mission-log、D/V、必要 owner，并一次 commit；不 push。
  最终只回：1.选中的物理自由度及六门证据，或 PHYSICS_BACKED_TESTBED_UNAVAILABLE；2.testbed 与
  baseline-adjudication verdict；3.method-factory terminal verdict；4.comparator、最佳候选、CI、
  METHOD_SIGNAL/active carrier；5.worker-log、artifact、verifier 和 commit SHA。" → D038
  [绑定结论：本轮不是继续挖 CB1；CB1 collapse-recovery family 已关闭，不运行其 block-size、μ、cost、
  初始化、z-only 或频域换名变体；CB1 物理自由度窄是 CP028 根因，本大包针对此升级 channel；段A 六门是
  上游物理 DOF 筛选屏（选 impairment），独立于 method-production 入口四门（选 method）；段间不停下
  等用户]

## 2026-07-30（campaign 授权）

- "咱们得多跑一些。至少跑10大包？" → D039
  （附长指令：授权至少 10 个有效科学大包的新子问题探索预算；完成 10 个有效包前，不再因为当前 portfolio
  0 READY 而要求 thesis pivot；setup、治理、任务准备、接口修复不计包数；建立最轻量 rolling queue；
  至少 5 个机制族、同族最多连续 2 包、第 5 包内部校准但不停线、第 10 包才做 campaign-level pivot/continue
  裁决；已完成/关闭线不得换名重开——NDA-ML 本体、G1 science repair、CB1 collapse family、Pilot-Jones
  已关闭小轴、PMD/PDL/Jones/CD 移植）
  [绑定结论：本轮立即端到端执行 Package 01（CPR 选择器 SNR 失配鲁棒性），A 登记决策+队列、B 执行，
  不在 A 后停止]

## 2026-07-30（P03 执行：撤回 T030 + 定点协同设计）

- [转述，绑定裁决长指令] "执行 10-package campaign 的 Package 03。先撤回无效 T030，再在同一对话端到端运行
  新的 P03；不得停在入口修订或任务准备阶段。" → D041
  （附绑定裁决：P01/P02 为 A_CPR_selector_robustness 两个有效包，campaign=2/10；A 族关闭不得继续；既有 T030
  FOE-residual→CPR 入口经独立历史审计 FAIL——重开 B10/B12 机制、未证明真实 post-FOE residual、1 MHz 是 FOE 前
  warning 参数、历史 Doppler 变化量级远低于 FOE 分辨率、comparator/残差范围未冻结；撤回 T030 保留 rejected brief
  该准备工作不计有效 P03；新 P03 family=B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN；P03 目标=判断已完成 DA/NDA
  CPR selector 定点部署时是否存在"统一位宽浪费资源或损害分支选择"真实工程问题，若存在构造并验证
  sensitivity-aware mixed-precision；不是重开 NDA-ML 也不得把旧浮点增益重计作新成果；冻结作用范围优先 selector
  控制路径；bit-true 基础模型必须真实定点合同禁止 decimal rounding 冒充；Phase A uniform-precision baseline、
  Phase B 3-5 mixed-precision、公平比较 + Pareto + 消融 + resource proxy 明确标注；六终态；论文边界无实际综合只声称
  bit-cost/resource proxy；独立 executor+verifier，允许一次包内确定性修复，有效完成后 campaign→3/10 families_started
  加 B，同一对话选择 P04 不同机制族入口但不运行，统一一次 commit 不 push；最终只回 5 项）
  [绑定结论：本轮端到端完成 P03，中间不参与技术判断；verifier V067 10/10 PASS，verdict PROBLEM_RESOLVED_BY_
  UNIFORM_PRECISION，campaign→3/10]

## 2026-07-30（P04 执行：撤回 16APSK 环比入口 + 连续 GG OOD）

- [转述，绑定裁决长指令] "执行 10-package campaign 的 Package 04。先撤回无效的 16APSK ring-ratio 入口，再在同一对话
  端到端执行'连续 GG 参数 OOD 下的 selector 鲁棒性'；不得停在入口修订或 problem probe 后。" → D042
  （附绑定裁决：campaign=3/10；A_CPR_selector_robustness 已关闭；B_FIXED_POINT family 本轮结束 P04 必须换族；
  原 P04 16APSK 环比失配入口 FAIL——γ 是调制格式配置不是当前信道随机量、selector 不读取环比、matched/configured
  demod 是显然常规解、撤回保留 rejected brief 不计有效包；原备选湍流标签失配同样不成立 selector 不读 turbulence label；
  合法新问题改写为"固定/AWGN 拟合的 CV decision boundary 在文献参数范围内训练未见过的连续 GG 分布上是否产生
  selector-specific regret"；family=C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS；只用已有来源支持的 GG 范围 σ_R² 位于
  weak/moderate/strong 锚点覆盖区间、由已验证公式映射 α/β、不引入饱和湍流/新传播模型/拍定参数、generator 用已有
  显式 (alpha,beta) 接口、原三锚点保留作回归控制；dev/held-out σ_R² 网格 + SNR cells + seeds + primary metric + MDE +
  selector-specific regret 定义在读结果前冻结；Phase A problem-bearing probe 比较 frozen original selector / 固定 DA /
  固定 NDA / 原三 turbulence anchor regression / per-cell best fixed branch 仅离线 diagnostic bound；运行时 selector 只用
  receiver-visible 输入严禁 turbulence label/true α,β/true h/TX truth 进 decide；无 selector-specific problem 则
  PROBLEM_ABSENT_ON_CONTINUOUS_GG 本包作有效负面 4/10 不构造方法；Phase B 最强廉价 comparator=独立 dev 连续 GG 网格上
  统一重调的现有 CV_MARGIN/SNR threshold 全区间单组全局参数不读 turbulence label 给相同调优预算 test 前冻结，若统一
  global retune 已消除问题则 PROBLEM_RESOLVED_BY_GLOBAL_RETUNE 不得包装方法，不得用'先估 turbulence level 再套规则'
  作 comparator/候选除非有独立 receiver-visible estimator 和不同信息增量 单纯把 CV 再映射成 label 属循环包装；Phase C
  仅当 global retune 后仍有残余 selector-specific regret 同包构造 3-5 机制不同最小候选仅用 receiver-visible 统计 dev freeze
  后跑 fresh held-out 保存 raw rows/branch occupancy/gain/regret/CI/help-hurt-tie 做消融，只有候选稳定超过 global-retune
  comparator 达冻结 MDE/CI/跨网格一致性才判 DIAGNOSTIC_METHOD_SIGNAL；其他终态 PROBLEM_ABSENT/RESOLVED_BY_GLOBAL_RETUNE/
  NO_DIAGNOSTIC_SIGNAL/BLOCKED_SHARED_TESTBED/EXECUTION_INVALID；独立 verifier 查 α/β 映射范围来源/dev-test σ_R² 网格隔离/
  seed 隔离/turbulence truth 未进 decide/original anchor regression/selector-specific regret 与共同分支退化区分/global retune
  公平性/raw→aggregate 与 verdict；允许一次包内确定性修复；有效完成后 accepted_valid→4/10 families_started 加 C 同一对话
  选择 P05 新机制族入口但不运行 不把连续 GG 负面外推成全部 turbulence robustness 统一一次 commit 不 push；最终只回 5 项）
  [绑定结论：本轮端到端完成 P04，verifier V068 8/8 PASS，verdict PROBLEM_ABSENT_ON_CONTINUOUS_GG，campaign→4/10]

## 2026-07-30（P05 binding decision 执行指令，用户中转）

- "执行 10-package campaign 的 Package 05，并完成第5包内部校准。一个对话内完成入口纠偏、fresh problem gate、条件式在线适配 factory、独立验证和主控接收；不得在校准或问题验证后停下来等用户。"
- "campaign=4/10；P01–P04 均围绕完成 selector/工程，P05 必须换对象"
- "撤回 P05-D FEC/旋转模糊：无真实 codec；threshold eval 不是 FEC；TX-bit rotation resolver 为 privileged；pilot resolver 旧线已裁决"
- "撤回 P05-E window/complexity：重复 B1 adaptive phase-window；'NDA 比 VV 复杂'的旧担忧不成立；selector 统计不是主要计算量；P03 已覆盖定点轴"
- "上述准备不计有效 P05。新 family = D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION"
- "必须明确：这里的 ML equalizer/ButterflyCNN 不是已完成的 NDA-ML CPR selector，不得混淆两条方法身份"
- "若 checkpoint、训练分布或任务身份无法闭合：BLOCKED_ML_TESTBED_IDENTITY。不允许拿身份不明 checkpoint 继续跑。"
- "只使用现有 provenance 支持的参数范围，不提高 SOP/Doppler/f_G 来制造问题。"
- "真实 TX symbols 只用于离线评分，不能进入任何在线适配或 gate。"
- "在 test 前冻结 problem gate，必须区分：1. ML 自身 OOD/时间漂移；2. corrected CMA 也共同退化；3. metric/alignment/warm-up 造成的伪差；4. 单 seed/checkpoint 偶然性。"
- "若 corrected baseline 下没有稳定 ML-specific regret：PROBLEM_ABSENT_WITH_CORRECTED_BASELINE。作为有效 P05 计入 5/10，不构造在线方法。"
- "已有 periodic-pilot fine-tune 仅可作为历史 cheap alternative，需计 pilot overhead，不能因旧 FAIL 而故意欠调。"
- "P06 必须再选一个不同机制族，使前六包至少覆盖5个家族；同一对话准备 P06 入口但不运行；统一一次 commit，不 push。"
- "最终只回：1. P05 terminal verdict；2. frozen ML、corrected CMA、传统在线 comparator、最佳候选关键数字与 CI；3. 是否形成 METHOD_SIGNAL/可包装的在线适配；4. campaign 5/10 中期校准与 P06 新机制族入口；5. worker-log、artifact、verifier、commit SHA。"
  → D043 / V069 / CP034（P05 verdict = PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER，5/10 mid-calibration 完成）

## 2026-07-31（P07 binding decision 执行指令，用户中转）

- "执行 campaign Package 07。必须在同一对话端到端完成入口纠偏、Phase 0、科学实验、独立验证、治理更新和一次统一 commit；不要只写任务简报后停止。" → D045
  （附绑定裁决长指令：worktree=`rdl-method-production-v2`/expected HEAD=3487d5a/branch=codex/rdl-method-production-v2；
  当前 accepted_valid_packages=6/10，五个机制族，0 METHOD_SIGNAL，0 active carrier；
  一、入口纠偏——P07 文件中的 F/G/H 只是未冻结名称扫描非合法入口（F timing offset 当前 1-sps 信道无过采样/脉冲成形/分数延迟；G 场景扩展无冻结 M-C-A 易重入 P04/FOE；H FEC/APSK coded chain blocked/APSK 环比已撤回），保留为 rejected brief 不运行；正式 P07=F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG，与 P03 必须严格区分（P03=DA/NDA selector 内部统计量数字定点精度；P07=接收模拟前端可变增益/ADC 满量程/削顶/量化分辨率，不得复用 P03 uniform precision 结论）；
  二、冻结 M-C-A——M=固定增益/固定满量程/有限位宽 I/Q ADC 后接冻结现有接收链；C=来源闭合 GG 动态幅度深衰落与强峰值时间交替；A=固定增益必须在两损害间折中（增益过高峰值 clipping/过低深衰落有效量化分辨率不足），目标判断矛盾是否真实产生接收性能损失、能否被标准因果 AGC 解决、robust/clipping-aware AGC 是否还有可区分增量；
  三、Phase 0 可信 ADC/AGC adapter——信号链固定 channel output→过去样本决定下一 block analog gain→I/Q rail clipping→有限位宽 uniform ADC→原冻结接收机；要求 1.明确定义 signed I/Q quantizer/full-scale/step size/saturation flag 2.gain 只能由过去已量化接收样本/rail-hit/接收机可见统计决定 3.禁止 true channel/TX symbol/未来 block/未量化幅度真值进 decide 4.float-bypass 必须与原接收链逐 realization 身份一致 5.固定增益/传统 AGC/新候选共享相同 realization/位宽/full-scale/更新周期/延迟 6.位宽/full-scale/update interval 必须来自已有硬件/论文资产或预先冻结敏感性范围 7.至少覆盖 6/8/10 bit 8.无法建立可信 adapter 则 EXECUTION_INVALID 不计 P07；
  四、Phase A 问题存在性——比较 ideal float ADC/dev-tuned 最佳固定增益 ADC/oracle per-block gain 仅作 headroom/Kill bound 不作 Go comparator；主要指标 PI-SER 或冻结主指标/EVM/clipping rate/effective occupied codes/相对 ideal ADC paired regret；dev 前冻结 problem MDE/至少多少物理条件过门/CI/help-hurt/跨位宽一致性/fresh seed ledger；若最佳固定增益在来源闭合 GG 下没有稳定跨位宽实质 regret 则 PROBLEM_ABSENT_ON_SOURCED_ADC_RANGE Phase B/C 不运行但有效 P07 可计入 7/10；
  五、Phase B 强传统 comparator——至少 causal RMS AGC/peak-hold attack-release AGC/可选标准 log-domain AGC；传统 comparator 必须使用相同过去信息/相同更新预算/增益上下限/slew-rate/延迟/dev-only 调谐/test 冻结/不读 true GG/channel；若最强传统 AGC 已恢复到冻结容差则 PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC 不进方法包装；
  六、Phase C 方法工厂——仅当问题存在且最强传统 AGC 未解决时运行，至少 4 种构造（dual-time-constant attack-release/clipping-aware anti-windup/robust Huber-percentile amplitude estimator/hysteretic two-range gain/可选 uncertainty-gated 但不得用 ML 充数），每候选必须不同作用机制不得同公式换超参，优先检查 cheap alternative，只有最佳新候选在 fresh held-out test 上超过最强传统 AGC/达冻结 MDE/paired CI 不跨零/跨多位宽湍流条件方向一致/没靠更多更新次数或更大信息预算获益/消融支持 clipping-resolution 机制才允许 DIAGNOSTIC_METHOD_SIGNAL，否则只能 NO_DIAGNOSTIC_METHOD_SIGNAL/PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC/EXECUTION_INVALID，若得 signal 只登记 pre-formal carrier 不直接宣称论文主方法；
  七、P06 措辞边界——不修改不重跑 P06 但后续记录必须准确表述 history-expanded>current-only、persistence>history-expanded 因此是"没有超过强传统 temporal baseline 的方法增量"不是"历史完全无信息"；
  八、治理与验证——有效科学执行才把 campaign 6→7/新增 F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG/不修改 Skill/controller/formal owner/protected history/P08 只准备不同机制入口不运行/executor verifier 分离/verifier 独立核查 ADC 数学/float bypass/causal AGC/truth leakage/dev-test 隔离/paired realization/raw→aggregate/跨位宽判据/terminal verdict/artifacts 保存 raw rows/aggregates/contract/source hashes/seed ledger/最后只统一 commit 一次不 push；
  最终只汇报五项：1.P07 terminal verdict 2.ideal/fixed/传统AGC/最佳候选关键指标 paired Δ与CI 3.clipping-resolution 问题是否存在是否产生 METHOD_SIGNAL/active carrier 4.campaign 7/10 状态与 P08 入口 5.worker-log/artifact/verifier/changed files/commit SHA）
  [绑定结论：本轮端到端完成 P07，中间不参与技术判断；verifier V071 10/10 ACCEPT，verdict NO_DIAGNOSTIC_METHOD_SIGNAL，campaign→7/10]

## 2026-07-31（P07-R 科学完整性修复执行指令，用户中转）

- "执行 P07-R 科学完整性修复。不要启动 P08，不把本轮另计为第八包。"
- "本轮必须在同一对话完成：根因复现 → 最小修复 → 物理消融 → fresh 重跑 → 独立 verifier → 治理纠偏 → 单次 commit。不 push。"
- "一、先冻结审计结论 —— P07 当前科学结论不得继续使用。需要验证的三个根因假设：H1 SCALE…H2 CONTROL…H3 LIFECYCLE…在任何修复前，分别建立最小失败测试…必须保存修复前失败证据。不能一边改一边猜。"
- "二、治理纠偏 —— 创建新的纠偏决策和验证血缘：D046 supersedes/amends D045 的科学有效性部分；V072 独立复核并取代 V071 的科学层结论；V071 保留，不删除，标为'合同一致性通过但物理正确性漏审'；原 P07 artifacts 保留并标 INVALIDATED，不覆盖。在修复重新得到有效科学结果前：accepted_valid_packages：7 → 6；current：P07-R；P08：暂停。最终若修复实验有效完成，再把计数恢复为 7/10；若仍 EXECUTION_INVALID，则保持 6/10。"
- "三、实现正确的 gain-aware ADC 链…不要直接修改旧 P07 产物来隐藏错误。新建明确的 p07r repair 路径或版本化文件。"
- "八、重新裁决问题…旧 P07 的 dev/test seeds 和输出已经观察，最终裁决必须使用全新且与 campaign 历史不相交的 dev/test trajectory ledger。保持原 MDE=0.15 dB，除非有预先登记且独立验证的理由，不得事后更改。"
- "十、收尾…若修复后形成有效 P07：campaign 恢复 7/10，再准备 P08 但不运行。若 EXECUTION_INVALID：campaign 保持 6/10，不得用治理完成冒充科学包。不修改 Skill/controller/formal owner/protected history。写 sim-preflight usage log。单次统一 commit，不 push。"
  → D046 / V072-PART1+2
  [绑定结论：本轮端到端完成 P07-R 科学完整性修复；verifier V072 PART2 10/10 ACCEPT；verdict PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION（旧 P07 +0.91dB 是 H1 SCALE artifact，corrected 链 W8/W10 +0.03~+0.07dB≪MDE）；campaign 恢复 7/10，F 族关闭]

## 2026-08-01（P08 coded-chain 场景扩展授权，用户中转）

- "行" → D047
  （附 P08 coded-chain 执行指令长 brief：worktree=rdl-method-production-v2/expected HEAD=0317e4a/branch=codex/rdl-method-production-v2，不 push，单次统一 commit；
  scope-change：原范围 pre-FEC/无真实 codec 的 diagnostic method factory → 新范围允许建立 source-auditable 最小真实 coded baseline 并运行 P08-P10 coded-layer package；禁止阈值模型冒充译码/随机玩具 LDPC 冒充标准/TX-truth LLR/未验证 codec 写论文；
  Phase 0A 标准码来源门（优先 DVB-S2 r2/3 16QAM/BICM；只 LDPC 无 BCH 须称 component；检索须子 agent 用 tools/search 或 primary source 主对话禁灌网页；禁手写 parity/随机 H/pyldpc 冒充/凭包名/悄悄换码率帧长；无法闭合 terminal=CODED_BASELINE_SOURCE_UNAVAILABLE）→ Phase 0B 最小真实 coded-chain sandbox（coded_contract/codec_adapter/coded_realization_adapter/receiver_to_llr/coded_metrics，不破坏 frozen common，复用 GG/SOP/AWGN 物理模型，禁 TX truth 改善 receiver）→ 编解码算法正确性门 12 项 + AWGN waterfall 三区（失败 terminal=CODED_CHAIN_IDENTITY_UNAVAILABLE）→ Phase A 问题门（B0/B1/B2/oracle，dev/test 全隔离新 seeds，主指标 required-SNR@frozen FER，MDE≥0.15dB）→ Phase B 条件式方法工厂（仅 Phase A 问题存活，≥3 机制不同候选 C1/C2/C3+可选C4）→ Phase C 公平比较归因 → 独立 verifier 15 项 → 治理收尾单次 commit；
  最终只汇报五项：1.采用的标准码/来源hash/真实 coded-chain 身份与 AWGN waterfall 2.B0/B1/B2/oracle/最佳候选 FER/post-BER/required-SNR/iterations/CI 3.P08 terminal verdict/问题是否存在/是否 METHOD_SIGNAL/active carrier 4.campaign 8/10 状态与 P09 条件式入口 5.scope-change/D/V/worker-log/artifact/verifier/changed files/commit SHA）
  [绑定结论：本轮端到端完成 P08 coded-chain 扩展包]

## 2026-08-01（P08-R coded-chain 科学完整性修复执行指令，用户中转）

- "执行 P08-R coded-chain 科学完整性修复。暂停 P09，不把本轮另计为第九包。"
- "本轮必须在同一对话完成：根因复现 → 治理回退 → coded-chain 身份澄清 → GG/信息/oracle/metric 修复 → fresh powered experiment → 条件式方法构造 → 独立 verifier → 一次统一 commit。不 push。"
- "二、治理立即纠偏 —— 新增 D048…P08 codec/AWGN 基础设施保留为 PARTIAL reusable asset；V073 的科学 ACCEPT 撤回；PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE 撤回；G family 暂不关闭；accepted_valid_packages：8→7；current：P08-R；P09 暂停。V073 保留，不删除…旧 P08 artifacts 保留并增加 INVALIDATED 标记，不覆盖、不删除。"
- "三、修复前最小失败证据 —— 任何修改前，建立并保存确定性 prefail tests：H1 GG provenance…H2 runtime information…H3 oracle action space…H4 metric contract…H5 coded identity wording…H6 state lifecycle / sample size…prefail evidence 必须在修复前保存。"
- "四、coded-chain 身份修复 —— 准确命名：'5G NR BG2 rate-matched LDPC component + Gray-16QAM BICM baseline'…对 bit interleaver 二选一并冻结：A 启用 num_bits_per_symbol=4 / B 保持禁用…不得在读取 test 后切换 A/B…补齐此前缺失项：reference vector 或独立第二实现交叉验证。"
- "六、receiver-visible σ² —— 所有 deployable baseline 禁止读取 true gamma。优先采用冻结的已知 calibration/pilot prefix…若已有合法 pilot 接口，复用它；若没有，新增最小固定 calibration prefix，不得使用整帧 TX truth。"
- "七、建立合法 oracle ladder —— 至少实现并区分：O0 global-truth oracle / O1 codeword/block-truth oracle / O2 finer/local truth bound…oracle 只作 Kill/headroom，不作 Go。如果 O1/O2 相对 strongest conventional 的 coded headroom 小于 MDE，问题直接关闭，不构造方法。"
- "八、重新冻结 metric contract —— 旧 P08 test seeds 全部视为已观察，禁止复用。先用新的 dev trajectories 确定一个可达到的 SNR/FER 工作区，再冻结 test…不得在 test 后从 A 临时切到 B。"
- "十一、独立 verifier V074 —— verifier 必须与 executor 分离，并逐项核查：1.五/六个 prefill 根因真实复现…V074 不得只复述合同或测试 PASS，必须沿 caller→callee 检查科学信息边界。"
- "十二、治理与收尾 —— 若修复后科学包有效：accepted_valid_packages：7→8；G family 根据新 verdict 决定关闭或保留…若仍 EXECUTION_INVALID：保持7/10…不修改 protected history，不 push，最后统一 commit 一次。"
  → D048 / V074


## 2026-08-01（P08-R2 执行指令）

- "执行 P08-R2 最终科学修复。P09继续暂停。本轮不是新包，不另计编号。"
- "worktree：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2 / expected HEAD：5a7823d / branch：codex/rdl-method-production-v2"
- "必须在同一对话完成：旧缺陷复现→campaign回退→receiver完整去除true-SNR→metamorphic信息门→正确功效设计→fresh crossing实验→条件式方法工厂→独立verifier→一次统一commit。不push。"
- "一、状态回退——新增D049/V075血缘：D048/V074保留，标为GG/oracle/identity层修复有效，但完整receiver信息边界与统计功效漏审；P08-R科学verdict撤回；accepted_valid_packages：8→7；G family重新打开；current=P08-R2；P09暂停；codec、5G-NR LDPC、真实bit interleaver、GG真相源、O0/O1/O2代码作为PARTIAL资产保留。旧P08/P08-R artifacts不覆盖，增加INVALIDATED标记。"
- "二、修复前确定性复现——先保存prefail evidence：H7 true-SNR上游泄漏（固定完全相同的rX/rY/calibration prefix/receiver state/codeword/noise realization，只修改隐藏truth gamma_bar，验证旧P08-R：equalized output发生变化/prefix residual发生变化/B0B1B2 LLR发生变化；记录max absolute difference和调用链 p08r_run.build_realization→real.equalize→blind h estimate→MMSE→demapper）；H8 AST verifier盲区（证明旧verifier只扫描B0B1B2函数体内的real.gamma_bar字面量，没有递归进入real.equalize()→self.gamma_bar；记录为何V074漏审）；H9统计合同（复算并证明 MDE_fer=0.2347来自固定n后的非配对Bernoulli近似；实验真实单位是paired trajectory；先固定n再把detectable difference命名为MDE不合法；dev FER=0.1 crossing真实存在；weak/fG1000、weak/fG100、moderate/fG100的O2 required-SNR headroom约在0.15dB附近；[0,+0.0141]不能称CI_lo>0；test逐trajectory选择min(B1,B2)不合法）。修复前证据落盘后才能改代码。"
- "三、receiver信息边界根修——禁止任何deployable路径读取：gamma_bar/true SNR；true h/theta；payload TX symbols/bits；evaluation residual；future samples。重新设计receiver接口：received prefix + known prefix symbols → receiver-visible pre-equalization noise/effective-residual estimate → blind amplitude/channel estimate → MMSE/equalizer → equalized prefix → demapper residual scale → payload LLR。"
  → D049 / V075

## 2026-08-01（P09 执行指令）

- "执行一个新的有效科学大包：P09。"
- "本轮目标：P09 = COMPUTE_CONSTRAINED_NDA_ML_SEARCH，围绕已有、已验证有效的 NDA-ML 方法做'低复杂度、性能保持'的毕业方法生产包。"
- "不要重新证明 NDA-ML 是否有效，也不要把它当成新发现。"
- "M = 当前 full-search NDA-ML；C = 有限计算量/实时接收约束；A = 均匀穷举大量候选导致计算冗余；目标 = 在 receiver-visible 信息不变的条件下，用结构化搜索显著减少 objective evaluations，同时保持原方法性能。"
- "建议冻结的双门：A. 性能非劣……CI upper ≤0.10 dB；B. 复杂度：objective evaluations 至少减少 4×。算法计数为 primary cost，墙钟时间仅 secondary，不用 Python timing 冒充硬件复杂度。"
- "命名最强廉价 comparator：至少包含 dev-tuned uniform coarse grid；如已有传统 hierarchical/coarse-to-fine search，必须纳入。"
- "true phase/noise/SNR/TX truth 不得进入 deployable decide。"
- "若无法证明计算问题或 novelty boundary，终止为 STRATEGIC_GATE，不计包。"
- "本轮端到端完成，不在入口选择后停下；只有入口门失败才停为 STRATEGIC_GATE。有效科学执行才计入 campaign；治理、修复、准备不计。"
  → D050 / V076

## 2026-08-01（计数纠正 + P09 重定向执行指令，用户中转）

- "在同一对话内完成两部分：A. 确定性纠正 campaign 当前计数；B. 端到端执行重定向后的 P09，不得在 A 或入口准备后停止。"
- "上一轮 P09 对 NDA-ML 的 STRATEGIC_GATE 保留：NDA-ML 是 closed-form estimator，不是 candidate/objective search，禁止换名重开 NDA_ML_BODY_REOPEN。"
- "但 campaign=8/10 是 stale/错误 current view：P08-R2 没有独立 pre-test contract/receipt/hash；dev 与 test 在同一 runner 中连续执行；最终合同、结果和 verifier 同时进入 a21fdba；无法证明最终合同在首次观察 test seeds 8000–8039 前不可变。"
- "按 confirmatory evidence fail-closed：accepted_valid_packages = 7/10。P08-R2 只能保留为：PARTIAL — corrected coded-chain/receiver/oracle engineering asset and local diagnostic evidence。G 族状态：STOPPED_WITH_PARTIAL_ASSET。不允许 P08-R3，也不允许 coded/interleaving 换名重开。"
- "纠正方法：1. 新增 D/V 血缘纠正，不删除旧记录；2. D049/V075 保留历史，但其'恢复第8包'的效力被新 D/V 取代；3. topic-index/current control block/registry 当前计数改为 7；4. mission-log 追加新 checkpoint，不篡改旧 checkpoint；5. D050/V076 的 NDA-ML STRATEGIC_GATE 保留；6. 纠正工作本身不计科学包；7. 完成纠正后立即进入下面 P09，禁止只提交治理修改。"
- "P09 = H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH。M：16APSK full blind phase search；C：有限实时计算预算；A：每个 window 对全部相位候选计算星座距离，存在 B×N 的搜索开销；目标：在相同 receiver-visible 信息、相同延迟和相同 BPS objective 下，减少 distance/objective evaluations，同时保持 full BPS 的恢复性能。这不是 NDA-ML 搜索，也不是重开 NDA-ML body。"
- "源码入口：projects/simulation/common/_recovery.py 中真实 bps_cpr；当前实现只支持 qpsk/qam16，需做最小 16APSK adapter；16APSK constellation/判决器优先复用 sc_nda_ml_sim.py 等已有资产；不修改 NDA-ML 本体。"
- "入口硬门（运行实验前逐项给出 file:line）：1.真实搜索自由度：BPS 确实枚举 B 个相位并逐候选计算距离；2.问题成立：full BPS 的主要复杂度确由该搜索产生；3.强传统 comparator 可实现（full uniform BPS/fixed coarse BPS/fixed two-stage coarse-to-fine BPS）；4.16APSK adapter 保持同一个 BPS objective 和信息边界；5.检查既有 ANN-CPR、2S-BPS、BMLPR 等 collision。"
- "若发现 16APSK fixed two-stage 已被现有代码/文献完全覆盖，不得伪造新颖性；仍可把它作为传统 comparator。候选只能声称：'面向当前 16APSK 接收链的 confidence-adaptive/local-refinement 实现'，不能声称首创低复杂度 BPS。若连问题或可区分 action 都无法成立，终止 STRATEGIC_GATE，不计包。"
- "四、真正的 pre-test freeze——不能再次使用'同一最终 commit + 最终字段一致'冒充 test 前冻结。在读取或运行任何 held-out seed 前，必须生成独立冻结凭据（contract 内容及 SHA256/runner/source hash/primary metric/dev/test seeds/cell/slice/full/comparator/candidate 集/MDE/non-inferiority threshold/complexity threshold/sample-size/power rationale/forbidden information/receipt creation time/test_started=false）。"
- "由于此前已发生三次 chronology 缺陷，本轮允许使用一次实验前 checkpoint commit 作为自动提交规则的长实验例外：Commit 1：计数纠正 + frozen contract + receipt，必须发生在任何 held-out test 前。随后 runner 必须：1.校验当前源码/contract hash 与 receipt 一致；2.将 test_started=true、receipt hash 写入 raw artifact；3.hash 不一致立即 EXECUTION_INVALID；4.held-out seed 如在现有 artifacts/ledger 中出现过，立即更换。实验完成后再做最终 Commit 2。不得 squash 两个 commit。"
- "比较合同共享：paired realization/modulation/SNR/GG-SOP/window/eval region/carrier-frequency-phase 输入/latency/receiver-visible 信息/downstream metric/dev-test seed isolation。传统 baseline ladder：B0 full uniform BPS/B1 dev-tuned fixed coarse BPS/B2 dev-tuned fixed two-stage BPS。候选最多三个（C1 confidence-gated local refinement/C2 curvature-score-gap guided refinement/C3 early-stop adaptive-width search），每个候选必须只有一个主要机制，并有消融，不得将三个机制堆成一个方法。"
- "Primary performance：required-SNR 或等价 dB-domain metric；fixed-label BER 与 PI-BER 双报，明确哪个是 primary；相对 full BPS 的性能损失 CI upper ≤0.10 dB。Primary complexity：实际计算过的 candidate-symbol distance evaluations；refinement、confidence 估计和 fallback 全部计入；至少降低 4×；wall-clock 只作 secondary；不能只统计 coarse stage 而漏掉 refinement。"
- "门控顺序：Phase A 确认 full BPS 有效并量化性能与搜索成本；Phase B 测试最强传统 fixed coarse/two-stage（若 B1/B2 同时满足性能损失 CI upper ≤0.10 dB + 复杂度降低 ≥4× → 终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS）；Phase C 只在传统 comparator 未解决时运行候选。"
- "只有候选在 fresh held-out test 上同时：1.对 full BPS 性能非劣；2.相对 full BPS 降低 ≥4×；3.稳定优于最强 fixed coarse/two-stage comparator；4.CI 和预设 MDE 均过门；才可判 COMPUTE_EFFICIENT_BPS_METHOD_SIGNAL。允许终态：PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS/NO_DIAGNOSTIC_METHOD_SIGNAL/COMPUTE_EFFICIENT_BPS_METHOD_SIGNAL/EVIDENCE_INSUFFICIENT/EXECUTION_INVALID/STRATEGIC_GATE。"
- "METHOD_SIGNAL 后建立 bounded method card（方法名/三步算法/相位搜索流程/最坏-平均 candidate evaluations/与 full-fixed-two-stage 差别/性能-复杂度 Pareto/confidence 触发率与 fallback 率/可用于毕业论文的方法描述/novelty ceiling 和已有工作 collision 边界）；它只能作为 pre-formal carrier，后续仍须回到 GW Step 1–3/3.5/4a，不直接写成正式创新结论。"
- "八、独立 verifier 必须由 fresh-context verifier 检查（11 项）：Commit 1 早于任何 held-out test/receipt-source-contract hash 闭合/held-out seeds fresh/16APSK BPS objective 实现正确/full-coarse-two-stage-candidate 信息和延迟公平/refinement 全部成本已计数/完整 deployable 调用图无 truth leakage/raw→aggregate/性能非劣和复杂度双门/terminal verdict 唯一/campaign 从正确的 7/10 更新/若本包有效无论正负才变成 8/10。"
- "九、最终只汇报五项（1.计数纠正结果及 pre-test receipt/Commit 1；2.full/最强传统 comparator/最佳候选的性能、复杂度和 CI；3.terminal verdict、METHOD_SIGNAL 和 active carrier；4.正确 campaign 计数及论文包装；5.worker-log/artifact/verifier/Commit 1/Commit 2 SHA）。不 push。"
  → D051 / V077（计数纠正）+ P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH（重定向，进行中）

## 2026-08-01（P09 纠偏 + P10 执行指令，用户中转）

- "在同一对话端到端完成：A. 将 P09 从 EVIDENCE_INSUFFICIENT 纠正为 EXECUTION_INVALID/KILL_C3；B. 执行 P10 = RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER。"
- "worktree：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2 / 当前 HEAD：51e9a8e"
- "一、P09 确定性纠偏——独立语义审计已经发现四项承重缺陷，必须从源码重新核实：1.(8,8)-16APSK 具有 π/4 旋转对称性；2.B0在完整2π搜索64点，实际包含8组对称重复；3.C3先调用 bps_objective_matrix 计算全部64点，再事后只计前8点，因此真实执行成本仍为64 eval/symbol；4.C3所有dev/test realization均固定B_used=8，没有数据依赖动作，不是adaptive early-stop；5.resolve_m16apsk_blockwise使用TX bits选择旋转，只能作truth-resolved/PI-like指标，不能称receiver-visible fixed-label BER；6.frozen 0.10dB与mde_ber=0.005换算不一致，且未使用paired Δ CI。处理：新增D/V纠偏，不删除D052/V078；将P09科学终态改为 EXECUTION_INVALID；P09不计包，campaign仍为7/10；P09代码和artifact保留并加INVALIDATED标记；H_BPS轴关闭：只剩'将搜索域缩到π/4基本域'的传统实现纠错资产；禁止P09-R、禁止扩大n、禁止把fixed basic-domain BPS包装成方法；完成后立即执行P10，不得只做治理提交。"
- "二、P10研究问题——P10 = RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER。禁止做已经Kill的'先跑ML，再检测失败，再切CMA'。本轮动作必须发生在payload处理前：M：固定使用ButterflyCNN或固定使用CMA；C：接收工况在长/慢变与短/快变之间变化，且只允许执行一个主专家；A：历史证据显示专家排名反转——长慢变条件ML占优，短快变/OOD条件CMA明显占优；目标：仅根据receiver-visible前缀与合法配置，在运行payload专家前选择ML或CMA，只执行被选中的一个。这是一种跨工况、风险约束的单专家接收策略，不声称新均衡器。"
  → D053 / V079（P09 纠正 EXECUTION_INVALID）+ P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER（进行中）
  [绑定结论：本轮端到端完成 P09 纠偏 + P10，中间不参与技术判断]
