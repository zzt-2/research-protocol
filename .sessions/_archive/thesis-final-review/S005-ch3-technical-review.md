# [S005] Ch3 技术正确性审查 + 跨章公式一致性

> 2026-05-25 | Phase 2.5 | 完成
> 子 agent: 6a (参数审查), 6b (公式审查), 6c (跨章一致性)

## 目标

验证 Ch3 (HGAT 卫星 DAG 任务卸载) 仿真参数、公式、指标在领域内的正确性，并检查三章公共公式（Shannon、FSPL、噪声）的一致性。

## 审查结果总览

| 判定 | 数量 | 说明 |
|------|------|------|
| **P0 必须修复** | 2 | noise_power 跨带宽共用; antenna_gain 未使用导致 G2S 速率≈0 |
| **P1 建议修复** | 4 | 排队模型描述不一致; 训练不充分; 奖励权重; 跨章轨道高度差异 |
| **P2 论文写作注意** | 3 | FSPL 距离保护; noise 物理依据标注; ISL 距离近似 |
| **PASS** | 33+ | 绝大多数参数与 K2/M01 主参考完全一致 |

---

## P0 级问题

### P0-1: noise_power 跨带宽共用（6a 发现）

**位置**: `config.py:52` + `channel.py:46`

**问题**: `noise_power_dbm = -100` (→ 1e-13 W) 被所有链路共用，但各链路带宽差异巨大：

| 链路 | 带宽 | 正确噪声功率 | 当前噪声 | SNR 偏差 |
|------|------|-------------|---------|---------|
| G2U | 20 MHz | -101 dBm ≈ 1e-13 W | -100 dBm | ≈正确 |
| G2S/U2S | 15 MHz | -101.2 dBm | -100 dBm | 噪声高估 1.3 dB |
| ISL | 1 GHz | -84 dBm | -100 dBm | **噪声低估 17 dB** |

-100 dBm 恰好对应 20MHz BW 在室温下的热噪声（NF≈1dB），说明它是以 20MHz 为基准校准的。ISL (1GHz BW) 的真实噪声应高约 17dB，当前实现使 ISL 的 SNR 被严重高估。

**与 K2/M01 的关系**: K2/M01 Table III 标注 σ² = -100 dBm，但 K2/M01 可能：(a) 每条链路独立定义噪声，或 (b) SNR 公式中 noise 已包含带宽归一化。需核实原文公式。

**修复方案**:
- 方案 A: 改为 PSD (`noise_psd_dbm_hz = -174 + NF`)，各链路 `noise_power = PSD * BW`
- 方案 B: 保留 -100 dBm 但仅为 G2U 校准，为其他链路独立设置
- 方案 C: 如 K2/M01 原文也是统一噪声，则保持一致并在论文中注明

### P0-2: antenna_gain 定义但未使用（6b 发现）

**位置**: `config.py:54` 定义 `antenna_gain=1.0`，但 `channel.py:compute_snr()` 未引用

**影响**: IoTD→LEO 直连 (Ka-band 20GHz, 500km):
- FSPL ≈ 172 dB, tx_power=1W → 接收功率 ≈ 6e-18 W
- SNR = 6e-18 / 1e-13 ≈ 6e-5 → **速率 ≈ 1.7 kbps ≈ 0**

与 K2/M01 对比: K2/M01 Table III 标注 G_P = 1 (0 dBi)，同样不用天线增益。但 K2/M01 有 4 UAV 做中继，IoTD 可能不走直连 G2S 路径。

**修复方案**:
- 如果 K2/M01 原文 G_P=1 不代表无天线增益（而是归一化到 EIRP 中），则需将 tx_power 调整为 EIRP（含天线增益）
- 如果 K2/M01 确实是 0 dBi，则 G2S 直连就是不可用的，agent 会自然学习走 IoTD→UAV→LEO 中继路径。论文需明确说明这一点
- **最低要求**: 删除 `antenna_gain` 和 `bw_alloc_factor` 这两个未使用参数，避免混淆

---

## P1 级问题

### P1-1: 排队模型描述不一致（6b）

**位置**: `env.py:179-182`

代码实现的是**确定性 FIFO 最大完成时间模型**:
```
completion_time = max(node_available, pred_finish) + transfer_time + compute_time
```

不是 M/M/1 排队模型（无泊松到达、无指数服务时间、无稳态排队延迟）。

**要求**: 如果 plan.md 或论文素材中提到"M/M/1 delay 模型"，需修正为"deterministic non-preemptive single-server scheduling"。在 DAG 调度场景下，确定性模型比 M/M/1 更合理（任务到达非泊松）。

### P1-2: 训练充分性偏弱（6a）

| 参数 | 当前值 | 文献参考 | 建议 |
|------|--------|---------|------|
| total_episodes | 500 | K2/M01 ~300, M06 ~1500 | ≥1000 + early stopping |
| update_interval | 10 episodes | PPO 标准 1024-4096 steps | 改为 step-based (2048) |

