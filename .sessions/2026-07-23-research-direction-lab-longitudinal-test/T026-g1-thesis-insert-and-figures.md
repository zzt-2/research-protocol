# Task Brief: G1 模块化论文小节与正式图生产

> 来源: S002 / D033 / CP024
> 产出位置: `projects/thesis-fso/worker-logs/step-026-g1-thesis-insert-and-figures.md`
> 日期: 2026-07-29
> 唯一文档: 执行方只拿到本 T；可读取本文列出的仓库材料

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 57
  action_class: THESIS_ARTIFACT_PRODUCTION
  mission_checkpoint: CP024
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T025 已形成一个内部有边界方法包，但它还不是可直接进入论文的成品。你的任务是
**直接产出可选的模块化论文小节与两张正式图**，而不是再写一份评价或包装报告：

1. 一份自包含中文论文小节；
2. 一张可编辑的方法流程 SVG；
3. 一张由既有 raw 数据确定性重算的分层结果 SVG；
4. 两图的 PNG 预览与绘图数据/脚本；
5. worker log。

科学上限固定为 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。不得新增实验、检索、
全文闭合、formal repair 或论文结构变更；不得把 G1 升成正式主方法。

## 1. 启动门

先读取：

1. `AGENTS.md`
2. `.agents/skills/research-direction-lab/SKILL.md`
3. `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
4. `.agents/skills/research-direction-lab/references/thesis-harvest.md`
5. `.agents/skills/external-output/SKILL.md`
6. external-output 的 `rules/translation.md`、`rules/claims.md`、
   `rules/exit-check.md`、`scenarios/paper.md`
7. paper-writing skill 与 `references/diagnosis.md`、`references/revision.md`、
   `references/verification.md`
8. design-paper-figures skill 与所需 pattern/renderer reference
9. `projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md`
10. `projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md`
11. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md`
    的 V060
12. `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/`
    下的 `src/methods.py`、`artifacts/raw-rows.csv`、
    `prefix-receipt.csv`、`result.json`
13. `projects/thesis-fso/direction-lab/anchor.yaml`
14. `projects/thesis-fso/thesis-framework.md`（只为识别当前论文结构接口，禁止修改）

运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T026-g1-thesis-insert-and-figures.md
git status --short
```

validator 非 PASS 或起点不 clean，立即返回
`BLOCKED_CONTROL_OR_DIRTY_START`。

INTAKE 合同：

```text
venue: N/A（硕士论文模块化备选小节）
target_reader: 导师与答辩评委，懂通信大领域但不知道内部研究过程
purpose: 形成可择优并入论文的自包含方法/结果材料
authoritative_science: V060 + methods.py + raw rows
claim_ceiling: LOCAL_SLICE / NONBINDING_DIAGNOSTIC
not_authorized: thesis-framework integration, novelty claim, new evidence
```

## 2. 冻结科学事实与必须修正的对外措辞

方法和数字以 T025/V060 为源，不重新选择结果。必须修正以下外部表达：

1. 不写“一段已知结构”或暗示已知发送符号。门控只读**接收信号前缀**，
   发送端真值只参与离线评价标签；
2. 不写“逐比特恒等”，应写“逐复样本恒等/输出样本不变”；
3. 不写“健康样本零代价”。正确说法是“健康分支不变换被评分后缀，因此零
   后缀变换扰动”；仍需计算前缀门控特征；
4. 不把 always-on normalization 写成普遍必然退化。只能写：它可能扰动健康
   输出，并且在当前局部切片的安全性指标上观察到退化；
5. 不写“恢复后的错误率约 0.56”。正确说法是：在离线标注的 collapse 条件
   子集上，相对 tuned CMA 的
   \(\Delta\mathrm{PI\!-\!SER}=-0.5598\)，即错误率绝对降低约 0.56；
6. 首次定义“偏振置换不变符号错误率
   （permutation-invariant symbol error rate, PI-SER）”；
7. 不把整个模块称为“无记忆层”。门控由 128-symbol prefix 冻结；只有冻结后
   的 suffix 标量变换是逐样本的；
8. “zero worst-case degradation”只能表述为当前 healthy local slice 的观测，
   不是数学保证或部署保证。

在线信息边界、公式、阈值、128-symbol prefix、10% trimmed mean、per-pol
sqrt scale 必须与 `methods.py` 一致。

## 3. 授权产物

只允许新增以下目录/文件：

```text
projects/thesis-fso/direction-lab/harvest/g1-thesis-insert.md
projects/thesis-fso/direction-lab/harvest/g1-figures/
  g1-method-flow.svg
  g1-method-flow.png
  g1-stratified-results.svg
  g1-stratified-results.png
  g1-stratified-results.csv
  plot_g1_stratified_results.py
