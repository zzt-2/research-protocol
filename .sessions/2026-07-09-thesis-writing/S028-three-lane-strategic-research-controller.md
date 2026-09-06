# [S028] 方法生产轻量主控

> 2026-08-30 | 战略调研编排 | 第一轮完成
> 2026-08-30 续接 | 连续方法生产 | RUNNING
> 2026-08-30 续接 | 第六批回收、第七批纸面门 | RUNNING
> 2026-08-30 续接 | 第七批回收、第八批 correctness 门 | RUNNING
> 2026-08-30 续接 | 第八批回收、第九批有界开发 | RUNNING
> 2026-08-30 续接 | 第二十批 C5-0 单格停机与 C5-5 轮换 | RUNNING

## 目标

以一个轻量主控持续推进共同平台、Ch4 与 Ch5 方法生产：每批最多三个互补新对话，主线程统一回收和拍板，直到两个方法章形成可写证据包或授权路线真实耗尽。

## 记录

### 唯一北极星

1. 论文题目：“星地激光通信信号处理关键技术研究”。
2. Ch3：已录用 Received-Power-Aware Adaptive CPR，不重构其方法身份。
3. 共同平台：DP-(8,8)-16APSK+BICM/LDPC 相干星地 FSO；Ch3 为 per-tributary CPR，Ch4/Ch5 为完整 2×2 链。
4. 论文还需要两个技术对象不同、故事专业的方法章；BER/FER 明确改善优先，B/C 级工程收益只作后备。
5. D044 已授权外部证据、候选 Groundwork、correctness smoke、实现、仿真、确认与章级证据包；仍不修改 Skill/controller，正式论文正文等证据冻结后再写。

### 第一轮阶段门（已完成）

回答：**什么样的共同 testbed/headroom 是物理合理且不人为画靶的；在该合同下，Ch4 五族和 Ch5 六族的第一批排序是否成立。**

第一轮不回答实现参数、代码结构、完整实验网格、论文措辞或外部新颖性。

### 三条互补工作线

| 任务 | 唯一决策域 | 状态 | 新对话 |
|---|---|---|---|
| T036 | 共同平台、损伤分工、headroom 与正确性 smoke 合同 | COMPLETE（198.8 s） | `01a04e70-29ba-7390-bf5c-97debaa005be` |
| T037 | Ch4 五个机制族的物理合法性、baseline 和优先级 | COMPLETE（235.7 s） | `01a04e70-29a5-7fd3-bdb5-53d3cadb16a5` |
| T038 | Ch5 六个机制族的物理合法性、baseline 和优先级 | COMPLETE（210.2 s） | `01a04e70-29d1-7901-8009-c1247b26af02` |

> 2026-08-30 派发：三条均从 commit `4c85f33` 建立隔离 worktree；只读任务已启动。该 commit 是派发基线，不是本轮最终提交号，后续主控状态仍在同一对话提交中 amend。

### 第一轮主控闭环（已完成）

1. `PLAN FREEZE`：北极星、当前门、三线任务和禁止事项先落盘。
2. `COMMIT GATE`：D043、S028、T036–T038 必须先进入同一最新 commit；新对话均从该 commit 建 worktree，禁止用未提交口头状态派发。
3. `ONE BATCH`：最多三个新对话并行，每条一个回合、约 15 分钟，只读本地证据。
4. `COLLECT`：主线程用 thread id 回收，不让工作线彼此接力或自行派生。
5. `CONTRADICTION MATRIX`：逐项列共同结论、冲突结论、证据缺口和对 D040–D042 的影响。
6. `MAIN JUDGMENT`：主线程给出唯一推荐，不用“各有利弊”逃避判断。
7. `USER GATE`：第一轮结束时等待用户确认；已由 D044 的持续授权取代。

### 当前防漂移检查（每次回收前后只回答四项）

- 当前工作是否直接推进 `WRITE-READY EXIT`，或关闭下一 positive action 的必要 blocker？
- 它是否处在 topic-index 当前 `active_lane/allowed_actions` 与 master-state formal step 内？
- 是否改变 D040 共同平台、D041 证据合同或 D044 硕士方法目标？若改变，才停下登记新 D###。
- 是否连续出现纯治理/一致性包而没有方法构造、比较或证据？若是，立即轮换到 positive work。

### 第一轮停机规则（已完成）

以下规则只适用于已经结束的 T036–T038，不再约束 D044 后续：当时每条只做一回合、只读本地材料，三线回收后等待用户门。D044 已明确授权外部证据与跨批自动推进。

### 第一轮回收结果

三条均在一个回合、约 3–4 分钟内完成，未修改文件、未实验、未联网、未派生任务。结构化回报可直接综合，说明“一轮三线 + 短输出 + UNKNOWN”控制方式有效。

共同结论：

1. 平台应固定共同调制/偏振/编码与真实 Ch4→Ch5 接口，但不同章节只主动扫描自身承重自由度；不得把 PDL、PMD、CFO、强人工残差一起叠加来制造收益。
2. Ch4 首轮设计优先级建议改为 `C4-2 APSK 环感知半盲 → C4-1 scaled-unitary 约束 → C4-0 时序正则`；C4-3/C4-4 暂不进首批。
3. Ch5 首轮设计优先级建议改为 `C5-1 APSK 几何软解调 → C5-2 syndrome 救援 → C5-0 残差 LLR 校准`；C5-5 明确只适合 B/C 工程后备。
4. 当前最大的事实缺口不是“参数取多少”，而是统一 APSK 链上经典均衡后的真实残差统计、有限 FIR/ISI 的物理来源、scaled-unitary 近似是否成立，以及目标 LDPC 的 syndrome/extrinsic/逐轮状态是否可见。

### 共同结论—冲突—缺口矩阵

| 议题 | 三线共同/局部结论 | 与既有规划的冲突 | 主线程综合判断 |
|---|---|---|---|
| 主动损伤 | Gamma–Gamma/功率/相噪主要由 Ch3 承重；SOP/pilot/2×2 结构由 Ch4；Ch4 后 residual/LDPC 由 Ch5 | S027 曾把 PDL/PMD/ISI 都当可能自由度 | 暂不主动加入 PDL、PMD、CFO；有限 FIR/ISI 保留为 `UNKNOWN`，先查物理来源再决定 |
| Ch4 首轮 | C4-2、C4-1 高于 C4-0 | S027 只列同批，未排序；历史 P11 容易让时间轴被默认优先 | 采用 `C4-2 > C4-1 > C4-0` 的设计优先级，但三者仍是 DESIGN_ONLY |
| Ch5 首轮 | C5-1、C5-2 高于 C5-0 | 旧 P08-R2 资产容易让标量校准被默认优先 | 采用 `C5-1 > C5-2 > C5-0` 的设计优先级；旧 P08 只作负先验和基础设施 |
| 强经典对手 | T036/T037 多处建议“被 EMA/RLS/MMA 吸收即停” | D031 明确强邻居/廉价替代只限制 claim ceiling，不自动 Kill | 只从 A 级 BER/FER 首批退出；若仍有真实 overhead/complexity/实现收益，可降为 B/C，不记科学 F；只有 correctness/truth leak/no-op 才 F |
| 数据流顺序 | T036 推荐物理链为 Ch4 equalization → Ch3 per-tributary CPR → demap → Ch5 | 论文章节顺序仍是 Ch3 CPR、Ch4 equalization、Ch5 decoding | 物理顺序与章节顺序不必相同，但必须在总框图和章首解释；是否需要调整章节顺序仍是未决，不在本轮擅自改 |
| 外部证据 | 本地材料能排优先级，不能冻结物理量级、经典 APSK baseline 或 LDPC 接口 | 原范围禁止外部检索 | 若继续，应只开一轮三线 bounded 外部调研，不直接进入实现或仿真 |

### 第一轮主线程唯一推荐（已获 D044 授权）

下一阶段先做一轮 bounded 外部证据调研，仍限三线：

1. **物理平台 authority**：星地/自由空间相干 DP 接收中 SOP、PDL、PMD/ISI、滤波记忆和 CFO 的真实来源与可引用量级，回答“有限 2×2 FIR 是否合理”。
2. **APSK 前端经典对手**：多环 APSK 的 CMA/MMA/半盲均衡、各向同性与径向—切向软解调的正确 baseline 和适用前提。
3. **编码接收 authority**：目标 LDPC 的 syndrome/posterior/extrinsic 可见性、等成本 rescue/NOMS/BICM-ID comparator，以及哪些动作更可能改善 FER 而非只省迭代。

三线只回答 authority/baseline/物理前提，不找“全新方向”，不做实验。回收后冻结共同平台与候选排序；随后必须先走候选级 Groundwork，不能直接进入 correctness smoke。

### D044 后的连续闭环（当前）

