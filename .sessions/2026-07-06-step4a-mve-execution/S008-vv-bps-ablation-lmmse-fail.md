# [S008] VV/BPS 经典 baseline 实测对照 + LMMSE 复现失败教训

> 2026-07-08 | 阶段：Step 4a 维度 D 收尾（baseline 矩阵补全） | 状态：DONE
> 来源：用户 S007 续接问"能拿哪个比 + 效果好吗"，主线分析后用户选方案 C（切 VV/BPS）

## 目标

用户问："我要是做比较，我能拿哪个比？以及，比起来效果好吗？" + "只要会议毕业，没啥大目标"。
主线分析 3 篇近年 baseline 可比性后给出：DA-ML 稳赢但逻辑上 DA 吃亏，NDA 同类（LMMSE/VV/BPS）是真正软肋。
用户原想先复现 LMMSE（#15 JPhoto，主题方法双贴合），失败后切方案 C（VV/BPS 经典 baseline）。

## 记录

### 阶段1：LMMSE (#15 JPhoto) 复现尝试（失败）

**实现**：`common/_recovery.py:lmmse_recovery`（average-energy 简化版，σ²_ε=N₀/2E_s 全程常数，预算 R⁻¹p 权重一次）。8PSK smoke test RMSE 0.024rad @20dB 看似对。

**复现验证**（`verify/lmmse_repro_check.py`）：16APSK(8,8) AWGN 信道高 SNR 严重 BER floor——@20dB LMMSE BER 0.018 vs NDA-ML 7.5e-4，差 24 倍，且随 SNR 升高 BER 不降（floor）。

**调试**：调 4 种公式变体——R 对角 AOPN 项倍数（1.0/0.5/0.125/0.0）+ 升幂归一化（(r/|r|)^M₀）vs 不归一化（r^M₀）。均不对：
- 归一化版：高 SNR BER 0.018（phi_std 0.158，真值 0.022，7× 波动）
- 不归一化版：BER 0.09~0.24 更差（|r|² 变化剧烈权重被高幅度样本主导）
- R 对角倍数调整：无质变

**根因诊断**：#15 论文 PDF→md 转换把 eq(5)(6)(7)（R 矩阵、p 向量、AOPN 方差闭式）转成 `picture intentionally omitted`。靠文字描述+物理推导重建的 R/p 缺关键细节（疑为 AOPN 方差升幂后精确表达 或 p 向量噪声修正项）。**这不是调参能解决，是公式不全**。

**TL-20 偏离即查落实**：发现 BER floor 立即停（没硬往下推），诊断为公式问题非物理问题。

### 阶段2：用户决策切方案 C

主线诚实汇报卡点 + 给 3 方案（A 继续硬磕查[13]/B 降级定性引用/C 换 VV/BPS）。用户选 C：
> "C吧"

理由（主线判断，用户认可）：会议毕业视角下，LMMSE 是 JPhoton 档级（次档 Trans），即便复现成功论文原话说 16APSK @ 2MHz 跟 DA-ML penalty 都 0.5dB（持平），边际价值有限。VV/BPS 是领域共识经典，common/ 已有实现，工作量小，审稿人更认。

### 阶段3：VV/BPS ablation 重跑（D-007 后真相源）

**发现**：`results/sc_nda_ml_{vv,bps}_ablation/` 已存在但全是 7/6 旧结果（D-007 前 AWGN 500kHz），需重跑。runner 代码已 D-007 适配（用 `awgn_wiener_channel` 默认 SIGMA2_P）。

**执行**：并行后台跑 `run_vv_ablation.py`（112s）+ `run_bps_ablation.py`（293s），5 seed × 4 场景。

**结果**（fair gain @ HD-FEC，正 = NDA-ML 赢 baseline）：

| 场景 | NDA-ML vs VV | 95% CI | NDA-ML vs BPS | 95% CI |
|---|---|---|---|---|
| AWGN | +0.006（持平）| [−0.017, +0.029] | **+0.117**（稳赢）| [+0.091, +0.144] |
| weak | −0.004（持平）| [−0.063, +0.055] | +0.047（CI 跨 0）| [−0.078, +0.172] |
| moderate | −0.004（持平）| [−0.014, +0.007] | **+0.057**（稳赢）| [+0.022, +0.092] |
| strong（工作区）| +0.109 | — | +0.106 | — |

**一致性自检**：VV/BPS 全场景 ≥ oracle（PASS，无超越信息论上界 bug）；VV @18dB AWGN=0.00346 落预期 [0.003,0.005]。

**核心解读**：
1. **NDA-ML vs VV 基本持平**——物理合理：NDA-ML（升幂+ML 闭式）vs VV（升幂+mean-angle）在低 PN（σ²_p=2.5e-5）下差异极小。"NDA-ML 不输经典 VV"成立。
2. **NDA-ML vs BPS 稳赢**（AWGN/moderate CI 下界 > 0）——BPS 是光纤 CPR 事实标准，NDA-ML 在单载波 M-APSK 场景赢它。
3. **VV/BPS 都稳赢 DA**（+1.2~+1.7dB）——印证"NDA 类方法公平对照赢 DA"稳健（不只我们方法）。

## 决策引用

- 无新建 D###（方向选择由用户拍板，LMMSE 失败是技术结果非方向决策）
- **建议在 decisions.md 加 D-008**（LMMSE 复现失败记录 + 方案 C 决策，防后续重试 LMMSE）——待用户确认是否记
- 引用既有：INVARIANT 10（核查机制中性双向）—— VV/BPS consistency 落实
- 引用既有：TL-20（偏离即查）—— LMMSE BER floor 立即停查

## 范围确认

- 本轮是否在 scope boundary 内：**是**（baseline 对照矩阵补全是 Step 4a 维度 D 收尾，在 topic-index 当前范围）
- 没碰简报正文（ADVISOR_BRIEFING 未动，守 handoff 约束）
- 没改主实验代码（VV/BPS 用既有 runner，只重跑刷新结果）
- LMMSE 加到 common/_recovery.py 但标 DEPRECATED（0 改动现有逻辑，守场景 B "新算法=1新文件+0改动"）

## 后续

1. **对照矩阵已齐（会议级）**：DA-ML（稳赢 +1.35~+2.5dB）+ VV（持平，证明不输经典）+ BPS（稳赢，证明赢光纤 CPR 标准）+ LMMSE（定性引论文）。可进简报重写 + 投稿。
2. **未做项**（REVIEW_NOTES TODO 仍 ⬜）：简报重写 / TODO-4 简报修正 / TODO-5 上行写报告 / TODO-6 Doppler 溯源 / TODO-7 加种子
3. **LMMSE 救援路径**（如未来要补）：下 [13] Wang 2022 T-SP 全文拿 R/p 闭式 → 重实现 → 验证。当前不优先。
4. **decisions.md D-008**（建议）：记 LMMSE 复现失败 + 方案 C 决策，防后续误重试。本轮先在 S008 + baseline_report §1.2 记，decisions.md 待用户定。
