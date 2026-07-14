# PROMPT-019: Q-DP3 维度 D MVE 生死验证 — 压μ（非冻结）能否救 BER

> 文件名: PROMPT-019-qdp3-mu-compress-mve.md
> 用途: 在新对话中执行。Q-DP3（预测性 fade 检测驱动的跨帧 DSP 恢复）维度 D MVE 第一优先验证——压μ能否救 BER。决定方向生死。
> 来源: D025（维度 A Conditional Go）+ D010（R7 冻结无效）+ D024（fade 前兆验证 PASS）+ D018（双口径）+ D022（standard-CMA 数据）
> 性质: GW Step 4a 维度 D MVE 生死验证，不是探索。
> 压μ PASS → Q-DP3 有恢复载体，进预测性增量验证；压μ FAIL → Q-DP3 物理 Kill，回路线 A 保底。

## 0. TL;DR（先读）

你在 `projects/simulation/`（本任务是跑代码 MVE）。

Q-DP3 经过维度 A 竞争分解（PROMPT-018/D025）Conditional Go 进 MVE。A0§1 核心担忧"为什么没人做"已解除，但 (b) 物理可行≠工程值得留了一个生死未知：恢复动作载体——压μ（非冻结）能否救 BER。

R7 硬冻结（μ=0）已证全 24 组合 ΔP_div=0 完全无效（D010/S008）。但"压μ"（降低非冻结，μ→μ/k）从未测过。若压μ也救不了 BER，预测性检测就没有载体 → 物理 Kill。

你的任务：跑压μ MVE，三对照（常规μ / fade 期间压μ / oracle），双口径（fixed/PI），判定压μ能否救 BER。

**最高纪律：**

1. 这是生死验证——压μ FAIL = Q-DP3 物理死。默认立场是"找它死的原因"（继承 PROMPT-018），不预设 PASS
2. 守 TL-20：先建理论预期（压μ 降漂移→应降 BER？还是像 R7 一样救不了？），偏离即查
3. 守 D018：fixed/PI 双口径必须并报，只报 PI 不报 fixed 会被审稿人攻击
4. 守 R7 阴影：R7 冻结无效不等于压μ无效（冻结=完全停更新，压μ=减速更新），但不能假设压μ一定更好——R7 实验 B 测到冻结期 SOP 累计漂移 1774°，压μ期间 SOP 同样不跟
5. 5 seeds 中间验证够（用户 S016 确认"只要不是最终版用来写在论文里的数据 5seed 够"），关键结论补 30

## 1. 必读（按优先级，全部必读）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D025（维度 A Conditional Go + 压μ MVE 前置）+ D010（R7 冻结无效全 24 组合 ΔP_div=0 + SOP 累计漂移 1774°）+ D018（双口径强制 fixed/PI 并报）+ D024（fade 前兆 85% 事件提前 ≥2µs）+ D022（standard-CMA 数据，ML 29/30 赢 p=1.19e-6）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/PROMPT_018_REPORT.md`（维度 A 完整报告——A0§1 四解释 + AFD 数据 + MVE 设计建议）
3. `stages/gw-feasibility.md` 维度 D 全文（MVE 执行规范 + FR-14 先验对照 + FR-15 贡献目标基线对照 + FR-20 参数溯源 + FR-21 oracle 上界）
4. `thesis-lessons.md` TL-20（先建理论预期）+ TL-22（好结果先查物理前提）+ TL-26（参数溯源）+ TL-27（量级核算）
5. `code-quality.md` + `reference/sim-template/`（写代码前必读）
6. `.agents/skills/sim-preflight/SKILL.md`（跑仿真前调用——C6 公式核对/C7 三方对照/C8 祖师爷警报）

## 2. Q-DP3 合并定义（来自 D024 + R006 P2.4，评估对象）

