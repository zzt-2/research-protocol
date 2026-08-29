# Ch5 Q-C5-1 GW Step 4a 纸面可行性

> T051｜2026-08-30｜只评估 A0 §0–§6、A'、A、B。
> 未进入维度 D/MVE；未实现、未实验、未形成 Go/Conditional Go。

## 0. 终态摘要

- **总 verdict：`PAPER_DIMENSIONS_PASS`**。
- **A0：PASS（纸面）**。Q-C5-1 的 M/C/A 与四判据仍成立；问题依据是低 pilot 下逐点 full covariance 的可估计性缺陷，不是“没有 exact collision”。
- **A'：PASS（纸面）**。主竞争维度冻结为同 pilot 预算下的 GMI 与 coded FER/required-SNR；估计方差、正定性与 BER 是机制/中间指标，pilot overhead 固定，复杂度只作次级或 fallback。
- **A：PASS（纸面）**。radial/tangential 结构将每点 covariance 的自由度从 3 降到 2；同环/跨偏振 shrinkage 进一步降低有效自由度，以可控偏差换取低样本方差与正定性。
- **B：PASS（有限 claim）**。Layton 2018、full covariance、Mahalanobis/log-det 与 generic shrinkage 均已占用；可保留的最窄差别仅是 pilot-limited APSK 几何结构化 estimator 与 matched-budget hierarchical pooling recipe。
- **唯一 blocker（通往科学 Go）**：尚无获授权的同预算 target-platform oracle/headroom 结果，因而还不知道 candidate v1 是否能在 GMI/FER 上超过 strongest cheap comparator。该项只能由后续单独授权的维度 D 闭合。

本报告只说明“值得进入维度 D 检验”，不说明方法已经有效。共同平台的 filter/FIR authority 债不阻塞 memoryless Ch5 最小切片；本候选不得借此主动叠加 receiver filter、PMD、PDL 或 CFO 制造 headroom。

## 1. 证据边界

### 1.1 承重事实

1. Layton 2018 已给出逐星座点 bivariate Gaussian、symbol-dependent full covariance、Mahalanobis/determinant likelihood、pilot sample covariance；低 pilot 时仅一般性建议跨 frame 或 biased shrinkage。证据：`papers/doi/10.1186_s13638-018-1136-z/content.md:135`、`:139`、`:149`。
2. Layton 的 pilot sweep 显示 pilot 增加会改善 coded BER 所需 SNR 直至平台，且高阶 APSK 因参数更多需要更多 pilots；但没有给 target DP-(8,8)-16APSK 上 structured-vs-unstructured 的数字。证据：同文 `:269`–`:283`。
3. T046 已冻结 receiver-visible/causal 边界与同预算 comparator ladder；Q-C5-1 的 M/C/A 和四判据为 4/4。证据：`projects/thesis-fso/literature_notes_apsk_soft_receiver.md:37`–`:48`、`:97`。
4. T049 在 63 个去重记录的 bounded slice 中未确认完整 recipe collision；Layton 是最强 primitive collision，generic shrinkage 也已存在。证据：`projects/thesis-fso/apsk-soft-receiver-groundwork/step3-5-supplement-report.md:32`–`:39`、`:50`–`:60`。
5. Ch4→Ch5 接口提供 post-equalization symbols、noise covariance metadata 与 constellation/labeling identity；若噪声未验证为 scalar，Ch5 不得静默使用 AWGN scalar 近似。证据：`projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:169`–`:182`。

### 1.2 证据不能支持的声称

- 不能声称首次提出 covariance-aware demapping、Mahalanobis/log-det LLR、APSK full covariance 或 covariance shrinkage。
- 不能声称 target DP-(8,8)-16APSK 上已存在可观测 BER/FER headroom。
- 不能声称本次 bounded Step 3.5 穷尽领域或证明不存在 exact recipe。
- 不能把 Layton 在 64/128-APSK、TWTA/phase-noise 场景的最高约 4 dB 迁移成我方预期数字。
- 不能用共同平台的 `Sigma_n` metadata 代替从当前/过去 pilots 实际估计 residual covariance。

