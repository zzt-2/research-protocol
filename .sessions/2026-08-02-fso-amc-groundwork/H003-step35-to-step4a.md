# Handoff: GW Step 3.5 终态 STEP3_5_SURVIVES → Step 4a / 用户决策

> 来源: S005 | 交接目标: 下一对话执行 GW Step 4a（或用户决策调整 C / 换 AMC 子族 / 停止）
> 日期: 2026-08-03 | 文件名: H003-step35-to-step4a.md

## 到哪了（状态）

GW Step 3 语义门纠偏 + Step 3.5 定向补充检索在本轮（S005/D005/R001/R003/V006）完成：
- **Step 3（D005 纠偏）**: 旧 STEP3_NO_VALID_PROBLEM 用自创四判据标签（problem_truth/actionability/novelty/thesis_fit）当 terminal gate → 循环门控（problem_truth 要求已证伪=Step 4a/MVE 证据前移；novelty 不属四判据=Step 3.5/4a 职责前移）。纠正为 **STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED**。R001 逐字核对 canonical 四判据 owner（glossary.md L22-31 SHA256 eafa43e3… + templates.md L301 SHA256 bdc93d41…）。保留 D004 的 Step 2 PASS / 5 CORE / Safi·L124 blocker / 精读事实提取。
- **Step 3.5（D005/R003）**: 按 canonical 四判据重建 Q-A（预测驱动风险失配）+ Q-B（动作位置-时间尺度失配），2 子 agent 并行定向检索 ~190 命中 + 引用链。**Q-A + Q-B 均 SURVIVES_STEP3_5** → 终态 **STEP3_5_SURVIVES**，存在 Step 4a 入口。
- 产出: R001（semantic-gate receipt）+ R003（Step 3.5 闭包）+ literature_notes_amc §6/§7/§11 重写 + D005 + V006 + 本 H。

## 下一步干什么

**下一合法动作 = GW Step 4a**（gw-feasibility §A0 §0 前置门控会再查 Q# 四判据；需新对话 + 用户授权）。**本轮不启动**（brief 明示到 Step 3.5 终态停止）。

Step 4a 启动前**建议优先关闭 3 个开放问题**（非硬前置，但影响 Step 4a 质量）：
1. **Q-A Safi UNVERIFIED 尾巴**: 合法获取 Safi 2019 全文（IEEE 订阅/ILL，DOI 10.1109/TVT.2019.2916843）→ 精读确认是否已覆盖 posterior/risk-aware 码率规则。若覆盖 → Q-A 转 COVERED。
2. **Q-B baseline 缺位**: 评估自建 coherent sat-ground GG 信道模型可行性（判据4 量化对标的工程前提；无合法 coherent 星地 AMC baseline，L023/L124/TCOMM2026/LCOMM2026 全 terrestrial）。
3. **Galijasevic DOI 异常 + L023 backward citation 缺口**: `10.1109/OJCOMS.2024.011100` 解析到 BELA 5G/6G（W6884651712），M 真实身份是 2025 "Channel-prediction-driven rate control for LDPC coding…"（c=4）+ ICC 2024 前身。用正确 DOI/标题重跑 citation。

**若用户决定不进 Step 4a**: 可调整 C 条件 / 换 AMC 子族 / 停止（跨阶段决策，**禁 agent 自行放宽 C**）。

## 纪律（和下一步直接相关的约束）

1. **FR-22 硬门控**: Step 4a 前置门控 §A0 §0 会再查 Q# 四判据；Q-A/Q-B 的 A 是**文献支持、可证伪**的失效假设，**不是已证伪**——Step 4a/MVE 才负责"已证伪"。禁把 Step 3.5 的 SURVIVES 当成"已验证可行"。
2. **FR-25/TL-32 Go/Kill 分离**: Step 4a Go 判据 = 赢传统未优化 baseline；oracle 上界（FR-21）只做 Step 4a 维度 D 收尾 Kill 工具，禁当 Go 判据，且只在 Step 3 走完+判据 A 成立后才触发。Q-B baseline 缺位时尤其注意：不可用 oracle 上界替代传统 baseline 对手。
3. **D003/D005 FR-26**: Safi/L124 全文缺失时禁据 abstract 推失效机制；Q-A 的 Safi UNVERIFIED 尾巴只能靠全文关闭，不能靠 abstract 推成 COVERED。
4. **canonical 四判据唯一 owner**（D005）: glossary.md L22-31 + templates.md L301。**禁再用自创标签**（problem_truth/actionability/novelty/thesis_fit）。
5. **TL-31/TL-33**: 动笔前必读 decisions.md + thesis-lessons；所有"已读/已确认"必附 file:line/API 证据。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC≠receiver campaign / GW 流程强制 / Go-Kill 分离 / 证据链强制 / **canonical 四判据 owner**）
- [ ] 已验证本文件至少 3 条关键事实声称:
  - D005 纠偏后 Step 3 终态 = STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（`literature_notes_amc.md` §7）
  - canonical 四判据 owner SHA256（`stages/glossary.md` = eafa43e3…073f610e74b，`templates.md` = bdc93d41…caa7b9e41）
  - Q-A/Q-B Step 3.5 终态 = SURVIVES_STEP3_5（`literature_notes_amc.md` §11.3 + R003）
- [ ] 已检查 _registry.yaml 本专题 status=active，conflicts_with=[]
- [ ] 已确认当前范围未违反"明确不含"（本轮不进 Step 4a/不设计方法/不跑仿真/不修 Skill/不碰 p05 log）

## 关键事实证据指针（接收方快速核对）

- semantic-gate owner receipt: `.sessions/2026-08-02-fso-amc-groundwork/R001-semantic-gate-owner-receipt.md`
- Step 3.5 检索 + 闭包: `.sessions/2026-08-02-fso-amc-groundwork/R003-step35-targeted-search-and-closure.md` + `search-archive/2026-08-03/`（55 文件）
- canonical 四判据重建 Q# + 竞争闭包表: `projects/thesis-fso/literature_notes_amc.md` §6 + §11
- D005 + V006: `.sessions/2026-08-02-fso-amc-groundwork/{decisions,verifications}.md`
- Safi/L124 BLOCKED: `papers/doi/10.1109_tvt.2019.2916843/metadata.json`（abstract-only）+ `papers/doi/10.1364_oe.595557/metadata.json`（abstract-only）

## 下一轮

**Step 4a 启动**（若用户授权）—— 读 `stages/gw-feasibility.md` §A0/A'/A/B/D + 先关闭 3 个开放问题（Safi 全文 / Q-B 信道模型可行性 / Galijasevic citation）。或用户决策调整 C / 换子方向 / 停止。