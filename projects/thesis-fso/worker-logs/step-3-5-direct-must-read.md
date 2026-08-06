# Worker Log: Step 3.5 direct must-read acquire -> read

> 2026-08-06 | 执行 T009 | 不改 canonical、不进 Step 4a/实现/仿真、不提交

## 范围与纪律

- 只核验 `10.1109/JLT.2025.3581618` 与 `10.1109/LPT.2017.2759584`（arXiv `1801.01598`）。
- exact-action verdict 仅来自成功取得的全文；摘要只可描述 blocker，不能裁碰撞。
- `tools/download` bash wrapper 在当前 Windows checkout 因 CRLF 直接报错；未修改工具文件，改用 wrapper 指向的等价底层 `~/.venvs/torch/bin/python tools/paper_download.py`。该运行方式仍走项目既有合法 acquisition pipeline。

## Acquisition receipts

### A. JLT 2025 — DOI `10.1109/JLT.2025.3581618`

| path | command/evidence | result |
|---|---|---|
| dry-run | `paper_download.py --doi 10.1109/JLT.2025.3581618 --dry-run` | planned canonical dir `papers/doi/10.1109_jlt.2025.3581618/` |
| 1. DOI/OA/Unpaywall pipeline | `paper_download.py --doi 10.1109/JLT.2025.3581618` | `FAIL all_failed`; failed receipt in `metadata.json` |
| 2. arXiv title lookup | official arXiv API exact-title query | `totalResults=0`; no arXiv ID/public manuscript found |
| 3. IEEE blit | exact title, `--source ieee --max 1 --download papers/doi/10.1109_jlt.2025.3581618` | bounded command timed out after 94 s; no PDF/content written |

- canonical directory contains only the failed `metadata.json`; no `source.pdf`/`content.md`。
- **blocker**：`PRIMARY_FULLTEXT_UNAVAILABLE_AFTER_THREE_PATHS`。
- **exact-action verdict**：`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`。摘要称同一 TS 同时支持 frame detection、timing recovery、FOE、SOP、IQ-skew，但不能由此判断是否单一 objective，也不能判断 timing 是否 fractional sample-level `tau`。
- 按止损纪律：不创建 read note、不追加 read-log、不把摘要写成 collision/no-collision。

### B. LPT 2017 — DOI `10.1109/LPT.2017.2759584`, arXiv `1801.01598`

| path | command/evidence | result |
|---|---|---|
| dry-run | DOI 与 arXiv 均预览 | canonical arXiv dir=`papers/arxiv/1801.01598/` |
| 1. official arXiv | `paper_download.py --arxiv 1801.01598` | `OK arxiv_pdf`; `source.pdf` + `content.md` |

- title：正文 H2 与派遣标题完全一致，人工 overlap=`1.0`；自动 `unverifiable` 已人工关闭。
- quality：`content.md` **156 行**；SHA256=`5e4d78323b260421fe15f22a7e62b230b324eb138c737611832aad23ced9aae7`；PDF SHA256=`5fd93abcd89fddf5429b20a32c73dacd5c36a9959031f069ae7c95d918404b89`。
- read note：`papers/_read_notes/1801.01598.md`。
- read-log：`projects/thesis-fso/read-log.md` 已追加 `1801.01598`。

## Fulltext action contract — LPT 2017

| axis | verdict | fulltext evidence |
|---|---|---|
| information | 两条 receiver-known chirps，共同形成两项 peak-shift equations | `content.md:49-83` |
| action | 对两条 chirp 分别算 FRFT fractional-correlation peak，再解一个 2x2 time/frequency coupling system | `content.md:37-83` |
| output | integer/symbol-domain frame offset `mu_hat` + CFO `gamma_hat` | `content.md:79-83` |
| timing | matched RRC/CD 后先 downsample 到 **1 sps**，再 joint sync | `content.md:95-99` |
| formula/metric | Eq. (6)-(13)：`R_ib(u)` -> peak shifts -> `Delta n_i=Delta t cos(phi_i)+Delta f sin(phi_i)` -> `mu_hat,gamma_hat` | `content.md:37-83`; `source.pdf` 公式复核 |
| jointness | 真 joint `(integer frame offset, CFO)`；不是顺序独立估计 | 同上 |
| fractional tau | **不存在**；`round(Delta t)` 且算法入口已 1 sps | `content.md:79-83,95-99` |

## 两篇 verdict

1. **JLT 2025**：`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`。三路径止损；摘要不得裁 exact action。
2. **LPT 2017**：`NO_EXACT_Q1_COLLISION_STRONG_NEIGHBOR`。它是真正 joint `(integer frame offset, CFO)` FRFT solver，但不输出 fractional `tau`，并且在 1-sps 下工作；故不是单一 objective 输出 `(frame index, fractional tau, CFO)` 的 exact collision。

## Q1 影响（不改 canonical）

- LPT 2017 占用“known chirps + coupled time/frequency metric 联合解 frame/CFO”的方法先例，必须作为 Q1 method prior/strong neighbor 处理。
- 它没有关闭 Q1 的 sample-level fractional timing 维度；不能据此宣称 Q1 新颖性，也不能据此 Kill/Go。
- JLT 2025 仍是全文 blocker；本 worker 不改变 canonical terminal、Q1 survivor 或 claim ceiling。

## 边界验证

- 未修改 canonical topic/session/master/literature notes。
- 未修改代码、`common/`、`params.py`、旧实验与 `p05_run*.log`。
- 未进入 Step 4a、方法实现、testbed、MVE 或仿真；未提交、未 push。
