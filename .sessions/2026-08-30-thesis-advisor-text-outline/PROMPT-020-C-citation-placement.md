# PROMPT-020: 加密期 C 批——参考文献落位（文献批对话执行）

> 来源: S014 + D037/D041 | 日期: 2026-09-07
> 前提: F1a/F1b/F2 已完成；正文基线 = worktree commit 279865a；治理编号本批 = S015 / D042 / V028
> 执行方: 文献批对话（PROMPT-010 线）；唯一入口 = 主仓 `毕设/写作材料/bib-phaseC-落位任务报告.md`

## 提示词正文（用户粘贴到文献批对话）

请执行参考文献落位批（Phase C）。全程自主推进不中途提问；拿不准的记入"待用户拍板项"。

**启动时使用 session-governance 报到**，读：`topic-index.md`（thesis-advisor-text-outline 专题）、最新 S###（F2 批记录）、`decisions.md` 的 D037—D041、`voice.md`。专题目录：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.sessions\2026-08-30-thesis-advisor-text-outline\`。

**唯一执行依据（必读，按它走）**：`D:\code\study\research-protocol\毕设\写作材料\bib-phaseC-落位任务报告.md` §1—§6（纪律/资产地图/目标数字/候选池/六步流程/禁用清单）+ `毕设\写作材料\bib-logs\ledger.md` 总台账。

**当前正文状态（比落位报告写作时新）**：
- TODO 占位 46 处：Ch1 31 / Ch2 11 / Ch4 4（F1/F2 批未新增）；全部待换核实键。
- 实键 34 个（Ch1 30/Ch2 8/Ch3 10/Ch4 2）；扩容后正文汉字 ≈56.6k，各节位置以"节名+段落主题"为准（报告已约定行号漂移规则）。
- F1 批新增了公式段（Ch2/3/4/5），F2 新增 14 张表——落位位置若与这些新内容相关（如 Ch4 结构约束推导段），优先用 D4 方向候选补强。

**任务**：按落位报告 §5 六步执行——TODO 映射→对号（按谱系挑不是全塞）→数量对账（目标 170–180 总量 / Ch1 130+ / 方法章各 20–30）→落位（一句话内插入 [@key]，不改句）→确定性复查（报告 §1.4 三查）→台账更新（L005）。

**硬边界**：
1. 只做"一句话内插入 [@key]"级改动；句子结构/事实/数字零改动；§2.6/§2.7 配额继续生效（落位不增加连接词与防御句）。
2. 只用 ledger 状态为核实:Crossref/REPAIRED/OK(VB) 的键；核实:未 与 TODO 修复清单禁用。
3. 原有 34 实键不动（petkovic2022 已修正键不变）。
4. 修改对象=六章 md（worktree）+ references.bib 不动（库已就绪）+ ledger 更新；改前每章 `cp {NN}-*.md {NN}-*.md.bak-C`。
5. 落位后确定性复查：TODO- 残留=0；每键在 references.bib；键集合变化=白名单内新增；标题/\tag/表题注/图引用计数不变。
6. 本批与 F3 图批**不并行**（先后执行，避免同文件踩行）——你跑完 C，图批才开。

**治理收尾**：S015/D042（登记落位裁量）/voice/topic-index/commit（只 add 本批文件）。交付报告：落位总数、TODO 清零确认、分章引用数 vs 目标、复查三查结果、待拍板项（含两个中文出处缺口）。不宣称定稿。
