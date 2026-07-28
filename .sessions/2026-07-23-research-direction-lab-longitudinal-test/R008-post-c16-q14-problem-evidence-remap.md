# [R008] Post-C16 Q14 problem-evidence carrier remap

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D023 / formal D034 / CP017

## 调研问题

T017 已按一次性退出边界把 C16-open 返回候选池，当前无 active scientific
carrier。在不运行实验、不修既有 source/evaluator package、也不把检索与
formalization 冒充方法产出的前提下，Q14、Q-ML4、B4 与 C04/C09-open 中哪个
候选最值得获得下一次有界工作包；该包为什么比至少两个替代项更可能最终产生
`METHOD_SIGNAL`？

## 发现

### 1. 当前合法边界

- foreground 为 epoch43 / CP017 / formal D034，只允许
  `PORTFOLIO_MAP`、`FORMAL_READINESS_REVIEW`、`CANDIDATE_FORMALIZATION`
  与任务准备。
- `portfolio/current.yaml` 明确
  `formal_active_carrier.id=NONE`；以下四项均不是 runnable carrier。
- current readiness census 仍为：

```text
READY=0
NEEDS_SMALL_ADAPTER=0
HYPOTHESIS_ONLY=4
```

- 本轮比较的是“哪个上游缺口最值得一次性关闭”，不是“哪个方法已经成立”。
  下一包的 `mission_method_delta` 固定为 `NONE`。

### 2. 四个机制级候选的六维比较

| candidate | 方法形态 | 预期增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **Q14：standard-CMA 后置 receiver-visible additive residual cascade（推荐）** | `z_out=z_CMA+gφ(z_CMA, causal CMA trace/context)`；runtime 禁止 TX truth、未来窗和 oracle branch；未来公平对手以 tuned CMA+DD-LMS/RDE 为主，blind affine 为辅助诊断 | T018 只完成强制 Step 3.5，并把四判据 2 从 UNKNOWN 裁为 PASS/FAIL/仍 UNKNOWN；固定 delta=`NONE`。只有 PASS 后的独立 Step 4a A0/A′/A/B 与后续 D MVE 才可能创建构造并公平比较 | “面向动态星地双偏振链路的在线 CMA 后置轻量残差校正，在保持盲跟踪与固定标签的同时补偿稳定、接收可见且传统级联未覆盖的剩余失真。”当前仅为候选包装 | **HYPOTHESIS_ONLY / MANDATORY_STEP3_5_MISSING**。S037/S038 已完成 5 篇全文与 Step 3；S039/D044 明确判据 1/3/4 PASS、2 UNKNOWN，且未执行 Q14 专属 Step 3.5，不得进入 A0/MVE | 一次 Step 3.5：3 个方法变体×场景/扩展词形成 ≥6 组合；actual Semantic Scholar + 至少一源；一篇核心竞品双向引用链；最多 3 轮收敛；新增高相关论文走 acquire/read；更新 Q14 综合分析。最后只按全文/abstract 证据裁决判据 2 | actual source、双向引用链、全文或 3 轮收敛任一失败即返回池；判据 2 仍 UNKNOWN、证据只依赖 TX truth/oracle/Kerr、或 simple DSP 已覆盖也立即轮换，不给第二个 Q14 problem-evidence package |
| **Q-ML4：coherent complex-field 双时间尺度代理与受约束反演** | 把 Gao 2025 的 CVAE 高频分支、residual BiLSTM 低频分支与 gate 从 IM/DD 辐照度代理重建为 strictly causal complex-field/symbol-level coherent proxy；cheap rule 为 AR/EMA 双时间尺度模型 | 下一包仍只能做 scene-transfer adjudication，delta=`NONE`；原文 79% BER 不得迁移计入 | “面向星地相干 FSO 多时间尺度湍流的双分支可微信道代理与受约束符号级反演补偿。” | **HYPOTHESIS_ONLY / SCENE_TRANSFER_BLOCKED**。原四判据只对约 30 m IM/DD、无 LO、辐照度级问题成立；coherent/star-ground 当前无 formal Q#、direct comparator 或实现 | 同时重建场景、复场输入、符号级输出、因果信息、direct coherent/star-ground competitor 与 cheap-rule comparator 六项合同 | complex-field 转译不守恒、只剩网络换场景、AR/EMA 覆盖或 direct competitor 占点即退出 |
| **B4：时延约束多速率 PADE+V–V 双环** | source-native 固定速率 PADE 粗频偏外环+V–V residual/phase 内环作 baseline；我方唯一可能增量是按 receiver hardware delay/parallelism 调度慢/快环更新率 | 下一包只可能 formalize carrier-specific M-C-A，delta=`NONE`；成功后仍需 PADE/双环基础实现 | “面向高并行星地相干接收的时延约束多速率双环载波恢复。” | **HYPOTHESIS_ONLY / MCA_BLOCKED**。源论文已拥有双环本身；现有时延证据来自 timing recovery 邻域，未证明载波双环固定更新率不足；仓库只有通用 DPLL/VV，无 PADE/双反馈状态机 | 闭合载波专属 latency 证据、合法 PADE 参数、direct multi-rate collision、comparator contract，再另建基础实现 | 全文/参数、载波专属 latency、residual novelty 任一失败即退出；禁止回到 PCS/Rs 或 D006 湍流环路旧轴 |
| **C04/C09-open：严格因果非仿射时序 residual corrector** | 在修复 self-referential target 后，用 receiver-visible 多 block history 预测非仿射 residual；必须先给出无常数解的 target 和 conditional-information contract | 下一包只能闭合 target/problem contract，delta=`NONE` | “面向动态盲均衡残差的严格因果时序校正。” | **HYPOTHESIS_ONLY / TARGET_CONTRACT_BLOCKED**。current portfolio 明确 C04 的 O1 target 有 input-independent zero-loss 解，C09 未在科学合法 target 上运行；F3 的 `+0.060 bits` 已撤回为 marginal-MI，不能当 conditional increment | 非退化 target 数学证明、receiver-visible conditional-information 证据、simple-DSP comparator 三项同时补齐 | target 仍有常数解、conditional information 不成立、或 simple DSP 覆盖即退出；不得先训练 GRU |

