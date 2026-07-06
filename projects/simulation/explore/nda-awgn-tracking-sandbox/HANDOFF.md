# Handoff: NDA-ML AWGN 逐符号跟踪改进实验(sandbox)

> 来源: S005(对话 5 续)| 交接目标: 试"NDA-ML 加逐符号跟踪能否追平 BPS",给老师看结果
> 文件名: HANDOFF.md(放 sandbox 自身目录内)
> 日期: 2026-07-06
> 用户状态: 吃饭去了,授权新对话在 sandbox 随便试,试完汇报

---

## 0. TL;DR(新对话先读)

**现状**:SC-NDA-ML 方向 5 seed 主实验 PASS(AWGN fair gain +0.78dB),但 BPS 消融发现 **AWGN HD-FEC 段 BPS 反超 NDA 0.53dB**(weak/moderate/strong 湍流 NDA 平手或赢)。

**深入诊断发现**(本轮新发现,关键):**NDA 和 BPS 在 AWGN 有 SNR-crossover**——低 SNR(5-10dB)NDA 赢 BPS(BER 差 7-19%),12dB 平手,**HD-FEC(18dB)落在 BPS 优势区**所以显得 BPS 反超。

**机制推测**:NDA-ML 的 AWGN 实现(`nda_ml_recovery(assume_df_zero=True)`)整块只估一个常相位 φ(mean-angle),**没跟踪块内 Wiener PN 漂移**(256 符号 × 40ps 累积相位方差 ~0.032rad)。BPS 有滑窗逐符号跟踪(Nw=101)→ high SNR 跟得上 Wiener PN。

