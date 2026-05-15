"""Simulation parameters aligned with simulator_design.md v2."""

import numpy as np

# ── Constellation (Starlink-like, reduced for simulation) ──────────
NUM_PLANES = 18
SATS_PER_PLANE = 22
NUM_SATS = NUM_PLANES * SATS_PER_PLANE  # 396 (subset of full 1584)
ORBIT_ALTITUDE_KM = 550.0
INCLINATION_DEG = 53.0
EARTH_RADIUS_KM = 6371.0
ORBIT_RADIUS_KM = EARTH_RADIUS_KM + ORBIT_ALTITUDE_KM
MIN_ELEVATION_DEG = 20.0
ORBIT_PERIOD_S = 2 * np.pi * np.sqrt(ORBIT_RADIUS_KM ** 3 / 3.986004418e5)

# ── Channel (Ku-band, aligned with simulator_design.md) ────────────
CARRIER_FREQ_HZ = 12e9             # Ku-band 12 GHz
BANDWIDTH_HZ = 250e6               # 250 MHz
SPEED_OF_LIGHT = 3e8               # m/s
WAVELENGTH_M = SPEED_OF_LIGHT / CARRIER_FREQ_HZ

TX_EIRP_DBW = 45.0                 # Satellite EIRP
RX_GAIN_DBI = 40.0                 # Ground terminal antenna gain (Starlink dish)
RX_NOISE_FIGURE_DB = 2.0
NOISE_TEMP_K = 290.0
K_BOLTZMANN_DBW_HZK = -228.6

# Atmospheric attenuation (ITU-R P.676 simplified)
A_ZENITH_DB = 0.2                  # Ku-band clear-sky zenith attenuation

# Shadow fading (3GPP TR 38.811, LoS)
# σ_SF(θ): elevation-dependent, interpolated from Table 6.6.2-1
# θ=20°→4.0dB, θ=45°→1.5dB, θ=90°→1.0dB
SHADOW_FADING_PARAMS = {
    "sigma_20": 4.0,   # dB at 20° elevation
    "sigma_45": 1.5,   # dB at 45° elevation
    "sigma_90": 1.0,   # dB at 90° elevation
    "sigma_min": 1.0,  # minimum σ
}

# ── Simulation ─────────────────────────────────────────────────────
SIM_DURATION_S = 7200.0            # 2 hours (covering full pass)
DT_S = 10.0                        # Decision interval 10s
NUM_STEPS = int(SIM_DURATION_S / DT_S)
NUM_UES = 15
SAT_CAPACITY = 10                  # Channels per satellite
NUM_EPISODES = 300
NUM_EVAL_SEEDS = 5

# UE location (Beijing area, matching L07's longitude range)
UE_CENTER_LAT = 40.0
UE_CENTER_LON = 116.0
UE_SPREAD_DEG = 3.0

# ── Reward function v2 (simulator_design.md §3) ───────────────────
SINR_MAX_DB = 22.0                 # Normalization reference
SINR_MIN_DB = -5.0                 # For HHS min-max normalization
ELEV_MAX_DEG = 90.0                # For HHS normalization

W_THROUGHPUT = 0.6                 # w_r
W_LOAD = 0.4                       # w_l
W_BLOCK = 0.5                      # w_b
W_HANDOVER = 0.1                   # w_h

# ── HHS (B1, L08 Algorithm 1) ─────────────────────────────────────
HHS_W_SINR = 0.5
HHS_W_ELEV = 0.15
HHS_W_LOAD = 0.25
HHS_W_STAB = 0.1
HHS_P_HO = 0.03
HHS_STAB_K = 0.2                   # Logistic steepness
HHS_STAB_MID = 15.0                # Logistic midpoint (steps)
HHS_DEGRADE_TH_DB = 8.0            # Forced HO threshold
HHS_UPGRADE_TH = 0.02              # Opportunity upgrade threshold

# ── Dueling DDQN (B2, L02 corrected) ──────────────────────────────
DDQN_LR = 1e-3
DDQN_GAMMA = 0.99
DDQN_EPS_START = 0.2
DDQN_EPS_END = 0.01
DDQN_EPS_DECAY = 300               # Exponential decay rate
DDQN_BUFFER_SIZE = 200_000
DDQN_BATCH_SIZE = 256
DDQN_TARGET_UPDATE = 1000          # Steps between target network sync
DDQN_HIDDEN = (256, 128)

# ── PPO (B3, L01/L10 reference) ───────────────────────────────────
PPO_LR = 3e-4
PPO_GAMMA = 0.99
PPO_GAE_LAMBDA = 0.95
PPO_CLIP_EPS = 0.2
PPO_ENTROPY_COEF = 0.01
PPO_VALUE_COEF = 0.5
PPO_UPDATE_EPOCHS = 10
PPO_MINIBATCH_SIZE = 64
PPO_ROLLOUT_STEPS = 2048
PPO_HIDDEN = (256, 256, 128)

# ── Verification thresholds ────────────────────────────────────────
LAG1_AUTOCORR_WARNING = 0.95
REWARD_DOMINATION_THRESHOLD = 0.95  # Single item >95% → FAIL
