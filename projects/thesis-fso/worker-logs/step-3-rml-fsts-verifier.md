# RML-FSTS Groundwork Step 3 独立验证报告

> 日期：2026-08-09
> verifier：fresh-context `/root/step3_verifier`
> 验证合同：`.sessions/2026-08-08-rml-fsts-groundwork/T001-rml-fsts-groundwork-step3-read.md`，重点 §7–§9
> 范围：只审查 Step 3；未执行 Web/Search、Step 3.5、Step 4a、smoke、实现、仿真或 MVE

## 总体结论

**PASS，P0/P1/P2=`0/0/0`。**

初审为 `PARTIAL, P0/P1/P2=0/2/1`。生产者按 T001 允许的唯一一次最小修复闭合了两项 P1 与一项 P2；同一 verifier 随后执行 fresh recheck，结果如下：

1. L01/L02/L04 的 owner/read-log source path 已改为 receipt 中的 shared absolute canonical；三条路径均存在，实际 bytes/SHA256 与 receipt 完全相同。L04 read-note 已追加 frozen canonical 覆盖说明，明确排除 worktree 不同哈希副本。
2. L02/L04 fresh reader 已改为 Verification/Validation/Uncertainty=`2/2/2`、`2/2/1`；五篇 reader 均只使用同一强制三轴，且与 owner 汇总逐篇一致。
3. owner 的 stale current-state 句已改为“Step 2 结束时状态”，不再与 Step 3 completed current view 冲突。
4. fresh 机械回归：`git diff --check` exit 0；YAML/JSON parse exit 0；staged=0；p05 hash 全匹配且 staged=0；forbidden tracked diff=0。

T001 §5.5/§7.1 的 independent verifier 门现已通过，Step 3 `✅ completed` 可被接受；Step 3.5 仍为 `⬜ NOT_STARTED`，不授权 Step 3.5/4a/smoke/实现/仿真/MVE。`verifications.md` 的 V002 尚未创建是调度方明确保留给本报告后的动作，本报告不据此判错；主控现在可以据本 PASS 写入 V002，并按 T001 执行一次统一 commit，不 push。

## 问题清单

### [RESOLVED] P1-01：owner/read-log 的 frozen source path 不可无歧义解析

**证据：**

- receipt 的冻结 canonical path 为：
  - L01 `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`
  - L02 `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/content.md`
  - L04 `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md`
- `projects/thesis-fso/literature_notes_rml_fsts.md:138,166,222` 与 `projects/thesis-fso/read-log.md:77-79` 均写成相对 `papers/doi/.../content.md`。
- 在当前 worktree 中，L01/L02 的这些相对路径不存在；L04 的相对路径存在，但实际为 `46,321 bytes / 52C1845701FB0FB388B9A359492C6EC77CE4FDA34F8E8F405858449541A21E5F`，而冻结 shared canonical 是 `46,966 bytes / 62E3BFDF6B803069342B49DC6D9F666899BD7257841E42D9A5003CFDFF5A9662`。
- L04 fresh reader 正确记录了 shared absolute path，说明本轮实际读取输入正确；问题在 owner/read-log/read-note 的后续可解析 provenance。L04 旧 read-note `papers/_read_notes/10.1109_jlt.2020.3003561.md:3,6` 仍保留相对路径，本轮增量只给 hash、未明确覆盖旧路径语义。

**影响：**违反 T001 §2.1 对 L04 的显式冻结路径纪律、§4.3 的 owner source-path 可解析要求以及 §7.1(5) 的 owner/read-log/read-note 一致性。后续 reader 按 owner/read-log 打开文件时可能读到错误副本。

**最小修复：**不删除旧事实；将 owner/read-log 的 L01/L02/L04 source path 改为 receipt 中的 shared absolute canonical path，或引入明确、可机械解析的 shared-root 记法并附 receipt 指针。对 L04 read-note 追加一条“本专题 frozen canonical 覆盖路径”说明，明确 worktree 同 DOI 副本禁止用于本专题。修后复算三处 path/hash/bytes。

