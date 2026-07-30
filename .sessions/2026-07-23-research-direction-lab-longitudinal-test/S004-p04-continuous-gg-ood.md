# [S004] P04 连续 GG OOD 选择器鲁棒性端到端执行

> 2026-07-30 | CAMPAIGN_EXPLORATION_DISPATCH (D039 campaign P04) | 状态: closed (CP033/V068)

## 目标

执行 10-package campaign 的 Package 04。先撤回无效的 16APSK 环比入口，再在同一对话端到端执行
"连续 GG 参数 OOD 下的 selector 鲁棒性"；不得停在入口修订或 problem probe 后（绑定裁决）。

## 记录

### 入口撤回（绑定裁决）

原 P04 入口（`P04-entry-selection-NOT-RUN.md`：16APSK 环比失配 + 备选湍流标签失配）经绑定裁决独立审计
四条 FAIL：①γ（环比）是调制格式配置非当前信道随机量；②冻结选择器 `decide(raw,γ_db,γ_lin)`
（`_a4_switch_common768_30seed.py:97-107`）信息边界干净——不读环比（环比只进 `per_block:124-139` 内
`m16apsk_demod` 即分支输出 ne_da/ne_nda 产生，selector 只读分支输出错误计数 `main:335-342`）也不读
turbulence label（`main:312` 循环变量从不传入 decide；`method.tex:75`/`abstract.tex:2` 明确"turbulence label
... are not control inputs" / "same received-power-driven rule ... without turbulence-specific retuning"）；
③matched/configured demod 是显然常规解；④两入口均无 selector 可作用面。保留 rejected brief 供审计，
不计有效 P04。合法问题改写为"固定/AWGN 拟合的 CV decision boundary 在文献 σ_R²∈[0.2,3.5] 范围内、训练未见过的
连续 GG 分布上是否产生 selector-specific regret"（family=C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS）。

### testbed 冻结（读结果前，worker-log §1）

- σ_R²→(α,β) 用 Al-Habash plane-wave 闭式（`system_model.tex:16-21`，验证复现 3 锚点 ≤2.70%；mcs `rytov_to_gg`
  piecewise-symmetric proxy 显式不用）。
- 显式 (α,β) 注入经 `generate_shared_realization_apsk(turb_params=...)`（`common/_channel.py:97-99,10-24`），
  复用 TL-13 共享信道。
- dev grid σ_R²∈{0.2,0.45,0.7,1.15,1.6,2.0,2.55,3.0,3.5}（含 3 锚点作回归/控制）；held-out σ_R²∈{0.3,0.9,
  1.35,1.85,2.3,3.15}（6 interior-only，disjoint）；SNR∈{5,7,9,11,13} dB；dev seeds 0-9 / held-out 30-49；
  MDE=0.15 dB（P01/P02/P03 同）；400 windows/cell。
- problem gate：pooled held-out interior regret `10·log10(sel/min(fixed_DA,fixed_NDA))` ≥ MDE AND CI_low>0。

### 执行

**锚点回归 gate（Phase A.1 BLOCKER）— PASS**：explicit (α,β) ≡ scene-name 路径，108 字段 0 mismatch。
一次包内确定性修复：`sigma2_to_ab` 在 3 训练 σ_R² 用冻结四舍五入锚点对（11.6,10.1)/(4.0,1.9)/(4.2,1.4)
（锚点训练于此非 Al-Habash 精确值），内部连续点用 Al-Habash（≤2.70% 偏离）。

**Phase A dev（450 cell, 288s）**：pooled interior regret +0.1393 dB（CI=[+0.0945,+0.1840]），CI_low>0 但 < MDE。
**关键诊断**：anchor-cell regret +0.2306 dB > interior +0.1393 dB → 非 OOD-specific。

**Phase A held-out（600 cell, 365s）**：pooled interior regret +0.1459 dB（CI=[+0.0827,+0.2090]），仍 < MDE。
dev/held-out 一致（差 0.007 dB）。Phase A 门（pooled，读结果前冻结）未过 → Phase B/C 不运行 →
**`PROBLEM_ABSENT_ON_CONTINUOUS_GG`**。

**诚实子区间**：9/30 interior cell 超 MDE 且 CI_low>0（σ_R² 0.3/0.9/1.35 × γ 5-11，最强 σ_R²=0.30 γ=9 +0.678 dB），
但非 OOD-specific——同一 over-NDA-select 在 weak 训练锚点上更强（σ_R²=0.2 γ{5,7,9,11}=+0.39/+0.78/+0.98/+0.56
均 > interior σ_R²=0.45 同 cell）。regret 随 σ_R² 增大单调下降，强湍流侧 <0.15、γ=13 dB 转负。selector 是通用
NDA-over-selector，连续 GG 形状不让 AWGN 拟合边界退化。

### 独立验证

verifier V068 **8/8 PASS**（raw→aggregate 0.000e+00、锚点门独立重跑 0 mismatch、seed 隔离干净、信息边界 AST 干净
true α/β/h 不进 decide、冻结文件未改仅新增 _p04_*、verdict 唯一正确、子区间诚实）。

### 治理更新

D042 / V068 / CP033 写入；topic-index control block 升 epoch 67→68、accepted_valid 3→4、current P04→P05、
families_started 追加 C、rolling_queue 追加 P04；mission-log 追加 CP033。

## 决策引用

- D042：P04 连续 GG OOD → PROBLEM_ABSENT_ON_CONTINUOUS_GG（新建）
- V068：P04 独立验收 8/8 PASS（新建）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D039 campaign 授权范围内第 4 个有效包，problem-first 三阶段门控；
  撤回两入口是绑定裁决要求，保留 rejected brief；无 protected owner/formal/Skill/thesis framework 改动、无 push、
  无新大型基础设施；一次包内确定性修复已披露）。

## 后续

- P05 是 mid-calibration 包（D039 §4 第 5 包内部校准，不停线）。P01-P04 verdict 序列 NO_SIGNAL/
  RESOLVED_REGION/RESOLVED_UNIFORM/ABSENT 全 honest negative，4 包都在"已完成选择器新失效条件"框架且作用区
  重叠（低 SNR/weak turbulence）→ **偏航信号**。P06+ 应换机制距离更远族（D 调制编码层 HD/SD-FEC/APSK 旋转模糊，
  或 E 信息复杂度边界 窗口长度/低复杂度降级），而非 C 族第 2 包或 A 族邻近轴。
- 本轮选择 P05 新机制族入口但不运行（绑定裁决"同一对话选择 P05 的新机制族入口，但不运行"）。
- weak-side-low-SNR 子区间（9/30 cell > MDE）作 future-work seed，但与已关闭 A 族（SNR-mismatch/region-retune）
  工作区重叠，TL-30 禁换名重开。
- 仍 0 active carrier；某 package 出 DIAGNOSTIC_METHOD_SIGNAL 且过 promotion preflight 前不晋级。