### 3. 为什么 Q14 比至少两个替代项更可能最终产生 METHOD_SIGNAL

1. **相对 Q-ML4**：Q14 已有 R009/S037/S038 的 Step 1–3 和 5/5 全文，方法
   接口、receiver-visible 边界以及 traditional comparator 候选均已落盘；缺口
   集中在一个强制 Step 3.5 和判据 2。Q-ML4 必须同时完成 IM/DD→coherent、
   irradiance→complex field、30 m→star-ground、proxy→symbol correction、
   comparator→task-matched 五重迁移，任一失败都会退化成“已有网络换场景”。
2. **相对 B4**：Q14 的 runnable receiver 接口、CMA output/trace、
   CMA+DD-LMS/RDE comparator 和 evaluation code 已存在。B4 连
   carrier-specific latency M-C-A 都未证，且 source 已拥有“双环”主体，仓库
   又没有 PADE/双反馈实现；它离 minimal construct 至少多出问题身份和基础实现
   两层债。
3. **相对 C04/C09-open**：Q14 的监督 residual 目标可以在未来使用独立训练流和
   receiver-only runtime，且 S038 已给出 L01/L04/L05 的相邻证据组合；
   C04/C09 当前目标本身有常数零损解，F3 temporal-information 证据又已撤回。
   先关闭 Q14 的外部证据缺口，比先发明一个无退化 target 更可逆、更可审查。
4. **不预支正面结论**：Q14 仍有 blind-affine harmful、hybrid-routing
   headroom=0.003693 和 P03 QPSK local-zero 等负先验。它们只提高 Step 3.5
   的证伪价值，不构成 family Kill。若 supplement 仍不能证明 receiver-visible
   residual 或 simple DSP 不足，Q14 当包退出。

### 4. Q14 候选正向方法合同

```yaml
positive_method_target: >-
  standard-CMA always-online 后的 strictly-causal receiver-visible additive
  residual corrector；只用 z_CMA 与冻结的 CMA trace/context，不使用 TX truth、
  future window、true channel/state 或 oracle branch at runtime
minimal_construct_after_future_gates: >-
  z_out=z_CMA+g_phi(z_CMA, causal trace/context)，带 no-op/identity gate；
  train/test stream 与 runtime information boundary 分离
fair_comparators:
  - tuned standard CMA
  - tuned CMA + DD-LMS 或 task-matched RDE cascade
  - receiver-visible blind affine / equally budgeted simple residual DSP
primary_packaging: >-
  动态星地双偏振链路中保留盲跟踪的轻量因果 residual correction
fallback_packaging: >-
  若增益只在特定 condition 存在，则形成低复杂度触发规则、适用边界与
  complexity/performance trade-off，而不夸大为通用 ML replacement
next_positive_action: >-
  先完成一次 T018 Groundwork Step 3.5；只有判据 2 获得外部问题证据并由
  独立 verifier/主控接收后，下一包才可进入 Step 4a A0/A'/A/B
```

### 5. T018 一次性边界

- action class 为 `CANDIDATE_FORMALIZATION`；formal active carrier 仍为
  `NONE`，T018 不是实验包。
- 严格执行 `gw-supplement.md`：≥6 关键词矩阵组合；actual Semantic Scholar
  + 至少一源；一个核心竞品的 forward/backward citation chain；最多 3 轮；
  新高相关论文走合法 acquire/read；最后一轮新增必读/建议读=0。
- 只用论文全文、abstract 与可核验 metadata 裁决判据 2；不得用本地实验、
  oracle gap、标题空白或“未发现直接论文”反向证明方法成立。
- 任一 coverage/fulltext/convergence 门失败，或判据 2 仍 UNKNOWN/FAIL，
  Q14 返回池且不给第二个 problem-evidence package；按顺序轮换 Q-ML4、B4、
  C04/C09-open。
- 即使得到 `PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO`，本包 delta 仍为
  `NONE`，且 Step 4a 必须由新 owner/新任务与独立审查另行授权。

## 结论

选择 Q14 获得一次 T018 Groundwork Step 3.5/problem-evidence workline，但不激活
scientific carrier。选择依据不是 residual 结果看起来正面，而是它相对
Q-ML4、B4 与 C04/C09-open 拥有最短且单一的 formal debt：Step 1–3、5 篇全文、
receiver 接口和传统 comparator 已存在，下一包能直接证伪“是否有可复用方法
产出”这一剩余判据。失败立即轮换，不运行实验。

## 对决策的影响

- live 新建 D024，formal owner 新建 D035；
- foreground 递增至 epoch44 / CP017 /
  `Q14_STEP35_PROBLEM_EVIDENCE_PREP`；
- formal active scientific carrier 保持 `NONE`；
- 新建 T018；独立 dispatch review PASS 前不执行；
- T018 最终接收后才追加 CP018，并独立记录 formal disposition、method delta、
  same-axis/repair/no-method streak 与 drift。