1. `CURRENT GATE`：当前只运行 T039–T041 三条 Groundwork Step 1 外部 authority 线；没有外部证据就不冻结 testbed 或 comparator。
2. `ONE BATCH`：每批最多三个相互独立的新对话；每条必须关闭一个技术不确定性，禁止只修状态或生成更多制度。
3. `COLLECT AND JUDGE`：主线程回收事实、处理冲突、更新候选排序；routine 结论自动进入下一合法步骤，不再逐批叫醒用户。
4. `NO SKIP`：每个执行候选必须在 master-state 有可核的 Step 1–3/3.5/4a 指针；设计卡、标题联想或共享 testbed 均不能代替。
5. `POSITIVE WORK`：每个工作包必须创建方法构造、完成公平比较或冻结章级证据；纯治理/一致性修补不得连续占用两个包。
6. `ROTATE`：同一方法族两个构造仍无 A/B 信号，停止第三个微变体并换机制族；单章全部机制族仍无 B 才触发战略停机。
7. `WRITE-READY EXIT`：Ch4/Ch5 分别达到 `THESIS_METHOD_READY`，具备动作链、算法步骤、fair baseline、主图数据、消融、边界和 claim ceiling，才算本 mission 完成。

### 第二批工作线

| 任务 | 唯一决策域 | formal step | 状态 | 新对话 |
|---|---|---|---|---|
| T039 | coherent FSO/星地 DP 物理平台与有限 2×2 FIR 合法性 | GW Step 1 | COMPLETE / `3f8aa05` | `01a04e91-6d2b-7302-a6fe-e2a10a1b92b9` |
| T040 | APSK 均衡与软解调的经典 baseline/适用前提 | GW Step 1 | COMPLETE / `f9ed5f2` | `01a04e91-6d68-7790-81f0-70c3371a0a85` |
| T041 | LDPC syndrome/posterior/extrinsic 接口与公平 comparator | GW Step 1 | COMPLETE / `5381740` | `01a04e91-6d4d-7b83-a818-8851ce09d28d` |

> 2026-08-30 派发：三条均从 `codex/rdl-method-production-v2` 的 commit `2e935ef` 建立隔离 worktree，task-control 均为 CP001/EXTERNAL_EVIDENCE；主线程只在回收后更新 formal authority。

### 第二批主线程裁决

1. 共同平台默认采用 memoryless single-tap 2×2 Jones mixing；光纤 PMD 不迁移到 FSO。有限 FIR 只在 receiver filter、I/Q timing skew 或其他直接 authority 下作为条件分支。
2. Ch4 首批只推进 C4-2 与 C4-1：C4-2 的公平主 comparator 是同 pilot/可靠度/预算的 LS+DD，并加入同初值 tuned RDE；C4-1 必须与 unconstrained/ridge LS 比较，且只在双奇异值近等时成立。
3. Ch5 首批推进 C5-1：必须正面对比 full-covariance Mahalanobis demapper，候选差异压在 pilot-only causal estimation、radial/tangential structure、shrinkage 与 DP-(8,8)-16APSK pooling。C5-2 保留后备，但当前 adapter 不提供 full hard codeword、syndrome、posterior/extrinsic 或逐轮 state，暂不进入实现。
4. 三条都是 Step 1 authority，不是方法成立。下一合法动作是 Step 2 下载/转换/覆盖报告；共享 platform、Ch4、Ch5 分三包，避免重复全文劳动。

### 第三批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T042 | 星地 coherent FSO/Jones/receiver-front-end 平台全文与参数覆盖 | GW Step 2 | COMPLETE / `ff8095a` / 6 qualified / accepted limitation / `01a04ea1-a21b-7b33-96e1-dad26f738101` |
| T043 | Ch4 C4-2/C4-1 comparator 与方法邻居全文覆盖 | GW Step 2 | BLOCKED / `3d3c1e6` / 5 qualified / missing direct APSK / `01a04ea1-a1e1-7831-8730-f5d73fda51a1` |
| T044 | Ch5 C5-1 demapper 与 C5-2 decoder 后备全文覆盖 | GW Step 2 | COMPLETE / `d8b6804` / 6 qualified / accepted debt / `01a04ea1-a206-72c2-aa99-484f273d4024` |

> 2026-08-30 派发：三条均从 commit `80edfae` 建立隔离 worktree，task-control 均为 CP002/GROUNDWORK_ACQUIRE；主线程不在 Step 2 期间提前形成 Q# 或启动实现。

### 第三批主线程裁决

1. T042 的 6 篇全文已覆盖 Jones/unitary-PDL、星地 CFO/相噪和 receiver filter/skew；大气偏振不进入主动 testbed 或承重 claim，因此该缺口按 D044 接受为 limitation，而不是继续追下载。
2. T044 的 Layton 2018 已直接覆盖 isotropic/scalar baseline 与 full/data-dependent covariance 竞争边界；Zhang 2013 仅是 nonblocking scalar-scaling debt，Ch5 允许进入 Step 3。
3. T043 的 5 篇全文已覆盖 CMA/MMA/RDE、coherent/Jones 与 pilot/DD comparator，但没有合格的 APSK 直接均衡全文。该缺口直接影响 C4-2 的多环迁移合法性，不以主控口头豁免；只补一个既有 T040 候选后再进 Step 3。
4. 下一批只开放一个 acquire 修复和两个 read/parameter positive-work 包；仍不实现、不实验、不做 Step 3.5。

### 第四批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T045 | 用 T040 既有候选闭合 Ch4 direct APSK equalization 全文缺口 | GW Step 2 repair | COMPLETE / `ac0a0aa` / `01a04ebb-badd-7082-af8a-52e8b55e1719` |
| T046 | Ch5 C5-1/C5-2 五至六篇全文结构化精读与 Q# 判定 | GW Step 3 | COMPLETE / `ab080e0` / Q-C5-1 4/4 / `01a04ebb-bade-7e82-b415-7fbb166895a7` |
| T047 | 共同 coherent FSO 平台参数、来源与 active/excluded 边界表 | platform authority read | COMPLETE / `8cb50a8` / 6 frozen + 9 UNKNOWN / `01a04ebb-bb27-7f92-8c1f-a339699e6c55` |

> 2026-08-30 派发：三条均从 commit `7f4f960` 建立隔离 worktree，task-control 为 CP003；均在一次 bounded 回合内提交，无实验、实现或派生方向。

### 第四批主线程裁决

1. T045 的 Baldi 2012 正文提供 4+12 APSK、DFE/LMS 与同场景比较，足以闭合“APSK 直接均衡全文”门；它没有 ring-aware cost，不构成 C4-2 exact collision。Ch4 Step 2 由 BLOCKED 改为 COMPLETE。
2. T046 确认 Layton 2018 完整覆盖逐星座点 full covariance、Mahalanobis 与 log-det；这些原子不得声称新颖。pilot-only causal radial/tangential estimator、跨环/跨偏振 shrinkage pooling 与同预算 comparator ladder 未被完整覆盖，Q-C5-1 四判据 4/4，可进 Step 3.5。
3. C5-2 因 adapter 缺 syndrome/CRC/soft reliability 继续后备，不阻塞 C5-1，也不在本批开接口实现。
4. T047 支持共同 smoke 默认 memoryless single-tap unitary 2×2 Jones；filter transfer/FIR span 没有冻结 authority，但 minimal smoke 不启用 FIR，因此是 conditional debt，不是当前 blocker。

### 第五批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T048 | Ch4 七篇全文精读，分别判定 Q-C4-2 与 Q-C4-1 | GW Step 3 | COMPLETE / `e5a6ea7` / 7 read / `01a04eca-1b3b-7a43-a6ad-5ec70fe115fc` |
| T049 | Ch5 Q-C5-1 完整 recipe 的 targeted collision/neighbor closure | GW Step 3.5 | COMPLETE / `4e50a73` / 63 unique / `01a04eca-1b6c-7872-b116-55566bce5645` |

### 第五批主线程裁决

1. T048 的 Q-C4-2 在七篇经典全文内没有完整 receiver-visible IAO 碰撞，且公平对手可冻结为同 LS 初值的 tuned RDE 与 tuned DD-LMS/RLS；它是 Ch4 唯一优先进入 Step 3.5 的对象。
2. Q-C4-1 只保留 `SURVIVES_BOUNDED / STRONG_RECIPE_NEIGHBOR`：Roudas 已覆盖短训练 LS + 受酉约束盲跟踪，scaled-polar/Procrustes 也属已知原子，故不与 Q-C4-2 同批推进。
3. T049 在 6 query + Layton 双向引用链的 63 个去重记录中未确认 C5-1 完整 recipe 碰撞；Layton 仍是 full covariance + Mahalanobis/log-det 的最强 primitive collision，目标只可主张 pilot-limited APSK 几何结构化 estimator 与 matched-budget pooling。
4. 下一批只推进 Ch4 Step 3.5 与 Ch5 Step 4a 纸面维度 A0/A'/A/B。两项未由主控接收前，维度 D、实现、smoke 与实验继续禁止。

