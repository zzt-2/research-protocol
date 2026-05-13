"""Simulation parameters from simulator_design.md §3.

Sources: K2/M01 (TMC 2026) primary, K3/M06/M08/M09 supplementary.
"""

import math

# === Network Topology (K2/M01 Table III) ===
N_IOTD = 10
N_UAV = 4
N_LEO = 8
N_CS = 1
AREA_SIZE = 1000.0  # meters (1 km × 1 km)

LEO_ALTITUDE = 500e3  # meters
LEO_PLANES = 2  # 2 × 4 configuration
LEO_SATS_PER_PLANE = N_LEO // LEO_PLANES
LEO_INCLINATION = 53.0  # degrees
LEO_MIN_ELEVATION = 10.0  # degrees
EARTH_RADIUS = 6371e3  # meters
MU_EARTH = 3.986004418e14  # m³/s²

# === Computing (K2/M01 Table III) ===
FREQ_IOTD = 0.8e9  # Hz
FREQ_UAV = 3.0e9
FREQ_LEO_RANGE = (4.0e9, 5.0e9)  # uniform sample
FREQ_CS = 10.0e9

KAPPA_IOTD = 5e-27
KAPPA_UAV = 1e-28
KAPPA_LEO = 1e-28
KAPPA_CS = 1e-28

TX_POWER_IOTD = 1.0  # Watts
TX_POWER_UAV = 2.0
TX_POWER_LEO = 5.0
TX_POWER_CS = 5.0

# === Channel (K2/M01 §II-C + Table III/IV) ===
BW_G2U = 20e6  # IoTD-UAV
BW_G2S = 15e6  # IoTD-LEO
BW_U2S = 15e6  # UAV-LEO
BW_ISL = 1e9  # LEO-LEO inter-satellite link
BW_L2C = 1e9  # LEO-CS

NOISE_POWER_DBM = -100.0
NOISE_POWER_W = math.pow(10, (NOISE_POWER_DBM - 30) / 10)

RICIAN_K = 2.0  # 3GPP TR 38.811, G2U link
ANTENNA_GAIN = 1.0  # G_P
BW_ALLOC_FACTOR = 2.0  # ζ_B

# Shadowed-Rician parameters (K2/M01 Table IV)
SR_LIGHT = {"b0": 0.879, "m": 10.13, "Omega": 0.001}
SR_AVERAGE = {"b0": 0.252, "m": 5.21, "Omega": 0.004}
SR_HEAVY = {"b0": 0.146, "m": 1.75, "Omega": 0.025}
SR_DEFAULT_CONDITION = "average"

# Fixed rates for non-fading links
RATE_CS_WIRED = 1e9  # 1 Gbps

# === DAG (K2/M01 §V + M06 Table VI) ===
N_TASKS = 20  # J = number of subtasks per DAG
TASK_INPUT_RANGE = (0.8e6, 4.0e6)  # bytes [0.8 MB, 4 MB]
TASK_OUTPUT_RANGE = (0.4e6, 1.0e6)  # bytes [0.4 MB, 1 MB]
TASK_CYCLES_RANGE = (1.0e9, 3.0e9)  # cycles [1, 3] Gcycles
TASK_DEADLINE_RANGE = (50.0, 60.0)  # seconds

DAGGEN_FAT = 0.6
DAGGEN_DENSITY = 0.4
DAGGEN_REGULAR = 0.9
DAGGEN_JUMP = 1

# === HGAT Architecture (M09 + M06) ===
NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]
EDGE_TYPES = [
    ("task", "dep", "task"),
    ("task", "to_iotd", "iotd"),
    ("task", "to_uav", "uav"),
    ("task", "to_leo", "leo"),
    ("task", "to_cs", "cs"),
    ("iotd", "link", "uav"),
    ("uav", "link", "leo"),
    ("leo", "link", "leo"),
    ("leo", "link", "cs"),
]
HGAT_LAYERS = 2
HGAT_HEADS = 4
HGAT_HIDDEN = 64

# === DRL / PPO (K2/M01 Table III, validated by sweep 2026-05-12) ===
PPO_LR = 5e-4
PPO_BATCH = 128
PPO_CLIP = 0.2
PPO_GAE_LAMBDA = 0.95
PPO_GAMMA = 0.99
PPO_EPOCHS = 4
PPO_MAX_GRAD_NORM = 0.5
PPO_ENTROPY_COEF = 0.05  # sweep-validated (1e-4~5e-4 lr, 10~40 interval, 0.01~0.1 entropy)

# === Reward (D009 + user specification) ===
# R = -(η_t · T_norm + η_e · E_norm + λ₁·Φ₁ + λ₂·Φ₂ + λ₃·Φ₃)
REWARD_ETA_T = 5.0  # latency weight (scaled up to balance with energy; T_norm << E_norm due to fast nodes)
REWARD_ETA_E = 0.5  # energy weight
REWARD_LAMBDA_1 = 10.0  # deadline violation penalty
REWARD_LAMBDA_2 = 5.0  # UAV compute resource overflow penalty
REWARD_LAMBDA_3 = 5.0  # LEO compute resource overflow penalty

# === UAV (K2/M01 Table III, fixed position — no trajectory optimization) ===
UAV_HEIGHT_RANGE = (40.0, 60.0)  # meters AGL
