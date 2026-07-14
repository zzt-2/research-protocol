# PROMPT-003: Q-CMA-FADE 进 Step 4a 维度 D MVE（CMA 深衰落发散 + ML 缓解）

> 粘贴此文档开新对话。这是 Q-CMA-FADE 方向进 Step 4a MVE 执行。
> 前序：dual-pol-osl-groundwork 专题（S001-S003 + R001/R002 + D001-D005）。

## 你要做什么

**执行 Q-CMA-FADE 的 Step 4a 维度 D MVE**——验证 CMA 在 GG 深衰落下发散，以及 ML 均衡器缓解发散 vs CMA 的增量。

Q-CMA-FADE = Q-DP2（分析型）+ Q-ML1（方法型）合并（D005），四判据全过最强候选。

## 第一步（必须按顺序）

1. **session-governance 报到**：读 `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
2. **读 MVE 契约**：`projects/simulation/explore/cma-fade-divergence/README.md`
3. **读组织规范**：`projects/simulation/SIM-ORG.md`（代码/结果怎么放）
4. **读框架**：`stages/gw-feasibility.md` §D（维度 D MVE 规范）+ `code-quality.md` 必做清单 + `reference/sim-template/` 模板

## MVE 分三步（守 FR-20/FR-21 + TL-20）

### Step A：建 GG 时间域衰落模型（FR-20 缺口，前置门控）

**这是 Q-CMA-FADE 的 Conditional 条件之一**（D002 原有风险继承）——现有文献只给 GG 幅度 PDF，衰落持续时间/频率全缺失。

要做的：
- 查大气湍流时间模型（Greenwood 频率 / 横风 / 功率谱）→ 建时间域衰落生成器
- 产出：`common/_channel.py` 扩展（**只扩不改**——SIM-ORG P4）或新文件
- 参数全部标文献来源（FR-20），禁止拍参数
- 验证：生成的衰落时间序列统计特性 vs 文献（相干时间 / 衰落持续时间 PDF / Rytov 方差）

**脚本**：`explore/cma-fade-divergence/gg_time_fading_model.py`
**结果**：`results/cma-fade-divergence/`（不放脚本旁——SIM-ORG P1）

### Step B：CMA 发散概率扫描（分析层，补 sat.1553 空白）

sat.1553§6 **自认**"probability of the equalizer diverging ... has not been analyzed"。

要做的：
- 用 Step A 的 GG 时间模型 + `common/_recovery` 的 CMA 均衡器（如缺 CMA 需扩 `common/_equalizer.py`）
- 扫描：发散概率 vs 衰落深度（scintillation index）/ CMA 步长 / 均衡器阶数
- **Qin/Nasr 没做的**：scintillation index 扫描（他们只测单一中强强度 r0=0.4mm 固定）
- 产出：发散概率曲线 + 发散条件判据

**脚本**：`explore/cma-fade-divergence/cma_divergence_scan.py`

### Step C：ML 均衡器 MVE（方法层，vs CMA）

要做的：
- 实现 ML 均衡器（参考 Qin VAE 模值环 / Nasr ANN——精读笔记 `papers/_read_notes/qin2025-vae-blind-equalizer.md` + `nasr2026-ann-dual-pol-equalizer.md`）
- 对比：ML 均衡 vs CMA，测度 = 发散概率 + BER + 收敛速度 + 深衰落恢复时间
- **baseline**：固定步长 CMA（FR-14 先验）+ Qin VAE / Nasr ANN（FR-15 贡献目标）
- **Freire2022 6 陷阱 checklist 必须遵守**（`papers/_read_notes/freire2022-nn-equalizer-caveats.md`）：jail window / PRBS 周期 / BER 非 EVM / batch≥1024 / 分类vs回归 / 复杂度报 RMpS

**脚本**：`explore/cma-fade-divergence/mve_cma_vs_ml.py`

## 纪律

1. **守 FR-22**：这是 Step 4a 维度 D MVE（Q-CMA-FADE 已过四判据 + Step 3 精读完成），不是跳框架
2. **守 FR-20**：每个物理参数标文献来源，GG 时间模型是前置门控
3. **守 FR-21**：若 Step B/C 显示发散概率≈0 或 ML vs CMA <0.5dB 且无其他测度优势 → 报 FAIL 不硬撑
4. **守 FR-14/FR-15**：必须含先验 baseline（CMA）+ 贡献目标 baseline（Qin/Nasr）
5. **守 TL-20**：跑仿真前先建理论预期（CMA 在什么衰落条件下应该发散），偏离即查
6. **守 SIM-ORG**：代码进 `explore/cma-fade-divergence/`，结果进 `results/cma-fade-divergence/`，每脚本头部 docstring 标方向+状态
7. **守 Freire2022 checklist**：ML 实验纪律（6 陷阱）
8. **守 sim-preflight skill**：跑 MVE 前触发（如已安装）
9. **主对话禁 WebSearch**：文献查证用 tools/search 子 agent
10. **单对话 3 步上限**：Step A 可能就占一整个对话（GG 时间模型不简单），别想一轮跑完 A+B+C

## 增量定位提醒（避免换皮 TL-12/D006）

**我们补的缺口**（不是照搬 Qin VAE）：
- Qin/Nasr：单一中强湍流 r0=0.4mm 固定 → 我们：**真实 GG 深衰落完整建模 + scintillation index 扫描**
- Qin/Nasr：报 BER/收敛现象 → 我们：**发散概率 + 发散机制解释**（sat.1553 自认空白）
- 测度：不只 dB，还有**发散概率 + 深衰落恢复时间**（新测度）

## 产出

1. GG 时间域衰落模型（common/ 扩展 + 验证通过）
2. CMA 发散概率扫描结果（results/）
3. ML vs CMA MVE 结果（results/）
4. 更新 `projects/thesis-fso/feasibility_report.md` Q-CMA-FADE 节
5. 更新本专题 decisions.md（MVE PASS/FAIL 记录）

---

## 背景速查（不用重读全部，报到后按需读）

- **Q-CMA-FADE 故事线**：`projects/thesis-fso/literature_notes.md` Q-CMA-FADE 章节
- **20 篇精读笔记**：`papers/_read_notes/`（关键：qin2025/qin2026/nasr2026/freire2022/sat.1553）
- **D005 合并决策**：`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D005
- **D004 攒材料策略**：同上 D004（MVE 已获授权推进，攒材料阶段完成）
- **仿真基建**：`projects/simulation/common/`（CMA/GG信道/载波恢复都在，可能需扩 CMA + GG时间域）
- **参数真相源**：`projects/simulation/params.py`
- **物理真相源**：`projects/simulation/SPEC.md`

## 候选池全景（Q-CMA-FADE 首选，但知道有备选）

| 排序 | 候选 | 状态 |
|---|---|---|
| **首选** | Q-CMA-FADE | 四判据全过，本 MVE 执行对象 |
| 备选 | Q-DP3（跨帧恢复） | Conditional Go，纯 DSP 不带 ML |
| 种子 | Q-ML4（双频分离） | 全过但未深探，等首选定了再看 |
