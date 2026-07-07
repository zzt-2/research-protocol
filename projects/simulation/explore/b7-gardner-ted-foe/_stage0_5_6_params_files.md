# B7 阶段 0.5 参数真相源 + 0.6 文件组织

> 阶段 0.5 + 0.6 | 专题 `2026-07-08-b7-gardner-ted-foe` | 日期 2026-07-08
> 依据：TL-26（参数溯源）+ FR-26/V6（读原文数值，不只引位置）+ INVARIANT 6（阶段 0 不写代码，参数草稿在 explore）+ D-007 教训（参数改后必须同步清理下游引用）+ 用户决策（B7 锚论文原参数 25GBaud/1.8kHz）
> 结论：**B7Params 修正版草稿（7 字段，全标 source_type+source+audit_flag，数值读自 `content.md` 行号）+ explore 目录结构落盘 + 下游引用同步清单**

## 0. 核查触发

H003 阶段 0.5 + 0.6 要求：
- 0.5：B7 参数进 params.py 单字段（草拟在 explore，不直接写 params.py）+ 读 B7 content.md 具体数值（FR-26 V6）+ 符号率/线宽场景差异决策（用户已拍板：B7 锚论文原参数）
- 0.6：确认 explore 目录结构 + 后续 sandbox/MVE 文件命名 + 下游引用同步清单（D-007 教训 2）

## 1. 阶段 0.5 参数真相源

### 1.1 现有 B7Params（params.py L606-680）的问题（V6 核查发现）

| 字段 | 现值 | 问题 | B7 原文真值（content.md 行号）|
|---|---|---|---|
| `DOPPLER_RANGE` | 23e9 | source 没引行号，note 说"fiber 场景"误导（实际是实验室模拟 Doppler，星地迁移动机）| 23e9（L49「scan range is set to 0 GHz–23 GHz」），正确 |
| `LEO_DOPPLER_RATE` | **30e3**（30kHz/s）| **错**—— Paillier/sat.1553 的值，B7 原文给了不同值 | **±100MHz @ 1GHz/s**（L47「periodic frequency excursion of ±100 MHz at a variation rate of 1 GHz/s」）|
| `OSNR_WORKING_POINT` | 10.0 | source 没引行号 | 10dB（L21/69），正确 |
| `GARDNER_SPS` | 2 | source 没引行号 | 2（隐含在 L47「downsampled to 2 sps before entering the FOE algorithms」）|
| `GARDNER_GAIN` | 0.01 | typical 非 literature | 正确（MVE 阶段环路增益典型值）|
| `PSA_PILOT_SPACING` | 32 | **概念错遗留**——PSA FOE 是谱不对称法不用 pilot | 删除（PSA FOE baseline 重写为谱不对称法，0.4 已决策）|
| **缺**：符号率 | — | 没字段 | **25GBaud**（L21/25/47「25-Gbaud DP-QPSK」）|
| **缺**：线宽 | — | 没字段 | **1.8kHz**（L47「Lorentzian linewidth of 1.8 kHz」）|
| **缺**：roll-off | — | 没字段 | **0.1**（L47「roll-off factor is set to 0.1」）|
| **缺**：接收 BW | — | 没字段 | **36.75GHz**（L47/49「receiver bandwidth of 36.75 GHz」）|
| **缺**：采样率 | — | 没字段 | **2.94 sps**（L47/49「sampling rate of 2.94 sps」）|

### 1.2 B7Params 修正版草稿（sandbox 阶段回写 params.py，本轮只在 explore 草拟）

