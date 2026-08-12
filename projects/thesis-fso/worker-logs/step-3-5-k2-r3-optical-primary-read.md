# K2 Step 3.5 Round 3：两篇 optical primary fulltext 动作核验

> 2026-08-12 | 范围：只做两篇 MUST 全文获取、title gate、动作合同与 Q001 collision ceiling；不改中央 owner/session，不进入 Step 4a/实现/仿真/Go/METHOD_SIGNAL。

## 1. 获取与身份回执

| DOI | 合法路径（每篇≤2） | canonical | title gate | receipt |
|---|---|---|---|---|
| `10.1109/WCNC57260.2024.10570836` | (1) `tools/download --doi`=`all_failed`；(2) `tools/blit --source ieee --download` 机构访问成功（CLI 最终因 Windows GBK 打印符号报错，但 PDF 已完整落盘） | `papers/doi/10.1109_wcnc57260.2024.10570836/source.pdf`, `content.md` | PASS，token overlap `0.636` | PDF SHA256 `B5B7FAA9EC5E8054E0263488D8DA93516508F135033D9156A33FBB8CD80456B8`；246 行 markdown |
| `10.1016/j.optcom.2024.130326` | (1) 既有 DOI/OA/Unpaywall=`all_failed`；(2) Warwick Research Archive 官方仓储 CC BY 4.0 published PDF | `papers/doi/10.1016_j.optcom.2024.130326/source.pdf`, `content.md` | PASS（自动器先抓 journal banner；跳过 `Optics Communications` 后正文 H2 与派遣标题逐字匹配） | PDF SHA256 `B92C30F4D31C29AB5BD1E7342FEAF47FA8D541708B776E6817571B63A035B0F1`；551 行 markdown |

两篇均为 `FULLTEXT_READ`，没有 abstract-only 判定或 UNRESOLVED 债。

## 2. Wang et al., WCNC 2024 — 完整动作合同

一手定位：signal/Wiener/AOPN model `content.md:33-63`；joint ML/MAP 与 iterative implementation `:65-125`；genie unwrap `:127-139`；结果与 benchmark ceiling `:147-205`。

| 轴 | 全文事实 |
|---|---|
| input | `N` 个 MPSK 复样值，每符号 1 sample；使用幅度 `|r(k)|` 与 `M` 次幂相位 `arg(r(k)^M/|r(k)|^M)/M`。decoder-free，但不是 single-tone residual-CFO model。 |
| state/model | 未知常量初相 `θ0` + 长度 `N` 的 Wiener random-walk phase vector `θ`；AWGN-induced AOPN 的对角协方差由接收幅度近似，Wiener covariance 由已知 `σp²` 给定。 |
| hypotheses | 无离散 wrap trajectory bank；`H=1`。正文的 `M` 个相位歧义结果没有并行保留，而由 genie truth 立即解除。 |
| score | `θ0` 用 Gaussian marginal likelihood 的二次型 ML；`θ` 用 conditional-Gaussian posterior mean/MAP。 |
| merge/prune | 无。 |
| lag/commit | 对当前 `N` 样本块联合估计 `θ0` 与整条 `θ[0:N-1]`；新增样本时递推更新并可重估整个向量。没有 fixed-lag irrevocable commit。 |
| trigger/fallback/reset | 无 receiver-visible trigger、fallback 或 reset。unwrap 使用真实 `(θ0+θ(k))` 的 genie-aided 区间 `±π/M`；论文明确结果仅是 ideal-unwrapping benchmark。 |
| causality | 块式/增长前缀估计；对块内第 `k` 个输出依赖同块后续样本，非固定时延 causal commit。递推式按新样本增长，但历史向量仍被联合重估。 |
| output | `θ0` ML、整条 Wiener PN `θ` MAP、补偿后的 MPSK 判决/BER；不输出 integer-wrap sequence、confidence 或 fallback flag。 |
| dependencies | 已知 `M`, `σp²`, `N0`/AOPN 模型；高 SNR 下以 `|r(k)|` 近似未知振幅；承重 unwrap 依赖不可部署的真实相位 genie。无 residual CFO state。 |
| ops/memory/worst latency | Schur complement 递推避免每步显式矩阵求逆，正文称只需 scalar operations；没有给每符号精确 op count。状态/协方差及整条 phase-vector 随 `N` 增长，fixed memory 与最坏 latency 未界定。 |
| task | MPSK 下 time-varying Wiener PN 的 joint initial-phase/PN estimation；只说适用于 optical，仿真为 QPSK/8PSK AWGN+Wiener，不是 coherent-FSO residual-CFO task。 |

**Q001 分类：`STRONG_NEIGHBOR / ORACLE_UNWRAP_REFERENCE`，非 exact collision。** 它加强 C01 同族 reference/accuracy ceiling，并直接证明 “Mth-power + Wiener ML/MAP” 仍把 unwrap 当外部承重前处理；但没有 Q001 的 explicit bounded integer-wrap hypotheses、receiver-only branch likelihood/merge-prune、fixed-lag commit、fixed memory/worst latency、confidence/fallback 和 unwrapped-sequence output。

