# 专题：三章审计修复执行

> 创建: 2026-05-22 | 状态: active
> 基于审计专题 S002-S005 的修复项统一执行，先清小改动（无GPU），再开GPU密集任务

## 进展线索

### S001-small-fixes.md — 三章小改动并行修复（2026-05-22）

派 3 个 executor 子 agent 并行处理 Ch1/Ch2/Ch3 全部无 GPU 修复项。
结果：Ch1 A1-A7 代码改造 ✅, Ch2 M4 Jain ✅, Ch3 审计小改动(E03/E10/E12/CV+Overflow) ✅

### S002-topology-upgrade.md — Ch3 完整物理仿真升级（2026-05-22）

Ch3 拓扑从抽象 4-regular 网格升级为 Walker-Delta 物理仿真。关键发现：inc=53° 无法产生极地间隙，改用 inc=86.4° + 纬度阈值 70° 断链。node_feat_dim 6→7（+degree_norm）。4 个尺度全部通过端到端测试。

### H001-topology-upgrade.md — Ch3 拓扑升级交接（2026-05-22）

Ch3 拓扑升级代码完成，交接至新对话执行 GPU 重跑(E01-E12, ~10-15h)。

### S003-gpu-rerun.md — Ch3 GPU 重跑 + 指标体系重构（2026-05-23）

**脚本兼容性修复**：run_seed.py(TypeError)、run_e04_quick.py(拓扑映射)、run_e05_e06.py(拓扑映射)。

**关键发现：GNN/ECMP MLU 比值不是 LEO 路由领域通行指标**。子 agent 调研 8 篇文献确认 LEO 领域主流用 E2E delay、throughput、CV，MLU ratio 仅互联网 TE 领域使用。

**指标体系重构**：加入 E2E delay（传播延迟 + M/M/1 排队延迟），叙事对齐文献主流。M/M/1 模型 `delay_factor = 1/(1-util)` 使 GNN 在 delay 维度反超 ECMP。

**全部 E01-E12 实验完成**。核心结果（66节点，3 seed）：

| 指标 | GNN | ECMP | MLP | GNN/ECMP | GNN/MLP |
|------|-----|------|-----|---------|---------|
| MLU | 1.378 | 1.436 | 1.637 | 0.96 | 0.84 |
| avg_delay(ms) | 137 | 171 | 373 | 0.80 | 0.37 |
| CV | 0.85 | 1.03 | 1.07 | — | — |

- E12 故障模式：11/12 赢，regional 最强 0.85
- E08/E09 消融：全故障率、全流量条件 GNN 赢
- E04-E06 泛化：48/288 有效，720 退化
- E10/E11 架构：3层最优，2头略优

## 已确认结论

### 不变量（继承自审计专题）
1. 三章主题：Ch1 路由 size gen → Ch2 切换 size gen → Ch3 拥塞/故障弹性路由
2. 方法统一叙事："GNN 结构化编码使零样本规模迁移成为可能"
3. 每章必须独立可发表（问题建模→算法设计→实验验证闭环）

### 其他结论
- Ch3 拓扑参数：alt=550km, inc=86.4°, F=1, polar_gap_lat=70°（纬度阈值，非距离阈值）
- Ch3 P×S 映射：48=4×12, 66=6×11, 288=12×24, 720=18×40
- 53° 倾角不可用：288/720 节点面内距离太近，5000km 阈值无效
- Ch3 旧实验数据（4-regular 抽象网格）不可复用，全部已重跑
- 旧代码已归档：git tag `ch3-pre-topology-upgrade`
- **GNN/ECMP MLU 比值非 LEO 路由通行指标**（调研确认），E2E delay 是主流
- **M/M/1 排队延迟模型**：`delay_factor = 1/(1-util)`，拥塞链路延迟被正确放大
- GNN 优势叙事：负载感知选路 → 避免拥塞 → 排队延迟低 → 总 E2E delay 优 20%
- 720 节点零样本泛化退化（10.9x 跨度过大），48/288 节点有效

## 未决项

1. ~~Ch3 GPU 重跑~~ ✅ E01-E12 全部完成
2. **Ch1 GPU 重跑**：5-seed 重跑（~105h）
3. **Ch2 GPU 补实验**：补充 seed + N=30/40 + 乒乓切换率（~6h）
4. **Ch3 paper-materials 更新**：全部表格和叙事需用新数据重写
5. **跨章写作素材**：符号统一表、TELGEN 框架、拓扑差异声明
6. DTAR baseline 复现（Ch3 P2，~1-2天，可选）

## 当前位置

Ch3 全部实验(E01-E12)在新拓扑上完成。待更新 paper-materials.md 和提交代码。下一步：Ch3 论文素材更新 → Ch1/Ch2 GPU 重跑。