```python
class B7Params(BaseModel):
    """B7 Gardner TED FOE 参数族 (B7 OFC 2026, ofc.2026.w2a.62)

    场景参数跟 NDA-ML (SystemParams) 不统一——B7 锚论文工作点在 25GBaud/1.8kHz，
    0.6dB 增量在此场景实测。复现 B7 锚方法必须用 B7 场景参数。
    跨候选可比性通过 fair gain 维度统一（都报 HD-FEC），不通过场景参数统一。
    用户决策：2026-07-08 对话 4，B7 用锚论文原参数。"""

    # === 锚论文场景参数（content.md 行号溯源，FR-26 V6）===
    R_SYM_B7: float = Field(
        25e9,
        description="符号率 25 GBaud（B7 锚论文场景，跟 NDA-ML 2.5GBaud 不统一）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L25/L47「25-Gbaud DP-QPSK」",
            "symbol": "R_SYM_B7",
            "unit": "sym/s",
            "audit_flag": AuditFlag.OK,
            "note": "用户决策（2026-07-08）：B7 用锚论文原参数，不跟 NDA-ML 统一。复现 B7 0.6dB 增量必须用 25GBaud",
        },
    )
    LASER_LW_B7: float = Field(
        1800.0,
        description="激光线宽 1.8 kHz（NL-FT-DFB 激光器 Lorentzian 线宽，B7 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「Lorentzian linewidth of 1.8 kHz」",
            "symbol": "Δν_B7",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "跟 NDA-ML LASER_LW=10kHz 不统一（B7 锚论文场景）",
        },
    )
    ROLL_OFF: float = Field(
        0.1,
        description="RRC 成型 roll-off 0.1",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「roll-off factor is set to 0.1」",
            "symbol": "α_RRC",
            "audit_flag": AuditFlag.OK,
        },
    )
    RX_BW_GHZ: float = Field(
        36.75e9,
        description="接收电带宽 36.75 GHz",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47/L49「receiver bandwidth of 36.75 GHz」",
            "symbol": "BW_RX",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    SPS_RX: float = Field(
        2.94,
        description="接收采样率 2.94 sps（FOE 前降采样到 2 sps）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47/L49「sampling rate of 2.94 sps, downsampled to 2 sps before entering the FOE algorithms」",
            "symbol": "sps",
            "unit": "sample/sym",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === Doppler 扫频参数 ===
    DOPPLER_RANGE: float = Field(
        23e9,
        description="Doppler 频偏扫描范围上限（0-23 GHz）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「scan range is set to 0 GHz–23 GHz and the interval is 1 GHz」",
            "symbol": "Δf_max",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    DOPPLER_INTERVAL: float = Field(
        1e9,
        description="Doppler 扫频间隔 1 GHz",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「interval is 1 GHz」",
            "symbol": "Δf_step",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    LEO_DOPPLER_EXCURSION: float = Field(
        100e6,
        description="LEO Doppler 频偏幅度 ±100 MHz（三角波模拟参数）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「periodic frequency excursion of ±100 MHz at a variation rate of 1 GHz/s」",
            "symbol": "Δf_LEO",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "原 LEO_DOPPLER_RATE=30e3 错误，B7 原文给的是 ±100MHz@1GHz/s",
        },
    )
    LEO_DOPPLER_RATE: float = Field(
        1e9,
        description="LEO Doppler 变化率 1 GHz/s（三角波斜率）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「variation rate of 1 GHz/s」",
            "symbol": "ḟ_LEO",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === 工作点参数 ===
    OSNR_WORKING_POINT_LOW: float = Field(
        10.0,
        description="OSNR 低 SNR 极限工作点 10 dB（B7 可解调，PSA FOE 失败）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L69「OSNR of 10 dB, which is where conventional algorithms fail」",
            "symbol": "OSNR_low",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )
    OSNR_WORKING_POINT_MAIN: float = Field(
        17.0,
        description="OSNR 主测点 17 dB（poster Fig.3a 主测条件）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「under an OSNR of 17 dB」",
            "symbol": "OSNR_main",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === Gardner TED 参数 ===
    GARDNER_SPS: int = Field(
        2,
        description="Gardner TED 每符号采样数（FOE 前降采样后）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「downsampled to 2 sps before entering the FOE algorithms」+ Gardner 1986 经典配置",
            "symbol": "SPS",
            "audit_flag": AuditFlag.OK,
        },
    )
    GARDNER_GAIN: float = Field(
        0.01,
        description="Gardner TED 环路增益（典型值，MVE 阶段近似）",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "Gardner TED loop gain 典型值（B7 锚论文未明确给精确值）",
            "symbol": "K_p",
            "audit_flag": AuditFlag.WARNING,
            "note": "典型值而非文献精确值，MVE 阶段近似",
        },
    )

    # === FEC 阈值（跨候选可比，跟 NDA-ML 对齐）===
    HD_FEC_THRESHOLD: float = Field(
        3.8e-3,
        description="7% HD-FEC BER 阈值（跨候选主判据，跟 NDA-ML 对齐）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 181/191（跟 NDA-ML 共用 FEC 阈值定义）+ B7 content.md 用 BER 2e-2（本字段是跨候选主判据补充）",
            "symbol": "BER_HD-FEC",
            "audit_flag": AuditFlag.OK,
            "note": "B7 锚论文用 BER 2e-2，本字段为跨候选可比补充（0.4 双工作点决策）",
        },
    )
    BER_SENSITIVITY_THRESHOLD: float = Field(
        2e-2,
        description="BER 2e-2 锚论文一致性校验工作点（receiver sensitivity）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L65/L69「receiver sensitivity by 0.6 dB at a BER of 2×10⁻²」",
            "symbol": "BER_sens",
            "audit_flag": AuditFlag.OK,
            "note": "锚论文一致性校验用，B7 实测 0.6dB @ 此工作点",
        },
    )

    model_config = ConfigDict(frozen=True)
```

