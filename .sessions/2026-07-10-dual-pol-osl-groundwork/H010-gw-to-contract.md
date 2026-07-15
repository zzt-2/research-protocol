# Handoff: GW Step 4a 完成 → 进 Contract（Q-CMA-FADE 定型）

> 来源: S020-S024（方法层穷举 + Q-DP4 评估 + 改动1 Kill）| 交接目标: 进 Contract 阶段，冻结 Q-CMA-FADE 形态，做参数溯源审计 + 反模式审查 + 实验完备性对标
> 文件名: H010-gw-to-contract.md
> 日期: 2026-07-15

## 已完成边界

**GW Step 1-4a 完整流程走完**。双偏振 OSL 搜索空间穷举（Step 1-3: 29 篇精读）+ Step 4a 四候选全部评估（Q-DP1/DP3/DP4/改动1 全 Kill）。**Q-CMA-FADE 是唯一存活方向**：分析层强（7 项稳结论）+ 方法层弱（D022 ML PI 优势 29/30 窄域统计显著）。

## Q-CMA-FADE 定型形态（进 Contract 冻结）

### 分析层（强，7 项稳结论，主控独立核验过）

1. **发散 μ 主导**（D006，384 trials，补 sat.1553 §6.3 L778 自认"发散概率未被分析"空白）
2. **SOP 驱动极化串扰是 BER 恶化真因**（D014，SOP×f_G 矩阵铁证：SOP=0 时 CMA=oracle ratio=1.0；SOP=4e-7 时 1.9-7.9×）——**论文核心分析层贡献**
3. **CMMA 不降发散**（R2，32/32 组合逐点相同 P_div）
4. **冻结完全无效**（R7，ΔP_div=0 全 24 组合，SOP 累计漂移 1774°/trial）
5. **LCR 伪相关**（R4/S009，r=0.96 是代理变量非因果：高 f_G→短 τ_c→块间 h 波动→梯度方差大→数值不稳定）
6. **GG 时间域衰落模型**（S004，AR(1) ρ≈0.99997，τ_c 落文献 1-100ms）
7. **SOP swap 一次性永久锁定 + 响应式方法结构性无效**（D027/D028，三类响应式全 FAIL：冻结/压μ/回滚）

### 方法层（弱但有，D022 数字硬）

- **D022**：ML（ButterflyCNNEqualizer2x2，Qin 2025 CNN 架构）PI-BER 优于 standard-CMA 29/30，exact p=1.19e-6（N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK 窄域）
- **方法层叙事 reframe**（主控提出，进 Contract 前定）：旧叙事"ML 缓解发散"已被 D020/D014 证伪。新叙事 = 分析层 D014（SOP 串扰真因）+ 方法层 D022（ML PI 优势）焊在一起——"为什么 ML 更好"用分析层回答（CMA 恒模多解在 SOP 下跳变 BER→0.5，ML 固定权重 swap 后消歧 PI 接近 oracle）
- **D029 Kill 强化叙事**：ML 训练一次 PI 口径已接近 oracle（excess 0.00191），swap 是标签问题非信息丢失

## 不要做什么（Dead Ends，全部已验证失败）

### 方向 Kill（物理结论，不可复活）

1. ❌ **Q-DP1 动态 SOP 跟踪**（D001）：均衡器 300krad/s 够用，A 物理基础不足
2. ❌ **Q-DP3 跨帧 fade 恢复**（D026）：压μ FAIL（0/5 胜），BER 真因是 SOP 非 fade，恢复动作无载体
3. ❌ **Q-DP4 SOP 防 swap**（D028）：形态2 约束无效（J_XCA 对 clean swap 互相关≈0）+ 形态1 回滚 dwell=11 块（R7 阴影），恒模代价多解地形结构性矛盾
4. ❌ **改动1 物理判据驱动 ML 重训练**（D029）：D=B（判据检测不到 swap + ML 训练一次 PI 已≈oracle 无重训练空间）

### 方法层升级 Kill

5. ❌ **ML 缓解发散叙事**（D020/D014 证伪）：BER 真因是 SOP 不是发散
6. ❌ **盲 VQ-VAE**（D019 deferred）：gate 崩，且 D029 证明 ML PI 口径已好，盲 vs 监督不公平问题降级
7. ❌ **自适应步长 CMA**（R005）：JR-CMA 占点
8. ❌ **DD-CMA/酉约束**（PROMPT-011 D016）：成熟先例
9. ❌ **ML 长序列"真失效"叙事**（D015 被 D018 修正）：fixed BER 0.5 是 swap 标签，PI-BER 0.005 接近 oracle

### 主控纪律 Dead End

10. ❌ **主控不自己跑诊断**：用户多次纠正，诊断交新对话
11. ❌ **不跳框架**：Contract 阶段须读 stages/contract.md，守 S0-S5 流程

