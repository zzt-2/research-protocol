"""Zero-shot generalization test: evaluate models trained on 10 IoTD at 10/20/30/50 IoTD."""

import json
from pathlib import Path

import numpy as np
import torch

from config import SimConfig
from env import SatelliteDAGEnv
from models_hgat import HGATActorCritic
from models_homo import GCNActorCritic, GraphSAGEActorCritic, MLPActorCritic

MODEL_CLS = {
    "hgat": HGATActorCritic,
    "graphsage": GraphSAGEActorCritic,
    "gcn": GCNActorCritic,
    "mlp": MLPActorCritic,
}

CHECKPOINT_DIRS = {
    "hgat": "results_final",
    "graphsage": "results_v2",
    "gcn": "results_v2",
    "mlp": "results_v2",
}

TRAIN_CONFIG = SimConfig()  # 10 IoTD
SCALES = [10, 20, 30, 50]
N_EVAL_EPS = 30
SEED = 99  # fixed eval seed


def load_model(model_name: str, seed: int, device: str):
    """Load best checkpoint for a model."""
    cls = MODEL_CLS[model_name]
    train_n_actions = TRAIN_CONFIG.total_tasks * TRAIN_CONFIG.n_nodes
    model = cls(TRAIN_CONFIG, train_n_actions).to(device)
    ckpt_dir = Path(CHECKPOINT_DIRS[model_name])
    ckpt_path = ckpt_dir / f"{model_name}_seed{seed}_best.pt"
    if not ckpt_path.exists():
        return None
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    model.eval()
    return model


def evaluate(model, env: SatelliteDAGEnv, config: SimConfig, n_eps: int) -> list[float]:
    """Run evaluation episodes, return list of rewards."""
    # Update node type sizes for homo models
    model._node_type_sizes = {
        "task": config.total_tasks,
        "iotd": config.n_iotd,
        "uav": config.n_uav,
        "leo": config.n_leo,
        "cs": 1,
    }

    rewards = []
    for ep in range(n_eps):
        obs, info = env.reset(seed=SEED * 1000 + ep)
        done, ep_reward = False, 0.0
        while not done:
            mask = info["action_mask"]
            action, _, _, _ = model.get_action(obs, mask)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_reward += reward
        rewards.append(ep_reward)
    return rewards


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    results = {}

    for model_name in ["hgat", "graphsage", "gcn", "mlp"]:
        print(f"\n=== {model_name.upper()} ===")
        for seed in [42, 123, 456]:
            model = load_model(model_name, seed, device)
            if model is None:
                print(f"  seed={seed}: no checkpoint, skip")
                continue

            for n_iotd in SCALES:
                cfg = SimConfig(n_iotd=n_iotd)
                env = SatelliteDAGEnv(cfg, seed=SEED)
                rewards = evaluate(model, env, cfg, N_EVAL_EPS)
                key = f"{model_name}_seed{seed}"
                if key not in results:
                    results[key] = {}
                results[key][n_iotd] = {
                    "mean": float(np.mean(rewards)),
                    "std": float(np.std(rewards)),
                    "best": float(max(rewards)),
                    "worst": float(min(rewards)),
                }
                print(f"  seed={seed} iotd={n_iotd:2d}: mean={np.mean(rewards):8.2f} "
                      f"±{np.std(rewards):7.2f}  best={max(rewards):8.2f}")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY: mean reward (avg over seeds)")
    print(f"{'Model':<12} " + " ".join(f"IoTD={s:>2d}" for s in SCALES))
    print("-" * 80)

    for model_name in ["hgat", "graphsage", "gcn", "mlp"]:
        row = f"{model_name:<12} "
        for n_iotd in SCALES:
            vals = []
            for seed in [42, 123, 456]:
                key = f"{model_name}_seed{seed}"
                if key in results and n_iotd in results[key]:
                    vals.append(results[key][n_iotd]["mean"])
            if vals:
                row += f"{np.mean(vals):8.1f} "
            else:
                row += f"{'N/A':>8s} "
        print(row)

    # Save
    with open("results_generalize.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to results_generalize.json")


if __name__ == "__main__":
    main()
