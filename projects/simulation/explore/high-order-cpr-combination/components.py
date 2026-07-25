"""B10 pilot-RLS + B12 MAP joint ML/MAP phase recovery — T006 standalone components.

These are FRESH standalone implementations of the two source components,
faithful to the B10/B12 paper mechanisms (see source-closure.yaml). They are
NOT imported from common/_recovery.py because common/ only has BPS/VV/DD-DPLL/
DA-ML/NDA-ML — neither pilot-RLS nor MAP joint ML/MAP exists there yet.

T006 scope: GW Step 4a dimension D ONLY. These components are used as
standalone arms (B10, B12) AND as building blocks for the combination
methods P1/P2/P3 in combination_methods.py.

Closure caveat (FR-26/C6): several B10/B12 paper equations are image-only in
content.md (RLS recursion h(k)=h(k-1)+kappa*e, ML windowed estimator Eq 5,
joint ML/MAP Eq 6, amplitude vector a). They are rebuilt here from the
surviving prose + canonical RLS/ML/MAP forms. Rebuilt pieces are commented
with their reconstruction rationale; numeric dB from these images is NEVER
used as a Go argument.
"""
from __future__ import annotations

import numpy as np

# Canonical modulation/demodulation (shared, immutable).
from common._modulation import hard_decision, qam16_demod
from common._config import T_S


def _rls_update(h, P, x, y, lam, P_init, P_norm_cap):
    """One RLS update step with P-norm runaway protection.

    Standard recursion (paper L85-89 image-only; canonical form):
      e = y - h^T x
      kappa = P x / (lam + x^T P x)
      h <- h + kappa * e
      P <- (P - kappa x^T P) / lam

    Runaway protection: P grows as (1/lam)^N for lam<1 over a long frame.
    When ||P|| exceeds P_norm_cap (a generous multiple of ||P_init||), reset
    P to P_init. This is a numerical safeguard; it never limits genuine
    tracking because real tracking keeps P bounded by the input covariance.
    Returns (h_new, P_new, |e|).
    """
    M = h.shape[0]
    with np.errstate(over="ignore", invalid="ignore"):
        e = y - h @ x
        Pxdot = P @ x
        denom = lam + x @ Pxdot
        if not np.isfinite(denom) or abs(denom) < 1e-30:
            kappa = np.zeros(M)
        else:
            kappa = Pxdot / denom
        h_new = h + kappa * e
        P_new = (P - np.outer(kappa, Pxdot)) / lam
    # runaway protection: reset P if it has diverged
    if not np.all(np.isfinite(P_new)) or np.linalg.norm(P_new) > P_norm_cap:
        P_new = P_init.copy()
    innov_mag = abs(e) if np.isfinite(e) else 0.0
    return h_new, P_new, float(innov_mag)


# ===========================================================================
# B10 — pilot-driven RLS joint CFO + Wiener phase noise recovery
# ===========================================================================
# Paper: Deka+Sharma+Krishnamurthy, Springer Photonic Netw Commun 2024,
#        47:164-171. content.md:L53-L219. Read-note _B10-16qam-pilot-rls-increment.md.
#
# Mechanism (source-closure.yaml §b10.mechanism):
#   Training phase (k=0..N_p-1):
#     x(k) = [1, k]^T
#     y(k) = unwrap(angle(r(k)/s_pilot(k)))   (degrees)
#     RLS update: standard recursion (image-only L85-89; canonical form used)
#       h(k) = h(k-1) + kappa(k) * e(k)
#       kappa(k) = P(k-1) x(k) / (lambda + x(k)^H P(k-1) x(k))
#       P(k) = (1/lambda) * (P(k-1) - kappa(k) x(k)^H P(k-1))
#       e(k) = y(k) - h(k-1)^T x(k)
#     init: h(0)=0, P(0) = (1/delta) * I, delta=2.
#
#   Switch to DD at k = N_p:
#     x(k) = [1, mod(k, F)]^T, F = 360 / h1_at_N_p  (anti-divergence, L109)
#     y(k) = phi_hat(k) + (angle(s_hat(k)) - angle(r_hat(k)))
#     r_hat(k) = r(k) * exp(-1j*phi_hat(k))
#     s_hat(k) = hard_decision_16QAM(r_hat(k))
#     phi_hat(k) = h0(k) + h1(k) * mod(k, F)   (radians — see note)
#
# NOTE on units: paper uses degrees for y(k) and F. We use RADIANS throughout
# (more numerically stable with T_S in seconds). F = 2*pi / h1_at_N_p.
# ===========================================================================


