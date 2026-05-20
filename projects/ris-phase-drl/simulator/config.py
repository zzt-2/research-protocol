"""Simulation configuration dataclass."""

from dataclasses import dataclass


@dataclass
class SimConfig:
    """RIS-assisted MU-MISO simulation parameters.

    Physical model: BS (M antennas) serves K single-antenna users via
    an RIS (N reflecting elements). Direct link is blocked (Hd=0).
    """

    # Physical constants
    c: float = 3e8

    # RIS parameters (Ref: L06:100, F3:32-64, L02:80)
    N: int = 100  # RIS elements
    M: int = 8    # BS antennas (Ref: L02:8)
    K: int = 4    # Users (Ref: L02:4)

    # Channel parameters
    kappa_db: float = 10.0  # Rician K-factor dB (Ref: MVE design)
    # VERIFY: total noise power (dBm) = kT0*B + NF = -174+70+10 = -94
    noise_power_dbm: float = -94.0  # Noise power (Ref: L06:SectionIV)
    tx_power_dbm: float = 30.0      # TX power dBm (Ref: micro-cell BS)
    pl_ref_db: float = -30.0        # Reference path loss dB (Ref: L02:SectionIV)
    pl_ref_dist_m: float = 1.0      # Reference distance m (Ref: L02:SectionIV)
    pl_exp_bs_ris: float = 2.2      # BS-RIS path loss exponent (Ref: L02:SectionIV)
    pl_exp_ris_ue: float = 2.8      # RIS-UE path loss exponent (Ref: [ASSUMPTION])
    dist_bs_ris_m: float = 50.0     # BS-RIS distance m (Ref: [ASSUMPTION])
    dist_ris_ue_m: float = 10.0     # RIS-UE distance m (Ref: [ASSUMPTION])

    # Episode parameters
    episode_len: int = 50  # Steps per episode (Ref: MVE design)
    direct_link_blocked: bool = True  # Direct link blocked (Ref: F3:II-A, MVE v2)

    # Training parameters
    total_episodes: int = 3000
    buffer_size: int = 100000   # (Ref: F3:1e5)
    batch_size: int = 256
    lr: float = 1e-3            # (Ref: F3:1e-3)
    gamma: float = 0.99         # (Ref: F3:0.99)
    tau: float = 1e-3           # (Ref: F3:1e-3)
    hidden_dims: tuple = (400, 300)  # (Ref: F3:400)
    seed: int = 42
    device: str = "cuda"

    # Derived quantities (computed in __post_init__)
    noise_power_linear: float = 0.0
    tx_power_linear: float = 0.0
    pl_bs_ris_linear: float = 0.0
    pl_ris_ue_linear: float = 0.0
    obs_dim: int = 0

    def __post_init__(self):
        assert self.M >= self.K, "ZF requires M >= K"
        assert self.N > 0 and self.M > 0 and self.K > 0
        assert self.episode_len > 0

        self.noise_power_linear = 10 ** (self.noise_power_dbm / 10) / 1000
        self.tx_power_linear = 10 ** (self.tx_power_dbm / 10) / 1000
        self.pl_bs_ris_linear = (
            10 ** (self.pl_ref_db / 10)
            * (self.dist_bs_ris_m / self.pl_ref_dist_m) ** (-self.pl_exp_bs_ris)
        )
        self.pl_ris_ue_linear = (
            10 ** (self.pl_ref_db / 10)
            * (self.dist_ris_ue_m / self.pl_ref_dist_m) ** (-self.pl_exp_ris_ue)
        )
        # obs = [Re(H1), Im(H1), Re(H2), Im(H2), cos(theta), sin(theta)]
        self.obs_dim = 2 * self.N * self.M + 2 * self.N * self.K + 2 * self.N
