"""M1: Orbital mechanics — Walker-delta constellation, visibility, elevation."""

import numpy as np
from numpy.typing import NDArray

MU_EARTH = 3.986004418e5   # km³/s²
EARTH_RADIUS = 6371.0      # km
OMEGA_EARTH = 7.2921159e-5 # rad/s


class WalkerConstellation:
    """Walker-delta LEO constellation with circular orbits.

    Precomputes ECEF positions for the full simulation. Uses a reduced
    satellite count (NUM_PLANES × SATS_PER_PLANE) to keep simulation
    tractable while maintaining realistic coverage over the service area.
    """

    def __init__(
        self,
        num_planes: int = 6,
        sats_per_plane: int = 11,
        altitude_km: float = 550.0,
        inclination_deg: float = 53.0,
        duration_s: float = 7200.0,
        dt_s: float = 10.0,
    ):
        self.num_planes = num_planes
        self.sats_per_plane = sats_per_plane
        self.num_sats = num_planes * sats_per_plane
        self.altitude = altitude_km
        self.inclination = np.radians(inclination_deg)
        self.orbit_radius = EARTH_RADIUS + altitude_km
        self.period = 2.0 * np.pi * np.sqrt(self.orbit_radius ** 3 / MU_EARTH)
        self.mean_motion = 2.0 * np.pi / self.period

        self.num_steps = int(duration_s / dt_s) + 1
        self.dt = dt_s

        self.raan = np.zeros(self.num_sats)
        self.init_anomaly = np.zeros(self.num_sats)
        for p in range(num_planes):
            for s in range(sats_per_plane):
                idx = p * sats_per_plane + s
                self.raan[idx] = 2.0 * np.pi * p / num_planes
                phase = 2.0 * np.pi * s / sats_per_plane
                phase_offset = 2.0 * np.pi * p / self.num_sats  # F=1 Walker delta
                self.init_anomaly[idx] = phase + phase_offset

        self.positions = self._precompute_positions()

    def _sat_eci(self, sat_idx: int, t: float) -> NDArray:
        r = self.orbit_radius
        nu = self.init_anomaly[sat_idx] + self.mean_motion * t
        Omega = self.raan[sat_idx]
        inc = self.inclination
        cn, sn = np.cos(nu), np.sin(nu)
        cO, sO = np.cos(Omega), np.sin(Omega)
        ci = np.cos(inc)
        x = r * (cO * cn - sO * sn * ci)
        y = r * (sO * cn + cO * sn * ci)
        z = r * sn * np.sin(inc)
        return np.array([x, y, z])

    def _eci_to_ecef(self, eci: NDArray, t: float) -> NDArray:
        theta = OMEGA_EARTH * t
        ct, st = np.cos(theta), np.sin(theta)
        return np.array([eci[0] * ct + eci[1] * st,
                         -eci[0] * st + eci[1] * ct,
                         eci[2]])

    def _precompute_positions(self) -> NDArray:
        """Shape: (num_steps, num_sats, 3) ECEF positions. Vectorized."""
        times = np.arange(self.num_steps) * self.dt  # (T,)
        nu = self.init_anomaly[np.newaxis, :] + self.mean_motion * times[:, np.newaxis]  # (T, N)
        cn, sn = np.cos(nu), np.sin(nu)
        cO, sO = np.cos(self.raan)[np.newaxis, :], np.sin(self.raan)[np.newaxis, :]
        ci = np.cos(self.inclination)

        r = self.orbit_radius
        x_eci = r * (cO * cn - sO * sn * ci)
        y_eci = r * (sO * cn + cO * sn * ci)
        z_eci = r * sn * np.sin(self.inclination)

        # ECI → ECEF rotation
        theta = OMEGA_EARTH * times  # (T,)
        ct, st = np.cos(theta)[:, np.newaxis], np.sin(theta)[:, np.newaxis]
        x_ecef = x_eci * ct + y_eci * st
        y_ecef = -x_eci * st + y_eci * ct
        z_ecef = z_eci

        return np.stack([x_ecef, y_ecef, z_ecef], axis=-1)  # (T, N, 3)

    def get_positions(self, step: int) -> NDArray:
        """ECEF positions at step. Shape: (num_sats, 3)."""
        return self.positions[step]


def geodetic_to_ecef(lat_deg: float, lon_deg: float, alt_km: float = 0.0) -> NDArray:
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)
    r = EARTH_RADIUS + alt_km
    return np.array([r * np.cos(lat) * np.cos(lon),
                     r * np.cos(lat) * np.sin(lon),
                     r * np.sin(lat)])


def compute_elevation(sat_pos: NDArray, ue_pos: NDArray) -> float:
    """Elevation angle (degrees) from UE to satellite."""
    d = sat_pos - ue_pos
    dist = np.linalg.norm(d)
    if dist < 1e-6:
        return 90.0
    sin_elev = np.dot(d / dist, ue_pos / np.linalg.norm(ue_pos))
    return np.degrees(np.arcsin(np.clip(sin_elev, -1.0, 1.0)))


def compute_elevation_batch(sat_positions: NDArray, ue_pos: NDArray) -> NDArray:
    """Elevation angles for all satellites. Shape: (num_sats,)."""
    d = sat_positions - ue_pos[np.newaxis, :]
    dist = np.linalg.norm(d, axis=1, keepdims=True)
    dist = np.maximum(dist, 1e-6)
    d_hat = d / dist
    n_hat = ue_pos / np.linalg.norm(ue_pos)
    sin_elev = (d_hat @ n_hat).squeeze()
    return np.degrees(np.arcsin(np.clip(sin_elev, -1.0, 1.0)))


def compute_visibility(
    sat_positions: NDArray, ue_pos: NDArray, min_elev_deg: float = 20.0
) -> NDArray:
    """Boolean mask: True for satellites above min_elev."""
    elev = compute_elevation_batch(sat_positions, ue_pos)
    return elev >= min_elev_deg


def generate_ue_positions(
    num_ues: int,
    center_lat_deg: float = 40.0,
    center_lon_deg: float = 116.0,
    spread_deg: float = 3.0,
    seed: int = 42,
) -> NDArray:
    """Random ground UE positions (ECEF). Shape: (num_ues, 3)."""
    rng = np.random.default_rng(seed)
    lats = center_lat_deg + rng.uniform(-spread_deg, spread_deg, num_ues)
    lons = center_lon_deg + rng.uniform(-spread_deg, spread_deg, num_ues)
    return np.array([geodetic_to_ecef(lat, lon) for lat, lon in zip(lats, lons)])
