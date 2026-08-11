# Handoff: GW Step 3 Q001 survives, ready for Step 3.5 confirmation

> 来源: S003 | 交接目标: 主控验收 Step 3，并决定是否授权 Step 3.5
> 文件名: H003-step3-ready-for-step3-5.md

## 已完成边界

- 用户 voice anchor：“行吧。说实话，干这么多又是啥也没出来真tm难受。”（已登记 `voice.md` → D003）；因此本轮采用两项 bounded repair 后立即裁决，不以 coverage 行政门继续空转。
- D003 以 qualified JLT 2023 CORE 将 Step 2 fulltext 由 4 补到 5；2019 fulltext unavailable 事实保持，terminal=`STEP2_ACCEPTED_WITH_2019_FULLTEXT_LIMITATION`。
- fresh readers 完成五篇全文：Johst 2024、Wang 2023、Liu JLT 2023、Tu JPHOT 2020、Yang ICCC 2022；各有 title gate、15字段、7结构段、通信参数与 completeness。
- 宽泛 adaptive combining、pilot-attenuation soft weight、known-OSNR admission 与 joint 2N×2 equalization 已归 comparator/collision boundary。
- Q001 收窄为 Wang 原文真实顺序上的 branch-local FS/alignment+phase-correction→MRC validity admission；四判据 4/4 PASS。
- fresh verifier 首验 `PARTIAL 0/2/0`，两项 bounded repair 后终验 `PASS 0/0/0`；V003 固化修复血缘。
- terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`；未进入 Step 3.5/4a，未实现、仿真或产出方法信号。

## 不要做什么

- 不把 Q001 外推为“所有 FS/CE/CPE 完成后”的已闭合问题；该位置还缺近期 task-matched baseline。
- 不把 Sun 2019 exact collision 写成 non-collision；全文缺失，动作仍 `UNRESOLVED`。
- 不把 Johst hard discard、Tu OSNR admission、Yang pilot weight、Liu 2N×2 或 SC/GSC 当新方法。
- 不跳 Step 3.5 直接进入 4a/smoke，不修 b3 caller，不重开 coded C1。

## 必读

1. `topic-index.md`
2. `R004-step3-direct-competitor-synthesis.md`
3. `decisions.md` D003/D004
4. `verifications.md` V003
5. `projects/thesis-fso/literature_notes_dsp_outage_multi_aperture.md`
6. `projects/thesis-fso/worker-logs/step-3-dsp-outage-independent-verifier.md`

## 接口变更（如有代码改动）

无代码改动。新增/更新五篇 canonical read notes 与 project read-log；四篇 ignored-paper notes 已显式纳入 Git。

## 失败数据附录（如涉及路线失败）

| 项目 | 结果 |
|---|---|
| verifier initial | `PARTIAL 0/2/0` |
| Major 1 | Wang action position 被误写为 all-DSP-after；已收窄到真实 branch-local pre-MRC 边界 |
| Major 2 | source/persistence/casing 链未闭合；已修 path、统一 lowercase canonical path、force-add |
| verifier final | `PASS 0/0/0` |

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| Sun 2019 无全文 | closest direct competitor exact action 要一手证据 | CRITICAL FOR STEP 3.5 | 主控授权 Step 3.5 后合法获取/等价一手动作证据 |
| post-all-FS/CE/CPE baseline | criterion 3 需 task-matched recent M | UNRESOLVED / EXCLUDED FROM Q001 PASS | Step 3.5 定向检索；未闭合不得外推 |
| b3 truth-h/RNG/offset | future experiment must be receiver-visible and paired | NOT TOUCHED | 仅 Step 4a 获授权且文献门通过后 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 本轮结果 |
|---|---|---|---|
| fulltext read | ≥5 title-matched qualified papers; 14+ fields; 7 sections | gw-read | 5/5 PASS |
| Q001 | M-C-A 四判据全部成立 | glossary | 4/4 PASS at branch-local boundary |
| 2019 limitation | 不用摘要裁 exact action | D003/T009 | PASS; `UNRESOLVED` |
| verifier | critical/major/minor=0/0/0 | T010 | PASS after bounded repair |
| scope | Step 3 only | D003 | 0 violations |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

只有主控另行授权后执行 Step 3.5：优先闭合 Sun 2019 完整 input-trigger-action-output，并检索真正 post-all-FS/CE/CPE baseline；同时做 branch-local `lock-aware / frame-sync-confidence / phase-validity / bounded-abstaining combining` exact collision。不得实现或仿真。