**你的任务**:在 sandbox 试"给 NDA-ML 加逐符号/块内相位跟踪",看能否追平 BPS 的 AWGN high-SNR 优势。**只改 sandbox 副本,不准动 common/ 或已验证的 simulator/**。

**成功判据**:AWGN HD-FEC 段(18dB,BER≈3.8e-3)改进后的 NDA BER ≤ BPS BER(0.0040)。若追平/反超 → NDA 真的更好(低 SNR 本来就赢 + high SNR 追平),论文叙事大幅增强。

**失败判据**:加跟踪反而让升幂噪声放大 dominate,BER 更差 → 说明块内常相位是合理近似,改进无解,论文走"湍流场景方法"定位。

---

## 1. 已完成边界(主对话做的事)

### 1.1 关键诊断数据(已落盘,新对话直接读)

**BPS vs NDA-ML vs DA ML AWGN 全 SNR BER**(来源 `projects/simulation/results/sc_nda_ml_bps_ablation/_bps_ablation_5seed.json` `.summary.awgn.points`):

| SNR(dB) | NDA BER | BPS BER | DA BER | oracle BER | NDA-BPS(负=NDA赢) |
|---|---|---|---|---|---|
| 5 | 0.186771 | 0.205214 | 0.253880 | 0.176498 | **-0.0184(NDA 赢)** |
| 8 | 0.110101 | 0.129240 | 0.130836 | 0.105208 | **-0.0191(NDA 赢)** |
| 10 | 0.070437 | 0.077230 | 0.076285 | 0.067021 | **-0.0068(NDA 赢)** |
| 12 | 0.042021 | 0.041979 | 0.042369 | 0.039502 | +0.0000(平手) |
| 14 | 0.023897 | 0.022710 | 0.023042 | 0.021574 | +0.0012(BPS 赢) |
| 16 | 0.012231 | 0.010880 | 0.011141 | 0.010028 | +0.0014(BPS 赢) |
| **18(HD-FEC)** | 0.005224 | **0.004028** | 0.004183 | 0.003407 | +0.0012(BPS 赢 → fair gain 算出 -0.53dB) |
| 20 | 0.001844 | 0.000960 | 0.001055 | 0.000671 | +0.0009(BPS 赢) |

**weak 湍流全 SNR 段 NDA 都赢 BPS**(虽然 margin 小):见同文件 `.summary.weak.points`,所有点 NDA-BPS < 0。

**结论**:问题集中在 AWGN high-SNR 段(14-20dB),尤其 HD-FEC(18dB)。

### 1.2 机制代码定位

**NDA-ML 当前 AWGN 实现**(`projects/simulation/common/_recovery.py:nda_ml_recovery`,行 171-250,重点看 `assume_df_zero=True` 分支):
```python
if assume_df_zero:
    raised = rx ** M0
    phi_raised = np.angle(raised.mean())  # ← 整块 mean-angle,一个常相位
    phi_est = phi_raised / M0
    df_est = 0.0
    rx_comp = rx * np.exp(-1j * phi_est)  # ← 全块用同一相位补偿
```

**问题**:256 符号块内 Wiener PN 累积相位方差 = 2π·500e3·(256·40e-12) ≈ 0.032 rad ≈ 1.8°。整块用 mean-angle 会"抹平"块内相位漂移,符号级残余相位误差在 high SNR 段成主导 → BER floor 比 BPS 高。

**BPS 当前实现**(`projects/simulation/common/_recovery.py:bps_cpr`,行 91-115):滑窗 Nw=101 逐符号搜最佳相位,能跟踪块内漂移。

---

## 2. 下一步干什么(sandbox 实验)

### 2.1 实验目标

**改进 NDA-ML AWGN 估计,加块内/逐符号相位跟踪,看能否在 HD-FEC 段追平 BPS**。

### 2.2 候选改进方案(试错,分层试错法 P3 最小切片)

**方案 1(最轻,优先试)**:块内分段 mean-angle
- 把 256 符号块切成 K 段(如 K=4 段 × 64 符号),每段独立 mean-angle 估相位,K 段相位之间线性插值或 hold
- 优点:实现简单,仍用升幂 mean-angle(保留 NDA-ML 内核)
- 参数旋钮:K(段数)。K=1 退化到现状;K=4/8/16 试

**方案 2(中)**:块内滑窗 mean-angle(类 BPS 但用升幂)
- 升 M₀=8 后,对 |rx^M₀|·exp(j·M₀·φ) 序列做滑窗(Nw)mean-angle,得逐符号相位
- 优点:直接对标 BPS 的滑窗机制
- 参数旋钮:Nw(窗长)。Nw=1 退化为逐符号(噪声大);Nw=256 退化到现状

**方案 3(重,慎用)**:用 `assume_df_zero=False` 完整单正弦 ML
- FFT 找频率(块内相位斜率)+ 线性回归相位
- 风险:B11 行 33 假设 df=0,FFT 找频率会锁噪声伪峰(D003 修复的就是这个 bug)
- 只有方案 1/2 都失败才试

### 2.3 实验设置(复用主实验参数,公平对照)

- **调制**:(8,8)-16APSK + Gray
- **信道**:AWGN + Wiener PN(CLW=500kHz, BAUD=25GBaud,σ²_p=2π·Δν·T_S)
- **SNR 扫描**:γ_d [5,8,10,12,14,16,18,20]dB(同主实验 AWGN,NDA 无 pilot 所以 γ_d=γ_tot)
- **N_sym/点**:102400(400 块 × 256),seed 固定
- **对照**:NDA-原 / NDA-改进(方案1/2/3) / BPS / oracle
- **判定指标**:HD-FEC(18dB,BER≈3.8e-3)处 NDA-改进 vs BPS BER

### 2.4 执行建议

1. **先读** `projects/simulation/common/_recovery.py:nda_ml_recovery` + `bps_cpr` + `projects/simulation/simulator/sc_nda_ml_sim.py`(看 AWGN 信道生成 + 评估)
2. **复用** `simulator/_b11_params.py` 参数(不准改参数)
3. **写 sandbox 脚本** `projects/simulation/explore/nda-awgn-tracking-sandbox/`(本目录):
   - `experiment.py`:跑 4 配置(NDA-原/NDA-方案1/NDA-方案2/BPS)× 8 SNR 点,输出 BER 曲线
   - 可选 `_results.json`:结构化结果
   - 可选 `_curves.png`:BER 曲线对比
4. **核心算子必须从 common/ 导入或复制 `nda_ml_recovery` 后改**(不准直接改 common/)。BPS 直接用 `common.bps_cpr`(但 m16apsk 适配版要复制,见 BPS 消融脚本 `simulator/run_bps_ablation.py` 的 `bps_cpr_m16apsk`)
5. **时间预算**:整个对话 < 用户回来时间(估 1-2 小时)。优先跑方案 1(K=4/8),跑完看趋势再决定方案 2

---

## 3. 纪律(必守)

1. **只改 sandbox 目录**(本目录 `projects/simulation/explore/nda-awgn-tracking-sandbox/`)。**不准改** `common/` / `simulator/` / 已验证的 MVE/Formal 代码。改了 = 破坏已 PASS 的主实验
2. **复用 common/ 的信道生成 + 调制 + BPS**(TL-13 共用同一信道实现,公平对照前提)
3. **参数全溯源**:不准拍参数。N_DFT/M0/CLW/BAUD/HD-FEC 都从 `_b11_params.py` 读
4. **诚实第一**:改进失败就报失败,不准为了让 NDA 赢而调 BPS 参数或作弊
5. **MVE 一致性纪律**(TL-23):改进后如果 AWGN HD-FEC BER 突然变得比 oracle 还低 → 一定有 bug(漏了 pilot overhead / 偷看了 tx / 单位错),停下来查
6. **守 AGENTS.md 主对话严禁 WebSearch**:需要查 BPS 文献用子 agent
7. **单对话 3 步上限**:本 sandbox 实验算 1 大步,留余量给分析

---

## 4. 结果汇报格式(用户回来后给)

写一份简短报告(放 sandbox 目录 `_RESULT_REPORT.md`),结构:

```markdown
# NDA-ML 逐符号跟踪改进实验报告

## 试了什么
- 方案 X(K=Y / Nw=Z)

## 结果
| SNR | NDA-原 | NDA-改进 | BPS | 改进是否追平 BPS? |
| 18(HD-FEC) | 0.0052 | X | 0.0040 | ✅/❌ |

## 判断
- 追平了 → 方案 X 有效,论文可增强叙事(NDA 低 SNR + high SNR 都赢)
- 没追平 → 块内常相位是合理近似,改进无解,走"湍流场景方法"定位

## 推荐下一步
- [一句话]
```

---

## 5. 接口变更

无(只改 sandbox,不动 common/simulator)。

## 6. 失败数据附录

无(sandbox 实验,失败也是合法结果,记录即可)。

## 7. 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| NDA-ML AWGN 块内常相位近似 | 方法完整性 | 本 sandbox 试改进 | 若追平 BPS,主实验代码升级 |
| BPS m16apsk 适配版在 `simulator/run_bps_ablation.py` | 复用 | 已实现,可参考 | sandbox 直接 import 或复制 |

---

## 8. 接收方验证(续接对话时)

- [ ] 已读本 HANDOFF 的 §0 TL;DR + §1 诊断数据
- [ ] 已验证 §1.1 表的关键数字(读 `_bps_ablation_5seed.json` 核查 AWGN 18dB NDA=0.0052 BPS=0.0040)
- [ ] 已确认 sandbox 目录 `projects/simulation/explore/nda-awgn-tracking-sandbox/` 存在且空(除本 HANDOFF)
- [ ] 已读 `common/_recovery.py:nda_ml_recovery` 的 `assume_df_zero=True` 分支(§1.2 机制)
- [ ] 已读 `simulator/run_bps_ablation.py` 的 `bps_cpr_m16apsk`(BPS 适配参考)

## 9. 上下文恢复(对话压缩后)

**最重要的一句**:NDA-ML 在 AWGN 被 BPS 反超 0.53dB 是真的,但深入看是 HD-FEC 工作点(18dB)恰好落在 BPS 优势区——低 SNR(5-10dB)NDA 反而赢 BPS。机制推测是 NDA 整块常相位没跟块内 Wiener PN 漂移。本 sandbox 试加块内跟踪能否追平。

**Dead Ends(已排除)**:
- ❌ 不要改 common/(破坏已 PASS 主实验)
- ❌ 不要重写 NDA-ML 算法骨架(只加块内跟踪,不动升幂 mean-angle 内核)
- ❌ 不要试方案 3(FFT-df)除非方案 1/2 全败(D003 修复的 bug 会回来)
- ❌ 不要为追平 BPS 而调 BPS 参数(作弊)

**Progress**:sandbox 已建,诊断数据已落盘,等新对话执行

**用户意图**:吃饭去了,授权随便试,试完看结果汇报。关心的是"NDA 能不能在 AWGN 追平 BPS" + "如果不能,论文怎么定位"

**已确认决策**:
- `DECIDED`:NDA-ML 主路径(DA ML baseline + per-block KF + 湍流场景全赢)站得住,sandbox 只是探索 AWGN 增强
- `TENTATIVE`:论文定位待 sandbox 结果 + 老师判断(湍流方法 vs 频谱效率方法 vs 双叙事)

**中间结论**:BPS AWGN 反超 0.53dB 是工作点选择问题不是方法碾压;NDA-ML 改进方向是加块内相位跟踪
