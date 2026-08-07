# Q1 GW Step 4a preflight discussion

> 2026-08-07 | 仅完成 A0 → A′ → A/B 分析与维度 D 的最小实验设计
> 当前终态：`STEP4A_PREFLIGHT_EVIDENCE_GAP`
> 未运行 MVE、semantic smoke 或仿真；未建立 testbed；未实现任何方法。

## 0. 权威入口与证据边界

- Q1 已在 `literature_notes_oversampled_sync.md:126-131` 通过 canonical 四判据，合法进入 A0 §0；
  “A 尚未被 MVE 证明”不是 A0 前门。
- 当前全文只证明 Q1 可证伪、baseline 合法且有量化输出；没有 B0/B1/B2 对 joint oracle 的差距数字，
  也没有稳定错误峰/误锁区数据（同文件 `:107-112`）。
- JOCN 2026 全文不可得只限制 exact-action novelty/“首次”措辞，不是 negative collision 或可行性证据
  （`step3-5-supplement-report.md:28-35,51-53`）。
- Q2 非 survivor，本报告不讨论。

## 1. A0 §0 与方法身份

### 1.1 Q1 canonical M-C-A

- **M**：Le Bidan 2-sps 顺序 acquisition chain，加 Sun/Wang/JLT shared-preamble frame–FOE 链。
- **C**：RRC、≥2 sps coherent FSO burst，fractional timing、frame offset、CFO 同时未知。
- **A**：顺序估计在同时未知参数下可能传播残余误差、选择错误相关峰或误锁。

证据要求一处修正：Le Bidan 强链不是“完全没有 coarse CFO 的 timing-first”。其顺序为
`coarse CFO → matched filter → Lee timing/interpolation → FSE/downsample → frame/fine CFO/CPE`
（`literature_notes_oversampled_sync.md:102-103`）。因此后续不得用无 coarse-CFO 的弱链作 B0；A 的可证伪对象是
**coarse CFO 后的残余频偏、分数定时与帧峰之间的顺序硬判决传播**。

### 1.2 接收离散信号模型

令过采样率为 \(L\ge2\)，采样间隔 \(T_s=T/L\)，已知前导符号为 \(a_m\)，接收等效脉冲为
\(q(t)\)。令整数帧起点为 \(d\)，分数采样偏移 \(\tau\in[-1/2,1/2)\)，CFO 为 \(\nu\)，
未知复增益为 \(\alpha\in\mathbb{C}\)，相位噪声为 \(\theta[n]\)，则前导窗口内

\[
r[n]=\alpha e^{j(2\pi\nu nT_s+\theta[n])}
\sum_{m=0}^{N_p-1} a_m q\!\left((n-d-\tau)T_s-mT\right)+w[n].
\]

- \(d\) 以整数样本平移 burst/preamble 支撑区；
- \(\tau\) 通过 RRC/Farrow 插值改变每个过采样点的幅相；
- \(\nu\) 产生跨样本线性相位；复 \(\alpha\) 同时吸收未知幅度与常相位，是 nuisance；
- \(\theta[n]\) 产生随机相位轨迹，\(w[n]\) 是加性噪声。

在 semantic smoke 中先设 \(\theta[n]=0\)，剥离 maintenance/phase-noise 问题。对 \(\alpha\) profile
后，可使用 receiver-visible 的归一化 GLRT/ambiguity score

\[
\Lambda(d,\tau,\nu)=
\frac{\left|x_{d,\tau}^{H}D(\nu)^{H}r\right|^2}
{\|x_{d,\tau}\|^2\,\|r_d\|^2},
\qquad
D(\nu)=\operatorname{diag}\{e^{j2\pi\nu nT_s}\}.
\]

一般情况下 \(\tau\) 同时改变脉冲采样，\(\nu\) 又在同一索引上产生相位斜率，且 \(d\) 改变截窗，
所以 \(\Lambda\) 不能写成三个独立一维函数的乘积。只有在 coarse CFO 已足够准确、前导相关性近理想、
窗口/guard 消除边界效应，或局部 Fisher/Hessian 的交叉项很小时，才可能近似可分。

