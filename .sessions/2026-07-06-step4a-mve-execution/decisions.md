# Decisions — Step 4a 维度 D MVE 执行

> 专题 `.sessions/2026-07-06-step4a-mve-execution/` 的决策记录。
> D### 按编号排列，血缘链通过 取代/被取代 字段维护。

## D001: baseline 复现优先于增量评估（方法论纠偏）

> status: active
> date: 2026-07-06
> 取代：无
> 被取代：无
> 依据: 用户原话 voice 2026-07-06（"我们是在复现啥？一般不是复现顶刊当 baseline 然后再继续我们自己的吗？"）

### 决策

**已发表 baseline（如 B11 IEEE PTL 2025）必须先复现立住，再做我们的增量评估。FR-21 oracle 上界是评估"我们自己的增量方法"的上界，不是评估已发表 baseline 的——baseline 在论文场景下的 dB 是既成事实，不需要用 oracle 上界重新判。**

### 理由

本对话步骤 3 主线误把 B11 当"我们自己的候选方法"做 FR-21 oracle 上界评估（CRB 层 + BER 层 + AWGN 复现三轮），用户原话戳穿："我们是在复现啥？一般不是复现顶刊当 baseline 然后再继续我们自己的吗？你这是在干啥？"

正确流程：
1. **复现 baseline**（B11 在 B11 原始场景 AWGN 下复现 +2dB）
2. **做我们的增量**（星地湍流迁移/单载波时域改进等）
3. **评估增量**（FR-21 oracle 上界判增量方法的 Go/Kill）

错误流程（本对话步骤 3 走的）：
1. ❌ 跳过 baseline 复现
2. ❌ 直接拿 B11 当我们方法做 FR-21
3. ❌ 三轮诊断后才意识到范围偏离（M6）

### 排除的替代方案

- "跳过 baseline 复现直接评估"：被用户纠正否决。原因：架构性不等价下（OFDM 频域 vs 单载波时域）评估结果反映的是实现差异不是方法差异，会误判。

### 影响范围

- 所有后续 baseline 处理（B11/B7/B3）必须先复现再做增量
- common/_recovery.py 的 nda_ml_recovery 已修 2 bug（D002 详述）
- 步骤 3 三轮诊断产出（CRB/BER/AWGN 脚本）保留作方法学参考，但不作 B11 Go/Kill 依据

### 来源

用户纠正（S002，voice 2026-07-06 "我们是在复现啥"原话）

## D002: B11 角色重定位 = 理论参考（非直接对标 baseline）

> status: active
> date: 2026-07-06
> 取代：无（不取代上游 D005/D006，仅细化 B11 处理）
> 被取代：无
> 依据: 调研 _star_ground_link_survey.md + 验证 _awgn_repro_results.json + critic _OFDM_infra_assessment.md + 用户原话 voice 2026-07-06（"方案 C：B11 作参考，做单载波时域 NDA-ML 改进"）

### 决策

**B11（IEEE PTL 2025 NDA-ML STO+CPE）在论文里定位为"理论参考"（'NDA 升 M₀ 次幂 + ML' 思想源头），不作直接对标 baseline。我们的增量 = 单载波时域下的 NDA-ML 改进（架构诚实，贴星地主流单载波）。不强行复现 B11 +2dB，增量 dB 重新锚定。**

### 理由

三重证据支撑：

1. **星地 FSO 主流是单载波**（_star_ground_link_survey.md）
   - DVB-S2/S2X 标准：单载波（QPSK/8PSK/M-APSK + BCH/LDPC）
   - DLR sat.1553 综述：标准 DSP 流水线无 OFDM 主流方案
   - 顶刊近期星地 FSO 论文（Horst 2023 Nature / Le Bidan 2023 ICSO / Fernandes JLT 2023 / Mouhammad JLT 2025）：无一例 OFDM 作星地主流
   - CCSDS O3K 星地光通信标准：单载波 DP-QPSK/16QAM
   - OFDM 在星地 FSO 仅研究探索（PAPR/ICI 问题）

2. **B11 是 OFDM 频域 ML，与单载波时域架构性不等价**（_OFDM_infra_assessment.md）
   - 频域 R(k)^M₀（子载波索引）vs 时域 r(n)^M₀（时域采样）：数学不等价
   - 频域 CPE 单常相位 vs 时域逐样本 Wiener θ(n)：方差放大 M₀² 倍
   - 频域 STO = DFT 循环移位定理（线性相位 2πτk/N）vs 时域整数 STO 是索引移位：完全不同模型
   - 频域有 DFT 处理增益，时域逐样本升幂无处理增益
   - 强行复现 +2dB 是"为复现而复现"

3. **B11 团队定位非星地主流**（_star_ground_link_survey.md）
   - B11 是 fiber+FSO 通用声明（行 9/191），仿真未建模 FSO 信道（行 33 假设湍流/Doppler/CFO 已补偿）
   - Kam 团队主体是 fiber CO-OFDM 相位噪声 ML 系列
   - B11 被引仅 1 次（HSR 地对车，背景引用）

### 排除的替代方案

- **方案 A（补 OFDM 基建复现 +2dB 再迁移）**：否决。原因：(a) OFDM 与星地主流脱节；(b) genie-aided 解卷绕（B11 行 129-131）非可实现，可能仍复现不了；(c) 工作量 3-4 子 agent 且与目标链路不匹配。
- **方案 B（放弃 B11 转 B7 Gardner TED FOE）**：保留作备选。B7 单载波+FOE 基建已就绪，但本轮先走方案 C（吸收 B11 思想到时域），B7 作并行候选保留。

### 影响范围

- **后续路径**：单载波时域 NDA-ML 改进（吸收 B11 升 M₀ 次幂思想 + 独立推导时域 CRLB + 重新锚定增量 dB）
- **common/_recovery.py**：nda_ml_recovery 已修 2 bug（D003 详述），assume_df_zero 参数 + resolve_m16apsk_blockwise
- **baseline 设计**：DA ML 用真符号 pilot（spacing=4 密集）近最优——单载波下 DA ML 不是"未优化 baseline"而是"pilot 充分时的近最优估计器"。后续增量方法要超越的是这个近最优 DA ML，不是 B11 论文里 decision-feedback 的 DA ML。
- **不变量 6 profile 第 8 次防线**：仍守（每候选先算上界），但上界评估对象是**我们的增量方法**不是已发表 baseline

### 来源

S002 + 调研 _star_ground_link_survey.md + 验证 _awgn_repro_results.json + critic _OFDM_infra_assessment.md + 用户原话 voice 2026-07-06（方案 C 拍板）

## D003: nda_ml_recovery 两 bug 修复（FFT-df 锁噪声伪峰 + 块间 resolve 失败）

> status: active
> date: 2026-07-06
> 取代：无
> 被取代：无
> 依据: 验证 _awgn_repro_results.json + 子 agent 诊断 _awgn_repro_diagnostic.py（Variant B 实现）

### 决策

**common/_recovery.py:nda_ml_recovery 修复两个 bug：(1) 加 assume_df_zero 参数（True 时跳 FFT-df 估常相位 CPE，B11 行 33 场景用）；(2) common/_modulation.py 加 resolve_m16apsk_blockwise / resolve_apsk8_blockwise（逐块解 M₀-fold 模糊，解 Wiener PN 累积致块间落入不同模糊）。**

### 理由

两个 bug 由 AWGN 复现诊断子 agent 发现，导致 B11 NDA-ML 在 AWGN 下 BER 灾难性输给 DA ML（−1.9 dB），修复后 BER 从 5.25e-3 → 2.07e-3 @ 18dB（Variant B 精确复现）。

**Bug 1（主因）**：FFT 频率搜索在 df=0 时锁噪声伪峰（B11 行 33 假设 CFO 已补偿，真 df=0，但代码对 rx^M₀ 做 FFT 找频率 + Quinn 插值锁到噪声伪峰 df_est≈188 kHz）。修复：assume_df_zero=True 时跳 FFT-df，直接 angle(mean(rx^M₀))/M₀ 估常相位 CPE。默认 False 保留现有 FFT-df 逻辑（未来星地 Doppler 残余用）。

**Bug 2**：resolve_m16apsk 全局单旋转无法解 8 重块间模糊（Wiener PN 累积致块间真 φ(k) 落入不同模糊 m）。修复：逐块 resolve（用每块 tx_bits 选最优 2π/8 旋转），block_size 默认 256（对齐 B11 DFT_SIZE）。

### 排除的替代方案

- "重写 nda_ml_recovery 全部逻辑"：否决。保留现有 FFT-df 分支作未来星地 Doppler 残余场景用，只加 assume_df_zero 分支。

### 影响范围

- common/_recovery.py: nda_ml_recovery 签名变（加 assume_df_zero 参数，默认 False 向后兼容）
- common/_modulation.py: 新增 resolve_m16apsk_blockwise, resolve_apsk8_blockwise
- common/__init__.py: 导出新增 2 函数
- 后续 NDA-ML 调用：B11 场景（CFO 已补偿）必须传 assume_df_zero=True + 用 blockwise resolve

### 来源

S002 + 子 agent 诊断（_awgn_repro_diagnostic.py Variant B）+ 验证 _awgn_repro_results.json

## D004: 单载波时域 NDA-ML 改进 GO_MVE + 公平对照框架确立

> status: active
> date: 2026-07-06
> 取代：无
> 被取代：无
> 依据: 调查 _crlb_results.json（解析 CRB + 信道校准修复后公平对照）+ 用户原话 voice 2026-07-06（"形态 A+C：频谱效率 + 湍流鲁棒性"）+ 调查 _ber_floor_diagnostic.json

### 决策

**单载波时域 NDA-ML 改进（形态 A+C）通过 FR-21 oracle 上界前置门控，GO_MVE 进 MVE。公平对照框架确立：DA ML 含 pilot overhead 1.25dB 总能量代价，NDA-ML 纯数据，比较在相同总功率/相同信息率下。**

**核心数学结论（D004-a，CRB 层）**：CRB_NDA(φ)/CRB_DA(φ) ≈ N_p/N = 1/4（per-symbol avg power equal）。M₀² 在升幂噪声方差放大（分母）和相位参数增益（分子）严格相消。**CRLB 层 NDA-ML 理论下界优于 DA ML**（用全 N 符号 vs 仅 N_p pilot）。上一轮 CRB 层子 agent 的 "M₀²·N_p/N=64×" 推导错误源于漏算 (d arg(z)/dφ)²=M₀² 项。

**公平对照 gain @ HD-FEC**（D004-b，信道校准修复后）：
- AWGN **+0.70 dB**（形态 A 频谱效率增量锚）
- weak **+1.20 dB**（形态 A+C）
- moderate **+1.92 dB**（形态 A+C 叠加）
- strong HD-FEC 不可达（物理上限，oracle@26dB=1.96e-2 也不可达），但 NDA 全工作区赢 DA（形态 C 鲁棒性，DA pilot 在 deep fade 崩溃）

### 理由

1. **CRB 层理论支撑**：M₀² 严格相消，NDA-ML 用全 N 符号估 CPE 信息量 > DA ML 仅 N_p pilot
2. **公平对照物理依据**：DA ML pilot overhead 1.25dB 是真实能量代价（相同总功率下 DA 信息符号有效 SNR 低 1.25dB）
3. **形态 A（AWGN）**：pilot overhead 1.25dB − NDA 升幂噪声/resolve 残差 ~0.5dB = 净 +0.7dB
4. **形态 C（湍流）**：DA pilot 在 deep fade 处 BER 崩溃（5dB weak 0.38 vs NDA 0.29），NDA 全帧积分对单点 fade 鲁棒
5. **信道校准修复**（关键，避免 BER floor 假象）：
   - 主因 D2（h_med 标量均衡残差）→ 修复 per-block h（NDA 盲 / DA pilot / oracle 真）
   - 次因 D1（CFO 残余 assume_df_zero=True 误用）→ 修复两阶段 fft_foe + nda_ml_recovery
   - 修复后 weak/moderate HD-FEC 可达（min BER 5.37e-4 / 2.71e-3）

### 排除的替代方案

- "用 naive 对照（不计 pilot overhead）"：否决。naive gain AWGN -0.55dB 误导（DA 总能量没算 pilot 代价），公平对照才反映真实系统对比
- "strong 湍流 HD-FEC 不可达判 fail"：否决。oracle 也不可达 = 物理上限（deep fade 主导），非估计器缺陷。NDA 全工作区赢 DA 即形态 C 成立
- "B7 并行开 MVE-SPEC"：后置。单载波 NDA-ML 已 GO，集中资源，B7 待 NDA-ML MVE 完后视情况开

### 影响范围

- **下一步**：跑 SC-NDA-ML MVE（H003 交接下轮，契约见 `explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md`）
- **baseline 对照框架**：所有后续 NDA vs DA 比较必须用公平对照（DA 含 pilot overhead 总能量代价）
- **信道校准**：所有后续 MVE 必须用 per-block h 均衡 + 两阶段 FOE+CPE（avoid BER floor 假象）
- **CRLB 数学**：上一轮 "M₀²·N_p/N=64×" 错误已澄清，后续升幂 ML 分析用正确 CRB_NDA/CRB_DA = N_p/N
- **形态 A+C 双增量叙事**：论文叙事框架（AWGN 频谱效率 + 星地湍流鲁棒性）

### 来源

S003 + 验证 _crlb_results.json + 调研 _ber_floor_diagnostic.json + 用户原话 voice 2026-07-06（"形态 A+C"）

## D005: SC-NDA-ML MVE PASS → Go（形态 A+C 双增量实证成立）

> status: active
> date: 2026-07-06
> 取代：无（落实 D004 的 GO_MVE 判定，进 Step 5）
> 被取代：无
> 依据: 验证 `_mve_results.json`（MVE 实测 BER + gain_analysis + FR-11/14/15/18 + TL-20 偏离检查）+ 主线独立 grep 核查 6 项 MVE 纪律落实（per-block h / 公平对照 / 两阶段 FOE / resolve blockwise / 共用信道 / N≥1e5）+ `SC-NDA-ML-MVE-SPEC.md` §5 pass/fail 标准
> 触发原话: 无（技术推导——Go 判定基于实测 fair gain 数字 vs SPEC §5 阈值，非用户 voice 触发）

### 决策

**单载波时域 NDA-ML 改进（形态 A+C）MVE 通过 SPEC §5 Go 标准，进 Step 5（Baseline 选定）。公平对照 fair gain @ HD-FEC（BER=3.8e-3）全 ≥0.5dB：AWGN +0.704 / weak +1.199 / moderate +1.922 dB；strong HD-FEC 物理不可达（oracle 也不可达）但 NDA 工作区(≥15dB)全赢 DA（per-point fair gain +1.19~+2.62dB）。TL-20 预期表 5 项全 PASS 0 DEVIATION。**

### 理由

**主指标全过 SPEC §5 Go 门**（公平对照 BER gain @ HD-FEC，DA 含 1.249dB pilot overhead 总能量代价）：

| 场景 | SPEC §5 Go 阈值 | 实测 fair gain | 判定 |
|---|---|---|---|
| AWGN（形态 A）| ≥0.5 dB | **+0.704 dB** | ✅ PASS |
| weak（形态 C）| ≥0.5 dB | **+1.199 dB** | ✅ PASS |
| moderate（形态 C）| ≥0.5 dB | **+1.922 dB** | ✅ PASS |
| strong | NDA 全工作区赢 DA（HD-FEC 物理不可达）| 工作区(≥15dB)全赢，per-point +1.19~+2.62dB | ✅ PASS（形态 C 鲁棒性）|

AWGN gain 0.704 dB > 0.5 dB，**不在 0.3-0.5 薄增益 Conditional 区间**，判 Go 非 Conditional。

**辅助判定（非一票否决）全过**：
- strong HD-FEC 不可达 = 物理上限（oracle 真 h@26dB min BER=1.96e-2 > 3.8e-3，deep fade 主导），非估计器缺陷 → 形态 C（NDA 全工作区赢）成立
- NDA-vs-oracle gap 全 <3dB（0.38/1.49/1.97/2.58 dB）→ 升幂 ML 实现正确，无 bug
- weak/moderate/strong 低 SNR cross-over（盲 h 噪声低 SNR 拖累）物理合理，SPEC §5 明示不判 fail

**TL-20 预期对照（5 项锚点全 PASS 0 DEVIATION）**：
- AWGN gain 在 [0.3,0.8] ✓ / weak 在 [0.5,1.5] ✓ / moderate 在 [1.0,2.5] ✓ / strong 不可达+工作区赢 ✓ / NDA-vs-oracle gap <3dB ✓

**核查机制中性双向（不变量 10）满足**：子 agent 返回数字主线独立 grep `_mve_results.json` + `_time_domain_crlb.py` 源码逐项核查 6 项 MVE 纪律落实（per-block h 行 250-282 / 公平对照 PILOT_OVERHEAD_DB 行 124 / 两阶段 FOE 行 285-297 / resolve_m16apsk_blockwise 行 167/300 / generate_shared_realization_apsk 行 411 / N_BLOCKS=400×256=102400）。

### MVE 实现说明（透明披露）

子 agent 的 `sc_nda_ml_mve.py` 是 `_time_domain_crlb.py`（S003 产出）的薄包装——`importlib` 加载后调其 `run_awgn/run_turb`，仅做输出 schema 映射。**核查结论**：`_time_domain_crlb.py` 本身是 S003 按 MVE 标准写的合格实现（per-block h + 公平对照 + 两阶段 FOE + resolve blockwise 全落实，名字虽叫 crlb 但实际跑了完整 BER 实验），子 agent 包装只是换数据契约格式，**底层 MVE 代码合格 → MVE 结论有效**。这不是循环验证伪 MVE——S003 那轮的 CRLB 推导 + BER 实验本就是 MVE 的两个视角（解析上界 + 实测验证），本轮把实测视角独立成 `_mve_results.json` 并补 FR-11 架构摘要 + FR-18 竞争格局。

### 排除的替代方案

- "因子 agent 包装而非独立实现判 MVE 无效"：否决。MVE 有效性判据是底层代码是否落实 MVE 纪律（per-block h / 公平对照 / 两阶段 FOE 等），不是"是否新写代码"。grep 核查 6 项纪律全落实，MVE 有效
- "strong HD-FEC 不可达判 fail"：否决。oracle 真 h 也不可达 = 物理上限（deep fade 主导），非估计器缺陷。NDA 全工作区赢 DA 即形态 C 成立（SPEC §5 辅助判定明示）

