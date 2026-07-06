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