### 1.3 四种方法身份

| 方法 | receiver-visible input | objective | action/output | 搜索维度 | 复杂度与身份 |
|---|---|---|---|---|---|
| **B0 强顺序链** | 同一段 ≥2-sps preamble samples、已知前导、合法搜索界 | coarse CFO、timing error、frame correlation、fine FOE 等阶段性局部 metric | \((\hat d,\hat\tau,\hat\nu)\) | 按顺序执行多个 1-D 搜索/环路 | 最低复杂度、模块成熟；是合法系统锚点，不是稻草人。硬判决后续不可回看被丢弃峰。 |
| **B1 timing bank** | 与 B0 完全相同 | 每个 polyphase/Farrow \(\tau_k\) 下运行 B0 的 frame/FOE，再以统一 normalized terminal score 选分支 | 同上 | \(K_\tau\) 个 timing hypotheses，每支内部执行 B0 | 约 \(K_\tau C_{B0}\)，可共享滤波/FFT。它是 hypothesis-bank/资源复制，不自动构成新方法。若 terminal score 与 \(\Lambda\) 相同并全局取最大，B1 在同一网格上与 C-oracle 数学等价。 |
| **B2 alternating refinement** | 与 B0 相同，加 B0/B1 初始化 | 在同一 \(\Lambda\) 或明确 surrogate 上轮流更新 \(\tau\) 与 \((d,\nu)\) | 同上及收敛标志 | 1-D/2-D 条件搜索交替 \(I\) 轮 | 约 \(I(C_\tau+C_{d,\nu})\)，便宜但可能落入局部峰。若没有共同 objective，只是重复调序；有共同 objective 才是 coordinate refinement。 |
| **C coupled estimator / C-oracle** | 与 B0 相同；不得读取 truth | 单一 profiled \(\Lambda(d,\tau,\nu)\)，保留跨参数候选与交叉项 | 全局 \((\hat d,\hat\tau,\hat\nu)\)、top-2 margin、局部曲率 | 3-D coarse grid 后 coupled refinement；oracle 指全局优化，不是 genie truth | naive 为 \(O(K_dK_\tau K_\nu N_p)\)，可用 FFT/polyphase/coarse-to-fine 降低。只有“统一 likelihood + 无中间硬判决 + 利用非零交叉项/全局 margin”才是相对 B0 的结构增量。 |

**C 相对 B1/B2 的不可替代增量尚未成立。** 若 B1 对相同 \(\Lambda\) 穷举所有 timing hypotheses，或
B2 在目标网格稳定到达同一全局最大值，则 C 没有 wrong-basin false-lock 增量；它最多转为计算图/复杂度实现问题。
这正是本轮最致命的 `EVIDENCE_GAP`。

## 2. A0 §1–§6 的致命点

### §1 性能间隙

当前没有 B0/B1/B2 相对 C-oracle 的实证、外推或论证数字，不能填写 ≥15%、5–15% 或 <5%。
结论为 `EVIDENCE_GAP`，不是“有空间”。唯一合法表述是：B0 的 simultaneous-unknown failure 尚待 Step 4a
验证（`literature_notes_oversampled_sync.md:107-112`）。

### §2 结构适配与可分性

- 对“是否需要 ML”：**不需要预设 ML**。Q1 是有限维参数估计，解析 GLRT、ambiguity function、
  polyphase/Farrow、FFT 与坐标迭代是自然方法族；MDP/S-A-R-P 不适用。
- 对“是否需要 coupled estimator”：一般 likelihood 非可分，但在目标 preamble 与 coarse preprocessing 下是否
  **数值上近似正交**尚未确认。
- LPT 2017 的 joint integer-frame/CFO 与 Du 2021 的 joint timing/CFO/CPO 提供两个确定性 joint 先例，
  只支持方法形态可行，不支持 Q1 的 headroom（`step3-5-supplement-report.md:30-32,47-49`）。

