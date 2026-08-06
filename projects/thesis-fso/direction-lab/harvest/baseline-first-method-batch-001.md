# Baseline-first Method Batch 001

> 日期：2026-08-06
> 范围：Research Direction Lab / design-only method synthesis
> 权威优先级：active decision / supersession banner > inventory > 旧正文
> 禁止动作：不检索空白，不实现，不仿真，不跑 MVE，不新建 Groundwork 专题
> **Terminal：`STRATEGIC_SHORTAGE_CONFIRMED`**

## 0. 裁决摘要

本批严格按“近期合法 baseline → 目标条件失效 → deployable action → 方法步骤 → comparator / cheap alternative → 章节包装 → 历史碰撞”生产。全文精读由三个独立子 agent 完成，主控只接收结构化摘要；本地论文库共确认 7 篇 2019+ 正式 baseline。基于其中 5 篇逐篇构造了 5 张完整方法卡，但 5 张分别在问题证据、现有动作、已关闭 dead end 或 strongest cheap alternative 门停止，survivor=0。

这不是“未找到空白”，也不是用负面审查代替方法生产：五张卡均先形成 receiver-visible input、deployable action、3–7 步流程、主图、消融与双层 packaging，随后才执行碰撞收据和十项门控。终局只说明：**当前本地 receiver/baseline 池与既有 testbed 下，没有合法的第二项方法候选；继续生产必须显式改变 candidate source、target chapter 或 research object。**

## 1. Phase A — 近期合法 baseline 池（7 篇）

### B01 — Paillier et al., JLT 2020：AGC + 二阶 DPLL

1. **方法 M**：AO 后数字 AGC 固定检相器增益，二阶 DPLL 拉入残频并逐符号跟踪相位。
2. **deployable input**：粗频偏预补偿、AO、相干检测和符号同步后的复数 I/Q；不使用 TX truth。
3. **action/output**：AGC 单位功率化 → BPSK 相位误差 → 比例/积分环路与 NCO 去旋转；输出载波同步符号。
4. **算法步骤**：AGC → `sI·sQ` 检相 → 二阶环路滤波 → NCO 积分 → 下一符号旋转 → 判决/差分译码。
5. **固定假设**：10-GBaud BPSK；GHz Doppler 已粗补、残频最大 100 MHz；理想 timing；AO 工况已成立。
6. **已知限制**：论文明确限定 BPSK、理想 timing、粗 FOE 不在范围内；高阶调制须换检相器；衰落使失锁临界 SNR 恶化约 5 dB。
7. **thesis-fso C/A**：当前 QPSK/16QAM 与 Gamma-Gamma 通道不能重建 TURANDOT+91 阶 Zernike AO；只能复现算法级闭环，不得迁移论文 AO 数字。
8. **≤半天入口**：现有 `_recovery.py:59-75,121-128` 已有同结构 DPLL 与 FOE→DPLL→VV 链；加论文式 AGC/检相器约 2–4 小时。

全文：`D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md:17,105-144,176,189,199,205`。代码：`projects/simulation/common/_recovery.py:59-75,121-128`，`projects/simulation/common/_channel.py:27-32,73-87`。

### B02 — Tang et al., JPHOT 2022：STSB 帧同步 + FOE

1. **方法 M**：`[A,B,A*,B*]` 共轭对称训练块，以 Park-style metric 定位帧首，再去调制估计 CFO。
2. **deployable input**：时钟同步/均衡后的 1-sps 复样本、receiver-known 对称训练块与训练周期。
3. **action/output**：定位训练块 → 估计 CFO → 补偿当前训练周期 payload；输出起点、频偏和补偿序列。
4. **算法步骤**：构造训练块 → timing metric → 峰值定位 → symmetric multiply → 相位增量聚合 → CFO 补偿。
5. **固定假设**：QPSK；前级同步/均衡完成；相邻符号的 LO/湍流相位近似不变；固定训练周期。
6. **已知限制**：单偏振 900 mm 室内实验；无 fixed-point/PPA；BER 收益混合 timing 与 FOE；只在首周期定位。
7. **thesis-fso C/A**：当前 caller 已持有 pilot/block 位置；不注入未知 frame offset 时 timing 问题不存在；训练信息类不能与 NDA 方法等同。
8. **≤半天入口**：在 `frame_sync_fsts.py:58-78` 替换真实对称块，接入 `joint_estimation_pipeline.py:122-169`；约 2–3 小时。