### 影响范围

- **下一步**：进 Step 5（Baseline 选定）。DA ML（pilot sp=4，pilot-aided 近最优）锁定为 FR-15 目标 baseline，NDA-ML 锁定为提出方法
- **feasibility_report.md**：本轮 MVE PASS 是 §D 维度 D 的实证，待写进 feasibility_report.md（守 TL-23 验证完再写——本轮已验证完，可写）
- **后续路径**：①写 feasibility_report.md 进 Step 5 ②视情况开 B7 Gardner TED FOE MVE（D004 已说"B7 待 NDA-ML MVE 完后视情况开"，现 NDA-ML Go，B7 可作并行第二候选或后置）③最后 B3 架构决策（多孔径阵列 vs 单链路）
- **形态 A+C 双增量叙事**：论文叙事框架确立（AWGN 频谱效率 + 星地湍流鲁棒性），MVE 实证支撑

### 来源

S004（本轮）+ 验证 `_mve_results.json` + 主线 grep 核查 `_time_domain_crlb.py` 6 项 MVE 纪律 + `SC-NDA-ML-MVE-SPEC.md` §5

## D-007: AWGN 场景重定义（B11 OFDM 参数 → 单载波参数）+ 线宽参数真相源统一

> status: active
> date: 2026-07-07
> 取代：无（贯彻 D002 重定位的遗留尾巴，不改 D002/D005 的判定逻辑，但 D005 的 AWGN 具体数字失效需重跑重判）
> 被取代：无
> 依据: 用户原话 voice 2026-07-07（"2 吧。这种问题不能留" + "一般来说，这种对比不应该是完全相同吗？怎么还分了俩？谁说的？"）+ D002（B11 重定位为理论参考不对标）+ sim-preflight `rules/param-source.md` v1.2.0（参数真相源统一规则）+ 子 agent 文献查证（Valjus sat.1553 §4.2 L438，存 `papers/doi/10.1002_sat.1553/content.md`）

### 决策

**AWGN 场景从"B11 复现场景（25GBaud/500kHz）"重定义为"我们方法的单载波 AWGN 验证（2.5GBaud/10kHz）"。线宽参数统一到 params.py 单一字段 `SystemParams.LASER_LW=10kHz`，消灭 3 套同义常量源（`_b11_params.CLW_B11` / `_time_domain_crlb.CLW_B11` / `params.B11Params.CLW`）+ 消灭函数默认参数固化（`doppler_phase(..., lw=LASER_LW)`）+ 消灭 sweep monkey-patch `__defaults__`。**

**三选项决策记录**（用户选 2）：
- 选项 1（双字段，AWGN 保 B11 25GBaud/500kHz，湍流保 10kHz）—— 否决：治标不治本，只把错误标清楚没纠正 D002 重定位没贯彻的根因
- **选项 2（单字段，AWGN 也改单载波 2.5GBaud/10kHz）—— 采纳**：科学对比要求两路径物理可比；D002 已把 B11 重定位为理论参考，AWGN 场景作为"NDA-ML vs DA ML"对比（都是我们自己的单载波方法）理应用单载波参数
- 选项 3（双字段，湍流改 50kHz 让 ΔνTs 可比）—— 否决：50kHz@2.5GBaud 典型性需文献论证，且不解决"对比本就该相同"的根本问题

### 理由

1. **D002 重定位的遗留尾巴**：D002 把 B11 从"直接对标 baseline"重定位为"NDA 升 M₀ 次幂思想源头"，我们的方法重定义为单载波时域 NDA-ML。但 D002 只剥离了 B11 的"方法思想"到 common/_recovery.py，**没清理 B11 的"场景参数"（25GBaud/500kHz OFDM）**，这些参数还留在 AWGN 信道（sc_nda_ml_sim.awgn_wiener_channel 读 P.SIGMA2_P_B11）。继续用 B11 场景参数 = 让"我们自己的方法对比"跑在别人论文的场景里，既不是复现 B11（D002 已说不对标），也不是诚实验证。

2. **param-source.md 失败模式 B 教科书案例**：线宽这一个物理量有 3 套数值源：
   - `params.py:SystemParams.LASER_LW=10e3`（湍流路径，WARNING）
   - `params.py:B11Params.CLW=500e3 + BAUD_RATE=25e9`（B11 参数族，OK）
   - `simulator/_b11_params.py:CLW_B11=500e3 + BAUD_B11=25e9`（**抄了一遍**，又标 B11 行号）
   - `explore/single-carrier-nda-ml/_time_domain_crlb.py:CLW_B11=500e3`（MVE 锚脚本**第 4 处**抄）
   用户原话戳穿："一般来说，这种对比不应该是完全相同吗？怎么还分了俩？谁说的？"——没人明确说，是 D002 重定位没贯彻的历史遗留。

3. **科学对比基本要求**：AWGN 场景比的是 NDA-ML vs DA ML（两个都是我们自己单载波方法），两路径符号率/线宽必须一致才物理可比。旧设定 AWGN=25GBaud/500kHz（σ²p=1.26e-4）vs 湍流=2.5GBaud/10kHz（σ²p=2.51e-5），相位噪声强度差 5 倍，跨场景结论不可比。

4. **导师意见 4（C4）直接满足**：简报 §3.1 写"激光线宽 500kHz"对 AWGN 成立、对湍流错（C4 违反）。统一后全场景 10kHz@2.5GBaud，前后一致。

5. **物理预期（TL-20）**：σ²p 从 1.26e-4 降到 2.51e-5（相位噪声弱 5 倍），NDA 升幂 ML 噪声方差放大减轻，AWGN fair gain 预期 ≥0.704dB（旧值），可能升至 0.8-1.0dB。pilot overhead 1.25dB 代价不变。**这是预期，必须实测。**

### 排除的替代方案

- "删 params.py 的 B11Params 类"：否决。explore/ 历史探针（_ber_oracle_upperbound/_crb_lower_bound）仍 import cfg.b11.M0_POWER 等。改 B11Params 的 CLW/BAUD_RATE/PN_VARIANCE 三字段标 DEAD 即可（保 import 不破，M0_POWER/HD_FEC_THRESHOLD/DFT_SIZE/CP_LEN 与线宽无关保持 active）。
- "回头救 500kHz 湍流"：否决。oracle 都不可达（raw BER 已核实），是真物理顶，改参数不影响这条结论。

### 影响范围

- **D005 AWGN fair gain +0.776±0.088 dB（5 seed）失效，需重跑重判**。weak/moderate/strong 不受影响（湍流路径参数没改，只改读法）。
- **MVE 一致性锚点必须同步重跑**：`_mve_results.json` 的 AWGN BER 用旧 σ²p=1.26e-4 跑的，consistency_check 会 FAIL 除非 MVE 也重跑。执行顺序硬约束：MVE → consistency_check → 主实验。
- **代码改动 9 文件**：params.py（B11Params 3 字段标 DEAD）/ common/_channel.py（doppler_phase 默认参数改 None）/ simulator/_b11_params.py（删 CLW_B11/BAUD_B11/T_S_B11，SIGMA2_P 从 LASER_LW 派生）/ simulator/sc_nda_ml_sim.py（rename + 加 sigma2_p 参数）/ explore/single-carrier-nda-ml/_time_domain_crlb.py（MVE 锚脚本必须跟）/ explore/single-carrier-nda-ml/sc_nda_ml_mve.py（meta 字段）/ simulator/run_linewidth_sweep.py（删 monkey-patch 改传参）/ simulator/run_kf_ablation.py + run_dd_kf_ablation.py（rename 同步）。
- **简报 C4 修正**：ADVISOR_BRIEFING.md §3.1/§4.1 线宽从"500kHz"改为"全场景统一 10kHz@2.5GBaud（ECL 典型，Valjus sat.1553 §4.2 L438）"。

### 来源

S005 续接（本轮参数统一+重跑）+ 用户原话 voice 2026-07-07（选项 2 拍板 + 反问戳穿根因）+ sim-preflight `rules/param-source.md` v1.2.0 + 子 agent 文献查证 Valjus sat.1553 §4.2

### 教训补充（2026-07-07 红旗核查发现）

D-007 执行中发现两个**同源问题**，属 param-source.md 规则精神的延伸，记录防复发：

1. **MVE-Formal 算法路径也算"真相源"**：执行中暴露 MVE `_time_domain_crlb.ber_nda_awgn` 用 `intra_block_tracking='none'`，Formal `sc_nda_ml_sim.ber_nda_awgn` 用 `'segmented'`，两者算法路径不统一。旧 σ²p 下差异恰好 <5% 一致性容差被掩盖（被当成"巧合 bit-exact"），新 σ²p 下差异放大到暴露才修。**这不是巧合，是 MVE-Formal 算法路径不统一的真 bug**。`param-source.md` 管"参数真相源统一"，**算法路径统一是其同源延伸**——consistency_check 的 5% 容差会放过路径差异，必须靠人工保证 MVE 和 Formal 用同一套估计器开关。

2. **结果目录"各写各的"是参数问题的下游**：发现 `sc_nda_ml_main`（D-007 新）和 `sc_nda_ml_main_improved`（旧）两目录并存且 AWGN 数字不同，且 `run_sdfec_eval.py` / `run_uplink_experiment.py` 仍引用旧目录 → 若跑 SD-FEC 会用旧 +1.483 数据得出错结论。已修引用 + 旧目录加 `_DEPRECATED.md`。**教训：参数真相源统一后，下游引用（脚本路径、results 目录、文档数字）必须同步清理，否则"统一"只做了一半。**

两条都已纳入 `usage-log 2026-07`。后续若新方向出现"MVE-Formal 路径差异"或"多 results 目录并存"，按 param-source.md 精神处理（统一 + 清理下游引用）。

## D-008: NDA-ML 漏 ML 加权 + 升幂未归一化（双 bug，vs VV 持平是 bug 非物理）

> status: **pending_fix**（bug 已确认，修复方案已定，sandbox 验证未做）
> date: 2026-07-08
> 取代：无（不推翻 D005/D-007 结论，但所有 vs VV/BPS ablation 结果待重判）
> 被取代：无
> 依据: 子 agent 精读 B11 PDF（`papers/doi/10.1109_lpt.2024.3523478/source.pdf`）Eq.12/16 + 代码核查 `common/_recovery.py:209-237` + 用户原话"这和 VV 持平真没问题吗？"（戳穿对照无意义）

### 决策（pending）

**Sandbox 验证后再决定全量重跑 or 降叙事。用户拍板：先 sandbox 验证再决定（防白跑）。**

### 双 bug 确认（公式证据）

**Bug 1 漏 ML 加权**：
- B11 Eq.16（p.561，df=0 τ=0 简化）：`φ̂ = (1/M₀) · 1ᵀΣ⁻¹ψ / 1ᵀΣ⁻¹1`，其中 `Σ⁻¹_{M₀ε} ∝ diag(|R(k)|²)`（p.560 协方差定义）
- 即 `φ̂ = angle(Σ |R(k)|² · ψ(k)) / M₀`（**加权** mean-angle，权重 = 升幂前接收幅值平方）
- 我们实现（`common/_recovery.py:232`）：`phi_raised = np.angle(raised.mean())`（**等权**）← 漏加权
- VV（`vv_cpr`）也是等权 mean-angle → 两者数学同族 → vs VV 持平是 bug 必然，非物理真实

**Bug 2 升幂未归一化**（子 agent 新发现，更隐蔽）：
- B11 Eq.5（p.560）：`y(k) = (R(k)/|R(k)|)^M₀`（**归一化**升幂，去幅度）
- 我们实现（`common/_recovery.py:213`）：`raised = rx ** M0`（未归一化，含 `|rx|^M₀` 幅度）
- 后果：若直接 `(raised * |rx|²).sum()` 补 Bug 1，实际权重变成 `|rx|^{M₀+2}`，**不是 B11 的 `|rx|²`**
- **两个 bug 必须一起修**，否则补了 Bug 1 也错

### 正确实现（子 agent 给，数学已验证）

```python
mag = np.abs(rx); mag[mag<1e-12] = 1e-12
yn = (rx/mag)**M0              # 归一化升幂（对齐 B11 Eq.5，去幅度）
w = mag**2                      # ML 加权 w_k = |R(k)|²
phi_est = np.angle((w*yn).sum()) / M0   # B11 Eq.16
```
segmented 分支段内同理：`seg_phi[k] = np.angle((w[lo:hi]*yn[lo:hi]).sum())/M0`。
FFT-df 分支（assume_df_zero=False）升幂步骤也改归一化 `yn`。

### 单载波迁移合法性

子 agent 确认：B11 的 R(k) 是 OFDM 频域子载波，但单载波时域样本 rx(k) 升 M₀ 次幂后相位模型 `y(k)=exp(jM₀(...))` 与 B11 Eq.5/6 同构，AOPN 方差 `σ²_ε(k)=N₀/(2|rx(k)|²)` 同构（高 SNR AWGN 相位近似）。**单载波 R(k)→rx(k)，加权 `w=|rx|²`，不取 DFT**。

### 理论预期（TL-20，sandbox 验证前先建）

ML 加权增益来源：
1. **(8,8)-16APSK 两环 4× 幅值差**（r1=0.547, r2=1.094，|rx|² 差 4 倍）——即使高 SNR 也存在
2. 噪声致幅值波动（低 SNR 明显）
3. 湍流 deep fade 致幅值波动（强湍流明显）

→ 预期加权在 (8,8)-16APSK + 强湍流场景 vs VV 能拉开差距；AWGN 高 SNR 收益可能小（样本 SNR 均匀）。
**关键不确定性**：当前 10kHz 低线宽下收益是否足够大可见。sandbox 先验证 AWGN + strong 两场景。

### 影响范围（pending sandbox 验证）

- **所有 vs VV/BPS ablation 结果（持平/+0.117）待重判** —— 若 sandbox 验证加权有效，全量重跑；若无效（加权在 10kHz 下收益可忽略），转降叙事
- **vs DA-ML 结论不受影响**（DA 对照不依赖 ML 加权，去 pilot 是真增量）
- **feasibility_report A'/§6 叙事再次待修**（D-007 红旗1 改的"AWGN 全维度赢"基于错误 ablation，pending 重判）
- **不变量**：D005/D-007 主结论（NDA vs DA 稳赢 1.3-2.5dB）不受影响

### 排除的替代方案

- "直接全量改 common/ 重跑"：否决（用户拍 sandbox 先验证，防白跑 + 防重蹈覆辙）
- "改回 500kHz 高线宽场景让加权收益明显"：否决（用户选先保持 10kHz 验证，且 500kHz@2.5GBaud 不真实 D-007 已定性）
- "降叙事不修代码"：pending sandbox 结果，若加权无效再走

### 教训（防新对话重蹈覆辙）

1. **sandbox 验证范围必须覆盖 vs 真 ML**：之前 sandbox（`explore/nda-awgn-tracking-sandbox`）只验证了 segK8 vs none（都是等权 mean-angle 变体），**没验证 vs B11 真 ML（加权版）**。新 sandbox 必须含"加权版 vs 等权版 vs VV"三方对照。
2. **一致性 bit-exact 不等于算法正确**：D-007 consistency 0.0000% PASS 是因为 MVE 和 Formal 都漏了同样的加权（都等权），"两者一致"只证明实现一致，不证明符合 B11。**一致性锚点只能查实现同步，查不了算法对错**。
3. **"vs 经典 baseline 持平"是高优先警报信号**：VV 是 1983 升幂 mean-angle 祖师爷，NDA-ML 若与它持平，要么数学同族（创新性质疑），要么对照不公平。**任何"与祖师爷方法持平"的结论出现时，必须立即查数学同族性，不能当"合理结果"接受**。
4. **D-007 选 10kHz 低线宽掩盖了这个 bug**：低线宽下样本 SNR 均匀，加权≈等权，bug 不易暴露。参数选择（D-007）和算法验证（本 D-008）是耦合的——改参数后必须重新审视算法实现是否在新区间仍正确。

### 来源

用户附和性核查"这和 VV 持平真没问题吗"（戳穿对照无意义）+ 子 agent 精读 B11 PDF Eq.12/16（`papers/doi/10.1109_lpt.2024.3523478/source.pdf` p.560-561）+ 代码核查 `common/_recovery.py:209-237`（等权 mean-angle + 未归一化升幂）。

## D-009: NDA-ML vs VV 体检定论 + D-007 线宽选择复核（交叉验证后：D-007 基本没错，W+ 路径依据不足）

> status: **active**（体检定论已确立；线宽修正路径 W+ 经交叉验证后依据不足，已排除；方法方向 pending 用户）
> date: 2026-07-08（本对话续接，含交叉验证修正）
> 取代：无（不修正 D-007，D-007 选 10kHz 跟实测主流一致；不推翻 D005/D-008 主结论）
> 被取代：无
> 依据: sandbox 三方对照（`explore/nda-awgn-tracking-sandbox/_ml_weighting_results.json` + `_vv_vs_nda_checkup.json` + unwrap 验证 `_verify_unwrap_order.py`）+ 子 agent 精读 B11 PDF + 子 agent 调研近年单载波 NDA-ML + 主线核查 Valjus §4.2 原文 + **子 agent 星地 FSO 线宽交叉验证（4 篇确切值：22/20/80kHz + Valjus 0.1-1MHz）**
> 触发原话: 用户 D-008 起点 → "和 VV 有区别吗？别实际上是一个？" → "为啥不直接用 VV？" → "不能是 E 或 Z" → "A. 先查证星地 FSO 线宽分布"

### 决策（pending 用户拍板方法方向）

**体检定论（已确立，不可推翻）**：
1. **ML 加权（B11 核心）在单载波时域全线无用**（11 扫描点加权 vs 等权 ≤1.7%），加权收益来自频域子载波/多环幅度离散，单载波时域 AWGN 物理机制不存在
2. **10kHz（实测主流）下 NDA-ML 跟 VV 数值上是一个**（加权/等权 vs VV 全程 |rel|<5%），D-008 教训3 警报成立
3. **segmented 块内跟踪在 ≥200kHz 拉开 VV -14%~-19%**，但 ≥200kHz 不在实测主流星地 FSO 区间（10-80kHz ECL），所以这个增量在真实场景看不见

