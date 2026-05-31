"""
VV Formula Math Analysis: Why Formula B fails.

Formula A: pe = np.unwrap(np.angle(avg)) / M
Formula B: pe = np.unwrap(np.angle(avg) * M) / M

The critical difference is WHEN you multiply by M relative to unwrap.
"""

import numpy as np

np.random.seed(42)
N = 4000  # total symbols
M = 4     # QPSK order
WIN = 64  # averaging window

print("=" * 72)
print("VV PHASE ESTIMATION: FORMULA A vs FORMULA B")
print("=" * 72)

# =====================================================================
# TEST 1: Linear phase (frequency offset) + small noise
# =====================================================================
print("\n" + "=" * 72)
print("TEST 1: LINEAR PHASE (FREQUENCY OFFSET) + SMALL NOISE")
print("=" * 72)

# True phase: linear trend (models frequency offset) + small noise
phi_true = np.cumsum(np.ones(N) * 0.02) + 0.1 * np.random.randn(N)

# QPSK symbols
bits = np.random.randint(0, M, N)
s = (1 / np.sqrt(2)) * np.exp(1j * (2 * np.pi * bits / M + np.pi / M))

# Received signal
rx = s * np.exp(1j * phi_true)

# 4th power operation: removes modulation
raised = rx ** M  # raised signal, angle should be M * phi_true

# Averaging via convolution
kernel = np.ones(WIN) / WIN
avg = np.convolve(raised, kernel, mode='same')

# --- Formula A: unwrap THEN divide ---
phase_A = np.unwrap(np.angle(avg)) / M

# --- Formula B: multiply by M THEN unwrap THEN divide ---
phase_B = np.unwrap(np.angle(avg) * M) / M

# Ground truth for the 4th-power signal: M * phi_true
# But after averaging, we expect the estimate to track M * phi_true smoothly.
# The true phase to compare against is phi_true (the original phase).

# Align indices (convolution edge effects)
margin = WIN
idx = slice(margin, N - margin)

err_A = phase_A[idx] - phi_true[idx]
err_B = phase_B[idx] - phi_true[idx]

mse_A = np.mean(err_A ** 2)
mse_B = np.mean(err_B ** 2)

print(f"\n  Symbols: {N}, Window: {WIN}, M: {M}")
print(f"  Phase range: [{phi_true.min():.2f}, {phi_true.max():.2f}] rad")
print(f"  4th-power angle range: [{np.angle(raised[idx]).min():.2f}, "
      f"{np.angle(raised[idx]).max():.2f}] rad")
print(f"\n  Formula A MSE: {mse_A:.6f} rad^2")
print(f"  Formula B MSE: {mse_B:.6f} rad^2")
print(f"  MSE ratio (B/A): {mse_B / max(mse_A, 1e-30):.1f}x")

# Show angle statistics before/after multiply-by-M
raw_angles = np.angle(avg[idx])
raw_angles_range = raw_angles.max() - raw_angles.min()
mult_angles = np.angle(avg[idx]) * M
mult_angles_range = mult_angles.max() - mult_angles.min()

print(f"\n  --- Angle statistics (after averaging, within window) ---")
print(f"  angle(avg) range:       {raw_angles_range:.2f} rad "
      f"(raw: [{raw_angles.min():.2f}, {raw_angles.max():.2f}])")
print(f"  angle(avg)*M range:     {mult_angles_range:.2f} rad "
      f"(raw: [{mult_angles.min():.2f}, {mult_angles.max():.2f}])")

# Count wrap-around jumps
def count_wraps(angles):
    diffs = np.diff(angles)
    wraps = np.sum(np.abs(diffs) > np.pi)
    return wraps

wraps_raw = count_wraps(raw_angles)
wraps_mult = count_wraps(mult_angles)
print(f"\n  Wraps in angle(avg):       {wraps_raw}")
print(f"  Wraps in angle(avg)*M:     {wraps_mult}")

