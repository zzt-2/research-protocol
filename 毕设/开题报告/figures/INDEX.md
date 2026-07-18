# 开题报告图表索引

> 最后更新：2026-06-05

## 目录结构

```
figures/
├── drawio/    可编辑的 draw.io 工程框图
├── png/       仿真结果图（Python生成）
├── others/    参考论文截图（对照用，不直接使用）
├── *.py       绘图/仿真脚本
├── *.json     仿真数据
└── *.pdf      PDF版本
```

---

## drawio/ — 工程框图

### 论文正文用图（fig_* 前缀）

| 文件 | 对应图号 | 内容 | 状态 |
|------|---------|------|------|
| fig_coherent_receiver.drawio | 图2-1 | QPSK相干检测星地激光通信系统框图 | ✅ 可用 |
| fig_carrier_sync_chain.drawio | 图4-2 | 载波恢复链：接收信号→预补偿→FFT-FOE→CPR→判决 | ✅ 可用 |
| fig_foe_module.drawio | 图4-3 | FFT频偏估计RTL架构：四次方→FFT→峰值检测→DDS | ✅ 可用 |
| fig_vv_cpr.drawio | 图4-4 | VV载波相位恢复：四次方→累加→取角→÷4→解卷绕→校正 | ✅ 可用 |
| fig_bps_cpr.drawio | 图4-5 | BPS盲相位搜索：B路并行（旋转→判决→距离）→最优相位选择 | ✅ 可用 |
| fig_dpll_second_order.drawio | 图4-6 | 二阶DPLL：鉴相→环路滤波→NCO闭环反馈 | ✅ 可用 |
| fig_turbo_sync.drawio | 图4-7附近 | 编码辅助迭代载波恢复：DPLL+LDPC双环 | ✅ 可用 |
| fig_cascade_signal_flow.drawio | 图3-3附近 | 三级级联：信道估计→均衡→载波同步（含误差传播） | ⚠️ P10可替代 |
| fig_fpga_architecture.drawio | 图5-1 | 接收端DSP总体架构：ADC→DDC→MF→TS→FOE→DPLL | ⚠️ P12可替代 |
| fig_link_budget.drawio | — | 链路预算（已取消，用公式+表格替代） | ❌ 废弃 |

### PPT/研究流程图（P* 前缀，v3 页码）

| 文件 | v3页码 | 内容 | 状态 |
|------|--------|------|------|
| P5-Timeline.drawio | P5 | 三阶段时间轴（奠基/成熟/扩展） | ✅ |
| P7-method-scenario-matrix.drawio | P7 | 5×2 方法-场景覆盖矩阵 | ✅ |
| P9-Entry-Point.drawio | P9 | 三层切入（需求→不足→路线） | ✅ |
| **P15-Ch2-链路预算.drawio** | **P15** | **系统链+链路预算→SNR范围/α/β** | ✅ |
| P17-Ch3-精度准则.drawio | P17 | 误差影响漏斗+准则桥（v2旧文件名） | ✅ |
| P19-Ch4-准则与探索.drawio | P19 | CPR方法分析+准则输出+拟探索（visio v2旧文件名） | ✅ |
| **P20-Ch5.drawio** | **P20** | **硬件数据通路+验证旁路+资源表** | ✅ |
| P28-Gantt.drawio | P28 | 甘特图（4任务11月） | ✅ |

**注意**：P15/P17/P19 是 v3 拆分后的后半页；前半页（P14系统模型/P16估计对比/P18同步分析）以表格为主，在 PPT 里直接做即可。

### PPT 当前推荐使用版本（v3 页码）

| v3页码 | 推荐文件 | 图型 | 备注 |
|--------|----------|------|------|
| P5 | P5-Timeline.drawio | 三阶段时间轴 | |
| P7 | P7-method-scenario-matrix.drawio | 5×2 方法-场景覆盖矩阵 | |
| P9 | P9-Entry-Point.drawio | 三层切入（需求→不足→路线） | |
| P11 | 结构图.drawio | 研究目标/内容框架图 | 已完成12处文字更新 |
| P15 | P15-Ch2-链路预算.drawio | 系统链+链路预算 | 轻页 |
| P17 | P17-Ch3-精度准则.drawio | 误差影响漏斗+准则桥 | |
| P19 | P19-Ch4-准则与探索.drawio | 方法机制对比+准则输出+拟探索 | 核心页 |
| P20 | P20-Ch5.drawio | 硬件数据通路+验证旁路+资源表 | |
| P29 | P29-Gantt.drawio | 甘特图（4任务11月） | |

### 早期规划/路线图

| 文件 | 内容 | 状态 |
|------|------|------|
| 结构图.drawio | 研究内容总结构（P11） | ✅ 当前P11版本 |
| 信道估计路线.drawio | 信道估计研究路线 | 旧版，P17-Ch3已替代 |
| 载波同步路线.drawio | 载波同步研究路线 | 旧版，P19-Ch4已替代 |
| FPGA验证路线.drawio | FPGA验证路线 | 旧版，P20-Ch5已替代 |
| page-08-literature-gaps.drawio | 文献空白分析（P8） | 可选小修 |

