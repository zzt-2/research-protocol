# step-038 — P08-R2 receiver 信息边界 + AST 门 + 统计功效合同三根因修复（G 族，修正重判二轮）

> 2026-08-01 | campaign P08-R2 | family G（修复后关闭）| executor: 主线程协调 + 子 agent
> 上游：D049（binding decision，冻结 P08-R 科学结论 H7/H8/H9）+ 用户 P08-R2 执行指令
> 验收：V075（19/19 ACCEPT，脚本 + 独立 sub-agent 双重核验）

## 任务

用户 P08-R2 执行指令：P08-R 科学结论（`PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` +
Phase A 数字 + V074 ACCEPT + G 族关闭 + accepted_valid=8）不得继续使用——V074 漏审三项承重科学合同。
systematic-debugging 流程：根因复现（保存修复前证据）→ 治理回退 → receiver 信息边界根修 → 正确功效设计 →
fresh crossing 实验 → 条件式方法工厂 → 独立 verifier → 单次 commit。不修改旧 p08r_* 文件隐藏错误，
新建 `p08r2_*` 版本化路径（D048 PARTIAL 资产 verbatim 复用）。不 push。

## 三根因复现（修复前，证据 `projects/simulation/results/p08r2_receiver_info_repair/p08r2_prefail_evidence.md` + `p08r2_h7_reproduce.json`）

- **H7 receiver 信息边界（致命）**：`p08r_chain.py:341-360` `CodedRealizationR.equalize()` 读 `self.gamma_bar`（SNR 循环变量）三处——`:344` 盲 h 噪声底 `nv=1/(2·γ)` / `:354` `h_est=max(p−nv,1e-6)` / `:358-359` `mmse_equalize(rx,h,self.gamma_bar)`（第 3 参 SNR γ，`_equalizer.py:15` 公式 `rx·√h/(h+1/γ)`，`1/γ` 为加性噪声功率）。`amp_limit(thresh=3.0)` 固定绝对 clip 合法保留。**数值复现**（`p08r2_h7_reproduce.py`）：固定 rX/rY/sX/sY/h/theta/prefix/codeword/noise realization，只翻 `real.gamma_bar` 12→18/8dB，max\|ΔeqX\| 高达 **0.145**、max\|Δprefix_resid\| 高达 0.108、max\|ΔB0 LLR\| 高达 **7.02**（远超 tol 1e-12/1e-9，改 decode decision）。**deployable decide 间接消费 true SNR**：equalize 输出 eqX/eqY 进 `estimate_sigma2_from_prefix` → σ²_prefix → B0 LLR 全链污染。
- **H8 AST verifier 盲区**：`p08r_verify.py:109-129` check #5 只抽 `method_B0/B1/B2` 函数体字面文本搜 `"real.gamma_bar"`，**不递归进入** `real.equalize()`（在 `p08r_run.build_realization:50` 于 method 前执行）→ 漏审 H7。V074 sub-agent 把 equalize 用 gamma_bar 作盲 h 噪声底错标 "future-work seed 非缺陷"——H7 数值复现证伪此归类（ΔLLR ±7 改 decide）。
- **H9 统计合同三处非法**：① **MDE=0.2347 来源非法**（`p08r_run.py:197` `mde_fer=2.802·√(2·0.16875·0.83125/40)`，固定 n=40 后 power-0.8 阈值冒充 MDE；MDE 须先验登记再反算 n）。② **CI_lo=0 不能称 >0**（`delta_B0_minus_O2=[+0.00547, lo=0, hi=0.01406]`，独立重算确认 lo=0.0；CI_lo=0 ≠ 效应不存在）。③ **per-trajectory min(B1,B2) cherry-pick**（`p08r_run.py:286 strongest_conv=np.minimum(B1,B2)`，逐 trajectory 选两 comparator 更优者，post-hoc selection 未在合同冻结）。

## 修复（新建 p08r2_*，不动 p08r_*）

