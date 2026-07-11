# Handoff: Q-CMA-FADE 方向扩展 — 压力测试后重新审视能出什么

> 来源: S006 续 + R003 | 交接目标: 下一个对话执行 R1/R4/R5（零风险后处理）+ R2/R7（关键前置判断）
> 文件名: H006-cma-fade-direction-expansion.md

## 到哪了（状态）

Q-CMA-FADE Step A/B/C 全跑完，MVE 技术上 PASS 但**压力测试修正为 Conditional Go（D008）**。核心问题：方法层（监督 ML 换 CMA）创新性不足 + 对比不公平（监督 vs 盲）+ QPSK 场景"用小步长就行"。

三个子 agent 调研 + R003 穷举后，方向可能扩展为三层故事（发散机制分析 + 公平对比 + 恢复协议），但**还没定最终形态**。用户要求"先穷举能出结果的子问题，记下来再讨论"——R003 已落盘 12 个子问题。

**当前不是"进 Contract"状态，是"重新审视方向能出什么"状态。**

## 下一步干什么

按 R003 建议路径，先做**零风险后处理 + 关键前置判断**：

### 第一批（零风险，几乎确定出结果）

1. **R1**: CMA 发散半解析界 — 把 `drift ∝ μ·σ_n·√(AFD)` 形式化，用数值 AFD/LCR（`gg_time_fading_model.py::fade_statistics` 已实现）代入，跟 Step B 的 384 trials 实测 P_div 对比验证
2. **R4**: 发散事件 vs AFD/LCR 相关性 — 从 Step B 的 diverge_idx + 同 channel 的 AFD/LCR 做 join + 算相关系数
3. **R5**: 系数漂移模型验证 — 从 Step B 的 w_norm_traj 提取实测漂移，跟 `drift ∝ μ·σ_n·√(n)` 预测对比 + R²

### 第二批（关键前置判断，决定方向生死）

4. **R2**: 实现 CMMA（级联多模 CMA），跑发散扫描 — 如果 CMMA 也发散 → "多模修星座失配但修不好深衰落"成立 → 恢复协议有空间
5. **R7**: 实现被动冻结（h<thr 时停止 CMA 更新），量化效果 — 如果冻结太有效（P_div→0）→ "问题被 trivial 方法解决" = 方向动摇

### 第三批（根据第二批结果决定）

6. 如果 R7 显示冻结不够好 + R2 显示 CMMA 也发散 → 做 R8/R9（冷重置 vs ML 热启动恢复时间 + 混合恢复协议）
7. 如果要做盲 vs 盲公平对比 → 做 R10（VQ-VAE 实现 + scintillation 扫描）

## 纪律（和下一步直接相关的约束）

1. **守 FR-22**：当前仍在 GW Step 4a 维度 D MVE 范围内（Step C 的扩展验证），不是跳框架
2. **守 TL-20**：R2/R7 跑之前先建理论预期 — CMMA 应该比 CMA 略鲁棒（多模误差幅度小）但仍会发散（梯度噪声驱动不变）；冻结应该大幅降 P_div 但有 SOP 漂移代价
3. **守 TL-22**：如果 R7 冻结 P_div→0 → 先花 5 分钟查物理前提（冻结期间 SOP 漂移多少？恢复后 BER 多差？）再判方向
4. **不急着定方向形态**：R003 列了三种可能形态（A 恢复协议为主 / B 盲 VAE 为主 / A+B 交集），等 R1/R2/R4/R5/R7 出结果后再定
5. **torch 可用**：scoop py311（`/c/Users/zzt/scoop/apps/python311/current/python`）有 torch 2.6.0+cu124 + CUDA RTX 4070。不是 PROMPT-005 说的"无 torch"
6. **SOP 速率用 1 krad/s**（4e-7 rad/sym，sat.1553 §6.3 真实值），不是 Step B 原来的 250 krad/s
7. **16QAM 是有价值的场景**（CMA modulus mismatch 是结构性缺陷），QPSK 场景弱（小步长够用）

## 必读（按优先级）

1. **`R003-resultable-subquestions.md`** — 12 个子问题穷举，高/中/低信心分级，这是本轮核心产出
2. **`decisions.md` D007+D008** — Step C Go 判定 + 压力测试修正为 Conditional Go
3. **`S006-stepC-ml-vs-cma-mve.md`** — Step C 执行记录 + 压力测试结果
4. **`explore/cma-fade-divergence/README.md`** — Step A/B/C 全结果 + 参数溯源表 + 发散条件判据
5. **`common/_cma.py`** — CMA 均衡器（发散判据定义在这里：|w|>10×init OR |z|>1e3）
6. **`common/_ml_equalizer.py`** — ML 均衡器（ButterflyCNNEqualizer2x2 + MLChannelEqualizer）
7. **`common/_gg_time.py`** — GG 时间域模型（gg_time_envelope）
8. **`explore/cma-fade-divergence/gg_time_fading_model.py`** — 数值 AFD/LCR 统计（fade_statistics 函数，R1/R4 要用）
9. **`results/cma-fade-divergence/`** — 所有实验结果 JSON（cma_divergence_scan / mve_cma_vs_ml / sup_stress_test）

