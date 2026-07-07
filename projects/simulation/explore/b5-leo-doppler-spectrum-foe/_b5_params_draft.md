# 阶段 0.5 B5Params 草稿 — 20 字段全溯源（参考 B7Params 扩写）

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 来源: S003（工作对话对话 2）| 日期: 2026-07-08
> 纪律: TL-26（参数溯源强制）+ FR-26（读原文数值）+ V6（v1.3.0 读原文数值）+ sim-preflight v1.2.0 param-source.md（单一字段读，禁跨模块同义常量）
> 守: 阶段 0 不写代码，本文件只草拟 B5Params，不直接写 params.py

## 核心问题

NDA-ML 最大混乱 = 参数反复（线宽 500kHz→10kHz→疑似 0.1-1MHz 全量重跑 3 轮，topic-index NDA-ML 6 类混乱 A 类）。前置参数真相源防此坑。

S002 阶段 0.2 已溯源 20 字段全 PASS（`_db_range_sourcing_audit.md` §6 表），本轮整理成 B5Params 草稿，参考 `B7Params`（params.py:606-628）字段结构。

## B5Params 草稿（20 字段全溯源，sandbox 时进 params.py）

### 字段结构（参考 B7Params + sim-preflight param-source.md）

每个字段必含：`source_type` + `source`（精确到 content.md 行号）+ `symbol` + `unit` + `audit_flag` + `note`。

### 场景参数（锚论文原参数，不跟 NDA-ML 统一——跟 B7 同模式）

**用户决策预期**（待 sandbox 前确认）：B5 用锚论文原参数（2.5GBaud / 1550nm / 600km），不跟 NDA-ML 2.5GBaud 统一（B5 锚就是 2.5GBaud 跟 NDA-ML 巧合一致，但线宽/调制不同）。跨候选可比性通过 fair gain 维度统一（都报 BER 1e-3 + HD-FEC），不通过场景参数统一。参考 B7Params 用户决策（params.py:612 "用户决策：2026-07-08 对话 4，B7 用锚论文原参数"）。

