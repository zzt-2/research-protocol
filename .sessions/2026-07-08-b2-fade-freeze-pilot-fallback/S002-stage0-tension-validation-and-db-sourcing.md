# [S002] 阶段 0.1 张力验证设计 + 阶段 0.2 dB 溯源核查

> 2026-07-08 | 阶段: 工作对话执行阶段 0.1-0.2（不写代码）| 状态: 完成，交下一对话执行 0.3-0.6

## 目标

承接主控对话 S001 + H001 派发，执行阶段 0.1（核心命题张力验证设计）+ 阶段 0.2（dB 溯源核查），不写代码。守 profile 第 9 次"急于推进"防线 + INVARIANT 6（阶段 0 六项规约全做完才进 sandbox）。

## 记录

### 报到 + 接收方验证（Trigger 1 + Trigger 5）

读完必读清单 1-7（topic-index / H001 / S001 / decisions / step4a decisions / B2-Q2 详情 / dB 口径核验 / 饱和池警示 / registry / profile）。

**接收方验证 4 条全打钩**（核查 3 条关键事实声称）：
- ✅ step4a 实测"DA pilot BER 0.38 vs NDA 0.29"——核查 `step4a-mve-execution/decisions.md:150, 157` 原文一致
- ✅ sat.1553 L440 +1dB 口径=PE vs VV+diff——核查 `_cut-b1b2b3-verify.md:144-145, 342` + 主线 Read `content.md:440` 原文
- ✅ B2-Q2 不撞 D006——核查 `_B2-deep-fade-freeze-increment.md:68, 75`
- ✅ depends_on 4 依赖全稳定（registry 核查）
- ✅ 未违反"明确不含"

### 阶段 0.1 核心命题张力验证设计（B2 最高优先）

**派子 agent T### 核查 step4a 实测细节**（6 类参数：DA pilot 配置 / NDA-ML 配置 / fade 场景 / BER 测试 / 崩溃机制 / 公平对照框架）。产出 `_step4a_detail_extract.md`。

**主线独立 grep + python 核查子 agent 数字**（不变量 10 核查机制中性双向）：
- PILOT_OVERHEAD_DB = 1.2494 dB ✅
- SIGMA2_P = 2.5133e-5 ✅
- 每 fade 块 25 pilot / DA pilot spacing=4 / da_ml 3 元组 vs nda_ml 4 元组 ✅
- BER 0.38/0.29 出处单一（仅 D004 L157）✅

**子 agent 3 个意外发现**（主线已验证属实）：
1. **σp² 是 Wiener PN 单值**（2.51e-5），weak/moderate/strong 是 GG α/β 块衰落三档——sat.1553 σp²=0.25 是 Rytov 方差，不同物理量
2. **BER 0.38/0.29 是 γ_d=5dB 低 SNR 绝对 BER**，跟 D005 HD-FEC fair gain +1.199dB 是不同 SNR 点（不冲突）
3. **"deep fade 崩溃"机制无量化对比**——step4a 没讨论 pilot spacing（4 符号）vs fade 相干时间（100 符号 fade 块）的关系

**主线设计 fair comparison 4 维度分解**（产出 `_tension_validation_design.md`）：

| 维度 | 张力分解 | 判定 |
|---|---|---|
| A（pilot 配置）| A1 spacing 不够密 → 不成立（pilot 远比 fade 密，25 pilot/fade 块）；A2 pilot 功率/类型可探索但偏离原命题 | 部分可分解 |
| B（触发条件）| **最大差异点**——step4a 静态 BER vs B2-Q2 动态恢复是不同测度 | 可分解 |
| C（pilot-aided 类型）| C1 换算法可验证；C2 路线根本弱是红线风险 | 部分可分解（C2 红线）|
| D（信道场景）| 场景差异是 sat.1553 +1dB 不能搬的物理根因 | 可分解 |

**核心结论**：张力**可分解**，不直接 Kill。B2-Q2 真正的增量可能在**动态恢复时间**（fade 恢复期 pilot 帮助重收敛），不是稳态 BER。sandbox 三方对照（阶段 1）验证后才能定 Go/Kill。

**关键论据**（B2-Q2 不撞 step4a 反证）：step4a 对比"全程 DA ML vs 全程 NDA ML"（稳态 BER）；B2-Q2 对比"双模切换 vs 纯 blind freeze"（动态恢复 + 稳态 BER）。机制不同（全程 vs fallback）。**但**：如果 B2-Q2 pilot 侧用 da_ml 且 fade 期 da_ml 仍崩溃，则 B2-Q2 pilot fallback 也崩溃 → 维度 C2 红线风险。

### 阶段 0.2 dB 溯源核查（INVARIANT 12 + FR-26）

**主线 Read sat.1553 content.md L430-460 原文**（不只引二次引用，守 FR-26 读原文数值）。

