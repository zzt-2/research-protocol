# Handoff: 对话 2 — 阶段 0.3-0.6 前置规约（架构 + 公平对照 + 参数 + 文件）

> 来源: S002 | 交接目标: 新工作对话执行阶段 0.3-0.6（不写代码）
> 日期: 2026-07-08
> 文件名: H002-conversation2-stage0-3-6.md

## 到哪了（状态）

工作对话 1 执行完阶段 0.1-0.2（S002/D002），**B3-Q2 不 Kill**。关键结论：

1. **阶段 0.1 门控 PASS**：星地多孔径阵列场景部分成立（有仿真+架构提案，无已部署工程；sat.1553 不提星地分集）；单链路 CRB ≈1.0~1.2dB ≥0.5dB（FR-21 不卡）。单链路强湍 FSTS 联合 vs 分立就是合法特长场景
2. **🔴 修正 4 支路 dB 转录错误（D002，FR-26 级）**：旧"4 支路 +2~3dB"实为 **2 支路**（jphot-L357/L375/L385 双源确认）。真实：2 支路 +2.09/+3.41dB；**4 支路 = 0.7dB(4-QAM)/2.14dB(16-QAM)**；**单支路 4-QAM 强湍 = 1.17dB（≥4 支路，单链路反而最显著）**
3. **阶段 0.2 A1 归属**：jphot 已 claim 两段式 FOE + FSTS + BL² 降噪（B3-Q2 无算法机制增量）；B3-Q2 切口 = **CPE 联合维度 + Doppler 维度（jphot-L208 自承缓变假设）+ 星地场景**（jphot 0 提 LEO/satellite）
4. **🔴 首要风险转移**：从"4 支路迁移"→"增益归因"——单链路 dB 来自 jphot 已 claim 的 BL² 算法结构，**baseline 必须含 jphot FSTS 才公平**（不只比传统 TS，否则增益是继承的）

未写代码，未进 sandbox。explore/b3-joint-estimation/ 有 4 份文档（0.1a/0.1b/0.1 整合/0.2）。

## 不要做什么

1. **不要跳阶段 0 写代码 / 进 sandbox**（守 profile 第 9 次防线 + INVARIANT 6：阶段 0 六项全做完才进 sandbox）
2. **不要 claim jphot 已有的算法机制**（两段式 FOE / FSTS / BL² 降噪 / 跨极化共轭 全部 jphot 已 claim，B3-Q2 不能当新点）
3. **不要 baseline 只比传统 TS**——必须含 jphot FSTS（否则 dB 增益是继承 jphot 的不是 B3-Q2 的）
4. **不要走环路 TF 联合建模**（前馈开环不撞 D006，环路 TF 撞转 B3-Q3，INVARIANT 13）
5. **不要用旧"4 支路 +2~3dB"数字**——已修正（2 支路才是 +2~3dB）
6. **不要自建信道**（TL-13，从 common/_channel.py 导入）

## 必读（按优先级）

1. **本 H002 + topic-index**（15 不变量，重点 11 已修正/12/13/14/15）+ **D002**（转录错误 + A1 归属结论）
2. **S002** 阶段 0.1-0.2 执行记录
3. **阶段 0.1-0.2 产出**（`explore/b3-joint-estimation/`）：
   - `_diversity_migration_validation.md`（0.1 主线判定，含转录错误详证）
   - `_a1_attribution_audit.md`（0.2 A1 归属，含 jphot claim 边界逐条）
   - `_stage0_1a_aperture_diversity_scene_survey.md`（0.1a 子 agent 场景文献）
   - `_stage0_1b_single_link_crb_upper_bound.md`（0.1b 子 agent CRB 推导）
