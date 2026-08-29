# Task Brief: C4-1 scaled-unitary pilot-LS Step 4a 纸面可行性

> 来源: S028 / D048 / T040–T048 / T064 | 产出位置: `projects/thesis-fso/polarization-demux-groundwork/step4a-c4-1-paper-feasibility.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 10
  action_class: GW_STEP4A_PAPER_FEASIBILITY
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 T064 已收窄为经典场景迁移的 C4-1 完成候选专属 GW Step 4a A0/A′/A/B，冻结问题、竞争维度、完整 receiver-visible recipe、适用边界、最小 comparator 与后续 correctness/headroom 停机门。只做本地证据综合与纸面判断；不得实现、仿真、联网检索、下载或修改论文正文。

## 候选冻结

- 目标场景：共同 DP-(8,8)-16APSK coherent FSO，memoryless single-tap `H=gQ`/near-scaled-unitary，短 balanced known pilots；无 PDL/PMD/FIR。
- baseline M：unconstrained pilot-LS `H_LS=Yp Xp^H (Xp Xp^H)^-1` 后直接求逆/正则逆。
- candidate action：`H_LS=U diag(s1,s2)V^H`，`g_hat=(s1+s2)/2`，`H_SU=g_hat U V^H`，`W=V U^H/g_hat`；输出 `z=W y` 和 receiver-visible `rho=s1/s2` applicability diagnostic。
- 已知事实：balanced pilots 下 post-LS projection 与 direct constrained scaled-unitary LS 代数等价；不得把 direct form 当独立新 estimator，也不得声称发明 polar/Procrustes/unitary Jones estimation。
- 最窄身份：经典 scaled-unitary constrained estimation 迁移到短 pilot DP-(8,8)-16APSK 星地相干解复用，并显式报告 receiver-visible 适用域/失效边界。

## 必须回答

1. A0：`M-C-A` 是否成立——短 pilot 下 unconstrained LS 的多余自由度是否有合理的方差/BER问题；问题四判据逐项 PASS/FAIL。
2. A′：主竞争维度是否冻结为同 pilot 开销下 payload BER，NMSE/inverse residual 只作机制；pilot overhead 相同。
3. A：结构假设是否匹配 frozen memoryless scaled-unitary slice；`rho` 是诊断还是动作，guard/fallback 是否必要且不靠拍阈值承重。
4. B：T064 强邻居与经典原子如何限制 claim；完整 target-scene recipe 未重复时，按 D031/D032 是否仍有 classical-migration 入口。
5. 冻结后续最小 ladder：unconstrained LS、tuned ridge、tuned singular-value floor/full-SVD inverse、C4-1、true `Q^H/g` oracle。direct constrained form只作等价检查，不重复计为 competitor。
6. 冻结 correctness：无噪 exact recovery、balanced equivalence、unitary/global-scale equivariance、nonunitary negative control、truth firewall。
7. 冻结最小 headroom：只允许 unitary slice、SNR `14/18 dB`、pilots `2/4`；所有 arms paired。若论文证据不能支持这些具体值，可标 `PARAMETER_AUTHORITY_BLOCKED`，但不得自行跑数据补洞。

## 纸面 terminal

- `PAPER_DIMENSIONS_PASS`：A0/A′/A/B 均成立，允许另派 correctness 实现；只表示 classical-migration 候选可测。
- `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY`：方法仅在 strict scaled-unitary slice 合法，rho/PDL 只作失效边界；仍可进入最小 correctness。
- `PAPER_FAIL_PROBLEM_ABSENT_OR_COLLISION`：完整 recipe collision、目标场景问题不存在或结构假设自相矛盾；关闭 C4-1，轮换 C4-0。
- `EVIDENCE_BLOCKED`：缺少承重公式/场景/参数 authority；列出最小缺口，不实现、不仿真。

## 交付与回报

交付唯一报告 `step4a-c4-1-paper-feasibility.md` 与必要 usage log。报告必须 facts-first，含 M-C-A、四判据、公式/IAO、baseline ladder、claim ceiling、correctness/headroom manifest、stop/pivot 和唯一下一步。运行 task-control validator、引用路径/行号检查与 `git diff --check`；最终一次 commit、不 push。不得新建候选、外部检索、实现、仿真、改 Skill/controller/正式论文正文。