- **M** = 预测性 + 即时混合 fade 检测驱动的跨帧 DSP 恢复
- 完整方法链：前兆检测 → 状态机门控 → 触发恢复动作 → 性能指标
- **本任务只验证"恢复动作"环节**（压μ能否救 BER），检测/门控/预测性增量是后续步骤
- **C** = 双偏振星地相干 FSO（intradyne 单孔径单链路 GG 湍流 LEO，帧间衰落）
- **恢复动作约束（D025）**：必须限定为轻量响应（压μ/冻结/切换），不能是 CMA 重锁定（AFD 10µs < CMA 重收敛 40µs，比值 0.25 物理死）

## 3. 关键物理数据（来自 PROMPT-018 子 agent 实测）

| 量 | 值 | 来源 |
|---|---|---|
| fade AFD（h<0.3, f_G=100Hz, strong） | 10.12 µs = 253 blocks | 20 seeds × 10⁷ 符号实测 |
| CMA 重收敛（10⁵ sym @2.5GBaud） | 40 µs | sat.1553 L757-758 换算 |
| 压μ响应延迟 | 40 ns（1 block） | 即时门控 |
| AFD/压μ响应 | 253 | 时间窗充足 |
| R7 冻结（μ=0）ΔP_div | 0（全 24 组合） | D010/S008，完全无效 |
| 冻结期 SOP 累计漂移 | 最高 1774°/trial | R7 实验 B |
| fade 前兆可辨识 | 85% 事件提前 ≥2µs | D024 |

## 4. 要执行的 MVE

### Step 0：理论预期（TL-20，动手前先写）

写下压μ的预期机制 + 失败条件：

- **预期 PASS 机制**：R1 漂移模型 `drift=μ·R²·σ_n·√(AFD/(block·T_S))` 线性正比于 μ，压μ直接降漂移 → 应降 BER
- **预期 FAIL 机制（R7 阴影）**：R7 冻结把漂移降到 0 都没救回 BER，说明 BER 恶化主因可能不是 fade 期间权重漂移，而是 (a) fade 期间噪声驱动 CMA 误差曲面变形 (b) 恢复后 SOP 已偏（压μ期间同样不跟 SOP）(c) CMA 跟踪滞后本身（D011/D014，非 fade 相关）
- **预定义 PASS 标准**：压μ PI-BER 显著低于常规μ（配对 Wilcoxon p<0.05, ≥5 seeds），且接近 oracle
- **预定义 FAIL 标准**：压μ与常规μ无显著差异（像 R7 冻结），或压μ反而更差

### Step 1：压μ实现（在现有 _cma.py 基础上）

- **现有基建**：`common/_cma.py`（2×2 蝶形 + 1×1 退化，standard-CMA 已补 z 因子 D022）+ `common/_gg_time.py`（GG 时间模型）+ `common/_ml_equalizer.py`（ML oracle）+ `common/params.py`
- **R7 冻结实现参考**：`r7_freeze_quantification.py` 的 `CMAEqualizer2x2WithFreeze`（深衰块跳过梯度更新）
- **压μ实现**：fade 期间（h < 阈值，如 0.3）μ → μ/k（k=10 即 μ=1e-3→1e-4），非 fade 期间恢复 μ。不是完全冻结（μ→0），是减速（μ→μ/k）
- **守 C6**：压μ公式对照 R1 漂移模型（drift∝μ），确认实现正确

### Step 2：三对照 MVE

| 对照 | 方法 | 说明 |
|---|---|---|
| A | CMA 常规 μ=1e-3（无压μ） | baseline，复用 D022 standard-CMA 数据 |
| B | CMA fade 期间压 μ=1e-4（功率阈值触发 h<0.3） | 本任务核心 |
| C | oracle（fade 期间完美 MMSE） | 上界参照 |

参数：f_G=100Hz, strong(α1.5β0.8), N=5M, QPSK, SNR=20dB, SOP=4e-7(1krad/s), late slice [4.375M,5M)（与 D022 一致便于对照）

### Step 3：双口径 BER（D018 强制）

- **fixed-label BER**：固定 X→sX, Y→sY 标签
- **PI-BER（排列不变）**：完整 2!×4×4 消歧后最优匹配
- 两者必须并报。PI 需 pilot/帧头开销（不是免费性能）

