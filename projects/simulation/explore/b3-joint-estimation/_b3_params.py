"""B3Params — B3-Q2 子系统协同联合估计参数（sandbox 实例化）。

来源: _fair_comparison_framework.md §0.5.3 接口定义（S003）。
参数溯源: 全标 source（TL-26/FR-20），f_dot 用 B5Params.DOPPLER_RATE_B5=56e6（B5 锚 L147，
sandbox 对话 3 子 agent 核查确认；DopplerParams.DOPPLER_HIGH=150e6 缺文献，禁用）。

守:
- TL-13/INVARIANT 8: 不污染 common，本文件只在 explore/b3-joint-estimation/
- FR-20/TL-26: 每个物理参数标 source，禁止拍参数
"""
from dataclasses import dataclass, field


@dataclass
class B3Params:
    """B3-Q2 sandbox 参数（单链路强湍+Doppler 主场景 S1）。"""

    # === 信道（复用 common，TL-13）===
    cn2: float = 1e-14          # 强湍 jphot-L357（grep 双源确认）
    z_km: float = 10.0          # jphot-L241（相位屏仿真距离）
    lw_hz: float = 50e3         # jphot-L231/L243（发射+各支路 LO 共享线宽）
    aperture_m: float = 0.2     # jphot-L243（接收望远镜口径）

    # === TS（jphot FSTS 结构）===
    ts_total: int = 320         # jphot-L299（TS 优化总长）
    bl: int = 20                # jphot-L289/L299（块长 BL=20，BL²=400 降噪因子）
    bn: int = 16                # jphot-L299（每段符号数）

    # === Doppler（B3-Q2 增量维度，f_dot 溯源债务已清）===
    # f_dot 精确值 = 56 MHz/s（B5 锚 optcom.2024.130981 L147 "maximum rate of change reaches 56 MHz/s"）
    # 已存 B5Params.DOPPLER_RATE_B5=56e6（params.py:904，literature audit_flag=OK）
    # 注意: DopplerParams.DOPPLER_HIGH=150e6（params.py:217）缺文献（derived 无公式），禁用
    f_dot: float = 56e6         # B5 L147 canonical 中值（sandbox 扫值轴）
    f_res: float = 1e6          # common F_RESIDUAL（params.py:239，FOE 频率分辨率，非 B5 残频）
    # B5 残频量级（参考，本字段不直接用 doppler_phase）：粗补偿后 <140MHz（B5 L23/L47）

    # === 多支路（S3 加分项，主场景 n_branches=1）===
    n_branches: int = 1         # 主场景单链路（jphot Fig.18 单支路 4-QAM 强湍 1.17dB 最显著）
    aperture_spacing_m: float = 0.05  # 多望远镜间距（> 强湍 r0≈2cm 即独立分集，对话 3 Fried 参数计算）

    # === 评估 ===
    fec_threshold: float = 3.8e-3  # jphot-L329/L357 HD-FEC
    r_sym_baud: float = 10e9    # jphot-L231

    # === Doppler 扫值轴（adaptation-scan A4 crossover，§0.4.5 L2）===
    # f_dot ∈ {0, 低, 中, 高} 找 M2/M3 crossover
    # 0=0Hz/s（GEO/静态，对照 jphot 缓变假设）
    # 低=10MHz/s（低仰角/星历预补偿后残余动力学保守值）
    # 中=56MHz/s（B5 L147 过顶最大值，canonical 文献值，crossover 主候选）
    # 高=100MHz/s（400km 文献上限~90MHz/s 取整，搜索摘要未验证但量级可靠）
    f_dot_sweep: tuple = (0.0, 10e6, 56e6, 100e6)

    # === 仿真规模 ===
    n_seeds: int = 10           # 多 seed（adaptation-scan 防坑：物理因果+多 seed）
    gamma_bar_sweep_db: tuple = (-20, -15, -10, -5, 0, 5, 10)  # SNR 扫值（BER vs 光功率曲线）


@dataclass
class B3SandboxConfig:
    """sandbox 三方对照配置（_fair_comparison_framework.md §0.4）。

    M1 传统分立 TS 管线（祖师爷/弱 baseline）
    M2 jphot FSTS（公平对照基准——同 FS+FOE 算法结构）
    M3 B3-Q2 联合（M2 + CPE 联合 + Doppler 维度）
    fair gain Go 判据 = gain_vs_M2 > 0（不用 gain_vs_M1，那是 jphot 继承增益）
    """
    modes: tuple = ('m1_traditional', 'm2_fsts', 'full', 'm3a_cpe_only', 'm3b_doppler_only')
    # M3a = M2 + CPE 联合（无 Doppler）→ CPE 贡献归因
    # M3b = M2 + Doppler（独立 CPE）→ Doppler 贡献归因
    # M3  = M2 + CPE 联合 + Doppler → 全量增量
    scenes: tuple = ('S1', 'S2')  # S1 单链路强湍+Doppler / S2 单链路强湍无 Doppler
    # S3 多支路加分项（sandbox 3b 或后续）