## 必读（进 Contract 时按优先级读）

1. **`stages/contract.md` 全文**（Contract 阶段 S0-S5 执行规范——**进 Contract 前必须读**，FR-22）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（当前位置 + 进展线索全量 + 不变量）
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D006/D014/D018/D022/D023（分析层核心 + 方法层定型数据）
4. `projects/thesis-fso/feasibility_report.md`（Q-DP4 章节含主控修正的 A' 增量论证 + 汇总表 Q-DP1/3 Kill）
5. `projects/thesis-fso/literature_notes.md`（Q-CMA-FADE 增量定位 + Q-DP4 条目）
6. `.sessions/2026-07-09-thesis-writing/voice.md`（导师约束：不能只分析得加方法 / 特定条件优异就行 / 会议不给修改机会 / BER 10⁻⁵底线 / 没后路）
7. `thesis-lessons.md`（TL-04 增量非空白 / TL-30 跳框架 / 全速查表）

## 接口变更

无新代码改动。现有代码基建（Contract 阶段复用）：
- `projects/simulation/common/_cma.py`（CMAEqualizer2x2）
- `projects/simulation/common/_ml_equalizer.py`（ButterflyCNNEqualizer2x2）
- `projects/simulation/common/_gg_time.py`（gg_time_envelope + GGTimeParams）
- `projects/simulation/explore/cma-fade-divergence/prompt019_mu_compress_mve.py`（StandardCMA2x2 含 Godard 1980 z 因子）
- 结果 JSON 在 `projects/simulation/results/cma-fade-divergence/`（gitignored）

## 已知债务（进 Contract 须处理）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 监督 vs 盲不公平 | D008 债务1 | D029 降级（ML PI 已好，盲 VAE gate 崩） | Contract 写作时说明 limitation |
| 方法照搬 Qin CNN | D008 债务2 | 无架构创新，改动1 Kill 后无升级 | 写作时诚实标注"场景迁移+分析增量" |
| seed-bias | h_mean CV≈1.0 | 论文 limitations | 写作时 + 最终结论补 30 seeds |
| BER 10⁻⁵ 达不到 | 导师硬要求 | 当前 PI-BER ~2e-3~3e-2 | 需高 SNR 补点 or 诚实标 pre-FEC |
| SOP 旋转速率实测缺失 | FR-20 | sop_rate=4e-7 是 sat.1553 §6.3 仿真值 | Contract S3 参数溯源审计 |
| D015 口径标注 | D029 发现 | Q3-B 0.002 是 fixed-label 非 PI | ✅ 已修正标注 |

## 验证阈值（方法层历史通过率）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| ML vs standard-CMA | 30seeds p<0.05 + ML≥25/30 | D022 预注册 | PASS（29/30, p=1.19e-6, 仅 N=5M/f_G=30）|
| ML 优势跨参数域 | N=2M 多参数点 ML 赢 | D023 扩展 | FAIL（f_G=1000 ML 赢 1/5）|
| 改动1 物理判据触发 | D PI < B + 接近 C | D029 预注册 | FAIL（D=B，判据不触发）|

## 接收方验证（续接 Contract 时必须完成）

- [ ] 已读 stages/contract.md 全文（FR-22 跨阶段必须读）
- [ ] 已读 topic-index 不变量段（7+1 条）
- [ ] 已验证本文件至少 3 条关键事实：
  - [ ] D022 ML 29/30 p=1.19e-6 → 查 prompt015_unified_baseline.json
  - [ ] D014 SOP=0 时 CMA=oracle ratio=1.0 → 查 decisions.md D014
  - [ ] D029 改动1 D=B 判据 0% 触发 → 查 prompt022_modification1_mve.json
- [ ] 已确认当前范围（Q-CMA-FADE 定型，不复活 Kill 方向）
- [ ] 已确认导师约束 5 条

## 下一轮

**进 Contract 阶段**。第一步读 `stages/contract.md`，按 S0-S5 流程：
- S0：检索验证（确认 Q-CMA-FADE 增量定位 vs Qin/Nasr 不换皮）
- S1：瓶颈诊断（CMA 性能瓶颈=恒模多解 SOP 跳变，已由 D014 完成）
- S2：指标模型审计（FR-17 领域指标 + FR-19 模型假设 + D018 双口径）
- S3：参数溯源审计（FR-20，关键物理参数标文献来源）
- S4：data-flow + 动作空间审计（FR-13/FR-16）
- S5：反模式审查 + 实验完备性对标

**Contract 阶段核心任务**：把分析层 7 项 + 方法层 D022 组织成论文结构，诚实标注 limitations（方法层弱+窄域+照搬 Qin），按导师约束③"特定条件优异就行"卖窄域优势。

**纪律**：进 Contract 必须先读 stages/contract.md，不跳 S0-S5。主控控场，实验交新对话。