**fresh 复核：PASS。** owner `:139,167,222` 与 read-log `:77-79` 均使用 receipt 的 shared absolute canonical。实测 L01/L02/L04 分别为 `55349/E30A...A9F`、`95745/49A7...EDD`、`46966/62E3...662`，三者均与 receipt 完全一致；L04 read-note `:105` 已明确 frozen canonical 与禁止的 worktree 副本。P1-01 关闭。

### [RESOLVED] P1-02：L02/L04 fresh reader 的 VVUQ 轴错误且与 owner 不一致

**证据：**

- T001 §3.5 与 `stages/gw-read.md:153-160` 强制每篇给出 **Verification / Validation / Uncertainty** 各 1–3 分。
- L02 reader `projects/thesis-fso/worker-logs/step-3-rml-fsts-l02-reader.md:215-217` 实际给的是 `Validity=2 / Verifiability=2 / Utility=3`，没有 Uncertainty 分。
- L04 reader `projects/thesis-fso/worker-logs/step-3-rml-fsts-l04-reader.md:241-243` 同样给的是 `Validity=2 / Verifiability=2 / Utility=3`，没有 Uncertainty 分。
- owner `projects/thesis-fso/literature_notes_rml_fsts.md:96,98` 却汇总为 L02 `Verification/Validation/Uncertainty=2/2/2`、L04 `2/2/1`；该数值没有在对应 fresh reader 的强制三轴中落盘。
- L01/L03/L05 reader 分别正确给出 `3/2/1`、`2/1/1`、`2/2/1`。

**影响：**五篇实验完备性没有按统一合同闭合，owner 汇总与 fresh reader 证据链不一致；T001 §5.5 的“五篇实验完备性完成”门不能判 PASS。

**最小修复：**仅修 L02/L04 reader 的三轴名称、评分与一句证据，并同步相应 read-note 增量/owner 汇总；不得把 Utility 当 Uncertainty。修后重新核对五篇均使用同一三轴。

**fresh 复核：PASS。** L02 reader `:215-217` 为 Verification/Validation/Uncertainty=`2/2/2`；L04 reader `:242-244` 为 `2/2/1`。全五篇 reader 均检出 Verification、Validation、Uncertainty，且不再检出旧轴 Validity/Verifiability/Utility；逐篇分数与 owner `:94-99` 一致。P1-02 关闭。

### [RESOLVED] P2-01：literature owner 保留了一条未标历史快照的 stale current-state 句

`projects/thesis-fso/literature_notes_rml_fsts.md:45` 写“当前状态=`STEP3_DISPATCH_READY`，Step 3 尚未开始”，与同文件 `:5,13` 的 Step 3 completed current view 冲突。该段位于 Step 2 历史章节，可以保留历史事实，但应改成“Step 2 结束时的状态”而非“当前状态”。

**fresh 复核：PASS。** 该句现为“**Step 2 结束时状态**=`STEP3_DISPATCH_READY`，当时 Step 3 尚未开始”，与 current view 不再冲突。P2-01 关闭。

## 逐项验收证据

