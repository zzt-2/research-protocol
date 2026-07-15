# Handoff: Contract 冻结 → Execute 阶段入口

> 来源: S026 | 交接目标: Execute 阶段（跑实验+出论文数据）
> 文件名: H011-contract-frozen-to-execute.md
> 日期: 2026-07-15

## 到哪了（状态）

**Contract 冻结完成**（2026-07-15，用户确认）。`projects/thesis-fso/contract.md` status: draft → frozen。

S0-S5 全过：
- S0 新颖性（复用 GW 29 篇，reframe 后分析层 7 项空白 + 方法层窄域）
- S1 瓶颈诊断（D014 SOP 串扰）
- S2 指标审计（FR-17 主指标改 fixed-label BER，PI-BER 降辅指标——**用户已确认**）
- S3 参数溯源（全 [ASSUMPTION] 消除，prompt023 补 SOP=0 矩阵 PASS）
- S4 端到端推演（data-flow.md 创建，8 步 DSP 信号流 + FR-13 均衡能力审计 + FR-16 信息增量审计全过）
- S5 压力测试 + 反模式 + 实验完备性（experiment_completeness_checklist.md 创建，Tier 1 六项全 pass）

**Q-CMA-FADE 冻结形态**：分析层（强，7 项稳结论）+ 方法层（弱，D022 窄域 PI 优势 29/30 p=1.19e-6）。

## 下一步干什么

**Execute 阶段**。但注意：Q-CMA-FADE 的 E1-E7 实验在 GW Step 4a 维度 D MVE 阶段**已基本跑完**（prompt004-023 系列），Execute 不是从零跑实验，是：

1. **补 E8（统计严谨性）**：核心 E3 已 30 seeds，其他关键点（E1 SOP×f_G 矩阵、E4 BER vs SNR）从 5 seeds 加到 ≥30 seeds + error bar
2. **补 T2-5（复杂度报告）**：ML 推理延迟实测（compute_rmps 已实现）+ CMA O(N·L·4)
3. **整理论文数据**：把 prompt 系列 JSON 结果整理成论文图表数据（BER vs SNR 曲线 / SOP×f_G 矩阵 / ML vs CMA 配对比较）
4. **写论文**：按导师约束（不能只分析得加方法 / 特定条件优异就行 / 会议不给修改机会 / BER 10⁻⁵ 底线 / 没后路）

**Execute 入口**：读 `stages/execute.md` 全文守 FR-22（转阶段必读）。读 `projects/thesis-fso/contract.md`（frozen）+ `data-flow.md` + `experiment_completeness_checklist.md`。

## 纪律（和下一步直接相关的约束）

1. **守 D018 双口径**：任何性能结论 fixed/PI 必须并报。PI-BER 须标 pilot/帧头开销（非免费）
2. **守 D023 收窄**：论文不得声称 ML 鲁棒优于 standard-CMA。H2 仅 N=5M/f_G=30 窄域
3. **守导师约束**：不能只分析得加方法（D022 方法层必须写进论文）/ 特定条件优异就行（窄域可卖，诚实标 limitation）
4. **守 FR-22**：Execute 阶段读 `stages/execute.md`，不自创流程
5. **不复活 Kill**：Q-DP1/DP3/DP4/改动1 是物理结论，不作贡献复活
6. **BER 口径警示（D029 核验）**：引述历史数字时须标注是 fixed-label 4 旋转口径还是 D018 完整 PI-BER（2!×4×4 消歧）。D015 Q3-B 报"PI=0.002"实为 fixed-label 4 旋转

## 已知债务（Execute/论文须处理）

| 债务 | Contract 处理 | Execute/论文动作 |
|---|---|---|
| 监督 vs 盲不公平（D008 债务 1）| F4 已标 | 论文 limitations 段 |
| 方法照搬 Qin CNN（D008 债务 2）| F4 已标 | 诚实"场景迁移 + 分析增量" |
| seed-bias（h_mean CV≈1.0）| E8 待补 | 关键点加到 ≥30 seeds |
| SOP_RATE 仿真值非实测 | Parameter Provenance 已标 | 论文 limitations |
| BER 10⁻⁵ 达不到 | S2 指标审计（pre-FEC 口径）| 论文说明 pre-FEC + 导师沟通 |

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - Contract frozen（contract.md status: frozen）— 查 `projects/thesis-fso/contract.md` 头部
  - data-flow.md 存在且含 FR-13/FR-16 审计 — 查 `projects/thesis-fso/data-flow.md`
  - experiment_completeness_checklist.md Tier 1 全 pass — 查 `projects/thesis-fso/experiment_completeness_checklist.md`
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

Execute 阶段第一步：读 `stages/execute.md` 全文 → 读 contract.md（frozen）+ data-flow.md + experiment_completeness_checklist.md → 确认 E1-E7 哪些已有数据可直接整理、哪些需补跑（E8 统计严谨性 + T2-5 复杂度）→ 规划论文数据整理 + 图表。
