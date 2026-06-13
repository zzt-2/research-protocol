"""参数重导出 — 参数真相源在 params.py"""
import os
import numpy as np
from params import SimulationConfig

_OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_CFG = SimulationConfig()

R_SYM = _CFG.system.R_SYM
T_S = _CFG.system.T_S
F_CARRIER = _CFG.system.F_CARRIER
LASER_LW = _CFG.system.LASER_LW

TURB = _CFG.get_turb_dict()
BLOCK = _CFG.experiment.BLOCK

DOPPLER_HIGH = _CFG.doppler.DOPPLER_HIGH
DOPPLER_LOW  = _CFG.doppler.DOPPLER_LOW
F_RESIDUAL   = _CFG.doppler.F_RESIDUAL

FIXED_CFG = _CFG.get_fixed_cfg()
FIXED_CFG_OPTIMAL = _CFG.get_fixed_cfg_optimal()

GAMMA_BAR_DEFAULT = _CFG.experiment.GAMMA_BAR_DEFAULT

DEF_B_BPS = _CFG.bps.B_default
DEF_NW_BPS = _CFG.bps.Nw_default

SIGMA2_LASER = _CFG.kf.sigma2_laser
Q_TURB_PARAMS = _CFG.get_q_turb_params()

PILOT_PATTERN = np.array([
    ( 1 + 1j) / np.sqrt(2),
    ( 1 - 1j) / np.sqrt(2),
    (-1 + 1j) / np.sqrt(2),
    (-1 - 1j) / np.sqrt(2),
])
