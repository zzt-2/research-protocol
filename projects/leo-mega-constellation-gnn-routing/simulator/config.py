"""Simulation configuration."""
from dataclasses import dataclass, field

# Physical constants
MU_EARTH = 398600.4418  # km³/s²
R_EARTH = 6371.0  # km
C_LIGHT = 299792.458  # km/s

# ISL parameters (source: L02 Starfield, L03 DuJo)
ISL_BANDWIDTH = 1e9  # Hz, 1 GHz — L03 DuJo §V-A1
ISL_MAX_DISTANCE = 5000.0  # km, disconnect threshold — L02 Starfield §2.2
ISL_SNR_REF = 1e15  # reference SNR at d_ref (optical link, very high)
ISL_D_REF = 2000.0  # km, reference distance for SNR model

# Walker-Delta configurations
CONFIGS = {
    'train_66': dict(P=6, S=11, F=1, alt=550, inc=53),
    'train_100': dict(P=10, S=10, F=1, alt=550, inc=53),
    'train_200': dict(P=10, S=20, F=1, alt=550, inc=53),
    'target_720': dict(P=18, S=40, F=1, alt=550, inc=53),
    'extend_1584': dict(P=72, S=22, F=1, alt=550, inc=53),
}

# Training
TRAIN_CONFIGS = ['train_66', 'train_100', 'train_200']
TARGET_CONFIG = 'target_720'

# Evaluation
N_SNAPSHOTS = 10  # topology snapshots per evaluation
SNAPSHOT_INTERVAL = 60.0  # seconds — L10 MCSR
N_TRAFFIC_MATRICES = 5  # per snapshot
N_SEEDS = 5  # random seeds

# RL
PPO_LR = 3e-4  # [ASSUMPTION] to be tuned
TRAIN_EPISODES = 1000

# GNN
GNN_LAYERS = 2
GNN_HIDDEN = 64
GNN_HEADS = 4
PE_DIM = 16
