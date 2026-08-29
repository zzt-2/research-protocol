# Q-C4-1 scaled-unitary pilot-LS — GW Step 4a 纸面可行性（A0/A′/A/B）

> 任务：T068｜日期：2026-08-30｜formal step：GW Step 4a paper dimensions only
> task-control：`PASS`（`rdl.task-control.v2` / epoch 10 / CP010 / `GW_STEP4A_PAPER_FEASIBILITY`）
> 总裁决：`PAPER_DIMENSIONS_PASS_WITH_BOUNDARY`
> headroom 参数状态：`PARAMETER_AUTHORITY_BLOCKED`
> 边界：未进入维度 D，未实现、未仿真、未给 Go/Conditional Go，未形成最终方法或论文正文。

## 0. Findings-first 结论

| 维度 | verdict | 纸面结论 | 尚未闭合的实证问题 |
|---|---|---|---|
| A0 | `PASS_WITH_BOUNDARY` | `M-C-A` 成立。strict `H=gQ`、短 balanced pilots 下，unconstrained 2×2 complex LS 估计 8 个实自由度，而 scaled-unitary 流形只有 5 个实自由度；多出的 3 个法向噪声自由度形成合理的方差问题 | 一阶方差下降是否传导为 payload BER 改善；当前没有 BER 数字 |
| A′ | `PASS` | 主竞争维度冻结为**相同 pilot 开销下 payload BER**；channel NMSE 与 inverse residual 只解释机制，不能单独承重 | BER 差异、统计灵敏度和工作区尚未实测 |
| A | `PASS_WITH_BOUNDARY` | 结构假设与当前 frozen memoryless unitary single-tap slice 匹配；`rho=s1/s2` 先只作 receiver-visible applicability diagnostic，不是自适应动作 | near-unitary 自动 guard 的 `tau_SU` 无 authority；nonunitary 偏差需 correctness negative control 暴露 |
| B | `PASS_WITH_BOUNDARY` | polar/Procrustes、unitary Jones estimation 与 balanced-pilot direct constrained form 都是已知原子/等价表述；但 bounded closure 未确认完整 target-scene recipe collision，D031/D032 仍允许 classical migration | 只允许窄场景迁移 claim；不得声称新 estimator、首次、SOTA 或普适性 |

总体 terminal 为 `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY`：C4-1 仅在 strict scaled-unitary slice 上具有纸面可测性，允许主控另派**最小 correctness**；这不是方法成立，也不授权 headroom 执行、正式结果或论文正文。

`14/18 dB × 2/4 pilots` 是 T068 指定的最小候选网格（`.sessions/2026-07-09-thesis-writing/T068-c4-1-scaled-unitary-step4a-paper-feasibility.md:37`），但本轮本地论文证据没有为这些具体数值提供 target-scene authority。因此 headroom manifest 可以冻结，执行状态必须保持 `PARAMETER_AUTHORITY_BLOCKED`；不得用本轮仿真补写来源。

## 1. 冻结研究对象、证据与 IAO

### 1.1 证据边界

- T048 已完成 7/7 全文精读；Q-C4-1 被裁为 `SURVIVES_BOUNDED / STRONG_RECIPE_NEIGHBOR`，不是 clean novelty（`projects/thesis-fso/literature_notes_apsk_front_end.md:19,119-131`）。
- T064 的九字段 ledger 未出现全 Y 的已发表对象，terminal 为 `SURVIVES_AS_CLASSICAL_MIGRATION`（`projects/thesis-fso/polarization-demux-groundwork/step3-5-c4-1-exact-recipe-closure.md:5,109-138`）。
- 当前平台直接支持 memoryless 2×2 Jones 与 unitary 默认边界；PDL-like nonunitary gain 只可作无量级 negative test，PDL/PMD/FIR 在最小 slice 中关闭（`projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:112-124,135-144`）。
- D048 只授权候选专属 A0/A′/A/B；paper gate 通过后仍须另过 correctness/headroom（`.sessions/2026-07-09-thesis-writing/decisions.md:1772-1796`）。

### 1.2 Frozen input → action → output

接收模型为

\[
Y_p=HX_p+N_p,\qquad X_pX_p^{\mathrm H}=cI_2,\ c>0,
\]

目标 slice 为

