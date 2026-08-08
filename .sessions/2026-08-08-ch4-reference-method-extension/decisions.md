# Decisions — Ch4 参考方法扩展

## D001: 冻结 reference-method extension 方法生产合同

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：critic: S001 三路独立过程/包装/范围审查综合 + 用户原话: `voice.md` 2026-08-08

### 决策

Ch4 不再从内部 supporting leftovers 继续包装，也不立即全领域 pivot；改为在星地相干 FSO 总伞下，从可复现 reference baseline、observed defect、one deployable action 与 fair comparator 出发生产完整方法包。入口门通过的单一胜者可获 3–7 天最小 testbed 预算。

### 理由

CCISP 的可写性来自“真实缺陷—可部署动作—现成 testbed—公平比较”的完整链，而近期流程把大量工作消耗在方法构造前的治理、假想廉价替代与基础设施 hard kill。reference-method extension 保留科学诚信门，但把最重的检索、统计与工程闭包后移到已选中的单一对象上。

### 排除的替代方案

- 不把 P1 shared-M0 reuse 恢复为 Ch4 独立方法；已有 generic shared-compute prior art，最多作 Ch5 内部优化。
- 不建设 decoder-feedback coded-chain 基础设施；当前 extrinsic/syndrome/callback 均未就绪。
- 不继续对 `SUPPORTING_ONLY` / `REJECT` 资产做 authority/package closure。
- 不立即离开 coherent FSO；先改变同领域内的 research object。
- 不把廉价替代当概念期想象性否决，除非存在 exact existing-action collision 证据。

### 影响范围

旧 `2026-07-20-research-direction-lab-system` 专题转 dormant，不再新增 S### 或承载科学执行。新专题下一步只做最多 3 个 research object / reference baseline 的入口选择。每对象最多 2 个 method-bearing package；两个对象失败后必须回用户做战略决策。`SUPPORTING_ONLY` / `REJECT` 继续不关闭 Ch4。

### 来源

S001；用户纠正与批准；三路 subagent 发散及交叉复核。

## D002: 本地 reference-method 入口无 survivor，交回战略决定

> status: superseded
> date: 2026-08-08
> 取代：无
> 被取代：D003
> 依据：调研: R001 + critic: 两路 fresh-context 本地审计 + 验证: V002（fresh-context verifier 初审 REJECT、修正稿 ACCEPT）
> 触发原话: 无（技术推导）

### 决策

terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。Paillier FG-DRC 与旧 K01 exact 相同且旧 D027 已接受为 `REJECT`；LBS-RDE 的星地 FSO defect 未建立。当前没有对象通过全部 7 门，不推荐入口，不进入 Groundwork。

### 理由

Paillier 论文只支持 fade 下失稳门限恶化，不支持承重的 post-fade NCO/state damage；现有 runner 也不是 time-correlated fade-exit testbed。更关键的是，本轮拟议方法名、动作、主图、消融与 comparator 均 exact collision 于旧 K01，而旧 D027 明确禁止降门晋级。LBS-RDE 则只有 fiber PMD/SOP defect，不能继承为星地 FSO 事实。

### 排除的替代方案

- 不选 Paillier FG-DRC：它是 exact K01 rejected package 复活；当前没有新 evidence 或授权推翻旧 D027。
- 不选 LBS-RDE pilot-density switching：reference 与重建预算可接受，但星地 FSO defect 为 UNKNOWN，论文原 likelihood gate 不能冒充新增动作。
- 不续 Pilot-Jones：fixed EMA 已吸收 gap，且对象包预算已超限。
- 不续 block-CMA/per-symbol Godard：新增动作 exact collision 于传统 comparator，旧对象包预算已超限。
- 不恢复 T001 明示禁止的 P1、decoder-feedback、CCISP 标量调参、C3、oversampled Q1、coded-burst 4b#1、AMC Q-A/Q-B、G1/P09。

### 影响范围

本轮只更新 R001、D002、V002、topic-index、registry current view 与 H002。D002 不创建 Q#、Go、METHOD_SIGNAL 或 thesis-ready 裁决；不授权检索、实现、仿真或 Groundwork。下一步必须由用户作战略范围决定。

### 来源

S001 / T001 / R001；两路 fresh-context 本地证据审计与 fresh-context verifier 对初稿的独立否决、修正后复核。

## D003: 入口审计不计对象失败，改设 defect-reproduction gate

> status: active
> date: 2026-08-08
> 取代：D002 的“战略耗尽 / 两对象失败”强度；保留 R001 的候选事实与 exact-collision 裁决
> 被取代：无
> 依据：critic: S001 对 T001 G3 与停止计数的规则审查 + 调研: R001 + 验证: V002
> 触发原话: 无（用户以零信息“行”批准纠偏，按 voice 规范不收录）

### 决策

terminal 修订为 `LOCAL_ENTRY_POOL_EXHAUSTED_DEFECT_REPRODUCTION_GATE_REQUIRED`。R001 只证明本地入口池没有可直接晋级的对象：C1/Paillier 仍因 exact K01 collision 保持 `REJECT`，C2/LBS-RDE 仍为 FSO defect `UNKNOWN`；它没有证明两个 research object 已完成 method-bearing package 并失败，也不足以触发全局战略耗尽。

