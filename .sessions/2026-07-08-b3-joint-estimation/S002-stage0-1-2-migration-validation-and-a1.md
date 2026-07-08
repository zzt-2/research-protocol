# [S002] 阶段 0.1-0.2 执行：4 支路迁移验证 + 单链路 CRB + A1 归属核查

> 2026-07-08 | 阶段 0 前置规约（0.1-0.2）| 状态：阶段 0.1-0.2 完成，不 Kill，进 0.3-0.6
> 来源: H001 + PROMPT-001 派发（工作对话 1）

## 目标

执行 B3-Q2 阶段 0.1（4 支路迁移验证 + 单链路 CRB 上界）+ 阶段 0.2（A1 归属核查），不写代码。判定门控：星地多孔径阵列不成立 + 单链路 CRB <0.5dB → 转 Kill。

## 记录

### 步骤 1：报到 + 必读清单 1-6

session-governance Trigger 1 报到。读 topic-index（15 不变量）/ H001 / S001 / decisions(D001) / B3 详评 / jphot / oe 笔记 / `_cut-b1b2b3-verify.md` / S031 详评 / D005 / D006 / `_recovery.py` / gw-feasibility §D / TL-13/20/26/27 / sim-preflight §1.6 C6-C8 / voice / B2 Kill D004。

接收方验证 4 条全打钩（topic-index 不变量 + 3 事实声称 + _registry depends_on + 明确不含）。

### 步骤 2：阶段 0.1 星地多孔径阵列场景验证 + 单链路 CRB（并发 2 子 agent）

**0.1a 星地多孔径阵列场景验证**（子 agent，606s）：
- 4 问结论：场景 A（地面多望远镜收卫星下行）有文献（Ma 2015 仿真 / Geisler 2016 架构）但无已部署工程实例；AO+多孔径分集无成熟组合（主流 = 单孔径+AO，Horst 2023）；ESA/JPL/NICT/CAS OGS 均单台大口径；sat.1553 不提星地分集（仅单孔径 aperture averaging）
- 主线 grep sat.1553 content.md:149 确认 PASS

**0.1b 单链路 CRB 上界**（子 agent，628s）：
- FOE CRB（FSTS 两段式 BL² 降噪 vs 传统 TS）：方差域 +26dB；可兑现灵敏度上界 ≈ +1.0~1.2dB（MSE 陡崖封顶）≥0.5dB，不触发 FR-21 Kill
- 自洽性 PASS（上界 1.2 ≥ 实测 1.17）
- **子 agent 主动报 2 个反直觉发现**：① "单链路 dB 砍半假设不成立"（单支路 1.17 ≥ 4 支路 0.7）② 增益归因警示（dB 来自 FOE 算法结构非协同）

### 🔴 FR-26 核查：发现 4 支路 dB 转录错误

0.1b 子 agent 的"单支路 ≥4 支路"反直觉结论触发主线独立 grep jphot 原文：
- jphot-L357（Fig.16/17 four-branch 专图）："PM 4-QAM ... **0.31 dB and 0.7 dB** strong turbulence [960/320]"
- jphot-L375（Fig.18 多支路对比）："branches 1,2,4,6 ... 4-QAM **1.17, 2.09, 0.7, 1.72** dB strong"
- jphot-L385（Conclusion）："**two-branch MRC** ... 2.09 and 3.41 in strong turbulence"

**坐实**：note-L36 + verify 文件 + S031 的"4 支路 +2.09/+3.41"实为 **2 支路**数字。4 支路真实 = 0.7dB(4-QAM)/2.14dB(16-QAM)。单支路 4-QAM = 1.17dB（≥4 支路）。

### 步骤 3：阶段 0.1 门控判定 + 阶段 0.2 A1 归属核查

**0.1 门控判定（不 Kill）**：星地多孔径阵列部分成立 + 单链路 CRB 1.0~1.2dB ≥0.5dB。守 D005 务实路线 + 导师"特长场景"标准，单链路强湍 FSTS 联合 vs 分立就是合法特长场景。

**0.2 A1 归属核查**（主线查 jphot 原文）：
- jphot 已 claim：FSTS 一套 TS 做 FS+两段式 FOE+MRC 联合 + BL² 降噪 + 跨极化共轭（全 B3-Q2 不能再 claim）
- jphot 未 claim / B3-Q2 切口：CPE 联合维度（jphot CPE 独立）/ Doppler 维度（jphot-L208 自承缓变假设）/ 星地场景（jphot grep LEO/satellite = 0 命中）
- **首要风险转移**：4 支路迁移 → 增益归因（单链路 dB 来自 jphot 已 claim 的 BL² 算法结构）
- baseline 硬约束：必须含 jphot FSTS（不只比传统 TS，否则增益是继承的）

### 产出物

1. `explore/b3-joint-estimation/_stage0_1a_aperture_diversity_scene_survey.md`（0.1a 子 agent）
2. `explore/b3-joint-estimation/_stage0_1b_single_link_crb_upper_bound.md`（0.1b 子 agent）
3. `explore/b3-joint-estimation/_diversity_migration_validation.md`（0.1 主线判定整合）
4. `explore/b3-joint-estimation/_a1_attribution_audit.md`（0.2 A1 归属）

## 决策引用

- **D002**（新建）：阶段 0.1-0.2 完成，不 Kill + 修正 4 支路 dB 转录错误 + B3-Q2 增量定位为迁移+维度扩展型
- D001（沿用）：开 B3-Q2 专题首验证迁移——已执行完成，结论不 Kill

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.2，不写代码，不进 sandbox）
- 未违反"明确不含"（不回头救 Kill 候选 / 不判其他方向 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 后续

### 已答（本轮闭合）
- 星地多孔径阵列场景：部分成立（不 Kill）
- 单链路 CRB：1.0~1.2dB ≥0.5dB（不 Kill）
- A1 归属（本地层）：jphot 已 claim 算法机制，B3-Q2 切口在 CPE/Doppler/星地

### 待办（下一对话）
1. **阶段 0.3 架构定性**：加 Doppler 维度的形态——前馈开环（不撞 D006）vs 环路 TF（撞转 B3-Q3）
2. **阶段 0.4 公平对照框架**：baseline 必须含 jphot FSTS
3. **阶段 0.5 参数真相源**：Cn²/线宽/望远镜口径/调制格式全标 source
4. **阶段 0.6 文件组织**：explore 目录 + MRC/帧同步/多支路管线接口
5. **🔴 派子 agent 查 BUPT 课题组 2024+ 续作**（Liqian Wang / Siqi Zhang，防自吞增量）
6. **修正转录错误**：note-L36 + `_cut-b1b2b3-verify.md:258-291` + S031 的"4 支路 +2~3dB"