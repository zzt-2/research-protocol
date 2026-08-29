# Ch5 post-Ch3/post-Ch4 residual authority audit

> T055 | 2026-08-30 | bounded read-only authority audit
> task-control validator: `PASS`
> 总裁决：`NO_AUTHORIZED_TARGET_RESIDUAL`

## 1. Findings first

1. **现有 artifact 中没有可直接进入 Ch5 target-platform headroom 的 post-Ch3/post-Ch4 residual。** Ch3 正式 runner 在内存中生成 carrier-corrected `selected_rx`，但正式 JSON 只保存 `selected_output_sha256`、BER/error counts、branch counts 与 realization identity；没有保存 known-pilot residual、residual phase error、cycle-slip-free jitter、每点/每环 covariance 或 sample count。因而不能从现有结果恢复 Ch5 所需的 `e_{i,p}=z_{i,p}-\hat\mu_{k,p}`。
2. **当前共同平台的主动默认 cell 是 circular control，不是 target residual。** single-tap unitary Jones 与 equal-variance circular white noise 经 exact `J^H`/正确 demux 后保持噪声协方差不变；该 cell 合法用于证明 scalar/per-ring scalar 退化关系，但不能诚实制造 radial/tangential headroom。
3. **Ch4 当前只有公式级和接口级 authority，没有 post-Ch4 residual 数字。** T052 明确写明 LS-only residual 的数值大小未知；当前目录也没有 Q-C4-2 的实现/result artifact。因此 `z/G_eff/Sigma_n/flags` 是冻结接口，不是已观测 residual distribution。
4. **receiver filter/IQ-skew/PDL/PMD 不能作为后备填空。** 最终 analogue/electrical filter 与 FIR span 仍为 UNKNOWN；IQ 模型结构虽有 authority，数值仅绑定 square-QAM conditional stress；PMD/CD/DGD 被明确排除出星地共同平台。旧 Pilot-Jones 强信号又被后续 temporal audit 追到无来源的 per-block Jones redraw，固定 component 后 impairment-added headroom 最大点估计仅 `0.080 dB`、95% CI 上界 `0.237 dB`。
5. **唯一值得保留的首选候选 cell 尚未获授权。** 它是“Ch3 branch-selected CPR 输出经过 Ch4 后，在已知 pilot 位置形成的 per-polarization、per-APSK-point residual”，而不是 synthetic anisotropy。它已有生成链零件和 receiver-visible 标签，但缺 post-Ch4 residual artifact 与 natural anisotropy/covariance 观测，所以本报告不能把它升级为 `CONDITIONAL` 或 `AUTHORIZED`。

## 2. 已核证据与 authority

