---
name: sim-preflight
description: 仿真前必看流程。触发场景：跑仿真/实验脚本、改实验参数、加新算法（载波恢复/KF/DPLL/VV/BPS/均衡）、验证 BER 或相位估计结果、为论文引用仿真数字、修改 common/ 或 params.py、新对话恢复仿真工作。强制按文档纪律操作，防止文档体系崩溃。遗漏即中断。
version: 1.2.0
last_updated: 2026-07-08
changelog: ./CHANGELOG.md
---

# 仿真前必看流程（sim-preflight）

本 skill 是 `projects/simulation/` 仿真体系的操作纪律。目的：**防止文档体系崩溃**——一旦文档乱了，后续无法恢复，整个研究报废。

本文件是**索引**。详细规则按场景和类别拆到 `scenarios/` 和 `rules/` 子目录，按需 Read。

## 0. 阶段边界（先判断本 skill 该不该上场）

本 skill **只管 Execute 阶段**——方向已选定、Contract 已冻结、进入仿真实现之后。4 个场景（跑实验/加算法/写论文/恢复）全部假设此前提。

**不该用本 skill 的阶段**（用了 = 越界跳步）：
- 方向探索/评判筛选 → 专题 `.sessions/2026-06-10-research-direction-exploration/`
- Groundwork 前置（论文精读/综述/baseline合法性/空白零假设）→ `stages/groundwork.md`, `stages/gw-read.md`
- MVE 本身 → `stages/gw-feasibility.md` §D（必含 FR-11~15）
- Contract（瓶颈诊断/参数溯源/动作空间/信息增量）→ `stages/contract.md`

⚠️ **常见跳步**：候选筛出后直接想跑 MVE。正确链 = 筛选 → Groundwork 前置 → 合规 MVE → Contract → Execute（本 skill）。

## 1. 核心 5 条（任何场景必守）

1. **信道共享**：必须用 `generate_shared_realization()`，禁止独立生成信道（TL-13 根因）
2. **元数据注入**：结果必须用 `save_results()`，禁止裸 `json.dump`（CP-4）
3. **参数溯源**：参数必须从 `params.py` 导入并标 `AuditFlag`，禁止硬编码（包括 `params.py` 内部 `default_factory=lambda: X(...)` 形式）
4. **公式来源**：公式必须从 `毕设/formulas-master.md` 取，禁止从 archive 或子文件取
5. **约定变更**：参数值/公式形式/信号模型/评估方法变更 → 必须在 handoff"约定变更"段记录 + 写使用日志

详见 `rules/tech.md` 和 `rules/doc-discipline.md`。

## 2. 场景路由

```
任务识别决策树（按顺序判断）：

1. 用户指令模糊（无具体算法/参数/操作类型）？
   → 场景 D Step 0（反问澄清）：scenarios/recover.md
2. 新对话第一次接触项目？
   → 场景 D（新对话恢复）：scenarios/recover.md
3. 改 params.py（加字段 / 改 CRITICAL 参数值）？
   → 场景 A（跑实验）必读"特例"段 + 场景 B（新参数模板）
4. 改 .py 代码？
   - 新建文件或改 common/ → 场景 B（加新算法）：scenarios/add.md
   - 只改 experiments/ 参数 → 场景 A（跑实验）：scenarios/run.md
5. 改 .md 论文文件且引用数字？
   → 场景 C（写论文）：scenarios/write.md
```

两者都做：按主任务选场景。主任务判定 = **用户最后一句强调的动词**（如"加 BPS 跑验证写论文"主任务 = 加 BPS）。如无法判定，**显式反问用户**，不允许默认选择。

## 3. 子文件索引

| 类别 | 文件 | 何时读 |
|------|------|-------|
| 场景 A | `scenarios/run.md` | 跑实验、改参数、复现结果 |
| 场景 B | `scenarios/add.md` | 加新算法、新模块、新参数 |
| 场景 C | `scenarios/write.md` | 写论文、引用数字 |
| 场景 D | `scenarios/recover.md` | 新对话恢复（最高风险） |
| 硬约束 | `rules/constraints.md` | 任何场景开始前 |
| 技术规则 | `rules/tech.md` | 写代码前 |
| 文档纪律 | `rules/doc-discipline.md` | 改任何 .md 前 |
| 中断协议 | `rules/interrupt.md` | 怀疑违规时 |
| 归档流程 | `rules/archive.md` | formulas-master 接近上限时 |
| 增量方向扫描 | `rules/adaptation-scan.md` | 跑 MVE/Contract/Execute 实验前找增量方向时 |
| 使用日志 | `rules/usage-log.md` | 每次任务结束时（强制） |
| 月度审计 | `rules/audit-skill.md` | 每月维护 skill 时 |

## 4. 触发时机

**显式触发**（用户说）：
- "跑仿真" / "跑实验" / "跑脚本"
- "加新算法" / "实现 XXX 方法"
- "验证结果" / "验证 BER"
- "改参数" / "调参"
- "写论文" / "引用数字"
- "继续昨天的仿真" / "恢复工作"

**隐式触发**（操作触发）：
- 修改 `projects/simulation/common/` 下任何文件
- 修改 `projects/simulation/params.py`
- 创建新的 `projects/simulation/experiments/` 脚本
- 在 `毕设/` 下改公式或结论

## 5. 快速自检命令

```bash
# 参数审计
cd projects/simulation && ~/.venvs/torch/bin/python -c "
from params import SimulationConfig, audit_params
r = audit_params(SimulationConfig())
print(f'CRITICAL: {r[\"summary\"][\"critical\"]}, DEAD: {r[\"summary\"][\"dead\"]}')
"

# 文档大小检查（formulas-master 预警线 2400）
wc -l 毕设/CONCLUSIONS.md 毕设/formulas-master.md 毕设/TERMS.md

# 全量测试
cd projects/simulation && ~/.venvs/torch/bin/python -m pytest tests/ -q

# 约定变更审计（每对话结束前）
git diff --name-only | grep -E "params.py|formulas-master.md|CONCLUSIONS.md"
# 如有匹配，最新 handoff 必须含"约定变更"段（详见 doc-discipline.md）

# 使用日志验证（事后审计，B 方案）
LOG=.sessions/sim-preflight-log/usage-$(date +%Y-%m).md
test -f "$LOG" && echo "本月已写日志" || echo "⚠️ 本月无日志，可能漏写（见 usage-log.md）"
```

## 6. 维护原则（强制）

- **skill 演进必须基于使用日志证据，不凭感觉**：改 skill 前，先跑 `rules/audit-skill.md` 的审计命令，列出失效规则
- **示例数字必须是格式占位**，不抄真实数字（真实数字会过期）。任何文件中出现具体数字 → 必须从真相源 grep 验证后再用
- **新增规则必须更新 CHANGELOG.md**，记录"日期 + 改动摘要 + 影响的规则编号 + 触发证据（来自 usage-log）"
- **月度审计**：每月初跑 `rules/audit-skill.md`，输出报告 → 改 skill → 写 CHANGELOG
