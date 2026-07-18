# [R013] 真实 selected complex-output mux 路线评估

> 2026-07-15 | 关联：专题 `2026-07-14-ccisp-content-expansion` / D014 / D015 / V010 / R011
> 授权：DIAGNOSE + PROPOSE；只读；禁止修改代码/论文/图/Skill/参数/数据/JSON；禁止运行仿真
> 独立核验：本轮通过 Read 独立核验 4 项关键事实，未照抄 R011

## 调研问题

T015 列出的 5 个问题：(1) 当前 error-count mux 的真实实现；(2) 实现 selected complex-output mux 能带来什么；(3) post-hoc mux、先选后跑 receiver、non-genie 在线算法三者的区别；(4) 需要改哪些接口、解决哪些相位模糊问题、重验哪些结果；(5) 哪一层才能真正支撑 adaptive CPR algorithm 定位。

---

## 发现

### 0. 当前真相表（独立核验，exact file:line）

本节独立核验 R011 结论。R011 的逻辑判断与当前权威文件一致；行号因 common-768 扩展版（`_a4_switch_common768_30seed.py`）新增 `ne_nda_common768` 变量有漂移（R011 记 :325-342，当前 :329-342），以当前文件为准。

#### 核验事实 1：DA/NDA recovery 实际返回哪些对象

| 函数 | 返回对象 | 复数输出 | 相位估计 | exact file:line |
|---|---|---|---|---|
| `da_ml_recovery` | `(rx_comp, phi_est, df_est)` | `rx_comp` = carrier-corrected 复数序列（256 样本） | `phi_est`（标量截距）, `df_est`（标量频偏） | `_recovery.py:136-168`（返回在 :167-168） |
| `nda_ml_recovery` (assume_df_zero=True 分支) | `(rx_comp, tau_est, phi_est, df_est)` | `rx_comp` = derotated 复数序列（256 样本） | `phi_est`（整块 mean-angle / 或 segK8 插值轨迹） | `_recovery.py:206-237`（返回在 :237） |

**结论**：两路 recovery **确实**各自返回 carrier-corrected 复数序列 + 相位估计。复数输出和相位估计在 callee 层**真实存在**。R011:13 PASS 与当前一致。

#### 核验事实 2：权威 caller（common-768）实际 mux 的对象

caller = `_a4_switch_common768_30seed.py:per_block()`（:110-139），被主循环 `main()` 的 block 循环调用（:321-342）。

调用链（caller → callee → returned object → use site）：

```
main() block loop (:321-342)
  ├─ estimate_h_blind_perblock / mmse_equalize / amp_limit → rxb (:325-326)  [均衡]
  ├─ estimate_h_pilot_perblock / mmse_equalize / amp_limit → rxp (:327-328) [均衡]
  ├─ per_block(rxb, rxp, bits, txs) (:329)
  │    ├─ fft_foe_m0_omega(rx_blind) → omega (:120)
  │    ├─ nda_ml_recovery(rx_blind*exp(-jωk)) → rc_nda, _, _, _  (:122-123)
  │    │      ★ phi_est 被 _ 丢弃；只保留 rc_nda（复数序列）
  │    ├─ da_ml_recovery(rx_pilot) → rc_da, _, _ (:125-126)
  │    │      ★ phi_est 被 _ 丢弃；只保留 rc_da（复数序列）
  │    ├─ resolve_m16apsk_blockwise(rc_nda, tb) → res_nda (:128)  [NDA 八重模糊消解，读 tx_bits]
  │    ├─ m16apsk_demod(res_nda) → dm_nda (:129)
  │    ├─ m16apsk_demod(rc_da) → dm (:131)
  │    ├─ ne_nda = sum(tb != dm_nda)         — 全 1024 bit 错误数 (:130)
  │    ├─ ne_da = sum(tba[is_d] != dma[is_d]) — 768 bit 错误数 (:136)
  │    └─ ne_nda_common768 = sum(tba[is_d] != dma_nda[is_d]) (:138)
  │    return ne_nda, ne_da, ne_nda_common768 (:139)  ★ 只返回 3 个整数
  ├─ decide(rx_raw, gdb, gl) → 'da'/'nda' (:334)
  │      ★ decide 只读 rx_raw 功率统计 + nominal SNR（:97-107）
  └─ if 'da': e_s_c768 += ne_d        (:337-338)
     else:    e_s_c768 += ne_n_c768   (:340-342)
            ★ selector 只累加错误计数，无 selected_phi / selected complex output
```

**关键事实（独立确认）**：
- **两路 recovery 在 selector 之前全部执行**（:329 先 per_block，:334 后 decide）。R011:16 与当前一致。
- **`phi_est` 两处均由 `_` 丢弃**（:122-123 的 `_, _, _`；:125-126 的 `_, _`）。无 `selected_phi`。R011:15 与当前一致。
- **`per_block()` 只返回 3 个整数错误计数**（:139）。复数序列 `rc_nda`/`rc_da` 在 per_block 作用域内即被解调丢弃，不向上传递。R011:15 与当前一致。
- **selector（decide）只读 `rx_raw` 功率 + nominal SNR**（:97-107），与错误计数、tx_bits、branch output **数据无关**。R011:25 "decision 在数据依赖上可先于两路恢复" PASS 与当前一致——**判据本身不依赖 branch output，但当前程序结构上先跑两路后判**。
- **mux 对象 = 错误计数**（`e_s_c768 += ne_d / ne_n_c768`，:337-342），**不是复数序列、不是 bits、不是相位**。R011:27 "selector 实际 mux 相位/复数 BLOCKED" 与当前一致。

#### 核验事实 3：NDA 八重相位模糊如何处理，是否读 tx_bits，发生在何处