**线宽修正路径 W+ 排除**：子 agent 交叉验证 4 篇确切线宽值（22/20/80kHz ECL 实测 + Valjus 0.1-1MHz 设计容限），实测主流星地 FSO 用窄线宽 ECL，不支持改到 100kHz-1MHz。D-007 选 10kHz 跟实测主流一致。

**方法方向 pending**（用户排除 E 找老师 + Z 转系统层，剩 X/其他）：
- 用户已明确"不能是 E（找老师）或 Z（转系统层）"——要保算法层创新
- 但体检定论显示：实测主流场景（10-80kHz）下 NDA-ML 算法层跟 VV 同族没增量
- **[2026-07-08 续接修正]** D-009 原报"segmented 在 ≥200kHz 拉开 VV -14%/-18% 是真增量"被**上行+VV Nw 扫描实验推翻**（见下"层 4 追加"）—— VV 把 Nw 从 64 调到 16 即反超 NDA-segmented（200kHz 赢 14%，500kHz 赢 68%）。segmented 跟踪**也无真增量**，原 D-009 的"高线宽 niche 场景"路径 W 排除。
- 矛盾：要保算法层创新 vs 实测主流+高线宽+上行场景算法层都没真增量（VV 调参就赢）

### 三层证据链

**层 1: sandbox 体检定论（实测）**

三方对照（加权 vs 等权 vs VV）跨线宽/调制/湍流 3 维度扫描：
- **ML 加权全线无用**：11 个点加权 vs 等权 BER 差 ≤1.7%（`_vv_vs_nda_checkup.json` sweep1/2/3 加权 vs 等权列）
- **拉开 VV 的是 segmented 跟踪非加权**：sweep1 线宽扫描 200kHz/500kHz 时加权 vs VV -13.9%/-19.4%，但**等权 vs VV 也 -13.8%/-18.0%**（主线独立从 JSON 原 BER 重算，子 agent 报告未直接给此列，归因"加权拉开"是错的）
- **拉开只发生在 ≥200kHz**：10-100kHz 全维度三方持平（加权/等权 vs VV 均 |rel|<5%）
- unwrap 顺序验证（`_verify_unwrap_order.py`）：第一轮 sandbox 报"加权 seg 暴涨 272%"是 brief 公式 unwrap 顺序 bug 伪影（升幂域 unwrap 才对，非还原域），修正后加权 seg 跟等权 seg bit-exact

**层 2: 子 agent 精读 + 调研（文献）**

- **B11 +2dB 来源**（子 agent 1，精读 PDF p.560-562）：B11 是 OFDM 频域，baseline = PA/DA-ML（频域方法），+2dB 是 OFDM 域 NDA-ML vs DA-ML。**B11 未对比加权 vs 等权（VV 形式）**。B11 信道是 AWGN+Wiener PN（**无频率选择性**），加权 |R(k)|² 来源是 APSK 多环幅度离散（非频率选择性）——子 agent 1 戳穿我上轮"加权增益来自频率选择性"的错误推断
- **近年单载波 NDA-ML 论文**（子 agent 2，12 组 query 召回 80 篇筛 6 篇）：**基本不拿"超 VV"当卖点**。靠 ML 最优性/相位噪声建模/联合估计/免导频/能效等。Wang/Kam 2024（JPhoton，就是 B11 同团队 Kam 的单载波线）改进 VV 靠 Wiener PN 最优 LMMSE 权重（非样本幅度加权）。**(8,8)-16APSK + 单载波 NDA-ML + 星地 FSO 组合文献空白**

**层 3: 主线核查 D-007 依据 + 子 agent 星地 FSO 线宽交叉验证（修正早结论）**

**初判（过早）**：主线读 Valjus §4.2 L438 "In general, a linewidth between 0.1 MHz and 1 MHz could be expected" + L395 "low-cost DFB lasers"，初判 D-007 选 10kHz 选错。

**交叉验证（修正初判）**：派子 agent 查 2020+ 星地 FSO 实测/仿真论文的线宽分布，结果：
| 论文 | 场景 | 线宽 | 激光器 | DOI |
|---|---|---|---|---|
| Naghshvarianjahromi 2022 Sensors | 地↔GEO 仿真 | 22 kHz | ECL | 10.3390/s22093435 |
| Anon 2023 Opt.Commun.129312 | LEO 星→地 FPGA 实时实验 | 20 kHz | TTX1995 ECL | 10.1016/j.optcom.2023.129312 |
| 2024 Opt.Express OE.520452 | FSO 20km PM-QAM | 80 kHz | 未明示 | 10.1364/OE.520452 |
| Valjus 2025 Sat.Commun. | OSL 综述 | 0.1-1 MHz | DFB（低成本设想）| 10.1002/sat.1553 |

**关键修正**：
- **实测/演示型星地 FSO 主流用 ECL ~20kHz**（3 篇确切值 22/20/80kHz），D-007 的 10kHz 跟实测主流一致
- **Valjus 的 0.1-1MHz 是"DFB 低成本场景的设计容限预期"**（L438 上下文是讨论"ΔwTs 高时 cycle slips 严重"的设计区间，非主流实测值），L395 "DFB" 是说" terrestrial 用 DFB"的背景，不是"OSL 必须用 DFB"
- **D-007 选 10kHz 没错**（跟 ECL 实测主流一致），但 D-007 引用 Valjus 时确实没读清"expected"语境（文献引用精度问题，非选错值）
- 样本局限：4 篇确切值偏少，3 篇付费墙未取（Liu 2025/Walsh 2022/Li 2022），但趋势清晰（实测主流窄线宽 ECL）

**结论修正**：走 W+（修正线宽到 100kHz-1MHz）**依据不足**——实测主流不支持，Valjus 的 0.1-1MHz 是设计容限非典型值。segmented 创新点（要 ≥200kHz）在实测主流场景（10-80kHz）下**仍不成立**。

**层 4 追加（2026-07-08 续接，推翻层 1 的 segmented 增量结论）**

用户追问两问触发：① 高线宽 segmented 增益是不是 VV 也有 ② 上行验证（导师要求）漏了 vs VV/BPS 对照。派子 agent 跑三实验（`_uplink_vv_check.json`），主线独立核查数字属实：

- **实验 1（上行 vs VV/BPS/DA，5 seed 工作区）**：NDA vs VV +0.090/+0.119 dB、NDA vs BPS +0.113/+0.141 dB（**全"中间"档 <0.3dB，持平**）；NDA vs DA +2.48/+3.07 dB（拉开，复现主实验上行方向）
- **实验 2（AWGN 高线宽 VV Nw 扫描，决定性）**：
  | 线宽 | NDA-seg | VV Nw64（默认）| VV Nw16（调优）|
  |---|---|---|---|
  | 200kHz | 4.62e-3 | 5.36e-3（VV 输 16%）| **3.98e-3（VV 反超 14%）**|
  | 500kHz | 1.81e-2 | 2.21e-2（VV 输 22%）| **5.89e-3（VV 大赢 68%）**|
- **实验 3（上行 VV Nw 扫描）**：VV Nw=32/64/128 时追上 NDA-seg（差<5%）

**层 1 推翻**：D-009 原"segmented 在 ≥200kHz 拉开 VV -14%/-18% 是真算法增量"**是错的**——VV 把 Nw 从默认 64 调到 16，立刻反超 NDA-segmented（500kHz 赢 68%）。**segmented 跟踪也无真机制增量**，D-009 的"高线宽 niche"路径 W 排除。原 D-009 层 1 关于 segmented 的归因（"拉开 VV 的是 segmented 跟踪"）数字对但归因错——真因是 VV 默认参数保守，不是 segmented 强。

**最终定论（2026-07-08，覆盖 D-009 层 1-3）**：
1. ML 加权全线无用（11 点 ≤1.7%，不变）
2. segmented 跟踪也无真增量（VV Nw=16 即反超）
3. 上行/下行/AWGN/湍流/低线宽/高线宽，**NDA-ML vs VV/BPS 全场景持平**（0.06-0.14 dB，中间档）
4. **唯一真实增量 = vs DA-ML 频谱效率**（上行 +2.48/+3.07、下行 +1.35~1.71 dB，pilot overhead 真代价）
5. NDA-ML 在估计器算法层**全面跟 VV/BPS 同族持平，且 VV 调参就赢**——没有"超经典方法"的硬增量空间

**方法方向现状**（用户排除 E/Z 后）：算法层已证无真增量空间，要保算法层创新 = 必须换方法（X 路线改进 VV，但 D-009 层 4 已证 VV 调参就赢 NDA，改进 VV 也难超 VV 本身）。矛盾未解，pending 用户决策（可能需重新考虑 E/Z）。

### NDA-ML vs VV 精确关系（回答用户"实际上是一个吗"）

| 维度 | 关系 | 10kHz 下 |
|---|---|---|
| 算法内核（升幂 mean-angle）| **同族** | 同 |
| 权重（加权 vs 等权）| 数值不同（数学）但退化（物理）| 退化到等权 |
| 块结构（逐块+segmented vs 滑窗逐符号）| **真差异** | 不产生 BER 差异 |
| **数值层（10kHz）** | **实际是一个** | 持平 <5% |
| 数值层（≥200kHz）| segmented 拉开 VV -14%~-19% | NDA-ML 优 |

### 影响范围（pending 用户拍板）

- **D-007 线宽选择**：10kHz 可能要修正回 Valjus 区间（100kHz-1MHz）。但 D-007 的"参数真相源统一"原则不动（仍单字段 LASER_LW，只是数值改）。需重新论证典型性（Valjus + 其他文献交叉验证，目前主要靠 Valjus 一篇）
- **D005/D-007 主结论**（vs DA-ML +1.3~2.5dB）：10kHz 下仍成立（DA 对照不依赖加权/segmented）。但若改高线宽，需重跑主实验 + 所有 ablation 重判
- **D-008 双 bug**：加权补对在数学上正确但物理收益不可见（10kHz 下），代码层补不补 pending
- **方法方向**：算法层创新 = segmented 块内跟踪（≥200kHz 拉开 VV），不是 ML 加权。走 X（换改进 VV）/ W（segmented + 高线宽）/ 其他 pending 用户

### 排除的替代方案

- "立即全量改线宽重跑"：否决（pending 用户拍板 + 需先补充文献交叉验证 Valjus 的 0.1-1MHz 不是孤证）
- "坚持 10kHz 承认算法层没创新"：用户明确拒绝（"不管怎么说不能是 E 或 Z"，E=找老师确认方向，Z=转系统层；意味着要保算法层创新）
- "降叙事写等权近似"：pending，若用户选"保 10kHz 不改"则只能走这条

### 待补充证据（TL-23 验证完再下结论）

1. **Valjus 的 0.1-1MHz 需 2-3 篇其他星地 FSO 文献交叉验证**（目前主要靠 Valjus 一篇 + DFB 常识）。子 agent 文献调研任务已派但未返回，主线 grep 本地文献找到 1911.01585（光纤 100kHz，非星地）。**需要专门查星地 FSO 实测论文的线宽**
2. **segmented 在 100kHz（非 200kHz）能否拉开 VV**：sweep1 显示 100kHz 加权 vs VV -2.2%（持平），但 200kHz 才 -13.9%。若 Valjus 区间下限 100kHz 仍持平，要走 W 可能需要 200kHz+（ΔνTs=8e-5，需论证）

### 教训（新增）

5. **"已查证文献 X"必须读原文数值不能只引位置**（FR-26 强化）：D-007 引"Valjus sat.1553 §4.2 L438"但没读 L438 原文"0.1-1MHz typical"，锁定 10kHz。证据链断在"引位置"而非"读数值"。
6. **子 agent 报告的归因要独立核查**：体检子 agent 报"加权拉开 VV"，主线独立算"等权 vs VV"发现等权也拉开，真因是 segmented 非加权。**不能信子 agent 的因果归因，只信其原始数字，归因主线自己做**。
7. **参数选择和算法验证耦合**（D-008 教训4 延伸）：D-007 选 10kHz 掩盖了所有算法创新（加权/LMMSE/segmented 都要 ≥200kHz）。参数选错 = 算法验证全废。改参数后必须重新审视算法在新区间是否正确 + 是否有增量。

### 来源

主线核查 Valjus sat.1553 §4.2 原文（L387-440）+ sandbox 三个 JSON（`_ml_weighting_results.json` / `_seg_rootcause_2x2.json` / `_vv_vs_nda_checkup.json`）+ unwrap 顺序验证（`_verify_unwrap_order.py`）+ 子 agent 精读 B11 PDF + 子 agent 调研近年单载波 NDA-ML + 用户连串追问（voice 2026-07-08：D-008 起点 → "和 VV 有区别吗" → "为啥不用 VV" → "不能是 E 或 Z"）。

## D-010: 导师确立 baseline 选取标准（5 条）+ 方向/复现源质量门

> status: active
> date: 2026-07-08
> 取代：无（确立老师权威标准，不取代 D005/D-007/D-009，但作为后续 baseline 池建设的约束）
> 被取代：无
> 依据: 用户转述导师电话原话（voice 2026-07-08 电话段 4 条）+ 用户补充"中心思想就是上面的"

### 决策

导师主动来电确立 baseline 选取 4 条 + 方向/复现源质量门 1 条，共 5 条标准。**这 5 条是后续 baseline 池建设 + 方向锚定的硬约束，执行优先级等同 D005 务实路线。**

#### baseline 选取 4 条（找 baseline 时用）

1. **同场景**：星地湍流信道（satellite-to-ground FSO + 大气湍流）
2. **同类型层级**：载波同步 / 定时同步 / 均衡这一层（DSP 物理同步层），**不再深入到子层**（钻到"载波相位恢复"子层会找不到 baseline）
3. **不找接近方法当 baseline**：禁止近亲 baseline（NDA-ML vs VV 数学同族=近亲，VV 不该当主 baseline）
4. **近年 + 权威**：2022+ 年 + IEEE Trans 级（TWC/TMC/TVT/JLT/JOCN/OL/OE 等）

#### 方向/复现源质量门 1 条（找方向/复现时用）

5. **只看够好的文章**：找方向 + 复现别人时必须挑扎实的权威 Trans，避开 letter/仿真不全/挑弱 baseline 凑数的论文——否则容易搞到假的不可复现

### 理由

老师电话原话明确（voice 2026-07-08 电话段）：

- "找baseline，找相同场景（比如说星地湍流信道）、相同类型（比如说，载波同步、定时同步、均衡这一层）就行，不要再深入了，不然找不到，而且万一出现了麻烦的问题不好解释"
- "尽量别找接近方法作为baseline"
- "要找近几年的，足够权威的作为baseline"
- "找方向的和复现别人时候，一定要看那些够好的，不然容易搞到假的不能复现"

#### 对当前处境的直接含义（5 条跟我们已有发现的互相印证）

- **标准 3（不找接近方法）↔ D-009 NDA-ML vs VV 全场景持平**：VV 是 NDA-ML 同族盲估计，**本来就不该当主 baseline**。这条给路线 A 的 baseline 结构（主比 DA-ML，VV 一句带过）背书。
- **标准 2（不深入子层）↔ B11 是最接近但偏薄**：之前在"载波相位恢复"子层找 baseline，确实难找（B11 是 CO-OFDM 频域无湍流）。放宽到"载波同步/定时/均衡层"，候选池会大很多。
- **标准 4（近年权威）↔ B 档 12 篇偏薄**：B 档有 LPT/OE 短文，作候选可以，**作 baseline 偏薄**。baseline 要补 IEEE Trans 级。
- **标准 5（看够好的）↔ LMMSE 复现失败教训（S008）**：LMMSE（#15 JPhoton）PDF→md 丢公式致复现失败，正是老师说的"搞到假的不能复现"风险。
- **标准 1（同场景星地湍流）↔ D006 open gap（B5/B7/B11/B12 全无湍流）**：我们要找的 baseline 必须建模星地湍流——而这恰恰是 B 档主流候选都没做的。**这是一个结构性张力**：老师要"同场景星地湍流"的 baseline，但同族近期论文大多没建模湍流。可能需要：(a) 放宽到"有湍流建模的同步/均衡层 Trans"（不限载波相位恢复子层）；(b) 或用"无湍流场景的 baseline + 我们加湍流做场景迁移对照"。

### 工具链现状（回答老师"trans 不好检索"是否成立）

老师电话前提"trans 好像别的源不好检索"——核查后对**我们这套工具不成立**：

| 层 | 工具 | 对 IEEE Trans 覆盖 |
|---|---|---|
| 搜元数据 | `tools/search`（S2/OpenAlex/SerpAPI/Exa） | ✅ venue/年份/被引数/DOI 全有，实测返回 "IEEE TMC" 等标注 |
| 下全文 PDF | `tools/blit --source ieee --download` | ✅ 校园网 IP 机构认证直下，50 次/会话 |

**但 blit 有一个缺陷已修**：`tools/blit.py:ieee_search`（原 217-243 行）venue 字段硬编码空串，搜出来分不清 Trans 还是会议——这可能是"不好检索"体感来源之一。本轮已加 description/publisher 元素解析（多策略 + fallback 正则），venue 现在能提取了。

### 排除的替代方案

- "钻到载波相位恢复子层找精准 baseline"：否决（老师明说"不要再深入了，不然找不到"）
- "用 VV/BPS 当主 baseline"：否决（老师明说"尽量别找接近方法"，D-009 已证 VV 跟 NDA-ML 同族持平）
- "用 letter/短文当 baseline"：否决（老师明说"足够权威"，标准 4 要求 Trans 级）

### 影响范围

