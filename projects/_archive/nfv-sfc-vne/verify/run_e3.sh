#!/bin/bash
# E3 Ablation Experiment: A1-A3 on WX100, 30ep, 3 seeds
# Run from projects/nfv-sfc-vne/
set -e

cd /mnt/d/code/study/research-protocol/projects/nfv-sfc-vne

PYTHON=~/.venvs/torch/bin/python
SCRIPT=verify/run_sfc_baselines.py
EPOCHS=30
VNRS=500
SEEDS="0 1 2"
ABLATION_SOLVERS="sfc_ppo_ablation_no_sfc_pe sfc_ppo_ablation_no_cross_attn sfc_ppo_ablation_no_edge_attr"
LOGDIR=results/e3_logs

mkdir -p "$LOGDIR"

# Count needed runs
total=0
skipped=0
for solver in $ABLATION_SOLVERS; do
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
echo "E3: Ablation Experiment (A1-A3)"
echo "============================================"
echo "Topology: WX100 | Epochs: $EPOCHS | VNRs: $VNRS | Seeds: $SEEDS"
echo "Runs needed: $total, Skipped: $skipped"
echo "Estimated time: ~$((total * 100)) min ($((total * 100 / 60))h)"
echo "============================================"
echo ""

if [ $total -eq 0 ]; then
    echo "All ablation results exist!"
else
    for solver in $ABLATION_SOLVERS; do
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
echo "=== E3 Ablation Summary ==="
$PYTHON verify/summarize_e3.py

echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] E3 Complete"
