# [S002] 仿真基础设施重建：18 Agent 深度分析记录

> 2026-06-12 | 深度分析 | 进行中
> Batch 1 (A1-A6) 现状审计 + Batch 2 (B1-B6) 最佳实践研究 + Batch 3 (C1-C6) 方案设计全部完成
> 待执行：与用户讨论并冻结最终方案，然后执行迁移

## 目标

派 18 个子 agent 对仿真基础设施进行全方位分析，为后续方案设计提供证据基础。

---

## Phase 7: Batch 1 — 现状深度审计（A1-A6）

### A1: SPEC.md 参数完整性 & 来源审计

**审计范围**：SPEC.md 中所有数值参数（41个）

**审计结果汇总**：

| 类别 | 总计 | ✅ 完整 | ⚠️ 部分 | ❌ 缺失 |
|------|------|---------|---------|---------|
| 系统参数 (§1.3) | 8 | 3 | 2 | 3 |
| 湍流 GG 参数 (§1.4) | 6 | 0 | 6 | 0 |
| KF Q 矩阵 (§2) | 6 | 0 | 0 | **6** |
| KF 初始化/辅助参数 | 4 | 0 | 0 | **4** |
| DPLL 参数 (§2) | 5 | 2 | 3 | 0 |
| FOE 参数 (§2) | 7 | 3 | 4 | 0 |
| 其他 | 5 | 1 | 2 | 2 |
| **总计** | **41** | **9 (22%)** | **17 (41%)** | **15 (37%)** |

**高风险缺失（按严重性排序）**：

1. **sigma2_turb (弱/中/强)** — 三个值 (1e-6, 1e-4, 1e-3) 直接控制 KF Q 矩阵，决定 KF 跟踪行为。零来源。如果偏离正确量级，所有 KF 结论都可能失效。

2. **F_RESIDUAL = 1 MHz** — 决定 FOE 后残余相位旋转率。与激光相位噪声和多普勒速率一起构成相位模型。无分析依据。

3. **Q_fine_df = (50e3)²** — 在所有 KF 恢复函数中覆盖 design_Q() 计算的 Q[1,1]。SPEC 中未记录此覆盖行为。

4. **BLOCK = 100** — 定义信道相干间隔。SPEC 6.1#13 已指出 BLOCK=20 在强湍流下表现更优 1.74 倍。具体数值无来源。

5. **导频开销 5%** — B4 测试确认 near-optimal，但未记录初始设计公式。

6. **P_init 值** — `[(pi/4)², (2*pi*100e3)²]` 在所有 KF 变体中硬编码，从未被验证。

**关键发现**：

- **Q 矩阵理论与实现不一致**：SPEC.md 定义了 Q_TURB_PARAMS 含 sigma2_turb 和 kappa 两个字段，但 design_Q() 仅读取 sigma2_turb。所有三个 kappa 值是**死参数**——在代码中从未被引用。
- **Q_fine_df 覆盖未记录**：design_Q() 的 Q[1,1] 计算被所有 KF 恢复函数用固定值 (50kHz)² 覆盖，SPEC 未记录此设计决策。
- **DEF_B_BPS = 32, DEF_NW_BPS = 61** — BPS 算法参数完全没有来源。
- **alpha_ema = 0.5** — EMA 平滑系数仅粗略验证。

**完整参数**：R_SYM (Zhao 2025)、T_S (推导)、f_c (C-band 标准)、ζ = √2/2 (Butterworth 设计点+仿真验证)、wT 上限 = 0.5 (PLL 稳定性约束)、nfft_zp = 8192 (工程选择)、Hanning 窗 (领域惯例)。

### A2: common.py 代码结构 & 模块化审计

**代码规模**：769 行，38 个函数，17 个全局常量

**函数聚类**（6 个自然分组）：

| 聚类 | 函数数 | 行范围 | 职责 |
|------|--------|--------|------|
| A: 信道模型 | 2 | 69-74, 200-205 | gg_block, doppler_phase |
| B: 调制/解调 | 10 | 76-197 | QPSK/16-QAM 调制解调、BER计数、硬判决 |
| C: 载波恢复 | 6 | 142-297 | FFT-FOE、DPLL、VV、BPS、Fixed 管线 |
| D: 卡尔曼滤波器 | 6 | 300-635 | design_Q、kf_unified、三种KF恢复变体 |
| E: 信号生成与均衡 | 6 | 380-472 | generate_shared_realization、insert_pilots、MMSE均衡 |
| F: 编排与I/O | 8 | 641-769 | run_* 便捷函数、run_trial_shared、save_results |

**依赖关系**（自下而上 DAG，无循环）：
```
常量 → [信道模型] + [调制/解调] → [信号生成与均衡]
  → [载波恢复] + [卡尔曼滤波器] → [编排与I/O]
```

唯一跨簇依赖：kf_unified 在第 326 行调用 vv_cpr 做 KF 初始化（16符号块）。

**耦合问题**：

1. **generate_shared_realization 硬编码 qpsk_mod**（第 392 行）→ 16-QAM 实验必须复制信号生成逻辑（约20行，在2个文件中重复）
2. **kf_pilot_recovery 97 行**，KF 更新步骤重复 3 次（第 571-586、598-613、617-633 行）→ 无法单独测试 h 估计逻辑
3. **7 个脚本使用 from common import *** → 任何重构有破坏风险
4. **run_trial_shared 硬编码方案名称**（'fixed', 'kf_oracle', ...）→ 新方案需改此函数

**可测试性**：
- 纯函数（可直接测试）：qpsk_mod/demod, ber_count, fft_foe, dpll_track, vv_cpr, bps_cpr, kf_unified 等
- RNG 依赖（需固定种子）：gg_block, doppler_phase
- I/O 副作用：save_results
- 有状态跨块传递：kf_*_recovery（状态通过函数参数传递，是良好模式）

