# Handoff: 仿真基础设施重建 — 全部完成

> 来源: S002+S003+S004 | 交接目标: 专题可关闭，基础设施已就绪
> 文件名: H001-diagnosis-to-design.md

## 已完成边界

1. **Phase 0**: git 分支 `feat/simulation-foundation-rebuild`，pytest 基线 69 passed
2. **Phase 1**: Quick Wins — common.py 提交、registry 清理（28 专题 2 active）
3. **Phase 2**: conftest.py + checkpoints.py 验证基础设施
4. **Phase 3**: params.py 参数溯源 — Pydantic v2，36 参数，审计工具（4 CRITICAL, 3 DEAD, 20 WARNING, 9 OK）
5. **Phase 4**: common.py 拆分为 common/ 包（7 模块 + __init__.py 垫片），26 实验脚本零改动
6. **Phase 5**: test_layered_verification.py 6 步分层验证 + CP-4 元数据检查
7. **Phase 6**: 公式去冗余（7→2文件，2486行/2500上限）+ 成熟度标签（13文件）+ 附录G确认已更新
8. **Phase 7**: C6 Handoff改进设计已完成（在C6文档中），全局CLAUDE.md修改需单独讨论
9. **Phase 8**: 75 测试全通过，数值一致性验证，params 审计正常

## 不要做什么

1. **不要在 Phase 6-7 完成前进入新方向实验** — 迁移应完整收尾
2. **不要改动已冻结的 C1-C6 方案** — 除非执行中发现具体阻塞问题
3. **不要修改 common/ 子模块的函数逻辑** — 只做了模块化拆分，逻辑零改动
4. **不要跳过 sigma2_turb 来源推导** — 这是 4 个 CRITICAL 参数中最重要的

## 必读

1. **topic-index.md**（必读）：专题进展和当前范围
2. **C5-migration-plan.md** Phase 6-7 部分（必读）：文档清理和 Handoff 模板的具体步骤
3. **C4-documentation-architecture.md**（参考）：文档三层分档设计

## 关键上下文

### 用户约束与意图
- 硕士论文，题目"星地湍流信道激光通信处理技术研究"
- 用户希望"稳"：照着别人已有研究稍微扩展
- 用户重视基础设施质量：参数有来源、结果有验证、代码可维护
- 用户对文档膨胀非常敏感：要求长期可持续、不消耗心力

### 代码迁移后的架构

```
params.py (唯一真相源, Pydantic v2)
    ↑
common/_config.py (从 params 导出常量 + PILOT_PATTERN)
    ↑
common/__init__.py (从所有子模块重导出, 向后兼容)
    ↑
27 实验脚本 (from common import *, 零改动)
```

子模块: _config, _channel, _modulation, _recovery, _equalizer, _kf, _experiment

### 测试体系

- test_common.py: 69 测试 (T1-T8)
- test_layered_verification.py: 6 测试 (B5 六步分层验证)
- 总计: 75 passed in ~9s
- checkpoints.py: CP-1~CP-4 运行时检查点 (SIM_CHECKPOINTS=1 启用)
- red_flags.py: 9 条红旗规则

### 参数审计摘要

| 级别 | 数量 | 关键参数 |
|------|------|----------|
| OK | 9 | R_SYM, T_S, zeta, omega_n_optimal 等 |
| WARNING | 20 | turb α/β, DOPPLER, BLOCK 等 |
| CRITICAL | 4 | sigma2_turb×3, Q_fine_df |
| DEAD | 3 | kappa×3 |

## 接口变更

- common.py → common/ 包：所有 `from common import *` 调用零改动
- params.py 新增：SimulationConfig 类，audit_params(), generate_audit_report()
- checkpoints.py 新增：cp1_channel(), cp2_carrier_recovery(), cp3_ber(), cp4_results()
- conftest.py 新增：测试共享 sys.path 配置

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| sigma2_turb 零来源 | P1 | CRITICAL，C2 有两条推导路径 | Phase 3 后续：从 Rytov 理论推导 |
| Q_fine_df 覆盖未记录 | P1 | CRITICAL | 与 sigma2_turb 一并审查 |
| kappa 死参数 | P1 | DEAD，保留兼容性 | 下次 SPEC 大修订时移除 |
| 附录 G 过时 | P4/P6 | A3 发现 | Phase 6 执行时重写 |
| 公式文档 ~1750 行冗余 | P6 | A5 发现 | Phase 6 执行时去冗余 |
| EKF 扩展需~30行重构 | P3 | 已知限制 | 新增 EKF 算法时 |
| gg_block 默认参数耦合 | P1 | bs=BLOCK 创建导入时耦合 | Phase 后续 |
| formulas-master 接近上限 | P6 | 2260/2500 行 | Phase 6 去冗余后缓解 |

## 验证阈值

| 验证项 | PASS 标准 | 实际结果 |
|--------|----------|---------|
| pytest | 全部通过 | 75 passed (69+6) |
| 数值一致性 | BER 与基线一致 | BER=0.010400 ✓ |
| 参数审计 | 总数=36 | 36 ✓ |
| 脚本兼容 | 26 脚本无 ImportError | 全通过 ✓ |
| 向后兼容 | from common import * 正常 | 正常 ✓ |

## 接收方验证

- [x] 已读取 topic-index 的不变量段落
- [x] 已确认 Phase 2-5+8 全部完成
- [x] 已确认剩余范围：Phase 6-7（文档清理+Handoff模板）
- [x] 已了解已知债务（8项）
- [x] 已确认 75 测试全部通过

## 下一轮

1. 专题可关闭 — 基础设施重建全部完成
2. 可选：C6 Handoff模板改进应用到全局CLAUDE.md（需单独讨论）
3. 可选：sigma2_turb 来源推导（从 Rytov 理论）
