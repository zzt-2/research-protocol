# Handoff: 对话 2 — 阶段 0.3-0.6 前置规约（架构定性 + 公平对照 + 参数真相源 + 文件组织）

> 来源: S002（工作对话对话 1）| 交接目标: 新工作对话执行阶段 0.3-0.6 四项规约
> 文件名: H002-conversation2-stage0-arch-fair-param-file.md
> 日期: 2026-07-08

## 到哪了（状态）

工作对话对话 1 完成阶段 0.1-0.2（够格路径验证 + dB/范围溯源核查），**未写代码，未进 sandbox**（守 profile 第 9 次防线 + INVARIANT 6）。

**阶段 0.1 核心结论**：B5-Q1 **够格走路径 C（鲁棒性维度）为主 + 路径 A/B 补充，不转 Kill**。
- 路径 C（主）：范围 15×（±4.5GHz vs 传统 ±312.5MHz）+ 56MHz/s 跟踪 + 低接收功率鲁棒性，会议够格（B7 同模式 OFC 已发先例，B5 范围 15× 比 B7 的 1.9× 更强）
- 路径 A（辅）：绝对指标对标 BUPT Arria 10 FPGA demo 会议模板（B4/B5 同模板）
- 路径 B（sandbox 验证维度）：湍流下 vs [60] Leven 补 dB 对比，若有 dB 增量则叠加够格，若无则靠 C/A
- 增量贡献：B5 锚 B2B 无湍流 → B5-Q1 加湍流验证范围优势+鲁棒性（对标 B11 加 FSO 湍流同模式）

**阶段 0.2 核心结论**：20 字段参数全溯源 PASS（±4.5GHz 五处一致 / 残频指标全读原文 / [60] Leven 7dB penalty 溯源到原文 L123 / 残频上限公式 Δfm=fs/8N 溯源到 sat.1553 引 [60] Leven 公式 27）。

**关键修正项**（H001 小事实错误）：
- H001 声称"±4.5GHz abstract/intro/experiment/conclusion 四处一致"→ 实际**五处 L23×2/L29/L47/L143/L149，不含 conclusion L167**（conclusion 只复述 ±312.5MHz + ±250MHz）
- H001 声称"[60] Leven 7dB penalty"→ B5 锚全文无此数字（B5 最大 ref [28]），数字来自 [60] Leven 原文 L123，不是 B5 锚的数字

## 下一步干什么（对话 2 = 阶段 0.3-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.3-0.6（4 项），不进 sandbox。
> **守 3 步上限**：0.3-0.6 四项规约主线定，不一定要子 agent。若超 3 步主动建议分对话。

### 阶段 0.3 架构定性（INVARIANT 13 B5 特殊，最高优先）

**核心问题**：湍流致功率波动归一化走前馈路径（合法不撞 D006）还是环路 TF 联合建模（撞 D006）？

**判定方向**（H001 已建议，需论证）：
- **走前馈归一化**（AGC / 归一化功率比）：不撞 D006，合法
- **禁环路 TF 联合建模**：撞 D006（D006 红线，B1 换皮模式）
- **关键前提验证**：前馈归一化后 B5 范围优势是否仍成立？湍流致幅度衰落会污染正负功率谱面积比 Rp-n，前馈归一化能处理但效果未知。**若前馈归一化后范围优势消失 → 红线警报（核心机制崩塌，路径 C 崩塌）**

产出 `explore/b5-leo-doppler-spectrum-foe/_architecture_decision.md`

### 阶段 0.4 公平对照框架设计（INVARIANT 14 + LEO Doppler 主题差异化）

**核心问题**：
1. baseline 是 [60] Leven Mth-power 还是传统 FFT FOE？
   - [60] Leven 是时域 Mth-power 精细 FE（有 FE 时无 penalty，无 FE 时 differential decoding 500MHz 致 7dB penalty L123），跟 B5 粗 CFO 任务环节不同
   - 传统 FFT FOE（fft_foe 4 次幂 blind QPSK 找谱峰，common/_recovery.py L37）跟 B5 同是频域找谱峰，任务环节对口
2. 范围 fair gain 怎么定义？
   - 捕获范围扩展倍数（B5 ±4.5GHz vs 传统 ±312.5MHz = 15×）
   - 残频指标对比（σ<140MHz / <5MHz vs baseline 残频）
   - BER 工作点对比（BER 1e-3 接收灵敏度 −48dBm）
3. 工作点选 BER 1e-3（B5 锚论文 + sat.1553 + [60] Leven 一致）还是 HD-FEC 3.8e-3（跨候选可比）？
4. **LEO Doppler 主题差异化**：B5（频域功率比）vs B7（定时域 TED 增益）vs B4（双反馈环），机制正交无撞车，叙事定位要明确

sat.1553 "SNR penalty vs 完美同步系统"口径（L353）可作 B5 vs baseline 公平对照框架参考。

产出 `explore/b5-leo-doppler-spectrum-foe/_fair_comparison_framework.md`

### 阶段 0.5 参数真相源前置（TL-26 + FR-26）

B5Params 草稿 20 字段全溯源已就绪（`_db_range_sourcing_audit.md` §6 表），参考 `B7Params`（params.py:611-628）扩写。关键参数：
- Doppler ±4.5GHz（B5 锚五处一致）
- Doppler rate 56MHz/s（B5 锚 L147 引 Ref [6]）
- 符号率 2.5GBaud / 波长 1550nm / 轨道 600km
- 精估范围 ±312.5MHz（=B/8，[60] Leven 公式 27 同族）
- 残频 σ<140MHz / <5MHz / 250MHz max
- 系数 α=6×10⁸ / FFT 1024 组 16 点 / ADC 5GSa/s 8bit / FPGA 312.5MHz