**建议模块划分**（来自 A2 审计）：

| 模块 | 内容 | 约 行数 | 公共 API |
|------|------|---------|---------|
| config.py | 所有常量字典 | ~30 | 全部常量 |
| channel.py | gg_block, doppler_phase + TURB/BLOCK/R_SYM 等 | ~50 | gg_block, doppler_phase |
| modulation.py | QPSK/16-QAM 调制解调、hard_decision、ber_count/resolve、ber_eval | ~120 | 所有函数 |
| carrier.py | fft_foe, dpll_track/dd, vv_cpr, bps_cpr, carrier_recovery_fixed | ~110 | 所有函数 |
| kalman.py | design_Q, kf_unified, kf_*_recovery, PILOT_PATTERN | ~250 | kf_*_recovery |
| signal.py | generate_shared_realization, insert_pilots, mmse_equalize, amp_limit, equalize_* | ~100 | 生成和均衡函数 |
| experiment.py | run_*, run_trial_shared, save_results, db_ratio | ~130 | run_*, save_results |
| __init__.py | 向后兼容重导出 | ~30 | 全部公共名称 |

**向后兼容策略**：创建 common.py 垫片，重导出所有名称。实验脚本零改动即可工作。

### A3: CONCLUSIONS.md 结论可靠性审计

**审计结果**：CONCLUSIONS.md 含 22 条带编号结论（C3-01 到 C3-05, C4-01 到 C4-15）+ 10 条待重验（P系列）+ 9 条已证伪（X系列）+ 3 条被拒结论。

**与附录 G 的差异**（附录 G 已过时，需要重写）：

| 差异类型 | 数量 | 说明 |
|---------|------|------|
| 附录 G 分级偏低 | 6 条 | C4-01/06/11/C3-01/C4-07/C4-12 在 common.py 重验后已升级，附录 G 未回写 |
| 编号映射错误 | 3 处 | C3-04/C4-07/C4-12~14 的描述与实际内容不匹配 |
| 新增结论遗漏 | 3 条 | C4-13(VV/BPS不兼容16-QAM)、C4-14(16-QAM强湍流BER平台)、C4-15(阻尼系数无显著影响) |
| 状态矛盾 | 1 条 | P-06 已标注"已重验"但仍留在待重验表中 |
| 措辞待确认 | 1 条 | P-09 标注"需修正措辞"但修正状态不明 |

**内部一致性检查**（7 对结论交叉验证）：全部一致。关键一致对：
- C4-01 vs C4-07：KF 强湍流 3.46% vs DPLL 1.88%，结论"KF 在强湍流下不如 DPLL"完全匹配
- C4-03 vs C4-10：VV 二态失败根因（h<0.02）与理论判据（β<1 时 E[1/h] 发散）一致
- C3-02 vs C3-05：QPSK 免疫（退化 0.12dB）vs 16-QAM 敏感（退化 11.6dB），物理解释一致

**建议**：
1. 重写附录 G（修正分级 + 编号 + 补充 C4-13/14/15）
2. P-06 从待重验表升级为主结论（或标注"已验证，待格式化"）
3. 确认 P-09 措辞修正状态

### A4: .sessions/ 专题生命周期合规审计

**审计范围**：_registry.yaml 中 21 个注册专题 + 磁盘上 5 个未注册目录

**严重不合规问题**：

1. **9 个已归档专题仍标 active/dormant**：目录已在 _archive/ 但注册表状态未更新：
   - framework-evolution, direction-scouting, thesis-structure-research (active → 应 closed)
   - chapter-quality-audit, thesis-chapter-fixes (active，且 description 自称"已关闭")
   - 2026-05-13-* (dormant → 应 closed)
   - 2026-05-17-leo-congestion-routing (dormant → 应 closed)

2. **3 个磁盘目录未注册**：
   - 2026-05-31-thesis-writing-prep (36文件/9,059行)
   - 2026-05-31-thesis-writing (36文件/3,591行)
   - 2026-06-04-citation-verification (5文件/452行)

3. **thesis-direction-pivot 膨胀**：108 文件 / 23,653 行，最后更新 12 天前，仍标 active。应标 dormant。

4. **thesis-chapter-fixes 重复 YAML 键**：两个 depends_on 键，第二个覆盖第一个。

5. **thesis-final-review 目录未归档**：注册表已标 closed 但目录仍在活跃位置（34文件/7,547行）。

**应标 dormant 的专题**：
- thesis-direction-pivot (108文件/2.4万行)
- thesis-sim-exploration (1文件/111行)
- thesis-simulation-consolidation (5文件/714行)
- 2026-05-30-ch3-direction-exploration (7文件/959行)
- 2026-06-04-advisor-review-revision (42文件/5,971行)

**真正活跃的专题仅 2 个**：2026-06-10-research-direction-exploration 和 2026-06-12-simulation-foundation-rebuild。

**建议动作**：
- P0（5分钟）：修正 9 个已归档专题的注册表状态为 closed，修复重复 YAML 键
- P1（15分钟）：将 thesis-direction-pivot 等 5 个专题标 dormant，将 thesis-final-review 移入 _archive/，补注册 3 个未注册目录

### A5: 公式文档冗余审计

**审计范围**：7 个公式相关文件，5096 行

**文件清单**：

| 文件 | 行数 | 公式编号 | 性质 |
|------|------|---------|------|
| formulas-master.md | 2260 | F1-F36, F3.1-F3.33, F4.1-F4.14, F5.1-F5.28 | 聚合主库 |
| formulas-index.md | 299 | 全部 133 条索引 | 派生索引 |
| formulas-ch2-system-model.md | 704 | F1-F36 | **100% 冗余**（与 master Ch2 完全重叠） |
| formulas-ch3-link-performance.md | 329 | F3.1-F3.21 | **100% 冗余**（与 master Ch3 完全重叠） |
| formulas-ch3ch4-sync.md | 945 | F3.1-F3.14, F4.1-F4.46 | 部分冗余 + **32 条独有**（F4.15-F4.46） |
| formulas-ch4-kf.md | 219 | F4.K1-F4.K13 | 部分冗余 + **13 条独有**（KF 完整推导链） |
| formulas-ch5-fpga.md | 340 | 无 F5.x 编号 | 互补性质（架构/资源/验证，非公式） |

