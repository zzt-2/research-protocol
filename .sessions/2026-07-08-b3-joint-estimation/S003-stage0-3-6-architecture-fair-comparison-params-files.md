# [S003] 阶段 0.3-0.6 执行：架构定性 + 公平对照 + 参数真相源 + 文件组织

> 2026-07-08 | 阶段 0 前置规约（0.3-0.6）| 状态：阶段 0 全部六项完成，不 Kill，进 sandbox
> 来源: H002 + PROMPT-002 派发（工作对话 2）

## 目标

执行 B3-Q2 阶段 0.3（架构定性）+ 0.4（公平对照框架）+ 0.5（参数真相源）+ 0.6（文件组织规约）+ 查 BUPT 2024+ 续作，不写代码。完成阶段 0 全部六项后，下一对话进 sandbox。

## 记录

### 步骤 1：报到 + 必读清单 1-5 + 派子 agent 查 BUPT（并发）

session-governance Trigger 1 报到。读 topic-index（15 不变量）/ H002 / S002 / decisions(D001/D002) / 阶段 0.1-0.2 产出（4 份）/ jphot content.md（grep L175/208/357/375/385）/ B3 详评 / D005/D006 / gw-feasibility §D / TL-13/20/26/27 / sim-preflight C6-C8 / _recovery.py / _channel.py。

接收方验证 3 事实全打钩：
- 4 支路 dB 转录错误（grep jphot-L375 Fig.18 + L385 Conclusion two-branch）PASS
- 单链路 CRB 1.0~1.2dB ≥0.5dB（`_stage0_1b` L120-122 自洽性 PASS）PASS
- jphot 两段式 FOE BL²（grep L175/L208）PASS

派子 agent 查 BUPT 2024+ 续作（后台并发，962s 返回）。

### 步骤 2：阶段 0.3 架构定性（前馈开环 vs 环路 TF）

**判定：走前馈开环**（一套 TS 块估 FS+FOE+CPE+Doppler，逐块前馈不进环路）。

D006 边界判据链（三重证据）：
1. D006（decisions.md L341）只禁"湍流相位进环路 TF 联合建模"，不禁前馈块估计
2. B3 详评 Q2（`_B3-...md` L77）："撞 D006？否——协同在 FS/FOE/分集合并子模块间，不涉 PLL 环路 TF"
3. jphot 本身就是前馈块估计（L101/L175 逐块前馈）

B3-Q2 前馈开环形态：[1]FS 相关峰 → [2]两段式 FOE → [3]Doppler 斜率块间回归（前馈）→ [4]CPE 联合复用 FOE 共轭积（前馈）→ [5]MRC 合并。全逐块前馈无环路反馈。

Doppler 维度前馈解：对连续 TS 块估出的 Δf̂_k 序列线性回归 → f_dot，前向补偿（外推），不进 PLL。**不撞 D006**——Doppler 是确定性轨道运动（非随机湍流相位，D006 禁区物理本质不同），形态是前馈估计+前向补偿无反馈环路。

撞 D006 的形态（排除，转 B3-Q3）：Doppler+湍流相位联合进环路 TF / KF 状态向量扩 [ω,f_dot,φ_T] / 湍流相位作 CPE 先验进环路。

产出：`_architecture_decision.md`。

### 步骤 3：阶段 0.4 公平对照 + 0.5 参数真相源 + 0.6 文件组织接口

三阶段合并产出（强耦合：0.4 baseline 依赖 0.3 架构，0.5 参数依赖 0.4 场景，0.6 接口依赖 0.4 三方对照）。

**0.4 公平对照框架**（防增益归因，D002 首要风险）：
- 三方对照矩阵：M1 传统分立 TS（祖师爷/弱 baseline）/ M2 jphot FSTS（公平基准，同 FS+FOE 算法结构）/ M3 B3-Q2 联合（M2 + CPE 联合 + Doppler 维度）
- fair gain 定义：`gain_vs_M2 = M2.BER - M3.BER`（B3-Q2 真实增量，Go 判据用这个）；`gain_vs_M1` 含 jphot 继承增益仅参考
- 🔴 增益归因熔断：若 `gain_vs_M2 ≤ 0`（B3-Q2 打不过 jphot FSTS）→ 红线警报转 Kill 讨论
- 消融设计：M3a(M2+CPE)/M3b(M2+Doppler)/M3(全量)，归因 CPE vs Doppler 各自贡献（<10% 该切口无效）

