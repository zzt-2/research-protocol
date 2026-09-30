# decode-budget-rule

PROMPT-028 / R038：迭代预算判决规则第一轮有界验证。在 decode-failure-rescue
冻结 LLR 缓存上，用接收可见的 syndrome 轨迹设计"无望帧提前中止 + 边际帧烧满
cap=200"的判决规则，目标 = cap200 档 FER（损失 ≤0.2pp）+ 接近 cap50 档的
平均迭代（16~19）。任务二（Pareto 左半支 cap10/cap15）从同一轨迹日志离线读出。

## 纪律（合同 `contract.yaml`，FROZEN_BEFORE_EXECUTION）

- 规则族 5 族 × 28 候选预注册；检查点 {20,30,50,100}；窗口 k=8；
  选择准则（W_pooled ≤ 2 且每批 W ≤ 1 下最大节省）预注册。
- dev 4 批（dev 64 / dev_M14 512 / dev_W12 512 / dev_S16 512 = 1600 帧）
  只做设计与阈值选择；三确认批在规则冻结后单次运行只评分，不回流设计。
- 实现门（读任何结果前）：G1 首 20 迭代 syndrome 与 raw_*{batch}.json 的
  B0 轨迹逐位一致（7 批全帧）；G2 确认批 converged_at + ie200 与
  raw_capability.json NOMS200 臂逐帧一致（6144/6144）。
- 真值只进评分与标签外构造（converged_at 本身接收可见）；特征全部接收可见。
- 失败不调参追正；oracle（dev 标签）只作选择与风险标注；≤2 轮。

## 运行（顺序固定：dev → 选择冻结 → confirm 单次 → 提取 → 评分）

```bash
cd projects/simulation/explore/decode-budget-rule
python run_trajectory.py --split dev       # -> results/decode-budget-rule/raw_traj_dev.json
python select_rule.py                      # -> frozen_rule.json（28 候选选择表）
python run_trajectory.py --split confirm   # -> raw_traj_confirm.json（冻结后单次）
python extract_iterates.py                 # -> raw_iterates_confirm.json（amend v1.1 度量提取 + 任务二 ie@{10,15}）
python score_confirm.py                    # -> summary.json（双口径 Pareto+判读）
```

环境：sionna==2.0.1（make_encoder 强制）、torch CPU、numpy、scipy。
Windows 本机：`C:\Users\zzt\.venvs\torch\Scripts\python.exe`。

## 结果（2026-09-27 首轮）

冻结规则 RC_120（检查点 {20,30,50,100} 处 syndrome 水平 ≥120 即砍）。
verdict = **KILL**（双口径一致）：FER 损失 +0.24/+0.49/+0.34pp 三条件全部
>0.2pp 门（主死因 = W12 错砍率 dev→confirm 迁移失败 1/512→10/2048）；
成本机制量活（平均迭代 53.8-58.3 → 14.6-18.2，−72~73%，p≈1e-134）。
详见 R038。

## 零改动声明

本模块零改动 `decode-failure-rescue/`、`decode-capability-audit/` 与一切旧
raw/冻结模块：只读 import `rescue_decoder`，只读 llr_cache npz 与锚点 JSON。
