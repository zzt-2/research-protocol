"""Graph snapshot: combines constellation, topology, channel into a single graph object."""
import numpy as np
import torch
from torch_geometric.data import Data

from config import ISL_MAX_DISTANCE, C_LIGHT, ISL_BANDWIDTH, ISL_SNR_REF, ISL_D_REF
from constellation import WalkerDelta
from topology import build_plus_grid_edges, compute_distances, filter_by_distance
from channel import isl_delay_ms, isl_capacity


def build_snapshot(walker: WalkerDelta, t: float = 0.0):
    """Build a graph snapshot at time t.

    Returns dict with:
      - pos: (N, 3) ECI positions
      - edge_index: (2, E_active) active ISL edges
      - edge_delay: (E_active,) propagation delay in ms
      - edge_cap: (E_active,) capacity in bps
      - edge_dist: (E_active,) distance in km
      - n_disconnected: number of ISLs disconnected
      - directions: (E_full, 4) direction label per edge [intra_fwd, intra_bwd, inter_r, inter_l]
      - direction_mask: (E_active,) which of the 4 directions each active edge corresponds to
    """
    pos = walker.positions(t)
    edge_index = build_plus_grid_edges(walker.P, walker.S)
    dists = compute_distances(pos, edge_index)

    # Direction labels for all edges (before disconnect)
    directions = _compute_direction_labels(edge_index, walker.P, walker.S)

    # Apply disconnect
    active_idx, active_dist, keep_mask = filter_by_distance(edge_index, dists)
    active_directions = directions[keep_mask]

    # Channel model
    delays = isl_delay_ms(active_dist)
    caps = isl_capacity(active_dist)

    return dict(
        pos=pos,
        edge_index=active_idx,
        edge_delay=delays,
        edge_cap=caps,
        edge_dist=active_dist,
        n_disconnected=int((~keep_mask).sum()),
        directions=active_directions,
        N=walker.N,
    )


def _compute_direction_labels(edge_index, P, S):
    """Label each edge with its direction: 0=intra_fwd, 1=intra_bwd, 2=inter_r, 3=inter_l.

    Returns (E,) int array with direction index, or -1 if unknown.
    """
    src, dst = edge_index[0], edge_index[1]
    labels = np.full(len(src), -1, dtype=np.int32)

    for i in range(len(src)):
        sp, sk = divmod(int(src[i]), S)
        dp, dk = divmod(int(dst[i]), S)
        if sp == dp:
            # Intra-orbit
            if dk == (sk + 1) % S:
                labels[i] = 0  # intra forward
            else:
                labels[i] = 1  # intra backward
        else:
            # Inter-orbit
            if dp == (sp + 1) % P:
                labels[i] = 2  # inter right
            else:
                labels[i] = 3  # inter left
    return labels


def compute_pe(plane_ids, sat_ids, P, S, pe_dim=16):
    """Compute Orbital PE: sin/cos encoding of (plane_idx/P, sat_idx/S)."""
    import math
    p_norm = plane_ids.float() / P
    s_norm = sat_ids.float() / S
    n_freq = pe_dim // 4
    parts = []
    for i in range(n_freq):
        freq = 2 ** i * 2 * math.pi
        parts.extend([
            torch.sin(freq * p_norm), torch.cos(freq * p_norm),
            torch.sin(freq * s_norm), torch.cos(freq * s_norm),
        ])
    return torch.stack(parts, dim=-1)


def snapshot_to_pyg(snap, dest_idx, plane_ids, sat_ids, P, S, pe_dim=16):
    """Convert snapshot dict to PyG Data object with precomputed PEs.

    Node features: [is_dest(1), own_PE(16), dest_PE(16)] = 33 dim
    Edge features: [delay_ms(1), dist_km(1)] = 2 dim
    Also computes direction availability mask (4 dirs per node).
    """
    N = snap['N']
    edge_index = torch.tensor(snap['edge_index'], dtype=torch.long)
    edge_attr = torch.tensor(
        np.stack([snap['edge_delay'], snap['edge_dist']], axis=-1),
        dtype=torch.float32
    )

    # Precompute all PEs
    all_pe = compute_pe(plane_ids, sat_ids, P, S, pe_dim)
    dest_pe = all_pe[dest_idx].unsqueeze(0).expand(N, -1)

    is_dest = torch.zeros(N, 1)
    is_dest[dest_idx] = 1.0

    x = torch.cat([is_dest, all_pe, dest_pe], dim=-1)  # (N, 33)

    # Direction availability mask: both orientations of each undirected edge
    OPPOSITE = {0: 1, 1: 0, 2: 3, 3: 2}
    dir_mask = torch.zeros(N, 4, dtype=torch.bool)
    edge_dirs = snap['directions']
    for e in range(edge_index.shape[1]):
        u, v = int(edge_index[0, e]), int(edge_index[1, e])
        d = int(edge_dirs[e])
        if d >= 0:
            dir_mask[u, d] = True
            dir_mask[v, OPPOSITE[d]] = True

    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, dir_mask=dir_mask)
    data.num_nodes = N
    return data


def get_orbital_pe_tensors(walker: WalkerDelta):
    """Precompute orbital PE inputs for a constellation.

    Returns:
      plane_ids: (N,) int tensor
      sat_ids: (N,) int tensor
      P: int
      S: int
    """
    plane_ids = torch.arange(walker.N) // walker.S
    sat_ids = torch.arange(walker.N) % walker.S
    return plane_ids, sat_ids, walker.P, walker.S
