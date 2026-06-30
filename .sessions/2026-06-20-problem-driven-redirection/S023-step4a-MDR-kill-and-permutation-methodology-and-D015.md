# [S023] 块 E Step 4a 重激活——AO+MDR MDR 侧 Kill + "排列组合"方法论讨论 + 立 D015 顶刊 baseline 溯源法

> 2026-06-30 | 块 E Step 4a + 方法论迭代 | 状态：MDR Kill，D015 方法论定稿，载波同步切入待执行
> 续接 H014（用户拍"你继续吧"授权 Step 4a 评估）

## 目标

续接 H014，块 E Step 4a 重激活，**首评 AO+MDR MDR 侧**（4 个 C 候选里数值最强但 A1 归属最大未知）。守 D009 checklist + §7.2 防造假 + 判 C≠立 Q#（FR-22）。

## 记录

### 1. AO+MDR MDR 侧 D009 checklist 评估

**前置 0 范围硬门**：✅ PASS（GEO 星地 + MDR 接收端处理 S007 边界内）。

**🔴 A1 方法归属 FAIL**（两种解释都不过）：
- 证据（§7.2 grep 核查 `papers/downloads/2026-06-26/11185295.md`）：论文贡献=机制/表征研究（abstract L7 "systematically investigate... a novel finding: mutually weakening/enhancement"），**不是提出 MDR**。MDR 在本文=**纯硬件功率求和**（L117/L123 "MDR(SUM3)=summed power of first n ports of the PL"，无 DSP 无合并算法）。9.1dB 是端口功率相加的硬件 diversity 增益
- 解释 A（窄义，改进论文 MDR）：论文 MDR 是硬件 PL 求和，我们做 DSP 合并=新提算法，不是改进 → A1 不过（Q1/Q2/Q3 死法同构）
- 解释 B（宽义，MDR 自适应合并 gap）：**补检索证 gap 被占**——3 次 tools/search 命中 2019/2020/2024 多篇直接 on-point：
  - 2019 Opt.Commun. "Adaptive digital combining for coherent FSO with **spatial diversity**"（"novel adaptive digital combining algorithm... eliminate time-varying channel fading estimation"）
  - 2020 Opt.Commun. "Low-complexity parallel real-valued weight adaptive digital combining for coherent FSO **modes diversity**"
  - 2024 Adv.Fiber Laser Conf. "Real-time implementation of **selection combining algorithm** for **mode diversity** FSO coherent"
  - **gap 不存在**：自适应按信道状态调合并权重 2019 起就是个有人做的方向，连 mode diversity 都覆盖了
- A2/A3/B/C 无需再判（A1 硬门槛已挂）

**初判 Kill AO+MDR MDR 侧**（D016）。判地 C 不变——MDR 物理有 9.1dB 信号（地有缝），但缝被别人填了不是我们的机会。**判地判"地有缝"≠找方向判"缝是我们的"，两件事分离**（H011 纪律 1）。

### 2. 🔴 用户"排列组合"方法论讨论（本轮核心，用户主导）

Kill MDR 后，用户提："既然别人做过，那我们是不是能排列组合？…类似地，别的方向，别人做过不少的，看看别人都怎么排列组合的，我们也排列组合？"——触发方法论讨论。

**主线 v1 校正（教条）**：主线把"排列组合"判成方法驱动=TL-30 跳步危险，提"找被批密度高的 baseline 不是找热门"。

**用户 push back（校正主线）**："做得多，那才说明我容易稍微搞一点点差别水一个出来啊？做得少，我都没有参考，很容易出问题的。"——**戳穿主线 v1 把"做得多"误读红海**。主线认错：TL-12 第 4 条明文"别人做过我们延伸=出 bug 概率低"，主线 v1 只读前半段（红旗）忽略后半段（延伸路线）。

**主线 v2 定稿（吸收用户洞察）**：
- 核心判据：**领域做得多 ✅ + 具体点没被占 ✅ = 最优**（要的"容易水"形态）
- "做得多"是优势（参考足、验证基准多、出 bug 低、导师接受）不是劣势——中文学位论文语境
- "做得少"才是危险（没参考、易翻车）
- MDR 死因不是"做得多"，是"adaptive combining 这个具体点被 2019+ 占完"

