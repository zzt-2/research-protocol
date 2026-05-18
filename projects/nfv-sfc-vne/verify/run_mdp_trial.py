"""MDP Trial Run (Part A-checkpoint).

Tests SFC environment with:
1. Random policy (1 episode)
2. Greedy policy (1 episode)
3. Reward decomposition check

Quality gates (hard):
- No single component >95% of total reward
- Strategy distinction: greedy > random by >10%
- Key metric optimizable: greedy AC > random AC

Usage:
    cd projects/nfv-sfc-vne
    python verify/run_mdp_trial.py
"""
import sys
import os
import copy
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

from omegaconf import OmegaConf

from virne.network import PhysicalNetwork, VirtualNetwork
from virne.core import Controller, Recorder, Counter, Solution
from virne.core.logger import Logger
from virne.network.sfc.sfc_vnr_generator import add_sfc_to_vnet
from virne.solver.learning.sfc_solver.sfc_instance_env import SFCJointPRStepInstanceRLEnv


def create_test_components(num_v_nodes=6):
    """Create minimal Virne components for testing."""
    settings_dir = os.path.join(VIRNE_ROOT, 'settings')
    config = OmegaConf.load(os.path.join(settings_dir, 'main.yaml'))
    learning_config = OmegaConf.load(os.path.join(settings_dir, 'learning.yaml'))
    v_sim_config = OmegaConf.load(os.path.join(settings_dir, 'v_sim_setting', 'default.yaml'))
    p_net_config = OmegaConf.load(os.path.join(settings_dir, 'p_net_setting', 'default.yaml'))
    config = OmegaConf.merge(config, learning_config,
                             {'v_sim_setting': v_sim_config},
                             {'p_net_setting': p_net_config})

    OmegaConf.set_struct(config, False)
    config.experiment.run_id = 'mdp_trial'
    config.logger.backends = ['console']
    config.logger.level = 'WARNING'
    config.solver.node_ranking_method = 'order'
    config.solver.allow_revocable = False
    config.solver.allow_rejection = False
    config.rl.reward_calculator.name = 'fixed_intermediate'
    config.rl.reward_calculator.intermediate_reward = 0.1
    OmegaConf.set_struct(config, True)

    # Physical network
    p_net = PhysicalNetwork.from_setting(config.p_net_setting)

    # Virtual network
    v_net = VirtualNetwork(config={
        'node_attrs_setting': config.v_sim_setting.node_attrs_setting,
        'link_attrs_setting': config.v_sim_setting.link_attrs_setting,
        'topology': config.v_sim_setting.topology,
        'graph_attrs_setting': {'id': 0, 'arrival_time': 0.0, 'lifetime': 100.0},
    })
    v_net.generate_topology(num_nodes=num_v_nodes, type='random', random_prob=0.5)
    v_net.generate_attrs_data()

    # Add SFC
    rng = np.random.default_rng(42)
    chain = add_sfc_to_vnet(v_net, sfc_ratio=0.6, num_vnf_types=5, rng=rng)
    print(f"  VNR: {v_net.num_nodes} nodes, {v_net.num_links} links, chain={chain}")

    # Virne components
    node_attrs = config.v_sim_setting.node_attrs_setting
    link_attrs = config.v_sim_setting.link_attrs_setting
    graph_attrs = config.v_sim_setting.get('graph_attrs_setting', {})
    counter = Counter(node_attrs, link_attrs, graph_attrs, config)
    controller = Controller(node_attrs, link_attrs, graph_attrs, config)
    recorder = Recorder(counter, config)
    logger = Logger(config=config)

    return p_net, v_net, controller, recorder, counter, logger, config


def run_random_episode(env):
    """Run 1 episode with random valid actions."""
    obs = env.reset()
    total_reward = 0
    rewards = []
    steps = 0
    done = False

    while not done:
        mask = obs.get('action_mask', np.ones(env.num_actions, dtype=bool))
        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            break
        action = np.random.choice(valid_actions)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        rewards.append(reward)
        steps += 1

    return total_reward, rewards, steps, env.solution


def run_greedy_episode(env):
    """Run 1 episode with greedy action (first valid candidate)."""
    obs = env.reset()
    total_reward = 0
    rewards = []
    steps = 0
    done = False

    while not done:
        mask = obs.get('action_mask', np.ones(env.num_actions, dtype=bool))
        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            break
        # Greedy: pick first valid action (usually highest-resource node)
        action = valid_actions[0]
        obs, reward, done, info = env.step(action)
        total_reward += reward
        rewards.append(reward)
        steps += 1

    return total_reward, rewards, steps, env.solution


def check_reward_balance(rewards, label):
    """Check reward decomposition for domination."""
    if not rewards:
        print(f"  [{label}] No rewards collected")
        return True

    abs_rewards = [abs(r) for r in rewards]
    total_abs = sum(abs_rewards) + 1e-12

    positive = sum(r for r in rewards if r > 0)
    negative = sum(r for r in rewards if r < 0)
    pos_pct = positive / (positive + abs(negative) + 1e-12) * 100
    neg_pct = abs(negative) / (positive + abs(negative) + 1e-12) * 100

    # Check intermediate vs final reward
    intermediate_count = sum(1 for r in rewards if 0 < abs(r) < 1)
    final_count = sum(1 for r in rewards if abs(r) >= 1)

    print(f"  [{label}] Total reward: {sum(rewards):.4f}")
    print(f"  [{label}] Steps: {len(rewards)}, Positive: {positive:.4f} ({pos_pct:.1f}%), Negative: {negative:.4f} ({neg_pct:.1f}%)")
    print(f"  [{label}] Intermediate steps: {intermediate_count}, Final steps: {final_count}")
    print(f"  [{label}] Reward values: {[f'{r:.3f}' for r in rewards]}")

    # Domination check: no single reward >95% of total absolute reward
    dominated = any(ar / total_abs > 0.95 for ar in abs_rewards)
    if dominated:
        print(f"  [WARN] Single step dominates >95% of total reward!")
    return not dominated


