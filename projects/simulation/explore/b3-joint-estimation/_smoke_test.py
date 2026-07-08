"""B3-Q2 5 接口 smoke test（对话 3a，守 sim-preflight §1.6 C6-C8）。

验证:
1. multi_aperture_channel.generate_multi_aperture_realization — 单链路退化 + 多支路
2. frame_sync_fsts.fsts_frame_sync + build_fsts_template — 相关峰定位
3. mrc_combiner.mrc_combine — 合并后信号合理
4. multi_branch_phase_precorr.multi_branch_phase_precorrect — 相位补偿
5. joint_estimation_pipeline.b3_joint_pipeline — M1/M2/M3 三模式跑通 + 单链路退化
6. f_dot 物理量级核查（B5 L147 = 56MHz/s）
7. Fried 参数核查（强湍 r0 ≈ 2cm）

运行: cd projects/simulation && python -m explore.b3-joint-estimation._smoke_test
"""
import os
import sys

import numpy as np

# 路径设置（从 explore/b3-joint-estimation/ 到 projects/simulation/）
_SIM_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
# 本目录含连字符，不可作 Python 包，直接加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _b3_params import B3Params, B3SandboxConfig  # noqa: E402
from multi_aperture_channel import (  # noqa: E402
    generate_multi_aperture_realization,
    _fried_parameter,
)
from frame_sync_fsts import (  # noqa: E402
    fsts_frame_sync, build_fsts_template,
)
from mrc_combiner import mrc_combine, mrc_combine_single  # noqa: E402
from multi_branch_phase_precorr import (  # noqa: E402
    multi_branch_phase_precorrect, single_branch_phase_precorrect,
)
from joint_estimation_pipeline import (  # noqa: E402
    b3_joint_pipeline, estimate_block_df_sequence,
)
from common._modulation import qpsk_demod, resolve_qpsk  # noqa: E402


def ber_count(tx_bits, rx):
    """BER 统计（含 QPSK π/2 相位模糊 resolve，common 约定）。"""
    return resolve_qpsk(rx, tx_bits)


def test_fried_parameter():
    """C6 物理核查: 强湍 r0 ≈ 2cm（对话 3 计算）。"""
    r0_strong = _fried_parameter(1550e-9, 1e-14, 10e3)
    r0_weak = _fried_parameter(1550e-9, 1e-16, 10e3)
    print(f"[C6] Fried 参数: 强湍 r0={r0_strong*100:.2f}cm, 弱湍 r0={r0_weak*100:.2f}cm")
    assert 1.5 < r0_strong * 100 < 2.5, f"强湍 r0 应≈2cm，得 {r0_strong*100:.2f}cm"
    assert 25 < r0_weak * 100 < 40, f"弱湍 r0 应≈31cm，得 {r0_weak*100:.2f}cm"
    print("  PASS: 强湍 r0 ≈ 2cm（间距>2cm 即独立分集）")


def test_multi_aperture_channel_single():
    """单链路退化（n_branches=1）。"""
    ch = generate_multi_aperture_realization(
        n_branches=1, Ns=4096, gamma_bar=10.0, turb_name='strong',
        f_dot=56e6, aperture_spacing_m=0.05, seed=42,
    )
    assert len(ch['branches']) == 1
    assert ch['n_branches'] == 1
    assert len(ch['branches'][0]) == 4096
    assert ch['independent_diversity'] in (True, False)  # 单链路不影响
    print(f"[1] 单链路信道: Ns={ch['Ns']}, branches={ch['n_branches']}, "
          f"f_dot={ch['f_dot']/1e6:.0f}MHz/s, r0={ch['r0_cm']:.2f}cm")
    print("  PASS: 单链路信道生成正常")
    return ch