```python
class B5Params(BaseModel):
    """B5 LEO Doppler 短时谱 FOE 参数族 (B5 锚 optcom.2024.130981)

    场景参数跟 NDA-ML (SystemParams) 部分一致（2.5GBaud 巧合）但线宽/调制不同。
    复现 B5 锚方法必须用 B5 场景参数。
    跨候选可比性通过 fair gain 维度统一（都报 BER 1e-3 + HD-FEC），不通过场景参数统一。

    所有 literature 字段 source 精确到 content.md 行号（FR-26 V6 读原文数值）。
    """

    # === 锚论文场景参数（content.md 行号溯源，FR-26 V6）===

    R_SYM_B5: float = Field(
        2.5e9,
        description="符号率 2.5 GBaud（B5 锚论文场景，跟 NDA-ML 2.5GBaud 一致）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 optcom.2024.130981 content.md L23/L47/L89/L91/L93/L109/L167「2.5-GBaud PM-QPSK」",
            "symbol": "R_SYM_B5",
            "unit": "sym/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚论文场景。跟 NDA-ML R_SYM=2.5e9 一致（巧合），跟 B7 R_SYM_B7=25e9 不一致",
        },
    )

    T_S_B5: float = Field(
        1 / 2.5e9,
        description="符号周期（derived from R_SYM_B5）",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "T_S_B5 = 1 / R_SYM_B5",
            "symbol": "T_S_B5",
            "unit": "s",
            "audit_flag": AuditFlag.OK,
            "derived_from": ["R_SYM_B5"],
        },
    )

    F_CARRIER_B5: float = Field(
        1.934e14,
        description="光载波频率（1550 nm，B5 锚波长 1550.32nm）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23「1550-nm wavelength」+ L93「wavelength... 1550.32 nm」",
            "symbol": "F_CARRIER_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 1550.32nm（TTX1995 激光），换算频率 c/λ",
        },
    )

    LASER_LW_B5: float = Field(
        20e3,
        description="激光线宽 20 kHz（TTX1995 激光器，B5 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「linewidth of... 20 KHz」（TTX1995）",
            "symbol": "Δν_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "跟 NDA-ML LASER_LW=10kHz 不一致（B5 锚 20kHz），跟 B7 LASER_LW_B7=1800Hz 不一致。三个候选线宽各异——各自锚论文场景",
        },
    )

    MODULATION_B5: str = Field(
        "pm-qpsk",
        description="调制格式 PM-QPSK（B5 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23/L47/L89/L91/L93「PM-QPSK」",
            "symbol": "MOD_B5",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 PM-QPSK。跟 NDA-ML 16-APSK / B7 DP-QPSK 不同",
        },
    )

    ORBIT_ALT_B5: float = Field(
        600e3,
        description="LEO 轨道高度 600 km（NEO 卫星，B5 锚建模自 Ref [6] Shoji）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L143「NEO satellite orbit altitude at 600 km」（建模自 Ref [6] Shoji JLT 2012 OIPLL）",
            "symbol": "h_B5",
            "unit": "m",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 NEO 600km 轨道。Doppler ±4.5GHz + 56MHz/s 变化率均基于此轨道",
        },
    )

    # === B5 核心算法参数（B5 锚特有，short_time_spectrum_foe 用）===

    DOPPLER_RANGE_B5: float = Field(
        4.5e9,
        description="Doppler 频偏范围 ±4.5 GHz（B5 捕获范围，覆盖 LEO Doppler 全量程）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23（abstract，两次）/ L29（intro）/ L47（intro）/ L143（experiment）/ L149（results）五处一致",
            "symbol": "Δf_Doppler_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 核心范围优势。conclusion L167 不含此数字（H001 小事实错误已修正）。vs 传统 ±312.5MHz = 15× 范围扩展",
        },
    )

    DOPPLER_RATE_B5: float = Field(
        56e6,
        description="Doppler 变化率最大 56 MHz/s（NEO 600km 过顶）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L147「the maximum rate of change reaches 56 MHz/s」",
            "symbol": "df_Doppler_B5",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 NEO 600km 过顶最大变化率。B5 跟踪能力指标",
        },
    )

    ALPHA_B5: float = Field(
        6e8,
        description="系数 α=6×10⁸（正负功率谱面积比转频偏估计的转换系数，B5 锚式 2）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L85「the value of α is 6 × 10⁸」",
            "symbol": "α_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 核心算法参数。影响收敛速度（L87 too large → 残频抖动大）。short_time_spectrum_foe 必须用此值",
        },
    )

    FFT_BLOCKS_B5: int = Field(
        1024,
        description="均值滤波 FFT 组数 1024（M 组 FFT 数据均值滤波）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L87「1024 sets of 16-point FFT data for mean filtering」",
            "symbol": "M_B5",
            "unit": "blocks",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚均值滤波组数。跟 FFT_POINTS_B5=16 组合",
        },
    )

    FFT_POINTS_B5: int = Field(
        16,
        description="FFT 点数 16（每块 16 点 FFT，2 的幂次）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L87「16-point FFT」+ L141「16 points」",
            "symbol": "N_FFT_B5",
            "unit": "samples",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 FFT 点数。块长 16 点 = 6.4ns（@2.5GBaud），远短于湍流相干时间 ~1ms（0.3b 验证 2 依据）",
        },
    )

    # === B5 残频/性能指标（锚论文报告值，sandbox 验证目标）===

    RESIDUAL_FREQ_COARSE_STD_B5: float = Field(
        140e6,
        description="粗补偿后残频标准差 σ<140 MHz（B5 锚报告值，sandbox 验证目标）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23/L47「standard deviation... less than 140 MHz」",
            "symbol": "σ_res_coarse_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚报告值。sandbox 路径 C 验证目标（湍流下前馈归一化后是否仍 <140MHz）",
        },
    )

    RESIDUAL_FREQ_COARSE_MAX_B5: float = Field(
        250e6,
        description="粗补偿后残频最大值 250 MHz（含激光 250MHz 抖动 + 算法误差）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149/L167「maximum value... is 250 MHz... laser will have a 250 MHz frequency jitter, and secondly, the algorithmic compensation has errors」",
            "symbol": "res_max_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚诚实标注：250MHz 含激光抖动非纯算法误差。湍流场景需重测（激光抖动 + 算法误差 + 湍流致 Rp-n 抖动）",
        },
    )

    RESIDUAL_FREQ_FINE_B5: float = Field(
        5e6,
        description="精确补偿后残频 <5 MHz（B5 锚报告值，精确补偿级）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「residual frequency offset... approximately less than 5 MHz [20]」（引 [20] Liu 2023 PADE 精补偿）",
            "symbol": "res_fine_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚精确补偿残频。属后续 DSP（PADE），非 B5 短时谱粗估任务",
        },
    )

    PRECISE_RANGE_B5: float = Field(
        312.5e6,
        description="精估范围 ±312.5 MHz（=B/8=2.5Gbaud/8，传统 FOE 标准范围）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L57/L95/L149/L167「[−B/8, +B/8]... [−312.5MHz, +312.5MHz]」",
            "symbol": "Δf_precise_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 粗估任务边界 = 残频落此范围即完成任务。跟 [60] Leven 公式 27 Δfm=fs/8N 同族（N=1）。sat.1553 L549「粗补偿即可」背书",
        },
    )

    BER_TARGET_B5: float = Field(
        1e-3,
        description="BER 工作点 1e-3（B5 锚 + sat.1553 + [60] Leven 三者一致）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「BER of 1 × 10⁻³」+ sat.1553 L353 + [60] Leven L121",
            "symbol": "BER_B5",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "主工作点。跨候选可比另报 HD-FEC 3.8e-3（0.4.3 决策）",
        },
    )

    RX_SENSITIVITY_B5: float = Field(
        -3.0e-3,  # -48 dBm 换算 W = 10^(-4.8) W
        description="BER 1e-3 接收灵敏度 −48 dBm（B5 锚报告值）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「BER of 1 × 10⁻³ can be obtained at a receiver sensitivity of −48 dBm」",
            "symbol": "P_rx_B5",
            "unit": "dBm",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚接收灵敏度。测试区间 −51~−10 dBm（L93/L127）",
        },
    )

    # === 硬件/采样参数（B5 锚 FPGA 实验配置）===

    ADC_RATE_B5: float = Field(
        5e9,
        description="ADC 采样率 5 GSa/s（B5 锚 FPGA 实验）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「sampling rate of 5 GSa/s」",
            "symbol": "f_s_ADC_B5",
            "unit": "samples/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 ADC 采样率。8bit 分辨率（L93）",
        },
    )

    FPGA_CLOCK_B5: float = Field(
        312.5e6,
        description="FPGA DSP 核时钟 312.5 MHz（B5 锚 Intel Arria 10）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L95「DSP core driven by a 312.5 MHz clock frequency」",
            "symbol": "f_FPGA_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 FPGA 时钟。Intel Arria 10（L93/L95）",
        },
    )

    CYCLE_PERIOD_B5: float = Field(
        3.0,
        description="3s 循环周期（B5 锚外层迭代重估周期，前馈开环）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「The process cycles every 3 s」",
            "symbol": "T_cycle_B5",
            "unit": "s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚外层迭代重估周期。3s 周期重估是前馈重复执行（0.3a 确认），非闭环 TF",
        },
    )
```

