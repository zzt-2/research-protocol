# decode-failure-rescue — 译码失败码字门控救援诊断（GW 4a-D 有界实验）

> 权威：`.sessions/2026-08-30-thesis-advisor-text-outline/R029` + 本目录 `contract.yaml`（执行前冻结）。
> 2026-09-20 本轮授权（D051）：只读限制解除，允许最小接口扩展 + 有界小规模实验；不改正文/不换场景/不动历史模块。

## 目的

在 T077 冻结格（DP-16APSK 中湍流 15dB，5G BG2 (1024,1536) NOMS(0.75,0) 20 迭代，FER≈0.258）上回答：

1. 失败码字的结构（停滞/振荡/慢收敛/收敛错码字占比；syndrome 权重与硬判错误数分布）；
2. 纯延长迭代（常规替代）能救回多少；
3. 定向擦除（R2）/配置切换（R3）相对延长的增量；
4. oracle 置零（O1，诊断专用）的 headroom。

## 布局

- `contract.yaml` — 预注册冻结合同（臂/指标/正确性门/预算/解释边界）。**执行后不改，修订走新版本。**
- `generate_llrs.py` — 复用 `../ch5-apsk-llr-calibration/single_cell.py` 冻结链生成逐帧 exact-APP LLR 缓存（smoke/dev/eval 三 split）。
- `rescue_decoder.py` — 仪器化 NOMS 译码器（Sionna 状态步进或镜像实现，按 contract decoder.route_decision）。
- `run_experiment.py` — 按合同跑臂，写逐帧 raw + summary 到 `../../results/decode-failure-rescue/`。
- `confirm_contract.yaml` — **确认轮合同（2026-09-20，R030 审查后）**：R2 映射修复 + 统一输出规则 + confirm2048 新样本 + B0/R1/R3/F 臂。运行前冻结。
- `run_confirm.py` — 确认轮运行器（`--verify-mapping` / `--anchor` / `--regress-dev` / `--generate` / `--run` 五个子命令）。
- `analyze_confirm_features.py` — **适用条件轮第一步**：confirm2048 只读特征分析（悬崖—边际带结构），输出 `analysis_confirm2048_features.json`。
- `conditions_contract.yaml` / `conditions_confirm.yaml` — **适用条件轮合同（2026-09-20，D053）**：机制发现、H1-H3 假设、开发批计划与冻结论选规则 / 确认两点冻结件。
- `run_conditions.py` — 条件运行器（`--tag/--seeds/--snr-db/--turb-alpha/--turb-beta`，复用确认轮臂逻辑与统计 + 构成带表；`--analyze-only` 重算构成表）。

## 确认轮要点（2026-09-20，权威 = confirm_contract.yaml + step-208）

- **R2 索引修复**：`rescue_decoder.internal_positions_to_tx` 补 `out_int_inv` 复合（内部 VN → x_short raw → 信道序）。`--verify-mapping` 全过（含 R030 实例 VN209→信道4 与 8 个端到端置零探针）。旧 R2 raw 保留为错误映射实现的历史记录，不据此判定定向擦除机制。
- **统一输出规则**：二阶段 syndrome=0（含早停接受步）→ 采用其输出；否则保留首阶段输出+失败标志。所有头条指标按最终输出计。
- **confirm2048**：seeds 30000–32047（与全部历史 seed 零重叠），15dB 冻结 cell，四臂共享逐帧缓存 LLR，一次运行。
- **结果**（final 口径）：R3 vs R1 = −16 帧（16胜0负，exact p=3.05e-5）；F（从头配置）拿走大部分 FER 收益且 BER +3884 bit 劣化；R3 BER 四臂最优；接受后仍错 0；R3 迭代 24.85 ≈ R1 25.07。详见 `step-208-decode-failure-rescue-confirm.md`。

## 适用条件轮要点（2026-09-20，权威 = conditions_*.yaml + step-209）

- **机制**：救援全部发生在信道硬判错误 [100,140) 边际带；悬崖 ≈140-160；≥160 帧跨全部 7 条件零救援。ch_hd_errors 为真值解释量（非部署信号）。
- **结果**：开发批 4 条件（W13/W12/M14/S16 ×512）+ 确认批 2 条件（confirm_W12 弱湍流12dB / confirm_S16 强湍流16dB ×2048）。**本轮所查条件未放大**：确认收益 −0.63pp（W12，13/0，p=2.44e-4）与 −0.83pp（S16，17/0，p=1.53e-5）vs 锚点 −0.78pp；中湍流降 SNR 反而稀释（H2 否）。正面：方向跨 7 条件 59胜0负；弱湍流点 R3 vs F = −11（p<0.001）显著——门控+热续价值超过配置本身。V039 独立复核 25/25 PASS。详见 `step-209-decode-failure-rescue-conditions.md`。

## 纪律

- 不修改 `ch5-apsk-llr-calibration/`、`coded-decoder-feedback/`、`common/` 任何文件。
- 所有臂共享同一逐帧 LLR 字节；eval 不调参；真值只进评分与 O1。
- 结果落 `projects/simulation/results/decode-failure-rescue/`；worker log 落 `projects/thesis-fso/worker-logs/step-207-*.md`（诊断轮）、`step-208-*.md`（确认轮）与 `step-209-*.md`（适用条件轮）。
