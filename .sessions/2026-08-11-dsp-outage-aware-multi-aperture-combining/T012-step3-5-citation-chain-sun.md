# Task Brief: Step 3.5 citation chain and Sun 2019 legal evidence

> 来源: S004 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-dsp-outage-citation-sun.md`
> 日期: 2026-08-11
> 唯一文档: 本 brief + 指定仓库工具/已有专题证据

## 0. TL;DR

对 Wang 2023 做前向+后向引用链，Liu/Johst 做补充链；同时继续 Sun 2019 DOI `10.1016/j.optcom.2019.03.069` 的合法获取与后续一手动作证据闭合。

**产出**：唯一 worker log；raw citation JSON 放 `search-archive/2026-08-11/step3-5-dsp-cite-*.json`。

**最高纪律**：

1. 引用链批量 screening 必须逐条读 abstract；S2-only 不当 verified citation。
2. Sun 无全文时绝不从摘要推 exact weight/order/trigger，也不机械判 blocker。
3. 只获取/筛查，不精读新全文、不判最终 terminal、不设计方法、不仿真。
4. 禁 ResearchGate/Google Scholar/webReader/绕访问控制；只用仓库 `tools/search`、`tools/download` 合法通道与已有资产。

## 1. 背景

Q001 边界同 T011：branch-local FS/alignment+phase correction 后、MRC 前的 validity-to-bounded reliability/abstention。Sun 2019 目前只知 coherent-FSO four-aperture adaptive digital combining、EGC baseline、摘要报告 3–10 dB；exact action=`UNRESOLVED`。

## 2. 任务详情

### 2.1 核心双向引用链

至少执行：

- Wang `10.1109/JPHOT.2023.3265847` forward，`--citations-source both`；
- Wang 同 DOI backward，`--citations-source openalex`；
- Liu `10.1109/JLT.2023.3276637` forward/backward（OpenAlex；若一侧 0 可保留 receipt）；
- Johst `10.1109/WISEE61249.2024.10850117` forward 或 backward 作邻接补充。

统一 `--top 100`，输出 `step3-5-dsp-cite-wang-forward.json` 等。逐条 title+abstract 筛 MUST/SHOULD，最多回传 10 篇。对 forward 候选核 publication year≥anchor year；S2-only 标 `UNVERIFIED_CITATION`。

### 2.2 Sun 2019 合法证据

1. 先查 canonical/shared `papers/`, downloads/manual、metadata、引用链资产，记录实际 availability。
2. 按 `stages/gw-acquire.md`/`tools-guide.md` 用 `tools/download` dry-run + 一轮合法 DOI/OA 获取；wrapper 因 CRLF 失败时，先记录原始错误，再仅使用仓库同一 download backend 的 documented CLI，不改工具代码。
3. 从 Sun 的 OpenAlex 前向/后向引用链找后续一手论文是否明确复述其算法 input/weight/order。二手引用只可缩小边界，不能等价全文。
4. 若得到 source/content，只做 identity/content gate并报告待 fresh reader；本任务不精读。

### 2.3 统一候选输出

每个高相关候选给：identity、链来源、abstract-supported fact、是否 fulltext available、provisional action signature、`MUST/SHOULD/MAY/REJECT`、相对 Q001 可能类别。单列 Sun：confirmed / unknown / legal-acquisition receipt / later-primary evidence。

## 3. 已知陷阱

- OpenAlex backward references 常含基础 MRC/EGC，不代表 direct competitor。
- later paper 对 Sun 的一句 related-work 转述不是完整 action signature。
- Wang/Liu 的 MRC/2N×2 顺序不能被标题“digital combining”模糊化。
- 新 PDF 只有 title/DOI/content quality 合格后才可交给下一 fresh reader。

## 4. 验收

- [ ] 至少 Wang 前向+后向链完成并有 raw receipt
- [ ] 链候选逐条 abstract screening，≤10 MUST/SHOULD
- [ ] Sun availability/合法获取/后续一手边界明确
- [ ] 未精读新全文、未判 terminal、未越权

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-dsp-outage-citation-sun.md`
