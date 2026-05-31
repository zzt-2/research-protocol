"""LEO Beam Hopping Simulator — GW Step 7 Part A."""
from .config import SimConfig
from .antenna import gain_at_angle, compute_gain_matrix
from .channel import free_space_path_loss_db, compute_sinr, compute_interference_graph
from .traffic import TrafficGenerator
from .env import BHEnv