### 第六批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T050 | Ch4 Q-C4-2 的 2019+ exact-recipe/strong-neighbor closure | GW Step 3.5 | COMPLETE / `3fcc33a` / 305 unique / `01a04ed9-ee55-72e0-95fc-d7687f886978` |
| T051 | Ch5 Q-C5-1 的问题适配、竞争维度、结构优势与新颖性-可行性解耦 | GW Step 4a A0/A'/A/B | COMPLETE / `f450ccc` / PAPER_DIMENSIONS_PASS / `01a04ed9-ee38-7052-ba78-52e5d43d88fd` |

### 第六批主线程裁决

1. T050 三轮由 `new MUST/SHOULD=0/1→0/3→0/0` 收敛，在 15 个 archive、305 个去重记录中未确认目标五项完整 recipe 碰撞，故 `Q-C4-2 SURVIVES`。Di Rosa–Richter 2021 是最强 recipe 邻居，但当前只有摘要级证据且调制为 PS-QAM；它压低 claim ceiling，不替代 Step 4a 的科学可行性判断。
2. T051 判定 Ch5 `PAPER_DIMENSIONS_PASS`：candidate v1 冻结为 pilot-limited APSK radial/tangential hierarchical structured covariance；最强廉价对手为 hard-pooled per-ring R/T，最强直接传统对手为 Layton per-point full covariance + matched generic shrinkage。该结果只允许准备维度 D，尚无科学 Go。
3. 两章都已经从“候选标题”进入具体输入—动作—输出 recipe；下一批继续先纸面门与 testbed seam，不用检索闭包冒充方法进展，也不直接启动实验。

### 第七批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T052 | Ch4 Q-C4-2 的问题适配、竞争维度、机制与候选 v1 | GW Step 4a A0/A'/A/B | COMPLETE / `de44014` / PAPER_DIMENSIONS_PASS / `01a04eea-14af-73d0-9ff2-a612f572a450` |
| Ch4 readiness audit | 现有代码/testbed seam、公式与最小 smoke 准备度 | pre-D audit | COMPLETE / CONDITIONAL_READY |
| Ch5 readiness audit | 现有代码/testbed seam、codec/metric 与最小 smoke 准备度 | pre-D audit | COMPLETE / PARTIAL_READY |

### 第七批主线程裁决

1. T052 将 Ch4 v1 冻结为：相同 2×2 pilot-LS 初值后，以 nearest-symbol distance 与 ring residual 的双证据二值门逐支路筛选 canonical RDE update；smooth weight 仅作同族 pivot。最强廉价替代是只用 native RDE ring residual 的单阈值门，公平主对手是 tuned plain RDE 与 DD-LMS/RLS。
2. 两章均完成纸面 A0/A'/A/B，但尚无 oracle/headroom 数字。静态审计表明可以在不改 `common/`/`params.py` 的独立目录实现和做 correctness smoke；Ch4 需从本地全文冻结 canonical update 式，Ch5 需冻结确定性 shrinkage 式且不能用合成 anisotropy 冒充目标场景存在性。
3. 下一批按 D041 分段：先实现与 correctness-only smoke，再由独立 verifier 接收；只有接收通过后才开放 headroom/performance。Ch5 另开只读 residual authority 线，确认 Ch3 输出或其他项目内已有资产能否合法形成 post-Ch4 residual cell。

静态 readiness 的可恢复事实压缩如下：Ch4 可复用 single-tap pilot-LS、确定性 unitary Jones 和 APSK mapping，但公共 DP generator 不支持 APSK、公共 CMA 更新式有已知缺陷，故必须独立实现并冻结 canonical 式号；最小 seam 是 `explore/ch4-apsk-ring-gated-rde/`。Ch5 可复用 APSK mapping、bit partition/GMI 模式和独立 LDPC decoder，但现有 demapper 是 16QAM，且 equal-white circular control 不提供 R/T headroom；最小 seam 是 `explore/ch5-apsk-structured-covariance/`，target residual 另由 T055 裁决。

### 第八批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T053 | Ch4 双证据 gated-RDE + cheap gate/plain RDE 的独立实现与 correctness smoke | GW Step 4a-D correctness | COMPLETE / repaired by T058 / T056 PASS |
| T054 | Ch5 structured covariance + B1/B2/B3 的独立实现与 correctness/GMI-identity smoke | GW Step 4a-D correctness | COMPLETE / T057 PASS |
| T055 | 从已有 Ch3/Ch4/平台资产闭合 Ch5 合法 residual cell 与参数 authority | pre-performance authority | COMPLETE / NO_AUTHORIZED_TARGET_RESIDUAL |

### 第八批主线程裁决

1. Ch4 初版把 nearest-symbol 所属环错误用于 canonical RDE update；T056 没有被测试一致性骗过，给出 `FAIL_REPAIRABLE`。T058 精确修复后，原 verifier fresh 重跑 7 tests、smoke、四臂分叉和 firewall，最终 `IMPLEMENTATION_CORRECTNESS=PASS`。
2. Ch5 correctness seam 独立复核 `PASS`；此前 per-point centering 后 ring covariance 分母的 DoF 缺陷已修为 `sum(n_k-1)`。该结论只证明 estimator/LLR 正确。
3. T055 的 `NO_AUTHORIZED_TARGET_RESIDUAL` 是 testbed blocker，不是方法科学失败。正确物理链固定为 `Ch4 demux → per-pol Ch3 DA CPR → Ch5 residual/demap`；禁止复制报告中反序的文字叙述。
4. CP008 只开放两个正向包：T059 Ch4 有界 development 与 T060 Ch5 residual bridge correctness。二者并行；Ch5 occurrence 必须等 Ch4 冻结后另开任务。

### 第九批工作线

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T059 | Ch4 预注册两轮 development：BER/headroom/gate discrimination/count-matched | GW Step 4a-D bounded development | COMPLETE / D / STOP_NO_METHOD_SIGNAL / `4113534` |
| T060 | Ch4→per-pol Ch3 receiver-residual bridge 的实现与 correctness | target residual bridge correctness | COMPLETE / T061 PARTIAL / repair required / `5b42e81` |

### 第十批主线程裁决与工作线

1. T062 独立重算确认 C4-2 的 candidate/cheap 在 D1–D3 均不优于 tuned plain，oracle headroom 约为零；接受预注册科学停机，不修 hash portability、不重跑、不增 gate。
2. Ch4 轮换 C4-1，但不借 C4-2 的 Step 3.5/Step 4a。先完成 candidate-specific exact-recipe closure；polar/Procrustes 经典性和 balanced-pilot 代数等价只降低 claim ceiling，不按 D031/D032 自动否决场景迁移。
3. T061 对 Ch5 bridge 为 PARTIAL：物理顺序和 firewall 成立；T063 只修完整 frozen-arm snapshot/hash 与连续 acquisition/observation scalar 时序。修复后必须由另一上下文独立复验。
4. occurrence 预注册场景不变，Ch4 anchor 冻结为 plain canonical RDE、`mu=1e-3`、`Np=4`、无 gate threshold；只有 bridge verifier PASS 才能启动。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T062 | C4-2 raw/aggregate/gate/stop 独立复算 | independent science verification | COMPLETE / PARTIAL provenance-only / scientific STOP accepted / `e371109` |
| T063 | Ch5 bridge frozen-arm provenance 与连续 scalar 时序窄修复 | target residual bridge correctness | COMPLETE / local 33 tests PASS / `e141cc6` |
| T064 | C4-1 scaled-unitary pilot-LS 候选专属 exact-recipe closure | GW Step 3.5 | COMPLETE / `SURVIVES_AS_CLASSICAL_MIGRATION` / `b5f1b61` |
| T065 | T063 修复的独立 correctness 与 provenance 复验 | independent science verification | COMPLETE / PASS / `1473867` |
| T066 | Ch5 共同链唯一一格 residual occurrence 诊断 | target residual occurrence smoke | COMPLETE / `DETECTABLE_OCCURRENCE` / `a4b6b67` |

### 第十批续接裁决

1. T065 独立 fresh 复验为 `PASS`：33 项测试、完整 frozen-arm snapshot/hash、连续 acquisition/observation scalar 时序及旧 firewall 全部成立，V020 的 Ch5 correctness 缺口关闭。
2. 按 D047 放行且仅放行 T066 的一个预注册 occurrence cell；它只判断 non-circular/point-dependent residual covariance 是否自然存在，不做 C5-1 estimator 性能、BER/GMI/FER 或参数搜索。
3. T066 若 `NO_DETECTABLE_OCCURRENCE`，立即轮换 C5-0 Step 2；若 `DETECTABLE_OCCURRENCE`，仍须另走 bounded development 才能判断方法。任何结果都不得追加第二 cell 或新 impairment。

