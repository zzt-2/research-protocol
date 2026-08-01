# P08-R2 prefail evidence — 修复前的确定性根因证据（H7/H8/H9）

> 2026-08-01 | P08-R2 SCIENCE_INTEGRITY_REPAIR | Phase 1 (systematic-debugging)
> 目的：在任何代码修改前，逐项固化 P08-R (D048/V074) 漏审的三项承重科学合同缺陷的源码级 + 数值级证据。
> 本文件所有 file:line 均为**修复前 HEAD = 5a7823d** 的快照，引用的是 P08-R 脚本（保留不改、标 INVALIDATED_BY_P08R2）。
> 证据收集方法：主线程读源码 + 数值复现脚本 + 2 个独立 Explore 子 agent 并行核验（mmse_equalize 语义、P07-R 不构成先例）。
> 关联：P08-R artifacts 在 `projects/simulation/results/p08r_coded_chain_repair/`（保留不删，本目录加 INVALIDATED_BY_P08R2.md）。

## Route check（三句）

1. 本轮不是 P09，是修复 P08-R 漏审的三项承重科学合同（P08-R2, SCIENCE_INTEGRITY_REPAIR，不计有效包数，同 P07-R/D046 与 P08-R/D048 模式）。
2. P08-R 的 GG/oracle/identity/H4-H6 修复有效，作为 PARTIAL reusable asset 保留；但 P08-R 当前科学结果（V074 ACCEPT / `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` / G 族关闭 / accepted_valid=8）无效——它在 receiver 仍消费 true SNR 的链上得出。
3. 只有修复后实验有效，才能恢复 accepted_valid 到 8/10；在此之前维持 7/10、G 族不关闭、P09 暂停。

## 三路 route（grounded in 真相源）

- H7（receiver 信息边界）：P08-R `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:341-360` `CodedRealizationR.equalize()` + `projects/simulation/common/_equalizer.py:13-15` `mmse_equalize` 公式语义。
- H8（AST verifier 盲区）：P08-R `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_verify.py:109-129` check #5 抽取逻辑。
- H9（统计合同）：P08-R artifacts `projects/simulation/results/p08r_coded_chain_repair/p08r_dev_workspace.json` + `p08r_phaseA_gate.json` + `p08r_phaseA_raw_rows.json` + `p08r_run.py:286,342-348`。

---

## H7 — equalize() true-SNR 上游泄漏（receiver 信息边界违反）✅ 复现

### 三处 gamma_bar 引用（修复前源码，逐字）

P08-R `p08r_chain.py` `CodedRealizationR.equalize()`（:341-360）：

```python
341:    def equalize(self) -> Dict[str, np.ndarray]:
342:        """Per-block MMSE + amp_limit equalization, receiver-visible per-block h."""
343:        nv = 1.0 / (2.0 * self.gamma_bar)   # ← H7: 盲 h 估计噪声底读 true SNR
344:        block = self.eval_block
...
354:                h_est[sl] = max(p - nv, 1e-6)   # ← h_est 含 true-SNR 噪声底
...
358:        eqX = amp_limit(mmse_equalize(self.rX, hX, self.gamma_bar), 3.0)  # ← MMSE 第3参 = true SNR
359:        eqY = amp_limit(mmse_equalize(self.rY, hY, self.gamma_bar), 3.0)
```

`self.gamma_bar` 是 SNR 循环变量（`p08r_run.build_realization:43` `g = 10**(snr_db/10)`），非 receiver-visible 估计。

### mmse_equalize 第 3 参 = SNR γ（不是 σ²）

`projects/simulation/common/_equalizer.py:13-15`：

```python
13: def mmse_equalize(rx, h, gamma_bar):
14:     """MMSE 均衡，h 可为标量或向量"""
15:     return rx * np.sqrt(h) / (h + 1/gamma_bar)
```

公式 `rx·√h/(h + 1/γ)` 中 `1/γ` 扮演加性噪声功率 σ² 的角色。**第 3 参语义是 SNR γ**，所以 receiver-visible 替换须是 γ_vis = 1/σ²_pre（其中 σ²_pre 是 receiver-visible pre-equalization 噪声估计）。

### amp_limit 合法（不读 γ）

`_equalizer.py:5-10`：`amp_limit(rx, thresh=3.0)` 是固定绝对幅度 clip（`mask = amp > thresh`），不读 gamma_bar。**保留不改**。

### H7 数值复现（修复前确定性证据）

脚本 `p08r2_h7_reproduce.py`：固定 rX/rY/sX/sY/h/theta/prefix/codeword/noise realization（在 γ_ref=12dB 建一次），**只翻转** `real.gamma_bar` 属性到 18dB / 8dB，重调 `equalize() + method_B0`，测 deployable 输出变化。结果存 `p08r2_h7_reproduce.json`：