- **下一步 baseline 池建设**：按 5 条标准检索（场景词 satellite-to-ground FSO turbulence + 类型词 carrier synchronization/timing recovery/equalization + 排除近亲 NDA-ML/VV/BPS + 过滤 2022+ IEEE Trans）
- **工具链**：blit venue 解析已修，待实测验证（下次跑 blit --source ieee 时确认 venue 字段非空）
- **路线 A/B 决策**：5 条标准跟两条路线正交（baseline 池是共用基建），不直接定 A/B，但标准 3（不找接近方法）给路线 A 背书，标准 1（同场景湍流）给路线 B 留空间
- **候选框架/skill 更新点**（用户提"后面可以改协议或者 skill 用"）：
  - `stages/groundwork.md` S4-7 baseline 合法性段可补"baseline 选取 4 条标准"（同场景/同类型层级/不找接近方法/近年权威）
  - `code-quality.md` 方法论适配性矩阵可补"复现源质量门"（标准 5：只看够好的，避 letter/仿真不全）
  - `tools-guide.md` §2 可补"IEEE Trans 检索策略"（search 搜元数据 + blit 下全文两步配合）
  - 这些更新**本轮不做**（守"先测不改协议"不变量），记录候选点待专题稳定后批量改

### 来源

用户转述导师电话原话（voice 2026-07-08 电话段 4 条原话 + "中心思想就是上面的"确认）+ 工具链核查（tools/blit.py:217-243 venue 硬编码空串 + tools/search venue 字段实测有值）+ D-009 NDA-ML vs VV 持平结论 + D006 open gap（B5/B7/B11/B12 全无湍流）。

## D-011: A1 参数适配（NDA 块长自适应 K）FAIL — 自适应策略无可实现增量

> status: active
> date: 2026-07-08
> 取代：无（记录 A1 适配扫描方向失败，不推翻 D005/D-007/D-009/D-010）
> 被取代：无
> 依据: 验证 `_a1_adaptive_k_results.json`（8 点 5 seed）+ 标定 `_a1_calibration.json`（35 点 4 判据 ρ）+ 主线独立核查 by_seed 原始数字 + adaptation-scan.md A1 失败信号判据
> 触发原话: 无（技术推导——A1 FAIL 判定基于实测 gain vs K16 = +0.000 dB + ρ<0.6 数字 vs TL-20 锚点 E4/E5 阈值，非用户 voice 触发；用户在实验前委托"不知道，都试试"是判据选择委托非方向决策）

### 决策

**A1 参数适配方向（NDA-ML 块长自适应 K 策略）经两阶段实验验证 FAIL，排除作算法层创新点。** 自适应-J4（可实现版）aggregate gain vs 固定 K=16 = +0.000 dB（退化到 always-K16），0/8 点 CI 显著赢 K16。即使 oracle 上界（非可实现）也仅 -0.474 dB 且 -2.46 dB 全来自 1000kHz 一个非主流极端点。

**核心失败机制**（三条，匹配 adaptation-scan.md A1 失败信号"最优值不随条件变 → 无自适应空间"）：
1. 最优 K 变化范围窄：跨线宽 K∈{8,16,32}，主战场 K=16（35 点中 71% 跟 oracle 持平）
2. 判据层失效：4 判据 Spearman ρ 全 <0.6（最强 0.361），J4（线宽代理）修正 unwrap bug 后仍 ρ=-0.019
3. 唯一显著点不在主流场景：1000kHz（D-009 已确认实测主流 ECL 10-80kHz）

### 理由

**阶段 1 标定（35 点单 seed）**：4 判据（J1 升幂幅值方差 / J2 scintillation / J3 盲 SNR / J4 升幂相位差分方差）vs 最优 K 相关性全不达可靠映射阈值 |ρ|≥0.6。J4 发现 unwrap bug（M₀=8 升幂相位 unwrap 路径错乱，D-009 unwrap 教训复发），修正为 mod 2π 相位增量后仍 ρ=-0.019（物理上：升幂后相位增量被 AWGN 噪声主导，单块 256 样本估计方差大）。

**阶段 2 验证（8 点 5 seed）**：adaptive-J4（用修正 J4 阈值映射）退化为 always-K16（J4 无预测力），gain 恒 0.000。oracle 上界拆解：1000kHz -2.463 dB（唯一显著）/ moderate -0.363 / strong -0.335 / 其余 ≤0.21 / AWGN100kHz +0.000。去掉 1000kHz 后 oracle aggregate 仅 -0.19 dB（薄增益区间下沿，且需完美判据实际达不到）。

**VV 参照**：VV Nw=64（固定）aggregate vs K16 = +0.219（稍差 K16），但 D-009 层 4 已证 VV 调 Nw=16 高线宽反超。"自适应"是普适思路（VV 也能自适应 Nw），NDA 的 K 自适应无独占优势。

### 排除的替代方案

- "用更强判据（如 LMMSE 权重 / 深度学习）"：否决。当前 4 判据已覆盖幅值/功率/SNR/相位四类物理量，且物理根因是"主战场 K=16 普适 + 升幂后相位增量被噪声主导"，换判据不改变这两个物理事实。
- "加更多线宽点找自适应空间"：否决。已扫 6 线宽点（10-1000kHz），信号集中在 1000kHz 一个极端点，加更多点不改变"主流场景 K=16 普适"结论。
- "用 K=32 作默认（高线宽最优）"：否决。K=32 在低线宽灾难（10kHz gain vs K16 = +2.00 dB，100kHz +2.35 dB），固定 K=32 全场景 aggregate +0.488 dB 远差于 K=16。

### 影响范围

- **A1 方向排除**：不能用"NDA 块长自适应 K"作算法层创新点
- **4 种适配扫描进度**：A2 已做（D002 频域→时域）/ A3 FAIL（S013）/ **A1 FAIL（本轮）**/ A4 待返回。3/4 已闭合且全 FAIL/已做。
- **防御性材料保留**：A1 实测数据 + 物理理由作防御性材料——被问"能不能自适应 K"时有实测回答"不能"
- **下一步 pending A4**：若 A4 也 FAIL → 4 种适配扫描全闭合，NDA-ML 算法层无显著增量方向确认（D-009 结论再加固），需回主对话想别的方向

### 教训（防新对话重蹈覆辙）

8. **"最优参数随条件变"不等于"自适应有空间"**：A1 信号判据（adaptation-scan.md）说"参数最优值随条件变 → 自适应有空间"，但实测显示 K 确实随线宽变（8→32），可这个变化范围窄 + 主战场有普适固定值（K=16 在 71% 场景持平 oracle）+ 判据无法捕捉 → 自适应无可实现增量。**A1 信号判据需补"变化范围是否足够大 + 是否存在普适固定值 + 判据能否预测"三重检验**，不能只看"是否变化"。
9. **unwrap 对升幂相位不可用（D-009 教训复发）**：M₀≥4 升幂后相位 `M₀·θ` 极易超 2π，`np.unwrap` 会路径错乱。线宽代理类判据必须用 mod 2π 相位增量（`(diff+π)%(2π)-π`），不能 unwrap。这是 D-009 unwrap 顺序 bug 后第 2 次同源问题。
10. **子 agent 的映射拟合要核查是否退化**：A1 子 agent 报告 J4 映射 thr=3.42 accuracy=0.40，表面像拟合了，实际是退化到 always-K16（accuracy=K16 baseline rate）。**核查方法**：看映射在标定集各 K 档的预测分布，若全预测同一档 = 退化。

### 来源

验证 `_a1_adaptive_k_results.json`（8 点 5 seed，adaptive_oracle ≡ fixed_k32 by_seed 一致已核查）+ 标定 `_a1_calibration.json`（35 点 4 判据 ρ）+ 主线独立核查 1000kHz 点 by_seed 原始数字 + adaptation-scan.md A1 失败信号判据 + TL-20 锚点 E4/E5 + D-009（K 扫描前置数据 + unwrap 教训 + 实测主流线宽 10-80kHz）。

---

## D012: 激活 B10/B12 高阶调制 CPR 组合方法 Step 4a 大包

> status: superseded
> date: 2026-07-25
> 取代：无（恢复本专题已有 B10/B12 Step 1–3 证据为当前 carrier）
> 被取代：D013
> 依据：literature_notes L20/L22；B10/B12 gw-read；dual-pol D066；live-test S001

### 决策

1. 当前 formal carrier 从 Pilot-Jones 转到
   `HIGH_ORDER_CPR_COMBINATION_METHOD`，仍处于 GW Step 4a。
2. 复用 B10 pilot-RLS 与 B12 frequency-domain pilot/MAP 已完成的 Step 1–3
   证据，不重做全量文献检索；但必须在 T006 source closure 中逐项恢复其信息源、
   输出动作、场景边界和参数 provenance。
3. T006 先在 uniform 16-QAM、星地 GG 湍流、合法 CFO/linewidth 范围和公平
   pilot overhead 下建立 strongest-simple baseline 与 truth-assisted Kill bound。
   所有 primary cells 的合法 headroom CI upper `<0.5 dB` 时立即 Kill，不建设方法。
   这是用户批准的 **T006 专属 infrastructure-investment gate**，显式覆盖本专题
   不变量 2/4/6 中“FR-21 <0.5 dB 只作参考”的旧校准；不反向改写其他历史候选。
4. headroom 存活时，同一包直接实现并比较：
   - pilot-RLS coarse → MAP residual cascade；
   - receiver-visible confidence/innovation gate；
   - adaptive-forgetting RLS。
   必须同时胜过 `B*` 和 B10/B12 standalone 最强组件，才可判组合方法 Go。
5. T006 止于 provisional Step 4a verdict；不进入 Step 5、Contract 或 Execute，不改
   shared generator，不建设通用基础设施。

### 理由

- 用户明确优先追求可包装方法和可用产出。B10/B12 有现成全文、精读、16/256-QAM
  方法链和 simulator 资产，比再开纯分析方向更可能在一个大包内形成方法。
- 组合不是无约束“拼算法”：三个候选分别对应 cascade、conditional routing 和
  state adaptation，均有不同输出动作且可与 standalone component 做合法消融。
- headroom 前置门阻止在物理空间不足时继续耗费实现成本。

### 排除的替代方案

- 不继续 Pilot-Jones：D066/V040 已关闭当前 complex component rescue axis。
- 不优先 residual/CMA correction：当前仍缺 receiver-visible information increment。
- 不恢复 P03：其主要阻断是 infrastructure/domain adequacy，不是短期方法形成机会。

### 影响范围

- 本专题新增 S014 与 T006 carrier。
- 当前 action class 仅 `HIGH_ORDER_CPR_COMBINATION_METHOD_PACKAGE`。
- 原 A4 adaptive CPR、B10/B12、NDA-ML 资产保持历史证据，不因本次切换被改写。

---

## D013: 拒收 T006 科学裁决并切换到 B1 自适应相位估计窗

> status: superseded
> date: 2026-07-25
> 取代：D012（仅取代其“当前 carrier”身份；D012 对 T006 的历史授权仍有效）
> 被取代：D014
> 依据：V001 / S015 / T006 source、raw rows 与主控数值探针

### 决策

1. T006 的工程产物按 `PARTIAL_REUSABLE_IMPLEMENTATION` 保留，但拒收
   `HEADROOM_SURVIVES` 和 `PROBLEM_SURVIVES_METHODS_FAIL` 两项科学裁决。
2. B10/B12 组合族状态为 `UNRESOLVED_IMPLEMENTATION_INVALID`，不得写成方法机制
   已失败，也不得把 9–20 dB 退化写入论文。
3. 不再为 T006 开无界修复包。原因不是一次局部 bug，而是 B10 source identity、
   B12 公式身份、pilot/data channel、oracle/evaluation 与统计门同时失效；继续修
   会把当前主线锁进实现考古。
4. 当前 formal carrier 切换为 `B1_ADAPTIVE_PHASE_WINDOW`，仍在 GW Step 4a。
   复用 B1 已完成的 Step 1–3 证据：固定窗相位估计在大 SNR 波动下的不足由
   sat.1553 明确提出，最优窗长由 SNR/phase-noise 比驱动。
5. 下一包 T007 必须先证明“最优窗确实随可观测条件变化且不存在普适固定窗”；
   该门失败立即 Kill。门通过后同一包实现三种 receiver-visible 自适应窗策略并做
   paired test，不另开小修包。

### 理由

- T006 的唯一 `0.6059 dB` survivor 被单个近随机 seed 主导：该 seed 贡献总和的
  `91.7%`；median 仅 `0.0447 dB`，删去最大值后 mean 仅 `0.0560 dB`。
- 当前 B10 在纯 CFO、20 dB AWGN 的 source-native probe 中，即使使用连续 128
  导频也得到 `0.158–0.404 BER`，CFO 斜率估计与真值相差多个数量级。这是实现
  身份失败，不是低线宽下机制无价值。
- B1 的方法形态更轻：复用现有 VV/pilot CPE，只新增条件估计、有限窗集合和
  hysteresis；可以在一个执行对话内完成理论门、方法和正式 test，符合“多做但不
  陷入一块”的用户约束。

### 排除的替代方案

- 不做 T006 全量修复：多层语义同时失效，且 robust headroom 信号薄。
- 不立即做 B9 DRE：DRE 依赖 oversampled waveform、低分辨率 DAC、匹配滤波与
  block-wise Viterbi，容易再次出现“关键链路没实现却先跑结果”的身份风险。
- 不恢复 Pilot-Jones/P03/Science Scout：现有 formal owner 没有给这些线新的动作授权。

### 影响范围

- 新建 S015/V001；live-test control epoch 递增到 9，T007 绑定
  `ADAPTIVE_PHASE_WINDOW_METHOD_PACKAGE`。
- T006 代码、raw artifacts 和 commit 不回滚、不改写；只修正 current scientific view。
- 仍止于 GW Step 4a，不进入 Step 5、Contract 或 Execute。

---

## D014: T008 身份修复失败，B1 返回候选池

> status: superseded
> date: 2026-07-26
> 取代：D013（仅取代当前 carrier 与下一动作；D013 对 T007/T008 的历史授权保留）
> 被取代：D015
> 依据：验证 V002 + live-test D002/CP008 + T008 task/runner/data-only 重算

### 决策

1. T008 的 `KILL_NO_ADAPTIVE_WINDOW_SPACE` 不接收；formal disposition 为
   `SCIENCE_VERDICT_REJECTED / BLOCKED_IDENTITY`，metric 子状态为
   `UNRESOLVED_NO_CROSSING`。
2. B1 family 不关闭，返回候选池；当前实现不再追加修复包。
3. 本专题暂时没有 active carrier。下一 carrier 必须由 live Goal campaign remap
   明确选择后，再以新的 formal 决策激活。

### 理由

- 所有 primary cell 都没有真实 HD-FEC crossing；执行器违反冻结任务，使用
  非 FEC 区域的 log-BER slope 生成 `dB-equiv` 触发 `<0.5 dB` Kill。
- 所谓 corrected oracle gate 只比较 B-cond 与 B*；per-block oracle 还跳过
  `N>BLOCK=100`，而冻结 B*=256，故 oracle identity 并未闭合。
- pilot 覆盖符号仍按原 data bits 计错，逐窗 VV 又缺跨窗 π/2 unwrap。去 pilot
  后 20 dB 仍有 QPSK BER 0.174–0.178、16QAM 0.272–0.280，不能称 working region。
- raw/fresh-test artifacts 未进入 commit，formal evidence closure 不完整。

### 排除的替代方案

- 不作 local/family Kill：当前数据只说明受污染 evaluator 下两个 fixed baseline
  接近，不能证明合法自适应空间消失。
- 不做第三个 B1 修复包：当前 mission 已连续八包无方法增量，继续修会偏离
  method-production 目标。

### 影响范围

- master-state 转为 `CAMPAIGN-REMAP-GOAL-HANDOFF-READY`。
- B1 的来源、测试和失败机制可复用；T008 数字不得作为论文方法/性能结论。
- 仍在 GW Step 4a 总阶段，不进入 Step 5/Contract/Execute。

### 来源

S015 续接 / V002 / live-test D002。

---

## D015: Goal campaign remap 激活 A4 deployable adaptive CPR

> status: superseded
> date: 2026-07-26
> 取代：D014（只取代“无 active carrier / 等待 remap”的当前动作；B1 返回池事实保留）
> 被取代：D016
> 依据：live R001/D003 + CP001–CP008 + S013 + thesis-writing D001–D008/H003
> 触发原话：live topic `voice.md` 2026-07-26

### 决策

1. 当前 formal carrier 激活为 `A4_DEPLOYABLE_ADAPTIVE_CPR`，仍处于 GW Step 4a。
2. A4 的正式 readiness 为 `READY_WITH_BOUNDED_IDENTITY_ADJUDICATION`：
   - 已有 B11/NDA-ML Step 1–3、A4 选择器、30-seed 数据、corrected/common-768
     资产和论文方法结构；
   - 旧 `+0.27–0.48 dB` 已确认是混合分母与 post-hoc oracle 假增益，禁止继承；
   - T009 必须重新关闭 common-payload、pilot/ambiguity、receiver-visible input、
     strongest-fixed comparator 与 real-crossing identity。
3. T009 的 positive method target 是统一 waveform/common mask 上的 receiver-visible
   block-wise DA/NDA selector。一次有界 identity 修复通过后，同包完成：
   - P1 validation-frozen two-stage rule；
   - P2 monotone validation selector；
   - P3 confidence-safe selector。
4. 主 comparator 是“不做适配”的 validation-frozen global fixed strategy；
   candidate set 必须包含 fixed DA、fixed NDA 与已在 S011 立住的 DPLL 异族传统
   baseline；B-cond 从同一集合选择，per-block oracle 只作 ceiling。
5. `METHOD_SIGNAL` 必须胜 global B*、不被 always-DA 或 DPLL 支配，并满足 T009 的
   paired CI、win fraction、regret closure 与 clean-degradation 门。只胜 fixed
   NDA 时最高 `PACKAGING_BOUNDARY`。
6. identity 或方法门失败后不再为 A4 开第二个 repair 包；A4 返回
   `PACKAGING_BOUNDARY / METHOD_FAIL_WITH_SPACE / BLOCKED_IDENTITY` 的精确状态，
   Goal 主控继续下一轮 remap。

### 正向方法合同

- `positive_method_target`：receiver-visible block-wise DA/NDA adaptive CPR。
- `minimal_construct`：P1 frozen two-stage；P2 monotone selector；P3
  confidence-safe selector。
- `fair_comparator`：fixed DA、fixed NDA、validation-frozen DPLL；
  global B*/B-cond 从三者选择，per-block oracle 仅作上界。
