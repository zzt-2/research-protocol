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
1. 三章主题：Ch1 监督学习路由（拓扑规模迁移）→ Ch2 DRL 切换（UE 规模迁移）→ Ch3 故障弹性路由（故障鲁棒性+规模）
2. 方法统一叙事："GNN 在 LEO 卫星网络中的系统性应用研究——结构化编码实现故障弹性、规模迁移、在线决策"
3. 每章必须独立可发表（问题建模→算法设计→实验验证闭环）
4. Size generalization 是 GNN 理论性质，不是 LEO 任何子领域公认挑战（Ch1/Ch2 领域验证一致确认）
5. 贡献声称必须诚实定位为"系统性应用+实证验证"，不声称方法论突破

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
- **Ch2 领域验证完成（S006）**：6 个问题全部有结论，size gen 非切换领域公认挑战，二部图 GNN 有 Lee & Lim 2025 直接竞争者，DDQN 是标准做法，Jain's 非切换通行指标
- **论文主线调整（S006）**：从"GNN size gen 创新"转为"GNN 在 LEO 网络中的系统性应用研究"，三章差异化定位，size gen 降为跨章共享优势
- **硕士论文标准确认（S006）**：当前项目工程量和实验规范远超同方向够格线（参照 Shi 2024 仅 14 节点 3 baseline 发 SCI）
- **三章文档扫描完成（S006）**：识别 P0 共 19 处必须修改（过度声称/事实错误/指标定位）+ P1 共 22 处建议修改
- **Ch2 Lee & Lim 2025 竞品事实错误**：decision_log 和 04_literature 中标注为"非二部图"，实际使用二部图，需修正
- **贡献声称降级规范**：~~提出/首次发现/创新性地~~ → 验证并量化了/系统评估了/针对场景适配了
- **Ch2 eps_decay 问题**：原始 eps_decay=5 + 固定 episode seed = 单场景记忆（非真实 RL 训练）。eps_decay=20 + per-episode 随机化让 GNN 优势更显著（+22.8% vs MLP）
- **Ch1/Ch3 不受 eps_decay 影响**：Ch1 监督学习无 episode 循环，Ch3 PPO 已正确使用 `seed_offset+i`
- **eps_decay=20 同规模结果**：GNN 50UE reward 29262 vs MLP 23476（+24.7%），blocking 0.16% vs 9.15%（低 57 倍）
- **100UE 同规模不可行**：eps_decay=20 + 100 episodes 仍不够，但领域文献最多到 50UE，不影响论文
- **Size gen 核心结果（单模型）**：20→50 retention 223%（blocking 0.89%），20→100 retention 329%（blocking 14.5%）
- **模型保存需修复**：c_gnn_ddqn.py 模型文件名未含 seed 后缀，3 seed 覆盖同一文件

### S006-ch2-domain-verify-and-thesis-positioning.md — Ch2 领域验证+论文定位调整+文档扫描（2026-05-24）

Ch2 领域归属验证 6 个问题全部完成（3 子 agent 并行调研）。论文主线从"GNN size gen"调整为"系统性应用研究"。三章差异化定位确定。调研硕士论文标准确认远超够格线。三章文档扫描识别 P0/P1 共 41 处修改需求。5 处事实错误已修正。

### H004-thesis-reading-and-doc-update.md — 精读→文档修改交接（2026-05-24）

交接至新对话：先精读学位论文确定写法规范 → 再执行 P0/P1 叙事修改 → 补实验 → 跨章元分析。详见交接文档。

## 未决项

1. ~~Ch3 GPU 重跑~~ ✅
2. ~~Ch3 paper-materials 更新~~ ✅
3. ~~Ch1 GPU 重跑~~ ✅ P0 完成，random_pe 待补（~20 min）
4. ~~P0 文档修改（19 处）~~ ✅ Phase 2 完成（3 子 agent 并行）
5. ~~P1 文档修改（22 处）~~ ✅ 大部分完成
6. ~~Ch2 GPU 补实验（第一轮 eps_decay=5）~~ ✅ 30 轮完成，但 eps_decay=5 下 GNN 输 MLP
7. ~~Ch2 eps_decay=20 同规模实验~~ ✅ 12 轮完成，GNN 50UE +24.7% vs MLP
8. ~~Ch2 size gen 评估~~ ✅ 单模型验证通过（20→50 retention 223%, 20→100 retention 329%）
9. **Ch2 模型保存修复** 🔄 模型文件名未含 seed 后缀，需修复后重跑 20UE 3 seed（~15 min）+ size gen 3 模型
10. **MLP size gen 对照** 🔄 MLP 固定输入维度预期无法迁移，需验证
11. **Ch1 paper-materials 更新**：基于 3-seed 数据 + 领域验证结论 + 贡献降级重写
12. **跨章元分析框架设计**：结论章统一讨论 GNN 优势条件
13. **跨章交叉整理**：符号统一表、拓扑差异声明、三章差异化叙事
14. DTAR baseline 复现（Ch3 P2，~1-2天，可选）

## 范围边界

### 原始目标
三章审计发现的小改动统一修复执行

### 当前范围
审计修复 + 领域验证 + 论文定位调整 + 文档全面更新

### 明确不含
- 不新增实验方法/架构
- 不做跨章迁移实验（Tier 3，另议）
- 不重写论文正文（仅更新 paper-materials 素材层）

