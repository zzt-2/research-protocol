# [S019] PROMPT-019 压μ MVE 生死验证 — Q-DP3 物理 Kill

> 2026-07-14 | GW Step 4a 维度 D MVE | 状态: 完成
> 来源: PROMPT-019（用户"我让你自己做这个"）

## 目标

执行 PROMPT-019：Q-DP3 维度 D MVE 生死验证——压μ（非冻结）能否救 BER。决定 Q-DP3 方向生死。压μ PASS → Q-DP3 有恢复载体进预测性增量；FAIL → Q-DP3 物理 Kill 回路线 A 保底。

## 记录

### 执行方式

主控直接执行（代码 MVE 属中任务，未派子 agent）。读全部必读文件（decisions.md D025/D010/D018/D024/D022 + 代码基建 _cma.py/r7_freeze_quantification.py/prompt015/prompt012/prompt013 + ml_long_seq_failure.py）后直接实现+跑。

### Step 0：理论预期（TL-20）

- **PASS 机制（可能性较低）**：R1 漂移模型 drift∝μ，压μ降 fade 期间漂移 → 若 BER∝drift 则应降 BER
- **FAIL 机制（可能性较高）**：R7 冻结漂移→0 都没救回 BER → fade 期间漂移非主因；D014 真因=SOP 极化串扰；压μ期间 SOP 同样不跟 → 压μ可能无效
- **预定义 PASS**：压μ PI-BER 显著低于常规（p<0.05, ≥4/5 胜），接近 oracle
- **预定义 FAIL**：压μ与常规无显著差异，或更差

### Step 1：压μ实现

新建 `prompt019_mu_compress_mve.py`，含 `StandardCMA2x2` 类（D022 合法 standard-CMA，含 Godard 1980 z 因子）+ 压μ逻辑。

- 压μ：fade 期间（h_block < threshold）μ→μ/k（k=10 即 1e-3→1e-4），非 fade 期间恢复 μ
- 与 R7 冻结区别：冻结=skip gradient（μ_eff=0）；压μ=gradient 仍算但步长缩小（μ_eff=μ/k）
- C6 公式核对：standard-CMA 梯度 `w += μ·(R²−|z|²)·z·r*`（Godard 1980），压μ用 mu_eff 替代 mu

Smoke test PASS（500K symbols, 1 seed, 2s）。

### Step 2-4：三对照 MVE 结果

5 seeds × 3 对照（A 常规μ / B 压μ / C oracle）× 双口径（fixed/PI），f_G=100Hz, strong, N=5M, QPSK, 20dB, SOP=4e-7, late [4.375M,5M)。

| 对照 | PI-BER | fixed BER | excess PI |
|---|---|---|---|
| A 常规μ=1e-3 | 0.0275 | 0.2261 | 0.0048 |
| B 压μ（μ→1e-4） | **0.0362** | 0.2262 | 0.0135 |
| C oracle | 0.0227 | 0.0227 | 0.0000 |

- 配对 Wilcoxon p=0.5000，B 赢 **0/5**
- fixed BER 几乎不变（0.2262 vs 0.2261）= SOP swap 未被触及
- 压μ期间 SOP 漂移 mean 48.4° / max 103.9°（R7 阴影证实）

阈值敏感性 h<0.2/0.3/0.5 三档全部 FAIL（0/5）。

### 死因定位

**根因 = D014 SOP 极化串扰**：压μ降 fade 期间权重漂移（drift∝μ），但 BER 恶化来自 SOP 持续旋转下恒模代价锁定跳变，两者正交。压μ不解决 SOP 串扰 → BER 不降反升（压μ还伤跟踪能力）。

**次要原因 = 压μ触发过频**：GG 强湍流 h 中位数 0.084 << 0.3，h<0.3 覆盖 90.6%，压μ退化为全局小 μ。

### 生死判定

**FAIL — Q-DP3 物理死**。恢复动作载体不存在：R7 冻结无效（D010）+ 压μ更差（本任务）+ CMA 重锁定物理死（AFD/重收敛=0.25）。三类恢复动作全部失效。Q-DP3 回路线 A（Q-CMA-FADE + 改动1）保底。

## 决策引用

- D025：维度 A Conditional Go，压μ能否救 BER 为 MVE 生死前置（**本任务 FAIL 触发 Kill**）
- D010：R7 冻结无效全 24 组合 ΔP_div=0 + SOP 累计漂移 1774°（R7 阴影）
- D014：SOP 驱动极化串扰是 CMA BER 恶化真因（本任务死因定位依据）
- D018：双口径强制 fixed/PI 并报（本任务双口径并报）
- D022：standard-CMA 数据 + ML 29/30 赢（路线 A 保底依据）
- D023：ML 优势 N=2M 不普适 + 改动1 新颖性 PASS（路线 A 升级路径）
- **D026（新建）**：Q-DP3 压μ MVE FAIL，物理 Kill

## 范围确认

- 本轮是否在 scope boundary 内：是（PROMPT-019 是 GW Step 4a 维度 D MVE，在原始目标「GW Step 1-4a 完整流程」范围内）

## 后续

- Q-DP3 Kill，路线 A（Q-CMA-FADE + 改动1）成为唯一方向
- 改动1（发散判据驱动 ML 重训练）须先界定"ML 有优势的参数域边界"再评估增量（D023）
- 分析层贡献不变（D006/D010/D014/D024 全部有效）
- feasibility_report.md Q-DP3 节须标注 Kill