- `primary_packaging`：Gamma–Gamma 湍流下接收功率感知的自适应 CPR。
- `fallback_packaging`：NDA safeguard、工作区边界或 complexity/robustness
  trade-off。
- `next_positive_action`：执行 live T009；不另派纯 audit 或纯 repair 包。

### 为什么比两个替代项更可能产生 METHOD_SIGNAL

- 比 B10/B12 少一个方法本体重建层：A4 的动作和输出分支已经存在；B10/B12
  source-native estimator、channel 与核心公式身份仍未闭合。
- 比 B1 少两个同轴失败包：B1 已连续 T007/T008 且 evaluator 不在可靠 working
  region，继续是第三个 evaluator repair；A4 是本轮第一次 formal adjudication。

### 边界

- T009 不修改旧 A4、paper、common、params、formal/current/mission owner；
- 不恢复 B1/T008、T006 repair、Pilot-Jones、P03 或 dormant Scout；
- 不进入 Step 5、Contract 或 Execute；
- live checkpoint 在主控接收 T009 前保持 CP008。

### 来源

live R001/D003；S013；thesis-writing H003 与 D001–D008；mission-log CP001–CP008。

---

## D016: T009 身份裁决失败，A4 返回候选池

> status: superseded
> date: 2026-07-26
> 取代：D015（只取代当前 carrier 与 next action；D015 对 T009 的历史授权、身份门和“不再二修”约束保留）
> 被取代：D017
> 依据：验证 V003 + T009 worker-log + executor commit `8ea886e4b5c1e3318fd9426dcc7e8aebcdf8a558`
> 触发原话：无（技术推导）

### 决策

1. 接受 T009 的 formal disposition：
   `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`，`mission_method_delta=NONE`。
   T009 在身份门停止，P1–P3 primary comparison 未运行，因此没有方法信号或方法
   包装结论。
2. `A4_DEPLOYABLE_ADAPTIVE_CPR` 返回候选池；不作 A4 family Kill，也不为当前
   A4 evaluator 开第二个 repair package。formal owner 当前无 active carrier，
   等待 live Goal campaign remap 产生新的 formal 激活决策。
3. 拒绝把“DA 在 9/9 validation conditions 获胜”写成可靠工作区内的物理支配或
   普适排序。该数字最多是错误 evaluator 下的局部观察，不得进入论文、方法卡、
   family Kill 或后续 carrier 排名依据。

### 核心失败机制

- shared transmitter/pilot 路径含随机生成，未闭合 common-payload 与已知导频身份；
  DA/NDA 的输入和评价人口因此不可证明同一。
- 1 MHz 频率条件在 DA/NDA 路径间存在不对称，不能把排序差异归因于 DA/NDA
  机制本身。
- validation 条件缺少足以支撑“可靠工作区”的来源，且没有合法 FEC crossing；
  因而既不能形成 dB 增益结论，也不能宣称可靠工作区内的物理支配。
- `raw.json` 与 `result.json` 位于 gitignored results 目录，未进入 executor
  commit；`git diff --check 8ea886e^ 8ea886e` 另因 8 个 EOF 空行告警失败。
  原提交可定位执行资产，但不构成可移植、格式闭合的 formal evidence package。

### 否决了什么

- 否决“DA 9/9 因而物理上支配 NDA”及据此关闭 A4 family。
- 否决把工程测试、DPLL smoke 或 identity abort 冒充 `METHOD_SIGNAL`。
- 否决在当前 A4 evaluator 上再开第二个 repair 包；D015 已预注册失败后回池。

### 可复用部分

- T009 task-control、DPLL 连续 VCO smoke、隔离实现和失败机制可作为 evaluator
  防错资产。
- executor commit `8ea886e4…` 与本地 ignored raw/result 保留为原始审计指针，
  但引用时必须同时标注其证据闭包限制。

### 影响范围

- 本专题仍处于 GW Step 4a；不进入 Step 5、Contract 或 Execute。
- D015 仅在“当前 carrier/next action”上被取代；其旧假增益禁继承、strongest
  comparator 要求、T009 历史授权和 no-second-repair 约束不被推翻。
- B1 的 D014 返回池事实、T008 拒收，以及更早 A4/NDA-ML 历史证据均不追溯改写。

### 来源

S016 / V003 / T009 worker-log / executor commit `8ea886e4…`。

---

## D017: 激活 B10 source-native adaptive pilot-RLS Step 4a carrier

> status: superseded
> date: 2026-07-26
> 取代：D016（只取代“无 active carrier / 等待 remap”的当前动作；T009 拒收、A4 返回池与 no-second-repair 事实保留）
> 被取代：D018
> 依据：live R002/D006 + B10 L20/Q1/Q2 + D012/V001 + Springer 2024 DOI metadata/fulltext + R002 §2.1 摘要级邻近方法先例
> 触发原话：无（技术推导）

### 决策

1. 当前 formal carrier 激活为 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，仍处于
   GW Step 4a 维度 D；不进入 Step 5/Contract/Execute。
2. B10 的 readiness 为 `FORMAL_READY_WITH_SOURCE_NATIVE_IDENTITY_GATE`：
   - L20/B10-Q1/Q2 的 Step 1–3 证据与 2024 全文存在；
   - D012 曾合法激活 B10/B12，但 V001 拒收 T006 的 estimator/channel/statistics
     身份，family 保持 `UNRESOLVED`；
   - T010 必须从原文重建 fixed B10，不得把 T006 组件改名复用。
3. T010 的 source-native gate 必须闭合：128 连续 pilot、训练→DD 生命周期、
   independently frozen pilot manifest、pilot/data 同一 TX 侧通道、standard RLS
   递推和 `h0/P0/δ/F` 初始化、全 radians、positive-CFO source smoke、无
   TX-truth/future/post-hoc resolve。
   `source-native` 仅指 estimator 身份；2.5 GBd 星地 GG primary 从
   `B5Params.R_SYM_B5` 读取并标 `SOURCE_TRANSFER`，不能把 B10 原文
   26 dB OSNR 等同于 electrical SNR。
4. gate 通过后同包比较：
   - P1：validation-frozen fixed-`λ` source-native B10；
   - P2：receiver-visible normalized-innovation update freeze；
   - P3：只由滞后一拍/EMA innovation 形成的有界 `λ_k`；
   - cheap amplitude-only freeze 与 conventional 4OPM+BPS /
     4OPM+DD-DPLL。
5. `METHOD_SIGNAL` 必须在 held-out paired test 同时胜 P1、cheap rule 与
   conventional B*，并闭合 working region、clean degradation、信息边界和统计门；
   其中 required comparator 必须共同具有真实 HD-FEC crossing，且所有纳入 Q²
   Go 的 seed 均 `BER<0.2`；no-crossing/collapse 只允许 outage/boundary 包装。
   oracle 只作上界。source smoke、代码创建、测试 PASS 或 negative result 均不是
   方法产出。
6. T010 若 `BLOCKED_IDENTITY` 或方法无增量，不开第二个 B10 repair；返回 live
   Goal 轮换到 C15 Step 1–3 formalization 或其他新 carrier。

### 正向方法合同

- `positive_method_target`：receiver-visible innovation-aware robust pilot-RLS
  CFO/PN tracking under GG fade-induced DD errors。
- `minimal_construct`：P1 fixed B10；P2 innovation freeze；P3 adaptive forgetting。
- `fair_comparator`：source-native P1、amplitude-only cheap gate、task-matched
  validation-frozen 4OPM+BPS 与 4OPM+DD-DPLL；相同 waveform、pilot/data mask、
  energy、realization、frequency-stage responsibility 和 tuning opportunity。
- `primary_packaging`：星地高阶 QAM 的创新量门控自适应 pilot-RLS CPR。
- `fallback_packaging`：source-native B10 星地迁移边界、低复杂度 update-freeze
  或 robustness/complexity operating regime。
- `next_positive_action`：执行 live T010；identity 通过后同包跑完整方法 slice。

### 排除的替代方案

- 不做 B10+B12 组合：B12 公式身份未闭合，会复刻 T006 多重归因混淆。
- 不直接跑 C15：Step 1–3 未完成，违反 FR-22。
- 不继续 B1/A4 evaluator：分别违反第三 repair 与 no-second-repair 边界。
- 不转 B9：当前星地 formal migration 与自相干基础设施均未闭合。

### 影响范围

- 更新本专题 current carrier 与 live authority；历史 D012–D016 血缘保留；
- 只允许 T010 隔离路径，不改 shared generator、common、params、论文或 owner；
- negative/blocked evidence 只作 scoped Step 4a 资产，不作 family/domain Kill。

### 来源

live R002/D006；B10 L20/Q1/Q2；D012/V001；DOI
`10.1007/s11107-024-01019-2` metadata/content；DOI
`10.1109/ICAIT66450.2025.11353303` 与 `10.1016/J.CJA.2015.05.001`
本地检索元数据（仅支持邻近方法族，不作精确公式来源）。

---

## D018: T010 Phase-B operational identity 合同纠错与一次确认授权

> status: superseded
> date: 2026-07-26
> 取代：D017（只取代 Phase-B residual/`λ`/source-smoke seed 合同；B10 carrier、方法目标、fair-comparison 与 no-second-package 边界保留）
> 被取代：D019
> 依据：验证 live V008 + T010 初次 source-smoke artifact + B10 PDF p.165–170 Eq.(1)/(8) 与 Fig.1 + 独立科学 verifier 反事实
> 触发原话：无（技术推导）

### 决策

1. formal carrier 仍为 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，仍在 GW Step 4a
   维度 D；不进入 Step 5/Contract/Execute。
2. T010 初次 `BLOCKED_IDENTITY` 的 formal verdict 被拒收为
   `SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID`：
   - `r=s·exp(+jφ)+n` 与 `exp(-j predicted)` 去旋下，operational residual 必须是
     `angle(derotated*conj(decision))`；旧任务的相反符号不能用于 identity Kill；
   - `.999` 不是论文 source parameter，且独立诊断证明会制造 10 GHz failure。
3. 只授权同一 T010 的一次 Phase-B confirm：固定 operational sign，固定
   `λ=.99`（`IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN`），保留
   seed `130001` 为 invalid-development evidence，并用此前未观察的 seed `130002`
   运行相同 1/10 GHz smoke。该参数与结果只服务 source identity，不是论文性能点、
   primary tuning 或 method delta。
4. 修订后的 control/formal/task 必须先独立审查。confirm 失败即接受
   `BLOCKED_IDENTITY` 并轮换；通过才允许另一独立科学 verifier 决定是否进入
   T010 Phase C。不得再改 sign、`λ`、seed 或补第二个 B10 repair/package。

### 理由

T010 尚未 final commit、未形成 CP010，且当前 verdict 被独立 verifier 以两个 P0
驳回。一次全新 seed 的包内确认是关闭任务合同债务的最小成本；接受假失败或直接
跳入方法比较都会破坏 source-native gate。

### 排除的替代方案

- 不接受被 P0 污染的 `BLOCKED_IDENTITY`。
- 不复用已观察 seed `130001` 作确认，不在 confirm seed 上调参。
- 不运行 Phase C/primary/validation/held-out。
- 不恢复 B12、B1、A4 或 T006 repair。
- confirm 不通过时不再留在 B10，转 C15 Step 1–3 formalization 或新 carrier。

### 影响范围

- formal authority 由 D017 递增到 D018；live control 对应 epoch 18 / CP009；
- 只授权 T010 Phase-B amendment、隔离代码/tests/artifacts 与 current projection；
- no-second-package、source-transfer claim ceiling 与 held-out 方法门保持不变。

### 来源

live D007/V008；T010 Phase-B artifact/report；DOI
`10.1007/s11107-024-01019-2` 原 PDF p.165–170。

---

## D019: T010 clean confirm seed 与 Phase-B 科学暂停门

> status: superseded
> date: 2026-07-26
> 取代：D018（仅更正 confirm seed 与 Phase-B 暂停回执；D018 的 operational residual、source-only `.99`、一次包内确认和 no-further-repair 边界保留）
> 被取代：D020
> 依据：独立 amendment review（P0=0/P1=3/P2=1）+ live D008 + V008 + repository exact-token seed census
> 触发原话：无（技术推导）

### 决策

1. formal carrier 与 GW Step 4a 不变。confirm seed 从已用于 canonical/RNG test 的
   `130002` 改为仓库 exact-token 零命中的 `130003`；`130002` 不作性能证据。
2. T010 必须在实际 confirm 前增加 synthetic residual-direction regression，并把
   seed `130003` 的 1/10 GHz BER gate 明确为唯一 confirm，不得预跑。
3. confirm PASS 后 executor 必须停止于
   `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW`。独立科学 verifier 与新的递增 control
   是进入 Phase C 的必要条件；T010 最终 §8 receipt 不能替代该中间门。
4. confirm 失败即接受 `BLOCKED_IDENTITY` 并轮换；通过也不构成 method delta。
   不得再改 sign、`.99`、seed 或开第二个 B10 package。

### 理由

identity confirmation 的证据完整性要求真正未执行的 seed；执行协议还必须在
Phase B 与 Phase C 之间显式暂停，避免 task receipt 语义绕过独立科学验收。

### 排除的替代方案

- 不复用 `130002`，不静默修改 epoch 18。
- 不允许 confirm 与 Phase C 在同一 executor turn 串行。
- 不新增调参、primary 或 held-out 动作。

### 影响范围

- formal authority 递增至 D019；live control 对应 epoch 19 / CP009；
- 只更新 owner/control/task/registry/current projections；确认执行仍待独立审查。

### 来源

live D008；独立 amendment reviewer；V008；T010 Phase-B tests。

---

## D020: 接收 B10 source identity 并授权 T010 Phase C

> status: superseded
> date: 2026-07-26
> 取代：D019（只取代“Phase C 未授权”的当前动作；D019 的 confirm 历史、operational residual、source-only `.99` 与 no-further-repair 保留）
> 被取代：D021
> 依据：验证 live V012 + T010 clean-confirm artifact/source contract + live D009
> 触发原话：无（技术推导）

### 决策

1. formal 接收 `SOURCE_IDENTITY_PASS / PHASE_B_CONFIRM_ACCEPTED`。source smoke
   只关闭 B10 estimator identity，`mission_method_delta=NONE`，不构成性能复现、
   `METHOD_SIGNAL` 或 promotion。
2. formal carrier 仍为 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，GW Step 4a 维度 D。
   授权同一 T010 分段 Phase C：
   - C1：方法/对照实现、direct information-increment、source-smoke seal 与
     read-only P2 closure，不消费 validation；
   - C1 独立审查 PASS 后，C2 只用 validation seeds 冻结方法、对照和 SNR cells；
   - C2 完成后再次独立科学验收；held-out/Phase D 仍未授权。
3. C2 若需多 turn，只能按预注册顺序增量落 raw；全矩阵完成前不作参数选择，
   任何 turn 都不得超过 15 分钟。
4. required comparator、working-region、crossing、claim ceiling 与 no-second-package
   科学门保持 T010 原定义；source PASS 不能放宽这些门。

### 理由

V012 已排除 sign、truth leakage、mask/mapping/noise 与 source lifecycle P0/P1。
继续到 bounded method construct 是当前最接近方法信号的合法动作；分离 C1/C2 和
独立验收可防止 evaluator/implementation PASS 冒充方法。

### 排除的替代方案

- 不把 Phase B 写成方法产出。
- 不重跑 source smoke，不修 T006/B12、B1/A4 或启动 C15/B9。
- 不在 Phase C 使用 held-out/test seeds。
- 不进入 Step 5/Contract/Execute。

### 影响范围

- formal authority 递增至 D020；live control 对应 epoch 20 / CP009；
- 只授权 T010 Phase C，Phase D/held-out 继续禁止。

### 来源

live D009/V012；T010 clean-confirm artifacts/source contract。

---

## D021: 接收 T010 C1 并授权 C2 validation freeze

> status: superseded
> date: 2026-07-26
> 取代：D020（只取代 C1 当前动作；D020 的 source identity、Phase-C 分段、
> working-region 与 no-second-package 合同保留）
> 被取代：D022
> 依据：验证 live V021 + T010 C1 source/experiment contract + live D010
> 触发原话：无（技术推导）

### 决策

1. formal 接收 `C1_IMPLEMENTATION_CONTRACT_PASS`。V021 的独立复审为
   `P0=0/P1=0/P2=1`；唯一 P2 是不可补造的 pre-C1 immutable snapshot 债务。
   C1 没有运行 validation/fair comparison，故 `mission_method_delta=NONE`。
2. formal carrier 保持 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，仍在 GW Step 4a
   维度 D。只授权同一 T010 的 C2：
   - validation seeds 仅 `131001–131005`；
   - 按预注册 Cartesian order 生成 tracked raw，未完成全矩阵前不选择参数；
   - 完整矩阵后分别全局冻结 P1/P2/P3/cheap/B* 与每个 GG 档最多 3 个相邻 SNR；
   - P2/P3 不得按 seed/cell best-of；test/held-out 不得读取。
3. C2 完成后必须停止于 `PARTIAL_C2_AWAITING_SCIENCE_REVIEW`。新的独立科学验收
   与递增 control 才能授权 Phase D。
4. required comparator、working-region、真实 FEC crossing、claim ceiling、
   no-second-package 和 C15 rotation 边界保持不变。

### 理由

C1 已关闭方法/对照接口身份，C2 是当前最小且直接的方法信息增量动作。它相对
C15 少一个完整 Step 1–3 周期，相对 B1/A4 避免重复 evaluator repair，相对继续
C1 审计能实际形成 validation-frozen fair comparison；因此在当前 formal-ready
集合中最可能推进到 `METHOD_SIGNAL`，但 C1 本身不构成方法进展。

### 排除的替代方案

- 不把 C1 PASS、测试或 evaluator closure 记为 method delta。
- 不运行 held-out/Phase D，不进入 Step 5/Contract/Execute。
- 不重跑 Phase-B source smoke，不修旧 T006/T008/T009。
- 不立即激活 C15/B1/B9；若 C2 或其独立验收表明无合法方法空间，则按原边界轮换。

### 影响范围

- formal authority 递增至 D021；live control 对应 epoch 22 / CP009；
- 只授权 T010 C2 validation freeze；Phase D/held-out 继续锁定。

### 来源

live D010/V021；T010 C1 source/experiment contract 与定向 tests。

