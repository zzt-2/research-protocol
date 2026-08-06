# Step 3.5 joint-estimator method priors acquire→read

> 日期：2026-08-06
> 任务：T010
> 范围：两篇 must-read 方法先例的有界合法 acquisition 与全文 action-contract 核验；不改 canonical，不进入 Step 4a/实现/仿真，不提交。

## Acquisition receipts

`tools/download` / `tools/blit` Bash wrapper 在当前 Windows worktree 因 CRLF 解析失败；未修改工具文件，改为调用 wrapper 实际指向的 `tools/paper_download.py`、`tools/blit.py` 与 `tools/pdf_convert.py`。这是等价入口偏差，所有命令均从项目根目录执行。

| DOI | bounded attempts | source/content | title gate | SHA / lines | acquisition verdict |
|---|---|---|---|---|---|
| `10.1109/JLT.2020.3042546` | preflight DOI dry-run PASS；1 OA/Unpaywall DOI downloader=`all_failed`；2 official arXiv exact-title query HTTP 200/0 entries；3 IEEE exact-title search 命中 doc `9281306`，blit 成功落盘 PDF（随后 console 因 GBK 无法打印 `✅` 报错，不影响文件），项目 converter PASS | `papers/doi/10.1109_jlt.2020.3042546/source.pdf` + `content.md`；原始 blit 副本保留于 `papers/downloads/2026-08-06/9281306.*` | 正文 H1 与派遣标题 exact match，overlap=`1.0` | PDF `2E64520B...B82B07`；content `6A0C5A20...B84731`；712 行 | `ACQUIRED_FULLTEXT_PASS` |
| `10.1007/s11082-024-06850-5` | preflight DOI dry-run PASS；1 OA/Unpaywall DOI downloader=`all_failed`；2 official arXiv exact-title query HTTP 200/0 entries；3 IEEE/CNKI applicability=`NOT_APPLICABLE_NOT_RUN`（Springer/OQE 不在 blit source contract） | DOI 目录只有失败 `metadata.json`，无 source/content | 无全文，不执行伪 title gate | metadata SHA256 `4DA354F3E249136496214F385E6955F533724092E7049216C8986307F758B487`；lines=N/A | `FULLTEXT_UNAVAILABLE_STOPPED` |

两篇均未使用 ResearchGate、Google Scholar 页面、publisher paywall 绕过或 web-reader 全文抓取。Springer 项已按适用路径止损，不空等、不用摘要冒充正文。

## Paper 1 action contract — Du et al., JLT 2021

| information | objective/search | output | frame output? | waveform/task fit | Q1 collision/delta | evidence lines |
|---|---|---|---|---|---|---|
| 已去 CP 的一个 `N`-sample CO-OFDM symbol interval；两个 receiver-known identical pilot symbols | joint likelihood `p(r|tau,epsilon,theta)` | TO/CFO/CPO | **否**；输入已假定 symbol interval/CP boundary 可用 | CO-OFDM、CP、subcarriers、circular sample offset；非 RRC single-carrier | true-joint statistical formulation 是 method prior；不占 `(frame,tau,CFO)` | `content.md:65-73,91,115-125` |
| `LN`-DFT 的 `L` 个 CFO-hypothesis spectra | 每 branch joint TO/CPO single-sinusoid ML；Euclidean/MF metric 选 branch | coupled `(tau,epsilon,theta)` | 否 | 依赖 known OFDM spectrum/DFT replicas | 证明“真正 joint `(tau,CFO,CPO)`”先例存在；Q1 禁称 generic first | `content.md:131-231` |
| coarse joint branch | secant CFO fine search，随后重算 TO/CPO | refined CFO/TO/CPO | 否 | `tau` 被正文称为 integer sample offset | coarse-to-fine 结构可迁移；fractional RRC timing 尚未被占 | `content.md:289-293,331-349` |
| amplitude-only spectra | blind CFO statistic，随后 joint TO/CPO | sequential CFO→TO/CPO | 否 | 同一 OFDM model | 给 error-propagation/complexity trade-off 邻近对照；不证明 Q1 A 成立 | `content.md:353-379` |

**全文 exact-action verdict**：`TRUE_JOINT_TAU_CFO_CPO_METHOD_PRIOR__NO_EXACT_Q1_COLLISION`。

理由：正文明确 joint maximize `(tau,epsilon,theta)`，所以 positive true-joint verdict 有全文支持；但其 observation 已是 CP-removed 单个 OFDM symbol，`tau` 为 circular integer-sample TO，且输出不含 frame index。它既不是 raw RRC single-carrier burst acquisition，也不是 coherent FSO turbulence task。Q1 只能声称更窄的 exact action/information delta，不能声称首次 joint timing/CFO estimation。

## Paper 2 action contract — OQE 2024 ConvNN/CapNN

| information | objective/search | output | frame output? | waveform/task fit | Q1 collision/delta | evidence |
|---|---|---|---|---|---|---|
| 本地索引摘要只筛到 QNSC CO-OFDM preamble/context | **UNRESOLVED_FULLTEXT_UNAVAILABLE** | 摘要声称 timing/frequency synchronization，但 target definition、loss、label granularity、jointness 均未全文核验 | 摘要未显示 frame；**不能据此作 negative proof** | 摘要级仅知 QNSC CO-OFDM，非 Q1 RRC single-carrier FSO | 只能保留 neural method-prior blocker；不得判 true joint，也不得判 exact collision | 无全文；acquisition receipt 如上 |

**exact-action verdict**：`UNRESOLVED_FULLTEXT_UNAVAILABLE`。摘要中的 “joint synchronization” 不能替代正文对 information、objective/loss、output 与处理顺序的核验，因此不创建伪 read note、不追加 read-log。

## Generic reuse vs sequential vs true joint

| class | 判据 | 本批结论 |
|---|---|---|
| shared-resource reuse | 同一 pilot/preamble 被多个可分离模块读取 | JLT 2021 不是仅此类；OQE 2024 无全文不可裁 |
| sequential | 前一估计/补偿后再估下一量 | JLT 2021 明确给出 CFO→joint TO/CPO 的 sequential alternative |
| true joint | 单一 likelihood/objective/search 同时耦合多个参数 | JLT 2021 **PASS for `(tau,CFO,CPO)`**；但不含 frame，且 information/task 不同 |

## Global read notes / read-log

- 新建：`papers/_read_notes/10.1109_jlt.2020.3042546.md`
- 更新：`projects/thesis-fso/read-log.md` 中既有 JLT 行，重读次数 `0→1`，补充 Q1 Step 3.5 用途与 IEEE doc ID。
- 修正 acquisition index：`papers/index.json` 中该 DOI 从 failed metadata entry 更新为 canonical `success` + title match。
- OQE 2024 无全文：不创建 read note，不追加 read-log。

## Blockers and claim ceiling

1. `10.1007/s11082-024-06850-5` 在两条适用合法路径失败且无适用 blit source，保持 `FULLTEXT_UNAVAILABLE_STOPPED`；其 network input encoding、loss、label、frame output 和是否真正 end-to-end joint 全部未决。
2. JLT 2021 已闭合为真正 joint `(tau,CFO,CPO)` method prior，但不是同信息、同动作、同任务 competitor。
3. 当前 claim ceiling：可以说“JLT 2021 已占 generic joint timing/CFO/CPO estimator prior”；不能说“Q1 exact `(frame,fractional tau,CFO)` collision 已发生”，也不能说 OQE 2024 已证明或排除 collision。
4. 未修改 canonical decisions/topic/master/literature notes，未进入 Step 4a、代码、testbed、MVE 或仿真，未提交。
