# Step 3.5 Q1 focused Round 2 convergence search

> 2026-08-06 | 仅执行 T011 | 3 个冻结 query | 未修改 canonical、代码或实验 | 未提交

## 执行环境与命令

- worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- 工具：仅 `bash tools/search`；每个 query 均请求 `s2 openalex arxiv`，每源最多 20 条、最终最多 50 条。
- 三个归档的实际结果行均来自 `semantic_scholar`；OpenAlex/arXiv 本轮没有进入最终归档的记录。
- 首次顺序批处理在 304 秒总超时后终止；前两个目标 JSON 已成功落盘。随后仅补跑缺失的第 3 个冻结 query，未重跑前两个成功项，也未增加第 4 个 query。

```bash
bash tools/search "single objective joint frame sampling phase carrier frequency offset coherent optical" \
  --sources s2 openalex arxiv --max-per-source 20 --top 50 \
  --output "search-archive/2026-08-06/step35-r2-single-objective-frame-sampling-cfo.json" --format json

bash tools/search "fractional delay frame frequency joint estimator single carrier coherent optical burst" \
  --sources s2 openalex arxiv --max-per-source 20 --top 50 \
  --output "search-archive/2026-08-06/step35-r2-fractional-delay-frame-frequency.json" --format json

bash tools/search "preamble joint burst arrival sampling phase carrier frequency offset estimator" \
  --sources s2 openalex arxiv --max-per-source 20 --top 50 \
  --output "search-archive/2026-08-06/step35-r2-preamble-burst-arrival-sampling-cfo.json" --format json
```

## 归档与 raw/unique

这里沿用 T005 口径：`raw` 是目标 JSON 的归档结果行数，`unique` 是该文件内按 DOI → arXiv → 规范化标题键去重后的数量；不猜测 provider 在相关性过滤前的原始召回数。

| query | archive JSON | raw/unique | SHA256 |
|---|---|---:|---|
| single objective joint frame sampling phase carrier frequency offset coherent optical | `step35-r2-single-objective-frame-sampling-cfo.json` | 20/20 | `39f9b02c52345918b23024d22888c28301dea1ef695c5bed82fef537f4568dc1` |
| fractional delay frame frequency joint estimator single carrier coherent optical burst | `step35-r2-fractional-delay-frame-frequency.json` | 4/4 | `a8adcbf9305cc1f16c95dcb139a7aacee7af3c213f2126a19411ab1eb97eb9a8` |
| preamble joint burst arrival sampling phase carrier frequency offset estimator | `step35-r2-preamble-burst-arrival-sampling-cfo.json` | 3/3 | `1c2e600c973d27bb8a4f89bdf8d90ee6316394a3a0bd4e3afb9471cb179df70c` |
| **合计** | 3 JSON | **27 rows / 25 cross-query unique** | — |

## 相对 known set 的确定性去重

去重键优先级固定为：规范化 DOI（lowercase/trim）→ arXiv ID（lowercase，去版本号）→ 规范化标题（lowercase，仅保留 Unicode 字母和数字）。

- T005 Round 1：80 cross-query unique。
- T006 双向引用链：43 entries。
- T008 P1/P2/P3：三个 DOI 均已包含在 T006 引用链中。
- 三者 union：122 个确定性键（80 + 43，扣除 1 个跨集合重复；T008 不再增加键）。
- Round 2：25 cross-query unique，其中 6 个命中上述 known keys，19 个仅在元数据层面为新。
- 另做“已读论文”防误报：19 个形式新增中，Tang 2022 `10.1109/JPHOT.2022.3161795` 已在 `literature_notes_oversampled_sync.md` CORE 表及 `read-log.md` 中登记，不能计为真正新增。

## 新增 must/should

| class | title | DOI/arXiv | abstract-supported reason |
|---|---|---|---|
| new must | 无 | — | 没有摘要支持同一 coherent-optical estimator/objective 同时输出 frame/burst position、fractional sample timing/phase 与 CFO。 |
| new should | 无 | — | 唯一满足“2019+ direct coherent optical 且仅缺 fractional sample timing”外形的 Tang 2022 已是本专题 CORE/read，不是新增。其余形式新增条目均至少缺两项动作、年份早于 2019，或不属于目标 coherent-optical synchronization task。 |

### 近失配项（不计新增 must/should）

| title | DOI | 摘要支持的动作 | 不计入原因 |
|---|---|---|---|
| Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication | `10.1109/JPHOT.2022.3161795` | CFSO training sequence 定位 frame temporal position + FOE；未把 fractional sample timing 放入同一动作 | 语义上可落 should，但已是 7-CORE 的 Tang 2022，确定性 read guard 判 known |
| Unified Training-Sequence Joint Carrier Recovery for 200 Gbps FTN Coherent PON Upstream | `10.1109/ACCESS.2026.3701043` | 单一短 pilot block 下 coarse/fine CFO + phase-noise/cycle-slip carrier recovery | 缺 frame/burst position 与 fractional sample timing，缺两项动作 |
| Polarization-Fading-Free Phase Recovery and Robust RSOP Tracking Using Frequency-Domain Pilot Tones in Optical DSCM Systems | `10.1109/LCOMM.2026.3651445` | FOE + CPE + RSOP tracking，正文已在全局 read-log 登记 | 缺 frame/burst position 与 fractional sample timing，且非本轮新读对象 |

## 语义分类

1. **真正 joint `(frame, fractional timing, CFO)` estimator**：0 篇。Round 2 没有补出同信息、同 objective、同输出的 exact-action competitor。
2. **frame + CFO，但 fractional timing 前置或缺失**：Tang 2022 STSB（已读 known）；LPT 2017 FRFT（R1 known）。二者都不能升级为三参数 joint action。
3. **joint timing + CFO，但无 frame output**：JLT 2021 joint ML CO-OFDM（R1 known）。它仍是方法先例，不是 exact task collision。
4. **generic shared training/preamble reuse 或 sequential modular chain**：Sun 2025、OE 2025 等均为 R1/T006 known；Round 2 未新增同时含三个动作的条目。
5. **carrier-only / different-task / old non-optical**：其余形式新增主要是 CFO+phase/RSOP、microwave photonics、RF Rydberg、显微成像、2019 年前 OFDM/CPM 等，均不满足 must/should。

## Round 2 结论

- Round 2 新增：**must=0 / should=0**。
- 本轮达到 `新增 must/should = 0`，因此按 T011 的 focused convergence 判据为 **是**。
- 不启动 Round 3；若主线认为需要扩大 known-set 或改变 must/should 语义，应由主线另行决定。
- 本 worker 未编辑 canonical decisions/topic/master/literature notes、代码或实验文件，未提交。