---

## D022: 接收 T010 B10 identity block 并返回 C15 formalization

> status: active
> date: 2026-07-26
> 取代：D021（只取代 B10/C2 当前动作；D020/D021 的历史 source/C1 接收与
> no-second-package/held-out 边界保留）
> 被取代：无
> 依据：验证 live V026 + T010 840-row raw checkpoint + worker-log deterministic diagnosis
> 触发原话：无（技术推导）

### 决策

1. formal 接收 T010 为 `BLOCKED_IDENTITY`，P0/P1/P2=`0/0/1`，
   `mission_method_delta=NONE`。positive 1 MHz primary transfer 在
   moderate/14 dB/seed `131004` 的 128-pilot unwrap 选错 `-2π` branch，
   进入 RLS 前的 observed LS slope 已为负；P1/P2/P3 共用初始化。
2. B10 source-native adaptive pilot-RLS 返回候选池且停止当前投资。840-row
   strict-prefix raw、17-file frozen hash、无 aggregate、heldout=false 是终局证据；
   不补矩阵、不改 positive-slope identity、不定义事后 exception row、不运行 Phase D，
   也不开第二个 B10 package。
3. 当前恢复为 **无 active scientific carrier**。下一 formal route 是
   `C15_REDUCED_CONSTELLATION_FORMALIZATION`，但只授权从新候选 Step 1 开始完成
   Step 1 search、Step 2 acquire 与 Step 3 close read/four-criteria readiness；
   上游任一项未闭合时不得进入 Step 4a/MVE。
4. 旧 C15 sandbox 的 unequal-step 结果只作失败事实：共同 μ=`0.03` 面对约 19×
   gradient scale 差，不能继承其 cost-family 机制结论、seed 或性能数字。

### 理由

T010 的失败发生在 source-native lifecycle，不是 P2/P3 update rule；修复需要改变
source identity 或 raw score contract，违反 no-second-package。C15 的补债成本高于
直接运行 ready carrier，但当前不存在另一个合法 ready carrier。它仍优于 B1
第三次 evaluator 重建、A4 第二次 identity repair 和 B9 新建完整自相干接收链；
先完成 Step 1–3 是最小合法且最可能重新形成方法载体的动作。

### 排除的替代方案

- 不接受测试、840 rows、科学早停或 negative result 为方法产出。
- 不修 T010/B10、T006/B12、B1/T008 或 A4/T009。
- 不恢复 dormant Science Scout/P03，不直接复用 C15 sandbox。
- 不进入 Step 4a、Step 5、Contract 或 Execute。

### 影响范围

- formal stage 保持 Groundwork，但 active carrier 清空；
- live control 应递增到 epoch 24 / CP010，只允许 C15 formalization preparation；
- master-state/current projections 必须把 B10 标为
  `BLOCKED_IDENTITY / RETURNED_TO_POOL`，并新增 C15 Step 1 待执行门；
- B10 raw 与 hashed execution contract 不改。

### 来源

live D011/V026；T010 worker-log/synthesis；R002；D021。

---

## D023: C15 formalization 先执行 Step 1 search 与 Step 2 acquire

> status: superseded
> date: 2026-07-26
> 取代：无（细化 D022，不改变无 active carrier 与禁止 MVE 边界）
> 被取代：D024
> 依据：调研 live R002 + 旧 C15 synthesis/contract 的 equalizer-cost identity +
> Groundwork `gw-search.md` / `gw-acquire.md` 硬门
> 触发原话：无（技术推导）

### 决策

1. C15 的 formal 对象是 **blind equalization cost/update family**，不是 carrier
   phase recovery。目标术语族包含 reduced constellation/Sato、CMA/MMA、
   RDE/radius-directed 与 staged CMA→RDE/MMA；这些关系必须由全文重新闭合。
2. 授权 T011 只完成：
   - Step 1：≥20 candidate、≥3 sources、≥2 mechanism routes、≥5 必读、正式发表
     占比 ≥50%，并做两个子方向的定向深搜；
   - Step 2：按三轮止损获取 ≥5 篇有效全文，逐篇 title/DOI/content quality 核对，
     产出覆盖面缺口报告。
3. T011 完成后必须停止于 `AWAITING_COVERAGE_CONFIRMATION`。覆盖面未经用户确认，
   不得派 Step 3 close read；Step 3/3.5/4a/MVE 继续锁定。
4. 旧 C15 Scout 的 `mu=0.03` unequal-step 对比、性能数字、seed 与
   `LOCAL_NEGATIVE` 都不是 formal evidence；只允许作为检索待核查的失败事实。
5. T011 不是 scientific experiment，不能产生 method delta；最多形成 formal
   readiness input。

### 理由

旧 C15 资产明确实现的是 2×2 blind equalizer cost，但对 Sato/RCCMA/RDE/MMA
血缘使用了未由本地全文闭合的注释，且共同步长使 convergence opportunity 不公平。
直接重跑会违反 FR-22 与 comparator fairness。先完成 Step 1–2 可以用最小成本
判断是否有足够 source、传统 comparator 和星地 task-fit 证据，并为后续 Step 3
提供合法输入。相对 B1/A4 的重复 identity/evaluator repair 与 B9 的新接收全链，
该 formalization 仍更可能解锁 `METHOD_SIGNAL`，但不能预支为方法进展。

### 排除的替代方案

- 不把 C15 写成 CPR，不用“相位代价”检索。
- 不运行旧 sandbox/MVE，不调 `mu`，不复用旧 seed 或 negative verdict。
- 不以摘要、旧注释或 source code docstring 替代全文。
- 不越过 coverage confirmation 进入 Step 3。
- 不进入 Step 4a、Step 5、Contract 或 Execute。

### 影响范围

- live authority 指向本 D023；control 递增至 epoch 25 / CP010；
- T011 action class 为 `CANDIDATE_FORMALIZATION`；
- C15 仍为 `NOT_ACTIVE_CARRIER`，formal stage 保持 Groundwork；
- D022 的 B10 no-second-package 与所有禁止边界继续有效。

### 来源

live D012/T011；R002；旧 C15 synthesis/contract；`stages/gw-search.md`；
`stages/gw-acquire.md`。

---

## D024: 接收 T011 检索覆盖阻断并授权 T012 canonical recovery

> status: superseded
> date: 2026-07-27
> 取代：D023
> 被取代：D025
> 依据：验证 live V029 + T011 worker log/archives + 共享多源索引与本地全文只读复核
> 触发原话：无（技术推导）

### 决策

1. 接收 T011 为 `BLOCKED_SEARCH_COVERAGE`：53 unique candidates 不能弥补
   1/3 actual sources；未进入 acquire 的止损合法。该处置不是 C15 scientific
   negative，`mission_method_delta=NONE`。
2. formal owner 继续保持 **无 active scientific carrier**。只授权 T012 一次
   source/canonical recovery：
   - 共享索引恢复至少三个真实 source families；
   - 现有近期全文只做可证的 metadata/title closure；
   - 三篇 canonical 原文各一次 exact-title IEEE/blit；
   - canonical 3/3 且 recent comparator/task-fit ≥2 后停在 coverage confirmation。
3. 任一 canonical 获取失败即 `BLOCKED_CANONICAL_FULLTEXT`，C15 返回候选池；
   不降低 fulltext/source 门，不给第二次获取 repair。
4. Step 3、3.5、4a/MVE、Step 5、Contract、Execute 均未授权。

### 理由

fresh single-source failure 是局部管道阻断。共享历史索引已有 Semantic Scholar、
SerpAPI Scholar、OpenAlex、Exa 直接相关召回；共享论文库已有 5 篇近期相关
content，包含 JR-CMA pointing-jitter 与 modulus-rings VAE coherent-FSO 的直接
碰撞。剩余债务集中为 Sato/Godard/Yang 三篇 canonical，而非新 evaluator 或仿真
基础设施。一次 T012 因此比 B1 第三 evaluator repair、A4 第二 identity repair 和
B9 新接收全链更可能产生 formal-ready 方法空间；但 T012 本身不能产生方法信号。

### 排除的替代方案

- 不把 shared historical metadata 当全文或创新性结论。
- 不修改正确 source/content，不猜 canonical DOI。
- 不修已禁止的 B1/A4/B10/T006，不恢复 Scout/P03。
- 不在 coverage confirmation 前进入 Step 3，不运行任何 MVE。

### 影响范围

- live authority 指向本 D024；control epoch 26 / CP011；
- T012 action class 为 `CANDIDATE_FORMALIZATION`；
- D022 的 B10 no-second-package 与所有阶段禁止边界继续有效。

### 来源

live D013/V029/T012；T011 worker log/archives；共享索引与论文库只读映射。

## D025: 接收 T012 task-interface blocker 并撤销当前 C15 workline

> status: superseded
> date: 2026-07-27
> 取代：D024
> 被取代：D026
> 依据：验证 live V031/V032/V033 + T012 worker log + epoch 29 final-binding FAIL
> 触发原话：无（技术推导）

### 决策

1. T012 正式处置为
   `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`，不是 C15 science
   disposition；`mission_method_delta=NONE`。
2. T012 在 source recovery、metadata closure、canonical acquire 前终止；
   C15 family 保持 `UNRESOLVED / RETURNED_TO_POOL`，不得伪称 source/canonical
   negative 或 Kill。
3. 撤销 D024 的当前 T012 workline，formal owner 继续无 active scientific
   carrier。下一步只做 post-T012 carrier remap，激活新 carrier 前不运行实验。
4. V032 已冻结最后一次 retry 退出条件；CIM fail-open P1 触发该条件，不做第四次
   task-interface amendment。

### 理由

继续修 T012 会把第三个确定性接口缺口变成第四次补丁，而仍未触及任何 formal
science uncertainty。停止并轮换比继续治理更符合 method-production mission：
当前 no-method streak 已到 12，且 C15 的 source/canonical 合同没有被执行，既
不能晋级也不能科学否决。

### 排除的替代方案

- 不把治理终验 PASS/FAIL 当方法产出。
- 不降 source/fulltext/readiness 门，也不绕过 Step 1–3 直接跑旧 C15 sandbox。
- 不恢复 B1/A4/B10 的下一 repair 包。
- 不在 remap 完成前运行 B9 或其他新实验。

### 影响范围

- live authority 转本 D025；foreground epoch 30 / CP012 只允许 remap/task
  preparation；
- master/current projections 标记 `NO_ACTIVE_SCIENTIFIC_CARRIER`；
- T012 关闭，C15 返回 pool；Step 3/4a/MVE/Step 5/Contract/Execute 仍未授权。

### 来源

live D014/V033；T012 worker log；V032 one-last-attempt contract；epoch 29
final-binding independent review。

---

## D026: 激活 B9 Step 1 formalization workline，保持无 active carrier

> status: superseded
> date: 2026-07-27
> 取代：D025
> 被取代：D027
> 依据：调研 live R003 + live D015 + B9 JLT 2023 主仓全文/metadata +
> Groundwork `gw-search.md`
> 触发原话：无（技术推导）

### 决策

1. formal owner 保持 `NO_ACTIVE_SCIENTIFIC_CARRIER`，但将当前合法 workline
   切换为 **B9 virtual-carrier self-coherent + DRE Step 1 formalization**。
2. 只授权 T013 完成 candidate-specific Step 1 search/evidence adapter：
   ≥20 candidates、≥3 个真实 source families、≥2 mechanism routes、≥5 必读、
   正式发表 ≥50%，并由执行 agent 对 title/abstract/venue/year/citation/
   publication status 做语义审查。
3. T013 结束于
   `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE`、
   `BLOCKED_SEARCH_COVERAGE` 或 `STEP1_NO_DISTINCT_PROBLEM_FOUND`；三者都必须
   `mission_method_delta=NONE`，且都不得被写成 B9 science Go/Kill。
4. Step 2/3/3.5/4a/MVE、Step 5、Contract、Execute 均未授权；B9 的
   `minimal_construct` 在 Step 3/3.5/4a 前不得冻结或实现。

### 候选正向方法合同（待 Step 1–3 验证）

- `positive_method_target`：在低比特 virtual-carrier self-coherent 星地 FSO 中，
  用因果可部署或预配置链路状态选择 DRE/CSPR 的复杂度—稳健性设置，并保留
  source-native fixed-DRE/RO 安全回退。
- `minimal_construct`：未冻结；只能在 Step 3/3.5/4a 完成后定义。
- `fair_comparator`：RO without DRE、source-native fixed DRE，以及经全文闭合的
  任务匹配传统 quantization-noise-shaping 方法。
- `primary_packaging`：星地低比特 DAC 自相干 FSO 的数字分辨率增强与稳健适配。
- `fallback_packaging`：固定 DRE 的星地迁移边界或复杂度/性能折中。
- `next_positive_action`：完成 T013 Step 1 coverage/collision adjudication。

### 理由

R003 比较 B9、C15、B1、A4 后确认：B9 是唯一同时拥有正式全文正向锚、明确方法
旋钮、未消耗 repair 配额且不违反既定 no-second/third-repair 边界的候选。其约
3/1/0.5 dB 只支持低 PNOB 下 DRE-vs-RO 的量化噪声动机；42 m FSO 也不自动迁移
到星地。Step 1 是裁决证据覆盖、竞争碰撞和 comparator 债务的最小合法动作。

### 排除的替代方案

- C15 保持 `UNRESOLVED / RETURNED_TO_POOL`；不把 T012 接口失败作 science Kill，
  也不做第四次 T012 amendment。
- B1/A4/B10 继续受既有第三/第二/第二 repair 禁止边界约束。
- 不用旧 read-note、search metadata 或内部 DRE-vs-RO 增益替代 formal Step 1–3。
- 不运行 B9 代码、实验、seed 或 MVE。

### 影响范围

- live authority 指向本 D026；foreground epoch 31 / CP012 只授权
  `CANDIDATE_FORMALIZATION`；
- T013 独立 dispatch review PASS 后，才可由不同 executor 执行 Step 1；
- formal stage 仍是 Groundwork；B9 在 Step 1–3/3.5 与 Step 4a readiness 审查
  之前不是 active scientific carrier。

### 来源

live R003/D015；B9 主仓
`papers/doi/10.1109_jlt.2023.3270673/{metadata.json,content.md}`；
`stages/gw-search.md`。

---

## D027: 接收 B9 Step 1 coverage block 并授权唯一一次多源修复

> status: superseded
> date: 2026-07-27
> 取代：D026
> 被取代：D028
> 依据：调研 live R004 + 验证 live V035 + T013 worker log/candidate view +
> Groundwork `gw-search.md`
> 触发原话：无（技术推导）

### 决策

1. formal owner 接收 T013：
   `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。B9 不是 Go/Kill，
   formal owner 继续 `NO_ACTIVE_SCIENTIFIC_CARRIER`。
2. T013 已满足数量、必读、发表和人工语义标注门，但实际 source family 只有
   OpenAlex；Route A 无 nonexcluded deep，Route B deep 不含 self-coherent/
   virtual-carrier/CSPR/phase-reconstruction 机制证据。
3. 只授权 T014 在 Groundwork Step 1 使用 S2、arXiv、IEEE 做一次多源与
   mechanism-deep coverage repair。禁止下载、Step 2/3/3.5/4a/MVE、实现和实验。
4. T014 若仍不足三源，或没有任一 route 以非 OpenAlex 的 mechanism-specific
   deep abstract 支持 candidate-specific residual problem，则 B9 返回候选池，
   不得第三次 Step 1 repair；live mission 必须轮换。
5. T014 PASS 也只完成 Step 1 并等待 acquire；`minimal_construct`、方法比较和
   active carrier 身份继续冻结。

### 候选正向方法合同（仍待 Step 1–3 验证）

- `positive_method_target`：低比特 virtual-carrier self-coherent 星地 FSO 中，
  用因果可部署或预配置链路状态选择 DRE/CSPR 复杂度—稳健性设置，并保留
  source-native fixed-DRE/RO 安全回退。
- `minimal_construct`：未冻结；Step 3/3.5/4a 前不得定义或实现。
- `fair_comparator`：RO without DRE、source-native fixed DRE、EFNS 与经全文
  闭合的任务匹配传统 quantization-noise-shaping 方法。
- `primary_packaging`：星地低比特 DAC 自相干 FSO 的数字分辨率增强与稳健适配。
- `fallback_packaging`：固定 DRE 的星地迁移边界或复杂度/性能折中。
- `next_positive_action`：T014 Step 1 multi-source/mechanism-deep repair。

### 理由

本次缺口是来源和定向机制覆盖，不是模型、evaluator 或仿真 identity 重建。
T013 已留下 21 条非排除、8 条必读、EFNS 直接 comparator 和 11 项 acquisition
debt；一次标准检索包可以明确通过或失败。相较 C15 两包未触及科学内容、B1 第三
evaluator rebuild、A4/B10 第二 identity repair，该动作成本最低且最接近恢复合法
carrier。其选择依据与六维比较见 live R004，不把概率判断当科学结果。

### 排除的替代方案

- 不把 OpenAlex 单源 metadata view 当 formal Step 1 完成。
- 不用共享索引历史来源字符串补算三源，不把零搜索结果推成创新空白。
- 不立即重启 C15、B1、A4 或 B10。
- 不提前获取 canonical papers；Step 2 仍未授权。

### 影响范围

- live authority 指向本 D027；foreground epoch 33 / CP013 只允许
  `CANDIDATE_FORMALIZATION`；
- T014 dispatch review 与 clean binding PASS 后才能执行；
- formal stage 保持 Groundwork，无 active scientific carrier。

### 来源

live R004/D016/V035；T013 commits `16176c2`、`7ca3cbf`；T013 worker log 与
`search-archive/2026-07-27/b9-step1-candidate-view.json`。

---

## D028: 接收 T014 source coverage block，B9 返回池并恢复 formal remap

> status: superseded
> date: 2026-07-27
> 取代：D027（只取代 B9 当前 workline 与下一动作；D027 对唯一 coverage repair
> 的历史授权和退出边界保留）
> 被取代：D029
> 依据：验证 live V037 + T014 worker log/receipt/raw archives + executor commit
> `5ba5a54cce3705186d8a921d4e4f2ec3c34bb7c8`
> 触发原话：无（技术推导）

### 决策

1. formal owner 接收 T014 为
   `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。A1 只形成
   OpenAlex+IEEE 两个真实 source family，`count=2<3`；S2/arXiv 没有实际返回。
