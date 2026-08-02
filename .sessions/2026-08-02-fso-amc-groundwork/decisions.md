# Decisions — 星地相干 FSO AMC Groundwork

> 架构决策、方向选择、路线失败记录。每条有取代/被取代字段形成血缘链。旧决策标 `superseded` 不删。

## D001: 新系统层范围与旧轴边界

> 2026-08-02 | status: active | 取代: 无 | 被取代: 无

**决策**: 本专题范围 = 星地相干 FSO + Gamma-Gamma 湍流 + 真实编码链/信息不确定性背景下的**自适应编码调制 (adaptive modulation and coding, AMC) 或链路适配**问题，作为毕业论文潜在第二项贡献的独立 Groundwork。明确**不属于**旧 receiver method-production campaign（载波同步/均衡/双偏振）；旧 campaign 的 negatives 不是 AMC 证据，旧工程资产（P08-R2 LDPC/prefix-LS/bit-true/info-boundary）只作可复用工程资产，不引用为 AMC 科学结论。

**边界（继承历史 dead-end，逐条见 topic-index dead-end ledger）**:
1. 不复活 ISL AMC prediction（确定性信道输给简单方法，`domain-comms.md:243-247`）。
2. 不复活链路自适应反馈环（反馈延迟 > 相干时间 2-10ms，TL-03）。
3. 不重新包装 ③ MCS 排程窄切片（oracle 上界 0.09 dB）。
4. 不复活"AMC + CPR 联合设计"（ω_n 跨调制一致使前提崩塌，C4-12）。
5. 不把自适应交织/纯PS/N1/coded-chain repair 换名冒充 AMC。
6. 不把 P08-R2 工程资产当 AMC 科学证据。
7. 新 AMC 须不同系统层真实动作，不能是既有 DA/NDA 自适应 CPR 换名。
8. 检索须识别并排除 "automatic modulation classification" 假命中。
9. 须解耦 AMC↔Ch4 BER 循环依赖（前馈或独立量度）。

**依据**:
- 用户执行提示词 §四"必须继承的历史边界"（8 条）。
- FR-26 核验：8 条中 #1/#2/#3/#6/#7/#8/#9 + #4 经 grep/Read 在 cited 文件确认；#5 经 registry 专题边界确认（详见 topic-index dead-end ledger 证据指针列）。
- `method-production-campaign-thesis-map.md`（A/B/C 级资产分级）。
- master-state.md §2 当前控制面桥接（AMC 须另开专题）。

**触发原话**: 无（技术推导 + 用户执行提示词派发；用户本轮未给态度原话，voice.md 记执行提示词关键约束 verbatim）。

**影响**: 锁定本专题范围与旧轴隔离；R001 候选族须逐条对照本决策的 9 条边界打勾。

## D002: Step 1 科学完整性限定修复 — 候选族修订 + identity 审计 + provenance receipt

> 2026-08-02 | status: active | 取代: 无（修订 R001 候选族地图与 Step 1 计数口径，不取代 D001 范围） | 被取代: 无

**决策**: 对 GW Step 1 做**限定完整性修复**（不撤销 Step 1）。Step 1 状态从 `STEP1_DONE` 修订为 `STEP1_ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR`。具体修订：

1. **候选族地图从 4 族（F1-F4）合并为 3 族（A/B/C）**。原 F4（相干物理信息 AMC，锚 L124）不再算"机制不同的第 4 族"，因为 L124 官方身份（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557）确认它**是一个真实的 coherent-FSO AMC 论文，AMC action 真实**（modulation selection driven by multi-dim CSI [SNR, scintillation index, phase variance]），即 L124 是 A 族（MCS/功率控制）的一个相干相位的实例，而非独立机制族。修订后：
   - **A_MCS_POWER_CONTROL** = instantaneous-CSI 分支（原 F3）+ delayed/statistical/uncertain-CSI 分支（原 F1）合并，因真实 action 相同（调制阶数/码率/功率切换）。
   - **B_HARQ_IR_RATE_ADAPTATION** = 原 F2，真实独立 action（IR-HARQ 重传+速率+功率），文献密集，当前更像 ENGINEERING_COMPONENT 候选。
   - **C_COHERENT_TX_ADAPTATION_UNVERIFIED** = 原 F4（L124 + L165），在 L124 全文身份/action/coding/CSI/channel/scenario 闭合前不算正式候选族（pre-fix 状态 `UNVERIFIED_BIBLIOGRAPHIC_HIT`）。
