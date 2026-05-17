"""SimConfig dataclass for LEO Walker delta congestion-aware routing simulator.

Parameters sourced from simulator-design.md §3.
"""

from dataclasses import dataclass


@dataclass
class SimConfig:
    # Walker delta constellation
    n_planes: int = 6
    sats_per_plane: int = 11          # 66 nodes for training
    altitude_km: float = 780.0        # Iridium
    inclination_deg: float = 86.4

    # ISL
    isl_capacity_gbps: float = 10.0   # [ASSUMPTION]
    isl_bandwidth_mhz: float = 500.0  # L06 DTAR
    polar_gap_lat: float = 70.0       # [ASSUMPTION] latitude threshold for inter-plane ISL disable

    # Traffic
    n_flows: int = 40
    n_heavy: int = 10
    heavy_demand_range: tuple = (3.0, 5.0)    # Gbps
    light_demand_range: tuple = (0.1, 1.0)    # Gbps
    n_popular: int = 3                         # hotspot destination count
    surge_factor: float = 5.0                  # DTAR surge
    time_varying: bool = True                  # NHPP intensity modulation
    tv_amplitude: float = 0.3                  # NHPP amplitude

    # Failures
    failure_rate: float = 0.08
    failure_mode: str = "random"      # random / regional

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

    def __post_init__(self) -> None:
        self.n_nodes = self.n_planes * self.sats_per_plane
        # n_edges updated after topology construction
        self.node_feat_dim = 6   # in_load, out_load, demand_as_src, demand_as_dst, is_hotspot, degree
        self.edge_feat_dim = 4   # utilization, edge_type, is_failed, capacity_norm

        assert self.n_planes > 0 and self.sats_per_plane > 0
        assert 0 <= self.failure_rate < 0.5
        assert self.isl_capacity_gbps > 0
        assert self.t_slots > 0
