# Handoff: 对话 1 — 阶段 0 前置规约（不写代码，先定 6 项规约防混乱）

> 来源: S001（专题开题 + 流程规划）| 交接目标: 新对话执行阶段 0 六项规约
> 文件名: H001-conversation1-stage0-preflight.md
> 日期: 2026-07-08

## 到哪了（状态）

专题 `.sessions/2026-07-08-b7-gardner-ted-foe/` 刚开。背景：

- **NDA-ML 单载波候选**（step4a-mve-execution 专题）卡住：D-008 双 bug（漏 ML 加权+升幂未归一，vs VV 持平是 bug 非物理）+ D-009 线宽 10kHz 疑似选错（Valjus 原文 0.1-1MHz）+ 方法方向待定（X/W/E/Z，用户拒 E/Z）。vs DA-ML 稳赢 +1.3~2.5dB 主结论不受影响，但 vs VV/BPS ablation 待 sandbox 重判
- 用户决策**同时跑第二候选 B7 分散风险**，但要求**先规划流程防重蹈 NDA-ML 混乱**
- NDA-ML 6 类混乱已诊断（参数反复/算法 bug/验证失效/方向重定位/文件混乱/文献引用），sim-preflight v1.3.0 已补 C6-C8 + interrupt 10-12 条防御

**B7 候选**（上游 S031 排序第 4，Conditional Go 会议最稳）：Gardner TED 复用 FOE（OFC 2026 poster，0.6dB @ BER 2e-2 + 1.9×范围 + OSNR 10dB），baseline PSA FOE，范围 in 星地 COSC。

## 下一步干什么（对话 1 = 阶段 0 前置规约，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约必须全做完才进 sandbox。禁跳阶段 0 直接写代码（NDA-ML 最大混乱就是阶段 0 没做）。
> **守 3 步上限**：本对话只做阶段 0（6 项规约拆 2-3 步），不进 sandbox。

### 步骤 1：报到 + 框架文件重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-08-b7-gardner-ted-foe/topic-index.md`（不变量 13 条 + B7 特殊风险 + NDA-ML 6 类混乱防御）
- `papers/_read_notes/_B7-gardner-ted-increment.md`（B7 锚方法 gw-read 结构化笔记，含 OFC 2026 详情）
- **sim-preflight v1.3.0 新增**：`.agents/skills/sim-preflight/rules/mve-validation.md`（V1-V6 清单）+ `SKILL.md` §1.6 C6-C8 + `rules/interrupt.md` 第 10-12 条
- `stages/gw-feasibility.md` §D 维度 D MVE 8 步
- `thesis-lessons.md` TL-20/25/26/27/13/24 速查
- `projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md`（MVE-SPEC 模板参照）

### 步骤 2：阶段 0.1 + 0.2（公式完整性 + 数学同族性）

> 这两项是 B7 最高风险（锚论文薄 + 祖师爷警报），优先做。

**0.1 锚论文公式完整性核查**：
- 核查 `papers/` 下 B7 OFC 2026 poster 是否落盘（找 ofc.2026.w2a.62 或 DOI 10.1364/ofc.2026.w2a.62）。未落盘先下载
- 读 poster 全文，**列出所有用到的公式 + 页码 + 公式编号 + 是否完整可实现**
- 公式不全（PDF→md 转 picture omitted / poster 省略推导）→ **直接标红不硬磕**（LMMSE 复现失败教训），切降级方案：
  - 降级 A：定性引用 B7（不作直接对标 baseline）
  - 降级 B：换 baseline（PSA FOE 作主 baseline，B7 作思想参考）
  - 降级 C：补 Gardner TED 1986 原始论文（T-Comm 1986 DOI 10.1109/tcom.1986.1096561）做公式交叉验证

**0.2 Gardner TED 数学同族性检查**（派子 agent 深度检查，≤15 分钟）：
- B7 锚方法（OFC 2026 Gardner TED 复用 FOE）跟 Gardner TED 1986 原版的数学关系
- B7 跟 VV / BPS 的数学关系（是否同族升幂 mean-angle 变体）
- **关键问题**：B7 的"复用 FOE"创新点是什么？跟 1986 原版的差异在哪？如果差异只是参数调度/场景迁移而非算法创新 → 数学同族 → 创新性受质疑（NDA-ML D-008 陷阱重演风险）
- 输出 `explore/b7-gardner-ted-foe/_lineage_check.md`（数学同族性结论 + 页码证据）

**判定门控**：
- 公式完整 + 非同族 → 进阶段 0.3
- 公式不全 → 切降级方案（0.1 降级 A/B/C）
- 数学同族 → **红线警报**，向用户报告"B7 跟 Gardner TED 1986 数学同族，创新性受质疑，建议={找拉开差距的条件/重新定位贡献/放弃 B7}"

### 步骤 3：阶段 0.3 + 0.4 + 0.5 + 0.6（架构/公平对照/参数/文件）

> 这四项规约化，不一定要子 agent，主线定。

**0.3 架构定性（前馈 vs 环路 TF）**：
- B7 锚方法是反馈环（Gardner TED → loop filter → NCO）。**如果我们的实现也走反馈环，环路 TF 联合建模则撞 D006**
- 决策：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策，跟 D006 边界 7 次模式同构）
- **建议前馈化**（避免 D006 纠缠），但需论证前馈化后 B7 的"复用 FOE"创新是否还成立
- 输出 `explore/b7-gardner-ted-foe/_architecture_decision.md`

