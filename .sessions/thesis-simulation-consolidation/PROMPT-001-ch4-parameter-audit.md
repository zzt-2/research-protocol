# PROMPT-001: Ch4 代码+参数审计

> 专题: thesis-simulation-consolidation | 续接: S001
> Python: `~/.venvs/torch/bin/python`
> 工作目录: `projects/thesis-figures/simulation/`（旧）+ `projects/simulation/`（新）

## 背景

S001 完成了仿真规范合并（SIM-SYSTEM.md + SIMULATION_SPEC.md → SPEC.md），确认了 D1/D2 评估方法实际一致（resolve_qpsk 统一使用），建立了新项目目录 `projects/simulation/`。

**本轮目标**：对 Ch4 全部代码做参数级审计，产出干净的代码清单 + 可靠结论清单。不跑新实验，只验证已有代码和结论。

## 必读（按顺序）

1. **`projects/simulation/SPEC.md`** — S001 合并后的唯一真相源
2. **`.sessions/thesis-simulation-consolidation/topic-index.md`** — 当前状态
3. **`thesis-lessons.md`** — TL-01 到 TL-19

## 审计范围

### 旧目录文件（projects/thesis-figures/simulation/）

| 文件 | 状态 | 本次审计重点 |
|------|------|-------------|
| `sim_ch4_systematic_analysis.py` | 参考值 | VV/DPLL π/4 偏移是否已处理 |
| `sim_ch4_kf_pilot_h.py` | 有保留价值 | KF 实现参数、TL-13 违规 |
| `sim_ch4_kf_verification.py` | 参考值 | 公平性检查 |
| `sim_ch4_kf_perblock_h.py` | 废弃 | DD 崩溃确认（仅确认参数） |
| `sim_ch4_kf_carrier_sync.py` | 废弃 | P-matrix bug 确认（仅确认参数） |
| `sim_kf_stress_common.py` | 活跃 | VV 公式、KF 参数、共享信道实现 |
| `sim_kf_stress_A1_A2_A3.py` | 活跃 | 依赖 common.py 的参数是否正确 |
| `sim_kf_stress_A4_A5.py` | 活跃 | 同上 |
| `sim_kf_stress_B1_B2.py` | 活跃 | 同上 |
| `sim_kf_stress_B3_B4_B5.py` | 活跃 | 同上 |
| `sim_kf_stress_C1_C2_C3.py` | 活跃 | 同上 |
| `sim_kf_stress_C4_C5.py` | 活跃 | 同上 |
| `sim_kf_stress_D1_D2.py` | 活跃 | 同上 |
| `sim_kf_stress_D3_D4_D5.py` | 活跃 | 同上 |
| `verify_systematic.py` | 参考值 | 同上 |

### 新目录文件（projects/simulation/）

| 文件 | 状态 | 本次审计重点 |
|------|------|-------------|
| `common.py` | S001 新建 | 参数与旧代码一致性 |
| `SPEC.md` | S001 合并 | 内容完整性 |
| `archive/README.md` | S001 创建 | 旧文件索引准确性 |

## 审计任务

### 任务 1：参数一致性矩阵

构建参数矩阵，对比所有文件中的关键参数：

| 参数 | SPEC.md 值 | common.py | stress_common.py | systematic | kf_pilot_h |
|------|-----------|-----------|-----------------|------------|------------|
| R_SYM | 2.5e9 | ? | ? | ? | ? |
| T_S | 400e-12 | ? | ? | ? | ? |
| LASER_LW | 10e3 | ? | ? | ? | ? |
| F_RESIDUAL | 1e6 | ? | ? | ? | ? |
| BLOCK | 100 | ? | ? | ? | ? |
| weak α | 4.0 | ? | ? | ? | ? |
| weak β | 3.0 | ? | ? | ? | ? |
| mod α | 2.5 | ? | ? | ? | ? |
| mod β | 1.8 | ? | ? | ? | ? |
| strong α | 1.5 | ? | ? | ? | ? |
| strong β | 0.8 | ? | ? | ? | ? |
| γ̄ default | 20dB | ? | ? | ? | ? |
| 信号模型 | √h·s | ? | ? | ? | ? |

任何不一致标记为 ❌。

### 任务 2：函数一致性审计

对比核心函数在不同文件中的实现：

1. **resolve_qpsk**：所有 10+ 个定义是否一致？
2. **ber_count**：所有定义是否一致？
3. **generate_signal / generate_rx**：信号生成是否遵循 r=√h·s·exp(jφ)+n？
4. **VV 相位估计**：`unwrap(angle*M)/M`（stress_common）vs `unwrap(angle)/M`（systematic）vs 新 common.py？
5. **DPLL 实现**：各文件是否一致？
6. **KF 实现**：stress_common vs kf_pilot_h 的 KF 核心循环是否一致？
7. **MMSE 均衡**：`rx*√h/(h+1/γ̄)` 在所有文件中是否一致？

### 任务 3：已知 Bug 状态确认

逐项确认 SPEC.md 中列出的已知 bug 的实际状态：

| Bug | 声称状态 | 代码行证据 | 实际状态 |
|-----|---------|-----------|---------|
| VV π/4 偏移 | 已确认未修 | ? | ? |
| resolve_qpsk 掩盖 CPR 失效 | 已确认 | ? | ? |
| P-matrix 重置 | 已确认，文件废弃 | ? | ? |
| VV unwrap(angle*M)/M | stress_common 有 | ? | ? |
| TL-13 违规 | stress 已修 | ? | ? |

### 任务 4：结论可靠性标记

对 SIMULATION_SPEC.md（旧）§5 的 13 条"已验证事实"和新 SPEC.md 中的结论，逐条标记：

- ✅ **已验证**：有代码证据 + 多种子验证
- ⚠️ **条件性成立**：在特定条件下成立，需标注条件
- ❌ **已证伪**：有明确反证
- 🔍 **待重验**：证据不足或方法有疑点

每条结论附：验证来源（文件:行号）、验证方法（种子数、参数范围）、置信度。

## 不要做什么

- **不跑新实验**——只读代码和已有结果
- **不修改任何代码**
- **不做方向判断**——不评判"KF 该不该用"、"系统性分析够不够"等问题
- **不更新 thesis-status.md 或 thesis-lessons.md**
- **不读 Ch3 代码**——Ch3 有独立的审计对话

## 输出格式

```
# Ch4 代码+参数审计报告

## 审计摘要
- 审计文件数：X
- 参数不一致：X 处
- 函数不一致：X 处
- Bug 确认：X/Y 项

## 任务 1：参数一致性矩阵
[表格]

## 任务 2：函数一致性
[逐函数对比]

## 任务 3：Bug 状态
[表格]

## 任务 4：结论可靠性
| # | 结论 | 标记 | 来源 | 条件/说明 |
|---|------|------|------|----------|

## 关键发现
[最重要的 3-5 个发现]
```

## 完成后

1. 写审计报告到 `.sessions/thesis-simulation-consolidation/S002-ch4-audit-report.md`
2. 更新 `topic-index.md`：新增 S002 进展线索 + 更新未决项
3. 不需要写 handoff——审计结果是最终交付物，用户直接读取即可
