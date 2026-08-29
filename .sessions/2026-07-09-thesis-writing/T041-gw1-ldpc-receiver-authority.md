# Task Brief: LDPC receiver-visible 接口与公平 comparator

> 来源: S028 | 产出位置: `projects/thesis-fso/direction-lab/harvest/ldpc-receiver-authority.md`
> 日期: 2026-08-30
> 唯一文档: 本 T + 当前仓库既有证据；允许用项目 `tools/search` 做外部学术检索

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 1
  action_class: EXTERNAL_EVIDENCE
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

为 Ch5 的 syndrome 引导失败码字救援、NOMS/调度后备和选择性 BICM-ID 完成 Groundwork Step 1 检索，回答标准 LDPC 实现可见哪些 receiver state、哪些 comparator 公平，以及哪些动作有机会改善 FER 而不只是多跑迭代。

最高纪律：只做 Step 1，不实现、不跑实验；syndrome、posterior/extrinsic、逐轮状态的可见性必须区分“算法上定义”与“当前 Python codec 实际接口”。不把额外计算隐瞒成免费增益。

## 1. 背景

Ch5 暂定优先级为 C5-1 几何软解调、C5-2 syndrome rescue、C5-0 LLR 校准。历史固定 NOMS 相对 baseline 改善很小；旧 coded decoder-feedback 在另一配置下失败。目标不是复活旧 claim，而是核清不同机制族的合法动作和 baseline。

## 2. 任务详情

1. 至少三组查询：LDPC syndrome-guided post-processing/unreliable-bit rescue；adaptive normalized/offset min-sum and scheduling；BICM-ID/extrinsic demapping for APSK/coherent optical。
2. 审查不少于 20 条元数据，优先 TCOM/TWC/JLT/JSAC/TCAS 和经典 decoder 文献；确认正式版本。
3. 对 C5-2/C5-0 及高成本后备分别给出：deployable input、动作、输出、计算代价、主 comparator、等成本廉价替代、最可能改善 BER/FER 的机制。
4. 明确“普通 restart/额外迭代/OSD/bit-flipping/固定 NOMS/完整 BICM-ID”分别会吸收什么，并给出公平预算口径。
5. 区分标准 syndrome、posterior LLR、extrinsic LLR 和逐轮 callback；列出进入实现前必须审查的当前 codec 接口。
6. 输出 5–8 篇 Step 2 必读候选，标全文可得性和需核对的公式/消融。

产出结构：一句话结论；state/interface 表；method/comparator 表；等成本合同；Step 2 候选；当前 codec 审查清单；UNKNOWN。保存产出并只提交该 harvest 文件及本任务生成的唯一 search JSON；最终回报 commit、路径和一句结论。

## 3. 已知陷阱

- syndrome-guided 方法必须比同等额外迭代或普通 restart 更好才能主张 FER 方法，但被吸收时可诚实降为工程/支持材料。
- 不把 decoder truth 或发送比特用于部署决策。
- 不把 detector-only 结果当 downstream FER 改善。

## 4. 验收

- [ ] 每个候选动作都有 receiver-visible 输入和等成本 comparator
- [ ] 明确当前 codec 接口需核对什么
- [ ] 5–8 篇 Step 2 候选可核
- [ ] 无实验、代码或论文正文修改