`resolve_m16apsk_blockwise(rc_nda, tb, block_size=256)`（:128），定义在 `_modulation.py:278-310`：
- 对每 256-sample block，试 8 个 `2π/8` 旋转，用**该 block 的 tx_bits** 选最低 BER 旋转（:304-308）。
- **读取 tx_bits**：`tb = bits[:P.N_DFT*P.BITS_PER_SYM]`（per_block :127），传入 resolve（:128）。
- **发生时点**：在 per_block 内部（:128），即**在 selector decide(:334) 之前**。resolve 发生在 NDA demod 之前，产生 `res_nda`，再 demod 得 `dm_nda`。

**相位模糊消解的时序**：均衡(:325-328) → per_block[:120-139 含 resolve] → decide(:334) → mux 错误计数(:335-342)。NDA 的八重模糊在选路**之前**就靠 tx_bits 消解了。

R011:14 / V010 "NDA ambiguity resolution selects among eight rotations using true tx_bits" 与当前一致（`_modulation.py:278-310`，caller `:128`）。

#### 核验事实 4：Fig.2 与 method.tex 当前声称强于实现的哪一层

**Fig.2（draw.io `fig2_adaptive_cpr.drawio`）当前语义**：
- `e_theta_da`（:117）：DA estimator → selector，边标签 `\hat{\theta}_{DA}`（:127）
- `e_theta_nda`（:124）：NDA estimator → selector，边标签 `\hat{\theta}_{NDA}`（:130）
- `e_selected`（:133）：selector → Phase compensation，边标签 `Selected \hat{\theta}`（:140）
- `phase`（:58）：Phase compensation 节点
- `e_raw`（:91）：raw r_k → Phase compensation（carrier-corrected 在此生成）
- `e_phase_down`（:94）：Phase compensation → Common downstream DSP（:67）
- `e_branch_selector`（:173）：Branch command → selector（控制路径）

Fig.2 画出的信息流：**两路相位估计进入 selector → 选出 Selected θ̂ → Phase compensation（用 Selected θ̂ 对 raw r_k 做相位补偿）→ Common downstream DSP**。这明确声称：(a) selector mux 的是**相位估计**（θ_DA/θ_NDA），(b) 存在**单一的 Selected θ̂**，(c) 存在**统一的 Phase compensation + Common downstream DSP**。

**method.tex 当前声称**：
- :4 "After selection, the DA path uses pilot-derived channel information, whereas the NDA path uses a received-power-based channel estimate. Figure~2 summarizes the parallel carrier-recovery branches and the two-stage control path" —— 描述了两路并行 + 控制路径，较中性。
- :25（DA 段）"This makes the DA output a carrier-corrected complex sequence with the same length and sample timing as the input window, **which allows the downstream demodulator to use the same interface for either selected branch**." —— **声称存在统一 downstream interface，且 selected branch 通过它**。这是实现真实性缺口的核心声称句。
- :39（NDA 段）"this eightfold phase ambiguity is resolved separately in each processing window by testing the eight constellation rotations against the transmitted bit labels...This transmitted-bit-assisted step is an ambiguity-resolved evaluation protocol: it is not an online input to the NDA phase statistic or to the selector." —— **已披露 tx_bits 辅助评估、非在线输入**。这一声称与实现一致（PASS）。
- :83 "the selected branch supplies the carrier-corrected samples to the subsequent demodulator. The implementation consequently realizes the sequence..." —— **声称 selected branch 供应 carrier-corrected samples 给 demodulator**。这是实现缺口（当前是错误计数 mux，不是 samples mux）。

**Fig.2 强于实现的层**：画出 `Selected θ̂ → Phase compensation → Common downstream DSP`，而实现中无 selected phase、无统一 phase compensation、无 common downstream（两路各自在 per_block 内解调）。
**method.tex 强于实现的层**：:25 和 :83 声称 "selected branch supplies carrier-corrected samples to downstream demodulator via same interface"，而实现中 selected 的对象是错误计数，复数序列在 per_block 内即被丢弃。

**论文声称—实现闭合度小结**：
| 声称层 | 实现是否支持 | 证据 |
|---|---|---|
| 两路各自产生复数序列 | ✅ PASS | `_recovery.py:167-168,237` |
| 两路各自产生相位估计 | ✅ PASS | `_recovery.py:167,237` |
| selector 判据只用 raw power + nominal SNR | ✅ PASS | `_a4...py:97-107` |
| NDA tx_bits 辅助消解（已披露非在线） | ✅ PASS（已披露） | `_a4...py:128`, `_modulation.py:278-310`, method.tex:39 |
| selector mux 两路相位估计 | ❌ FAIL | `_a4...py:122-126` 丢弃 phi_est |
| 存在单一 Selected θ̂ | ❌ FAIL | 无 selected_phi 变量 |
| 存在统一 Phase compensation + Common downstream | ❌ FAIL | per_block 内各自解调，无 common downstream |
| selected branch 供应 carrier-corrected samples 给 demodulator | ❌ FAIL | selected 的是错误计数 |

---

### 1. 三层定义与边界（A/B/C 严格分开）

> T015 要求 post-hoc mux、先选后跑 receiver、non-genie 在线算法三者必须分开，不得混称。

#### A. 指标等价的 post-hoc complex-output mux

**定义**：
- 两个 CPR 分支照常**全部运行**（不改变当前两路先算的结构）；
- selector 仍按当前窗口判决（raw power + nominal SNR，`decide()` 不变）；
- 与当前唯一区别：在**统一 demod 之前**选择已恢复的复数序列（即把 `rc_da` 或 `rc_nda[res_nda]` 之一向上传递为 `selected_rx`），而不是先各自 demod 再 mux 错误计数；
- 仍可沿用当前仅供离线 BER 评估的 `tx_bits` 消歧（NDA 八重模糊消解逻辑不变）。

