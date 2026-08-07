# Handoff: coded-burst Groundwork 在 Step 1 证据不足关闭

> 来源: S001 | 交接目标: 未来仅在出现新承重证据时判断是否重开 Step 1 缺口补证
> 日期: 2026-08-07

## 到哪了（状态）

6/6 query 已收口，D002 terminal=`STEP1_EVIDENCE_INSUFFICIENT`，V001/fresh verifier `ACCEPT`、blocker=0。三张预卡均为 HYPOTHESIS_ONLY，没有候选同时通过六项 reopen gate；Step 2 未执行。专题 closed，master-state 已同步。

## 下一步干什么

没有当前执行动作。只有用户提供或允许获取能同时补足以下两类缺口的新证据时，才讨论重开：①真实低仰角星地强条件 occurrence + threshold-conditioned AFD/相关尺度；②至少新增一篇 2019+ strict task-matched placement/interleaving/segmentation baseline。重开后第一件事是复核 R001/R002 的缺口，不是下载现有 CORE 或运行 coded-chain。

## 纪律（续接者必须注意的）

- 旧 4b#1 的 `Lburst=60–428`、B=27 容量约 810、0/15 超容、0 dB 上界保持永久有效。
- ms coherence 不是 recoverable burst duration；simulation/stress 参数不是真实 occurrence。
- 不用 depth switching、LLR calibration、AMC/HARQ 或 generic RF mapping 充当新方法/strict baseline。
- 不运行 coded-chain；P08-R2 只有工程 BOM 价值，现有 lifecycle/placement/schema/metric 不闭合。
- 不把 `STEP1_EVIDENCE_INSUFFICIENT` 写成领域不存在或 outage 已被证明主导。

## 失败数据附录

- physical-support / temporal-span：`UNKNOWN / UNKNOWN`。
- strict 2019+ task-matched baseline：`1`（要求 ≥2）。
- search API：S2 + OpenAlex 两源（`gw-search.md` 要求 ≥3）。
- testbed：lifecycle=PARTIAL、placement controllability=NO、schema=PARTIAL、delay/overhead metric=NO。
- 工期：最小 adapter 3.75–5.0 人日；完整 testbed 8.5–12.0 人日。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 两篇 SPIE 仅 abstract | 承重物理参数需全文/一手指针 | target `α/β`、Rytov、AFD 未闭合 | 用户允许 Step 1 补证且全文可得 |
| JPHOT 2021 AFD 仅 abstract | burst/outage 分界需 threshold-conditioned AFD | 无数值 | 同上 |
| search 三源门未过 | GW Step 1 ≥3 搜索源 | 仅 S2+OpenAlex | 出现足以改变 terminal 的新证据后才补；不为凑门重跑 |
| P08-R2 placement/lifecycle 缺口 | action/lifecycle 必须可执行验证 | 现有 runner 不满足 | 只有 Step 1–4a 合法晋级后才投资 adapter |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 当前状态 |
|---|---|---|---|
| physical occurrence | 一手 target 场景参数 + provenance | 用户 reopen gate 1 | UNKNOWN |
| recoverable burst | AFD/相关 span 可与 codeword/interleaver span比较，且不是整块 outage | 用户 gates 2–4 | UNKNOWN |
| recent baseline | ≥2 篇 2019+ strict task-matched CORE | 用户 Step 2 要求 | 1 |
| testbed scope | 最小 adapter 不明显超过约 5 天 | 用户 BOM 门 | 3.75–5.0 人日，中风险 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：strict baseline=1 → 待核 R002/R005
  - 声称2：Step 2 未执行 → 待核 git/papers/status
  - 声称3：P08-R2 四项 BOM 不闭合 → 待核 R003/源码
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