**去冗余方案**：
1. 将 F4.15-F4.46（32条 FFT/VVPE/BPS/DPLL 补充推导）迁入 master Ch4
2. 将 F4.K1-F4.K13（13条 KF 推导链）迁入 master Ch4
3. 归档 ch2-system-model.md (704行) 和 ch3-link-performance.md (329行)
4. 重命名 ch5-fpga.md 为 fpga-reference.md（它不是公式文件）
5. 更新 formulas-index.md 反映合并后完整列表

**预期效果**：7 文件/5096行 → 3 文件/~3350行（减少 ~1750 行、4 个文件）

### A6: 实验脚本有效性审计

**审计范围**：27 个 Python 脚本（含 common.py）+ 16 个结果文件

**关键事实**：

1. **VV 公式从未在 common.py 中出错**。错误存在于旧 stress_common.py（`unwrap(angle*M)/M` vs 正确 `unwrap(angle)/M`）。所有 16 个结果文件都在正确的 common.py 下生成。

2. **common.py 有 129 行未提交更改**，全部为添加性（QAM16 支持 + dpll_track_dd + hard_decision 提取 + save_results），未触及任何信号处理核心。

3. **结果分类**：

| 类别 | 数量 | 说明 |
|------|------|------|
| 可直接复用 | 12 | multi_seed_sweep, nw_sweep 系列, dpll_omega_sweep 系列, nmse 系列, zeta_sweep |
| 附条件可用 | 7 | bridge_ch3_ch4, nmse_vs_ber（缺元数据但核心未变）, QAM16 相关 |
| 诊断/非论文 | 6 | plot_snr_curves, test_qam16, vv_formula_head2head, vv_formula_math, analytical_* |
| 需重跑 | **0** | 无脚本产出错误结果 |
| 应废弃 | **0** | 无脚本存在根本缺陷 |

4. **结果文件元数据**：仅 3 个文件有 _meta MD5（dpll_zeta_sweep 匹配当前 common.py，其余 2 个为中间版本但信号核心未变）。13 个结果文件无元数据跟踪。

5. **Fixed 方法 omega_n 注意**：multi_seed_sweep.py 的 Fixed 方法需确认使用 FIXED_CFG_OPTIMAL（omega_n=20MHz）而非默认 FIXED_CFG（omega_n=8MHz）。

---

## Phase 8: Batch 2 — 最佳实践研究（B1-B6）

### B1: 仿真代码组织最佳实践

**参考项目**：
- **OptiCommPy**（光纤通信仿真）：域层扁平模块 — `comm/modulation.py`, `dsp/carrierRecovery.py`, `models/channels.py`
- **komm**（通信库）：One-class-per-file + ABC，每个算法一个类
- **scipy.signal**：按处理层分模块，公共包装器委托私有实现

**7 个组织模式**：

1. **域层扁平模块**（推荐，OptiCommPy 风格）：按处理层分模块，每个模块一个文件。最简单的心理模型。

2. **One-class-per-file + ABC**（komm 风格）：每个算法一个类继承 ABC。最大扩展性，但对 770 行项目过重。

3. **调度器 + 算法表**：单个调度函数按名称选择算法。实验脚本保持简洁。

4. **Frozen dataclass 配置**：系统参数和实验参数分离为 frozen dataclass。IDE 友好，防意外修改。

5. **全局 RNG 状态管理**：模块级 RNG 实例，可注入替换。解决当前 np.random 全局状态依赖。

6. **数值代码测试策略**：
   - 确定性种子 + 黄金文件
   - Property-based testing（Hypothesis）：roundtrip（mod→demod→mod = identity），单调性，退化情况
   - 参考比较：简化情况对比已知结果

7. **管线即数据**：实验编排函数将仿真视为数据流过各阶段。库提供构建块，用户组装。

**推荐模块划分**（与 A2 审计一致，OptiCommPy 模式）：

```
config.py (~60行) — Frozen dataclass: SystemConfig, ScenarioConfig, RecoveryConfig
channel.py (~80行) — gg_block, doppler_phase, generate_shared_realization
modulation.py (~100行) — QPSK/16-QAM 调制解调, hard_decision, BER 计数
recovery.py (~250行) — FFT-FOE, DPLL, VV, BPS, KF 全部载波恢复算法
equalizer.py (~60行) — MMSE 均衡, amp_limit, equalize_oracle/hmed
metrics.py (~30行) — ber_eval, db_ratio
experiment.py (~120行) — run_*, run_trial_shared, save_results
pipeline.py (~60行) — 轻量注册表 + 配置驱动管线（B6 的新增）
__init__.py (~15行) — 向后兼容重导出
```

### B2: 可复现研究文档系统

**5 个文档模式**：

1. **Diataxis 内容分类**：每份文档分为 Reference/How-to/Explanation/Tutorial 四类。映射到三层分档：Reference→锚点层, Explanation→积累层, How-to→快照层。

2. **ROT 审计**（Redundant/Outdated/Trivial）：定期扫描文档，标记冗余（同一信息在2+文件）、过时（已被取代）、琐碎（无决策/结论/交接价值）。每 5-10 个会话执行一次。

3. **单一真相源 + 所有权分配**：每个文件定义最大范围和拥有者。超出范围则拆分或修剪。CLAUDE.md 的文档职责表已部分实现，需加强执行。