**性质**：这是**表达/接口层的修复**，把"selected 对象从错误计数提升为复数序列"。它让 Fig.2 的 `Selected θ̂ → Phase compensation` 和 method.tex:25/:83 的 "selected branch supplies carrier-corrected samples" 在**对象层面**成立。

**为什么通常不改变 common-768 BER**：当前 error-count mux 与 post-hoc complex-output mux 在以下 7 个严格条件下**数值 bit-exact 等价**（确定性 hard demod + 同一消歧规则 + 同一 common-768 mask + 整窗二选一 + selector 与 branch output/tx_bits 无关 + downstream 仅同一确定性硬判 + 指标只对逐窗错误数求和）：
- 当前 `per_block` 对 NDA 先 resolve（:128）再 demod（:129）得 `dm_nda`，对 DA 直接 demod（:131）得 `dm`；error-count mux 选的是 `ne_d`（DA 的 demod 结果）或 `ne_n_c768`（NDA demod 在 common-768 位上的错误数）。
- post-hoc complex-output mux 若把 `rc_da` 或 `res_nda` 之一选出，再统一 demod，由于 demod 是确定性算子（`m16apsk_demod`，`_modulation.py:222-258`），**对同一复数序列的 demod 结果不变**。
- 因此 selector 选 DA 窗时，无论"先 demod DA 再取 ne_d"还是"先选 rc_da 再统一 demod 再算 ne_d"，ne_d 相同；NDA 窗同理。
- **结论**：A 的默认预测是 common-768 BER **零不一致**（bit-exact），不是增益。任何 BER 改善或不一致优先视为实现错误/消歧时点变化/指标变化/对齐错误。

**不节省分支计算**：A 仍两路全跑（:329 per_block 两路都算），只是 mux 对象从计数变成序列。**禁止把 A 写成计算量降低**。

**不含**：在线可部署性（仍依赖 tx_bits 消歧）；EVM/LLR/FEC 等价（hard-BER 等价不得外推）；算法贡献（只是接口闭环）。

#### B. 功能性 branch-routed adaptive CPR receiver

**定义**：
- 控制器**先决定分支**（decide() 提前到两路 recovery 之前）；
- 每个窗口**只执行被选 CPR 分支**，并输出统一复数序列；
- 需明确：control feature（当前是 raw power + nominal SNR，已满足"选路前可得"）、判决时点（提前到均衡前）、状态重置（湍流每窗重启相位 realization，当前 `_channel.py` 每窗 new seed，已满足）、均衡输入（blind h vs pilot h，当前两路用不同 h，:325-328，需约定选 DA 时用 pilot h、选 NDA 时用 blind h）、分支状态（无跨窗状态，每窗独立）、downstream demod 接口（统一 m16apsk_demod）；
- 离线评估可暂时保留 genie-aided ambiguity resolution（NDA 仍用 tx_bits 消歧），但**必须显式标注不可部署边界**。

**性质**：这是**功能性的 receiver 架构**——真正"先选后跑"。它让 Fig.2 的 `Selected θ̂ → Phase compensation → Common downstream DSP` 在**控制流层面**成立（控制器决定跑哪条路），且**可能降低分支计算**（每窗只跑一条路，省 50% branch compute）。

**比 A 更能支撑 adaptive CPR 身份的原因**：A 只修复"selected 对象是复数序列"，但两路仍全跑、选路仍在处理后——这只是后处理 mux，控制器没有真正"路由"计算资源。B 让控制器**真正先决策、再执行单一分支**，这是 adaptive CPR scheme/method 作为"复合处理链"的**控制论实质**（D014 的 two-stage selection 作为"核心内部控制机制"才真正成立）。

**B 与 A 等价的前提**（预注册）：
- decide() 判据数据独立于 branch output（已满足，:97-107 只读 raw power）；
- 把 decide() 从 :334 提前到 :329 之前，**不改变 decide 的输入**（rx_raw 在 :324 已得，gdb/gl 在 :316-317 已得）；
- 选 DA 时执行 DA 路（pilot h + da_ml_recovery + demod），选 NDA 时执行 NDA 路（blind h + nda_ml_recovery + resolve + demod）；
- 由于 demod 确定性，每窗只跑被选分支的 demod 结果 = 当前两路全跑后取该分支的 demod 结果。
- **结论**：在上述前提下，B 的逐窗错误计数应与 A **bit-exact 等价**。若控制输入依赖尚未执行的分支输出，则"先选后跑"不可直接成立——但当前 decide() 不依赖 branch output，故前提满足。

**不含**：在线可部署性（仍依赖 tx_bits 消歧 NDA 模糊）；但比 A 多了"真正先选后跑 + 可能省计算"的 receiver 功能。

#### C. 可部署的 online adaptive CPR algorithm

**定义**：
- 分支选择与相位模糊消解都**不读取发送比特**；
- 需要一个 **online ambiguity resolver**（不依赖 tx_bits 的 NDA 八重模糊消解），或 differential / coded-aid / state mechanism；
- 这是**新增算法组件**，不是实现修复。

**为什么可能超出当前投稿修复范围**：
- 当前 NDA 的八重模糊完全依赖 tx_bits（`_modulation.py:278-310`，resolve_m16apsk_blockwise 每 block 试 8 旋转用 tx_bits 选最低 BER）。`_modulation.py:168` 注释已标注"纯盲 NDA 可改用每块硬判决众数投票（本轮先用 tx_bits 版本）"——这是**已知的未实现项**。
- 闭合 non-genie ambiguity resolver 是一个**独立的研究问题**（需设计盲旋转选择算法、验证其 BER 性能、对比 tx_bits oracle 的损失），涉及新方法、新实验、新 baseline。
- 按 FR-22，这构成**新算法 scope**，需走 Groundwork/Contract，不是 implementation repair。