### 第十一批主线程裁决与工作线

1. T064 没有确认九字段完整 target-scene recipe 碰撞；balanced pilots 下 post-LS scaled-polar 与 direct constrained scaled-unitary LS 代数等价，因此 C4-1 不得包装成新估计理论，但可按 D031/D032 作为经典结构估计迁移到 DP-(8,8)-16APSK 星地相干接收的硕士候选。
2. T066 在唯一预注册 cell 完成 `64/64` windows。主控从 raw 独立重建 reducer，D1/D2/D3 与 aggregate 的最大绝对差为 `0.0`，terminal=`DETECTABLE_OCCURRENCE`；D3 mean=`0.0870608267`、95% CI=`[0.0642673878,0.1112830033]`。
3. CP010 并行开放两个正向包：T068 只做 C4-1 候选专属 Step 4a A0/A′/A/B；T067 做 Ch5 两轮有界 BER/GMI 开发。C4 不得跳到实现，Ch5 不得增加新损伤或完整 coded grid。
4. Ch5 若 C1 被 B2/B3 吸收，不自动关闭章节：按真实结果收缩为 B2/B3 的经典场景迁移；只有 B1 以上所有结构臂都无 BER/GMI 信号才关闭 C5-1 并轮换 C5-0。所有 provisional 胜者仍需 fresh-seed confirmation。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T067 | Ch5 B1/B2/B3/C1 同预算 BER/GMI 与两轮自动收缩 | GW Step 4a-D bounded development | COMPLETE / `NO_METHOD_SIGNAL` / D |
| T068 | C4-1 scaled-unitary pilot-LS 的问题适配、竞争维度、机制与有限 claim | GW Step 4a A0/A′/A/B | COMPLETE / `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY` |

### 第十二批主线程裁决与工作线

1. T068 以 `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY` 收敛：C4-1 的 8→5 实自由度降方差问题、balanced-pilot 等价、IAO、baseline ladder 与有限 claim 均成立。独立审查指出 C2/C3/C5 三处可执行性歧义后，主控已把协变恒等式、nonunitary 理论对照和 exact-zero fail-closed 写清。
2. `14/18 dB × 2/4 pilots` 是在看结果前冻结的研究设计轴，不是待拟合的物理常数；只要不冒充某篇论文的 source reproduction，也不因结果临场更改，就不再作为 literature-authority blocker。T069 可以先过 C0–C5，再在同一任务内运行一次有界 BER headroom。
3. T067 Round 1 完成 64/64 windows；B2/C1 相对 B1 的 BER 点估计略低，但 BER/GMI CI 均跨 0，B3 明显退化。terminal=`NO_METHOD_SIGNAL`、grade=`D`、Round 2 未授权且未运行。C5-1 关闭，不加损伤或参数救场。
4. 独立 verifier 从 raw 绕过项目 reducer 重算 `max_abs_delta=0.0`、54 tests PASS；其 `PARTIAL` 只来自未触发的双 simple-winner 选择分支。该缺陷不影响本次负终态，且路线已关闭，故不为死代码另开修复。
5. CP011 并行开放 T069 与 T070。C4 若 scaled-unitary 或 ladder 中更简单的 deployable arm 对 plain LS 有稳定 BER 信号，按真实最简胜者形成有限 classical-migration 包；所有 deployable arms 无信号则轮换 C4-0。Ch5 从既有 C5-0 方法卡的候选级 Step 2 重新取证，不跳到实现。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T067 | Ch5 structured covariance held-out BER/GMI | GW Step 4a-D bounded development | COMPLETE / `NO_METHOD_SIGNAL` / D / `b791113` |
| T068 | C4-1 scaled-unitary paper dimensions | GW Step 4a A0/A′/A/B | COMPLETE / `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY` / `c86123a` |
| T069 | C4-1 corrected C0–C5；PASS 后一次预注册 BER headroom | GW Step 4a-D correctness + bounded development | READY |
| T070 | C5-0 LLR calibration 的候选级全文获取与 coverage closure | GW Step 2 acquire | READY |

### 第十三批主线程裁决与工作线

1. T069 的 C0–C5、13 项测试、4×64 raw、tune/eval 隔离和 truth firewall 已由独立上下文复核 PASS。C4-1 相对 strongest cheap B2 在两格 `Np=2` 与 `14 dB,Np=4` 显著改善；`18 dB,Np=4` 均值轻微退化但 CI 跨 0。
2. C4 的真实方法身份收窄为 scaled-unitary 公共增益—偏振矩阵联合估计。B2 与 C4 的偏振方向相同，不能包装为新旋转；B2 是真实廉价胜者且必须作为主 baseline 显示。
3. CP012 只开放 T071 一次 fresh confirmation：算法、B1/B2 参数、四格场景与终态规则全部冻结，只换 `7000/7100/7200/7300` 四组全新 seeds；development artifacts 只读，confirmation 独立落盘。
4. T070 继续按 CP011 原边界完成 C5-0 Step 2。它与 T071 并行，任何一条都不得等待另一条而擅自跨步；T070 通过后仍只开放 Step 3 精读，不直接实现。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T069 | C4-1 scaled-unitary correctness + bounded BER | GW Step 4a-D bounded development | COMPLETE / `C4_STRUCTURED_SIGNAL` / `PROVISIONAL_A` / `464df3d` |
| T070 | C5-0 LLR calibration 全文池与 coverage closure | GW Step 2 acquire | ACTIVE |
| T071 | C4-1 固定配方、全新 seeds 的单次 confirmation | fresh-seed confirmation | READY |

### 第十四批主线程裁决与工作线

1. T070 以 6 篇 qualified fulltexts 闭合 C5-0 Step 2，A/B/C 三桶为 `4/3/4`。唯一 P1 是 B0 与 matched reference 的文字混淆，已修为 mismatched `s=1/alpha=1` 对 `B_match/O1`，原独立审查者复核 PASS。
2. C5-0 不从“覆盖足够”直接跳实现。CP013 只开放 T072 对冻结六篇的 Step 3 精读，重点辨别 receiver-visible online calibration 与依赖 truth/offline GMI 的标定，并收敛至多一个 canonical Q#。
3. T071 已在 CP012 下合法启动且冻结配方不变，继续完成不受 epoch 更新影响。其实现对话只给 frozen terminal，必须再由独立上下文从 confirmation raw 重算后，主控才判断 Ch4 是否进入章级材料化。
4. 两线继续共享同一北极星：C4 负责短导频偏振解复用，Ch5 负责软信息可靠度；不为追求表面新颖性增加损伤、候选或高维自由度。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T070 | C5-0 LLR calibration 全文池与 coverage closure | GW Step 2 acquire | COMPLETE / `STEP2_READY_FOR_STEP3` / `f489438` |
| T071 | C4-1 固定配方、全新 seeds 的单次 confirmation | fresh-seed confirmation | ACTIVE / frozen run completed / package pending |
| T072 | C5-0 冻结六篇全文精读与 canonical Q# | GW Step 3 read | READY |

### 第十五批主线程裁决与工作线

1. T071 用四组全新 seed bases 一次完成 4×64 confirmation，冻结终态 `C4_CONFIRMED_STRUCTURED_SIGNAL`；没有调参、重跑 development、扩格或救场。另一上下文绕过 aggregate 从 raw 重算，19 tests、hash、fixed parameters 与 truth firewall 全部 PASS。
2. C4 按硕士级合同正式升为 `THESIS_METHOD_READY`。方法不是新旋转算法，而是短 balanced-pilot DP-(8,8)-16APSK 下的 scaled-unitary 公共增益—偏振矩阵联合估计；B2 最强廉价对手必须出现在章内。
3. Ch4 science 线到此停机。CP014 只开放 T073，把已冻结事实变成内部章级 fact matrix、蓝图、可编辑方法图和 raw-derived 结果图；不以“写作需要”为由补跑格子。
4. T072 已进入三路各两篇的只读精读，继续按 CP013 启动授权运行；不得因为 Ch4 已 ready 而降低 C5 的 receiver-visible、正确 baseline、BER/FER 与独立验证底线。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T071 | C4-1 固定配方、全新 seeds confirmation | fresh-seed confirmation | COMPLETE / `C4_CONFIRMED_STRUCTURED_SIGNAL` / `42643b0` |
| T071 independent verifier | raw-only CI/hash/firewall/method-entry audit | independent science verification | COMPLETE / PASS / P0-P1=`0/0` |
| T072 | C5-0 冻结六篇全文精读与 canonical Q# | GW Step 3 read | ACTIVE / 3×2 subagents running |
| T073 | C4 fact matrix、章结构、方法图与结果图材料化 | internal chapter evidence package | READY |

