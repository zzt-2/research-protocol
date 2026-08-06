# Independent Verifier Report — Oversampled Coherent Sync Groundwork

> 日期：2026-08-06
> 基准：`0ac0119c4982b539c322b79773c563cafdbbd9a6`
> 模式：fresh-context、只读审计；未联网、未下载、未运行仿真；除本报告外未修改文件
> 总体裁决：**FAIL**

## 1. Findings（按严重度）

### Important 1 — Step 2 缺少“最接近拟议联合方法的直接竞品”，terminal 过早

`step1-search-report.md:47-53` 已把 JLT 2025 `10.1109/JLT.2025.3533197` 和 2026 JOCN
`10.1364/JOCN.587273` 识别为最接近 `receiver-known preamble → clock/frame/frequency` 动作的跨场景
直接竞品；其中 JOCN 明示 clock recovery + frame/FOE，比当前 CORE 中只做 frame+carrier 的 OE 2024
更贴近 Q1 动作。可是 `step2-acquisition-receipt.json:26-113` 的 6 篇 CORE 不含二者，JLT 2025 仅有一次
失败记录（`:129-132`），JOCN 2026 未进入 acquisition receipt。`step2-coverage-report.md:33` 仍宣称达到覆盖门，
同时 `:37` 又承认 JLT 2025 是最高优先级碰撞风险，前后不闭合。

这违反用户冻结的 Step 2 必含角色 5，故当前不能判 `STEP2_READY_FOR_USER_CONFIRMATION`。必须获取并核验
JLT 2025/JOCN 2026 中至少一篇真正最接近的全文，或在按每篇三路径止损后把 Step 2 标为明确的覆盖阻塞/缺口，
再重新裁决 terminal；不能用 OE 2024 的“同场景”替代“同动作最接近”。

### Important 2 — RDL 注册表与当前控制面不同步

RDL `topic-index.md` 已是 epoch 22 / CP009 / `OVERSAMPLED_SYNC_STEP2_USER_CONFIRMATION`，
`mission-log.md` 已追加 CP009，`master-state.md:8,30-40` 也指向新专题；但 `.sessions/_registry.yaml`
中 `2026-07-20-research-direction-lab-system` 的 `last_updated`、`description` 仍停在 D027/CP008 /
`STRATEGIC_SHORTAGE_CONFIRMED`。新专题条目虽已登记，权威入口仍形成两套当前状态。必须把该 active system
topic 的注册表快照同步到 CP009（或在修复 Important 1 后同步到重裁 terminal）。

### Important 3 — 参数有真实全文来源，但“设置/推导/仿真/测量”标签未逐项闭合

数值可在全文中复核：GEO 2023 的 ±30 ppm、±5 GHz、600 kHz、2 sps、roll-off 0.1 属于设计要求或仿真；
Valjus 2025 的 ±20 ppm 来自地面标准，约 50 ppm 是轨道条件推导，60–100 ppm 是该文数值仿真/实现假设；
Paillier 2020 的 100 MHz 是假设的残余 CFO，1.4 ms 与约 5 dB 是 TURANDOT/AO + DPLL 数值仿真结果，
不是外场测量。`literature_notes_oversampled_sync.md:35-40` 只明确标注 GEO 数字为设计/仿真，未逐项标注
Valjus/Paillier 的证据类型，容易把“measured acquisition time”（仿真曲线内测得）误读为实测。必须补齐
`数值 | 全文位置 | 证据类型（标准/设计要求/推导/仿真/外场测量） | 可用范围`；现阶段不得称参数已冻结。

### Minor 1 — S001 含过时的“尚未进入 Step 2”当前态句子

`S001-step1-step2-execution.md:18` 写“当前执行 GW Step 1；尚未进入 Step 2”，但 `:23-25` 又记录 Step 2
完成。应改成明确的历史时点表述，避免恢复时误判。

### Minor 2 — acquisition receipt 的路径计数字段语义冲突

`step2-acquisition-receipt.json:21-22` 记手工 fallback 为 0，而 `:136` 写
`per_failed_paper_manual_path_count: 1`。正文实际含义是“每篇共执行 1 条项目工具路径”，不是 1 条手工路径。
应改字段名或值，使三路径止损可机器审计。

## 2. 八项门控复核