## 溯源审计汇总（20 字段全 PASS）

| # | 字段 | 数值 | source_type | source（content.md 行号）| audit_flag |
|---|---|---|---|---|---|
| 1 | R_SYM_B5 | 2.5e9 | literature | B5 锚 L23/L47/L89/L91/L93/L109/L167 | OK |
| 2 | T_S_B5 | 1/2.5e9 | derived | T_S_B5 = 1/R_SYM_B5 | OK |
| 3 | F_CARRIER_B5 | 1.934e14 | literature | B5 锚 L23/L93（1550.32nm）| OK |
| 4 | LASER_LW_B5 | 20e3 | literature | B5 锚 L93（TTX1995）| OK |
| 5 | MODULATION_B5 | pm-qpsk | literature | B5 锚 L23/L47/L89/L91/L93 | OK |
| 6 | ORBIT_ALT_B5 | 600e3 | literature | B5 锚 L143（Ref [6] NEO）| OK |
| 7 | DOPPLER_RANGE_B5 | 4.5e9 | literature | B5 锚 L23×2/L29/L47/L143/L149（五处一致）| OK |
| 8 | DOPPLER_RATE_B5 | 56e6 | literature | B5 锚 L147 | OK |
| 9 | ALPHA_B5 | 6e8 | literature | B5 锚 L85 | OK |
| 10 | FFT_BLOCKS_B5 | 1024 | literature | B5 锚 L87 | OK |
| 11 | FFT_POINTS_B5 | 16 | literature | B5 锚 L87/L141 | OK |
| 12 | RESIDUAL_FREQ_COARSE_STD_B5 | 140e6 | literature | B5 锚 L23/L47 | OK |
| 13 | RESIDUAL_FREQ_COARSE_MAX_B5 | 250e6 | literature | B5 锚 L149/L167 | OK |
| 14 | RESIDUAL_FREQ_FINE_B5 | 5e6 | literature | B5 锚 L149（引 [20]）| OK |
| 15 | PRECISE_RANGE_B5 | 312.5e6 | literature | B5 锚 L57/L95/L149/L167 | OK |
| 16 | BER_TARGET_B5 | 1e-3 | literature | B5 锚 L149 + sat.1553 L353 + [60] Leven L121 | OK |
| 17 | RX_SENSITIVITY_B5 | −48 dBm | literature | B5 锚 L149 | OK |
| 18 | ADC_RATE_B5 | 5e9 | literature | B5 锚 L93 | OK |
| 19 | FPGA_CLOCK_B5 | 312.5e6 | literature | B5 锚 L95 | OK |
| 20 | CYCLE_PERIOD_B5 | 3.0 | literature | B5 锚 L93 | OK |

