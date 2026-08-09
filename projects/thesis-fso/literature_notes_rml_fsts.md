# RML-FSTS Literature Owner

> 独立 owner：`.sessions/2026-08-08-rml-fsts-groundwork/`
> 研究对象：Wang 2023 FSTS fixed-lag/`BL` condition-dependence
> 当前记录 Step 1–2 已完成且覆盖面经用户确认；T001 仅派发 Step 3，尚不含 Q# 或目标缺陷裁决。

## GW Progress

| Step | 状态 | 日期 | commit | 证据 | 下游门控 |
|---|---|---|---|---|---|
| 1 search | ✅ PASS | 2026-08-08 | `a52bb5d6` | R001 + `rml-fsts-step1-search-receipt.json` + 7 query JSON | 允许 Step 2 |
| 2 acquire | ✅ USER_CONFIRMED | 2026-08-09 | `a52bb5d6` | 5 篇合格 CORE + R002 + coverage/receipt + D003 | 允许 Step 3 |
| 3 read | 🟦 DISPATCH_READY | 2026-08-09 | — | S002 + D003 + T001 | 只执行当前 5 篇；完成/阻塞后停止 |
| 3.5 supplement | ⬜ NOT_STARTED | — | — | — | Step 3 未完成前禁止 |
| 4a feasibility | ⬜ NOT_STARTED | — | — | — | Step 3/3.5 未完成前禁止 |

## Step 1 候选表

| # | DOI | Priority | 路线 | CORE 预判 | 全文状态（Step 1 结束时） |
|---:|---|---|---|---|---|
| 1 | `10.1109/JPHOT.2023.3265847` | 必读 | A/C | C1/C2/C4 | 共享全文待 Step 2 核验 |
| 2 | `10.1109/JPHOT.2022.3161795` | 必读 | A | C2/C4 | 待 Step 2 |
| 3 | `10.1364/OE.520452` | 必读 | A/C | C2/C4 | 共享库待 Step 2 核验 |
| 4 | `10.1016/J.OPTCOM.2020.126046` | 必读 | A | C2/C4 | 待 Step 2 |
| 5 | `10.1109/CHINACOM.2009.5339877` | 必读 | B | C3 | 待 Step 2；题名不能冒充全文 |
| 6 | `10.1109/TVT.2022.3218937` | 必读 | B | C3 | 共享全文待 Step 2 核验 |
| 7 | `10.3390/electronics10232942` | 建议读 | B | C3 | 待 Step 2 |
| 8 | `10.1155/2009/821819` | 建议读 | B | C3 | 待 Step 2 |
| 9 | `10.1109/JLT.2020.3003561` | 必读 | C | C4 | 共享全文待 Step 2 核验 |
| 10 | `10.1364/OE.505931` | 必读 | C | C4 | 待 Step 2 |
| 11 | `10.1364/OE.448956` | 必读 | C | C4 | 待 Step 2 |
| 12 | `10.1109/WiSEE61249.2024.10850117` | 必读 | C | C4 | 共享全文待 Step 2 核验 |

## Step 1 边界

- source fact：fixed `BL/BN` 与 modulation、training length、received power 条件有关，低功率存在 timing/FOE 退化。
- target hypothesis：同一 receiver-visible condition 内是否有 lag-ranking crossover 仍未知。
- strongest cheap alternative：未来必须保留 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。
- prior-art ceiling：不得声称首创 multi-lag、stepwise correlation、FSTS 或联合同步。

## Step 2 覆盖

- 合格 CORE 5 篇：Wang 2023（C1/C2/C4）、Enhanced 2024（C2/C4）、Morelli 2009（C3）、Paillier 2020（C4）、Yu 2023（C3）。
- Tang 2022 与 WiSEE 2024 因 metadata/provenance 矛盾不计入；另 5 篇全文止损后仍缺失。
- Step 2 coverage terminal=`STEP2_READY_FOR_USER_CONFIRMATION` 的用户确认关口已满足；当前状态=`STEP3_DISPATCH_READY`，Step 3 尚未开始。

## Step 3 派发边界

- 冻结精读输入：Wang 2023、Enhanced 2024、Morelli 2009、Paillier 2020、Yu 2023，共 5 篇合格 CORE。
- Yu 2023 先闭合共享 `source.md` 到 canonical `content.md` 的字节一致路径适配与 title/DOI preflight；失败则 title-abort 并返回 Step 2。
- 四判据只采用 `stages/glossary.md` canonical 四项；不得增加 `problem_truth` 或 `novelty` 门。
- 无 Q# 全过时保持 Step 3 `BLOCKED/IN_PROGRESS`，记录回 `gw-search` 的恢复路径；通过时只将 Step 3 标为 `✅ completed`，不自造 terminal。
- T001 到 Step 3 边界停止；不进入 Step 3.5/4a，不运行 smoke、实现或仿真。
