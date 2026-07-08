# Handoff: 对话 3b — sandbox 三方对照跑数 + 分层 Go/Kill 判定

> 来源: S004 | 交接目标: 新工作对话跑完三方对照（M1/M2/M3 + 消融）+ 分层 Go/Kill，给 Go/Kill 结论
> 日期: 2026-07-09
> 文件名: H004-conversation3b-sandbox-rundata.md

## 到哪了（状态）

对话 3a 执行完阶段 1 sandbox 前半（S004），5 接口全部实现 + smoke test 全 PASS + MVE 主脚本骨架跑通。关键状态：

1. **sandbox 前置债务 4 项清偿**（3 子 agent 并发 + 1 主线计算）：
   - f_dot 溯源 ✅ = **56 MHz/s**（B5 锚 optcom.2024.130981 L147，grep 核验 + params.py:904 `DOPPLER_RATE_B5=56e6` 已存）
   - SSRN 6293357 + OECC 2026 abstract 亲验 ⚠️ **仍未亲验**（Cloudflare 拦截 + PDF -400，与已知缺口一致，不阻塞）
   - 张思齐 CNKI ✅ 硕博 0 条（工具有效）+ Siqi Zhang BUPT 同组确认 + **CPE 联合切口未被吞**（JCSCR 是复杂度优化非 FOE→CPE 复用）
   - 多望远镜间距 ✅ Fried 参数主线算：强湍 r0≈1.98cm（间距>2cm 即独立分集），弱湍 r0≈31cm

2. **5 接口实现**（`projects/simulation/explore/b3-joint-estimation/`）：
   - `_b3_params.py`（B3Params + B3SandboxConfig，全标 source）
   - `multi_aperture_channel.py`（⑤ 多望远镜信道，TL-13 复用 common）
   - `frame_sync_fsts.py`（② FSTS 相关峰）
   - `mrc_combiner.py`（① MRC，单支路退化）
   - `multi_branch_phase_precorr.py`（③ 多支路相位预校正，前馈开环）
   - `joint_estimation_pipeline.py`（④ 核心，M1/M2/full/m3a/m3b 五模式）
   - `_smoke_test.py`（9 测试全 PASS）+ `b3_joint_mve.py`（MVE 主脚本骨架跑通）

3. **🔴 框架暴露的关键设计问题**（3b 必答，见"下一步"）：
   - common T_S=0.4ns（2.5GBaud），jphot 用 10GBaud（T_S=0.1ns）
   - 2.5GBaud 下 8192 符号=3.3μs，Doppler 项 π·f_dot·t²≈0.002 rad **几乎无影响**
   - jphot dB 数字（1.17dB）是 10GBaud 测的，2.5GBaud 下 Doppler 动态差 16×

## 不要做什么

1. **不要 baseline 只比传统 TS**——必须含 jphot FSTS（M2），否则增益是继承的（D002/D003 硬约束）
2. **不要用 gain_vs_M1 当 Go 判据**——用 gain_vs_M2（B3-Q2 真实增量）
3. **不要 L1 全条件 FAIL 就直接 Kill**——守 §0.4.5 分层，走 L2 Doppler crossover + L3 失效边界（S013 教训）
4. **不要走环路 TF**（前馈开环不撞 D006，INVARIANT 13）
5. **不要 claim jphot 已有的算法机制**（两段式 FOE / FSTS / BL² 降噪 / 跨极化共轭全被 claim）
6. **不要用旧"4 支路 +2~3dB"数字**（D002 修正：2 支路才 +2~3dB；4 支路 0.7-2.14dB；单支路 1.17dB）
7. **不要自建信道**（TL-13，从 common/_channel.py 导入；多支路扩展在 explore 做）
8. **不要污染 common**（5 接口全在 explore/b3-joint-estimation/）
9. **不要跳过 T_S 保真度判断直接跑全量**——2.5GBaud 下 Doppler 几乎无影响，跑出的"无增益"可能是参数族错位不是方法失败

