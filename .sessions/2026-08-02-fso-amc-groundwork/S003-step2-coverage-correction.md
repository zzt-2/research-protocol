# [S003] Step 2 覆盖纠偏轮（D003 主控裁决）— 补充获取 + CORE 重判 + 治理纠偏

> 2026-08-02 | 阶段: GW Step 2 acquisition（覆盖纠偏）| 状态: 完成 — Step 2 终态 STEP2_BLOCKED_BY_COVERAGE_GAP（4 CORE 全文 < 5 门槛），未进 Step 3

## 目标

一个对话内完成：(A) Step 2 覆盖纠偏与补充获取；(B) 若补齐 ≥5 篇真正 CORE 全文，立即进 GW Step 3 全文精读。不进 Step 3.5/4a/方法设计/仿真。

## 记录

### A0 主控裁决登记（D003）

承接用户执行提示词（paste-attachment 2026-08-02-230536）的主控裁决：D002/R002/H001 宣称的"Step 2 PASS / 6 篇覆盖 A/B/C 三族"**不成立**。6 篇（L165/L023/L096/L146/L075/L090）只过文件/转换质量门（content.md ≥50 行 + 身份闭合），**未做 CORE 判定**。主控重判：
- 保守核心集缩窄到 L023/L096/L146 3 篇。
- L075 改标 `SEMANTICALLY_DISPUTED_PENDING_FULL_READ`（不预判纯 classification，不计核心）。
- L165（AO/物理实验边界）、L090（fixed STTC，"adaptive"名义）不计核心。
- L124（C 族身份闭合关键）保持 `C_L124_FULLTEXT_BLOCKED`，无全文则 C 族不得通过问题/新颖性判断。
- 以 D003 取代当前矛盾状态，不改写历史 checkpoint（R002/H001 加 supersession banner）。

D003 已写入 decisions.md；触发原话登记 voice.md。

### A1 确定性补充获取（先查仓库历史索引，不直接从零搜索）

候选 5 篇身份先经 `search-archive/_index/all-papers.jsonl` + 子 agent（Crossref/S2/Unpaywall API）确认：

| 论文 | DOI | OA 状态 | 获取结果 |
|---|---|---|---|
| Safi 2019 | 10.1109/tvt.2019.2916843 | IEEE paywall，无 OA（Unpaywall is_oa=false，S2 openAccessPdf 空） | ✗ 3 路径止损（tools/download + 子 agent API 全空） |
| Chang 2025 | 10.1109/JPHOT.2025.3602148 | IEEE gold-OA CC-BY（标题实为"…Maritime Communication Systems: Design and Analysis"，非"Maritime FSO"） | ✗ 3 路径止损（tools/download + ieeexplore stampPDF/stamp.jsp 404→/denied/ + 子 agent 确认 bot-block） |
| Sun 2018 | 10.1364/OE.26.029319 | Optica gold-OA CC-BY | ✗ 2 路径止损（tools/download 不覆盖 Optica + opg.optica.org viewmedia.cfm → Radware bot-challenge） |
| **Galijasevic** | 10.1109/OJCOMS.2024.011100 | IEEE OJCOMS（DOI 注册于 PDF 但 Crossref/doi.org 暂未索引）；NSF PAR 预印本 OA | ✓ **获全文**（NSF PAR `par.nsf.gov/servlets/purl/10587906`，897950 bytes，SHA256 3234f8bb…，content.md 481 行） |
| L124 | 10.1364/oe.595557 | Optica gold-OA VOR（2026-07-13 发表） | ✗ 2 路径止损（tools/download JS-challenge HTTP 202 + 子 agent Radware bot-challenge） |

获取纪律：tools/download / tools/convert / 合法 OA URL 直取；**未用 WebReader/ResearchGate/Scholar 抓全文**（遵守 gw-acquire.md 禁令）。3 路径止损后停止，未绕过访问控制。

### A2 CORE 判定（逐篇，子 agent 全文验证）

3 个子 agent 并行读 7 篇有全文论文的 method+experiment，按 CORE 定义（运行时可部署 AMC action + FSO/CSI/turbulence condition + 非 classification/AO/fixed/post-hoc + 能进 M-C-A 或当直接竞品）判定：

| 论文 | CORE? | 判定理由（全文证据） |
|---|---|---|
| **L023** | **YES** | mod 格式(2/4/8-QAM)+per-mode power loading + RX MIMO decoder 切换，CSI-driven；MDM-FSO 湍流（von Karman phase screen，r0=0.5/0.9/1.1mm，非 GG）；运行时 TX+RX 适配；+5.2dB vs uniform；分析了反馈 staleness 极限 ~60km LEO |
| **L096** | **YES** | RCPC code-rate(4/5,1/2,1/3)+Mn-QAM per state via IR-HARQ sliding-window；LEO sat-ground FSO lognormal 湍流+pointing+FSMC；cross-layer TX link-adaptation；~600Mbps；CSI=ACK/NAK perfect-CSI 假设 |
| **L146** | **YES** | joint adaptive MCS(mf-QAM FSO+3GPP MCS RF)+UAV power+trajectory via DDPG，robust JOMPT-CU under CSI uncertainty；FSO/RF SUTIN lognormal+pointing+Nakagami+IMPERFECT CSI(Gaussian est error σ²=1/N)；运行时 TX MCS controller；0.85Gb/s |
| **Galijasevic** | **YES** | runtime TX dynamic LDPC code-rate selection(PBRL 8/9..8/80, k=8192, 16 rates ~0.5dB)；FSO lognormal 湍流 10ms 相干时间，FEEDBACK DELAY 1-4ms + zero/linear/quadratic CSI predictors；real runtime link-adaptation；linear best ≤2ms(98-101% zero-delay) |
| Safi 2019 | **YES (PROVISIONAL)** | abstract 明证 joint/standalone adaptive coding-rate + TX power control + GG 湍流 + channel-estimation error（observation-window length 可调）；**无全文**（IEEE paywall）→ 不计 5 篇门槛 |
| L075 | **DISPUTED** | core artifact = CNN-LSTM-Attention softmax 分类器 on RX STFT（confusion-matrix eval + true-label training）→ modulation CLASSIFICATION（dead-end#8 族）；AMC framing claimed 但无 CSI 估计/反馈环；不计核心 |
| L165 | **NO** | adaptive action = AO wavefront 校正（Shack-Hartmann + 97-actuator DM 1.5kHz）；调制固定 per measurement 比较 not switch；AO 边界 |
| L090 | **NO** | 4-state STTC，"adaptive orthogonality controller"= 数学 ξ-parameterization，design-time config 非 feedback-driven；fixed-scheme 研究，无运行时 AMC action |