2. **F1 headroom 纠正**：F1（现 A 族的 delayed/statistical CSI 分支）**并非完全避开**旧 0.09 dB MCS 天花板（dead-end#3）。它与旧路线共享长时间尺度信息驱动的 MCS/码率切换，新增点只是"不确定信息约束"，headroom **未证**，须 Step 4a 维度 D 的 oracle 上界（FR-21）核算。
3. **"直接竞品 0 篇确认"改为 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`**：4 个 alias collision query（coherent FSO ACM ModCod satellite / optical feeder variable-rate FEC / FSO rate-compatible LDPC puncturing / satellite optical DVB-S2X ACM）共 32 命中，0 直接竞品；但 Exa 402 透支 + OpenAlex 0 命中 + S2 限速，覆盖有 caveat，不把搜索未命中解释成真实空白（FR-23）。
4. **title-abstract identity 审计结论**：6 个 normalized-abstract 重复组覆盖 18 条 hit，根因是 Exa/SerpAPI abstract 抓取污染（少数通用 survey 摘要被反复注入到不同标题的条目）。受影响 shortlist/flagged 条目：**L124（abstract 是 6G-roadmap，真实 abstract 经 Crossref 确认为 coherent-FSO AMC）/ L020 / L038 / L090**。这些条目的 abstract 不可信，须用 title+DOI 定身份。
5. **L038 标签纠正**：原标 `chinese-FSO-AMC` 错误——L038 标题是英文，DOI 10.1080/24751839.2026.2637258（Taylor & Francis，非中文刊），应标 `IM/DD-FSO-AMC`（与 L020 同组）。其 abstract 同样是污染的 OWC-survey 文本。
6. **L070 标签一致性**：L070 文字声称属"mod-classification 排除 5 条"之一，但其 pri 是 `备选`（未排除）。修订：L070 维持 `备选`，文字改为"borderline demod/AI-mod survey，非纯 classification，pri=备选（保留观察）"，与 pri 一致。
7. **provenance receipt**：`search-archive/2026-08-02/_step1_receipt.json`（force-add）固化检索合同、raw 文件 SHA256、shortlist provenance、L124 官方身份、alias repair 结果、确定性重放命令。raw JSON 继续 gitignored，但 receipt 使 clean clone 至少能恢复检索合同与哈希。

**保留 V001**：V001（Step 1 原 12 项 checklist）仍 PASS 12/12，但明确它**漏审 title-abstract identity 和 source provenance 口径**（V001 Check 3 把 manifest published=153 当 cosmetic 误差，未追到 _alldigest 真值 115；V001 未做 normalized-abstract 分组审计）。新增 V002 记录本次修订血缘。

**依据**（证据链，FR-26）:
- 确定性重算脚本 `tools/amc_step1_recompute.py` + 输出 `tools/_amc_step1_recompute_out.json`（从 raw JSON 重算：32 文件=17 unique query / 16 非零；published 115/209=55.0%；6 dup-abstract 组覆盖 18 条；priority 分布 必读10/建议读17/待确认4/备选57/排除121）。
- L124 官方身份：Semantic Scholar Graph API（exact title match, with S2_API_KEY）+ Crossref `/works/10.1364/oe.595557`（title/authors/Optics Express 34(14):26128/abstract）双源交叉验证。OpenAlex HTTP 429 不可用，但不影响双源确认。
- 4 alias collision query：`search-archive/2026-08-02/{coherent-fso-acm-modcod-satellite,optical-feeder-link-variable-rate-fec,fso-rate-compatible-ldpc-puncturing,satellite-optical-dvbs2x-acm}.json`（SHA256 见 receipt）。
- `_step1_receipt.json`（23KB，json parse OK，raw hash 与磁盘一致）。

**触发原话**: 无（技术推导 + 用户执行提示词 §三 Phase A 限定修复指令；用户本轮 voice 见 voice.md "2026-08-02 Phase A 执行提示词" 段）。

**影响**: Step 1 修订为 ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR；候选族数从 4 降为 3（A/B/C）；L124 在 Step 2 必须得到确定身份结论（全文）；Step 2 shortlist 不变（12 篇），但 L038 标签与 L124 身份状态更新；进入 Phase B（Step 2 acquisition）。