全文：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_jphot.2022.3161795/content.md:1-21,39-85,115-195`。代码：`projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py:15-78`，`projects/simulation/common/_recovery.py:37-56,435-464`。

### B03 — Wang et al., JPHOT 2023：FSTS 双偏振两阶段 FOE

1. **方法 M**：X/Y 双偏振交错共轭 FSTS，一套序列完成帧同步、支路对齐与粗细两阶段 FOE。
2. **deployable input**：共享 LO 的双偏振训练段、receiver-known FSTS；不需要 TX payload truth。
3. **action/output**：输出帧起点、粗/细频偏及总频偏，并对数据流去旋转。
4. **算法步骤**：FSTS 构造 → Park metric → MRC/偏振解复用 → 跨偏振粗估 → 补粗频偏 → 间隔 `BL` 细估 → 合并补偿。
5. **固定假设**：两偏振共享 CFO/LO；最短训练约 320 symbols；10-GBaud PM-4/16QAM、50 kHz 线宽。
6. **已知限制**：细估捕获范围缩小 `BL` 倍；低功率/短训练时峰消失；`BL/BN` 依赖调制和接收功率；仅仿真。
7. **thesis-fso C/A**：dual-pol 生成器尚未注入共享 CFO/laser phase；若任务仅单偏振或纯 CPE，则 task mismatch。
8. **≤半天入口**：复用 dual-pol channel 与单偏振 carrier 注入，增加 FSTS builder/metric/两级公式；约半天。

全文：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:11-19,101-107,119-160,175-215,231-267,299,309,385`。代码：`projects/simulation/common/_dual_pol_channel.py:56-149`，`projects/simulation/common/_channel.py:35-54`。

### B04 — Fan et al., Optics Communications 2024：短时谱粗 FOE

1. **方法 M**：16 点短 FFT、1024 块谱均值、正负频谱面积偏置与标定系数 `alpha` 映射粗 CFO，结合星历调 LO。
2. **deployable input**：ADC 后、MIMO/均衡前复样本，可加公开星历预测；无 pilot/TX truth。
3. **action/output**：估计大范围粗 CFO/LO 调谐方向，将残频压入后续精 FOE 捕获范围。
4. **算法步骤**：星历预调 → 分块 FFT → 谱平均 → 正负面积偏置 → `alpha` 映射 → 调 LO 并迭代。
5. **固定假设**：2.5-GBaud PM-QPSK、5 GSa/s、20 kHz 激光；`alpha` 绑定硬件谱形；约 3 s PC/LO 循环。
6. **已知限制**：仅 coarse FOE；无明确单次误差范围；残频仍可达 250 MHz；B2B 而非湍流链。
7. **thesis-fso C/A**：当前 residual CFO 仅 1 MHz；历史公平对照已证星历+传统 FFT 19/19 与其持平且精度高约 10 倍，原范围优势归零。
8. **≤半天入口**：仓内已有完整 `short_time_spectrum_foe` 与 iterator，仅需 comparator 包装。

全文：`D:/code/study/research-protocol/papers/doi/10.1016_j.optcom.2024.130981/content.md:1,13-19,45-57,71-95,115-149,167`。代码：`projects/simulation/common/_recovery.py:471-588`；历史：`.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md:134-167,233`。

### B05 — Lin et al., ISCAS 2022：定点低时延 VV4E CPR

1. **方法 M**：QPSK VV4E 的 fixed-point Cartesian FPGA pipeline：近似 MAC、43 路相位降噪树、CORDIC、并行 unwrap 和 LUT 旋转。
2. **deployable input**：含 AWGN/CPN 的并行 QPSK 复样本。
3. **action/output**：定点估计、展开并补偿 carrier phase，输出校正后的复序列。
4. **算法步骤**：四次幂 → 43 路树 → 六旋转 CORDIC → 并行 unwrap → sin/cos LUT → complex multiply。
5. **固定假设**：QPSK；固定 `Nw=43`；MAC 5 fractional bits；trig 7 fractional bits；LUT depth 128。
6. **已知限制**：只含 CPE；7b/5b 相对 float 约 0.25 dB；横向硬件条件不统一；无功耗和统计重复。
7. **thesis-fso C/A**：全链 FOE/SOP/湍流可能改变孤立 CPE 位宽主导关系；软件 bit-true 不能复现 FPGA PPA/22-cycle latency。
8. **≤半天入口**：以 `_recovery.py:78-88` float VV 为 anchor 加 Q-format wrapper；约 2–4 小时。

