"""Gymnasium Env 模板 — 取自 leo-beam-hopping-gnn 项目。

最佳实践：
- 继承 gymnasium.Env，5-tuple 返回 (obs, reward, terminated, truncated, info)
- super().reset(seed=seed) 确保基类 RNG 一致
- observation_space / action_space 在 __init__ 中定义，方便 VecEnv 包装
- info dict 包含 reward 分解和关键指标，便于 TensorBoard 记录
- action masking 通过 info['action_mask'] 传递，不修改 space 定义
"""
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from .config import SimConfig


class SimEnv(gym.Env):
    """通用卫星通信 Gymnasium 环境。

    State:  (N, C) array — N 个实体各 C 个归一化特征
    Action: 离散索引（spaces.Discrete），与 GNN actor-critic 的 Categorical 策略匹配
            连续空间场景请改用 spaces.Box + 连续策略头（Gaussian policy）
    Reward: 由 RewardCalculator 计算，总奖励 + 分解
    Episode: T 步，terminated=True 表示 episode 自然结束
    """

    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig | None = None, seed: int | None = None):
        super().__init__()
        self.config = config or SimConfig()
        self.N = self.config.n_beams
        self.T = self.config.t_slots

        # --- CUSTOMIZE --- 根据问题定义 action/observation space
        # 离散动作空间：选择 N 个实体中的一个（与 Categorical 策略匹配）
        # 连续空间场景请改用 spaces.Box + 连续策略头（Gaussian policy）
        self.action_space = spaces.Discrete(self.N)
        # 示例：(N, 4) 归一化特征：需求/队列/信道增益/干扰
        obs_dim = 4  # --- CUSTOMIZE ---
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(self.N, obs_dim), dtype=np.float32
        )

        # 内部状态
        self._rng = np.random.default_rng(seed)
        self._seed = seed
        self.t = 0

        # --- CUSTOMIZE --- 初始化环境特有状态
        self.queues = np.zeros(self.N, dtype=np.float64)
        self.demands = np.zeros(self.N, dtype=np.float64)
        self._served = np.zeros(self.N, dtype=np.float64)

        # RewardCalculator 集成
        from .reward import RewardCalculator
        self.reward_calc = RewardCalculator(
            w_throughput=self.config.reward_alpha,
            w_fairness=self.config.reward_beta,
            w_penalty=self.config.reward_gamma,
            sinr_max_db=self.config.sinr_max_db,
        )

    def reset(self, seed: int | None = None, options: dict | None = None):
        # 必须调用 super().reset 让基类管理 np_random
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self.t = 0
        self.queues = np.zeros(self.N, dtype=np.float64)
        # --- CUSTOMIZE --- 重置其他状态
        self.demands = self._generate_demand()

        obs = self._get_obs()
        info = self._get_info()
        return obs, info

    def step(self, action: int):
        action = int(action)

        # --- CUSTOMIZE --- 核心仿真逻辑
        # 1. 根据 action 计算系统响应（调度、资源分配等）
        self._served = self._simulate_step(action)

        # 2. 计算奖励（使用 RewardCalculator）
        sinr_db = 10.0  # --- CUSTOMIZE: 替换为实际 SINR 计算 ---
        reward, reward_decomp = self.reward_calc.compute_reward(
            sinr_db=sinr_db, served=self._served, demanded=self.demands,
        )

        # 3. 更新环境状态
        self.queues = np.maximum(self.queues + self.demands - self._served, 0)
        self.demands = self._generate_demand()
        self.t += 1

        # 4. 终止条件
        terminated = self.t >= self.T
        truncated = False  # 仅在超时/外部截断时为 True

        obs = self._get_obs()
        info = self._get_info()
        # 丰富的诊断信息，便于训练监控
        info['reward_decomp'] = reward_decomp
        info['served'] = self._served
        info['step'] = self.t
        # Action mask：哪些 action 是合法的（可选）
        info['action_mask'] = np.ones(self.N, dtype=bool)  # --- CUSTOMIZE ---

        return obs, float(reward), terminated, truncated, info

    def _get_obs(self) -> np.ndarray:
        """构建归一化观测，映射到 [0, 1] 区间。"""
        d_max = self.config.demand_max_mbps
        q_max = self.config.demand_max_mbps * 2  # 队列上限一般 > 需求上限
        obs = np.stack([
            np.clip(self.demands / d_max, 0, 1),
            np.clip(self.queues / q_max, 0, 1),
            # --- CUSTOMIZE --- 加入信道、干扰等特征
            np.zeros(self.N),  # placeholder: channel_gain_norm
            np.zeros(self.N),  # placeholder: interference_norm
        ], axis=1)
        return obs.astype(np.float32)

    def _get_info(self) -> dict:
        """返回诊断信息，不包含奖励分解（step 中追加）。"""
        return {
            'demands': self.demands.copy(),
            'queues': self.queues.copy(),
        }

    def _generate_demand(self) -> np.ndarray:
        """生成流量需求。--- CUSTOMIZE --- 替换为实际流量模型。"""
        lo = self.config.demand_min_mbps
        hi = self.config.demand_max_mbps
        return self._rng.uniform(lo, hi, self.N)

    def _simulate_step(self, action: int) -> np.ndarray:
        """根据 action 执行一步仿真，返回各实体服务量。

        --- CUSTOMIZE --- 替换为核心物理层/调度逻辑
        """
        # 最简示例：选中实体获得服务，其余获得部分服务
        served = np.full(self.N, self.config.demand_min_mbps * 0.1, dtype=np.float64)
        served[action] = self.demands[action] * 0.8
        return served
