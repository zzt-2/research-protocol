# Voice — 星地相干 FSO AMC Groundwork

> 用户/导师原话档案，按日期。除零信息推进/应答外都收，不去重。
> 仅标 →产出(可选) 和 ⟶冲突；导师/批注标来源。原话占主体，不加说明。
> 本轮为执行提示词派发任务，用户原话来源 = 执行提示词文本（paste-attachment），非对话内即时原话。

## 2026-08-02（执行提示词关键约束，verbatim）

- "在'星地相干自由空间光通信 + Gamma-Gamma 大气湍流 + 真实编码链/信息不确定性'背景下，寻找一个有希望成为毕业论文第二项贡献的自适应编码调制或链路适配问题。" → D001（原始目标冻结）
- "本轮只做 Groundwork Step 1"
- "不得进入 Step 2、Step 3、Step 3.5、Step 4a，不下载/精读全文，不设计方法，不跑仿真，不写 Go/No-Go，不产生 METHOD_SIGNAL。"
- "本轮不要再修改 Skill。"
- "不得下载全文。Step 2 acquisition 只准备清单，不执行。"
- "下一合法动作只能是：'主控验收 Step 1 后，进入 Groundwork Step 2 全文获取。'"
- ⟶ 旧边界（防换名重开）："不要把这些局部历史结果扩张成'所有 AMC 都无效'"——继承但不复活 dead-end #1-#9。

## 2026-08-02（Phase A+B 执行提示词，verbatim，paste-attachment 2026-08-02-214730）

- "你负责在一个对话内完成：A. AMC Groundwork Step 1 科学完整性限定修复；B. 修复通过后立即继续 Groundwork Step 2 全文获取。不要在 A 完成后停止。" → CP002/D002
- "Phase A 经独立 verifier PASS 后，立即进入 Phase B；不得只修文档后结束。"
- "L124 不是简单删除"——"修复前状态必须为 `UNVERIFIED_BIBLIOGRAPHIC_HIT`。"
- "修订后不得继续声称'4 个机制不同族'。至少改成：1. A_MCS_POWER_CONTROL… 2. B_HARQ_IR_RATE_ADAPTATION… 3. C_COHERENT_TX_ADAPTATION_UNVERIFIED…" → D002
- "F1 并非完全避开旧 0.09 dB MCS 天花板" → D002 headroom 纠正
- "'直接竞品 0 篇确认'改为 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`" → D002
- "不把搜索未命中解释成真实空白。"
- "补做最多 4 个别名 collision query，限定为 Step 1 修复，不扩成新地勘…如果产生新直接竞品，加入 Step 2 shortlist；不重新制作 209 条大表。"
- "Step 2…≥5 篇核心论文成功转为合格 content.md…若不足 5 篇或关键直接竞品被付费墙阻塞，诚实停在 `STEP2_BLOCKED_BY_COVERAGE_GAP`。不要进入 Step 3。"
- "禁止用 WebReader、ResearchGate、Scholar 页面抓全文。"
- "下一合法动作只能是：Step 2 PASS：主控/用户确认覆盖面后进入 Step 3；Step 2 BLOCKED：用户补充关键全文或确认当前覆盖面。禁止直接进入 Step 3。"
- "四个既有未跟踪 p05_run*.log 不修改、不暂存、不删除。"

## 2026-08-02（Phase A+B 执行提示词纠偏轮，verbatim，paste-attachment 2026-08-02-230536）

