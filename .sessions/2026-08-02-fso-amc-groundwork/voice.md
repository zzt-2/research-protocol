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