下一轮允许一次有界 candidate-source expansion：比较 2–4 个机制不同的外部 reference baseline，最多推荐 1 个 `READY_FOR_GW_STEP1_DEFECT_REPRODUCTION`。入口候选只需具备“外部已发表 defect + 向目标 FSO 条件迁移的物理机制 + 0.5–1 天可证伪 smoke 合同”，不要求目标 FSO defect 在入口期预先成立。

### 理由

T001 的 G3 一方面允许“低成本、可证伪的 defect reproduction”，另一方面禁止实验，却在入口裁决时要求 defect 已在目标场景成立；这一组合会系统性排除所有尚未做 smoke 的跨场景 reference extension。与此同时，D001 的“两对象失败”原意是两个机制不同对象真正完成 method-bearing package 后仍无增量，不是两个 entry-screening 候选没通过七门。把入口审计计入停止条件，会在方法构造之前重新运行成否决机器。

### 排除的替代方案

- 不恢复 C1/Paillier/K01：其方法动作、主图、消融与 comparator 是已证实 exact collision，仍受旧 `REJECT` 约束。
- 不把 C2 的 fiber defect 直接写成星地 FSO defect：它只能作为未来候选源证据，必须另有迁移机制和 smoke 合同。
- 不因邻域 prior art 自动封禁整个机制族：只有 exact object/action collision 才能入口期拒绝；邻近 prior art 只限制未来 claim。
- 不在本轮执行 smoke、实现、仿真或 Groundwork；T002 只选入口。下一轮必须按 `stages/groundwork.md` 从 GW Step 1 开始，只有走完 Step 1–3 并进入 Step 4a 后才可执行预注册 smoke。
- 不继续从当前两项本地 leftovers 补第三个名字；候选必须来自扩展后的外部 reference source。

### 影响范围

更新本专题 topic-index、S001、H002 supersession banner、registry current view，并新增自包含 T002。每对象 2 包 / 两对象停止计数从正式 method-bearing package 或已授权 defect-smoke 执行开始；T001/T002 入口筛选均不计数。T002 预留 R002、D004、V003、H003 作为执行产出编号。

### 来源

S001 规则纠偏；R001/V002 事实边界；用户批准继续。

## D004: 选择 RML-FSTS 作为唯一 defect-reproduction Groundwork 入口

> status: active
> date: 2026-08-08
> 取代：无（执行 D003 授权的有界入口裁决，不改写 D003）
> 被取代：无
> 依据：调研: R002 + critic: 两个 fresh-context science agent 的 source/physics/collision 审查 + 验证: V003（初审 PARTIAL，修复后 PASS，P0/P1/P2=0/0/0）
> 触发原话: 无（技术推导）

### 决策

terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`。唯一选择 C1 RML-FSTS research object：以 Wang et al. 2023 FSTS fixed lag/`BL` 的条件依赖与低功率退化为 source-domain defect，下一对话从 Groundwork Step 1 启动 defect-reproduction；C2 BUM-CMA 因 source-domain weak-branch gradient defect `UNVERIFIED` 不入场。

该入口不是 Q#、Go、METHOD_SIGNAL、defect 成立、方法成立或章节完成；本轮 `mission_method_delta=NONE`，object/package failure 计数保持 `0/0`。

### 理由

C1 有具体 2023 主流 reference、本地全文精读证据、可证伪的 FSO transfer hypothesis、0.5–1 天 defect-only smoke 合同、一个 receiver-visible future-action identity、无 exact historical collision、可辨认的章节路径和 3–7 天条件预算。smoke 的最强廉价替代冻结为 modulation/TS length/receiver-power-conditioned single-lag lookup；只有该 lookup 在同一可见条件内仍留下超 MDE regret 才可 PASS。C2 虽有 2023 JLT baseline 与多孔径 FSO 迁移路径，但论文没有证明“弱分支污染固定步长 CMA gradient”，且当前无 0.5–1 天 faithful testbed；不能用推断填补 E2/E4。

### 排除的替代方案

- 不选 C2 BUM-CMA：E2/E4/E7/E8 失败；P05/C15 的 confidence/fade gating 还形成高邻近度，未来 claim 区分度不足。
- 不恢复 Paillier/K01、B10 pilot-RLS、B3-Q2 Doppler-rate、C3/P09 adaptive CPR window 或合同所列其他 exact object。
- 不把 multi-lag CFO 的邻域 prior art 当整族禁令；它只把未来 claim 限定为 FSTS 特定、湍流/低功率条件下的 receiver-visible reliability fusion。
- 不在本轮运行 smoke 或测试未来 RML-FSTS action；预注册 smoke 只复现 fixed-lag defect，且须在下一对话完成 GW Step 1–3 后才能进入 Step 4a。
- 不用较弱的 global fixed lag 制造 headroom：known modulation、TS length 与 receiver-visible received-power 必须进入 dev-frozen conditioned single-lag cheap comparator；它若在 MDE 内解决问题，则 future multi-lag action 不得晋级。

### 影响范围

新增 R002 与 H003，追加 V003，更新 S001、topic-index 与 registry current view。D001–D003、R001/V002/H002 历史保留；四个 `p05_run*.log`、科学代码、Skill、旧 dormant topic 与正式论文不变。

### 来源

S001 / T002 / R002；两个 fresh-context science agent 的独立 source 与机制审查。
