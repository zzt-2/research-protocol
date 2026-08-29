# Task Brief: C5-5 reliability-driven LDPC budget 冻结两篇全文 Step 3 精读

> 来源: S028 / D059 / V034 / T079 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step3-fulltext-read.md`、两篇 read notes、`projects/thesis-fso/read-log.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 21
  action_class: C5_5_GW_STEP3_FROZEN_FULLTEXT_READ
  mission_checkpoint: CP021
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行候选 `Q-C5-5`“基于码字可靠性的 LDPC 迭代预算分配”的候选级 GW Step 3。完整精读 T079 冻结的两篇 qualified fulltexts，辨清 reliability-driven dynamic scheduling、ordinary CRC/syndrome early stop、maximum-iteration budget 与 `Q-C5-5` 的实际输入—动作—输出关系；最终只裁决候选是否仍有一个可进入 Step 3.5 的 canonical Q#。

本任务不搜索、不下载、不实现、不仿真、不修改 decoder 接口，也不进入 Step 3.5。P0 DOI `10.1109/ACCESS.2019.2899106` 仍是未取得全文的已知债务，禁止用错配 arXiv 或标题摘要补结论。

## 冻结全文池与顺序

1. `papers/doi/10.1587_transfun.2024eal2080/content.md` — Liu et al., *Reliability-List-Based Check-Belief Propagation Decoding of LDPC Codes*, IEICE Transactions on Fundamentals, 2025。
2. `papers/doi/10.1109_wcsp52459.2021.9613326/content.md` — He et al., *Lowering the Error Floor of Quantized NR LDPC Decoders by a Post-Processing on Trapping Sets*, WCSP 2021。

不得新增第三篇，不得读取 rejected P0 的错误内容，不得用搜索 archive 的标题/摘要代替全文。He 2021 的 legacy `source.pdf` 实为纯文本这一 source-format debt 必须保留，但其 canonical `content.md` 可用于本次精读。

## 开始前强制读取

1. 根 `AGENTS.md`、本 brief、topic-index CP021、D059/V034、T078 Step 1 报告、T079 coverage report 与 worker log。
2. `stages/groundwork.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md`、`templates.md` 的 literature-notes 模板与 `thesis-lessons.md` TL-31–33；运行 task-control validator。
3. 冻结两篇的 metadata、content 与既有 read note/read-log；既有 He 2021 read note 只能复用事实，不能替代 C5-5 视角的全文核对。

## 执行纪律

1. 论文全文精读必须按项目规则分派给内部只读 subagents：建议两个 subagent 各读一篇，返回结构化摘要；主任务负责统一 schema、逐项交叉核验、综合 Q# 与最终 terminal。subagent 不得检索、下载、写文件、运行实验或派生新方向。
2. 每篇先做 title/identity 自检。按 `gw-read` 提取标准 14+ 字段、源文件路径、具体公式/算法位置、实现数值、baseline 与实验完备性；传统通信论文不适用的 DRL 状态/奖励/网络字段写 `N/A（原因）`，不得省略。结构化 7 子表中的状态、动作、建模假设、适配性、问题 M-C-A 与四判据必须完整；奖励/网络等不适用项明确 N/A。
3. 对每篇至少提取：runtime input/state 是否 receiver-visible、动作粒度、schedule/list update、stop/budget rule、最大迭代数、baseline、同等 edge-update/迭代成本口径、sorting/list/post-processing overhead、decoder 输出、统计设置和 claim scope。
4. 新建 Liu 2025 read note，并按需补充 He 2021 既有 read note 的 C5-5 专属段；向 `projects/thesis-fso/read-log.md` 增补或更新对应记录。不得改写与本候选无关的旧精读结论。

## 必答科学问题