**0.5 参数真相源**（TL-26/FR-20，全标 source + 读原文 grep 核验）：
- 复用 `_stage0_1b` L9-36 已核参数表（Cn²=1e-14/线宽 50kHz/口径 0.2m/10GBaud PM-4-QAM/TS 320/BL=20/FEC 3.8e-3）
- 补 Doppler 维度参数（f_dot 待 sandbox 标定，溯源债务标注）
- B3Params 草稿接口定义

**0.6 文件组织**（INVARIANT 14）：
- explore/b3-joint-estimation/ 目录结构
- 五个新建代码接口：① MRC 合并器 ② 帧同步 FSTS 相关峰 ③ 多支路相位预校正 ④ 联合估计管线（前馈开环）⑤ 多望远镜信道扩展
- 复用清单：common 的 generate_shared_realization / fft_foe / vv_cpr / bps_cpr / doppler_phase / gg_block（TL-13 不自建）
- 不进 common 边界（多支路扩展全在 explore）

产出：`_fair_comparison_framework.md`（含 0.4/0.5/0.6 三节）。

### 步骤 4：BUPT 续作核查（子 agent 产出 + 主线 grep 核验）

子 agent 查 BUPT 课题组（Liqian Wang / Kunfeng Liu / Siqi Zhang）2024+ 续作（962s 返回）：

**核心结论**：B3-Q2 三切口（CPE 联合 / Doppler / 星地）**均未被单篇 BUPT 续作完整吞没**，但存在"迫近自吞"风险。

| 切口 | 覆盖状态 | 关键证据 |
|---|---|---|
| CPE 联合 | 部分覆盖（单链路地面）| JCSCR 2023（abstract 已验证）已做 FOE+CPE 联合 carrier recovery，但单链路地面，非"分集下 CPE 联合" |
| Doppler | 未覆盖（负证据）| 已验证 abstract 无一提 Doppler 联合；jphot-L208 缓变假设未推翻 |
| 星地场景 | 部分覆盖（单链路非分集）| BUPT 确已跨入星地（SSRN 2025 + OECC 2026，但 abstract 未亲验），均单链路未叠加分集/CPE/Doppler |

**主线核验**：子 agent 产出质量 PASS——验证等级标注诚实（abstract 已验证 vs 搜索摘要未验证分开），张思齐学位论文标"未检索到，Siqi Zhang 关系未确认"诚实，无脑补。TTQP 2024 场景冲突标"以已验证 read-note 为准，待复核"诚实。

**迫近自吞风险**（非 Kill，timeline 风险）：BUPT 构件齐全（CPE 联合+空间分集+星地 FS+FOE），2025-2026 持续活跃，12 个月内汇合论文概率非低。记入 D003。

**未完成项**（标债务）：
- SSRN 2025 + OECC 2026 abstract 未亲验（Cloudflare 拦截）— sandbox 前需补
- 张思齐学位论文 + Siqi Zhang 同组关系未确认 — 建议 CNKI 专项核查

产出：`_bupt_followup_audit.md`。

### 步骤 5（追加）：adaptation-scan A1-A6 扫描（S013 教训 + 用户"有思路都可以试试"）

用户指向 S013（NDA-ML 适配扫描：A1/A3 FAIL / A4 PASS），触发 B3-Q2 的 adaptation-scan 规则扫描（`.claude/skills/sim-preflight/rules/adaptation-scan.md`——找增量前必扫 A1-A6）。核心教训：锁死"全条件赢"判据跑 9 对话全堵死，条件切换才出信号。

**6 维扫描结果**：
- A1 参数适配（BL 自适应）：中信号（jphot-L299 自承 BL 受多因素影响），但 S013 A1 FAIL 先验在
- **A2 结构适配（Doppler 维度）**：✅ 强信号（jphot-L208 自承缓变假设）——**已用**（M3 核心）
- A3 组合适配（FSTS+跟踪）：中（S013 反面教训，跨 fade 记忆撞 D006 风险）
- **A4 条件适配（Doppler crossover）**：⭐ 主信号候选——jphot 缓变假设在高 Doppler 失效，M2/M3 可能在 Doppler 动态轴有 crossover
- A5 评价维度（outage）：弱-中，作 A4 补充
- **A6 失效边界（高 Doppler）**：✅ 强——jphot 在高 Doppler 直接失效，B3-Q2 扩展适用边界（跟 A4 互补，叙事更强）

