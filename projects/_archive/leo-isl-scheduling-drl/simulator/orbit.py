"""M1: OrbitPropagator — Keplerian two-body propagation for Walker Delta constellation.

Generates a Walker Delta constellation from orbital parameters and propagates
satellite positions using Keplerian two-body mechanics. Outputs ECI positions (km).

Uses simple Kepler equation solver (Newton's method) for near-circular orbits.
Sufficient for ISL scheduling simulation — SGP4 perturbations (J2, drag) are
small effects that don't change the scheduling problem structure.
"""

import numpy as np
from . import config


class OrbitPropagator:
    def __init__(self, n_planes=None, sats_per_plane=None, altitude=None,
                 inclination_deg=None, epoch=None):
        self.n_planes = n_planes or config.N_PLANES
        self.sats_per_plane = sats_per_plane or config.SATS_PER_PLANE
        self.n_sats = self.n_planes * self.sats_per_plane
        self.altitude = altitude or config.ALTITUDE
        self.inclination = np.radians(inclination_deg or config.INCLINATION_DEG)

        self.sma = config.RE + self.altitude  # semi-major axis (km)
        self.period = 2 * np.pi * np.sqrt(self.sma ** 3 / config.MU)  # s
        self.mean_motion = 2 * np.pi / self.period  # rad/s

        self._elements = self._build_constellation()

    def _build_constellation(self):
        """Store Keplerian elements for each satellite."""
        raan_step = 2 * np.pi / self.n_planes
        ma_step = 2 * np.pi / self.sats_per_plane
        ecc = 1e-4  # near-circular

        elements = []
        for p in range(self.n_planes):
            raan = p * raan_step
            for s in range(self.sats_per_plane):
                ma0 = s * ma_step
                elements.append((raan, ma0, self.inclination, ecc, 0.0))
                # (RAAN, mean_anomaly_0, inclination, eccentricity, arg_perigee)
        return elements

    def propagate(self, elapsed_seconds):
        """Propagate all satellites to given elapsed time(s).

        Args:
            elapsed_seconds: float or 1-D array of floats.

        Returns:
            (n_sats, 3) ECI positions in km, or (n_times, n_sats, 3).
        """
        scalar = np.isscalar(elapsed_seconds)
        times = [float(elapsed_seconds)] if scalar else np.asarray(elapsed_seconds, dtype=float)

        results = np.empty((len(times), self.n_sats, 3))
        n = self.mean_motion

        for ti, t in enumerate(times):
            for i, (raan, ma0, inc, ecc, argp) in enumerate(self._elements):
                ma = ma0 + n * t
                results[ti, i] = _kepler_to_eci(self.sma, ecc, inc, argp, raan, ma)

        return results[0] if scalar else results

    def eci_to_lla(self, positions_eci, elapsed_seconds):
        """ECI → (lat, lon, alt) in (rad, rad, km).

        Accounts for Earth rotation since epoch.
        """
        theta = config.OMEGA_EARTH * elapsed_seconds
        ct, st = np.cos(theta), np.sin(theta)
        x = positions_eci[:, 0] * ct + positions_eci[:, 1] * st
        y = -positions_eci[:, 0] * st + positions_eci[:, 1] * ct
        z = positions_eci[:, 2]

        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        lat = np.arcsin(np.clip(z / r, -1, 1))
        lon = np.arctan2(y, x)
        alt = r - config.RE
        return lat, lon, alt


def _solve_kepler(ma, ecc, tol=1e-12, max_iter=20):
    """Solve Kepler's equation E - e*sin(E) = M using Newton's method."""
    E = ma + ecc * np.sin(ma)  # initial guess (good for small e)
    for _ in range(max_iter):
        f = E - ecc * np.sin(E) - ma
        fp = 1 - ecc * np.cos(E)
        dE = f / fp
        E -= dE
        if abs(dE) < tol:
            break
    return E


def _kepler_to_eci(a, ecc, inc, argp, raan, ma):
    """Convert Keplerian elements to ECI position vector.

    Returns (x, y, z) in km.
    """
    E = _solve_kepler(ma, ecc)

    # True anomaly
    nu = 2 * np.arctan2(
        np.sqrt(1 + ecc) * np.sin(E / 2),
        np.sqrt(1 - ecc) * np.cos(E / 2),
    )

    # Distance from focus
    r = a * (1 - ecc * np.cos(E))

    # Position in orbital plane
    x_orb = r * np.cos(nu)
    y_orb = r * np.sin(nu)

    # Rotation matrices: orbital plane → ECI
    c_raan, s_raan = np.cos(raan), np.sin(raan)
    c_argp, s_argp = np.cos(argp), np.sin(argp)
    c_inc, s_inc = np.cos(inc), np.sin(inc)

    # Combined rotation: R_z(-RAAN) · R_x(-inc) · R_z(-argp)
    x = (c_raan * c_argp - s_raan * s_argp * c_inc) * x_orb + \
        (-c_raan * s_argp - s_raan * c_argp * c_inc) * y_orb
    y = (s_raan * c_argp + c_raan * s_argp * c_inc) * x_orb + \
        (-s_raan * s_argp + c_raan * c_argp * c_inc) * y_orb
    z = (s_argp * s_inc) * x_orb + (c_argp * s_inc) * y_orb

    return np.array([x, y, z])
