# Handoff: 对话 3 — 阶段 1 sandbox（联合估计 vs 分立管线三方对照）

> 来源: S003 | 交接目标: 新工作对话执行阶段 1 sandbox（联合估计 vs 分立管线三方对照 M1/M2/M3）
> 日期: 2026-07-08
> 文件名: H003-conversation3-sandbox.md

## 到哪了（状态）

工作对话 2 执行完阶段 0.3-0.6（S003/D003），**阶段 0 全六项闭合**，B3-Q2 不 Kill。关键结论：

1. **架构定死：前馈开环**（INVARIANT 13 + D003）：一套 TS 块估 FS+FOE+CPE+Doppler，逐块前馈不进环路，不撞 D006（三重证据：D006 只禁湍流相位进环路 TF / B3 详评 Q2 判否 / jphot 本身前馈）。Doppler 维度 = 块间 Δf̂_k 序列线性回归 → f_dot 前向补偿（确定性轨道运动，非随机湍流，物理本质不同）
2. **公平对照框架定死**（D002 首要风险对策 + D003）：三方对照 M1 传统分立 TS / M2 jphot FSTS（公平基准）/ M3 B3-Q2 联合。**fair gain Go 判据 = gain_vs_M2 > 0**（不用 gain_vs_M1，那是 jphot 继承增益）。增益归因熔断：gain_vs_M2 ≤ 0 → 转Kill
3. **消融归因**：M3a(M2+CPE)/M3b(M2+Doppler)/M3(全量)，CPE 贡献 + Doppler 贡献各自 <10% → 无真实增量转Kill
4. **参数真相源**（TL-26，全标 source grep 核验）：Cn²=1e-14 / 线宽 50kHz / 口径 0.2m / 10GBaud PM-4-QAM / TS 320 / BL=20 / FEC 3.8e-3。Doppler f_dot 待 sandbox 标定（溯源债务）
5. **文件组织接口定死**（INVARIANT 14）：explore/b3-joint-estimation/ 下 5 个新建代码接口（MRC 合并器 / 帧同步 FSTS / 多支路相位预校正 / 联合估计管线 / 多望远镜信道），复用 common 的 fft_foe/vv_cpr/bps_cpr/generate_shared_realization/doppler_phase
6. **BUPT 续作核查**（D003）：三切口（CPE 联合/Doppler/星地）均未被单篇完整吞没，但迫近自吞风险（构件齐全，12 个月内汇合论文概率非低）——非 Kill，timeline 风险
7. **adaptation-scan A1-A6 扫描**（S013 教训 + 用户"有思路都试试"）：主信号 = A4（Doppler crossover）+ A6（失效边界扩展）。已补进 §0.4.5 **分层 Go 判据**——L1 全条件 / L2 Doppler crossover 降级 / L3 失效边界降级。全条件赢判据（gain_vs_M2 > 0）从严降为第一层，高 Doppler 特长场景留作保底

未写代码，未进 sandbox。explore/b3-joint-estimation/ 有 8 份文档（0.1a/0.1b/0.1整合/0.2 A1/0.3架构/0.4-0.6公平对照+参数+接口/BUPT审计/adaptation-scan）。

## 不要做什么

1. **不要 baseline 只比传统 TS**——必须含 jphot FSTS（M2），否则 dB 增益是继承 jphot 的不是 B3-Q2 的（D002/D003 硬约束）
2. **不要用 gain_vs_M1 当 Go 判据**——那是 jphot 继承增益，Go 判据用 gain_vs_M2（B3-Q2 真实增量）
3. **不要走环路 TF 联合建模**——前馈开环不撞 D006（INVARIANT 13），环路 TF 撞 D006 转 B3-Q3
4. **不要 claim jphot 已有的算法机制**（两段式 FOE / FSTS / BL² 降噪 / 跨极化共轭全被 claim）
5. **不要用旧"4 支路 +2~3dB"数字**——已修正（2 支路才 +2~3dB，4 支路 0.7-2.14dB，单支路 1.17dB）
6. **不要自建信道**（TL-13，从 common/_channel.py 导入；多支路扩展在 explore 做，不进 common）
7. **不要忽略增益归因熔断**——sandbox 出 gain_vs_M2 ≤ 0 必须停下来转 Kill 讨论，不能当"还没调好"

## 必读（按优先级）