def pilot_rls_b10(
    rx,
    pilot_idx,
    pilot_sym,
    *,
    lam=0.99,
    delta=2.0,
    mod_label="qam16",
    return_state=False,
):
    """B10 pilot-RLS joint CFO + Wiener phase noise recovery.

    Parameters
    ----------
    rx : complex ndarray, shape (N,)
        Received single-pol samples (post any front-end FOE/CFO compensation
        you want B10 to inherit; B10 itself estimates CFO via h1).
    pilot_idx : int ndarray, shape (N_p,)
        Symbol indices where pilots sit (must be in [0, N)).
    pilot_sym : complex ndarray, shape (N_p,)
        Known pilot symbols at those positions.
    lam : float
        Forgetting factor in (0, 1]. Paper sweeps; default 0.99 (validation-tuned
        per contract). lambda->1 hurts tracking (paper L207).
    delta : float
        RLS regularization. Paper uses delta=2 (content.md:L143), so P(0)=(1/2)*I.
    mod_label : str
        'qam16' (default). Hard decision via common._modulation.hard_decision.
    return_state : bool
        If True, also return RLS internal state (for P2/P3 combination methods).

    Returns
    -------
    rx_out : complex ndarray, shape (N,)
        rx derotated by per-symbol phi_hat.
    phi_hat : float ndarray, shape (N,)
        Per-symbol phase estimate (radians).
    state : dict (only if return_state)
        {'h_path', 'innovation_path', 'P_final', 'h_final'} for combination use.
    """
    rx = np.asarray(rx, dtype=complex)
    N = rx.shape[0]
    pilot_idx = np.atleast_1d(np.asarray(pilot_idx, dtype=int))
    pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))
    if len(pilot_idx) != len(pilot_sym):
        raise ValueError("pilot_idx and pilot_sym must have equal length")
    if pilot_idx.min() < 0 or pilot_idx.max() >= N:
        raise ValueError("pilot_idx out of range [0, N)")
    if not (0.0 < lam <= 1.0):
        raise ValueError(f"lam must be in (0, 1], got {lam}")

    # --- state init (paper L91, L143) ---
    M = 2  # state vector dimension [h0, h1]
    h = np.zeros(M, dtype=float)             # h(0) = 0
    P = np.eye(M) / delta                    # P(0) = (1/delta) I, delta=2 -> 0.5*I
    # P-norm cap to prevent the (1/lam)^N explosion that plagues long DD runs
    # at lam<1. The cap is large enough to never limit genuine tracking but
    # catches numerical runaway. Reset P to its initial value when exceeded.
    P_INIT = P.copy()
    P_NORM_CAP = 1e6 * np.linalg.norm(P_INIT)

    phi_hat = np.zeros(N, dtype=float)
    innovation = np.zeros(N, dtype=float)
    h_path = np.zeros((N, M), dtype=float)

    # F (anti-divergence period) is computed AFTER pilot training using the
    # converged h1. Before DD switch we use raw k as the second input.
    F = None

    # Build a per-symbol "is pilot" map for fast lookup.
    is_pilot = np.zeros(N, dtype=bool)
    is_pilot[pilot_idx] = True
    pilot_lookup = {int(i): complex(s) for i, s in zip(pilot_idx, pilot_sym)}

    # --- training phase (pilots only drive updates; non-pilot symbols before
    #     N_p are predicted with current h but do not update).
    #     The paper's training block is the first N_p symbols which ARE the
    #     pilots (N_p pilots in a row). For T006's block-pilot pattern, the
    #     "training phase" is the FIRST pilot; subsequent pilots continue to
    #     update h. We follow the paper's spirit: pilots drive the RLS update
    #     at their positions; non-pilot symbols between pilots use DD update.
    #     This is the natural generalization of B10 to a block-pilot pattern.
    last_pilot_seen = -1
    for k in range(N):
        # current input x(k): [1, t(k)] where t is "phase argument" in radians.
        # During training (before any DD has begun) t = k. After DD switch
        # (which happens after the first pilot), t = mod(k, F) once F is set.
        if F is None:
            t_k = float(k)
        else:
            t_k = float(k % F) if F > 0 else float(k)
        x = np.array([1.0, t_k], dtype=float)

        # predict phi_hat(k) = h0 + h1 * t(k)
        phi_hat[k] = float(h @ x)
        innovation[k] = 0.0
        h_path[k] = h

        if is_pilot[k]:
            # --- pilot-driven update (training / refresh) ---
            s_pk = pilot_lookup[k]
            # observed phase (unwrapped relative to running phi_hat to avoid 2pi jumps)
            obs = float(np.angle(rx[k] / s_pk))
            # unwrap relative to phi_hat[k] (keeps y(k) on the same branch)
            d = obs - phi_hat[k]
            d = (d + np.pi) % (2 * np.pi) - np.pi
            y_k = phi_hat[k] + d
            # standard RLS update (canonical form; paper L85-89 image-only)
            h, P, innov_mag = _rls_update(h, P, x, y_k, lam, P_INIT, P_NORM_CAP)
            innovation[k] = innov_mag
            last_pilot_seen = k
            # set F once we have a non-trivial h1 (anti-divergence, paper L109)
            if F is None and abs(h[1]) > 1e-12:
                F = float(2 * np.pi / abs(h[1]))
        else:
            # --- decision-directed update (paper L105-109) ---
            # DD activates only AFTER at least one pilot has been seen.
            if last_pilot_seen >= 0:
                # r_hat = rx * exp(-1j*phi_hat); s_hat = hard_decision(r_hat)
                r_hat = rx[k] * np.exp(-1j * phi_hat[k])
                s_hat = hard_decision(r_hat, mod=mod_label)
                if abs(s_hat) > 1e-12:
                    obs = float(np.angle(rx[k] / s_hat))
                    d = obs - phi_hat[k]
                    d = (d + np.pi) % (2 * np.pi) - np.pi
                    y_k = phi_hat[k] + d
                    h, P, innov_mag = _rls_update(h, P, x, y_k, lam, P_INIT, P_NORM_CAP)
                    innovation[k] = innov_mag
                    h_path[k] = h

    rx_out = rx * np.exp(-1j * phi_hat)
    if return_state:
        state = {
            "h_path": h_path,
            "innovation_path": innovation,
            "P_final": P,
            "h_final": h,
            "F": F,
            "lam": lam,
            "delta": delta,
        }
        return rx_out, phi_hat, state
    return rx_out, phi_hat