4. **活文档 + 自动化一致性检查**：
   - 断链检测（grep `[link](path)` 验证目标存在）
   - 参数一致性检查（锚点层提取数值，扫描积累层矛盾）
   - 过时检测（N 个会话未修改的文件标黄）
   - 大小门控（超过层级限制时警告）

5. **成熟度标签**（Digital Garden 模式）：DRAFT / ACTIVE / FROZEN / ARCHIVED。恢复路径只读 ACTIVE，可降低 60-70% 恢复成本。

**三层分档详细设计**：

| 层级 | 更新策略 | 大小限制 | 自动化检查 |
|------|---------|---------|-----------|
| 锚点层 | 仅通过 D### 决策变更，绝不追加 | 500 行硬限制 | 参数提取脚本检测多文件定义 |
| 积累层 | 只追加，超限归档最旧条目 | 1000 行软限制 | 文件大小监控 + 交叉引用验证 |
| 快照层 | 刷新式重写，旧快照标 FROZEN | 300 行硬限制 | 引用解析到锚点/积累层文件 |

**不建议采用的**：完整 docs-as-code CI/CD 流水线（过重）、LLM 文档同步（引入不确定性）、正式内容管理系统（解决发布问题而非我们的问题）。

### B3: 参数溯源追踪最佳实践

**关键发现：无现成工具解决"每个参数有文献来源"的问题。** 科学仿真项目中普遍手工完成，无自动化验证。

**推荐技术栈**：

| 层级 | 工具 | 用途 |
|------|------|------|
| 参数定义 | Pydantic BaseModel + Field(json_schema_extra={...}) | 单一真相源，替换裸 Python 常量 |
| 来源元数据 | Field(description=..., json_schema_extra={"source": "doi:...", "equation": "..."}) | 每个参数携带来源 |
| 死参数检测 | 自定义 AST 遍历 lint | 比较模型字段与实际使用 |
| SPEC 一致性 | 从 Pydantic model 自动生成 SPEC.md 表格 | 不可能出现 SPEC/代码不一致 |
| 变更日志 | Git + model 中的 changelog 字段 | 参数变更留痕 |

**具体设计（params.py 骨架）**：

```python
class SourceType(str, Enum):
    literature = "literature"   # 引用论文+页码/公式
    derived = "derived"         # 推导链有文档
    typical = "typical"         # 社区标准默认值
    measured = "measured"       # 实验数据
    assumption = "assumption"   # 未验证，需论证

class QMatrixParams(BaseModel):
    sigma2_turb: float = Field(
        ...,
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE — empirical tuning parameter",
            "audit_flag": "CRITICAL: no literature basis",
        },
    )
    kappa: float = Field(
        ...,
        json_schema_extra={
            "audit_flag": "DEAD: defined but never used in code",
        },
    )
```

**自动检测机制**：

1. **死参数检测**：AST 遍历比较 Pydantic 模型字段名 vs 代码中实际引用 → 发现 kappa
2. **未记录覆盖检测**：比较 SPEC 值 vs 代码常量 → 发现 Q_fine_df
3. **来源审计报告**：`model.audit_provenance()` → 分类 complete/partial/missing/dead
4. **SPEC 自动生成**：从模型生成 markdown 表格 → 消除 SPEC/代码漂移

### B4: 验证/测试框架

**已创建的测试文件**：
- `tests/test_common.py`：69 个测试，8 个层级（T1-T8）
- `tests/red_flags.py`：9 个红旗规则（RF-01 到 RF-09）
- `tests/VERIFICATION.md`：4 个验证检查点（CP-1 到 CP-4）

**测试层级设计**：

| 层级 | 类名 | 测试数 | 捕获什么 |
|------|------|--------|---------|
| T1 | TestT1SignalPrimitives | 11 | 调制/解调 roundtrip bug，功率归一化，星座错误 |
| T2 | TestT2CarrierRecovery | 8 | FFT-FOE 精度，VV/DPLL/BPS 跟踪失败，管线完整性 |
| T3 | TestT3KalmanFilter | 7 | Q 矩阵合理性，P 对称/正定，收敛性，跨块 P 传播 |
| T4 | TestT4ChannelFairness | 8 | 确定性种子，信号模型 SNR 验证，h>0，导频插入正确性 |
| T5 | TestT5PhysicalInvariants | 9 | BER 范围，NaN/Inf，SNR 单调性，强湍流>弱湍流 |
| T6 | TestT6RegressionGuard | 5 | 防止 VV 公式 bug 复现，DPLL>VV(强湍流)，optimal vs default |
| T7 | TestT7ParameterConsistency | 13 | SPEC.md 参数锁定到文档值 |
| T8 | TestT8NumericalStability | 7 | 极端 SNR（-5dB~40dB），短信号，零输入不崩溃 |

**红旗规则**：

| 规则 | 严重性 | 检测什么 |
|------|--------|---------|
| RF-01 | CRITICAL | BER 超出 [0,1] |
| RF-02 | CRITICAL | BER≈0.5 在高 SNR（载波恢复完全失败） |
| RF-03 | WARNING | BER>10% 在 20+ dB SNR |
| RF-04 | WARNING | BER 远离 SPEC.md 已知范围 |
| RF-05 | CRITICAL | dB 增益>20（基线有 bug，如旧 VV 公式） |
| RF-06 | CRITICAL | h≤0 |
| RF-07 | CRITICAL | NaN/Inf |
| RF-08 | WARNING | 跨种子零方差（种子未传播） |
| RF-09 | INFO | 缺少 channel_seed（公平性未验证） |

**验证检查点**（管线中的强制检查位置）：
- CP-1：信道生成后（h>0, SNR 正确, 种子确定性）
- CP-2：载波恢复后（BER 合理范围, NaN/Inf 检查）
- CP-3：实验循环内（多种子方差>0, 增益合理）
- CP-4：结果保存前（红旗规则全通过）