**最小研究问题（不凭空指定方案）**：
1. 盲旋转选择：能否用每块硬判决结果的某种一致性度量（如重调制误差、星座旋转自洽性）替代 tx_bits 选最低 BER？需验证在中低 SNR / strong 湍流下是否退化。
2. 差分编码：是否引入差分编码消除模糊？需评估带宽/复杂度代价，且改变调制方案。
3. 编码辅助：能否用 FEC 译码反馈消解模糊？需引入译码器-同步器联合迭代，超出当前 receiver 架构。
4. 跨窗状态：能否用上一窗的相位估计约束本窗模糊？需定义状态传递机制，但当前湍流每窗重启 realization（`_channel.py`，topic-index 不变量"每 256 点重启"），跨窗相位不连续。

**不含**：任何未经上述研究问题闭合就声称的"可部署""在线""non-genie"。

---

### 2. 效果矩阵

> T015 必答问题 2-3：A/B/C 各自能新增哪些可证明能力；哪些只是表达/接口闭环，哪些是算法能力，哪些必须靠新结果证明。

| 能力维度 | 现状（error-count mux） | A：post-hoc complex-output mux | B：branch-routed receiver | C：non-genie online algorithm |
|---|---|---|---|---|
| **论文定位与 Fig.2 真实性** | FAIL（D015）：Fig.2 画 selected phase，实现是 error-count mux；method.tex:25/:83 声称 selected samples 给 downstream | **修复"selected 对象"层**：selected 复数序列真实存在，Fig.2 的 Selected θ̂→Phase comp 在对象层成立。但两路仍全跑，selector 仍在处理后，"控制器路由"语义仍弱 | **修复"控制流"层**：控制器真正先选后跑，Fig.2 的 Branch command→selector→单路执行在控制流层成立。最接近 D014 的 two-stage control 实质 | **修复"可部署"层**：完整闭合，但属新算法 scope |
| **BER（common-768 hard-BER）** | 当前权威数字（V009 PASS） | **默认预测：零不一致（bit-exact）**。不增益 | 在等价前提下：与 A bit-exact 等价（decide 数据独立） | 需新结果：盲消歧有 BER 损失待测 |
| **计算量** | 两路全跑 | **不节省**（仍两路全跑，只改 mux 对象） | **可能省 ~50% branch compute**（每窗只跑一条路）——但需实测确认 blind/pilot h 估计本身的开销占比 | 与 B 同（先选后跑），加盲消歧开销 |
| **EVM / LLR / FEC / burst / sequence-level analysis** | 不支持（只存错误计数） | **解锁**：selected 复数序列可算 EVM、可喂 soft-demod 得 LLR、可接 FEC、可做突发/序列级分析——这是 A 相对现状的**真实新增能力** | 同 A（selected 序列存在）+ 先选后跑 | 同 B + non-genie |
| **在线可部署性** | BLOCKED（tx_bits 消歧） | 仍 BLOCKED（保留 tx_bits 消歧） | 仍 BLOCKED（离线评估保留 genie-aided，须标注） | **PASS**（不读 tx_bits）——但需新算法+新验证 |
| **对 adaptive CPR 定位的支撑强度** | 不足以支撑 D014（D015 BLOCKED） | **部分支撑**：让 Fig.2/method "selected output" 在对象层真实，但 two-stage control 仍是后处理 mux，导师"估计算法"可能仍不满足 | **较强支撑**：two-stage control 成为真正的控制机制（先选后跑），最接近 D014 的 scheme/method 身份 | **完整支撑**：可部署 adaptive CPR algorithm，但属新研究 |
| **能力性质** | — | **表达/接口闭环**（审计性修复） | **receiver 功能**（架构层）+ 可能的计算节省 | **算法能力**（新方法） |

**关键区分**：
- A 的收益**几乎全是表达/接口闭环**（Fig.2 真实性 + method.tex 闭合 + 解锁 EVM/LLR 等下游指标），**不改变 BER、不省计算、不增可部署性**。
- B 在 A 基础上新增**receiver 功能**（先选后跑）和**可能的计算节省**，更接近 adaptive CPR 的控制论实质。
- C 才是**算法能力**，但需新研究，超出投稿修复。

---

### 3. 分路线实现 delta（文件/函数/接口级，不写代码）

> T015 必答问题 4：每条路线涉及哪些 exact files/functions/interfaces。

#### A 的 delta

| 文件 | 函数/位置 | delta（描述，不写代码） |
|---|---|---|
| `_a4_switch_common768_30seed.py` | `per_block()` (:110-139) | 返回值从 `(ne_nda, ne_da, ne_nda_common768)` 改为增加返回 selected 复数序列（如 `rc_da` 或 `res_nda` 之一，由后续 decide 决定）。但 decide 在 per_block 之后，故需把 decide 移入 per_block 或返回两路序列让主循环选。最小 delta：返回两路 carrier-corrected 序列 `(rc_da, res_nda)` + 3 个错误计数，主循环按 decide 选其一为 `selected_rx`。 |
| 同上 | `main()` block loop (:321-342) | 新增 `selected_rx = rc_da if c=='da' else res_nda`；可选地把 selected_rx 存入 per-seed 记录（供 EVM/LLR 计算）。错误计数逻辑不变（等价性保证）。 |
| 接口变更 | per_block 返回签名 | 从 `Tuple[int,int,int]` → `Tuple[int,int,int,np.ndarray,np.ndarray]`（3 计数 + 2 序列）。主循环消费方式变化。 |
| 论文 | method.tex:25,83 / Fig.2 | selected 复数序列真实存在后，:25/:83 的 "selected branch supplies carrier-corrected samples" 在对象层成立。Fig.2 的 Selected θ̂→Phase comp 可保留（或微调标注为 selected complex output）。**但两路仍全跑、selector 仍在处理后，Fig.2 的"控制器路由"语义仍需标注或收窄。** |