全文：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_iscas48785.2022.9937906/content.md:1-5,23-25,37-41,55-63,79-180,188-219`。代码：`projects/simulation/common/_recovery.py:78-88,121-128`。

### B06 — Hu et al., JLT 2023：pilot-LMS + receiver-side MIMO detector chain

1. **方法 M**：pilot-LMS 动态信道估计 → 只消除 ISI/记忆的 MIMO FIR → MMSE/SIC/SIC-MLD/MLD 检测器选择。
2. **deployable input**：帧同步/FOE 后多路复样本、已知 pilot、OSNR/EVM、估计信道及 condition。
3. **action/output**：更新 `Hhat`、均衡并选择检测器，输出恢复 QAM 符号；本池只保留接收端子链。
4. **算法步骤**：preamble → pilot-LMS → pilot 间插值 → FIR 去记忆 → 估 OSNR/condition/EVM → detector route → demap。
5. **固定假设**：有限记忆非酉 MIMO；pilot 间可插值；1 pilot + 9 payload；逐帧 CSI 有效。
6. **已知限制**：步长敏感；约 400–500 m 单相位屏；完整 TX loading 受 RTT/Greenwood 门限制；强湍流仅 12 个实现。
7. **thesis-fso C/A**：公共 dual-pol anchor 只有标量衰落+单位旋转；完整 MDM/TX loading 超范围，但邻接 Pilot-Jones testbed 有 2x2 PDL/PMD、pilot-LS 与正则逆。
8. **≤半天入口**：限定 2x2 receiver slice，复用邻接 testbed，加 MMSE/SIC/SIC-MLD 三臂；约 3–4 小时。

全文：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_jlt.2023.3242215/content.md:3,17-29,60-72,93-130,147-171,193-241,281-323`。代码：`projects/simulation/explore/pilot-jones-complex-repair/semantic_channel.py:93-205`，`pilot_and_baselines.py:38-203`。

### B07 — Cao et al., COL 2022：peak-density/K-means 半径校准 + CMMA/RDE

1. **方法 M**：从 PS-QAM 幅度密度峰自动估计环数/初始半径，再以 K-means 精化，替换 CMMA/RDE 固定参考半径。
2. **deployable input**：clock recovery 后的 PS 高阶 QAM 复样本幅度。
3. **action/output**：输出环数、半径和决策边界，驱动 CMMA/RDE 抽头更新并输出均衡符号。
4. **算法步骤**：取内环 → 极坐标幅度 → 局部密度 → 高密度距离 → 定中心/K → K-means → 更新 CMMA/RDE references。
5. **固定假设**：PS 高阶 QAM；内环可辨；聚类块内准静态；clock recovery 已成功。
6. **已知限制**：只验证 PS-256QAM/80 km SSMF/离线 DSP；完整链含 VNLE 与 121-tap DD-LMS；约 1 dB 不能全归因于校准。
7. **thesis-fso C/A**：当前仅均匀 QPSK/16QAM；Gamma-Gamma common gain 会被误当半径漂移；须先分离块级增益与环比。
8. **≤半天入口**：在现有 `CMMAEqualizer2x2` 前加 density-peak/K-means，以 PS-16QAM 做身份适配；约 3–4 小时，不声称精确复现 PS-256QAM 光纤链。

