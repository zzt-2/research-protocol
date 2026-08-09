# Task Brief: RML-FSTS Step 4a source calibration and structural-action audit

> 来源: S004 / V006 | 日期: 2026-08-09
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md`

## 0. 任务

fresh-context、只读判断原 Q1 structural `(B_N,B_L)` semantic smoke 能否用本地一手证据建立可承重的 condition/channel/calibration contract。不得实现、不得运行 performance grid、不得改任何现有文件；只写指定 worker-log。最多 15 分钟。

## 1. 必读/可读

- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md`
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`
- `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md` V006
- shared Wang canonical `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md` 与 metadata/read-note
- 本地 Al-Habash/Gu/Valjus source、`projects/simulation/params.py:100-170`、相关 verified channel tests；需要时可读论文局部公式，不做新泛搜

## 2. 必答

1. 从 Wang 一手材料恢复所有可确认 receiver-power 点/扫轴、weak/strong `C_n^2`、path/aperture/coupling/noise、CFO/linewidth、B0 `(B_N,B_L)` qualitative/numeric anchor；给 file:line，无法恢复标 UNKNOWN。
2. structural action set：每个 action 重建 320-symbol FSTS，哪些变量必须随 `B_L` 变化；如何用 shared base PRBS + channel/CFO/PN/noise latent innovations 做 action-specific waveform 的 paired cluster，不声称 identical rx。
3. B2 的 action-before receiver-power information：原 chain 是否有 AGC/power estimate；若需 common probe/previous-frame estimate，是否改变任务/overhead，能否合法冻结。
4. 是否能从 Wang `C_n^2=1e-16/1e-14`、10 km、wavelength/path assumptions，经一手公式得到 GG/phase-screen替代；列方程、输入、输出与哪些失真。Gu `(alpha,beta)` 是否只能 transfer，不可冒充 Wang。
5. dBm→electrical SNR/noise 是否能由已有 responsivity/LO/shot+thermal参数唯一恢复；缺哪些量。不得自行补典型值。
6. 最小 B0 calibration gate：在什么 exact source point/trend 下，paper default必须复现什么；当前材料是否足够。
7. 给唯一结论：`SOURCE_CALIBRATED_STRUCTURAL_SMOKE_READY` / `NEEDS_LOCAL_RECOVERABLE_INPUT` / `HARD_BLOCKED_FOR_SCIENTIFIC_TERMINAL`。区分能跑 diagnostic 与能发 Q1 terminal。

## 3. 验收格式

```markdown
# RML-FSTS source-calibration audit
## Verdict
## Wang source condition ledger
## Structural action and paired-latent contract
## B2 action-before observability
## Cn2/channel transfer
## Power-to-SNR/noise closure
## B0 calibration gate
## Recoverable gaps vs hard blockers
## Recommended unique next action
## Evidence pointers
```

## 4. 禁止

- 不把 Gu GG 参数写成 Wang phase-screen等价。
- 不以 noiseless identity代替 source performance calibration。
- 不修改 D010/contract/T014，不跑 adapter/grid。
- 不因 PDF缺失自动 blanket block；先穷尽 local HTML、metadata、read-note与已有 source formulas。
