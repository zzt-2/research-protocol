"""Integration test for MatchingGAT solver."""
import sys, os
sys.path.insert(0, 'Virne')
import torch, numpy as np
from omegaconf import OmegaConf, open_dict
from virne.network import Generator
from virne.core import Controller, Recorder, Counter
from virne.core.logger import Logger
from virne.solver import SolverRegistry
from virne.solver.learning.sfc_solver import sfc_baselines
from virne.utils.config import add_simulation_into_config
from virne.core.environment import SolutionStepEnvironment

settings_dir = 'Virne/settings'
config = OmegaConf.load(os.path.join(settings_dir, 'main.yaml'))
learning_config = OmegaConf.load(os.path.join(settings_dir, 'learning.yaml'))
v_sim_config = OmegaConf.load(os.path.join(settings_dir, 'v_sim_setting', 'default.yaml'))
p_net_config = OmegaConf.load(os.path.join(settings_dir, 'p_net_setting', 'default.yaml'))
config = OmegaConf.merge(config, learning_config, {'v_sim_setting': v_sim_config}, {'p_net_setting': p_net_config})

with open_dict(config):
    config.solver.solver_name = 'sfc_ppo_matching_gat'
    config.solver.node_ranking_method = 'order'
    config.solver.allow_revocable = False
    config.solver.allow_rejection = False
    config.v_sim_setting.num_v_nets = 50
    config.training.num_train_epochs = 1
    config.training.use_cuda = True
    config.training.gpu_id = 0
    config.experiment.run_id = 'test_matching_gat'
    config.experiment.seed = 42
    config.logger.backends = ['console']
    config.logger.level = 'WARNING'
    config.logger.verbose = 0
    config.rl.reward_calculator.name = 'fixed_intermediate'
    config.rl.reward_calculator.intermediate_reward = 0.1
    config.rl.if_use_negative_sample = False
    config.rl.if_use_baseline_solver = False
    config.sfc = {'sfc_ratio': 0.6, 'num_vnf_types': 5, 'seed': 42}

add_simulation_into_config(config)
print('Generating dataset...')
p_net, v_net_simulator = Generator.generate_dataset(config, save=False)
print(f'PN: {p_net.num_nodes} nodes, {p_net.num_links} links, VNRs: {v_net_simulator.num_v_nets}')

node_attrs = config.v_sim_setting['node_attrs_setting']
link_attrs = config.v_sim_setting['link_attrs_setting']
graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
counter = Counter(node_attrs, link_attrs, graph_attrs, config)
controller = Controller(node_attrs, link_attrs, graph_attrs, config)
recorder = Recorder(counter, config)
logger = Logger(config=config)

print('Creating MatchingGAT solver...')
solver_cls = SolverRegistry.get('sfc_ppo_matching_gat')
solver = solver_cls(controller, recorder, counter, logger, config)
print(f'Solver: {solver_cls.__name__}, device: {solver.device_name}')

# Test 1: Inference
print('Test 1: Inference on first 10 VNRs...')
env = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)
solver.eval()
instance = env.reset(seed=42)
results = []
for i in range(10):
    solution = solver.solve(instance)
    results.append(solution.get('result', False))
    if i < 9:
        next_out = env.step(solution)
        instance = next_out[0]
        if next_out[2]:
            break
print(f'  Results: {results}')
print(f'  AC: {sum(results)}/{len(results)} = {sum(results)/len(results):.3f}')

# Test 2: Short training (1 epoch, 50 VNRs)
print('Test 2: Training 1 epoch (50 VNRs)...')
env2 = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)
solver.train()
solver.learn(env2, num_epochs=1)
print('  Training completed')

# Test 3: Post-training inference
print('Test 3: Post-training inference...')
env3 = SolutionStepEnvironment(p_net, v_net_simulator, controller, recorder, counter, logger, config)
solver.eval()
instance = env3.reset(seed=42)
results2 = []
for i in range(10):
    solution = solver.solve(instance)
    results2.append(solution.get('result', False))
    if i < 9:
        next_out = env3.step(solution)
        instance = next_out[0]
        if next_out[2]:
            break
print(f'  Results: {results2}')
print(f'  AC: {sum(results2)}/{len(results2)} = {sum(results2)/len(results2):.3f}')

print()
print('ALL INTEGRATION TESTS PASSED!')