| 翻转 | pol | max\|Δeq\| | max\|Δprefix_resid\| | max\|ΔLLR\| |
|------|-----|-----------|----------------------|-------------|
| 12→18dB | X | 7.72e-02 | 5.71e-02 | 1.88e+00 |
| 12→8dB  | X | 1.45e-01 | 1.08e-01 | 5.17e+00 |
| 12→18dB | Y | 7.28e-02 | 4.92e-02 | 2.01e+00 |
| 12→8dB  | Y | 1.36e-01 | 9.31e-02 | 7.02e+00 |

**判定**：所有 tol（Δeq<1e-12, ΔLLR<1e-9）全部突破。**H7 CONFIRMED**——receiver 的 equalized samples、prefix residual、B0 LLR 全部随隐藏 true SNR 变化。`estimate_sigma2_from_prefix`（V074 标"receiver-visible"）的输入 `eqp` 本身已被 gamma_bar 污染，所以它产出的 σ² 也间接受 true SNR 影响（σ²_prefix: 6.43e-02→6.26e-02/7.45e-02）。**deployable decide 间接消费 true SNR**。

### 调用链（caller→callee）

```
p08r_run.build_realization (g = 10**(snr/10))
  → CodedRealizationR(..., gamma_bar=g).realize()  # 物理生成（合法用 γ）
  → real.equalize()
      → nv = 1/(2·self.gamma_bar)            # H7① 盲 h 噪声底
      → h_est = max(p_rx − nv, 1e-6)         # H7② h 含 true SNR
      → mmse_equalize(rx, h_est, self.gamma_bar)  # H7③ MMSE 用 true SNR
      → amp_limit(.., 3.0)                   # 合法
  → method_B0(eq, prefix)
      → estimate_sigma2_from_prefix(eqp, sp) # eqp 已被 ①②③ 污染
      → demap → LLR                          # LLR 被 true SNR 间接污染
```

### H7 捕获要求（修复后必须满足）

deployable path（equalize → MMSE → prefix σ² → demap → LLR）禁止读 `gamma_bar`/`h_truth`/`theta`/`sX`/`sY`/future samples；pre-equalization 噪声须来自 receiver-visible prefix LS 残差（σ²_pre）；MMSE 第 3 参 = γ_vis = 1/σ²_pre。**metamorphic 信息门**：固定 realization 只改隐藏 `gamma_bar`，deployable 输出 Δ<tol。

---

## H8 — AST verifier 盲区（V074 #5 漏审 H7 的原因）✅ 复现

### V074 check #5 抽取逻辑（修复前源码，逐字）

P08-R `p08r_verify.py:109-129`：

```python
109:    # 5. B0/B1/B2 no true γ/h/θ/TX leakage (AST scan of p08r_chain/phaseA)
...
113:    deploy_src = ""
114:    for name in ("method_B0", "method_B1", "method_B2"):
115:        # extract function body lines
116:        lines = src_A.split("\n")
117:        in_fn = False; body = []
118:        for ln in lines:
119:            if f"def {name}(" in ln: in_fn = True
120:            elif in_fn and ln.startswith("def ") and name not in ln: break
121:            elif in_fn: body.append(ln)
122:        deploy_src += "\n".join(body) + "\n"
...
126:    reads_true_gamma = "real.gamma_bar" in deploy_src
127:    c = uses_prefix and not reads_true_gamma
```

**缺陷**：抽取只覆盖 `method_B0/B1/B2` 三个函数体的**字面文本**，搜 `"real.gamma_bar"`。它**不递归进入**：
- `real.equalize()`（在 `p08r_run.build_realization:50` 于 method 调用前执行，其体在 :344/:358/:359 读 `self.gamma_bar`）
- `mmse_equalize`（_equalizer.py:13 第 3 参）
- `estimate_sigma2_from_prefix`（其输入 eqp 已被污染）

由于 `method_B0` 函数体里只出现 `eq["eqX"]`（已 equalized）和 `estimate_sigma2_from_prefix(eqp, sp)`，不含字面 `real.gamma_bar`，所以 check #5 PASS——但 H7 泄漏发生在上游 equalize()，method 函数体检测不到。

### V074 sub-agent 同样归类错误

`verifications.md` V074 #5（:3887）原文："sub-agent 指出 equalize() 用 gamma_bar 作盲 h 估计噪声底（receiver-side 模块，非 decide 泄漏）——非缺陷，记录为 future-work seed"。**此归类错误**：equalize() 的输出 eqX/eqY 直接进 `estimate_sigma2_from_prefix` → B0 LLR，是 decide 路径的上游，不是孤立 receiver-side 模块。H7 数值复现（上表）证明 LLR 随 true SNR 变 ±7，远超 decide 阈值。

### H8 捕获要求（修复后必须满足）

verifier AST 必须**递归遍历 deployable 调用图**——从 `method_B0/B1/B2` 出发，对每个被调用的 receiver 函数（`real.equalize`、`mmse_equalize`、`estimate_sigma2_from_prefix`、新增的 prefix LS 估计器）递归扫禁用字面量（`gamma_bar`/`gamma`/`h_truth`/`theta`/`sX`/`sY`/future）。metamorphic 门作为运行时双重保险。