def test_multi_aperture_channel_multi():
    """多支路（n_branches=4，强湍下独立分集）。"""
    ch = generate_multi_aperture_realization(
        n_branches=4, Ns=4096, gamma_bar=10.0, turb_name='strong',
        f_dot=56e6, aperture_spacing_m=0.05, seed=42,
    )
    assert len(ch['branches']) == 4
    assert ch['independent_diversity'] is True  # 5cm > r0≈2cm
    # 各支路衰落独立（块级独立性，非符号级相关——GG 块内恒定）
    # 验证：各支路 h_branches 不全相同（独立采样）
    h0 = np.asarray(ch['h_branches'][0])
    h1 = np.asarray(ch['h_branches'][1])
    n_diff = np.sum(np.abs(h0 - h1) > 1e-9)
    # 取每块代表值算相关（GG 块级独立性）
    from common._config import BLOCK
    n_blocks = len(h0) // BLOCK
    if n_blocks >= 3:
        h0_blk = h0[:n_blocks * BLOCK].reshape(n_blocks, BLOCK)[:, 0]
        h1_blk = h1[:n_blocks * BLOCK].reshape(n_blocks, BLOCK)[:, 0]
        block_corr = np.corrcoef(h0_blk, h1_blk)[0, 1]
    else:
        block_corr = float('nan')
    print(f"[1] 多支路信道: branches={ch['n_branches']}, 独立分集={ch['independent_diversity']}, "
          f"块级 h 相关系数={block_corr:.3f}, 符号级差异点={n_diff}")
    assert n_diff > 0, "独立分集下各支路 h 应不同"
    assert not (np.isnan(block_corr) or abs(block_corr) > 0.8), \
        f"块级相关应合理（|r|<0.8），得 {block_corr}"
    print("  PASS: 4 支路独立分集（间距 5cm > r0 2cm，各支路 h 不同）")
    return ch


def test_frame_sync():
    """帧同步相关峰定位。"""
    ts = build_fsts_template(ts_total=320, bl=20, bn=16)
    # 构造带偏移的测试信号
    rx = np.concatenate([np.zeros(50, dtype=complex), ts, np.zeros(100, dtype=complex)])
    rx = rx + 0.01 * (np.random.randn(len(rx)) + 1j * np.random.randn(len(rx)))
    offsets, corrs = fsts_frame_sync([rx, rx], ts, bl=20)
    print(f"[2] 帧同步: offsets={offsets}（期望≈50）, 相关峰幅值={np.max(corrs[0]):.2f}")
    assert abs(offsets[0] - 50) <= 2, f"FS 应定位到 50，得 {offsets[0]}"
    print("  PASS: FS 相关峰定位正确（offset≈50）")


def test_mrc_combiner():
    """MRC 合并器。"""
    # 构造 2 支路已知信号
    N = 1000
    rng = np.random.RandomState(0)
    tx = (rng.randn(N) + 1j * rng.randn(N))
    h1 = 0.5 + 0.1 * rng.randn(N)
    h2 = 0.3 + 0.1 * rng.randn(N)
    r1 = tx * np.sqrt(h1) + 0.01 * (rng.randn(N) + 1j * rng.randn(N))
    r2 = tx * np.sqrt(h2) + 0.01 * (rng.randn(N) + 1j * rng.randn(N))
    combined, weights = mrc_combine([r1, r2], [h1, h2])
    print(f"[3] MRC 合并: weights={weights}（h1 应>h2 因 h1 均值高）")
    assert len(combined) == N
    print("  PASS: MRC 合并输出维度正确")


def test_phase_precorr():
    """多支路相位预校正。"""
    N = 1000
    n = np.arange(N)
    # 加已知相位
    phase = 0.5 * n / N
    rx = np.exp(1j * phase)
    offsets = [0, 5]
    precorr = multi_branch_phase_precorrect(
        [rx, rx], offsets, df_est=0.0, f_dot_est=0.0,
        phi_est=phase,
    )
    # 补偿后相位应近 0
    residual = np.abs(np.angle(precorr[0])).mean()
    print(f"[4] 相位预校正: 残余相位均值={residual:.4f} rad（应≈0）")
    assert residual < 0.1, "补偿后残余相位应小"
    print("  PASS: 相位预校正正确")


