# 关键技术规则

每条规则有"要求 + 豁免条件 + 违反后果"。所有规则尽量前置门控（开始前承诺），不是事后检查。

## 规则表

| # | 规则 | 要求 | 豁免条件 | 违反后果 |
|---|------|------|---------|---------|
| T1 | 信道共享 | 必须 `generate_shared_realization()` | 单点诊断脚本（不对比 BER） | 假增益（P-05 教训） |
| T2 | 元数据注入 | 必须 `save_results()` | 临时调试输出（不进 results/） | 结果不可追溯 |
| T3 | 参数溯源 | 必须 `params.py` + `AuditFlag` | 一次性实验脚本（标 DEAD） | 参数无来源，结论不可信 |
| T4 | 公式来源 | 必须 `formulas-master.md` | 新推导（须先追加到 master） | 公式版本混乱（VV bug 教训） |
| T5 | 分层验证 | 新算法跑 6 步相关项 | 算法适配矩阵已替换（见 `scenarios/add.md`） | 错误隐藏到端到端才暴露 |
| T6 | 红旗检查 | 结果过 `red_flags.py` | 无 | 种子未传播等静默错误 |

## 前置门控 checklist（开始任务前承诺）

开始任何代码任务前，逐条核对：

- [ ] 我会用 `generate_shared_realization()`，不会自己 `np.random` 生成信道
- [ ] 我会用 `save_results()`，不会裸 `json.dump`
- [ ] 我会从 `params.py` 导入参数，不会硬编码
- [ ] 我会从 `formulas-master.md` 取公式，不会从论文草稿或记忆取
- [ ] 我会在 handoff 记录约定变更

## sigma2_turb 双推导路径

`sigma2_turb` 是 4 个 CRITICAL 参数中最重要的。若用到湍流方差，必须从以下两条路径之一反推：

1. **Rytov 相位结构函数**：从 Rytov 方差 σ_R² 反推相位方差
2. **GG 闪烁指数**：从 Gamma-Gamma 闪烁指数 σ_I² 反推

推导细节见 S002 分析结果。推导结果写入 `params.py` 的 `json_schema_extra`。

## red_flags.py 9 条覆盖范围

`red_flags.py` 当前覆盖的失败维度（已知）：
- 随机种子未传播
- 信道未共享（多方法独立生成）
- 元数据缺失
- 参数未溯源
- 公式编号断裂
- 安全等级误用
- 文档超限
- 拥有者冲突
- 引用 ❌ 结论

**已知盲区**（red_flags 不查，需人工核对）：
- 符号一致性（如 h 在不同章节含义）—— 查 `TERMS.md`
- 单位错误（Hz vs rad/s）—— 查 `params.py` 的 `unit` 字段
- 量纲错误（dB vs 线性）—— 写代码时自查
- 采样率匹配（不同模块的 fs 假设）—— 检查 import