---

## H9 — 统计合同三处非法（已数值复现）✅ 复现

### H9① MDE=0.2347 来源非法（post-hoc power 阈值冒充 MDE）

P08-R `p08r_run.py:197`：

```python
197: mde_fer_est = 2.802 * np.sqrt(2 * p_hat * (1 - p_hat) / max(n_test, 1))
```

其中 `p_hat=0.16875`（dev B0 FER @ weak/1000/12dB），`n_test=40`（**已固定**）。算出 `mde_fer_est = 0.23466`（artifact `p08r_dev_workspace.json:115` `mde_fer: 0.23466096539409256`）。

**判定**：这是"固定 n=40 后 power-0.8 的检测阈值"，**不是 MDE**。MDE 的定义是先验登记的"最小值得关注的效应量"（来自毕业价值/论文级 Δ），应当**先于** n 决定，再用 MDE 反算所需 n。P08-R 把 n 固定后的 power 阈值命名为 MDE，是**统计合同非法**。

### H9② CI_lo=0 不能称 CI_lo>0

P08-R artifact `p08r_phaseA_gate.json` `test_results.delta_B0_minus_O2`：

```json
"delta_B0_minus_O2": [0.00546875, 0.0, 0.0140625]   # [mean, ci_lo, ci_hi]
```

`ci_lo = 0.0`（独立重算确认：bootstrap 2000 次，`rng=20260801`，lo=0.0 hi=0.01406）。**CI 下界正好 0**，不能当作"正信号被排除"。verdict 代码（`p08r_run.py:342-348`）用 `CI_lo > 0` 作门，CI_lo=0 时判 False 进 PROBLEM_ABSENT——但 "CI_lo=0" 不等价于 "效应不存在"，只等价于"数据不足以排除 0"。须诚实标 `evidence_insufficient` 或显式说明 CI_lo=0 含义。

### H9③ per-trajectory min(B1,B2) 是 post-hoc cherry-pick

P08-R `p08r_run.py:286`：

```python
286:    strongest_conv = np.minimum(B1, B2)  # best of B1/B2 per trajectory
```

**判定**：逐 trajectory 在两个 conventional comparator（B1 temperature-scaling、B2 decoder-tuning）里**选更优者**再算统计量 `B0 - strongest_conv`，是 post-hoc selection。这种"事后挑好的"会系统低估 B0-conv 差距（向 conv 有利偏），且未在 metric contract 冻结。合法做法：预登记**单一** conventional comparator（B1 或 B2 之一），或两条独立 delta（B0-B1、B0-B2）分别报，不取 min。

数值佐证：本数据集 B1 mean FER = B2 mean FER = 0.1148（数值相同，B1=B0/T 在此数据上无区分度），min(B1,B2) mean = 0.1133 < min(meanB1, meanB2) = 0.1148，证实 min 运算引入了 0.0015 的 post-hoc 偏移。

### H9 真实统计单位（确认）

`fer_traj` 取值（test 40 traj）：`{0.0, 0.03125, 0.0625, 0.09375, 0.40625, 1.0}`——已是 32 cw × 2 pol 聚合（n_cw_per_pol=16 × 2 pol = 32 cw/trajectory），独立单位 = trajectory/seed（不是 cw）。dev FER=0.1 交叉在 weak/fG1000 @ 12-14dB 之间真实存在（dev_summary: 12dB B0=0.169 / 14dB B0=0.0）。

### H9 捕获要求（修复后必须满足）

MDE = 先验登记值（按 D005 务实路线 + 论文级 FER delta ~0.05），记录与 power 阈值的换算；power 分析改为"在登记 MDE 下算所需 n，按停止规则采"。CI_lo=0 诚实标 "无正信号证据" 或 `evidence_insufficient`。去掉 per-trajectory min(B1,B2)，预登记单一 comparator（倾向 B2，因 B1=B0/T 数值无区分度）或两条独立 delta。

---

## 汇总：三项缺陷的科学后果

1. **H7（receiver 信息边界）**：equalize() 读 true SNR，污染 eqX/eqY → prefix σ² → LLR，deployable decide 间接消费 oracle 信息。所有 P08-R 数字（B0/B1/B2/O0/O1/O2 mean FER、Δ、CI、verdict）均在泄漏链上得出。
2. **H8（AST 盲区）**：V074 #5 只扫 method 函数体字面，不递归，漏审 H7；sub-agent 把 equalize 错归类为"非 decide 模块"。
3. **H9（统计合同）**：MDE 是 post-hoc power 阈值非先验；CI_lo=0 当排除；min(B1,B2) 是 cherry-pick。

**结论**：P08-R verdict `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` **无效**——它在 receiver 仍消费 true SNR 的链上、用非法统计合同得出。V074 ACCEPT 漏审 H7/H8/H9。需 P08-R2 修复后重做。D048 的 GG/oracle/identity/H4-H6 修复 + D047 入口裁决继续有效，作为 PARTIAL reusable asset。