- "当前 Step 2 不是 PASS，而是 STEP2_BLOCKED_BY_COVERAGE_GAP。" → D003
- "已获取的 6 篇只通过文件/转换质量门；当前保守核心集只有：L023/L096/L146" → D003
- "L075 标记为 SEMANTICALLY_DISPUTED_PENDING_FULL_READ，不预判为纯 classification，也不提前计入核心。" → D003
- "L165 是 AO/物理实验边界；L090 是否存在真实运行时 adaptation 待全文语义核查，均不得先计核心。" → D003
- "L124 是关键 coherent-FSO AMC 直接竞品；没有全文时，coherent-C 族不得通过问题/新颖性判断。" → D003
- "允许在其他 ≥5 篇核心全文齐备后推进 A/B 两族 Step 3，不允许因 L124 付费墙让全部 Groundwork 无限停滞；但必须显式保留 C_L124_FULLTEXT_BLOCKED。" → D003
- "以上以新 D### 取代当前矛盾状态，不改写历史 checkpoint。"
- ⟶ 推翻 R002/H001 "Step 2 PASS / 6 篇全部核心 / A/B/C 三族已全部覆盖" 的乐观判定。
- "Safi 2019 很可能已经覆盖'GG + channel-estimation error + adaptive coding/power'，不得再把这一宽泛问题包装成空白。"
- "Galijasevic predictive adaptive LDPC 很可能覆盖'反馈时延/信道预测 + 动态码率'，必须确定剩余切片。"
- "重点寻找的不是'没人做过 AMC'，而是：现有 M 在星地 coherent/GG/coded-chain 的具体 C 下因 A 产生可验证失效，而且现有直接竞品没有解决。"
- "不使用 oracle headroom 作为 Go 判据。"
- "不进入 Step 3.5/4a，不跑 MVE，不提出最终算法。"
- "若无 Q# 全过，终态为 STEP3_NO_VALID_PROBLEM，不包装空白、不设计方法。"
- "全程一次统一 commit，不 push。"

## 2026-08-03（本轮执行提示词关键约束，verbatim，转述自执行提示词文本；非对话内即时原话，做触发锚）

- "本轮在一个对话内完成：1. 用仓库现有 Nguyen 2024 全文解除 Step 2 blocker；2. 重判 Step 2；3. 若五篇 CORE 门成立，立即完成 GW Step 3 全文精读；4. 到 Step 3 终态停止，不进入 Step 3.5/4a，不设计方法、不跑仿真。" → D004
- "Nguyen 2024 正式身份：…IEEE Transactions on Aerospace and Electronic Systems, vol. 60, no. 5, 2024, DOI 10.1109/TAES.2024.3403809。"
- "保留原始 provenance，禁止声称它是公开 OA；正文页脚显示 IEEE Xplore 机构授权下载。" → D004 provenance
- "L124 全文仍缺，因此必须保留 C_L124_FULLTEXT_BLOCKED。" → D004
- "Safi 2019 无全文，仅作 PROVISIONAL_DIRECT_COMPETITOR，不计五篇门槛，也不得据摘要推导实现细节。" → D004
- "全文精读必须委托 fresh-context 子 agent；最多同时 3 个，每个不超过 15 分钟。主线程只负责问题框定、结构化汇总和最终判断。"
- "L124/Safi 全文缺失时：不允许 coherent-C 族或 Safi 邻近切片通过 novelty closure；不得以题目、摘要或引用描述替代全文事实。" → D004
- "Step 3 终态只能二选一：STEP3_PASS_WITH_VALID_Q 或 STEP3_NO_VALID_PROBLEM。"
- "禁止把这些宽泛问题重新命名成空白。"
- "不修改 Skill；不修改 dormant receiver campaign；不碰四个既有 p05_run*.log；单次统一 commit，不 push。"

## 2026-08-03（本轮执行提示词关键约束，verbatim，paste-attachment 2026-08-03-105947）

