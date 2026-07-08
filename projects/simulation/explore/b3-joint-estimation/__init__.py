"""B3-Q2 子系统协同联合估计 explore 包（INVARIANT 14，不进 common）。

5 个新建代码接口（_fair_comparison_framework.md §0.6.2）:
    ① mrc_combiner.py — MRC 合并器
    ② frame_sync_fsts.py — 帧同步 FSTS 相关峰
    ③ multi_branch_phase_precorr.py — 多支路相位预校正
    ④ joint_estimation_pipeline.py — 联合估计管线（核心，M1/M2/M3）
    ⑤ multi_aperture_channel.py — 多望远镜信道扩展

参数: _b3_params.py（B3Params + B3SandboxConfig）
"""
