# E01 Seed 0 Results

## Training
- seed: 0
- episodes: 330 (early stopped at ep 330, KL divergence 0.2094 > threshold 0.15)
- elapsed: 244.0s
- best_reward: -67.6041
- device: cuda (RTX 4070)

## Evaluation (50 episodes, deterministic)
- mean_MLU: 2.1093
- std_MLU: 0.8849

## vs Baselines
- ECMP MLU: 1.9664 -> GNN/ECMP: 1.0727 (target <=0.90) **FAIL**
- MLP MLU: 2.5249 -> GNN/MLP: 0.8354 (target <=0.85) **PASS**
- SP MLU: 2.3674 -> GNN/SP: 0.8910

## Convergence Analysis
- Training stopped early at ep 330/500 due to KL divergence (avg_kl=0.2094 > 0.15)
- Reward was not plateauing: last50 reward at ep 300 was -71.98, best was -67.60
- The KL threshold (0.15) may be too aggressive for this task -- policy was still improving
- High entropy (~375-376) suggests the policy remained exploratory, never converged to decisive actions
- Std_MLU of 0.8849 is very high relative to mean (42%), indicating inconsistent routing quality

## Key Observations
1. GNN does NOT beat ECMP -- 7.3% worse. Fails primary Contract target.
2. GNN beats MLP by 16.5% and beats SP by 10.9%. Meets secondary targets only.
3. Early stop triggered on KL, not reward plateau. The model was still learning but KL divergence grew too fast.
4. High MLU variance (0.88) suggests the model handles some traffic patterns well but fails on others.

## Convergence Judgment
- **MARGINAL**: Fails ECMP target (1.07x vs 0.90x) but beats MLP and SP. Early stop on KL may have cut learning short. A higher KL threshold or KL-penalty training could help.
