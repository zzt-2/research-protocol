"""M2: VisibilityConnectivity — distance + LoS + FOR → candidate ISL edges.

Vectorized implementation: O(n²) numpy operations instead of Python loops.
For 1584 sats: ~0.05s vs ~0.5s with Python loop (~10x speedup).
"""

import numpy as np
from . import config


class VisibilityConnectivity:
    def __init__(self, z_max=None, for_angle_deg=None):
        self.z_max = z_max or config.Z_MAX
        self.for_angle = np.radians(for_angle_deg or config.FOR_ANGLE_DEG)
        self._sin_for = np.sin(self.for_angle)

    def compute(self, positions_eci):
        """Compute candidate ISL edges from satellite ECI positions (vectorized)."""
        n = len(positions_eci)
        pos = positions_eci

        # Upper triangular pairs: i < j
        ii, jj = np.triu_indices(n, k=1)
        diff_ij = pos[ii] - pos[jj]  # pos[i] - pos[j], shape (m, 3)
        dist_sq = np.sum(diff_ij ** 2, axis=1)

        # Distance filter
        z_max_sq = self.z_max ** 2
        mask = (dist_sq < z_max_sq) & (dist_sq > 1.0)

        if not np.any(mask):
            return []

        vi, vj = ii[mask], jj[mask]
        vd_sq = dist_sq[mask]
        vd = np.sqrt(vd_sq)

        # Segment from i to j: pos[j] - pos[i] = -diff_ij
        seg = -diff_ij[mask]  # (m, 3)

        # LoS check (vectorized)
        pi = pos[vi]
        t = -np.sum(pi * seg, axis=1) / vd_sq
        t = np.clip(t, 0.0, 1.0)
        closest = pi + t[:, np.newaxis] * seg
        los_mask = np.sum(closest ** 2, axis=1) > config.RE ** 2

        # FOR check (vectorized, both directions)
        norms = np.sqrt(np.sum(pos ** 2, axis=1))

        cos_alpha_ij = np.sum(pi * seg, axis=1) / (norms[vi] * vd)
        cos_alpha_ji = np.sum(pos[vj] * (-seg), axis=1) / (norms[vj] * vd)
        for_mask = (np.abs(cos_alpha_ij) <= self._sin_for) & \
                   (np.abs(cos_alpha_ji) <= self._sin_for)

        combined = los_mask & for_mask
        ri, rj, rd = vi[combined], vj[combined], vd[combined]

        return list(zip(ri.tolist(), rj.tolist(), rd.tolist()))

    def build_adjacency(self, edges, n_sats):
        """Convert edge list to adjacency structures."""
        if not edges:
            return np.zeros((2, 0), dtype=int), np.zeros((0,), dtype=float)

        src, dst, dist = zip(*edges)
        src = np.array(src, dtype=int)
        dst = np.array(dst, dtype=int)
        dist = np.array(dist, dtype=float)

        edge_index = np.stack([
            np.concatenate([src, dst]),
            np.concatenate([dst, src]),
        ], axis=0)
        edge_distances = np.concatenate([dist, dist])

        return edge_index, edge_distances