**0.4 公平对照框架设计**：
- B7 baseline 是 PSA FOE（时域方法），跟 NDA-ML 的 DA ML（pilot overhead）不同维度
- fair gain 怎么定义？工作点选 BER 2e-2（B7 锚论文工作点）还是 HD-FEC 3.8e-3（NDA-ML 一致）？
- **建议跟 NDA-ML 对齐用 HD-FEC**（跨候选可比），但 B7 锚论文用 BER 2e-2，需论证 HD-FEC 下 B7 增量是否仍成立
- 范围维度（1.9×估计范围）怎么量化进 fair gain？
- 输出 `explore/b7-gardner-ted-foe/_fair_comparison_framework.md`

**0.5 参数真相源前置**：
- B7 参数一开始进 params.py 单字段（sim-preflight v1.2.0 param-source.md）：
  - Doppler range 0-23GHz（B7 OFC 2026）
  - OSNR 10dB 工作点（B7 OFC 2026）
  - LEO Doppler rate（参考 Paillier / sat.1553 / Fernandes，**读原文数值不只引位置**——D-009 教训 5）
  - 符号率 / 线宽（跟 NDA-ML 统一用 LASER_LW 单字段，但 B7 场景可能不同，需论证）
- 每个参数全标 source_type + source + audit_flag
- 输出 params.py 的 B7Params 类草稿（不直接写 params.py，先在 explore 里草拟）

**0.6 文件组织规约**：
- 定死 `explore/b7-gardner-ted-foe/` 目录结构：
  ```
  explore/b7-gardner-ted-foe/
  ├── B7-MVE-SPEC.md              # 契约（仿 N1-MVE-SPEC.md 9 节）
  ├── _lineage_check.md            # 0.2 数学同族性结论
  ├── _architecture_decision.md    # 0.3 架构定性
  ├── _fair_comparison_framework.md # 0.4 公平对照框架
  ├── _crb_lower_bound.py          # FR-21 oracle 上界（阶段 3）
  ├── _crb_results.json
  ├── b7_gardner_ted_mve.py        # MVE 脚本（阶段 3）
  ├── _mve_results.json
  └── (sandbox 三方对照在 nda-awgn-tracking-sandbox 模式下另开)
  ```
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。NDA-ML 最大混乱就是阶段 0 没做（边跑边发现公式不全 / 参数散抄 / 架构没定）
2. **INVARIANT 11 Gardner TED 1986 数学同族性前置**（B7 特殊）：必须在阶段 0.2 做深度检查。数学同族 = NDA-ML D-008 陷阱重演（vs VV 持平被当合理接受），**红线警报**
3. **INVARIANT 12 架构定性前置**（B7 特殊）：阶段 0.3 定死前馈 vs 环路。**禁边跑边定架构**（NDA-ML D-002 B11 OFDM→单载波重定位教训）。环路撞 D006 需单独决策
4. **INVARIANT 13 锚论文公式完整性前置**（B7 特殊）：OFC 2026 poster 90 行很薄，靠文字重建风险高于 NDA-ML。**公式不全直接标红不硬磕**，切降级方案（LMMSE 复现失败教训）
5. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
6. **TL-26 参数溯源 + 读原文数值**：每个参数标文献来源 + **读原文具体数值**（D-009 教训 5，D-007 引 Valjus 位置没读数值锁定错 10kHz）
7. **TL-13 共用同一信道**：B7 从 `common/_channel.py` 导入，禁自建
8. **5 个口径警示**（切法地图继承）：B7 0.6dB @ BER 2e-2 + 1.9×范围 + OSNR 10dB（不是"赢 baseline 几 dB"硬标尺，会议级别下范围+鲁棒性维度够格）

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约。阶段 3 MVE 才写代码，届时另写 handoff）

## 失败数据附录（如涉及路线失败）

无（首对话，未跑 MVE。但**继承 NDA-ML 失败数据**作参照：D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B7 OFC 2026 poster 是否落盘 | FR-26 证据链 | 阶段 0.1 核查 | 对话 1 步骤 2 |
| Gardner TED 1986 原始论文 | 公式交叉验证 | 阶段 0.1 降级 C | poster 公式不全才触发 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B7，但 B7 参数选择可参考 NDA-ML 教训 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 公式完整性 | 所有核心公式完整可实现 + 标页码 | V1 (v1.3.0) | 未跑 |
| 阶段 0.2 数学同族性 | B7 跟 Gardner TED 1986 非同族（有算法层差异）| V3+C8 (v1.3.0) | 未跑 |
| 阶段 0.3 架构定性 | 前馈化合法不撞 D006 | INVARIANT 12 | 未跑 |
| sandbox 三方对照 | 改进版/1986 原版/PSA FOE 三方归因可信 | V2+C7 (v1.3.0) | 未跑 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或 B7 锚论文 BER 2e-2 工作点 | D005 + SPEC §5 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] B7 锚论文是 OFC 2026 poster（核查 `papers/_read_notes/_B7-gardner-ted-increment.md`）
  - [ ] NDA-ML D-008 是漏 ML 加权+升幂未归一双 bug（核查 step4a-mve-execution/decisions.md D-008）
  - [ ] sim-preflight v1.3.0 新增 C6-C8 + interrupt 10-12（核查 `.agents/skills/sim-preflight/SKILL.md` §1.6 + `rules/interrupt.md` 第 10-12 条）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖：上游 + 切法地图 + 精读沉淀 + step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 2**（阶段 0 完成后）：
- 阶段 1 sandbox 三方对照（Gardner TED 改进版 / 1986 原版祖师爷 / PSA FOE baseline）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- sandbox 发现 Gardner TED 跟 1986 原版持平 → 红线警报（查数学同族性，阶段 0.2 没查清的重验）

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
