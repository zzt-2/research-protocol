"""E2 Cross-Topology Generalization Experiment.

MatchingGAT vs B1-B3 on BRAIN/WX500 (primary) + GEANT (supplementary).
30 epochs, 3 seeds each.

Usage:
    cd projects/nfv-sfc-vne
    python verify/run_e2.py --topo brain --dry-run
    python verify/run_e2.py --topo brain
    python verify/run_e2.py --topo all
"""
import sys
import os
import time
import argparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

from omegaconf import OmegaConf, open_dict

from virne.network import Generator
from virne.core import Controller, Recorder, Counter
from virne.core.logger import Logger
from virne.core.environment import SolutionStepEnvironment
from virne.solver.base_solver import SolverRegistry
from virne.utils.config import add_simulation_into_config

# Register SFC solvers
from virne.solver.learning.sfc_solver import sfc_baselines  # noqa: F401

TOPO_CONFIGS = {
    'geant': {'file_path': 'Virne/datasets/topology/Geant.gml', 'display': 'GEANT (23 nodes)'},
    'brain': {'file_path': 'Virne/datasets/topology/Brain.gml', 'display': 'BRAIN (161 nodes)'},
    'wx500': {'file_path': 'Virne/datasets/topology/Waxman500.gml', 'display': 'WX500 (500 nodes)'},
}

# E2 solvers: MatchingGAT vs B1-B3 (Contract specifies B1-B3 for E2)
SOLVERS = {
    'sfc_pg_mlp': 'B3: PG-MLP',
    'sfc_ppo_dual_gat+': 'B2: DualGAT+',
    'sfc_ppo_matching_gat': 'Ours: MatchingGAT',
}

SEEDS = [0, 1, 2]
EPOCHS = 30
VNRS = 500


def build_config(topo_name, solver_name='sfc_pg_mlp', seed=0,
                 num_epochs=30, num_v_nets=500):
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
        config.training.use_cuda = True
        config.training.gpu_id = 0
        config.experiment.run_id = f'e2_{topo_name}_{solver_name}'
        config.experiment.seed = seed
        config.logger.backends = ['console']
        config.logger.level = 'INFO'
        config.logger.verbose = 1
        config.rl.reward_calculator.name = 'fixed_intermediate'
        config.rl.reward_calculator.intermediate_reward = 0.1
        config.rl.if_use_negative_sample = False
        config.rl.if_use_baseline_solver = False
        config.sfc = {'sfc_ratio': 0.6, 'num_vnf_types': 5, 'seed': 42}

        # Override topology
        topo_cfg = TOPO_CONFIGS[topo_name]
        config.p_net_setting.topology.file_path = topo_cfg['file_path']

    add_simulation_into_config(config)
    return config


def train_and_evaluate(config):
    solver_name = config.solver.solver_name
    num_epochs = config.training.num_train_epochs
    topo_id = config.experiment.run_id.split('_')[1]

    print(f"\n{'=' * 60}")
    print(f"E2: {solver_name} on {topo_id}")
    print(f"  Epochs: {num_epochs}, VNRs: {config.v_sim_setting.num_v_nets}, Seed: {config.experiment.seed}")
    print(f"{'=' * 60}\n")

    p_net, v_net_simulator = Generator.generate_dataset(config, save=False)
    print(f"  Network: {p_net.num_nodes} nodes, {p_net.num_links} links")

    node_attrs = config.v_sim_setting['node_attrs_setting']
    link_attrs = config.v_sim_setting['link_attrs_setting']
    graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
    counter = Counter(node_attrs, link_attrs, graph_attrs, config)
    controller = Controller(node_attrs, link_attrs, graph_attrs, config)
    recorder = Recorder(counter, config)
    logger = Logger(config=config)

    solver_cls = SolverRegistry.get(solver_name)
    solver = solver_cls(controller, recorder, counter, logger, config)

    env = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)

    start_time = time.time()
    solver.learn(env, num_epochs=num_epochs)
    elapsed = time.time() - start_time

    # Final validation
    solver.eval()
    instance = env.reset(seed=config.experiment.seed)
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

    ac = info.get('success_count', success_count) / max(info.get('v_net_count', v_net_count), 1)
    r2c_final = info.get('long_term_r2c_ratio', 0)

    print(f"\n  Results: AC={ac:.4f}, R2C={r2c_final:.4f}, time={elapsed / 60:.1f}min")

    result = {
        'solver_name': solver_name, 'ac': ac, 'r2c': r2c_final,
        'elapsed': elapsed, 'num_epochs': num_epochs,
        'num_v_nets': config.v_sim_setting.num_v_nets,
        'topology': topo_id, 'p_net_nodes': p_net.num_nodes,
    }

    # Save result
    results_dir = os.path.join(PROJECT_ROOT, 'results', 'e2')
    os.makedirs(results_dir, exist_ok=True)
    result_file = os.path.join(results_dir, f'{topo_id}_{solver_name}_seed{config.experiment.seed}.txt')
    with open(result_file, 'w') as f:
        for k, v in result.items():
            f.write(f"{k}: {v}\n")

    return result


