# Thesis method packaging gate — GREEN raw responses

> 2026-08-03 | fresh-context, read-only behavioral regression

## Shared conditions

- prompt: `prompt.md`
- prompt SHA256: `87bb7f717513651c25e17ac73c5b473be4ba4891fcebb5d5caca1a5107fadd66`
- context: `fork_turns=none`; agents received the prompt and read only the
  current `SKILL.md`, `method-production.md`, and `thesis-harvest.md`
- access: shared filesystem read access; no file modifications, no scientific
  execution, no later audit summaries
- final Skill source SHA256:
  - `SKILL.md`: `79ae2b355d787808452581f9e1bd5c245c9a90e7c10cfd817235ddb43461d3b9`
  - `method-production.md`: `e424e7498cc6068f7d7f348843ea048883d30fe8b03265691c4ee41aea552fc2`
  - `thesis-harvest.md`: `f6a386814dadb66def2622d07344e2888f63fdc2a9540da06398551442f18559`

The agents were not shown `scorer.md` or any prior response.

## Agent `/root/packaging_blind_green_1`

```text
- `formal_science_disposition`: `PROBLEM_RESOLVED_BY_REGION_RETUNING`。复杂候选被常规离线区域重调吸收，关闭该候选；无 `METHOD_SIGNAL`，无活跃科学 carrier。
- `mission_method_delta`: `PACKAGING_BOUNDARY`，不是方法信号或正式方法进展。

- `thesis_method_disposition` 按独立 action lineage 判断：
  - Pilot-SNR adapter：`NEEDS_ONE_BOUNDED_PACKAGE`。其链路为“接收机可见导频 → SNR 估计 → 调整 DA/NDA 选择 → 输出分支决策”，已修复 4/5 个 harm cells，保留为潜在工程组件。
  - 复杂候选：`SUPPORTING_ONLY`。常规离线区域重调已解决其声称的问题。

- `harvest`：
  - `BOUNDARY_RESULT`：名义 SNR 失配会损害继承的 DA/NDA selector；adapter 在当前证据范围内修复 4/5 个 harm cells。
  - `BASELINE_ADJUDICATION` / `LOCAL_NEGATIVE`：复杂候选未超过充分调优的常规离线区域重调。
  - `REUSABLE_ASSET`：接收机可见的 pilot-SNR adapter。
  - 不登记 `METHOD_SIGNAL`；所有条目沿用已接受包中的证据指针和哈希，不扩张 claim ceiling。

- 下一合法动作：优先完成 adapter 的唯一 bounded closure，而非进入 method factory。用独立调优、相同运行时信息与导频预算的离线区域重调作为充分常规 comparator，以最强静态鲁棒阈值/区域策略为 cheap alternative，在 held-out mismatch grid 上做配对比较、adapter 消融及复杂度/时延核算。若稳定胜出，则评估 `THESIS_ENGINEERING_COMPONENT`；若失败，则降为 `SUPPORTING_ONLY`，不再串联新的 packaging package。
```

## Agent `/root/packaging_blind_green_2`

```text
- `formal_science_disposition`: `PROBLEM_RESOLVED_BY_REGION_RETUNING`。复杂候选被常规离线区域重调吸收；本包无 `METHOD_SIGNAL`，不建立 active scientific carrier。
- `mission_method_delta`: `PACKAGING_BOUNDARY`。这不是方法信号；但混合包中仍有一条可分离的真实动作链，不能随复杂候选一并关闭。

- `thesis_method_disposition`：

  - Pilot-SNR 适配器：`NEEDS_ONE_BOUNDED_PACKAGE`
    - M-C-A：继承的 DA/NDA selector 在 nominal-SNR mismatch 条件下，因区域选择未反映接收端实际 SNR 而受损。
    - 动作链：接收端可见 pilots → 估计 pilot SNR → 调整 DA/NDA 区域选择 → 输出所选分支结果。
    - 当前证据：修复 5 个受损 cell 中的 4 个。
    - 当前贡献层级：`SUPPORTING_MATERIAL`；若唯一闭包通过，可升级为有界的 `THESIS_ENGINEERING_COMPONENT`。
    - claim ceiling：仅声称接收端可部署的 mismatch-robust selector adaptation，不声称新的估计原理或普适方法。
  - 复杂候选：`SUPPORTING_ONLY`。其价值限于证明离线 region retuning 已足以解决对应问题，不构成独立贡献。

- Harvest：

  - `BOUNDARY_RESULT`：nominal-SNR mismatch 会损害继承的 DA/NDA selector；pilot-SNR adapter 在当前冻结范围内修复 4/5 harm cells。不得外推到未测试失配区间。
  - `BASELINE_ADJUDICATION`：常规 offline region retuning 吸收复杂候选的收益，因此复杂候选关闭。
  - `WRITING_MATERIAL`：保留“失配失效—接收端适配—剩余边界”的实验叙事。账本应引用本包实际 artifact、hash 和范围，不把纠正后的结论重复计作贡献。

- 下一合法动作：优先执行 pilot-SNR adapter 的唯一 bounded packaging package，而不是进入 method factory 或继续形式化新候选。冻结同一 5-cell mismatch 切片与配对样本，对比经独立调优的 offline region retuning 及最强廉价固定鲁棒阈值，加入 adapter on/off 与 nominal-SNR/pilot-SNR 输入消融，并报告性能、代价及第 5 个 cell 的边界。该包结束后必须立即定案：通过则 `THESIS_METHOD_READY`（工程组件）；失败则降为 `SUPPORTING_ONLY`，不得在同一标签下继续串联包装包。
```

Both responses satisfy all four frozen PASS criteria in `scorer.md`.