### B5: 仿真与理论对比验证方法

**分层验证协议**（按依赖顺序）：

```
步骤1: AWGN-QPSK BER（最基础验证）
  失败 → 停止，修复调制/解调/噪声生成
  通过 ↓
步骤2: Gamma-Gamma 信道（矩 + KS 检验）
  失败 → 停止，修复信道生成 (gg_block)
  通过 ↓
步骤3: AWGN+衰落 BER（无载波恢复）
  失败 → 检查噪声缩放、功率归一化
  通过 ↓
步骤4: VV 相位方差（仅 AWGN）
  失败 → 检查 VV 实现
  通过 ↓
步骤5: DPLL 相位方差（仅 AWGN）
  失败 → 检查 DPLL 环路滤波器系数
  通过 ↓
步骤6: 完整系统验证（VV/DPLL + 衰落 + 多普勒）
  失败 → 组件级调试
```

**容差设置**：

| 指标 | 正常容差 | 宽松容差 | 何时用宽松 |
|------|---------|---------|-----------|
| BER (10⁻²~10⁻³) | <20% 相对误差 | 2倍因子 | — |
| BER (10⁻⁴~10⁻⁵) | <50% | 10倍因子 | 每点错误数<30 |
| BER (<10⁻⁵) | 10倍因子 | 100倍因子 | 每点<10错误 |
| 相位方差 | 0.5~2.0倍比值 | 0.3~3.0倍 | 非线性区域 |
| NMSE | <20% | <50% | 极低 SNR 或强湍流 |
| 信道矩 | <1%(均值), <2%(方差) | <5% | N<100,000 |
| 分布 KS 检验 | p>0.05 | p>0.01 | 样本<5,000 |

**样本量指南**：每个 SNR 点至少 100 个错误。BER=10⁻⁵ → N=10⁷ bits。GG 信道矩用 10⁶ 样本。VV/DPLL 相位方差用 50,000 符号 × 200 种子。

**仿真与理论不符时的调试流程**：
1. 隔离故障组件（噪声功率、信号功率、理论公式 SNR 定义、样本量）
2. 最小复现：h=1.0, φ=0, 无多普勒, 无激光噪声 → 定位 bug 层级
3. 常见根因（按频率排序）：噪声方差缩放错误 > 归一化不匹配 > 块级 vs 符号级 h > 星座旋转/相位模糊 > SNR 定义差异

**发表证据标准**（IEEE TCOM/JLT/TWC）：
- BER 曲线：4-6 个 SNR 点叠加仿真与解析
- 分布验证：2-3 种湍流条件的直方图 vs PDF
- 相位跟踪：稳态相位方差表格
- 最基本要求：AWGN BER 完美匹配 + 衰落 BER 趋势正确

### B6: 可扩展 DSP 管线架构

**参考框架**：
- **GNU Radio**：流图模型，块继承 gr::block，DAG 调度器。功能强大但对离线仿真过重。
- **MATLAB Comm Toolbox**：System Objects，step() 方法。简单但无注册表或配置驱动组合。
- **OpenMMLab mmengine**：装饰器注册表 + 配置驱动。最适合研究代码库规模。

**三个架构选项**：

| 选项 | 描述 | 新增代码 | 适合度 |
|------|------|---------|--------|
| A: 轻量注册表 + 函数包装 | 注册名→函数映射，管线从配置列表构建 | ~170 行 | **推荐** |
| B: ABC + 插件发现 | ProcessingBlock ABC，importlib 自动发现 | ~300 行 | 偏重 |
| C: 数据流图 | GNU Radio 风格 DAG | 500+ 行 | 过度工程 |

**推荐方案 A 实现设计**：

核心基础设施（~60 行）：
```python
_BLOCKS: dict[str, Callable] = {}

def register_block(name: str):
    """装饰器：注册处理块"""
    def decorator(fn):
        _BLOCKS[name] = fn
        return fn
    return decorator

def run_pipeline(steps: list[dict], shared: dict) -> dict:
    """执行配置驱动的处理管线"""
    for step in steps:
        block_fn = get_block(step['block'])
        shared['signal'] = block_fn(shared, **step.get('params', {}))
    return shared
```

管线定义（配置驱动）：
```python
register_pipeline('fixed_vv', [
    {'block': 'equalize_oracle'},
    {'block': 'foe_fft',  'params': {'N_fft': 1024}},
    {'block': 'dpll',     'params': {'omega_n': 8e6}},
    {'block': 'vv',       'params': {'Nw': 64}},
])
```

**添加新算法的流程**（以 ANN 载波恢复为例）：
1. 新建 `blocks/ann_cpr.py`（1 个文件）
2. 用 `@register_block('ann_cpr')` 装饰器注册
3. 在管线配置中引用 `{'block': 'ann_cpr', 'params': {...}}`
4. **零改动现有代码**

**有状态块处理**（KF Pilot）：通过 shared dict 约定传递额外上下文（data_idx, h_est 等）。

---

## 跨 Agent 综合分析

### 审计发现 → 设计原则 覆盖验证

| 设计原则 | A1-A6 审计证据 | B1-B6 实践支撑 |
|---------|---------------|---------------|
| P1: 参数必须有来源 | A1: 37%参数缺来源，kappa死参数，Q_fine_df未记录覆盖 | B3: Pydantic溯源模型 + 自动SPEC生成 |
| P2: 决策必须有背景 | A3: 附录G过时，编号错误 | B2: 成熟度标签 + ROT审计 |
| P3: 验证必须强制 | A6: 13个结果文件无元数据，A2: 无任何测试 | B4: 69个pytest测试 + 9条红旗规则 |
| P4: 信息必须跨对话连续 | A4: 9个已归档仍标active，3个未注册 | B2: 恢复路径只读ACTIVE |
| P5: 红旗信号必须自动触发 | A1: sigma2_turb零来源但控制所有KF结论 | B4: RF-01~RF-09 自动检测 |
| P6: 恢复成本必须可控 | A4: thesis-direction-pivot 108文件/2.4万行, A5: 5096行公式7文件 | B2: 三层分档+大小限制 |