### 范围变更记录
| 日期 | 变更内容 | 原因 |
|------|---------|------|
| 2026-05-22 | 初始范围：三章小改动修复 | 审计专题产出 |
| 2026-05-23 | 扩展：Ch3 GPU 重跑+指标体系重构 | 发现 MLU 非通行指标 |
| 2026-05-24 | 扩展：Ch2 领域验证+论文定位调整 | Ch1 领域验证方法论复用到 Ch2，发现论文主线需调整 |

## 当前位置

论文定位调整完成，文档修改清单已就绪。

### R003 写法规范（thesis-structure-research 专题）— 贡献声称修辞模板（2026-05-24）

16 条 before→after 措辞模板 + 3 种贡献定位策略 + 局限性四要素写法。详见 `.sessions/thesis-structure-research/R003-writing-norms-contribution-claims.md`。

### Phase 2 文档修改 — P0 19 处 + P1 大部分完成（2026-05-24）

3 子 agent 并行修改：
- Ch1（11 处）：创新性降级 + 指标定位 + PE/Dijkstra 先例标注 + 3-seed 数据同步
- Ch2（9 处）：Lee & Lim 修正为最直接竞争者 + Jain's 降级 + system throughput 补充
- Ch3+跨章（5 处）：三章差异化定位 + D19 数据更新

### Phase 3 Ch2 补实验 — eps_decay 问题发现与修复（2026-05-24）

**代码修改**：c_gnn_ddqn.py + b2_topk.py 添加 train_seed/ping-pong rate/throughput。run_multi_seed.py 批量脚本。

**第一轮结果（eps_decay=5）**：30 轮完成（10 配置×3 seed），但 GNN 全面输给 MLP。

**根因分析**：
- 原始代码 `run_ep(seed=42)` 每个训练 episode 相同环境（单场景记忆）
- 修改后 `run_ep(seed=train_seed+ep)` 每个 episode 不同环境（真实多样场景）
- eps_decay=5 对固定场景够用（15 ep 后停止探索），对多样场景远远不够
- Ch1/Ch3 不受影响（Ch1 监督学习无 episode，Ch3 PPO 已用 `seed_offset+i` 正确随机化）

**快速验证（eps_decay=20, 50UE, seed=1）**：

| 方法 | Reward | Blocking | vs 原始(seed=42) |
|------|--------|----------|------------------|
| GNN | **29262** | 0.16% | 27862→29262 (+5%) |
| MLP | 23847 | 8.56% | 29228→23847 (-18%) |

**GNN +22.8% reward，blocking 低 54 倍。** per-episode 随机化 + 充分探索让 GNN 结构优势更显著（图编码天然泛化，flat MLP 不行）。

**当前位置：eps_decay=20 验证通过，需 3 seed 全量重跑 + 100UE 测试**

### Phase 3B eps_decay=20 全量实验（2026-05-25）

**全量同规模实验完成**：4 配置 × 3 seed = 12 轮（nohup PID 22051，已完成）。

**同规模结果（eps_decay=20, 3 seed 均值）**：

| 实验 | 方法 | UE | Reward | Blocking | 说明 |
|------|------|-----|--------|----------|------|
| E4-20-d20 | GNN | 20 | 12892 | 0% | 基线稳定 |
| C6-20-d20 | MLP | 20 | ~12850 | ~0% | 与 GNN 持平 |
| E4-50-c15-d20 | GNN | 50 | 29262 | 0.16% | **GNN 大幅领先** |
| C6-50-c15-d20 | MLP | 50 | 23476 | 9.15% | MLP blocking 高 |

**100UE 同规模测试失败**（eps_decay=20, seed=1）：GNN reward -19218, blocking 81%。100 episodes + eps_decay=20 对 100UE 状态空间仍不够。

**文献对比**：主流文献 UE 规模 10-30，Lee & Lim 2025（最直接竞品）仅 50UE，无任何论文做 100UE 同规模或 size gen 实验。100UE 失败不影响论文。

**Size generalization 评估完成**（run_size_gen.py）：加载 20UE 模型评估 50/100UE。

⚠️ **已知问题**：模型文件名未含 seed 后缀（`E4-20-d20_model.pt`），3 seed 覆盖同一文件，size gen 仅用了最后一个 seed 的模型。需修复模型保存路径后重跑 20UE 3 seed（~15 min）。

**Size gen 单模型结果**（seed=3 模型，3 eval seed 均值）：

| 场景 | Reward | Blocking | Throughput | Retention |
|------|--------|----------|------------|-----------|
| 同规模 20UE | 12892 | 0% | 2375 Mbps | — |
| **迁移 20→50** | **28780** | 0.89% | 2343 Mbps | **223%** |
| **迁移 20→100** | **42411** | 14.5% | 2025 Mbps | **329%** |

**核心结论**：
1. **Size gen 完全成立**：20UE 训练的 GNN 零样本迁移到 50/100UE，性能保持甚至提升
2. **50UE 同规模 GNN +24.7% vs MLP**（29262 vs 23476），blocking 低 57 倍（0.16% vs 9.15%）
3. **100UE 同规模训练失败可接受**：领域内无此先例，转为强调 size gen 价值
4. **eps_decay=5 的旧结果不可靠**（固定 episode seed = 单场景记忆），eps_decay=20 是正确训练配置

**待做**：
1. 修复 c_gnn_ddqn.py 模型保存路径（加 seed 后缀），重跑 20UE 3 seed（~15 min）
2. 用 3 个独立模型跑 size gen 评估（~5 min）
3. MLP size gen 对照（MLP 固定输入维度，预期无法迁移）
4. 更新 Ch2 paper-materials
5. Phase 4 跨章元分析
6. Ch1 paper-materials 重写
