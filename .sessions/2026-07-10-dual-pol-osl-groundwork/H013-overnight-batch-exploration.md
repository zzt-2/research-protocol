# Task Brief: 方法层增强夜间批量探索（C→B→D→E 无人值守）

> 来源: S027 续（主控对话，用户"开一个对话跑一晚上"）| 产出位置: 回传到本专题 decisions.md + results JSON
> 日期: 2026-07-16
> 唯一文档: 执行方（新对话）只拿到这一个文档 + 可读 .sessions/ + 源码

## 0. TL;DR（你先读）

你在 `/d/code/study/research-protocol`，手上有完整的 Q-CMA-FADE 方法层增强探索代码基建。

**你的任务**：按 **C→B→D→E** 顺序（A 类已 KILL，D031），逐类做方法层增强探索。每类走"GW Step 1 检索 → 四判据 → MVE"完整流程（守 FR-22，不跳步）。跑多久由你定，但**慢慢跑别跳步，跑通一类再进下一类**。

**最高纪律**（5 条，违反任何一条 = 失败）：
1. **不跳框架**：每类必须先 GW Step 1 检索（防撞车）→ 四判据 → MVE，哪怕你觉得肯定行。归类批量≠跳框架
2. **守 D031 物理教训**：训练阶段 loss/约束/数据增强触及不到 test 段 swap（A 类 KILL 根因）。子方向进 MVE 前先判"是否触及 test 段"——不触及的直接 defer 用同构论证，省算力
3. **守 D018**：任何性能结论 fixed/PI 双口径并报
4. **不改 common/**：所有新脚本隔离写在 `explore/cma-fade-divergence/prompt0{NN}_*.py`，import 复用 common/
5. **每类跑完立即写决策+落盘**：无论 Go/Kill，都要在 decisions.md 记 D### + results JSON 落盘 + 更新 topic-index 当前位置。别攒着最后一起写（防上下文丢失丢结论）

**产出**：每类一个 D### 决策记录 + 一个 prompt0{NN}_*.py 脚本 + 一个 results JSON。全类跑完后回传主控。

## 1. 背景（理解任务必需的，标"了解即可不对照评价"）

### Q-CMA-FADE 是什么

双偏振星地光通信 CMA 均衡研究。分析层已定稿（7 项稳结论，硬贡献）。方法层弱（D022：ML 在窄域 N=5M/f_G=30 的 PI-BER 优于 standard-CMA 29/30 胜 p=1.19e-6）。用户解冻方法层重新探索增强空间（D030）。

### 为什么夜间批量跑

用户要睡觉，让你跑一晚上。好处是算力时间充裕，可以慢慢把 C/B/D/E 四类穷举完。风险是无人纠偏，所以这份文档把约束写死。

### D014 核心物理（所有类都要攻的真因）

**SOP（State of Polarization）极化串扰是 CMA BER 恶化真因**：2×2 蝶形 CMA 恒模代价函数收敛点不唯一，SOP 持续旋转下权重跳到混淆 X/Y 偏振的次优解（polarization lock swap）。SOP=0 时 CMA=oracle ratio=1.0（完美），SOP>0 时 ratio 升到 1.9-6.9×。所有方法层增强的目标 = 缓解 SOP 串扰导致的 BER 恶化。

### D031 核心教训（A 类 KILL，所有类的筛选判据）

A 类（改 loss）整体 KILL 根因：**训练阶段 loss/约束触及不到 test 段 swap**。swap 发生在 test 段（block 36698+），是 CMA 在线更新跳盆地；ML 是固定权重前馈，test 段权重不更新。训练时加的 loss 正则（SOP 不变性/对比学习）学到的"SOP 不变性"泛化不到 test late 段 57° 极端旋转。**与 D027 V3（Q-DP4 形态2 约束 Kill）同构**。

**这条教训的筛选作用**：任何"只在训练阶段起作用"的改动（loss 正则/数据增强/课程学习）触及不到 test 段 swap，大概率 KILL。只有"触及 test 段"的机制（在线微调/混合架构/pilot 估计）才值得跑 MVE。

## 2. 任务详情

### 2.1 各类的具体任务

按 **C→B→D→E** 顺序（D030 成本从低到高，A 已 KILL）。

---

#### **C 类（改训练）**

**子方向 + D031 过滤**：

| 子方向 | 触及 test 段？ | 处理 |
|---|---|---|
| **C1 在线微调**（test 段周期性小步更新权重）| ✅ 是 | **跑 MVE** |
| C2 SOP 数据增强（训练扩 SOP 角度）| ❌ 否（同 A 类失败/D015 Q3-A 同构）| defer 用同构论证，不跑 |
| C3 课程学习（训练 curriculum）| ❌ 否 | defer |

**GW Step 1 检索**（只查 C1）：关键词 "online fine-tuning optical equalizer" / "online adaptation neural network optical communication" / "test-time adaptation equalization"。用 `bash tools/search`（从项目根目录）。若撞车（有人完全做过同场景同机制）→ defer 记理由。无撞车 → 进 MVE。

**MVE 设计**（C1 在线微调）：
- 复用 `prompt024_a_class_loss_variants.py` 的训练框架，但 test 段改为"每 K blocks 用最近数据微调一小步"（K 扫 [1000, 5000, 10000]，微调 lr 扫 [1e-5, 1e-4]）
- 对照：L0 baseline（固定权重，不微调）vs C1-各档
- 参数域锁定：N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK/seeds 1000-1004/late[4.375M,5M)
- **Go/Kill 预注册**：C1 任一档 mean PI < L0 且 ≥4/5 seeds 胜 p<0.05 → Go；否则 Kill
- **消融**：微调 lr=0（=不微调）得退回 L0

---

#### **B 类（改架构）**

**子方向**：

| 子方向 | 机制 | 撞车风险 |
|---|---|---|
| **B1 复值网络** | 现在是 8 实值 CNN 拆实虚部，信号物理上是复的。改 complex-valued conv | RF MIMO 成熟（查占点）|
| **B2 SOP 角度 attention** | 让网络对 SOP 旋转角敏感，attention 加权 | 查"rotation equivariant CNN optical"|
| **B3 双分支偏振分治** | X/Y 偏振分治分支，SOP 串扰本质是偏振混叠 | 查"dual branch polarization demux"|

**GW Step 1 检索**：每个子方向 2-3 组关键词。重点查 RF MIMO 均衡（复值网络成熟区）+ 光纤偏振跟踪（SOP attention 可能有人做过）。

**注意 D031 过滤**：B 类是架构改动，test 段仍是固定权重前馈。**单纯改架构不触及 test 段 swap**（同 A 类时序正交问题）。所以 B 类的合理预期是"更好的固定权重降低残余误差"而非"解决 test 段 swap"。如果检索后发现某架构能在训练时学到 SOP 不变性且泛化到 test 极端旋转（打破 D031 时序正交），那才值得重点跑。

**MVE 设计**：复用 prompt024 框架，改 `_ml_equalizer.ButterflyCNNEqualizer2x2` 的网络定义。三个架构变体 + L0 baseline 横向对比。

---

#### **D 类（CMA+ML 混合）— 成本高**

**子方向**：

| 子方向 | 机制 |
|---|---|
| **D1 CMA 跟 SOP + ML 修 swap** | CMA 在线跟踪 SOP 旋转（保跟踪能力），swap 检测后切 ML 消歧（ML 固定权重不跳盆地）|
| D2 选择性切换 | 检测到 swap 切 ML ← **注意 Q-DP4 形态1（D028）Kill 了检测+回滚，dwell=11 块。D2 要论证为什么切 ML 比回滚好** |

**GW Step 1 检索**："hybrid CMA machine learning equalization" / "CMA neural network switching"。

**成本警告**：D 类要**新写均衡器**（CMA+ML 切换逻辑），不是改 loss 或网络定义。预计实现 + 调试 2-3 小时。如果 C/B 类跑完时间还充裕（夜间还有 3+ 小时）再做 D 类。

**特殊风险（D028 阴影）**：Q-DP4 形态1 检测+回滚 Kill 根因是 swap 检测时已在 swap 盆地（dwell=11）。D1/D2 的检测同样面临这个问题——**检测到 swap 时 CMA 已在 swap 盆地，切 ML 切的是已经被污染的状态**。MVE 要验证"切 ML 后能否从 swap 盆地恢复"。

---

#### **E 类（pilot 前置）— 成本最高**

**子方向**：插 pilot 估 SOP 角度 → 前馈补偿 SOP → 再均衡。

**GW Step 1 检索**："pilot-aided SOP estimation optical" / "pilot-aided polarization tracking"。

**成本警告**：E 类要**新写 SOP 估计器**（pilot 插入 + 估计 + 补偿），成本最高。**只有 C/B/D 全跑完且时间充裕才做 E 类**。

**特殊价值**：E 类是最不同的一条路——不攻均衡器本身，攻上游 SOP 估计。D014 证明 SOP 是真因，那直接估 SOP 补偿掉比在均衡器里绕更上游。如果能成，这是最有方法论新意的方向。

### 2.2 执行方式（每类的标准流程）

**严格顺序，不跳步**：

```
对每个类（C→B→D→E）:
  1. GW Step 1 检索（5-15 min）：bash tools/search 查撞车
     - 撞车（完全有人做过同场景同机制）→ defer，记 D###，进下一类
     - 无撞车 → 继续
  2. D031 过滤：子方向是否触及 test 段？
     - 不触及（训练阶段 loss/数据增强/课程）→ defer 用同构论证，进下一子方向或下一类
     - 触及 → 继续
  3. 四判据（快判，不写长报告）：
     - 具体技术矛盾（攻 D014 SOP 真因）？
     - 有方法产出形态？
     - 有 baseline（L0/D022 锚点）？
     - 能做对比？
     - 全过 → 继续；任一不过 → defer
  4. MVE 实现：新建隔离脚本 prompt0{NN}_*.py（不改 common/，import 复用）
  5. MVE 运行：5 seeds + 消融 + 双口径（D018）
  6. Go/Kill 判定：对照预注册判据
  7. 落盘：results JSON + decisions.md 记 D### + 更新 topic-index 当前位置
  8. 进下一类
```

### 2.3 产出格式（强制，每类完成后立即写）

**决策记录**（decisions.md 追加 D###）：
```markdown
## D###: {类名}（{子方向}）{Go/Kill}

> status: active
> date: 2026-07-16
> 依据: 验证: results/cma-fade-divergence/prompt0{NN}_*.json + GW Step 1 检索 search-archive/2026-07-16/

### 决策
{一句话 Go/Kill}

### 核心数据
{mean PI / 胜场 / p 值 / 消融}

### 检索结果
{撞车评估}

### 触发原话
> 触发原话: 无（夜间批量探索，H013 派发；结论来自数据验证非用户态度）
```

**topic-index 当前位置更新**：每类完成后把"当前类"推进一格。

## 3. 已知陷阱（基于历史失败的具体案例）

### 陷阱 1：跳检索直接跑（FR-22 / TL-30）

**症状**：觉得某方向肯定没人做过，跳过 GW Step 1 直接写代码跑 MVE。
**后果**：撞已有方法 = 换皮，论文被毙。A3 VAE 就是检索才发现 Qin 组 2026 TCCN 硬撞车。
**防线**：每类第一步必须 tools/search，哪怕 5 分钟。

### 陷阱 2：D031 时序正交重蹈（A 类 Kill 根因）

**症状**：C2 SOP 数据增强 / C3 课程学习 / 纯 B 类架构——都是训练阶段改动，触及不到 test 段 swap。
**后果**：跟 A 类一样 KILL（floor 效应 + 时序正交）。
**防线**：子方向进 MVE 前先问"这个改动 test 段起不起作用"。不起作用 defer。

### 陷阱 3：fixed/PI 单口径（D018）

**症状**：只报 fixed-label BER 或只报 PI-BER。
**后果**：fixed BER swap 后≈0.5（标签错配），单看 fixed 会误判 ML 全崩；单看 PI 会忽略消歧开销。
**防线**：任何性能结论双口径并报。复用 `prompt012_longseq_audit.evaluate_outputs`。

### 陷阱 4：改 common/（隔离原则）

**症状**：直接改 `_ml_equalizer.py` 或 `_cma.py` 加新功能。
**后果**：破坏已有验证结果的可复现性（D020 就是 current-CMA 缺 z 因子导致基线混杂）。
**防线**：所有新代码写 `prompt0{NN}_*.py` 隔离脚本，import 复用 common/。

### 陷阱 5：攒着最后一起写（上下文丢失）

**症状**：跑完 C/B/D/E 四类，最后一起写决策。
**后果**：上下文压缩/超时，中间类结论丢失。
**防线**：每类跑完立即写 D### + 落盘 JSON + 更新 topic-index。

### 陷阱 6：floor 效应误判（D031）

**症状**：5 seeds 里 3/5 clean seeds PI≈0（floor），只看均值发现"没改善"。
**后果**：误判 Go/Kill。clean seeds 本来就完美，只有 swap-prone seeds（1000/1002）有改善空间。
**防线**：看 per-seed 分布，不只看均值。改善要看 swap-prone seeds 的 PI 降没降。

## 4. 验收（你跑完后主控怎么检查）

- [ ] 每类一个 D### 决策（Go/Kill/defer 明确）
- [ ] 每类一个 prompt0{NN}_*.py 隔离脚本（不改 common/）
- [ ] 每类一个 results JSON（5 seeds + 消融 + 双口径）
- [ ] GW Step 1 检索记录（每类 search JSON 在 search-archive/2026-07-16/）
- [ ] topic-index 当前位置已推进
- [ ] D031 时序正交过滤有体现（defer 的子方向标了理由）
- [ ] 全类跑完有总结（哪类 Go/哪类 Kill/整体方法层结论）

## 附：代码基建速查（复用，别重写）

| 基建 | 路径 | 用途 |
|---|---|---|
| 信道生成 | `explore/cma-fade-divergence/ml_long_seq_failure.py` 的 `gen_channel` | 双偏信道 + SOP 旋转 + GG 衰落 |
| oracle 下界 | 同上 `oracle_equalize` | 完美 CSI 线性接收机下界 |
| standard-CMA | `explore/cma-fade-divergence/prompt019_mu_compress_mve.py` 的 `StandardCMA2x2` | Godard 1980 含 z 因子 |
| ML 均衡器 | `common/_ml_equalizer.py` `ButterflyCNNEqualizer2x2` + `MLEqualizer` | Qin 2025 CNN 架构 + MSE 监督训练 |
| 双口径评估 | `explore/cma-fade-divergence/prompt012_longseq_audit.py` `evaluate_outputs` | fixed/PI BER + 2!×4×4 消歧 |
| A 类横向对比框架 | `explore/cma-fade-divergence/prompt024_a_class_loss_variants.py` | λ 扫描 + 甜点选择 + 配对 Wilcoxon + 自定义训练循环（C/B 类改这里）|
| SOP=0 矩阵 | `prompt023_sop0_matrix.py` | D014 复现（参考撞车判据）|

**参数域锁定**（所有类一致）：N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK/seeds 1000-1004/late[4.375M,5M)。这是 D022 域，可复现。

**Python**：`/c/Users/zzt/scoop/apps/python311/current/python`（3.11 torch2.6.0+cu124 CUDA RTX4070）

## 附：必读文件（进新对话后按优先级读）

1. **本文件**（H013）— 你的任务书
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D030（解冻+候选地图+准入）+ D031（A 类 Kill 教训+时序正交）+ D014（SOP 真因）+ D022（baseline 数据）
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md` 当前位置 + 不变量 8 条
4. `stages/groundwork.md` Step 1 检索 + Step 4a 四判据段（FR-22）
5. `projects/simulation/common/_ml_equalizer.py`（ML 基建，改架构看这里）

## 附：产出回传位置

- 决策记录 → `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` 追加 D032+
- 脚本 → `projects/simulation/explore/cma-fade-divergence/prompt025+.py`
- 结果 → `projects/simulation/results/cma-fade-divergence/prompt025+.json`（gitignored）
- 检索 → `search-archive/2026-07-16/`
- topic-index → 更新当前位置段
- session note → `.sessions/2026-07-10-dual-pol-osl-groundwork/S028-{slug}.md`