### 最紧急的 5 项行动

1. **补全 sigma2_turb 来源**（P1/CRITICAL）：无来源但控制所有 KF 结论。需推导或引用。
2. **记录 Q_fine_df 覆盖行为**（P1/HIGH）：代码覆盖了 SPEC 中的 design_Q() 输出但未记录原因。
3. **提交 common.py 129 行未提交更改**（A6）：纯添加性，提交确保可追溯。
4. **清理 _registry.yaml**（A4/P0）：9 个专题状态修正，5 分钟完成。
5. **运行 pytest 测试**（B4）：验证当前代码基线，8 秒完成。

### 待 Batch 3 解决的设计问题

| 问题 | 来源 | Batch 3 负责 Agent |
|------|------|-------------------|
| 代码模块具体拆分方案 | A2 + B1 | C1 |
| 参数溯源系统具体实现 | A1 + B3 | C2 |
| 验证检查点集成方案 | A6 + B4 + B5 | C3 |
| 文档架构最终设计 | A3+A4+A5 + B2 | C4 |
| 从现状到目标的迁移路径 | 全部 | C5 |
| Handoff/会话管理改进 | A4 + B2 | C6 |

---

---

## Phase 9: Batch 3 — 方案设计（C1-C6）

### C1: 代码模块结构方案

**输出文件**：`projects/simulation/DESIGN-modular-split.md`（692行）

**核心决策**：
- common.py 拆为7个 `_` 前缀域模块 + `__init__.py` 垫片
- **跳过 @register_block**：25个脚本无一需要注册模式，未来需要时再加
- `_` 前缀约定：子模块为内部模块，公共API仅通过 `from common import *` 获取
- OUT 路径用双 `os.path.dirname` 保持语义（指向 `simulation/` 而非 `simulation/common/`）
- 附录A审计全部27个脚本，确认25个导入common的脚本100%名称覆盖

**模块划分**：8个文件（`__init__.py` + 7模块），~1020行（从769行拆分，含垫片和文档字符串）

### C2: 参数溯源系统方案

**输出文件**：`projects/simulation/params_design.md`（1271行）

**核心决策**：
- 8个 Pydantic BaseModel（frozen=True）+ 1个 SimulationConfig 聚合模型
- 每个参数附带 source_type/source/audit_flag/equation/derived_from
- sigma2_turb 两条推导路径：Rytov理论相位结构函数 / Gamma-Gamma闪烁指数反推
- kappa 确认为 DEAD 参数（项目级 grep 验证），标记 deprecated
- SPEC.md 参数表由 `generate_spec_md()` 自动生成，永不手动编辑
- `audit_params()` 函数：分类 OK/WARNING/CRITICAL/DEAD，检测未记录覆盖

**审计结果**：8 OK / 23 WARNING / 4 CRITICAL / 3 DEAD

### C3: 验证/检查点系统方案

**输出文件**：`projects/simulation/tests/INTEGRATION_PLAN.md`（791行）

**核心决策**：
- `SIM_CHECKPOINTS` 环境变量控制检查点启用/禁用
- common.py 仅需新增3行（检查点调用），其余在独立模块中
- 69个已有测试全部通过（已验证，9.69秒）
- 发现并修复了 red_flags.py 的导入路径 bug
- 发现 save_results 双模式问题（多数实验有自己的本地版本，无元数据）
- `checkpoints.py` 独立模块，不侵入业务代码

### C4: 文档架构方案

**输出文件**：`.sessions/2026-06-12-simulation-foundation-rebuild/C4-documentation-architecture.md`（567行）

**核心决策**：
- 三层分档：毕设/下14文件分为锚点(5)/积累(6)/快照(3)
- 成熟度标签 `<!-- maturity: X -->` 降低恢复成本60-70%
- 去冗余：公式文档7文件/5096行 → 3文件/~3350行
- 注册表清理：修正9个状态错误、补注册3个未注册目录
- 零外部工具依赖——纯文件系统约定+git+CLAUDE.md规则
- 6个迁移阶段，46个清单项，~90分钟

### C5: 综合迁移方案

**输出文件**：`.sessions/2026-06-12-simulation-foundation-rebuild/C5-migration-plan.md`（695行）

**核心决策**：
- 8阶段迁移：Phase 0(安全网) → Phase 1(Quick Wins) → Phase 2(验证基础设施) → Phase 3(参数溯源) → Phase 4(代码模块化) → Phase 5(分层验证) → Phase 6(文档清理) → Phase 7(Handoff改进) → Phase 8(最终验证)
- 依赖顺序：C3验证基础 → C2参数溯源 → C1模块化（C4文档和C6 handoff独立于代码）
- 5个Quick Wins可在10分钟内完成
- 总时间~3小时，可分2-3个对话执行
- 每阶段有验证命令和回滚策略

### C6: Handoff/会话管理改进方案

**输出文件**：`.sessions/2026-06-12-simulation-foundation-rebuild/C6-handoff-session-management.md`（626行）

**核心决策**：
- Handoff 新增"约定变更"段落（强制）——直接解决最高频丢失类型
- topic-index 双区设计：不变量区(~50行)+工作区——恢复阅读量从553行降至~50行
- 自动状态漂移检测在 session-governance 中实现
- 200行 handoff 大小指导
- 大型专题(>50文件)拆分标准及操作流程

---

## Phase 10: Batch 3 执行过程

### 10.1 调度策略

