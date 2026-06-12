# Handoff: 仿真基础设施重建 — 方案已冻结，待执行迁移

> 来源: S002 | 交接目标: 下个对话开始执行 C5 迁移方案
> 文件名: H001-diagnosis-to-design.md

## 已完成边界

1. **18 Agent 深度分析全部完成**：A1-A6 现状审计 + B1-B6 最佳实践 + C1-C6 方案设计
2. **独立架构审查完成**：6方案质量评分、跨方案一致性检查、3个扩展场景验证
3. **3个问题已修复**：P0 真相源冲突、P1 C3行引用、P1 Pydantic v2语法
4. **方案已冻结**：C1-C6 全部冻结，5个已知限制记录但不阻塞
5. **完整记录在 S002**：~800行，含所有发现、数据、建议、审查、修复

## 不要做什么

1. **不要在迁移完成前进入新方向实验** — 基础不可靠则结论不可信
2. **不要缝补旧体系** — 已有方案从问题出发重新设计
3. **不要跳过 Quick Wins 直接做重构** — Quick Wins 是安全网和信心基础
4. **不要改动 C1-C6 冻结方案** — 除非执行中发现具体阻塞问题
5. **不要忽视已知限制** — EKF扩展需~30行重构、formulas-master接近上限

## 必读

1. **S002**（必读，~800行）：完整分析记录，含 Phase 7-12（审计+实践+设计+审查+修复+冻结）
2. **C5 迁移方案**（必读，695行）：`.sessions/.../C5-migration-plan.md` — 执行时按此方案逐步推进
3. **topic-index.md**（必读）：专题进展、已确认结论、已知限制

## 关键上下文

### 用户约束与意图
- 硕士论文，题目"星地湍流信道激光通信处理技术研究"
- 用户希望"稳"：照着别人已有研究稍微扩展
- 用户重视基础设施质量：参数有来源、结果有验证、代码可维护
- 用户对文档膨胀非常敏感：要求长期可持续、不消耗心力
- 用户要求从实际踩过的坑反推设计，不要缝补
- 用户强调"这些是珍贵资料"——发现必须完整记录

### 6 条设计原则（已验证覆盖度）
1. 参数必须有来源且单一真相源
2. 决策必须有背景
3. 验证必须在节点强制执行
4. 信息必须跨对话连续
5. 红旗信号必须自动触发
6. 恢复成本必须可控

### C5 迁移方案 8 阶段摘要

| 阶段 | 内容 | 预计时间 | 依赖 |
|------|------|---------|------|
| Phase 0 | 安全网：git分支+基线测试 | 5min | 无 |
| Phase 1 | Quick Wins：提交common.py+清理registry+pytest | 10min | Phase 0 |
| Phase 2 | 验证基础设施：conftest.py+checkpoints.py | 20min | Phase 1 |
| Phase 3 | 参数溯源：params.py+SPEC自动生成 | 40min | Phase 2 |
| Phase 4 | 代码模块化：拆分common.py为7模块+垫片 | 40min | Phase 3 |
| Phase 5 | 分层验证：test_layered_verification.py | 20min | Phase 4 |
| Phase 6 | 文档清理：去冗余+注册表+成熟度标签 | 30min | 独立于Phase 2-5 |
| Phase 7 | Handoff改进：模板+双区topic-index | 15min | 独立于Phase 2-5 |
| Phase 8 | 最终验证：全量测试+脚本兼容性 | 10min | 全部 |

### 架构审查关键结论

- **扩展性**：新参数/新实验=优秀，新验证/文档=良好，新算法/新信道=部分支持
- **最易扩展方向**：突发感知KF（~335行新增，0行改现有代码）
- **需小幅重构方向**：EKF（~30行改_kf.py提取共享逻辑）
- **总体评价**：方案对"稳"的定位匹配，后续多为在现有框架上扩展

### 已知限制（不阻塞迁移）

1. EKF 扩展需~30行重构 `_kf.py`
2. `gg_block` 默认参数 `bs=BLOCK` 创建导入时耦合
3. `formulas-master.md` 2260行接近2500上限
4. 成熟度标签无自动强制执行
5. C4 ROT审计频率需实际测试后调整

## 接口变更

无代码改动。已创建的设计文档（不涉及运行时接口）：
- `projects/simulation/DESIGN-modular-split.md` — 代码模块化设计
- `projects/simulation/params_design.md` — 参数溯源设计
- `projects/simulation/tests/INTEGRATION_PLAN.md` — 验证集成设计
- `.sessions/.../C4-documentation-architecture.md` — 文档架构设计
- `.sessions/.../C5-migration-plan.md` — 综合迁移方案
- `.sessions/.../C6-handoff-session-management.md` — Handoff改进设计

B4 已创建的测试文件（可运行）：
- `projects/simulation/tests/test_common.py`（69个测试）
- `projects/simulation/tests/red_flags.py`（9条红旗规则）
- `projects/simulation/tests/VERIFICATION.md`（验证检查点文档）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| SPEC.md 37% 参数无来源 | P1 | A1审计完成，C2方案冻结 | Phase 3 执行时统一补全 |
| kappa 死参数 | P1 | A1发现，C2标记DEAD | Phase 3 执行时移除 |
| Q_fine_df 覆盖未记录 | P1/P2 | A1发现 | Phase 3 执行时记录 |
| 附录 G 过时 | P4/P6 | A3发现 | Phase 6 执行时重写 |
| 9 个已归档专题仍标 active | P4/P6 | A4发现 | Phase 1 Quick Win 清理 |
| 公式文档 ~1750 行冗余 | P6 | A5发现 | Phase 6 执行时去冗余 |
| common.py 129 行未提交 | P3 | A6发现 | Phase 1 Quick Win 提交 |
| thesis-direction-pivot 应 dormant | P6 | A4发现 | Phase 1 Quick Win 标 dormant |
| sigma2_turb 零来源 | P1 | CRITICAL，C2有两条推导路径 | Phase 3 执行时推导补全 |

## 验证阈值

| 验证项 | PASS 标准 | 来源 |
|--------|----------|------|
| Quick Wins | common.py已提交 + registry已清理 + pytest通过 | C5 Phase 1 |
| 参数溯源 | SPEC.md 每个参数有来源（至少assumption级别） | C2 方案 |
| 代码模块化 | 27脚本全部零改动运行 | C1 方案 + 附录A审计 |
| 文档去冗余 | 公式7→3文件，减少~1750行 | C4 方案 |
| 全量测试 | 69 pytest + 分层验证通过 | C3 方案 |
| 扩展性 | 新算法/参数/实验可零改动加入 | 架构审查验证 |

## 接收方验证

- [x] 已读取 topic-index 的不变量段落
- [x] 已确认方案已冻结（C1-C6 + 3个修复）
- [x] 已确认迁移执行顺序（C5 8阶段）
- [x] 已确认当前范围：执行迁移，不做新方向实验
- [x] 已了解已知限制（5项，不阻塞）

## 下一轮

1. 执行 Phase 0：创建 git 分支 `refactor/simulation-foundation`，运行 pytest 基线
2. 执行 Phase 1 Quick Wins：提交 common.py、清理 _registry.yaml、运行 pytest
3. 按 C5 方案逐阶段执行，每阶段完成后验证
