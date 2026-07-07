# [S007] SD-FEC 重跑 + 近年 Trans baseline + TL-20 预期表更新

> 2026-07-07（续 2026-07-08） | 阶段：Step 4a 维度 D 收尾执行 | 状态：DONE
> 2026-07-08 续接：blit 下载 3 篇 baseline 全文 + subagent 精读 + 主线集成判断
> 来源：续接 S006（D-007 重跑完），本轮做 REVIEW_NOTES §三 TODO 收尾项

## 目标

按 REVIEW_NOTES §三 TODO，做方法结论"做扎实"的三个收尾项（去掉简报相关）：
1. SD-FEC 阈值评估重跑（TODO-2，必做）—— run_sdfec_eval.py 已改指 sc_nda_ml_main，纯后处理刷新
2. 补近年 Trans baseline（TODO-3，必做如目标 Trans）—— 子 agent 检索 + DOI 验证
3. TL-20 预期表更新（任务3）+ 消融后置项记录（TODO-8 可选）

## 记录

### 任务1：SD-FEC 阈值评估重跑（C1-C5 自检全过）

**执行**：`python simulator/run_sdfec_eval.py`（纯后处理，读 sc_nda_ml_main/_main_experiment_5seed.json，~1 分钟）

**SANITY 锚点 PASS**：HD-FEC 3.8e-3 档 4 场景全部 bit-exact 复现主实验（max |Δ| = 0.000 dB）→ **D-007 改引用无遗漏，真相源对齐**

**核心结果**（fair gain @ 各 BER 阈值，正=NDA 赢）：

| 阈值 | AWGN | weak | moderate | strong |
|---|---|---|---|---|
| HD-FEC 3.8e-3（对照）| +1.351 CI[+1.305,+1.397] | +1.529 CI[+1.131,+1.928] | +1.712 CI[+1.314,+2.110] | 不可达 |
| **SD-FEC 25% pre-FEC 2e-2（导师要的核心档）** | **+1.299 CI[+1.288,+1.309]** | **+1.348 CI[+1.065,+1.631]** | **+1.554 CI[+0.971,+2.136]** | 不可达 |
| post-FEC 1e-7 | 不可达（NDA floor 6.8e-4）| 不可达（floor 5.2e-4）| 不可达（floor 2.5e-3）| 不可达（floor 2.4e-2）|

**结论**：
1. **方法结论在更严格 SD-FEC 阈值下稳健**：25% SD-FEC 档三场景全正且 CI 下界 > 0
2. **post-FEC 1e-7 全不可达**：BER floor（5e-4~2.4e-2）远高于 1e-7，是单载波 M-APSK 无信道编码仿真的物理事实（需级联实际 SD-FEC 编解码才能评估 post-FEC），如实记录非方法缺陷
3. **strong 全档不可达**：与主实验一致（oracle 也不可达），工作区 γ_tot≥15dB per-point 赢叙事照搬

**C1-C5 自检**：C1 PASS（6档阈值网格）/ C2 PASS（HD-FEC/pre-FEC SD-FEC/post-FEC 三档标注清楚，pilot overhead 与 FEC 开销区分）/ C3 N/A（不动 baseline）/ C4 PASS（strong 不可达一致 + pilot_overhead 同源）/ C5 N/A（不新增场景）

**清理**：删 `results/sc_nda_ml_sdfec_eval/_STALE_D007.md`

### 任务2：补近年 Trans baseline（核查机制中性双向 PASS）

**检索**：派子 agent 用 `bash tools/search` 跑 4 组关键词（M-APSK carrier phase / FSO carrier sync / NDA recovery / phase noise compensation），召回 87 篇初筛 15 篇精筛 5 篇近年 IEEE Trans 级。原始结果在 `search-archive/2026-07-07/`

**DOI 验证（INVARIANT 10）**：派独立子 agent 用 Crossref API 逐个验证 5 个 DOI，**5 篇全 VERIFIED**（无 INVALID/MISMATCH）。#4 标题截断漏 "and Its Performance"、#5 年份 online 2023-10/print 2024-02 歧义已注，非幻觉。

