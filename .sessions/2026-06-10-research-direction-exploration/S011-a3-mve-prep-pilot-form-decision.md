# [S011] A3 MVE 前置准备 — Li 2019/Cheng 2014 精读（PAPU 公式三缺）+ Pilot 形态对照决策

> 2026-06-17 | 阶段: Groundwork §4a 维度 D（MVE）前置 TL-22 验证 | 状态: MVE 假设表定稿待 Cheng 2013 结果，pilot 形态决策定（MVE 做对照实验）
> 来源: H006（A3 进维度 D MVE handoff）+ 用户压缩后续接 | 方法: 2 子 agent gw-read（Li 2019 + Cheng 2014）+ 主对话分析

## 目标

承接 H006，启动 A3 §4a 维度 D（MVE）。本轮目标：**MVE 前置 TL-22 物理前提验证**（精读 BC-4 关键论文 Li 2019 + 其算法来源 Cheng 2014，确认 PAPU 可复现性）+ **MVE 假设表定稿**（含 pilot 形态选型）+ **explore 目录 + 自包含 README 建立**（用户要求）。本轮**不执行 MVE**（MVE 是子 agent 任务，下一轮做）。

## 记录

### 接收 H006 验证（Trigger 5 完成）

3 条关键事实声称全 PASS：
- A3 四维度全过（S009 维度进度表确认）
- BC-4 = phase unwrap cycle slip（D006 BC-4 行 + S009 A0-5）
- 性能间隙 2.3dB[实证]（本轮直读 Paillier content.md:200 "2.3 dB power penalty at a BER=10⁻⁴" 精确吻合；L190 +5dB / L196 negligible / L206 open-loop 呼吁 全部 verified）

无 FAIL，scope 在 D001 后续阶段链 Groundwork §4a 维度 D 内，未碰 Contract/Execute/仿真正式环境。

### MVE 假设表初稿 + 用户决策（AskUserQuestion #1）

**用户决策（2026-06-17）**：
1. **MVE 物理保真度 = 方案 B（Paillier 复现）**——重新生成 σ²_I=0.684 deep fade 时序，pilot CPE + PAPU vs AGC+DPLL，6-8h
2. **代码必须放 `/explore/xxxx/` + 自包含 README**（"哪怕完全没有上下文也能进行不同实验代码的整合"）
3. **先派子 agent 精读 Li 2019**（TL-22 物理前提验证）

### TL-22 验证执行（2 子 agent gw-read）

**子 agent 1（Li 2019 精读）**：写入 `papers/_read_notes/li2019-papu-cycleslip.md`，PDF 落盘 `papers/manual/li2019-papu-cycleslip/source.pdf`（3.5MB）。

**子 agent 2（Cheng 2014 精读）**：写入 `papers/_read_notes/cheng2014-papu-source.md`，全文经 docksci mirror（Optica Gold OA 镜像）抓取。

### ✅ 关键发现 1：PAPU 公式三次缺失后第三次（Cheng 2013 原始文）获完整公式 — TL-22 红线解除

| 来源 | 给了什么 | 缺什么 |
|---|---|---|
| **Li 2019**（应用层）| VVPE 公式 $\hat\theta_{VV}=\frac{1}{M}\arg(\sum r_k^M)$ + Fig 2b 流程图 | unwrap 算子 / CS 检测判据 δ / CS 修正公式 **全缺**，指向 Cheng refs |
| **Cheng 2014**（应用层 OE）| 信号模型 Eq.(1)(2) + 文字描述 + Fig 1(a) 框图 | unwrap 算子 / CS 检测判据 / CS 修正公式 **同样全缺** |
| **✅ Cheng 2013**（PAPU 原始提出，OE 21(19) DOI 10.1364/OE.21.022166）| **Eq.(1)-(5) 5 个公式全部精确抄到** | 无缺（完整）|

**实证数字 verified**（场景：光纤无湍流）：
- Li 2019: 0.78% pilot + LDPC(1.46,1)+RS(255,239)，filter length 8/16/20 时 PRE-FEC OSNR gain 3.1/1.3/0.6 dB，POST-FEC OSNR gain 3/1/0.5 dB
- Cheng 2014: 0.39% pilot + BPS+PAPU，30 Gbaud QPSK + 4 MHz 等效线宽，BER=1e-3 处 SNR penalty < 1 dB，优于 differential coding
- **Cheng 2013: 1.56% pilot overhead + 10 Gbaud DP-16QAM + 6 MHz linewidth + JP-CPE+PAPU，BER<2×10⁻² @ 15dB OSNR，CS 概率<10⁻³ @ OSNR≥16.5dB/2.4MHz，优于 FWBW 和差分编码**