## 2. A0 §0：合法问题门

### 2.1 固定 Q# 与 M/C/A

- **Q#**：`Q-C5-1`。
- **M**：Layton 式逐点 unstructured 2×2 full-covariance estimator，并在相同 LLR 中使用该 covariance。
- **C**：DP-(8,8)-16APSK；Ch4 后的两个 tributary；runtime 只允许当前/过去 pilot residual；每点 pilot 样本少；相同 pilot/sample/update budget。
- **A**：每个星座点的 covariance 可独立、稳定、正定地估计，因此无需利用 APSK radial/tangential 几何，也无需同环/跨偏振统计强度共享。
- **拟议产出**：一个 receiver-visible 的 structured shrinkage covariance estimator，以及与 Mahalanobis/log-det bit LLR 相接的完整同预算 receiver recipe。

### 2.2 四判据复核

| 判据 | verdict | 依据 |
|---|---|---|
| 具体 M-C-A 矛盾 | PASS | M、C、A 均可操作；缺陷是低样本估计问题，不是领域标题或文献空白。 |
| 方法产出形态 | PASS | estimator、pooling、PD projection 与 LLR 接口可形成可复用算法链。 |
| 可对标 baseline | PASS_WITH_CLAIM_LIMIT | Layton 是直接 conventional comparator；isotropic/per-ring/full ladder 明确。Layton 为 2018，因此只能作为经典直接 baseline，不包装成“近期竞品”。 |
| 可量化对标 | PASS | covariance NMSE/condition、GMI、BER、FER/required-SNR、复杂度均可按同预算比较。 |

**A0 §0 verdict：PASS。** T049 的 `Q-C5-1 SURVIVES` 只处理 collision；本节的成立依据是 M 在 C 下的样本复杂度与估计稳定性缺陷。若后续发现共同平台每点实际 pilot 数足以让 full covariance 稳定并消除下游差距，问题即被实证否定。

## 3. A0 §1–§6：问题—方法适配

### §1 性能间隙

当前没有 target-platform 数字，故不得按 ≥15%、5–15% 或 <5% 给 Go/Kill。现有证据只支持三个纸面事实：

1. 每点 real 2×2 symmetric covariance 有 3 个自由度；样本均值未知时，样本 covariance 的秩至多为 `N_k-1`，`N_k≤2` 时必然不可逆，略高于该下限时逆矩阵与 log-det 仍可能高方差。
2. `(8,8)-16APSK` 单偏振共有 16 点：covariance-only 参数为 48；双偏振独立估计为 96。Layton 自身确认高阶 modulation 需要更多 pilots 才到性能平台。
3. 是否存在 end-to-end headroom 仍未知：structured estimator 可能降低 NMSE，却不一定跨过 decoder threshold 或改善 FER。

因此本节为 **paper-level PASS / numeric gap UNKNOWN**。未知数字不作为 Go 论据；它就是后续 oracle/headroom 门要回答的唯一问题。

### §2 问题结构与复杂学习必要性

本问题不需要 ML、DRL 或复杂学习。它是带 APSK 几何先验的小样本 covariance estimation：

- 星座 ring/angle 是固定、receiver-visible 的确定性信息；
- radial/tangential rotation、样本二阶矩、解析 shrinkage 与 eigenvalue floor 均有闭式实现；
- runtime 不需要训练集、神经网络、状态转移或跨 episode optimization。

**结论**：复杂学习路线应在 A0 被拒绝；这不 Kill 当前候选，因为当前候选本身就是简单解析 estimator。若后续必须依赖 learned mapping 才产生差距，应 Pivot，而不是把复杂学习追加到 v1。

### §3 相邻先例与方法血缘

- Layton 证明 data-dependent covariance 可进入 APSK/QAM likelihood，并明确低 pilot 可使用 biased shrinkage。
- Schäfer–Strimmer 只占用 generic analytic covariance shrinkage/PD 原子。
- T049 的 polar/ring-aware 邻居只占用几何似然或 ring prior 原子，没有 target pilot-residual structured estimator。

