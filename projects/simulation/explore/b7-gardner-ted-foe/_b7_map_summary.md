# B7 Fig.1a 数值重建摘要 — Gardner TED gain ↔ Doppler f_D

> 日期 2026-07-07 | 脚本 `_b7_map_reconstruction.py` | 数据 `_b7_map_results.json` | 图 `_b7_map_curve.png`
> 重建对象: OFC 2026 W2A.62 poster Fig.1a (PDF→md 丢失的机制图)
> 方法学: 25-Gbaud 单偏振 QPSK, RRC α=0.1 (SPS_UP=16), 确定性频偏 rx=tx·exp(j2πf_D t),
> Gardner e(k)=Re{y_mid·(y*curr−y*prev)}, S-curve=E[e(τ)] τ∈[0,T) 16 点, N_sym=1024,
> G=max|S-curve|. 噪声条件做 6 次实现平均 (单次实现会伪化周期判断).
> ⚠️ 解释器偏差: 任务给的 `~/.venvs/torch/` 本机不存在; 用 scoop python311 (numpy2.4.3/scipy1.17.1/mpl3.10.8), deps 齐全. 不影响数值.

## Q1: G(f_D) 随 f_D 是否周期变化? → **是, 周期 = baud rate B = 25 GHz**

诊断扫频 0–75 GHz, FFT 主频能量占比:

| 条件 | 主频能量占比 | 测得周期 | 归一化 |
|---|---|---|---|
| 无噪声 | **94.5%** | 25.33 GHz | 1.01·B |
| OSNR 17 dB | **87.1%** | 25.33 GHz | 1.01·B |

确定性铁证: `G_abs(0)=G_abs(25)=G_abs(50)=0.13214` **完全相等** (JSON 可 grep). 周期=符号率 B=25 GHz, 吻合 poster "归一化到 baud rate". 机制真实.

## Q2: 跟 poster "可逆映射" 描述符相符吗? → **部分不符 — 周期真, 但 (−B,B) 内不可逆**

poster 行 37 称 "(−B,B) 内可逆". 主测段 0–23 GHz 数值显示:
- 无噪曲线 **U 形**: G 在 0→~13 GHz 单调降 (0.132→0.007), ~13→23 GHz 升 (0.007→0.128)
- 单谷, **1 转折点** → 同一 G 对应 2 个 f_D, 即 **2:1 映射, 非单射**
- 这正是 poster Fig.1b "生成两个 Doppler 候选" 的物理来源
- OSNR 17 dB 噪声使转折点数升至 14, 6× 平均后底层 U 形仍可见

poster "可逆"应理解为"半个周期 (0,B/2) 内单调可逆", 非整个 (−B,B). 描述符不精确, 但双候选算法自洽.

## Q3: 机制是否成立? → **成立** (无需找反例物理原因).

物理推测 (标注: 推测): f_D 在符号周期 T 引入净相位旋转 Δφ=2π·f_D·T, QPSK 星座旋转后相邻样本过零斜率被调制, Gardner S-curve 峰随 Δφ 以周期 f_D=B (Δφ=2π) 变化, 是 2π 相位模糊的时域表现.

均为现象报告 + 推测归因, 不评价 poster 对错. 原始数字在 JSON.