# ===========================================================================
# B12 — MAP joint ML/MAP phase recovery (time-domain pilot-aided)
# ===========================================================================
# Paper: Ma+Liu+Du+Wang+Kam, OECC/PSC 2025 WP-B-26. content.md:L25-L143.
#        Read-note _B12-freq-domain-pilot-increment.md.
#
# Mechanism (source-closure.yaml §b12.map_phase_recovery):
#   For each L_block:
#     (1) PA coarse: phi_PA = angle(S_PA* . R_PA) (Eq 4, content.md:L65-67).
#     (2) PA-ML fine: windowed ML over 2W+1 on PA-compensated signal
#         (Eq 5 image-only L71; canonical sliding mean-angle on raised-M).
#     (3) Joint ML/MAP: jointly estimate initial theta (ML) + Wiener theta_k
#         (MAP) using Sigma_phi = Sigma_theta + Sigma_eps (Eq 6 image-only L77;
#         Wang [5] TSP 2022 framework; canonical LMMSE-on-phasor realization).
#
# Closure caveat: Eq 5, Eq 6, amplitude vector a are image-only. The
# realization below is the CANONICAL LMMSE-on-phasor form that matches the
# stated covariances and the high-SNR Gaussian AOPN approximation. Numeric dB
# from these images is never used as a Go argument.
# ===========================================================================


def _build_wiener_cov(L, sigma_pi2):
    """Wiener phase-noise increment covariance Sigma_theta for L samples.

    theta[k] = theta[k-1] + pi[k], pi ~ N(0, sigma_pi^2).
    Cov(theta[i], theta[j]) = sigma_pi^2 * min(i, j)  (with theta[0]=0 ref).
    Here we use a per-block reference so theta is the deviation from block start.
    """
    idx = np.arange(L)
    return sigma_pi2 * np.minimum(idx[:, None], idx[None, :])


