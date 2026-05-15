"""M2: VisibilityConnectivity — distance + LoS + FOR → candidate ISL edges.

For each satellite pair, checks:
1. d_{ij} ≤ z_max (3000 km)
2. Line-of-sight (no Earth occlusion)
3. FOR angle constraint (ISL within terminal's field of regard)
"""

import numpy as np
from . import config


class VisibilityConnectivity:
    def __init__(self, z_max=None, for_angle_deg=None):
        self.z_max = z_max or config.Z_MAX
        self.for_angle = np.radians(for_angle_deg or config.FOR_ANGLE_DEG)
        self._sin_for = np.sin(self.for_angle)

    def compute(self, positions_eci):
        """Compute candidate ISL edges from satellite ECI positions.

        Args:
            positions_eci: (n_sats, 3) ECI positions in km.

        Returns:
            edges: list of (i, j, distance_km) tuples.
        """
        n = len(positions_eci)
        # Pairwise difference vectors
        diff = positions_eci[:, np.newaxis, :] - positions_eci[np.newaxis, :, :]
        dist_sq = np.sum(diff ** 2, axis=2)

        # Precompute norms for LoS / FOR
        norms = np.sqrt(np.sum(positions_eci ** 2, axis=1))  # (n,)

        z_max_sq = self.z_max ** 2

        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if dist_sq[i, j] > z_max_sq:
                    continue
                d = np.sqrt(dist_sq[i, j])
                if d < 1.0:
                    continue
                if not self._los(positions_eci[i], positions_eci[j], diff[i, j], dist_sq[i, j]):
                    continue
                if not self._for(positions_eci[i], positions_eci[j], d, norms[i]):
                    continue
                if not self._for(positions_eci[j], positions_eci[i], d, norms[j]):
                    continue
                edges.append((i, j, d))
        return edges

    @staticmethod
    def _los(p1, p2, diff, diff_sq):
        """Line-of-sight: segment p1-p2 doesn't intersect Earth."""
        t = -np.dot(p1, diff) / diff_sq
        t = max(0.0, min(1.0, t))
        closest = p1 + t * diff
        return np.dot(closest, closest) > config.RE ** 2

    def _for(self, p_src, p_dst, dist, norm_src):
        """FOR angle check: ISL direction within terminal's steering cone.

        Terminal can point within ±FOR from local horizontal.
        Angle from zenith must be in [90°-FOR, 90°+FOR].
        """
        dz = p_dst[2] - p_src[2]
        cos_zenith = dz / dist  # simplified: zenith ≈ z-direction for near-polar orbits
        # More accurate: use actual zenith direction
        # z_hat = p_src / |p_src|;  cos_alpha = dot(z_hat, d_hat)
        z_hat_z = p_src[2] / norm_src
        d_hat_z = (p_dst[2] - p_src[2]) / dist
        cos_alpha = z_hat_z * d_hat_z + (
            p_src[0] * (p_dst[0] - p_src[0]) + p_src[1] * (p_dst[1] - p_src[1])
        ) / (norm_src * dist)
        return abs(cos_alpha) <= self._sin_for

    def build_adjacency(self, edges, n_sats):
        """Convert edge list to adjacency structures.

        Returns:
            edge_index: (2, n_edges) int array [src, dst] pairs (bidirectional).
            edge_distances: (n_edges,) float array in km.
        """
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
