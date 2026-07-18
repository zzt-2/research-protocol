---
name: sim-preflight
description: 仿真前必看流程。触发场景：跑仿真/实验脚本、改实验参数、加新算法（载波恢复/KF/DPLL/VV/BPS/均衡）、验证 BER 或相位估计结果、为论文引用仿真数字、修改 common/ 或 params.py、新对话恢复仿真工作。强制按文档纪律操作，防止文档体系崩溃。遗漏即中断。
version: 1.3.1
last_updated: 2026-07-10
changelog: ./CHANGELOG.md
---

# 仿真前必看流程（sim-preflight）

本 skill 是 `projects/simulation/` 仿真体系的操作纪律。目的：**防止文档体系崩溃**——一旦文档乱了，后续无法恢复，整个研究报废。

本文件是**索引**。详细规则按场景和类别拆到 `scenarios/` 和 `rules/` 子目录，按需 Read。

## 0. 阶段边界（先判断本 skill 该不该上场）

本 skill **只管 Execute 阶段**——方向已选定、Contract 已冻结、进入仿真实现之后。4 个场景（跑实验/加算法/写论文/恢复）全部假设此前提。

**不该用本 skill 的阶段**（用了 = 越界跳步）：
- 方向探索/评判筛选 → 专题 `.sessions/2026-06-10-research-direction-exploration/` 或 `.sessions/2026-07-10-equalization-layer-direction-scouting/`（均衡层方向侦察）
- Groundwork 前置（论文精读/综述/baseline合法性/空白零假设/方法-改进矩阵）→ `stages/groundwork.md`, `stages/gw-read.md`, 对应专题 `.sessions/*-direction-scouting/`
- MVE 本身 → `stages/gw-feasibility.md` §D（必含 FR-11~15）
- Contract（瓶颈诊断/参数溯源/动作空间/信息增量）→ `stages/contract.md`

⚠️ **常见跳步**：候选筛出后直接想跑 MVE。正确链 = 筛选 → Groundwork 前置 → 合规 MVE → Contract → Execute（本 skill）。

⚠️ **均衡层专题特别提示**（2026-07-10）：`.sessions/2026-07-10-equalization-layer-direction-scouting/` 的阶段 0-4a（流程规划/地勘/精读/判读/Go-NoGo）全在 GW 范围内，**不用本 skill**。阶段 5 MVE（若 Go）才用本 skill。方向侦察阶段守的是 session-governance + D017 v2 + D018 + §7.2 + glossary 四判据，不是本 skill 的 5 条核心。

## 1. 核心 5 条（任何场景必守）

1. **信道共享**：必须用 `generate_shared_realization()`，禁止独立生成信道（TL-13 根因）
2. **元数据注入**：结果必须用 `save_results()`，禁止裸 `json.dump`（CP-4）
3. **参数溯源**：参数必须从 `params.py` 导入并标 `AuditFlag`，禁止硬编码（包括 `params.py` 内部 `default_factory=lambda: X(...)` 形式）。**v1.2.0 扩展**：同一物理量（线宽/符号率/噪声/衰落）跨场景必须从 params.py **单一字段**读，禁止函数默认参数固化（`def f(..., lw=LASER_LW)`）、禁止跨模块同义常量（`_b11_params.CLW_B11` vs `params.LASER_LW`）——详见 `rules/param-source.md`
4. **公式来源**：公式必须从 `毕设/formulas-master.md` 取，禁止从 archive 或子文件取
5. **约定变更**：参数值/公式形式/信号模型/评估方法变更 → 必须在 handoff"约定变更"段记录 + 写使用日志

详见 `rules/tech.md`、`rules/param-source.md` 和 `rules/doc-discipline.md`。

## 1.5 实验设计扎实性自检（C1-C5，跑任何新实验前必过）

> 来源：导师 2026-07-07 反馈抽象的通用清单（详见 `projects/simulation/REVIEW_NOTES.md` §二）。这五条是"通信物理层仿真做扎实"的通用要求，跨方向通用。

| # | 维度 | 自检问题 | 触发时机 |
|---|------|---------|---------|
| **C1** | 关键参数必须扫描，不能单点 | 我的关键参数（SNR/线宽/速率/衰落强度）是只测一个点还是扫了范围？单点结论站得住吗？ | 实验设计时 |
| **C2** | 评估指标对齐领域标准，区分 pre/post-FEC | 评估阈值是 pre-FEC 还是 post-FEC？HD-FEC 还是 SD-FEC？跟领域惯例一致吗？ | 实验设计时 |
| **C3** | 对比对象够档级（近年顶刊），不只对老经典 | baseline 有几篇近年(2022+) IEEE Transactions 级？方法来源本身是 Trans 还是 Letters？**精读分层**（2026-07-10 补）：baseline 必须 Trans 级（D-010 标准 4），但思路来源可含 Letters/会议（做"扩写溯源"——已扩成 Trans 读 Trans，未扩写读本身，常是新想法第一篇如 Du PTL 2025）；红线：Letters/会议不能当主 baseline | baseline 选定时 + 投稿前 |
| **C4** | 场景描述与实验设置严格一致 | 我写的损伤（论文/简报）和代码实际建模的损伤逐项对应吗？有没有"写了但没测"或"测了但没写"的参数？ | 写文档时 + 投稿前 |
| **C5** | 场景选择要论证，不能照搬文献默认值 | 我选这个场景有具体理由吗？最能体现方法价值，还是最方便？ | 场景设计时 |

**触发时机**：不要求每次主动查，但以下时刻**必须**逐条核对：① 准备投稿前（C1-C5 全过）② 老师/审稿人反馈后（看反馈指向哪条）③ 开新方向跑实验前（C1/C2/C5 先想清楚再跑）。

