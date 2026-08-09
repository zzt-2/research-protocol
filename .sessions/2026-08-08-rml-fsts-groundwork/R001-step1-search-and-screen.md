# [R001] RML-FSTS Step 1 检索与初筛

> 2026-08-08 | 关联：2026-08-08-rml-fsts-groundwork / D001

## 调研问题

正式 Groundwork Step 1 能否建立覆盖 task-matched FSTS、multi-lag/stepwise prior art 与 coherent-FSO transfer physics 的可审查候选池，并为 Step 2 给出 8–12 篇 shortlist？

## 发现

### 检索与复用

- 先复核 T002 四份缓存：4/4 SHA256 与原 receipt 匹配；只作历史复用，不冒充正式 Step 1。
- 正式执行 7/7 个 semantic query group：一轮 A/B/C 各 1 组；二轮选择 A/B，各 2 组。q4/q5 是有效 0-result，仍保留为定向负结果；未补第八组。
- 一轮 stdout 可得 q1 `40/40→15`、q2 `41/41→27`；q3 控制器超时后形成有效 60 条 JSON，按 `source_api` 可复算 71 个 retained source occurrences / 60 个唯一 retained identity，未伪造丢失的 stdout raw 值。
- q1/q2 的 raw/dedup 数值是执行时 stdout 同步记录，检索 wrapper 未另存 raw artifact；对应 retained 中间产物已按 SHA256 固化。`rml-fsts-step1-canonical-ledger.json` 逐条保存 131 个合并输入、10 个身份碰撞、121 个 canonical identity、71 个正式发表判定及本地索引行指针，使终端计数可独立复算；不把 stdout 观察值冒充 raw artifact。
- 二轮 q4/q5/q6/q7 retained 分别为 `0/0/19/2`。实际贡献源并集为 S2、OpenAlex、SerpAPI Scholar、Tavily；0 命中或报错源不计覆盖。

### AI 初筛

三名 fresh-context screener 分别审查 q1/q2/q3，另一名 screener 审查 q6/q7；每条结果均按 title+abstract+venue+year+citation+publication_status 写回 priority/reason，未用 relevance score 代替语义判断。

| 输入 | 条目 | 必读 | 建议读 | 待确认 | 备选 | 排除 |
|---|---:|---:|---:|---:|---:|---:|
| q1 | 15 | 2 | 2 | 1 | 2 | 8 |
| q2 | 27 | 1 | 1 | 6 | 4 | 15 |
| q3 | 60 | 5 | 9 | 7 | 13 | 26 |
| q6 | 19 | 1 | 1 | 2 | 6 | 9 |
| q7 | 2 | 0 | 0 | 0 | 0 | 2 |
| **未去重合计** | **123** | **9** | **13** | **16** | **25** | **60** |

加入三份路线报告已明确的 8 个本地索引身份后，共 131 records；按人工确认的 9 组标题/身份碰撞、DOI、无 DOI 时规范化 title 依次去重，移除 10 个重复输入，得到 121 unique，其中正式发表 71，比例 `58.68%`。完整身份账本及其输入证据见 `search-archive/2026-08-08/rml-fsts-step1-canonical-ledger.json`。

### 三路线覆盖

- **路线 A — task-matched FSTS/training-aided FOE**：Wang 2023 source、Tang 2022 STSB、Cheng 2020 low-OSNR joint FFS、Wang 2024 enhanced frame+carrier recovery 形成 2019+ direct pool。q4/q5 零命中不支持 novelty closure。
- **路线 B — multi-lag/stepwise prior art 与 strongest conditioned single-lag alternative**：Yu 2023 stepwise AC→AC→multi-CC、Dong 2009 multi-correlation-lag、Electronics 2021 multi-pilot AC 与 Morelli 2009 practical two-stage CFO 形成明确 prior-art 警报；泛称 multi-lag/stepwise 不能作为新颖性声称。
- **路线 C — coherent-FSO transfer physics**：Paillier 2020、Wang 2023/2024、实时分集合并、branch block phase correction 等文献支持湍流/低功率/分支相位与 carrier reliability 值得全文核验；它们不证明 lag-ranking crossover。

### Step 2 shortlist

| # | 论文 | DOI | CORE 预判 |
|---:|---|---|---|
| 1 | Wang 2023 FSTS | `10.1109/JPHOT.2023.3265847` | C1/C2/C4 |
| 2 | Tang 2022 STSB | `10.1109/JPHOT.2022.3161795` | C2/C4 |
| 3 | Wang 2024 enhanced frame/carrier recovery | `10.1364/OE.520452` | C2/C4 |
| 4 | Cheng 2020 low-OSNR joint FFS | `10.1016/J.OPTCOM.2020.126046` | C2/C4 |
| 5 | Dong 2009 multi-correlation-lag | `10.1109/CHINACOM.2009.5339877` | C3 |
| 6 | Yu 2023 stepwise AC/CC | `10.1109/TVT.2022.3218937` | C3 |
| 7 | Electronics 2021 efficient synchronization | `10.3390/electronics10232942` | C3 |
| 8 | Morelli 2009 practical CFO | `10.1155/2009/821819` | C3 |
| 9 | Paillier 2020 space-ground AO+DPLL | `10.1109/JLT.2020.3003561` | C4 |
| 10 | 2023 real-time coherent-FSO diversity combining | `10.1364/OE.505931` | C4 |
| 11 | 2022 branch block phase correction | `10.1364/OE.448956` | C4 |
| 12 | 2024 data-aided multi-format coherent-FSO DSP | `10.1109/WiSEE61249.2024.10850117` | C4 |

### Exact claim boundary

允许：在当前有限 metadata/abstract 池中，尚未闭合一篇同时满足 task-matched coherent FSO、相同 overhead、receiver-visible information、dev-frozen modulation×TS-length×power conditioned single-lag/`BL` lookup，并直接与多 lag 方案比较的论文；这是待全文验证的具体 gap hypothesis。

禁止：把它升级成 novelty closure；把 source-domain condition-dependence 写成 target lag-ranking crossover；宣称 conditioned single-lag 已失败、多 lag 必要或 future action 已设计/验证；做 Q#/Go/Kill/METHOD_SIGNAL。

## 结论

`STEP1_PASS`。121 unique ≥20；actual sources=4 ≥3；唯一必读 ≥5；A/B 两路线各完成 2 组二轮定向检索；正式发表 58.68% ≥50%；四类指定候选均进入 shortlist。可以进入 Step 2 获取与覆盖面门。

## 对决策的影响

不产生新科学方向决策，不改变 `0/0` 计数。Step 1 PASS 只授权 Step 2；不授权 Step 3/3.5/4a、smoke、实现或仿真。