这些先例足以支持“各组件可执行”，但不支持“组合后必有 GMI/FER 增益”。因此本节无致命不匹配，也无经验性 Go。

### §4 MDP 非平凡性

`N/A`。候选是确定性统计 DSP，不存在 S/A/R/P、策略学习或延迟奖励。把它改写成 MDP/学习问题会增加无必要复杂度并违反 §2。

### §5 负面证据与预注册 failure modes

bounded evidence 中没有找到 target 完整 recipe 的失败报告；这不等于不存在失败。维度 D 前必须保留以下可证伪 failure modes：

1. **近各向同性**：thermal-noise 主导时 `σ_r²≈σ_t²`，scalar/per-ring scalar 已吸收全部收益。
2. **几何错配**：residual 主轴不沿 symbol radial/tangential 方向；丢弃 rotated off-diagonal 会产生系统偏差。
3. **硬 pooling 偏差**：同环不同点因前端残差、labeling 或非线性而不交换；pooling 降方差但抹掉真实 point dependence。
4. **跨偏振负迁移**：两个 tributary 的长期统计强度不同；直接合并 samples 会污染 covariance。
5. **时间失配**：causal window 太长跟不上残差变化，太短则样本不足。
6. **指标不传递**：covariance NMSE/PD 改善没有转化为 GMI、BER 或 FER 改善。

### §6 先验覆盖与 strongest cheap alternative

主指标不能只与 raw/singular full covariance 比较。最强廉价替代冻结为：

**`hard-pooled per-ring radial/tangential covariance`**：把同一 ring 的所有 pilot residual 旋转到共同 radial/tangential frame，直接为每个 ring、每个 polarization 估计一对方差；不保留 point-local covariance，不做分层 shrinkage。它用同一 receiver-visible 信息，只有单偏振 4 个 covariance 参数、双偏振 8 个，天然正定且直接攻击小样本缺陷。

若该 cheap comparator 已获得 candidate v1 相对 scalar/full 的 ≥95% end-to-end 改善，而 v1 的 point-local shrinkage 增量 <5%，则 v1 的承重机制被简单策略覆盖，必须 Pivot 到 hard pooling 或降为复杂度/鲁棒性小组件。

**A0 总 verdict：PASS（纸面）**。没有结构性致命信号；唯一未闭合项是 target-platform 的可量化 headroom。

## 4. A'：竞争维度分解

| 维度 | 角色 | 先验覆盖 | candidate v1 预期增量 | 能否承重 |
|---|---|---|---|---|
| covariance variance/bias | 机制诊断 | full 低 pilot 方差高；hard pooling 偏差可能高 | 在两者之间做 bias–variance interpolation | 否，单独 NMSE 改善不够 |
| positive-definiteness / conditioning | correctness gate | floor、generic shrinkage、hard pooling 都可解决 | 结构保证更稳定的 inverse/log-det | 否，已被廉价方案覆盖 |
| GMI | 软信息主指标 | scalar/full/hard pooling 均可计算 | 更匹配的 LLR 应提高 GMI | **是，主承重之一** |
| BER | 中间应用指标 | conventional | GMI 改善应降低 pre/post-demapper BER | 支撑，不单独替代 FER |
| FER / required SNR | coded receiver 主指标 | conventional | 在相同 LDPC/iterations 下改善 FER 或 target-FER 所需 SNR | **是，首要承重** |
| pilot overhead | 固定公平条件 | 所有方法相同 | candidate 不允许多拿 pilot | 否；不是竞争维度 |
| runtime / storage | 次级/fallback | scalar/hard pooling 最低，full 最高 | 少于 full 的存储/逆矩阵不稳定处理 | 仅 fallback B/C |

### 指标优先级

