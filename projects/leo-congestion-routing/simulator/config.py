"""SimConfig dataclass for LEO Walker delta congestion-aware routing simulator.

Orbital parameters matched to Ch1 (leo-mega-constellation-gnn-routing) for cross-chapter consistency.
"""
from dataclasses import dataclass, field


# Physical constants (shared with constellation.py)
MU_EARTH = 398600.4418   # km^3/s^2
R_EARTH = 6371.0         # km

# ISL link budget
ISL_MAX_DISTANCE = 5000.0  # km, disconnect threshold (polar gap emerges naturally)

# Walker-Delta configs per experiment size: n_nodes -> (P, S)
SIZE_CONFIGS = {
    48:  (4, 12),
    66:  (6, 11),
    288: (12, 24),
    720: (18, 40),
}


@dataclass
class SimConfig:
    # Walker delta constellation (matched to Ch1)
    n_planes: int = 6
    sats_per_plane: int = 11          # 66 nodes for training
    altitude_km: float = 550.0        # km (Starlink-like, matches Ch1)
    inclination_deg: float = 86.4     # degrees (Iridium-like, enables polar gap)
    walker_delta_F: int = 1           # Walker-Delta phasing factor
    polar_gap_lat: float = 70.0       # latitude threshold for inter-plane ISL disable

    # ISL
    isl_capacity_gbps: float = 10.0   # [ASSUMPTION]
    isl_bandwidth_mhz: float = 500.0  # L06 DTAR

    # Traffic
    n_flows: int = 40
    n_heavy: int = 10
    heavy_demand_range: tuple = (3.0, 5.0)    # Gbps
    light_demand_range: tuple = (0.1, 1.0)    # Gbps
    n_popular: int = 3                         # hotspot destination count
    surge_factor: float = 1.0                  # DTAR surge (1.0 = no surge, per contract main eval)
    time_varying: bool = True                  # NHPP intensity modulation
    tv_amplitude: float = 0.3                  # NHPP amplitude

    # Failures
    failure_rate: float = 0.08
    failure_mode: str = "random"      # random / regional / cascading

    # Episode (K-path sequential routing)
    k_paths: int = 4                  # candidate paths per flow (MVE validated)
    t_slots: int = 1                  # legacy: kept for traffic.py compat (unused in K-path mode)

    # GNN
    gnn_type: str = "gat"
    n_layers: int = 2
    n_heads: int = 4
    hidden_dim: int = 64

    # Training
    lr: float = 3e-4
    clip_eps: float = 0.2
    gamma: float = 0.99
    gae_lambda: float = 0.95
    n_epochs: int = 4
    batch_size: int = 64
    max_grad_norm: float = 0.5
    entropy_coef: float = 0.01
    total_episodes: int = 500
    n_seeds: int = 3
    n_eval: int = 50
    update_interval: int = 10
    early_stop_patience: int = 50

    # Device
    device: str = "cuda"
    seed: int = 42

    # Derived (computed in __post_init__)
    n_nodes: int = 0
    n_edges: int = 0
    node_feat_dim: int = 0
    edge_feat_dim: int = 0
    max_degree: int = 0

    def __post_init__(self) -> None:
        self.n_nodes = self.n_planes * self.sats_per_plane
        self.node_feat_dim = 7   # in_load_norm, out_load_norm, is_current_src, is_current_dst, current_demand_norm, is_hotspot, degree_norm
        self.edge_feat_dim = 4   # utilization, edge_type, is_failed, capacity_norm
        self.max_degree = 4      # +Grid max possible degree (2 intra + 2 inter)

        assert self.n_planes > 0 and self.sats_per_plane > 0
        assert 0 <= self.failure_rate < 0.5
        assert self.isl_capacity_gbps > 0
        assert self.t_slots > 0

    @classmethod
    def from_n_nodes(cls, n_nodes: int, **overrides) -> "SimConfig":
        """Create config for a specific node count using SIZE_CONFIGS mapping."""
        if n_nodes not in SIZE_CONFIGS:
            raise ValueError(f"No SIZE_CONFIG for {n_nodes} nodes. Available: {list(SIZE_CONFIGS.keys())}")
        P, S = SIZE_CONFIGS[n_nodes]
        return cls(n_planes=P, sats_per_plane=S, **overrides)
