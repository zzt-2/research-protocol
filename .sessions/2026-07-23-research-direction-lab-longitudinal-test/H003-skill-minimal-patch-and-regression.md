# Handoff: Skill 最小 patch 与历史回归

> 来源: R010 / D058（本轮是 closeout audit，按 RDL 三层记录纪律不新建 S） | 交接目标: 只修改 Skill 的三类规则并做历史 case 回归
> 文件名: H003-skill-minimal-patch-and-regression.md

## 已完成边界

campaign 已按 D058/V084 收口为 `SATURATED_NO_ACTIVE_CARRIER / DORMANT`。最终有效计数 7，`METHOD_SIGNAL=0`，active carrier=0。P11 已从错误的 9–15 dB 叙述纠正为实际固定 20 dB partial baseline。论文资产已按 A/B/C 分级，当前视图已统一。

## 不要做什么

- 不运行仿真，不修 P08/P09/P10/P11/G1，不为凑 10 包建 P12。
- 不启动 AMC；AMC 是新系统层级，后续若获授权必须另开 Groundwork 专题。
- 不把 7 个负面包、partial asset、G1/P09 反例升级成方法贡献。
- 不扩大成 controller 重写，不新增第四或第五类 patch。

## 必读

1. `topic-index.md` 的不变量与当前控制面。
2. `R010-campaign-final-effect-and-root-cause-audit.md` §4–§6。
3. `decisions.md` D058 与 `verifications.md` V084。
4. `projects/thesis-fso/direction-lab/harvest/method-production-campaign-thesis-map.md`。
5. 系统专题 `.sessions/2026-07-20-research-direction-lab-system/` 的 D019/V013。

## 接口变更（如有代码改动）

无。下一轮拟修改的 Skill 合同仅限三类：

```yaml
patch_categories:
  - executable_semantic_gates
  - contribution_tiers
  - lightweight_persistence
science_execution_authorized: false
amc_groundwork_authorized: false
```

## 失败数据附录（如涉及路线失败）

- accepted valid packages: 7；method signals: 0；active carriers: 0。
- 至少 7 条 verifier ACCEPT 后被后续语义审计推翻；P11 再增加一条未生效 SNR 标签纠偏。
- recovery elapsed/files-read 仍为 `UNMEASURED`。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| Skill 尚未实现三类 patch | 先收口事实，再改系统 owner | PENDING | 下一对话唯一执行任务 |
| 恢复时间未实测 | recovery receipt 必须记录真实 elapsed/files/lane-match | UNMEASURED | 下一次真实 compact/fork |
| D057 有重复且首份截断 | 历史不删，靠 supersession 消歧 | 由 D058 supersede | 不回写删除历史 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| executable semantic gate 回归 | P07/P08/P09/P10/P11/G1 历史缺陷均被相应门截获 | R010 撤回链 | 待测 |
| contribution tier 回归 | negative/partial/packaging 不得升到 T2/T3 | D058 | 待测 |
| persistence 回归 | 普通包不强制新增 D/V，topic-index 保持 current snapshot | R003/R010 | 待测 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

只做 Research Direction Lab Skill 最小 patch：可执行语义门、贡献层级、轻量持久化；用 P07/P08/P09/P10/P11/G1 做历史回归。通过后停下并汇报。不要启动 AMC。
