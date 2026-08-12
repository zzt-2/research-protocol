# Handoff: Step 4a defect smoke scientific termination

> 来源: S005 | 交接目标: 主控接收 Q001 negative terminal 并保持 closed
> 文件名: H005-step4a-problem-absent.md

## 已完成边界

- D007 例外下完成 A0→A′→A/B、独立 sandbox、dev freeze、Commit 1、五批 held-out、raw merge、2000-replicate aggregate 与 fresh verifier。
- G1=`3.1111% [2.3333%,3.9444%]` FAIL；G2 regret=`0.1114% [-0.3785%,0.4947%]`、outage +0 FAIL。
- D008 terminal=`PROBLEM_ABSENT_OR_TOO_SMALL`；Q001 closed，`mission_method_delta=NONE`。

## 不要做什么

- 不调参数、换事件定义、扩大 SNR/offset/GG 以重跑 Q001。
- 不实现 soft weighting/abstention，不跑 fair comparison/Contract。
- 不把 verifier PASS 写成 science PASS；它只证明 negative evidence 可接受。
- 不把 negative defect smoke 写成 exact collision、领域无问题或底座无效。

## 必读

1. `R006-step4a-defect-smoke.md`
2. `decisions.md` D007/D008
3. `verifications.md` V005
4. `projects/simulation/explore/dsp-outage-aware-combining/artifacts/test/aggregate.json`
5. `projects/simulation/explore/dsp-outage-aware-combining/task-5-merge-aggregate-report.md`

## 接口变更（如有代码改动）

新增独立 defect-smoke sandbox；未修改历史 b3、common、params 或正式论文代码。deployable arms 仅 B0/B1/B2；O1 为 truth-only evaluator。

## 失败数据附录（如涉及路线失败）

| 门 | 数字 | 终态影响 |
|---|---|---|
| G1 | 56/1800=3.1111%，CI 2.3333%–3.9444% | 低于 10%，first fail-stop |
| G2 | regret 0.1114%，CI -0.3785%–0.4947%；outage +0 | damage 未成立 |
| G3 | B2 regret 0.1114%，CI -0.3907%–0.5062% | diagnostic fail |
| G4 | AUC delta .000464，CI -.000675–.001692 | power-only 几乎完全吸收 |

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| strict aggregate iterator | direct CLI 应可复现 | process-local tuple adapter；独立重算一致 | 仅未来维护测试工具时修，不改变本终态 |
| Sun/Xie/Qiu action | 一手全文裁 exact action | 历史 claim limitation | 不构成 Q001 恢复入口 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 本轮结果 |
|---|---|---|---|
| G1 | ≥10%，≥3 cells | D007 freeze | FAIL，3.1111% |
| G2 | regret≥10%或outage+5pp，CI low>0 | D007 freeze | FAIL，0.1114%/0pp |
| evidence acceptance | raw/hash/schema/recompute/info boundary 全闭合 | V005 | PASS 0/0/1 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

保持 closed/idle。下一算法对象必须由主控重新选择，不得在本专题复活 Q001。
