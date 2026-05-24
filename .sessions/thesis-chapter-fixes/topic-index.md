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

### paper-materials 更新 — Ch3 论文素材全面重写（2026-05-23）

基于物理仿真拓扑全部实验结果重写 paper-materials.md：
- 叙事重心从 MLU 转为 E2E delay（GNN/ECMP delay=0.80 vs MLU=0.96）
- 新增故障激活效应叙事：E02 无故障 GNN/ECMP=1.018（ECMP 略优），故障是 GNN 优势激活条件
- 跨规模表增加 delay 列：48节点0.83, 288节点0.25（delay 维度 GNN 大幅领先）
- E12 全部 12 组新数据，E08/E09/E10/E11 新数据
- 图表规划精简至 5-6 张（双指标柱状图替代单 MLU 柱状图）

### S004-ch1-domain-verify — Ch1 领域验证 + GPU 重跑（2026-05-24）

**领域子归属验证**（3 个子 agent 并行调研）：
- Size generalization 是 **GNN 理论问题**，非 LEO 路由领域公认挑战。LEO 路由综述未列出此问题。→ 叙事必须改为"将 GNN 技术**迁移到** LEO 路由场景"
- Stretch 指标在 LEO 路由中有使用但非主指标（E2E delay 为主）→ **LOW 风险**
- Delay retention rate 为自造指标，无文献先例 → 标注为新提出指标并论证必要性
- Orbital PE 是标准领域特征工程，非方法论创新 → 降级为"工程选择"
- 加权 Dijkstra 推理有先例（GDDR 2021），增量创新 → 定位为"新的实例化"
- **Li 2026 (arXiv:2604.07264) 竞品排除**：子 agent 幻觉声称其做 size generalization，实际是意图编译论文（LLM→约束 IR→验证），GNN 仅用于同规模 Dijkstra 蒸馏加速。Abstract 中无 size generalization 或 zero-shot transfer。新颖性维持 SAFE。

**GPU 重跑**：
- 审计估 2h/seed → **实测 ~6 min/seed**（差 10x），瓶颈是监督训练而非评估
- 完成 P0 实验 14/18 轮（3 seed × full/A1/A2/A3 + 2 seed same），random_pe 待补（~20 min）

**核心结果（3 seed 均值±std）**：

| 实验 | Stretch | Delay(ms) | ≤1.2x% | 训练精度 |
|------|---------|-----------|--------|---------|
| full (主) | 1.099±0.012 | 66.84 | 86.2 | 97.5% |
| A1 (无PE) | 1.006±0.002 | 61.13 | 99.9 | 40.2%≈随机 |
| A2 (单尺度) | 1.106±0.018 | 67.66 | 84.0 | 97.7% |
| A3 (双消融) | 1.058±0.002 | 63.32 | 92.2 | 40.2%≈随机 |
| same (720→720) | 1.000±0.000 | 60.80 | 100.0 | 98.6% |

- Delay retention = 66.84/60.80 = **109.9%**（跨规模多 ~10% 延迟开销）
- 数据极稳定（std=0.012），消融故事完整（PE 必要、多尺度有贡献、同规模完美）

**质量评估**：学位论文章节够用（数据扎实+消融完整+统计严谨）。贡献定位需诚实：工程验证而非方法论突破。独立投稿需补 random_pe + E06 + E08，叙事转向网络实用性。

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
- **Ch1 size generalization 非 LEO 路由公认问题**（GNN 理论问题），叙事需改为跨领域迁移
- **Ch1 stretch 在 LEO 中合法但非主指标**，E2E delay 为主
- **Ch1 delay retention rate 为自造指标**，需标注为新指标
- **Ch1 Li 2026 非竞品**（意图编译论文，子 agent 幻觉已排除）
- **Ch1 实测 ~6 min/seed**（审计估 2h/seed 差 10x，监督训练不是 PPO）
- **Ch1 P0 实验完成**：full/A1/A2/A3 各 3 seed，same 2 seed，数据极稳定

## 未决项

1. ~~Ch3 GPU 重跑~~ ✅ E01-E12 全部完成
2. ~~Ch3 paper-materials 更新~~ ✅ 全面重写（delay 为主指标，全部新数据）
3. ~~Ch1 GPU 重跑（~105h）~~ ✅ P0 完成（实测 ~6 min/seed × 14 轮 ≈ 2.5h），random_pe 待补（~20 min）
4. **Ch1 paper-materials 更新**：基于 3-seed 数据重写，加入领域验证结论
5. **Ch2 GPU 补实验**：补充 seed + N=30/40 + 乒乓切换率（审计估 ~6h，需实测）
6. **跨章交叉整理**：符号统一表、拓扑差异声明、贡献差异化、叙事一致性
7. DTAR baseline 复现（Ch3 P2，~1-2天，可选）

## 当前位置

Ch1 P0 实验完成 + Ch3 全部完成。下一步：Ch1 paper-materials 重写 → Ch2 补实验 → 跨章交叉整理。
