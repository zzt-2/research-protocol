# [R005] 论文方法章保留门行为回归

> 2026-08-03 | 关联：2026-07-20-research-direction-lab-system / D021

## 调研问题

现有 Skill 的问题究竟是“不会判断什么能包装”，还是“正常科学包收尾时没有自动做包装判定”？怎样用最小修订保住 2A/2B，同时不放松科学门？

## 发现

1. 确定性 RED：在修改 Skill 前先增加结构测试，针对 HEAD `5b69a0e` 运行时因缺少 `THESIS_METHOD_READY` 与独立 chapter-capability checkpoint 而失败；这证明正常收尾没有强制结构槽位。
2. 未保留原始响应的探索性 microtest 曾提示混合包血缘问题，但其样本数不作为承重证据。
3. 最小修订增加四状态 checkpoint，并明确按可分离 real-action lineage 裁决：一个复杂候选被 conventional alternative 吸收，不得抹掉同包里另一条真实可部署动作链。
4. GREEN：2/2 保留原文的 fresh-context 样本通过 `prompt.md` 四项判据；均保留 pilot-SNR adapter 为 `NEEDS_ONE_BOUNDED_PACKAGE`，同时保持 `METHOD_SIGNAL=0`、active scientific carrier=0，并优先路由唯一 bounded closure。

完整行为 prompt、RED source identity/失败摘录与 GREEN 原始响应见 `.agents/skills/research-direction-lab/tests/forward/runs/thesis-method-packaging-gate/`。

## 结论

最小正确修订不是降低 `METHOD_SIGNAL` 标准，也不是增加新的贡献评分器，而是：每个 evidence-valid accepted package 必填独立 `thesis_method_disposition`；混合包按可分离动作链裁决；只有一个决定性缺口时允许 `NEEDS_ONE_BOUNDED_PACKAGE`；invalidated/unauthorized/artifact 仍为 `REJECT`。

## 对决策的影响

支持 D021。2A/2B 当前只获得“值得分别诊断一个 bounded package”的入口，不代表实验 PASS 或论文方法已经成立。
