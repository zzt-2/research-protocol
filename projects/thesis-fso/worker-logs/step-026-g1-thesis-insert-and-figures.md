# Step 026 — G1 模块化论文小节与正式图生产

> Task: T026 (THESIS_ARTIFACT_PRODUCTION, CP024, control epoch 57)
> Date: 2026-07-29
> 来源: S002 / D033 / CP024
> Status: `THESIS_INSERT_READY_FOR_MASTER_REVIEW` | mission_method_delta: `NONE`
> artifact_delta: `WRITING_MATERIAL`
> **只产论文插入段 + 两张图 + 可复现资产；不新增实验/检索/科学证据/formal repair；
> 不改 thesis-framework；不把 LOCAL_SLICE 提升为正式主方法；不 push。**

## 0. Task boundary（纪律自检）

- 本步只产出可选的模块化论文小节、一张可编辑方法流程图、一张由既有 raw 数据确定性
  重算的分层结果图及其 PNG 预览与绘图数据/脚本。
- **未做**：新增实验、检索、全文精读闭合、formal repair；未修 T025 package/worker log；
  未改 thesis-framework / references.bib / 论文正文；未改方法/runner/raw/result/测试/
  common 代码；未把候选升级为正式主方法。
- **只新增授权文件**（见 §6 清单），未改其他文件。

