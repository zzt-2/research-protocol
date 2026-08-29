# Task Brief: Ch5 APSK soft receiver GW Step 3 结构化精读

> 来源: S028 | 产出位置: `projects/thesis-fso/literature_notes_apsk_soft_receiver.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 3
  action_class: GROUNDWORK_READ
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行 GW Step 3，完整精读 T044 的 6 篇 qualified full texts，主对象是 C5-1 structured APSK covariance demapper，C5-2 decoder rescue 只作机制后备：

1. `papers/doi/10.1186_s13638-018-1136-z/content.md` — Improved demapping for channels with data-dependent noise。
2. `papers/doi/10.1109_vetecs.2009.5073425/content.md` — Bit-interleaved LDPC-coded modulation with iterative demapping and decoding。
3. `papers/doi/10.1109_lcomm.2010.07.100508/content.md` — Adaptive-normalized/offset min-sum algorithm。
4. `papers/doi/10.1186_s13638-016-0769-z/content.md` — Ordered-statistics decoding for LDPC telecommand links。
5. `papers/doi/10.1109_wcsp52459.2021.9613326/content.md` — trapping-set post-processing。
6. `papers/doi/10.1109_iccc59590.2023.10507492/content.md` — syndrome-guided bit-flipping representative。

## gw-read 强制清单

- 每篇先做 title 自检；mismatch 立即 ABORT 并写 read-log。
- 每篇使用标准 14+ 字段模板，含源文件路径、至少两句核心贡献、具体实现数值、baseline 与适配性；传统 DSP/FEC 论文不适用的 state/action/reward/network 字段必须写 `N/A（原因）`，不得省略。
- 完成 7 个结构化子表：状态空间、动作空间、奖励函数、建模假设、网络架构、适配性分析、问题提取 M/C/A + 四判据；公式必须内联 LaTeX。
- 对至少 3 篇核心论文做实验完备性提取；对 Layton 2018 和另一篇标杆做写作架构提取。
- 形成综合分析：方法分类、局限、趋势、背景、研究问题清单。至少给出 C5-1 的 Q# 四判据结论，并单列 C5-2 是否有合法 Q#；不得因“经典邻居强”自动 Kill，只判断完整 recipe 是否 exact identical、目标动作是否还有可陈述差别。
- 每篇生成 `papers/_read_notes/{paper_id}.md`，并向 `projects/thesis-fso/read-log.md` 追加合规记录。

## C5-1 必答问题

- Layton 2018 是否已经完整覆盖“样本依赖 full covariance + Mahalanobis/log-det demapping”；若覆盖，pilot-only causal estimation、radial/tangential structure、跨偏振/跨环 shrinkage pooling 是否仍是 receiver-visible 且非完全相同的 recipe？
- 公平 comparator 必须是什么：isotropic scalar、per-ring scalar、full covariance；各自需要相同哪些 pilot/sample/budget？
- 从全文提取可直接实现的 covariance estimator、regularization、likelihood/LLR 公式与信息边界。

## 边界与验收

- 不检索、不下载、不做 Step 3.5/4a、不实现、不实验、不改仿真/Skill/controller/论文正文。
- 只提交 dedicated literature notes、6 篇 read notes、read-log 追加和必要的 read receipt/report。
- ≥5 篇完整精读且至少一条 Q# 过四判据才 PASS；否则输出 `STEP3_NO_Q_SURVIVOR` 或精确 blocker，不擅自补文献。
- 最终回报 commit、read count、Q# 数、C5-1 exact-collision verdict 和唯一 blocker。