2. A1 停止符合冻结合同；A2/A3/A4、deep archives 与 candidate view v2 均未
   运行或生成。没有全文获取、精读、实现、仿真或 seed。
3. B9 状态改为
   `RETURNED_TO_POOL / STEP1_SEARCH_COVERAGE_BLOCKED`。本结果不是 B9
   science Kill，也不证明 candidate-specific problem 不存在；但唯一 Step 1 repair
   已消费，禁止第三个 B9 Step 1 包。
4. formal owner 继续 `NO_ACTIVE_SCIENTIFIC_CARRIER`。下一动作恢复 carrier
   remap；在至少三个候选完成方法形态、预期增量、包装句、formal readiness、
   最小补债和失败轮换点比较前，不得激活 carrier 或运行实验。

### 核心失败机制

T014 在公开检索端没有获得足够的独立来源：两个 S2/arXiv broad archive 均为零，
IEEE 只有 Route A 一条结果。该证据只关闭“再做一次标准 coverage repair 能否满足
三源门”这一不确定性，不关闭 B9 family。

### 排除的替代方案

- 不做第三个 B9 Step 1 repair，不降低三源/mechanism-deep 门。
- 不把历史 shared-index source 字符串、失败调用或零结果配置计为真实来源。
- 不进入 B9 Step 2/3/4a，不将 coverage blocker 包装为创新空白或方法材料。
- 不在 formal remap 前恢复 C15/B12/B1/A4 的实现或实验。

### 影响范围

- live authority 指向本 D028；foreground 为 epoch 35 / CP014 /
  `POST_B9_CARRIER_REMAP`；
- formal stage 保持 Groundwork，无 active scientific carrier；
- B9 的 T013/T014 metadata 和 coverage 失败作为 portfolio 证据保留，未来只有
  新的外部来源能力或正式范围变化才可重新评估，不得原样重试。

### 来源

live S001/D017/V037；T014 worker log、receipt/raw archives；commit `5ba5a54c`。

---

## D029: 激活 B12 source-native fade-reliability MAP standalone carrier

> status: superseded
> date: 2026-07-27
> 取代：D028（只取代“无 active carrier”与 remap 下一动作；D028 对 T014/B9
> 的接收、回池与第三包禁令保留）
> 被取代：D030
> 依据：调研 live R005 + formal D012/D013/D014/D022/D028 + B12
> `literature_notes.md` Q2 与两篇本地全文
> 触发原话：无（技术推导）

### 决策

1. formal carrier 激活为
   `B12_MAP_FADE_AOPN_STANDALONE`，仍处于 GW Step 4a 维度 D。它是
   B12-Q2 standalone 新契约，不是 T006 B10+B12 combination repair。
2. `positive_method_target`：按 OECC 2025 Eq.4–7 与 TSP 2022 [5] 的
   Σθ/Σε 定义实现 source-structured MAP，对 receiver-visible
   amplitude/innovation 驱动的异方差 AOPN 权重加入有界
   observation-precision/standardized-residual clip，形成深衰落可靠度稳健化。
3. `minimal_construct`：source-structured MAP + 一个预注册 reliability
   bound；identity
   和 direct-information tests 通过后，同包完成 primary GG+Wiener paired
   comparison。
4. `fair_comparator`：source-structured PA、PA-ML、MAP、fixed-variance 或
   hard fade skip，以及同一 TX/pilot/data/realization 上 validation-frozen
   BPS 或 DD-DPLL。
5. `primary_packaging`：深衰落星地高阶 QAM 的幅度可靠度约束 MAP CPR；
   `fallback_packaging`：source-native MAP 的 working-region/失稳边界与
   low-complexity robustness–performance trade-off。negative/boundary 不是主方法。
6. T015 单包退出：source-like 排序失败即 `BLOCKED_IDENTITY`；无法建立共同
   working region 只记 boundary；robust method 不胜 MAP、cheap rule 与
   traditional B* 则最多 `FAIR_COMPARISON_RUN`。OECC 未给 W、pilot sequence、
   sample count/seed 和 penalty 精确定义；全部必须标 project assumptions，
   不允许宣称 bit-exact/full-numeric reproduction，也不允许第二个 B12 repair 包。
7. 独立 dispatch review PASS 前不得执行 T015；executor 完成后由不同 agent
   独立科学验收。

### 理由

R005 证明当前不足三个 direct-ready scientific carrier：B12 standalone 是唯一
`NEEDS_SMALL_ADAPTER`；C15 仍为 `HYPOTHESIS_ONLY`，下一包 method delta 必为
NONE；B1/A4/B10/B9 均有明示 no-repair/return 边界。B12 已有 Q#、Step 1–3、
本地全文和精确公式恢复路径，能在一个包中把必要 identity preflight 与正向构造、
公平对照连起来，因而比至少两个替代项更可能产生 `METHOD_SIGNAL`。

### 排除的替代方案

- 不恢复 C15 第三个 formalization 包，不做 T012 第四 amendment；
- 不返回 B1/A4/B10 的被禁止修复包，不做第三个 B9 Step 1 包；
- 不复用 T006 组合实现，不接回 B10，不做 CW+MAP 或无来源联合 CFO ML；
- 不把 source/test/governance PASS 或 negative/boundary 写成方法。

### 影响范围

- live authority 指向本 D029；
- foreground 为 epoch 36 / CP014 / `B12_STANDALONE_METHOD_PREP`；
- T015 dispatch 前只允许 task preparation、contract review 和绑定验证；
- formal 阶段保持 Groundwork Step 4a，不进入 Step 5/Contract/Execute。

### 来源

live S001/R005/D018；formal D012/D013/D014/D022/D028；B12 本地全文与
`projects/thesis-fso/literature_notes.md`。

## D030: 接收 T015 novelty/physics dispatch block 并撤销 B12 active carrier

> status: superseded
> date: 2026-07-27
> 取代：D029（取代 B12 active carrier 与 T015 派遣；D029 的 source 边界、
> project-assumption ceiling 和 no-second-repair 约束保留）
> 被取代：D031
> 依据：验证 live V038/V039/V040 + IEEE primary metadata
> 触发原话：无（独立科学审查）

### 决策

1. formal 接收
   `BLOCKED_NOVELTY_COLLISION / PACKAGE_WITHDRAWN_BEFORE_EXECUTION`。T015
   从未通过 dispatch review，未运行 seed，不能形成 B12 science verdict 或
   `CONSTRUCT_CREATED`。
2. 原 contract 有两项 P0：湍流 state lifecycle 把无来源的 iid 100-symbol
   channel block、128-symbol algorithm block 与物理 coherence 混用；Huber
   IRLS precision 错写为 `w²/sigma_eps`，正确为 `w/sigma_eps`。
3. DOI `10.1109/JLT.2025.3600402` 的 primary identity/abstract 已直接覆盖
   Huber robust update + covariance adaptation + Bayesian CPR，并报告相对
   BPS 的 0.66 dB 级收益。全文合法恢复失败，因此不能建立 B12 one-step
   batch adapter 的方法差异；按 novelty gate fail-closed。
4. B12-Q2 family 不 Kill，但 standalone 当前路线返回池并禁止第二个 B12
   repair。formal active carrier 清空；仍留在 GW Step 4a，不进入 Step 5。
5. 下一 formal action 仅为 post-B12 carrier remap：比较至少 B4、B6、C15
   三种机制的六维 readiness，并由独立 agent 审查。新 owner 与 clean task
   binding 前禁止任何实验。

### 理由

方法有效性不能替代 source/novelty 合法性。generic Huber CPR 已有直接竞品，
而原 T015 又会用非物理 fade lifecycle 改变增益来源；继续执行只能生产不可包装
的工程 adapter 或假方法信号。轮换符合 D029 的单包退出边界。

### 排除的替代方案

- 不做第二个 B12 source/fulltext/implementation repair；
- 不用摘要缺公式作为忽略 collision 的理由；
- 不恢复 B10+B12 combination、CW+MAP 或未闭合的联合 CFO ML；
- 不进入被禁止的 B1/A4/B10/B9 repairs、Scout/P03 或 Step 5。

### 影响范围

- live authority 指向 D019；
- foreground 为 epoch 37 / CP015 / `POST_B12_NOVELTY_REMAP`；
- formal active carrier=`NONE`，T015 withdrawn；
- formal 阶段保持 Groundwork Step 4a。

### 来源

live S001/D019/V038/V039/V040；T015；IEEE document `11129614`；
DOI `10.1109/JLT.2025.3600402`。

---

## D031: 授权 C15 一次性 Step 1–2 formalization，不激活 scientific carrier

> status: superseded
> date: 2026-07-27
> 取代：D030（只取代 post-B12 remap 下一动作；D030 对 T015/B12 的接收、
> no-second-repair 与实验禁令保留）
> 被取代：D032
> 依据：live R006/D020 + B4/B6/C15 独立 formal-readiness audits +
> Groundwork Step 1–2 规范
> 触发原话：无（技术推导）

### 决策

1. formal workline 激活为
   `C15_DISK_NATIVE_FORMALIZATION_ADAPTER / CANDIDATE_FORMALIZATION`；
   formal active scientific carrier 仍为 `NONE`。C15 不是 runnable
   Step 4a carrier，不得运行 seed/MVE。
2. T016 是新的、一次性的 Step 1 view/recent identity/canonical staging 包，
   取代旧 T012 interface，不继承旧 preflight amendment。Step 1 只可复用
   T011 archives 与项目 frozen shared index，
   以实际 source identity、语义去重、priority 和 coverage 通过
   `gw-search.md` 质量门；Step 2 只可闭合明列 recent/canonical fulltext，
   遵守 `gw-acquire.md` 获取止损。
3. 若 atomic source family ≥3、去重候选 ≥20、正式发表 ≥50%、必读 ≥5、
   ≥2 技术子方向、8–12 篇 pool、recent fulltext ≥5 且 canonical 3/3 worktree
   staging 均闭合，T016 生成 preliminary coverage-gap report 并停止在
   `AWAITING_CANONICAL_PROMOTION`。T016 禁止写 shared main repo；promotion
   另包独立审查，正式 coverage confirmation 前不得进入 Step 3。
4. T016 的 method delta 冻结为 `NONE`；source、metadata、canonical、coverage
   或 governance PASS 都不是方法。任一硬门失败即
   `BLOCKED_FORMAL_READINESS`，C15 返回池并禁止第二个 source package。
5. R006 已证明为什么这比 B4、B6 更接近方法信号：C15 有具名 construct、
   comparator、cheap rule、现存 FIR runner 与明确 Step 3 collision gate；
   B4 尚无 carrier-specific M-C-A 且缺核心实现，B6 已被 direct sources 与
   D006 边界压缩到无正向合同。
6. 独立 dispatch review 与 clean committed binding 前不得执行 T016。T016
   完成后由不同 science verifier 裁决 formal disposition、method delta、
   streak、weight 与 drift。

### 排除的替代方案

- 不把 C15 formalization 写成 active scientific carrier 或方法包；
- 不续修 T012，也不恢复其复杂 CIM/process preflight；
- 不运行旧 C15 shared-mu sandbox，不使用 seeds 71–80，不精读或写 Q#；
- 不恢复 B4/B6/B1/A4/B10/B9/B12 或 Scout/P03 的实验。

### 影响范围

- live authority 指向 D020；
- foreground 为 epoch 38 / CP015 / `C15_FORMALIZATION_PREP`；
- T016 只允许 Step 1–2 source/fulltext formalization；
- formal stage 保持 Groundwork；没有 active scientific carrier，不进入
  Step 3/Step 4a experiment/Step 5/Contract/Execute。

### 来源

live S001/R006/D020；formal D030；T011/T012 receipts；B4/B6/C15 三项
readiness audit；`stages/gw-search.md`、`stages/gw-acquire.md`。

---

## D032: 接收 C15 formal-readiness identity block 并清空 workline

> status: superseded
> date: 2026-07-27
> 取代：D031（取代 C15 当前 formalization workline；D031 的一次性退出、
> method-delta NONE 与实验禁令保留）
> 被取代：D033（只取代下一 formal workline；T016/C15 正式处置继续有效）
> 依据：验证 live V047 + T016 Phase-A artifact/worker log
> 触发原话：无（独立科学验收）

### 决策

1. formal 接收
   `BLOCKED_FORMAL_READINESS / BLOCKED_IDENTITY_CONFLICT`。T016 在 A1
   正确停止，未形成 acquisition pool、recent identity、canonical staging、
   coverage confirmation、Step 3 或任何实验。
2. T016 的 `mission_method_delta=NONE`。数量门的局部 PASS 不能激活 scientific
   carrier，也不能形成方法或论文结论。
3. candidate view 的三组 DOI conflict 足以触发冻结 hard block；V047 又确认
   provenance summary 不完全可复现，故该 artifact 只保留为 partial defensive
   evidence。
4. C15 family 不 Kill，返回候选池；不得第二个 source/formalization package，
   不得 Phase B、alias repair、旧 shared-mu sandbox、Step 3 或 MVE。
5. formal active scientific carrier 继续为 `NONE`；foreground 转 epoch41 /
   CP016 / post-C15 remap。新 owner 与 task 通过独立审查前不得运行任何新实验。

### 理由

D031 已预注册任一 source/canonical/coverage hard gate 失败即返回池。按冻结
合同接收 stop、同时拒绝不完整 coverage 声称，既保留 C15 未被科学 Kill 的正确
边界，也阻止 no-method mission 继续积累元数据 repair。

### 排除的替代方案

- 不修 `.short`/`.v1` alias 后继续 T016；
- 不把数量门 PASS 晋级为 Step 1/2 PASS；
- 不运行 Phase B、Step 3、旧 C15 sandbox 或 seed/MVE；
- 不恢复 B1/A4/B10/B9/B12 等已禁止 repair。

### 影响范围

- live authority 指向 D021；
- C15=`BLOCKED_FORMAL_READINESS / RETURNED_TO_POOL /
  NO_SECOND_SOURCE_PACKAGE`；
- foreground=epoch41 / CP016 / post-C15 remap；
- formal stage 保持 Groundwork，无 active scientific carrier。

### 来源

live S001/D021/V047；T016；step-016 worker log；candidate-view artifact；
formal D031。

## D033: 授权 C16-open 一次性 Step 1–2 formalization

> status: superseded
> date: 2026-07-27
> 取代：D032（只取代 post-C15 remap 的下一 formal workline；D032 的 T016
> identity block、C15 return/no-second-source 边界保留）
> 被取代：D034（只取代当前 formal workline 与下一动作；D033 的 T017
> 一次性合同、C16-open no-second-source 与 science ceiling 保留）
> 依据：调研 live R007 + current portfolio/harvest + Q14 D044 + formal D032
> 触发原话：无（机制级 remap 的技术推导）

### 决策

1. 当前 formal stage 继续为 `GROUNDWORK`，active scientific carrier 继续
   `NONE`。R007 的 readiness census 为
   `READY=0 / NEEDS_SMALL_ADAPTER=0 / HYPOTHESIS_ONLY=5`。
2. 只授权 C16-open
   `FULL_COMPLEX_2X2_FIR_NONMODULUS_FORMALIZATION` 一次性 Step 1–2
   workline。候选 positive target 是 capability-aligned complex FIR
   non-modulus blind equalizer，不是旧 spatial whitening+real-Givens code。
3. T017 action class 为 `CANDIDATE_FORMALIZATION`，预期
   `mission_method_delta=NONE`。允许多源检索、AI candidate review、
   bounded acquisition、title/source identity/content-quality 检查与
   coverage-gap report；禁止精读、Q#、实现、simulation/Probe/MVE。
4. Step 1 门为 actual source≥3、unique≥20、正式发表≥50%、必读≥5、
   route≥2；Step 2 门为 priority pool 8–12 且合法 fulltext≥5。
5. 成功终态只能是 `AWAITING_COVERAGE_CONFIRMATION`，未经用户极短确认不得
   进入 Step 3。失败终态为 `BLOCKED_FORMAL_READINESS`，C16-open 返回池且
   不得第二个 source/formalization package。
6. task、owner、control 与 current projections 必须先经独立 dispatch review；
   review PASS 前不得执行 T017。

### 理由

current portfolio 已明确旧 C16 的机制负面无效：其 comparator 缺 11-tap FIR
能力，且使用污染 seeds/post-hoc oracle。这个 amendment 只证明 axis reopened，
不证明新方法有效。一次 Step 1–2 formalization 是把“可能存在 task-matched
非模 FIR 方法族”转成可审查文献身份的最小合法动作；它比直接改代码更符合
FR-22，也比继续 C15/B1/B10 等 repair 更符合 method-production rotation。

### 排除的替代方案

- 不把旧 C16 synthesis 恢复为 current science；
- 不把 generic JADE/ICA provenance 当 complex convolutional FIR 身份；
- 不在检索/全文门前实现 FIR HOS；
- 不因 formalization PASS 直接激活 carrier 或记 method delta；
- 不绕过 `gw-acquire.md` coverage confirmation 人工门。

### 影响范围

- live authority 转 D022；foreground=epoch42 / CP016；
- formal carrier 仍 NONE，new workline=C16 Step 1–2 only；
- C15、B1、A4、B10、B9、B12 的退出/repair 禁令不变；
- T017 验收前不改变 GW Progress 或 literature_notes 的完成状态。

### 来源

live S001/R007/D022；formal D032；portfolio/current；harvest/current；
Q14 S039/D044；R006。

## D034: 接收 T017 formal-readiness block 并清空 C16-open workline

> status: superseded
> date: 2026-07-27
> 取代：D033（只取代 C16-open 当前 formal workline 与下一动作；D033 的
> 一次性退出、method-delta NONE 与实验禁令保留）
> 被取代：D035
> 依据：验证 live V049 + T017 worker/candidate/raw artifacts
> 触发原话：无（独立科学验收）

### 决策

1. formal 接收
   `BLOCKED_FORMAL_READINESS / BLOCKED_SEARCH_OR_IDENTITY`，delta=`NONE`。
   T017 在 A6 正确停止，未进入 Phase B、coverage confirmation、Step 3、
   Q#、实现或实验。
