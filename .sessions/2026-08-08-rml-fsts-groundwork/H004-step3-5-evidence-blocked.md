# Handoff: RML-FSTS Step 3.5 证据阻塞

> **SUPERSEDED BY D008/V005/H005**：本文件保留执行阶段历史。130981 共享全文漏查且 8 项 blocker 等强分类过严；不得再据本 Handoff 阻断 Step 4a。

> 来源: S003 | 交接目标: 取得关键一手全文后只重开 Step 3.5 action-level 竞争裁决
> 日期: 2026-08-09

## 到哪了（状态）

Step 3 继续由 D005/V003/H003 保持 `✅ completed`。本轮 D006 授权的 mandatory Step 3.5 已完成 8-query matrix、三类真实来源、Wang/Enhanced 双向引用链、三轮检索止损与新增全文处理；R004/D007 将 terminal 记为 **证据阻塞**，V004 fresh-context 独立终验 10/10 gates PASS。Qualified fulltext 中未确认 exact collision 或 conditioned single-lag lookup 等价，但 8 项关键一手全文仍不可得，因此 Step 4a 没有入口。

## 下一步干什么

优先获得以下任一关键一手全文，并按 T005/T007 的 identity/path/SHA/bytes/action 字段做 fresh fulltext read：Cheng 2020、OE.561252、ACP/IPOC 10809664、SSRN 6293357、Optics Communications 130981；两篇 Optica 与 Dong 2009 继续作为边界债务。取得全文后只重开 Step 3.5 exact-action/cheap-lookup 裁决，更新 R004/D007 current views；未闭合前不得进入 Step 4a。

## 纪律（续接者必须注意的）

- “qualified evidence 未确认 collision”不等于首次或新颖；缺全文项保持 UNKNOWN。
- exact action 是 receiver-visible condition→lag/`B_L`/correlation-distance selection 或 condition-aware multi-lag weighting；TS/FFT/STFT/CPR/combining 邻接不自动碰撞。
- dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 始终作为 strongest cheap alternative；不要包装成 adaptive method。
- 不开 R4；三轮检索上限已用尽。只有新取得的一手全文才构成重开 Step 3.5 的新证据。
- 不进入 Step 4a、smoke、仿真、MVE、方法设计或实现；四个 `p05_run*.log` 继续保持未跟踪且不动。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 8 项关键全文不可得 | exact boundary 必须由一手全文承重 | `EVIDENCE_BLOCKED` | 获得合法全文并完成 identity/SHA/action read |
| R2 Q4 与 R3 源限定补查均超时 | timeout 不是 0 命中 | 三轮上限已达，禁止 R4 | 仅新全文，不再追加语义 query |
| conditioned lookup 胜负未知 | 最强廉价替代不得遗漏 | 保留 comparator 身份；未比较 | 只有 Step 3.5 闭合后才可在 Step 4a 比较 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 当前结果 |
|---|---|---|---|
| Step 3.5 检索纪律 | 8-query matrix、≥2 actual sources、核心竞品双向链、最后一轮0新增或达到3轮上限 | `stages/gw-supplement.md` | V004 PASS：达到三轮上限；R3 timeout 如实记录 |
| exact boundary | 所有承重竞品有 identity/fulltext/SHA/action evidence | 用户本轮约束 + FR-26 | V004 确认 BLOCKED：8 项缺全文 |
| Step 4a 入口 | Step 3.5 竞争边界闭合 | FR-22 | V004 确认 NO ENTRY |

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：R1 8/8 query + 三类实际来源 → 验证结果：[PASS/FAIL + receipt]
  - 声称2：Wang/Enhanced 双向引用链 63→51 unique → 验证结果：[PASS/FAIL + receipt]
  - 声称3：8 项关键全文不可得且 Step 4a NO ENTRY → 验证结果：[PASS/FAIL + R004/D007]
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
