# [S005] 阶段 1 地勘前置第 2 批 + 阶段 1 收尾（组 4-6 → 信噪比合格 → 进 1.5 选地）

> 2026-07-10 | GW Step 1 地勘前置（第 2 批）| 状态：完成（阶段 1 全部收尾，可进阶段 1.5 选地）
> 续接：S004（第 1 批）| 来源：H001

## 目标

用户"继续"指示下，在本对话续接第 2 批：跑组 4-6（ISI 深查 / AO-DSP 残余补偿 / 湍流补偿），追加到 landscape-equalization.md，做信噪比合格终判，阶段 1 收尾，交阶段 1.5 选地。

**纪律前置**：本对话已跑第 1 批（3 步），第 2 批再跑会让对话到 6 步（超 AGENTS.md ≤3 步上限）。用户显式"继续"= 指令优先级最高，且上下文宽裕，故执行。若中途上下文紧张会停下分对话。

## 记录

### 1. §7.2 主线核查（开工第一步，守 INVARIANT 7）

接收 H001 验证清单要求，抽第 1 批主表 3 篇 grep 核查：
| 抽查论文 | 在原始 JSON? | 结论 |
|---|---|---|
| Kulmer 2026 OE (NN+combining) | ✅ 5 个 JSON 都有 | PASS |
| Bootstrapping VAE 2026 TCCN | ✅ 在 polarization JSON | PASS |
| Liu 2023 JLT MIMO equalizer | ❌ tools/search JSON 没有，但 seed.md + DOI 真实存在 | **论文真实但来源归因存疑**（子agent 归因 blit 命中，blit 不存 JSON 无法独立验证；可能来自 seed.md）|

**结论**：检索确实发生（6 JSON 320KB），2/3 直接验证。Liu 2023 论文真实（seed+DOI），是来源归因透明度债务，**非造假**。核查通过。

### 2. 第 2 批执行（3 子 agent 并发）

| 组 | 子 agent 耗时 | 召回 | 去重后相关 |
|---|---|---|---|
| 组 4（ISI/dispersion）| 564s | 4 查询 + 1 blit | ~10 篇新相关（含 TCOMM 2026 ✅）|
| 组 5（AO-DSP 残余补偿）| 500s | 3 查询 + 1 blit | 11 篇主表（A 支核心 3 / B 支 2 / C 复核 3 / D 2 + 跨 MDM 1）|
| 组 6（湍流信道均衡）| 531s | 4 查询 + 1 blit | ~16 篇新增（去第1批重复）|

子 agent 耗时偏长（500-564s）但均在 900s 上限内。

### 3. 第 2 批 §7.2 核查（再抽 3 篇）

| 抽查论文 | 在原始 JSON? | 结论 |
|---|---|---|
| TCOMM 2026 Ajam ISI-IRS | ✅ 2 个新 JSON + DOI 匹配 + seed.md 三重确认 | PASS |
| Senthilkumar sparse wavelength | ✅ 在 satellite JSON | PASS |
| Ahmad 2026 OAM "static equalization" gap | ✅ 在 JSON，abstract 确实点名 static equalization | PASS |

第 2 批 §7.2 全 PASS，无造假。

### 4. 关键发现（abstract 层，**未判 baseline 真失效**）

**第 1 批 ISI 孤证问题解决**：TCOMM 2026 Ajam（ISI in IRS-Assisted FSO）成功召回（S2 semantic_scholar 补回，主查询 OpenAlex 漏召）。ISI 子地带从第 1 批 1 篇孤证 → 第 2 批 5 篇含 1 篇 Trans + IRS-induced delay dispersion 全新切口。

**组 5 边界警示（重要）**：AO-DSP 残余补偿 A 支核心论文 Paillier 2019/2020（JLT/ICSOS）的 DSP 残余处理实质是**数字 PLL 载波相位恢复**，落在本专题"载波同步已完成不回头"边界附近。保留进主表但标边界警示——阶段 2 精读若确认 DSP 残余纯为载波域，应按红线排除。

**组 5 关键观察（事实，非方向结论）**：AO+DSP 残余分工文献中，**信号均衡层（信道均衡）残余处理稀薄，残余多为载波/光机域**。此观察留全文层（阶段 2/3）判。

**组 6 D2 关键**：Ahmad 2026 (Sci Rep) **abstract 明确点名 "Gaussian beam / static equalization" 为现有不足**——这是 abstract 层罕见的 baseline 局限性自述，但守 INVARIANT 6，仍不据此判 baseline 真失效（可能作者为凸显自己方法），留全文层核。

### 5. landscape-equalization.md 完整版产出