### A3 Step 2 通过判定

| 要求 | 状态 |
|---|---|
| ≥5 篇 CORE 全文 | ✗ **4 篇**（L023/L096/L146/Galijasevic）< 5 门槛 |
| Safi（CORE 但无全文）| ✗ PROVISIONAL abstract-only，不计门槛 |
| L075（DISPUTED）| ✗ classification，不计核心 |
| L165/L090（边界）| ✗ AO/fixed-STTC，不计核心 |
| L124（C 族）| ✗ 全文未获（Optica bot-block），C 族 BLOCKED |

**Step 2 终态 = STEP2_BLOCKED_BY_COVERAGE_GAP**（4 CORE 全文 < 5）。按执行提示词"若 Step 2 未达到 ≥5 篇 CORE，只汇报 Step 2 blocker，不伪造 Step 3 结果"——**Phase B（Step 3）不执行**。

### A4 持久 acquisition receipt

`search-archive/2026-08-02/_step2_acquisition_receipt.json`（11 篇，每篇含身份/路径/SHA256/CORE 判定/理由/blocker/失败路径；coverage_summary.step2_verdict=STEP2_BLOCKED）。PDF/content gitignored，receipt force-add 确保删除 worktree 后仍可恢复来源+身份+CORE 判定。

### A5 治理纠偏

- **topic-index**：GW Progress 表 Step 2 行 PASS→🔴BLOCKED；范围变更记录加 D003；进展线索加 S003/D003/V003/V004 + R002/H001 supersede 标注；当前位置/未决项/下一合法动作全面改写（Step 2 BLOCKED，二选一用户决策）。
- **R002**：顶部加 D003 supersede banner（"Step 2 PASS/三族覆盖"废止，身份+内容质量门判定仍有效）。
- **H001**：顶部加 D003 supersede banner（交接前提"Step 2 PASS"不成立，"下一步进 Step 3"作废）。
- **V003**：独立文件 `V003-final-audit.md` 合并入 verifications.md 作 V003 条目（治理纠偏：禁独立 V 文件冒充正式 V###），独立文件删除。原 2 PARTIAL 复核：Issue 1（R001 body 无 banner）本轮复核已闭合（§4 F### headers + Q1 + 顶部均有 D002 标注）；Issue 2（未提交/receipt 未 force-add）S002 已在 commit 6ada2bc 闭合，本轮 S003 同处理。
- **V004**：新建，验证 D003 CORE 重判 + Step 2 BLOCKED（PASS，证据链完整）。
- **R001 §4 F1-F4 banner**：复核确认已存在（L303/322/341/360 内联 `〔D002：…〕` + L384 废止注释 + L7-10 顶部声明），V003 Issue 1 已闭合。
- **L090 路径**：`papers/manual/L090-intechopen/`（manual slug），metadata.json 含真实 DOI 10.5772/intechopen.84911；manual 获取按 slug 命名合规，路径问题澄清（非错误）。
- **registry + master-state**：last_updated 同步 D003；master-state §2 AMC 指针更新 Step 2 BLOCKED。

## 决策引用

- D001：新系统层范围与旧轴边界。
- D002：Step 1 科学完整性限定修复（候选族 4→3 + identity 审计 + receipt）。
- **D003（新建）**：Step 2 覆盖纠偏 — STEP2_BLOCKED_BY_COVERAGE_GAP，保守核心集 3→4（含 Galijasevic），L075 DISPUTED/L165·L090 边界/L124 C 族 BLOCKED。
- V001/V002：Step 1 验证（PASS）。
- **V003（合并）**：Phase A+B 独立终审（PASS 10/12 + 2 PARTIAL，本轮 Issue 1 复核已闭合）。
- **V004（新建）**：Step 2 覆盖纠偏验证（PASS，BLOCKED 判定成立）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（Step 2 acquisition 覆盖纠偏 + 补充获取 + CORE 重判 + 治理纠偏；不动 Step 3-4a/Skill/p05 log/不抓全文/不设计方法/不跑仿真）。
- Step 2 BLOCKED 时按执行提示词**未进 Step 3**（不伪造）。

## 后续

- **Step 2 blocker（核心未决项）**：CORE 全文 4 < 5。用户决策二选一：(1) 手动补全文（Safi/Chang/Sun/L124 至少 1 篇 CORE 全文）→ Step 2 重判 PASS → 进 Step 3；(2) 确认"4 CORE 全文 + Safi abstract"可接受 → 授权仅推 A/B 两族 Step 3（C 族 BLOCKED）。
- L124 全文是 C 族身份闭合关键（用户手动获取 DOI 10.1364/oe.595557）。
- L075 语义仲裁、中文检索 cookie/IP（L050/L206）、候选族最终数均待 Step 3（若进）。