Batch 3 按并发限制分两批派发：
- **第一批**（C1-C3）：代码模块结构、参数溯源、验证检查点
- **第二批**（C4-C6）：文档架构、迁移方案、Handoff改进

C5 需要综合 C1-C4/C6 的输出，因此安排在第二批最后执行。

### 10.2 执行时间线

| 时间 | 事件 | 结果 |
|------|------|------|
| T+0 | 派发 C1, C2, C3 | 全部成功 |
| T+5min | C1 完成 | DESIGN-modular-split.md (692行) |
| T+5min | C2 完成 | params_design.md (1271行) |
| T+7min | C3 完成 | tests/INTEGRATION_PLAN.md (791行) |
| T+7min | 派发 C4, C5, C6 | — |
| T+11min | C5 因 API 529 过载失败 | 0 token 消耗 |
| T+12min | C4 因 API 529 过载失败 | — |
| T+12min | C6 完成 | C6-handoff-session-management.md (626行) |
| T+12min | 重试 C4, C5 | — |
| T+17min | C5 第二次 API 529 过载 | — |
| T+18min | C4 完成 | C4-documentation-architecture.md (567行) |
| T+18min | 第三次重试 C5 | — |
| T+22min | C5 完成 | C5-migration-plan.md (695行) |

**教训**：API 过载在高并发场景下概率显著增加。3个agent同时启动时过载概率约33%（2/6次失败），应考虑错峰派发或降低并发数。

### 10.3 各方案产出摘要

| Agent | 输出文件 | 行数 | 核心设计 |
|-------|---------|------|---------|
| C1 | `projects/simulation/DESIGN-modular-split.md` | 692 | 7个`_`前缀域模块 + `__init__.py`垫片，跳过@register_block，25脚本100%兼容，附录A审计全部27脚本导入名称 |
| C2 | `projects/simulation/params_design.md` | 1271 | 8个Pydantic BaseModel(frozen=True) + SimulationConfig聚合，4 CRITICAL(sigma2_turb×3,Q_fine_df)，3 DEAD(kappa×3)，SPEC自动生成 |
| C3 | `projects/simulation/tests/INTEGRATION_PLAN.md` | 791 | SIM_CHECKPOINTS环境变量门控，common.py仅增3行，69测试已验证通过(9.69s)，发现save_results双模式问题 |
| C4 | `.sessions/.../C4-documentation-architecture.md` | 567 | 三层分档(锚点5/积累6/快照3)，成熟度标签`<!-- maturity: X -->`，去冗余7→3文件，6阶段46清单项 |
| C5 | `.sessions/.../C5-migration-plan.md` | 695 | 8阶段迁移(Phase0安全网→Phase7最终验证)，~3小时/2-3对话，5个Quick Wins(<10分钟)，每阶段验证命令+回滚策略 |
| C6 | `.sessions/.../C6-handoff-session-management.md` | 626 | Handoff新增"约定变更"段落，topic-index双区设计(恢复553行→50行)，200行handoff大小指导，>50文件拆分标准 |

---

## Phase 11: 架构审查

用户要求派子 agent 审阅全部6个方案并评估扩展性。使用 `oh-my-claudecode:architect` agent 执行。

### 11.1 审查方法

审查 agent 独立读取了全部6份设计文档 + common.py 源代码 + 验证了 Pydantic 版本(2.10.6)。评估维度：
- A. 方案质量（完整性/一致性/可行性/简洁性）
- B. 扩展性评估（6个子维度）
- C. 潜在问题
- D. 3个具体扩展场景验证

### 11.2 各方案质量评分

| 方案 | 评分 | 主要优点 | 主要问题 |
|------|------|---------|---------|
| C1 模块化 | **A-** | 38函数全覆盖审计，25/25脚本导入覆盖，依赖DAG无循环 | `_config.py`与`params.py`双重真相源冲突；`gg_block`默认参数`bs=BLOCK`创建导入时耦合 |
| C2 参数溯源 | **B+** | 38参数逐个审计分类，sigma2_turb CRITICAL标记有理，SPEC自动生成 | 与C1的`_config.py`角色重叠；Pydantic v1语法（已修复）；四层链 params→common→_config→__init__ |
| C3 验证集成 | **A-** | 环境变量门控设计精良，分层B5协议是物理验证非单元测试，正确识别双保存模式 | 引用重构前结构（已修复）；red_flags导入用sys.path操作而非conftest.py |
| C4 文档架构 | **A** | 三层分类优雅可执行，ROT审计具体有时限，成熟度标签低调巧妙 | formulas-master 2260行接近2500上限；"每10会话"审计与"不消耗心力"有张力 |
| C5 迁移方案 | **A** | 8阶段每阶段有验证/回滚，依赖图可视化验证排序，3小时+对话分解现实 | C2/C1中间态链路脆弱；C3检查点阶段在C1模块化之后导致行引用不匹配 |
| C6 Handoff | **B+** | "约定变更"直接解决最高频丢失，topic-index活跃区50行上限实用，三层状态漂移防御 | 成熟度标签无自动强制执行（手动标记可能再次漂移）；"3会话未激活→dormant"需要跟踪机制 |

### 11.3 跨方案一致性检查

#### 矛盾1：双重单一真相源（严重性：高，**已修复**）

- C2 S5.1：`params.py` 作为新的唯一真相源
- C1 S1.2：`_config.py` — 参数唯一真相源
- C5 S5.2 选择A：`_config.py` 从 `params.py` 导入，解决冲突
- **修复**：重写 C1 `_config.py` 段落，明确声明从 `params.py` 导入，移除重复 dataclass 定义

#### 矛盾2：C3 引用重构前结构（严重性：中，**已修复**）

- C3 插入点 `common.py:765` → 模块化后为 `common/_experiment.py` 的 `save_results()`
- **修复**：两处 `common.py:765` 引用更新为模块化后路径