**A 不改**：`decide()`（:97-107）、`_recovery.py`、`_modulation.py`（resolve 逻辑）、信道参数、seed、窗口数、common-768 mask。

#### B 的 delta（在 A 基础上）

| 文件 | 函数/位置 | delta |
|---|---|---|
| `_a4_switch_common768_30seed.py` | `main()` block loop (:321-342) | 把 `decide(rx_raw, gdb, gl)` 从 :334（per_block 之后）**提前到 :329 之前**（per_block 之前）。先 decide，再按决定只执行被选分支。 |
| 同上 | block loop 结构 | 重构为 `c = decide(...)` → `if c=='da': 只跑 pilot h + da_ml_recovery + demod` / `else: 只跑 blind h + nda_ml_recovery + resolve + demod`。省去另一路的均衡+recovery+demod。 |
| 同上 | `per_block()` | 拆分为 `per_block_da(rx_pilot, bits, txs)` 和 `per_block_nda(rx_blind, bits)`，或在 per_block 内按 decide 分支只算一路。 |
| 等价性验证 | 新增断言 | 需新增验证：B 的逐窗 ne_d/ne_n_c768 与 A（两路全跑）bit-exact 一致。 |
| 论文 | method.tex / Fig.2 | 可声称"控制器先决策、每窗只执行被选分支"，Fig.2 的 Branch command→selector→单路执行成立。**计算节省可声称（须实测）。** 仍须标注 NDA genie-aided 消歧不可部署。 |

**B 改**：主循环控制流顺序、per_block 结构。**B 不改**：decide 判据、recovery/demod/resolve 逻辑、信道参数。

#### C 的 delta（在 B 基础上）

| 文件 | 函数/位置 | delta |
|---|---|---|
| `_modulation.py` | `resolve_m16apsk_blockwise` (:278-310) | 新增**盲旋转选择**版本（不读 tx_bits），如硬判决众数投票 / 重调制误差最小化。`_modulation.py:168` 注释已预留此扩展点。 |
| `_a4_switch_common768_30seed.py` | per_block_nda | 盲消歧替换 tx_bits 消歧。需新参数控制 online/offline 模式。 |
| 新 baseline / 新实验 | — | 盲消歧 vs tx_bits oracle 的 BER 损失；跨 SNR/湍流场景验证。**这触发 Groundwork/Contract（FR-22）。** |
| 论文 | 全文 | 可声称"可部署 online adaptive CPR algorithm"。但属新贡献，需新结果支撑。 |

---

### 4. Ambiguity-resolution 决策树

> T015 要求明确消歧边界。

```
问：NDA 八重相位模糊如何消解？
│
├─ 当前实现（A/B 共用，离线评估）
│    resolve_m16apsk_blockwise(rc_nda, tb, block_size=256)
│    每 block 试 8 旋转，用 tx_bits 选最低 BER
│    → genie-aided（读发送比特）
│    → 仅支持离线 BER 评估，不支持在线输出
│    证据: _modulation.py:278-310, _a4...py:128
│
├─ A（post-hoc mux）
│    消歧逻辑不变（仍 tx_bits），只是 mux 对象从计数变序列
│    → 仍 genie-aided，仍不可部署
│    → 但 selected 复数序列是消歧后的（res_nda），非 raw
│
├─ B（branch-routed receiver）
│    消歧逻辑不变（仍 tx_bits），但只在选 NDA 时执行
│    → 仍 genie-aided，离线评估保留，须显式标注不可部署
│
└─ C（non-genie online）
     需盲消歧（不读 tx_bits）
     → 待研究问题：盲旋转选择 / 差分 / 编码辅助 / 跨窗状态
     → 未闭合前 deployable selected output = BLOCKED
     → 不得用 post-hoc tx_bits 结果代替
```

**负例（T015 要求列出）**：
- 未经消歧的 NDA raw complex output（`rc_nda` 未经 resolve）**不应**被错误要求与已消歧 BER 完全等价——raw 有八重模糊，BER 灾难性高（`_modulation.py:282-283` 注释"全局单旋转无法同时解所有块模糊 → BER 灾难"）。
- hard-BER 等价（A 的默认预测）**不得外推**为 EVM/LLR/FEC 等价——EVM/LLR/FEC 是 soft/序列级指标，hard-BER bit-exact 不蕴含它们等价（虽然 A 解锁了计算它们的**能力**，但具体数值需新计算）。

---

### 5. 预注册验证计划、PASS/BLOCKED 标准与反例

> T015 要求可执行、可否决、不过拟合的验证合同。

#### A 的预注册验证

**预测**：在现有 common-768 全部权威 case/seed/window（V009 的 33 点 × 30 seed × 400 window）上，selected complex sequence 经同一 ambiguity resolution（tx_bits）与同一 hard demod 后的逐窗 errors，与当前 error-count mux **零不一致**；selector counts（n_select_da/n_select_nda）和两条 fixed-branch 结果（ne_da, ne_n_c768）保持不变。

**PASS 标准**：
- 逐窗 ne_da、ne_n_c768、e_s_c768 与当前权威 JSON（`_a4_switch_common768_30seed_snr5_25_step2.json`）bit-exact 一致；
- n_select_da + n_select_nda = n_windows（400）不变；
- paper_summary 的 mean_gain_db / ci95 与 V009 复算值一致（容差 1e-12，对齐 `validate_authoritative_result` :238-239）；
- selected_rx 数组成功提取（shape = (256,) complex），DA 窗 = rc_da，NDA 窗 = res_nda。

