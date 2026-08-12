# Handoff: K2 GW Step 2 acquisition complete

> 来源: S002 | 交接目标: 主控裁决是否授权 Groundwork Step 3
> 文件名: H002-step2-ready-for-user-confirmation.md

## 已完成边界

- D003 只开放 Step 2 acquisition；12 篇入池，9 qualified、8 CORE。
- A reference/unwrap、B full mixture/fixed-order、C recent coherent optical/FSO 三路线都有全文；P0 C01 Wang TSP 2022 与 C02 TCOM 2016 均闭合。
- C06/C07/C13 全文不可得，保留为 coverage limitation；没有把 metadata/abstract 算作全文。
- V002 fresh verifier 复算 receipt/hash/count/route/terminal 后 PASS；terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。

## 不要做什么

- 不在未授权时进入 Step 3，不抽完整 input→decision→action→output，不判 D1/D2 collision/Q#。
- 不把 acquisition coverage 包装成 non-collision、新颖性、Go、方法或论文贡献。
- C05/C09/C10 公式相关声称必须回看 source PDF；不能只依赖有 glyph loss 的 fast conversion。
- 不用 C06/C07/C13 的摘要替代全文，也不再绕访问控制获取。

## 必读

1. `topic-index.md`
2. `R004-step2-acquisition-coverage.md`
3. `projects/thesis-fso/multi-hypothesis-phase-unwrapping/step2-acquisition-receipt.json`
4. `verifications.md` V002
5. `stages/gw-read.md`（仅在主控授权 Step 3 后）

## 接口变更（如有代码改动）

无。

## 失败数据附录（如涉及路线失败）

- C06 `10.1016/j.optcom.2024.130326`：合法 DOI/OA/Unpaywall/arXiv 通道 `all_failed`。
- C07 `10.1117/12.3107192`：合法 DOI/OA/Unpaywall/arXiv 通道 `all_failed`。
- C13 `10.1016/j.yofte.2020.102208`：合法 DOI/OA/Unpaywall/arXiv 通道 `all_failed`。
- 本轮无科学实验或方法失败。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| C06/C07 recent action | direct recent competitor 要全文抽动作 | 全文 unavailable | 若后续成为承重 exact-action debt，再请求用户补全文 |
| C13 pilot-reset action | cheap comparator 要一手细节 | 全文 unavailable | Step 3 先用 C09/C14/C10；若结论依赖 C13 再阻断 |
| C05/C09/C10 公式 glyph | 公式声称必须可核 | source PDF 完整，markdown 局部损失 | Step 3 公式字段回看 PDF |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 本轮 |
|---|---|---|---|
| CORE fulltext | ≥5 qualified CORE | delegation/gw-acquire | 8 |
| 路线 coverage | A/B/C 均有全文 | delegation | 3/1/6 |
| P0 blockers | reference + full mixture 均闭合 | delegation | C01/C02 PASS |
| terminal | 只允许 Step 2 三 terminal | delegation | READY |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 12/9/8 与 A/B/C=3/1/6：machine receipt 复算
  - C01/C02 source/content hash 与 identity：receipt + canonical
  - C06/C07/C13 无 source/content 且未计 qualified：receipt + canonical stub
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

等待主控 coverage confirmation。若授权 Step 3，先重读 `stages/gw-read.md` 并按全文动作/复杂度合同精读；不得凭本 handoff 自动开始。
