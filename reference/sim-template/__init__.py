"""sim-template — 卫星通信 GNN+DRL 仿真模板包。

统一导出核心组件，方便外部 import：
    from reference.sim_template import SimConfig, SimEnv, RewardCalculator, BaseActorCritic
"""

from .config import SimConfig
from .env import SimEnv
from .reward import RewardCalculator
from .model_gnn import BaseActorCritic

__all__ = [
    "SimConfig",
    "SimEnv",
    "RewardCalculator",
    "BaseActorCritic",
]
