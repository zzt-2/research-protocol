# [S004] 对话 3a+3b — sandbox 前置债务清偿 + 5 接口实现 + smoke test → 物理深查 Kill

> 2026-07-09 | 阶段 1 sandbox（对话 3a）| 状态：3a 完成，3b 待跑数
> 2026-07-09 续接（对话 3b）| 状态：3b 物理深查后 Kill，专题 closed
> 来源: H003 派发（PROMPT-003），本轮 = 对话 3 的前半（补债务 + 实现 + smoke），后半（三方对照跑数 + Go/Kill）拆到 3b

## 目标

执行 H003 派发的阶段 1 sandbox 前半（守 profile "急于推进"防线 + AGENTS.md 3 步上限，PROMPT-003 建议 3a/3b 拆分）：
1. 补 sandbox 前置债务 4 项（f_dot 溯源 / SSRN-OECC abstract 亲验 / 张思齐 CNKI / 多望远镜间距）
2. 实现 5 个新建代码接口（按 `_fair_comparison_framework.md` §0.6.2 蓝图）
3. smoke test + MVE 主脚本骨架（b3_joint_mve.py）跑通

## 记录

### 0. 报到 + 路径不一致发现（报到即核查）

session-governance Trigger 1 + Trigger 5（接收 H003）完成后，**独立 grep 核查发现路径不一致**：
- H003 / PROMPT-003 启动协议 / AGENTS.md 目录结构表写的产出路径 = `explore/b3-joint-estimation/`
- 阶段 0 的 8 份产出**实际在** `projects/simulation/explore/b3-joint-estimation/`
- §0.6.1 蓝图自身用的是正确路径（`projects/simulation/explore/...`）
- 本轮新建代码写入**正确路径** `projects/simulation/explore/b3-joint-estimation/`

**另含连字符目录不可作 Python 包**（explore/__init__.py L8-9 注释）：`b3-joint-estimation` 含 `-`，不能 `from explore.b3_joint_estimation import`。本轮按 b5/a3 现有模式：每脚本 `sys.path.insert` 本目录 + 直接 `from frame_sync_fsts import`（非包相对导入）。

H003 三条关键事实声称验证全 PASS（架构前馈开环 / fair gain= gain_vs_M2 / BUPT 三切口未吞没）。

### 1. 补 sandbox 前置债务（4 项，3 子 agent 并发 + 1 主线计算）

**子 agent 产出主线独立 grep 核查**（PROMPT-003 纪律）：

| 债务 | 方式 | 结果 | 主线 grep 核查 |
|---|---|---|---|
| f_dot 溯源 | 子 agent | ✅ **56 MHz/s**（B5 锚 optcom.2024.130981 L147 "maximum rate of change reaches 56 MHz/s"）| ✅ grep L147 PASS + params.py:904 `DOPPLER_RATE_B5=56e6` 存在 |
| SSRN 6293357 + OECC 2026 abstract 亲验 | 子 agent | ⚠️ **仍未亲验**（SSRN Cloudflare 拦截 + preview 截断；OECC PDF -400 + HTML 无逐篇 abstract）。标题级信号倾向"星地单链路未汇合"但不靠标题推断 | 与已知 BUPT 审计缺口一致，未恶化，不阻塞 sandbox |
| 张思齐学位论文 CNKI 核查 | 子 agent（CNKI/万方 blit）| ✅ **CNKI/万方硕博 0 条**（工具对照测试有效，"未检索到"=确无，非故障）+ Siqi Zhang = BUPT 同组确认（TTQP Photonics 2024 作者群）| ✅ B3-Q2 CPE 联合切口**未被吞**（JCSCR 是复杂度优化合并补偿，非 FOE 信号复用至 CPE）|
| 多望远镜间距 | 主线计算（Fried 参数）| ✅ 强湍 r0 ≈ 1.98cm（Cn2=1e-14, z=10km, λ=1550nm），间距 >2cm 即独立分集；弱湍 r0 ≈ 31cm | 物理推导自洽 |

**🔴 新发现的前置债（不阻塞 sandbox，登记）**：
- `DopplerParams.DOPPLER_HIGH=150e6`（params.py:217）**缺文献来源**（derived 无公式），且 500km 与 B5 锚 600km 轨道不一致。B3-Q2 用 `B5Params.DOPPLER_RATE_B5=56e6`（已 OK 溯源）作中值，不用 DOPPLER_HIGH。
- `F_RESIDUAL=1e6`（params.py:239）实际是 **FOE 频率分辨率**（Δf≈1/(4·N_fft·T_S)），**非** B5 残频（B5 残频 140-250MHz 在 B5Params 另列）。命名易混，B3-Q2 用 f_res=1e6 作 FOE 分辨率（不直接当 B5 残频）。

### 2. 实现 5 个新建代码接口（§0.6.2 蓝图）

全部写入 `projects/simulation/explore/b3-joint-estimation/`（正确路径）：

