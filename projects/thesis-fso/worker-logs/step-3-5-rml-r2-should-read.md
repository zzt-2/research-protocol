# Step 3.5 R2：三篇 should-read 排除审计

> Task：`.sessions/2026-08-08-rml-fsts-groundwork/T006-step3-5-r2-should-read.md`
> 日期：2026-08-09
> 边界：只关闭 3 篇 R1 should-read 的 identity/action 债务；不改 current views，不进入 Step 4a，不触碰 p05/pyc。

## Acquisition/identity table

| DOI | title / year | 实测通道与状态 | canonical path / SHA256 / bytes |
|---|---|---|---|
| `10.1016/J.OPTCOM.2024.130981` | Coarse frequency offset estimation and compensation based on short-time spectrum analysis in FSO communication system / 2024 | `tools/download` wrapper 因 CRLF 失败；等价 `paper_download.py --force`=`all_failed`；Crossref identity PASS；OpenAlex `W4401610732`=`closed`、无 OA PDF；S2 `2b2f...`=`CLOSED`。**FULLTEXT_UNAVAILABLE** | source/content=`null`；metadata=`papers/doi/10.1016_j.optcom.2024.130981/metadata.json`；source SHA/bytes=`null` |
| `10.1109/ICAIT66450.2025.11353316` | A coherent communication scheme characterized by low complexity and enhanced robustness / 2025 | OA pipeline `all_failed`；项目 `blit --source ieee` 搜得 IEEE document `11353316` 并实际写入 PDF。工具只在成功后的 `✅` 状态打印处触发 GBK exception；PDF 完整。**QUALIFIED_FULLTEXT** | `papers/doi/10.1109_icait66450.2025.11353316/source.pdf` / `425afd5437b6fa0842b4e399aef6cfb8da68048721969ae71366f2bd69553077` / `1184672`；`content.md` / `a65fe9cd6a03483c7e5f1f5e9fb5f0eb40542041413661779a3c01ebd682dc30` / `36387` |
| `10.1109/JLT.2021.3063251` | Joint OSNR and Frequency Offset Estimation Using Signal Spectrum Correlations / 2021 | OA pipeline `all_failed`；项目 `blit --source ieee` 搜得 IEEE document `9368984` 并实际写入 PDF；同样仅成功打印触发 GBK exception。**QUALIFIED_FULLTEXT** | `papers/doi/10.1109_jlt.2021.3063251/source.pdf` / `a9f39140238df3df2afffe785ffd1825da992f8284cc7eadce69a5efb2929bfd` / `1742567`；`content.md` / `65571b703b615d400c3ba9b3071aa818e6ce9f1ff46d8ea266569e7caa1a3346` / `48595` |

两篇 IEEE PDF 均通过项目转换器 `tools/pdf_convert.py`（`tools/convert` wrapper 在本 Windows worktree 因 CRLF 不能执行）生成 canonical `content.md`；未自行实现 PDF 解析。

## Fulltext action evidence

### 10.1016/J.OPTCOM.2024.130981

- 只有 Crossref/OpenAlex/S2 identity 与标题级信息；合法全文不可得。
- “short-time spectrum”的 window 是否固定/自适应、是否受 receiver condition 驱动，均不能靠标题终判。
- action fields、lag/window/block 参数、comparators 与 fixed/adaptive 均为 **UNKNOWN**；没有全文行号，禁止据此排除 exact collision。

### 10.1109/ICAIT66450.2025.11353316

- action：固定 QPSK training 经 FFT 主谱峰做 coarse FOE，再利用训练排列的相邻符号 differential-conjugate phase 做 fine FOE（`content.md:45-47,67-79,185-187`）。
- information source / granularity：frame sync 后截取的 training samples；每 frame 输出 CFO 标量并补偿，不输出 lag、`B_L` 或 window action（`content.md:47,79`）。
- lag/window/block：training length 在 B2B sweep 后统一固定为 960；不是 condition-aware selector（`content.md:115-117`）。
- condition / online-offline：received power、SNR、turbulence 只用于分层评估；实际实验由 ADC 后 MATLAB offline DSP 处理（`content.md:103-107,121-145,171-181`）。
- comparators：Wang 2023 FSTS [10] 与 Wu 2022 TS/FFT+4th-FFT [12]（`content.md:87-89,211-217`）。

### 10.1109/JLT.2021.3063251

- action：FO sweep → 上下边带 spectral correlation/SCDF → quadratic fit coarse FOE/FOC → downsampling + 4th-power FFT fine FOE（`content.md:43,161-175,191`）。
- information source / granularity：CDC 后 samples 与相隔一个 symbol-rate 的上下边带分量；每块输出 CFO/OSNR，不输出 time-lag/`B_L` selector（`content.md:53-71,107-119,163-175`）。
- fixed parameters：100 MHz narrowband filter；离线统一选 `Fs=±7.5 GHz`、`ΔF=1 GHz`、`Th=0.4`、`q=14`；运行时不按 OSNR/modulation/power 选 lag/window（`content.md:119,193-227,265`）。
- online/offline / comparators：DSO 后 offline DSP；比较 no FOC、perfect FOC、conventional FFT-FOE（`content.md:231,249-265`）。

## Collision classification

| DOI | classification | exact collision | cheap lookup equivalent | 结论 |
|---|---|---:|---:|---|
| `10.1016/J.OPTCOM.2024.130981` | `UNKNOWN_FULLTEXT_UNAVAILABLE` | UNKNOWN | UNKNOWN | 标题中的 STFT/window 不能替代全文动作证据，保留 blocker。 |
| `10.1109/ICAIT66450.2025.11353316` | `architecture_adjacent` | false | false | 固定 training-spectrum estimator；power/turbulence 不是 selector 输入。 |
| `10.1109/JLT.2021.3063251` | `architecture_adjacent`（含 offline parameter optimization 子特征） | false | false | spectral-component correlation 不是 time-lag family；固定 `ΔF/Th/q` 不是 condition→lag lookup。 |

两篇 qualified 全文都没有实现或实质吸收 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。

## R2 disposition

- 3 篇 identity：**3/3 closed**。
- action debt：**2/3 closed**（两篇 IEEE qualified fulltext）；`10.1016/J.OPTCOM.2024.130981` 因全文不可得保持 **UNKNOWN/blocker**。
- 可确认排除的两篇均只是 estimator-architecture adjacent；没有发现 hidden condition→lag/`B_L`/window action。
- 本 worker 不据此宣布 Step 3.5 terminal、novelty、Go/Kill，也不建议方法。

## Files changed and boundaries

- 指定产出：`projects/thesis-fso/worker-logs/step-3-5-rml-r2-should-read.md`；`search-archive/2026-08-09/rml-fsts-step3-5-r2-should-read-receipt.json`。
- canonical qualified papers：两篇 IEEE 的 `source.pdf`、`content.md`、`metadata.json`；对应两份 `papers/_read_notes/`。
- acquisition raw：两份 `search-archive/2026-08-09/rml-fsts-r2-*-blit.json`。
- 未修改 topic/literature/master-state/current views；未读取或触碰 p05/pyc；未进入 Step 4a、仿真、MVE 或方法设计。