### 1.3 参数溯源审计（TL-26 + FR-26 V6）

| 字段 | source_type | audit_flag | 来源精确到行 |
|---|---|---|---|
| R_SYM_B7 | literature | OK | content.md L21/L25/L47 |
| LASER_LW_B7 | literature | OK | content.md L47 |
| ROLL_OFF | literature | OK | content.md L47 |
| RX_BW_GHZ | literature | OK | content.md L47/L49 |
| SPS_RX | literature | OK | content.md L47/L49 |
| DOPPLER_RANGE | literature | OK | content.md L49 |
| DOPPLER_INTERVAL | literature | OK | content.md L49 |
| LEO_DOPPLER_EXCURSION | literature | OK | content.md L47 |
| LEO_DOPPLER_RATE | literature | OK | content.md L47 |
| OSNR_WORKING_POINT_LOW | literature | OK | content.md L21/L69 |
| OSNR_WORKING_POINT_MAIN | literature | OK | content.md L49 |
| GARDNER_SPS | literature | OK | content.md L47 + Gardner 1986 |
| GARDNER_GAIN | typical | WARNING | 典型值（B7 未给精确值）|
| HD_FEC_THRESHOLD | literature | OK | B11 行 181/191（跨候选共用）|
| BER_SENSITIVITY_THRESHOLD | literature | OK | content.md L21/L65/L69 |

**审计结论**：14/15 OK，1 WARNING（GARDNER_GAIN 典型值）。所有 literature 字段 source 精确到 content.md 行号（FR-26 V6 满足）。对比旧 B7Params（多数 source 只写"B7 OFC 2026"没行号），溯源精度提升。

### 1.4 符号率/线宽场景差异决策（用户已拍板）

**决策**：B7 用锚论文原参数 25GBaud/1.8kHz，**不跟 NDA-ML 统一**（NDA-ML 用 2.5GBaud/10kHz）。

**理由**（D-007 教训防重蹈）：
1. B7 锚论文工作点在 25GBaud/1.8kHz，0.6dB 增量在此场景实测（content.md L21/65）
2. 复现 B7 锚方法必须用 B7 场景参数，否则增量数值不可比（重蹈 NDA-ML D-007 覆辙：场景重定义后增量消失）
3. 跨候选可比性通过 fair gain 维度统一（都报 HD-FEC 工作点），不通过场景参数统一
4. NDA-ML 那边继续用 2.5GBaud/10kHz（SystemParams.LASER_LW 单字段）

**B7Params 不合并进 SystemParams**：SystemParams 是 NDA-ML 仿真真相源（2.5GBaud/10kHz），B7Params 是 B7 仿真真相源（25GBaud/1.8kHz），两套独立。common/_channel.py 导入时按候选方法选（B7 脚本 import B7Params，NDA-ML 脚本 import SystemParams）。

### 1.5 下游引用同步清单（D-007 教训 2：参数改后必须同步清理）

sandbox 阶段回写 params.py 后需检查的下游引用：