**框架 A0 第 5 项负面证据核查**：现有 Step 3/3.5 材料没有记录以
`joint/coupled frame timing CFO + limitation/challenge/failure/unsuccessful/no gain` 为目标的专门负面检索。
Step 3.5 的两轮 query 与引用链用于 exact-action collision/coverage，不等价于失败/无收益搜索。因此本项为
`EVIDENCE_GAP`；不能声称“没有失败报告”，也不能据当前两个成功先例判 A0 全通过。若后续 smoke 被批准，
执行前只允许先复用本地 search archive/read notes 做一次有界核查；需要新 Web 检索则另行授权并由子 agent 执行。

### §3 可辨识性与退化条件

1. **frame–fractional decomposition**：若不限制 \(\tau\) 的基本区间，\((d,\tau)\) 与
   \((d+1,\tau-1)\) 等价；必须冻结 \(\tau\in[-1/2,1/2)\)。
2. **CFO alias**：\(\nu\) 只在 modulo \(F_s\) 意义可辨，必须用 coarse-CFO 物理先验限制搜索区间。
3. **preamble 周期/重复结构**：周期相关、重复块或 CAZAC cyclic shift 可生成等高或近等高 frame/CFO 峰；
   guard、搜索窗与 top-2 margin 必须显式。
4. **短前导/小 roll-off**：timing derivative 能量不足时，\(\tau\) 信息弱；未知复增益/常相位还会吸收部分方向。
5. **近似正交退化**：coarse CFO 很准、长随机前导且边界效应小，\(\tau\)–\(\nu\) 交叉项可能趋小，
   这会直接支持“顺序链近似最优”零假设。

分析方案：固定整数 \(d\) 后，对复 nuisance \(\alpha\) profile；其 tangent space 由模板方向
\(x\) 与 \(jx\) 张成，\(P_\perp\) 投影到该 nuisance tangent space 的正交补。随后计算
\(J_{ij}=\frac{2}{\sigma^2}\Re\{(\partial_i\mu)^HP_\perp(\partial_j\mu)\}\) 及
\(\rho_{\tau\nu}=|J_{\tau\nu}|/\sqrt{J_{\tau\tau}J_{\nu\nu}}\)；同时用离散 ambiguity surface 的
top-1/top-2 margin 与错误峰连通区处理 CRLB 无法描述的全局 false lock。CRLB 只在正确 frame basin 内有效，
不能替代错误峰审计。

### §4 廉价先验覆盖

- **polyphase/Farrow grid**：最危险的覆盖者；若使用同一全局 score，可在离散网格上完全吸收 C。
- **coordinate descent**：可用少量迭代吸收大部分 coupled-refinement 收益，但可能受错误峰初始化影响。
- **coarse CFO first**：已有强链已经采用，可能把 \(\tau\)–\(\nu\) 交叉项压到可忽略。
- **normalized correlation**：消除未知幅度/局部能量差，可能直接修复错误峰而无需新 estimator。

