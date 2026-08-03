# [R003] Step 3.5 定向补充检索 + 竞争闭包（Q-A / Q-B）

> 2026-08-03 | 关联：专题 `2026-08-02-fso-amc-groundwork` / D005 / S005
> 执行方式：2 个并行子 agent（Q-A / Q-B），各 ≤15 分钟，主线程只接收结构化摘要 + 竞争闭包表。
> 全部检索 JSON 落盘 `search-archive/2026-08-03/`（55 个文件，含 6+6 专属 query + 4 补充 query + 引用链 JSON + Safi/Galijasevic citation + Galijasevic title-search）。

## 调研问题

D005 按 canonical 四判据重建出 Q-A（预测驱动自适应编码的风险失配）+ Q-B（相干星地 AMC 动作位置-时间尺度失配）两个 Step 3 层 SURVIVES 候选。本 R003 回答：**Q-A / Q-B 在 Step 3.5 定向检索 + 引用链 + 竞争闭包后，是否被直接竞品实质覆盖？** 各 Q 终态 ∈ {SURVIVES_STEP3_5 / COVERED_BY_EXISTING_WORK / WEAK_SCENARIO_MIGRATION / BLOCKED_BY_MISSING_FULLTEXT / TOO_BROAD_OR_MECHANISM_UNPROVEN}。

## 发现

### 1. 检索规模

**Q-A**：6 专属 query（每 query ~20 命中，共 ~120）+ Galijasevic forward/backward citation（**未闭合**，见 §4 caveat）+ Safi 2019 forward citation（S2 成功，**49 被引**筛后 48 相关）。
**Q-B**：6 专属 query（每 query 19-20 命中，共 ~119）+ 4 补充 query（25/25/20/0）+ L023 forward citation（S2 **23**，筛后 **0 直接 sat AMC**）+ Nguyen2024 forward citation（S2 **5**，筛后 **0 coherent sat AMC**）。

总命中 ~190+，跨 S2/OpenAlex/SerpAPI/arXiv/Exa 多源（部分源限速/透支，caveat 见 §4）。

### 2. Safi / L124 全文获取（3 路径均失败，仍 BLOCKED）

- **Safi 2019**（DOI 10.1109/TVT.2019.2916843）：tools/download `all_failed`；Unpaywall `is_oa=False, closed`；作者机构仓储无 OA 副本。→ **仍 PROVISIONAL abstract-only**，不计 baseline 门槛，**禁据 abstract 推失效机制**（FR-26）。
- **L124**（DOI 10.1364/OE.595557）：tools/download `all_failed`；Optica OA URL 三种（viewmedia/fulltext/abstract）全返回 **HTTP 202 + Radware JS-challenge**（`/checkjs.cfm` bot-block）；arXiv 0 条。→ **仍 C_L124_FULLTEXT_BLOCKED**。
- 二者 3 路径穷尽合法获取，**未绕过访问控制，未用 WebReader/Scholar**。

### 3. 竞争闭包表

#### Q-A 闭包表（预测驱动自适应编码的风险失配）

| paper | DOI/year | 同 M(预测/CSI不确定下码率选择) | 同 C(星地FSO+延迟/估计误差+深衰) | 解决 A(预测后验缺失/risk-aware) | verdict |
|---|---|---|---|---|---|
| Nguyen/Le/Pham 2024 (TAES) | 10.1109/TAES.2024.3403809 / 2024 | **是**（ESN 点预测→rate+power） | **是**（sat FSO+delayed CSI） | **否**（"accurately predicted CSIs" 点预测，把 outdated CSI 当动机非纳入码率规则） | **PARTIAL_OVERLAP**（最强近邻，A 留缝）|
| Galijasevic ICC 2024 | 10.1109/ICC51166.2024.10622619 / 2024 | 是（M 的前身） | 部分（FSO+delay，非星地 IM/DD） | 否（点预测） | PARTIAL_OVERLAP（M 前身）|
| Safi 2019 (TVT) | 10.1109/TVT.2019.2916843 / 2019 | 部分（coding+power under est-error） | 是（FSO+est-error；GG/sat 全文未确认） | **abstract 看不出 risk-aware/posterior** | **UNVERIFIED**（全文 BLOCKED，FR-26 禁推）|
| ETRI 2026 rateless polar HAPS-FSO | 10.4218/etrij.2025-0461 / 2026 | 部分（rateless，ideal CSI 无预测） | 部分（HAPS-ground，无延迟/误差） | 否 | DISTINCT |
| 其余（JLT2020 PS / TVT2024 HAP-Multi-UAV / IJLEO2019 MIMO-K / JLT2025 self-adaptive / JLT2025 matched-filter） | — | 否 | — | 否 | DISTINCT |