### 第十六批主线程裁决与工作线

1. T073 已形成 15 个文件、九类交付。独立 reviewer raw-only 重算、B2/C4 身份和两图审查无 P0/P1；两个视觉 P2 局部修复后由 reviewer 与主控实际 PNG 复核关闭，terminal=`CH4_WRITE_PACKAGE_READY`。Ch4 不再接收科学或材料化任务。
2. T072 完成 6/6 全文精读与唯一 `Q-C5-0`：post-Ch4→Ch3 known-pilot residual → per-frame global positive scalar → channel/extrinsic LLR → frozen LDPC。独立复核修正一处 receiver-visibility P2 后为 `PASS 0/0/0`。
3. C5-0 的强制风险不是一般 novelty，而是 B2 与 direct variance plug-in B3 的 max-log/APP 等价，以及相同目标平台是否已有九字段完整 recipe。CP015 只开放 T074 做 45 分钟、最多两轮的 Step 3.5；邻近场景或经典原子只压 claim，不自动 Kill。
4. T074 未收口前禁止 Step 4a、实现、仿真和正式正文；收口后若存活，下一包仍先做 paper dimensions/correctness contract，不直接跑 BER。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T072 | C5-0 冻结六篇全文精读与 canonical Q# | GW Step 3 read | COMPLETE / `STEP3_CLASSICAL_MIGRATION_READY_FOR_STEP3_5` / `c34a202` |
| T073 | Ch4 fact matrix、章结构、方法图与结果图材料化 | internal chapter evidence package | COMPLETE / `CH4_WRITE_PACKAGE_READY` / `c3b401d` |
| T074 | C5-0 exact target recipe、B2/B3 等价与 claim ceiling | GW Step 3.5 supplement | READY |

### 第十七批主线程裁决与工作线

1. T074 只运行 Round 1 并收口；未发现同一 DP-(8,8)-16APSK coherent-FSO 九字段完整 recipe，terminal=`STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM`。现有 online scaling、variance plug-in、coherent-optical 与 APSK likelihood 邻居只限制 claim，不自动关闭硕士级场景迁移。
2. max-log 在 uniform/common-variance/channel-only 合同内 B2=B3；exact APP 一般不等价，需逐 bit 核查。B3 是同信息预算硬对手，不得删除，也不得靠换名字把被吸收的 B2 留作独立方法。
3. 任务内 reviewer 修复三项 P1 后为 `PASS 0/0/1`；主 worktree 另一独立核查为 `PASS 0/0/3`。主控已修正唯一值得立即处理的 per-frame-scalar 歧义；剩余均为局部 P2/证据限制，不影响 terminal。
4. CP016 只开放 T075 纸面 Step 4a。首个解析停机点是当前 `alpha=0.75` fixed normalized-min-sum：无 clipping/quantization/offset 时公共正缩放正齐次。必须先证明自然 reliability mismatch、B0→O1 headroom 与非齐次作用链，才可另行授权 correctness 实现。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T074 | C5-0 exact target recipe、B2/B3 等价与 claim ceiling | GW Step 3.5 supplement | COMPLETE / `STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM` / `6b74f26` |
| T074 independent verification | 九字段、代数、性能语义与 terminal | independent science verification | COMPLETE / PASS / P0-P1=`0/0` |
| T075 | C5-0 natural mismatch、decoder headroom、B1/B3 吸收与 correctness contract | GW Step 4a A0/A′/A/B | READY |

### 第十八批主线程裁决与工作线

1. T075 以 `PAPER_DIMENSIONS_PASS_B2` 收口。方法身份不是新 LLR 理论，而是目标 DP-(8,8)-16APSK 星地相干链中、冻结/黑盒 LDPC 外部的 current-frame pilot-residual global LLR calibration。
2. 64-window residual variation 只证明自然 observation，不证明 held-out reliability 或 BER/FER。理想 fixed NMS 的公共缩放为零效应；B2 只可能经目标部署链的 fixed preclip/internal clip/filler 形成非齐次作用。
3. 内部 adaptive threshold/filler reparameterization 必须披露并限制 claim，但因其修改 decoder 内部，不作为 frozen-interface B2 的自动否决。B3 max-log 是 identity control，B3 exact APP 是同信息预算强 comparator/correctness 分叉；不拼成双方法。
4. 独立验收 `PASS / P0=0 / P1=0 / P2=1`；唯一 P2（旧 16QAM demapper preclip 被写成目标既成事实）已改为 APSK seam 的候选继承合同。
5. CP017 只开放 T076 的 C0–C6 correctness：16APSK label/sign/noise factor、APSK→LDPC interleaver/bit order、clip/filler placement、max-log B2=B3、exact-APP non-identity、NMS homogeneity 与 truth firewall。禁止 occurrence、headroom、BER/FER、调参和新损伤。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T075 | C5-0 natural mismatch、decoder headroom、B1/B3 吸收与 correctness contract | GW Step 4a A0/A′/A/B | COMPLETE / `PAPER_DIMENSIONS_PASS_B2` / `0bfdb1c` |
| T075 independent verification | final report、自然 residual 复算、吸收边界与 C0–C6 | independent science verification | COMPLETE / PASS / P0-P1=`0/0` |
| T076 | target APSK→5G LDPC receipt 与 B2/B3 action selection | GW Step 4a-D correctness-only | READY |

### 第十九批主线程裁决与工作线

1. T076 以 `CORRECTNESS_PASS_B2_ACTION` 收口：10 项 target correctness 与 3 项既有 LDPC 参考测试在任务 worktree 和主 evidence worktree 均 fresh PASS。目标 APSK mapping/label、LLR sign、`N0` 因子、coded grouping、live `out_int_inv`、16 filler、clip 顺序与 one-frame-one-scalar 均有 receipt。
2. 首轮外部独立复核真实发现 decoder 顺序错误与 B1 只存在于伪造 arm 两个 P1；任务以明确 RED→GREEN 补成真实 B1 action、live backend clip probe 与正确 rate-recovery→BP 顺序。修复后独立 reviewer=`PASS/P0-P1-P2=0-0-0`。初审 FAIL 保留在 V031，不用 consistency 掩盖 correctness 问题。
3. T076 只证明 action 合法。max-log B2=B3 继续保留；exact APP 四 bits 均有 nonidentity，B3 保留为同预算强 comparator。固定 clip/filler nonhomogeneity 不是 BER/FER 证据。
4. CP018 只开放 T077 一个继承 T066 的 frozen natural cell；按 pilot residual→held-out payload reliability、B0→O1、B1/B2/B3 三门顺序执行。FER 为主、BER 必报；任何门失败立即停，不换 SNR/pilots/window/损伤救场。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T076 | target APSK→5G LDPC receipt 与 B2/B3 action selection | GW Step 4a-D correctness-only | COMPLETE / `CORRECTNESS_PASS_B2_ACTION` / `8b6a644` |
| T076 independent verification | C0–C6、B1 真实 action、live order/clip 与 scope | independent science verification | COMPLETE / PASS / P0-P1-P2=`0/0/0` |
| T077 | 一个 frozen natural cell 的 reliability、coded headroom 与 B1/B2/B3 | GW Step 4a-D single-cell falsifier | READY |

### 第二十批主线程裁决与工作线

1. T077 以 `SINGLE_CELL_NO_HEADROOM` 收口。Gate 1 固定 128 帧 reliability rank signal 很强（`rho=0.9856654`，单侧 95% lower=`0.9758980`），说明 pilot residual 是有效观测；这不自动构成 coded 方法收益。
2. Gate 2 固定 512 帧 B0/O1 BER=`0.0492935/0.0533390`，`BER_B0-BER_O1=-0.00404549`、95% CI=`[-0.00556197,-0.00266070]`。O1 FER 只少 1 个 frame，无法抵消 BER 明确变差；目标 scalar-auxiliary oracle 没有 coded headroom。
3. Gate 3 按预注册顺序未开放，evaluation raw 只有 B0/O1；B1/B2/B3 不能被写成科学失败或已比较。C5-0 只按“无承重 headroom”关闭，不换 cell、不调 scalar、不补损伤救场。
4. 独立 raw reviewer 初审 P1 是摘要链无法 raw-only 重算；补 canonical `audit_pair_receipt/hash` 后复验 `PASS/P0-P1-P2=0-0-3`。三个 P2 只限制 truth mutation、seed bit-exact 与 resume 声称，不改变 terminal。
5. CP019 按 D056 既定顺序轮换 C5-5，但只开放 45 分钟 candidate-specific GW Step 1 authority reconciliation：冻结 Q#/IAO/baseline/fulltext gap/interface gate。禁止实现、仿真、补 decoder adapter 或偷跑 Step 2。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T077 | 单格 reliability 与 coded headroom falsifier | GW Step 4a-D | COMPLETE / `SINGLE_CELL_NO_HEADROOM` / `7e7f0b7` |
| T077 independent verification | split/hash/rho/BER/FER/CI/terminal | independent science verification | COMPLETE / PASS / P0-P1-P2=`0/0/3` |
| T078 | C5-5 reliability-prioritized decoder scheduling authority reconciliation | candidate-specific GW Step 1 | COMPLETE / `STEP1_C5_5_EVIDENCE_GAP_BOUNDED` / `4d2df71` |