| # | 验收项 | 结论 | 证据摘要 |
|---:|---|---|---|
| 1 | 仅 Step 3 边界 | PASS | tracked diff 仅专题 S002/D004/topic/registry、3 份既有 read-note、literature/master/read-log；untracked 仅 R003/H002、5 reader logs 与既存 p05 logs。无科学代码、仿真参数、正式论文、旧专题或 Skill diff；产出文本均明确 Step 3.5/4a 未授权。 |
| 2 | 五篇 title/DOI/path/SHA/bytes 与 Yu adapter | PASS | receipt=`PASS_5_OF_5`；逐篇实际 hash/bytes 与 receipt 相等。L04 tar 中 `bare_jrnl.tex` 的 `\\title{}` 与派遣题名逐字一致，metadata DOI 一致。Yu shared source 与 adapter 均 `72,748 bytes / 97DB13AB40E6548AE70A01C12027B7085CA3123976353C5683DAE3350D8924A6`。 |
| 3 | 5×标准字段、7 子表、通信参数、非 DRL N/A | PASS（字段本体） | 5 reader logs 均有 identity、16项事实字段、A–G 子表、通信参数。动作均明确“非 action space”；reward 均为 N/A（非学习型确定性 DSP）；network 均为 N/A（非神经网络），未硬造 MDP/NN。 |
| 4 | 五篇实验完备性、三篇写作架构 | PASS | 五篇均使用 Verification/Validation/Uncertainty 三轴，分数与 owner 一致。L01/L02/L04 写作架构均覆盖三级结构/比例、System/Problem/Algorithm、符号参数、图表/caption、baseline/消融/复杂度、Intro/Conclusion、公式组织和共同基础引用。 |
| 5 | read-notes/read-log/owner 一致且旧内容保留 | PASS | L03 read-note 存在，285行/24,418 bytes，SHA256 与 L03 reader 完全相同；L05 同样与 reader byte-identical。L01/L02/L04 git diff 均为在旧笔记末尾追加增量，旧内容未删。read-log 每个 paper_id 仅一行且重读次数为 1/1/1、首读为 0/0；shared source path 与 receipt 一致，L04 read-note 已明确 frozen canonical 覆盖。 |
| 6 | source/target 与 C3/C4 角色 | PASS | owner/R003/五 reader 一致：Wang fixed `B_L`/tradeoff/低功率退化为 FACT；target crossover/failure/headroom 为 INFERENCE/UNKNOWN；Morelli/Yu 仅 C3 prior-art ceiling，Paillier 仅 C4 transfer physics。 |
| 7 | 缺失竞争者不承担 Q | PASS | Cheng/Dong/Electronics/OE.505931/OE.448956/Tang/WiSEE 只出现在 debt 矩阵，字段含允许使用/禁止承重；Q1 来源只用 L01/L02 与 L04 C4 physics，未用缺失全文承担公式、机制或 novelty。 |
| 8 | Q 表只用 canonical criteria | PASS | owner Q1 表列 M/C/A、方法产出形态及判据1–4，恰与 glossary 四项一致；`证据状态` 独立。`problem_truth/novelty` 只出现在禁止/边界说明中，不是 gate。Q1=4/4。 |
| 9 | Step 3 状态、Step 3.5 未授权、无虚构 terminal | PASS | 没有 `STEP3_PASS`/`STEP3_NO_VALID_PROBLEM` 等虚构 terminal；Step 3.5/4a/smoke/实现/仿真均未进入。修复后 independent verifier 门通过，Step 3 completed 判定符合 §5.5。 |
| 10 | literature/master/topic/registry/D004/H002 同步 | PASS | 六处均写 Q1=4/4、Step 3 completed、Step 3.5 NOT_STARTED、failure=0/0、下一动作仅新对话 mandatory Step 3.5；owner 历史快照已消除歧义。V002 仅等待主控据本报告回填。 |
| 11 | failure=`0/0` | PASS | receipt boundaries、R003、D004、topic、registry、master、H002 均为 research-object/method-package=`0/0`；无 Go/Kill/METHOD_SIGNAL。 |
| 12 | Git/YAML/JSON/staged/p05/禁区 | PASS（pre-commit） | `git diff --check` exit 0；registry YAML 与 Step2/Step3 receipt JSON 均 parse exit 0；staged count=0；四个 p05 logs hash 与 S002 初始值完全一致且均未暂存；diff 无禁止路径。 |

## 五篇 preflight 实测

| L# | DOI | actual bytes | actual SHA256 | 判定 |
|---|---|---:|---|---|
| L01 | `10.1109/JPHOT.2023.3265847` | 55,349 | `E30A66FE650FF065C65746943B52CC48AFC0476900F90421FEBD1F9B5D351A9F` | PASS |
| L02 | `10.1364/OE.520452` | 95,745 | `49A7FD02DB0A2758E3998C678F56190FBAA9D029D4CBA346320A8E94F8193EDD` | PASS |
| L03 | `10.1155/2009/821819` | 40,638 | `E565C4E846324013B276E0246FA087FD3518746F6A3791D7D95D300C4B78E132` | PASS |
| L04 | `10.1109/JLT.2020.3003561` | 46,966 | `62E3BFDF6B803069342B49DC6D9F666899BD7257841E42D9A5003CFDFF5A9662` | PASS |
| L05 adapter | `10.1109/TVT.2022.3218937` | 72,748 | `97DB13AB40E6548AE70A01C12027B7085CA3123976353C5683DAE3350D8924A6` | PASS，source=adapter |