**BLOCKED / 反例**：
- 若出现 BER 改善 → 优先视为实现错误（消歧时点变化 / 指标变化 / 对齐错误），**不能写成算法增益**。
- 若 selector counts 变化 → decide 提前导致输入变化（违反"decide 数据独立"前提），BLOCKED，查 decide 输入。
- 若逐窗 ne 不一致 → demod 非确定性 or mask 错位，BLOCKED。
- 若有人把 hard-BER bit-exact 外推为"EVM/LLR 也等价"→ 反例：EVM/LLR 需单独计算，hard-BER 等价不蕴含。

**运行成本**：A 需改 per_block 返回 + 主循环 selected_rx 提取，重跑 33 点 × 30 seed × 400 window（与 V009 同量级，约 V009 的 elapsed_sec 量级）。**属"重跑现有网格"，不改算法/判据/参数/场景**，但**超出当前专题"不运行新仿真"不变量**——需用户批准 scope change（见 §7）。

#### B 的预注册验证

**预测**：在 A 等价前提满足下（decide 数据独立、每窗只跑被选分支、demod 确定性），B 的逐窗错误计数与 A **bit-exact 等价**。

**PASS 标准**：
- B 的 ne_da/ne_n_c768/e_s_c768/n_select 与 A bit-exact 一致；
- B 的 selected_rx 与 A 的 selected_rx bit-exact 一致；
- 计时：B 的 per-window branch compute < A 的 per-window branch compute（只跑一路 vs 两路）。

**BLOCKED / 反例**：
- 若 B 与 A 不等价 → decide 提前改变了 per_block 的副作用（如 blind h / pilot h 估计有随机性？需核查 `estimate_h_blind_perblock` / `estimate_h_pilot_perblock` 是否确定性），BLOCKED。
- 若控制输入依赖尚未执行的分支输出 → "先选后跑"不可直接成立（但当前 decide 不依赖，故不应触发）。

#### C 的预注册验证

**预测**：未闭合 non-genie ambiguity resolver 前，**deployable selected output = BLOCKED**。

**PASS 标准**（闭合后）：
- 盲消歧 NDA BER vs tx_bits oracle NDA BER 的损失量化（跨 SNR/湍流）；
- 盲消歧 selector common-768 gain 与 oracle 消歧版的差异；
- 新 baseline（如纯 VV/BPS 盲 CPR）对比。

**BLOCKED**：不得用 post-hoc tx_bits 结果代替 non-genie 结果声称可部署。

**所有路线共同约束**：没有 fresh rerun 与独立 verifier 前，禁止形成新的数字或性能声称。

---

### 6. 范围、证据、工期/运行成本风险

#### 当前任务属于 implementation repair 还是 new algorithm scope？

| 路线 | 性质 | 触发门控 |
|---|---|---|
| A | **implementation repair**（接口/表达闭环） | session-governance scope change（因需重跑网格，超出"不运行新仿真"）；**不触发** Groundwork/Contract（不改算法、不加新方法）；sim-preflight 适用于重跑验证 |
| B | **implementation repair + receiver 架构调整**（控制流重构，不改算法逻辑） | 同 A 的 scope change；sim-preflight；需等价性验证；**不触发** Groundwork/Contract（decide/recovery/demod 逻辑不变，只是执行顺序+范围） |
| C | **new algorithm scope**（新增盲消歧方法） | **触发 Groundwork/Contract（FR-22）**：新方法、新 baseline、新实验；sim-preflight；session-governance 新专题或大 scope change |

#### 工期/运行成本（只报可从项目事实量化的）

- A 重跑成本：与 V009 同量级（33 点 × 30 seed × 400 window）。V009 的 elapsed_sec 记录在 JSON provenance 中（`_a4...py:482`），具体数值需读 JSON meta——本轮不读 JSON 内容（只读路径确认），**不编数字**。量级估计：与 D013 的 990 seed-point 运行同阶。
- B 重跑成本：与 A 同量级（同样网格），但每窗只跑一路，理论 branch compute ~50%——但 h 估计、信道生成等开销不变，实际 wall-clock 节省需实测，**不编比例**。
- C 成本：**无法从项目事实量化**（需先研究盲消歧方法，研究工期未知），标 BLOCKED。

#### 证据风险

- A/B 的等价性论证基于"demod 确定性 + decide 数据独立"——这两个前提已在代码中确认（`m16apsk_demod` 无随机性；`decide` :97-107 只读 rx_raw/gdb/gl）。但 B 把 decide 提前后，需确认 `estimate_h_blind_perblock`/`estimate_h_pilot_perblock` 是否确定性（本轮未深入读这两个函数，**标为待验**）。
- Fig.2/method.tex 的声称层已核验（§0 核验事实 4），但 Fig.2 的最终视觉碰撞（R010 记录的三处尺寸碰撞）与本轮无关。

---

### 7. 三档建议（保守 / 推荐 / 激进）

> T015 必答问题 5-7。在 7 页且用户要求精炼的背景下，评估叙事收益 vs 新增解释/验证成本。

#### 保守档：收窄为 branch-decision + post-hoc selected-BER evaluation（不改代码）

**内容**：不实现 selected complex-output mux。把 Fig.2 和 method.tex 的声称**收窄**：Fig.2 删除/改 `Selected θ̂ → Phase compensation` 链路，改为"两路并行 recovery + branch decision（error-count level）+ post-hoc selected-BER evaluation"；method.tex:25/:83 收窄 "selected branch supplies carrier-corrected samples" 为 "selected branch's error count is accumulated"。

- **为什么**：零代码改动、零重跑、零新仿真。事实完全可支持（D015 已确认 error-count mux 是真相）。满足"不编造"。
- **为什么不选（代价）**：Fig.2 需重做语义 brief（不是局部挪字，D015 已否决 R010 局部修）；method.tex 的 adaptive CPR 叙事削弱——导师"应该是估计算法"（voice.md）**可能不满足**，因为 branch-decision + post-hoc BER 评估更像"评估方法"而非"估计算法"。D014 的 scheme/method 定位在保守档下**支撑不足**。
- **叙事收益**：低。省了实现成本，但丢了 adaptive CPR 定位的实现支撑。