\[
H=gQ,\qquad g>0,\quad Q^{\mathrm H}Q=I_2,
\]

且无 PDL、PMD、FIR 或 receiver branch imbalance。

完整 receiver-visible recipe 冻结为：

1. **input**：receiver-known balanced pilots `X_p`、对应接收 pilots `Y_p`、payload samples `y`；
2. unconstrained LS：
   \[
   \widehat H_{LS}=Y_pX_p^{\mathrm H}(X_pX_p^{\mathrm H})^{-1};
   \]
3. SVD：`H_LS=U diag(s1,s2)V^H`，约定 `s1>=s2>=0`；
4. scaled-unitary projection：
   \[
   \widehat g=(s_1+s_2)/2,\quad \widehat H_{SU}=\widehat gUV^{\mathrm H};
   \]
5. demultiplexing action：
   \[
   W=VU^{\mathrm H}/\widehat g,\qquad z=Wy;
   \]
6. **output**：`z`、`g_hat`、`rho=s1/s2` 与 numerical-valid flag；`rho` 只报告 applicability，不在本阶段驱动分支。

当 `g_hat=0`、`s2=0` 或数值无效时必须 fail closed 到一般 LS 家族；本报告不拍浮点容差。对于“near-unitary 但非 strict”的运行时 guard，必须另有 development authority 后冻结 `tau_SU`，并将 fallback 预注册为 tuned ridge 或 full-SVD floor 中的最强者。当前 strict slice 不靠 `rho` 阈值承重。

### 1.3 Balanced-pilot 等价性

当 `X_pX_p^H=cI` 时，

\[
\min_{g\ge 0,Q^HQ=I}\lVert Y_p-gQX_p\rVert_F^2
\]

等价为对 `H_LS` 的 Frobenius nearest scaled-unitary problem，其最优解为

\[
Q^\star=UV^H,\qquad g^\star=(s_1+s_2)/2.
\]

所以 direct constrained scaled-unitary LS 与 `unconstrained LS → scaled-polar` 是**同一 estimator 的两种表述**，不是两个 competitor，也不能制造两项贡献。完整推导与边界见 `projects/thesis-fso/polarization-demux-groundwork/step3-5-c4-1-exact-recipe-closure.md:40-75`。

## 2. A0：问题—方法适配性预检

### 2.1 §0 M-C-A 与问题四判据

| 元素 | 冻结定义 |
|---|---|
| M | 同一 balanced pilot block 上的 unconstrained complex 2×2 pilot-LS，随后直接 inverse；增强版本为 independently tuned ridge 与 independently tuned singular-value floor/full-SVD inverse |
| C | DP-(8,8)-16APSK coherent FSO；`H=gQ` 的 memoryless single-tap slice；短 receiver-known balanced pilots；equal-branch white noise；无 PDL/PMD/FIR |
| A | unconstrained LS 未使用真实 scaled-unitary 结构，在短 pilot 下保留 3 个不属于 `gU(2)` 流形的实法向噪声自由度；直接求逆还会把这部分估计噪声传入 payload demultiplexing |

| 问题判据 | verdict | facts-first 依据 |
|---|---|---|
| 1. 具体 M/C/A | `PASS` | M、C 与多余自由度机制均可逐式定义；不是“DP-APSK 上没人做”这一空白陈述 |
| 2. 有方法产出形态 | `PASS` | 产出是闭式 `X_p,Y_p → H_LS → H_SU,W → z,rho` recipe，可复用为 receiver estimator/demux 与适用域诊断 |
| 3. 有 baseline 可对标 | `PASS_WITH_BOUNDARY` | unconstrained LS、ridge、SV-floor 均为正确经典 baseline；2022 Kabsch/unitary estimator 还以 data-aided LS 为 comparator，但本地仅摘要级。按 D031/D032，经典 baseline 与强邻居限制 claim，不因非期刊级 novelty 自动 Kill（`.sessions/2026-07-09-thesis-writing/decisions.md:1094-1115,1138-1166`） |
| 4. 能量化对标 | `PASS` | 同 pilot overhead 下 payload BER 为主；channel NMSE、inverse residual、`rho` 为机制；oracle 给出上界但不作 Go 对手 |

四判据结论：`4/4 PASS_WITH_BOUNDARY`。边界来自经典原子与强 recipe 邻居，不来自问题缺失。

