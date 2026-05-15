"""M4: TrafficGenerator — GHS-POP ground stations → flow demands.

Generates non-uniform traffic based on population-weighted ground station
distribution. Uses gravity model for inter-GS demand with Poisson noise.

Verification: land traffic >> ocean traffic (all GS on land by construction).
"""

import numpy as np
from . import config


# Major population centers (lat_deg, lon_deg, relative_weight)
# Covers all continents, weighted by approximate metro population
_POPULATION_CENTERS = [
    # East Asia
    (35.7, 139.7, 37.0), (31.2, 121.5, 28.0), (39.9, 116.4, 22.0),
    (37.6, 127.0, 10.0), (34.7, 113.6, 8.0), (30.6, 104.1, 16.0),
    # South/SE Asia
    (19.1, 72.9, 21.0), (28.6, 77.2, 32.0), (13.8, 100.5, 10.0),
    (1.3, 103.8, 6.0), (-6.2, 106.8, 10.0),
    # Europe
    (51.5, -0.1, 14.0), (48.9, 2.4, 12.0), (52.5, 13.4, 4.0),
    (41.9, 12.5, 4.0), (40.4, -3.7, 6.0), (55.8, 37.6, 12.0),
    # North America
    (40.7, -74.0, 20.0), (34.1, -118.2, 15.0), (41.9, -87.6, 9.0),
    (29.8, -95.4, 7.0), (19.4, -99.1, 21.0), (45.5, -73.6, 4.0),
    # South America
    (-23.6, -46.6, 22.0), (-34.6, -58.4, 15.0), (-12.0, -77.0, 10.0),
    # Middle East / Africa
    (30.0, 31.2, 20.0), (25.2, 55.3, 5.0), (-1.3, 36.8, 5.0),
    (6.5, 3.4, 15.0), (-26.2, 28.0, 6.0),
    # Oceania
    (-33.9, 151.2, 5.0), (-37.8, 145.0, 5.0),
]


class TrafficGenerator:
    def __init__(self, n_gs=None, seed=42):
        self.n_gs = n_gs or config.N_GS
        self.rng = np.random.default_rng(seed)
        self.min_elev = np.radians(config.MIN_ELEVATION_DEG)

        self.gs_lat, self.gs_lon, self.gs_pop = self._generate_gs()
        # Pre-compute GS positions in ECEF (km) for visibility check
        self.gs_ecef = self._lla_to_ecef(
            np.radians(self.gs_lat), np.radians(self.gs_lon)
        )

        # Pre-compute gravity model demand matrix (normalized)
        self._demand_scale = self._build_gravity_matrix()

    def _generate_gs(self):
        """Sample GS positions from population centers with jitter."""
        centers = np.array(_POPULATION_CENTERS)
        lats_c, lons_c, weights = centers[:, 0], centers[:, 1], centers[:, 2]
        probs = weights / weights.sum()

        indices = self.rng.choice(len(centers), size=self.n_gs, p=probs)
        lat = lats_c[indices] + self.rng.normal(0, 2.0, self.n_gs)
        lon = lons_c[indices] + self.rng.normal(0, 2.0, self.n_gs)
        pop = weights[indices]
        return lat, lon, pop

    def _build_gravity_matrix(self):
        """Gravity model: demand ∝ sqrt(pop_i · pop_j) / distance_ij^0.5."""
        n = self.n_gs
        pop_sqrt = np.sqrt(self.gs_pop)

        # Angular distance on sphere
        lat_r, lon_r = np.radians(self.gs_lat), np.radians(self.gs_lon)
        dlat = lat_r[:, None] - lat_r[None, :]
        dlon = lon_r[:, None] - lon_r[None, :]
        a = np.sin(dlat / 2) ** 2 + np.cos(lat_r[:, None]) * np.cos(lat_r[None, :]) * np.sin(dlon / 2) ** 2
        ang_dist = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
        dist_km = config.RE * ang_dist
        dist_km = np.maximum(dist_km, 1.0)

        demand = pop_sqrt[:, None] * pop_sqrt[None, :] / np.sqrt(dist_km)
        np.fill_diagonal(demand, 0)
        demand /= demand.max()
        return demand

    @staticmethod
    def _lla_to_ecef(lat, lon):
        """Lat/lon (rad) → ECEF (km), spherical Earth."""
        r = config.RE
        x = r * np.cos(lat) * np.cos(lon)
        y = r * np.cos(lat) * np.sin(lon)
        z = r * np.sin(lat)
        return np.stack([x, y, z], axis=-1)

    def find_visible_sats(self, sat_lat, sat_lon, sat_alt):
        """Find visible satellites for each GS (elevation > min_elev).

        Args:
            sat_lat, sat_lon: (n_sats,) in radians.
            sat_alt: (n_sats,) altitude in km.

        Returns:
            gs_to_sat: (n_gs,) int array, index of best visible satellite (-1 if none).
        """
        n_sats = len(sat_lat)
        gs_to_sat = np.full(self.n_gs, -1, dtype=int)
        best_elev = np.full(self.n_gs, -np.inf)

        sat_ecef = self._lla_to_ecef(sat_lat, sat_lon) * ((config.RE + sat_alt) / config.RE)[:, None]

        for g in range(self.n_gs):
            gs = self.gs_ecef[g]
            for s in range(n_sats):
                sat = sat_ecef[s]
                d = sat - gs
                dist = np.linalg.norm(d)
                gs_norm = np.linalg.norm(gs)
                sin_elev = (np.dot(gs, d)) / (gs_norm * dist)
                # sin_elev > 0 means satellite is above horizon
                elev = np.arcsin(np.clip(sin_elev, -1, 1))
                if elev > best_elev[g]:
                    best_elev[g] = elev
                    gs_to_sat[g] = s

        gs_to_sat[best_elev < self.min_elev] = -1
        return gs_to_sat

    def generate(self, sat_lat, sat_lon, sat_alt, base_demand_gbps=10.0):
        """Generate flow demands between satellite pairs.

        Args:
            sat_lat, sat_lon: (n_sats,) radians.
            sat_alt: (n_sats,) km.
            base_demand_gbps: scale factor for total demand.

        Returns:
            flows: list of (src_sat, dst_sat, demand_gbps) tuples.
        """
        gs_to_sat = self.find_visible_sats(sat_lat, sat_lon, sat_alt)

        # Map GS demands to satellite pairs
        sat_demand = {}
        for g1 in range(self.n_gs):
            s1 = gs_to_sat[g1]
            if s1 < 0:
                continue
            for g2 in range(g1 + 1, self.n_gs):
                s2 = gs_to_sat[g2]
                if s2 < 0 or s1 == s2:
                    continue
                key = (min(s1, s2), max(s1, s2))
                d = self._demand_scale[g1, g2] * base_demand_gbps
                # Add Poisson noise (multiplicative)
                d *= self.rng.poisson(1.0) + self.rng.random()
                sat_demand[key] = sat_demand.get(key, 0) + d

        flows = [(s, d, dem) for (s, d), dem in sat_demand.items()]
        return flows

    def get_gs_positions(self):
        """Return GS (lat_deg, lon_deg, population_weight)."""
        return self.gs_lat.copy(), self.gs_lon.copy(), self.gs_pop.copy()
