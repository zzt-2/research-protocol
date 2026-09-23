# step-210 — 连续均衡/信道跟踪主选块两级承重性诊断（R031 §六任务②③④）

> 2026-09-23 | 授权：D055/D056（PROMPT-025 夜间自主执行轮）| 模块：`projects/simulation/explore/ch4-init-burden-diagnostic/`
> 合同：`contract.yaml`（阶段一，执行前冻结）+ `contract_phase2.yaml`（阶段二，v1.0→v1.1→v1.2，eval 前冻结）
> 结果目录：`projects/simulation/results/ch4-init-burden-diagnostic/` | 治理：R033/V041/D057+/S018§29

## 目的

回答 R031 两个 Kill 问题：① 现有链前端估计误差（4 Walsh 前导 LS 估 Jones + plain RDE μ=1e-3 冷启动，`post_ch4_ch3_bridge.py:349-350`）是否承重（真值初始化 FER 差）；② 连续轨迹合同下跨窗信息能否兑现、部署臂能否胜过 EMA/RLS 廉价对手。

## 实现要点（真值提取与隔离）

- 零改动冻结模块。B0 臂走 `single_cell.run_coded_receiver` 冻结路径。
- 真值提取 = 冻结生成器 RNG 流重播（legacy: gg_block→doppler_phase；PCG64(seed): random_su2→noise），逐帧 bit 级重建验证 `jones @ (tx·scalar) + noise == received`（512+2048+512 帧全过，无一例外）。
- 真值只进 oracle 臂的 demux 初始化/冻结与评分层；不进 B0、DA CPR、LLR、译码。
- seed 隔离：anchor 4000-4511（复现用）；eval 60000-60511；confirm 61000-63047；阶段二 dev info 70000-70255 / eval info 71000-71511 / traj 80000-80015——与全部 14 个历史块零重叠。

## 阶段一（任务②）

- **实现门（anchor replay）**：seeds 4000-4511 B0 逐帧 bit_errors 与 T077 raw **512/512 完全一致**，聚合 FER=132/512=0.2578。PASS。
- **eval 512 帧**（B0/O1/O1S/O2 同帧配对）：
  - B0 FER=0.3086；O1（纯真值 J^H）=0.4141（**显著更差** −0.1055 [−0.1328,−0.0800]：RDE 从酉初始化获取公共增益 |c| 是真实包袱）；
  - **O1S（无噪前导 LS 理想初始化，Jones+公共尺度真值）=0.2227，B0−O1S=+0.0859 [+0.0605,+0.1113]，46胜/2负，p=8.4e-12 → ALIVE**；
  - O2（理想 demux 冻结无 RDE）=0.2188，O1S−O2=+0.0039 CI 触 0 → **给定理想初始化 RDE 增量≈0（2/512 帧）**；"RDE 残差"不是误差来源，前端价值全部在初始化精度；
  - 分层：增益集中 Q2 边际带（帧均 gg 0.32-0.72：0.242→0.039）；Q1 深衰（≤0.317）0.99→0.85 大头救不动；Q3/Q4 全过。
- **confirm 2048 帧**（冻结论选后跑）：B0−O1S=+0.0776 [+0.0659,+0.0894]，160胜/1负，p=1.1e-46；O1S−O2=+0.0005 CI 含 0。幅度复现，方向/机制全同。**阶段一结论冻结：前端估计误差承重（ALIVE），进阶段二。**

## 阶段二（任务③④）

