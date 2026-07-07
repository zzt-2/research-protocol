# [S006] D-007 线宽参数真相源统一 + 重跑主实验/sweep

> 2026-07-07 | 阶段: Execute（sim-preflight 管辖，导师反馈触发）| 状态: 完成

## 目标

消灭线宽参数"各写各的"根因（3 套同义常量源 + 函数默认参数固化 + sweep monkey-patch），统一到 params.py 单一字段 `SystemParams.LASER_LW`，重跑全部实验验证。

## 记录

### 触发与决策（D-007）

导师 2026-07-07 意见 1（线宽扫描 10k-500kHz）触发。上轮 skill 补强已诊断根因（LASER_LW 两源差 50 倍），本轮执行修复。

**关键转折**：主线最初给 3 选项（双字段保 B11 参数 / 单字段 AWGN 改单载波 / 双字段湍流改 50kHz），用户反问"一般来说这种对比不应该是完全相同吗？怎么还分了俩？谁说的？"戳穿根因——是 D002 重定位没贯彻的遗留（B11 方法思想剥离了，B11 场景参数 25GBaud/500kHz 没清理）。用户拍板**选项 2**（AWGN 改单载波 2.5GBaud/10kHz，单字段统一）。

D-007 决策记录在 `decisions.md`。voice.md 登记 3 条原话。

### 代码改动（9 文件 + 1 deprecated 标注）

| 文件 | 改动 |
|------|------|
| `params.py` | B11Params.CLW/BAUD_RATE/PN_VARIANCE 标 DEAD（保 explore 探针 import 不破）；LASER_LW 补 Valjus sat.1553 §4.2 溯源 |
| `common/_channel.py` | `doppler_phase(N, f_res=None, f_dot=None, lw=None)` 默认参数改 None + 函数体读 SimulationConfig；`generate_shared_realization(_apsk)` 加 lw 参数透传 |
| `simulator/_b11_params.py` | 删 CLW_B11/BAUD_B11/T_S_B11，`SIGMA2_P = 2π·LASER_LW·T_S`（单载波派生）|
| `simulator/sc_nda_ml_sim.py` | rename SIGMA2_P_B11→SIGMA2_P；`awgn_wiener_channel`/`run_awgn`/`run_turb` 加 sigma2_p/lw 参数（供 sweep 传参）|
| `explore/single-carrier-nda-ml/_time_domain_crlb.py` | MVE 锚脚本改单载波参数 + **加 intra_block_tracking='segmented' 对齐 Formal**（NDA 路径修复）|
| `explore/single-carrier-nda-ml/sc_nda_ml_mve.py` | meta 字段 clw_b11→laser_lw/r_sym/sc_sigma2_p |
| `simulator/run_linewidth_sweep.py` | **删 monkey-patch `__defaults__`** 改传参注入；修对照路径 bug（sc_nda_ml_main_improved→sc_nda_ml_main）|
| `simulator/run_kf_ablation.py` + `run_dd_kf_ablation.py` | rename SIGMA2_P_B11→SIGMA2_P, T_S_B11→T_S_GLOBAL |
| `explore/nda-awgn-tracking-sandbox/experiment.py` | 加 DEPRECATED 头注（引用已删字段，不再可运行）|

### 自检（步骤 1c，全过）

- param-source grep：函数默认参数固化 = 0，__defaults__ = 0（仅注释），旧常量名 CLW_B11/SIGMA2_P_B11 = 0（代码，注释除外）
- audit_params：DEAD 从 3（kappa×3）增到 6（+CLW/BAUD_RATE/PN_VARIANCE）；LASER_LW=10000.0
- 语法检查 10 文件全 OK；import 烟雾测试全 OK（SIGMA2_P=2.5133e-05 正确）
- test_common.py 关键断言（LASER_LW==10e3, SIGMA2_LASER==2π·LASER_LW·T_S）PASS

### 重跑（步骤 2，含 NDA 路径修复）

**执行顺序**：MVE → consistency_check → 主实验 → sweep（硬约束，反了 consistency 必 FAIL）。

1. **MVE 重跑**：AWGN fair gain +0.704→+1.193（σ²p 弱 5×）；weak/moderate/strong 不变
2. **consistency_check 首次 FAIL**：AWGN-NDA 两端 rel_err 6-18%（DA/oracle 全 bit-exact 证明信道一致）
3. **NDA 路径差异诊断**：派 explore agent 对比发现根因——MVE `_time_domain_crlb.ber_nda_awgn` 用默认 `intra_block_tracking='none'`，Formal `sc_nda_ml_sim.ber_nda_awgn` 用 `'segmented'`。旧 σ²p 巧合 bit-exact，新 σ²p 暴露。
4. **修复**：MVE 加 `intra_block_tracking='segmented'` 对齐 Formal
5. **consistency 重跑 PASS**：4 场景全 0.0000% bit-exact；MVE AWGAN fair gain +1.193→+1.310（segK8 让 NDA 更强）
6. **主实验 5 seed**：AWGN +1.351±0.072（旧 +0.776±0.088）；weak/moderate/strong 逐位不变（回归 PASS）；seed0 bit-exact 复现 MVE
7. **线宽 sweep**：传参注入正路可行（无 monkey-patch）；10kHz 档 vs 主实验逐 seed 一致；500kHz 湍流崩塌重现（strong −0.816dB，真物理顶）

**子 agent 误判修正**：sweep 子 agent 报告"主实验基线陈旧"——核查发现是 sweep 脚本对照路径 bug（读 `sc_nda_ml_main_improved` 而非 `sc_nda_ml_main`），已修。不变量 10 核查机制中性双向的价值。

### 文档同步（步骤 3）

- `baseline_report.md`：AWGN 主指标表 + per-seed + avg-curve + §4.5 一致性描述
- `feasibility_report.md`：+0.704→+1.310 批量替换 + D-007 头注 + CLW 参数溯源更新
- `ADVISOR_BRIEFING.md`：§3.1 线宽 500kHz→10kHz + §4.1 参数表（线宽/符号率/Doppler）+ §4.2 AWGN 数字 + §5 segK8 叙事 + TODO-1 状态
- `REVIEW_NOTES.md`：意见 1 回应 + TODO-1 ⬜→✅ + §五 已执行段

## 决策引用

- **D-007**：AWGN 场景重定义（B11 OFDM→单载波）+ 线宽参数真相源统一（新建）
- D002（B11 重定位为理论参考）—— D-007 是 D002 遗留尾巴的清理

## 范围确认

- 本轮是否在 scope boundary 内：**是**。导师反馈触发的参数统一 + 重跑，属 Execute 阶段 sim-preflight 管辖。未跳框架（FR-22），未改 D005 Go 判定逻辑（只更新数字）。
- 范围变更：无（在原专题范围内）

## 后续

1. **简报发给导师**：ADVISOR_BRIEFING.md C4 已修正（线宽/符号率/Doppler 全场景统一），可发
2. **SD-FEC 阈值评估**（REVIEW_NOTES TODO-2）：本轮范围外，下轮
3. **补近年 Transactions baseline**（TODO-3）：取决于目标期刊层级
4. **TL-20 上界更新**：MVE 的 TL-20 awgn 上界 +0.8dB 现在触发 DEVIATION（新 AWGN gain +1.31 超旧上界），需更新到 +1.5dB 左右（下轮或写作时）
5. **NDA 路径差异的根因记录**：MVE 和 Formal 两个 ber_nda_awgn 独立实现，旧值巧合 bit-exact 新值暴露——这是"独立实现一致性验证"的局限性，segK8 这种增强必须同步两边。已记入 D-007 + usage-log。
