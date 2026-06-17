"""确认 bug：pilot 位置实际是随机数据，不是 pilot_sym。

信道 with_pilot_header=False（默认），tx 全是随机 QPSK。
我却在 pilot_idx 位置当 pilot_sym 提取相位——提取的是随机数据相位，自然失效。
"""
import numpy as np
from a3_channel import generate_shared_realization, ber_count
from a3_baselines import fft_foe

ch = generate_shared_realization(8192, 20.0, 'strong', seed=42)
N = len(ch['rx_raw'])
sp = 8
pilot_idx = np.arange(0, N, sp)
pilot_sym = (1+1j)/np.sqrt(2)

print("=== bug 确认：pilot 位置 tx 是什么？===")
print(f"  tx[pilot_idx[:8]] = {ch['tx'][pilot_idx[:8]].round(3)}")
print(f"  pilot_sym = {pilot_sym:.3f}")
print(f"  → tx[pilot] {'=' if np.allclose(ch['tx'][pilot_idx[:8]], pilot_sym) else '≠'} pilot_sym")
print(f"  → 确认：pilot 位置是随机 QPSK 数据，不是 pilot_sym（bug 确认）")

print("\n=== 修复：生成信道时 with_pilot_header=True，pilot 位置放已知 pilot_sym ===")
# 需要修改 generate_shared_realization 让 pilot 位置真的是 pilot_sym
# 当前 with_pilot_header=True 时 tx[pilot_idx] = (1+1j)/sqrt2，但 frame_len 默认 64
# 我要的是 sp=8 的密集 pilot。改用 with_pilot_header + frame_len=8

ch2 = generate_shared_realization(8192, 20.0, 'strong', seed=42, with_pilot_header=True, frame_len=sp)
pilot_idx2 = ch2['pilot_idx']
print(f"  with_pilot_header=True, frame_len={sp}")
print(f"  tx[pilot_idx2[:8]] = {ch2['tx'][pilot_idx2[:8]].round(3)}")
print(f"  → tx[pilot] {'=' if np.allclose(ch2['tx'][pilot_idx2[:8]], pilot_sym) else '≠'} pilot_sym")

# 现在用正确 pilot 提取
f0 = fft_foe(ch2['rx_raw'], M=4)
rx_defo = ch2['rx_raw'] * np.exp(-1j * f0 * np.arange(N))
phi_true_resid = ch2['phi_ao'] + ch2['phi_doppler'] - f0*np.arange(N)

# pilot 相位提取（这次 tx[pilot] 真的是 pilot_sym）
pilot_phase = np.angle(rx_defo[pilot_idx2] / pilot_sym)
pilot_phase_u = np.unwrap(pilot_phase)
phi_ref = np.interp(np.arange(N), pilot_idx2, pilot_phase_u)
rx_comp = rx_defo * np.exp(-1j * phi_ref)
dm = ch2['data_bits_mask'].copy()
ber = ber_count(ch2['tx'], rx_comp, data_mask=dm, resolve_ambiguity=True)

rx_oracle = ch2['rx_raw'] * np.exp(-1j * ch2['phi_total'])
ber_oracle = ber_count(ch2['tx'], rx_oracle, resolve_ambiguity=True)
ber_raw = ber_count(ch2['tx'], rx_defo, resolve_ambiguity=True)

# 估计误差
err = pilot_phase_u - phi_true_resid[pilot_idx2]
print(f"\n  pilot 估计误差 std: {np.std(err):.4f} rad (CRLB ≈ {1/np.sqrt(2*100*0.81):.4f})")
print(f"  oracle={ber_oracle:.6f}, raw+foe={ber_raw:.6f}, pilot={ber:.6f}")
gf = (ber_raw - ber) / max(ber_raw - ber_oracle, 1e-9)
print(f"  gap_fill = {gf:.2%}")
