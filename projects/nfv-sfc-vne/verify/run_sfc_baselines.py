"""SFC baseline training script.

Runs RL baseline solvers (pg_mlp, ppo_dual_gat+, ppo_dual_gcn) under
SFC constraint environment and collects metrics for baseline_report.md.

Usage:
    cd projects/nfv-sfc-vne
    python verify/run_sfc_baselines.py --solver sfc_pg_mlp --epochs 3
    python verify/run_sfc_baselines.py --solver sfc_ppo_dual_gat+ --epochs 5
"""
import sys
import os
import time
import argparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

import numpy as np
from omegaconf import OmegaConf, open_dict

from virne.network import Generator
from virne.core import Controller, Recorder, Counter
from virne.core.logger import Logger
from virne.core.environment import SolutionStepEnvironment
from virne.solver.base_solver import SolverRegistry
from virne.utils.config import add_simulation_into_config

# Register SFC solvers
from virne.solver.learning.sfc_solver import sfc_baselines  # noqa: F401


def build_config(num_v_nets=2000, seed=0, solver_name='sfc_pg_mlp',
                 num_epochs=30, use_cuda=True, gpu_id=0):
    """Build merged Virne config for SFC training."""
    settings_dir = os.path.join(VIRNE_ROOT, 'settings')
    config = OmegaConf.load(os.path.join(settings_dir, 'main.yaml'))
    learning_config = OmegaConf.load(os.path.join(settings_dir, 'learning.yaml'))
    v_sim_config = OmegaConf.load(os.path.join(settings_dir, 'v_sim_setting', 'default.yaml'))
    p_net_config = OmegaConf.load(os.path.join(settings_dir, 'p_net_setting', 'default.yaml'))
    config = OmegaConf.merge(config, learning_config,
                             {'v_sim_setting': v_sim_config},
                             {'p_net_setting': p_net_config})

    with open_dict(config):
        config.solver.solver_name = solver_name
        config.solver.node_ranking_method = 'order'
        config.solver.allow_revocable = False
        config.solver.allow_rejection = False
        config.v_sim_setting.num_v_nets = num_v_nets
        config.training.num_train_epochs = num_epochs
        config.training.use_cuda = use_cuda
        config.training.gpu_id = gpu_id
        config.experiment.run_id = f'sfc_{solver_name}'
        config.experiment.seed = seed
        config.logger.backends = ['console']
        config.logger.level = 'INFO'
        config.logger.verbose = 1
        config.rl.reward_calculator.name = 'fixed_intermediate'
        config.rl.reward_calculator.intermediate_reward = 0.1
        config.rl.if_use_negative_sample = False
        config.rl.if_use_baseline_solver = False
        # SFC config
        config.sfc = {
            'sfc_ratio': 0.6,
            'num_vnf_types': 5,
            'seed': 42,
        }

    add_simulation_into_config(config)
    return config


def train_baseline(config):
    """Run training for one SFC baseline solver."""
    solver_name = config.solver.solver_name
    num_epochs = config.training.num_train_epochs
    num_v_nets = config.v_sim_setting.num_v_nets

    print(f"\n{'=' * 60}")
    print(f"SFC Baseline Training: {solver_name}")
    print(f"  VNRs: {num_v_nets}, Epochs: {num_epochs}, Seed: {config.experiment.seed}")
    print(f"{'=' * 60}\n")

    # Generate dataset
    print("Generating dataset...")
    p_net, v_net_simulator = Generator.generate_dataset(config, save=False)
    print(f"  Physical network: {p_net.num_nodes} nodes, {p_net.num_links} links")
    print(f"  VNR simulator: {v_net_simulator.num_v_nets} VNRs")

    # Create components
    node_attrs = config.v_sim_setting['node_attrs_setting']
    link_attrs = config.v_sim_setting['link_attrs_setting']
    graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
    counter = Counter(node_attrs, link_attrs, graph_attrs, config)
    controller = Controller(node_attrs, link_attrs, graph_attrs, config)
    recorder = Recorder(counter, config)
    logger = Logger(config=config)

    # Create solver
    solver_cls = SolverRegistry.get(solver_name)
    solver = solver_cls(controller, recorder, counter, logger, config)
    print(f"  Solver: {solver_cls.__name__}")
    print(f"  Device: {solver.device_name}")

    # Create environment
    env = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)

    # Train
    start_time = time.time()
    solver.learn(env, num_epochs=num_epochs)
    elapsed = time.time() - start_time

    # Final validation
    print(f"\n{'=' * 40}")
    print(f"Training complete: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"{'=' * 40}")

    # Run validation
    print(f"\nRunning final validation...")
    solver.eval()
    instance = env.reset(seed=config.experiment.seed)
    success_count = 0
    v_net_count = 0
    r2c_list = []

    while True:
        solution = solver.solve(instance)
        next_instance, reward, done, info = env.step(solution)
        v_net_count += 1
        if info.get('result', False) or solution.get('result', False):
            success_count += 1
        r2c = info.get('long_term_r2c_ratio', 0)
        if done:
            break
        instance = next_instance

    ac = info.get('success_count', success_count) / max(info.get('v_net_count', v_net_count), 1)
    r2c_final = info.get('long_term_r2c_ratio', 0)

    print(f"\n{'=' * 60}")
    print(f"Results for {solver_name}:")
    print(f"  AC (Acceptance Rate): {ac:.4f}")
    print(f"  R2C (Revenue-to-Cost): {r2c_final:.4f}")
    print(f"  Training time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"  VNRs per epoch: {num_v_nets}")
    print(f"{'=' * 60}")

    return {
        'solver_name': solver_name,
        'ac': ac,
        'r2c': r2c_final,
        'elapsed': elapsed,
        'num_epochs': num_epochs,
        'num_v_nets': num_v_nets,
    }


def main():
    parser = argparse.ArgumentParser(description='SFC baseline training')
    parser.add_argument('--solver', type=str, default='sfc_pg_mlp',
                        choices=['sfc_pg_mlp', 'sfc_ppo_dual_gat+', 'sfc_ppo_dual_gcn'],
                        help='Solver to train')
    parser.add_argument('--epochs', type=int, default=30, help='Number of training epochs')
    parser.add_argument('--vnr', type=int, default=2000, help='Number of VNRs per epoch')
    parser.add_argument('--seed', type=int, default=0, help='Random seed')
    parser.add_argument('--gpu', type=int, default=0, help='GPU ID')
    parser.add_argument('--no-cuda', action='store_true', help='Disable CUDA')
    args = parser.parse_args()

    config = build_config(
        num_v_nets=args.vnr,
        seed=args.seed,
        solver_name=args.solver,
        num_epochs=args.epochs,
        use_cuda=not args.no_cuda,
        gpu_id=args.gpu,
    )

    result = train_baseline(config)

    # Save result to file
    results_dir = os.path.join(PROJECT_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    result_file = os.path.join(results_dir, f'{args.solver}_seed{args.seed}.txt')
    with open(result_file, 'w') as f:
        for k, v in result.items():
            f.write(f"{k}: {v}\n")
    print(f"\nResults saved to {result_file}")


if __name__ == '__main__':
    main()
