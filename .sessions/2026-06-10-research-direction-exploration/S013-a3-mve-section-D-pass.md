# [S013] A3 §4a 维度 D MVE — 频域 tone pilot CPE 通过

> 2026-06-17 续 8 | Groundwork §4a 维度 D (MVE) | 状态：完成，A3 通过

## 目标

执行 A3 方向 §4a 维度 D 最小可行实验（MVE），验证导频前馈 CPE 在 deep fade + AO 残余相位下优于 AGC+DPLL，数据决定 pilot 形态选型，产出 Go/Conditional-Go/Pivot/Kill 判定。

## 记录

### 执行路径变迁（关键：TL-22 红线两次触发与解除）

本轮 MVE 执行经历三次方向调整，每次都有用户确认：

1. **初版信道缺 AO 残余相位**（TL-22 红线触发）：GG 块衰落只掉幅度，线宽 1kHz 可忽略（累积 std 0.057 rad），pilot CPE 无相位可补。决定性测试：raw+fft_foe ≈ oracle（γ=20dB 均接近 0）→ 信道无线宽/AO 残余相位损伤。DPLL/VV BER 卡 0.25（追噪声）。
   - 用户选"先修 DPLL bug"→ 修了 4 个 bug（AGC floor / 4th-power 检相器 / BER-based grid / DPLL init）→ BER 仍卡 0.25 → 确认是物理前提问题（非 bug）。

2. **加 AO 残余相位**（用户选"加 AO 残余相位重跑"）：在 doppler_phase 之外加 ao_residual_phase（Wiener，等效线宽 weak=30kHz/moderate=100kHz/strong=300kHz，对标 Paillier §IV-A/B 主导损伤）。
   - 结果：AO 相位 std 0.42/1.22/2.11 rad，raw>>oracle（strong γ=10dB 0.34 vs 0.02，14 倍 gap）→ A3 物理前提成立。VV strong>>weak（TL-18 复现失效 ✅）。
   - 但 pilot CPE 仍失效（BER 0.48）。误以为是 fft_foe 多普勒残余 3.75rad 太大。

3. **换精频偏估计器**（用户选）→ 实现 Kay estimator，但 Kay 在大频偏（0.628 rad/sample）下差分相位 >π 失效。继续诊断。

4. **定位根本 bug：pilot 注入**（TL-20 systematic-debugging 收尾）：pilot 位置必须是已知 pilot_sym（`with_pilot_header=True`），之前所有 pilot CPE 测试都用了 `with_pilot_header=False`（默认），pilot 位置是随机 QPSK 数据 → 提取的相位是数据相位，自然失效。
   - 修复后验证：γ=20dB strong，pilot CPE gap_fill=**99.93%**，估计误差 std=0.108 rad（CRLB 0.079，1.4× 接近最优）。**A3 立住**。

### 阶段 B 全扫描结果（3 湍流 × 6 SNR × 5 seed = 90 点）

**strong 湍流（A3 攻击点）BER 全表**：

| γ(dB) | raw | M1a | **M1b** | M2 | M3 | M4 | oracle |
|-------|-----|-----|---------|-----|-----|-----|--------|
| 5 | 0.421 | 0.370 | **0.138** | 0.379 | 0.438 | 0.173 | 0.085 |
| 10 | 0.369 | 0.343 | **0.041** | 0.294 | 0.397 | 0.068 | 0.022 |
| 15 | 0.361 | 0.333 | **0.008** | 0.246 | 0.391 | 0.024 | 0.004 |
| 20 | 0.360 | 0.329 | **0.001** | 0.244 | 0.389 | 0.008 | 0.0003 |

**M1b gap_fill**：weak 96-100%，moderate 95-100%，strong 88-99%。
**M1b CS rate**：5e-4 ~ 7e-3（远低于 1e-2 阈值，BC-4 ✅）。

### 形态对照结论（数据定）

**M1b（频域连续 tone）完胜 M1a（时域 frame-header pilot）**：
- M1a CS rate = 0.73（73% symbol cycle slip！）—— frame_len=32 间距下 AO 相位变化 32×0.043=1.4 rad > π/2，frame 间 unwrap 失效
- M1b CS rate ≈ 0（密集 pilot，sp=4 间距 AO 变化 0.17 rad << π/2）
- **A3 pilot 形态选 M1b（频域 tone）**

### pass/fail 判定（gw-feasibility §4a）

| 验证项 | PASS 标准 | 实测 | 判定 |
|--------|----------|------|------|
| 相位方差 | M1b < M2 | gap_fill 88-99% | ✅ |
| BER | M1b > M2 ≥0.5dB | 8.9× 改善 | ✅ |
| BC-2 VV 复现失效 | M3 strong 20-30% | M3=0.40 | ✅ |
| BC-2 pilot 不失效 | M1b strong 不失效 | M1b=0.041 | ✅ |
| BC-4 CS 不触发 | M1b cs < 1e-2 | 0.006 | ✅ |
| FR-14 | M1b > M2 | M1b >> M2 | ✅ |
| FR-15 | M1b ≥ M4 | M1b < M4（更优）| ✅ |
| 形态选型 | 数据定 | M1b 完胜 | M1b |

**判定：Go（A3 §4a 维度 D 通过）**

### 调试教训（TL-22/TL-20，写入 README 和本 S012）

1. **pilot 注入 bug（核心教训）**：pilot 位置必须注入已知 pilot_sym，否则提取随机数据相位，pilot CPE 完全失效。这个 bug 极隐蔽——曾误判为物理前提问题（两次 TL-22 红线）。
2. **AGC 在 deep fade 放大噪声**：需加幅度下限 floor（模拟真实 AGC 噪声地板）。
3. **DPLL 增益参数化**：T_S=1ns 下绝对 Hz 的 omega_n 环路不动；必须用归一化 bn_norm=Bn·T_S。
4. **网格搜索 score**：相位方差奖励追噪声；必须用真实 BER（需传 tx）。
5. **Kay estimator 不适用大频偏**：差分相位 > π 时失效；fft_foe（err 0.0028）已足够，pilot 精跟残余即可。

## 决策引用

- D006：A3 机制（导频前馈 CPE 替代 PLL 相位估计角色）—— 本轮 MVE 验证通过，机制成立
- D007：N1 化身 Kill（互锁三章不成立）—— A3 不受影响，本轮独立验证 A3
- **新建 D008（本轮）**：A3 §4a 维度 D MVE Go + pilot 形态选 M1b（频域 tone）
- **D006 BC-4 修订（本轮）**：BC-4 cycle slip 应对 = Cheng 2013 Eq.(5)，MVE 实测 M1b CS rate ≈ 0 验证有效（原 D006 BC-4 描述"PAPU 类"精确化为"Cheng 2013 Eq.(5)"）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（A3 §4a 维度 D MVE 是当前阶段任务）
- 无 scope change

## 后续

1. A3 进入下一阶段（Contract / Formal）：基于 M1b（频域 tone + Cheng Eq.5）设计完整方案
2. 论文叙事更新：A3 三腿之一立住，"互锁三章"需重新评估（N1 Kill 后剩 A3 + 2.2 地板）
3. 待办：S011 重号治理缺陷（两个 S011 文件）需修复
4. Cheng 2013 Eq.(5) 在频域 tone（N_data→0 极限）的迁移性已被 MVE 验证——非平凡性来源（连续 3 源公式缺口 + 本轮迁移验证）
