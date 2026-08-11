# Handoff: Step 3.5 exact-action evidence blocked

> 来源: S004 | 交接目标: 主控接收 Step 3.5 终态并保持 idle
> 文件名: H004-step3-5-evidence-blocked.md

## 已完成边界

- 完成 Round 1 8-query matrix、Wang/Liu/Johst/Sun 前后向引用链与 Round 2 6-query 定向补查；最后一轮 new MUST/SHOULD=`0/0`。
- 新增 Zhang 2023 全文定向精读，确认其为 estimator-changing neighbor、非 exact collision。
- Sun 2019 与 4 篇新增 MUST 直接竞品均完成合法资产/获取核查；承重全文仍不可得。
- R005 统一抽取动作签名并裁 terminal=`EVIDENCE_BLOCKED`；Q001 无 Step 4a 入口。
- 未设计方法、实现、仿真、修改 b3 caller 或重开 coded C1。

## 不要做什么

- 不把“未确认 exact collision”写成 non-collision、新颖性、方法成立或 METHOD_SIGNAL。
- 不因已检索收敛而忽略 Xie/Qiu 的 primary-fulltext action debt。
- 不用标题、摘要或二手引文补齐 trigger/weight/admission/no-valid 字段。
- 不自行进入 Step 4a；不再重跑同义宽泛 query。

## 必读

1. `R005-step3-5-exact-action-closure.md`
2. `decisions.md` D005/D006
3. `verifications.md` V004
4. `projects/thesis-fso/literature_notes_dsp_outage_multi_aperture.md`
5. `projects/thesis-fso/worker-logs/step-3-5-dsp-outage-citation-sun.md`
6. `projects/thesis-fso/worker-logs/step-3-5-direct-candidate-acquisition.md`

## 接口变更（如有代码改动）

无代码改动。新增 Zhang 2023 canonical read note/read-log；新增检索、引用链、获取与定向精读 receipts。

## 失败数据附录（如涉及路线失败）

| 项目 | 结果 |
|---|---|
| Round 1 search | 115 raw / 45 unique；MUST/SHOULD=0/0 |
| citation chains | 134 raw / 121 unique；新增 MUST/SHOULD=5/5 |
| Round 2 search | 6 raw / 4 unique；new MUST/SHOULD=0/0 |
| direct acquisition | Sun + 4 MUST 均无 qualified primary fulltext；4 MUST 实下 0/4 |
| readable new direct neighbor | Zhang 2023 = neighbor，不是 exact collision |
| terminal | `EVIDENCE_BLOCKED`；不是 scientific Kill |

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| Xie/Qiu exact action | direct identity 必须用一手全文裁完整动作 | UNRESOLVED_BEARING | 合法取得全文或等价后续一手完整动作证据 |
| Sun 2019 exact action | 摘要/二手不能裁窄 collision | UNRESOLVED_LIMITATION | 同上 |
| broader post-all-FS/CE/CPE | criterion 3 需近期 task-matched baseline | EXCLUDED | 新一手 baseline 明确该位置 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 本轮结果 |
|---|---|---|---|
| search convergence | 最后一轮 new MUST/SHOULD=0 | D005/gw-supplement | PASS，Round 2=0/0 |
| exact collision | 同 input-trigger-action-output 一手确认 | D005 | 未确认 |
| survival evidence | 无 confirmed collision 且承重动作充分 | D005 | FAIL，direct action debt 未闭合 |
| scope | Step 3.5 only | D005/V004 | T016 首验 PARTIAL 0/1/2；bounded repair 后 final PASS 0/0/0 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

保持 idle。只有主控取得承重 primary fulltext/等价一手动作证据并显式授权后，才可做 bounded Step 3.5 repair；否则不得进入 Step 4a 或重复搜索。
