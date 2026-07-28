# [R007] Post-C15 机制级 carrier remap

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D021 / formal D032 / CP016

## 调研问题

T016 已按一次性退出边界把 C15 返回候选池，当前无 active scientific carrier。
在不运行 seed/MVE、不修旧 evaluator/source package、也不把 formalization 冒充
方法产出的前提下，哪个机制级候选最值得获得下一次一次性正式化工作包，并且其
到 `METHOD_SIGNAL` 的路径为何优于至少两个替代项？

## 发现

### 1. 证据边界与 readiness 口径

- 当前前台控制为 epoch 41 / CP016 / formal D032，只允许
  `PORTFOLIO_MAP`、`FORMAL_READINESS_REVIEW` 与任务准备。
- `projects/thesis-fso/direction-lab/portfolio/current.yaml` 明确
  `formal_active_carrier.id=NONE`；因此以下均是 **formalization candidate**，
  不是已激活 carrier。
- readiness 采用 RDL current 口径：
  `READY` 必须同时具备实现、合法输入/输出合同、公平 comparator、evaluator
  与 runnable entry；只有方法想法或旧代码不构成 READY。
- 本轮为开放 portfolio 的有界刷新，不声称数学完备。候选来自 current
  portfolio 的 reopened axes、formal history 的未决 Q#、现有全文笔记和明确的
  task-mismatch/scene-transfer 债。
- 旧 C16 `synthesis.v1.md` 的“机制负面/关闭 paradigm axis”已被 current
  portfolio D017 amendment 取代；本轮只继承其实现形态事实，不继承旧科学结论。

### 2. 五个机制不同候选的六维比较