**对 0.4 框架的修正**：补进 §0.4.5 分层 Go 判据（L1 全条件 / L2 Doppler crossover 降级 / L3 失效边界降级）。把"全条件赢"从严判降级为第一层，给 A4/A6 留活路，符合 D005 务实路线 + 导师特长标准（特长=高 Doppler 动态）。

**防换皮**：B3-Q2 A4 crossover 轴（Doppler 动态强度，确定性量）跟 NDA-ML A4（per-block 有效 SNR，随机量）物理量正交，机制不同，不算换皮——但两专题若都发条件切换论文必须显式区分叙事。

产出：`_adaptation_scan_b3.md` + `_fair_comparison_framework.md` §0.4.5 补充。

### 产出物

1. `explore/b3-joint-estimation/_architecture_decision.md`（0.3 架构定性）
2. `explore/b3-joint-estimation/_fair_comparison_framework.md`（0.4 公平对照含 §0.4.5 分层判据 + 0.5 参数真相源 + 0.6 文件组织接口）
3. `explore/b3-joint-estimation/_bupt_followup_audit.md`（BUPT 续作核查，子 agent 产出）
4. `explore/b3-joint-estimation/_adaptation_scan_b3.md`（A1-A6 适配扫描，sandbox 前必扫）

## 决策引用

- **D003**（新建）：阶段 0.3-0.6 完成 + 架构走前馈开环（不撞 D006）+ BUPT 迫近自吞风险登记（非 Kill，timeline 风险）
- D002（沿用）：不 Kill + 转录错误修正 + A1 归属——本轮 0.3-0.6 在此基础上定架构/baseline/参数/接口
- D001（沿用）：开 B3-Q2 专题——阶段 0 全六项完成

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.3-0.6，不写代码，不进 sandbox）
- 未违反"明确不含"（不回头救 Kill 候选 / 不判其他方向 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 后续

### 已答（本轮闭合）

1. 架构定性（阶段 0.3）：走前馈开环，不撞 D006（三重证据）
2. 公平对照框架（阶段 0.4）：三方对照 M1/M2/M3 + fair gain @ HD-FEC + 增益归因熔断（gain_vs_M2 ≤ 0 转Kill）
3. 参数真相源（阶段 0.5）：全标 source + 读原文 grep 核验 + Doppler 参数债务标注
4. 文件组织（阶段 0.6）：explore 目录 + 5 新建接口定义 + 复用清单
5. BUPT 续作核查：三切口均未被单篇完整吞没，迫近自吞风险登记

### 待办（下一对话 sandbox 阶段）

1. **阶段 1 sandbox**：联合估计 vs 分立管线三方对照（M1/M2/M3），单链路强湍 + Doppler 主场景
2. **Doppler 参数 f_dot 溯源补全**（FR-20 债务）：深查 B5 锚 optcom.2024.130981 / Vieira 原文 f_dot 精确值
3. **SSRN 2025 + OECC 2026 abstract 亲验**（BUPT 审计债务）：防 BUPT 已发汇合论文
4. **张思齐学位论文 CNKI 核查**（BUPT 审计债务）：确认 Siqi Zhang 同组关系
5. **🔴 修正转录错误**（D002 遗留）：note-L36 + `_cut-b1b2b3-verify.md:258-291` + S031 的"4 支路 +2~3dB"（仍未修，待专门处理）
6. **多望远镜间距参数设定**（0.6 债务）：空间相干长度依赖 Cn²+距离需算

### 红线（下一对话必守）

- sandbox 发现 `gain_vs_M2 ≤ 0`（B3-Q2 打不过 jphot FSTS）→ 增益归因熔断，转 Kill 讨论
- CPE 联合贡献 <10% + Doppler 贡献 <10% → B3-Q2 无真实增量，转 Kill 讨论
- 禁 baseline 只比传统 TS（必须含 jphot FSTS，否则增益是继承的）
- 禁走环路 TF（前馈开环不撞 D006，环路 TF 撞转 B3-Q3）
