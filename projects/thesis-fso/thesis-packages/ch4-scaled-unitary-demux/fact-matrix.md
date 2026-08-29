# Fact matrix — Ch4 scaled-unitary 偏振估计与解复用

> Paper-writing 状态机：`INTAKE ✓ → DIAGNOSE ✓ → PROPOSE ✓ → WRITE ✓ → VERIFY 进行中 → DELIVER 待独立审查`
> 合同批准指针：T073 + D052；目标读者=硕士论文作者/导师；`venue=N/A`；本轮明确不含正式论文正文和新增科学实验。

## 1. 生命周期问题表

| ID | symptom / 写作需要 | root cause | evidence | minimal test | rejection criterion | level | affected artifacts | contract | implementation | verification |
|---|---|---|---|---|---|---|---|---|---|---|
| F01 | 方法身份易被写成“新旋转” | B2 `tau=1` 与 C4 共用 `UV^H` | `development.py:154-169`；D052-3 | 展开 B2/C4 公式 | 任一材料隐去共同方向 | L5 | 方法图、算法框、ledger | D052/T073 | 明示只改变公共尺度 | reviewer 待填 |
| F02 | 结果数字需可写且可复算 | 正式 aggregate 不能替代 raw 证据 | `confirmation_raw.json`；V027 | raw-only 重算 4×64 + pooled 128 | 与 V027 任一值不符 | L2/L3 | CSV、结果图 | T073-6/7 | `plot_ch4_results.py` | 本地 fresh PASS |
| F03 | 方法链需与实现一致 | 公式、fail-closed 与 runtime I/O 易漂移 | `scaled_unitary.py:32-88`；`development.py:125-182` | caller→callee→action trace | truth 进入 deployable action 或公式不符 | L4/L5 | 算法框、方法图 | T073-4/8 | 固结算法框与语义 brief | reviewer 待填 |
| F04 | 章结构需保持有限 claim | 场景只验证 strict scaled-unitary slice | D052-4；V027 P2 | 每节检查适用域/禁止外推 | 暗示 PDL/PMD/FIR/CPR/LDPC 已验证 | L5 | blueprint、ledger | D052/T073 | 独立边界节 | reviewer 待填 |

## 2. 核心事实与证据链