全文：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.3788_col202220.080601/content.md:1-25,42-72,87-140,163-169`。代码：`projects/simulation/explore/cma-fade-divergence/r2_cmma_divergence.py:69-165`。

### 池外排除

- Du et al., PTL 2025 NDA-ML STO/CPE：论文原法用真实相位展开，非 deployable；segmented 路径与 C3 exact action 相同。
- Liu et al., Optics Communications 2023 double-feedback+VV：本地仅 article preview，缺完整公式链。
- JLT 2024 prefix-sum/CT-MLE、JLT 2019 LUT-free DPSK、JLT 2024 temporal-correlation demux：任务或基础设施超过半天门。
- 多篇 OE/JLT calibration/combining 候选只有索引、无本地有效全文，不进入池。

## 2. Phase B/C — 五张 baseline-first 方法卡与碰撞收据

### K01 — Ch4 / Fade-Guarded DPLL Reacquisition Controller

1. **章节槽位和方法名**：Ch4 carrier recovery；Fade-Guarded DPLL Reacquisition Controller（FG-DRC）。
2. **精确 M-C-A**：M=Paillier AGC+DPLL；C=Gamma-Gamma fade 造成低功率且 phase-detector innovation 爆发；A=固定环路继续积分噪声并可能 cycle slip，恢复后仍带错误 NCO 状态。
3. **baseline 全文**：`D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md:115-144,189,205`（AGC/DPLL 链、衰落失锁恶化与 BPSK/timing 边界）。
4. **input → action → output**：滑窗接收功率 CV、AGC gain、相位创新幅值 → `TRACK / HOLD / REACQUIRE` 三态命令 → 连续相位补偿流与 lock-state flag。
5. **算法流程**：
   1. AGC 后计算短窗功率/CV 和 wrapped phase innovation；
   2. 以 dev-frozen 双阈值判 `TRACK/HOLD`；
   3. `TRACK` 正常更新比例/积分状态；
   4. `HOLD` 冻结积分器，仅保留预测旋转；
   5. fade 退出且创新连续达标时短 pilot/DPLL 重捕获；
   6. 恢复 normal bandwidth 并输出 lock flag。
6. **baseline 不足原因**：论文固定 AGC 目标与固定二阶环路，不显式管理 fade 期间的 NCO 状态；这是从其数据流可推得的部署风险，不外推论文 5 dB 数字。
7. **fair comparator**：论文式 fixed AGC+DPLL；同样粗 FOE、同样 pilot/reacquisition budget。
8. **strongest cheap alternative**：普通 AGC + 固定 DPLL + threshold cycle-slip detector + unconditional pilot reinitialization。
9. **最小实现切片/工作量**：在现有 DPLL 加 3-state wrapper 和 flag，2–4 小时；不重建 AO。
10. **主结果图**：fade depth/duration × post-fade relock symbols，附 cycle-slip rate；不是 BER headline。
11. **消融**：去 power gate、去 innovation gate、HOLD 改 fixed update、去 pilot reacquire。
12. **claim ceiling**：最多 `THESIS_ENGINEERING_COMPONENT`；只称 receiver state-management。
13. **primary packaging**：衰落感知的闭环状态管理组件。
14. **fallback packaging**：DPLL fade failure/reacquisition 边界与实现建议。

**五字段碰撞收据**

- `existing_action_collision`：无 exact collision。CCISP/`branch_route_b` 只说明抽象 controller 结构相似；其受控对象是 DA/NDA 分支，K01 受控对象是 DPLL 内部状态，不能据此判同动作。
- `historical_dead_end`：P06/G1/P07-R 只提供相邻风险：历史信息和增益校准曾被常规动作吸收，但不构成 K01 exact dead end。
- `strongest_cheap_alternative`：fixed DPLL + standard cycle-slip detector + unconditional pilot reacquisition；尚无同工况实证证明它完全吸收 K01，因此本批不越过问题证据门进入 comparator 裁决。
- `reopen_condition`：先用现有 receiver-visible trace 证明 fixed AGC+DPLL 在主流 fade 下真实出现 post-fade 错误 NCO/重捕获延迟，并冻结同 pilot budget 的常规 slip-detector comparator。
- `authority_pointer`：baseline `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md:115-144,189,205`；inventory 的“仅为碰撞入口”警示 `internal-method-kernel-inventory.yaml:9-11`。

**裁决：REJECT — `PROBLEM_EVIDENCE_INSUFFICIENT`。** 论文证明 fixed AGC+DPLL 与 fade 下临界 SNR 恶化，未证明 K01 承重的 post-fade 错误 NCO 状态或 reacquisition 必要性；不能从 controller 形状补造问题。

### K02 — Ch4 / Confidence-Triggered STSB Relocalization

1. **章节槽位和方法名**：Ch4 synchronization/FOE；Confidence-Triggered STSB Relocalization（CT-SR）。
2. **精确 M-C-A**：M=Tang STSB 仅首训练周期定位；C=长 burst 的采样/帧边界漂移或训练峰衰落；A=固定周期算术沿用旧起点，后续 CFO 估计可能抽到错误训练窗。
3. **baseline 全文**：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_jphot.2022.3161795/content.md:43-85,115-161`（STSB 流程、首周期定位与混合收益）。
4. **input → action → output**：每周期 Park peak-to-sidelobe、peak position innovation、received power → `reuse expected index / local relocalize / full relocalize` → 更新训练起点和 CFO 补偿流。
5. **算法流程**：
   1. 从 manifest 推算下一训练窗；
   2. 在窄邻域计算 STSB metric 与 peak confidence；
   3. 高置信直接复用 expected index；
   4. 中置信在窄窗重定位；
   5. 低置信触发全窗定位并重置周期基准；
   6. 在确认训练块上估 CFO 并补 payload。
