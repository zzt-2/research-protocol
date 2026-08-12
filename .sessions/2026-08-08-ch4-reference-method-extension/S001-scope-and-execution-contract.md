# [S001] Ch4 reference-method extension 范围与执行合同

> 2026-08-08 | 立项 | 完成
> 2026-08-08 续接 | T001 回传纠偏 | T002 待派发
> 2026-08-08 续接 | T002 回传 | 入口裁决完成，V003 PASS
> 2026-08-08 续接 | H003 接收与 T003 准备 | T003 待派发
> 2026-08-08 续接 | T003 回传 | 科学执行迁入独立专题，Step 2 READY
> 2026-08-11 续接 | K1 blocked 后自动轮换 | K2/K3 入口重裁完成，无 survivor
> 2026-08-12 续接 | candidate-source / research-object scope change | K2 唯一恢复 Step 1 入口

## 目标

把“为 Ch4 产出一个真实方法章”的意图固化成轻量、可恢复、可停止的执行合同，避免继续在 supporting 审计、概念期预算预杀和同一小范围循环中偏航。

## 记录

经三路独立分析与交叉复核，CCISP 能成方法的关键不是先做完整治理闭包，而是已有可复现 baseline、实际性能缺陷、receiver-visible action 与成熟 testbed；近期长程流程则常在方法构造前投入过重 collision、provenance 与基础设施门控。用户接受转向 reference-method extension：仍在星地相干 FSO 总伞内，优先选择一个可复现的外部 reference baseline，先复现并观察具体缺陷，再增加一个可部署动作，并把廉价替代放进公平比较。

本专题只冻结入口合同，不选择具体科学对象。下一轮最多比较 3 个 research object / reference baseline，选出至多 1 个正式入口。单一胜者可获 3–7 天最小 testbed 预算；每个对象最多 2 个 method-bearing package，两个机制不同对象均无方法增量时必须回用户做战略范围决策。

T001 回传后，主控复核发现规则本身造成过早停止：G3 允许低成本 defect reproduction，却在同轮禁止实验并要求目标 FSO defect 已成立；同时把两个 entry-screening 候选未过门误算成“两个 research object 已失败”。R001 的事实结论保留——Paillier/K01 是 exact collision，LBS-RDE 的 FSO defect 仍未知——但战略耗尽强度由 D003 取代。

用户批准纠偏后，当前范围改为一次有界 candidate-source expansion。T002 只从外部 reference baseline 中比较 2–4 个机制不同对象，最多选 1 个进入“以 defect reproduction 为目标的 Groundwork”。入口期允许用“外部已发表 defect + FSO 迁移物理机制 + 0.5–1 天可证伪 smoke 合同”通过准备门；不在 T002 内真正运行 smoke。下一轮仍须从 GW Step 1 开始，不能把预注册 smoke 提前到 Step 3/4a 之前。

T002 已完成 4/4 组定向 query 与两个机制不同候选的入口比较。C1 RML-FSTS 以 2023 FSTS 的 fixed lag/`BL` 条件依赖为 source defect，八门全过并成为唯一 `READY_FOR_GW_STEP1_DEFECT_REPRODUCTION` 入口；C2 BUM-CMA 因 weak-branch gradient defect 未被论文支持且 faithful smoke/testbed 未闭合而不入场。独立 verifier 初审要求把廉价替代从 global fixed lag 收紧为 modulation/TS/power-conditioned single-lag lookup，且它仍失败才允许 smoke PASS；该修复不改变入口层级。未来 smoke 只复现 fixed-lag defect，不测试 RML-FSTS 方法；本轮未实现、仿真、运行 smoke 或进入 Groundwork。

T002 是 entry screening，当前 object/package failure 计数仍为 `0/0`。只有下一轮从 GW Step 1 合法启动、Step 1–3 通过并在 Step 4a evidence-valid 执行 smoke 后才开始计数。

V003 fresh-context verifier 初审 `PARTIAL`，发现 cheap comparator 过弱、query receipt 未持久化、prior-art identity 缺失；主线程逐项修复后复核 `PASS`，P0/P1/P2=`0/0/0`。最终接受 RML-FSTS 唯一入口与 terminal，未留下修复项。