### 2.2 短 pilot 方差问题

balanced pilots 与 equal-white noise 下，

\[
\widehat H_{LS}=H+E,\qquad E=N_pX_p^H/c,
\]

`E` 在 2×2 complex matrix 的 8 个实坐标上局部各向同性。一般 complex 2×2 LS 有 8 个实自由度；`gU(2)` 在 `g>0` 处有 `1+dim_R U(2)=5` 个实自由度。若真值位于 strict scaled-unitary 流形，高 SNR/小扰动下一阶正交投影只保留 5 维切空间噪声并删除 3 维法向噪声，因此局部一阶 channel-MSE 比例为约 `5/8`，即法向噪声项约减少 `3/8=37.5%`。

这是**解析局部方差预测**，不是 BER、NMSE 实测数字，也不适用于显著 nonunitary truth。它足以证明问题不是凭标题联想，但不能证明 payload BER 必然改善。若 tuned ridge/SV-floor 已回收同等或更大 BER headroom，C4-1 按预注册停机，不以“结构更漂亮”保留。

### 2.3 方法类型适配

本项目 master-state 将该线定义为 `reference-method extension（非 ML）`。因此 `gw-feasibility` 中 ML 状态空间、跨域 ML 先例与 MDP `S/A/R/P` 条款为 `N/A（非 ML）`，不能机械套用为 Kill 条件。对应的传统估计问题是：已知低维物理流形能否以一个无学习、闭式、receiver-visible 的投影降低有限样本估计方差，同时不引入结构偏差。

候选采用最简单的闭式结构估计，没有学习器、长期奖励、隐状态策略或额外数据，满足“先检查简单方法”的 A0 原意。

### 2.4 负面证据与先验覆盖

- polar/Procrustes、nearest unitary/scaled-unitary 与 unitary Jones estimation 均是经典原子；这否定“新 estimator”身份，不否定目标场景迁移。
- Roudas 2010 已覆盖短 training + LS initialization + 低维 unitary demux/blind tracking，是最强全文通信邻居；2022 Kabsch 是最强新邻居，但都未确认九字段完整 target-scene recipe collision（`projects/thesis-fso/polarization-demux-groundwork/step3-5-c4-1-exact-recipe-closure.md:95-122`）。
- ridge 与 SV-floor 可能用更一般、低偏差的方式回收短-pilot BER；因此二者必须独立调优并进入同开销 ladder，不能只打裸 LS。

A0 terminal：`PASS_WITH_BOUNDARY`。问题存在性为解析合理且可证伪，BER headroom 仍是未闭合假设。

## 3. A′：竞争维度分解

| 竞争维度 | 承重级别 | 公平口径 | 本候选预期 | 停机解释 |
|---|---|---|---|---|
| payload BER | **唯一主承重** | 同 bits、同 `H`、同 noise、同 `X_p/Y_p`、同 pilot count/energy、paired arms；各 baseline 独立同预算 tuning | strict unitary + short pilots 时，降低 channel-estimation noise 传播 | 不优于 best tuned LS/ridge/SV-floor，则问题对方法章 absent |
| channel NMSE | 机制诊断 | `||H_hat-H||_F^2/||H||_F^2`；truth 只在 evaluator | 验证 `5/8` 一阶趋势与 bias-variance 机制 | NMSE 改善而 BER 不改善，不能承章 |
| inverse residual | 机制诊断 | `||WH-I||_F`；truth 只在 evaluator | 验证逆矩阵是否更接近 demux identity | residual 改善而 BER 不改善，不能承章 |
| `rho=s1/s2` | applicability diagnostic | 只由 `H_LS` 计算；与 truth nonunitarity 仅离线对照 | strict unitary 下趋近 1，nonunitary control 下偏离 1 | 不得单独作为性能或方法结果 |
| pilot overhead | 公平约束 | 所有非-oracle arms 使用完全相同 pilots；direct constrained form不重复计数 | 无额外 pilots | overhead 不同则比较无效 |
| 复杂度 | 说明项 | 报告 2×2 SVD 与 inverse 的实际调用，不以 proxy 冒充时延 | 固定小矩阵额外成本 | 不能替代 BER 主指标 |

