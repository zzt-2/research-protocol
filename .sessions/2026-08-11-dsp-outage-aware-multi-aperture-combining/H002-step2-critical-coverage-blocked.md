# Handoff: GW Step 2 critical direct-competitor coverage blocked

> 来源: S002 | 交接目标: 主控取得用户 coverage confirmation
> 文件名: H002-step2-critical-coverage-blocked.md

## 已完成边界

- 对冻结九篇池完成 existing-asset audit、`tools/download` DOI/OA 两轮与 IEEE 第三轮合法获取。
- fulltext available/content qualified=`4/9`：WiSEE 2024、Wang 2023、ICCC 2022、JPHOT 2020。
- frozen optical CORE qualified=`2/5`：WiSEE 2024、Wang 2023；RF comparator 与 optical neighbor 未替代 CORE。
- 2019 P0 identity confirmed，但 fulltext unavailable：非 OA、无 arXiv/PDF URL，合法获取链均失败。
- R002/R003 已固定 paths/identity/provenance/bytes/SHA-256/lines/quality；V002 fresh verifier=`PASS 0/0/0`。
- terminal=`STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`；Step 3=`NOT_AUTHORIZED`。

## 不要做什么

- 不把 abstract、参考文献命中、read-note 或网页片段当 P0 全文。
- 不用 ICCC、JPHOT 2020 或其他 generic neighbor 凑 optical CORE。
- 不在 coverage confirmation 前进入 Step 3、提取完整动作签名或给 exact-collision 结论。
- 不实现、不仿真、不修 b3 caller、不运行 smoke；不重开 coded C1。

## 必读

1. `topic-index.md`
2. `R002-step2-acquisition-coverage.md`
3. `R003-step2-acquisition-receipt.md`
4. `verifications.md` V002
5. `decisions.md` D002

## 接口变更（如有代码改动）

无代码改动。新增两篇 canonical paper asset：ICCC 2022 与 JPHOT 2020 的 `source.pdf`、`content.md`、metadata；papers/search-archive 按仓库策略忽略，不在 Git 提交中强制纳入。

## 失败数据附录（如涉及路线失败）

| 项目 | 结果 |
|---|---|
| P0 DOI/OA | `all_failed` |
| P0 S2/OpenAlex | non-OA；arXiv/PDF URL 均空 |
| Geisler DOI/viewmedia | `all_failed` |
| Access IEEE 第三轮 | 两次 30 s stream timeout；未留下可验证文件 |
| 总 targeted qualified | 4/9 |
| optical CORE qualified | 2/5 |

这是 coverage failure，不是方法或碰撞裁决。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 2019 direct competitor 无全文 | 最近 direct competitor 必须 fresh-context 精读后才能比较完整动作 | CRITICAL GAP | 用户提供合法 PDF/HTML，或显式接受 claim limitation |
| optical CORE 仅 2/5 | Step 2 目标≥5 CORE | BLOCKED | 补齐核心全文并重跑 identity/content gate |
| C26 identity 未闭合 | comparator 应有正式 identity | UNKNOWN | 后续若仍需要，单独闭合；不得替代 P0 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 本轮结果 |
|---|---|---|---|
| content quality | ≥50 有效行、identity 一致、无反爬/大面积乱码 | gw-acquire + D002 | 4/4 claimed qualified PASS |
| CORE coverage | ≥5 qualified optical/reference CORE | 本轮冻结合同 | 2/5，FAIL |
| P0 availability | source/content 可验证 | 本轮 critical blocker | unavailable，FAIL |
| verifier | P0/P1/P2=0/0/0 | T006 | PASS |

## 接收方验证（续接对话时必须完成）

- [x] 已读取 topic-index 的不变量段落
- [x] 已验证本文件中的至少 3 条关键事实声称
  - qualified=`4/9`：PASS — R002/R003/V002。
  - P0 fulltext unavailable：PASS — worktree/shared-root/DOI/downloads/manual 无 source/content。
  - Step 3 原为 `NOT_AUTHORIZED`：PASS — topic/master/registry；本轮由 D003 显式 scope change。
- [x] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with：B3 closed、RDL dormant；coded C1 只作禁止重开边界。
- [x] 已确认当前范围未违反“明确不含”：D003 显式撤销旧阻塞并仅开放 Step 2 repair + Step 3。

## 下一轮

主控只需让用户二选一：

1. 手动提供 P0 合法全文至 `papers/manual/{slug}/` 并补 metadata，然后仅重跑 Step 2 quality gate；
2. 明确确认接受 P0 未精读、exact collision unresolved 的 coverage/claim limitation，并另行决定是否授权 Step 3。

主控已选择接受 2019 fulltext limitation，并以 JLT 2023 做 Step 2 narrow repair；后续以 D003/S003 为当前入口。
