"""Two-body orbital mechanics for LEO satellite constellation.

Provides satellite position, ground track, visibility and slant-range
computations used by the HGAT simulation environment.
"""

from dataclasses import dataclass

import numpy as np

from config import (
    EARTH_RADIUS,
    LEO_ALTITUDE,
    LEO_INCLINATION,
    LEO_MIN_ELEVATION,
    LEO_PLANES,
    MU_EARTH,
    N_LEO,
)

EARTH_ROTATION_RATE = 7.2921e-5  # rad/s


@dataclass
class LEOSatellite:
    plane_id: int
    sat_id_in_plane: int
    raan: float  # right ascension of ascending node (rad)
    initial_phase: float  # true anomaly at t=0 (rad)


class OrbitalMechanics:
    """Circular-orbit LEO constellation model.

    Uses ECI (Earth-Centered Inertial) coordinates internally.
    Ground positions are rotated into ECI via Earth rotation for
    visibility / elevation calculations.
    """

    def __init__(
        self,
        n_leo=N_LEO,
        n_planes=LEO_PLANES,
        altitude=LEO_ALTITUDE,
        inclination=LEO_INCLINATION,
        earth_radius=EARTH_RADIUS,
        mu=MU_EARTH,
    ):
        self.n_leo = n_leo
        self.n_planes = n_planes
        self.sats_per_plane = n_leo // n_planes
        self.altitude = altitude
        self.inclination = np.radians(inclination)
        self.earth_radius = earth_radius
        self.mu = mu

        self.semi_major_axis = earth_radius + altitude
        self.period = 2.0 * np.pi * np.sqrt(self.semi_major_axis ** 3 / mu)
        self.mean_motion = 2.0 * np.pi / self.period  # rad/s

    def create_constellation(self, seed: int = 42) -> list[LEOSatellite]:
        rng = np.random.default_rng(seed)
        satellites: list[LEOSatellite] = []
        raan_spacing = 2.0 * np.pi / self.n_planes

        for plane in range(self.n_planes):
            raan = plane * raan_spacing
            phase_spacing = 2.0 * np.pi / self.sats_per_plane
            # Small random offset so Walker-like pattern isn't perfectly uniform
            phase_offset = rng.uniform(0, phase_spacing)
            for idx in range(self.sats_per_plane):
                satellites.append(
                    LEOSatellite(
                        plane_id=plane,
                        sat_id_in_plane=idx,
                        raan=raan,
                        initial_phase=phase_offset + idx * phase_spacing,
                    )
                )
        return satellites

    def satellite_position(self, sat: LEOSatellite, t: float) -> np.ndarray:
        """ECI position (x, y, z) in metres at time *t* seconds."""
        nu = sat.initial_phase + self.mean_motion * t  # true anomaly (circular)
        a = self.semi_major_axis

        # Position in perifocal (orbital plane) frame
        x_pf = a * np.cos(nu)
        y_pf = a * np.sin(nu)

        # Rotate: inclination around x-axis, then RAAN around z-axis
        cos_i = np.cos(self.inclination)
        sin_i = np.sin(self.inclination)
        cos_raan = np.cos(sat.raan)
        sin_raan = np.sin(sat.raan)

        x = cos_raan * x_pf - sin_raan * cos_i * y_pf
        y = sin_raan * x_pf + cos_raan * cos_i * y_pf
        z = sin_i * y_pf

        return np.array([x, y, z])

    def satellite_ground_track(
        self, sat: LEOSatellite, t: float
    ) -> tuple[float, float]:
        """Sub-satellite point (latitude, longitude) in degrees.

        Longitude accounts for Earth rotation so the result is in the
        ECEF (ground-fixed) frame.
        """
        pos = self.satellite_position(sat, t)
        r = np.linalg.norm(pos)
        lat = np.degrees(np.arcsin(pos[2] / r))
        lon_inertial = np.degrees(np.arctan2(pos[1], pos[0]))
        lon = (lon_inertial - np.degrees(EARTH_ROTATION_RATE * t)) % 360.0
        if lon > 180.0:
            lon -= 360.0
        return lat, lon

    def _ground_eci(
        self, lat_deg: float, lon_deg: float, t: float
    ) -> np.ndarray:
        """Convert ground (lat, lon) to ECI at time *t*."""
        lat = np.radians(lat_deg)
        lon_inertial = np.radians(lon_deg) + EARTH_ROTATION_RATE * t
        re = self.earth_radius
        clat = np.cos(lat)
        x = re * clat * np.cos(lon_inertial)
        y = re * clat * np.sin(lon_inertial)
        z = re * np.sin(lat)
        return np.array([x, y, z])

    def elevation_angle(
        self,
        sat: LEOSatellite,
        ground_lat: float,
        ground_lon: float,
        t: float,
    ) -> float:
        """Elevation angle (degrees) of *sat* seen from ground point."""
        sat_pos = self.satellite_position(sat, t)
        gnd_pos = self._ground_eci(ground_lat, ground_lon, t)
        diff = sat_pos - gnd_pos
        dist = np.linalg.norm(diff)
        # Angle between diff vector and local horizon plane at ground point
        # sin(elev) = dot(diff, gnd_pos_unit) / dist
        gnd_unit = gnd_pos / np.linalg.norm(gnd_pos)
        sin_elev = np.dot(diff, gnd_unit) / dist
        return np.degrees(np.arcsin(np.clip(sin_elev, -1.0, 1.0)))

    def is_visible(
        self,
        sat: LEOSatellite,
        ground_lat: float,
        ground_lon: float,
        t: float,
        min_elev: float = LEO_MIN_ELEVATION,
    ) -> bool:
        return self.elevation_angle(sat, ground_lat, ground_lon, t) >= min_elev

    def get_visible_sats(
        self,
        ground_lat: float,
        ground_lon: float,
        t: float,
        min_elev: float = LEO_MIN_ELEVATION,
    ) -> list[int]:
        return [
            i
            for i, sat in enumerate(self.satellites)
            if self.is_visible(sat, ground_lat, ground_lon, t, min_elev)
        ]

    def distance_to_ground(
        self,
        sat: LEOSatellite,
        ground_lat: float,
        ground_lon: float,
        t: float,
    ) -> float:
        """Slant range (metres) from ground point to satellite."""
        sat_pos = self.satellite_position(sat, t)
        gnd_pos = self._ground_eci(ground_lat, ground_lon, t)
        return float(np.linalg.norm(sat_pos - gnd_pos))

    def setup_constellation(self, seed: int = 42) -> None:
        """Create constellation and store internally."""
        self.satellites = self.create_constellation(seed)