竞争顺序冻结为 `payload BER > channel NMSE / inverse residual > rho / complexity`。pilot overhead 始终相同，不是可供候选单独获益的轴。oracle 只量化 headroom，不属于 deployable baseline，也不能成为 Go 判据。

## 4. A：结构优势、适用域与 guard/fallback

### 4.1 结构优势与可证伪机制

在真值 `H=gQ` 且 balanced LS noise 局部各向同性时，`H_LS` 的 3 个法向自由度只包含估计噪声；scaled-polar 正交投影删除这些分量，同时保留公共尺度与 unitary mixing 的 5 维切空间。相对裸 LS，这是一项明确的 bias-free（一阶、模型内）降方差动作；相对 ridge/SV-floor，它使用更强的等奇异值结构，因此可能进一步降方差，也更容易在结构失配时产生偏差。

该机制被以下任一事实推翻：

1. 无噪 strict-unitary exact recovery 或 balanced equivalence 不成立；
2. paired unitary slice 中 C4-1 不优于 best tuned unconstrained/ridge/SV-floor 的 payload BER；
3. oracle `Q^H/g` 相对 best conventional arm 无 BER headroom；
4. 改善只存在于 NMSE/inverse residual，未传导到 BER；
5. candidate action 或 fallback 读取 true `H/Q/g`、truth PDL、eval BER 或未授权未来信息；
6. nonunitary negative control 仍被误报为“结构适用”，或投影偏差未被暴露。

### 4.2 `rho` 的身份

`rho=s1/s2` 是 **diagnostic，不是 action**：

- 它可由 receiver 的 `H_LS` 直接计算，满足 receiver-visible；
- 它不能证明真值无 PDL，也不能把估计噪声与真实非酉性完全分开；
- 当前报告不定义 `rho<=tau_SU` 的拍脑袋阈值，不把 guard 选择贡献计入方法；
- strict unitary headroom slice 由预注册场景定义，而不是运行时偷看 truth；
- 若未来把方法扩展为 near-unitary 自动 guard，必须用 development-only receiver observations 冻结 `tau_SU`，在 eval 前锁定，并与 always-C4-1、always-fallback 同时比较。

fallback 对实际 recipe 是必要安全边界，但当前只冻结语义：numerical invalid 时 fail closed；已知/声明超出 strict slice 时回 tuned ridge 或 full-SVD floor 中的冻结强者。PDL/PMD/FIR 的阈值与分布没有 authority，不能靠它们制造方法空间（`projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:51-55,184-191`）。

### 4.3 最小 comparator ladder

| arm | 冻结动作 | 角色 |
|---|---|---|
| B0 unconstrained LS | `H_LS=YpXp^H(XpXp^H)^-1`，再直接 inverse | 当前经典 baseline |
| B1 tuned ridge | `H_ridge=YpXp^H(XpXp^H+lambda I)^-1`；`lambda` 仅 development tuning | 一般低方差增强 baseline |
| B2 tuned SV-floor | 对 `H_LS` 做 full SVD，保留两个奇异值，仅以独立 tuned floor 稳定 inverse | 最强廉价结构替代，不强制等奇异值 |
| C4-1 | 两奇异值取均值的 scaled-polar，`W=VU^H/g_hat` | 候选 |
| O1 true oracle | `W_oracle=Q^H/g` | 非部署 BER headroom 上界 |

direct constrained scaled-unitary LS 只进入 balanced-equivalence correctness，不重复计为 competitor 或曲线。所有 deployable arms 必须共享 pilot、payload、channel/noise realization、tuning-call budget 与评价代码；O1 与 deployable 结果分栏。

A terminal：`PASS_WITH_BOUNDARY`。结构优势只在 strict scaled-unitary slice 合法；near-unitary/PDL 扩展未获授权。

## 5. B：新颖性—可行性解耦

### 5.1 新颖性事实与 claim ceiling

现有证据支持：

- balanced pilots 下 post-LS scaled-polar 与 direct constrained scaled-unitary LS 代数等价；
- polar/Procrustes、scaled matrix-nearness 与 unitary Jones estimation 均不是新原子；
- Roudas 2010 与 2022 Kabsch 是强邻居；
- bounded Step 3.5 尚未确认“算法步骤 + receiver-visible I/O + 目标场景 + 关键配置”完整相同的已发表 recipe。

因此唯一可用身份是：

