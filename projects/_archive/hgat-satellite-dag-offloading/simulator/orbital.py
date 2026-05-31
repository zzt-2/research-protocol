"""Two-body orbital mechanics for LEO satellite constellation."""

from dataclasses import dataclass

import numpy as np

from config import SimConfig

EARTH_ROTATION_RATE = 7.2921e-5  # rad/s


@dataclass
class LEOSatellite:
    plane_id: int
    sat_id_in_plane: int
    raan: float  # right ascension of ascending node (rad)
    initial_phase: float  # true anomaly at t=0 (rad)


class OrbitalMechanics:
    """Circular-orbit LEO constellation model (ECI coordinates)."""

    def __init__(self, config: SimConfig):
        self.cfg = config
        self.n_leo = config.n_leo
        self.n_planes = config.leo_planes
        self.sats_per_plane = config.sats_per_plane
        self.inclination = np.radians(config.leo_inclination)
        self.earth_radius = config.earth_radius
        self.semi_major_axis = config.semi_major_axis
        self.period = config.orbital_period
        self.mean_motion = config.mean_motion
        self.satellites: list[LEOSatellite] = []

    def create_constellation(self, seed: int = 42) -> list[LEOSatellite]:
        rng = np.random.default_rng(seed)
        satellites: list[LEOSatellite] = []
        raan_spacing = 2.0 * np.pi / self.n_planes

        for plane in range(self.n_planes):
            raan = plane * raan_spacing
            phase_spacing = 2.0 * np.pi / self.sats_per_plane
            phase_offset = rng.uniform(0, phase_spacing)
            for idx in range(self.sats_per_plane):
                satellites.append(LEOSatellite(
                    plane_id=plane, sat_id_in_plane=idx, raan=raan,
                    initial_phase=phase_offset + idx * phase_spacing,
                ))
        return satellites

    def setup_constellation(self, seed: int = 42) -> None:
        self.satellites = self.create_constellation(seed)

    def satellite_position(self, sat: LEOSatellite, t: float) -> np.ndarray:
        """ECI position (x, y, z) in metres at time *t* seconds."""
        nu = sat.initial_phase + self.mean_motion * t
        a = self.semi_major_axis
        x_pf = a * np.cos(nu)
        y_pf = a * np.sin(nu)
        cos_i, sin_i = np.cos(self.inclination), np.sin(self.inclination)
        cos_raan, sin_raan = np.cos(sat.raan), np.sin(sat.raan)
        x = cos_raan * x_pf - sin_raan * cos_i * y_pf
        y = sin_raan * x_pf + cos_raan * cos_i * y_pf
        z = sin_i * y_pf
        return np.array([x, y, z])

    def satellite_ground_track(self, sat: LEOSatellite, t: float) -> tuple[float, float]:
        """Sub-satellite point (lat, lon) in degrees (ECEF frame)."""
        pos = self.satellite_position(sat, t)
        r = np.linalg.norm(pos)
        lat = np.degrees(np.arcsin(pos[2] / r))
        lon_inertial = np.degrees(np.arctan2(pos[1], pos[0]))
        lon = (lon_inertial - np.degrees(EARTH_ROTATION_RATE * t)) % 360.0
        if lon > 180.0:
            lon -= 360.0
        return lat, lon

    def _ground_eci(self, lat_deg: float, lon_deg: float, t: float) -> np.ndarray:
        lat = np.radians(lat_deg)
        lon_inertial = np.radians(lon_deg) + EARTH_ROTATION_RATE * t
        re = self.earth_radius
        clat = np.cos(lat)
        return np.array([re * clat * np.cos(lon_inertial),
                         re * clat * np.sin(lon_inertial),
                         re * np.sin(lat)])

    def elevation_angle(self, sat: LEOSatellite, ground_lat: float,
                        ground_lon: float, t: float) -> float:
        sat_pos = self.satellite_position(sat, t)
        gnd_pos = self._ground_eci(ground_lat, ground_lon, t)
        diff = sat_pos - gnd_pos
        dist = np.linalg.norm(diff)
        gnd_unit = gnd_pos / np.linalg.norm(gnd_pos)
        sin_elev = np.dot(diff, gnd_unit) / dist
        return np.degrees(np.arcsin(np.clip(sin_elev, -1.0, 1.0)))

    def is_visible(self, sat: LEOSatellite, ground_lat: float,
                   ground_lon: float, t: float) -> bool:
        return self.elevation_angle(sat, ground_lat, ground_lon, t) >= self.cfg.leo_min_elevation

    def get_visible_sats(self, ground_lat: float, ground_lon: float,
                         t: float) -> list[int]:
        return [i for i, sat in enumerate(self.satellites)
                if self.is_visible(sat, ground_lat, ground_lon, t)]

    def distance_to_ground(self, sat: LEOSatellite, ground_lat: float,
                           ground_lon: float, t: float) -> float:
        sat_pos = self.satellite_position(sat, t)
        gnd_pos = self._ground_eci(ground_lat, ground_lon, t)
        return float(np.linalg.norm(sat_pos - gnd_pos))