**Q-A 闭包结论**：**无任何 FSO 文献做 posterior-aware / Bayesian / risk-aware / outage-constrained code-rate rule under prediction error**（posterior/risk-aware query 在 FSO 域 0 命中；outage-constrained 命中全为 RIS/SWIPT 波束成形非码率）。唯一同 M+C 的 Nguyen2024 用点预测且把 outdated CSI 当**动机**而非纳入码率规则——**恰好印证 Q-A 的 A 仍开放**。Safi 处理 estimation error 但全文 BLOCKED，UNVERIFIED 尾巴待全文关闭。

#### Q-B 闭包表（相干星地 AMC 动作位置-时间尺度失配）

| paper | DOI/year | 同 M(单环 TX+RX CSI 反馈 AMC) | 同 C(LEO RTT≈/>相干时间) | 解决 A(分层控制解时间尺度失配) | verdict |
|---|---|---|---|---|---|
| L023 (JLT 2023) | 10.1109/JLT.2023.3242215 / 2023 | **是**（=Q-B 的 M 本体） | **否**（terrestrial，自陈 LEO 不可行） | 否（单环，是 Q-B 要解构的对象） | **PARTIAL_OVERLAP**（M 本体，非解决方案）|
| Nguyen2024 (TAES) | 10.1109/TAES.2024.3403809 / 2024 | 部分（TX-only，RX 无 AMC） | **是**（sat，delay>相干） | 部分（ESN 预测补偿，但单环非分层） | PARTIAL_OVERLAP（同 C，思路=预测非分层；IM/DD）|
| Slow/Fast AMC massive MIMO | 10.1049/cmu2.12389 / 2022 | 否（RF cellular） | 否（RF） | **是（FAMC+SAMC 分层）** | **DISTINCT（RF split-timescale 先例，强反例：路径非空，但未迁移到 FSO/sat）**|
| Two-Timescale Movable Antenna | 2025 arXiv | 否（RF） | 否 | 是（two-timescale） | DISTINCT（RF 先例第二例）|
| L124 | 10.1364/oe.595557 / 2026 | 是（coherent AMC） | **否（terrestrial，abstract Crossref 验证；FR-26 禁推实现）** | 否（physics-informed 单框架，未分层） | PARTIAL_OVERLAP / UNVERIFIED（最接近 coherent AMC，非 sat，全文 BLOCKED）|
| L165 sat feeder coherent+AO | 10.1038/s41377-023-01201-7 / 2023 | 否（AO 层非 AMC） | 部分（sat-ground） | 否 | DISTINCT（boundary AO）|
| MaxSpecEff Adaptive Coherent Terrestrial FSO (TCOMM 2026) | 10.1109/TCOMM.2026.3694829 / 2026 | 部分（coherent AMC 容量界） | **否（terrestrial）** | 否（单环） | DISTINCT |
| Adaptive MQAM Terrestrial Coherent FSO (LCOMM 2026) | 10.1109/LCOMM.2025.3648035 / 2026 | 部分 | 否（terrestrial） | 否 | DISTINCT |

**Q-B 闭包结论**：Q-B 的分层契约在 **FSO/sat 域无直接竞品**（L023 forward 23 + Nguyen forward 5 + 10 query ~190 命中 0 直接覆盖）。split-timescale 思想在 **RF massive-MIMO 域已有成熟先例**（10.1049/cmu2.12389）证明技术路径非空。**关键风险**：**不存在合法 coherent 星地 AMC 近期 baseline**（L023/L124/TCOMM2026/LCOMM2026 全 terrestrial；L165 sat 但 action=AO）→ Q-B 判据3（近期 baseline）的 baseline 缺位，Step 4a 若做量化对标需**自建 coherent sat-ground GG 信道模型**产生 baseline。