1. **首要**：同 pilot budget、同 decoder 下的 FER/required-SNR。
2. **共同主指标**：GMI，用于在 decoder threshold 尚未冻结时验证 LLR 信息质量。
3. **机制指标**：covariance NMSE、eigenvalue/condition number、PD failure rate。
4. **支撑指标**：BER、runtime、stored parameters。

不可承重：仅“保证正定”、仅“估计更稳”、仅“复杂度比 full 低”、或在 pilot overhead 不相同的比较中获益。

**A' verdict：PASS。** 声称已从易被简单策略吸收的 PD/NMSE 维度转到 GMI/FER；同时保留 cheap comparator 防止虚假增量。

## 5. A：结构优势与最小 oracle/headroom 计划

### 5.1 自由度与 bias–variance 机制

对星座点 `k`、polarization `p`，令 `R(θ_k)` 把 I/Q residual 旋转到 radial/tangential frame：

\[
\Sigma_{k,p}^{\mathrm{str}}
=R(\theta_k)
\operatorname{diag}(v_{r,k,p},v_{t,k,p})
R^T(\theta_k).
\]

- unstructured full：3 covariance DOF/点，即单偏振 48、双偏振 96。
- point-local radial/tangential：2 DOF/点，即单偏振 32、双偏振 64。
- hard per-ring radial/tangential：2 DOF/ring，即单偏振 4、双偏振 8。
- hierarchical shrinkage：保留 64 个 local 参数的表达能力，但通过 shrinkage 把有效自由度连续压向 8；若 ring target 还只共享跨偏振统计强度而不共享瞬时 samples，则避免把两个 tributary 强行设为同分布。

候选的结构优势不是“参数更少必然更好”，而是：在低 `N_k` 时删除与 APSK 几何不一致的 rotated cross-term，并把 noisy local variance 向同 ring target 收缩，从而降低 inverse/log-det 的估计方差；代价是主轴不对齐或同环不齐性时引入偏差。维度 D 必须同时测这两面。

### 5.2 最小 oracle/headroom 计算计划（本轮不执行）

后续若获维度 D 授权，先做纯 headroom gate，再决定是否实现完整 MVE：

1. 固定一份独立的大样本 calibration/evaluation residual，仅用于 oracle，不进入 deployable estimator。
2. 用同一 `μ_k` 估计和同一 LLR/decoder，计算：oracle unstructured、oracle radial/tangential、isotropic、per-ring scalar、hard-pooled radial/tangential、Layton unstructured+generic shrinkage。
3. 先比较 oracle radial/tangential vs oracle unstructured，量化几何投影偏差；再比较 deployable estimators 与各自 oracle，分离 model bias 与 estimation variance。
4. 在冻结的低 pilot budgets 上报告 covariance NMSE/condition、GMI、BER、FER/required-SNR；所有方法使用相同 pilots、causal window、update rate 与 decoder iterations。
5. oracle 只作 Kill/ceiling 工具，不作 Go comparator。若 oracle structured 相对 strongest cheap comparator 的 required-SNR headroom 在全部授权 cells 均 `<0.5 dB`，直接 `KILL_BEFORE_MVE`。

**A verdict：PASS（纸面）**。结构优势可证伪、自由度与偏差—方差方向明确；实际 headroom 未计算。

## 6. B：新颖性—可行性解耦

### 6.1 外部 novelty

- bounded Step 3.5 未确认完整 recipe collision，故可以保留下一 formal gate。
- 该结果不能支持 first/SOTA/exhaustive claim。
- Layton 已完整覆盖 full covariance + Mahalanobis/log-det；Schäfer–Strimmer 已覆盖 generic shrinkage；这些都压低 claim ceiling。
- 可保留的最窄身份：**pilot-limited APSK radial/tangential structured covariance with matched-budget hierarchical pooling for DP soft demapping**。

### 6.2 科学 feasibility

科学 feasibility 不依赖“无人做过”，而依赖以下机制链：

