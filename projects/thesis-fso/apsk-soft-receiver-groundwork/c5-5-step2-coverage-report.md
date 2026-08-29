# C5-5 reliability-driven LDPC iteration budget — Groundwork Step 2 coverage

> T079｜2026-08-30｜起点 authority `9e80cccf9120d5de82cdf6c0ef6cf81cb4b5ab83`
> 范围：最多 3 篇的候选级 GW Step 2 acquisition；只冻结全文身份、质量、coverage 与 Step 3 read pool。

## 1. Facts-first 结果

```text
STEP2_C5_5_READY_FOR_STEP3
```

- task-control：CP020 / epoch 20 / `C5_5_GW_STEP2_BOUNDED_ACQUISITION`，validator=`PASS`。
- 搜索预算：调用 `2/4` 个聚焦 query；第一条完整返回，第二条在 CLI 汇总超时前已写出可解析 archive。没有 WebSearch/webReader。
- pool arithmetic：P0 尝试 `1` 篇 + P1 fresh acquisition `1` 篇 + 本地复用 comparator `1` 篇 = 审计 `3` 个对象；qualified=`2`，rejected identity mismatch=`1`。
- coverage：direct scheduling=`1`；可审 ordinary early-stop/maximum-iteration comparator=`1`；qualified fulltexts=`2/3`。
- P0 DOI `10.1109/ACCESS.2019.2899106` **未取得 canonical fulltext**。项目 downloader 将近似题名误配为 `arXiv:cs/0702111v2` 的 2007 论文，metadata 已给 `title_check=mismatch`、overlap=`0.3333333333`；该内容不计 qualified，也不得在 Step 3 当作 P0 阅读。
- 2025 RL-CBP 是动作等价的 recent primary substitute；因此满足 D058 的“P0 不可得时须有等价 primary substitute”条件。该替代只解除 Step 3 输入阻塞，不关闭 P0-specific provenance/exact-collision debt。

## 2. Acquisition ledger

| 对象 | canonical identity / 来源 | local fulltext 与质量 | 快速定位标签 | qualified |
|---|---|---|---|---|
| P0：Zhang & Chen, *Residual-Decaying-Based Informed Dynamic Scheduling for Belief-Propagation Decoding of LDPC Codes*, IEEE Access 2019, DOI `10.1109/ACCESS.2019.2899106` | T041 OpenAlex metadata 给正式 DOI、OA 与 IEEE PDF URL；单 DOI downloader=`all_failed`；T041 定向下载又误配到 `arXiv:cs/0702111v2` | `papers/doi/10.1109_access.2019.2899106/metadata.json`：expected title 与 real title 不同，`title_check=mismatch`；错误 source/content 经哈希留据后删除，防止污染 canonical cache | `REJECTED_IDENTITY_MISMATCH` | **NO** |
| Liu et al., *Reliability-List-Based Check-Belief Propagation Decoding of LDPC Codes*, IEICE Trans. Fundamentals, 2025, DOI `10.1587/transfun.2024eal2080` | OpenAlex metadata + J-STAGE OA PDF；downloader method=`oa_pdf` | `papers/doi/10.1587_transfun.2024eal2080/source.pdf`：PDF magic valid，5 pages，2,882,056 B；`content.md`：239 total / 100 effective lines；题名 overlap=`0.8888888889`；公式、调度步骤、仿真实验/结果段均存在 | `DIRECT_SCHEDULING` | **YES** |
| He et al., *Lowering the Error Floor of Quantized NR LDPC Decoders by a Post-Processing on Trapping Sets*, WCSP 2021, DOI `10.1109/WCSP52459.2021.9613326` | 已有 canonical metadata，title check=`match`、overlap=`1.0`；本轮本地复用，不重复下载 | `papers/doi/10.1109_wcsp52459.2021.9613326/content.md`：231 total / 122 effective lines；DOI、maximum iterations、CRC early stop、算法和 results 均可定位。legacy `source.pdf` 实为纯文本而非 PDF，页数不可由 PDF parser取得；这是 source-format debt，不影响现有 readable fulltext 身份 | `EARLY_STOP_COMPARATOR` | **YES_WITH_SOURCE_FORMAT_DEBT** |

### 2.1 Hash receipt