| 门控 | 裁决 | 独立证据 |
|---|---|---|
| Phase 0 authority reconciliation | **PASS** | D023 明确 T004 被 ordinary regional retune 压过、T005 single-branch 与 CCISP select-before-execute 重复。commit `1140134e...` 证实 2A 无 held-out、terminal=`REJECT`；commit `67970307...` 证实 scheduling 本身 PASS，但动作身份与 CCISP 重复，Q(8,6) 为 `SUPPORTING_ONLY`（360 shards、漏 459 次 stage-2、13 dB 不可表示）。inventory 的 2A=`REJECT`、2B=`SUPPORTING_ONLY` 及禁止复活边界与现权威一致。 |
| 六份 search JSON | **PASS** | 六个 query 与 receipt 一致，SHA256 全匹配。逐文件 raw/unique/2019+ 为 `29/29/9`、`36/36/11`、`13/13/2`、`25/25/12`、`21/21/7`、`16/16/1`；跨文件为 `140 raw / 130 unique / 42 recent raw / 39 recent unique`。实际 result source 为 Tavily 90、SerpAPI Scholar 35、OpenAlex 6，加组合标签 9；JSON 的六项 `sources` 是 requested sources，不代表六源均产生命中。 |
| impairment 真实性与参数来源 | **PARTIAL** | timing/SCO/frame/carrier/fade 的工程真实性有全文支持，关键数字也可定位；但 Important 3 的证据类型标签未闭合，fractional timing 初始分布、frame-offset 分布、真实 fade 深度/持续时间和 fade 中 SCO 仍被诚实列为缺口。 |
| 2019+ task-matched baseline | **PASS（预卡层）** | Q1 有 Tang 2022、Wang 2023、OE 2024；Q2 有 Paillier 2020 + 近期卫星 timing/system 文献组成的传统顺序链。它们足以避免 `RECENT_BASELINE_UNAVAILABLE`，但不是新方法 Go，也未闭合联合任务优越性。 |
| Q1/Q2 非场景换名与碰撞边界 | **PARTIAL** | Q1 的增量限定为 sample-level fractional timing/frame/CFO；Q2 是 stateful timing/carrier hold/update/reacquire，机制与 CCISP branch selection 不同。两卡不是单纯 FSO/GG 改名；但最接近直接竞品全文缺失，故 exact-collision 边界未闭合。 |
| BOM 与停止门 | **PASS** | 16 项分类含 1 READY、8 SMALL_ADAPTER、7 NEW_INFRASTRUCTURE、0 EXTERNAL_BLOCKED；逐项合计 18.5 人日。合并 11–14 日、Q1 5.5–7.5 日、Q2 7–9 日没有明显低估，且清楚披露 SCO 状态、时间索引、truth/metric、paired waveform 与 baseline runner 风险。当前“不触发”基于停止条件是“完整平台重建 + 明显超过约 5 日”的合取逻辑；若候选必须合并 acquisition+maintenance，则应改判工程侧停止门成立。 |
| Step 2 六篇 identity/provenance/content | **FAIL（内容完整性 PASS，角色覆盖 FAIL）** | 两个证据根的 6 个 `content.md` 均存在；content SHA 全匹配；行数 `278/244/455/891/1582/873` 全匹配且 ≥50；题名均命中，4 篇 DOI 正文直接命中，另 2 篇由题名/metadata/source 交叉确认；3 个现存 source SHA 全匹配；未发现 403/Cloudflare/captcha 拦截页。CORE 角色 1–4 可覆盖，但角色 5 缺失，见 Important 1。 |
| 未进入 Step 3/实现/仿真；保护日志 | **PASS** | base 后改动仅为治理/研究 Markdown、JSON/YAML 与 ignored search receipts；无 Python/common/params/result 改动，无暂存文件。四个 `p05_run*.log` 仍为未跟踪且未暂存，mtime 均为 2026-07-30，早于本轮；哈希分别为 `7843B048...`、`735E4650...`、`C76887C...`、`95A1D184...`。 |

## 3. 结构与文件边界

- JSON：8/8 可解析；YAML：registry 与 inventory 2/2 可解析。
- 新专题具备 `topic-index.md`、S001、decisions、voice；S001 的必需锚点齐全。
- 除四个受保护历史日志外，未跟踪文件均属于本轮声明产出；六份 search JSON 位于 ignored
  `search-archive/2026-08-06/`，与 receipt 路径一致。
- 未发现 Step 3 笔记、实现、仿真、MVE、method claim 或意外代码文件。

## 4. 最终裁决与必须修复项

**FAIL。** Phase 0、检索统计、BOM、六篇文件身份/哈希/内容质量和阶段边界均可独立复现；失败来自
Step 2 必含角色未满足且 current terminal/控制面据此过早推进。

必须修复后再验：

1. 补取并核验 JLT 2025 或 JOCN 2026 这类最接近 joint clock/frame/frequency 动作的全文；若三路径后仍失败，
   明确记录覆盖阻塞并重裁 Step 2 terminal，不能继续称 6-CORE coverage ready。
2. 依据重裁结果同步 RDL system 的 `_registry.yaml`、topic control、mission-log、master-state、新专题
   topic-index/S001/decisions 与两个 Step 2 receipts/reports。
3. 给所有物理数值补证据类型，明确没有外场测量的值不得写成测量量级或冻结参数。

下一合法动作仍仅是 CORE 补充/替换与状态纠偏；不得进入 Step 3、实现或仿真。
