# PROMPT-029：R038 第一轮判决规则实验的独立复核（V043）

> 来源: S018§32 / D062 / PROMPT-028 交付条款（"独立 agent 复核 → V043"）
> 交付目标: 对 R038 全部关键声称做独立重算复核，产出 V043 记录素材
> 工作树：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2（bash: /d/code/study/research-protocol/.worktrees/rdl-method-production-v2）
> 专题：.sessions/2026-08-30-thesis-advisor-text-outline/
> 说明：本提示词为自包含任务书（T 类）。原计划由实验对话内子 agent 执行，因 agent 派发接口故障改为人工开新对话执行。编号：V043（verifications.md）；如需 session 记录用 S018§32 附注，不新开 S。

## 0. TL;DR（执行方先读）

你在复核一轮 LDPC 译码迭代预算判决规则实验（PROMPT-028/R038）。实验声称：冻结规则 RC_120（检查点 {20,30,50,100} 处 syndrome 绝对水平 ≥120 即中止该帧）在三确认批上 verdict=KILL（FER 损失 +0.24/+0.49/+0.34pp vs cap200 固定点，>0.2pp 门），但成本机制量活（平均迭代 53.8/54.7/58.3→15.0/14.6/18.2）。你的任务：**独立重算**这些声称（不是读 summary 复述），逐项 PASS/FAIL，产出复核报告。**最高纪律：①只读不写仓库（计算用 python 内联，禁止在仓库内新建/修改任何文件）；②独立重实现规则语义（不要 import 实验模块 _common.py）；③发现不一致如实报，不圆场。**

## 1. 背景（理解任务必需，了解即可不对照评价）

- 实验在冻结 LLR 缓存上跑 NOMS(0.75,0) cap=200 全轨迹译码（每帧 200 个逐迭代 syndrome 计数 s_1..s_200），从 28 个预注册候选中在 dev 池（4 批 1600 帧）选出 RC_120，冻结后在三确认批（M15/W12/S16 各 2048 帧）单次评分。
- 规则三态：s_t==0 → 接受停（成本 t）；t∈{20,30,50,100} 且 s_t≥120 且未接受 → 中止（成本 t，失败）；否则烧满 200。
- FER 双口径：a=停点迭代代输出语义（接受帧看 accepted_info_ok；砍帧失败；烧满帧看 info_errors_at_200==0）——与 R036 固定点同定义；b=接受语义（砍帧一律失败）。
- 合同：projects/simulation/explore/decode-budget-rule/contract.yaml（v1 冻结+amend v1.1）。报告：.sessions/2026-08-30-thesis-advisor-text-outline/R038-iteration-budget-rule-first-round.md。

## 2. 数据与工具

- 数据：projects/simulation/results/decode-budget-rule/{raw_traj_dev.json, raw_traj_confirm.json, raw_iterates_confirm.json, frozen_rule.json, summary.json}
- 结构：raw_traj_*.json → batches{名字: {seeds[], syndrome_weights[[200]], converged_at[]（1-based 首 syndrome=0，-1=无）, info_errors_at_200[], accepted_info_ok[]}}；raw_iterates_confirm.json → batches{cond: {ie_at_10[], ie_at_15[], cut_frame_index[], cut_stop_iter[], cut_ie_at_stop[]}}
- 锚点：results/decode-failure-rescue/raw_confirm2048.json（B0 20 迭代 syndrome）；results/decode-capability-audit/raw_capability.json（NOMS200 臂）
- Python：/c/Users/zzt/.venvs/torch/Scripts/python.exe（numpy/scipy 可用）

## 3. 复核项（逐项 PASS/FAIL/PARTIAL + 数字证据；独立重算优先）

1. G1 抽验：raw_traj_confirm.json M15 批抽 20 帧，syndrome_weights 前 20 个 vs raw_confirm2048.json 同 seed B0.syndrome_weights 逐位一致。
2. G2 抽验：抽 20 帧（含 converged_at=-1 的），converged_at 与 info_errors_at_200 vs raw_capability.json M15 NOMS200 臂同 seed 一致。
3. 规则语义独立重实现（W12 全 2048 帧）：期望 accept=1555 / cut_correct=454 / cut_wrong=10 / exhaust=29 / mean_it≈14.59。
4. FER 口径 a 重算（W12）：规则 FER≈0.2393；cap200 固定 FER=(ie200>0).mean()≈0.2344；差≈+0.49pp。
5. M15/S16 快速复算：FER 0.2275/0.2354、mean_it 15.02/18.21、错砍 3/4。
6. 省算 CI 抽验（W12）：d=it_cap200ES−it_rule 逐帧，均值≈40.07，2000 次 bootstrap CI95 下界远 >0（R038 引 [36.9,43.3]）。
7. 选型准则核对（frozen_rule.json candidate_table）：RC_120 满足"W_pooled≤2 且每批 W≤1 中节省最大"，fallback_used=false。
8. 防泄漏：dev 四批 seeds（5000-5063/41000-41511/42000-42511/43000-43511）与确认批（30000-32047/50000-52047/53000-55047）零重叠。
9. 零改动：git status/log 确认 decode-failure-rescue/、decode-capability-audit/、results/decode-capability-audit/ 无修改；新文件只在 explore/decode-budget-rule/、results/decode-budget-rule/、.sessions/2026-08-30-thesis-advisor-text-outline/（注：R039 第二轮正在并行生成新文件，属预期，不算违规）。
10. 报告数字对账：R038 §二 Pareto 表 8 行×3 条件 vs summary.json pareto_fer_vs_mean_it；accepted_wrong=0 与 accepted_info_ok 全真；cap10/cap15 FER 复算（口径 a：成功=conv≤cap 或 ie@cap==0）。
11. 事后 oracle 扫描抽验：自实现 RD_0.65（red=s_c/max(s_1,1)≥0.65 同检查点）在 W12 错砍数（期望 4）与三条件 FER 损失量级（0.00/+0.20/+0.15pp）。
12. 文本诚实性：R038 如实报告 KILL、amend v1.1 口径事件、事后扫描"非部署证据"标注、未失败调参。

## 4. 产出格式

最终消息给：逐项 PASS/FAIL/PARTIAL+一行证据；不一致清单（文件+字段+期望 vs 实际）；总结论（通过/不通过+必改项）。主对话将据此写 V043 到 verifications.md。

## 5. 已知陷阱

- 引用常量是 4 位小数舍入（0.2251 vs 461/2048=0.225098），对账容差 5e-5。
- summary.json 的 p_sign 对全同对（wins+losses=0）为 1.0 属正常。
- 结论限所跑合同（BG2 z=104、exact-APP LLR、NOMS(0.75,0)、cap200）；不要外推评判。