**立 D015「顶刊 baseline 溯源法」**（5 步流程 + 4 档判读表 + 5 条红线，详见 decisions.md D015）。这是 D005/TL-04/TL-12/S010 的**合成执行流程**，FR-24 grep 确认是新的（不是方法论边界重复，是执行方法合成）。

**方法论讨论的副产物**：TL-31 追加第 4 次复现——主线差点新建"排列组合方法论 D###"，FR-24 grep 发现已覆盖。新增教训：①主线在"务实"维度偏严苛是反复偏差（D007+本次）②用户直觉在"务实 vs 严苛"多次校正主线 ③真正该立 D### 的是执行方法合成不是边界重复。

### 3. 载波同步切入授权 + 边界（用户拍"慎重"先规划不立刻检索）

用户拍"先试试载波同步？这玩意做的人那可太多了"+ "先把方法论落下来"+ "慎重"。

**为什么载波同步符合 D015 选锚标准**：
- 领域做得多 ✅（PLL/OPLL/DPLL 是经典，批 2 有 4 篇 + TS-KF/CPR 等大量积累）
- 批 2 判地结论"有缝但人少"=具体点**没占满**（领域热但缝还在）——这正是 D015 第 1 档最优形态
- 跟开题方向（DPLL）对得上，导师接受度高

**载波同步 D015 溯源执行边界**（待 H015 交接下一对话执行，本轮不跑）：
1. **选锚**：近年顶刊（JLT/OE/TCOMM/PTL 2022+）一篇载波同步 baseline（PLL/OPLL/DPLL/FOE），做得多。候选锚：批 2 已落盘的 OPLL（10.3390_photonics10121312）/ FOE FSTS（10.1109_jphot.2023.3265847）/ DPLL（10.1109_jlt.2020.3003561）/ RSOP（10.1109_LCOMM.2026.3651445）——先选 1 个
2. **拉引用网络**：锚的引用列表（20-50 篇），筛批/改进锚的
3. **🔴 具体点占住检查**：找还没被占的具体点（批 2"有缝但人少"的精确 gap——OPLL 湍流相位+piston+多普勒联合建模无人占，是候选）
4. **精读 ≤5 篇验证**（不漫灌）
5. **对标 D009**：活缝过 A1/A2/A3 才立 Q#

**红线继承 D015**：①做得多✅但具体点没被占 ②≤5 篇不漫灌 ③A1 归属真边界 ④顶刊锚 2022+ ⑤先回答"为什么这个点没人填"（TL-04）

## 决策引用

- **D015（新建）**：顶刊 baseline 溯源法（务实路线选向执行方法）
- **D016（新建）**：Kill AO+MDR MDR 侧（A1 FAIL + gap 被 2019+ 占）
- 引用 D005（务实路线）/ D009（checklist）/ TL-04（空白查为什么）/ TL-12（做得多=延伸路线✅）/ TL-30（禁方法驱动）/ TL-31（第 4 次复现）
- 判地 C（D014）不变——MDR Kill 不否定地有缝，是找方向判缝不是我们的

## 范围确认

- 本轮是否在 scope boundary 内：**是**（Step 4a 评估 + 方法论迭代都在 D013/D014 既定路径内，不立 Q# 守住，AO 分开标守住，D015 是 D005 执行方法补全非范围扩张）

## 后续

**下一对话执行 H015（载波同步 D015 溯源）**：
1. 报到 + 读 D015/D016 + 载波同步执行边界
2. 选锚（载波同步近年顶刊 baseline）
3. 拉引用网络 + 具体点占住检查 + ≤5 篇精读
4. 对标 D009 → 立不立 Q# 报用户

**🔴 给下一对话的提醒**：
- **慎重**（用户原话）：先选锚定边界再检索，不漫灌
- 载波同步批 2"有缝但人少"是 D015 第 1 档最优形态的候选，但具体点占住检查必须做（别重蹈 MDR"领域热但点被占"覆辙）
- 剩 3 个 C 候选（OAM/OQAM/阵列）暂挂，载波同步溯源完再回头评（用户重心在载波同步）
- D015 红线 5：先回答"为什么这个具体点没人填"（OPLL 联合建模无人占是因为硬件门槛还是真遗漏，要查）