1. **本 H003 + topic-index**（15 不变量，重点 11/12/13/14/15）+ **D003**（架构前馈开环 + 公平对照三方矩阵 + BUPT 风险）
2. **S003** 阶段 0.3-0.6 执行记录
3. **阶段 0 全产出**（`explore/b3-joint-estimation/`）：
   - `_architecture_decision.md`（0.3 前馈开环架构 + D006 边界三重证据 + 流程定义）
   - `_fair_comparison_framework.md`（0.4 三方对照矩阵 + §0.4.5 **分层 Go 判据** + 消融设计 + 0.5 参数表 + 0.6 五接口定义——**sandbox 实现的直接蓝图**）
   - `_adaptation_scan_b3.md`（A1-A6 适配扫描，主信号 A4 Doppler crossover + A6 失效边界扩展——**sandbox 若 L1 全条件 FAIL 必读降级保底路**）
   - `_bupt_followup_audit.md`（BUPT 续作核查，三切口覆盖判断）
   - `_diversity_migration_validation.md` + `_a1_attribution_audit.md`（0.1/0.2 背景）
   - `_stage0_1b_single_link_crb_upper_bound.md`（CRB 上界 1.0~1.2dB，增益归因警示）
4. **jphot 原文**：`papers/doi/10.1109_jphot.2023.3265847/content.md` L101/175/208/357/375/385（FS+FOE+MRC claim 边界 + 两段式 FOE BL² + 结论 2 支路数字）
5. **框架 + 教训**：`stages/gw-feasibility.md` §D（FR-20/21/11/14/15）+ thesis-lessons TL-13/20/26/27 + sim-preflight §1.6 C6-C8（公式核对/三方对照/祖师爷警报）
6. **上游决策**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md` D005（务实路线）/ D006（环路 TF 红线）
7. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe/vv_cpr/bps_cpr/da_ml/nda_ml/gardner_ted/psa_foe/short_time_spectrum）+ `_channel.py`（generate_shared_realization/generate_shared_realization_apsk/doppler_phase/gg_block）+ `_config.py`（T_S/LASER_LW/TURB/BLOCK/F_RESIDUAL/DOPPLER_HIGH）

## 下一步干什么（对话 3 = 阶段 1 sandbox）

### 步骤 1：报到 + 补 sandbox 前置债务

报到（session-governance Trigger 1）+ 读必读清单 1-7。补债务：
- Doppler f_dot 溯源（深查 B5 锚 optcom.2024.130981 / Vieira 2023 f_dot 精确值）
- SSRN 2025 + OECC 2026 abstract 亲验（防 BUPT 已发汇合论文）
- 张思齐学位论文 CNKI 核查（确认 Siqi Zhang 同组关系）
- 多望远镜间距参数设定（空间相干长度依赖 Cn²+距离）

### 步骤 2：实现 5 个新建代码接口（按 0.6 定义）

按 `_fair_comparison_framework.md` §0.6.2 接口定义实现（explore/b3-joint-estimation/ 内）：
1. `multi_aperture_channel.py`（⑤ 多望远镜信道扩展，从 common 单支路扩展）
2. `frame_sync_fsts.py`（② 帧同步 FSTS 相关峰）
3. `mrc_combiner.py`（① MRC 合并器）
4. `multi_branch_phase_precorr.py`（③ 多支路相位预校正）
5. `joint_estimation_pipeline.py`（④ 联合估计管线，含 M1/M2/M3 三模式）

### 步骤 3：sandbox 三方对照（M1/M2/M3）

- 主场景 S1：单链路（n_branches=1）强湍（Cn²=1e-14）+ Doppler（f_dot）
- 对照 S2：单链路强湍无 Doppler（验证 Doppler 维度增量）
- 加分项 S3：多支路（2/4）强湍（验证是否压缩增益）
- **🔴 多扫一维：Doppler 动态强度轴**（adaptation-scan A4 要求）——扫 f_dot ∈ {0, 低, 中, 高} 找 M2/M3 crossover 点
- 指标：BER vs 接收光功率 @ HD-FEC 3.8e-3 + FOE MSE + CPE RMSE + **outage 概率（A5 补充）**
- **fair gain**：gain_vs_M1（参考）+ gain_vs_M2（Go 判据）
- 消融：M3a(M2+CPE) / M3b(M2+Doppler) / M3(全量)

### 🔴 步骤 4：分层 Go/Kill 判定（守 §0.4.5 三层，不要 L1 FAIL 就 Kill）

按 `_fair_comparison_framework.md` §0.4.5 + `_adaptation_scan_b3.md`：

- **L1 全条件**：gain_vs_M2 > 0（全条件）+ CPE/Doppler 贡献 ≥10% → **Go（强）**，进阶段 2/3
- **L2 Doppler crossover（A4 降级）**：L1 FAIL 时扫 f_dot 维度。若高 Doppler 区 gain_vs_M2 > 0 且物理因果清晰（jphot-L208 缓变假设失效）→ **Go（条件特长场景）**，卖点降级"高动态条件下联合估计特长"
- **L3 失效边界（A6 降级）**：L2 也无明显 crossover 时，查 jphot 在高 Doppler 是否直接失效（BER 爆/发散）。若 jphot 失效而 B3-Q2 仍工作 → **Go（失效边界扩展）**，卖点"扩展 jphot FSTS 适用边界"
- **Kill**：L1+L2+L3 全 FAIL → 真 Kill

**纪律**：S013 教训——不要 L1 FAIL 就当废，NDA-ML 跑 9 对话全条件判据全堵死，最后是 A4 条件切换出信号。B3-Q2 先验同向（CPE CRB≈0 + Doppler 无锚），L2/L3 很可能是真信号所在。

## 接口变更（如有代码改动）

本轮（对话 2）无代码改动（阶段 0 不写代码）。对话 3 将新增 5 个 explore 模块（接口已在 `_fair_comparison_framework.md` §0.6.2 定义）。

## 失败数据附录（如涉及路线失败）

无（本轮不 Kill，阶段 0.3-0.6 门控 PASS）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 4 支路 dB 转录错误未全修 | TL-21 确定性 grep | D002 已在 decisions/topic-index 修正，但 note-L36/verify 文件/S031 原文未改 | 跨专题专门修（不影响 B3-Q2 推进） |
| Doppler f_dot 溯源未完成 | FR-20/TL-26 | common 已建模 f_dot 但精确值未查 B5 锚原文 | 对话 3 sandbox 前补 |
| SSRN 2025 + OECC 2026 abstract 未亲验 | FR-26 证据链 | BUPT 子 agent 标"未验证"（Cloudflare 拦截） | 对话 3 sandbox 前补（防 BUPT 汇合论文） |
| 张思齐学位论文 + Siqi Zhang 同组关系 | FR-26 | 未检索到，未确认 | 对话 3 CNKI 专项核查 |
| 多望远镜间距参数无锚 | TL-26 | jphot 未给具体值 | 对话 3 sandbox 设（空间相干长度算） |
| CPE 联合增益预期偏薄 | TL-20 先建理论预期 | 0.1b CRB ≈0dB，消融设计验证 | sandbox M3a 验证 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 单链路 CRB（FR-21）| ≥0.5dB | FR-21/gw-feasibility §D step 5 | S002 PASS（1.0~1.2dB）|
| 架构 D006 边界 | 前馈开环不撞 | INVARIANT 13 + D006 | S003 PASS（三重证据）|
| 公平对照 baseline | 含 jphot FSTS | D002/D003 增益归因对策 | S003 框架定（M2）|
| BUPT 自吞风险 | 三切口未单篇吞没 | FR-26 续作核查 | S003 PASS（但迫近风险）|
| **sandbox gain_vs_M2** | **> 0**（待 sandbox 验） | D003 增益归因熔断 | **待验** |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 15 不变量（重点 11/12/13/14/15）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 架构走前馈开环不撞 D006（核查 `_architecture_decision.md` §1 三重证据 + D006 decisions.md L341）
  - [ ] fair gain Go 判据 = gain_vs_M2（核查 `_fair_comparison_framework.md` §0.4.2 三方对照矩阵 + 增益归因熔断）
  - [ ] BUPT 三切口均未被单篇完整吞没（核查 `_bupt_followup_audit.md` §3 覆盖判断表）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 个依赖专题产出已验证）
- [ ] 已确认当前范围（阶段 1 sandbox，写代码实现 5 接口 + 三方对照）未违反"明确不含"

## 下一轮

**对话 3**（本轮 = 阶段 0.3-0.6 完成）：
- 阶段 1 sandbox（联合估计 vs 分立管线三方对照 M1/M2/M3）
- 实现 5 个新建代码接口（按 0.6 定义）
- 补 sandbox 前置债务（Doppler f_dot 溯源 + SSRN/OECC abstract + 张思齐 CNKI + 多望远镜间距）
- Go/Kill 判定（守增益归因熔断：gain_vs_M2 ≤ 0 转 Kill）

**对话 4**（sandbox Go 后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
