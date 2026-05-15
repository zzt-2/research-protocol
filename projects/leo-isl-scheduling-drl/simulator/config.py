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
N_LCT = 3  # laser terminals per satellite [L01/L02, D012]

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