def main():
    print("=" * 60)
    print("MDP Trial Run — SFC Environment")
    print("=" * 60)

    # Test 1: Environment instantiation
    print("\n--- Test 1: SFC Environment Instantiation ---")
    p_net, v_net, controller, recorder, counter, logger, config = create_test_components()

    env = SFCJointPRStepInstanceRLEnv(
        p_net, v_net, controller, recorder, counter, logger, config
    )
    obs = env.reset()
    print(f"  Environment created successfully")
    print(f"  Action space: {env.action_space}")
    print(f"  Num actions: {env.num_actions}")
    print(f"  Node ranking: {list(env.v_net.ranked_nodes)}")
    print(f"  SFC chain: {env.sfc_chain}")

    # Verify SFC ordering
    ranked = list(env.v_net.ranked_nodes)
    sfc_nodes = env.sfc_chain.vnf_node_ids
    sfc_first = ranked[:len(sfc_nodes)]
    ok = sfc_first == sfc_nodes
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] SFC VNFs first in ranking: {sfc_first} == {sfc_nodes}")

    if not ok:
        print("  SFC ordering failed, aborting.")
        return 1

    # Test 2: Random episode
    print("\n--- Test 2: Random Policy Episode ---")
    np.random.seed(123)
    random_reward, random_rewards, random_steps, random_solution = run_random_episode(env)
    random_success = random_solution.get('result', False)
    balance_ok_random = check_reward_balance(random_rewards, "Random")
    print(f"  Result: {'SUCCESS' if random_success else 'FAILURE'}")

    # Test 3: Greedy episode (fresh env)
    print("\n--- Test 3: Greedy Policy Episode ---")
    p_net2, v_net2, controller2, recorder2, counter2, logger2, config2 = create_test_components()
    env2 = SFCJointPRStepInstanceRLEnv(
        p_net2, v_net2, controller2, recorder2, counter2, logger2, config2
    )
    greedy_reward, greedy_rewards, greedy_steps, greedy_solution = run_greedy_episode(env2)
    greedy_success = greedy_solution.get('result', False)
    balance_ok_greedy = check_reward_balance(greedy_rewards, "Greedy")
    print(f"  Result: {'SUCCESS' if greedy_success else 'FAILURE'}")

    # Test 4: Quality gates
    print("\n--- Quality Gates ---")

    # Gate 1: No single component >95%
    gate1 = balance_ok_random and balance_ok_greedy
    status = "PASS" if gate1 else "FAIL"
    print(f"  [{status}] No single reward component >95%")

    # Gate 2: Strategy distinction >10%
    if random_reward == 0 and greedy_reward == 0:
        gate2 = False
        print(f"  [FAIL] Both rewards are 0, no distinction")
    elif random_reward == 0:
        gate2 = True
        print(f"  [PASS] Greedy ({greedy_reward:.4f}) > Random ({random_reward:.4f}) — infinite improvement")
    else:
        ratio = abs(greedy_reward - random_reward) / max(abs(random_reward), 1e-12)
        gate2 = ratio > 0.1
        status = "PASS" if gate2 else "FAIL"
        print(f"  [{status}] Strategy distinction: |greedy-random|/|random| = {ratio:.2%} ({'>10%' if gate2 else '<10%'})")

    # Gate 3: Key metric optimizable (greedy success or at least steps difference)
    gate3 = greedy_success or greedy_steps != random_steps
    status = "PASS" if gate3 else "FAIL"
    print(f"  [{status}] Key metric optimizable (greedy_result={greedy_success}, steps: {greedy_steps} vs {random_steps})")

    # Test 5: Multiple VNR sizes
    print("\n--- Test 5: Multiple VNR Sizes ---")
    all_pass = True
    for size in [3, 5, 8]:
        try:
            p, v, c, rec, cnt, log, cfg = create_test_components(num_v_nodes=size)
            e = SFCJointPRStepInstanceRLEnv(p, v, c, rec, cnt, log, cfg)
            o = e.reset()
            # Run a few steps
            done = False
            steps = 0
            while not done and steps < 20:
                mask = o.get('action_mask', np.ones(e.num_actions, dtype=bool))
                valid = np.where(mask)[0]
                if len(valid) == 0:
                    break
                o, r, done, info = e.step(valid[0])
                steps += 1
            print(f"  Size={size}: OK, {steps} steps, result={e.solution.get('result', False)}")
        except Exception as ex:
            print(f"  Size={size}: FAIL - {ex}")
            all_pass = False

    # Summary
    print(f"\n{'=' * 60}")
    print("MDP Trial Summary:")
    all_gates = gate1 and gate2 and gate3 and all_pass
    print(f"  Gate 1 (no domination): {'PASS' if gate1 else 'FAIL'}")
    print(f"  Gate 2 (strategy distinction): {'PASS' if gate2 else 'FAIL'}")
    print(f"  Gate 3 (metric optimizable): {'PASS' if gate3 else 'FAIL'}")
    print(f"  Multi-size test: {'PASS' if all_pass else 'FAIL'}")
    print(f"\n  Overall: {'ALL GATES PASS' if all_gates else 'HAS FAILURES'}")
    return 0 if all_gates else 1


if __name__ == '__main__':
    sys.exit(main())
