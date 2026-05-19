#!/bin/bash
# Training queue: ablation 5ep → MatchingGAT 30ep
# Run from projects/nfv-sfc-vne/
set -e

PYTHON=~/.venvs/torch/bin/python
SCRIPT=verify/run_sfc_baselines.py
ABLATION=verify/run_ablation.py

echo "=== Step 1: Ablation study (5 epochs each) ==="
$PYTHON $ABLATION --epochs 5 --vnr 500 --skip-full 2>&1 | tee results/ablation_5ep.log

echo ""
echo "=== Step 2: MatchingGAT full training (30 epochs) ==="
$PYTHON $SCRIPT --solver sfc_ppo_matching_gat --epochs 30 --vnr 500 2>&1 | tee results/matching_gat_30ep.log

echo ""
echo "=== All training complete ==="
echo "Results in results/ directory"
