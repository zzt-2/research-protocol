# [S010] G1 promotion groundwork 一次性重开 — 终态 G1_SIGNAL_INVALID_SCALE_ARTIFACT + P11 降级

> 2026-08-01 | G1_PROMOTION_GROUNDWORK（用户授权一次性重开 + P11 纠偏） | DONE — scale artifact 终态，诚实停止于 GW Step 1 前

## 目标

在同一对话中完成一次有边界的 G1 promotion workline：纠正 P11 + 对 G1 补齐语义审计/直接竞品/真实传统 comparator + 重走 Groundwork Step 1-3/3.5/4a，仅在全部 Go 后跑一次多切片 confirmation。必须遵守 Groundwork 硬门，若 Step 3/3.5/4a 失败诚实停止，不得先跑实验再补文献。plan §99 明文 stop condition：若 G1 只是 post-CMA 输出缩放且收益完全来自固定阈值 detector 尺度敏感，立即判 `G1_SIGNAL_INVALID_SCALE_ARTIFACT`，不进入文献包装或实验。

## 记录

### 执行路径

1. **启动恢复与 scope change**（plan §一）：读取纵向专题 topic-index/mission-log/D039/D041/D053-D056 + G1 harvest + G1 代码/raw + master-state GW Progress + stages/groundwork.md + gw-read/gw-supplement/gw-feasibility + thesis-lessons + research-direction-lab/session-governance/sim-preflight 规范。建立 D057 scope-change（decisions.md）：仅取代 D041/D039"不得第二个 G1 promotion 包"一条，D041 旧证据判断继续有效，其他 forbidden axis 全部不变，foreground control → G1_PROMOTION_GROUNDWORK。
2. **恢复 G1 真实身份**（plan §二）— 语义审计：fresh-context 子 agent `agent_cc6845fc` + 主线程源码复核，沿 caller→callee 不信任 doc 名字联想。11/11 项 PASS（见 worker-log step-042 + audit artifact）。**核心发现**：G1 = post-CMA per-pol per-block output 复标量乘，零 CMA tap 反馈，下游 fixed-threshold 16QAM slicer 无 AGC（contract 自承 "cannot undo magnitude scale"）。→ `G1_SIGNAL_INVALID_SCALE_ARTIFACT`。
3. **历史信号重新审计**（plan §三）— fresh-context 子 agent `agent_c5c1b3ed` 从 1120 raw rows 独立重算：collapse ΔPI-SER −0.56，healthy worst 0.0，gate 19/20 vs 1/29。**关键解读**：数字"强"恰好因为是 scale artifact（rescale 固定 grid 制造强恢复 + identity 制造强 safety），与代码审计一致而非矛盾。
4. **GW Step 1-3/3.5/4a — 跳过**（plan §99 stop condition 满足）：plan §二明文 scale artifact terminal 不进入文献包装或实验。Groundwork 诚实停止于 Step 1 前：A0 §0 前置门控拦（无过四判据 Q#；问题 A detector scale calibration 是部署接收机用 AGC 解决的平凡常规问题，非研究空白）。
5. **P11 纠偏**（plan §一，同时执行）：主线程从 `p11_phaseA_test_raw.json` 192 rows 逐 cell 复算。撤回 D056 三项过度措辞（B2 严格优于 B0/跨 SNR/LS 唯一解决者）。P11 降级 PARTIAL_LOCAL_9to15DB_BASELINE_ASSET，accepted_valid 8→7。chronology + linear FIR 身份 + raw 保留。

### 关键判断

**为什么停在 Step 1 前**：用户 plan §99 是显式的最快 kill-switch。语义审计沿真实 caller→callee（不信任"safe-gated normalization"名字联想）证明 G1 是 post-CMA scalar multiply + fixed-threshold slicer scale sensitivity。这是 detector 校准问题（问题 A），不是 genuine state-dependent switching（问题 C）。问题 A 是部署接收机用 AGC 解决的平凡常规问题，不构成研究空白。强行进 Step 2-3 文献闭包 = 违反用户明文 stop condition。

**为什么 P11 降级合理**：raw 数据逐 cell 复算（不是信 D056 的 pool 数字）：weak_fg30_9dB cell B0=0 perfect 优于 B2=4.83e-6（B2 在该 cell 劣于 B0，非"严格优于"）；strong_fg1000_15dB cell B4 zero-pilot blind CMA 9.94e-4 优于 B0 supervised 1.09e-3（blind CMA 也是强 comparator，非"LS 唯一解决者"）；SNR 覆盖仅 9-15dB（非"跨 SNR"）。chronology 闭合保留有效（非 P08-R2 型缺陷）。

**两个子 agent 裁决为何不矛盾**：code audit verdict = G1_SIGNAL_INVALID_SCALE_ARTIFACT；raw-rows verdict = HISTORICAL_SIGNAL_STRONG_ENOUGH_TO_CONTINUE_GW。看似冲突，实际一致——raw 数字强恰好因为是 artifact 才强（rescale 固定 grid 制造强恢复 + identity 制造强 safety）。如果 raw 数字弱，反而可能暗示有非 scale 机制值得查；raw 数字强 + 代码审计证明是 scale artifact = 终态确定。

## 决策引用

- D057：scope-change G1 promotion groundwork 一次性重开 + P11 降级 + G1_SIGNAL_INVALID_SCALE_ARTIFACT 终态（新建）
- V083：G1 语义审计 11/11 + P11 raw 复算（新建）
- D056：P11 PROBLEM_RESOLVED_BY_COMPLEX_LS（被 D057 取代计数与措辞；chronology + linear FIR 身份保留有效）
- D041：G1 FORMAL CLOSED / EVIDENCE_INCOMPLETE（继续有效，升级为 INVALID_SCALE_ARTIFACT）
- D039：campaign 授权（G1 promotion 一次性例外已用尽）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。用户授权一次性 G1 promotion groundwork 重开 + P11 纠偏，plan §99 明文允许 scale artifact 终态停止。
- **未恢复 CB1 family / 未做第二三个 G1 repair / 未绕 GW 跑旧 G1 / 未改正式论文结论 / 未升级历史局部结果 / 未重开其他 forbidden axis**。
- Groundwork 诚实停止（Step 1 前，A0 §0 拦），未跳步、未先跑实验。
- 纠偏 + Groundwork 工作不计科学包。

## 后续

- G1 promotion 一次性授权已用尽；G1 safe-gated-normalization scale artifact 加入 forbidden axis（禁换名重开 post-CMA amplitude gating / prefix-gated scaling / safe-gated normalization 等同对象，TL-30）。
- P11 降级 PARTIAL_LOCAL_9to15DB_BASELINE_ASSET；不做 P11-R。
- campaign accepted_valid=7/10，remaining_valid=3，未终止，0 active carrier，claim ceiling LOCAL_SLICE/NONBINDING_DIAGNOSTIC。
- **下一合法动作**：用户决定 D039 campaign 后续——(1) P12 继续探索 remaining 3 有效包预算（须过 problem-bearing 入口四门，禁重开所有 forbidden axis）；(2) 论文范围决策（G1 scale-artifact 诚实结论 + 局部负面 harvest + linear FIR 监督开销部分证据[9-15dB only]）；(3) 收尾审计（让原 system design 对话根据磁盘证据审计）。
- 本轮无 sprint/无 held-out seed/无 method card/无 commit 之外产物。单次最终 commit（plan §十三 No-Go 模式）。不 push。
