# Step 1 Quick Test Log

## Smoke Test
- Status: PASS
- Obs shapes: x=(66,6), edge_index=(2,264), edge_attr=(264,4)
- Initial episode MLU: 2.9418 (untrained random policy)
- Steps completed: 20/20

## Training
- seed: 42
- episodes: 100
- update_interval: 10
- early_stop_patience: 50 (not triggered)
- elapsed: 70.5s
- best_reward: -66.6680
- episode_reward_mean: -69.5842
- episode_reward_last10_mean: -69.2257
- final ploss: 0.1050
- final entropy: 375.3711

## Evaluation (deterministic, 50 episodes)
- mean_MLU: 2.0702
- std_MLU: 0.8699

## Baseline Comparison
- ECMP MLU: 1.9664
- GNN/ECMP ratio: 1.05 (GNN 5% worse than ECMP)
- SP MLU: 2.3674
- GNN/SP ratio: 0.87 (GNN 13% better than SP)
- MLP MLU: 2.5249
- GNN/MLP ratio: 0.82 (GNN 18% better than MLP)

## Analysis
- After only 100 episodes of training, GNN (2.07) already outperforms SP (2.37) and MLP (2.52)
- GNN has not yet surpassed ECMP (1.97) -- needs more training (default config uses 500 episodes)
- High std (0.87) suggests policy is still unstable; longer training expected to reduce variance
- best_reward = -66.67 corresponds to the best rolling mean across update intervals, not a single episode
- Pipeline is fully functional: config -> env -> model -> train -> evaluate -> checkpoint save/load

## Conclusion
Pipeline verification PASS. Training converges in the right direction. Full training (500 episodes, 3 seeds) recommended for final results.