### 第二十一批主线程裁决与工作线

1. T078 将 C5-5 从泛化“动态调度”收缩为 per-codeword reliability-driven iteration-budget allocation。Q#/IAO、truth firewall 与成本输出闭合；它只改变 decoder call budget，不改前端、demapper 或 CN equation。
2. Sionna per-call `num_iter` 使最小 adapter 有界且无需自写 BP；static `cn_schedule` 不是 receiver-driven dynamic priority，callbacks/state 也尚未进入项目 seam。
3. 最大吸收风险是 ordinary syndrome/CRC early-stop 与 equal-total-update fixed decoder。若后续只胜 fixed-20，不能升为主方法；必须在 Step 3/4a 把这两个 comparator 写进承重合同。
4. 当前唯一 blocking gap 是 DOI `10.1109/ACCESS.2019.2899106` direct scheduling 全文与至多 2 篇直接 budget/early-stop comparator 全文。CP020 只开放 T079 Step 2 acquisition；不得在同一包精读、裁决 exact collision、实现或仿真。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T078 | C5-5 Q#/IAO、absorption ledger 与接口门 | GW Step 1 | COMPLETE / `STEP1_C5_5_EVIDENCE_GAP_BOUNDED` / `4d2df71` |
| T078 independent audit | budget-only 身份、early-stop 吸收与最小 seam | independent science audit | COMPLETE / `EVIDENCE_GAP` / no file changes |
| T079 | 2019 direct scheduling + 至多 2 篇 budget/early-stop primary fulltexts | GW Step 2 acquisition | COMPLETE / `STEP2_C5_5_READY_FOR_STEP3` / `2426f50` |

### 第二十二批主线程裁决与工作线

1. T079 审计 3 个目标身份并冻结 2 篇 qualified Step 3 fulltexts：Liu et al. 2025 reliability-list-based CBP 直接覆盖 reliability-driven dynamic scheduling；He et al. 2021 NR-LDPC 直接覆盖 CRC/综合征早停、最大迭代预算与工程实现口径。
2. DOI `10.1109/ACCESS.2019.2899106` 没有取得合格全文。下载候选实际是 arXiv `cs/0702111v2` 的 2007 入侵检测论文，标题 overlap=`0.3333`；错误 source/content 已拒绝，仅保留 identity-mismatch receipt。P0 exact collision 因此仍为 UNKNOWN，不能写成“未发现完全相同”。
3. 独立 verifier 首轮发现 2024/2025 发表年、尾随空格与 line count 三项证据卫生问题；修复后复验 `READY=YES / P0-P1-P2=0-0-0`。接入主 worktree 后的第二次独立检查又抓到 binary-patch 管道损坏 PDF 与 registry 仍停 CP020；主控从 clean task worktree 精确恢复 PDF/content 并更新 registry，fresh PDF=`2,882,056` B、magic=`%PDF`、SHA=`FAB2C271...`，content SHA=`ED0B33DF...`。任务 commit=`2426f50dde12928c01a0b69651f2a4578414078d`。
4. CP021 只开放 T080：精读恰好两篇冻结全文，逐项裁决 dynamic scheduling、ordinary early-stop、per-codeword predecode budget allocation 与 equal-total-update 公平口径。不得扩大检索、实现、仿真或同包进入 Step 3.5。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T079 | 2019 P0 identity 审计 + 至多 2 篇 direct comparator 获取 | GW Step 2 acquisition | COMPLETE / `STEP2_C5_5_READY_FOR_STEP3` / `2426f50` |
| T079 independent verification | identity、全文质量、coverage、年份与 staged scope | independent evidence verification | COMPLETE / PASS / P0-P1-P2=`0/0/0` |
| T080 | 冻结两篇的动作链、early-stop 吸收与九字段碰撞 | GW Step 3 fulltext read | READY |

### 第二十三批主线程裁决与工作线

1. T080 完成冻结两篇 `2/2` 全文精读并以 `STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5` 收口。Liu 2025 是 decoder-internal check-belief residual→local update-order strong neighbor；He 2021 的 ordinary CRC/syndrome early stop 是 mandatory cheap comparator。两者均非 current-codeword LLR-derived predecode reliability→per-codeword `num_iter` cap 的完整 recipe，P0 2019 provenance debt 继续保留。
2. 独立内容 reviewer 初审 `PASS_WITH_P2 / 0-0-4`；四项 P2（v0 input、M-C-A easy-codeword 归因、CRC cadence、VVUQ 分母）修复后原 reviewer `RECHECK: PASS`。T080 精确 5 文件、task commit=`28262945417a7c264052ee85ccffeafea6a28710`。
3. 用户指出 Ch4 只有 14/18 dB 四格并不等于最终通信方法章完成：SNR 上界应由实用 pre-FEC 门限决定，百分比 BER 改善必须换成固定 BER 的 required-SNR gain；还需 pilot、机制、星地场景、结构边界和复杂度证据。D060 因此暂停 C5-5 Step 3.5，将唯一 foreground lane 改为 Ch4 production-evidence。
4. CP022 只做设计/preflight，不跑 smoke：核对 Ch3 正式 SNR/门限/湍流口径，审计 Ch4 参数化 seam、metrics、truth firewall、算量与 checkpoint 能力，冻结 smoke→production→独立验证设计。C4 action、B2 主对手、DP-(8,8)-16APSK 双偏振平台和有限 claim 不变。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T080 | 两篇 frozen fulltexts 的动作链、early-stop 吸收与九字段碰撞 | GW Step 3 fulltext read | COMPLETE / `STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5` / `2826294` |
| T080 independent content review | source→九字段→terminal 与四项 P2 修复 | independent evidence verification | COMPLETE / `RECHECK: PASS` |
| Ch4 production preflight | Ch3 authority alignment、simulator seam、章级证据合同与预算 | thesis production evidence design | IN_PROGRESS / CP022 |

### 第二十四批主线程裁决与工作线

1. T081 已把 Ch4 最终证据包冻结为五图三表和十项 gated tasks；旧四格只作 historical method-entry evidence，不与新 raw 混算。
2. 第一位独立 preflight reviewer 判 `NEEDS_REPAIR/P0-P1-P2=0-5-0`：corrected anchor 混入两个变量、B3_PSC 门不完整、Rytov/scintillation 语义错误、required-SNR uncertainty 不完整、三个结果相关规则未冻结。主控逐项修复后，第二位 verifier 又指出 Np4 CI、tau 分支和 rounded-parameter SI 三项 P1；再次修复后 fresh terminal=`CH4_PRODUCTION_PREFLIGHT_READY/P0-P1=0-0`。
3. 最短止损链冻结为 A1 exact historical-observation demapper replay 与 A2 new production-seam bridge。A1 必须 256/256 hashes 等同历史，只隔离 demapper；A2 才引入新 RNG/B3_PSC。任何一步失败都不扩损伤救图。
4. D061/CP023 只开放 T082 common demapper correctness repair。先以 failing test 证明 radius-OR 违反 full ML，再做最小实现修复和 direct-caller regression；本 checkpoint 禁止任何 BER replay/smoke/production。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T081 | Ch4 完整章证据设计、统计合同与止损门 | production-evidence preflight | COMPLETE / `CH4_PRODUCTION_PREFLIGHT_READY` |
| T081 independent reviews | 根因隔离、cheap comparator、RNG/statistics/scene/tuning | independent preflight verification | COMPLETE / repaired to `P0-P1=0-0` |
| T082 | common 16APSK exact-ML demapper TDD repair | correctness-only | READY / CP023 |

### 第二十五批主线程裁决与工作线