**主线筛选写入 COMPARISON_REFS.md §一 E 段（3 篇主推）**：
- **#15 Wang et al. IEEE Photonics J 2024** "V&V Carrier Phase Estimation for Multi-Ring M-APSK with Wiener PN and Its Performance"（DOI:10.1109/JPHOT.2024.3415635）—— M-APSK+VV(我们baseline)+Wiener PN，主题极度贴合
- **#16 Wang et al. Optics Express 2024** "Enhanced frame sync + carrier recovery coherent FSO"（DOI:10.1364/OE.520452）—— 相干 FSO 载波恢复，场景最贴合
- **#17 Yu et al. IEEE TVT 2023** "Joint Frame Opt + Carrier Sync for Satellite"（DOI:10.1109/TVT.2022.3218937）—— 卫星载波同步 CRB 理论锚

**覆盖度改善**：近年+严格Trans 占比 21%(3/14) → **29%(5/17)**（严格档级口径，#15 JPhoton 档级次档不计入严格 Trans），改善但未过半。核心瓶颈仍是方法来源 Du PTL 2025 是 Letters（补 baseline 解决不了，只能靠方法深度）

**备选未实现**：#5 Zhang OptComm 2024（Elsevier 中档档级不够）/ #3 Matalla JLT 2025（SDM 光纤非卫星 FSO，方法论参照）

### 任务3：TL-20 预期表更新 + 消融后置项

**TL-20 偏离核查**：AWGN 实测 +1.351 超 D-007 前旧预期上界 +0.8（SC-NDA-ML-MVE-SPEC.md §2 表），触发"偏离即查代码"。核查结论：**合理超出非 bug**——D-007 重定义场景（σ²p 从 500kHz B11 OFDM → 10kHz 单载波，弱 5×）+ MVE 加 segmented 块内跟踪对齐 Formal 后 NDA 全帧积分优势放大。旧预期基于过强 PN，新场景 NDA 优势更大（gain 1.351 > pilot overhead 1.249 → 估计精度维度也赢 DA）。

**文档更新**：
- `SC-NDA-ML-MVE-SPEC.md` §2：预期表加"D-007 后实测"列 + 偏离处理记录段 + 新量化锚点（AWGN gain > +1.5 核对 σ²p 是否仍 10kHz）
- `baseline_report.md` §3：加 TL-20 理论预期对照段（三场景 0 DEVIATION，AWGN 合理超出已论证）
- `feasibility_report.md` FR-18：消融后置状态段（DD-KF/BPS迁移/decision-feedback DA ML 标"论文写作前补"，不影响核心结论，CCISP 紧→未来工作，基建 run_kf/dd_kf_ablation.py 已就位）
- `REVIEW_NOTES.md` §三：TODO-2/3 标 ✅，TODO-8 状态更新

## 决策引用

- 无新建 D### 决策（本轮全是收尾执行 + 文档同步，不改架构/方向/不变量）
- 引用既有：D-007（AWGN 场景重定义，上一轮 S006 新建）—— 本轮 SD-FEC 重跑结果一致性证实 D-007 改引用正确
- 引用既有：INVARIANT 10（核查机制中性双向）—— 本轮 DOI Crossref 验证落实

## 范围确认

- 本轮是否在 scope boundary 内：**是**
  - 任务1/2/3 全在 REVIEW_NOTES §三 TODO 清单内（topic-index 当前范围"Step 4a 维度 D 收尾"）
  - 没碰简报正文（ADVISOR_BRIEFING 只上轮改了附录行，本轮不动）
  - 没碰 6 次 Kill、没跳框架、没改框架文件、没污染 common
- 3 步上限：任务1/2/3 各算 1 步，未超

### 续接：blit 下载 + subagent 精读 3 篇 baseline（2026-07-08）

用户要求"把那几篇用 blit 下下来然后 subagent 精读"。