| 对象/字段 | 事实 | 证据指针 | authority / 本裁决用途 |
|---|---|---|---|
| foreground authorization | CP007 允许 `LOCAL_PARAMETER_AUTHORITY_AUDIT`，禁止 performance grid/scientific experiment | `.sessions/2026-07-09-thesis-writing/topic-index.md:13-25,35-38`; `.sessions/2026-07-09-thesis-writing/T055-ch5-postch4-residual-authority-audit.md:6-27` | task-control validator `PASS`；只授权本报告 |
| 共同平台主模型 | `y=a e^{jθ}Jx+n`，`J^H J=I`；默认 memoryless single-tap unitary Jones | `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:33-55,110-117` | `SUPPORTED_ACTIVE/SUPPORTED_FIXED` |
| circular-control noise | equal-branch independent circular white noise；unitary mixing 前后 covariance 不变 | `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:131-152` | 合法 control；不构成 R/T target |
| Ch4→Ch5 接口 | `z[k,pol]`, `G_eff`, `Sigma_n`, `sample_phase`, `impairment_flags`, constellation/labeling；Ch5 不重新注入损伤 | `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:169-182` | 接口 authority；不是 residual observation |
| 平台 UNKNOWN | branch 实测 covariance、final filter transfer function/FIR span、APSK CPR 参数均未闭合 | `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:184-202` | filter/FIR target blocking；禁止凭经验补值 |
| Ch3 信道相位 | GG realization 保存 `phi`; 相位含 residual CFO/ramp 与 Wiener laser PN | `projects/simulation/common/_channel.py:35-54,57-93` | generator authority；`phi` 是 truth，不能给 deployable Ch5 |
| Ch3 正式配置 | 2.5 GBaud、10 kHz linewidth；`sigma_laser^2=2πΔνT_s` | `projects/simulation/params.py:48-95,296-306` | 当前 Ch3 local config；linewidth 标为 `WARNING`，不得外推为共同 DP/coded platform 的已验证值 |
| Ch3 正式 grid | weak/moderate/strong，SNR `5:2:25 dB`，30 seeds，400×256-symbol windows，768 common bits/window | `projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py:12-18`; `projects/simulation/results/ccisp_family1_selector_a_30seed.json:17-58` | formal result scope；不自动成为 post-Ch4 cell |
| Ch3 carrier-corrected output | NDA/DA branches 返回 complex corrected sequence；runner 根据 branch command 选 `selected_rx` | `projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py:24-44`; `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_branchrouted_30seed.py:115-165` | 生成链零件存在；selected sequence 仅瞬时存在 |
| Ch3 持久化字段 | artifact 保存 hashes、errors、bits 与 branch counts；没有 residual/covariance field | `projects/simulation/results/ccisp_family1_selector_a_30seed.json:60-79`; `projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py:42-46` | **blocking evidence**：hash 不可反演 residual |
| Ch3 独立验证范围 | verifier 验证 A/B 等价和 BER/gain，未验证 residual covariance | `projects/simulation/results/ccisp_family1_independent_verification.json:1-20` | 证明现有验证口径不覆盖 Ch5 target |
| Ch4 LS/RDE 状态 | memoryless unitary/equal-white slice；LS residual 大小没有数字；输出接口已规定 | `projects/thesis-fso/apsk-front-end-groundwork/step4a-paper-feasibility.md:23-53,102-137` | paper authority only；无现成 post-Ch4 result |
| Ch5 target contract | runtime 只用 current/past known-pilot residual；target 必须比较 full/scalar/ring/R/T covariance，并由 GMI/FER 承重 | `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-paper-feasibility.md:33-43,90-109,154-164,205-247` | 规定本审计必须找到 natural residual，不能用 metadata 或 synthetic anisotropy 代替 |
| 旧 Jones/PDL/PMD 结果 | per-block Jones redraw 无来源；固定 component 后 max point/CI upper=`0.080/0.237 dB`，轴被 scoped Kill | `projects/thesis-fso/worker-logs/step-005-pilot-jones-temporal-semantics-adjudication.md:18-49` | 不得作为 backup target 或复活旧强信号 |

## 3. Circular-control 理论判断

设 Ch4 的合法最小 cell 为 `y=Jx+n`，其中 `J` unitary、`n~CN(0,σ²I)`，oracle/正确 demux 为 `z=J^H y=x+J^Hn`。于是

\[
\operatorname{Cov}(J^Hn)=J^H(\sigma^2 I)J=\sigma^2 I.
\]

对任意 APSK 点旋转到 radial/tangential frame，协方差仍为 scalar identity，所以 `σ_r²=σ_t²` 且 rotated off-diagonal 为零。有限 pilot-LS 的估计误差可以留下随机 demux error，但当前 authority 没有它的数值、point/ring 条件 covariance 或通过正确性的 Q-C4-2 artifact；仅凭“有限 pilot”不能把它宣称为 natural anisotropy。故该 cell 只能是 **circular null/control**。

## 4. Primary / backup cell

### 4.1 Primary（首选候选，但当前未授权）

**名称**：`Ch3-selected-CPR known-pilot residual after Ch4 demux`。

**完整生成链**：

`DP-(8,8)-16APSK known pilots/payload`
`→ authority-backed GG + Wiener phase/CFO realization`
`→ Ch3 receiver-visible branch selection and DA/NDA CPR`
`→ Ch4 common pilot-LS initialization + plain RDE / accepted Q-C4-2 output`
`→ ambiguity-aligned z[k,pol] at known pilot positions`
`→ e[k,pol]=z[k,pol]-x_pilot[k,pol]`
`→ group only by fixed constellation_id / point / ring / polarization`
`→ estimate radial/tangential/full/scalar covariance under an identical causal pilot budget`。

