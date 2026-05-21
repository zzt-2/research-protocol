"""GRC baseline evaluation with multiple seeds for E1.

GRC is heuristic (no training), so we only run evaluation with 3 seeds
to get consistent VNR generation across all baselines.
"""
import sys
import os
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

from omegaconf import OmegaConf, open_dict

from virne.network import Generator
from virne.network.sfc.sfc_vnr_generator import add_sfc_to_simulator
from virne.core import Controller, Recorder, Counter
from virne.core.logger import Logger
from virne.core.environment import SolutionStepEnvironment
from virne.solver.base_solver import SolverRegistry
from virne.utils.config import add_simulation_into_config


def build_grc_config(seed=0, num_v_nets=500):
    settings_dir = os.path.join(VIRNE_ROOT, 'settings')
    config = OmegaConf.load(os.path.join(settings_dir, 'main.yaml'))
    learning_config = OmegaConf.load(os.path.join(settings_dir, 'learning.yaml'))
    v_sim_config = OmegaConf.load(os.path.join(settings_dir, 'v_sim_setting', 'default.yaml'))
    p_net_config = OmegaConf.load(os.path.join(settings_dir, 'p_net_setting', 'default.yaml'))
    config = OmegaConf.merge(config, learning_config,
                             {'v_sim_setting': v_sim_config},
                             {'p_net_setting': p_net_config})

    with open_dict(config):
        config.solver.solver_name = 'grc_rank'
        config.solver.node_ranking_method = 'order'
        config.solver.allow_revocable = False
        config.solver.allow_rejection = False
        config.v_sim_setting.num_v_nets = num_v_nets
        config.training.num_train_epochs = 1
        config.experiment.run_id = 'sfc_grc_rank'
        config.experiment.seed = seed
        config.logger.backends = ['console']
        config.logger.level = 'WARNING'
        config.logger.verbose = 0
        config.sfc = {
            'sfc_ratio': 0.6,
            'num_vnf_types': 5,
            'seed': 42,
        }

    add_simulation_into_config(config)
    return config


def run_grc_eval(config):
    seed = config.experiment.seed

    p_net, v_net_simulator = Generator.generate_dataset(config, save=False)
    add_sfc_to_simulator(v_net_simulator, sfc_ratio=0.6, num_vnf_types=5, seed=42)

    node_attrs = config.v_sim_setting['node_attrs_setting']
    link_attrs = config.v_sim_setting['link_attrs_setting']
    graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
    counter = Counter(node_attrs, link_attrs, graph_attrs, config)
    controller = Controller(node_attrs, link_attrs, graph_attrs, config)
    recorder = Recorder(counter, config)
    logger = Logger(config=config)

    solver_cls = SolverRegistry.get('grc_rank')
    solver = solver_cls(controller, recorder, counter, logger, config)

    env = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)

    start_time = time.time()
    instance = env.reset(seed=seed)
    success_count = 0
    v_net_count = 0

    while True:
        solution = solver.solve(instance)
        next_instance, reward, done, info = env.step(solution)
        v_net_count += 1
        if info.get('result', False) or solution.get('result', False):
            success_count += 1
        if done:
            break
        instance = next_instance

    elapsed = time.time() - start_time
    ac = info.get('success_count', success_count) / max(info.get('v_net_count', v_net_count), 1)
    r2c_final = info.get('long_term_r2c_ratio', 0)

    print(f"  GRC seed={seed}: AC={ac:.4f}, R2C={r2c_final:.4f}, time={elapsed:.1f}s")
    return {'solver_name': 'grc_rank', 'ac': ac, 'r2c': r2c_final,
            'elapsed': elapsed, 'num_epochs': 1, 'num_v_nets': config.v_sim_setting.num_v_nets}


def main():
    print("=" * 50)
    print("GRC Baseline (B1) — 3 seeds evaluation")
    print("=" * 50)

    results = []
    for seed in [0, 1, 2]:
        config = build_grc_config(seed=seed, num_v_nets=500)
        result = run_grc_eval(config)
        result['seed'] = seed
        results.append(result)

        # Save individual result
        results_dir = os.path.join(PROJECT_ROOT, 'results')
        os.makedirs(results_dir, exist_ok=True)
        with open(os.path.join(results_dir, f'grc_rank_seed{seed}.txt'), 'w') as f:
            for k, v in result.items():
                f.write(f"{k}: {v}\n")

    # Summary
    import numpy as np
    acs = [r['ac'] for r in results]
    r2cs = [r['r2c'] for r in results]
    print(f"\n  GRC Summary: AC={np.mean(acs):.4f}±{np.std(acs):.4f}, "
          f"R2C={np.mean(r2cs):.4f}±{np.std(r2cs):.4f}")


if __name__ == '__main__':
    main()