## 必读（按优先级）

1. **本 H004 + topic-index 15 不变量**（重点 11/13/14）+ **D003**（架构前馈开环 + 公平对照三方矩阵）
2. **S004** 对话 3a 执行记录（含 T_S 问题详述 + 新债登记）
3. **`_fair_comparison_framework.md` §0.4.2 三方对照 + §0.4.5 分层 Go/Kill + §0.6.2 五接口定义**（实现蓝图）
4. **`b3_joint_mve.py`**（MVE 主脚本，3b 在此基础跑全量）+ **`_smoke_test.py`**（9 测试已 PASS，3b 可参考验证模式）
5. **`_adaptation_scan_b3.md`**（A1-A6，L1 FAIL 必读降级保底路）
6. jphot 原文 `papers/doi/10.1109_jphot.2023.3265847/content.md` L101/175/208/243/357/375/385
7. common 基建：`projects/simulation/common/_recovery.py`（fft_foe/vv_cpr/bps_cpr）+ `_channel.py`（generate_shared_realization/doppler_phase/gg_block）+ `params.py`（DOPPLER_RATE_B5=56e6 L904 / DOPPLER_HIGH=150e6 L217 缺文献）

## 下一步干什么（对话 3b = sandbox 跑数 + Go/Kill）

### 步骤 1（🔴 首要）：定 T_S/baud-rate 保真度

骨架跑数暴露 Doppler 在 2.5GBaud 下影响过小（t² 项对 T_S 敏感）。3b 先定：
- **选项 A**：B3-Q2 sandbox 用 jphot 10GBaud（T_S=0.1ns）—— 保 jphot dB 数字保真，但需改 B3Params 传自定义 T_S（不污染 common 的 SystemParams）
- **选项 B**：保持 common 2.5GBaud —— 接受 Doppler 动态小，可能 Doppler 切口在 2.5GBaud 下本就无效（物理结论）
- **建议**：走 A（保 jphot 保真），因 jphot dB 数字是 B3-Q2 的对标基准。实现：B3Params 加 r_sym_baud=10e9，信道/pipeline 内部用 1/r_sym_baud 作 T_S（不 import common T_S）

### 步骤 2：全量三方对照跑数（定 T_S 后）

`b3_joint_mve.py` 已有骨架，改 `main()` 跑全量：
- SNR sweep（gamma_bar_sweep_db 全 7 点）× f_dot sweep（4 点）× 5 模式 × 多 seed（n_seeds=10）
- S1（单链路强湍+Doppler）+ S2（单链路强湍无 Doppler = S1 fdot=0 复用）
- 消融：M3a（M2+CPE 无 Doppler）/ M3b（M2+Doppler 独立 CPE）/ M3（全量）
- 指标：BER vs SNR @ HD-FEC 3.8e-3 + FOE MSE + CPE RMSE + outage

### 步骤 3：分层 Go/Kill 判定（守 §0.4.5）

- L1 全条件：gain_vs_M2 > 0 全条件 + CPE/Doppler 贡献各≥10% → Go（强）
- L2 Doppler crossover：L1 FAIL 时扫 f_dot，高 Doppler 区 gain_vs_M2 > 0 且物理因果清晰（jphot-L208 缓变假设失效）→ Go（条件特长场景）
- L3 失效边界：jphot 高 Doppler 直接失效（BER 爆/发散），B3-Q2 仍工作 → Go（失效边界扩展）
- Kill：L1+L2+L3 全 FAIL

### 步骤 4：写 _sandbox_report.md + S005 + H005（或 Kill 文档）

## 接口变更（如涉及代码改动）

