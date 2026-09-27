# PROMPT-028：迭代预算判决规则第一轮有界验证 + Pareto 补点（缓存上实验）

> 来源: S018§31 / D060 / R036 §五设计①② / D059 | 交付目标: 把迭代预算控制的"创新点论证"变成"结果"——规则无论量活量死都是导师会面材料
> 用户授权：全程自主，不中途提问；与 PROMPT-027 检索对话**并行**，互不写对方文件
> 工作树：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2（bash: /d/code/study/research-protocol/.worktrees/rdl-method-production-v2）
> 专题：.sessions/2026-08-30-thesis-advisor-text-outline/

请接手译码迭代预算控制方向的实验轮。背景：R036/D059 已量出——迭代轴 20→200 = −40/−97/−40 帧零负例；早停 FER 逐帧等价；NOMS+ES cap50 三条件同时优于冻结基线（FER/成本/BER）；**未量的只剩判决规则本身**：能否用接收可见的校验轨迹提前区分"真死帧"与"差时间的边际帧"，用 cap50 档的平均成本拿 cap200 档的 FER。你的任务是设计、冻结并验证这条规则的第一轮。

一、启动（按序读，不重新调研）

1. session-governance 报到；跑仿真前过 sim-preflight skill（场景 A+B）。
2. 读 topic-index 当前控制段、D059、R036（重点 §三§五）、R035（早停 headroom 与五臂设计）、`explore/decode-capability-audit/`（contract.yaml + README + run_audit.py 的臂结构）、`explore/decode-failure-rescue/rescue_decoder.py`（RescueDecoder/轨迹语义）、`results/decode-failure-rescue/raw_confirm*.json` 的 frames[].B0.syndrome_weights（20 迭代轨迹样例）。
3. 编号：实验报告=R038 起，独立复核=V043 起，决策=D062 起（D061 预留给检索对话），S018 追加 §32 起。git add 仅限自己文件。正常 commit。

二、硬约束（用户原话级，违反即停）

第二方法必须是 DSP 算法（估计/滤波/检测/译码家族的消息/估计/判决规则本身）——本轮实验不因此越权宣布"方法成立"，成章归用户/导师；星地相干场景不变；零论文正文、零旧 raw 改动、零冻结模块改动；全部新建独立模块（建议 `explore/decode-budget-rule/`），只读 import 既有模块；真值只进评分与开发集标签。

三、任务一（核心）：判决规则第一轮有界验证

**数据与特征（开发集）**：先在 llr_cache 的 dev 批（dev / dev_W12 / dev_S16 等，见 `results/decode-failure-rescue/llr_cache/`）上跑带**全轨迹日志**的 NOMS 译码（cap=200，逐迭代 syndrome 计数 + 最终信息输出）。特征原料=当前帧自己的校验轨迹（接收可见）；开发标签=同帧 NOMS200 结局（收敛于第几轮 / 永不收敛）。

**规则族（预注册候选，开发集上选择后冻结；允许在合同里写明选择准则）**：
- 特征候选：最近 k 轮 syndrome 均值 / 斜率 / 振荡计数 / 绝对水平 / 相对首轮降幅；
- 动作：三态——收敛即停（校验全过）/ 无望即砍（特征过阈值→中止，标失败）/ 否则续到 cap；
- 检查点候选：{20, 30, 50, 100}（到达检查点算一次特征与判决）；
- 目标读数：cap=200 下把平均迭代压到接近 cap50 档（16~19），FER 保持 cap200 档（−40/−97/−40 帧水平）。

**确认（确认集）**：规则冻结后在三确认批缓存（confirm2048 / confirm_W12 / confirm_S16，各 2048 帧）上单次运行。**防泄漏写进合同**：规则设计与阈值选择只用 dev；确认集只跑一次只评分。

**主读数**：FER vs 平均迭代 的 Pareto——规则点 vs 固定点族（B0 固定20 / B0+ES / NOMS+ES cap50 / cap200 已实测可复用，R3 救援线三确认批数字直接引用）+ 本轮新跑点。配对统计沿 decode-capability-audit 口径（帧级 bootstrap CI95 + 符号检验）。

**预注册判读（先冻结后运行）**：
- ALIVE：规则点相对同 cap 固定点有 CI 下界>0 的平均迭代节省且 FER 损失 ≤0.2pp；或同 FER 下成本显著低于 cap50 点。
- KILL：任一条件 FER 损失 >0.2pp，或成本节省 CI 含 0——规则 Kill，如实落账（这也是有效产出：导师会面材料里的"此路不通"实测证据）。
- 预算：≤2 轮设计—运行—诊断；失败不调参追正；oracle 只作 Kill 工具。

四、任务二（便宜补点，条件于余量）

固定迭代 {10, 15}（Pareto 左半支，同缓存同配对）；可选 cap=100 中点。若任务一占满预算则任务二降级为建议。

五、交付

R038：开头直接给——规则 ALIVE/KILL、若活给出 Pareto 坐标（规则点 vs 全部固定点）、若死给出死因与保留资产。收尾：独立 agent 复核 → V043；治理更新（S018§32、D062+、topic-index、voice、registry）；统一 commit。

六、边界

结论限所跑合同（三确认批+dev 缓存、BG2 z=104、exact-APP LLR、浮点仿真）；不写正文；不自动进入方法生产；不碰 PROMPT-027 检索对话的文件；定点化/硬件验证属 Ch5 计划，不在本轮。