#### 推荐档：实现 A（post-hoc complex-output mux）+ 收窄 Fig.2/method 为"selected complex output 真实存在但两路全跑"

**内容**：实现 A（per_block 返回 selected 复数序列，主循环提取），重跑 common-768 网格验证 bit-exact 等价。Fig.2 保留 `Selected θ̂ → Phase compensation` 但标注/收窄"两路并行评估、selector 在处理后选路"（或改为 selected complex output 而非 selected phase）；method.tex:25/:83 的 "selected branch supplies carrier-corrected samples" 在对象层成立。**不声称计算节省、不声称可部署、不声称 BER 增益。**

- **为什么**：A 是**最小实现修复**，让 Fig.2/method 的核心声称（selected output 真实存在）在对象层成立，且**默认 BER 不变**（零风险，bit-exact）。A 还**解锁 EVM/LLR/FEC 等下游指标能力**（虽本轮不算，但为未来留口）。A 不改算法/判据/参数，只改 mux 对象，属 implementation repair。
- **为什么不选激进（B/C）**：B 的"先选后跑"虽更接近 D014 控制论实质，但需重构主循环控制流 + 等价性验证 + 确认 h 估计确定性，工期和风险高于 A，且 BER 仍等价（无新性能证据）；C 属新算法 scope，触发 Groundwork/Contract，远超投稿修复。在 7 页精炼约束下，A 的叙事收益（Fig.2/method 真实性闭合）已足以覆盖其实现成本（per_block 返回签名 + 重跑验证），而 B 的额外收益（计算节省 + 控制流真实）需更多解释和验证篇幅，性价比在投稿场景下不如 A。
- **为什么不选保守**：保守档可能不满足导师"估计算法"，且 Fig.2 重做语义 brief 成本不比 A 低。
- **代价**：A 需 scope change（重跑网格超出"不运行新仿真"不变量），需用户批准。A 仍不能声称"先选后跑"或"可部署"——导师"估计算法"在 A 档下**仍可能不满足**（A 是后处理 mux，控制器未真正路由）。**这是 A 的根本局限，须如实告知用户。**

#### 激进档：实现 B（branch-routed receiver）或 C（non-genie online algorithm）

**内容 B**：在 A 基础上把 decide 提前、每窗只跑被选分支，验证等价 + 计算节省。**内容 C**：新增盲消歧方法，走 Groundwork/Contract，新 baseline/实验。

- **为什么可能值得**：B 让 D014 的 two-stage control 成为真正的控制机制（先选后跑），最接近导师"估计算法"；C 完整闭合可部署性。
- **为什么不选（作为本轮推荐）**：B 的 BER 仍等价（无新性能证据），计算节省需实测且 h 估计确定性待验，控制流重构工期长；C 属新研究 scope，超出投稿修复，且盲消歧研究工期无法量化（BLOCKED）。在投稿时间约束下，B/C 的收益不足以覆盖其实现+验证+解释成本。**B/C 可作为 A 之后的后续工作或学位论文延伸，不建议作为本轮投稿修复。**

#### 推荐档的选择理由小结

A 是**实现真实性缺口的最小闭合**：它让 Fig.2/method 的 selected-output 声称在对象层成立（修复 D015 的核心 FAIL），默认 BER 零风险（bit-exact），不改算法/判据/参数，且解锁下游指标能力。它的局限（不先选后跑、不可部署、可能仍不满足"估计算法"）须如实告知用户，由用户判断是否足够，或是否追加 B。**不得用增加篇幅作为默认收益**——A 的收益是真实性闭合，不是凑页。

---

### 8. 下一轮可执行 change contract 草案

> T015 要求标 DRAFT / NOT APPROVED。

```
=====================================================================
CONTRACT: CCE-SEL-001 (DRAFT / NOT APPROVED)
标题: 实现 post-hoc selected complex-output mux (路线 A) 并闭合 Fig.2/method 真实性
状态: DRAFT — 待用户在"保守/推荐/激进"三档间拍板后方可进入 WRITE
授权范围: 代码 per_block 返回签名修改 + 主循环 selected_rx 提取 + common-768 网格重跑验证 + Fig.2/method.tex 受限修订
=====================================================================

前提: 用户批准推荐档（A），并批准 scope change（重跑 common-768 网格，超出"不运行新仿真"不变量）

代码 delta (projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py):
  1. per_block() 返回值从 (ne_nda, ne_da, ne_nda_common768) 扩展为
     (ne_nda, ne_da, ne_nda_common768, rc_da, res_nda)
     — rc_da = da_ml_recovery 的 rx_comp (carrier-corrected DA 序列)
     — res_nda = resolve_m16apsk_blockwise(rc_nda, tb) (消歧后 NDA 序列)
  2. main() block loop 新增: selected_rx = rc_da if c=='da' else res_nda
     — 错误计数逻辑 (e_s_c768 += ne_d / ne_n_c768) 不变 (等价性保证)
     — 可选: selected_rx 存入 per-seed 记录 (供未来 EVM/LLR)
  3. 不改: decide(), _recovery.py, _modulation.py (resolve), 信道参数, seed, 窗口数, common-768 mask

验证 delta:
  4. 重跑 33 点 × 30 seed × 400 window (与 V009 同网格)
  5. 独立 verifier 核查: 逐窗 ne_da/ne_n_c768/e_s_c768 与当前权威 JSON bit-exact 一致
     (容差 1e-12, 对齐 validate_authoritative_result)
  6. 核查: n_select_da + n_select_nda = 400 不变; selected_rx shape=(256,) complex
  7. PASS 标准: A 的预注册验证 (§5) 全部满足; 任何 BER 不一致 = 实现错误, 非增益

论文 delta (仅在代码验证 PASS 后):
  8. method.tex:25/:83 的 "selected branch supplies carrier-corrected samples" — 在对象层成立, 保留或微调
  9. Fig.2: Selected θ̂ → Phase compensation 链路 — 标注/收窄为 "两路并行评估, selector 在处理后选路"
     (不声称先选后跑; 不声称计算节省; 不声称可部署)
  10. 不改: abstract/introduction/conclusion 的 selector 性能数字 (D008/D009/D013 冻结)

显式不含:
  - 不实现 B (先选后跑) — 留作后续
  - 不实现 C (non-genie) — 属新算法 scope
  - 不声称 BER 增益 (默认 bit-exact)
  - 不声称计算节省 (两路仍全跑)
  - 不声称可部署 (仍 tx_bits 消歧)

风险:
  - A 可能仍不满足导师"估计算法" (A 是后处理 mux, 控制器未真正路由) — 须如实告知用户
  - scope change 需用户批准 (重跑超出"不运行新仿真")
=====================================================================
```

