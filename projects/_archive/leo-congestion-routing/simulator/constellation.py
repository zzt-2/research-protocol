"""Walker-Delta constellation: satellite position calculation.

Ported from leo-mega-constellation-gnn-routing/simulator/constellation.py.
"""
import numpy as np

MU_EARTH = 398600.4418   # km^3/s^2
R_EARTH = 6371.0         # km


class WalkerDelta:
    """Walker-Delta constellation defined by T/P/F + altitude + inclination.

    Satellite indexing: idx = p * S + k, where p = plane index, k = sat index in plane.
    """

    def __init__(self, P, S, F=1, alt=550.0, inc=53.0):
        self.P = P
        self.S = S
        self.F = F
        self.alt = alt
        self.inc = np.radians(inc)
        self.N = P * S
        self.r = R_EARTH + alt
        self.period = 2 * np.pi * np.sqrt(self.r ** 3 / MU_EARTH)
        self.mean_motion = 2 * np.pi / self.period

        # RAAN per plane: Omega_p = 2*pi*p / P
        self._raan = 2 * np.pi * np.arange(P) / P

        # Initial argument of latitude: u0_{p,k} = 2*pi*(k + F*p/P) / S
        k_arr = np.arange(S, dtype=np.float64)
        p_arr = np.arange(P, dtype=np.float64)
        self._u0 = (2 * np.pi / S) * (
            k_arr[np.newaxis, :] + (self.F * p_arr[:, np.newaxis] / self.P)
        )  # (P, S)

        self._cos_raan = np.cos(self._raan)[:, np.newaxis]
        self._sin_raan = np.sin(self._raan)[:, np.newaxis]
        self._cos_inc = np.cos(self.inc)
        self._sin_inc = np.sin(self.inc)

    def positions(self, t=0.0):
        """ECI positions at time t (seconds). Returns (N, 3) in km."""
        u = self._u0 + self.mean_motion * t  # (P, S)

        cos_u = np.cos(u)
        sin_u = np.sin(u)

        x = self.r * (self._cos_raan * cos_u - self._sin_raan * sin_u * self._cos_inc)
        y = self.r * (self._sin_raan * cos_u + self._cos_raan * sin_u * self._cos_inc)
        z = self.r * sin_u * self._sin_inc

        return np.stack([x.ravel(), y.ravel(), z.ravel()], axis=-1)  # (N, 3)

    def latitudes(self, t=0.0):
        """Geocentric latitude in degrees at time t. Returns (N,) array."""
        pos = self.positions(t)
        r_xy = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2)
        return np.degrees(np.arctan2(pos[:, 2], r_xy))

    def plane_sat_index(self, idx):
        """Convert flat index to (plane, sat_in_plane)."""
        return idx // self.S, idx % self.S

    def flat_index(self, p, k):
        """Convert (plane, sat_in_plane) to flat index."""
        return p * self.S + k