进入正式 MVE 前的硬退出：B1 或 B2 覆盖 C 相对 B0 的主指标改善 ≥95%，或 B1 与 C 同网格同 score
数值等价，则 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`。

### §5 单一方法产出维度

本候选只选择 **wrong-basin false-lock rate** 为主要贡献维度。`acquisition success` 是其严格互补报告口径；ambiguity
surface、估计误差、SNR、latency/complexity 与 preamble overhead 都只作诊断/约束，不并列包装成贡献。
本 smoke 的所有 cell 都含前导且四法必须输出估计，因此 `miss` 明确为 N/A，不在主指标中混算。

若最终只形成工程组件，只有在以下条件同时满足时才足以支撑一章中的独立方法节：存在真实可部署动作
（例如 coupled coarse-to-fine pruning 或共享 score 计算图）、相对 B1/B2 有公平对照、实际 caller 路径的
false-lock 或计算量有稳定差异，并能给出算法步骤、消融、主图与作用边界。共享 preamble、模块调序、
资源复用或换名本身不够。

### §6 跨域先例与空白零假设

| 零假设 | 当前判断 | 为什么尚未反驳 |
|---|---|---|
| H0-1 顺序链已经近似最优 | **高风险、未反驳** | 真实系统普遍采用 coarse CFO/clock preprocessing；当前没有 B0 误锁数据。 |
| H0-2 联合搜索复杂度高而收益小 | **高风险、未反驳** | naive 3-D search 显著贵；没有 headroom 或 cost/benefit 数字。 |
| H0-3 选定 preamble 下参数天然近似正交 | **高风险、未反驳** | 一般 likelihood 非可分不等于目标工作点数值耦合强；FIM/Hessian 尚未计算。 |
| H0-4 真实系统已由 coarse CFO/clock preprocessing 解耦 | **部分被现有链支持** | Le Bidan 已 coarse-CFO-first，Tang/Wang 多在 clock/downsample 后做 frame/FOE；必须在 evidence-faithful B0 上验证 residual coupling。 |

“当前全文池未发现 exact action”只属于 novelty 边界，不反驳任何零假设。

## 3. A′ / A / B 竞争维度矩阵

| 维度 | B0/B1/B2 的强项 | C 的可用空间 | 当前证据 |
|---|---|---|---|
| **wrong-basin false-lock rate（唯一主维度）** | B1 全 timing bank、B2 反馈修正可能很强 | 仅当顺序硬判决跨 basin 丢信息、且 B1/B2 不能 ≥95% 吸收时存在 | **EVIDENCE_GAP；尚无 ≥5% 空间** |
| acquisition reliability | 与主维度互补，不单独立贡献 | 仅作 success-rate 报告 | 无数字 |
| SNR penalty / local RMSE | coarse CFO + timing bank + normalized correlation 可能已近 CRLB | 非零 Hessian 交叉项可能提供局部收益 | 无 FIM/CRLB/实证 |
| latency / complexity | B0 最强；B2 通常次之；B1 可并行 | C naive 最弱，只有 coarse-to-fine/pruning 才可能成为工程组件 | 只有复杂度式，无实测 |
| preamble overhead | Sun/Zhou/JLT 已用 shared/partitioned preamble 强覆盖 | 不作为本候选贡献 | JOCN 缺口进一步压低泛化措辞 ceiling |

**维度 A**：C 的结构优势只能来自“统一 likelihood 保留跨参数峰与交叉项，避免中间硬判决丢失”。
但 B1/B2 是增强传统 baseline；若它们复现同一 surface/argmax，结构优势消失。

**维度 B**：可说“当前可得全文池未确认同信息、同动作、同任务的 exact estimator”；不可说“首次”、
“无人做过 joint timing/CFO”或“JOCN 不碰撞”。JOCN 摘要已占 single-preamble multi-action 语义，
故后续措辞上限只能是目标 waveform、信息、输出与工况下的 bounded coupled acquisition rule。

## 4. 维度 D：≤1 天 deterministic semantic smoke 合同（只设计）

### 4.1 Probe 问题与边界

- **问题**：目标 preamble/预处理下，是否存在稳定的非可分错误峰区，使 visible-only C-oracle 在
  wrong-basin false-lock rate 上有 ≥5% 相对改善，且 B1/B2 不能吸收其 ≥95%？
- **假设**：coarse CFO 残差、fractional timing 与 frame peak 的交叉项会使 B0/B1/B2 在一片相邻工况
  选择错误 basin，而统一 3-D GLRT 能避免。
- **否决条件**：objective 可分/近似可分；B1 与 C 同网格等价；B1/B2 覆盖 ≥95%；不存在稳定错误峰区；
  或 C 相对 B0 的 wrong-basin false-lock rate 相对改善 <5%。
- **预算**：单个只读设计合同；获用户后续授权才可由子 agent 在 ≤1 天执行。不得 productionize、建 testbed、
  改 `common/`/`params.py` 或用结果作论文数字。

### 4.2 最小 waveform 与 paired realization

1. 一个冻结的 receiver-known 64-symbol QPSK preamble，RRC roll-off 0.1，2 sps，TX RRC + RX matched filter；
   不含 payload/FEC、SCO/drift、Gamma-Gamma、Wiener PN、maintenance loop、完整 BER/EVM。
2. preamble 精确符号优先从 Sun/Wang/Zhou 已读全文固定；若使用 fixed-seed diagnostic QPSK，结果只能是
   semantic，不得外推到文献 preamble。
3. 每个 cell 只生成一次 `rx_samples`，B0/B1/B2/C 消费完全相同的 sample array、窗口、前导、搜索界与噪声；
   不允许“同 seed 但各分支重新生成”。
4. `C-oracle` 仅表示 visible likelihood 的全局 dense-grid optimum；不得读取 \((d^*,\tau^*,\nu^*)\)。

### 4.3 identity、grid 与输出

- **无噪声 identity**：\((d,\tau,\nu)=(0,0,0)\) 时四法必须回传 identity；zero impairment 的生成/匹配
  误差低于数值容差；任一失败立即 `SEMANTIC_INVALID`，不解释科学结果。
- **真值 grid（小规模）**：\(d\in\{-8,0,+8\}\) samples；
  \(\tau\in\{-0.4,-0.2,0,0.2,0.4\}\) sample；CFO 分两层：文献 residual
  \(\{0,\pm50,\pm100\}\) MHz 与 design-range stress \(\{\pm5\}\) GHz。后者只测试 coarse stage，
  不与 residual 结果混合。
- **噪声**：先执行 noiseless surface；若 identity 通过，再以冻结 deterministic AWGN seed 做少量诊断 SNR。
  SNR 点必须在执行前补来源或明确标 `diagnostic sentinel`，不得据此作物理 headroom claim。
- **surface**：保存/绘制四法可比较的 \(\Lambda(d,\tau,\nu)\)、top-1/top-2 margin、错误峰连通区；
  同时输出 \(\rho_{\tau\nu}\) 或局部 Hessian 交叉项。
- **primary metric**：wrong-basin false-lock rate。grid-only 等价切片要求输出的 \((d,\tau,\nu)\) 三个
  hypothesis index 与真值 cell 完全一致；允许 coupled refinement 的切片要求 \(\hat d=d^*\)、
  \(|\hat\tau-\tau^*|\le\Delta_\tau/2\)、\(|\hat\nu-\nu^*|\le\Delta_\nu/2\)。任一条件失败即 false lock。
  分母为全部 preamble-present paired cells，`acquisition_success=1-R_FL`；`miss=N/A`，不设 detection threshold。
- **改善与覆盖**：\(G_C=(R_{FL,B0}-R_{FL,C})/\max(R_{FL,B0},\epsilon)\)；若 \(R_{FL,B0}=0\)，
  直接判无可用 headroom。对 \(k\in\{B1,B2\}\)，
  \(coverage_k=(R_{FL,B0}-R_{FL,k})/(R_{FL,B0}-R_{FL,C})\)，只在分母为正时计算。
- **真实计算量**：记录实际 complex MAC、FFT 次数、Farrow/interpolation 次数、候选 score 次数、wall time；
  同进程 warm-up 后重复 5 次取 median，不用大 O 代替 caller-path 计算量。

### 4.4 information contract

```yaml
receiver_visible:
  - rx_samples
  - known_preamble
  - sps_and_rrc_definition
  - frozen_search_bounds
  - method_hyperparameters_frozen_before_scoring
  - common_hypothesis_grid_for_equivalence_slice
  - common_profiled_glrt_score_definition
  - common_fixed_observation_window_and_normalization
  - deterministic_tie_break_rule
  - refinement_stop_rule