- **连续轨迹合同**：gg_time AR(1) 块链（τ_c=1/(2πf_G)，f_G=100Hz 档；30/300 敏感性）+ SOP 线性演化（4e-7 rad/symbol，expm(jθA)@J₀，A 轨迹级随机无迹厄米）+ 连续 doppler/Wiener 相位；T077 噪声语义。
- **v1.1 修订（回归门修实现）**：v1.0 的 GG 块全局 256 网格平铺使块边界在 260 符号帧内漂移；rho-check 探针（f_G=1e7）暴露深(0.065)→强(8.6)帧中跳变给前导增益留 60+ 强符号 → 冻结 plain RDE 径向动力学增益过冲翻号发散（traj81010-f14 符号 204 起）。对照实证：冻结 T077 生成器 3000 帧 0 发散（含 111 个 block1<0.1 深帧）——gg_block(260) 固定把块边界放符号 256。修订为帧内对齐 T077 约定（帧 t 用链条目 2t/2t+1）。**附带机制登记（实现探针观察，非科学声称）：深→强帧内 GG 跳变 + ≥60 强符号会发散冻结 plain RDE。**
- **回归门**：rho-check（f_G=1e7, sop=0, 512 帧）B0* FER=0.2383 ∈ [0.20,0.36]，gg 均值 1.039 ∈ [0.9,1.1]。PASS（delegation 模式 bit 级 = 阶段一 anchor replay PASS 复用）。
- **v1.2 修订（第 1 轮调参诊断出跟踪臂缺陷，eval 未跑时修）**：第 1 轮 dev 调参 EMA/RLS/C40 全网格 FER 0.69-0.93 塌缩（B0* 0.12、C40 λ_r=0.5 0.13 不受影响）。机制：连续相位合同下公共相位每帧推进 2π·1e6·260·0.4ns≈0.653 rad，跨帧平均旋转相位矩阵 → 幅度塌缩；RDE 更新严格径向（z'ᵢ=zᵢ(1+μgᵢ(Rᵢ²−|zᵢ|²)‖y‖²)，帧内相位不变）、DA CPR 消常数相位，故单先验臂（ORC 型）不受影响。修复 = 跨帧输入项公共相位规范化 W·exp(−0.5j·angle(det W))（det 变正实；实现过程中还修掉两个次生缺陷：半角符号首版写反致相位翻倍；半角 ±1 分支在 det 相位跨 ±π 回卷时翻号需对运行参考做符号对齐）。B0* 不动。第 1 轮调参作废留档 `phase2_tuning_round1_diagnosis.json`。
- 修复后探针（traj80000/80003）：初始化误差阶梯 ORC 0.014-0.018 < EMA 0.073-0.110 ≈ RLS < C40 0.119-0.149 < B0* 0.160-0.227，符合理论序。
- **臂**：B0*（μ* dev 调优）/ ORC（上一帧真值理想先验，规范化域）/ EMA(β) / RLS(λ) / C40(λ_r) / EMA0（EMA 冻结无 RDE 简化探针）。
- eval/sensitivity/三道门判读：见 contract_phase2.yaml（gate A 时间轴 / gate B 身份 / gate C 幅度）。

（eval 与敏感性数字由 R033 承载，本 log 记录执行事实与修订链。）

## 纪律自检

- 不修改 ch5-apsk-llr-calibration / ch5-apsk-structured-covariance / ch4-apsk-ring-gated-rde / common / params.py（git status 复核）。
- 不复用旧 LLR 缓存（从物理帧层重新生成）；不修改任何历史 raw。
- 预注册判读规则于两份合同，eval 前冻结；看结果后未改阈值/未加臂/未换 seed。
- 阶段一 1 轮 + confirm；阶段二第 1 轮（回归门修实现+调参诊断）+ 第 2 轮（修复后调参+eval），在"每阶段最多两轮"预算内。

## V041 复核轮（收尾，2026-09-23）

- 独立 agent 五项检查：raw 重算 PASS（eval 4 帧×4 臂 + anchor 2 帧三方 bit 级一致；附加严格真值重放 6 seed BIT_EXACT）/ 锚点与统计 PASS（512/512、wins/losses 与 bootstrap CI 逐位复现）/ 真值隔离 PASS（行号级）/ 实现与合同 PASS（冻结模块零改动、seed/判读/冻参一致）/ 数值抽查 5a PASS。**总裁定 PASS with notes。**
- 必修①（已修）：`run_diagnostic.py` 真值逐帧验证写成自比较（`array_equal(recon, recon)`）——合同承诺的 bit 级门空转；存量数字由锚点门 + 外部严格重放双重证实。修正为 `array_equal(recon, received)`。
- 必修②（已修+重跑，合同 v1.3）：RLS 臂求解共轭错（厄米 R 下 `solve(R,P.T).T` = P·conj(R⁻¹) ≠ 合同 P·R⁻¹）。修复 → 仅重调 RLS 网格（λ=0.99 仍选中，dev 0.0469→0.0312）→ 重跑 eval+sens30+sens300：**三批判读全部不变（IDENTITY_COLLAPSE）**；RLS 修复后 131/512 与 EMA/ORC 同触顶。旧 raw 留档 `results/ch4-init-burden-diagnostic/rls_conjugate_bug/`。
- 建议两项已落实：R033 轨迹叙事勘误（4 深衰/10 好/2 边际；10/10 不一致帧）；phase1_frozen_pre_confirm.json CI 转写笔误 erratum 字段补记。