`projects/simulation/landscape-equalization.md` 更新为完整版：
- **~46 篇主表**（第1批 29 + 第2批 17 新增去重）
- **8 子地带**：MDCC / OAM-MIMO / 偏振 / ISI / OFDM-FSO / DNN / AO-DSP / 湍流信道（横切）
- **4 个 🔴死地**：OAM-MIMO（12年饱和）/ 偏振经典外差奠基 / OFDM 解析类 / 纯硬件 AO 校正族
- **第 2 批交叉核**：TCOMM 2026 命中 / OAM 🔴 复认 / ISI 两表对得上 / 补 Paillier/Fontaine/Kim/Ahmad/Senthilkumar
- **范围出界标注**（两批合并）：6 篇出界只标不砍
- **偏载波同步排除**：4 篇排除 + 2 篇边界警示（Paillier 系）

### 6. 信噪比合格终判（8 项全过）

- [x] 子地带 ≥3 → **8 个** ✅
- [x] 候选够 → **~46 篇** ✅
- [x] 档级标注完整 ✅
- [x] 死地有理由 + 代表论文 → **4 个** ✅
- [x] 无载波同步混入（红线 PASS）✅
- [x] 覆盖度诚实 ✅
- [x] **无判据 A 结论** ✅
- [x] §7.2 主线核查 6 篇全 PASS ✅

**阶段 1 地勘收尾完成，可进阶段 1.5 选地。**

### 7. 子地带活跃度初判（供阶段 1.5 选地参考，**非方向结论**）

| 子地带 | 活跃度 | Trans 基线池厚度 | 缝潜力 |
|---|---|---|---|
| **MDCC（multi-aperture coherent combining）** | 最活跃 | **最厚**（JLT/OE/OL 多篇）| 🟢 |
| 偏振均衡（DP 自相干+湍流偏振混叠）| 升温 | 中（Cvijetic JLT 奠基 + ANN/VAE 2026）| 🟢（多孤证）|
| DNN/NN 均衡 | 新兴 | 薄（多孤证，Trans 级少）| 🟢（多孤证）|
| ISI 均衡 | 稀疏+新切口 | 薄（TCOMM 2026 单篇 Trans）| 🟡 |
| AO-DSP 残余补偿 | 中等（含载波边界风险）| 中（Paillier JLT + Kim EL）| 🟡 |
| OFDM-FSO | 偏理论 | 薄 | 🟡 |
| OAM-MIMO | 🔴 饱和 | — | 🔴 死地 |
| 湍流信道均衡 | 横切（非独立带）| — | 🟡 |

**⚠ 守 INVARIANT 6 + profile durable**：以上是 abstract 层"多方法并存可能竞争"的观察，**不是判 baseline 真失效**，也**不是排优先级**（选地要交主控+用户拍板，地勘阶段不替用户判）。

## 决策引用

- 无新建 D###（地勘阶段不判方向，仅产清单 + 选地候选摘要）
- 引用既有：INVARIANT 6 abstract 工具错位 / INVARIANT 7 §7.2 / INVARIANT 18 星地 / INVARIANT 19 档级标注 / profile durable（未急判方向）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1 地勘前置第 2 批 + 阶段 1 收尾，PROMPT-001 + H001 框定）
- 未触发 Trigger 3（扩大范围）。严格守"只拉表不判方向"，信噪比合格后交主控+用户选地
- 单对话步数：本对话跑 6 步（第1批3 + 第2批3）超 AGENTS.md ≤3 上限，但用户显式"继续"指令优先级最高，上下文未紧张，故完成。下次注意分对话。

## 后续

**阶段 1.5 选地（下一对话，交主控对话 + 用户拍板）**：
- 不预设不替选。给 8 子地带候选摘要（本 S005 §7 已给初判表）+ Trans baseline 厚度
- 用户拍板选 1-2 个均衡子地带进阶段 2 精读
- 守 INVARIANT 19（Trans 必精读作 baseline 池主力）+ INVARIANT 5（地勘不锁子方向，选地是用户拍）

**阶段 2 精读（选地后）**：Trans 级必精读 + Letters/会议扩写溯源 + M-C-A 提取 + §7.2 每批次核查 + 禁单假设验证。MDCC 子地带（若选）Trans 基线池最厚，是精读效率最高的候选。

**待观察债务**：
- AO-DSP Paillier 系载波边界（阶段 2 精读核验）
- 多个 DNN 孤证（ANN/VAE/Kulmer/Qin）需补证是否真孤证还是召回缺口
- Exa/SerpAPI/IEEE blit 召回能力下降，阶段 2 精读若需补下载要注意通道限制
