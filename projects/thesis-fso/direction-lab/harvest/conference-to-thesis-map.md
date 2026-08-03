# Conference-to-Thesis Extension Map

> **SUPERSEDED / PAUSED — D025→D026 (2026-08-03)：保留为旧 dossier，不再代表最终 thesis contract；当前唯一条件式 spine 见 D026。**

> 2026-08-03 | 关联专题: `2026-07-09-thesis-writing`（thesis-writing/thesis-structure owner）| 状态: DIAGNOSE/PROPOSE 产物，本轮不进 WRITE
> 权威会议稿锚: `projects/simulation/paper/ccisp2026/main.tex` + sections/*（V026/V027/V028 = 当前 5 页权威构建）
> 配套文件: `asset-claim-matrix.yaml`、`figure-table-plan.md`、`journal-extension-readiness.md`、`bounded-package-recommendation.md`

本文件回答 brief 的 Phase A + Phase D：从 CCISP 会议稿提取 contribution contract，并把 campaign 资产映射到唯一推荐的学位论文 blueprint。**不给选项堆，只给唯一推荐结构**。

---

## 1. 会议稿投稿状态（必须核实）

- **状态**: `CONFERENCE_MANUSCRIPT_COMPLETE / SUBMISSION_STATUS_UNKNOWN`
- **核实证据**: 在 `projects/simulation/paper/ccisp2026/` 及 `.sessions/2026-07-14-ccisp-content-expansion/` 全量检索，**未发现真实投稿编号、投稿系统回执或录用通知**。
- **纪律**: 不得声称"已投稿"或"已录用"。论文本身是完整可投稿会议稿（V026 PASS，5 页，fresh build，独立终验），但投稿动作无证据。
- **tracked main.pdf**: 当前 `.worktree` 下 `main.pdf` 的 hash（`56f2fb…`）**与权威终稿不一致**（≠ V026 `D5EC13FE…` ≠ V028 `06D45979…`），即 tracked PDF **不是权威终稿**。权威 = 当前 LaTeX 源 + V026–V028（5 页）。本轮不改源稿；如需 fresh build 验证，在临时目录做，不覆盖源稿。

## 2. 会议稿合法口径（brief 主控纠偏，硬约束）

| 维度 | 合法值 | 来源 |
|---|---|---|
| 场景 | 三档 downlink Gamma–Gamma（weak/moderate/strong，σ²_R=0.2/1.6/3.5 → (α,β)=(11.6,10.1)/(4.0,1.9)/(4.2,1.4)） | `system_model.tex`；D019 |
| 代表工作点 | 9 dB | `results.tex`、`abstract.tex` |
| 对比基准 | 相对 fixed NDA（common-payload BER-ratio） | `results.tex` Eq.(7) |
| headline | 改善约 0.8–1.5 dB | `abstract.tex`、`results.tex:45` |
| Monte Carlo | 30 seeds × 400 windows/点；768-bit common payload | `results.tex:14` |
| selector | 两阶段：received-power CV gate（τ_CV=1.10·(0.74+0.12e^{-γ/5})）+ fixed 13 dB effective-SNR gate | `method.tex` Eq.(5)(6) |
| 执行 | 每 256 samples/window **先选后执行** DA/NDA 单支 | `method.tex:4`；V015/V016 route-B |

**禁止复活口径**（本轮不得出现在任何 dossier / blueprint）: 26/29；uplink；1.2–1.9 dB；3.1 dB；D018/V026 之前撤回的旧 figures/claims；旧 `error floor` 声称（V019 已收窄为"residual turbulence-limited BER over evaluated SNR range"）。

---

## 3. Phase A — 会议稿 Contribution Contract

从当前 CCISP 正文（`abstract.tex` + sections/*）逐项提取：

| contribution 字段 | 内容 | 正文指针 |
|---|---|---|
| **problem** | 湍流 downlink 中每窗有效 SNR 变化，使固定 DA / NDA 的相对 BER 排序随 SNR/工作区翻转；现有 DA/NDA/joint 方法优化固定观测模型，不随接收功率调整参考类 | `introduction.tex:7`；`results.tex:21-25` |
| **baseline** | fixed DA、fixed NDA（以及 oracle 相位恢复仅作参考曲线，不作对手） | `results.tex:16` |
| **method action** | 每 256-sample window 先由 CV+effective-SNR 两阶段规则选 DA/NDA，再**仅执行**所选分支，输出一条 carrier-corrected 复数序列 | `method.tex:4,36-71` |
| **information source** | DA: 64 pilots/窗（每 4 符 1 pilot）；NDA: 8th-power + 频谱；controller: 仅 raw received power `q_k=|r_k|²` 与 nominal SNR（**不读** turbulence label / realized gain / tx bits） | `method.tex`；`system_model.tex:41` |
| **core mechanism** | received-power CV（测功率离散）→ effective-SNR proxy（blind `ĥ_dsp`）→ 固定 13 dB 门 → 单支执行 | `method.tex` Eq.(5)(6) |
| **primary metric** | $G_\mathcal{C}^{(s)}=10\log_{10}(P_{b,\mathcal C,\mathrm{NDA}}^{(s)}/P_{b,\mathcal C,\mathrm{ADP}}^{(s)})$，768-bit common non-pilot payload，paired-seed mean + 95% CI | `results.tex` Eq.(7) |
| **headline result** | 9 dB：三档全正，约 0.8–1.5 dB，弱湍流最大 | `results.tex:45` |
| **claim ceiling** | (1) 仅在低-中 SNR 区集中，高 SNR 趋零；(2) 高 SNR error floor 随湍流增强上升；(3) 同一冻结控制边界跨三档，不含湍流专用重调；(4) 三交叉点 14.5/16.9/16.0 dB 是诊断性曲线交点，**不是** 13 dB 控制门 | `results.tex:23,25,47`；V017/V019 |
| **图论证职责** | Fig.1 系统模型总览；Fig.2 两阶段 selector select-before-execute；Fig.3 三档 BER（DA/NDA/oracle）；Fig.4 DA–NDA crossover；Fig.5（=Fig.3 of synthesis）common-payload BER-ratio reduction + 95% CI | `main.tex:25-41`；figures/ccisp_fig{2,3,4}_*.pdf |
| **因 5 页限制未展开** | (a) 鲁棒性：SNR 失配、连续 GG、工作区变化下 selector 稳定性；(b) 部署实现：branch-routing 真实 branch-compute、定点、coded receiver 信息边界；(c) 失效/边界实验池 P01–P07-R；(d) 传统强 comparator 边界；(e) G1/P09 方法学反例 | campaign harvest（见 §5） |

### Conference-claim → Thesis-extension-question → Asset → Missing-evidence

| conference claim (meeting) | thesis extension question | available asset | missing evidence |
|---|---|---|---|
| 9 dB 三档 0.8–1.5 dB | headline 在更多 SNR/连续 GG 下是否稳定？ | P04 continuous GG（held-out pooled regret +0.146 dB） | 连续 GG 统一表（小验证） |
| 两阶段冻结规则跨三档 | SNR 失配下 selector 是否退化？ | P01 SNR mismatch（0.32–0.70 dB 损害 5 cell，adapter 恢复 4/5） | adapter+continuous GG 统一鲁棒性表 |
| 同一规则无湍流重调 | 传统重调能吃掉多少？是不是新算法？ | P02 region retune（weak 9→11 dB，+0.454 dB） | 无（边界已闭合，只需写成"设计规律/传统增强边界"） |
| 每 256 样本先选后跑 | 真实部署：能否省 branch-compute？定点是否保持？ | branch-routing（990/990 bit-exact）+ P03 fixed-point（0/132000 identity） | full-grid branch-compute timing（formal 口径，warm-up/重复）；float-vs-Q BER |
| 每 256 样本先选后跑 | 进 coded receiver 后信息边界/metric 仍合法？ | P08-R2 coded chain（5G NR LDPC + prefix-LS + metamorphic + AST） | pre-test freeze rerun（chronology PARTIAL） |

---

## 4. Phase B — 按 P0–P5 问题链重聚类 campaign

**不再按"有没有新算法"分组**。每项资产映射到下列问题链（brief 指定）：

| 问题 | 回答 | 主要资产 | claim ceiling |
|---|---|---|---|
| **P0**: 固定 DA/NDA 为何在湍流/SNR/工作区变化下需自适应？ | 会议稿已答（Fig.3 翻转 + Fig.4 crossover） | CCISP Fig.3/4 | 已闭合（会议贡献） |
| **P1**: selector 在 SNR 失配与工作区变化下是否稳定？ | 不完全稳定：5 cell 损害 0.32–0.70 dB；receiver-visible adapter 恢复 4/5；但 adapter 自带 ≈−2.5 dB 偏置地板，weak@9 残留 | P01 SNR mismatch；P02 region retune | `NO_DIAGNOSTIC_SIGNAL`（P01）/`PROBLEM_RESOLVED_BY_REGION_RETUNING`（P02）；Ch4 鲁棒性边界，**非独立贡献、非新算法**（D040 A-family 封顶） |
| **P2**: 连续/训练未见 GG 参数下是否仍稳定？ | 是：held-out pooled regret +0.146 dB < MDE 0.15，且**非 OOD-specific**（regret 随 σ²_R 单调下降，是 selector 的平坦属性） | P04 continuous GG（D042） | `PROBLEM_ABSENT_ON_CONTINUOUS_GG`；可作 Ch4 "selector 适用边界" 证据 |
| **P3**: selector 能否先选后跑（而非离线双分支）？ | 能：990/990 selector 端 bit-exact（旧参数 V011 + formal 参数 V015） | branch-routing `_a4_branchrouted_30seed.py` | code-path 回归证据可写；**74.6% 仅单条件 weak@5dB，非完整接收机复杂度**；non-genie 可部署性 BLOCKED（NDA 仍 tx_bits 消歧） |
| **P4**: 有限位宽实现是否保持选择与性能？ | 保持：Q(8,6) 0/132000 identity；gain-bearing regret +0.027 dB（<MDE）；混合精度 ≤+0.0166 dB | P03 fixed-point（D041） | **仅数值精度/实现可行性**；无 FPGA LUT/DSP/功耗；float-vs-Q BER 曲线不存在 |
| **P5**: 进 coded receiver 后信息边界/噪声估计/metric 是否仍部署合法？ | 机制合法但 chronology PARTIAL：coded chain 是**通用验证设施**（与 selector 主线分离），prefix-LS + metamorphic + AST 形成完整工具链 | P08-R2（D048/D049/D051） | `STOPPED_WITH_PARTIAL_ASSET`（无 pre-test freeze receipt）；放 Ch5/附录作验证设施，**不硬并成 selector 方法** |

**负面资产归类**（brief Phase B §7）: P05–P07-R 等跨对象负面只有能直接解释 selector/receiver 设计边界的进正文；其余进附录/limitations 或不使用。G1（D057 scale artifact）/P09（D053 consistency≠correctness）= 方法学反例，进 threats-to-validity/附录，**禁晋级为方法**。AMC（D008/D009）= 仅"为何不继续扩方向"背景，**不进主包装**。

---

## 5. Phase D — 唯一推荐 Thesis Blueprint（不给选项堆）

**唯一推荐**（与 `campaign-level-thesis-contribution-synthesis.md` 的"唯一推荐 spine"一致）：

```
Ch1 绪论
  └ 问题背景 + 一个主方法 + 实现验证 + 边界（不提"多算法多贡献"叙事）
Ch2 系统模型与 receiver chain
  └ GG block fading + DA/NDA CPR 基础 + pilot overhead + 相位过程 + SNR 约定
Ch3 CCISP adaptive CPR 方法与正式结果（会议稿主锚）
  └ 问题 → 两阶段 selector → 先选后执行 → 9 dB 0.8–1.5 dB → 三图 + metric
Ch4 selector 鲁棒性、传统重调与适用边界
  └ P01 SNR mismatch + P02 region retune + P04 continuous GG + P11 strong-traditional 边界
  └ 合并 P01–P07-R 负面为一张"鲁棒性/边界表"，不拆 7 个创新
Ch5 branch-routed、定点、coded receiver-visible 实现
  └ branch-routing 990/990 + P03 Q(8,6) identity + P08-R2 验证设施
  └ 实现验证章，非方法章；无 FPGA 资源/功耗声称
Ch6 结论与边界
  └ 主方法 + 实现验证 + 边界 + 未来工作（含 AMC 一句，需用户授权新 GW）
```

### 每章必填字段

| 章 | research question | chapter contribution | conference reused | campaign asset | figure/table | claim ceiling | missing evidence | 前后接口 |
|---|---|---|---|---|---|---|---|---|
| **Ch1** | 湍流 FSO downlink CPR 如何随接收功率自适应？ | 定位单一主方法 + 实现验证 + 边界 | CCISP intro（背景+DA/NDA 互补） | AMC freeze（背景一句） | — | 不夸多贡献 | — | →Ch2 给模型 |
| **Ch2** | 信号/信道/CPR 基础如何定义？ | 统一模型与符号 | CCISP system_model 全节 | — | 复用 Fig.1 | SNR 约定冻结 | — | →Ch3 用模型 |
| **Ch3** | 两阶段冻结规则如何工作 + 9 dB 正式结果 | **会议主贡献（主方法）** | CCISP method + results 全节 + Fig.2/3/4/5 | branch-routing（支撑"先选后跑"实现） | Fig.2/3/4/5（复用会议三图 + Fig.1） | 0.8–1.5 dB / 9 dB / 三档；高 SNR 趋零；error floor 边界 | headline 数字可从 `selector_a` JSON 权威 raw 确定性复算（见 §6） | ←Ch2 模型；→Ch4 鲁棒性 |
| **Ch4** | selector 在失配/连续 GG/工作区变化下是否稳定？传统重调边界？ | **鲁棒性研究贡献（成立）** | CCISP 两阶段规则作为被检验对象 | P01 + P02 + P04 + P11 | 一张统一鲁棒性/边界表 | 边界（NO_DIAGNOSTIC / RESOLVED_BY_RETUNE / ABSENT_ON_CONTINUOUS_GG）；非新算法 | 统一表需小验证（见 `bounded-package-recommendation.md`） | ←Ch3 规则；→Ch6 边界 |
| **Ch5** | 部署实现：branch-compute、定点、coded 信息边界是否保持？ | **部署实现贡献（成立，限定实现可行性）** | CCISP select-before-execute 数据流 | branch-routing + P03 + P08-R2 | Fig.2（branch router）+ Q-format regret 表 + coded FER 点表 | 实现可行性；**非 FPGA 资源/功耗**；coded 无 freeze receipt（PARTIAL） | full-grid branch-compute timing（formal）；float-vs-Q BER；coded freeze rerun | ←Ch3 输出接口；→Ch6 |
| **Ch6** | 主方法 + 实现 + 边界 + 未来 | — | CCISP conclusion | AMC 一句 | — | — | — | ←Ch4/5 |

### 必答（brief Phase D）

- **Ch4 是否构成独立"鲁棒性研究贡献"？** **是**。P01+P02+P04+P11 围绕同一被检验对象（CCISP 两阶段 selector）的稳定性/适用边界，形成统一问题（"冻结规则在失配/连续/重调下是否稳定？"），是独立可写的鲁棒性章节。**但它不是新算法**——结果多为 `NO_DIAGNOSTIC_SIGNAL`/`RESOLVED_BY_REGION_RETUNING`/`ABSENT_ON_CONTINUOUS_GG`，是边界证据不是新方法。
- **Ch5 是否构成独立"部署实现贡献"？** **是（限定）**。branch-routing 990/990 + P03 Q(8,6) identity + P08-R2 验证设施共同回答"会议方法的部署/实现是否保持选择与性能"。**但 claim ceiling = 实现可行性/数值精度**，不能声称 FPGA LUT/DSP/功耗，coded chain 无 freeze receipt。
- **哪些是 thesis contribution，哪些不是新算法？**
  - 新算法：**无**（本轮范围内）。CCISP adaptive CPR 是主方法，campaign 没有产出第二算法（`NO_SECOND_CONTRIBUTION_YET`，D058 campaign 饱和）。
  - thesis contribution（可写学位论文但非新算法）：Ch4 鲁棒性边界研究 + Ch5 部署实现验证。
- **这套结构在现实硕士论文中为何成立？** 学位论文（vs 会议）需要：方法章（Ch3）+ 鲁棒性深化（Ch4）+ 实现验证（Ch5）。同门学位论文常见套路 = 一个主方法 + 鲁棒性/实现扩展（profile "倾向务实可毕业" + D005）。Ch4/Ch5 用已有资产填实，不开新方向，符合用户"不要重新找第二方法"。
- **是否仍需要第二个独立算法？** **不需要**。campaign-level synthesis 已定 `NO_SECOND_CONTRIBUTION_YET`，AMC（D009）确认无第二主方法。若用户未来授权新 GW 跑 AMC，可作未来工作，但**不在本轮 blueprint 内**。

## 6. headline 数字可机检性（修正 synthesis 的过悲观标注）

`campaign-level-thesis-contribution-synthesis.md` 标注 Ch3 headline gain "结果 JSON 无 gain 字段，machine-uncheckable"。**修正**：selector A 权威 JSON（`ccisp_family1_selector_a_30seed.json`，authority params_sha256 与 `params.py` 一致）每 cell 含 `selected_errors` / `fixed_nda_errors` / `n_bits=768`，$G_\mathcal{C}^{(s)}=10\log_{10}(\text{fixed\_nda\_errors}/\text{selected\_errors})$ 可**确定性复算**，9 dB paired-seed mean 跨三档可直接重算并比对 0.8–1.5 dB。**headline 数字是 machine-checkable 的**（只是没有预聚合 `gain_db` 字段，需一行复算）。→ `bounded-package-recommendation.md` 把"统一 figure/table regeneration"列为 RECOMPUTE_ONLY。
