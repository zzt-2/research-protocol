# 简报：载波同步四候选并行进展（2026-07-08）

> 给：导师
> 来自：学生
> 主题：星地载波同步 Step 4a 维度 D MVE 四候选并行推进情况
> 状态：1 dormant / 3 active（B7/B2/B5），均为 Step 4a 阶段（MVE 前置规约 + sandbox）

## 一句话总览

载波同步方向开了四个候选并行推进。NDA-ML（B11）单载波已坐实 vs DA-ML +1.35~2.5dB 增量但发现双 bug（vs VV 持平是 bug 非物理），现 dormant 修 bug。B7 Gardner TED 跑到 sandbox 4/6 步且核心机制实测成立（周期相关 G(0)=0.132 铁证）。B2 fade-freeze pilot fallback sandbox 三 Go 全 FAIL 后转救援路线（放松前馈化 + power-boosted pilot）。B5 LEO Doppler 短时谱 FOE 阶段 0 全完成短时谱 FOE 估计器已实现待跑 sandbox。

## 四候选状态总表

| 候选 | 主题 | 状态 | 阶段 | 锚论文 | 当前关键数字 |
|---|---|---|---|---|---|
| **NDA-ML**（B11-Q1）| 单载波 NDA-ML STO+CPE | dormant | D-008 双 bug + D-009 线宽待修 | PTL 2025（已发）| vs DA-ML +1.35~2.5dB ✅ / vs VV 持平（bug）⚠️ |
| **B7-Q1** | Gardner TED 复用 FOE | active | sandbox 4/6 步 | OFC 2026 poster | G(0)=0.132 周期相关铁证 ✅ / CRB 下界 59.42kHz ✅ |
| **B2-Q2** | fade-freeze + pilot fallback | active | sandbox FAIL → 救援 D003 | SPIE 2020（已发）| 三 Go 全 FAIL / 稳态 +0.02dB / 动态恢复结构性失效 |
| **B5-Q1** | LEO Doppler 短时谱 FOE | active | 阶段 0 完，待 sandbox | Optics Comm 2024（已发）| ±4.5GHz 范围扩展 15× / 够格走路径 C 鲁棒性维度 |

---

## 候选 1: NDA-ML（B11-Q1）单载波 — dormant

**M-C-A**：DA ML+PA 在 (8,8)-16APSK 25GBaud 下判决错误传播+PA 频谱效率低 → NDA-ML 盲估去 pilot。

**已坐实**：vs DA-ML **+1.35~2.5dB 稳赢**（5 seed 一致，去 pilot 真增量，不依赖 bug）。这是主结论不受影响。

**两个待修问题**：
1. **D-008 双 bug**：vs VV 持平是 bug 不是物理真实
   - Bug 1：B11 Eq.16 是 ML 加权 mean-angle（权重=升幂前接收幅值平方），我们实现漏了加权（等权 mean-angle）→ 跟 VV 数学同族 → 持平必然
   - Bug 2：升幂未归一化，B11 Eq.5 是 `(R/|R|)^M₀` 去幅度，我们实现是 `R^M₀` 含幅度
   - 修复方案已定，等 sandbox 验证后再决定全量重跑 or 降叙事
2. **D-009 线宽疑似选错**：D-007 选 10kHz 低线宽，Valjus 原文 typical 0.1-1MHz，低线宽掩盖了 D-008 bug（样本 SNR 均匀加权≈等权）

**下一步**：方法方向 X（换改进 VV）/W（segmented+高线宽）待用户拍板（拒 E 找老师 / Z 转系统层）。

---

## 候选 2: B7 Gardner TED 复用 FOE — active，sandbox 4/6 步

**M-C-A**：传统 PSA FOE 在星地 COSC 高 CFO 场景下估范围窄（0-12GHz）失效 → Gardner TED 增益周期相关作 Doppler 指纹复用 FOE（0-23GHz）。

