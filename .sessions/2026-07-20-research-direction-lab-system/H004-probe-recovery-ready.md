# Handoff: Probe/current-view 体系终验完成，进入连续科学 campaign

> 来源: S012 | 交接目标: 使用 D013 轻量体系恢复科学现状并连续推进多个机制分支
> 文件名: H004-probe-recovery-ready.md

## 已完成边界

- `research-direction-lab` 已采用 `Probe → Scout → Deep Evidence`；Probe 默认一份 compact record，Scout 的 receipt/verifier 按风险选用，Deep Evidence 才要求完整链。
- 科学语义 smoke 先于 provenance/扩算力；常数/平凡解、identity、output support、最小 overfit、简单 comparator 和信息边界已进入主 Skill。
- 恢复热路径固定为 STATUS、adapter、state/current、portfolio/current、harvest/current；显式 disposition 优先于 mtime/旧 prose。
- reducer、STATUS 和 adapter 已有动态门；三类 forward scenarios、真实 H009 historical RED 和 V011 独立终验均闭合。
- repo 与全局 Skill 56 个非缓存文件 SHA256 全等；完整测试 `90 passed, 1 skipped`。
- 本轮没有运行科学实验、训练 ML、创建 legacy B004 或改写 B001–B003/P03 Atlas/旧 raw artifacts。

## 不要做什么

- 不要回到“每个极小问题都造 manifest/receipt/verifier/synthesis/session/handoff”的旧流程。
- 不要把 artifact fidelity PASS 当作科学语义 PASS。
- 不要按 mtime、文件长度或旧 handoff 的措辞恢复当前结论。
- 不要只修 C04/C09 或只盯一个 winner；保持多个机制分支，局部 blocker 后轮转。
- 不要把 Scout 数字自动写入论文，或绕过 Groundwork/Contract/Execute 正式晋级。
- 不要修改 protected history、创建 legacy B004、push 或在每个小步骤等待用户。

## 必读

1. `.sessions/2026-07-20-research-direction-lab-system/T001-resume-large-science-campaign.md`
2. `.sessions/2026-07-20-direction-lab-science-scout/H010-s009-semantic-audit-recovery.md`
3. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md` 的不变量、D016、V005
4. `.agents/skills/research-direction-lab/SKILL.md`
5. `projects/thesis-fso/direction-lab/project.v1.yaml` 与现有 STATUS/state/portfolio/harvest

## 接口变更（如有代码改动）

```yaml
contracts:
  - id: current-view-paths
    change: Project Adapter paths 新增可选 probes / portfolio_history / harvest_current
    compatibility: 旧 adapter 不强制立即迁移
  - id: disposition-lineage
    change: 后续 DISPOSITION 必须显式替换同实体当前 event；悬空/跨实体/非当前 replacement 拒绝
  - id: status-current-harvest
    change: adapter 声明 harvest_current 后必须用匹配的 --harvest-current；inactive entries 不进入 STATUS
  - id: work-intensity
    change: Probe 最轻；Scout integrity extras conditional；Deep Evidence full chain required
```

## 失败数据附录（如涉及路线失败）

- 无 Skill 的 Probe RED 为一个 paired-input 问题默认规划 5 份产物；GREEN 降为一个 compact record。
- semantic partial RED 能发现 objective mismatch，但缺完整 identity/current-harvest 处置；GREEN 全部闭合。
- H009 historical RED SHA256：`61ea49edeb8fb6c7cd1ac1278e47775c9f17616357478f520d9267ff51c5041b`。
- verifier 首轮 PARTIAL 的三项 P1 与二轮文案冲突均已在 V011 关闭。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 科学项目 current files 仍含旧 preview 命名/内容 | 五入口恢复应反映 H010/D016 | 待下一 campaign 做有界迁移 | Phase 0 先对账，完成后立即科学推进 |
| STATUS LF/CRLF | renderer 与 tracked bytes 应一致 | 既有 Windows 行尾债务 | 修改该 STATUS 或建立跨平台 CI 时处理 |
| 长期自动稳定性 | 单次 forward test 不外推长期可靠 | 尚待真实连续 campaign 观察 | 每个较长工作窗后审计一次偏离与治理成本 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| Probe 成本 | 一个问题默认一个 record，无全链 | D013 | GREEN 1/1 |
| 语义先行 | semantic FAIL 不扩算力、不判 family | D013 | GREEN 1/1 |
| current recovery | 不复述 invalidated 旧结论 | D013/D016 | GREEN 1/1 |
| Skill 回归 | 0 failure | V011 | 90 pass, 1 env skip |
| 独立终验 | P0/P1/P2=0（本轮范围） | V011 | PASS |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证至少 3 条关键事实：H010 当前科学结论；V011 的 90 pass/1 skip；repo/global Skill hash 全等
- [ ] 已检查 `_registry.yaml` 中本专题和 science-scout 的 depends_on/conflicts_with
- [ ] 已确认当前范围不违反“protected history 不改、legacy B004 不建、Scout 不自动进论文”

## 下一轮

直接执行 T001。先做有界 current-view 对账，然后在同一工作窗内推进多个机制分支；不要做完一个 Probe 就停。只有所有合法路径耗尽、需战略扩域或不可逆操作时才请求用户。