**Cheng 2013 PAPU 完整公式（M1a 直接用）**：
- Eq.(1) 信号模型：$s(k) = c(k)\exp(j\theta(k)) + n(k)$，θ 为 Wiener
- Eq.(2) Pilot 相位估计：$\hat\phi(m) = \arg(\sum_{i=0}^{P-1} d^*(i)\cdot s(mP+i))$
- Eq.(3)(4) Unwrap 算子：标准 numpy.unwrap 等价（rng·f_rng，QPSK partitioning rng=π/2）
- ⭐ **Eq.(5) CS 修正核心公式**：$\hat\phi^u_k = \hat\phi^{0,u}_k - \text{round}[(\hat\phi^{0,u}_k - \hat\phi'(k))/2\pi]\cdot 2\pi$
- CS 检测三层阈值：π/2（round 边界）/ π/3（工程防 false fluctuation）/ π/2（仿真统计）

**抓取路径**：sci-hub.ru 镜像（Optica 直连被 Cloudflare JS challenge 封，无 PMC 仓库镜像）。若未来重抓路径相同。

### ⚠️ 关键发现 2：Pilot 形态不匹配但 PAPU 可机械迁移（Cheng 2013 修正了 Cheng 2014 note 的过度悲观）

| Pilot 形态 | 代表 | unwrap 机制 | 与 A3 设想关系 |
|---|---|---|---|
| **frame-header pilot / 时域 symbol pilot** | Cheng 2013 / Li 2019 / Cheng 2014 | 离散锚点 + 两点间插值；CS 检测靠 pilot 间相位差突变 | A3 设想**不是这个** |
| **频域连续 pilot tone** | A3 设想 / PASC 路线 | 连续相位参考；CS 检测靠 tone 相位瞬时跳变或 SNR 跌破 | A3 设想**是这个** |

**判定修正（Cheng 2013 结果驱动）**：
- Cheng 2014 note 曾担心"频域 tone 不能机械迁移 PAPU"——基于 Cheng 2014 没公式的推测
- **Cheng 2013 Eq.(5) 实际可机械迁移到频域 tone**：Eq.(5) 是 symbol-by-symbol feedforward 修正，不依赖两 pilot 间插值的具体形态（插值只是给 $\hat\phi'(k)$，频域 tone 直接替换为连续 pilot 相位即可，反而更简单不需插值步骤）
- ⭐ **PAPU 思想 + Eq.(5) 公式均可迁移 A3，BC-4 名义可上**

**重要副作用不变**：频域连续 tone 是 **PASC 路线特征**（D006 BC-1）。A3 设想频域 tone + 数字前馈 CPE 与 PASC 频域 tone + 光域自共轭补偿**形态相同，仅后端不同**。BC-1 区分须更精细——不是"形态区分"而是"数字 vs 光域"。

### 💡 关键发现 3：A3 非平凡性反而增强

连续两个来源不给 PAPU 公式这件事，反向证明 A3 不能 trivial 重做：
- 若 A3 用频域 tone + 自行设计 CS 应对（不借 PAPU），就是真正的"前馈 CPE 在湍流 FSO 的 cycle slip 应对"原创设计
- 避开"PASC 路线"和"PAPU 机械迁移"两个陷阱
- 符合 D001 E 三检验的"非平凡性"维度

### 用户决策（AskUserQuestion #2）

**用户决策（2026-06-17）**：
1. **MVE 做形态对照实验**——同时跑时域 symbol pilot + 频域连续 tone，数据决定 A3 pilot 形态选型
2. **再派子 agent 查 Cheng 2013 原文**（拿 PAPU 公式，TL-22 红线严格满足）
3. **先写 S011**（MVE 前置准备 session note，含 3 发现 + D006 BC-4 修订预告）

### A3 MVE 假设表 v3（形态对照版，Cheng 2013 公式回填后定稿）

**核心假设（两形态并列验证）**：
> 在 deep fade（σ²_I=0.684 Paillier 条件）下，对比 (a) 时域 frame-header pilot + PAPU（Cheng 2013 Eq.(5)）vs (b) 频域连续 tone + PAPU（Cheng 2013 Eq.(5) 迁移，不需插值）vs (c) AGC+DPLL baseline：
> ① pilot CPE（两形态）相位估计方差 < AGC+DPLL；
> ② BER 改善 ≥0.5dB；
> ③ cycle slip 不触发（BC-4）；
> ④ 数据决定 A3 pilot 形态选型

**对比方法（FR-14/15）**：
| 方法 | 角色 | 实现来源 |
|---|---|---|
| M1a 时域 frame-header pilot + PAPU（Cheng 2013 Eq.(1)-(5)） | 主方法候选 A | 新写（Cheng 2013 公式已精确获取，机械复现）|
| M1b 频域连续 tone + PAPU（Cheng 2013 Eq.(5) 迁移，N_data→0 极限） | 主方法候选 B | 新写（A3 设想，pilot 连续给参考不需插值）|
| M2 AGC+DPLL | FR-14 最强简单先验 | common.py `fft_foe` 风格 + 新写 DPLL |
| M3 VV 盲 CPE | BC-2 失效参照 | common.py `fft_foe` |
| M4 PASC 数字近似 | FR-15 目标基线 | 数字近似 + 记录差距 |

**pass/fail 标准（量化阈值）**：
| 验证项 | PASS 标准 | 阈值来源 |
|---|---|---|
| 相位方差 | M1a/M1b < M2（deep fade σ²_I=0.684）| Paillier 2.3dB gap |
| BER | M1a/M1b > M2 ≥0.5dB | Valjus +1dB 锚 |
| BC-2 | M3 deep fade cycle slip 复现（TL-18: BER 10-13%→27-30%），M1a/M1b 不失效 | TL-18 |
| BC-4 | M1a/M1b cycle slip 率 < M3 | Ip&Kahn 2009 / Cheng 2013 Eq.(5) |
| FR-14 | M1a/M1b > M2（非仅 > 无处理）| gw-feasibility |
| FR-15 | M1a/M1b ≥ M4 近似（或记录差距）| gw-feasibility |
| **形态选型** | M1a vs M1b 在 BC-2/BC-4 上差异显著则数据定，不显著则用 M1b（频域 tone + Cheng 2013 Eq.(5) 迁移，A3 设想 + 非平凡性 + BC-1 须精细区分）| 本轮决策 |

**TL-25 起飞检查单（6 条落实）**：
1. 共享信道：M1a/M1b/M2/M3/M4 共用同一 GG+CFO+噪声实现
2. 重生信道：σ²_I 改变时重新生成（用户选方案 B，信道须新写复现 Paillier §IV-C 条件）
3. 从 common.py 导入：信道（`gg_block`/`doppler_phase`）导入；pilot 注入 + CPE + PAPU（Cheng 2013 Eq.5）独立新模块（A3 主方法）
4. 基线已优化：AGC+DPLL 先做参数网格搜索（TL-14）
5. 先写理论预期：pilot 方差<DPLL / BER +0.5~1.5dB / VV 应失效 / 频域 tone PAPU 应有效（Cheng 2013 验证迁移性）/ M1a vs M1b 差异预期不明（数据决定）
6. 输出含元数据：`save_results` 注入 git hash + md5

**FR-11 架构摘要（DSP 语义对应，MVE 必填）**：
- 动作空间 → **处理粒度 per-block**（pilot 每 block 估一次相位）
- 决策粒度 → **per-block 相位补偿**（vs DPLL per-symbol 更新）
- 对比范式 → **pilot 前馈开环 CPE（两形态）vs AGC+DPLL 闭环**
- 奖励语义 → **绝对值**（相位方差、BER）
- 先验对照 → AGC+DPLL 得分 + pilot 得分 + 比值

**已知简化偏差（FR-18）**：
- 简化项：信道新生成（不复用 common.py 现成 GG 分块，复现 Paillier §IV-C deep fade 时序）
- 对主方法影响：M1a/M1b 在真实 deep fade 下表现可能比合成 GG 差
- 对 baseline 影响：M2 AGC+DPLL 在 Paillier 复现条件下应有 +5dB critical SNR（与原文对齐 = baseline 强度参考）
- 预判真实化后：若 M1 在 Paillier deep fade 下仍 < M2，结论可信；若 M1 失效，触发 BC-4 cycle slip 验证深入

### D006 BC-4 修订方向（待 MVE 后正式写入 decisions.md）

原 BC-4 措辞："A3 必须含 cycle slip 应对设计（PAPU 类），并在维度 D MVE 验证 deep fade 下不触发 cycle slip"

**修订方向**（Cheng 2013 公式获取后精确化，本轮发现驱动）：
1. "PAPU 类"措辞精确化为 **"Cheng 2013 Eq.(5) CS 修正公式：φ̂_u = φ̂⁰_u − round[(φ̂⁰_u − φ̂'_pilot)/2π]·2π"**——TL-22 红线解除，公式可机械复现
2. pilot 形态适用性：Eq.(5) 是 symbol-by-symbol feedforward，**频域连续 tone（A3 设想）和时域 frame-header pilot（Cheng 2013 原场景）均可机械使用**（频域 tone 是 N_data→0 极限，不需插值反而更简单）
3. CS 检测三层阈值（Cheng 2013 verified）：π/2（round 边界）/ π/3（工程防 false fluctuation）/ π/2（仿真统计）

**正式修订时机**：MVE 结果出来后，据实写入 D006（MVE 验证哪种形态 + Eq.(5) 在湍流 deep fade 下是否有效）。

### explore 目录与自包含 README（用户要求）

已建 `explore/a3-pilot-cpe-mve/`（用户明确要求"代码写到 /explore/xxxx/ 下，自带完整说明"）。README 待 MVE 执行子 agent 填写，必须包含：
- 实验目的（A3 §4a 维度 D MVE）
- 信号模型声明（TL-01 锁定，引用 Paillier §II-IV + A3 机制定位 D006）
- 4 BC 验证条件 + FR-11/14/15 不可降级条件
- TL-25 起飞检查单 6 条
- 文件结构（信道生成 / M1a / M1b / M2 / M3 / M4 / 结果聚合）
- 运行命令（自包含，无外部上下文依赖）
- 元数据输出格式

## 决策引用

- **D006（待更新）**：BC-4 措辞修订（"PAPU 类"→"cycle slip 应对设计（unwrap+CS 检测+修正）"+ pilot 形态适用性判定）。本轮为**修订预告**，正式修订在 MVE 后
- D001：执行（§4a 维度 D MVE 是当前步骤）
- D002：参照（common.py 是旧方向代码资产，信道可复用但载波恢复不可）
- D004：参照（互锁三章主轴，A3 这条腿进 MVE 验证）
- 无新建决策（本轮是 MVE 前置准备，MVE 结果后才拍板）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。§4a 维度 D MVE 前置（TL-22 物理前提验证 + 假设表定稿）属 D001 后续阶段链 Groundwork §4a 维度 D，在原始目标"系统性扫描找方向"内。**未执行 MVE，未碰 Contract/Execute/仿真正式环境**
- **范围变更**：无新增。MVE 做形态对照实验（而非单形态）是执行细节非范围扩展。pilot 形态从"频域 tone 设想"扩展到"两形态对照"是 D006 BC-4 修订预告范围，不扩 D001

## 后续

### 下一轮：MVE 执行（子 agent，≤1 天）

1. **Cheng 2013 子 agent 结果回填**（agent_6a0d74a6 后台运行中）——若拿到 PAPU 公式，M1a 用之；若三次缺失，M1a 用标准 unwrap + π/M 阈值自设
2. **MVE 子 agent 执行**（explore/a3-pilot-cpe-mve/）——5 方法（M1a/M1b/M2/M3/M4）× 多 SNR 点 × 多种子，输出结果 JSON + 元数据
3. **MVE 结果判定**（gw-feasibility §4a 决策表）：Go / Conditional-Go / Pivot / Kill
4. **写入 S012 + 更新 topic-index/decisions**（含 D006 BC-4 正式修订 + A3 §4a 维度 D 判定）

### 不做（Dead Ends，承 S009 + 本轮新增）

- ❌ 在 Cheng 2013 公式未回填前硬编 PAPU 算子（TL-22 红线）
- ❌ 把 Li 2019/Cheng 2014 的光纤 dB 数字直接搬 A3 增益预期（场景不同，须 MVE 独立测）
- ❌ 跳过形态对照直接选频域 tone（用户明确要求数据决定）
- ❌ 把频域 tone + 数字 CPE 与 PASC 混淆（BC-1 区分须 M4 PASC 近似实证）
- ❌ 在 MVE 结果未出前修订 D006 BC-4 正式条款（本轮只是预告）
- ❌ 在未读 thesis-lessons.md TL-25 前启动 MVE 执行（AGENTS.md 强制，本轮已读）

### 本对话纪律提醒

本对话已执行：H006 接收验证 + 2 子 agent gw-read（Li 2019/Cheng 2014）+ 1 后台子 agent（Cheng 2013）+ 2 次 AskUserQuestion + S011 写入。**接近单对话步数上限**。MVE 执行须在新对话或下一轮做（视 Cheng 2013 结果回来时机）。
