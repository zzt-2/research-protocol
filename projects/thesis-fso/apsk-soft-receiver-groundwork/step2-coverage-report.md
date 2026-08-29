# Ch5 APSK soft receiver — GW Step 2 coverage report

> Task: T044 | Date: 2026-08-30 | Scope: acquisition and coverage gate only
>
> No Step 3 reading, Q#, feasibility decision, implementation, or experiment is included.

## 文献覆盖面状态

- 审计候选：9 篇（T040/T041 的 8 个 exact targets + 1 个同机制 syndrome-BF substitute）。
- Qualified full text：6 篇。
- Failed exact targets：3 篇。
- 内容质量不达标：0 篇。
- Coverage verdict：`PASS_WITH_ONE_NONBLOCKING_DEBT`。

### Qualified full text

| ID | 论文 | 机制覆盖 | 存储路径 | 正文行数 / 非空行 | 身份门 |
|---|---|---|---|---:|---|
| T040-001 | Layton et al., *Improved demapping for channels with data-dependent noise* (2018) | 标准 isotropic/scalar demapper；symbol-dependent full covariance demapper | `papers/doi/10.1186_s13638-018-1136-z/` | 442 / 221 | DOI、题名、正文一致 |
| T041-004 | Baldi et al., *On the use of ordered statistics decoders for low-density parity-check codes in space telecommand links* (2016) | OSD/MRB rescue | `papers/doi/10.1186_s13638-016-0769-z/` | 648 / 330 | DOI、题名、正文一致 |
| T041-002 | He et al., *Lowering the Error Floor of Quantized NR LDPC Decoders by a Post-Processing on Trapping Sets* (2021) | trapping-set post-processing | `papers/doi/10.1109_wcsp52459.2021.9613326/` | 231 / 122 | DOI、题名、正文一致 |
| T041-006 | Wu et al., *Adaptive-Normalized/Offset Min-Sum Algorithm* (2010) | adaptive NOMS | `papers/doi/10.1109_lcomm.2010.07.100508/` | 192 / 96 | DOI、题名、正文一致 |
| T041-007 | Xie et al., *Bit-Interleaved LDPC-Coded Modulation with Iterative Demapping and Decoding* (2009) | APSK BICM-ID / iterative demapping | `papers/doi/10.1109_vetecs.2009.5073425/` | 223 / 112 | DOI、题名、正文一致 |
| T044-S01 | Zhao et al., *An Improved Syndrome Bit Flipping Decoder with Narrowed Flipping Set for LDPC Codes* (2023) | syndrome-BF rescue（同机制 substitute） | `papers/doi/10.1109_iccc59590.2023.10507492/` | 239 / 119 | DOI、题名、正文一致 |

所有 qualified 条目均超过 50 行有效内容；题名、作者区、章节、算法/公式与参考文献连续，未见大面积乱码。PDF fast conversion 对部分公式符号有常规字符损失，但不存在把摘要误当全文或仅标题/节名的情况。

### Failed exact targets

| 原 ID | 论文 | 失败类型 | 状态 |
|---|---|---|---|
| T040-002 | Zhang/Kim, *Performance Enhancement by Scaling Soft Bit Information of APSK* (2013), DOI `10.7840/kics.2013.38c.10.858` | OA transport failure | JSON 明确为 OA 且有 KoreaScience PDF 直链；项目 downloader 两次均遇到对端连接重置。不是付费墙。 |
| T041-001 | *The Syndrome Bit Flipping Algorithm for LDPC Codes* (2023), DOI `10.1109/lcomm.2023.3272277` | exact-identity miss | 第一轮 title→arXiv 错配到 *Gradient Descent Bit Flipping Algorithms for Decoding LDPC Codes*；IEEE exact-title 获取只返回近邻。以 T044-S01 同机制 substitute 保证 BF 覆盖，但不冒充 exact paper。 |
| T041-008 | Chen–Fossorier, *Reduced-Complexity Decoding of LDPC Codes* (2005), DOI `10.1109/tcomm.2005.852852` | exact-identity miss | 第一轮错配到 *Reduced-Complexity Column-Layered Decoding and Implementation for LDPC Codes*；IEEE exact-title 获取未命中原文。未把近邻算作 exact recipe。 |

## 覆盖面分析

### C5-1 structured-covariance demapper

`PASS`。Layton 全文不是摘要级证据：

- `content.md:105-111` 给出 symbol-dependent bivariate Gaussian 与非对角 covariance；
- `content.md:131-145` 给出 likelihood、determinant 与 covariance estimation；
- `content.md:189` 明确比较 constant circularly symmetric covariance 的 standard demapper 与 proposed covariance-based demapper。

因此，一篇全文已同时覆盖验收要求中的 isotropic/scalar side 与 full covariance/data-dependent side。Zhang 2013 的 scalar soft-bit scaling exact recipe 仍是唯一 coverage debt，但不再阻断 C5-1 的 Step 3 比较入口。

### C5-2 decoder rescue backup

`PASS`，但只保证文献覆盖，不开放实现接口：

- adaptive NOMS：T041-006；
- rescue/OSD/BF：T041-004 + T044-S01；
- trapping-set post-processing：T041-002；
- APSK iterative demapping：T041-007。

最低门要求“至少 NOMS + 一种 rescue/OSD/BF”已超过；Chen–Fossorier exact full text 缺失不影响这一最低 coverage verdict。

## Exact-recipe collision ledger

| Target | 初始错配 | 处理结果 |
|---|---|---|
| T041-001 syndrome BF | arXiv `0711.0261v2`，实际为 GDBF | exact target 记 failed；另收录题名/DOI 独立的 syndrome-BF substitute |
| T041-006 adaptive NOMS | arXiv `cs/0609088v1`，实际为 normalized min-sum derivation | 由 IEEE PDF `5545625` 替换，resolved |
| T041-007 APSK BICM-ID | arXiv `2211.12655v1`，实际为 energy-based modulation | 由 IEEE PDF `5073425` 替换，resolved |
| T041-008 Chen–Fossorier | arXiv `1204.2577v1`，实际为 column-layered decoder | exact target 记 failed；未冒充 resolved |

## Decoder-interface debt

当前 adapter 只返回 hard information bits，尚不提供 C5-2 文献机制所需的内部信息：

- OSD/MRB 需要 channel soft values / LLR reliability ordering；
- adaptive NOMS 需要 check-node message state 与迭代相关 normalization/offset；
- syndrome-BF 与 trapping-set rescue 至少需要 syndrome、失败状态及 channel reliability / residual pattern；
- BICM-ID 需要 decoder soft output 回灌 demapper，而非仅 hard information bits。

因此 C5-2 仍是“文献覆盖完成、接口未授权”的后备路线。本报告不提出接口实现方案。

## 付费墙缺口

- 已确认付费墙缺口：0。
- T040-002 是 OA transport failure，不得标成付费墙。
- T041-001/T041-008 是 exact identity/retrieval miss，不以摘要或近邻全文代替。

## 引用质量分析

- 正式发表：6/6 qualified。
- 预印本：0/6（0%）。
- 来源结构：SpringerOpen/EURASIP 2 篇，IEEE 正式会议/期刊 4 篇。

## 用户行动项与 Step 3 gate

- [ ] 用户确认本 coverage report。
- [ ] Zhang 2013 若后续人工取得，按 DOI 路径补入；当前作为单一非阻塞 coverage debt。

**阻塞 Step 3 的唯一 blocker：用户尚未确认本 coverage report。** 文献数量门、C5-1 双侧覆盖门和 C5-2 后备覆盖门均已满足。
