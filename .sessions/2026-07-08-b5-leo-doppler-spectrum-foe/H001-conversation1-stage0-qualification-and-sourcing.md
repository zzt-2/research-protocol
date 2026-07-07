# Handoff: 对话 1 — 阶段 0.1-0.6 前置规约（够格路径验证 + dB/范围溯源 + 架构 + 公平对照 + 参数 + 文件）

> 来源: S001（主控对话开题）| 交接目标: 新工作对话执行阶段 0.1-0.6 六项规约
> 文件名: H001-conversation1-stage0-qualification-and-sourcing.md
> 日期: 2026-07-08

## 到哪了（状态）

主控对话开题完成（D001），阶段 0 六项规约设计完成。**未写代码，未进 sandbox**（守 profile 第 9 次"急于推进"防线 + INVARIANT 6）。

**关键特征（工作对话首验证）**：
- B5-Q1 **不是 dB 增量是范围优势**（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展）
- D005 "赢 baseline 几 dB" 标尺下不够格（`_cut-b4b5-verify.md:64-66` 明确"本体无 vs baseline 改善 X dB 对比"）
- 会议门槛放宽允许范围维度够格（BUPT Arria 10 FPGA demo 会议模板）

→ **阶段 0.1 = 验证范围优势够格路径**，不直接当 Go 判据。

## 不要做什么（踩过的坑、已排除的方向）

1. **不要直接当 Go 跑 MVE**：范围优势够格路径未验证（不是 dB 增量）+ 饱和池警示双红旗，直接跑 = 跳阶段 0 重蹈 NDA-ML 覆辙
2. **不要跳阶段 0 直接写代码**：profile 第 9 次"急于推进"防线 + INVARIANT 6。六项规约全做完才进 sandbox
3. **不要默认够格**：B5-Q1 靠范围维度够格必须阶段 0.1 验证具体路径（BUPT Arria 10 FPGA demo 会议模板 / 补 dB 对比 / 鲁棒性维度），不能因为"15× 范围扩展听起来很厉害"直接够格
4. **不要走环路 TF 联合建模**：阶段 0.3 湍流致功率波动归一化必须走前馈路径（合法不撞 D006），环路 TF 联合建模撞 D006
5. **不要自建信道**：B5 从 `common/_channel.py` 导入（TL-13）
6. **不要污染 common**：explore 阶段探针不直接进 experiments，MVE 通过才转正。short_time_spectrum_foe 在 explore 验证通过后才进 common
7. **不要把 B5-Q1 当"稳够格"候选**：范围优势够格路径 + 饱和池竞争 + 代码新增需求三重风险。如果阶段 0.1 验证后范围优势无法走会议够格路径，转 Kill 是合法选项

## 必读（按优先级）

