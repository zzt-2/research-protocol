# Handoff: A 类（改 loss）KILL，下一类 C（改训练）

> 来源: S027 | 交接目标: C 类（改训练）GW Step 1 检索 + 批量 MVE
> 日期: 2026-07-15
> 文件名: H012-c-class-loss-failed-next.md

## 到哪了（状态）

D030 方法层解冻后第一类 **A 类（改 loss）整体 KILL（D031）**。L1 SOP 不变性正则 + L2 swap 对比学习在 4 档 λ [0.001/0.01/0.1/1.0] × 5 seeds（含 D027 swap-prone 1000/1002）横向 MVE，甜点 λ 均 2/5 胜 p=0.75 不显著；A3 VAE 盲损失 GW Step 1 检索硬撞车（Qin 组 2026 IEEE TCCN "Bootstrapping Blind Equalizer DP-coherent FSO via modulus-rings VAE" = 同作者组+同场景+同机制）defer 不跑。L0 baseline 5-seed mean PI=0.01020 复现 D022。

**核心物理结论（D031，火力重定向依据）**：A 类失败根因 = floor 效应（3/5 clean seeds PI≈0 已无改善空间）+ **时序正交**（L1/L2 loss 正则在训练段施加，但 swap 是 test 段 CMA 在线更新跳盆地 D027/D028，训练时学到的"SOP 不变性"泛化不到 test late 段 57° 极端旋转）。**与 D027 V3（Q-DP4 形态2 约束 Kill）同构**——训练阶段的 loss/约束触及不到 test 段 swap。

## 下一步干什么

**下一类 = C 类（改训练）**，按 D030 执行顺序（A→C→B→D→E，A 已 KILL）。但 C 类进 MVE 前须先用 D031 物理洞察过滤：

- **在线微调**（test 段持续更新权重）→ **触及 test 段**，值得跑
- **SOP 数据增强**（训练时扩 SOP 角度范围）→ **不触及 test 段**（同 A 类失败/D015 Q3-A 同构），大概率 KILL，可跳过或快速验证
- **课程学习**（训练 curriculum）→ **不触及 test 段**，同上

建议：C 类 GW Step 1 检索只查"在线微调 optical equalization"撞车，SOP 增强/课程学习用 D031 同构论证直接 defer（省算力守 D005）。若在线微调无撞车 → 横向 MVE（复用 prompt024 框架，改训练循环而非 loss）。

## 纪律（和下一步直接相关的约束）

1. **守 FR-22**：C 类仍走 GW Step 1 检索（防撞车）→ 四判据 → MVE，归类批量≠跳框架
2. **守 D030 准入**：拼也行 + 试了没用再说 + 唯一硬防线=检索防撞车 + 消融可验（λ=0/拿掉模块得退）
3. **守 D018**：双口径 fixed/PI 并报（复用 `prompt012_longseq_audit.evaluate_outputs`）
4. **守 D031 物理洞察**：训练阶段 loss/约束/数据增强触及不到 test 段 swap——C 类只跑"触及 test 段"的子方向（在线微调），其余用同构论证 defer
5. **复用基建**：`prompt024_a_class_loss_variants.py` 的自定义训练循环 + L0 baseline 锚点 + λ 扫描 + 配对 Wilcoxon Go/Kill 流程可直接复用（C 类改训练循环而非 loss 定义）
6. **参数域锁定**：N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK/seeds 1000-1004/late[4.375M,5M)（D022 域，可复现）

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - A 类 KILL：查 `results/cma-fade-divergence/prompt024_a_class_loss.json` step3_go_kill = {L1: 2/5 p=0.75 KILL, L2: 2/5 p=0.75 KILL}
  - A3 撞车：查 `search-archive/2026-07-15/a3-vae-blind.json` L002 "Bootstrapping Blind Equalizer for Dual-Polarization Coherent" 2026
  - L0 复现 D022：查 JSON step1 L0 mean PI=0.01020 ≈ D022/D029 B=0.01028
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（方法层探索在 D030 授权范围内）

## 接口变更（如有代码改动）

- 新增隔离脚本 `projects/simulation/explore/cma-fade-divergence/prompt024_a_class_loss_variants.py`（不改 common/，import 复用 _ml_equalizer.ButterflyCNNEqualizer2x2 + ml_long_seq_failure.gen_channel/oracle_equalize + prompt012_longseq_audit.evaluate_outputs）。自定义训练循环 `train_variant(loss_name, lam)` 支持 L0_mse/L1_sop_invariance/L2_swap_contrast 三 loss。C 类可复用此框架，改训练循环段。
- 新增结果 `results/cma-fade-divergence/prompt024_a_class_loss.json`（55 runs 完整数据）

## 失败数据附录（A 类 KILL 具体数据）

| 变体 | 甜点 λ | mean PI | ΔPI vs L0 | 胜场 | p 值 | 判定 |
|---|---|---|---|---|---|---|
| L0 baseline | — | 0.01020 | — | — | — | 对照锚点 |
| L1 SOP 不变性正则 | 0.001 | 0.01019 | +0.00001（更差）| 2/5 | 0.75 | KILL |
| L2 swap 对比 | 0.1 | 0.01017 | +0.00003（微差）| 2/5 | 0.75 | KILL |
| L3 VAE 盲损失 | — | — | — | — | — | DEFER（撞车）|

L0 per-seed PI: 1000=0.01000, 1001=0.0, 1002=0.04098, 1003=0.00001, 1004=0.0（3/5 clean=floor, 2/5 swap-prone）。
消融：L1 λ=0 mean=0.01035, L2 λ=0 mean=0.01039（均 <0.01 差退回 L0，PASS）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| C 类 SOP 增强/课程学习未跑实证 defer | D030"试了没用再说"放开试 | D031 同构论证 defer（非实证）| 若主控要求穷举实证则补跑（预期 KILL）|
| A3 VAE 重构为"SOP 专攻盲 VAE"未评估 | D030 准入放宽（拼也行）| defer 待定 | 若 A1+A3 混合方向需复活则另开决策 |
| B/D/E 类未探索 | D030 全类穷举 | 待执行 | C 类完成后按顺序 |

## 下一轮

1. **C 类 GW Step 1 检索**（~10 min）：查"online fine-tuning optical equalizer / online adaptation neural network optical communication"撞车。SOP 数据增强/课程学习用 D031 同构论证 defer 不检索
2. **C 类横向 MVE**（若在线微调无撞车）：复用 prompt024 框架，改训练循环（test 段在线微调 vs L0 baseline），5 seeds + 消融
3. C 类完成后看全貌：若仍 KILL → 进 B 类（改架构，成本上升）；若全类穷举完仍 KILL → 接受 D022 窄域形态进 Execute（D030 软退出判据）
