# Task Brief: Step 4a Cn2 / power-to-noise physical transfer audit

> 来源: S004 / V006 | 日期: 2026-08-09
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-physical-transfer.md`

## 任务

fresh-context、只读评估能否用本地一手公式把 Wang 2023 的 `C_n^2=1e-16/1e-14`, 10 km, aperture/coupling, ROP、responsivity/LO/shot+thermal noise 转成可执行 baseband realization，而不拍参数。允许做确定性计算/小型公式 sanity check，不运行 estimator/performance grid，不改任何文件（除指定 worker-log），不联网，最多 12 分钟。

## 必读

- Wang shared `content.md:231-243,279-319,339-375`
- `projects/simulation/params.py:73-170` 与对应本地 source pointers
- `projects/simulation/common/_gg_time.py` / `_dual_pol_channel.py` 及 verified tests
- 本地 Al-Habash/Valjus/Gu canonical/read-note 中与 Rytov→GG、coherence time、receiver noise直接相关的公式
- V006 P0-2

## 必答

1. 用 source equation列出 `C_n^2, lambda, L`→Rytov→`alpha,beta` 的计算；哪些输入 Wang未给（例如 wavelength），使用项目 typical值是否只允许 sensitivity而非 source reproduction。
2. Wang phase-screen + coupling 与 scalar GG 的保真差异：对 320-symbol fine FOE ranking哪些结构保留/丢失。
3. dBm ROP + LO + responsivity + shot/thermal → discrete complex AWGN variance是否唯一；缺 bandwidth、temperature/load/noise figure等时明确无法闭合。
4. 能否以 measured receiver power直接作为 cell axis、只把 SNR当后验测量而不做 dBm→SNR映射；这是否仍能运行 estimator并比较 structural `B_L`。
5. 给 `PHYSICAL_TRANSFER_READY / SOURCE_CONDITION_ONLY_NO_NOISE_CLOSURE / HARD_BLOCKED` 与唯一最小补件。

## 边界

不得用典型 thermal 参数补空；不得把 formula consistency当 source calibration；所有数值标 source/derived/assumption。
