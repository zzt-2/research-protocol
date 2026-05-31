# HGAT 卫星 DAG 任务卸载

> 状态: dormant | 创建: 2026-05-13 | 最后更新: 2026-05-13

## 进展线索

| 编号 | 文件 | 摘要 |
|------|------|------|
| H001 | H001-initial.md | Phase 0-3 完成：修复 3 个致命 bug（入口任务分配、不可达路径返回值、episode seed）、多 IoTD 环境重写（23 节点/200 任务/4600 动作空间）、MDP 试运行 3/3 通过（Greedy -16.7 vs Random -206K）。Phase 4 训练已启动后台运行。 |

## 已确认结论

- 多 IoTD 环境架构已定型：IoTD[0..9] + UAV[10..13] + LEO[14..21] + CS[22]，每 IoTD 独立 LEO 可见性计算
- 3 个致命 bug 已修复：入口任务 input_data 上传时间计算、不可达路径返回 0（非 1bps）、episode_counter seed 递增
- MDP 试运行验证通过：Greedy 策略显著优于 Random，奖励无单一项主导（max 70.3%）
- Random reward 双峰现象属正常（偶发高效分配 vs 全堆 IoTD）

## 未决项

- Phase 4 训练结果：后台 task `b749sh8it`，输出在 `simulator/results_v2/`，待检查完成状态
- Phase 5 baseline report：各方法 500ep x 3 seed 结果表、learning curves、奖励分解对比、与 K2/M01 趋势对比
- 成功标准：HGAT > GraphSAGE > GCN > MLP > Random，且 HGAT vs GraphSAGE 差距 >10%
- 单 IoTD → 多 IoTD 重写后的完整方案文档（当前记录在 `.omc/plans/multi-iotd-refactor.md`）

## 当前位置

Groundwork Step 7 执行中：Phase 0-3 已完成，Phase 4 训练后台运行，等待训练完成后进入 Phase 5 生成 baseline report。
