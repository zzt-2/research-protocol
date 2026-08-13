# [R026] 跨技术对象方法深挖包装综合

> 2026-08-13 | 关联：D032 / D034 / D035 / S024 / T029–T031

## 调研问题

在不恢复实验、文献检索或 Groundwork 的前提下，P11、P05、P08-R2 能否依靠已有本地动作链和结果，分别形成与 received-power-aware adaptive CPR 技术对象不同的硕士方法章；若不能，硬阻断在哪里。

## 发现

### 终局总表

| 技术对象 | 方法正式身份 | 当前最窄真实结果 | 终局 |
|---|---|---|---|
| 双偏振线性均衡 | **少导频 2×2 Butterfly Complex-LS 系数校准**（P11） | 固定实际 20 dB、仅 X 输出：1% pilot LS runner-defined BER `3.17625e-4`，50% label Adam `3.85875e-4`，CI 跨零；pilot-adjusted goodput proxy 约 `1.98x` | `PACKAGEABLE_NOW_WITH_LIMITS` |
| 双偏振盲在线均衡 | **面向固定流标签连续性的在线 CMA 接收机替换**（P05） | strong GG/SOP、20 dB、`f_G=30/100`：frozen supervised FIR fixed-label BER 约 `0.4992`，CMA 为 `1.76e-4/1.17e-3`；PI-BER 无稳定优势 | `PACKAGEABLE_NOW_WITH_LIMITS` |
| 编码接收/译码 | **限定工作点的 Offset-Normalized Min-Sum 译码配置方法**（P08-R2） | weak/1000 Hz/12 dB：共享 prefix-calibrated chain 上，B0 FER `0.1546875`，dev-frozen `alpha=.875, offset=.1` 为 `0.1484375`；CI `[0.00078125,0.0140625]` | `PACKAGEABLE_NOW_WITH_LIMITS` |

三项均未发现 artifact、故意错误 baseline、部署链 truth leakage 或不存在实际动作等真实性硬阻断。最初三个 agent 均倾向把理想补强当准入门；经 D032 最低合同复审后，更多 seed、更多 SNR、pristine confirmation、公平 CMA 全闭环等均被重新归为证据增强项，不是现有有限命题的包装前置条件。

### P11 章级 dossier

**章名**：少导频 Complex-LS 双偏振 Butterfly FIR 校准方法。

**方法链**：双偏振 RX 与冻结 1% pilots → 构造双偏振实值增广设计矩阵 → 两个 complex-LS 问题估计 `wXX/wXY/wYX/wYY` → 冻结 2×2、11-tap Butterfly FIR → 输出 `zX/zY`。

**主 baseline**：相同 2×2、11-tap 线性 FIR，使用前 50% 连续 TX labels 和 Adam 校准。LS 原子是方法本体，不再另称 baseline；RLS 仅作实现消融；CMA 是未裁决强邻居。

**建议小节**：

1. 双偏振 Butterfly FIR 与监督开销问题；
2. 稀疏导频 Complex-LS 建模与闭式求解；
3. 缓冲块式校准及信息边界；
4. Adam/RLS/CMA 对照边界与现有局部结果；
5. pilot-overhead、goodput proxy 与适用限制。

**必须限制**：当前只验证 X 输出；评分不是严格 payload-only；所有 cell 实际固定 20 dB；BER 差 CI 跨零；`1.98x` 是显式公式化 proxy，不是 packet goodput；CMA absorption=`UNRESOLVED`；不是在线 tracking、新 LS、新 CNN 或跨 SNR 方法。

**为什么无需先补实验**：四组系数动作真实，Adam baseline 正确；评分合同更可能给 Adam 更多 in-sample 优势，不会制造 LS 优势。X-only 与 training/pilot 混入只限制数字标签和覆盖面，不使上述局部命题为假。

### P05 章级 dossier

**章名**：面向固定流标签连续性的盲在线 CMA 双偏振接收机替换。

**方法链**：原始双偏振 RX → 单位中心抽头初始化的 2×2、11-tap CMA → 每 64 symbols 执行 Godard-with-z 更新 → fixed-label 输出；TX truth 只用于离线评分。

**主 baseline**：首 50% TX labels、15 epochs Adam 训练后冻结的同维度线性 Butterfly FIR。比较身份是“静态监督接收机 vs 盲在线接收机”的系统替换，不冒充同预算消融。