**下载（用户选"blit ieee + download 降级 备份"方案）**：
- #15 JPhoto + #17 TVT：blit --source ieee --download 下成功（IEEE 校园网认证通过，会话用量 2/50）。PDF 首页标题验证 PASS（TITLE-MISMATCH 警告是 blit 抓期刊页眉当 real_title，实际 PDF 正确）。移到 `papers/doi/10.1109_jphot.2024.3415635/` 和 `papers/doi/10.1109_tvt.2022.3218937/`，tools/convert 转 source.md（284 行 / 718 行）
- #16 OE：tools/download --doi 发现 6 月已下过（firecrawl_scrape），content.md 890 行在 `papers/doi/10.1364_oe.520452/`

**精读（3 个 subagent 并发，各 ≤500 词结构化摘要）**：

| 维度 | #15 JPhoto V&V-LMMSE | #16 OE PRBS+cyclic QPSK | #17 TVT G-PSAM CRB |
|---|---|---|---|
| 调制同款 | ✅ **(8,8)-16APSK 完全同款** | ❌ 方阵 16QAM | ❌ QPSK/16QAM |
| 信道贴合 | ⚠️ Wiener PN ✅ / 无湍流 | ⚠️ 相屏湍流 / 无 Wiener/GG | ❌ 纯 AWGN |
| 方法同类 | ✅ **NDA M₀=8 次幂同框架**（差异：LMMSE vs ML）| ❌ DA 训练序列 FOE | ❌ DA 帧优化 |
| FEC 阈值 | BER=10⁻² | 1.5e-3 | 无 FEC |
| 可对比性 | ⚠️ **最强并列 baseline** | ⚠️ 场景参照 | ⚠️ 理论锚（CRB）|

**主线集成判断**：
1. **#15 JPhoto 升级为最强并列 baseline**——星座 (8,8)-16APSK + Wiener PN + NDA M₀=8 次幂框架跟我们完全同款，差异只在权重优化（LMMSE R⁻¹p vs 我们 ML）+ 信道（无湍流）。它已把 DA-ML PE 作对照（跟我们 baseline 同款），16APSK(8,8) @ 2MHz LMMSE penalty ≈0.5dB @ BER=10⁻²，ΔvT≈3×10⁻⁴。**可作"同框架不同权重优化策略"并列对照**。风险：BER=10⁻² 阈值、40Gb/s 非我们 2.5GBaud、Genie-aided 解模糊理想化
2. **#16 OE 降级为场景参照**——调制/方法/任务层级全不同（DA-FOE vs NDA-CPE），且 content.md **公式全空**（MathJax 没抓到），复现性受限
3. **#17 TVT 定位理论锚**——调制信道方法全不同（纯 AWGN RF 卫星），但 DA&NDA CRB 推导跟我们公平对照框架理论契合（CRB_DA&NDA < CRB_NDA ≪ CRB_DA，R≈1/η）

**精读后发现的结构性缺口**：3 篇里只有 #15 方法同类但档级次档（JPhoton），严格 Trans 的 #16/#17 方法都异类。**"(8,8)-16APSK + NDA-ML + 星地 FSO + 近年 + 严格 Trans"五者交集 baseline 检索未召回**——物理事实（该交集领域窄），不是检索不全。对策：放宽到 NDA 方法大类 或 接受 Du PTL 2025 + #15 JPhoto 作主要方法对照组合。

**文档更新**：COMPARISON_REFS.md §一E 三篇评价列全改为"精读后可对比性结论"，§三盘点加第 4 条结构性缺口说明。

## 后续

1. **简报重写**（用户明确"等全弄好重写，本轮不动"）：ADVISOR_BRIEFING 现在数字是 D-007 后 +1.351 但未含 SD-FEC 新结果 + 近年 Trans baseline，等用户决定重写时机
2. **未做项**（REVIEW_NOTES TODO 仍 ⬜）：
   - TODO-4 简报修正（Doppler 参数补全等，跟简报重写合并）
   - TODO-5 上行场景纳入主实验写进 baseline_report + 简报
   - TODO-6 Doppler 参数文献溯源（F_RESIDUAL/DOPPLER_LOW 现是 assumption）
   - TODO-7 加种子到 10+
   - TODO-8 DD-KF 消融（CCISP 紧→未来工作，基建已就位）
3. **等老师定**：目标期刊层级（Trans/Letters/国内会议），决定要不要继续补方法深度（CRLB 紧致性证明等）