- **H7 fix** `estimate_pre_eq_noise_from_prefix()`：用 32-sym 已知 prefix 对 2×2 effective channel 做 LS 解 `H_eff`（4 复未知数 / 64 复方程，60 dof 残差），返回 receiver-visible σ²_pre。`CodedRealizationR2.equalize()`：盲 h 噪声底用 σ²_pre（替代 1/(2γ)）；MMSE 第 3 参用 γ_vis=1/σ²_pre（替代 gamma_bar）；amp_limit(3.0) 保留。
- **metamorphic 信息门** `p08r2_metamorphic_gate.py`：固定 realization 只翻 gamma_bar (6/9/12/15/18/22 dB)，所有 cell worst max\|ΔeqX\|=0.00e+00, worst max\|ΔLLR_X\|=0.00e+00（**精确零**，H7 runtime 铁证）。
- **H9 fix** `MetricContractR2`：mde_fer=0.05（a-priori，按 D005 务实路线 + 论文级 FER delta，非 post-hoc power 阈值）；power 分析 n_required≈814 at power 0.8 仅为透明度。`p08r2_run.py`：去 min(B1,B2)，B2 单一预登记 comparator + B0-B1/B0-B2 两条独立 delta；EVIDENCE_INSUFFICIENT 终态（CI_hw>MDE/2 触发）。
- **H8 fix** `p08r2_verify.py` check #6：`recursive_forbidden_check` 递归遍历 deployable 调用图（method_B0/B1/B2 + equalize + estimate_pre_eq_noise_from_prefix + gamma_vis_from_prefix + estimate_sigma2_from_prefix + llr_per_cw_from_eq），forbidden_set={gamma_bar,h_truth,theta}，max_depth=5。

## Fresh crossing 实验（dev 9000-9019 / test 8000-8039，disjoint from P08-R 6000-6019/7000-7039 + campaign history）

- frozen cell weak@1000Hz@12dB（dev B0 FER≈0.15，operating region [0.1,0.3]）。
- test 40 trajectories × 6 方法 paired，~400s。
- mean FER: B0=0.155 / B1=0.155 / B2=0.148 / O0=0.155 / O1=0.153 / O2=0.139（全聚集，无 LLR 校准信号）。
- delta_B0_minus_B2: mean=+0.0063 CI=[+0.0008,+0.0141] hw=0.0066（≪MDE=0.05）。
- delta_B2_minus_O2: mean=+0.0094 CI=[+0.0016,+0.0195] hw=0.0090（≪MDE，oracle 无 headroom）。
- evidence_sufficient=True（CI_hw≤MDE/2）；conv_helps=False；oracle_headroom=False。
- mechanism：3/40 B0 all-cw-fail（deep burst），O2 也 2/40 不可恢复；O2 partial rescue 6/40。

## 终态

`PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`（同 P08-R 物理机制，但这次在真正 γ-free corrected receiver 链 + 先验 MDE + 新 seeds + 无 cherry-pick 下得出）。Phase B/C 不运行（gate 顺序：O1/O2 headroom≪MDE）。

## 独立 verifier V075

脚本 19/19 PASS（含 H7 递归 AST 0 违规 + metamorphic 门 Δ=0.0 + H9 先验 MDE + 无 min(B1,B2) + EVIDENCE_INSUFFICIENT 可达 + fresh seeds + raw→aggregate relErr=0.0）。独立 sub-agent（fresh context，不信任 executor）7 项全 ACCEPT（H7 leak 复现 / H7 fix 正确 / metamorphic runtime / H8 verifier 递归 / H9 统计 / fresh seeds / verdict sanity + recompute relErr=0.0），无 executor 自述与实际差异。

## 治理纠偏

- D049：accepted_valid 8→7→8（恢复）；current=P08-R2→P09（入口准备不运行）；G 族关闭；P09 继续暂停。
- V074 标"16/16 consistency + H1-H6 PASS 但 H7/H8/H9 漏审"，保留不删；V075 取代 V074 科学层。
- 旧 P08-R artifacts 加 INVALIDATED_BY_P08R2.md（不删不改）；D048 PARTIAL 资产（5G NR LDPC / CodecAdapterR / 真 3GPP interleaver / GG params import / O0-O1-O2 ladder / H4 dev-freeze / H6 trajectory-cluster）在 p08r2_chain.py verbatim 复用。

## TL 教训登记

P07-R/D046 → P08/D048 → P08-R2/D049 是 "consistency≠correctness" 教训三度重演——verifier 必须递归遍历 deployable 调用图（不只复述合同/扫函数体字面）+ 跑运行时 metamorphic 门。此条作为 sim-preflight mve-validation.md 强化项候选。

## artifacts

- 脚本：`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_{chain,phaseA,run,verify,metamorphic_gate,h7_reproduce}.py`
- 结果：`projects/simulation/results/p08r2_receiver_info_repair/{p08r2_prefail_evidence.md, p08r2_h7_reproduce.json, p08r2_metamorphic_gate.json, p08r2_dev_workspace.json, p08r2_phaseA_gate.json, p08r2_phaseA_raw_rows.json, p08r2_v075_result.json}`
- 旧 P08-R 标记：`projects/simulation/results/p08r_coded_chain_repair/INVALIDATED_BY_P08R2.md`
- session note：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/S007-p08r2-receiver-info-repair.md`
