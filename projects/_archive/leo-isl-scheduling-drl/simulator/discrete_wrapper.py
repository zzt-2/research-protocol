"""Discrete action wrapper: converts {AS-IS, FORCE-ON, FORCE-OFF} to continuous scores."""

import numpy as np
import torch
from torch_geometric.data import Data


def obs_to_data(obs):
    """Convert obs dict to PyG Data."""
    node_feat = torch.tensor(obs["node_features"], dtype=torch.float32)
    edge_feat = torch.tensor(obs["edge_features"], dtype=torch.float32)
    if len(obs["candidate_edges"]) > 0:
        edge_index = torch.tensor(
            [[i, j] for i, j, _ in obs["candidate_edges"]], dtype=torch.long
        ).t().contiguous()
    else:
        edge_index = torch.zeros((2, 0), dtype=torch.long)
    return Data(x=node_feat, edge_index=edge_index, edge_attr=edge_feat)


class DiscreteActionWrapper:
    """Converts discrete {AS-IS, FORCE-ON, FORCE-OFF} actions to continuous scores.

    Wraps env.step(scores) interface:
    - base_scores from pretrained model's backbone (sigmoid output)
    - AS-IS(0):    keep base_scores[idx]
    - FORCE-ON(1): scores[idx] = 1.0
    - FORCE-OFF(2): scores[idx] = 0.0
    Then env.step(final_scores) -> LCT constraint applies automatically.
    """

    def __init__(self, env, model, device='cpu'):
        """
        Args:
            env: ISLEnvironment instance
            model: DiscreteRLGNN or SupervisedGNN with get_base_scores or predict_scores
            device: torch device
        """
        self.env = env
        self.model = model
        self.device = device

    def _get_base_scores(self, obs):
        data = obs_to_data(obs).to(self.device)
        if hasattr(self.model, 'get_base_scores'):
            return self.model.get_base_scores(data)
        elif hasattr(self.model, 'predict_scores'):
            return self.model.predict_scores(data)
        else:
            raise AttributeError(
                "Model must have get_base_scores or predict_scores method"
            )

    def step(self, discrete_actions):
        """Convert discrete actions to scores, call env.step().

        Args:
            discrete_actions: (n_candidates,) int array in {0, 1, 2}

        Returns:
            Same as env.step(): obs, reward, terminated, truncated, info
        """
        discrete_actions = np.asarray(discrete_actions)

        # Get base scores from pretrained model
        obs = self.env._build_obs()
        base_scores = self._get_base_scores(obs)

        # Apply discrete overrides
        final_scores = base_scores.copy()
        if len(discrete_actions) > 0:
            final_scores[discrete_actions == 1] = 1.0  # FORCE-ON
            final_scores[discrete_actions == 2] = 0.0  # FORCE-OFF
            # AS-IS (0): no change

        return self.env.step(final_scores)

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def __getattr__(self, name):
        if name in ('env', 'model', 'device'):
            raise AttributeError(name)
        return getattr(self.env, name)
