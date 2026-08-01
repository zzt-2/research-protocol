# [S006] P08-R coded-chain 科学完整性修复（G 族，六根因 systematic-debugging）

> 2026-08-01 | campaign P08-R / SCIENCE_INTEGRITY_REPAIR | 状态: done（V074 16/16 ACCEPT）

## 目标

执行用户 P08-R coded-chain 科学完整性修复指令：修复旧 P08 的六项科学合同缺陷（H1-H6），
在 corrected chain 下重新裁决 coded-LLR-calibration 问题。暂停 P09，不把本轮另计为第九包。
本轮必须在同一对话完成：根因复现→治理回退→身份澄清→GG/信息/oracle/metric 修复→fresh experiment
→条件式方法构造→独立 verifier→一次统一 commit。不 push。

## 记录

### Route check（三句）
1. 本轮不是 P09，是修复 P08 的承重科学合同（P08-R, SCIENCE_INTEGRITY_REPAIR，不计有效包数，同 P07-R/CP037）。
2. coded-chain 基础设施可保留为 PARTIAL reusable asset，但当前 P08 科学结果（V073 ACCEPT / PROBLEM_ABSENT / G 族关闭 / accepted_valid=8）无效。
3. 只有修复后实验有效，才能恢复 accepted_valid 到 8/10；在此之前维持 7/10、G 族不关闭、P09 暂停。

### Phase 1 根因复现（prefail evidence，修复前确定性证据）
3 个独立 Explore 子 agent 并行核验 + 主线程交叉复核，六项根因全部源码级确认：
- H1：p08_phaseA_gate.py:86 硬编码 scenes={weak:(1.2,1.2),moderate:(4.2,1.4),strong:(8.0,4.0)} vs params.py:100-228 真值 weak=11.6,10.1/moderate=4.0,1.9/strong=4.2,1.4（三档全错，档位错位）。
- H2：6 处 σ²=1/(2γ_bar)（循环变量，非 receiver-visible）。
- H3：_oracle_sigma2 返回单 global scalar，不覆盖候选 local/blockwise。
- H4：Primary A 全 inf 静默退未冻结 raw FER-delta，MDE 从未生效。
- H5：LDPC5GEncoder 未传 num_bits_per_symbol，sionna §5.4.2.2 interleaver 永不激活，worker-log 谎称 triangle。
- H6：16 cw 当独立样本，raw 缺逐 cw h/fade 字段。
证据存 `projects/simulation/results/p08r_coded_chain_repair/p08r_prefail_evidence.md`。

### Phase 2 治理纠偏（D048）
- accepted_valid 8→7；current=P08-R；P09 暂停；G 族暂不关闭。
- V073 标"合同一致性通过但科学合同六项漏审"，保留不删；旧 artifacts 加 INVALIDATED_BY_P08R.md。

### Phase 2 coded-chain 身份冻结（option A，test 前）
验证 sionna LDPC5GEncoder 传 num_bits_per_symbol=4 ⇒ out_int 真 3GPP §5.4.2.2 sub-block+triangle
置换（1536 unique，1534/1536 moved，前 12=[0,384,768,1152,1,385,...]，Q=384）；noiseless roundtrip
BER=0；burst-fade 下 A vs B 区分度低（物理发现非身份问题）。冻结 option A（p08r_identity_freeze.md）。

### Phase 3 最小修复脚本（p08r_*，旧 p08_* 不动）
- p08r_chain.py：H1 get_gg_scenes()；H5 CodecAdapterR(num_bits_per_symbol=4)；H2 CalibrationPrefix + estimate_sigma2_from_prefix；H3 O0/O1/O2；H6 CodedRealizationR。
- p08r_phaseA.py：H4 MetricContractR（fresh seeds）；H6 bootstrap_ci trajectory-cluster；method_B0/B1/B2/oracle。
- p08r_run.py：orchestrator（dev scan→freeze metric before test→tune→test→mechanism decomp→verdict）。
- p08r_verify.py：V074 16 项。

### Phase 4 fresh powered experiment（240s）
- dev workspace：B0 FER 清晰从 ~0.5-0.68（10dB）降到 0（22dB），跨所有 scene/fG（旧 P08"卡在0.2"是 H1+H2 artifact）。
- frozen cell：weak@1000Hz@12dB，dev B0 FER=0.169，MDE_fer=0.2347（power 0.8，n_test=40）。
- test（40 fresh trajectories paired）：mean FER B0/B1/B2/O0/O1/O2=0.115/0.115/0.113/0.115/0.115/0.109；Δ(B0−O2)=+0.0055 CI=[0,0.014]≪MDE。
- mechanism decomposition：4/40 不可恢复深衰落 trajectory（h_truth 0.29-0.41），O2 也译不出；32/40 B0 full success。
- verdict：**PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE**。Phase B/C 不运行（gate 顺序）。

### 独立 verifier V074
脚本 16/16 PASS + 独立 sub-agent（fresh context，不信任 executor 自述）沿 caller→callee 检查科学信息边界，
逐项核 H1-H6 + AST + mechanism 独立重算一致，最终 **ACCEPT**。future-work seed（非缺陷）：equalize 盲 h 估计用 gamma_bar 作噪声底。

## 决策引用

- D048：P08 coded-chain 科学完整性修复（新建）——冻结旧 P08 科学结论六根因，campaign 8→7，重做 corrected chain。
- V074：P08-R 独立 verifier 16/16 ACCEPT（新建）——取代 V073 科学层。
- CP039：mission-log checkpoint（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D047 scope-change 授权 coded-chain 场景扩展，本轮修复其在执行中暴露的六项科学合同缺陷，未扩范围；P09 入口准备是 D047 既定 next_legal_action）。

## 后续

- campaign accepted_valid 恢复 8/10，G 族关闭。
- 仍 0 active carrier；claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。
- P09 入口准备（不运行）：必须换不同机制族（G 已关闭），候选 coded operating-boundary / receiver-ranking，须重新过 problem gate。
- 旧 P08 数字不得进入论文或 harvest，除非被 P08-R 新结果重新支持（新结果支持同一物理归因但 corrected chain）。
- future-work seed：equalize 盲 h 估计可改 prefix-based noise floor 加固信息边界（非缺陷，V074 标注）。
