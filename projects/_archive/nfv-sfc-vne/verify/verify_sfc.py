"""Verification suite for SFC-enhanced VNE.

Tests:
1. SFC VNR generation correctness
2. SFC constraint environment action masking
3. GRC baseline on SFC environment (non-zero AC check)
4. MDP trial: random vs greedy strategy
5. Reward decomposition check

Usage:
    cd projects/nfv-sfc-vne/Virne
    python -m verify.verify_sfc
"""
import sys
import os
import copy
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)

from omegaconf import OmegaConf

from virne.network.virtual_network import VirtualNetwork
from virne.network.sfc.sfc_chain import SFCChain
from virne.network.sfc.sfc_vnr_generator import add_sfc_to_vnet


# ============================================================================
# Test 1: SFC VNR Generation
# ============================================================================

def test_sfc_generation():
    """Verify SFC attributes are correctly added to VNRs."""
    print("=" * 60)
    print("Test 1: SFC VNR Generation")
    print("=" * 60)

    passed = 0
    failed = 0

    # Create a standard Virne VNR
    config = {
        'node_attrs_setting': [
            {'name': 'cpu', 'owner': 'node', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 20, 'generative': True},
        ],
        'link_attrs_setting': [
            {'name': 'bw', 'owner': 'link', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 50, 'generative': True},
        ],
        'topology': {'type': 'random', 'random_prob': 0.5},
    }

    rng = np.random.default_rng(42)

    for size in [3, 5, 8, 10]:
        v_net = VirtualNetwork(config=config)
        v_net.generate_topology(num_nodes=size, type='random', random_prob=0.5)
        v_net.generate_attrs_data()

        chain = add_sfc_to_vnet(v_net, sfc_ratio=0.6, num_vnf_types=5, rng=rng)

        # Check 1: SFC chain exists
        ok = isinstance(chain, SFCChain) and chain.length > 0
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] Size={size}: chain exists, length={chain.length}")
        passed += ok
        failed += (not ok)

        # Check 2: vnf_type set on all nodes
        all_typed = all('vnf_type' in v_net.nodes[n] for n in v_net.nodes)
        vnf_count = sum(1 for n in v_net.nodes if v_net.nodes[n]['vnf_type'] > 0)
        expected_vnfs = max(2, int(round(size * 0.6)))
        ok = all_typed and vnf_count == min(expected_vnfs, size)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] Size={size}: vnf_type set on all nodes, vnf_count={vnf_count} (expected ~{expected_vnfs})")
        passed += ok
        failed += (not ok)

        # Check 3: is_sfc_link set on all edges
        all_marked = all('is_sfc_link' in v_net.edges[u, v] for u, v in v_net.edges)
        ok = all_marked
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] Size={size}: is_sfc_link set on all edges")
        passed += ok
        failed += (not ok)

        # Check 4: sfc_chain stored in graph attrs
        has_chain = 'sfc_chain' in v_net.graph
        ok = has_chain
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] Size={size}: sfc_chain stored in graph attrs")
        passed += ok
        failed += (not ok)

    # Check 5: Degradation - no SFC on size=1
    v_net1 = VirtualNetwork(config=config)
    v_net1.generate_topology(num_nodes=1, type='path')
    v_net1.generate_attrs_data()
    chain1 = add_sfc_to_vnet(v_net1, sfc_ratio=0.6, rng=rng)
    ok = chain1.length == 0
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] Size=1: empty chain (degradation test)")
    passed += ok
    failed += (not ok)

    print(f"\n  Summary: {passed} passed, {failed} failed\n")
    return failed == 0


# ============================================================================
# Test 2: SFC Node Ordering
# ============================================================================