**显式 trivial deletion/truncation test：FAIL（不是 Q001 的简单删减版）。** 若只删除其 full-vector ML/MAP、把 `N` 截短或只留 3 个状态，都不会得到离散 `2π` wrap trajectory bank；若把 genie unwrap 删除，算法输入合同反而断裂。要成为 Q001 必须新增 deployable branch generation/score/merge-prune/fixed-lag commit/fallback，而不是删除已有模块。反方向上，Q001 后接 Wang ML/MAP 可复用本文 estimator，但这只是 downstream reference reuse，不是 action equivalence。

## 3. Zhang et al., Optics Communications 2024 — 完整动作合同

一手定位：Wiener model `content.md:66-78`；MVV 三步动作 `:80-132`；receiver placement `:134-166`；comparators/complexity `:228-312`；practical variant `:314-358`。

| 轴 | 全文事实 |
|---|---|
| input | CD compensation 后的 coherent DP-64QAM（并扩到 DP-256/1024QAM）复符号；receiver ADC 为 2 samples/symbol。ring classification 使用 symbol amplitude；不是 decoder-free single-tone sufficient statistic。 |
| state/model | centered CPR sliding window；laser PN 建模为 Wiener process。默认 CPR length 61（`2N+1`, 即 `N=30` lookahead），现实失真例使用 101；没有 residual-CFO state，主仿真默认忽略 frequency offset/PMD。 |
| hypotheses | 每个非标准 QPSK-ring 符号构造 `+θn/-θn` 两个 constellation-orientation candidates（Ring 6 另含原方向）；它们是每符号调制去除方向，不是跨时间 `2π` wrap trajectories。 |
| score | 以窗口内标准 QPSK points 的 normalized fourth-power mean 为 reference；计算候选与 reference 的 complex modulus distance，并以 `Thr_fil` 过滤错误旋转。阈值具体值/调参规则正文未冻结。 |
| merge/prune | 只有 per-symbol candidate filtering/exclusion；无 trajectory merge、跨时刻 survivor score 或 bounded branch bank。 |
| lag/commit | 对 `2N+1` centered window 求 fourth-power average，输出中心 symbol phase estimate；等价固定 lookahead `N`，但没有 hypothesis commit 语义。随后使用普通 phase unwrapping，细节仅引用他文。 |
| trigger/fallback/reset | 无 ambiguity/reliability trigger、no-valid flag、fallback 或 reset；错误旋转候选按阈值过滤，若 reference/candidate 都不可靠时正文没有处置合同。 |
| causality | centered window 明确依赖未来 `N` symbols，故非零-lookahead；可流式滑窗实现，但不是 causal lag-0，亦无 worst-latency contract。 |
| output | 每 symbol laser phase estimate `φ(n)=1/4 angle(sum Y(n+k)^4)`，unwrap 后补偿符号/BER；无显式 integer-wrap sequence、confidence/fallback flag。 |
| dependencies | 高阶 square-QAM 几何、9 rings/8 amplitude thresholds、已知 rotation offsets、窗口内至少有可信 `X_QPSK` reference、phase 在短 CPR window 连续。系统为 fiber WDM，含 ASE/EEPN/Kerr；不等于 FSO fading。 |
| ops/memory/worst latency | Table 2：MVV=`7M+B` per processed symbol（`M`=one complex multiply cost, `B`=one block update）；比 VV 的 `16/3 M+B` 稍高、低于 VV&RA/VV&CT 的 `37/3 M+2B`。需 `2N+1` window buffer；没有 hardware-specific `B`、memory bytes 或 worst latency。 |
| task | 高阶 coherent optical-fiber QAM laser PN/EEPN CPR，核心是让全部 constellation points 经 ring/rotation 参与 VV averaging；不是 single-tone MPSK residual CFO + wrap-suffix pollution task。 |

**Q001 分类：`CHEAP_ESTIMATOR_CHANGING_NEIGHBOR`，非 exact collision。** 它占用“有限候选 + receiver-visible distance + 过滤 + fixed centered window”几个动作原子，也提供强 optical cheap comparator/复杂度锚；但候选语义、状态、score 累积、commit、输出、输入任务均不同，且其 unwrap 本身未给算法合同。

**显式 trivial deletion/truncation test：FAIL。** 删除 9-ring/rotation/filtering 只会退化为普通 VV/window averaging；把每符号 `±θn` 候选截为 `H≤3` 仍不产生 temporal integer-wrap trajectories、path likelihood、merge/prune 或 fixed-lag commit。要得到 Q001 必须替换 candidate semantics，并新增跨时状态与 fallback/output contract。因此 Q001 不是 MVV 的简单删减/截断；MVV 只能作为 estimator-changing cheap neighbor。

## 4. 合并裁决与 claim ceiling

1. 两篇全文均 **没有确认 Q001 完整 exact action**。
2. WCNC 2024 把 C01 estimator family 延伸到 MPSK 数据去除，但其 genie unwrap 是关键不可部署依赖；合法 claim 仅为 `ORACLE_UNWRAP_REFERENCE/accuracy benchmark`。
3. Optics Communications 2024 的 finite per-symbol rotation candidates 不能改写成 finite temporal wrap hypotheses；合法 claim 仅为 `CHEAP_ESTIMATOR_CHANGING_NEIGHBOR`。
4. 这两篇不证明 coherent-FSO defect occurrence/headroom，也不授权 Q001 novelty、Go、方法或 Step 4a。

`terminal = PAIR_FULLTEXT_READ_NO_EXACT_Q001_COLLISION`