## 1. 启动门与 clean 起点

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T026-g1-thesis-insert-and-figures.md
# → PASS
git status --short   # → clean（起点无改动）
```

## 2. 实际读取的材料

按任务 §1 读取：AGENTS.md；research-direction-lab 的 SKILL.md + evidence-and-claims.md
+ thesis-harvest.md；external-output SKILL.md + rules/{translation,claims,exit-check}.md
+ scenarios/paper.md；paper-writing diagnosis；design-paper-figures SKILL.md；T025 方法包
`g1-safe-gated-normalization-package.md` 与 step-025 worker log；V060；`methods.py`；
`raw-rows.csv` / `prefix-receipt.csv` / `result.json`；`anchor.yaml`；
`thesis-framework.md`（只读，识别接口，未改）。

INTAKE 合同：venue=N/A（硕士论文模块化备选）；目标读者=导师与答辩评委；
purpose=可择优并入论文的自包含方法/结果材料；authoritative_science=V060+methods.py+
raw rows；claim_ceiling=LOCAL_SLICE / NONBINDING_DIAGNOSTIC；not_authorized=
thesis-framework integration、novelty claim、new evidence。

## 3. Reference readiness gate（方法流程图）

委托 Explore agent 在本地（papers/、projects/、reference/）检索同结构职责的接收机算法
流程图样本。结果：5 张可定位、同为"门控决策流水线"的样本，全部位于
`projects/simulation/figures/fig1-reference-previews/`（B2-04 / B2-02 / A6-08 / A1-04 /
A1-02），其中 A1-04（接收 DSP 算法切换流程图）、A6-08（黑白门控流水线）、B2-04（菱形门
决策）经视觉确认为同结构职责。可迁移规则：操作框矩形 + 菱形质量门 + 显式 Yes/No 分支 +
共享前端后接门控；不可迁移：神经网络多级串联/解码器长串行。
**未触发 BLOCKED_VISUAL_REFERENCE_GATE。** 无 web 检索/下载。

## 4. 图 B：分层结果图（确定性重算）

脚本 `plot_g1_stratified_results.py` 只读 `raw-rows.csv`（不重跑仿真、不手抄点位）。
统计单位 = seed-cluster（种子内同离线子集各信道 ΔPI-SER 等权均值得一个种子值，10⁴ 次
bootstrap 95% CI）。Δ = method PI-SER − baseline PI-SER，负=改善。

### 重算锚点核对（`--verify`）

```text
collapse mean  computed -0.5597956731  anchor -0.5597956731  [PASS 1e-10]
collapse CI_lo computed -0.6947115385  anchor -0.6947115385  [PASS]
collapse CI_hi computed -0.4063964844  anchor -0.4063964844  [PASS]
collapse help/hurt 12 / 0  [PASS]
healthy G1 worst degradation 0.0  [PASS]
healthy G1 cluster mean -0.0028409091  [PASS]
RESULT: PASS（全部锚点在容差内复现）
```

**RNG 约定核对**：bootstrap 需与 result.json 的 CI 口径一致。经确定性比对，权威约定为
`np.random.default_rng(42)` + 种子值按 seed-id 字符串序排列 + 一次性批量抽取
`(n_boot,n)` 索引矩阵。这是**对齐统计口径**（确定权威 RNG 实现），**非改数据**——均值
在 1e-10 复现，CI 在 1e-9 复现，数据值/方法/单位均未改动。

### 图 B 内容

两 panel：(a) collapse 子集逐种子 ΔPI-SER + 簇均值/CI + help/hurt；(b) healthy 子集
本方法 vs 始终归一化主对照（robust_scalar）逐对退化分布，标 MDE=0.005。图注含 local
slice、条件子集、seed-cluster CI、healthy panel 仅作分布可视化、未形成泛化/竞品结论。
**未做单 bar chart 包装 overall performance。** 视觉 QA（本地图片查看）：CJK 正常、
无重叠/截断、两 series 用圆点/叉标记黑白可辨。产物：`g1-stratified-results.{svg,png}` +
`g1-stratified-results.csv`。

## 5. 图 A：方法流程图

手写可编辑 SVG（`g1-method-flow.svg`，1000×460，低饱和配色，黑白可辨），按冻结语义
brief：CMA 均衡输出 → 前缀/后缀切分 → 双偏振拼接特征 m₂/cv → 菱形健康门（m₂≥0.6 且
cv≥0.1）→ 是：后缀不变（a=1）/ 否：逐偏振稳健功率 + 平方根缩放 a_x,a_y → 后缀标量变换 →
判决输入。箭头分类：实线=数据流、虚线=控制流；**无 suffix→gate 反馈箭头**（后缀数据流
直接绕过门控到输出）。公式/阈值/截尾均值/ε=10⁻⁹ 均与 methods.py 一致。
XML 解析 PASS（well-formed，33 文本节点），无内部代号泄露。PNG 预览经 cairosvg 渲染，
视觉 QA：CJK 正常、无重叠/穿字/截断、箭头可辨。产物：`g1-method-flow.{svg,png}`。

## 6. 论文小节 g1-thesis-insert.md

结构按任务 §4：问题与设计动机 / 门控归一化方法 / 计算流程与复杂度 / 局部仿真结果 /
适用边界 / 并入论文时仍需补充的证据 / 内部 provenance 注释。

确定性自检（provenance 注释之前）：

- CJK 字符数 1960（在 1800–3000 内）；
- 内部代号（G1/M4/T024/V060/D032/D033/D041/Gate6/Phase A/Phase B/FR-21/FR-25/
  NONBINDING/LOCAL_SLICE 等）：正文 **0 命中**（初稿前言曾含 `LOCAL_SLICE/
  NONBINDING_DIAGNOSTIC` 标签，已转译为普通中文）；
- 禁用措辞（逐比特恒等 / 健康样本零代价 / 首次 / 显著优于 / SOTA / 可部署 / 普适 / 解决）：
  **0 命中**；
- 承担论证职责的数字全部在位：0.9578、CI [0.885,1.000]、−0.5598、CI [−0.6947,−0.4064]、
  19/1/1/28、49、12、MDE；
- PI-SER 全称定义（permutation-invariant symbol error rate）在首次缩写使用**之前**；
- 任务 §2 强制修正措辞全部落实：写"接收信号前缀"非"已知结构"、写"逐复样本恒等"非
  "逐比特恒等"、写"健康分支零后缀变换扰动"非"健康样本零代价"、写"始终归一化可能扰动
  健康输出且当前切片观察到退化"非普遍必然退化、写"ΔPI-SER=−0.5598 错误率绝对降低约
  0.56"非"恢复后错误率约 0.56"、明确门控由 128 符号前缀冻结、zero-worst 仅作当前切片观测。
- 结果叙事严格按"现象—对照—解释—边界"；49 对未写成 49 个独立 seed。
- 定位为"16QAM 扩展备选"，未声称与当前 QPSK/Gamma-Gamma/CPR 主线融合。

## 7. Changed files（本步产出）

```text
projects/thesis-fso/direction-lab/harvest/g1-thesis-insert.md
projects/thesis-fso/direction-lab/harvest/g1-figures/g1-method-flow.svg
projects/thesis-fso/direction-lab/harvest/g1-figures/g1-method-flow.png
projects/thesis-fso/direction-lab/harvest/g1-figures/g1-stratified-results.svg
projects/thesis-fso/direction-lab/harvest/g1-figures/g1-stratified-results.png
projects/thesis-fso/direction-lab/harvest/g1-figures/g1-stratified-results.csv
projects/thesis-fso/direction-lab/harvest/g1-figures/plot_g1_stratified_results.py
projects/thesis-fso/worker-logs/step-026-g1-thesis-insert-and-figures.md  (本文件)
```

均为授权新增；无其他文件改动。

## 8. 独立 reviewer 审查

安排两个独立只读角色（semantic/claims + figure/visual），分别独立审查小节语义/声称与
两图的标签/箭头/重算/视觉。

### Figure/visual reviewer：P0=0 / P1=0 / P2=2，判 PASS

- 图 A 标签/流程与冻结 brief 一致；箭头分类正确（实线数据流、虚线控制流）；**无
  suffix→gate 反馈箭头**；公式（0.6/0.1、平方根、10% 截尾、ε=10⁻⁹）与 methods.py 一致；
  SVG XML well-formed、文本可编辑；PNG 视觉 QA 无 tofu/重叠/截断，两分支颜色+位置可辨。
- 图 B 只读 raw-rows.csv（无重跑）；`--verify` PASS、全部锚点在容差内复现；统计单位
  seed-cluster 正确、healthy panel 仅作分布可视化（未对 pair 算 CI）；非单 bar 包装；
  图注披露 local slice/条件子集/seed-cluster CI/分布仅作可视化/无泛化竞品结论；视觉 QA
  两 series 圆点/叉标记黑白可辨。P2 仅为图例未单列蓝色合并箭头（语义自明）与一处正交
  箭头交叉（颜色区分，非文本遮挡）——非阻塞。

### Semantic/claims reviewer 初审：P0=1 / P1=0 / P2=2，判 FAIL

- 公式/信息访问、PI-SER 定义与 ΔPI-SER 口径、条件子集非全样本、49 非 49 seed、
  zero-worst 作观测、无 overclaim、CI 用 V060 正确口径 [0.885,1.000]、禁用措辞 0 命中、
  正文 0 内部代号、framework 边界（16QAM 扩展备选非融合）——全 PASS。
- **P0（数据错误）**：塌缩种子数误写为"20 个塌缩种子"，正确为 13（result.json
  `collapse.gated_scalar` n_seeds=13，help/hurt/tie=12/0/1；V060 class support=13）。
- P2：缺少任务 §2 item2 指定短语"逐复样本恒等"（语义已对、禁用"逐比特恒等"已去除）。

### 修复（P0 + 可顺带修的 P2）

- P0：塌缩现象句改为"该子集含 13 个种子簇，其中 12 个显著改善、0 个显著退化、1 个并列
  （MDE=0.005）"，删除错误的"20 个塌缩种子"。注：图 B 脚本本就用 13 个塌缩种子簇且
  `--verify` 复现 help/hurt=12/0，图与数据一致；仅小节文字写错，已改。
- P2：健康分支描述采用任务指定短语"被评分后缀逐复样本恒等（输出样本不变）"。

### 复审（确定性重核，TL-21）

对小节（provenance 注释前）做确定性 grep：

```text
CJK 字符数 1972（在 1800–3000 内）
含 "13 个种子簇": 是   仍含 "20 个塌缩种子": 否
含 "逐复样本恒等": 是   含禁用 "逐比特恒等": 否
内部代号（G1/M4/T024/T026/V060/D032/D033/Gate6/Phase A/Phase B/LOCAL_SLICE/NONBINDING/formal Go）: 0 命中
禁用措辞（首次/显著优于现有方法/SOTA/可部署/普适/解决/健康样本零代价/恢复后的错误率约）: 0 命中
关键数字（0.9578 / 0.885 / 1.000 / −0.5598 / −0.6947 / −0.4064 / 19/1/1/28 / 49）: 全部在位
```

图 B `--verify` 复跑仍 PASS（锚点未动，图未重渲染）。公式与数字未改动（初审已 PASS），
故仅重核文字正确性。

**最终：semantic/claims P0/P1/P2=0/0/0（P0 已改、P2 已顺修），figure/visual
P0/P1/P2=0/0/0，审查通过。**

## 9. 验证命令

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T026-g1-thesis-insert-and-figures.md
python projects/thesis-fso/direction-lab/harvest/g1-figures/plot_g1_stratified_results.py --verify
git diff --check
git status --short
```

确认只新增授权文件，做一个 consolidated commit，不 push。