| candidate | 方法形态 | 预期增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **C16-open：能力对齐的 full-complex 2×2 FIR non-modulus blind equalizer（推荐一次性 Step 1–2 formalization）** | 面向双偏振时域卷积混合的完整复数 2×2 FIR 非模盲均衡；候选机制为 source-backed convolutional HOS / cumulant joint-diagonalization 或精读后确认的等价非模机制。必须与 11-tap butterfly CMA/MMA 对齐 tap、样本、更新预算；禁止复用旧 spatial whitening + real-Givens heuristic | **T017 固定为 `NONE`**：只闭合 Step 1–2 formal readiness。若后续 Step 3/3.5 形成合法 Q#，再进入 Step 4a；只有更后的最小构造包才可能产生 `CONSTRUCT_CREATED + FAIR_COMPARISON_RUN`，并以稳定优于 tuned CMA/MMA 才计 `METHOD_SIGNAL` | “面向动态星地 PM-16QAM 的时域能力对齐非模高阶统计盲 FIR 均衡方法。”该句目前只是候选包装，不得对外声称 | **HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE**。current portfolio 只证明旧 C16 task-mismatched，equalizer-paradigm axis 因而 reopened；`literature_notes.md` 没有 C16 的 formal Step 1–3 条目，旧代码只给 generic JADE/ICA/FastICA provenance，未闭合 complex convolutional FIR、光相干任务与 direct competitor identity | 一次 Step 1–2 包：≥3 actual sources、≥20 unique、正式发表≥50%、必读≥5、≥2 route；取得≥5 篇合法全文并形成 coverage-gap report。停止在用户 coverage confirmation 前，不精读、不写 Q#、不实现、不实验 | source<3、找不到 task-matched complex FIR 非模方法族、核心全文<5、或 direct competitor 已占满同一 M-C-A，任一即返回池且不给第二个 C16 source/formalization 包；优先轮到 Q14 problem-evidence closure，其次 Q-ML4 scene-transfer adjudication |
| **Q14：standard-CMA 后置 additive residual cascade** | `z_out=z_CMA+gφ(z_CMA, context)`；只允许 receiver-visible context，并与 CMA-only、fixed+PI、同预算 simple-DSP residual、raw-ML 和 oracle 分开比较 | 下一包只能把四判据 2 从 UNKNOWN 闭合为 PASS/FAIL，预期 `NONE`；只有问题存在且 cheap DSP 不能覆盖后才可能建 residual head | “面向动态星地双偏振链路的在线 CMA 后置轻量残差校正，在保留盲跟踪能力的同时补偿稳定可辨识的剩余失真。” | **HYPOTHESIS_ONLY / PROBLEM_EVIDENCE_BLOCKED**。Step 1–3 与 5/5 全文已完成，但 `literature_notes.md:123`、S039、D044 明确四判据 2 UNKNOWN；未授权 A0/MVE。P03 的 QPSK local zero-headroom、blind affine harmful 与 exact hybrid-routing 低 headroom 只是负先验，不作 family Kill | 一次不实现方法的 receiver-visible information-increment/problem closure；必须证明残差稳定且不能被 fixed+PI/simple DSP 吸收，再重写 Q14 | 判据 2 仍 UNKNOWN、simple DSP 吸收残差、或合法输出没有 decision/soft-information收益即退出，不再把单一 residual 微变体独占主线 |
| **B4：时延约束多速率双环载波恢复** | source-native PADE 粗频偏外环 + V–V residual/phase 内环作为 baseline；候选增量只能是依据 receiver hardware delay/parallelism 调度慢/快环更新率，不能把湍流相位塞进环路传函 | 下一包仍为 `NONE`；先证明 carrier-specific latency M-C-A 与 residual novelty，随后还需 PADE/双环基础实现 | “面向高并行星地相干接收的时延约束多速率双环载波恢复，以慢速 PADE 外环和快速 V–V 内环协同约束动态捕获、残频与资源代价。” | **HYPOTHESIS_ONLY / MCA_BLOCKED**。源论文已拥有双环本身；B4 精读只给 timing-feedback latency 邻近证据，合法 PADE 参数/全文和载波专属 delay problem 不闭合；仓库只有通用 DPLL/VV 资产，无 PADE/双反馈状态机 | 闭合 PADE/环路参数、载波专属 latency 证据、direct multi-rate competitor 与 comparator contract；成功后仍要新建基础实现 | 全文/参数、载波专属 latency、residual novelty 三门任一失败即退出；禁止转回 PCS/Rs 或 D006 湍流环路旧轴 |
| **Q-ML4：双时间尺度湍流代理与受约束反演** | 将 Gao 2025 的 CVAE 高频分支 + residual BiLSTM 低频分支 + gate，从 IM/DD 辐照度代理改写为 coherent complex-field/receiver-visible DSP 代理；cheap comparator 为 AR/EMA 双时间尺度规则和同容量单分支模型 | 下一包只能做 source identity、scene-transfer 与 Q# 重写，预期 `NONE`；不能把原文 79% BER 当相干星地增量 | “面向星地相干 FSO 多时间尺度湍流的双分支可微信道代理与受约束符号级反演补偿。” | **HYPOTHESIS_ONLY / SCENE_TRANSFER_BLOCKED**。`literature_notes.md:1109` 的旧“全过”只对应原 IM/DD 问题；全文笔记明确原方法是辐照度级、约 30 m 地面实验、无 LO，非 complex-field/符号级相干 DSP。当前无 formal owner、direct competitor 或实现 | 一次 scene-transfer adjudication：证明 complex-field 转译仍保留双频失效机制与 receiver-visible output，补 direct coherent/star-ground competitor；否则不建模型 | 转译后机制不守恒、方法只剩场景替换、cheap AR/EMA 足以覆盖，或 direct competitor 占点即退出 |
| **C04/C09-open：非仿射因果时序 residual corrector** | 修复旧 self-referential affine target 后，以严格因果多 block receiver-visible history 预测非仿射 residual；必须先定义非退化 target 和与 simple DSP 的信息增量合同 | 下一包只能做 target/problem contract，预期 `NONE` | “面向动态盲均衡残差的严格因果时序校正，在不使用发送真值的条件下利用跨块状态连续性。” | **HYPOTHESIS_ONLY / TARGET_CONTRACT_BLOCKED**。current portfolio 明确 C04 目标存在 input-independent zero-loss 解，C09 未在科学合法 target 上运行；F3 的 `+0.060 bits` 又已撤回为 marginal-MI，不能当 conditional-information 证据 | 一次非退化 target 数学检查 + receiver-visible conditional-information contract；不得先训练 GRU | target 仍有常数解、conditional information 不成立、或 fixed+PI/simple DSP 覆盖即退出 |

### 3. READY census 与其他候选为何不能补足

本次有界刷新得到：

```text
READY=0
NEEDS_SMALL_ADAPTER=0
HYPOTHESIS_ONLY=5
INFRASTRUCTURE_BLOCKED>=3
```

因此不存在三个可直接运行的合法 carrier。其他 current 候选不能被拿来凑数：

- C01/C02/C05/C06 已被 conventional detector ceiling 与 non-positive lead-time
  限定；C03/C07 缺 action hook。
- C08/C10/C11 是当前局部负面或已完成 conventional variants；C12 的旧 GMI
  bound 是 metric confound；C14 只支持 scope-narrow initialization diagnostic。
- exact hybrid routing 的 legal FIR expert oracle headroom 只有 0.003693，具体
  contract 已关闭；F1 为 TESTBED_BLOCKED，F4 缺 coded chain。
- C15 明确 `NO_SECOND_SOURCE_PACKAGE`；B1/A4/B10/B9/B12 分别受第三
  evaluator repair、第二 identity/lifecycle repair、第三 Step 1、第二
  novelty/implementation repair 禁令约束。
- B6 的 source-native atan2/Z-ODPLL 已被直接源覆盖，没有正向 residual
  construct；B8 还缺完整 square-law/self-coherent optical chain 且场景/调制
  双重错位。

### 4. 为什么 C16-open 比至少两个替代项更可能最终产生 METHOD_SIGNAL