projects/thesis-fso/worker-logs/step-026-g1-thesis-insert-and-figures.md
```

不得修改：

- T025 package/worker log；
- `.sessions/**`；
- master-state、projects-overview、current YAML；
- `thesis-framework.md`、`references.bib` 或任何论文正文；
- 方法、runner、raw/result、测试或 common 代码。

## 4. 论文小节

创建 `g1-thesis-insert.md`。这是一份模块化备选，不假装已经并入当前论文。

建议结构：

1. `## 接收端前缀门控的安全幅度归一化`
2. `### 问题与设计动机`
3. `### 门控归一化方法`
4. `### 计算流程与复杂度`
5. `### 局部仿真结果`
6. `### 适用边界`
7. `### 并入论文时仍需补充的证据`
8. `<!-- INTERNAL PROVENANCE: ... -->`

写作要求：

- 正文约 1800–3000 个中文字符，不用内部代号；
- 开头从双偏振相干接收机、盲均衡输出幅度异常和 always-on 校正风险讲起；
- 给出 pooled gate 特征、identity/scale 条件、per-pol sqrt scale 公式；
- 图首次出现前定义图中缩写；
- 结果叙事严格按“现象—对照—解释—边界”；
- 只报告承担论证职责的数字：
  - gate 诊断：eligible 49、balanced accuracy 0.9578、cluster CI 约
    `[0.885,1.000]`；
  - collapse：ΔPI-SER `−0.5598`、CI `[−0.6947,−0.4064]`、12/0；
  - healthy：当前切片 worst degradation `0`；
  - map ablation 可选，若使用必须明确不是直接竞品；
- 不把 49 对写成 49 个独立 seed；
- 不写“首次、显著优于现有方法、SOTA、可部署、普适、解决”；
- 不在外部正文展开错误 Gate6、D4 占位或流程历史；只在内部 provenance
  注释中保留最小来源指针；
- 当前 `thesis-framework.md` 以 QPSK/Gamma-Gamma/CPR 为主体，本小节只标为
  “双偏振星地光链路接收 DSP 的 16QAM 扩展备选”，不得擅自改论文目录或声称
  已与当前主线融合。

## 5. 图 A：方法流程图

目标：一眼说明“同一接收前缀决定 identity 或 per-pol sqrt scale，后缀不反馈”。

### Reference readiness

先委托子 agent 从本地已获得论文/学位论文中找至少 2 张可定位、同为接收机
算法流程/门控处理结构的图。每张记录：

`paper/path | figure/page | structural role | transferable rule | non-transferable detail`

不新增 web 检索或下载。若本地找不到 2 张可定位、同结构职责的样本，停止为
`BLOCKED_VISUAL_REFERENCE_GATE`；不得凭“通用流程图很简单”绕过 reference
readiness gate。

### Semantic brief

必须包含并冻结以下 label/flow：

```text
CMA 均衡输出
128 符号接收前缀
双偏振拼接特征 m2 与 cv
是否满足健康条件？
是：后缀保持不变
否：逐偏振稳健功率估计
平方根幅度缩放 ax, ay
判决输入
```

箭头分类：

- CMA output 到 prefix/suffix：数据流；
- features 到 branch：控制流；
- scale parameter 到 suffix multiplier：控制流；
- suffix 到 output：数据流；
- 禁止画 suffix→gate 反馈箭头。

渲染要求：

- editable SVG 为主，PNG 只作预览；
- 紧凑论文比例，建议约 1000×460，不做 16:9 标题页；
- 低饱和配色，黑白打印仍可区分；
- 无装饰图标、3D、阴影、海报式卖点标注；
- 所有公式来自冻结源；
- SVG XML 可解析，字体与箭头不截断、不穿字。

## 6. 图 B：分层结果图

必须从 `raw-rows.csv` / `prefix-receipt.csv` 确定性重算，不能手抄点位或重新跑
仿真。保存脚本、CSV、SVG 和 PNG。

推荐两 panel：

- **(a) collapse 条件子集**：以 seed cluster 为统计单位，画本方法相对 tuned
  CMA 的逐 seed ΔPI-SER + 均值/95% CI；明确负值表示改善；
- **(b) healthy 条件子集**：画本方法与冻结的 always-on primary comparator
  `robust_scalar` 的逐 pair
  degradation 分布或 ECDF，并标 MDE=`0.005`；不得把 pair 当独立统计单位计算 CI。

冻结核对锚：

```text
collapse mean ≈ -0.559796
collapse CI ≈ [-0.6947, -0.4064]
collapse help/hurt = 12/0
healthy G1 worst degradation = 0
healthy G1 cluster mean ≈ -0.0028409
```

脚本计算值超过 `1e-6`（均值）或 `5e-4`（CI，bootstrap RNG 允许）偏离锚点，
立即停止为 `BLOCKED_EVIDENCE_RECOMPUTE_CONFLICT`，不得为了对齐改数据。

图注必须包含：

- local slice；
- collapse/healthy 是离线标签条件子集；
- CI 的 seed-cluster 单位；
- healthy panel 若展示 pair distribution，明确它只作分布可视化；
- 当前未形成领域泛化或直接竞品结论。

不得只做一个 bar chart 把条件均值包装成 overall performance。

## 7. 审查与验证

至少安排两个独立只读审查角色：

1. **semantic/claims reviewer**
   - 公式与信息访问是否一致；
   - PI-SER/ΔPI-SER 是否定义正确；
   - local/conditional 是否被抬成 overall/general；
   - 是否暗示已知 TX prefix、formal Go、novelty 或竞品胜利；
2. **figure/visual reviewer**
   - label、箭头与 data/control flow；
   - SVG editability/XML；
   - PNG 最终尺寸下的截断、重叠、字体和黑白可辨性；
   - 结果图是否由 raw 重算、统计单位是否正确。

用本地图片查看工具检查两个 PNG；不能只看生成日志。P0/P1 必须为 0。

运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T026-g1-thesis-insert-and-figures.md
python projects/thesis-fso/direction-lab/harvest/g1-figures/plot_g1_stratified_results.py --verify
git diff --check
git status --short
```

确认只新增授权文件，做一个 consolidated commit，不 push。

## 8. 终态与回执

允许：

- `THESIS_INSERT_READY_FOR_MASTER_REVIEW`
- `BLOCKED_EVIDENCE_RECOMPUTE_CONFLICT`
- `BLOCKED_VISUAL_REFERENCE_GATE`
- `BLOCKED_VISUAL_QA`
- `BLOCKED_CONTROL_OR_DIRTY_START`

成功时：

```text
status: THESIS_INSERT_READY_FOR_MASTER_REVIEW
mission_method_delta: NONE
artifact_delta: WRITING_MATERIAL
commit: <sha>
worker_log: projects/thesis-fso/worker-logs/step-026-g1-thesis-insert-and-figures.md
thesis_insert: projects/thesis-fso/direction-lab/harvest/g1-thesis-insert.md
figures: projects/thesis-fso/direction-lab/harvest/g1-figures/
one_line_result: <一句普通中文，说明已生成什么、局部证据上限和是否可直接并入论文>
```

不要返回长篇过程，不要 push。
