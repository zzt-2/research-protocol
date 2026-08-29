# Ch4 scaled-unitary 偏振解复用写作包

> 状态：`CH4_WRITE_PACKAGE_REVIEW_PENDING`
> 用途：硕士论文作者/导师的内部章级材料；`venue=N/A`
> 正式方法名：**基于缩放酉约束的短导频偏振信道估计与解复用方法**

本包把已经由 D052/V027 冻结为 `THESIS_METHOD_READY` 的证据整理为可追溯的写作输入。它不是正式论文正文，也不表示完整论文实验已经完成。核心动作是：由双偏振短平衡导频得到 2×2 pilot-LS 估计，对其做 SVD，并投影到 `g>0, Q∈U(2)` 的缩放酉集合，随后用投影矩阵的逆完成偏振解复用，再把两路输出交给 Ch3 CPR。

## 文件导航

- `fact-matrix.md`：事实、数字、公式、实现和允许主张的一一映射。
- `chapter-blueprint.md`：按章写作顺序组织的三级标题、承重句和证据入口。
- `algorithm-box.md`：可直接据此排版的算法框与复杂度边界。
- `claim-and-citation-ledger.md`：允许/必须披露/禁止主张以及引用候选。
- `data/ch4-confirmation-summary.csv`：从 confirmation raw 独立派生的四格及 pooled Np=2 统计。
- `plot_ch4_results.py`：raw-only reducer、V027 锚点检查与结果图生成器。
- `method-figure-semantic-brief.md`：方法图冻结标签、箭头和视觉编码。
- `generate_method_figure.py`：可重复生成方法 SVG 与 PNG preview。
- `figures/ch4-ber-comparison.{svg,png}`：四格 confirmation 结果图。
- `figures/ch4-method-flow.{svg,png}`：双偏振导频估计—解复用—Ch3 CPR 方法图。
- `verification.md`：生成命令、逐值核验、视觉 QA 与独立审查结论。

## 权威源

1. `.sessions/2026-07-09-thesis-writing/decisions.md` 的 D052。
2. `.sessions/2026-07-09-thesis-writing/verifications.md` 的 V027。
3. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/confirmation_raw.json`。
4. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/scaled_unitary.py` 与 `development.py`。
5. `projects/thesis-fso/polarization-demux-groundwork/step4a-c4-1-paper-feasibility.md`、`step4a-c4-1-fresh-confirmation.md`。

## 仍未覆盖

- 未验证 PDL、PMD、FIR、支路不平衡、非等噪声、时变 SOP、CFO、CPR 联合效应或 LDPC 全链。
- 本包未定义 near-unitary 运行时阈值，也没有把 `rho=s1/s2` 用作自适应分支。
- 未做第二次 confirmation、扩 SNR/pilot 网格或与近期强方法的全面横向比较。
- O1 仅为离线 oracle；不可描述为可部署接收机。