| 文件 | 接口 | 守 |
|---|---|---|
| `_b3_params.py` | B3Params + B3SandboxConfig | FR-20/TL-26 全标 source（f_dot→B5 L147，Cn2→jphot-L357，口径→jphot-L243）|
| `multi_aperture_channel.py`（⑤）| generate_multi_aperture_realization | TL-13 从 common 导入 gg_block/doppler_phase，单支路退化到 generate_shared_realization；Fried 参数判分集 |
| `frame_sync_fsts.py`（②）| fsts_frame_sync + build_fsts_template | jphot-L101 跨极化共轭相关 peak detection |
| `mrc_combiner.py`（①）| mrc_combine + mrc_combine_single | jphot-L101 共享 LO 归一化 MRC，单支路退化 |
| `multi_branch_phase_precorr.py`（③）| multi_branch_phase_precorrect + single | 前馈开环（INVARIANT 13），数学 r_k·exp(-j·(2π·df·(n-offset_k)·Ts + π·f_dot·(n·Ts)² + φ)) |
| `joint_estimation_pipeline.py`（④核心）| b3_joint_pipeline（mode='full'/M3 / 'm2_fsts'/M2 / 'm1_traditional'/M1 / 'm3a_cpe_only' / 'm3b_doppler_only'）| 复用 common fft_foe/vv_cpr/bps_cpr；两段式 FOE BL²（jphot-L175/L208）；块间 f_dot 线性回归（B3-Q2 增量，不撞 D006）；联合 CPE 复用 FOE 共轭积 |

**实现关键点**：
- 两段式 FOE：`_two_stage_foe`（粗 fft_foe + 细 BL² 降噪，jphot-L175/L208）
- Doppler 斜率：`_estimate_f_dot_from_block_sequence`（块间 Δf̂_k 序列线性回归，0.3 架构 §2.2，不撞 D006）
- 联合 CPE：`_joint_cpe`（复用 FOE 共轭积先验，0.3 架构 §2.3，0.1b CRB 预警 ≈0dB）
- BER 统计含 QPSK π/2 相位模糊 resolve（common `resolve_qpsk` 约定）—— 首次跑 smoke test 暴露此 bug，VV 后直接 demod BER=0.258（模糊），resolve 后 0.034

### 3. smoke test + MVE 骨架

**`_smoke_test.py`（9 测试全 PASS）**：
- C6 物理核查：Fried 参数强湍 1.98cm / 弱湍 31.30cm；f_dot 溯源 56MHz/s
- 接口单元：单链路退化 / 4 支路独立分集（块级相关 0.069）/ FS 定位（offset≈50）/ MRC 维度 / 相位预校正（残余 ~0）
- 管线集成：M1/M2/full 单链路跑通 BER 合理 / Doppler 维度管线跑通

**`b3_joint_mve.py`（骨架跑通）**：
- S1 单链路强湍 + Doppler 扫值 × SNR 扫值 × 5 模式 × 多 seed
- L1/L2/L3 分层 Go/Kill 判定逻辑实现
- 结果存 `results/b3_sandbox_results.json`
- 骨架小规模跑通（2 SNR × 2 f_dot × 2 seed）：L1 FAIL（7/28），L2 微弱信号（高 Doppler 区 gain_vs_M2 ~0.001）

### 🔴 框架暴露的关键设计问题（3b 必答）

骨架跑数暴露 **Doppler 在当前 T_S 下影响过小**：
- common T_S = 1/2.5e9 = 0.4ns（2.5GBaud，单载波 NDA-ML/B7 参数族）
- jphot 用 10GBaud（T_S=0.1ns）
- 8192 符号 = 3.3μs（2.5GBaud），Doppler 项 π·f_dot·t² 在此时间内 = π·56e6·(3.3e-6)² ≈ 0.002 rad —— **几乎无影响**
- M3 vs M2 的 gain_vs_M2 在高 SNR 反而变负（M3 加 Doppler 补偿反而干扰）—— 因 Doppler 项本就小，补偿引入噪声

**3b 需先定**：B3-Q2 是否应用 jphot 10GBaud 的 T_S？这影响 Doppler 物理量级（t² 项对 T_S 敏感）。jphot dB 数字（1.17dB 单支路）是 10GBaud 下测的，若用 2.5GBaud 跑，Doppler 动态范围差 16×（T_S² 比例）。这是 sandbox 保真度问题，不是 bug。

> ⚠️ **3b 续接纠错**：上面"Doppler 动态范围差 16×（T_S² 比例）"的分析**方向反了**——10GBaud 的 T_S 更小 → N·T_S 更小 → Doppler 项 π·f_dot·(N·T_S)² **更小**不是更大。换 10GBaud 救不了 Doppler 切口，T_S 不是根因。根因是物理量级本身可忽略（见续接段 3b 分析）。

## 决策引用