1. T082 以真实 RED→GREEN 闭合公共 16APSK hard demapper：冻结 inner-ray 点历史判错，512 点云有 17/2048 bit mismatches；最小 diff 删除 radius forcing 后 focused 3 tests 与指定 113 tests 全过。
2. 独立 reviewer 自建 constellation/oracle，使用不同 seed 核对 16,384 新 complex points，label/bit mismatch 均为 0；fresh common 69 tests 全过，P0-P1-P2=`0-0-0`。该 PASS 只证明正确性，不证明 C4 BER 信号。
3. D062/CP024 只开放 T083 A1 exact historical-observation replay。新 runner 必须 256/256 复现 T071 hashes，旧 raw immutable；只有 demapper/scoring identity 与 BER counts 可变。
4. A1 gate 固定为 pooled Np2 `C4-B2` CI upper `<0` 且两个 Np4 cell CI lower `<=0`。FAIL 立即停止完整 Ch4 production；PASS 才能另开 A2/new RNG seam。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T082 | common 16APSK global-ML demapper | correctness-only | COMPLETE / `DEMAPPER_CORRECTNESS_REPAIR_PASS` |
| T082 independent review | 16,384-point oracle、common regression、scope/hash | independent code verification | COMPLETE / PASS / P0-P1-P2=`0-0-0` |
| T083 | 256 historical observations corrected-demapper replay | A1 causal replay | READY / CP024 |

### 第二十六批主线程裁决与工作线

1. T083 exact replay 在 corrected global-ML scoring 下完成；256/256 observation identities 与 1280/1280 mechanism rows 保持历史一致，证明唯一科学变量确为 demapper scoring。
2. 四格 C4−B2 均为负；pooled Np2 95% CI=`[-0.00868396,-0.00433086]`，两个 Np4 cell 均无显著回归。独立 reviewer 从 raw 自建 parser/bootstrap 精确复算，P0-P1-P2=`0-0-0`。
3. 只读故事审查确认五图三表足以构成专业独立方法章；承重叙事必须写成“受约束矩阵估计+完整 receiver recipe”，不能写成“把一个奇异值换成平均值”。旧 `thesis-framework.md` 仍是 QPSK/载波同步/FPGA 目录，待正式 production 数字冻结后再同步，不在 correctness 阶段抢写。
4. D063/CP025 只开放 T084 production core TDD。先闭合 balanced pilots、RNG substreams、latent pairing、三档 authority、B3_PSC、mismatch 与 truth firewall，再另开 A2 BER bridge；本 checkpoint 不产生新 BER。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T083 | corrected-demapper historical observation replay | A1 causal replay | COMPLETE / `DEMAPPER_REPLAY_PASS` |
| T083 independent review | raw identity、机制量、bootstrap、hash/firewall | independent scientific verification | COMPLETE / PASS / P0-P1-P2=`0-0-0` |
| T084 | production kernel public interfaces and invariants | A2 correctness preparation | READY / CP025 |

### 第二十七批主线程裁决与工作线

1. T084 以 19-error initial RED、一次 nonfinite-scale RED 和 17-case provenance mutation RED 完成 production core TDD；最终 focused 46 tests PASS。
2. 独立初审发现 consumer 未核 namespace/turbulence metadata 的 P1 并判 INVALID；修复后 fresh review 重放 17/17 exploits 全 fail closed，final P0-P1-P2=`0-0-1`。P2 仅限制 B3 mechanism metric 标签。
3. D064/CP026 只开放 T085 A2 fixed bridge。四格共享 64 fresh latent IDs，pooled Np2 bootstrap 按 latent cluster 联合两个 SNR；C4 必须同时越过 B2 与 B3_PSC。
4. A2 仍是前置门而非 thesis data。任何 cheap-comparator fail 都直接停止 full production，不借扩样、换轴或选择性统计救场。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T084 | production kernel public interfaces/invariants | A2 correctness preparation | COMPLETE / `PRODUCTION_CORE_CORRECTNESS_PASS` |
| T084 independent review | RNG/B3/mismatch/truth oracles + provenance exploit | independent code/science verification | COMPLETE / repaired to PASS / P0-P1-P2=`0-0-1` |
| T085 | fixed 4×64 new-latent bridge with B3_PSC gate | A2 production-seam bridge | READY / CP026 |

### 第二十八批主线程裁决与工作线

1. T085 canonical raw 仅执行一次；独立 raw-only reviewer 对 64 IDs×4 cells×5 arms、128/128 pairing、64-cluster bootstrap与 frozen hashes复算为 P0-P1-P2=`0-0-0`。生成器后置 authority-validator 修订造成 byte-level generation binding=`PARTIAL`，但未发现 scientific execution 路径或 immutable raw 被修改。
2. 预注册强门真实失败：C4−B3_PSC pooled Np2 95% CI 跨 0，terminal=`CHEAP_COMPARATOR_NOT_CLEARED`。C4−B2 则显著为负；B3−B2/B0 的探索性独立 CI 在四格及 pooled Np2 全部严格为负。
3. 主线程按 D031/D032 的硕士级标准与 D060 的成章优先级，不隐藏 B3、也不让它一票否决。C4/B3 被统一重判为“方向估计 + 两种尺度准则”的一个方法族：C4 是 channel-domain 无参数主变体，B3 是 receiver-domain pilot-calibrated 强变体/ablation；两者不能冒充两个独立贡献。
4. D065/CP027 只开放 T086：disjoint tuned-B2 development、结构 smoke 与 scientific manifest/execution-lock 设计冻结。formal 128-window production、作图和正文仍关闭。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T085 | fixed A2 C4-vs-B2/B3 stop gate | A2 production-seam bridge | COMPLETE / `CHEAP_COMPARATOR_NOT_CLEARED` / raw immutable |
| T085 independent review | raw census/pairing/bootstrap/hash/terminal + exploratory B3 signal | independent science verification | COMPLETE / artifact PASS / science gate FAIL / P0-P1-P2=`0/0/0` |
| T086 | tuned-B2 development、minimal smoke、scientific manifest freeze | thesis-grade family production preparation | READY / CP027 |

### 第二十九批主线程裁决与工作线

1. T086 canonical tuning只运行一次，独立raw-only复算12个objective最大差0；moderate/Np2选择tau=.5，其余11格tau=1。tuned B2未触发12/12 dominance stop。
2. ID20999 tuning smoke与ID21999 formal-structure smoke均在所有worktree外运行；delta0 H/observations exact引用与positive-delta同噪声构造闭合。
3. receipt stale-test P1以同一immutable raw重归约修复；raw/aggregate不变。scientific manifest唯一冻结，SHA=`417f3348...21079`，future T087 hashes保持null。
4. D066/CP028只开放T087 formal execution seam TDD、ID29999全网格单latent smoke与唯一execution lock；128 formal IDs继续禁止。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T086 | tuned baseline、structure smoke、scientific manifest | production freeze | COMPLETE / `CH4_FAMILY_PRODUCTION_FREEZE_READY` |
| T086 independent reviews | 12 tau raw复算、receipt/hash、manifest、tests | independent verification | COMPLETE / PASS / P0-P1-P2=`0/0/3` |
| T087 | formal runner/reducer/tests、ID29999 smoke、execution lock | formal execution seam | READY / CP028 |

### 第三十批主线程裁决与工作线

1. T087 runner/reducer/entry 完成 TDD 与多轮独立静态修复；唯一 ID29999 OS-temp smoke 返回 `FORMAL_SMOKE_STRUCTURAL_PASS`，独立 raw-only census=`1/3/119/595/ref1`，未产生论文数字。
2. 首个 tracked lock SHA=`3942883a...a45a492` 的所有内容绑定均正确，但 lock 存在后的 fresh focused suite 仅 `17/19`：两项pre-freeze测试永久断言canonical lock不存在。独立终态=`CH4_FORMAL_EXECUTION_SEAM_INVALID/P0-P1-P2=0-1-3`，formal IDs未开放。
3. D067/CP029只开放T088 final-state self-consistency repair：保留runner/reducer/entry与smoke，修测试的absent/present双态语义，exact删除无效lock并生成一个replacement lock；不重跑smoke、不改scientific manifest、不运行formal IDs。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T087 | runner/reducer/tests、ID29999 smoke、首个tracked lock | formal execution seam | COMPLETE / smoke PASS / final lock INVALID |
| T087 independent review | temp raw复算、lock binding、post-lock fresh tests | independent verification | COMPLETE / `0/1/3` / NO-GO |
| T088 | final-state-safe tests、invalid lock replacement | execution-lock repair | READY / CP029 |

### 第三十一批主线程裁决与工作线

1. T088在旧invalid lock存在态复现`17/19`并修至`19/19`；旧lock exact删除后absent态、新replacement lock present态同一suite均`19/19`，没有skip/xfail。
2. replacement lock唯一生成，SHA=`095dc989...227987`，独立final P0-P1-P2=`0-0-3`；manifest、runner/reducer/entry/tests、deps、HEAD、environment与population actual match。
3. D068/CP030只开放T089 exact `--formal`一次生成canonical raw并停机；reduction、grade、作图与正文继续关闭。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T088 | final-state-safe tests与replacement lock | execution-lock repair | COMPLETE / READY / P0-P1-P2=`0/0/3` |
| T089 | frozen 128-latent no-override raw | canonical formal production | READY / CP030 |