1. **本 H001 + topic-index**（14 不变量，重点 11/12/13/14 B5 特殊风险）
2. **S001** 开题 + 阶段 0 规约设计 + 复用基建盘点
3. **B5 锚论文全文**（`papers/doi/10.1016_j.optcom.2024.130981/content.md` 252 行，2026-07-04 用户手动下载落盘）—— abstract/intro/experiment/conclusion 四处一致 ±4.5GHz，残频指标全在
4. **B5-Q1 详评**：
   - `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` L55-60（M-C-A 草稿）+ L100-167（全文增量核验段，S003 已做 D006/D005/范围三维判定）+ L162（D006 边界残留）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b4b5-verify.md` L59-69（范围优势核验）+ L64-66（"本体无 vs baseline 改善 X dB"警示）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-map-final-b1-b12.md` §A L19-29（饱和池定位）+ §C L118-165（饱和池警示）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b4b5-paillier-pool.md` L39-46（B5 切法动作 + Paillier 大池定位）
5. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe L37 / fft_foe_m0_omega 在 sc_nda_ml_sim.py:137 / 其他估计器）+ `params.py` L611-628（B7Params 参数族模板）
6. **sim-preflight v1.3.0**：`rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条 + `SKILL.md` §1.6 C6-C8
7. **框架文件**：`stages/gw-feasibility.md` §D 维度 D MVE 11 步 + thesis-lessons TL-13/20/26
8. **上游决策链**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md`（D005 务实路线 / D006 红线 / D017/D018 判读框架）+ S031（B5-Q2 排第二档 #6 依据）
9. **参照候选（LEO Doppler 主题交叉）**：
   - `.sessions/2026-07-08-b7-gardner-ted-foe/` — B7 Gardner TED（LEO Doppler rate 适配，机制正交）
   - `.sessions/2026-07-06-step4a-mve-execution/decisions.md` L113/119/247 — NDA-ML Doppler 已建模但是残余级（F_RESIDUAL=1MHz），不是 B5 ±4.5GHz 全量程

## 下一步干什么（对话 1 = 阶段 0.1-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.1-0.6（6 项），不进 sandbox。
> **守 3 步上限**：0.1 派子 agent（核查 B5 全文 + BUPT 模板对标），0.2-0.6 主线定。若超 3 步主动建议分对话。

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读必读清单 1-9。

### 步骤 2：阶段 0.1 够格路径验证（B5 最高优先）

> INVARIANT 11（B5 特殊）前置 + sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报。

**0.1a 核查 B5 范围优势的具体指标**（派子 agent，≤15 分钟）：
- 读 `papers/doi/10.1016_j.optcom.2024.130981/content.md` 全文（252 行）
- 核查所有数字（abstract/intro/experiment/conclusion 四处一致 ±4.5GHz，残频 σ<140MHz / <5MHz / ±312.5MHz 精估范围 / BER 1e-3 −48 dBm）
- 核查 B5 vs [60] Leven 的对比（本体无"vs baseline 改善 X dB"对比只给绝对指标）
- 核查 B5 是否验证了湍流场景（`_B5-...-increment.md:144` 自承"未涉湍流仅 B2B 实验"）

**0.1b 验证够格路径**（主线定）：
- **核心问题**：±4.5GHz vs 传统 ±312.5MHz 的 15× 范围扩展能不能当 D005 会议门槛下的 Go 判据？
- **够格路径选项**（每条都要论证）：
  - **路径 A（BUPT Arria 10 FPGA demo 会议模板）**：绝对指标够发会议（B4/B5 同模板），B5 范围扩展 + 绝对残频 <5MHz 是绝对指标。对标 B4（Arria 10 demo ±920MHz @ 0.5dB）看 B5 ±4.5GHz 范围扩展够不够会议级
  - **路径 B（补 dB 对比）**：在星地湍流信道下 vs [60] Leven 做 dB 对比。但 B5 本体无湍流无 dB，强补可能不真实
  - **路径 C（鲁棒性维度）**：范围扩展 + 鲁棒性（Doppler rate 56MHz/s 下的跟踪稳定性）够格
  - **路径 D（Kill）**：范围优势无法走会议够格路径，转 Kill
- **判定门控**：
  - 路径 A/B/C 任一成立 → B5-Q1 够格，进 0.2
  - 三条路径都不成立 → **红线警报**，B5-Q1 转 Kill
- 输出 `explore/b5-leo-doppler-spectrum-foe/_qualification_path_validation.md`

### 步骤 3：阶段 0.2-0.6（主线定，不一定要子 agent）

**0.2 dB/范围溯源核查**（INVARIANT 12 B5 特殊）：
- ±4.5GHz 出处（B5 锚 optcom.2024.130981，abstract/intro/experiment/conclusion 四处一致）
- 残频指标全读原文数值（σ<140MHz 最大 250MHz 含激光抖动 / 精确补偿 <5MHz / ±312.5MHz 精估范围 / BER 1e-3 −48 dBm）
- 读 [60] Leven 的 7 dB penalty 数字（differential decoding 500MHz 致 7dB，`_B5-...-increment.md:43`）
- 输出 `explore/b5-leo-doppler-spectrum-foe/_db_range_sourcing_audit.md`

**0.3 架构定性（前馈归一化 vs 环路 TF）**（INVARIANT 13 B5 特殊）：
- B5 前馈功率比假设信号幅度稳定，湍流致幅度衰落会污染功率比估计
- **若把湍流致功率波动纳入前馈归一化（AGC/归一化功率比）则不撞 D006**
- **若纳入环路 TF 联合建模则撞 D006**（边界，只标不砍，与 B6-Q2/B7-Q2 同模式）
- 决策：建议前馈归一化（避免 D006 纠缠），但需论证前馈归一化后 B5 的范围优势是否还成立
- 输出 `explore/b5-leo-doppler-spectrum-foe/_architecture_decision.md`

**0.4 公平对照框架设计**（INVARIANT 14 B5 特殊 + LEO Doppler 主题差异化）：
- baseline 是 [60] Leven Mth-power 还是传统 FFT FOE？
- 范围 fair gain 怎么定义？（捕获范围扩展倍数 / 残频指标对比 / BER 工作点对比）
- 工作点选 BER 1e-3（B5 锚论文）还是 HD-FEC 3.8e-3（跨候选可比）？
- **LEO Doppler 主题差异化**：B5（频域功率比）vs B7（定时域 TED 增益）vs B4（双反馈环），机制正交无撞车，但叙事定位要明确
- 输出 `explore/b5-leo-doppler-spectrum-foe/_fair_comparison_framework.md`

**0.5 参数真相源前置**（TL-26 + FR-26 读原文数值）：
- B5 参数一开始进 params.py 单字段：
  - Doppler ±4.5GHz（B5 锚 abstract/intro/experiment/conclusion 四处一致）
  - Doppler rate 56MHz/s（B5 锚 experiment，引用 Ref [6] NEO 600km 轨道）
  - 符号率 2.5GBaud（B5 锚 PM-QPSK）
  - 波长 1550nm（B5 锚）
  - 精估范围 ±312.5MHz（B5 锚，2.5Gbaud/8）
  - 残频指标 σ<140MHz / <5MHz（B5 锚）
- 每个参数全标 source_type + source + audit_flag + **读原文具体数值**
- 参考 `B7Params`（params.py:611-628）扩 B5Params 草稿（不直接写 params.py，先在 explore 里草拟）

**0.6 文件组织规约**：
- 定死 `explore/b5-leo-doppler-spectrum-foe/` 目录结构
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- short_time_spectrum_foe 接口定义（可参考 fft_foe_m0_omega 作起点骨架）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。进入新阶段前先一句话讲清"在干啥+为什么"
2. **INVARIANT 11 够格路径首验证**（B5 特殊）：0.1 必须验证范围优势在 D005 会议门槛下的够格路径。**默认够格 = 跳阶段 0 重蹈覆辙**
3. **INVARIANT 12 饱和池警示 + Paillier 大池**（B5 特殊）：B5 饱和池 §A 跟 B4 共锚 Paillier 43 篇大池。切法地图 §C 警示"饱和池是 dB 最难出区"。B5 走范围维度能否绕开此警示需 0.1 验证
4. **INVARIANT 13 D006 边界残留**（B5 特殊）：湍流致功率波动归一化必须走前馈路径（合法不撞 D006），禁环路 TF 联合建模
5. **INVARIANT 14 代码基建新增需求**（B5 特殊）：short_time_spectrum_foe 需新写，可参考 fft_foe_m0_omega（sc_nda_ml_sim.py:137）作起点骨架（分块 FFT 复用），但"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"核心算法需新写
6. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
7. **TL-26 参数溯源 + 读原文数值**：每个参数标文献来源 + **读原文具体数值**（D-009 教训 5）
8. **TL-13 共用同一信道**：B5 从 `common/_channel.py` 导入，禁自建
9. **核查机制中性双向**（继承）：子 agent 产出 + 主线独立 grep 核查，只信原始数字不信归因

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约 + 核查探针。核查脚本若写，放 `explore/b5-leo-doppler-spectrum-foe/`，私有 `_` 前缀，不进 experiments/）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**B5-Q1 潜在失败模式**（未触发但需警惕）：
- 阶段 0.1 验证后够格路径三条都不成立 → B5-Q1 转 Kill
- 阶段 0.3 前馈归一化后范围优势消失（湍流致功率波动污染功率比估计）→ 核心机制崩塌
- 阶段 0.4 fair comparison 后 B5 范围优势在饱和池竞争中不够突出 → 转 Kill

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B5-Q1 够格路径未验证 | INVARIANT 11 | pending 阶段 0.1 验证 | 0.1 |
| B5 本体无湍流无 dB | INVARIANT 11 + D005 | pending 阶段 0.1 够格路径 + 0.4 公平对照 | 0.1 / 0.4 |
| short_time_spectrum_foe 需新写 | INVARIANT 14 | pending sandbox/MVE 实现 | sandbox / MVE |
| B5Params 参数族待扩 | TL-26 | pending 阶段 0.5 草拟 | 0.5 |
| LEO Doppler 主题跟 B7/B4 差异化 | INVARIANT 14 | pending 阶段 0.4 叙事定位 | 0.4 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B5，B5 参数选择可参考 NDA-ML 教训 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 够格路径验证 | 范围优势能转化成会议够格叙事（BUPT 模板/补 dB/鲁棒性）| INVARIANT 11 | 未跑 |
| 阶段 0.2 dB/范围溯源 | ±4.5GHz + 残频指标全读原文数值 | INVARIANT 12 + V6 | 未跑 |
| 阶段 0.3 架构定性 | 前馈归一化合法不撞 D006 | INVARIANT 13 | 未跑 |
| sandbox 三方对照 | B5 短时谱/[60] Leven/传统 FFT FOE 三方归因可信 | V2+C7 (v1.3.0) | 未跑 |
| MVE 范围 fair gain | ±4.5GHz 覆盖 + 残频 <5MHz @ BER 1e-3 或范围扩展 ≥10× | D005 + INVARIANT 11 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B5 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] B5 本体无"vs baseline 改善 X dB"对比只给绝对残频/范围指标（核查 `_cut-b4b5-verify.md:64-66`）
  - [ ] ±4.5GHz 出处 B5 锚 abstract/intro/experiment/conclusion 四处一致（核查 `papers/doi/10.1016_j.optcom.2024.130981/content.md:23, 29, 143, 167`）
  - [ ] B5 不撞 D006（前馈频域找谱峰，核查 `_B5-short-time-spectrum-cfo-increment.md:145, 162`）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 依赖：上游 + 切法地图 + 精读沉淀 + step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 2**（阶段 0.1-0.6 完成后）：
- 阶段 1 sandbox 三方对照（B5 短时谱 FOE / [60] Leven Mth-power / 传统 FFT FOE）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- short_time_spectrum_foe 实现（参考 fft_foe_m0_omega 作起点骨架）
- sandbox 发现 B5 范围优势消失（湍流致功率波动污染功率比）→ 红线警报（核心机制崩塌）

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
