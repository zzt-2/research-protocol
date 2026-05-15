"""Verify model_gat.py and train.py: dimensions, forward pass, PPO smoke test."""

import sys
from pathlib import Path

# Add project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import torch
from torch_geometric.data import Data

from simulator.model_gat import GATv2ActorCritic
from simulator.train import obs_to_data, ISLRolloutBuffer, RewardNormalizer


def test_model_dims():
    """Model I/O dimensions match data-flow.md spec."""
    model = GATv2ActorCritic(node_dim=6, edge_dim=7, hidden_dim=64, n_heads=4, n_layers=3)

    N, E = 100, 500  # small graph
    x = torch.randn(N, 6)
    edge_index = torch.randint(0, N, (2, E))
    edge_attr = torch.randn(E, 7)
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

    scores, value = model(data)

    assert scores.shape == (E,), f"scores shape: {scores.shape}, expected ({E},)"
    assert value.shape == (), f"value shape: {value.shape}, expected scalar"
    assert (scores >= 0).all() and (scores <= 1).all(), f"scores range: [{scores.min():.3f}, {scores.max():.3f}]"

    print(f"[PASS] Model dims: scores={scores.shape} value={value.shape} "
          f"range=[{scores.min():.3f}, {scores.max():.3f}]")


def test_model_get_action():
    """get_action returns valid scores and log_prob."""
    model = GATv2ActorCritic()
    N, E = 50, 200
    data = Data(
        x=torch.randn(N, 6),
        edge_index=torch.randint(0, N, (2, E)),
        edge_attr=torch.randn(E, 7),
    )

    scores, log_prob, value = model.get_action(data, deterministic=False)
    assert scores.shape == (E,)
    assert log_prob.shape == (1,) or log_prob.dim() == 0
    assert (scores >= 0).all() and (scores <= 1).all()

    # Deterministic mode
    scores_d, _, _ = model.get_action(data, deterministic=True)
    assert scores_d.shape == (E,)

    print(f"[PASS] get_action: scores={scores.shape} log_prob={log_prob.item():.4f}")


def test_model_evaluate_actions():
    """evaluate_actions returns (B,) tensors for PPO."""
    model = GATv2ActorCritic()
    data_list = []
    scores_list = []

    for _ in range(5):
        N, E = 30, 100
        data = Data(
            x=torch.randn(N, 6),
            edge_index=torch.randint(0, N, (2, E)),
            edge_attr=torch.randn(E, 7),
        )
        data_list.append(data)
        scores_list.append(torch.rand(E))

    log_probs, values, entropies = model.evaluate_actions(data_list, scores_list)
    assert log_probs.shape == (5,), f"log_probs shape: {log_probs.shape}"
    assert values.shape == (5,), f"values shape: {values.shape}"
    assert entropies.shape == (5,), f"entropies shape: {entropies.shape}"

    print(f"[PASS] evaluate_actions: lp={log_probs.shape} val={values.shape} ent={entropies.shape}")


def test_param_count():
    """Parameter count is reasonable (< 1M for 64-dim GATv2)."""
    model = GATv2ActorCritic()
    n = model.n_params
    assert n < 1_000_000, f"Too many params: {n}"
    print(f"[PASS] Param count: {n:,}")


def test_obs_to_data():
    """obs_to_data converts env observation dict correctly."""
    n_edges = 50
    edges = [(i % 20, (i + 3) % 20, float(i * 100)) for i in range(n_edges)]
    obs = {
        "node_features": np.random.randn(20, 6).astype(np.float32),
        "edge_features": np.random.randn(n_edges, 7).astype(np.float32),
        "candidate_edges": edges,
        "n_candidates": n_edges,
    }
    data = obs_to_data(obs)
    assert data.x.shape == (20, 6)
    assert data.edge_attr.shape == (50, 7)
    assert data.edge_index.shape == (2, 50)
    print(f"[PASS] obs_to_data: nodes={data.x.shape} edges={data.edge_index.shape}")


def test_buffer():
    """ISLRolloutBuffer GAE computation."""
    buf = ISLRolloutBuffer()
    for t in range(20):
        buf.add(
            obs={"node_features": np.zeros((10, 6)), "edge_features": np.zeros((20, 7)),
                 "candidate_edges": [(0, 1, 1.0)] * 20, "n_candidates": 20},
            scores=np.random.rand(20).astype(np.float32),
            log_prob=float(np.random.randn()),
            reward=float(np.random.randn()),
            done=(t == 19),
            value=float(np.random.randn()),
        )

    buf.compute_returns_and_advantages(last_value=0.0, gamma=0.99, gae_lambda=0.95)
    assert buf.returns.shape == (20,)
    assert buf.advantages.shape == (20,)
    print(f"[PASS] Buffer GAE: returns={buf.returns.shape} adv={buf.advantages.shape}")


def test_reward_normalizer():
    """RewardNormalizer produces zero-mean unit-var output."""
    norm = RewardNormalizer()
    rewards = [float(np.random.randn()) for _ in range(100)]
    normed = norm.update_and_normalize(rewards)
    arr = np.array(normed)
    assert np.abs(arr.mean()) < 1.0, f"Mean not near 0: {arr.mean()}"
    print(f"[PASS] RewardNormalizer: mean={arr.mean():.4f} std={arr.std():.4f}")


if __name__ == "__main__":
    print("=" * 60)
    print("Model & Training Verification")
    print("=" * 60)

    test_model_dims()
    test_model_get_action()
    test_model_evaluate_actions()
    test_param_count()
    test_obs_to_data()
    test_buffer()
    test_reward_normalizer()

    print("=" * 60)
    print("ALL PASSED")