> 将经典 scaled-unitary constrained estimation 迁移到 receiver-known balanced short pilots、memoryless strict-scaled-unitary 2×2 Jones mixing 的 DP-(8,8)-16APSK 星地相干解复用，并显式报告 receiver-visible singular-value-ratio applicability diagnostic 与失效边界。

禁止声称发明 polar/Procrustes、scaled-unitary projection、direct constrained estimator 或 unitary Jones estimation；禁止“首次”、SOTA、普适最优；禁止外推到显著 PDL、PMD、FIR、branch imbalance、不等噪声或任意调制。D031/D032 明确规定强邻居、经典原子与廉价替代只限制有限 claim；只有完整 recipe collision、真实性失败或目标场景无真实改善才关闭候选（`.sessions/2026-07-09-thesis-writing/decisions.md:1103-1115,1147-1166`）。

### 5.2 可行性预测

可行性来自“正确低维结构投影删除短-pilot LS 法向噪声”的解析机制，以及 strict unitary single-tap 平台 authority；不来自“没人做过 DP-APSK FSO”。预测仅为：在 pilot 信息有限且真值严格满足 `H=gQ` 时，C4-1 可能以较低 channel-estimation variance 改善 payload BER。实际改善幅度、工作区与是否胜过 tuned ridge/SV-floor 均未知。

### 5.3 空白零假设

| 空白可能原因 | 反驳/处理 | 当前状态 |
|---|---|---|
| direct constrained estimator 已存在，post-LS form 只是重写 | 承认两者 balanced-equivalent，只计一个 estimator；不声称估计理论新颖，claim 收缩为 target-scene migration | `RESOLVED_BY_CLAIM_CEILING` |
| strict scaled-unitary 场景过窄，现实 PDL/branch imbalance 会使投影有偏 | 当前平台主动默认 unitary，故可作 bounded slice；nonunitary 只作 negative control，不能外推 | `BOUNDARY` |
| tuned ridge/SV-floor 已回收全部 BER headroom | 两者进入独立调优 ladder；若 C4-1 对二者均无 BER 改善则关闭 | 待 headroom |
| 短 pilots 的 LS 方差虽下降，但 payload BER 对该差异不敏感 | BER 为唯一主承重；NMSE-only 结果不构成方法 | 待 headroom |
| 九字段完整 target-scene recipe 实际存在但 bounded closure 漏检 | T064 明确是非穷尽 survival；后续任何可核 collision 都可重开裁决，当前不得写“首次” | `BOUNDED_UNCERTAINTY` |

以上零假设没有在纸面上证明问题 absent 或结构自相矛盾；其中两项已通过 claim/boundary 收缩处理，剩余项交给最小 headroom，而不是以期刊级 novelty 自动 Kill。

B terminal：`PASS_WITH_BOUNDARY`。

## 6. 最小 correctness manifest（唯一可立即另派的后继）

本 manifest 只验证语义，不输出方法性能：

| gate | 最小检查 | PASS 条件 | FAIL 后果 |
|---|---|---|---|
| C0 无噪 exact recovery | balanced full-rank `X_p`、`N=0`、多个 `g>0` 与随机 `Q∈U(2)` | `H_LS=H_SU=H`，`W=H^-1`，`z=x` 到数值容差 | `CORRECTNESS_FAIL`，禁止 headroom |
| C1 balanced equivalence | 同一 `Y_p,X_p` 分别算 post-LS projection 与 direct constrained objective | 两者的 `H_hat`、objective 与 demux output 一致到数值容差 | `CORRECTNESS_FAIL` |
| C2 unitary/global-scale equivariance | 对输入施加左右 unitary basis change `L,R` 与非零 complex global scale `alpha` | 验证 `P(LHR)=L P(H) R`、`W(LHR)=R^H W(H)L^H`、`P(alpha H)=alpha P(H)`、`W(alpha H)=alpha^-1 W(H)`；`rho` 对上述变换不变 | `CORRECTNESS_FAIL` |
| C3 nonunitary negative control | paired 构造 `delta=0` 与 `H=g U diag(1+delta,1-delta)V^H`、`0<delta<1`；仅作数学 negative，不声称物理 PDL 值 | 无噪下 `delta=0` 应有 `rho=1`、projection bias/residual 为 0；`delta>0` 应复现理论 `rho=(1+delta)/(1-delta)` 与非零投影 bias/residual，并不得计入适用域 | 失效边界无效，禁止 claim |
| C4 truth firewall | hidden-truth metamorphic：固定 `X_p,Y_p,y`，只改 true `H/Q/g` 与评分 metadata | C4-1 action、`z/g_hat/rho` byte-identical；oracle/scoring 可变但与 deployable path 隔离 | `TRUTH_LEAKAGE`，候选无效 |
| C5 numerical fail-closed | 零矩阵、exact rank-deficient、NaN/Inf fixtures | 不产生伪 inverse 或伪 applicability PASS；明确返回 invalid/fallback request。near-zero 阈值不在 correctness 临场拍定，若后续需要则在 development 前单独预注册 | `CORRECTNESS_FAIL` |