| 关键字段 | 当前 authority | 状态 |
|---|---|---|
| modulation/geometry | `(8,8)-16APSK` identity已冻结；具体 DP labeling 不能从平台六篇补造 | `SUPPORTED_PROJECT_IDENTITY`，需沿用同一 mapping |
| Ch3 phase generator | GG + CFO/ramp + Wiener PN 生成链存在 | `SUPPORTED_LOCAL_GENERATOR` |
| linewidth / symbol rate | 当前 Ch3 formal 为 `10 kHz / 2.5 GBaud`；共同平台另有 `100 kHz/laser / 32 GBaud` conditional point | **不得混写**；第一 cell 必须只选一个完整、带 hash 的配置 |
| branch-selected CPR output | `selected_rx` 在 runner 内存在 | `TRANSIENT_ONLY` |
| post-Ch4 `z[k,pol]` | 接口已定义 | `NO_RESULT_ARTIFACT` |
| known-pilot label | Ch3 DA/NDA runner 已有 pilot indices/symbols | `RECEIVER_VISIBLE` |
| ambiguity alignment | NDA path已有 resolve；DA path输出 carrier-corrected sequence | 必须在 residual receipt 明确是否/如何统一消歧，不能用 payload truth |
| residual units | complex baseband symbol units；R/T variance为归一化 symbol-energy² | `DERIVABLE_AFTER_OUTPUT_FREEZE`，现无 artifact |
| natural anisotropy / ring dependence | phase residual理论上可能表现为 tangential、随 ring energy变化 | `UNKNOWN`；不得作为既有事实 |
| sample counts / causal window | Ch5要求 current/past pilots、同预算 | `UNKNOWN`；现有 BER grid 的 400 windows 不能替代 per-point residual count |

**与 Ch3/Ch4 claim firewall**：Ch3 只承载“已有 branch-selected CPR 输出”，本 cell 不重新声称 CPR 增益；Ch4 只承载“产生共同 `z` 与 metadata”，本 cell 不把 RDE gate 的 BER 改善预设为事实；Ch5 只在 residual 已自然观测后比较 covariance estimators。不得用 `phi` truth 构造 deployable residual，不得把 Ch3 原单支路证据改写成 DP/coded/post-Ch4 验证。

### 4.2 Backup

**无合法 backup。**

- memoryless unitary Jones + equal-white noise 是 circular control；
- receiver filter/IQ-skew/FIR 缺共同 APSK 参数和 passing platform artifact；
- PDL/PMD/fiber stress 要么 conditional/unknown，要么明确 excluded/scoped killed；
- synthetic radial/tangential anisotropy 只允许 correctness identity，不是 target-platform cell。

## 5. UNKNOWN 与 blocking

| UNKNOWN | 是否阻塞 headroom | 原因 |
|---|---|---|
| post-Ch3 selected output 的可复算 complex samples | **是** | 现有 artifact 只有 SHA，无法计算 residual |
| post-Ch4 `z[k,pol]` 与 `Sigma_n/flags` receipt | **是** | Ch4 尚无当前 candidate result；接口不等于观测 |
| known-pilot residual 的 point/ring/pol sample counts | **是** | 无法判断 full covariance 的实际小样本缺陷 |
| `σ_r²-σ_t²`、rotated off-diagonal、scalar-gap | **是** | 未证明 target residual 偏离 circular control |
| final filter/FIR authority | 对本 primary 否；对 filter/IQ backup **是** | primary 明确保持 memoryless；backup 不能借 UNKNOWN 开启 |
| Ch3 `10 kHz/2.5 GBaud` 与共同平台 conditional `100 kHz/32 GBaud` 的选择 | **是** | 混合两套参数会制造不存在的 authority |

**唯一 blocker（归并）**：缺少一个带完整 config/hash、只含 receiver-visible 信息的 **post-Ch3 + post-Ch4 known-pilot residual artifact**，因此 natural covariance geometry 与实际 pilot sample budget均不可审计。

## 6. 最小下一动作（只描述，不派任务）

在不新增任何 impairment、不调参追求增益的前提下，为现有共同链增加一个只读 observation seam：持久化每个 known pilot 的 `cell/seed/window/pol/point/ring/branch/z/x_pilot/e`，同时记录 Ch3/Ch4/config SHA、pilot indices、ambiguity handling、`G_eff/Sigma_n/impairment_flags` 与每组 sample count。先只生成 circular-control receipt 和 primary candidate receipt；若 primary 中 `σ_r²-σ_t²`、rotated off-diagonal 或 covariance-aware oracle 相对 scalar control 均无可检测差距，则保持 Ch5 headroom 关闭。该动作是最小 testbed 改动，不需要 synthetic anisotropy；在获得新的正式授权前不得执行。

## 7. 最终裁决

`NO_AUTHORIZED_TARGET_RESIDUAL`

首选候选 cell 是 **Ch3 branch-selected CPR 后、再经 Ch4 输出的 known-pilot complex residual**，但当前仅有生成链零件，没有可审计 residual artifact，故仍不是 authorized cell。唯一 blocker 是 post-Ch3/post-Ch4 receiver-visible residual artifact 缺失。