---

### 9. 最终判定

> T015 交付结构第 10 项：分别评价当前事实闭合、路线可决策性、可实现性、可部署性。

| 维度 | 判定 | 理由 |
|---|---|---|
| **当前事实闭合** | **PASS** | 4 项关键事实独立核验完成（§0），均有 exact file:line。当前实现 = error-count mux，无 selected phase/complex output/common downstream。R011/V010/D015 结论与当前权威文件一致（行号漂移已修正）。 |
| **路线可决策性** | **PARTIAL** | A/B/C 定义与边界清晰（§1），效果矩阵（§2）和实现 delta（§3）可供决策。但"哪一档足以满足导师估计算法"**需用户/导师判断**——A 可能不足，B 更接近但成本高，C 超范围。本轮给出推荐档（A）但**不替用户拍板**。 |
| **可实现性（A）** | **PASS（条件性）** | A 的 delta 清晰（per_block 返回签名 + 主循环提取），等价性前提已确认（demod 确定性 + decide 数据独立）。但需 scope change（重跑网格）批准。 |
| **可实现性（B）** | **PARTIAL** | B 需控制流重构 + 确认 h 估计确定性（待验）+ 等价性验证。可行但工期/风险高于 A。 |
| **可实现性（C）** | **BLOCKED** | C 需新盲消歧方法，属新算法 scope，触发 Groundwork/Contract，工期无法量化。 |
| **可部署性** | **BLOCKED**（A/B） / **待研究**（C） | A/B 仍依赖 tx_bits 消歧，不可部署。C 闭合盲消歧后可部署，但属新研究。 |

**仍需用户拍板 / 导师澄清的事项**：
1. **导师"应该是估计算法"具体指哪个技术对象**（topic-index 未决项遗留）：A（后处理 complex-output mux）是否足够，还是必须 B（先选后跑 receiver）才能称为"估计算法"？
2. **是否批准 scope change**（重跑 common-768 网格）：A/B 都需重跑，超出当前"不运行新仿真"不变量。
3. **三档选择**：保守（收窄不改代码）/ 推荐（A）/ 激进（B 或 C）。
4. **Fig.2 的最终语义**：若选 A，Fig.2 的 Selected θ̂→Phase comp 是保留（对象层成立）还是收窄（标注两路全跑）？需图资产对话配合。

## 结论

当前权威实现是 **error-count mux**（selector 只累加错误计数，丢弃两路 phi_est，无 selected phase/complex output/common downstream）。Fig.2/method.tex 的 selected-output 声称强于实现（D015 FAIL 成立，本轮独立核验确认）。

三层区分：
- **A（post-hoc complex-output mux）**= 表达/接口闭环的审计性修复。让 selected 复数序列真实存在，Fig.2/method 在对象层成立，**默认 BER bit-exact 不变**，不省计算，不可部署。解锁 EVM/LLR 等下游能力但本轮不算。**可能仍不满足导师"估计算法"**（A 是后处理 mux，控制器未真正路由）。
- **B（branch-routed receiver）**= 功能性 receiver 架构。控制器真正先选后跑，最接近 D014 two-stage control 实质，可能省 ~50% branch compute。BER 在等价前提下与 A 一致。但仍不可部署（tx_bits 消歧）。需控制流重构 + 等价性验证。
- **C（non-genie online algorithm）**= 新算法 scope。闭合可部署性，但需盲消歧新方法，触发 Groundwork/Contract，超出投稿修复。

**推荐档 = A**（最小真实性闭合，零 BER 风险，解锁下游能力），但**如实告知 A 的局限**（不先选后跑、不可部署、可能不满足"估计算法"），由用户判断是否追加 B。change contract `CCE-SEL-001` DRAFT 已就绪，待用户三档拍板。

## 对决策的影响

- **不新建 D###**：本轮是路线评估（R note），决策权在用户。待用户三档拍板后，由主线程新建 D016（路线选择）并登记 voice.md。
- **D015 保持 active**：A/B/C 任一落地前，selected-output 实现缺口仍 BLOCKED。
- **D014 保持 active**：A/B/C 的选择决定 D014 定位的实现支撑强度，但 D014 本身（目标定位）不动。
- **若用户选 A 并批准 scope change**：进入新对话执行 `CCE-SEL-001`（代码 delta + 重跑验证 + 论文/Fig.2 受限修订），需 sim-preflight + 独立 verifier。
- **若用户选保守档**：Fig.2 需重做语义 brief（非局部挪字），method.tex 收窄，不重跑——但须重新评估是否满足导师"估计算法"。
- **若用户选 C**：开新 Groundwork/Contract 专题，走 FR-22。