#### 矛盾3：Pydantic v1/v2 语法（严重性：低，**已修复**）

- C2 全部10处 `class Config: frozen = True`（v1语法）
- 实际安装 Pydantic 2.10.6
- **修复**：替换为 `model_config = ConfigDict(frozen=True)`

#### 差距1：EKF扩展需要部分重构（严重性：中，记录但未修复）

- `kf_unified` 硬编码 2 状态线性模型 `F = [[1,T_S],[0,1]]`
- EKF 需要可插拔的 F/H/Jacobian
- C1 声称 EKF 零改动，实际需~30行重构 `_kf.py`
- **处理**：记录为已知限制，执行时再处理

#### 差距2：时间相关信道扩展需接口改造（严重性：中，记录但未修复）

- `gg_block(N, a, b, bs)` 返回扁平数组，无时间结构
- AR(1)模型需顺序生成、跨块状态记忆
- **处理**：通过新增函数 `gg_block_ar1` 解决，不改现有接口

### 11.4 扩展性评估（审查 agent 结论）

| 维度 | 评级 | 关键证据 |
|------|------|---------|
| 新参数 | **优秀** | Pydantic + 自动SPEC + audit_params()，新增参数近乎零成本 |
| 新实验 | **优秀** | `from common import *` 保持，新脚本完全独立 |
| 新验证 | **良好** | 检查点通用(CP-1~CP-4适用任意信道/恢复组合)，但新算法需加验证层 |
| 文档 | **良好** | 三层分档+大小限制有效，但 formulas-master 2260行接近上限 |
| 新算法(EKF) | **部分支持** | 需~30行重构 `_kf.py`（提取共享迭代循环），非零改动但可控 |
| 新信道模型 | **部分支持** | `_channel.py` 自包含可新增函数，但 `generate_shared_realization` 需扩展接口 |

### 11.5 三个扩展场景验证结果

**场景1：时间相关GG信道（E1方向）**
- ~190行新增，0行改现有代码
- 需：`_channel.py` 新函数 + `TurbulenceTemporalParams` + 时间统计测试 + CP-1扩展
- `generate_shared_realization` 需加 `channel_type` 参数（选项a，向后兼容）
- **评定：自然支持**

**场景2：扩展卡尔曼滤波（EKF）**
- ~300行新增，~30行改 `_kf.py`（重构共享逻辑）
- 需：新文件 `_ekf.py` + 3个恢复运行器 + `EKFParams` + EKF专用测试
- `kf_unified` 的内联 F/H 矩阵需提取为可插拔参数
- **评定：可控但非零改动**

**场景3：突发感知KF（A1方向）**
- ~335行新增，0行改现有核心代码
- 不需新信道模型——检测现有GG信道中的深衰落
- `kf_burst_adaptive_recovery` 调用现有 `kf_unified` 并动态调整 Q
- **评定：最易扩展的路径**

### 11.6 审查 agent 问题清单

| 级别 | 问题 | 状态 |
|------|------|------|
| P0 | `_config.py` vs `params.py` 真相源冲突 | **已修复** |
| P1 | C3 行引用基于重构前结构 | **已修复** |
| P1 | Pydantic v1 语法不匹配 v2.10.6 | **已修复** |
| P1 | EKF 扩展需~30行重构 `_kf.py` | 记录为已知限制 |
| P2 | `gg_block` 默认参数 `bs=BLOCK` 导入时耦合 | 记录，暂不处理 |
| P2 | `params.py` 的"兼容方法"模式随参数增长有维护负担 | 记录，当前3个方法可控 |
| P2 | C4 ROT 审计"每10会话"可能消耗心力 | 实际测试后调整频率 |

---

## Phase 12: 方案冻结

### 12.1 冻结决策

经过 18 agent 分析（A1-A6 审计 + B1-B6 最佳实践 + C1-C6 方案设计）+ 独立架构审查 + 3个问题修复，用户确认方案可以冻结。

### 12.2 冻结后的方案清单

| 产出 | 文件 | 行数 | 状态 |
|------|------|------|------|
| 代码模块化方案 | `projects/simulation/DESIGN-modular-split.md` | 692 | 已修复P0，冻结 |
| 参数溯源方案 | `projects/simulation/params_design.md` | 1271 | 已修复P1(v2语法)，冻结 |
| 验证集成方案 | `projects/simulation/tests/INTEGRATION_PLAN.md` | 791 | 已修复P1(行引用)，冻结 |
| 文档架构方案 | `.sessions/.../C4-documentation-architecture.md` | 567 | 冻结 |
| 综合迁移方案 | `.sessions/.../C5-migration-plan.md` | 695 | 冻结 |
| Handoff改进方案 | `.sessions/.../C6-handoff-session-management.md` | 626 | 冻结 |

### 12.3 已知限制（冻结但不阻塞）

1. EKF 扩展需~30行重构 `_kf.py`（非零改动）
2. `gg_block` 默认参数 `bs=BLOCK` 创建导入时耦合
3. `formulas-master.md` 2260行接近2500上限
4. 成熟度标签无自动强制执行（手动标记）
5. C4 ROT审计频率需实际测试后调整

---

## 决策引用

- D-003（隐含）：方案冻结——C1-C6全部冻结，3个P0/P1问题已修复，5个已知限制记录但不阻塞
- D-C2-01（C2 方案中）：Q_fine_df 覆盖行为保留但在 SPEC 中明确记录

## 范围确认

- 本轮在 scope boundary 内：是（18 agent 深度分析 + 架构审查 + 方案冻结）
- 范围超出：未超出

## 后续

1. 执行 C5 迁移方案 Quick Wins：提交 common.py 129行、清理 _registry.yaml、运行 pytest
2. 按阶段执行迁移：验证基础 → 参数溯源 → 代码模块化 → 文档清理 → Handoff改进
3. 预计2-3个对话完成迁移