H003 接收验证已完成：D004 的 terminal 与 `decisions.md` 一致；R002 明确 source defect 只到 fixed lag/`BL` 条件依赖，目标星地 lag-ranking crossover 仍为 UNKNOWN；R002/topic-index 均确认 object/package failure 计数为 `0/0` 且未授权 smoke。registry 查重仅命中本控制专题，没有独立 RML-FSTS Groundwork 专题。

T003 已准备。执行方必须先查 registry，再新建独立 `2026-08-08-rml-fsts-groundwork` 专题；单对话只运行正式 GW Step 1 与 Step 2，并在覆盖面报告交用户确认处停止。Step 3/3.5/4a、预注册 smoke、实现和仿真全部保持禁止。

T003 已完成：独立执行 owner 为 `.sessions/2026-08-08-rml-fsts-groundwork/`；Step 1 PASS，Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。本专题转为 dormant 来源 owner，不再承载 RML-FSTS 科学执行。

2026-08-11 主控在 K1/Q001 以 `EVIDENCE_BLOCKED` 收口后授权一次 bounded auto-rotation，只重裁原四卡剩余的 K2/K3。接收核验确认 topic-index 不变量与 registry 血缘未变；D005 临时扩大当前范围，但不授权实验、下载或新全文精读。原四卡 action signature 从执行对话 JSONL 恢复后，全部重新锚定到仓内 primary/source，不以聊天记忆作为证据。

两个 fresh-context science agent 分别审计 K2/K3。K2 的 suffix pollution 为 TSP 2022 明确 published defect，但 future action 未唯一化，且 TCOM 2016 order-2/3 mixture tracker 对多轨迹/likelihood/merge-prune/confidence 构成高风险强邻居；因 task/target 不同，不声称 exact collision 或已完全吸收。K3 缺 task-matched published fixed-JP failure，原 JP-V&V 反而报告 fixed coupling 可 near-optimal。R003/D006 因此给出 terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_SHORTAGE`。未创建新专题、未运行 GW Step 1、未实现或仿真；入口拒绝不计 research-object failure。

2026-08-12 Q001 用一天内 defect smoke 证明问题不存在或过小后关闭；不再调参重跑或作为 Ch4 材料。主控据用户对较大单方向预算的既有接受，显式改变 candidate source 与 research object：停止接收链微缺陷枚举，唯一恢复 K2。R004 重新逐字段审计 TCOM 2016，结论为 mandatory full-general comparator 而非 exact same action。D007 纠正旧 E5/E7 的 Step 1 前置过严门，并把单方向 fair comparison 预算上调为预计 5–9 天；本轮仍只授权新专题 Step 1，不授权下载、实现或仿真。

## 决策引用

- D001：冻结 Ch4 reference-method extension 执行合同（新建）。
- D002：本地入口池无直接 survivor；候选事实保留，战略耗尽强度被 D003 取代。
- D003：入口审计不计对象失败，改设 defect-reproduction gate（新建）。
- D004：选择 RML-FSTS 作为唯一 defect-reproduction Groundwork 入口（新建）。
- V003：独立 verifier 初审 PARTIAL、修复后 PASS，P0/P1/P2=`0/0/0`。
- T003：RML-FSTS 独立 Groundwork Step 1–2 任务已回传；执行 owner 见 `.sessions/2026-08-08-rml-fsts-groundwork/`。
- D005：临时恢复 dormant owner，只做 K2/K3 bounded entry re-adjudication（新建）。
- D006：K2/K3 均无入口 survivor，terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_SHORTAGE`（新建）。
- V004：fresh-context verifier 经三轮措辞修复后 final PASS，Critical/Major/Minor=`0/0/0`。
- D007：改变 candidate source / research object 与预算；唯一恢复 K2 Groundwork Step 1 入口（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（T003 科学执行在独立专题完成；本专题只更新 current-view 交接）。

## 后续

本专题仍是 dormant source owner。K2 科学执行迁到独立 `2026-08-12-multi-hypothesis-phase-unwrapping` 专题；本文件不承载 Step 1 以后动作。
