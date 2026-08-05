# [R001] Step 3 直接竞品与 P1 问题裁决

> 2026-08-05 | 关联：2026-08-05-shared-m0-foe-cpe-groundwork / D002

## 调研问题

在不进入 Step 3.5/4a 的前提下，全文精读关闭两篇 HIGH★ 直接竞品，建立 comparator、matched-output、
复杂度协议，并判断 P1 能否形成通过 canonical 四判据的 Q#。

## 发现

1. 九篇全文均由 fresh-context worker 逐篇 title 自检并通过；逐篇字段、七子表和证据见
   `papers/_read_notes/`，总表见 `projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`。
2. CSNDSP 2014 的 FOE 输入是相邻符号乘积的相位增量，CPR 输入是符号本身，最优 monomial 阶数也
   不同；它只提出硬件块“可能共享”，没有 shared sequence 实现或资源结果（源 `content.md`
   L47–55, L113–117, L151–161, L181–195）。
3. JLT 2018 明确只算一次一符号 correlation 给 FE/PR 共享，并报告 adders −23%、multipliers −25%、
   latency −25%（L63–89）；L73–75 与 L237 又明确记载 OFC 2016 已共享 differential m-th-power FE
   和 Viterbi PR 的 m-th power。generic P1 action 因而发生 existing-action collision。
4. 仍可精确定义的窄 delta 是 `raised=x^M0` 跨 FOE→CFO correction→CPE 的生命周期，以及
   `raised*exp(-j*M0*omega*k)` 与原域 `exp(-j*(omega*k+phi))` 的 matched-output 合同；但九篇池
   未关闭 OFC 2016 一手 exact boundary。“未见”不等于 novelty。
5. 合法 comparator 必须分层：当前串行同估计器；JLT 2018/OFC 2016 conventional refactor；LPT
   2016/JLT 2019 cheap arithmetic；ISCAS 2022/LCOMM 2026 hardware；TSP/JPHOT estimator-changing。
6. Q-P1-01 判据 1/2/4 PASS，判据 3 FAIL：项目要求 2019+ 顶刊 task-matched recent baseline，而直接
   shared-action 证据为 2016/2018；2019+ 论文没有把当前重复 raised-domain 计算指出为其 failure A。

## 结论

九篇全文已读，但没有 canonical 四判据全过的 P1 Q#；按 `gw-read.md` L198 与 `glossary.md` L65–70，
状态必须保持 Step 3 BLOCKED/IN PROGRESS，不能离开 Step 3。失败机制是 generic existing-action
collision、recent task-matched baseline 缺位与 OFC 2016 一手证据不足；`trivial refactor` 仅为高风险
解释，不能在 Step 3 定性为最终 Kill。P1 只保留 `THESIS_ENGINEERING_COMPONENT` 的窄候选层级。

## 对决策的影响

D003 记录 generic action collision 与窄 delta；其自造 terminal 已被 V003 证伪并由 D004 取代。
不改变 D001 的冻结 M/C/A，不授权回 search、Step 3.5/4a/实现/仿真。
