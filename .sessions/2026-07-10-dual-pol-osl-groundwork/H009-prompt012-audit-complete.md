# Handoff: PROMPT-012 双口径重审完成，待主控选择后续叙事

> 来源: S013 | 交接目标: 基于 D018 决定 Q-CMA-FADE 方法层下一步
> 日期: 2026-07-13

## 到哪了（状态）

PROMPT-012 四项重审及独立验证已完成，正式证据见报告与 V002。D015 的“ML 长序列真失效”已被 PI 口径否证；D014 的 10-seed 切片全为交换；S005 的 μ 主导保留但零风险安全阈值撤回；N=2M 的 ML PI 优势在三个 f_G、每格 10/10 paired seeds 中保留。

## 下一步干什么

先读 D018、V002 和 `PROMPT_012_REPORT.md`，只讨论一个选择：Q-CMA-FADE 方法层是按“短序列 PI 优势 + 流标识开销/长序列边界”重写，还是停止方法层并只保留经审计的发散分析层。选定前不新增方法实验。

## 纪律（续接者必须注意的）

- fixed-label 与 PI-BER 必须并报；PI 需 pilot/帧头，不能写成免费恢复。
- 不再引用“μ≤1e-3 零发散”“D014 等于断开”“ML 长序列真失效”。
- N=2M 的 ML 优势不得外推到任意序列长度或其他未审计参数域。
- 保留 dirty worktree；本轮结果 JSON 被 gitignore，仅脚本、测试、报告和治理记录入库。

## 接口变更

```yaml
contracts:
  - id: C001
    type: interface-change
    description: "PROMPT-012 三个隔离审计入口与双口径结果合同"
    location: "projects/simulation/explore/cma-fade-divergence/prompt012_*_audit.py"
    change: "fixed/PI BER、失败分类、共享 seed、显式 Torch seed、完整 experiment signature、脚本 SHA"
    consumed_by: "D018 / V002 / PROMPT_012_REPORT.md"
    verification_result: "PASS"
    verified_by: "V002"
```

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| PI 消歧开销未量化到具体帧结构 | PI 不是免费性能 | 本轮只声明需 pilot/帧头 | 若论文采用 PI 曲线或方法层叙事 |
| N=2M 优势适用域有限 | 不把切片外推成全域 | 仅审计 f_G=30/100/1000、strong、QPSK | 若声称跨长度/调制/湍流普适 |
| 原 S005 与本审计 SOP 不同 | 参数口径可追溯 | 原扫描 SOP=1e-4；本审计按 PROMPT-012 用 4e-7 | 若替换原 384-trial 全扫描数字 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 正式审计完整性 | 每格 10 shared seeds；cell 唯一；脚本 SHA一致，长/短实验签名完整 | PROMPT-012 / seed-bias 债务 | 3/3 审计 PASS |
| 双口径与分类 | verifier 从 trials 重算 0 不一致 | P6 分离审查 | 3/3 PASS |
| 代码测试 | 三目标测试全通过 + py_compile + diff-check | verification-before-completion | 见 V002 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - [ ] S005 μ=1e-3 为 3/20 发散 → 查 divergence JSON
  - [ ] N=5M ML 10/10 clean-swap、PI≈0.00523 → 查 longseq JSON
  - [ ] N=2M 三 f_G 均 ML paired win 10/10 → 查 shortseq JSON
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
