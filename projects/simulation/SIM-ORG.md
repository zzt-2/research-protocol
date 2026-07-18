# 仿真代码组织规范（SIM-ORG）

> 本文件是 `projects/simulation/` 下的**代码组织规范**（目录结构 + 文件命名 + 结果存放 + 探索目录契约）。
> **拥有者**：本文件（组织规范的唯一完整定义）。SPEC.md 是仿真物理真相源，本文件是代码组织规范，职责分离。
> **关系**：继承并细化 `2026-06-12-simulation-foundation-rebuild` 冻结的"域层扁平模块化 + params.py 单一真相源"方案，补齐该方案未覆盖的 explore/experiments 内部组织、代码-结果分离、README 契约。
> **创建**：2026-07-11，起因 Q-CMA-FADE 进 MVE 前定组织（D005 候选合并后）。

---

## 1. 核心原则（5 条，不可违反）

| # | 原则 | 理由 |
|---|------|------|
| **P1** | **代码和结果物理分离** | explore/ 历史教训：py 和 json 混放导致 200+ 文件无法分辨。新代码一律 `*.py` 旁不放结果，结果进 `results/` |
| **P2** | **每个探索目录必须有 README.md** | explore/ 历史教训：b2/b5/b7 等无 README，无法分辨属于哪个方向、是否 Kill、脚本间关系 |
| **P3** | **参数单一真相源 = params.py** | foundation-rebuild 已冻结。新方向扩 params.py，不在脚本里硬编码物理参数（FR-20 参数溯源） |
| **P4** | **公共模块只扩不改** | foundation-rebuild 已冻结。新算法 = 1 个新文件 + 0 改动现有 common/ 代码 |
| **P5** | **探索脚本标注方向 + 状态** | 每个脚本头部 docstring 标 `方向: Q-CMA-FADE / 状态: WIP|MVE-PASS|KILL`，便于分辨死活 |

---

## 2. 目录结构规范

```
projects/simulation/
├── common/                        # 公共包（已模块化，冻结。只扩不改——P4）
│   ├── __init__.py                #   向后兼容重导出
│   ├── _config.py                 #   常量（真相源 params.py）
│   ├── _channel.py                #   GG 信道 / Doppler / 共享实现
│   ├── _modulation.py             #   QPSK/16QAM/8APSK + ber_eval
│   ├── _recovery.py               #   fft_foe / dpll / vv_cpr / bps_cpr
│   ├── _equalizer.py              #   MMSE 均衡
│   ├── _kf.py                     #   Kalman 滤波
│   └── _experiment.py             #   run_* 编排 + save_results
│
├── params.py                      # 参数单一真相源（Pydantic，冻结——P3）
├── SPEC.md                        # 仿真物理真相源（信号模型/参数/方法表）
├── SIM-ORG.md                     # ★ 本文件（代码组织规范）
├── README.md                      # 项目导航（结构说明 + 脚本索引）
│
├── explore/                       # 探索类（MVE 前的可行性验证 + 消融）
│   ├── [方向-slug]/               #   每个探索方向一个子目录
│   │   ├── README.md              #     ★ 强制（P2）：MVE 契约 + 脚本关系
│   │   ├── *.py                   #     实验脚本
│   │   └── (不放结果——P1)
│   ├── cma-fade-divergence/       #   Q-CMA-FADE（新建）
│   ├── nda-awgn-tracking-sandbox/ #   A4 历史（不动）
│   ├── b5-leo-doppler-spectrum/   #   A4 历史（不动）
│   └── ...                        #   其余历史 explore 不动
│
├── experiments/                   # 正式实验（MVE PASS 后从 explore/ 升级到这里）
│   └── *.py
│
├── results/                       # ★ 结果集中（P1）
│   ├── [实验名]/                   #   按实验分子目录
│   │   ├── *.json                 #     数据
│   │   └── *.png                  #     配图（或进 figures/）
│   └── ...
│
├── figures/                       # 图表输出（论文级，带风格审查）
├── tests/                         # 测试（pytest）
├── verify/                        # 验证脚本（6 类验证）
└── archive/                       # 归档（废弃文件索引）
```

### explore/ vs experiments/ 的区别（重要）

