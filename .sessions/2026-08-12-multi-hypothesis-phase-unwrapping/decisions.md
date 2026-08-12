# Decisions — 有界多假设固定滞后相位解缠 Groundwork

## D001: 创建唯一 K2 Groundwork 专题，只授权 Step 1

> status: active
> date: 2026-08-12
> 取代：无
> 被取代：无
> 依据：上游 2026-08-08-ch4-reference-method-extension D007 / R004
> 触发原话: [转述]“稍微大一些也可以”

### 决策

建立本专题，唯一研究对象为 Wang TSP 2022 phase-unwrapping suffix pollution 在 coherent FSO residual CFO + laser Wiener PN 下的任务适配低复杂度扩展。只执行 Groundwork Step 1；TCOM 2016 full mixture 与 fixed order2/3 作为 mandatory comparator，预计单方向公平比较 5–9 天可接受但尚未授权。

### 理由

上游 A adjudication 六项硬门均通过且未确认 exact action collision。旧 D006 的 entry rejection 是旧门槛/旧预算下的历史结论，已由 D007 改变 current scope；本专题从 Step 1 正常积累证据，不继承方法结论。

### 排除的替代方案

- 不比较其他候选，不复活 Q001/K1/K3/K4。
- 不跳过 Step 2/3/3.5/4a 运行 MVE。
- 不把动作原子或设计形态写成方法。

### 影响范围

只创建 Step 1 文档、检索 JSON、project progress owner 和 master/registry current view。

### 来源

上游 D007/R004；registry duplicate check；Groundwork Step 1 规范。

## D002: Step 1 通过，等待 Step 2 confirmation

> status: active
> date: 2026-08-12
> 取代：无
> 被取代：无
> 依据：调研: R001–R003 + 验证: V001（初审 PARTIAL，修复后 final fresh PASS）
> 触发原话: 无（技术裁决）

### 决策

terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。11 query / 2 rounds 的三路线 corpus 通过数量、来源、formal、must-read 和语义初筛门；没有一手证据确认 D1/D2 完整动作 exact collision。V001 初审 PARTIAL 的 formal 归并、编号和预声明问题已修，final fresh verifier=`PASS 0/0/0`；Step 2 仍 `NOT_AUTHORIZED`。

### 理由

TCOM 2016 是 full-general capability superset，必须比较但完整 I→D→A→O 与 K2 不同。最新 optical/FSO CPR 和 slip mitigation 仍有全文动作债，适合进入 acquisition，而非在 Step 1 凭摘要判新颖或预杀。

### 排除的替代方案

- 不把 Step 1 PASS 写成 Q#、Go、方法、METHOD_SIGNAL 或论文贡献。
- 不因 abstract 缺少 fixed-lag/trigger 关键词声称 non-collision。
- 不在主控确认前下载或全文精读。

### 影响范围

更新 topic/master/registry 与 H001；下一合法动作只有 Step 2 confirmation。

### 来源

R001–R003；V001。

## D003: 接受 Step 1 coverage，只授权 Groundwork Step 2 acquisition

> status: active
> date: 2026-08-12
> 取代：D002 的 `Step 2 NOT_AUTHORIZED` operational gate
> 被取代：D004 的 `Step 3 NOT_AUTHORIZED` operational gate
> 依据：验证: V001 + 调研: R001–R003 + 主控明确授权
> 触发原话: [转述]“本轮只做Step2，完成后停，不进Step3。”

### 决策

接受 commit `215a200` 的 Step 1 coverage，当前范围从 Step 1 confirmation gate 扩为只执行 Groundwork Step 2 acquisition。目标是取得能决定 D1/D2 collision 与 baseline 合法性的高价值全文，而不是用跨任务 RF/coded/general phase-tracking 论文凑五篇。Step 3 继续 `NOT_AUTHORIZED`。

### 理由

H001 接收核验确认 Step 1 corpus、mandatory comparator 边界与 registry 血缘一致。当前承重不确定性来自 P0/P1 论文的全文可得性和身份/内容质量，而不是需要新搜索或算法设计；按 gw-acquire 先复用 canonical、再走最多三条合法获取路径，可以在不提前精读动作的条件下闭合 coverage。

