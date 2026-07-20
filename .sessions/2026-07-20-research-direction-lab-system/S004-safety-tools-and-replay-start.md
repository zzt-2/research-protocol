# [S004] 确定性工具与历史 replay 启动

> 2026-07-20 | Task 4–5 实施 | 已完成

## 目标

在 Phase 1 已验证地基上，按 H001 实施 Task 4–5：只增加确定性安全小工具和只读历史 replay fixtures；不创建项目 adapter 实例，不运行科学实验。

## 记录

H001 接收核验：

- Skill 行数与接口：PASS——`SKILL.md` 为 71 行，ProjectAdapterV1 required 顶层字段为 10 个。
- Phase 1 验证：PASS——新体系定向测试 `10 passed`，旧 Direction Lab targeted baseline `62 passed`。
- 隔离与范围：PASS——当前为 linked worktree `codex/research-direction-lab-system`，工作树干净，Task 6 `project.v1.yaml` 不存在。
- 注册表：当前专题 `conflicts_with=[]`；`framework-evolution`、governance pilot、simulation foundation 三个依赖专题均存在。

用户当前指令“继续吧”依 H001 的唯一下一阶段解释为授权 Task 4–5。该短句属于 `voice.md` 规范明确排除的零信息推进语，不写入 voice；授权对象由 H001 和本范围变更共同固定。

实施结果：

- Task 4 已形成五个领域中立的确定性工具及测试。首轮独立审查发现事件并发追加可断链，修复后终验又发现 wrong-head 拒绝会留下空文件；两项均已按 RED→GREEN 修复。
- Task 5 已形成四个只读历史 replay fixtures。审查先修正 Atlas 的 claim ceiling（`DIAGNOSTIC` → `SLICE`），终验再把 current-CMA 的来源从执行提示词改绑为历史 report，并收窄为 report 直接支持的事实。
- 本阶段没有创建项目 Adapter 实例、forward test、shadow、B004 或科学实验；正式结论等待修复后的独立终验复审。

## 决策引用

- D004：批准 Phase 2 仅实施 Task 4–5（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；见 topic-index 2026-07-20 / D004 范围变更。

## 后续

修复后的全阶段独立复审已 PASS，见 V002；下一阶段入口见 H002。本轮不进入 Task 6–10。