truth_scoring_only:
  - true_frame_index
  - true_fractional_tau
  - true_cfo
  - injected_phase_and_noise
  - tx_waveform_before_impairments
forbidden_in_method:
  - payload_truth
  - true_alignment_or_lag
  - oracle_rotation
  - truth_selected_grid_or_branch
```

必须做 hidden-truth metamorphic check：固定 `receiver_visible`，只改变 truth metadata，四法输出须 byte-identical。

**B1/C 等价判据**：只在 equivalence slice 使用完全相同的 \((d,\tau,\nu)\) 候选集合、复 \(\alpha\)
profiling、\(\Lambda\) 定义、固定扩展 observation window、模板 zero-padding、normalization 与 tie-break；
B1 必须对所有三元候选取全局 argmax。score 在预注册数值容差内一致且 argmax/tie-break 一致，才可称
grid-equivalent。C 的连续 refinement 另作扩展切片，不能反向用于宣称 B1 grid 不等价。tie-break 冻结为
“score 差在容差内时按 \((d,\tau,\nu)\) 字典序取最小”；所有方法使用同一规则。

### 4.5 参数来源清单

| 参数 | 预定值/范围 | 来源与等级 |
|---|---|---|
| 调制、RRC、sps | QPSK、roll-off 0.1、2 sps | Le Bidan GEO 2023 设计/数值设置，`literature_notes_oversampled_sync.md:43` |
| preamble length | 64 symbols | Le Bidan frame 设计，`literature_notes_oversampled_sync.md:45`；精确序列仍需从已读全文冻结 |
| total/design CFO | ±5 GHz | Le Bidan 设计要求，`:44`；非真实分布 |
| residual CFO | 100 MHz anchor；smoke 用 0/±50/±100 MHz | Paillier 2020 假设的固定预补偿残差，`:50`；非外场测量 |
| fractional \(\tau\) | 基本区间内 sentinel grid | 分布尚未冻结，`:54-55`；只用于 semantic identity/coupling，不支持发生概率 |
| frame offset | -8/0/+8 sample sentinel | 分布尚未冻结，`:54-55`；只用于索引/峰语义 |
| SNR | 执行前补来源或标 diagnostic sentinel | 当前 `EVIDENCE_GAP`，不得拍物理阈值 |

### 4.6 预注册 terminal

1. 任一 identity、paired-realization、truth-isolation 或 score-comparability gate 失败：
   `SEMANTIC_INVALID`，修复合同；不作科学终态。
2. objective 可分/近似可分，B1/B2 覆盖 C 改善 ≥95%，无稳定错误峰区，或 C 的主指标上界 <5%：
   `STEP4A_PREFLIGHT_KILL_OR_PIVOT`，不建 testbed。
3. 解析与 surface 同时显示非可分耦合，存在至少 2×2 相邻 \((\tau,\nu)\) cells 的稳定错误峰区，
   C 对 B0 的 wrong-basin false-lock rate 相对改善 ≥5%，且 B1/B2 均覆盖 <95%：
   `STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE`，交用户批准后再设计/运行正式 MVE。
4. 参数、surface 或等价性不足以裁 2/3：`STEP4A_PREFLIGHT_EVIDENCE_GAP`。

## 5. 本轮终态与下一合法动作

**终态：`STEP4A_PREFLIGHT_EVIDENCE_GAP`。**

理由不是“A 尚未被 MVE 证明”，而是两个更窄、可执行的缺口：

1. 没有 B0/B1/B2 对 C-oracle 的性能间隙与稳定误锁区证据；
2. B1 在相同 grid/score 下可能与 C 数学等价，C 相对增强传统 baseline 的不可替代结构增量尚未成立。

下一合法动作仅为：用户审阅并决定是否授权执行上述 ≤1 天 deterministic semantic smoke。未获授权前，
不得派执行 T、不得运行脚本、不得建立 5.5–7.5 日 acquisition testbed，也不得写 Go/Conditional Go。