6. **baseline 不足原因**：论文固定训练周期并只做首次定位；若真实 receiver 存在边界漂移，该 shortcut 不再成立。
7. **fair comparator**：论文 first-only STSB；每周期 full STSB；传统 manifest arithmetic + local correlator。
8. **strongest cheap alternative**：每个周期直接在 expected index 附近做固定小窗相关；无需三态 controller。
9. **最小实现切片/工作量**：给现有 FSTS scaffold 加随机 frame drift、confidence 和三态定位，3–4 小时。
10. **主结果图**：drift rate × missed-training probability / correlation evaluations。
11. **消融**：无 confidence、仅 peak ratio、固定 local window、always full relocalize。
12. **claim ceiling**：`THESIS_ENGINEERING_COMPONENT`，且须先证明现实 drift 来源。
13. **primary packaging**：长 burst 的低开销同步维护器。
14. **fallback packaging**：STSB 对 frame-offset/drift 的适用边界。

**五字段碰撞收据**

- `existing_action_collision`：无 exact collision；threshold/controller 只是结构相似，不作否决依据。当前 caller 已知 block/pilot 位置属于独立的问题真实性证据。
- `historical_dead_end`：P02 已证明区域阈值/参考点重调可吸收表面自适应收益；P1 不得以 shared training/compute 改名恢复。
- `strongest_cheap_alternative`：manifest arithmetic + fixed local correlator；因当前 caller 没有 frame drift，本批在问题门停止，不声称已实证完全吸收。
- `reopen_condition`：现有 testbed 内出现有来源、非人为注入的 frame drift，且 fixed local correlator 在同预算下产生显著 miss ceiling。
- `authority_pointer`：`internal-method-kernel-inventory.yaml:32-62,64-78`；longitudinal D040 `:2514-2543`；P1 closed system D025-D026 `decisions.md:838-915`。

**裁决：REJECT — `PROBLEM_ABSENT_IN_CURRENT_CALLER`。** fixed local correlator 只保留为若未来出现真实 drift 时的 mandatory comparator。

### K03 — Ch4 / Receiver-Calibrated Hybrid Coarse FOE

1. **章节槽位和方法名**：Ch4 coarse carrier acquisition；Receiver-Calibrated Hybrid Coarse FOE（RC-HCFOE）。
2. **精确 M-C-A**：M=Fan short-time spectrum FOE；C=front-end response/AGC 改变正负谱面积与 `alpha` 映射，且 current residual CFO 已很窄；A=固定硬件标定可能偏置，仍需多次 LO 迭代。
3. **baseline 全文**：`D:/code/study/research-protocol/papers/doi/10.1016_j.optcom.2024.130981/content.md:71-95,115-149,167`。
4. **input → action → output**：星历 residual prior、正负谱面积比、receiver-known calibration tone/pilot spectrum → 预测置信区间并选择 `FFT fine / short-spectrum coarse→FFT fine` → 残频估计和 LO command。
5. **算法流程**：
   1. 星历预补并生成 residual interval；
   2. receiver calibration block 估计谱不对称零点/斜率；
   3. 若 interval 落传统 FFT 捕获范围，直接 FFT fine；
   4. 否则校准短时谱映射并作一次 coarse command；
   5. 用相同 FFT fine 估 residual；
   6. 超置信界则报告 reacquisition，不继续盲迭代。