**建议小节**：

1. 固定流标签接口与 PI-BER 盲区；
2. frozen supervised Butterfly FIR baseline；
3. 在线 2×2 CMA 数据流、方程与信息边界；
4. strong GG/SOP 下 fixed-label 与 PI-BER 配对结果；
5. 场景迁移、复杂度与限制。

**必须限制**：不是 Butterfly continuation；CMA 没有数学标签锁定保证；结果只覆盖两个 20 dB cell、3 paired seeds/格；Phase A/B 是同组 paired cases，不称独立确认；PI-BER 无稳定优势；不声称新 CMA、普遍优于 ML 或端到端 FEC/framer 收益。

**为什么无需先补实验**：正式性能脚本的 15 epochs 可以直接定义 baseline，Phase0 的 20 epochs 只用于确定性检查；两格 6/6 seed 的 fixed-label delta 约 0.5，远高于 MDE，n=3 限制外推但不使两个本地条件命题为假。

### P08-R2 章级 dossier

**章名**：面向编码湍流 FSO 接收机的限定工作点 Offset-Normalized Min-Sum 译码方法。

**方法链**：双偏振 RX＋32-symbol known prefix → receiver-visible residual scale → blockwise gain/MMSE equalization → post-EQ prefix noise scale → max-log 16QAM LLR → 20-iteration LDPC offset-normalized min-sum → hard bits。

**主 baseline**：共享同一 prefix calibration、equalizer、码率和 BP 预算的 B0：`alpha=.75, offset=0`。方法新增仅为 dev-frozen `alpha=.875, offset=.1`；`clip=20` 已被共同 `llr_max=20` 吸收，不能单列贡献。

**建议小节**：

1. 编码 FSO 模型和 receiver-visible 信息边界；
2. 共享 prefix residual calibration 接收底座；
3. 工况冻结的 offset-normalized min-sum 译码配置；
4. paired trajectory FER 与 truth-only oracle 边界；
5. 单工作点适用范围与限制。

**必须限制**：prefix calibration 不是 B2 增益来源；不能称完整 2×2 channel identification；O2 是 truth-assisted oracle；只限 weak/1000 Hz/12 dB operating point；不称在线自适应、独立 clipping 增益、跨工况鲁棒或一般性 FER 改善。

**为什么无需先补实验**：B0/B2 baseline 公平、动作真实、n=40 paired 且 4 gain/36 tie/0 loss、CI 下界为正。single-slice 和 chronology debt只限制 claim ceiling，不能将现有局部参数配置方法提前否决。

## 横向判断

1. **最强现有章级结果：P05。** 数字差距大、问题解释清楚、与 CPR 技术对象独立；代价是方法原子完全经典，贡献必须严格定位为场景迁移＋receiver replacement＋fixed-label evaluation contract。
2. **最清楚的小方法：P08-R2。** 技术对象与 CPR/均衡都不同，baseline 和局部改善干净；代价是动作仅为 `alpha/offset` 配置且单工作点，适合务实硕士章，不适合高 novelty 叙事。
3. **最像传统“提出方法”的结构：P11。** 有明确闭式模型和 pilot-budget 对比，但当前结果只覆盖 X 输出且评分合同较弱；可以写，答辩防御性低于 P05。
4. P11 与 P05 同属双偏振均衡对象，不宜同时算两个独立核心技术章。若两者都收，可一主一辅或二选一。

当前可形成的跨对象骨架是：

- received-power-aware adaptive carrier phase recovery（CPR）；
- P05 或 P11（二选一，双偏振均衡）；
- P08-R2（编码接收/译码）。

这只是方法族可行性结论，不是最终 thesis spine 决策。

## 结论

三项均已经追到“包得动”的稳定终态，不需要以补实验作为方法身份准入门。若后续恢复执行，任何 confirmation 仅用于扩大 claim、增强答辩防御或修正评价合同，不得再次被偷换为“没有它就不是方法”。外部 exact-recipe duplication 仍均为 `NOT_CHECKED`。

## 对决策的影响

D035 第一批目标完成。下一步应由用户在 P05/P11 的均衡方法身份与 P08-R2 的小动作/独立对象之间讨论章节取舍；不自动派实验、检索或正文写作。
