# Handoff: BER 补点实验结果回传写作专题

> 来源: S013（step4a 实验日志）| 交接目标: 把 BER 补点实验结果交给写作专题用于主图绘制 + 跟老师汇报
> 文件名: H002-ber-extension-experiment.md

## 已完成边界

**导师要求 BER 展示到 1e-5 的补点实验已跑完（5 seed 探索性，两轮）。**

任务来源：S002 末尾"后续"段 + 导师反馈"BER 要展示到 1e-5"（现有 30seed 主实验只到 1e-2~1e-4）。

**两轮补点**：
- 第一轮（`run_ber_ext_5seed.py`，6 场景补到 44/46dB，115s）：验证 brief 预判。结果推翻了"strong/uplink 有 deep fade 地板"的预判——BER 全程单调下降无趋平。
- 外推发现 strong/uplink 到 1e-5 需 64-81dB（无物理意义）。用户决策（本轮）：折中方案，补到 50dB 探边界即可。
- 第二轮（`run_ber_ext2_5seed.py`，strong/uplink 补到 50dB，18s）：确认"仍在降只是慢"，无地板。

**核心结论（一句话）**：3 个场景（awgn/weak/moderate）能画到 1e-5；3 个场景（strong/uplink_moderate/uplink_strong）画不到，无地板但衰减率慢（~1.4×/2dB vs 轻湍流 ~3×/2dB），到 1e-5 需 64-81dB 远超实际工作区。

**已生成**：
- 分析报告：`projects/simulation/results/sc_nda_ml_ber_ext_5seed/_ber_ext_5seed_report.md`（含 5 段格式：SNR 范围+最低BER / 1e-5达标 / 地板实测+外推 / 结论+怎么跟老师说 / 数据位置）
- 合并图：`projects/simulation/figures/fig2_ber_ext_merged.png/.pdf`（6 子图，30seed 实线 + 5seed 补点虚线，标 HD-FEC 3.8e-3 线 + 1e-5 线）
- JSON：`_ber_ext_5seed.json`（第一轮）+ `_ber_ext2_5seed.json`（第二轮）

## 不要做什么

- **不要硬补 strong/uplink 到 1e-5**：外推需 64-81dB，远超星地 FSO 实际工作区，补这种点无物理意义（守 TL-22）。已用 50dB 探边界确认"无地板、仍在降只是慢"。
- **不要把 NDA<oracle 的 9 个单 seed"违例"当算法错误**：全部是 BER≤1e-4 区的离散计数涨落（错误 bit ≤30，泊松统计），mean 层面算法 NDA≥oracle 成立。详见报告 §3 TL-23 自检段。
- **不要改 common/ 或现有 30seed 配置**：补点脚本（`run_ber_ext_5seed.py` / `run_ber_ext2_5seed.py`）是薄包装，除 SNR 范围 + seed 数外一切沿用 `run_main_experiment_30seed.py`（守 TL-13）。`common/` 未动。
- **画图时不要把零错点当真零**：awgn/weak 高 SNR 区 BER=0 是分辨率极限（102400×4=409600 bits 无错，~2.4e-6），画图时用 2.4e-6 下限替代 0 避免 log 报错（`plot_ber_ext.py` 已处理）。

## 必读

1. `projects/simulation/results/sc_nda_ml_ber_ext_5seed/_ber_ext_5seed_report.md` —— 完整分析报告（最高优先，含怎么跟老师讲的话术）
2. `projects/simulation/figures/fig2_ber_ext_merged.png` —— 合并主图（6 子图）
3. S002（本专题）末尾"后续"段 —— 本轮任务来源 + 图表方案锁定（5 图 + 2 表，图 2 = BER vs SNR 4 子图下行）

## 接口变更（如有代码改动）

无 common/ 改动。新增 3 个独立脚本（薄包装，复用 `sc_nda_ml_sim.run_awgn/run_turb`）：
- `simulator/run_ber_ext_5seed.py`（第一轮补点，6 场景）
- `simulator/run_ber_ext2_5seed.py`（第二轮补点，strong/uplink 到 50dB）
- `simulator/plot_ber_ext.py`（合并画图）