1. **相对 Q14**：C16-open 的问题入口是一个已由 current authority 明确确认的
   comparator capability mismatch——旧 spatial 2×2 HOS 不能对抗 11-tap 2×2
   FIR CMA，因此 equalizer-paradigm axis 合法 reopened。Q14 已经完成 5/5
   全文仍无法证明 residual information 存在，且有 blind-affine harmful 与
   low-headroom 负先验。C16 的下一门能直接回答“是否存在 task-matched 非模 FIR
   方法族与直接竞品”；Q14 下一门仍先回答“问题是否存在”。
2. **相对 B4**：C16 与当前 coherent dual-pol FIR receiver 的输入、输出、指标和
   runner 接口同域，公平 comparator 可直接定义为 tuned 11-tap CMA/MMA。B4
   的双环已由 source 拥有，剩余增量只有未证的 multi-rate scheduling，并且缺
   carrier-specific latency M-C-A 与 PADE/状态机实现。C16 少一个新接收链层级，
   更可逆，也更接近可运行的 method slice。
3. **相对 Q-ML4**：C16 不需把 30 m IM/DD 辐照度代理迁移为星地 coherent
   complex-field 符号级 DSP；它只需闭合算法身份、FIR capability 与 direct
   competitor。Q-ML4 同时承担场景、信号表示、输出和公平对手四类迁移债，方法
   形态虽强但更可能退化成“把已有网络换场景”。
4. **不预支方法产出**：上述比较只决定哪个上游门最值得关闭。T017 的
   `mission_method_delta` 冻结为 `NONE`；检索/下载/coverage PASS 仍不是方法
   信号。只有后续合法 Step 3/3.5/4a 与公平最小构造共同成立，才可能记
   `METHOD_SIGNAL`。

### 5. C16-open 正向方法合同（候选态）

```yaml
positive_method_target: >-
  source-backed full-complex 2x2 FIR non-modulus blind equalizer，匹配当前
  dual-pol temporal-memory receiver，不使用 TX truth、future window 或 oracle
  branch at runtime
minimal_construct: >-
  11-tap complex butterfly FIR HOS/joint-diagonalization（或 Step 3 确认的等价
  非模机制），与 tuned 11-tap CMA 和 MMA 使用相同样本、tap、warm-up 和更新预算
fair_comparator:
  - tuned 11-tap 2x2 butterfly CMA
  - tuned task-matched 11-tap 2x2 MMA
primary_packaging: >-
  时域能力对齐的非模高阶统计盲 FIR 均衡
fallback_packaging: >-
  若 standalone HOS 不适合动态跟踪，则只在 source 与 Step 4a 支持时评估
  HOS initialization/front-end + CMA/MMA tracking 的低复杂度级联
next_positive_action: >-
  先用一次 T017 闭合 Step 1–2 formal readiness；coverage confirmation、
  Step 3/3.5 与 Step 4a 通过前不实现 minimal construct
```

### 6. T017 的一次性边界

- action class：`CANDIDATE_FORMALIZATION`；formal active carrier 仍为 NONE。
- Step 1 必须使用至少三组不同角度查询和二轮 route-specific deep search，
  actual source family ≥3、unique ≥20、正式发表 ≥50%、必读 ≥5、覆盖至少
  `convolutional complex BSS/HOS FIR` 与
  `coherent-optical PM-QAM non-modulus blind equalization` 两条 route。
- Step 2 只选择 8–12 篇 priority pool，按 `gw-acquire.md` 三轮止损取得并检查
  ≥5 篇合法 `content.md`；必须核对 title/metadata/source identity。
- 形成 coverage-gap report 后停止。即使全文门通过，也停在
  `AWAITING_COVERAGE_CONFIRMATION`；未获用户极短 coverage 确认前不得 Step 3。
- 不运行旧 C16 sandbox，不复用 seeds 71–80，不写 Q#，不实现，不运行
  simulation/Probe/MVE，不更新 formal/current owner。
- source、identity、route coverage 或 fulltext 任一硬门失败即
  `BLOCKED_FORMAL_READINESS`，C16-open 返回池且不给第二个 source/
  formalization package。

## 结论

选择 **C16-open full-complex 2×2 FIR non-modulus blind equalizer** 获得一次
T017 Step 1–2 formalization workline，但不激活 scientific carrier。它不是因为
旧 HOS 结果“看起来互补”，而是因为 current authority 已确认旧比较器 task
mismatch，从而留下一个具体、可证伪、与当前 receiver 接口同域的能力对齐问题。
T017 只关闭 formal readiness 债，预期 method delta 为 NONE；失败立即轮换。

## 对决策的影响

- live 新建 D022，formal owner 新建 D033；
- foreground 递增至 epoch 42 / CP016 /
  `C16_FIR_HOS_FORMALIZATION_PREP`；
- formal active scientific carrier 保持 NONE；
- 新建 T017；独立 dispatch review PASS 前不执行；
- T017 接收后才追加 CP017，并独立记录 formal disposition、method delta、
  same-axis/repair/no-method streak 与 drift。
