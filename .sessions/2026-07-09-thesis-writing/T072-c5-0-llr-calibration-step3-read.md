# Task Brief: C5-0 LLR calibration 冻结六篇全文 Step 3 精读

> 来源: S028 / D051 / T070 / V026 | 产出位置: `projects/thesis-fso/literature_notes_apsk_llr_calibration.md`、六篇 read notes、`projects/thesis-fso/read-log.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 13
  action_class: GW_STEP3_READ_C5_LLR_CALIBRATION
  mission_checkpoint: CP013
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行候选 C5-0“均衡/相位恢复后残差可靠性感知 LLR 校准”的 GW Step 3。完整精读 T070 冻结的六篇 qualified fulltexts，辨清哪些原子可由接收端 pilots/known symbols 在线执行、哪些依赖真实 SNR/bit truth/offline GMI；最终至多形成一个 canonical Q#。不继续搜索，不下载，不做 Step 3.5、实现或仿真。

## 冻结全文池与顺序

1. QF2 `papers/arxiv/1111.7265v1/content.md` — Szczecinski，mismatched L-values 的线性校准。
2. QF3 `papers/arxiv/1709.10393/content.md` — Alvarado et al.，known-symbol residual、auxiliary channel 与 GMI。
3. QF4 `papers/arxiv/1911.01585v3/content.md` — Yoshida et al.，pilot SNR、mismatch 与 post-FEC/GMI 边界。
4. QF1 `papers/arxiv/0805.1327/content.md` — Martinez et al.，mismatched BICM 的理论 baseline。
5. QF5 `papers/doi/10.1186_s13638-018-1136-z/source.md`，并以同目录 canonical `source.pdf` 核对 — Layton et al.，APSK/data-dependent noise demapper。
6. QF6 `papers/doi/10.1109_vetecs.2009.5073425/content.md` — Xie et al.，APSK one-shot/iterative demapping；source-format caveat 保留。

不得新增第七篇，不得用标题/摘要替代全文，也不得因已有 read note 就跳过本候选视角的全文核对。

## 执行纪律

1. 先读根 `AGENTS.md`、本 brief、D051/V026、T070 report，以及 `stages/groundwork.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md` 和 `thesis-lessons.md` TL-31–33；运行 task-control validator。前置恢复控制在总预算约 10%。
2. 论文全文精读必须按项目规则分派给内部只读 subagents，建议 3 个 subagent 各读 2 篇；主任务负责统一 schema、交叉综合与最终 Q# 判断。subagent 不得检索、下载、写文件、派生新方向或运行实验。
3. 每篇先核对 title/identity；按 gw-read 模板提取至少：具体公式与式号、动作所需 runtime input、是否含 bit truth/true SNR/offline distribution、输出、baseline、metric、适用 decoder、复杂度、与 C5-0 的关系（exact recipe / executable primitive / strong neighbor / background）。传统通信论文不适用的 DRL 字段明确写 `N/A（原因）`，不得省略。
4. 为六篇生成或更新 `papers/_read_notes/{paper_id}.md`，向 `projects/thesis-fso/read-log.md` 追加六条；综合报告 facts-first，保留来源路径与公式位置，不用二手摘要作承重证据。

## 必答科学问题

1. 正确 B0 是否始终是同一 max-log/APP demapper、同一估计/假设 auxiliary-channel 参数、未经校准的 mismatched LLR（`s=1/alpha=1`）；匹配 likelihood/真实噪声是否明确单列 `B_match/O1`？
2. receiver-visible reliability 能否由 post-Ch4→Ch3 后的已知 pilots/residual 构成；在线估计量、因果窗口、帧级更新时间和最小样本数分别是什么？不得把 Yoshida 含真实 SNR 的关系直接改写为 deployable pilot 公式。
3. 校准动作到底作用于 channel/extrinsic LLR、a-priori LLR 还是两者；进入冻结 LDPC decoder 前的输入—动作—输出链是什么？正比例缩放对 uncoded hard decision 不变，收益必须落在 soft decoder/GMI/FER/BER 链上。
4. 自由度应是 global、per-frame、per-ring、per-bit-channel 还是其有界组合？先列最简单全局 scalar；任何额外自由度都必须有 receiver-visible statistic 支撑，不能只为制造增益。
5. Layton 的 per-point covariance/centroid 是否是高维强邻居而非 scalar exact recipe；Xie 的 iterative demapper 是否改变 one-shot baseline 身份；offline GMI-optimal scalar 与 online pilot-derived scalar 的差距如何诚实表述？
6. 在共同平台 `Ch4 demux → Ch3 per-tributary CPR → APSK demap/LDPC` 中，能否写出唯一 M-C-A：现有 B0 在什么 residual/reliability mismatch 条件 C 下因何机制 A 使软信息失配；候选动作如何只用接收端可见量缓解它？

## Comparator 与 Q# 合同

- comparator ladder 至少包含：B0 未校准 mismatched LLR；`B_match/O1` 匹配 reference；全局 scalar cheap alternative；只有全文支持且信息/样本预算公平时才列 per-ring/per-bit 或 Layton 高维邻居。
- 强邻居与经典原子只限制 claim ceiling，不自动否决硕士级场景迁移。不得声称首次、SOTA、新估计理论或全面领先。
- canonical Q# 必须同时给：M-C-A 四判据；receiver-visible input→action→output；baseline 与 cheap alternative；可证伪的目标场景；预期主指标与最低必要消融；外部证据边界。若无法满足，只写明确 blocker，不拼接多个不完整候选。

## 冻结终态

1. `STEP3_Q_SURVIVES_READY_FOR_STEP3_5`：形成一个满足四判据、receiver-visible IAO 明确、baseline 身份正确的 Q#；仅表示可另开 Step 3.5。
2. `STEP3_CLASSICAL_MIGRATION_READY_FOR_STEP3_5`：动作主要为经典 scalar/estimator 迁移，但目标场景 recipe 与证据边界仍清楚；同样只允许主控评估是否开 bounded Step 3.5。
3. `STEP3_NO_LEGAL_Q`：在线输入不可闭合、问题不存在/不可测，或只能依赖 truth/offline 标定而无法形成诚实 receiver action。停止，不补第七篇、不实现试试看。
4. exact recipe collision 不在本任务用扩检索裁决；若全文池内已出现明显完整重复，记录为 Step 3.5 的高风险入口，不擅自搜索闭包。

## 交付与验证

1. 交付综合 literature notes、六篇 read notes、read-log 追加和必要的 worker/read receipt；报告含六篇逐文表、跨文综合、唯一 Q# 或 blocker、terminal 与唯一下一步。
2. 由一个未参与单篇提取的内部 reviewer 对公式—输入—动作—baseline 映射做独立内容审查；这是内容正确性审查，不是检索或新方向探索。
3. 运行 task-control validator、确定性路径/identity 检查和 `git diff --check`。不运行任何仿真、实验、测试网格或下载命令。
4. 单任务墙钟 75 分钟；前 15 分钟必须完成分工与至少两篇抽取。若 60 分钟仍未形成综合，只收敛已有六篇，不扩范围。一次 commit、不 push；最终回报 commit、6/6 read count、Q#、terminal、claim ceiling 与 blocker。