**阶段 0 六项规约全完成**（D001-D005）：
- **0.1 公式完整性**：Gardner TED 1986 公式源用学生本地 Matlab 代码（`毕设/旧本科代码/PSKTimingErrDetector.m`），不切降级
- **0.2 数学同族性**：B7 vs Gardner TED 1986 = **弱同族 (B)**（共享底层 TED 公式但任务正交：B7 做 FOE 估频偏，1986 做 STR 检测定时误差），**非 NDA-ML D-008 陷阱**
- **0.3 架构定性**：FOE 前馈化不撞 D006
- **0.4-0.6**：fair gain 二维报告 + B7Params 15 字段全溯源 + explore 目录落盘

**Sandbox 前 4 步已完成**（D006）：
- B7Params 回写到 params.py
- PSA FOE baseline 重写（谱不对称法）
- **TED_gain 解析推导**：G(f_D)=K_max·|cos(πf_D/B)|，与脉冲形状无关，闭合 D002 残留风险
- **CRB 下界 59.42kHz**（<<扫频间隔 1GHz，FR-21 不卡）
- **周期相关实测铁证**：G(0)=0.132142，FFT 主频能量占比无噪 95.9% / OSNR17dB 90.7%（>50% 阈值）

**下一步**（剩 2 步）：
- 步骤 5：三方对照主脚本（B7 proposed / Gardner 1986 TR 祖师爷 / PSA FOE baseline）
- 步骤 6：MVE + consistency + Go/Conditional Go/Kill 判断

**风险**：三方对照若 B7 vs Gardner 1986 BER gap <0.1dB（持平）即停（V3 祖师爷红线）；0.6dB @ BER 2e-2 在 HD-FEC 处可能 <0.3dB 触发 Conditional Go。

---

## 候选 3: B2-Q2 fade-freeze + pilot fallback — active，sandbox FAIL 转 D003 救援

**M-C-A**：[79] Matsuda FOE freeze 在 deep fade 冻结后恢复时 FO 已漂移需重新收敛 → 双模切换（blind freeze + pilot-aided fallback）。

**阶段 0 六项规约 + sandbox 全完成**（S001-S004 + D001-D003）。

**关键发现：sandbox 三 Go 全 FAIL**
1. **动态恢复结构性失效**（致命）：前馈架构下 fade→非fade 第 1 块 BER 已近稳态（比值 0.80），A_recover ≡ C_recover 21 点全相同。**前馈化导致动态恢复测度失效**（架构-测度不匹配）
2. **稳态 BER 公平 gain 仅 +0.02dB**（远低于 0.5dB 阈值）
3. **范围扩展无**

**C2 红线解除**（da_ml 多数 fade 场景赢 blind NDA-ML），命题逻辑可继续。

**方向定夺（D003，用户推翻主线 Kill 建议）**：转救援路线——放松前馈化（D002）+ 加 power-boosted pilot。
- 精读 D006 后修正：[79] 式闭环 hold 不撞 D006（门控用功率不用相位），阶段 0.3 前馈化 INVARIANT 过度保守
- 3 个诚实风险已标注（power-boost overhead / 跟 [79] 差异够格性 / sat.1553 +1dB 口径错位）

**下一步**：阶段 1.5 重设计（0.3 重定性闭环 hold / 0.4 重审公平对照加 power-boost overhead / 0.5 加参数 / 重跑 sandbox）。

---

## 候选 4: B5-Q1 LEO Doppler 短时谱 FOE — active，阶段 0 完待 sandbox

**M-C-A**：[60] Leven Mth-power 时域相位增量（QPSK 专用）在 LEO 下行 Doppler ±4.5GHz 大动态下 FPGA 资源大且 M-PSK 专用 → 分块 FFT + 正负功率谱面积比 + 星历预测（不限 QPSK 无 pilot）。

**特殊**：**不是 dB 增量是范围优势**（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展），D005 "赢 baseline 几 dB" 标尺下不够格。