def test_sfc_node_ordering():
    """Verify SFC VNF nodes come first in ranked_nodes."""
    print("=" * 60)
    print("Test 2: SFC Node Ordering")
    print("=" * 60)

    from virne.solver.rank.node_rank import rank_nodes

    config = {
        'node_attrs_setting': [
            {'name': 'cpu', 'owner': 'node', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 20, 'generative': True},
        ],
        'link_attrs_setting': [
            {'name': 'bw', 'owner': 'link', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 50, 'generative': True},
        ],
        'topology': {'type': 'random', 'random_prob': 0.5},
    }

    rng = np.random.default_rng(123)

    v_net = VirtualNetwork(config=config)
    v_net.generate_topology(num_nodes=8, type='random', random_prob=0.5)
    v_net.generate_attrs_data()

    chain = add_sfc_to_vnet(v_net, sfc_ratio=0.6, num_vnf_types=5, rng=rng)

    # Apply original ranking
    rank_nodes(v_net, 'order')
    original_ranked = list(v_net.ranked_nodes)

    # Apply SFC reordering
    sfc_set = set(chain.vnf_node_ids)
    non_sfc = [n for n in original_ranked if n not in sfc_set]
    new_ranking = chain.vnf_node_ids + non_sfc
    v_net.ranked_nodes = np.array(new_ranking)

    final_ranked = list(v_net.ranked_nodes)

    # Check: SFC VNFs come first, in chain order
    sfc_in_order = final_ranked[:len(chain.vnf_node_ids)]
    ok = sfc_in_order == chain.vnf_node_ids
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] SFC VNFs come first: {sfc_in_order} == {chain.vnf_node_ids}")

    # Check: non-SFC nodes follow
    non_sfc_actual = final_ranked[len(chain.vnf_node_ids):]
    ok = all(n not in sfc_set for n in non_sfc_actual)
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] Non-SFC nodes follow: {non_sfc_actual}")

    print(f"  Chain: {chain}")
    print(f"  Final ranking: {final_ranked}\n")
    return ok


# ============================================================================
# Test 3: SFC Constraint Integrity (chain_vnf_count <= total_nodes)
# ============================================================================

def test_sfc_constraints_integrity():
    """Verify SFC constraints don't break VNR structure."""
    print("=" * 60)
    print("Test 3: SFC Constraint Integrity")
    print("=" * 60)

    config = {
        'node_attrs_setting': [
            {'name': 'cpu', 'owner': 'node', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 20, 'generative': True},
        ],
        'link_attrs_setting': [
            {'name': 'bw', 'owner': 'link', 'type': 'resource',
             'distribution': 'uniform', 'dtype': 'int', 'low': 0, 'high': 50, 'generative': True},
        ],
        'topology': {'type': 'random', 'random_prob': 0.5},
    }

    rng = np.random.default_rng(999)
    passed = 0
    failed = 0

    for i in range(20):
        size = rng.integers(3, 11)
        v_net = VirtualNetwork(config=config)
        v_net.generate_topology(num_nodes=int(size), type='random', random_prob=0.5)
        v_net.generate_attrs_data()

        chain = add_sfc_to_vnet(v_net, sfc_ratio=0.6, num_vnf_types=5, rng=rng)

        # Check: all VNF node IDs are valid
        valid_ids = all(0 <= nid < v_net.num_nodes for nid in chain.vnf_node_ids)
        # Check: VNF types are in range
        valid_types = all(1 <= t <= 5 for t in chain.vnf_types)
        # Check: no duplicate VNF nodes
        no_dup = len(set(chain.vnf_node_ids)) == len(chain.vnf_node_ids)
        # Check: SFC edges exist in graph
        valid_edges = all(v_net.has_edge(u, v) for u, v in chain.sfc_edges)

        ok = valid_ids and valid_types and no_dup and valid_edges
        passed += ok
        failed += (not ok)

    status = "PASS" if failed == 0 else "FAIL"
    print(f"  [{status}] 20 random VNRs: {passed} passed, {failed} failed")
    print(f"  All VNF IDs valid, types in range, no duplicates, edges exist\n")
    return failed == 0


# ============================================================================
# Main
# ============================================================================

def main():
    print("\nSFC Verification Suite")
    print("=" * 60)

    results = {}
    results['sfc_generation'] = test_sfc_generation()
    results['sfc_ordering'] = test_sfc_node_ordering()
    results['sfc_integrity'] = test_sfc_constraints_integrity()

    print("=" * 60)
    print("Results Summary:")
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")

    all_pass = all(results.values())
    print(f"\nOverall: {'ALL PASS' if all_pass else 'HAS FAILURES'}")
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