### 4. Caveat（检索充分性，gw-supplement.md L57-64）

- **Galijasevic DOI 解析异常**：`10.1109/OJCOMS.2024.011100` 在 OpenAlex/Crossref 解析到 "BELA Zero-Trust 5G/6G"（W6884651712），与真实 M 论文（Galijasevic 2025 "Channel-prediction-driven rate control for LDPC coding…", c=4 + ICC 2024 前身）不符。→ Galijasevic forward/backward citation **未闭合**（OpenAlex/S2 持续 429 + Exa NO_MORE_CREDITS）。**影响评估**：不影响 Q-A 闭包结论（Nguyen2024 + Safi forward 49 已足够支撑），但建议 Step 4a 前用正确标题/DOI 重跑 Galijasevic citation。
- **L023 backward citation 缺口**：OpenAlex 未索引该 DOI、S2 backward 跳过 → split-timescale/receiver-driven 鼻祖溯源未在本次工具链闭合。建议 Step 4a 前手动读 L023 references 段补齐。
- **L124/Safi 全文 BLOCKED** → Q-A 的 Safi UNVERIFIED 尾巴 + Q-B 的 L124 UNVERIFIED 仍开。二者全文到手可能改变判定（Safi 可能覆盖 Q-A 的 A；L124 可能是 Q-B 的 coherent 直接竞品）。
- **`q-b-rx-directed-leo-infeasible.json` 0 hit**（多源透支/Scholar rate-limit），未直接证伪但与 Q-B 结论一致（无 receiver-driven LEO AMC 工作）。
- 检索充分性判据：关键词矩阵覆盖（Q-A/Q-B 各 6 query）✅、源覆盖（≥2）✅、引用链（≥1 篇核心竞品双向：Safi forward✅ / Galijasevic 未闭合⚠ / L023 forward✅ backward✗）部分、收敛性（最后一轮新增必读/建议读：Q-A 发现 ETRI2026+ICC2024 前身；Q-B 发现 RF 先例+TCOMM/LCOMM 2026 terrestrial coherent AMC 容量界）。

## 结论

**两个 Q 都 SURVIVES_STEP3_5**：
- **Q-A = SURVIVES_STEP3_5**（带 Safi UNVERIFIED 尾巴）— 无 FSO posterior/risk-aware 码率规则直接竞品；Nguyen2024 点预测印证 A 开放。Safi 全文到手前 UNVERIFIED 尾巴不能关闭，但 Step 3.5 层不要求关闭（FR-26：禁据 abstract 推；全文 BLOCKED → 保留 blocker 不强判 COVERED）。
- **Q-B = SURVIVES_STEP3_5**（带 scenario-migration + baseline 缺位风险）— FSO/sat 域无分层契约直接竞品；RF massive-MIMO 先例证明路径非空。**风险**：无合法 coherent 星地 AMC baseline，Step 4a 量化对标需自建信道模型。

→ **存在 Step 4a 入口**（≥1 个 Q SURVIVES_STEP3_5）。**本轮不启动 Step 4a**（brief 明示到 Step 3.5 终态停止）。

## 对决策的影响

- **不新建 D###**：Step 3.5 终态由 D005 已确立的 canonical 四判据框架 + 本 R003 闭包证据支撑，终态 STEP3_5_SURVIVES（Q-A/Q-B 均 SURVIVES）记录在 S005 + literature_notes §11 + topic-index，不需额外决策（Step 4a 启动是下一轮跨阶段决策，须用户授权）。
- **Q-A 的 Safi UNVERIFIED 尾巴 + Q-B 的 baseline 缺位** 是 **Step 4a 的开放问题**（不是 Step 3.5 终止条件）：Step 4a 启动前应优先 (a) 合法获取 Safi 全文关闭 UNVERIFIED；(b) 评估 Q-B 自建 coherent sat-ground GG 信道模型的可行性（判据4 能否量化对标的工程前提）。
- **Galijasevic DOI 异常 + L023 backward 缺口** 记为 Step 4a 前债务（用正确 DOI/标题重跑 citation）。
- 不修改 Skill / dormant receiver / 4 个 p05 log（边界遵守）。
