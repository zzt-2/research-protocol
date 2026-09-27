# PROMPT-027：迭代预算控制方向的定向碰撞检索（九字段占位判定）

> 来源: S018§31 / D060 / R036 / D059 | 交付目标: 把创新点论证里所有 NOT_CHECKED 的"别人做过什么"变成实底
> 用户授权：全程自主，不中途提问；结论限检索证据；与 PROMPT-028 实验对话**并行**，互不写对方文件
> 工作树：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2（bash: /d/code/study/research-protocol/.worktrees/rdl-method-production-v2）
> 专题：.sessions/2026-08-30-thesis-advisor-text-outline/

请接手学位论文第二方法候选（**译码迭代预算控制：基于校验轨迹的双向判决规则——砍无望帧+续边际帧**）的定向碰撞检索。这个方向的创新点论证目前有一块 NOT_CHECKED（R036 对决策 risk 中明确登记：停机准则/变迭代族 × 衰落双峰 × 预算重分配的组合未见占位记录，但从未做过定向碰撞检索）。你的任务是把这块补成实底。

一、启动（按序读，不重新调研）

1. session-governance 报到（本专题 topic-index 当前控制段、D059、voice 2026-09-27 条目）。
2. 读 R036 §五（创新点三层论证）§六、R027 §三卡 1 第 7 条（重复检查的邻居清单与 NOT_CHECKED 标注）§七（10 篇全文缺口——只取与本任务相关者）、R035（早停六篇在库的证据位置）。
3. 编号：你的报告=R037 起；S018 追加 §31 起（与实验对话的 §32 分开，各写各的）；若产生占位判定决策可落 D061。git add 仅限你自己的文件。正常 commit。

二、任务：三个查询簇的定向检索 + 九字段碰撞判定

**查询簇 A（停机准则/变迭代族）**：LDPC/Turbo decoder stopping criteria、early termination、adaptive/variable iteration count decoding、iteration allocation。目的：确认"停机准则族做到哪了"——特别是**有没有双向规则**（不止早停省计算，还把省下的迭代预算重分配给差一口气的帧）。
**查询簇 B（衰落信道上的迭代分配）**：two-stage / re-decoding / frame-level iteration allocation in fading channels、reliability-based retransmission 替代（接收端内部，不含 HARQ 反馈）。目的：查"按帧难度分配迭代数"有没有人做过、在什么信道。
**查询簇 C（FSO/光 FEC 自适应）**：FSO/turbulence-aware FEC decoding、optical SD-FEC adaptive iteration、GG channel + LDPC/turbo。目的：场景占位检查——有没有人在 FSO 湍流语境做过迭代预算类方法。

**已知摘要级邻居，全文获取后逐篇九字段对照**（R027 卡 1/卡 4 遗留）：
- "早停 2026"（选择性 BICM-ID 变体，摘要级）
- GA-tuned OMS for BG2（2026）
- adaptive-NMS GCLDPC（2025）
- WCL 2022 自适应因子（AWGN 0.3-1.9dB）
- TVT 2019（R027 §七登记全文缺失）
- bootstrapped FSO 2023（EURASIP，WBF 族）
- 任务一新命中者（按同标准处理）

**九字段**：处理对象 / 动作规则 / 场景与信道 / 码型与帧结构 / 指标 / 对照设置 / 报告增益 / 与我们的差异 / 判定（**占位**=完全一样；**部分占位**=同机制不同场景或同场景不同机制；**不占位**）。

三、任务二：精读门（GW Step 3）

对判定**占位或部分占位**的文献（预计 ≤3 篇）做全文精读（项目精读模板），其余到摘要+方法节级即可。若簇内发现"双向预算重分配"已有人做且场景就是衰落/FSO——这是最高优先级发现，全文精读并单独成节。

四、交付 R037

开头直接给三行结论：
1. 创新点表述的合法性边界——哪些子句可以写"未见文献报道"（有检索证据支撑）、哪些必须写"近邻存在"（列邻居）；
2. 占位/部分占位文献总数与最危险的一篇（离我们最近的）；
3. 对 PROMPT-028 实验对话的建议（如对照臂需要加谁）。
正文：逐邻居九字段表 + 检索覆盖说明（查了什么、没查什么）+ slug 清单附录。

五、纪律与边界

- **不跑实验、零代码改动、零论文正文**。这是检索+精读对话。
- 检索走 `tools/search`（结果自动入 search-archive/），下载走 `tools/download`（papers/ 按规则建路径）；主对话严禁 WebSearch/webReader——web 查询必须在子 agent 内做并 ≤500 词摘要回传；对每篇功能/贡献断言用 Semantic Scholar API 或 DOI 交叉验证（规范见 AGENTS.md）。
- 单子 agent ≤15 分钟；一次 ≤3 个并发。
- 不把"库里没有"写成"世界上没有"；结论全部挂 slug/DOI 指针。
- 完成即收口：不进入方法生产、不写正文、不修改实验对话的任何文件。