def run_grc_eval(topo_name, seed, num_v_nets=500):
    """GRC heuristic evaluation for a given topology."""
    from virne.network.sfc.sfc_vnr_generator import add_sfc_to_simulator

    config = build_config(topo_name, solver_name='grc_rank', seed=seed,
                          num_epochs=1, num_v_nets=num_v_nets)
    with open_dict(config):
        config.logger.level = 'WARNING'
        config.logger.verbose = 0

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
        next_instance, _, done, info = env.step(solution)
        v_net_count += 1
        if info.get('result', False) or solution.get('result', False):
            success_count += 1
        if done:
            break
        instance = next_instance

    elapsed = time.time() - start_time
    ac = info.get('success_count', success_count) / max(info.get('v_net_count', v_net_count), 1)
    r2c_final = info.get('long_term_r2c_ratio', 0)

    print(f"  GRC {topo_name} seed={seed}: AC={ac:.4f}, R2C={r2c_final:.4f}, {elapsed:.1f}s")

    result = {
        'solver_name': 'grc_rank', 'ac': ac, 'r2c': r2c_final,
        'elapsed': elapsed, 'num_epochs': 1,
        'num_v_nets': num_v_nets, 'topology': topo_name,
        'p_net_nodes': p_net.num_nodes,
    }

    results_dir = os.path.join(PROJECT_ROOT, 'results', 'e2')
    os.makedirs(results_dir, exist_ok=True)
    result_file = os.path.join(results_dir, f'{topo_name}_grc_rank_seed{seed}.txt')
    with open(result_file, 'w') as f:
        for k, v in result.items():
            f.write(f"{k}: {v}\n")

    return result


def result_exists(topo_name, solver_name, seed):
    results_dir = os.path.join(PROJECT_ROOT, 'results', 'e2')
    path = os.path.join(results_dir, f'{topo_name}_{solver_name}_seed{seed}.txt')
    return os.path.exists(path)


def main():
    parser = argparse.ArgumentParser(description='E2 Cross-Topology Experiment')
    parser.add_argument('--topo', type=str, default='all',
                        choices=['geant', 'brain', 'wx500', 'all'],
                        help='Topology to test')
    parser.add_argument('--dry-run', action='store_true', help='Show plan without running')
    args = parser.parse_args()

    topos = ['brain', 'wx500', 'geant'] if args.topo == 'all' else [args.topo]

    # Count needed runs
    needed = []
    for topo in topos:
        for solver in SOLVERS:
            for seed in SEEDS:
                if not result_exists(topo, solver, seed):
                    needed.append((topo, solver, seed))

    print("=" * 60)
    print("E2: Cross-Topology Generalization")
    print("=" * 60)
    print(f"Topologies: {[TOPO_CONFIGS[t]['display'] for t in topos]}")
    print(f"DRL runs needed: {len(needed)} / {len(topos) * len(SOLVERS) * len(SEEDS)} total")
    print(f"Estimated time: ~{len(needed) * 100} min ({len(needed) * 100 // 60}h)")
    print("=" * 60)

    if args.dry_run:
        for topo, solver, seed in needed:
            print(f"  Would run: {TOPO_CONFIGS[topo]['display']} / {SOLVERS[solver]} / seed={seed}")
        return

    # Run DRL experiments
    for topo, solver, seed in needed:
        if result_exists(topo, solver, seed):
            continue
        print(f"\n[{time.strftime('%H:%M:%S')}] START {topo}/{solver}/seed{seed}")
        try:
            config = build_config(topo, solver_name=solver, seed=seed,
                                  num_epochs=EPOCHS, num_v_nets=VNRS)
            train_and_evaluate(config)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        print(f"[{time.strftime('%H:%M:%S')}] DONE {topo}/{solver}/seed{seed}")

    # Run GRC for each topology
    print(f"\n{'=' * 60}")
    print("GRC Baseline per topology")
    print(f"{'=' * 60}")
    for topo in topos:
        for seed in SEEDS:
            if not result_exists(topo, 'grc_rank', seed):
                run_grc_eval(topo, seed, VNRS)

    print("\nE2 Complete!")


if __name__ == '__main__':
    main()
