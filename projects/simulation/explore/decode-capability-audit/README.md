# decode-capability-audit

PROMPT-026 / R036 任务二：译码块两个从未测过的算法轴，在 decode-failure-rescue
冻结 LLR 缓存（三个独立确认批 M15/W12/S16 × 2048 帧 = 6144 帧）上的首批诊断。

## 诊断

- **A 译码能力 oracle**：SPA（Sionna `cn_update_phi`，boxplus/phi 精确和积更新）
  × {20,50,200} 迭代 vs NOMS(0.75,0)×20（冻结基线），另加 NOMS×{50,200}
  迭代对照分解"迭代轴 vs 算法轴"。按每帧 pre-decode 硬判决错误数 e0 四分位
  分层（深衰/边际/好帧）。
- **B NOMS 配置网格**：α∈{0.75,0.8125,0.875,0.9375}×β∈{0,0.05,0.1,0.15}
  ×20 迭代 × 三条件。量"逐条件最优 vs 全局固定"的 headroom（H1/H2/H3）。

## 判读（预注册，运行前冻结）

合同 `contract.yaml`（FROZEN_BEFORE_EXECUTION）。核心规则：
- A：ΔFER(B0−SPA200) 三条件全部 CI95 上界 < +0.005 → 译码算法能力轴闭死
  （NOMS-20 已贴 BP 家族能力上缘，"深衰=信息丢失"升级为测量结论）；
  任一条件 CI95 下界 > +0.005 → 量活。
- B：H1（B0−逐条件最优）三条件全部 CI95 上界 < +0.005 → 配置空间轴闭死。
- oracle 只作 Kill 工具与 headroom 度量（FR-21/TL-32）；失败不调参追正；
  每诊断最多 2 轮设计—运行—诊断。

## 纪律

- **零改动** `decode-failure-rescue/` 任何原文件——本模块只读 import
  `rescue_decoder`（同一 encoder/引擎构造/坐标映射），只读 llr_cache npz。
- 真值（truth_info/truth_coded）只进评分与 e0 分层，不进任何译码臂内部。
- 实现门（读任何结果前）：B0 在缓存上与 raw_confirm*.json 逐帧 bit 级一致；
  SPA stepped==单发 fresh（flooding 无状态性）；SPA200 在 4 个 B0 干净帧零错。

## 运行

```bash
cd projects/simulation/explore/decode-capability-audit
python run_audit.py --diagnostic capability   # -> results/decode-capability-audit/raw_capability.json
python run_audit.py --diagnostic grid         # -> results/decode-capability-audit/raw_grid.json
python summarize.py                           # -> summary.json（判读+分层+CI）
```

环境：`sionna==2.0.1`（make_encoder 强制校验）、torch CPU、numpy。
