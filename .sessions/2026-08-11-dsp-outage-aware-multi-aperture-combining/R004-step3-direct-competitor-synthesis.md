# [R004] Step 3 direct-competitor synthesis

> 2026-08-11 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D003

## 调研问题

五篇合格全文是否已吸收 branch-local DSP validity 驱动 bounded soft weight/abstention；并区分它与“所有独立 FS/CE/CPE 完成后”这一尚缺 task-matched baseline 的更宽位置。

## 发现

### 身份与读取覆盖

五篇均通过 title gate，均完成 15/15 标准字段、7/7 结构段、通信参数与实验完备性审计：Johst WiSEE 2024、Wang JPHOT 2023、Liu JLT 2023、Tu JPHOT 2020、Yang ICCC 2022。完整字段见专题 literature owner 与三个 Step 3 worker logs。

### 动作矩阵

| 论文 | input → action → output | 裁剪边界 |
|---|---|---|
| Sun 2019 | multiple coherent-FSO signals → adaptive digital combining（摘要级）→ combined signal | exact weight/trigger/DSP ordering 不可断言 |
| Wang 2023 | FSTS branch samples → FS/alignment + phase correction + MRC + FOE → combined symbols | 无 validity weight/drop |
| Liu 2023 | post-IQ/clock N×H/V streams → 2N×2 CMA/RDE FIR joint equalize/combine → two PM streams | estimator-changing；无 explicit admission/abstention |
| Johst 2024 | known-sequence DSP + SNR/BER → low-SNR DSP；outage/hard discard boundary → valid stream/outage marker | hard comparator；未测试 soft combining |
| Tu 2020 | aligned fields + known OSNR/loss → choose M, rotate, positive-gain recursive EGC → coherent sum | known-OSNR conditional admission；非 DSP validity |
| Yang 2022 | pilots/attenuation + `Hhat` → attenuation-derived continuous weight + MRC → decisions | RF pilot-amplitude soft weight；非 FS/CE/CPE validity、无 abstention |

### Canonical Q001

- **M**：Wang 2023 的实际顺序：per-branch FSTS FS/alignment + branch phase correction → MRC → shared pol-demux/FOE；Liu 2023 2N×2 为 strongest estimator-changing alternative。
- **C**：在该 pre-MRC 边界，支路功率与 branch-local FS/phase-correction validity 异质，部分支路近/越过局部 DSP outage、其余仍有效。
- **A**：channel amplitude/phase correction 不等于 validity；Wang 链没有 admission 变量，invalid branch-local stream 仍可获非零贡献，Johst 已明确 outage branch 会恶化 combining、应硬丢弃。该失效可被 corrected MRC 无伤害或固定 discard/SC/GSC 完全吸收而证伪。
- **产出形态**：receiver-visible branch-local sync/phase/available estimation validity → bounded branch reliability/abstention → combined sequence + no-valid-branch flag；Step 3 不设计公式。

四判据：①具体技术矛盾 PASS；②deployable method output PASS；③近期 task-matched baseline PASS（Wang 2023 的实际 branch-local-DSP→MRC 位置 + Liu 2023 + Johst 2024）；④paired BER/outage 可量化 PASS。强比较器必须包括 fixed SNR discard、SC/GSC、corrected estimated-channel MRC，以及适用时 Liu 2023 2N×2；EGC 不作 strawman。

“所有独立 FS/CE/CPE 全部完成后再合并”的更宽位置在本批没有近期 task-matched baseline，criterion 3=`UNRESOLVED`；它只作为 Step 3.5 baseline-alignment debt，不并入 Q001 的 PASS。

### Collision limitation

宽泛 adaptive combining、pilot-amplitude soft weighting、known-OSNR admission、joint adaptive equalization均已被占，不得作为贡献。Sun 2019 仍为 closest direct collision risk；因无全文，exact action 保持 `UNRESOLVED`。仅因 Q001 存活，其合法全文和完整 action signature 转为 Step 3.5 critical debt。

## 结论

`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`。

这是问题候选通过 Step 3 文献门，不是方法有效、新颖性闭合、Go/Kill 或 METHOD_SIGNAL。未进入 Step 3.5/4a，未实现或仿真。

## 对决策的影响

建立 D004。下一合法动作仅为主控确认后执行 Step 3.5：补 Sun 2019 exact-action debt，并围绕 post-DSP/lock-aware/multi-source validity 做窄碰撞检索。