2. 正确冻结数字为 source family=`1<3`、unique=44、
   published/preprint/unknown=`41/3/0`、ratio=`0.9318181818`、
   must-read=`2<5`、R1/R2 direct=`1/3`、pool=10、quarantine=0。
3. V049 的 TechRxiv 误标与缺 per-source receipt 使 artifact 证据质量
   PARTIAL；两项均不改变 source/must-read 双硬失败，不能触发 repair。
4. C16-open family 不 Kill，返回候选池；不得第二个 source/formalization
   package、Phase B、第六查询、label/receipt repair、旧 spatial HOS 或 seed。
5. formal active scientific carrier 继续为 `NONE`；foreground 转
   epoch43 / CP017 / post-C16 remap。新 owner/task 通过独立审查前不得运行
   任何新实验。

### 理由

D033 已预注册 source 或必读密度门失败即返回池。接收局部数量/route 信号但
拒绝跨过多源与核心材料门，既不把检索失败冒充方法负面，也阻止 no-method
mission 继续消耗第二个元数据修复包。

### 排除的替代方案

- 不修 TechRxiv label、source receipt 或追加第六查询后继续 T017；
- 不运行 Phase B、Step 3、旧 C16 sandbox 或 seed/MVE；
- 不把 published ratio、route 命中或 task PASS 晋级为方法增量；
- 不恢复 C15/B1/A4/B10/B9/B12 等已禁止 repair。

### 影响范围

- live authority 指向 D023；
- C16-open=`BLOCKED_FORMAL_READINESS / RETURNED_TO_POOL /
  NO_SECOND_SOURCE_PACKAGE`；
- foreground=epoch43 / CP017 / post-C16 remap；
- formal stage 保持 Groundwork，无 active scientific carrier。

### 来源

live S001/D023/V049；T017；step-017 worker log；candidate/raw artifacts；
formal D033。

---

## D035: 激活 Q14 mandatory Step 3.5 problem-evidence formal workline

> status: superseded
> date: 2026-07-27
> 取代：D034（只取代 post-C16 当前 formal workline 与下一动作；D034 对
> T017/C16-open 的正式处置与退出边界继续有效）
> 被取代：D036
> 依据：调研 live R008 + Q14 S037/S038/S039/D044 + current
> portfolio/master-state + framework gw-supplement/gw-feasibility
> 触发原话：无（技术推导；长期 Goal 自主推进授权见 live D004）

### 决策

1. formal 选择 Q14 获得一次 Groundwork Step 3.5 /
   problem-evidence workline；这不是 active scientific carrier，formal
   active carrier 继续为 `NONE`。
2. T018 只执行关键词矩阵、多源检索、核心竞品双向引用链、新论文合法
   acquire/read、收敛检查与四判据 2 裁决；固定 delta=`NONE`。
3. positive method contract：
   - target：strictly-causal receiver-visible additive residual after
     always-online standard CMA；
   - minimal construct 仅在未来 gates 后为
     `z_out=z_CMA+gφ(z_CMA, causal trace/context)` + no-op gate；
   - fair comparator：tuned standard CMA、tuned CMA+DD-LMS/RDE、
     equally-budgeted simple residual DSP；
   - primary packaging：保留盲跟踪的轻量因果 residual correction；
   - fallback：条件式触发规则与复杂度/性能边界。
4. Step 3.5 只有 actual Semantic Scholar + 至少一源、双向引用链、最多三轮
   收敛与新增高相关论文处理全闭合后才可裁决问题证据。
5. `PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO` 也只允许主控另建 A0 owner/task；
   executor 无权激活 carrier 或进入 Step 4a。
6. coverage/fulltext/convergence 失败或判据 2 仍 UNKNOWN/FAIL 时，Q14 返回池，
   不给第二个 problem-evidence package；按 live R008 轮换。
7. foreground 为 epoch44 / CP017；独立 dispatch review PASS 前禁止执行
   T018。禁止所有 simulation/Probe/MVE/seed、旧路线修补、Scout/P03、
   Step 5/Contract/Execute。

### 理由

Q14 已有合法 Step 1–3 与 5 篇全文，问题接口和 strongest cheap comparator
均可从现有 receiver 资产定义；未完成的是框架明确强制的 Step 3.5 和判据 2。
相对 Q-ML4 的多重场景迁移、B4 的问题/实现双债和 C04/C09 的退化 target，
该 workline 最接近一个可证伪的 Step 4a 入口，同时失败成本最低。

### 排除的替代方案

- 不运行 residual MVE 反向证明问题；
- 不把 local negative、oracle gap、TX truth residual 或无直接先例写成合法性；
- 不先做 Q-ML4 scene transfer、B4 PADE 实现或 C04/C09 GRU；
- 不修 T017/C16 source receipt、label 或任何既有 no-repair workline。

### 影响范围

- formal stage 保持 Groundwork；
- active scientific carrier=`NONE`；
- Q14=`STEP35_PROBLEM_EVIDENCE_WORKLINE_SELECTED_NOT_ACTIVE`；
- foreground=epoch44 / CP017；T018 最终验收前不进入 A0 或实验。

### 来源

live R008/D024；Q14 R009/S037/S038/S039/D044；R006/R007；
portfolio/current；master-state；gw-supplement；gw-feasibility。

---

## D036: T018 delegated coverage gate 与 receipt contract formal amendment

> status: superseded
> date: 2026-07-27
> 取代：D035（保留 Q14 一次性 Step 3.5 workline、positive method contract、
> carrier=`NONE`、delta=`NONE` 与失败即轮换；只取代 dispatch contract）
> 被取代：D037
> 依据：critic live V050 + framework gw-acquire/gw-supplement + tools/search CLI/source
> 触发原话：live `voice.md` 2026-07-26（D004 已记录 Goal 主控端到端授权；本次无新原话）

### 决策

1. formal 继续授权 Q14 一次 mandatory Step 3.5/problem-evidence workline；
   active scientific carrier 仍为 `NONE`，T018 固定 delta=`NONE`。
2. 若检索新增 1–5 篇必读/建议读，Phase B 分为：
   `acquire + coverage-gap report → independent verification → delegated master
   approval → read`。前一步未形成磁盘 PASS receipt 时不得进入后一步。
3. D004 的用户端到端授权只在本 mission 中把 `gw-acquire` 的技术 coverage
   confirmation 委托给 Goal 主控；不允许 executor 自认通过，也不修改通用
   framework。私有全文或用户独占材料仍是外部资源阻塞。
4. T018 必须使用冻结 `-o` 路径，分开七个 terminal 与两个 continuation
   状态；continuation 不形成 CP、formal disposition、streak 或 no-method 计数。
5. 既有与新增论文全文的权威根冻结为共享主仓库
   `D:\code\study\research-protocol\papers`；worktree 稀疏 `papers/` 不得用来
   判断全文缺失。executor 必须记录共享 content path/hash并保护既有改动。
6. foreground=epoch45 / CP017 /
   `Q14_STEP35_TASK_AMENDMENT_REVIEW`；独立复审 PASS 前不得执行。
7. Q14 Step 4a/A0、实现、实验、第二个 problem-evidence package和既有
   no-repair workline继续禁止。

### 理由

初版科学方向与正向合同由 V050 确认成立，但 task 在 Step2→3 coverage gate、
固定 citation receipt 与 continuation schema 上不合法。把 acquisition 与 read
拆开，并在中间加入独立 verifier + delegated master gate，既保留框架防偏目的，
又执行用户“不负责阅读技术日志或判断科学正确性”的最新明确授权。

### 排除的替代方案

- 不删 coverage gate，也不把 report 当形式性 PASS；
- 不让 executor 同时获取、确认、精读和综合；
- 不因 task-contract 修复把 Q14 冒充 active carrier 或方法进展；
- 不运行 Step 4a/MVE 反向证明问题合法性。

### 影响范围

- formal authority 切换到 D036；
- live D025/T018/control/current projections 同步 epoch45；
- mission checkpoint 仍为 CP017，方法 streak 不变；
- T018 必须重新经过独立 dispatch review。

### 来源

live V050/D025/D004；R008；D035；Q14 S037/S038；T018；gw-acquire；gw-supplement；
tools/search CLI。

---

## D037: 激活 Q15 prefix-gated shell calibration 的 Groundwork Step 1–2

> status: superseded
> date: 2026-07-28
> 取代：D036 的 Q14/T018 当前 formal workline；Q14 保持冻结未决
> 被取代：D038
> 依据：验证 live V053 + live D028 + T020 commit `5cf76d5`
> 触发原话：无（技术推导）

### 决策

1. formal active scientific carrier 仍不记为 Step 4a carrier；只建立 Q15 的
   `GROUNDWORK_STEP1_2_WORKLINE_SELECTED`。
2. Q15 候选动作是：在 fixed-μ blind FIR CMA 后，用 receiver-visible
   calibration prefix 检测低功率/多壳层塌缩；健康时 identity，触发时应用
   frozen public-16QAM quantile-shell radius transport。
3. T020 只作为 Step 1 的 diagnostic seed，不完成任何 GW Step。它支持的上限是
   “值得检索和获取全文”，不支持 Q15 四判据、novelty、formal comparator 或
   MVE Go。
4. T021 只执行 Groundwork Step 1 与 Step 2：完成多源候选检索、AI 初筛、二轮
   定向检索、direct-collision/cheap-alternative map、公共全文获取与
   coverage-gap report，然后暂停。
5. Q15 的必查替代解释包括：robust/tuned CMA、RDE/MMA/MCMA、restart/
   multistart/reinitialization、blind AGC/normalization、radius-directed 或
   distribution-matching post-equalization。若 direct competitor 已覆盖同一
   M-C-A，或稳健传统替代直接吸收问题，必须如实报告，不得靠改名保留候选。
6. coverage report 未经主控验收前，禁止 Step 3 精读；即使 coverage PASS，也
   必须由新递增 formal/live decision 授权下一包。

### 理由

live V053 接收了本 campaign 第一个 P0=0 的 factory-level 方法信号，但也确认
改善由 7/20 seeds 的 CMA collapse 主导。继续工厂会违反 one-last package；
直接实验会跳过 FR-22，并可能把初始化/传统 baseline 脆弱性误包装为方法贡献。
Step 1–2 能以最低成本回答新颖性碰撞、近期 baseline 和 cheap-alternative
三项决定性问题。

### 排除的替代方案

- 不恢复 Q14/T018：Q15 已有实际构造与 held-out 诊断信号，方法产出距离更短；
- 不直接进入 Step 3 或 4a：尚无 Q15 专属全文池与合法 Q#；
- 不补 T020 artifact 后重跑：这些是 formal experiment 前的证据合同债，不是
  Step 1–2 的前置阻塞；
- 不创建新 scientific topic：Q15 仍属于既有 dual-pol OSL Groundwork owner。

### 影响范围

- formal topic 的 current workline 切换到 Q15 Step 1–2；
- live epoch51/CP019/T021 与本决策绑定；
- master-state/current projections 更新；Q14/T018 保留冻结历史，不作 Kill。

### 来源

live D028/V053；T020；groundwork/gw-search/gw-acquire；FR-22。

---

## D038: 接收 Q15 Step 1–2 PARTIAL 并授权带收据前置门的 Step 3

> status: superseded
> date: 2026-07-28
> 取代：D037 的 Step 1–2 workline
> 被取代：D039
> 依据：验证 live V054 + live D029 + T021 commit `287fb6a`
> 触发原话：无（技术推导）

### 决策

1. Q15 formal stage 保持 `GROUNDWORK`，无 active Step 4a carrier。
2. T021 接收为 `STEP1_EVIDENCE_PARTIAL / STEP2_COVERAGE_PARTIAL`：129、
   121/129、11 必读和六篇独立核心全文有效；三源 PASS 因 IEEE raw receipt
   缺失撤回。
3. T022 获得一次 `GROUNDWORK_STEP3_WITH_RECEIPT_PREFLIGHT` workline：
   先闭合 IEEE raw 与五篇 blit canonical/index receipt，再精读六篇独立核心与
   两篇补充全文。
4. Step 3 产出必须包含 direct-collision、cheap-alt、传统 comparator 与 Q15
   M-C-A/四判据表；D1/C1/C4 固定为 Step 3.5 mandatory debt。
5. D1/C1/C4 未闭合时，Step 3 只能形成 `PENDING_STEP35` 的 Q# 候选，
   不得把四判据写成最终全过；未经新决策不得进入 Step 3.5、4a、实现或实验。

### 理由

T021 已有足够多的真实全文开始形成科学判断，但完整性收据不满足“Step 1 全门
PASS”。合并前置修复与精读，比降低门槛或新增纯修复包更符合 FR-22 和
method-production 的产出约束。

### 排除的替代方案

- 不把 T021 直接记为 Step 1 PASS；
- 不因一项 raw receipt 否定全部全文；
- 不越过 Step 3 精读直接使用 T020 诊断信号；
- 不恢复 Q14/T018 或第三轮方法工厂。

### 影响范围

- formal workline 更新为 Q15 Step 3 with receipt preflight；
- foreground epoch52 / CP020 / T022；
- Step 3.5/4a/实验继续锁定。

### 来源

live D029/V054；T021；groundwork/gw-acquire/gw-read；FR-22。

---

## D039: 接收 Q15 Step 3 PARTIAL 并授权终局 Step 3.5 + 条件式 Step 4a

> status: superseded
> date: 2026-07-28
> 取代：D038 的 Step 3 workline
> 被取代：D040
> 依据：验证 live V056 + live D030 + T022 commit `f3a47260f732e0987743f32bffc6d21d7f92e6aa`
> 触发原话：无（技术推导）

### 决策

1. formal stage 保持 `GROUNDWORK`；T022 只接收为
   `STEP3_CONTENT_COMPLETE_WITH_SCIENTIFIC_REFRAME`。
2. Q15 四判据当前为 `1=PARTIAL / 2=PARTIAL / 3=PASS / 4=PASS`，不是合法
   Step 4a Q#。D1 公开全文和定向 normalization/MMA 证据必须先在 Step 3.5
   闭合。
3. T023 Phase A 只做 Step 3.5。只有 Phase A 形成四判据全过 Q#，才允许同包
   进入 Phase B Step 4a。
4. Phase B 的首要对手是 correct sqrt amplitude normalization，而不是裸 CMA
   或 oracle。必须同时比较 pooled/per-pol/robust/gated scalar 与 M2/M4，
   使用严格 prefix、共享 realization、seed-cluster CI 和 fresh seeds。
5. T023 是 Q15 最后一个 work package。No-Go/blocked 均退出；只有
   `Q15_STEP4A_RECOMMENDATION_READY` 才返回主控请求用户确认，不自动进 Step 5。

### 理由

Step 3 精读确认 equalizer-internal radius/switching 先例很多，但没有排除输出端
Q15 的信息增量。与此同时，T020 conventional scalar comparator 的振幅公式错误，
使当前正信号不能支撑问题存活。把 Step 3.5 与条件式 Step 4a 合并，既遵守
FR-22 的顺序门控，也避免再产生一个只修文档或只修 baseline 的空包。

### 排除的替代方案

- 不把 T022 直接标 Step 3 全 PASS；
- 不在 Step 3.5 前运行 Step 4a；
- 不恢复第三个普通 method factory；
- 不把 D1/C1/C4 全文数量当唯一门；真正门是 direct collision 和合法强简单
  comparator；
- 不授权 Step 5/Contract/Execute。

### 影响范围

- formal current workline 更新为 Q15 terminal Step 3.5 + conditional Step 4a；
- live epoch53 / CP021 / T023；
- T020 artifacts 保持只读，所有新实证进入隔离目录。

### 来源

live D030/V056；T022；T020 source audit；groundwork/gw-supplement/
gw-feasibility；FR-22/FR-25。

---

## D040: Q15 map formal No-Go，派生 G1 gated normalization 诊断 carrier

> status: active
> date: 2026-07-28
> 取代：D039 的 Q15 terminal workline
> 被取代：无
> 依据：验证 live V058 + live D031 + T023 commit
> `89d8174c56a7729c34a1268ef52394c58e889924`
> 触发原话：无（技术推导）

### 决策

1. T023 因 Phase A 四判据未全过却进入 Phase B，不接收为合法 Step 4a。
   Q15 nonlinear-map formal disposition 为 `STEP35_NO_Q_NO_GO`，不得 repair。
2. 越门 Phase B 仅作 diagnostic：M4 map 在 old/fresh 都输给同门控 correct-sqrt
   scalar；但 `gated_scalar` 相对 tuned CMA 的诊断改善与 healthy-worst=`0`
   成立，登记为 `METHOD_SIGNAL / NONBINDING_DIAGNOSTIC`。
3. 以 Q15-derived fallback / salvaged component
   `G1_SAFE_GATED_NORMALIZATION` 进入 T024。先完成 gated
   normalization 自身的 recent-baseline/direct-collision/四判据闭合；全部 PASS
   后才允许同包 formal Step 4a confirm。
4. T024 使用全新 seeds、完整 gate/prefix/scale/offline-class raw receipt，并把
   gated scalar 与 tuned CMA、always-on correct normalization、M4 map 和最强
   target-matched cheap alternative 逐对比较。
5. T024 无论 collision、blocked 或 confirm FAIL 都退出 G1；PASS 只形成
   recommendation-ready method card，不进 Step 5。

### 理由

T023 的 binding 终态不合法，但它意外分离了两个机制：nonlinear map 没有增量，
receiver-visible identity fallback + correct scale 则在两组诊断 slices 上兼有恢复
和健康安全。该低复杂度构造比当前 hypothesis-only 候选更接近毕业方法，值得一次
守门后的正式确认。

### 排除的替代方案

- 不恢复 Q15 map 或第四次 Q15 repair；
- 不把越门实验直接当 formal Step 4a；
- 不把 always-on normalization 的健康退化误写成低于 MDE；
- 不先做纯文献包再另留实验包；T024 合并碰撞门与条件式 confirm。

### 影响范围

- formal stage 仍为 Groundwork；
- active formalization workline 改为 G1 delta-specific closure + conditional
  Step 4a；
- live control 由 D031/V058/epoch54/CP022 管理。

### 来源

live D031/V058；T023 raw/result/source；D039；FR-22/FR-25。