1. Liu 2025 的 reliability/check-belief 是译码器内部消息、外部 channel/pilot reliability，还是二者组合？其动作发生在 edge/check-node 更新顺序、每轮 list、总迭代预算还是码字间预算分配？与“译码前按码字可靠性分入少量 `num_iter` 档位”是 primitive overlap、strong neighbor，还是九字段完整动作碰撞？
2. He 2021 的 CRC/syndrome early stop 在第几阶段、何时检查、最大迭代数如何设置、post-processing 何时触发？普通 early stop 是否已经在同一 receiver-visible 信息与相同 decoder 下，实现了 `Q-C5-5` 想要的成本—性能自适应，还是只在码字成功后停止、无法预先给困难码字更多预算？
3. `Q-C5-5` 的最小 IAO 是否仍可诚实写成：当前码字的外部 channel/pilot reliability → 少量冻结预算档位 → 同一 fixed NMS/OMS 的 per-call `num_iter` → decoded bits、BER/FER 与真实平均/P95 edge-update 成本？其中任何字段若必须依赖 decoder-internal truth/state，应明确判非法或改写边界，不能脑补 adapter。
4. 公平 comparator ladder 至少如何包含：tuned fixed NMS/OMS、ordinary syndrome/CRC early stop、equal-total-update extra-iteration、standard flooding/layered、frozen reliability-bin→iteration LUT？两篇全文实际支持哪些，哪些只能保留为后续合同而非文献事实？
5. P0 2019 全文缺失是否使 Step 3 无法裁决，还是 2025 direct substitute 足以判断 candidate-level Q#、只把“完全重复未发现”的 claim ceiling 压低？必须把“证据不足”和“动作被吸收”分开。

## 九字段碰撞表（逐篇必填）

对每篇与 `Q-C5-5` 逐项填写 `same / different / unknown` 并给全文位置：

1. target code/decoder；
2. operating context / target scene；
3. receiver-visible input；
4. state statistic；
5. action；
6. action granularity / timing；
7. update/stop/budget rule；
8. output and objective；
9. cost/fairness contract。

只有九字段承重链整体相同才可判完整动作碰撞；词面或单个 primitive 重合只能记 strong neighbor/primitive overlap。反过来，场景不同也不能掩盖同一动作在同一接口上被廉价 early-stop 完整吸收。

## Q# 与 claim ceiling

- 若存活，只允许一个 canonical `Q-C5-5`，必须给 M-C-A 四判据、receiver-visible IAO、最小预算档位动作、baseline/cheap alternative、可证伪目标、复杂度指标、外部证据债务与最多“目标场景中的经典接收机预算迁移/扩展”claim。
- 不得声称首次、SOTA、全部近期方法未做过、全面领先或已经有 BER/FER 收益。
- 强邻居不自动否决硕士级方法；但同接口的 ordinary early-stop 若完全吸收承重增益，必须判 `ABSORBED_CLOSE`，不得把隐瞒已知反证当成 claim 策略。

## 冻结终态

1. `STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5`：两篇全文下仍形成四判据成立、IAO 明确、未被 ordinary early-stop/dynamic scheduling 完整吸收的唯一 Q#；只表示可由主控另开 Step 3.5。
2. `STEP3_C5_5_ABSORBED_CLOSE`：已有动作在同一接口/信息/成本口径下完整占据，或 ordinary early-stop 已吸收预算分配的承重机制；关闭 C5-5，不实现试试看。
3. `STEP3_C5_5_EVIDENCE_INSUFFICIENT`：P0 缺失或两篇全文不足以诚实裁决关键动作；列唯一 blocker，回主控决定关闭或另行限界，不得扩搜、实现或仿真补证据。

## 交付与验证

1. 主报告：`projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step3-fulltext-read.md`；逐篇 read notes、read-log 增量与 `projects/thesis-fso/worker-logs/step-080-c5-5-gw3-frozen-fulltext-read.md`。
2. 报告 facts-first，含 2/2 identity/read receipt、逐篇标准条目、实验完备性、九字段碰撞表、cross-paper synthesis、ordinary early-stop absorption verdict、唯一 Q# 或 blocker、terminal、claim ceiling 和唯一下一步。
3. 由一个未参与单篇提取的内部 reviewer 做独立内容审查，重点核对全文位置、input/action/granularity、early-stop 与 exact-collision 结论；内容正确性审查不能退化为路径/格式 consistency。
4. 运行 task-control validator、确定性 identity/path 检查、报告术语 grep 与 `git diff --check`。不运行仿真、实验、测试网格或下载命令。
5. 墙钟 60 分钟；前 15 分钟必须完成分工和至少一篇结构化抽取，45 分钟时强制收敛到三选一 terminal。一次 commit、不 push；最终回报 commit、2/2 read count、Q#、early-stop verdict、terminal、claim ceiling 与 blocker。
