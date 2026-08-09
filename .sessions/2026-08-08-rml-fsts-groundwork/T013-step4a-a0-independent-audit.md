# Task Brief: RML-FSTS Step 4a A0 §0–§6 独立科学审计

> 来源: S004 | 产出位置: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md`
> 日期: 2026-08-09
> 唯一文档: 执行方先读本 T 与指定 owners，不读取其他 agent 产出，保持独立

---

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
**你的任务**：fresh-context、只读完成 Q1 A0 §0–§6 的独立科学审计，判断 semantic smoke 是否具备合法问题、baseline、物理参数与最快证伪路径；不提前看 T011/T012 产出。
**产出**：只写 `projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md`；不改 owner/code，不运行实验。

**最高纪律**：
1. Q1 只是假设：不得把 source condition dependence 偷换成 target crossover。
2. B2 conditioned single-lag lookup 是最强廉价 comparator；不能只比较 B0/B1。
3. Go 对手是合法传统 comparator；O1/oracle 只作 headroom/Kill，不能据 oracle headroom 宣 Go。
4. SSRN 6293357 是高风险全文债，不是 blanket blocker；禁止首次/novelty closure。
5. `consistency PASS` 不等于算法/科学正确；不设计 controller，不制造 METHOD_SIGNAL。
6. 总耗时不超过 15 分钟。

## 1. 必读 owners

- `.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md`
- `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md` D008–D009
- `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md` V005
- `projects/thesis-fso/literature_notes_rml_fsts.md`
- `projects/thesis-fso/master-state.md` 当前 RML-FSTS 控制桥
- `stages/gw-feasibility.md`
- `thesis-lessons.md` TL-20、TL-22、TL-26–TL-33

## 2. 冻结 Q1 与门限

- M：Wang/Enhanced fixed-lag/fixed-`B_L` FSTS。
- C：PM-4/16QAM、320-symbol FSTS、receiver power/SNR、弱/强湍流等有依据条件。
- A：fixed action 的最优值/排序可能随 receiver-visible condition 变化，产生 CFO-MSE/outage regret。
- smoke gate：B2 后 `>=20% normalized CFO-MSE regret` 或 `>=10 pp outage regret`，跨多个条件/seeds 稳定、非调谐/公平性/单异常解释。
- no crossover → Kill；B2 absorbs → Resolved；stable observable actionable residual → 才可 bounded MVE。

## 3. 必答 A0 §0–§6

按以下标题逐项回答，不套用与本 deterministic selector 无关的 ML/MDP 话术：

0. 合法问题与四判据：证据指针、FACT/INFERENCE/UNKNOWN。
1. 方法身份与动作空间：B0/B1/B2/O1/C1 的输入、动作、输出、对手角色。
2. deployable 信息边界：online known / receiver-estimated / oracle / post-hoc。
3. baseline ladder 与公平调谐：dev/test freeze、搜索预算、paired realizations、Go/Kill 对手分离。
4. 物理条件与参数 provenance：调制、TS、power/SNR、湍流、CFO/linewidth；已证/未证与外推限制。
5. testbed readiness：问题承载自由度、baseline failure/action alignment、named comparator、可执行 metric；READY/NEEDS_ADAPTER/BLOCKED。
6. 最快证伪路径与 terminal map：最小 cells/seeds/lag set、crossover/regret/observability 次序和立即停止点。

另附 A′/A/B 简表：竞争维度、结构优势是否只是查表、空白至少 3 个结构性原因与反驳；只决定是否允许 smoke，不宣称方法成立。

## 4. 产出格式（强制）

```markdown
# RML-FSTS A0 independent audit
## Verdict
ALLOW_SEMANTIC_SMOKE / A0_KILL / A0_PIVOT / BLOCKED
## §0 Legal problem
## §1 Method identity/action space
## §2 Deployable information boundary
## §3 Baseline ladder and fairness
## §4 Physical provenance
## §5 Testbed readiness
## §6 Fastest falsifier and terminal map
## A-prime / A / B
## Fatal signals
## Claim ceiling
## Evidence pointers
```

## 5. 验收

- [ ] §0–§6 全部逐项回答
- [ ] B2 与 O1 角色未混淆
- [ ] testbed readiness 不是“有脚本就 ready”
- [ ] 给出最快 falsifier 与 stop rules
- [ ] 无 controller/novelty/METHOD_SIGNAL 越权

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md`