### Step 4：5 seeds → 判定 → 若 PASS 补 30

- 先跑 5 seeds 看方向（用户 S016 确认中间验证 5 seeds 够）
- 5 seeds 方向明确（PASS 或 FAIL）→ 若 PASS 补到 30 seeds 做正式统计（配对 Wilcoxon）；若 FAIL 方向明确不补

## 5. 已知陷阱（本任务专属）

1. **R7 冻结≠压μ**：冻结=完全停更新（μ→0），压μ=减速更新（μ→μ/k）。R7 无效不等于压μ无效，但 R7 实验 B 的 SOP 漂移 1774° 阴影——压μ期间 SOP 同样不跟，压μ可能也救不了 SOP 极化串扰（D014 真因）
2. **压μ可能伤跟踪**：压μ不仅降 fade 期间漂移，也降正常期跟踪能力。若压μ触发太频繁或阈值太松，正常期跟踪变差反伤 BER。须记录压μ触发频率/占比
3. **阈值敏感性**：h<0.3 阈值是任意的。压μ效果可能强依赖阈值。跑完后做阈值敏感性扫描（h<0.2/0.3/0.5）
4. **D014 SOP 极化串扰**：CMA BER 恶化主因是 SOP 驱动极化串扰（D014），不是 fade 期间漂移。压μ可能降漂移但不解决 SOP 串扰 → 可能 FAIL。这是最可能的死因
5. **AFD 10µs 是均值**：中位仅 0.16µs（噪声级），长尾 p99=184µs。压μ对短 fade（中位）可能无效（太短来不及触发），对长 fade（p99）可能有效。须按 fade 深度/持续时间分层分析
6. **别只看 P_div**：R7 只看发散概率（ΔP_div=0），但 D011 证明 CMA 即使不发散也有跟踪滞后 BER penalty。本任务看 BER（PI-BER），不是 P_div

## 6. 产出格式（强制）

```text
# PROMPT-019 研究报告：Q-DP3 压μ MVE 生死验证

## TL;DR
[PASS/FAIL + 一句话理由 + 压μ救了多少 BER]

## 理论预期（TL-20）
[动手前写的预期机制 + 失败条件]

## 压μ实现
[实现方式 + C6 公式核对 + 脚本路径]

## 三对照结果（5 seeds → 30 seeds if PASS）
| 对照 | fixed BER | PI-BER | 说明 |
|---|---|---|---|
| A 常规μ | | | baseline |
| B fade压μ | | | 核心 |
| C oracle | | | 上界 |

## 统计判定
[配对 Wilcoxon p 值 + 胜场 + 是否 PASS 标准]

## 阈值敏感性
[h<0.2/0.3/0.5 三档对比]

## 分层分析（按 fade 深度/持续时间）
[短 fade vs 长 fade 压μ效果差异]

## R7 阴影验证
[压μ vs 冻结差异 + SOP 漂移影响]

## 生死判定
[PASS → Q-DP3 有载体，进预测性增量验证 / FAIL → Q-DP3 物理 Kill，回路线 A]

## 若 PASS：预测性增量 MVE 设计建议
[预测性压μ vs 响应性压μ vs 常规 三对照]

## 若 FAIL：死因 + 可复用部分
[死因定位 + 分析层/基建可复用部分]
```

## 附：决策上下文（你了解即可）

- 路线 A（Q-CMA-FADE ML 加固）已 Go 但 D023 收窄（ML 优势 N=2M 不普适），方法层单独不足以支撑强贡献
- 路线 B（Q-DP3）天花板更高，但压μ生死未知。压μ PASS → B 优先；压μ FAIL → B 死回 A 保底
- 分析层（发散 μ 主导 + SOP 极化串扰 + GG 时间模型 + fade 前兆）无论 A/B 都稳，是最确定产出
- 压μ是"恢复动作载体"验证，不是"预测性检测"验证。载体 PASS 后才验证预测性 vs 响应性增量（区分 vs JR-CMA）