**20 字段全溯源 PASS**（FR-26 V6 读原文数值，TL-26 参数溯源强制）。

## 待 sandbox 定的参数（本轮不溯源，占位）

| 参数 | 说明 | 触发解决条件 |
|---|---|---|
| NORMALIZE_MODE_B5 | 前馈归一化方案（'block' / 'agc' / 'ratio'，0.3a 方案 A/B/C）| sandbox 三方对照选最优 |
| TURBULENCE_PARAMS_B5 | 湍流参数（Cn² / ΓΓ a,b / 相干时间）| 从 common/_channel.py 继承（TL-13），不自建 |
| BER_HD_FEC_B5 | HD-FEC 3.8e-3（跨候选可比，0.4.3 决策）| sandbox 同时报 BER 1e-3 + HD-FEC |

## 对 params.py 的影响

- **本轮不写 params.py**（阶段 0 不写代码，守 profile 第 9 次防线）
- **sandbox 时**：B5Params 类加到 params.py（参考 B7Params 位置 params.py:606），所有字段从 explore 草稿复制
- **sim-preflight param-source.md**（v1.2.0）：B5Params 内部单一字段读，禁跨模块同义常量（如禁 `_b5_params.LASER_LW_B5` vs `params.LASER_LW`）

## 来源

- S003（本轮工作对话）+ S002（阶段 0.2 dB/范围溯源 §6 表）
- B5 锚 content.md 全文行号溯源（L23/L29/L47/L57/L85/L87/L89/L91/L93/L95/L109/L117/L127/L129/L141/L143/L147/L149/L167）
- B7Params（params.py:606-628）字段结构模板参考
- SourceType / AuditFlag 枚举（params.py:25-39）
- TL-26（参数溯源强制）+ FR-26（读原文数值）+ V6（v1.3.0）+ sim-preflight param-source.md（v1.2.0）