| | explore/ | experiments/ |
|---|---|---|
| 阶段 | MVE 前（可行性/消融） | MVE PASS 后（正式对比实验） |
| 脚本性质 | 快速验证、可能 throwaway | 稳定、可复现、进论文 |
| 升级路径 | explore/ →（MVE PASS）→ experiments/ | — |
| 文件命名 | 自由（建议 `_` 前缀表内部辅助脚本） | `sim_[方法]_[场景].py` 规范命名 |

**一个方向的代码生命周期**：
```
新方向 → explore/[slug]/ 写 MVE 脚本
  → MVE PASS → 脚本升级到 experiments/ + 结果进 results/
  → MVE FAIL/KILL → explore/[slug]/ 保留 + README 标 KILL（归档不删，留教训）
```

---

## 3. 探索目录 README 契约模板（P2 强制）

每个 `explore/[方向-slug]/` 必须有 `README.md`，格式：

```markdown
# [方向名] 探索

> 方向: Q-CMA-FADE | 来源: D005 | 状态: WIP | 创建: 2026-07-11

## 研究问题
M-C-A 一句话 + 四判据过否（链 literature_notes Q# 条目）

## MVE 契约（FR-11）
- 动作空间: ...
- 决策粒度: ...
- 对比范式: vs 传统 CMA
- 奖励/测度: 发散概率 + BER + 收敛速度
- 先验 baseline（FR-14）: 固定 CMA
- 贡献目标 baseline（FR-15）: Qin VAE / Nasr ANN

## 脚本清单
| 脚本 | 用途 | 状态 | 结果位置 |
|------|------|------|---------|
| mve_cma_vs_ml.py | CMA vs ML 均衡深衰落对比 | WIP | results/cma-fade-divergence/ |

## 参数溯源（FR-20）
关键物理参数来源（标文献），不硬编码。
```

---

## 4. 结果文件存放规范（P1）

### 命名
- JSON: `results/[实验名]/[脚本名]_results.json`
- 图表: `results/[实验名]/[脚本名]_[描述].png` 或 `figures/`（论文级）
- 绝不在 `explore/[slug]/` 下放 json/png

### 实验名约定
按 `[方向]-[子实验]`，如 `cma-fade-divergence/divergence-prob-scan`。

### 结果索引
results/ 顶层维护 `index.md`（可选），记录每个结果目录对应的实验/脚本/方向。

---

## 5. 新方向起步清单（Q-CMA-FADE 示例）

新方向进 MVE 前做这几步：

- [ ] 建 `explore/[方向-slug]/` 目录
- [ ] 写 `explore/[方向-slug]/README.md`（按 §3 模板，含 MVE 契约 FR-11）
- [ ] 确认参数进 `params.py`（不在脚本硬编码，FR-20）
- [ ] 确认复用的 common/ 模块（缺的扩新文件，不改现有——P4）
- [ ] 建 `results/[方向-slug]/` 结果目录
- [ ] 每个脚本头部 docstring 标方向 + 状态（P5）
- [ ] 读 `code-quality.md` 必做清单 + `reference/sim-template/` 对应模板

---

## 6. 历史代码处理策略

**不动历史，只管新的**（用户 2026-07-11 决策）：
- explore/ 下 b2/b3/b5/b7/b11/nda-awgn 等历史目录 = A4 线和已 Kill 方向，保持原样
- thesis-figures/simulation/（SPEC.md 标"已废弃"）= 历史遗物，新代码不往那写
- 新代码一律进 `explore/cma-fade-divergence/` + `results/cma-fade-divergence/`

历史代码如需复用结论，先查 `archive/README.md` 的废弃/参考/已替代标记，不直接引用未重验的结果。

---

## 7. 与已有规范的关系

| 已有规范 | 来源 | 本文件关系 |
|---------|------|-----------|
| 域层扁平模块化 | foundation-rebuild S002（冻结） | **继承**，§2 目录结构基于此 |
| params.py 单一真相源 | foundation-rebuild | **继承**，P3 |
| sim-template 12 文件模板 | reference/sim-template/ | **引用**，新方向起步读模板 |
| code-quality 必做清单 | code-quality.md | **引用**，§5 起步清单 |
| SPEC.md 物理真相源 | projects/simulation/SPEC.md | **互补**，SPEC 管物理，本文件管组织 |
| execute.md 实验流程 | stages/execute.md | **对齐**，MVE/实验阶段定义一致 |

本文件不重复上述内容，只补它们**未覆盖的**：explore/ 内部组织、代码-结果分离、README 契约模板。