---

## png/ — 仿真结果图

### 载波同步方法对比（开题核心图组）

三张图共同叙事：**分湍流条件的载波同步方法选择与参数设计准则**。

| 文件 | 内容 | 数据来源 | 脚本 |
|------|------|---------|------|
| ber-snr-carrier-sync.png | 载波同步方法BER vs SNR：VV/BPS/DPLL × 3湍流 | sweep_20260601_181320.json, sweep_bps_10seed.json | plot_snr_ber_sweep.py |
| ber-nw-sensitivity.png | 前馈窗长敏感性：VV/BPS BER vs Nw × 3湍流 | nw_sweep.json | plot_nw_sweep.py |
| ber-dpll-omega-sensitivity.png | DPLL环路带宽敏感性：BER vs ω_n × 3湍流 × 3 SNR | dpll_omega_sweep.json | plot_dpll_omega_sweep.py |

- **图1**（方法选择）：不同湍流下三种载波同步范式的适用性边界
- **图2**（前馈参数设计）：弱湍流Nw≥64收敛，中等≥128，强≥256~512
- **图3**（反馈参数设计）：弱湍流稳定范围大，强湍流ω_n>20M即失锁

仿真统一参数：50种子 × 50k符号（图2/3），10种子 × 100k符号（图1），common.py验证，median+保序回归+Savitzky-Golay平滑。

### 其他仿真图

| 文件 | 对应 | 内容 |
|------|------|------|
| ber-snr-gg-fading.png | Ch3 | GG衰落基础BER曲线 |
| fig_kaiti_ch3_nmse_sensitivity.png | 图3-10 | 级联灵敏度：NMSE对BER的影响 |
| fig_kaiti_ch4_dpll_design.png | 图4-8/9 | DPLL设计参数 |
| fig_kaiti_ch4_method_matrix.png | 图4-7 | 方法对比矩阵 |
| fig_gg_pdf.png | 图2-5 | Gamma-Gamma PDF曲线 |
| fig_pilot_pattern.png | 图3-1 | 导频图案（⚠️ 括号倾斜待修） |

---

## others/ — 参考论文截图

| 文件 | 来源 | 可参考画什么 |
|------|------|-------------|
| dongfan_fig2-3_dsp-flow.png | 董凡图2-3 | **DSP处理链框图**（图2-2/图4-2参考） |
| dongfan_fig5-1_fpga-dsp-chain.png | 董凡图5-1 | **FPGA DSP链**（图5-1参考） |
| dongfan_fig5-2_foe-rtl.png | 董凡图5-2 | **FOE RTL架构**（图4-3参考） |
| baijiajun_fig2-6_demod-flow.png | 百家军图2-6 | **解调流程** |

---

## 缺口清单（待画/待确认）

### PPT图剩余项

| v3页码 | 文件 | 当前判断 | 建议 |
|--------|------|----------|------|
| P11 | 结构图.drawio | 已完成文字更新，结构可用 | 如时间允许，再升级反馈箭头/复合框 |
| P8 | page-08-literature-gaps.drawio | 视觉基础较好 | 可做标题、箭头标签、术语小修 |

### P1 优先级（建议画）

| 图号 | 标题 | 参考来源 | 状态 |
|------|------|---------|------|
| 图2-2 | 接收端DSP处理链 | 董凡图2-3 | 待画（简单水平链） |
| 图4-4 | VV载波相位恢复原理 | — | ✅ fig_vv_cpr.drawio |
| 图4-5 | BPS算法原理 | — | ✅ fig_bps_cpr.drawio |
| 图4-6 | 二阶DPLL框图 | — | ✅ fig_dpll_second_order.drawio |

### P2 优先级（可省略 / 不适合drawio）

| 图号 | 标题 | 备注 |
|------|------|------|
| 图2-4 | 星地链路几何示意 | drawio不适合，建议PPT画 |
| 图2-7 | Kolmogorov湍流谱 | 曲线图，Python画 |
| 图5-11 | TestBench验证框架 | 可省略 |

---

## 绘图脚本

| 脚本 | 产出 |
|------|------|
| plot_snr_ber_sweep.py | ber-snr-carrier-sync.png（方法选择图） |
| plot_nw_sweep.py | ber-nw-sensitivity.png（前馈窗长敏感性） |
| plot_dpll_omega_sweep.py | ber-dpll-omega-sensitivity.png（DPLL带宽敏感性） |
| plot_ber_vv_vs_dpll.py | ber-vv-vs-dpll-*.png（旧版，已归档） |
| plot_constellation.py | constellation-vv-vs-dpll.png（旧版，已归档） |
| plot_phase_tracking.py | phase-tracking-vv-vs-dpll.png（旧版，已归档） |
| plot_kaiti_figures.py | 开题阶段仿真图 |
| plot_p009_figures.py | P-009图表规划相关 |