`每点 pilot 少 → full covariance inverse/log-det 高方差或不稳定`
`→ APSK 几何提供可验证的 radial/tangential 低维假设`
`→ 同环/跨偏振统计强度 shrinkage 降方差`
`→ 更匹配且稳定的 LLR`
`→ GMI/FER 在同 pilot 预算下改善`。

前三个箭头有统计结构与邻居证据；最后两个箭头尚无 target-platform 数字，必须由维度 D 判定。

### 6.3 空白零假设

| 可能原因 | 反驳/处置 |
|---|---|
| generic shrinkage 已足够，没必要 APSK-specific structure | 不口头反驳；加入 unstructured+generic shrinkage 与 hard-pooled R/T 两个强 comparator。 |
| residual 在目标平台近 isotropic，radial/tangential 信息为零 | 不口头反驳；oracle anisotropy与 scalar gap 为 pre-MVE Kill gate。 |
| 同环/跨偏振并不 exchangeable，pooling bias 大于降方差收益 | 不口头反驳；分别消融 ring pooling 与 cross-pol strength sharing。 |
| full covariance 在实际 pilot budget 已足够稳定 | 不口头反驳；冻结真实 `N_k`，比较 condition/NMSE 与 GMI/FER。 |
| decoder threshold 吸收全部 LLR 改善 | 不口头反驳；GMI 与 coded FER 同时报，FER 不改善则主 claim 不成立。 |

**B verdict：PASS_WITH_NARROW_CLAIM。** novelty 只允许限定完整 recipe；feasibility 仍以可证伪的 end-to-end metric 为准。

## 7. Candidate recipe v1（Step 4a-D 前冻结）

### 7.1 输入—动作—输出

**输入**：

- 当前与过去 causal window 内的 known pilot labels `x_i` 与 Ch4 后接收 symbols `z_i,p`；
- 固定 `(8,8)-16APSK` ring/angle/labeling identity；
- `G_eff` 与已验证的 post-equalization noise metadata；
- 固定 window/forgetting、pilot count 与 update schedule。

**动作**：

1. 所有方法共用同一个 receiver-visible centroid/residual estimator，得到 `e_i,p=z_i,p-μ̂_{k,p}`。
2. 用 `R(-θ_k)` 将 residual 旋转到 radial/tangential frame。
3. 计算 point-local diagonal second moments `D̂_{k,p}`。
4. 由同 ring 各点的 pilots 构造 ring target；跨偏振只共享 target strength/收缩强度，默认不直接混合两 tributary 的瞬时 residual samples。
5. 采用冻结的解析 shrinkage 规则

\[
\widetilde D_{k,p}=(1-\lambda_{k,p})\widehat D_{k,p}
+\lambda_{k,p}T_{r(k),p},\qquad 0\le\lambda_{k,p}\le1,
\]

并对 eigenvalues 使用所有 full/structured comparator 共享的 numerical floor `ε`。
6. 旋回 I/Q 得到 `Σ̃_{k,p}`，与所有 covariance-aware 方法共用同一 Mahalanobis/log-det bit-LLR 与 LDPC decoder。

**输出**：每点、每 polarization 的正定 structured covariance 与 bit LLR；不输出或使用 hidden channel/noise truth。

### 7.2 Receiver-visible firewall

允许：known pilots、当前/过去接收 pilot samples、固定 constellation geometry、运行时 Ch4 metadata、冻结超参数。
禁止：payload transmitted labels、真实 channel/Jones、真实 noise realization/covariance、未来 frame、用 evaluation BER/FER 选择 `λ`/window、跨 evaluation window 回看调参。

`λ`、cross-pol strength-sharing 系数、window 与 `ε` 可在独立 development slice 调参并冻结；不得按 test cell 用 truth 或最终指标重选。

## 8. 公平 comparator 合同

所有 comparator 必须共享：pilot positions/counts、causal window、centroid estimator、update rate、development tuning budget、numerical PD floor family、LLR max-log/exact-sum实现、BICM mapping、LDPC code/iterations、paired samples 与 evaluation cells。