## Canonical Q# 复核

| Q# | 判据1：M-C-A | 判据2：方法产出 | 判据3：近期 baseline | 判据4：量化对标 | 结论 |
|---|---|---|---|---|---|
| Q1 | PASS：Wang fixed-`B_L` / 固定 modulation-TS-power bin 内 receiver-visible condition / single-lag ranking 稳定假设，A 可证伪且仍为 INFERENCE | PASS：condition-to-lag design rule / reusable curve family | PASS：Wang 2023 IEEE Photonics Journal 是具体 2019+ M | PASS：CFO MSE、BER/sensitivity、range、complexity，对 Wang 与 conditioned lookup | 4/4；仅问题候选，不代表 A 已证、novelty 或 Go |

## 原始命令结果摘要

1. `git diff --check` → exit `0`，无 whitespace error。
2. `git diff --cached --name-only` → `0` 项；四个 `p05_run*.log` 的 staged 查询为空。
3. p05 实测：
   - `p05_run.log` → `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
   - `p05_run2.log` → `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
   - `p05_run3.log` → `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
   - `p05_run4.log` → `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
4. Python `yaml.safe_load(.sessions/_registry.yaml)` → `YAML_OK topics=61`；`json.load` Step2/Step3 receipts → 均 `JSON_OK`；parse exit `0`。
5. receipt 五篇路径逐一 `Test-Path + Get-Item.Length + Get-FileHash SHA256` → 5/5 exists，bytes/hash 与 receipt 完全相同。
6. Yu shared source 与 adapter `Get-FileHash` → 完全相同；`byte_identical=true` 可独立复算。
7. L03/L05 reader 与 read-note 分别 `Get-FileHash` → 两对均 byte-identical；L03 read-note 明确存在。
8. `git diff --name-only` → 10 个 tracked 变更，均属当前 Step 3/治理允许路径；`git ls-files --others --exclude-standard` → R003、H002、5 reader logs 与四个 p05 logs，无科学代码/仿真参数/正式论文/旧专题/Skill。
9. `git check-ignore -v` → Step3 receipt、L03/L05 新 read-note、Yu adapter 均被 `.gitignore` 命中。adapter 按 T001 可保持 ignored；receipt 与 L03/L05 read-note 属统一提交的必需 Step 3 产出，最终提交时需要显式 force-add。当前尚未 commit/push，符合 verifier 前 staged=0 要求。

## 最小修复后 fresh 复核结果

1. 三篇 shared canonical source path：3/3 exists，hash/bytes 与 receipt 3/3 完全相同；owner/read-log 3/3 指向相同 absolute path。
2. 五篇 reader VVUQ：5/5 使用 Verification/Validation/Uncertainty；owner 分数逐篇一致；旧错误轴 0 处。
3. current view：literature/master/topic/registry/D004/H002 均为 Step 3 completed、Step 3.5 NOT_STARTED、Q1=4/4、failure=0/0；owner stale 句已改成 Step 2 历史快照。
4. fresh mechanical gates：`git diff --check` exit 0；YAML topics=61、Step2/Step3 JSON 均 parse PASS；staged=0；p05 staged=0 且四 hash 与初始值完全一致；forbidden tracked diff=0。
5. scope：tracked diff 10 项均在 T001 允许路径；untracked 仅 R003/H002、五 reader logs、本 verifier 报告与四个既存 p05 logs；未进入 Step 3.5/4a，未运行 smoke/实现/仿真/MVE。

**最终判定：PASS，P0/P1/P2=`0/0/0`。允许主控写 V002 并执行一次统一 commit；receipt 与 L03/L05 read-note 仍需显式 force-add，Yu adapter 可保持 ignored；不得 push。**