- **D004（新建，3b Kill）**：Kill B3-Q2——三切口全物理 FAIL（CPE CRB≈0dB + Doppler 物理可忽略 + 星地非增量）
- D001/D002/D003：superseded by D004（标 superseded 不删）
- K001（新建）：B3-Q2 Kill 验证 PASS（TL-20 理论预期 + TL-22 物理前提双重证据）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1 sandbox 前半，补债务 + 实现 + smoke，未越界）
- 未违反"明确不含"（不回头救旧候选 / 不改框架 / 不污染 common / 不跳框架）

## 🔴 续接：对话 3b — TL-20 物理量级分析 + TL-22 深查 → Kill（D004/K001）

用户"你先接着做吧"启动 3b。开跑前主线先**纠正 3a 的一个分析错误**（FR-26 自纠）：S004/H004 写"10GBaud 下 Doppler 动态更大（T_S² 比例）"——**方向反了**。Doppler 相位 = π·f_dot·(N·T_S)²，10GBaud T_S 更小 → N·T_S 更小 → Doppler 项**更小**。T_S 不是根因。

这促使主线先做 TL-20 物理量级分析（不跑全量），核心发现：

**B3-Q2 Doppler 切口在 TS 块时间尺度下物理可忽略**（f_dot=56MHz/s，B5 L147）：
- 块间（TS=320 符号）频偏跳变 = 7.2Hz（2.5GBaud）/ 1.8Hz（10GBaud）
- FOE 估计分辨率 = 610kHz（2.5GBaud）/ 2.4MHz（10GBaud）
- **块间跳变比 FOE 分辨率小 5 个数量级** → FOE 测不出 Doppler 变化
- 要破坏 jphot 缓变假设需 f_dot ≈ 4768GHz/s = 物理 LEO 最大值的 **8.5 万倍**

用户选"先深查再定"。派子 agent 深查 4 否决条件，主线独立 grep 核查：
- (a) 残余 f_dot ≤ 全 Doppler（物理必然）→ 不推翻
- (b) 56MHz/s = df/dt 非误用，LEO 文献数十 MHz/s（GHz/s 系激光不稳度非轨道斜率）→ 不推翻
- (c) jphot 未测 LEO Doppler，但块尺度缓变假设成立 → 不推翻
- (d) 公式/单位复核无误 → 不推翻
- **4 否决条件 0/4 推翻**，主线独立 grep B5 L143-149 + params.py:904 + 0.1b CRB L88 核查全 PASS

关键洞察：B5 L149 自己的 Doppler 跟踪是"750 measurements lasting ~13 min"——分钟级跨帧，Doppler 斜率只在跨帧才有意义，单帧 μs 级捕捉不到。

综合三切口：CPE CRB≈0dB（0.1b L88 已证）+ Doppler 物理可忽略 + 星地非增量（D002）→ gain_vs_M2≈0，§0.4.5 三层全物理 FAIL。

用户确认"Kill B3-Q2（物理双重证据）"。**未跑全量 sandbox**——物理已死跑只确认不翻盘，省算力守 D005。写 D004（Kill）+ K001（验证）+ voice + 标 D001-D003 superseded。

**3a 分析错误教训**：3a 骨架 L1 FAIL（gain_vs_M2≈0）当时归因"f_dot_est 占位 + T_S 问题"待 3b，实际根因是物理量级，骨架数据本就是真实信号。教训：sandbox 骨架 gain≈0 不要轻易归因"还没接好"，先做 TL-22 物理前提核查（本轮纠正了，用户"先深查再定"是对的）。

## 后续（3b Kill 后更新）

B3-Q2 已 Kill（D004/K001），专题 closed。无后续 sandbox 工作。

**Kill 后残留（交主控）**：
1. **候选池重排**：B3-Q2 Kill 后活跃候选剩 NDA-ML(dormant)/B7(active sandbox)/B5(Kill salvage 全无信号)，需主控重新排候选池决定下一个候选或转向
2. **跨专题债**：转录错误"4 支路 +2~3dB"未全修（D002 遗留，影响历史准确性不影响 B3-Q2）；DopplerParams.DOPPLER_HIGH=150e6 缺文献（跨专题）
3. **可复用资产**：5 接口代码 + f_dot 物理量级分析方法（块间跳变 vs FOE 分辨率，可作 Doppler 切口快速预筛工具）+ Fried 参数 + CRB 推导框架 + BUPT 审计方法——供后续候选/教训用
4. **方法论教训**（D004 已记）：① CRB≈0 的切口不该进 sandbox 实现层（TL-20 应作硬门控筛切口）② 任何"时变/漂移"切口必须先算算法时间窗内物理量级 vs 估计分辨率，差>3 数量级直接物理 Kill 不进 sandbox ③ sandbox 骨架 gain≈0 不要轻易归因"还没接好"，先 TL-22 物理前提核查 ④ 时间尺度对齐是时变切口首要核查项