### 排除的替代方案

- 不把 metadata/abstract 当全文，不在 Step 2 判 exact collision、Q#、Go 或方法。
- 不下载后顺手进入 Step 3，不实现、不仿真。
- 不复制共享根 canonical 制造双 owner；只做合法引用或最小 adapter。
- 不用 RF/coded/general tracker 替代 coherent optical/FSO task baseline。

### 影响范围

新增 S002/R004/machine receipt/V002/H002，更新 topic/master/registry/voice；只在 canonical paper 路径合法写入获取结果。完成后停在 coverage confirmation terminal。

### 来源

主控 delegation；S002 handoff reception；V001/R001–R003。

## D004: 接受 Step 2 coverage，只授权 Groundwork Step 3 全文精读

> status: active
> date: 2026-08-12
> 取代：D003 的 `Step 3 NOT_AUTHORIZED` operational gate
> 被取代：D005 的 Step 3 terminal 与后续 gate
> 依据：H002/R004/V002/machine receipt + 主控明确授权
> 触发原话: [转述]“本轮只做Step3，完成后停；不得进Step3.5/4a、实现或仿真。”

### 决策

接受 commit `5a1ef98` 的 Step 2 coverage，当前范围扩为只执行 Groundwork Step 3：对 9 篇 qualified 全文完成结构化精读，闭合 exact action/complexity contract，并按 glossary 四判据形成或否决 canonical Q001。Step 3.5、Step 4a、实现和仿真继续 `NOT_AUTHORIZED`。

### 理由

H002 接收核验确认 12 篇审计中 9 篇 qualified、8 篇 CORE，A/B/C 三路线及 P0 reference/full-mixture 已闭合；当前承重问题从“是否有全文”转为“全文动作、复杂度和任务边界如何”。按 gw-read 由 fresh 子 agent 精读、主线程统一综合，可以在不提前实验的条件下裁 TCOM 2016 与 D1/D2 的边界。

### 排除的替代方案

- 不凭摘要、标题或旧聊天记忆裁 exact collision。
- 不把 Step 3 的可证伪问题判断写成 Step 4a 的实验证据。
- 不设计算法、跑 smoke、实现或进入 Step 3.5。

### 影响范围

新增 S003、Step 3 research/read-note/read-log、V003、H003，并同步 topic/master/registry/voice；不修改旧 Q001/coded/p05 或 unrelated dirty 文件。

### 来源

主控 delegation；H002/R004/V002；gw-read/glossary/templates。

## D005: Step 3 只保留 D1-shaped Q001，D2 降为可选组件

> status: active
> date: 2026-08-12
> 取代：D004 的 Step 3 in-progress operational state
> 被取代：无
> 依据：R005 + 9 篇 fulltext read + V003 PASS
> 触发原话: 无（技术裁决）

### 决策

terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`。保留唯一 Q001：decoder-free single-tone 下的 bounded discrete-wrap hypotheses 与 fixed-lag commit；D2 reliability-triggered expansion 不作为第二 Q，只可在后续成为 Q001 的可选 average-cost component/ablation。

### 理由

Q001 glossary 四判据 4/4。TCOM 2016 在 primitive capability 上是 full-general superset，但完整 input/state/schedule/output/resource contract 与 Q001 不同；C09/C10/C11/C12 已分块吸收 D2 的 trigger/adaptation/fade robustness/slip-suppression 动机，强保 D2 会退化为包装。

### 排除的替代方案

- 不把 H=3、fixed lag、confidence、merge/prune 任一原子声称为新颖。
- 不把 Step 3 literature support 写成 FSO defect occurrence、Go 或方法成立。
- 不跳过 Step 3.5 进入 Step 4a/实现/仿真。

### 影响范围

更新 owner/R005/topic/master/registry 与 handoff。下一合法动作仅 Step 3.5 exact-action/claim closure，需新授权。

### 来源

R005；canonical read notes；gw-read/glossary。