- "继续 AMC Groundwork。本轮一次完成：1. 纠正 Step 3 语义门误用；2. 按协议唯一四判据重判 Q#；3. 完成 GW Step 3.5 定向补充检索和竞争闭包；4. 给出是否存在可进入 Step 4a 的问题。5. 到 Step 3.5 终态停止，不进入 Step 4a/MVE，不设计方法、不跑仿真。"
- "不接受当前：STEP3_NO_VALID_PROBLEM。原因不是论文读取失败，而是 Step 3 使用了错误的判据并产生循环门控。" → D005
- "协议唯一合法的问题四判据必须从 owner 逐字读取，不得按本轮 prompt 转述自行重写：stages/glossary.md、templates.md。" → D005 / R001
- "`problem_truth/actionability/novelty/thesis_fit` 不是 owner 定义的四判据，不得继续作为 Step 3 terminal gate。" → D005
- "已知其核心含义为：1. 存在明确、具体的 M-C-A 技术矛盾；2. 能形成可复用的方法产出；3. 有近期、真实的 baseline；4. 能量化对标。"
- "Step 3 要求的是文献支持、具体、可证伪的失效假设 A；Step 3 不要求已经用 MVE 证明退化；Step 3.5 负责定向补充检索、相邻工作和 novelty closure；Step 4a 才负责性能间隙、方法适配性和核心假设验证。"
- "原 Q1…保持 WEAK_SCENARIO_MIGRATION，不自动晋级。"
- "原 Q3…保持 TOO_BROAD_MECHANICAL_COMBINATION，除非收窄成单一 baseline、单一 load-bearing assumption 和单一可观察失效。"
- "Q4 Safi、Q5 L124 在无全文时继续 BLOCKED。"
- "论文自列 future work 不等于 novelty 自动失败；它只能作为问题原料，仍须做竞争闭包。"
- "不得因为'尚无 MVE'否决 Q-A/Q-B。"
- "每个 Q 至少：2 组不同表述的专属 query；forward/backward citation 检查；直接竞品、近邻竞品、反例三类筛选；优先检查最近五年正式发表论文。"
- "每篇最多三类合法获取路径，失败即止损，不绕过访问控制。无法获取时保留 blocker，不根据摘要推断实现细节。"
- "只有至少一个 Q 为 SURVIVES_STEP3_5，下一合法动作才是 Step 4a。不得在本轮启动 Step 4a。"
- "若 Q-A/Q-B 都失败：不制造第三个弱 Q；终态为 STEP3_5_NO_SURVIVING_PROBLEM；交用户决定调整条件 C、换 AMC 子族或停止该方向。"
- "V005 保留历史，不删除；标明它验证的是本地自写合同一致性，没有核对 canonical criteria owner，因此科学语义层失效。"
- "但留下回归候选：'verifier 必须核对 canonical criteria owner，不能只验证本地 prompt/contract 自洽。'"
- "不修改 dormant receiver campaign；不碰四个既有 p05_run*.log；单次统一 commit，不 push。"

## 2026-08-03（Step 4a 执行提示词，来源: paste-attachment 2026-08-03-124917）

- "进入 AMC Groundwork GW Step 4a。" → S006
- "当前主控优先项为 Q-A；Q-B 暂存。"
- "Q-B 仅完成 A0。不得并行搭建其完整 testbed。"
- "若 Q-A 出现致命项，则不运行 Q-B MVE，也不制造第三个 Q；提交 Pivot/Kill recommendation。"
- "任何数字必须标：EMPIRICAL；EXTRAPOLATED；ARGUMENT_ONLY。外推和论证不能单独支撑 Go。"
- "Galijasevic DOI/题名/正式 venue 的异常；其公式、码率集合、预测输入和反馈模型必须从原 PDF 核对，不得只依赖 markdown 摘要。"
- "Safi 和 L124 全文仍缺：Safi 只作 UNVERIFIED_DIRECT_COMPETITOR；不根据摘要推断实现细节。"
- "A0/A′/A/B 任一致命，立即停止，不得靠 MVE 翻案。"
- "Go/No-Go 最终决定属于用户；执行者只能提交 recommendation。"
- "创新只能落在'简单先验覆盖低且改善空间 ≥5%'的维度。"
- "若 B2/B3/B4 已在主指标上覆盖候选或 oracle 空间的 ≥95%，直接 RECOMMEND_KILL_OR_ENGINEERING_COMPONENT。不得为了保留复杂方法而弱化传统 baseline。"
- "Oracle 只作 Kill/headroom bound，不作 Go 判据。"
- "禁止因为现有 `_gg_time.py` 名字相似就直接复用。调用链语义不一致则在 MVE 前 BLOCKED。"
- "不得在本轮新建真实 LDPC decoder。若真实 decoder 是验证该假设不可替代的承重前提，应停止为 INFRASTRUCTURE_BLOCKED，而不是搭建多日工程。"
- "executor 不能自行最终 Go/No-Go，只能提交 recommendation，等待用户确认。"
- "即使本轮 RECOMMEND_GO，也不得宣称 Groundwork 完整闭合；缺少的 3 篇需在进入 Step 5 前补齐或由用户明确处理。"
- "不得覆盖旧 receiver feasibility_report。不得修改 common/、params.py、正式论文结论、Skill 或 dormant receiver campaign。四个既有 p05_run*.log 不动。"