6. **baseline 不足原因**：固定 `alpha` 绑定论文 front-end；当前窄 residual 工况中 coarse branch 可能解决不存在的问题。
7. **fair comparator**：同星历先验下 traditional FFT FOE；原 Fan iterative short-spectrum FOE。
8. **strongest cheap alternative**：星历预补 + traditional FFT FOE。
9. **最小实现切片/工作量**：已有两 baseline，只加校准 fit 与 route wrapper，2–3 小时。
10. **主结果图**：initial residual range × residual RMSE / LO iterations；必须同 ephemeris information。
11. **消融**：固定 `alpha`、无 route、无 confidence stop、不同 front-end slope。
12. **claim ceiling**：若存活也仅 acquisition engineering component。
13. **primary packaging**：校准感知的大范围/窄范围 FOE 路由。
14. **fallback packaging**：星历公平性与 short-spectrum calibration sensitivity。

**五字段碰撞收据**

- `existing_action_collision`：是；receiver statistic/prior → branch select 已被 CCISP/route-B 占有，`alpha`/工作区校准落入 P01/P02/D040。
- `historical_dead_end`：B5 同轴公平对照已得 FFT+星历 19/19 = Fan 19/19，且 FFT residual 约 0.976 MHz、Fan 约 10.27 MHz；范围优势完全归星历。
- `strongest_cheap_alternative`：同信息的星历预补 + FFT FOE，已实证完全吸收。
- `reopen_condition`：出现星历+FFT 无法覆盖、而 receiver-visible short-spectrum branch 在同信息/同硬件标定预算下有解析上界优势的新任务区间。
- `authority_pointer`：B5 `decisions.md:134-167,233`；inventory `:14-30,32-78`。

**裁决：REJECT — exact historical dead end；不得恢复 B5。**

### K04 — Ch5 / Overflow-Aware Block-Floating VV4E

1. **章节槽位和方法名**：Ch5 receiver implementation；Overflow-Aware Block-Floating VV4E（OA-BF-VV）。
2. **精确 M-C-A**：M=Lin fixed-point VV4E；C=FSO received-power variation/AGC transient 改变内部 dynamic range；A=全程固定 Q-format 可能在 fade 后放大时 overflow，或在平稳段浪费 fractional precision。
3. **baseline 全文**：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_iscas48785.2022.9937906/content.md:79-180,188-219`。
4. **input → action → output**：block max magnitude、overflow counter、phase-innovation variance → 选择共享 exponent 与预冻结 `{Q6.4,Q7.5,Q8.6,Q9.7}` profile → bit-true phase-corrected samples + overflow flag。
5. **算法流程**：
   1. 在 43-symbol block 统计 headroom；
   2. 选择 block exponent，统一缩放 fourth-power/adder inputs；
   3. 依据 phase variance 从冻结 profile 选 fractional bits；
   4. 执行定点 tree/CORDIC/unwrap/LUT；
   5. overflow 时饱和并升级下一 block profile；
   6. 输出补偿样本与 profile trace。
6. **baseline 不足原因**：论文固定 5/7 fractional bits，不覆盖 FSO block-to-block dynamic range。
7. **fair comparator**：float VV；论文 uniform Q-format ladder；统一高精度 Q(8,6)。
8. **strongest cheap alternative**：ordinary AGC + uniform Q(8,6)。
9. **最小实现切片/工作量**：软件 bit-true profile/exponent wrapper，3–4 小时；不声称 FPGA PPA。
10. **主结果图**：power dynamic range × BER/phase RMSE/overflow，附平均 bit-operations proxy。
11. **消融**：仅 block exponent、仅 precision switch、无 overflow feedback、uniform Q(8,6)。
12. **claim ceiling**：`THESIS_ENGINEERING_COMPONENT` 上限。
13. **primary packaging**：FSO dynamic-range aware CPR arithmetic。
14. **fallback packaging**：uniform precision robustness verification。

**五字段碰撞收据**

- `existing_action_collision`：是；P03 exact action 已比较 uniform/mixed precision 与 resource proxy；P07-R/G1 又证明 gain 问题由普通 AGC 吸收。
- `historical_dead_end`：P03 `0/132000` bypass mismatch，Q(8,6) regret `+0.027 dB`，mixed 相对 uniform 仅 `+0.0166 dB`，terminal=`PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`。
- `strongest_cheap_alternative`：ordinary AGC + uniform Q(8,6)，已覆盖 block-floating 的必要性。
- `reopen_condition`：真实硬件 synthesis/PPA 或有来源 dynamic-range 工况证明 uniform Q(8,6) 不能满足 overflow/BER/资源联合门，且 mixed/block-floating 超过 MDE。
- `authority_pointer`：`internal-method-kernel-inventory.yaml:80-94,154-171,206-213`；longitudinal D058 `:3603-3619`。

**裁决：REJECT — exact P03 collision，uniform precision 已解决。**

### K05 — Ch5 / Fade-Separated Blind Radius Calibration

1. **章节槽位和方法名**：Ch5 blind equalization/calibration；Fade-Separated Blind Radius Calibration（FS-BRC）。
2. **精确 M-C-A**：M=Cao density-peak/K-means radius calibration；C=Gamma-Gamma common gain 与星座 ring statistics 同时变化；A=直接聚类绝对幅度会把 channel gain 当成 constellation-radius drift，污染 CMMA/RDE references。
3. **baseline 全文**：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.3788_col202220.080601/content.md:42-72,87-140,163-169`。
4. **input → action → output**：receiver amplitudes、block median/quantiles、density peaks → 联合估计 common gain 与归一化 ring-ratio references → gain-normalized samples、CMMA/RDE radii 和 confidence flag。
5. **算法流程**：
   1. 以 robust median/quantile 估 block common scale；
   2. 除 scale 得相对幅度；
   3. 对内环计算 density peak 与 `K`；
   4. K-means 精化相对 ring radii；
   5. 以 confidence gate 决定更新或保持旧 references；
   6. 将 scale 交 AGC、ring ratios 交 CMMA/RDE；
   7. 输出均衡符号与校准 trace。