### 第三十二批主线程裁决与工作线

1. T089唯一exact formal进程exit=0、wall409.5s，raw SHA=`642c7ae9...a72c5b`、size=89,419,500 bytes，checkpoint成功清除。
2. 独立reviewer未导入runner/reducer，穷举namespace、cell-latent、H/observation/action hashes、cross-Np pairing、truth与delta0；terminal=`CH4_CANONICAL_FORMAL_RAW_READY/P0-P1-P2=0-0-3`。
3. D069/CP031只开放T090 canonical reducer一次与独立raw-only统计复算；尚未接收任何正式BER、grade或图表结论。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T089 | frozen 128-latent canonical raw | formal production | COMPLETE / RAW READY / `0/0/3` |
| T090 | crossing/bootstrap/grade与独立raw复算 | formal reduction | READY / CP031 |

### 第三十三批主线程裁决与工作线

1. T090 pre-run门全PASS，但direct entry在内存reduce完成后、首次publication import处因空PYTHONPATH失败，exit1、无aggregate/receipt/tmp；不能称pre-statistics。
2. raw/manifest/lock与11项authority bytes保持exact。独立无写入probe确认显式`PYTHONPATH=repo;simulation;seam`可闭合import且environment不变。
3. D070/CP032只开放T091一次corrected publication attempt与独立raw-only统计复算；不改bound code、不重跑formal。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T090 | direct canonical reducer | formal reduction | COMPLETE / `FAILED_PRE_WRITE_IMPORT_PATH` / no artifacts |
| T091 | explicit-environment canonical publication + independent stats | reduction repair | READY / CP032 |

### 第三十四批主线程裁决与工作线

1. T091 corrected publication 只执行一次并返回 grade A；aggregate/receipt 与 raw/双锁绑定 exact，无 tmp。
2. 独立 reviewer 直接从 immutable raw 重算全部正式统计；757 个科学节点最大绝对差 `0.0`，C4 在 moderate Np2/Np4 相对 tuned B2 的 required-SNR gain 均有 95% CI lower `>0`，chapter gate=true。
3. D071/CP033 将唯一前台切到 Ch4 论文材料化：先生成完整 formal figures/tables 并独立核数，再写完整第四章并由不同 reviewer 做论文级审查。禁止新增实验、改科学口径或恢复 Ch5。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T091 | canonical publication + raw-only statistics | formal reduction | COMPLETE / GRADE A / `0/0/3` |
| T092 | canonical figures, tables and traceable plot data | chapter materialization | READY / CP033 |
| T093 | complete Ch4 draft and independent paper-level review | thesis writing | WAIT T092 |

### 第三十五批主线程裁决与工作线

1. 用户明确收窄目标为“先准备材料，正文以后自行组织”；T093 未启动并冻结为 `PAUSED_NOT_EXECUTED`。
2. T092 已生成五组 formal 结果图、三张正文候选表、五份 CSV 与确定性脚本；主线程已做第一轮视觉审查并修正图例重叠、strong 场景裁轴、误差棒标签和 B3 标量语义。
3. D072/CP034 只允许独立核数/核图与作者素材卡更新；材料包 ready 后停机，不自动进入正文或总纲。

| 任务 | 唯一决策域 | formal step | 状态 |
|---|---|---|---|
| T092 | figures/tables/CSV/scripts | author materialization | COMPLETE / T094 PASS |
| T093 | complete chapter prose | thesis writing | PAUSED_NOT_EXECUTED / D072 |
| T094 | independent full-data/visual/semantic audit | material verification | COMPLETE / V047 / `0/0/3` |
| T095 | formal facts/method/claim/figure/material-index cards | author material finalization | COMPLETE / T096 PASS |
| T096 | independent author-material package review | material verification | COMPLETE / V048 / `0/0/0` |

### 第三十六批主线程裁决与工作线

1. 用户确认六章一级标题采用“两个具体方法章 + 一个共享 FPGA 实现章”的命名，不再沿用开题阶段宽口径的“……方法研究”标题。
2. D074/CP036 只开放无图导师文字版的内容合同讨论；目标是先让导师判断题目、章节、方法身份和工程闭环，不在结构获认可前加入图件或展开完整正文。
3. Ch3/Ch4 证据边界保持不变，尚未联合验证；第五章只有在形成真实级联 FPGA 信号处理链时才能保留“信号处理链”的章名。

| 工作项 | 当前状态 | 下一门 |
|---|---|---|
| 六章一级标题 | LOCKED / D074 | 导师反馈后再调整 |
| 无图导师文字版 | PROPOSE / NOT DRAFTED | 用户批准内容合同 |
| 二级标题、图件、正式正文 | PAUSED | 结构与文字版范围确认 |

## 决策引用

- D040：共同 DP-(8,8)-16APSK coded coherent FSO 平台。
- D041：正确性门→开发矩阵→PROVISIONAL 分级→fresh confirmation→FINAL 分级。
- D042：13 张机制级卡仅为设计地图。
- D043：一轮三线只读战略调研、主线程单点综合（新建）。
- D044：恢复连续方法生产，routine 阶段不再等待用户门（新建）。
- D045：两章进入 Step 4a-D 实现与 correctness 门，性能实验继续关闭（新建）。
- D046：开放 Ch4 有界开发与 Ch5 真实残差桥，禁止为结果扩网格（新建）。
- D047：接受 C4-2 科学停机，轮换 C4-1；Ch5 bridge 修复并独立复验后才跑一格 occurrence（新建）。
- D048：接收 Ch5 occurrence 并开放 C4 paper gate / Ch5 bounded development（新建）。
- D049：接收 C4 bounded paper PASS、关闭 C5-1 并轮换 C5-0（新建）。
- D050：接收 C4-1 provisional 信号，只开放冻结配方 fresh confirmation（新建）。
- D051：接收 C5-0 Step 2，只开放冻结六篇全文的 Step 3 精读（新建）。
- D052：C4-1 冻结为 thesis-method-ready，只开放章级证据材料化（新建）。
- D053：接收 Ch4 写作包与 C5-0 Step 3，只开放 bounded exact-recipe 闭包（新建）。
- D054：接收 C5-0 Step 3.5，只开放纸面 Step 4a 与解析停机审计（新建）。
- D055：接收 C5-0 Step 4a 纸面 PASS，只开放目标 APSK→LDPC correctness seam（新建）。
- D056：接收 C5-0 target codec correctness，只开放一个预注册自然单格（新建）。
- D057：接收 C5-0 单格无 coded headroom，关闭该形态并轮换 C5-5 Step 1（新建）。
- D058：接收 C5-5 Step 1 bounded evidence gap，只开放窄 Step 2 获取（新建）。
- D059：接收 C5-5 Step 2 有界全文池，只开放冻结两篇的 Step 3 精读（新建）。
- D060：接收 C5-5 Step 3 并暂停 Ch5，重开 Ch4 生产级章证据扩展（新建）。
- D061：接收 Ch4 production-evidence preflight，只开放 16APSK demapper correctness repair（新建）。
- D062：接收 common 16APSK demapper correctness repair，只开放 A1 historical-observation replay（新建）。
- D063：接收 corrected-demapper 历史重放，只开放 production core TDD（新建）。
- D064：接收 production core correctness，只开放 A2 production-seam bridge（新建）。
- D065：接收 A2 廉价比较器未清除事实，将 Ch4 收缩为方向—尺度解耦方法族并开放一次生产冻结包（新建）。
- D066：接收方向—尺度方法族 production freeze，只开放 formal execution seam（新建）。
- D067：T087 科学执行链保留、首个 tracked lock 作废，只开放终态自洽修复（新建）。
- D068：接收 replacement execution lock，只开放一次 canonical formal raw production（新建）。
- D069：接收唯一 canonical formal raw，只开放一次归约与独立统计复算（新建）。
- D070：T090 pre-publication import failure，不改bound code并开放一次显式环境归约（新建）。
- D071：接收 Ch4 Grade A 正式证据，只开放图表与完整章节材料化（新建）。
- D072：Ch4 暂不写完整正文，只闭合可供作者组织的正式材料包（新建）。
- D073：接收 Ch4 作者材料包并停在可组织状态（新建）。
- D074：锁定学位论文一级章名并转入无图导师文字版讨论（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。D074 已按用户显式确认登记范围变更；当前只讨论无图导师文字版的内容合同，完整正文、图件、Skill/controller、Ch5与新实验均不在当前范围。

## 后续

Ch4 作者材料包已由 T096 独立终验，P0/P1/P2=`0/0/0`。无图导师文字版的内容、篇幅、方法强度请示与生成门控已按用户要求拆入 `2026-08-30-thesis-advisor-text-outline`；本专题不再起草该稿，T093/C5-5 保持暂停。
