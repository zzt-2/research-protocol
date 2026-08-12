# [S005] Step 4a feasibility-first defect smoke

> 2026-08-11–2026-08-12 | Groundwork Step 4a | closed

## 目标

在 D006 novelty debt 保留的前提下，按 D007 只验证 Q001 的 occurrence、damage、cheap-comparator residual room 与 receiver-visible observability；不实现候选方法。

## 记录

- Git 血缘核验：`608da01` 为 `d5eddb2` 的直接父提交；目标专题在两提交间无漂移。
- H004 接收核验：Round 1/引用链/Round 2 计数、Zhang neighbor、Sun/Xie/Qiu primary debt、V004 final PASS 均与 R005/V004 一致。
- registry：依赖 b3 joint-estimation 与 RDL system 均存在；coded decoder-feedback conflict 保留，且本轮不读取 decoder/FEC 信息。
- A0 fresh-context 预审：Q001 四判据仍为 4/4；未发现阻止纯 defect smoke 的新科学致命项。承重风险是 tuned SNR gate/GSC 可能吸收全部损失，或 receiver-visible validity 在控制 power 后没有信息增量。
- 实验顺序：完成 A0→A′→A/B 与 caller/information audit；只有分析门允许才建立独立 sandbox。dev 冻结后先提交 immutable receipt，再运行 held-out。
- 历史 b3 baseline 两次新鲜执行均复现自身 BER gate 失败（m1=`0.429626...`、m2/full≈`0.4300`，要求 `<0.3`），并确认 truth-h、全局 RNG、未注入 offset/FSTS 与错误 MRC 公式债务；旧文件保持不改，转入独立 sandbox。
- 独立 sandbox 采用 TDD：初版 reviewer 抓出 cell label 语义泄漏、随机 QPSK 冒充 FSTS 与 nominal/instantaneous SNR 混淆；bounded repair 后改为无语义 receiver DTO、BN=16/BL=20 单偏振 Park/FSTS proxy、瞬时 SNR 明确口径。第二轮 reviewer 抓出浅层 AST、相位顺序和 unguarded sync margin；修后递归 caller→callee audit、branch-local pilot correction→MRC、guard=`±1` 全部闭合。
- 统计管线 reviewer 两轮抓出可伪造 receipt、dev/test/schema 不 fail-closed、O1 非 truth-weight、event-only bootstrap、异方差噪声与 equal-noise MRC 不一致等问题。最终统一为同方差接收噪声、信号增益表达 H1/H2，B0/O1 分别用 estimated/truth channel 的同模型 MRC；raw/receipt/hash/grid/seed/candidate/重采样均 fail-closed。fresh final review=`PASS`，全测=`42 passed`；运行时 generator-exhaustion 回归修复后=`43 passed`。
- dev 只运行一次：20 seeds × 18 cells=`360` paired realizations，`6480` raw rows。第一次 strict tune 因 cell generator 被笛卡尔积耗尽而 fail-closed；物化 tuple 后复用同一 raw 完成冻结，未重跑。
- 冻结值：B1 `tau=-8 dB`；B2 `K2→L2/K4→L4`；strongest cheap=`B2`。dev-only AUC power=`0.9926801`、multi=`0.9960666`、delta=`0.0033864`，仅作冻结诊断，不是 test/science 结论。`freeze_receipt.json` 已写 `test_started=false`，七项 hash 独立一致；held-out 尚未开始。
- chronology Commit 1=`cbb8a2d` 后，held-out 按五个 20-seed batch 运行；每批 360 pairs/2520 rows，receipt/hash/schema 均通过。merged raw=`12600` rows、`1800` pairs。
- 冻结门结果：G1=`3.1111% [2.3333%,3.9444%]` FAIL；G2 relative BER regret=`0.1114% [-0.3785%,0.4947%]`、outage excess=`0` FAIL。G3/G4 仅诊断：B2 regret 同为 `0.1114%`；multi-source AUC delta over power-only=`0.000464`，CI=`[-0.000675,0.001692]`。
- independent verifier 从 raw 重算一致，V005=`PASS 0/0/1`。D008 依 fail-stop 裁 terminal=`PROBLEM_ABSENT_OR_TOO_SMALL`，不恢复 problem-bearing candidate；专题关闭。

## 决策引用

- D007：保留 novelty debt，开放一次 feasibility-first defect smoke（新建）。
- D008：G1/G2 negative，Q001 scientific termination（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D007 scope change record）。

## 后续

无。Q001 已按 D008 scientific fail-stop 关闭；不得重调、构造方法、fair comparison 或以另一组参数复活。