每个参数全标 source_type + source + audit_flag + 原文行号。先在 explore 草拟，不直接写 params.py。

### 阶段 0.6 文件组织规约

- 定死 `explore/b5-leo-doppler-spectrum-foe/` 目录结构（已建，现有 _qualification_path_validation.md + _db_range_sourcing_audit.md）
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- short_time_spectrum_foe 接口定义（参考 `fft_foe_m0_omega` sc_nda_ml_sim.py:137 作起点骨架，分块 FFT 部分复用，"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"核心算法需新写）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。进入新阶段前先一句话讲清"在干啥+为什么"
2. **INVARIANT 13 D006 边界残留**（B5 特殊）：湍流致功率波动归一化必须走前馈路径（合法不撞 D006），禁环路 TF 联合建模。**路径 C 的核心前提=前馈归一化后范围优势仍成立，阶段 0.3 必须验证**
3. **INVARIANT 14 代码基建新增需求**（B5 特殊）：short_time_spectrum_foe 需新写，可参考 fft_foe_m0_omega（sc_nda_ml_sim.py:137）作起点骨架（分块 FFT 复用），但"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"核心算法需新写
4. **TL-13 共用同一信道**：B5 从 `common/_channel.py` 导入，禁自建
5. **核查机制中性双向**（INVARIANT 10）：子 agent 产出 + 主线独立 grep 核查，只信原始数字不信归因（D-009 教训 6）
6. **TL-26 + FR-26 + V6**：每个参数标文献来源 + 读原文具体数值
7. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
8. **不污染 common**（INVARIANT 14 + 红线 6）：explore 阶段探针不直接进 experiments，MVE 通过才转正。short_time_spectrum_foe 在 explore 验证通过后才进 common

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约。short_time_spectrum_foe 接口定义在 0.6 定，实现留 sandbox/MVE）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**B5-Q1 潜在失败模式**（未触发但需警惕）：
- 阶段 0.3 前馈归一化后范围优势消失（湍流致功率波动污染功率比估计）→ **核心机制崩塌，路径 C 崩塌**，需立即停并报主控对话
- 阶段 0.4 fair comparison 后 B5 范围优势在饱和池竞争中不够突出 → 转 Kill
- sandbox 三方对照发现 B5 范围优势在湍流下不成立 → 红线警报

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B5-Q1 够格路径已验证（路径 C）| INVARIANT 11 | ✅ 阶段 0.1 完成（够格走路径 C）| 已解决 |
| B5 dB/范围溯源已核查 | INVARIANT 12 + TL-26 | ✅ 阶段 0.2 完成（20 字段全溯源）| 已解决 |
| 前馈归一化后范围优势是否成立 | INVARIANT 13 + 路径 C 前提 | pending 阶段 0.3 验证 | 0.3 |
| B5 本体无湍流无 dB | INVARIANT 11 + D005 | ✅ 0.1 确认（路径 C 加湍流作增量）| 0.3 / 0.4 |
| short_time_spectrum_foe 需新写 | INVARIANT 14 | pending sandbox/MVE 实现（0.6 定接口）| sandbox / MVE |
| B5Params 参数族待扩 | TL-26 | ✅ 20 字段溯源就绪，pending 0.5 草拟 | 0.5 |
| LEO Doppler 主题跟 B7/B4 差异化 | INVARIANT 14 | pending 阶段 0.4 叙事定位 | 0.4 |
| [60] Leven 7dB penalty 语义警示 | FR-26 | ✅ 0.2 溯源完成（是 differential decoding 无 FE 场景，不是 B5 vs [60] Leven 直接对比）| 0.4 公平对照设计时注意 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B5 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 够格路径验证 | 范围优势能转化成会议够格叙事（BUPT 模板/补 dB/鲁棒性）| INVARIANT 11 | ✅ PASS（路径 C 成立）|
| 阶段 0.2 dB/范围溯源 | ±4.5GHz + 残频指标全读原文数值 | INVARIANT 12 + V6 | ✅ PASS（20 字段全溯源）|
| 阶段 0.3 架构定性 | 前馈归一化合法不撞 D006 **+ 范围优势仍成立** | INVARIANT 13 + 路径 C 前提 | 未跑 |
| 阶段 0.4 公平对照框架 | baseline 选定 + 范围 fair gain 定义 + LEO Doppler 差异化 | INVARIANT 14 | 未跑 |
| sandbox 三方对照 | B5 短时谱/[60] Leven/传统 FFT FOE 三方归因可信 | V2+C7 (v1.3.0) | 未跑 |
| MVE 范围 fair gain | ±4.5GHz 覆盖 + 残频 <5MHz @ BER 1e-3 或范围扩展 ≥10× | D005 + INVARIANT 11 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B5 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] B5-Q1 够格走路径 C（核查 `_qualification_path_validation.md` 0.1c 判定门控段）
  - [ ] [60] Leven 7dB penalty 来自 [60] Leven 原文 L123 不是 B5 锚（核查 `_db_range_sourcing_audit.md` §3 + 主线 grep `papers/doi/10.1109_lpt.2007.891893/content.md` L123）
  - [ ] B5 锚 conclusion L167 不含 ±4.5GHz（核查 `_db_range_sourcing_audit.md` §1 + 主线 sed `papers/doi/10.1016_j.optcom.2024.130981/content.md` L163-168）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 3**（阶段 0.3-0.6 完成后）：
- 阶段 1 sandbox 三方对照（B5 短时谱 FOE / [60] Leven Mth-power / 传统 FFT FOE）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- short_time_spectrum_foe 实现（参考 fft_foe_m0_omega 作起点骨架）
- sandbox 发现 B5 范围优势消失（湍流致功率波动污染功率比）→ 红线警报（核心机制崩塌）

**对话 4**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