| ID | comparator | 角色 |
|---|---|---|
| B0 | global isotropic scalar covariance | 最低 conventional anchor |
| B1 | per-ring scalar covariance | 使用相同 ring identity 的廉价 scalar baseline |
| B2 | hard-pooled per-ring radial/tangential covariance | **strongest cheap comparator**；检验 local shrinkage 是否必要 |
| B3 | Layton per-point unstructured full covariance + task-matched generic shrinkage/floor | 最强直接 conventional comparator；不能故意保留 singular raw 实现当稻草人 |
| C1 | candidate v1 hierarchical structured shrinkage | 待检验方法 |

raw unbiased Layton full covariance 可作为诊断曲线，但 B3 才是 Go 对手。candidate v1 同时必须胜过 B2 与 B3 中较强者，不能只胜 B0/B1。

## 9. 最小消融与预期方向

### 9.1 最小消融

1. `C1 - local`：令 `λ=1`，退化为 B2，检验 point-local adaptivity。
2. `C1 - ring pooling`：只保留 point-local R/T + floor，检验同环 pooling。
3. `C1 - cross-pol sharing`：两个 tributary 完全独立估计收缩强度，检验跨偏振统计共享。
4. `C1 - R/T`：改为 B3 的 unstructured full generic shrinkage，检验几何结构。
5. `C1 scalarized`：令 `v_r=v_t`，检验 anisotropy 是否真正承重。

### 9.2 预期方向

- very-low pilot：B3 方差/condition 风险最大；B2 最稳；C1 只有在“存在 point dependence 且可被收缩保留”时才应胜 B2。
- pilot 增多：B3 逐渐追平 oracle；C1 增益应缩小，若结构 bias 存在可能反转。
- thermal-noise/isotropic：B0/B1/B2 已足够，C1 不应声称收益。
- anisotropic/data-dependent residual：C1 应先改善 GMI，再可能转化为 BER/FER。
- polarization statistics 不一致：关闭 cross-pol sharing 应更好；若相反，sharing 只作低频超参数共享，不升级成样本同分布假设。

## 10. Pre-MVE Kill/Pivot 条件

### `KILL_BEFORE_MVE`

满足任一即不进入完整 MVE：

1. 无法冻结 receiver-visible 的 pilot/sample/update contract，或 comparator 无法取得相同 pilot 与 tuning budget。
2. oracle radial/tangential 相对 oracle unstructured 的 bias 已使 GMI/FER 更差，且不存在 bounded operating slice。
3. oracle structured 相对 B2 strongest cheap comparator 在全部授权 cells 的 required-SNR headroom均 `<0.5 dB`。
4. post-Ch4 residual 在授权 cells 中对 scalar 假设无可检测偏离，且 B0/B1 与 covariance oracle 的 GMI/FER 差距 `<5%`。

### `PIVOT`

1. B2 获得 C1 相对 B0/B3 的 ≥95% end-to-end 改善、C1 增量 <5%：Pivot 到 hard-pooled per-ring R/T recipe。
2. generic unstructured shrinkage B3 胜 C1：Pivot 到 generic shrinkage implementation/complexity framing，不再承重 APSK geometry。
3. cross-pol sharing 单独造成退化：删除跨偏振项，保留 per-polarization ring shrinkage。
4. GMI 改善但 FER 不改善：只可降为 demapper-quality/supporting result，不得作为 Ch5 主方法章。

## 11. 本包结论

`Q-C5-1` 的纸面问题结构、竞争维度、结构机制与有限 claim 均可进入下一门，因此 verdict 为 **`PAPER_DIMENSIONS_PASS`**。candidate v1 已冻结为无需复杂学习的 receiver-visible hierarchical structured shrinkage estimator；B2 hard-pooled per-ring radial/tangential covariance 是 strongest cheap comparator，B3 Layton+generic shrinkage 是最强直接 conventional comparator。

本包没有作 Go。唯一剩余 blocker 是维度 D 的同预算 oracle/headroom 证据；在主控明确授权前，不实现、不 smoke、不运行实验。