| Fact ID | 可验证事实 | 数据/代码/公式指针 | 比较对象与 metric | 图/表入口 | 引用入口 | 可写结论 | 禁止外推 |
|---|---|---|---|---|---|---|---|
| M01 | balanced pilots 上的 baseline 为 `H_LS=Y_pX_p^H(X_pX_p^H)^{-1}` | `scaled_unitary.py:32-48`；Step4a 报告 `:49-63` | B0；同 pilot 开销 | 方法图/算法框 | Roudas 2010 只作通信邻居，不证明本闭式 | 先由短导频估计 2×2 复信道 | 不称该 LS 为新算法 |
| M02 | `H_LS=U diag(s1,s2)V^H`，`g_hat=(s1+s2)/2`，`H_SU=g_hat UV^H` | `scaled_unitary.py:50-76`；Step4a 报告 `:49-81` | C4 相对 B0/B1/B2 | 方法图 | Schönemann/Higham 为经典 Procrustes/polar 原子候选 | 结构投影联合估计公共尺度与酉混合 | 不称新估计理论、首次或 SOTA |
| M03 | 解复用矩阵为 `W=VU^H/g_hat`，输出 `z=Wy` | `scaled_unitary.py:69-88`；`development.py:164-182` | 相同接收 payload | 方法图/算法框 | 2×2 Jones/demux 背景可引 Roudas/Kikuchi | 投影后以闭式逆完成双偏振解复用 | 不暗示已完成 CPR/LDPC 联合验证 |
| M04 | `rho=s1/s2` 仅为 receiver-visible diagnostic | `scaled_unitary.py:62-75`；Step4a 报告 `:156-166` | 不属于 performance action | 方法图注记 | 无需用它承重新颖性 | 可报告结构适用性诊断 | 不定义或暗示 `rho` 阈值/在线 gate |
| M05 | exact rank deficiency、零奇异值、NaN/Inf 均 fail closed | `scaled_unitary.py:20-29,32-48,50-76` | numerical validity | 算法框 | 无 | 数值无效时拒绝产生伪逆 | 未实现一般 near-zero 容差或自适应 fallback |
| M06 | B2 `tau=1` 把两个奇异值均 floor 到 `s1`，故与 C4 都使用 `UV^H`；差别为尺度 `s1` vs `(s1+s2)/2` | `development.py:154-169` | primary comparator=B2 | ledger/结果图 | 无 | confirmation 支持公共尺度估计带来的有限 BER 改善 | 不主张更优偏振旋转 |
| E01 | 四格均含 64 个 paired confirmation windows，每行 payload bits=32768 | `confirmation_raw.json`；`run_confirmation.py:31-80`；`plot_ch4_results.py:68-122` | BER=`Σbit_errors/Σpayload_bits` | CSV/结果图 | 无 | 四格结果具有相同 window 与 bit 聚合定义 | 不混用 window-mean 与 pooled-count BER |
| E02 | 14 dB/Np=2：B2/C4=`0.08277035/0.07667112`，相对降幅 7.37%，差值 CI `[-0.00954738,-0.00306168]` | raw-only CSV row `snr14_np2`；V027 | C4−B2 paired window bootstrap | 结果图 | 无 | C4 在该冻结格优于 B2 | 不外推其他 SNR/pilot |
| E03 | 14 dB/Np=4：B2/C4=`0.07178736/0.06990385`，相对降幅 2.62%，CI `[-0.00354064,-0.00019817]` | raw-only CSV row `snr14_np4`；V027 | 同上 | 结果图 | 无 | 有限但方向明确的 BER 改善 | 不选择性省略小增益格 |
| E04 | 18 dB/Np=2：B2/C4=`0.03875256/0.03550529`，相对降幅 8.38%，CI `[-0.00548053,-0.00143516]` | raw-only CSV row `snr18_np2`；V027 | 同上 | 结果图 | 无 | C4 在该冻结格优于 B2 | 不外推完整工作区 |
| E05 | 18 dB/Np=4：B2/C4=`0.02216578/0.02104330`，相对降幅 5.06%，CI `[-0.00216106,-0.00026414]` | raw-only CSV row `snr18_np4`；V027 | 同上 | 结果图 | 无 | C4 在该冻结格优于 B2 | 不删除该格或改坐标夸张差异 |
| E06 | pooled Np=2：B2/C4=`0.06076145/0.05608821`，差=`-0.00467324`，CI=`[-0.00686385,-0.00282661]`，相对 7.69% | raw-only CSV row `pooled_np2`；D052-2/V027 | 128 paired windows 的逐 window 差值 bootstrap | blueprint/结果节 | 无 | pooled 短导频支持有限公共尺度收益 | 不当作独立第五个实验格 |
| B01 | 验证场景为 static 2×2 unitary mixing + common scalar Gamma–Gamma + equal circular AWGN、DP-(8,8)-16APSK | `confirmation_manifest.json`；T071 frozen recipe；D052-4 | 目标验证 slice | 方法图右上注记 | 平台 authority 只能支撑场景 | 结论限定于冻结目标场景 | 不包含 PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC |

## 3. 实现真值三联表

### information_access

- Deployable B0/B1/B2/C4 runtime 输入仅为 `arm, X_p, Y_p, y_payload, parameter`；接口见 `development.py:125-132`。
- C4 内部只读取 pilot-LS、SVD、payload observations；`H_true` 与 payload truth 不进入 `receiver_action`。
- `H_true` 和 transmitted bits 仅在 `oracle_action`/`score_action` 中用于 O1 与离线评分，见 `development.py:185-213`。
- 因此正文必须把 O1 称为 oracle，不能把它与 deployable arms 混为一类。

### metric_signature

- 四格 headline BER：每 cell 64 windows × 每 window 每 arm 32768 payload bits；`Σbit_errors/Σpayload_bits`。
- paired difference：每 window 的 `BER_C4−BER_B2`，PCG64 seed `2026083004`，2000 resamples，2.5%/97.5% quantiles。
- pooled Np=2：合并 14/18 dB 的 128 个 Np=2 window，保留相同 paired difference 定义；不是把两个 cell 的相对百分比取平均。

### state_lifecycle

- 每 cell 固定 64 个 seeds；每 seed 由一个 PCG64 stream 生成同一 `Q/g/noise/pilots/payload` realization。
- 同一 window 的五个 arms 共用观测；估计器无跨 window state，逐 window 重置。
- 结论只支持 independent static windows，不支持 cross-window tracking 或时变 SOP 连续性。

## 4. 论证图

`短导频下 unconstrained 2×2 LS 保留多余法向噪声自由度` → `scaled-unitary SVD 投影删除模型内法向扰动并估计公共尺度` → `闭式逆矩阵完成偏振解复用` → `同开销、同 realization 与 B2 比较` → `四格及 pooled Np=2 BER 均改善` → `仅支持 strict scaled-unitary 目标场景中的有限公共尺度收益`。