| 路径 | SHA-256 |
|---|---|
| `papers/doi/10.1587_transfun.2024eal2080/source.pdf` | `FAB2C2718D02544B9A1DDD55B0B0A2A5AEF3A7B504429F9C6C9BA0BC907F214E` |
| `papers/doi/10.1587_transfun.2024eal2080/content.md` | `ED0B33DF4531A0AD2CA92BF6CF420CECFC59D9EA7CA59514B141078375D79509` |
| `papers/doi/10.1109_wcsp52459.2021.9613326/content.md` | `D96B1A8BA3814DE96FF10FB2C330E2BAA53A0BFE00408F70956B4D65DB1F25B2` |
| rejected P0 content（已删除，哈希保存在 metadata） | `9105D56A9A7C7E0C4CA46F3E8AE5C1281834C442A5265859C09818C7FCEE3A4D` |

## 3. Coverage 与缺口

| 必需桶 | 覆盖对象 | 状态 | 本轮允许的结论 |
|---|---|---|---|
| direct scheduling | 2025 RL-CBP | `COVERED` | 有一篇 recent primary readable fulltext 可供 Step 3 审计；不在 Step 2 解释其动作是否 exact collision。 |
| early-stop / iteration-budget comparator | He 2021 | `COVERED_WITH_SOURCE_FORMAT_DEBT` | 有可读 primary fulltext可审 maximum-iteration、CRC/syndrome early stop 与 complexity comparator；legacy source 扩展名错误须保留。 |
| P0 residual-decaying paper | 无 | `IDENTITY_BLOCKED` | 不能声称 P0 已获取、已读或已裁决；2007 arXiv 近邻不得冒充。 |
| recent-neighbor debt | 2025 RL-CBP 已补 | `CLOSED_FOR_STEP3_INPUT` | Step 3 可用 recent direct neighbor；不等于 prior-art collision 已闭合。 |

本 terminal 的 claim ceiling 是：**Step 3 输入池已就绪，但 P0-specific exact-collision/provenance 仍为 UNKNOWN**。若后续结论必须承重 P0 的 residual-decay 细节，须由主控另行决定是否补合法 canonical source；T079 不继续下载或扩搜。

## 4. 冻结 Step 3 read pool

读取顺序冻结如下，不得把 rejected P0 加入：

1. `papers/doi/10.1587_transfun.2024eal2080/content.md`
   - Step 3 必须回答：input/state、check-belief/reliability 的可观测定义、action granularity、schedule/list update rule、stop/budget rule、baseline、equal-update/complexity口径、sorting/list overhead，以及与 `Q-C5-5` 九字段的关系。
2. `papers/doi/10.1109_wcsp52459.2021.9613326/content.md`
   - Step 3 必须回答：maximum-iteration 与 CRC/syndrome early-stop 的精确位置、first/second-stage 边界、普通 early-stop comparator 如何公平对齐、是否吸收 budget-only 候选、complexity 与 overhead 口径，以及与 `Q-C5-5` 九字段的关系。

明确排除：

- `papers/doi/10.1109_access.2019.2899106/metadata.json` 所记录的 rejected `cs/0702111v2`：identity mismatch；错误 source/content 已删除，禁止作为 P0 或 qualified pool 成员。
- 搜索 archive 的 title/abstract：只作候选身份与 acquisition provenance，不作 Step 3 方法结论。

## 5. Search / acquisition receipt

- Q1：`Residual-Decaying-Based Informed Dynamic Scheduling belief-propagation LDPC 10.1109/ACCESS.2019.2899106`
  - archive：`search-archive/2026-08-30/t079-c5-5-p0-exact.json`
  - 返回 2 篇；用于取得 2025 RL-CBP substitute。
- Q2：`LDPC adaptive maximum iterations reliability-aware early termination iteration budget decoding`
  - archive：`search-archive/2026-08-30/t079-c5-5-budget-early-stop.json`
  - 4 条均不比本地 He 2021 更直接；没有继续下载。
- downloader：`tools/download` wrapper 在 Windows CRLF 下无法由 Git Bash 解析；本轮调用 wrapper 指向的同一项目入口 `tools/paper_download.py`，未修改工具文件或改变下载管线。

## 6. 唯一下一步

主控接收本报告后，若认可 P0 substitute 的 claim ceiling，只可另派冻结两篇 pool 的 **GW Step 3 精读**。T079 不进入 Step 3，不裁决 exact collision，不实现/仿真/修改 decoder，也不更新 formal authority。
