"""Backward-compatible re-export layer.
All names from the old common.py are available here.
Usage: `from common import R_SYM, gg_block, ...` still works.
"""

# Constants
from ._config import (
    R_SYM, T_S, F_CARRIER, LASER_LW,
    TURB, BLOCK,
    DOPPLER_HIGH, DOPPLER_LOW, F_RESIDUAL,
    FIXED_CFG, FIXED_CFG_OPTIMAL,
    GAMMA_BAR_DEFAULT,
    DEF_B_BPS, DEF_NW_BPS,
    SIGMA2_LASER, Q_TURB_PARAMS,
    PILOT_PATTERN,
)

# Channel
from ._channel import (
    gg_block, doppler_phase,
    generate_shared_realization, generate_shared_realization_apsk,
)

# Modulation
from ._modulation import (
    qpsk_mod, qpsk_demod, ber_count, resolve_qpsk,
    qam16_mod, qam16_demod, ber_count_qam16, resolve_qam16,
    ber_eval, hard_decision,
    apsk8_mod, apsk8_demod, ber_count_apsk8, resolve_apsk8,
    resolve_apsk8_blockwise,
    m16apsk_mod, m16apsk_demod, ber_count_m16apsk, resolve_m16apsk,
    resolve_m16apsk_blockwise,
)

# Recovery
from ._recovery import (
    fft_foe, dpll_track, dpll_track_dd,
    vv_cpr, bps_cpr, carrier_recovery_fixed,
    da_ml_recovery, nda_ml_recovery,
    gardner_ted_recovery, psa_foe_recovery,
)

# KF
from ._kf import (
    design_Q, kf_unified, get_pilots,
    kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery,
)

# Equalizer
from ._equalizer import amp_limit, mmse_equalize, equalize_oracle, equalize_hmed

# Experiment
from ._experiment import (
    insert_pilots,
    run_fixed, run_kf_oracle, run_kf_frame_h, run_kf_pilot, run_bps,
    db_ratio, run_trial_shared, save_results,
)

# matplotlib setup
import matplotlib
matplotlib.use('Agg')

# scipy import for backward compat
from scipy.stats import gamma as gamma_dist
