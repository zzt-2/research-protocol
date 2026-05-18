"""GRC baseline test on SFC-augmented VNRs.

Verifies:
1. Virne pipeline works with SFC-augmented VNRs (GRC doesn't use SFC features)
2. GRC achieves non-zero AC (risk mitigation: SFC VNRs aren't trivially unsolvable)

Usage:
    cd projects/nfv-sfc-vne
    python verify/run_grc_baseline.py
"""
import sys
import os
import copy
import time
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

from omegaconf import OmegaConf, DictConfig

from virne.network import PhysicalNetwork, Generator
from virne.network.sfc.sfc_vnr_generator import add_sfc_to_simulator
from virne.core import Controller, Recorder, Counter
from virne.core.logger import Logger
from virne.solver.base_solver import SolverRegistry
from virne.utils.config import add_simulation_into_config


def run_grc_test(num_v_nets=50, sfc_ratio=0.6):
    print("=" * 60)
    print(f"GRC Baseline Test (num_v_nets={num_v_nets}, sfc_ratio={sfc_ratio})")
    print("=" * 60)

    # Load and merge configs (mimic Hydra defaults)
    settings_dir = os.path.join(VIRNE_ROOT, 'settings')
    config = OmegaConf.load(os.path.join(settings_dir, 'main.yaml'))
    learning_config = OmegaConf.load(os.path.join(settings_dir, 'learning.yaml'))
    v_sim_config = OmegaConf.load(os.path.join(settings_dir, 'v_sim_setting', 'default.yaml'))
    p_net_config = OmegaConf.load(os.path.join(settings_dir, 'p_net_setting', 'default.yaml'))
    # Hydra wraps these under v_sim_setting / p_net_setting keys
    config = OmegaConf.merge(config, learning_config,
                             {'v_sim_setting': v_sim_config},
                             {'p_net_setting': p_net_config})

    # Override for quick test
    OmegaConf.set_struct(config, False)
    config.solver.solver_name = 'grc_rank'
    config.v_sim_setting.num_v_nets = num_v_nets
    config.training.num_epochs = 1
    config.experiment.run_id = 'sfc_grc_test'
    config.logger.backends = ['console']
    OmegaConf.set_struct(config, True)
    add_simulation_into_config(config)

    # Generate dataset
    print("\nGenerating dataset...")
    p_net, v_net_simulator = Generator.generate_dataset(config, save=False)
    print(f"  Physical network: {p_net.num_nodes} nodes, {p_net.num_links} links")
    print(f"  VNR simulator: {v_net_simulator.num_v_nets} VNRs")

    # Add SFC attributes to all VNRs
    print(f"\nAdding SFC attributes (ratio={sfc_ratio})...")
    add_sfc_to_simulator(v_net_simulator, sfc_ratio=sfc_ratio, num_vnf_types=5, seed=42)

    # Check SFC attributes
    sample_vnet = v_net_simulator.v_nets[0]
    chain = sample_vnet.graph.get('sfc_chain', None)
    print(f"  Sample VNR: {sample_vnet.num_nodes} nodes, chain={chain}")

    # Create components
    node_attrs = config.v_sim_setting['node_attrs_setting']
    link_attrs = config.v_sim_setting['link_attrs_setting']
    graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
    counter = Counter(node_attrs, link_attrs, graph_attrs, config)
    controller = Controller(node_attrs, link_attrs, graph_attrs, config)
    recorder = Recorder(counter, config)
    logger = Logger(config=config)

    # Create GRC solver
    solver_cls = SolverRegistry.get('grc_rank')
    solver = solver_cls(controller, recorder, counter, logger, config)
    print(f"\n  Solver: {solver_cls.__name__}")

    # Run GRC on VNRs
    print(f"\nRunning GRC on {num_v_nets} VNRs...")
    from virne.core.environment import SolutionStepEnvironment
    env = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)

    start_time = time.time()
    instance = env.reset(seed=42)
    success_count = 0
    r2c_list = []
    vnet_count = 0

    while True:
        solution = solver.solve(instance)
        next_instance, _, done, info = env.step(solution)
        vnet_count += 1
        if info.get('result', False) or solution.get('result', False):
            success_count += 1
        r2c = info.get('long_term_r2c_ratio', 0)
        if done:
            break
        instance = next_instance

    elapsed = time.time() - start_time

    # Results
    ac = info.get('success_count', success_count) / max(info.get('v_net_count', vnet_count), 1)
    r2c_final = info.get('long_term_r2c_ratio', 0)

    print(f"\n{'=' * 40}")
    print(f"Results:")
    print(f"  AC (Acceptance Rate): {ac:.4f}")
    print(f"  R2C (Revenue-to-Cost): {r2c_final:.4f}")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  VNRs processed: {info.get('v_net_count', vnet_count)}")
    print(f"  Success count: {info.get('success_count', success_count)}")

    # Check: non-zero AC
    if ac > 0:
        print(f"\n  [PASS] AC={ac:.4f} > 0 — SFC VNRs are solvable by GRC")
    else:
        print(f"\n  [FAIL] AC=0 — SFC VNRs are not solvable!")
        return False

    return True


if __name__ == '__main__':
    ok = run_grc_test()
    sys.exit(0 if ok else 1)