**C1/C2 是"实验设计扎实性"，C3 是"学术定位扎实性"，C4/C5 是"场景严谨性"。** 本项目 2026-07-07 的线宽根因正是 C1（单点 500kHz 当通用）+ C4（简报写 500kHz 但湍流实为 10kHz）双重违反。

## 1.6 算法正确性自检（C6-C8，MVE/sandbox/对照实验前必过）

> 来源：NDA-ML D-007~D-009 教训（consistency PASS 但算法错 / vs 祖师爷持平当合理 / 参数变更掩盖 bug）。这三条是"算法层正确性"通用要求，跟 C1-C5 的"实验设计扎实性"正交。详见 `rules/mve-validation.md`。

| # | 维度 | 自检问题 | 触发时机 |
|---|------|---------|---------|
| **C6** | 公式来源逐项核对，禁靠文字重建 | 核心公式是否从原 PDF 核对并标页码+公式号？PDF→md 转换把公式转 picture omitted 时是否标红不硬磕？ | MVE-SPEC 设计 / 实现算法时 |
| **C7** | MVE/sandbox 必含三方对照（消融+祖师爷） | 验证是否含"我们的方法 / naive消融 / 祖师爷经典"三方？缺任一方归因不可信 | MVE / sandbox 设计时 |
| **C8** | "vs 祖师爷方法持平"即警报 | 结果跟领域经典方法（VV 1983/Gardner 1986/BPS）持平时，是否立即查数学同族性？是否当"合理结果"默默接受？ | 任何 vs 经典方法对照出结果时 |

**C6 是"实现忠实原文"，C7 是"消融+对照完备性"，C8 是"创新性警报"。** 本项目 NDA-ML D-008 三重违反：C6（漏读 B11 Eq.16 ML 加权）/ C7（sandbox 只两方无祖师爷）/ C8（vs VV 持平当合理接受长达 2 session）。

**强制触发**：MVE PASS 判 Go 前，C6-C8 必须全过（详见 `rules/mve-validation.md` V1-V6 清单）。

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
| **参数真相源（v1.2.0）** | `rules/param-source.md` | **写信道函数 / 写 sweep 脚本 / 跨场景比较前** |
| **MVE 算法正确性（v1.3.0）** | `rules/mve-validation.md` | **MVE 设计/sandbox 验证/对照实验/参数变更重跑前** |
| **增量方向扫描（v1.2.1）** | `rules/adaptation-scan.md` | **MVE/Contract/Execute 前找增量方向时 + Kill 前必跑 6 类适配（B5 教训）** |
| 文档纪律 | `rules/doc-discipline.md` | 改任何 .md 前 |
| 中断协议 | `rules/interrupt.md` | 怀疑违规时 |
| 归档流程 | `rules/archive.md` | formulas-master 接近上限时 |
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

# 参数真相源统一审计（v1.2.0，详见 rules/param-source.md）
# 1. 函数默认参数固化（def 签名里直接绑模块常量，import 时冻结）
grep -rn "def [a-z_]*([^)]*=[A-Z_]" projects/simulation/ --include="*.py" || echo "OK: 无默认参数固化"
# 2. 跨模块同义常量（同一物理量多处定义）
grep -rn "LASER_LW\|CLW\b\|R_SYM\|BAUD\b" projects/simulation/ --include="*.py" | grep -v "import\|#" | head

# 使用日志验证（事后审计，B 方案）
LOG=.sessions/sim-preflight-log/usage-$(date +%Y-%m).md
test -f "$LOG" && echo "本月已写日志" || echo "⚠️ 本月无日志，可能漏写（见 usage-log.md）"
```

## 5.1 算法正确性自检（C6-C8，v1.3.0）

```bash
# C6: 核心公式是否标页码+公式号（无标注 → 补核对）
grep -rE "Eq\.|equation|p\.[0-9]|公式" projects/simulation/explore/*/  --include="*.py" --include="*.md" | grep -E "[0-9]" | head

# C7: MVE/sandbox 是否含三方对照（不足 3 个 → 补消融或祖师爷）
grep -rE "from common import|from common._recovery import" projects/simulation/explore/*/  --include="*.py" | grep -oE "(vv_cpr|bps_cpr|nda_ml|da_ml|gardner|dpll|kf_)" | sort -u

# C8: 最近 results 是否有 vs 祖师爷方法持平（|gain|<0.05dB 或 BER ratio [0.95,1.05]）
grep -rE "gain.*0\.0[0-9]|ratio.*0\.9[5-9]|ratio.*1\.0[0-5]" projects/simulation/results/ projects/simulation/explore/*/  2>/dev/null | head
# 如有 vs VV/BPS/Gardner 持平 → 查数学同族性（见 interrupt.md 第 10 条）

# V4: 参数变更是否触发算法重审（查最近 params.py 改动）
git diff HEAD~3 -- projects/simulation/params.py | grep -E "^\-.*[0-9]|^\+.*[0-9]" | grep -iE "lw|linewidth|baud|r_sym|sigma2|kappa"
# 如有 CRITICAL 参数改动 → 检查同 commit 是否同时改算法或跑 sandbox
```

## 6. 维护原则（强制）

- **skill 演进必须基于使用日志证据，不凭感觉**：改 skill 前，先跑 `rules/audit-skill.md` 的审计命令，列出失效规则
- **示例数字必须是格式占位**，不抄真实数字（真实数字会过期）。任何文件中出现具体数字 → 必须从真相源 grep 验证后再用
- **新增规则必须更新 CHANGELOG.md**，记录"日期 + 改动摘要 + 影响的规则编号 + 触发证据（来自 usage-log）"
- **月度审计**：每月初跑 `rules/audit-skill.md`，输出报告 → 改 skill → 写 CHANGELOG