| 文件 | 引用旧字段 | 需改 |
|---|---|---|
| `common/_recovery.py:psa_foe_recovery` L435 | 旧 PSA_PILOT_SPACING（删除）+ 概念错 | sandbox 重写谱不对称法 |
| `explore/single-carrier-nda-ml/*.py` | 不引用 B7Params | 无需改（NDA-ML 用 SystemParams）|
| `explore/b7-gardner-ted-foe/_b7_map_reconstruction.py` | 硬编码 25GBaud/0.1/16sps | sandbox 改成 import B7Params（0.2a 子 agent 硬编码已记录，可接受）|
| `explore/n1-pcs-gain/*.py` | 不引用 B7Params | 无需改 |
| `explore/a3-pilot-cpe-mve/*.py` | 不引用 B7Params | 无需改 |

**清理策略**：旧 B7Params 字段（DOPPLER_RANGE/OSNR_WORKING_POINT/GARDNER_SPS/GARDNER_GAIN）保留同名不破兼容，新增字段（R_SYM_B7/LASER_LW_B7/ROLL_OFF/RX_BW_GHZ/SPS_RX/DOPPLER_INTERVAL/LEO_DOPPLER_EXCURSION/LEO_DOPPLER_RATE 修正值/OSNR_WORKING_POINT_LOW/OSNR_WORKING_POINT_MAIN/HD_FEC_THRESHOLD/BER_SENSITIVITY_THRESHOLD）sandbox 阶段补全。`PSA_PILOT_SPACING` 删除（概念错）+ `LEO_DOPPLER_RATE` 值修正（30e3→1e9）。

## 2. 阶段 0.6 文件组织

### 2.1 explore 目录结构（当前 + sandbox/MVE 规划）

```
projects/simulation/explore/b7-gardner-ted-foe/
├── _formula_completeness_check.md      # 阶段 0.1 公式完整性（D001，已落盘）
├── _b7_map_reconstruction.py           # 阶段 0.2a 数值重建脚本（sandbox 复用扩展）
├── _b7_map_results.json                # 阶段 0.2a 数值重建数据（coarse/fine/diag）
├── _b7_map_curve.png                   # 阶段 0.2a 数值重建图
├── _b7_map_summary.md                  # 阶段 0.2a 子 agent 摘要
├── _lineage_check.md                   # 阶段 0.2b 数学同族性分析（D002）
├── _stage0_2_summary.md                # 阶段 0.2 综合报告
├── _architecture_decision.md           # 阶段 0.3 架构定性（D003）
├── _fair_comparison_framework.md       # 阶段 0.4 公平对照框架（本轮新建）
├── _stage0_5_6_params_files.md         # 阶段 0.5+0.6 参数+文件组织（本文件）
├── _b7params_draft.py                  # 阶段 0.5 B7Params 草稿（sandbox 回写 params.py）【待建】
│
│   # === sandbox 阶段（阶段 1，下对话开始）===
├── _crb_lower_bound.py                 # FR-21 oracle 下界（B7 FOE 的 CRB，待建）
├── _crb_results.json                   # CRB 结果（待建）
├── _ted_gain_analytic.py               # B7 TED_gain(f_D) 解析推导 + Leven 对比（残留风险闭合，待建）
├── _psa_foe_asymmetry.py               # PSA FOE baseline 重写（谱不对称法，待建）
├── b7_gardner_ted_mve.py               # MVE 主脚本（待建）
├── B7-MVE-SPEC.md                      # MVE 契约（仿 N1/NDA-ML SPEC，待建）
└── _mve_results.json                   # MVE 结果（待建）
```

### 2.2 文件命名规约

- **阶段 0 产出**：`_` 前缀（探针/分析，非主脚本），如 `_fair_comparison_framework.md`
- **sandbox/MVE 主脚本**：无 `_` 前缀，如 `b7_gardner_ted_mve.py` / `B7-MVE-SPEC.md`
- **FR-21 oracle**：`_crb_lower_bound.py`（跟 NDA-ML 命名一致 `_crb_lower_bound.py`）
- **数据/图**：跟脚本同 stem + `_results.json` / `_curve.png`

### 2.3 跟 NDA-ML 文件组织对照（防 E 类混乱）