## 失败数据附录（如涉及路线失败）

**预判失败（非实验失败）**：brief 原预判"strong/uplink 有 deep fade 地板，补 +18dB BER 卡在 10⁻² 不动"。**实测推翻**：BER 在 28→50dB 全程单调下降（strong 从 1.76e-2 降到 2.0e-4，~1.9 个数量级），衰减率稳定 1.35–1.7×/2dB，无趋平 → 无地板。

**这是对 deep fade 机制的正确化**：deep fade 的正确表征是"BER 曲线斜率显著变缓"（衰减率从轻湍流 ~3×/2dB 降到 ~1.4×/2dB），不是"BER 卡死"（伪地板）。原"伪地板"叙事若写进论文会被审稿人质疑，需修正。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 补点是 5 seed 非正式统计 | CI 可信需 30 seed | 报告/图注已标清"5 seed 探索性" | 若老师要求正式统计 → 升级到 30 seed（seed 策略已对齐 30seed 前 5 个，可直接扩） |
| 主图 6 子图 vs S002 锁定 4 子图 | S002 图 2 定 4 子图（下行 awgn/weak/mod/strong） | 本轮画了 6 子图含上行，画法定稿时可裁 | 跟老师确认主图画 4 子图（下行）还是 6 子图（含上行） |
| moderate 刚破 1e-5（46dB oracle=8.3e-6） | 稳健破 1e-5 需更多裕度 | 46dB 时 DA=9.1e-6 略高于 1e-5 | 若老师要更稳的 1e-5 图 → moderate 补到 48-50dB（衰减率 ~1.8×，48dB oracle≈4.6e-6） |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| TL-23 NDA≥oracle（mean 层面） | mean NDA≥oracle，0 违例 | TL-23 | 主区间 100%（30seed 0 违例）；高 SNR 补点区 mean 层面 2 个微小计数伪影翻转（awgn@22/weak@36，≤30 bits 区） |
| 配置一致性 | 除 SNR 范围+seed 数外与 30seed 一致 | TL-13 / 任务纪律 | PASS（薄包装，common/ 未动，参数全 import） |
| 数据拼接连续性 | main 顶→ext 起的 BER 跨度符合衰减率 | 数据合理性 | PASS（全程 2dB gap，无重叠无缺失） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（写作专题定位 = GW 阶段写作准备辅助，不跑新实验）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] moderate 46dB oracle BER = 8.3e-6（已破 1e-5）—— 查 `_ber_ext_5seed.json` summary.moderate.points 末点
  - [ ] strong 50dB oracle BER = 1.95e-4（离 1e-5 还差 20×）—— 查 `_ber_ext2_5seed.json` summary.strong.points 末点
  - [ ] 外推到 1e-5 需 SNR：strong ~68dB / uplink_strong ~81dB —— 查报告 §3.2
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（依赖 step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（本轮是回 step4a 跑实验，实验产物回传写作专题，未在写作专题跑实验——守 FR-22）

## 下一轮

**主图绘制方向已定，数据齐了**。本轮把 BER 补点 + 合并图做完，下一轮写作专题可：
1. **跟老师汇报 BER 补点结果**（用报告 §4 的话术：3 场景到 1e-5 + 3 场景 deep fade 衰减慢 + 画法建议）
2. **定主图最终画法**：本轮合并图是初版（6 子图 + 5seed 虚线区分）。需跟老师确认：①画 4 子图（下行，S002 原定）还是 6 子图（含上行）②strong/uplink 子图纵轴是否收窄到 1e-4~1e-1（不硬凑 1e-5）
3. **简报补 BER 补点结论**：把"BER 能画到 1e-5 的 3 场景 + deep fade 衰减率数据"加进 ADVISOR_BRIEFING
4. **论文包装流程**（S002 末尾用户提的"把这坨包得像样"）：本轮数据是图 2 主图的完整数据源，可进论文 System/Results 节

**注意**：本轮实验跑在 step4a 专题（实验日志记 S013），结果回传写作专题。写作专题本身不跑实验（守 FR-22）。如需再补点（如 moderate 补到 48-50dB）或正式统计（升级 30 seed），回 step4a 专题跑。
