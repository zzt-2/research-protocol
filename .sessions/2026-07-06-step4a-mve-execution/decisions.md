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
