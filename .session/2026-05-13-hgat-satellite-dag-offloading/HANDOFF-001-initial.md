# Handoff 2026-05-13

## 当前进度
- 阶段：Groundwork Stage 7
- 状态：Phase 4 训练后台运行中
- 本轮完成：Phase 0-3 全部完成（bug 修复 + 多 IoTD 环境重写 + MDP 试运行）

## 本轮改动

### Phase 1: 修复 3 个致命 bug
1. `environment.py` step(): 入口任务分配到非 IoTD 节点时计算 input_data 上传时间
2. `environment.py` _get_link_rate(): 不可达路径返回 0 而非 1 bps
3. `environment.py` run_*_episode(): episode_counter 递增 seed

### Phase 2: 多 IoTD 环境重写
- `dag.py`: 新增 MultiDAGBundle + get_ready_tasks_multi + DAGTask.owning_iotd 字段
- `environment.py`: 完整重写（23 节点, 200 任务, 4600 动作空间）
  - 节点布局: IoTD[0..9] UAV[10..13] LEO[14..21] CS[22]
  - 每 IoTD 独立 LEO 可见性计算
  - _build_graph: task→owning_iotd 边, 每 IoTD 独立 LEO 可见性
- `models_hgat.py`: n_actions 改为构造函数参数
- `models_homo.py`: 清理未使用 import
- `train.py`: 先建 env 取 n_actions 再建 model
- `dqn_train.py`: 同上
- `config.py`: N_IOTD 100→10

### Phase 3: MDP 试运行 3/3 通过
- Greedy(-16.7) vs Random(-206K)
- 奖励无单一项主导（max 70.3%）

## 关键上下文
- 训练后台 task ID: `b749sh8it`
- 训练输出: `simulator/results_v2/`
- Random reward 双峰是正常的（偶把任务分到高效节点 vs 堆在 IoTD）

## 下一步
1. 等训练完成（检查 `results_v2/` 下文件）
2. Phase 5: 生成 `baseline_report.md`
   - 各方法 500ep × 3 seed 结果表
   - Learning curves 图
   - 奖励分解对比
   - 与 K2/M01 趋势对比
3. 成功标准: HGAT > GraphSAGE > GCN > MLP > Random, HGAT vs GraphSAGE 差距 >10%

## Git commits
- `86f72cc` → checkpoint: pre-multi-iotd
- `feat(hgat): 修复 3 个致命 bug（Phase 1）`
- `feat(hgat): Phase 2 多 IoTD 环境重写 + Phase 3 MDP 试运行通过`
