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
