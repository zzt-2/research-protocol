#!/bin/bash
# E1 Main Comparison: MatchingGAT vs B1-B5, WX100, 30ep, 3 seeds
# Run from projects/nfv-sfc-vne/
set -e

cd /mnt/d/code/study/research-protocol/projects/nfv-sfc-vne

PYTHON=~/.venvs/torch/bin/python
SCRIPT=verify/run_sfc_baselines.py
EPOCHS=15
VNRS=300
SEEDS="0 1 2"
# Core comparison only: MatchingGAT (ours) vs DualGAT+ (primary baseline)
SOLVERS="sfc_ppo_dual_gat+ sfc_ppo_matching_gat"
LOGDIR=results/e1_logs

mkdir -p "$LOGDIR"

# Count needed runs
total=0
skipped=0
for solver in $SOLVERS; do
    for seed in $SEEDS; do
        outfile="results/${solver}_seed${seed}.txt"
        if [ -f "$outfile" ]; then
            skipped=$((skipped + 1))
        else
            total=$((total + 1))
        fi
    done
done

echo "============================================"
echo "E1: Main Comparison Experiment"
echo "============================================"
echo "Topology: WX100 (Waxman 100 nodes)"
echo "Epochs: $EPOCHS, VNRs/epoch: $VNRS, Seeds: $SEEDS"
echo "Runs needed: $total, Skipped (existing): $skipped"
echo "Estimated time: ~$((total * 100)) min ($((total * 100 / 60))h)"
echo "============================================"
echo ""

if [ $total -eq 0 ]; then
    echo "All DRL results exist. Running GRC baseline..."
else
    for solver in $SOLVERS; do
        for seed in $SEEDS; do
            outfile="results/${solver}_seed${seed}.txt"
            if [ -f "$outfile" ]; then
                echo "[SKIP] $solver seed=$seed"
                continue
            fi
            logfile="${LOGDIR}/${solver}_seed${seed}.log"
            echo ""
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] START $solver seed=$seed"
            $PYTHON $SCRIPT --solver $solver --epochs $EPOCHS --vnr $VNRS --seed $seed 2>&1 | tee "$logfile"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] DONE $solver seed=$seed"
        done
    done
fi

echo ""
echo "=== GRC Heuristic Baseline (B1) ==="
$PYTHON verify/run_grc_e1.py 2>&1 | tee "${LOGDIR}/grc_baseline.log"

echo ""
echo "=== E1 Summary ==="
$PYTHON verify/summarize_e1.py

echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] E1 Complete"