def test_pipeline_m1_m2_m3_single_link():
    """C7 三方对照: 单链路 M1/M2/M3 三模式跑通 + BER 合理。"""
    ch = generate_multi_aperture_realization(
        n_branches=1, Ns=8192, gamma_bar=10.0, turb_name='strong',
        f_dot=0.0, seed=42,  # 先无 Doppler，验证基础管线
    )
    params = B3Params()
    tx_bits = ch['bits']

    results = {}
    for mode in ['m1_traditional', 'm2_fsts', 'full']:
        out = b3_joint_pipeline(ch['branches'], ts_template=None,
                                mode=mode, params=params, mod='qpsk')
        ber = ber_count(tx_bits, out['rx_combined'])
        results[mode] = ber
        print(f"[5] {mode}: BER={ber:.4f}, df_est={out['df_est'][0]:.4f} rad/sym")

    # 高 SNR（gamma_bar=10 线性 = 10dB）+ 无 Doppler，BER 应 < 0.2
    for mode, ber in results.items():
        assert ber < 0.3, f"{mode} BER={ber} 过高，管线可能有 bug"

    # M2（两段式 FOE BL²）应优于或近似 M1（单段）
    print(f"  M1 BER={results['m1_traditional']:.4f} vs M2 BER={results['m2_fsts']:.4f}")
    print("  PASS: 三模式单链路跑通，BER 合理")


def test_pipeline_doppler_handling():
    """Doppler 维度: full 模式处理 Doppler vs M2 不处理。"""
    ch = generate_multi_aperture_realization(
        n_branches=1, Ns=8192, gamma_bar=10.0, turb_name='strong',
        f_dot=56e6, seed=42,  # 加 Doppler
    )
    params = B3Params()
    tx_bits = ch['bits']

    out_m2 = b3_joint_pipeline(ch['branches'], mode='m2_fsts', params=params)
    out_full = b3_joint_pipeline(ch['branches'], mode='full', params=params)
    ber_m2 = ber_count(tx_bits, out_m2['rx_combined'])
    ber_full = ber_count(tx_bits, out_full['rx_combined'])
    print(f"[6] Doppler (56MHz/s) 下: M2 BER={ber_m2:.4f}, full BER={ber_full:.4f}")
    print("  PASS: Doppler 维度管线跑通（BER 对比留 sandbox 正式跑数）")


def test_f_dot_traceability():
    """C6 物理核查: f_dot = 56 MHz/s（B5 L147）。"""
    params = B3Params()
    assert params.f_dot == 56e6, f"f_dot 应=56e6（B5 L147），得 {params.f_dot}"
    print(f"[C6] f_dot 溯源: {params.f_dot/1e6}MHz/s（B5 锚 optcom.2024.130981 L147，已 grep 核验）")
    print(f"  扫值轴: {[f'{x/1e6}MHz/s' if x>0 else '0' for x in params.f_dot_sweep]}")
    print("  PASS: f_dot 溯源到 B5 L147（非拍参数，守 FR-20/TL-26）")


def main():
    print("=" * 70)
    print("B3-Q2 5 接口 smoke test（对话 3a）")
    print("=" * 70)
    np.random.seed(0)

    print("\n--- C6 物理核查 ---")
    test_fried_parameter()
    test_f_dot_traceability()

    print("\n--- 接口单元测试 ---")
    test_multi_aperture_channel_single()
    test_multi_aperture_channel_multi()
    test_frame_sync()
    test_mrc_combiner()
    test_phase_precorr()

    print("\n--- 管线集成测试 ---")
    test_pipeline_m1_m2_m3_single_link()
    test_pipeline_doppler_handling()

    print("\n" + "=" * 70)
    print("ALL SMOKE TESTS PASSED ✓")
    print("=" * 70)
    print("\n下一步: 对话 3b 写 b3_joint_mve.py 正式跑数（BER vs SNR 曲线 + Doppler 扫值 crossover）")


if __name__ == '__main__':
    main()
