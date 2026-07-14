# [S017] PROMPT-016 执行：扩参数域鲁棒性（5 seeds）+ 改动1新颖性快查

> 2026-07-14 | GW Step 4a 维度 D MVE 扩展（A 边） | 状态：完成，回传主控
> 来源: D022（P015 GO，方法层卖点解冻）+ 用户"两边同时推"+ "能不能动一点点让它好一点点"

## 目标

执行 PROMPT-016 两段任务：
- 段 1（机械活）：5 seeds 扩参数域（f_G/SNR/16QAM），看 ML 优势鲁棒性，拿曲线给论文 results
- 段 2（新颖性快查）：查"用发散判据驱动 ML 训练调度"（改动1）有没有人做过

最高纪律：段1 用 5 seeds；段2 严守场景鉴别；不自己写 D###，结果回传主控。

## 记录

### 治理触发

- Session Start（Trigger 1）：topic 16 S 文件 ≥15 触发 inflation BLOCK 阈值，但判定 PROMPT-016 是 topic-index 当前位置段明确登记的 A 边任务 + 有 D021 范围变更记录，按"已有 scope change record"处置，标注不强制新记录
- 段 2 新颖性查走子 agent（主对话严禁 WebSearch/webReader）
- 段 1 脚本主控自写自跑 + P6 独立复核 per-seed 数据

### 段 1：扩参数域结果（N=2M, 5 seeds, 6 唯一 cell）

**核心反预期**：ML 相对 standard-CMA 的 PI-BER 优势在 N=2M 下**不普适**——6 cell 里 ML 仅 2 cell 均值更优。

| cell | ML PI | stdCMA PI | oracle | ML/std 胜场 |
|---|---:|---:|---:|:---:|
| fg30_qpsk_snr20 | 0.0699 | 0.0853 | 0.0198 | 4/5 |
| fg100_qpsk_snr20 | 0.0837 | 0.0911 | 0.0220 | 3/5 |
| fg1000_qpsk_snr20 | 0.0417 | 0.0021 | 0.0007 | **1/5** |
| fg30_qpsk_snr15 | 0.1158 | 0.1086 | 0.0661 | 2/5 |
| fg30_qpsk_snr10 | 0.1753 | 0.1456 | 0.1208 | 2/5 |
| fg30_16qam_snr20 | 0.2532 | 0.1327 | 0.0736 | 2/5 |

跨 cell：ML excess 均值 0.073 vs stdCMA 0.044，ML 均值更优仅 2/6 cell。

**与 PROMPT-015 的关键差异（陷阱3实证）**：同 seeds 1000-1004 / f_G=30 / QPSK / 20dB——
- N=5M（P015）：ML 5/5 赢，excess 0.00005-0.031
- N=2M（本扫描）：ML 4/5 赢（seed1004 翻转），excess 0.0001-0.16

根因 = late_slice 的 SOP 累积旋转量不同。N=5M late=[4.375M,5M) SOP 漂移大→CMA 漂错解→ML 优势显著；N=2M late=[1.75M,2M) SOP 漂移小→standard-CMA 完美锁定（好 seed PI≈0）→ML 监督残余误差反而更差。

**Sanity**：current-CMA 全 6 cell 最差（PI 0.22-0.35），standard 补 z 因子后全 6 cell 更好（与 P015 一致）。per-seed 经独立重算验证。

**grid 去重说明**：PROMPT-016 §2 文字"35 cells"把基准点算了两次，实际 6 唯一 cell × 5 seeds = 30 trials。

### 段 2：改动1 新颖性快查结果

**改动1 有真创新空间**。核心创新点"用物理发散判据当 ML 重训练触发信号"在 FSO/卫星光和广义通信均无先例。
- Qin/Kulmer/Li：冻结训练（train once）
- Nasr 2026：固定 θ 角网格预训练（非信道状态触发），最危险邻近占点
- Freire-TL：光纤非 FSO，触发是离散参数变化非物理判据
- B2 FOE-freeze / JR-CMA 误差阈值：经典 DSP 的物理 gating，无人移到 ML 训练调度
- Q-new-3 不构成威胁：文献已区分"调在线步长 vs 调重训练触发"

须守边界陷阱（触发频率二难）+ 写作显式区分"信道状态触发"vs Nasr"固定网格预训练"。

### 执行细节

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）。AGENTS.md 指定的 `~/.venvs/torch` 在本 Win 机不存在，用 scoop（PROMPT-016 §4 指定路径）
- 后台全量跑因 harness 10min 上限中断，改 `--max-runs` 分批前台跑（per-seed checkpoint 续跑）
- 复用 ber_vs_snr_scan / ber_16qam_vs_fg 的 7 参 gen_channel（gamma_bar 参数化）；evaluate_outputs 是 QPSK 专用（内部 4 旋转 BER），16QAM cell 自写 evaluate_outputs_16qam（LS 相位校正 + 排列不变 PI-BER）
- run_cma_diagnostic 的 late_slice 默认 [4.375M,5M) 是 N=5M 专用，N=2M 须传 [1.75M,2M)
- CMA overflow RuntimeWarning（高 μ/低 SNR 下 |z|² 溢出）是数值发散预期表现，非 bug

## 决策引用

- 无决策（守 PROMPT-016 §0 最高纪律第3条"不自己写 D###，结果回传主控"）
- 关联 D022（P015 GO，方法层卖点解冻）——本扫描数据显示该卖点外推受限

## 范围确认

- 本轮是否在 scope boundary 内：**是**。PROMPT-016 是 topic-index 当前位置段明确登记的 A 边任务，D021 范围变更已覆盖"统一合法 baseline 后重比"的参数域扩展

## 后续

回传主控后由主控决策：
1. 段 1 反预期（N=2M 下 ML 优势不普适）是否影响 D022 的方法层卖点定位——建议主控将"ML 优于 standard-CMA"严格限定在 N=5M/f_G=30 参数域，不外推
2. 改动1 是否值得投入——有真创新空间但须先界定"ML 有优势的参数域边界"（N 和 SOP 累积旋转临界点）
3. 等 B 边（PROMPT-017 Q-DP3 前置厘清）回传后，两边汇合做方法层战略判断

主控若要基于段 1 数据做决策（如修正 D022 适用边界或立改动1 方向），由主控写 D###。

产出：
- 报告：`projects/simulation/explore/cma-fade-divergence/PROMPT_016_REPORT.md`
- 脚本：`prompt016_param_sweep.py` + `prompt016_plot_trends.py`
- 结果：`results/cma-fade-divergence/prompt016_param_sweep.json`（30 trials + 6 summaries）
- 图：`results/cma-fade-divergence/prompt016_figures/fig{1,2,3}_*.png`