**sat.1553 L440 +1dB 原口径精确锁定**：
- +1dB = pilot-based PE **vs** VV+差分编码
- 场景：QPSK + AWGN PN（Equation 17）scenario 4（上行强湍 σp²(Rytov)=0.25）
- 测度：SNR penalty @ BER=10⁻³
- VV+diff penalty ~1.5dB，pilot vs VV+diff +1dB → pilot 自身 penalty ~0.5dB

**五重口径差异**（B2-Q2 为什么不能搬）：
1. 对比方法：PE vs VV+diff（不是 FOE freeze 双模切换 vs blind freeze）
2. 估计对象：PE（不是 FOE freeze）
3. 调制：QPSK（不是 16-APSK M₀=8）
4. 场景：OFDM-ish AWGN PN（不是单载波时域 GG 块衰落）
5. 测度：penalty @ BER=10⁻³（不是 fair gain @ HD-FEC 或动态恢复时间）

**意外发现**（sat.1553 L440 的 B2-Q2 叙事锚点）：
> "pilot-based phase estimation could be combined with a second blind phase estimator to further improve performance [58]"

sat.1553 综述作者明确提了"pilot + 盲组合"open direction——正好是 B2-Q2 双模切换的叙事锚点（A1 归属 + 动机叙事支撑）。ref [58] 具体论文待查（阶段 0.5 附带）。

**物理根因**（为什么 sat.1553 +1dB 在单载波时域可能不成立）：
- sat.1553：pilot PE 比 VV+diff 好（两种都依赖判决/差分，fade 都退化，pilot 稍好）
- B2-Q2：pilot-aided vs blind ML（blind 用全帧积分，fade 鲁棒性不同机制）
- step4a 实证：单载波时域 pilot 反而比 blind 差（跟 sat.1553 OFDM 结论方向相反）

## 决策引用

- D001（继承）：开 B2-Q2 专题 + 首验证张力策略
- 无新建决策（阶段 0.1-0.2 是规约设计，非架构/方向决策；核心命题是否 Kill 取决于 sandbox 阶段 1，不是本阶段）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.2 前置规约，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约未全做完，本轮只做 0.1-0.2，0.3-0.6 留下一对话
- **守 3 步上限**：本轮 3 步（①报到+读必读清单 ②阶段 0.1 子 agent+主线设计 ③阶段 0.2 dB 溯源）
- **守 executor 角色边界**：只执行阶段 0 规约，不进 sandbox 不写 MVE 代码

## 后续

### 交下一对话执行阶段 0.3-0.6（H002 交接）

1. **阶段 0.3 架构定性**（前馈 vs 环路 TF）：双模切换的前馈化（fade 检测门控+模式切换不纳入环路 TF）合法不撞 D006
2. **阶段 0.4 公平对照框架设计**：baseline 是纯 blind freeze [79] 还是 sat.1553 blind gating？fair gain 测度（阶段 0.1 已建议动态恢复时间 + 稳态 BER 双测度）？pilot overhead 摊薄（fade 占空比 × 25%）？叙事定位（双模切换 vs 纯盲差异化，用 sat.1553 L440 [58] open direction 锚）
3. **阶段 0.5 参数真相源前置**：fade σp² / OSNR / 符号率 / 线宽 / pilot 配置全标 source + 读原文数值（含 ref [58] 查证）
4. **阶段 0.6 文件组织规约**：`explore/b2-fade-freeze-pilot-fallback/` 目录结构 + 命名规则

### 阶段 0.1-0.2 关键发现留给后续阶段

1. **阶段 0.1 维度 B 是 B2-Q2 最可能站住的维度**：动态恢复时间测度（step4a 没测）—— 阶段 0.4 公平对照框架要把这个制度化
2. **阶段 0.1 维度 C2 是红线风险**：sandbox 三方对照必须回答"所有 pilot-aided 变体在 fade 是否都输 NDA-ML"
3. **阶段 0.2 sat.1553 [58] 是 B2-Q2 叙事锚点**：阶段 0.4 动机叙事用这个 open direction
4. **阶段 0.2 ref [58] 具体论文待查**：阶段 0.5 附带任务

### 主控对话跟进点

- 核查阶段 0.1 的张力验证设计是否真消化了 step4a 实测反证（不是绕过）—— **主线判定：已分解为 4 维度，未绕过，但维度 C2 红线风险明确**
- 核查阶段 0.2 的 dB 溯源是否把 sat.1553 +1dB 限定到原始口径 —— **主线判定：已限定到 PE vs VV+diff，B2-Q2 增量来源已明确为独立 MVE**
- B2-Q2 跟 NDA-ML 的交叉：阶段 0.1 发现"动态恢复时间"是 NDA-ML 没测的维度，B2-Q2 若在此维度有增量对 NDA-ML 方法方向决策有交叉验证价值
