# Handoff: Batch 1 单轴小批完成，准备性能判断

> 来源: S047 | 交接目标: 在真实参数 small batch 合同通过后，决定是否扩大 paired 性能批或截断单轴
> 文件名: H015-batch1-small-batch-next.md

## 已完成边界

Batch 0.5 已 PASS（V006）；Batch 1 smoke 已 PASS（V007）；真实参数 pilot + 5-seed small batch 已完成并由独立 verifier 审计 PASS（V008）。四臂为 standard-CMA baseline、fade-freeze(h<0.1)、gradient-clip P99=0.0023782561886470004、gradient-clip P95=0.0005869870890765639。N=100000、seeds41–45、valid_samples=99968；freeze全0，P99 clip仅seed43触发61 blocks，P95为seed43=721/seed45=74；无 divergence/swap/fade。结果只作机制与合同记录，不作性能 Go/Kill。

用户长期约束原话："深耕一个点，从这个点延伸"；"一次列出所有的可能方向，再按合适的流程一批一批排、跑"；"首先去找方向，找完目前能找的，再划分，再跑"。

## 不要做什么

- 不把 threshold_h=2.0 触发烟测当真实 fade 结论。
- 不把 5-seed small batch 的 fixed/PI 差异当性能 Go/Kill。
- 不跳过 pilot/预注册判据直接扩成长跑；不分别修补 r7/prompt030/prompt015 历史入口。
- 不把 post-hoc PI 或 swap detector 当在线方法。

## 必读

1. `topic-index.md`
2. `S041-candidate-family-map-batch-plan.md`
3. `S047-batch1-real-parameter-paired-small-batch.md`
4. `verifications.md` V006–V008
5. `projects/simulation/master-state.md`（若路径存在则以实际项目状态文件为准）

## 接口变更（如有代码改动）

新增统一 Batch 接口：`BatchConfig`、`run_canonical_batch`、`standard_cma_adapter`、`batch1_fade_methods.run_method/make_method`；method contract 含 `zX/zY/valid_mask/diverged/divergence_symbol`，runner 统一输出 fixed/PI/window/events/source SHA。

## 失败数据附录（如涉及路线失败）

无路线失败；FIR 首尾零填污染曾被发现并修正：seed41 fixed/PI 0.0336914→0.0015625，seed42 0.0317383→0。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|----------|-------------|
| WSL worktree 的 `_meta.git_commit` 为空 | 结果需可追溯 | runner/method source SHA 已补齐；git 字段仍为空 | 正式结果迁移到可解析 Git 环境或补脚本审计 |
| freeze 在真实 pilot 未触发 | 单轴机制需有事件覆盖 | 5-seed small batch 全0 | 扩大参数域/长度前先重新冻结合同 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| small-batch contract | schema/mask/source SHA/finite 全通过 | V008 | 1/1 |

## 接收方验证

- [ ] 已读取 topic-index 不变量段落
- [ ] 已验证至少 3 条关键事实声称
- [ ] 已检查 registry depends_on/conflicts_with
- [ ] 已确认当前范围未违反明确不含

## 下一轮

先决定是否扩大 paired seed 数；若扩大，预注册主判据需包含 divergence、swap、recovery 与 fixed/PI 双口径，并保持四臂单轴分离。