4. **B3-Q2 详评**（复核用）：`papers/_read_notes/_B3-subsystem-coordination-increment.md` + `10.1109_jphot.2023.3265847.md`（注意 note-L36 4 支路数字错）+ `10.1364_oe.520452.md`
5. **框架 + 教训**：`stages/gw-feasibility.md` §D + thesis-lessons TL-13/20/26/27 + sim-preflight §1.6 C6-C8
6. **上游决策**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md` D005（务实路线）/ D006（环路 TF 红线）
7. **复用基建**：`projects/simulation/common/_recovery.py`（单支路估计器，多支路需新建）

## 下一步干什么（对话 2 = 阶段 0.3-0.6，不写代码）

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读必读清单 1-7，重点 D002 + 0.1/0.2 产出。

### 步骤 2：阶段 0.3 架构定性（INVARIANT 13 + D006）

> B3-Q2 联合估计是前馈开环（一套 TS 同时估 FS+FOE+CPE）不撞 D006。若具体化为"湍流相位+多普勒进环路 TF 联合建模"则撞 D006 转 B3-Q3。

核心问题：B3-Q2 加 Doppler 维度的具体形态？
- **前馈开环**（一套 TS 块估计 FS+FOE+CPE+Doppler，不进环路）→ 不撞 D006，推荐
- **环路 TF**（Doppler 进 PLL 环路 TF 联合建模）→ 撞 D006（D006 已 Kill Q12 湍流相位进环路），转 B3-Q3
- 判定：建议前馈开环（jphot 本身就是前馈块估计，加 Doppler 维度保持前馈）
- 输出 `explore/b3-joint-estimation/_architecture_decision.md`

### 步骤 3：阶段 0.4 公平对照框架（含 baseline 硬约束）

- **baseline 必须含 jphot FSTS**（不只传统 TS，D002 硬约束）
- 对照矩阵：① 传统分立 TS 管线（jphot baseline）② jphot FSTS（同算法结构，公平对照）③ B3-Q2 联合（FSTS + CPE 联合 + Doppler 维度）
- fair gain @ HD-FEC 3.8e-3，单链路强湍场景为主
- 输出 `explore/b3-joint-estimation/_fair_comparison_framework.md`

### 步骤 4：阶段 0.5 参数真相源前置（TL-26/FR-20）

- Cn²=1e-14（强湍）/ 线宽 50kHz / 望远镜口径 0.2m / 10GBaud PM-4/16-QAM（jphot 锚，全标 source 行号）
- 读原文数值（不靠笔记转录，D002 教训）
- 输出 B3Params 草稿

### 步骤 5：阶段 0.6 文件组织规约

- `explore/b3-joint-estimation/` 目录结构
- 新建代码接口定义：① MRC 合并器 ② 帧同步（FSTS 相关峰搜索）③ 多支路相位预校正 ④ 联合估计管线 ⑤ 多望远镜信道扩展（INVARIANT 14）
- 单支路估计器（fft_foe/vv_cpr/bps_cpr/da_ml）复用作子组件

### 🔴 步骤 6（建议并入步骤 1-2 任意一步）：派子 agent 查 BUPT 课题组 2024+ 续作

- 查 Liqian Wang / Siqi Zhang / Kunfeng Liu 2024+ IEEE/Optica 续作（防 BUPT 自吞 B3-Q2 增量）
- 查张思齐学位论文是否同组
- 超过 3 步主动建议分对话

## 接口变更（如有代码改动）

无（本轮不写代码）。

## 失败数据附录（如涉及路线失败）

无（本轮不 Kill，阶段 0.1-0.2 门控 PASS）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 4 支路 dB 转录错误未全修 | TL-21 确定性 grep | D002 已在 decisions/topic-index 修正，但 note-L36/verify 文件/S031 原文未改 | 下一对话或专门修 |
| BUPT 2024+ 续作未查 | FR-26 证据链 | 本轮超 3 步未派子 agent | 对话 2 步骤 6 |
| CPE 联合维度 dB 无锚 | TL-20 先建理论预期 | jphot CPE 独立，B3-Q2 加 CPE 联合的增益未知 | sandbox/MVE 阶段验证 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 单链路 CRB（FR-21）| ≥0.5dB | FR-21/gw-feasibility §D step 5 | 本轮 PASS（1.0~1.2dB）|
| 星地多孔径场景真实性 | 有文献支撑（非造问题）| 导师"特长场景"标准 | 本轮 PASS（部分成立）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 15 不变量（重点 11 已修正/12/13/14/15 B3-Q2 特殊）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 4 支路真实 = 0.7dB(4-QAM)/2.14dB(16-QAM)，2 支路才是 +2~3dB（核查 jphot content.md L357/L375/L385）
  - [ ] 单链路 CRB ≈1.0~1.2dB ≥0.5dB（核查 `_stage0_1b_single_link_crb_upper_bound.md` 自洽性段）
  - [ ] jphot 已 claim 两段式 FOE BL² 降噪（核查 jphot content.md L175/L208）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 个依赖专题产出已验证）
- [ ] 已确认当前范围（阶段 0.3-0.6，不写代码）未违反"明确不含"

## 下一轮

**对话 3**（阶段 0.3-0.6 完成后）：
- 阶段 1 sandbox（联合估计 vs 分立管线三方对照，含 jphot FSTS baseline）
- 多望远镜信道 + MRC 合并器 + 帧同步实现
- sandbox 发现联合估计打不过 jphot FSTS → 红线警报（增益归因风险坐实）

**对话 4**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
