# [S007] Research Direction Lab 只读使用推演

> 2026-07-20 | 桌面演练 | 已完成（非行为验收）
> 2026-07-20 | Phase 3 收口 | 独立终验 PASS

## 目标

用 Task 6 的真实只读投影推演一次启动恢复、局部阻断换路、证据范围解释、次级论文材料收获和下一动作记录，检查目标使用形态是否清楚且不过重。

## 记录

### 推演边界

- 输入只包括 `STATUS.v1.md`、`project.v1.yaml`、`portfolio/current.v1.yaml`、`harvest/ledger.v1.yaml` 和既有历史指针。
- 不运行 Task 8 blind prompt，不给 Skill 行为打 PASS 分，不创建 batch，不执行科学 runner，不补造数字。

### 1. 启动恢复

用户入口只读 `STATUS.v1.md`。58 行内可直接恢复：formal=`BLOCKED`、当前允许 `READ_ONLY_MIGRATION_PREVIEW`、standard-CMA anchor、P03 当前 focus、六个 blocked axes、B003/P03 最近结论、九项 harvest、next action 和 strategy condition。Adapter/portfolio/harvest 仅由 Skill 内部按需下钻。

### 2. 局部阻断换路

读取 portfolio 后遇到 P01/U25=`DEFERRED_ARCHITECTURE`：缺 receiver-state snapshot、observable action hook 和 fork replay。演练没有继续修补 U24 runner，也没有因 P01 阻断停下询问用户；在只读授权内转向已经存在的 P03/Atlas 证据，继续完成范围解释与材料收获。

### 3. 证据范围与次级收获

- P03/Atlas 只支持 runnable representative subdomain 的 `LOCAL_NEGATIVE`，claim ceiling=`SLICE`。
- 16QAM、receiver-CSI/pilot、soft/coded output 仍是 `INFRASTRUCTURE_BLOCKED`，不是负结果；candidate/family 保持 open。
- 次级论文材料被保留：analog residual energy 明显变化不等于 hard-decision headroom；hard-decision local negative 不能关闭 coded/LLR/GMI/FER path；P01 action interface 是可复用合同但尚无真实动作效果。

### 4. 下一动作与战略边界

当前授权内的合法自动动作是验证只读投影并渲染 STATUS；没有获准的科学 runner。系统因此没有伪造“继续跑”，而是留下三条需战略选择的证据化路线：P03 回池、投资一条干净 blocked-axis closure、或转向已有候选族。改变贡献线或显著基础设施投入时才需要用户决策。

### 5. 推演发现并修复的问题

- 首版 STATUS 512 行、24 KB，全量 dump 四份对象，违反轻量入口；已改为八问 compact view，58 行、约 4.8 KB。
- 仅限制行数可被超长单行绕过；已加入 UTF-8 byte-aware 有界格式化、显式截断和超长对抗测试。
- 首版只显示 formal `BLOCKED`，未显示当前仍允许的只读动作；现已并列显示 Formal status、Currently allowed 和 Prohibited actions。

### 结论

组织形态符合 `STATUS-first + 一层按需下钻`，桌面推演未发现必须新增控制器的理由。它证明的是投影和使用入口可理解，不证明 Skill 已能长期自动可靠运行；该结论只能由 Task 8 forward tests 与后续 shadow 给出。

## 决策引用

- D005：本轮推演限定为只读桌面演练。
- D007：STATUS 固定为有界八问 view-model（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

Task 6–7 全阶段独立终验已由 V003 PASS。Task 8 仍未授权；下一入口为 H003，等待用户决定是否进入 fresh-agent forward tests。

Phase 3 首轮终验发现 durable Adapter 绑定 sibling worktree 绝对路径、声明的 STATUS command 实际为空操作。两项均已按 TDD 修复：指针改为 repo-relative；renderer 增加四输入 stdout-only CLI，真实 subprocess 输出与 STATUS 字节一致且不写项目文件。修复后 V003 独立终验 PASS。