**阶段 0 六项规约全完成**（S001-S003 + D001）：
- **0.1 够格路径**：走路径 C（鲁棒性维度，对标 B7 OFC 已发先例）+ 路径 A（BUPT Arria 10 FPGA demo 模板）补充。不转 Kill
- **0.2 dB/范围溯源**：20 字段全溯源 + [60] Leven 7dB penalty 溯源到原文 L123
- **0.3 架构定性**：前馈归一化路径定死（湍流致功率波动归一化不撞 D006）
- **0.4-0.6**：公平对照框架（baseline=传统 FFT FOE + [60] Leven 祖师爷 + fair gain 二维）+ B5Params 20 字段 + short_time_spectrum_foe 接口

**实现进度**：`_short_time_spectrum_foe.py`（31KB）+ `_leven_mthpower_foe.py`（13KB）已落盘并 import 编译，含 C6 公式重建标注（PDF→md 公式丢失，从文字重建）+ normalize_mode 三方案 + 迭代收敛处理。

**下一步**：sandbox 三方对照（B5 短时谱 / [60] Leven Mth-power 祖师爷 / 传统 FFT FOE）。

**风险**：低 SNR 块归一化放大噪声可能致残频超 140MHz（sandbox 确认条件）；B5 锚式 2-4 PDF→md 公式丢失（picture omitted），实现靠文字重建有公式核对风险。

---

## 跨候选观察：LEO Doppler 主题机制正交

B5/B7/B4 三个候选是 LEO Doppler 大动态的三种正交解法，可作大论文跨章节统一叙事：

| 候选 | 机制 | 范围/dB | 维度 |
|---|---|---|---|
| **B5-Q1** | 频域正负功率谱面积比 | ±4.5GHz 粗估（15×）| 算法层 |
| **B7-Q1** | 定时域 TED 增益周期相关 | 0-23GHz 扫频 + 0.6dB OSNR | 算法层 |
| B4-Q1（未开）| 双反馈环架构 | ±920MHz @ 0.5dB | 架构层 |

机制正交无撞车风险，B5 频域积分 / B7 定时域周期相关 / B4 双环架构运算结构无共享。

## 守住的防线（教训总结）

- **NDA-ML D-008 vs VV 持平陷阱**：B7 阶段 0.2 数学同族性检查 + B2 阶段 0.1 张力验证设计都是反这个陷阱的防线（B7 已验证非同族，B2 验证 da_ml 在 fade 多数赢 blind）
- **TL-20 先建理论预期**：B7 sandbox 步骤 3 给出 G(f_D)=K_max·|cos(πf_D/B)| 解析式
- **TL-26 参数溯源**：B7Params 15 字段 + B5Params 20 字段全标文献来源
- **FR-22 GW 流程门控**：四候选全在 Step 4a 维度 D，无跳框架
- **D005 务实路线 + FR-21 降级**：B7 CRB 下界 59.42kHz << 扫频间隔 1GHz，FR-21 不卡

## 需要您指点的事项

1. **NDA-ML 方法方向（X/W）**：vs VV 持平是 bug，修完 sandbox 后选 X（换改进 VV）还是 W（segmented+高线宽）？您之前意见 1（线宽扫描 10k-500kHz）已触发 D-007，但 Valjus 原文 typical 0.1-1MHz 我们现在没用，要不要修正回 Valjus 区间？
2. **B2 救援路线认可**：用户已推翻主线 Kill 建议选救援（放松前馈化 + power-boosted pilot）。如果您觉得救援路线不成立可以喊停
3. **B5 够格路径（路径 C 鲁棒性维度）**：B5 不是 dB 增量是范围优势，靠鲁棒性维度够格（对标 B7 OFC 已发先例）。如果您觉得会议级别需要补 dB，B5 要重新评估
4. **大论文叙事**：B5/B7/B4 LEO Doppler 三种正交解法能否作跨章节统一叙事？还是各自独立成章？

## 备注

本简报事实来自仓库 `.sessions/` 下各专题的 S### session note + decisions.md + sandbox results.json，可追溯。NDA-ML 专题 `2026-07-06-step4a-mve-execution/`，B7/B2/B5 专题 `2026-07-08-{b7-gardner-ted-foe,b2-fade-freeze-pilot-fallback,b5-leo-doppler-spectrum-foe}/`。