# Show what unwrap does
unwrapped_A = np.unwrap(raw_angles)
unwrapped_B = np.unwrap(mult_angles)
correction_A = unwrapped_A - raw_angles
correction_B = unwrapped_B - mult_angles
print(f"\n  Unwrap total correction (A): {np.sum(np.abs(correction_A)):.2f} rad")
print(f"  Unwrap total correction (B): {np.sum(np.abs(correction_B)):.2f} rad")

# =====================================================================
# TEST 2: Turbulence-like conditions (Gamma-Gamma fading + AWGN)
# =====================================================================
print("\n" + "=" * 72)
print("TEST 2: GAMMA-GAMMA TURBULENCE + AWGN")
print("=" * 72)

# Gamma-Gamma fading parameters
alpha_gg = 2.5
beta_gg = 1.8
block_size = 100
n_blocks = N // block_size

# Generate Gamma-Gamma fading coefficients
X = np.random.gamma(alpha_gg, 1.0, n_blocks)
Y = np.random.gamma(beta_gg, 1.0, n_blocks)
h_blocks = X * Y  # Gamma-Gamma fading amplitude (simplified)
h_blocks = h_blocks / np.mean(h_blocks)  # normalize mean to 1

# Expand to per-symbol
h = np.repeat(h_blocks, block_size)[:N]
# Add random phase per block (turbulence-induced phase)
turb_phase_blocks = 0.3 * np.random.randn(n_blocks)
turb_phase = np.repeat(turb_phase_blocks, block_size)[:N]

# SNR
snr_db = 15
snr_lin = 10 ** (snr_db / 10)
noise_power = 1.0 / snr_lin

# True phase: linear trend + turbulence phase + small noise
phi_true2 = np.cumsum(np.ones(N) * 0.02) + turb_phase + 0.05 * np.random.randn(N)

# QPSK symbols
bits2 = np.random.randint(0, M, N)
s2 = (1 / np.sqrt(2)) * np.exp(1j * (2 * np.pi * bits2 / M + np.pi / M))

# Received signal with fading and noise
rx2 = h * s2 * np.exp(1j * phi_true2) + np.sqrt(noise_power / 2) * (
    np.random.randn(N) + 1j * np.random.randn(N)
)

# 4th power
raised2 = rx2 ** M

# Averaging
avg2 = np.convolve(raised2, kernel, mode='same')

# Formulas
phase_A2 = np.unwrap(np.angle(avg2)) / M
phase_B2 = np.unwrap(np.angle(avg2) * M) / M

err_A2 = phase_A2[idx] - phi_true2[idx]
err_B2 = phase_B2[idx] - phi_true2[idx]

mse_A2 = np.mean(err_A2 ** 2)
mse_B2 = np.mean(err_B2 ** 2)

print(f"\n  SNR: {snr_db} dB, Fading: Gamma-Gamma (alpha={alpha_gg}, beta={beta_gg})")
print(f"  Block size: {block_size}, N blocks: {n_blocks}")
print(f"  Phase range: [{phi_true2.min():.2f}, {phi_true2.max():.2f}] rad")

raw_angles2 = np.angle(avg2[idx])
mult_angles2 = raw_angles2 * M

print(f"\n  Formula A MSE: {mse_A2:.6f} rad^2")
print(f"  Formula B MSE: {mse_B2:.6f} rad^2")
print(f"  MSE ratio (B/A): {mse_B2 / max(mse_A2, 1e-30):.1f}x")

wraps_raw2 = count_wraps(raw_angles2)
wraps_mult2 = count_wraps(mult_angles2)
print(f"\n  Wraps in angle(avg):       {wraps_raw2}")
print(f"  Wraps in angle(avg)*M:     {wraps_mult2}")

# =====================================================================
# DETAILED WALKTHROUGH: What happens at each step
# =====================================================================
print("\n" + "=" * 72)
print("DETAILED MECHANISM: WHY FORMULA B FAILS")
print("=" * 72)