6. **baseline 不足原因**：原论文在 PS-256QAM 光纤链上估绝对半径，没有分离 FSO common fade 与星座结构。
7. **fair comparator**：原 density-peak/K-means；fixed-radius CMMA/RDE；ordinary block AGC + fixed references。
8. **strongest cheap alternative**：ordinary AGC/normalization + dev-frozen CMMA/RDE radii。
9. **最小实现切片/工作量**：复用现有 CMMA，增加 robust scale + density/K-means；3–4 小时，仅作 PS-16QAM 身份适配。
10. **主结果图**：scintillation × equalizer convergence/BER，附 radius error；与 AGC comparator 同信息。
11. **消融**：无 scale separation、无 confidence hold、fixed K、ordinary AGC + fixed radii。
12. **claim ceiling**：理论上 `THESIS_ENGINEERING_COMPONENT`；不得称新 blind equalizer 原理。
13. **primary packaging**：fade/calibration 分离的 blind radius adapter。
14. **fallback packaging**：FSO gain 对盲半径校准的失效边界。

**五字段碰撞收据**

- `existing_action_collision`：是；blind AGC/radius calibration 已在 Q15/G1 历史关闭；P07-R/G1 的共同 gain artifact 被 ordinary AGC 消除；confidence hold 又落入 threshold/controller 族。
- `historical_dead_end`：P07-R fixed-gain regret 仅 0.03–0.07 dB，问题在 gain calibration 后消失；G1 是 scale-sensitive slicer artifact；Q15 nonlinear map 无 gate+scale 外增量。
- `strongest_cheap_alternative`：ordinary block AGC + fixed/dev-retuned radii，完整吸收 common-gain 分离动作。
- `reopen_condition`：合法 PS-FSO baseline/testbed 在 ordinary AGC 后仍显示 ring-ratio 非平稳、且超过固定/retuned radii 的可检出上界；不能只靠人工 PS-16QAM 适配制造。
- `authority_pointer`：inventory `:48-62,154-171`；longitudinal D040 `:2514-2543`；formal Q15/D040 历史见 `topic-index.md` current snapshot。

**裁决：REJECT — ordinary AGC/retune absorbs；Q15/G1/P07-R collision。**

## 3. Phase D — 十项方法生产门