## 已有资产（不用重做）

| 资产 | 文件 | 状态 |
|------|------|------|
| GG 时间域模型 | `common/_gg_time.py` | PASS (GAR KS<0.006) |
| CMA 2×2 蝶形均衡器 | `common/_cma.py` | PASS (Godard 1980, block-wise) |
| ML CNN 蝶形均衡器 | `common/_ml_equalizer.py` | PASS (Qin 2025 架构, MSE 监督) |
| MMSE oracle 均衡 | `common/_equalizer.py` | 已有（不改，P4） |
| 发散扫描数据 | `results/.../cma_divergence_scan_results.json` | 384 trials, 128 组合 |
| ML vs CMA MVE 数据 | `results/.../mve_cma_vs_ml_results.json` | 25 runs, 三方对照 |
| 压力测试数据 | `results/.../sup_stress_test_results.json` | 16QAM/小步长/SOP 漂移 |
| 数值 AFD/LCR | `gg_time_fading_model.py::fade_statistics` | PASS |

## 接口变更（如有代码改动）

R2 需新建 `common/_cmma.py`（级联多模 CMA，P4 只扩不改）。
R7 需在 `_cma.py` 加 freeze 模式或在 explore/ 新建脚本（不改 common/，P4）。
R1/R4/R5 是纯后处理，不改代码。

## 失败数据附录

### D008 压力测试关键数据

**Sup-1 16QAM 安全区（μ=1e-3）CMA BER 不稳定**：
- trial 0: CMA BER=0.26, ML=0.033, oracle=0.019, raw=0.26
- trial 1: CMA BER=0.047, ML=0.0001, oracle=0.0000
- trial 2: CMA BER=0.29（还发散了）, ML=0.0000

**Sup-2 QPSK μ=1e-3 在危险区信道（f_G=1000Hz strong）够用**：
- μ=1e-3 BER≈0.0001（≈oracle）→ "用小步长就行"在 QPSK 成立 → QPSK 方向弱

**Sup-3 ML SOP 漂移**：
- ≤20°: BER=0.0000（零退化）
- 45°: BER=0.43（崩溃）
- 90°: BER=0.50（完全失效）

### Step B 发散条件判据

- 安全区（P_div≈0）：μ ≤ 1e-3
- 临界区（P_div 0~1）：μ ≈ 5e-3
- 危险区（P_div≥0.67）：μ ≥ 1e-2 且 f_G ≥ 100 Hz
- 发散由 μ 主导，f_G 第二驱动（LCR 机制），湍流深度影响弱

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 监督 vs 盲不公平 | 公平对照（FR-03） | 当前 ML 用 MSE 监督（需 pilot），CMA 盲 | R10 实现 VQ-VAE 后解决 |
| 增强基线缺失 | FR-03 增强基线 | 只跟了裸 CMA，没跟 CMMA | R2 实现 CMMA 后解决 |
| 方法创新性不足 | TL-12 换皮红线 | 网络结构照搬 Qin，损失更简单 | R8/R9 恢复协议 或 R10/R11 盲 VAE 后解决 |
| SOP 速率不一致 | 物理一致性 | Step B 用 250 krad/s（过快），Step C 改 1 krad/s | Contract 阶段统一用 1 krad/s |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| R1 解析界 vs 实测 | R²>0.5 或趋势一致 | TL-20 理论预期 | 未测 |
| R2 CMMA 发散 | CMMA P_div > 0 in 危险区 | 物理推导（梯度噪声驱动不变） | 未测 |
| R7 冻结效果 | P_div 下降 + SOP 漂移代价存在 | sat.1553 [79] 未量化 | 未测 |
| R8 热启动 vs 冷重置 | 热启动恢复时间 < 冷重置 | 理论（从近优权重出发 vs 初始权重） | 未测 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

验证建议：
1. 读 `R003-resultable-subquestions.md` 确认 12 个子问题清单完整
2. 读 `decisions.md` D008 确认 Conditional Go 的修正理由
3. 检查 `results/cma-fade-divergence/sup_stress_test_results.json` 确认压力测试数据存在
4. 运行 `python explore/cma-fade-divergence/mve_cma_vs_ml.py --smoke` 确认代码可跑

## 下一轮

1. 先做 R1/R4/R5（纯后处理，零风险）— 用 Step B 已有数据 + fade_statistics + w_norm_traj
2. 再做 R2（实现 CMMA）+ R7（实现 freeze）— 关键前置判断
3. 根据 R2/R7 结果决定第三批做恢复协议（R8/R9）还是盲 VAE（R10）
4. **不急着定方向最终形态** — 等数据出来再讨论