HGAT 参数量 > GraphSAGE，收敛更慢。500 episodes × ~200 steps/update 偏少。

**注意**: 当前结果可能是以 500 episodes 跑出来的，如果结果已经收敛（early stop 触发），则无需重跑。需检查训练日志确认。

### P1-3: 奖励权重 η_t/η_e = 10:1（6a）

eta_t=5.0 (延迟) vs eta_e=0.5 (能耗) 的 10:1 比例。代码注释说明因 T_norm << E_norm 需放大匹配量级。

**风险**: 可能导致能耗被忽略，与 K2/M01 的"联合优化延迟和能耗"目标不一致。

**建议**: 在 MDP 试运行中验证 reward decomposition 各分量的实际占比。如果延迟 >80%（触发 domination_threshold），需调高 eta_e。

### P1-4: 跨章轨道高度差异（6c）

| 章 | 高度 | 来源 |
|----|------|------|
| Ch1 | 550 km | Starlink 参考 |
| Ch2 | 550 km | Starlink 参考 |
| Ch3 | 500 km | K2/M01 |

**建议**: 论文中注明各章参考不同文献即可。550 vs 500 km 对仿真结果影响很小。

---

## P2 级问题（论文写作注意）

### P2-1: Ch3 FSPL 无距离下界保护（6c）

`channel.py:21` 的 `free_space_path_loss()` 无 `np.maximum(distance, 1.0)` 保护。实际场景中卫星-地面距离不会接近 0，风险低，但建议补充防御性代码。

### P2-2: Ch3 noise_power 物理依据需标注（6c）

论文中应注明 -100 dBm 的等效条件（如"对应 T=290K, NF≈1dB, B=20MHz 的热噪声功率"）。

### P2-3: ISL 距离用近似计算（6b）

`env.py:314-315` 用两颗卫星到地面平均距离的差值近似 ISL 距离。对 t=0 快照仿真可接受，跨时隙仿真需改为卫星间 3D 欧氏距离。

---

## 跨章一致性总结（6c）

### 公式一致性: PASS

| 公式 | Ch1 | Ch2 | Ch3 | 一致？ |
|------|-----|-----|-----|--------|
| Shannon | B·log₂(1+SNR) | B·log₂(1+SNR_lin) | B·log₂(1+snr) | **一致** |
| FSPL | 简化 ISL 模型 | 20·log₁₀(4πd/λ) | 20·log₁₀(4πdf/c) | **等价** (Ch2/Ch3) |
| 衰落 | 无 (ISL真空) | Shadow fading AR(1) | Rician + Shadowed-Rician | **合理差异** |
| 噪声 | 隐含在 snr_ref | kTBF 物理公式 | 固定 -100 dBm | **方式不同**，量级一致 |
| 轨道高度 | 550 km | 550 km | 500 km | **差异需说明** |
| 最小仰角 | N/A | 20° | 10° | **差异需说明** |

### 不存在一致性问题

三章的核心物理模型数学上一致。差异均源于不同研究场景的合理选择（ISL vs 用户链路 vs 多链路卸载）。

---

## Ch3 参数审查完整清单（6a）

### 完全匹配 K2/M01 的参数 (PASS, 33 项)

n_uav=4, n_leo=8, n_cs=1, area_size=1km×1km, 2×4 星座配置, leo_altitude=500km, freq_iotd=0.8GHz, freq_uav=3GHz, freq_leo=4-5GHz, freq_cs=10GHz, kappa_uav/leo/cs=1e-28, G2U BW=20MHz, G2S BW=15MHz, Rician K=2.0, Shadowed-Rician 三组参数(light/average/heavy)完全一致, atmo_loss=0.5dB, n_tasks=20, task_input=[0.8,4]MB, task_output=[0.4,1]MB, task_cycles=[1,3]Gcycles, daggen fat=0.6/density=0.4/regular=0.9, PPO lr/batch/clip/gamma, orbital_period 自动计算正确

### 需关注的参数 (WARN, 5 项)

1. n_iotd=10 (K2/M01=100) — 缩小 10×，需 scalability 实验
2. task_deadline=[50,60]s — 偏宽松（本地执行最复杂任务仅 3.75s），需确认是 DAG 级还是子任务级
3. total_episodes=500 — 可能不充分
4. update_interval=10 — 偏小
5. gae_lambda=0.95 vs M06=0.98 — 差异微小

---

## 决策引用

- 无新建决策

## 范围确认

- 本轮是否在 scope boundary 内：是（对话 6 = Ch3 技术审查 + 跨章一致性）

## 后续

1. **P0 问题处理**: 核实 K2/M01 原文中 noise 和 antenna_gain 的定义，确定修复方案
2. **对话 8 衔接**: P0/P1 修复后更新到 Ch2+Ch3 数据确认对话
3. **论文写作**: P2 问题在写作阶段处理