| 卡 | 2019+ baseline | M-C-A 表面过 | action 不碰撞 | receiver-visible | 非 oracle/TX truth | cheap alt 未吸收 | adapter ≤半天 | 完整步骤/图/消融 | fallback | ≥T2 | 终态 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| K01 FG-DRC | PASS | **FAIL**（承重 failure 未证） | PASS | PASS | PASS | NOT_REACHED | PASS | PASS | PASS | PASS | REJECT |
| K02 CT-SR | PASS | **FAIL**（当前 caller 问题不存在） | PASS | PASS | PASS | NOT_REACHED | PASS | PASS | PASS | PASS | REJECT |
| K03 RC-HCFOE | PASS | **FAIL**（同信息 FFT 已解决） | **FAIL** | PASS | PASS | **FAIL** | PASS | PASS | PASS | PASS | REJECT |
| K04 OA-BF-VV | PASS | PASS | **FAIL** | PASS | PASS | **FAIL** | PASS | PASS | PASS | PASS | REJECT |
| K05 FS-BRC | PASS | PASS | **FAIL** | PASS | PASS | **FAIL** | PASS | PASS | PASS | PASS | REJECT |

说明：K01/K02 在问题真实性/证据层停止，不能因抽象 controller 结构相似判 exact collision，也不进入 cheap-alternative 实证裁决；K03/K04/K05 再分别受历史同轴证据或 conventional alternative 约束。没有卡同时通过十门，因此不得以“最接近”凑 survivor。

## 4. 历史对象总碰撞审查

- **P01–P11/G1**：K01/K02 只与 controller/threshold 结构相似，不判 exact collision，并已在问题门停止；K03/K04/K05 分别命中粗 FOE 公平性、fixed point、AGC/radius/gain-artifact 等已审轴。D058 明确历史负面/边界不得升级。
- **AMC**：没有卡改变系统层级；不得把 Hu 的 TX loading 或 detector routing塞入 dormant AMC。AMC 仅在显式 scope change + 新 GW 专题后可恢复。
- **P1**：共享升幂计算图已 `RECENT_BASELINE_UNAVAILABLE / SUPPORTING_ONLY / closed`；训练序列或共享计算的卡不得改名恢复。
- **C3**：adaptive segmented CPE 已 `PHYSICAL_PREMISE_UNSUPPORTED / closed`；本批不选择 K/窗口，不使用极端线宽，不恢复 C3。
- **Ch4 旧卡**：顶部 supersession banner 的 `NO_CONSTRUCT_SURVIVES` 优先于旧 survivor prose；本批没有复用 C3 action signature。
- **Ch5 旧卡**：D024 对 P1 的临时设计 survivor 已被后续 P1 closed authority 限制为 supporting-only；K04 不以 mixed precision 恢复 P03/P1。

总 authority：`projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml:5-11,14-171,206-213`；`ch4-concept-method-batch-001.md:1-19`；system `decisions.md:838-915`；P1 `H003-bounded-closure-stop-p1.md`；C3 `topic-index.md`。

## 5. 唯一终局与下一合法动作

### `STRATEGIC_SHORTAGE_CONFIRMED`

- baseline 池充分：7 篇均为 2019+ 正式发表、本地有效全文、方法身份可确认，并有不超过半天的算法级复现/适配入口；没有触发补充 broad search。
- 方法生产完成：5 张机制不同的卡均先形成完整动作链，再分别在问题证据、权威碰撞或 strongest cheap alternative 门停止；survivor=0。
- 贡献层级：本批没有新的 `THESIS_ENGINEERING_COMPONENT`，更没有 `THESIS_MAIN_METHOD`。可保留的只是 baseline 库与边界材料，不能冒充方法贡献。
- 下一合法动作只能由用户显式选择一种战略改变：
  1. **改变 candidate source**：引入新的、可读全文且带现成 receiver testbed 的 baseline 族；
  2. **改变 target chapter**：从 Ch4/Ch5 receiver DSP 转向已有证据更厚的实现验证/系统工程章节；
  3. **改变 research object**：引入新的物理自由度或系统层级，并重新从正式 GW Step 1 开始。

本轮不推荐任何卡进入 GW，不新建 Groundwork 专题，不提供“第六个弱候选”。