对话 3a 新增 5 接口 + 2 脚本（签名见 `_fair_comparison_framework.md` §0.6.2 + 各文件 docstring）：
- `generate_multi_aperture_realization(n_branches, Ns, gamma_bar, turb_name, f_dot, aperture_spacing_m, seed, ...)` → dict
- `fsts_frame_sync(branches, ts_template, bl)` → (offsets, corrs)
- `build_fsts_template(ts_total, bl, bn)` → np.ndarray
- `mrc_combine(branches, h_branches)` → (combined, weights)；`mrc_combine_single(rx, h)` → combined
- `multi_branch_phase_precorrect(branches, offsets, df_est, f_dot_est, phi_est)` → list；`single_branch_phase_precorrect(rx, df_est, f_dot_est, phi_est)` → ndarray
- `b3_joint_pipeline(branches, ts_template, mode, params, mod)` → dict（mode: 'full'/'m2_fsts'/'m1_traditional'/'m3a_cpe_only'/'m3b_doppler_only'）
- `estimate_block_df_sequence(rx, ts_total, bl, bn)` → list（Doppler 回归用）

**3b 可能改动**：B3Params 加 r_sym_baud + 自定义 T_S（步骤 1 选项 A）。

## 失败数据附录（如涉及路线失败）

无（3a 不 Kill，5 接口全 PASS）。骨架小规模跑数 L1 FAIL（7/28），但这是骨架非全量，且 f_dot_est 是占位（真实 Doppler 估计待 3b 接 block-df 序列），L1 数据**不可作 Go/Kill 依据**。

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| SSRN 6293357 + OECC 2026 abstract 未亲验 | FR-26 证据链 | Cloudflare/PDF 拦截，子 agent 二次尝试仍失败 | 人工浏览器补抓（不阻塞 sandbox） |
| DopplerParams.DOPPLER_HIGH=150e6 缺文献 | FR-20/TL-26 | derived 无公式，500km vs B5 600km 不一致 | 跨专题修（B3 用 56e6，不影响） |
| F_RESIDUAL=1e6 命名易混 | 代码清晰 | 实际是 FOE 分辨率非 B5 残频 | 文档标注（已记 S004） |
| T_S/baud-rate 保真度（10 vs 2.5GBaud）| TL-20 理论预期 | 骨架暴露 Doppler 在 2.5GBaud 下影响过小 | 对话 3b 步骤 1 定 |
| CPE 联合增益预期偏薄 | TL-20 | 0.1b CRB ≈0dB，消融待验证 | sandbox M3a 验证 |
| 转录错误"4 支路 +2~3dB"未全修 | TL-21 | D002 已在 decisions 修，note/verify/S031 未改 | 跨专题专门修 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| smoke test 5 接口 | 9 测试全 PASS | sim-preflight §1.6 C6-C8 | S004 PASS（9/9） |
| **sandbox gain_vs_M2** | **> 0**（L1）or 高 Doppler crossover（L2）| D003 增益归因熔断 + §0.4.5 | **待 3b 验** |
| T_S 保真度（10GBaud）| Doppler 项 π·f_dot·t² 量级显著 | 物理推导 | 待 3b 步骤 1 定 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 15 不变量（重点 11/13/14）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] f_dot = 56 MHz/s（核查 `papers/doi/10.1016_j.optcom.2024.130981/content.md` L147 + `params.py:904`）
  - [ ] 5 接口已实现且 smoke test PASS（核查 `projects/simulation/explore/b3-joint-estimation/_smoke_test.py` 跑通）
  - [ ] T_S 问题真实（核查 common `_config.py` T_S=1/2.5e9 vs jphot-L231 10GBaud，算 Doppler 项量级）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 个依赖产出已验证）
- [ ] 已确认当前范围（阶段 1 sandbox 跑数 + Go/Kill）未违反"明确不含"

## 下一轮

**对话 3b**（本轮 = 3a 完成）：
1. 定 T_S/baud-rate 保真度（步骤 1，🔴 首要）
2. 全量三方对照跑数（SNR×f_dot×5模式×多seed + 消融）
3. 分层 Go/Kill 判定（守 §0.4.5）
4. 写 _sandbox_report.md + S005 + H005（或 Kill 文档）

**对话 4**（sandbox Go 后）：阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
