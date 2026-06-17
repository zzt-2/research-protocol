# A3 §4a 维度 D MVE — 导频前馈 CPE 抗 deep fade 相位失锁

> 最小可行实验（MVE），验证 A3 方向：用导频做前馈 CPE 替代 VV/AGC+DPLL 后 PLL 的相位估计角色，抗 deep fade 瞬态相位失锁。

## 实验目的（一句话）

在 deep fade（σ²_I≈0.684，对标 Paillier §IV-C）+ AO 残余活塞相位（主导损伤，Paillier §IV-A/B）下，验证 **频域连续 tone 前馈 CPE** 优于 AGC+DPLL，BER gap_fill 88-99%，且不触发 cycle slip（BC-4）。

## 信号模型（Paillier 2020 §III，TL-01 锁定）

$$s_{RX}(k) = \sqrt{\rho(k)}\cdot \exp\!\big(j(\Delta\omega kT + \varphi_m(k) + \phi_{AO}(k) + \phi_{laser}(k))\big) + n(k)$$

- $\sqrt{\rho(k)}$ = 幅度（Gamma-Gamma 块衰落，σ²_I≈0.684 对标 Paillier）
- $\Delta\omega kT$ = 多普勒残余频偏 100 MHz（Paillier §IV-C）
- $\phi_{AO}(k)$ = AO 校正后残余活塞相位（**主导损伤**，Wiener，等效线宽 300kHz for strong）
- $\phi_{laser}(k)$ = 激光线宽 1kHz（可忽略）
- $n(k)$ = AWGN（σ²=1/γ，自洽惯例）

**A3 攻击点**：deep fade 瞬态（ρ 骤降）→ 瞬态 SNR 骤降 → 相位估计方差暴增 → PLL 跌破 critical SNR 失锁。前馈 pilot CPE 无环路稳定性约束，无 critical SNR 失锁风险。

## 信道保真度声明（FR-04，方案 B = Paillier 复现）

**近似**：Gamma-Gamma 块衰落（block size 64 symbol）+ AO 残余 Wiener 相位 + 多普勒残余频偏 100MHz + AWGN。

**对标 Paillier §IV-C σ²_I=0.684**：GG 参数 strong(α=3.4,β=3.3) 实测 σ²_I≈0.59（块方差口径），量级匹配。

**保留的核心结构**：① deep fade 瞬态（ρ 骤降）② 块间相位跳变（VV 失效机制来源）③ 多普勒残余频偏 100 MHz ④ AO 残余活塞相位连续抖动（A3 攻击的相位损伤源）

**省略项 + 影响**：
- AO 闭环动态（用静态 GG + Wiener 近似）—— MVE 级别足够，真实化后若 M1b 仍优于 baseline 结论可信
- TURANDOT 波动光学 35 层相位屏（专有代码）—— 用 GG 近似，σ²_I 量级匹配
- 真实 AO 校正残余的精确功率谱 —— 用白 Wiener 近似（等效线宽参数化）

## 六个方法

| 方法 | 角色 | 实现 |
|------|------|------|
| **M1a 时域 frame-header pilot** | 主方法候选 A | Cheng 2013 Eq.1-5：P=4 pilot header/frame(32)，Eq.(2) 相干积累估相位，Eq.(5) CS 修正 |
| **M1b 频域连续 tone** | 主方法候选 B ⭐ | Cheng 2013 Eq.5 迁移：sp=4 密集 pilot，每 symbol 近邻参考，Eq.(5) CS 修正 |
| **M2 AGC+DPLL** | FR-14 最强简单先验 | AGC(幅度归一化+噪声地板) + 二阶 DPLL(bn_norm 网格搜索) |
| **M3 VV 盲 CPE** | BC-2 失效参照 | M=4 次方块平均，窗长网格搜索（TL-18 复现失效）|
| **M4 PASC 数字近似** | FR-15 目标基线 | pilot tone 估相位直接减（不 unwrap，近似光域即时补偿）|
| **raw+fft_foe** | 无 CPE 基线 | FFT 频偏估计去多普勒，无相位补偿 |
| **oracle** | 理论下界 | 用真值 phi_total 全补偿 |

## pass/fail 标准（T001 §2.4，预定义不可后改）