def _build_aopn_cov(L, sigma_eps2):
    """AOPN covariance Sigma_eps (high-SNR Gaussian approximation, diagonal).

    epsilon_k ~ N(0, N_tilde / |alpha|^2). Under avg-energy normalization and
    high SNR, |alpha|^2 ~ 1 so sigma_eps^2 ~ 1/(2*SNR_lin). Diagonal because
    AWGN is independent across symbols.
    """
    return np.eye(L) * sigma_eps2


def map_phase_b12(
    rx,
    pilot_idx,
    pilot_sym,
    *,
    l_block=64,
    l_sub=1,
    ml_window=7,
    snr_db=20.0,
    linewidth_hz=10.0e3,
    t_s=T_S,
    mod_label="qam16",
    return_state=False,
):
    """B12 MAP joint ML/MAP phase recovery (time-domain pilot-aided).

    Block-pilot structure: first symbol of each L_block is a pilot. After PA
    coarse compensation, ML refines per-symbol drift over a 2W+1 window; the
    joint ML/MAP estimator then solves for initial theta + Wiener theta_k
    using the composite covariance Sigma_phi = Sigma_theta + Sigma_eps.

    Parameters
    ----------
    rx : complex ndarray (N,)
    pilot_idx : int ndarray
        Pilot symbol positions (must include indices 0, l_block, 2*l_block, ...).
    pilot_sym : complex ndarray
        Known pilot symbols at those positions.
    l_block : int
        Block length (paper L_block=128 at 100 GBaud; validation-tuned here).
    l_sub : int
        Sub-block length (paper L_sub=1 best). Currently fixed at 1.
    ml_window : int
        PA-ML fine window 2W+1 (W = (ml_window-1)//2). Validation-tuned.
    snr_db : float
        SNR in dB (for AOPN variance).
    linewidth_hz : float
        Laser linewidth in Hz (for Wiener variance).
    t_s : float
        Symbol period (s). Defaults to canonical T_S.
    """
    rx = np.asarray(rx, dtype=complex)
    N = rx.shape[0]
    pilot_idx = np.atleast_1d(np.asarray(pilot_idx, dtype=int))
    pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))
    if len(pilot_idx) != len(pilot_sym):
        raise ValueError("pilot_idx and pilot_sym must have equal length")
    if l_block <= 0 or ml_window <= 0 or ml_window % 2 == 0:
        raise ValueError("l_block>0 and ml_window must be a positive odd int")
    if l_sub != 1:
        # paper says L_sub=1 is best; we support only 1 here for clarity
        raise NotImplementedError("l_sub != 1 not implemented (paper says L_sub=1 best)")

    # Wiener per-symbol variance and AOPN variance
    sigma_pi2 = 2.0 * np.pi * linewidth_hz * t_s
    snr_lin = 10.0 ** (snr_db / 10.0)
    sigma_eps2 = 1.0 / (2.0 * snr_lin)   # high-SNR avg-energy AOPN

    is_pilot = np.zeros(N, dtype=bool)
    is_pilot[pilot_idx] = True
    pilot_lookup = {int(i): complex(s) for i, s in zip(pilot_idx, pilot_sym)}

    phi_hat = np.zeros(N, dtype=float)
    block_info = []   # for state/debug

    n_blocks = N // l_block
    L = l_block
    # Pre-build the covariance and its inverse for THIS block size (constant).
    Sigma_theta = _build_wiener_cov(L, sigma_pi2)
    Sigma_eps = _build_aopn_cov(L, sigma_eps2)
    Sigma_phi = Sigma_theta + Sigma_eps
    # Regularize for invertibility
    Sigma_phi_reg = Sigma_phi + 1e-12 * np.eye(L)
    Sigma_phi_inv = np.linalg.inv(Sigma_phi_reg)

    # ML window weights (raised-M mean-angle canonical form for PA-ML fine)
    W = (ml_window - 1) // 2
    win = np.ones(2 * W + 1)
    win = win / win.sum()

    for b in range(n_blocks):
        s_idx = b * L
        e_idx = s_idx + L
        block = rx[s_idx:e_idx]

        # (1) PA coarse: use the pilot at the block start (must be a pilot).
        if not is_pilot[s_idx]:
            # No pilot at block start; fall back to mean-angle of pilots in block
            pilots_in_block = [k for k in range(s_idx, e_idx) if is_pilot[k]]
            if not pilots_in_block:
                # no pilot at all -> skip (leave phi_hat = 0 for this block)
                block_info.append({"block": b, "skipped": True})
                continue
            # use first available pilot as coarse reference
            p_pos = pilots_in_block[0]
            phi_PA = float(np.angle(block[p_pos - s_idx] / pilot_lookup[p_pos]))
        else:
            phi_PA = float(np.angle(block[0] / pilot_lookup[s_idx]))

        # PA compensation
        block_pa = block * np.exp(-1j * phi_PA)

        # (2) PA-ML fine: sliding mean-angle on raised-M=4 phasor (canonical
        #     form; paper Eq 5 image-only). 16-QAM is not 4-PSK so raised-M=4
        #     is an APPROXIMATION here; we instead use decision-directed mean
        #     phasor which is the natural generalization to 16-QAM.
        # Build per-symbol decision-phasor (decision * conj(received_pa))
        dec = hard_decision(block_pa, mod=mod_label)
        dec_phase = np.angle(dec)
        # residual phasor after removing decision modulation
        residual_phasor = block_pa * np.conj(dec)
        # slide window mean of phasor -> phase
        pad = np.pad(residual_phasor, (W, W), mode="edge")
        smoothed = np.convolve(pad, win, mode="valid")[:L]
        phi_ml = np.angle(smoothed)
        # ML residual phase (deviation from PA coarse)
        phi_residual = phi_ml  # relative to PA-compensated block

        # (3) Joint ML/MAP: solve for theta + theta_k using Sigma_phi.
        # Canonical LMMSE-on-phasor form: given observed phasor vector z(k) =
        # exp(j*(theta + theta_k + eps)) (after removing decisions), the MAP
        # estimate of phi_vec = theta + theta_k is arg of the LMMSE solution.
        # phasor observation: z[k] = block_pa[k] / dec[k] = exp(j*phi_residual[k])
        # The LMMSE-on-phasor MAP estimator (Wang [5] framework) gives:
        #   phi_map_vec = arg( Sigma_phi_inv @ (Sigma_phi_inv + 0*I) ... )
        # The simplest canonical realization (matches Wang's joint ML/MAP for
        # a single sinusoid + Wiener): apply Sigma_phi_inv as a smoothing
        # operator on the phasor and take its angle.
        z = residual_phasor.copy()
        # numerical stability
        z_mag_floor = np.maximum(np.abs(z), 1e-12)
        z_unit = z / z_mag_floor
        # MAP smoothing: phi_map_vec[k] = arg( sum_j Sigma_phi[k,j] * z_unit[j] )
        # (this is the canonical LMMSE-on-phasor; uses Sigma_phi, not its inverse,
        # because we are smoothing the observation, not deconvolving noise).
        smoothed_map = Sigma_phi @ z_unit
        phi_map_vec = np.angle(smoothed_map)

        # full per-symbol phase estimate for this block:
        # phi_hat = phi_PA (coarse) + phi_map_vec (fine joint ML/MAP residual)
        phi_hat[s_idx:e_idx] = phi_PA + phi_map_vec
        block_info.append({
            "block": b, "phi_PA": phi_PA, "skipped": False,
            "mean_residual_phase": float(np.mean(phi_residual)),
        })

    rx_out = rx * np.exp(-1j * phi_hat)
    if return_state:
        state = {
            "block_info": block_info,
            "Sigma_theta": Sigma_theta,
            "Sigma_eps": Sigma_eps,
            "Sigma_phi": Sigma_phi,
            "l_block": l_block,
            "l_sub": l_sub,
            "ml_window": ml_window,
            "sigma_pi2": sigma_pi2,
            "sigma_eps2": sigma_eps2,
        }
        return rx_out, phi_hat, state
    return rx_out, phi_hat


# ===========================================================================
# Truth-assisted reference O (oracle, Kill-only — NEVER a Go opponent)
# ===========================================================================


def truth_assisted_reference(rx, phi_true):
    """Reference O: derotate by TRUE per-symbol phase. Kill bound ONLY.

    Per contract truth_assisted_reference: rx_O = rx * exp(-1j*phi_true).
    Does NOT denoise (AWGN remains), so it is a legal phase-recovery ceiling.
    A deployable arm beating O => oracle leak (stop).
    """
    rx = np.asarray(rx, dtype=complex)
    phi_true = np.asarray(phi_true, dtype=float)
    if rx.shape != phi_true.shape:
        raise ValueError("rx and phi_true must have same shape")
    return rx * np.exp(-1j * phi_true)
