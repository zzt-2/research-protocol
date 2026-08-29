# Task Brief: Ch4 scaled-unitary thesis method 章级写作包

> 来源: S028 / D052 / T069 / T071 / V025 / V027 | 产出位置: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 14
  action_class: CH4_METHOD_PACKAGE_MATERIALIZATION
  mission_checkpoint: CP014
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务与写作状态

把已经冻结为 `THESIS_METHOD_READY` 的 Ch4 证据转换成一套“打开即可开始写章”的内部材料包；不编辑正式论文正文，不产生新科学数字。按 `paper-writing` 执行 `INTAKE→DIAGNOSE→PROPOSE→WRITE→VERIFY→DELIVER`：本 brief 与 D052 是已批准 change contract，target reader=硕士论文作者/导师，venue=`N/A`，权威源为 T068/T069/T071/V027、实现与 raw artifacts。

正式方法名冻结为：**基于缩放酉约束的短导频偏振信道估计与解复用方法**。英文工作名可用 *Short-Pilot Scaled-Unitary Constrained Polarization Estimation and Demultiplexing*，不得自行创造夸张缩写。

## 交付目录

在 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/` 形成：

1. `README.md`：包状态、方法一句话、文件导航、权威源、仍未覆盖项。
2. `fact-matrix.md`：每个核心事实/数字/公式对应数据或文件指针、比较对象、metric 意义、可写结论与禁止外推；无指针不得进入蓝图。
3. `chapter-blueprint.md`：按“问题与场景→baseline→方法推导→算法流程→复杂度→仿真设置→结果→边界”给出三级标题、每节承重句、对应图表/公式/引用与建议篇幅；这是内部写作蓝图，不是正式段落。
4. `algorithm-box.md`：冻结输入、输出、pilot-LS、SVD、`g=(s1+s2)/2`、`H_SU=gUV^H`、逆矩阵/解复用、fail-closed 条件与复杂度；公式须从 T068/实现核对，不凭记忆。
5. `claim-and-citation-ledger.md`：允许主张、必须披露、可省略的内部失败史、禁止主张、引用候选与 exact source pointers。B2 必须作为主廉价对手；C4 与 B2 同 `UV^H` 的事实不能隐藏。
6. `data/ch4-confirmation-summary.csv`：由 confirmation raw 独立 reducer 生成的四格 B0/B1/B2/C4/O1 BER、C4−B2 mean/CI、相对降幅与 pooled Np2；逐值对 V027。
7. `plot_ch4_results.py`、`figures/ch4-ber-comparison.svg` 与 PNG preview：只画 confirmation 四格，主视图清楚比较 B2 与 C4，并保留 B0/O1 作为上下文；不得选择性删除较小增益格或修改坐标制造夸张视觉。
8. `method-figure-semantic-brief.md`、`figures/ch4-method-flow.svg` 与 PNG preview：用 `design-paper-figures`，参考本专题已批准的中文论文图风格和共同链，画紧凑可编辑矢量图。必须包含双偏振短导频输入、pilot-LS、SVD/缩放酉投影、逆矩阵解复用、两路输出→Ch3 CPR；区分数据流与估计/控制流，不画未启用的 PDL/PMD/FIR/LDPC。
9. `verification.md`：记录生成命令、CSV 对 raw/V027 的逐值检查、SVG/PNG 尺寸与视觉 QA、标签/箭头/黑白可读性、独立 reviewer 结论和 terminal。

## 冻结事实与展示政策

- Confirmation 四格相对 B2 的 BER relative reduction=`7.37%/2.62%/8.38%/5.06%`；Np=2 pooled B2/C4=`0.06076145/0.05608821`，absolute diff=`-0.00467324`，95% CI=`[-0.00686385,-0.00282661]`，relative=`7.69%`。所有数值须从 raw fresh 派生并与 V027 对齐。
- 方法场景仅为静态 unitary 2×2 + common scalar Gamma–Gamma + equal circular AWGN、DP-(8,8)-16APSK、短 balanced pilots；无 PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC。图中可标“目标验证场景”，不能暗示全链损伤均已验证。
- Favorable presentation：正式建议优先展示 confirmation 与 pooled Np2，开发集只放 provenance/内部附录；已停 C4-2、无关失败和全仓 collection errors 不进入对外主叙事。四格均支持核心 claim，故不得挑格。任何影响公平性/方法身份/metric 的事实必须保留。
- 主张限于“缩放酉结构投影在短导频目标场景相对正确 LS/SV-floor baseline 带来有限 BER 改善”；不得写新旋转、新估计理论、首次、SOTA、全面超过近期强方法或已完成全编码链。

## 边界、QA 与冻结终态

1. 禁止运行 confirmation/development，禁止修改仿真、raw/aggregate/receipt、Skill/controller 或正式论文正文；只允许 raw-only 读取、确定性派生、绘图与内部文档。
2. 方法图采用 editable SVG first；data plot 用确定性脚本。两张 PNG 只是 preview。必须在论文栏宽/页面宽近似尺寸下检查文字、箭头、图例、色盲/黑白区分与无截断。
3. 由未参与生成的内部 reviewer 对 fact matrix→蓝图→两图做独立证据/语义/视觉审查；P0/P1 必须为 0，P2 可保留明确局部限制。
4. `CH4_WRITE_PACKAGE_READY`：所有九类交付存在，CSV 数字逐值匹配 raw/V027，方法图标签与箭头语义正确，结果图不夸张，独立 reviewer PASS 或仅 P2；否则 `CH4_WRITE_PACKAGE_PARTIAL` 并列精确缺口。不得把内部包 terminal 写成正式论文已写完。
5. 墙钟 60 分钟；前 10 分钟完成 fact matrix 骨架和 renderer 选择，40 分钟时优先保证数据图、方法图与蓝图齐全。一次 commit、不 push；回报 commit、terminal、目录、两图预览路径、独立审查与任何 blocker。
