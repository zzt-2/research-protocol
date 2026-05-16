"""Shared constants for LEO ISL scheduling simulator."""

# Earth
RE = 6371.0  # km
MU = 398600.4418  # km³/s²
C_LIGHT = 299792.458  # km/s
OMEGA_EARTH = 7.2921159e-5  # rad/s

# Constellation (Starlink Phase I v2 [L04])
N_PLANES = 24
SATS_PER_PLANE = 66
N_SATS = N_PLANES * SATS_PER_PLANE  # 1584
ALTITUDE = 550.0  # km
INCLINATION_DEG = 53.0  # degrees

# ISL
Z_MAX = 3000.0  # km, max ISL range [L01 §III-A]
FOR_ANGLE_DEG = 60.0  # degrees [L01 §III-A]
N_LCT = 4  # laser terminals per satellite [L01/L02, D030: match B1's 4 fixed ISLs]

# Channel (Gaussian beam [L01 §II-C])
WAVELENGTH = 1.55e-6  # m (1.55 μm)
W0 = 9.87e-3  # m (beam waist radius)
P_TX = 20.0  # W
BANDWIDTH = 1.0e9  # Hz (1 GHz)
APERTURE = 0.01  # m² (receiver area)
RESPONSIVITY = 0.5  # A/W
SIGMA_NOISE = 3e-7  # A (noise current std)
SIGMA_JITTER = 1e-5  # rad (10 μrad [L01 §II-B])
OUTAGE_EPS = 1e-3  # outage probability threshold [L01 §III-D]

# Traffic
N_GS = 100  # [L01]
MIN_ELEVATION_DEG = 10.0  # degrees

# Timing
TAU = 10.0  # s, decision interval [D007]
EPISODE_STEPS = 50  # [D008]
SETUP_DELAY_MIN = 2.0  # s [L04]
SETUP_DELAY_MAX = 30.0  # s [L04]

# Reward weights [D009]
W_THROUGHPUT = 1.0
W_SWITCH = 0.3
W_SETUP = 0.2

# Routing
HOP_DELAY = 0.001  # s (1 ms/hop [L04])

# ILP Solver
ILP_TIME_LIMIT = 60       # seconds, max solve time per snapshot
ILP_GAP_TOL = 0.01        # 1% optimality gap tolerance

# Phase A (Supervised Pretraining)
PHASE_A_LR = 1e-3
PHASE_A_EPOCHS = 100
PHASE_A_BATCH_SIZE = 32
PHASE_A_EARLY_STOP = 15
PHASE_A_N_SNAPSHOTS = 500

# Phase B (Discrete RL Fine-tuning)
PHASE_B_LR = 1e-4
PHASE_B_EPISODES = 200
PHASE_B_UPDATE_INTERVAL = 5
PHASE_B_PPO_EPOCHS = 4
PHASE_B_ENTROPY_COEF = 0.05
PHASE_B_FREEZE_UPDATES = 2
PHASE_B_CLIP_EPS = 0.2
PHASE_B_GAMMA = 0.99
PHASE_B_GAE_LAMBDA = 0.95

# Discrete action space
N_DISCRETE_ACTIONS = 3     # AS-IS=0, FORCE-ON=1, FORCE-OFF=2