correctness 实现不得顺手加入 SNR/pilot grid、PDL 参数、guard threshold 或 BER 结果。

## 7. 最小 headroom manifest（冻结但暂不可执行）

### 7.1 Frozen grid

- slice：仅 strict unitary memoryless single-tap `H=gQ`、equal-branch circular white noise；无 PDL/PMD/FIR/IQ imbalance；
- SNR：`14 dB`、`18 dB`；
- balanced pilot counts：`N_p=2`、`N_p=4`；
- arms：B0 unconstrained LS、B1 tuned ridge、B2 tuned SV-floor/full-SVD inverse、C4-1、O1 true `Q^H/g` oracle；
- paired：每个 cell 的 bits、`X_p`、`Q/g`、pilot noise、payload noise 与 seeds 在所有 arms 间完全相同；
- primary：payload BER；mechanism：channel NMSE、`||WH-I||_F`、`rho`；pilot overhead 完全相同；
- tuning：B1/B2 各自在 development-only 数据上独立调优且共享相同 tuning-call budget；C4-1 无 `rho` gate tuning；eval 前冻结。

### 7.2 Parameter authority status

平台论文 authority 支持 strict unitary single-tap slice，但没有为 target DP-(8,8)-16APSK 冻结 `14/18 dB` 与 `2/4 pilots`。因此：

`PARAMETER_AUTHORITY_BLOCKED`

该状态只阻断 headroom 执行，不阻断 §6 的纯 algebraic correctness。解除方式必须是主控提供可核的本地论文/正式平台 authority，或显式将这些点降为“不承载物理代表性的开发诊断点”；T068 executor 不自行联网、下载或跑数据补洞。

### 7.3 Stop / pivot

**关闭 C4-1 并轮换 C4-0**（任一成立）：

1. 任一 correctness C0–C5 FAIL；
2. 完整 target-scene recipe collision 获得可核证据；
3. oracle 相对 best tuned non-oracle arm 无 payload-BER headroom；
4. C4-1 在所有冻结 cell 均不优于 best tuned B0/B1/B2 的 payload BER；
5. 任何优势依赖 truth、不同 pilots、不同 tuning budget 或不同 realization；
6. 只有 NMSE/inverse residual 改善而 payload BER 无改善。

**只收窄，不扩损伤救结果**：

- 只有 `N_p=2` 有 BER 改善 → claim 收窄为 minimal-pilot slice；不增加 PDL/PMD/FIR；
- ridge 或 SV-floor 为最强者 → C4-1 不以更复杂结构强行保留；按 D048 停止本候选；
- nonunitary control 暴露偏差 → 保留为 limitation，不据此新增 guard 方法或新候选；
- `rho` 有诊断排序但无 authority threshold → 保持 diagnostic，不升级为动作。

## 8. 最终裁决与唯一下一步

`A0=PASS_WITH_BOUNDARY / A′=PASS / A=PASS_WITH_BOUNDARY / B=PASS_WITH_BOUNDARY`。

总体 terminal：`PAPER_DIMENSIONS_PASS_WITH_BOUNDARY`。

独立状态：`PARAMETER_AUTHORITY_BLOCKED`（仅 headroom grid）。

**唯一下一步**：由主控另派 §6 的最小 correctness 实现与独立复核；在 C0–C5 全 PASS 且 `14/18 dB × 2/4 pilots` 参数 authority 解除前，不运行 headroom，不给 Step 4a Go/Conditional Go，不写正式论文正文，不创建新候选。
