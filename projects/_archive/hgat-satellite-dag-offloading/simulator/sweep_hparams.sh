#!/usr/bin/env bash
# Hyperparameter sweep for HGAT (and optionally GraphSAGE/GCN).
# Phase 1: entropy=0.05, lr × interval 3×3 = 9 groups
# Phase 2: fix best (lr, interval), sweep entropy 3 groups
# Phase 3 (optional): quick lr sweep for GraphSAGE/GCN
set -euo pipefail

PYTHON=~/.venvs/torch/bin/python
BASEDIR=/mnt/d/code/study/research-protocol/projects/hgat-satellite-dag-offloading/simulator
cd "$BASEDIR"

EPISODES=100
SEED=42
ENTROPY_FIX=0.05

LRS=(1e-4 2e-4 5e-4)
INTERVALS=(10 20 40)
ENTROPIES=(0.01 0.05 0.1)

OUTDIR=results_sweep
mkdir -p "$OUTDIR"

run_one() {
    local model=$1 lr=$2 interval=$3 entropy=$4
    local tag="${model}_lr${lr}_int${interval}_ent${entropy}"
    local dir="${OUTDIR}/${tag}"
    mkdir -p "$dir"
    echo "=== $tag === $(date +%H:%M:%S)"
    "$PYTHON" train.py \
        --model "$model" --episodes "$EPISODES" --seeds "$SEED" \
        --lr "$lr" --update-interval "$interval" --entropy "$entropy" \
        --output-dir "$dir" 2>&1 | tail -5
}

echo "========== Phase 1: HGAT lr × interval (entropy=$ENTROPY_FIX) =========="
for lr in "${LRS[@]}"; do
    for int in "${INTERVALS[@]}"; do
        run_one hgat "$lr" "$int" "$ENTROPY_FIX"
    done
done

echo ""
echo "========== Analyzing Phase 1 results =========="
"$PYTHON" -c "
import json, numpy as np
from pathlib import Path

results = []
for d in sorted(Path('$OUTDIR').glob('hgat_lr*_int*_ent${ENTROPY_FIX}')):
    jf = list(d.glob('hgat_seed*.json'))
    if not jf: continue
    data = json.load(open(jf[0]))
    rw = data['episode_rewards']
    last50 = rw[-50:]
    tag = d.name.replace('hgat_', '').replace('_ent${ENTROPY_FIX}', '')
    results.append((tag, np.mean(last50), np.std(last50)))

results.sort(key=lambda x: x[1], reverse=True)  # higher is better (less negative)
print(f'{\"lr x interval\":<25} {\"last50 mean\":>12} {\"last50 std\":>10}')
print('-' * 50)
for tag, m, s in results:
    print(f'{tag:<25} {m:>12.0f} {s:>10.0f}')

best_tag = results[0][0]
parts = best_tag.split('_')
best_lr = parts[0].replace('lr', '')
best_int = parts[1].replace('int', '')
print(f'\nBest: lr={best_lr}, interval={best_int} => mean={results[0][1]:.0f}')
# Write best params for Phase 2
with open('$OUTDIR/_best_phase1.txt', 'w') as f:
    f.write(f'{best_lr} {best_int}')
"
echo ""

BEST_PARAMS=$(cat "$OUTDIR/_best_phase1.txt")
BEST_LR=$(echo "$BEST_PARAMS" | awk '{print $1}')
BEST_INT=$(echo "$BEST_PARAMS" | awk '{print $2}')

echo "========== Phase 2: HGAT entropy sweep (lr=$BEST_LR, interval=$BEST_INT) =========="
for ent in "${ENTROPIES[@]}"; do
    run_one hgat "$BEST_LR" "$BEST_INT" "$ent"
done

echo ""
echo "========== Analyzing Phase 2 results =========="
"$PYTHON" -c "
import json, numpy as np
from pathlib import Path

results = []
for d in sorted(Path('$OUTDIR').glob(f'hgat_lr${BEST_LR}_int${BEST_INT}_ent*')):
    jf = list(d.glob('hgat_seed*.json'))
    if not jf: continue
    data = json.load(open(jf[0]))
    rw = data['episode_rewards']
    last50 = rw[-50:]
    ent = d.name.split('_ent')[1]
    results.append((ent, np.mean(last50), np.std(last50)))

results.sort(key=lambda x: x[1], reverse=True)
print(f'{\"entropy\":<12} {\"last50 mean\":>12} {\"last50 std\":>10}')
print('-' * 37)
for ent, m, s in results:
    print(f'{ent:<12} {m:>12.0f} {s:>10.0f}')

print(f'\nBest entropy: {results[0][0]} => mean={results[0][1]:.0f}')
with open('$OUTDIR/_best_overall.txt', 'w') as f:
    f.write(f'lr=${BEST_LR} interval=${BEST_INT} entropy={results[0][0]}')
"

echo ""
echo "========== Phase 3: GraphSAGE & GCN lr sweep =========="
for model in graphsage gcn; do
    for lr in "${LRS[@]}"; do
        run_one "$model" "$lr" 10 0.01
    done
done

echo ""
echo "========== Final Summary =========="
"$PYTHON" -c "
import json, numpy as np
from pathlib import Path

rows = []
for d in sorted(Path('$OUTDIR').glob('*_lr*_int*_ent*')):
    jf = list(d.glob('*.json'))
    if not jf: continue
    data = json.load(open(jf[0]))
    rw = data['episode_rewards']
    last50 = rw[-50:]
    rows.append((d.name, np.mean(last50), np.std(last50)))

rows.sort(key=lambda x: x[1], reverse=True)
print(f'{\"config\":<45} {\"last50 mean\":>12} {\"last50 std\":>10}')
print('-' * 70)
for tag, m, s in rows:
    print(f'{tag:<45} {m:>12.0f} {s:>10.0f}')

best = rows[0]
print(f'\n=== BEST OVERALL: {best[0]} => mean={best[1]:.0f}, std={best[2]:.0f} ===')
"
echo ""
echo "Done. $(date)"