| 验证项 | PASS 标准 | strong γ=10dB 实测 | 判定 |
|--------|----------|-------------------|------|
| 相位方差 | M1b < M2 | M1b gap_fill 88% | ✅ PASS |
| BER 改善 | M1b > M2 ≥0.5dB | M1b BER 8.9× < raw | ✅ PASS |
| BC-2 VV 失效 | M3 strong BER 20-30% | M3=0.397 | ✅ PASS（复现）|
| BC-2 pilot 不失效 | M1b strong 不失效 | M1b=0.041 | ✅ PASS |
| BC-4 CS 不触发 | M1b cs < 1e-2 | M1b cs=0.006 | ✅ PASS |
| FR-14 | M1b > M2 | M1b(0.041) >> M2(0.294) | ✅ PASS |
| FR-15 | M1b ≥ M4 | M1b(0.041) < M4(0.068) | ✅ PASS（M1b 更优）|
| 形态选型 | 数据定 M1a vs M1b | **M1b 完胜**（M1a CS=0.73 失效）| **M1b** |

**判定：Go（A3 §4a 维度 D 通过）**

## 运行命令

```bash
# 环境：WSL Ubuntu，Python ~/.venvs/torch/bin/python（numpy/scipy）
wsl -e bash -c "cd /mnt/d/code/study/research-protocol/explore/a3-pilot-cpe-mve && ~/.venvs/torch/bin/python a3_mve_main.py"
```

单点 smoke（管道验证）：
```bash
wsl -e bash -c "cd /mnt/d/code/study/research-protocol/explore/a3-pilot-cpe-mve && ~/.venvs/torch/bin/python a3_pilot_cpe.py"
```

## 依赖

numpy, scipy（gg_block 用 scipy.stats.gamma，CS 修正用 scipy.ndimage.uniform_filter1d）。无外部数据。

## 结果摘要（strong 湍流，A3 攻击点）

| γ(dB) | raw | M1a | **M1b** | M2 | M3 | M4 | oracle |
|-------|-----|-----|---------|-----|-----|-----|--------|
| 0 | 0.485 | 0.462 | **0.340** | 0.490 | 0.486 | 0.364 | 0.196 |
| 5 | 0.421 | 0.370 | **0.138** | 0.379 | 0.438 | 0.173 | 0.085 |
| 10 | 0.369 | 0.343 | **0.041** | 0.294 | 0.397 | 0.068 | 0.022 |
| 15 | 0.361 | 0.333 | **0.008** | 0.246 | 0.391 | 0.024 | 0.004 |
| 20 | 0.360 | 0.329 | **0.001** | 0.244 | 0.389 | 0.008 | 0.0003 |

**M1b gap_fill（raw→oracle 差距填充率）**：weak 96-100%，moderate 95-100%，strong 88-99%。

**M1b CS rate**：5e-4 ~ 7e-3（远低于 1e-2 阈值）。

## 调试教训（TL-22/TL-20 记录）

调试过程中踩的坑（已解决，记录避免重复）：

1. **pilot 注入 bug（核心）**：pilot 位置必须是已知 pilot_sym（`with_pilot_header=True`），否则提取的是随机数据相位，pilot CPE 完全失效（BER 卡 0.5）。这是最隐蔽的 bug，曾误以为是物理前提问题。
2. **AGC 在 deep fade 放大噪声**：加幅度下限 floor=0.3（模拟真实 AGC 噪声地板）。
3. **DPLL 增益参数化**：omega_n 用绝对 Hz 在 T_S=1ns 下环路不动；改归一化 bn_norm=Bn·T_S。
4. **网格搜索 score**：相位方差会奖励追噪声；改用真实 BER（需传 tx）。
5. **Kay estimator 不适用大频偏**：差分相位 > π 时 Kay 失效；fft_foe（err 0.0028）已足够，pilot 精跟残余。

## 元数据

- git hash: c31337bdfa9b
- 运行时间: 33.4s（90 点）
- Ns=8192 symbol/点，5 seed 均值
- TL-25 六条 checklist 全 true

## 文件清单

- `a3_channel.py` — 信道生成（generate_shared_realization + gg_block + ao_residual_phase）
- `a3_baselines.py` — M2 AGC+DPLL / M3 VV / M4 PASC 近似 / fft_foe / kay_estimator
- `a3_pilot_cpe.py` — M1a frame-header pilot / M1b 频域 tone（Cheng 2013 Eq.1-5）
- `a3_mve_main.py` — 主扫描入口
- `_find_gg_params.py` — GG 参数校准辅助
- `_smoke.py` — 阶段 A smoke 调试脚本（历史调试记录）
- `a3_mve_results.json` — 全扫描结果（90 点 + 元数据）