| 混乱类（NDA-ML 教训）| NDA-ML 问题 | B7 防御（本节规约）|
|---|---|---|
| E. 文件混乱 | MVE 薄包装 + 双套参数共存 + 两 results 目录 | 单 explore/b7-gardner-ted-foe/ 目录 + 单 B7Params 真相源 + 单 _mve_results.json |
| 参数反复 | 线宽 500kHz→10kHz 全量重跑 | 0.5 参数真相源前置（本文件 §1）+ 不写 params.py 草拟在 explore |
| 算法 bug | D003/D-008 双 bug | 0.1 公式完整性 + 0.2 数值重建 + V1 公式逐项核对 |
| 文献引用 | D-007 引 Valjus 位置没读原文数值 | 0.5 所有参数 source 精确到 content.md 行号（FR-26 V6）|

## 3. 阶段 0.5 + 0.6 判定

| 维度 | 判定 | 依据 |
|---|---|---|
| B7Params 草稿完整性 | 15 字段全标 source_type+source+audit_flag | TL-26 + FR-26 V6（行号溯源）|
| LEO_DOPPLER_RATE 修正 | 30e3 → 1e9（Hz/s）| content.md L47「1 GHz/s」|
| 符号率/线宽场景决策 | B7 锚论文原参数 25GBaud/1.8kHz | 用户决策（2026-07-08）+ D-007 教训 |
| 下游引用同步清单 | 5 个文件核查（4 无需改 + 1 sandbox 重写）| D-007 教训 2 |
| explore 目录结构 | 落盘确认 + sandbox/MVE 命名规约 | 防 E 类混乱 |
| 阶段 0 不写 params.py | B7Params 草稿在 explore，sandbox 回写 | INVARIANT 6 |

**门控结论**：0.5 + 0.6 通过。**阶段 0 六项规约全部完成（0.1-0.6）**，可进 sandbox（下对话）。

## 4. 对后续的影响（sandbox 阶段，下对话）

1. **B7Params 回写 params.py**（sandbox 第一步）：本文件 §1.2 草稿回写，删 PSA_PILOT_SPACING，修 LEO_DOPPLER_RATE，补 7 个新字段
2. **PSA FOE baseline 重写**（sandbox 第二步）：新写 `_psa_foe_asymmetry.py`（谱不对称法 Vieira 2023），不用旧 `psa_foe_recovery`
3. **B7 TED_gain(f_D) 解析推导 + Leven 对比**（sandbox 第三步，残留风险闭合）：`_ted_gain_analytic.py`，排除跟 Leven M-th-power FOE [7] 等价（V3 残留风险）
4. **CRB 下界**（sandbox 第四步，FR-21）：`_crb_lower_bound.py`，B7 FOE 的 CRB 下界。FR-21 在 D005 下降级为参考不当 Kill 门，但 sandbox 仍算作对照
5. **三方对照**（sandbox 第五步）：B7 proposed FOE / Gardner 1986 TR / PSA FOE，按 0.4 §4 架构执行
6. **MVE + consistency**（sandbox 第六步）：B7-MVE-SPEC.md 契约 + b7_gardner_ted_mve.py + TL-20 理论预期表（0.4 §5 已草拟）

## 5. 证据指针

- B7 原文参数：`papers/doi/10.1364_ofc.2026.w2a.62/content.md` L21（25-Gbaud+OSNR 10dB）/ L25（25-Gbaud）/ L47（1.8kHz+0.1+36.75GHz+2.94sps+±100MHz@1GHz/s+2sps）/ L49（0-23GHz+1GHz+17dB+36.75GHz+2.94sps）/ L65（0.6dB@BER 2e-2）/ L69（OSNR 10dB）
- 旧 B7Params：`projects/simulation/params.py` L606-680（7 字段，3 问题：LEO_DOPPLER_RATE 错 + 缺 5 字段 + PSA_PILOT_SPACING 概念错）
- NDA-ML 场景参数：`params.py` SystemParams L44-91（2.5GBaud/10kHz）
- D-007 教训：`.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-007（场景重定义后增量消失 + 下游引用同步）
- 用户决策：voice.md 2026-07-08 对话 4（B7 锚论文原参数）