print("""
STEP-BY-STEP ANALYSIS:

1. After raising rx^M (M=4), the signal angle is:
   angle(rx^M) = M * phi_true + M * modulation_angle + M * noise_angle

   The modulation component is removed by the M-th power (it becomes
   a constant 2*pi*k for QPSK), so:
   angle(rx^M) ≈ M * phi_true + noise

   The raw angle lives in [-pi, pi] (principal value).
   If M * phi_true spans, say, 0 to 6*pi, the raw angle wraps
   around [-pi, pi] multiple times.

2. After averaging (convolution), the wrapped signal is smoothed.
   The averaged angle is STILL in a reduced range because averaging
   does not unwrap. It smooths the wrapped values.

3. FORMULA A: unwrap(angle(avg)) / M
   - angle(avg) is in roughly [-pi, pi]
   - np.unwrap detects jumps > pi and adds 2*pi corrections
   - This correctly recovers the continuous M*phi_true phase
   - Dividing by M gives phi_true
   - The signal to unwrap has a range of ~[-pi, pi] per sample
   - Jumps between consecutive samples are typically small
   - unwrap works correctly: few false detections

4. FORMULA B: unwrap(angle(avg) * M) / M
   - angle(avg) is in [-pi, pi]
   - MULTIPLYING BY M=4 gives [-4*pi, 4_pi] range
   - Now consecutive samples can differ by up to 4*pi * delta
   - np.unwrap uses threshold pi (default) to detect wraps
   - With 4x the range, MANY legitimate phase differences exceed pi
   - unwrap INCORRECTLY adds 2*pi corrections to these points
   - This introduces systematic errors that accumulate
""")

# Numerical demonstration
print("-" * 72)
print("NUMERICAL DEMONSTRATION (first 20 samples from Test 2):")
print("-" * 72)
print(f"{'k':>4s} {'angle(avg)':>10s} {'angle*M':>10s} "
      f"{'unwrap(A)':>10s} {'unwrap(B)/4':>12s} {'true*4':>10s}")
print("-" * 72)

true4 = phi_true2[idx] * M
ang_demo = raw_angles2[:20]
ang4_demo = ang_demo * M
uw_A_demo = np.unwrap(ang_demo)
uw_B_demo = np.unwrap(ang4_demo)

for k in range(20):
    print(f"{k:4d} {ang_demo[k]:10.4f} {ang4_demo[k]:10.4f} "
          f"{uw_A_demo[k]:10.4f} {uw_B_demo[k]/4:12.4f} {true4[k]:10.4f}")

print("-" * 72)

# Show the false wrap detection
print("\nFALSE WRAP DETECTION IN FORMULA B:")
diffs_raw = np.diff(raw_angles2)
diffs_mult = np.diff(mult_angles2)
false_positives = np.sum(np.abs(diffs_mult) > np.pi) - wraps_raw2
print(f"  Jumps > pi in angle(avg):   {wraps_raw2} (legitimate wraps)")
print(f"  Jumps > pi in angle(avg)*M: {wraps_mult2} (total detected)")
print(f"  False positives:             {wraps_mult2 - wraps_raw2}")
print(f"  Each false positive adds a 2*pi correction error,")
print(f"  which after dividing by M=4, gives pi/2 = {np.pi/2:.4f} rad error.")

# =====================================================================
# CONCLUSION
# =====================================================================
print("\n" + "=" * 72)
print("CONCLUSION")
print("=" * 72)
print(f"""
The fundamental error in Formula B is the ORDER OF OPERATIONS:

  Formula A:  unwrap(angle(x)) / M    -- CORRECT
  Formula B:  unwrap(angle(x) * M) / M -- WRONG

Mathematical reason:
  - np.unwrap is designed to handle signals in the [-pi, pi] range
  - It detects wrap-around by looking for jumps > pi
  - Multiplying angle by M BEFORE unwrap expands the range to [-M*pi, M*pi]
  - This creates {wraps_mult2 - wraps_raw2} false wrap detections
  - Each false detection injects a 2*pi/M = pi/2 rad phase error

In Test 1 (clean, linear phase):
  Formula A MSE: {mse_A:.6f},  Formula B MSE: {mse_B:.6f}

In Test 2 (turbulence + noise):
  Formula A MSE: {mse_A2:.6f},  Formula B MSE: {mse_B2:.6f}

Formula B degrades dramatically because turbulence causes larger
phase variations per block, which after *M amplification trigger
even more false unwrap corrections.
""")
