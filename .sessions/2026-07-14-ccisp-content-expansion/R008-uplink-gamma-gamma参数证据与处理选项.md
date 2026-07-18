# [R008] 上行 Gamma--Gamma 参数证据与处理选项

> 2026-07-15 | 关联：2026-07-14-ccisp-content-expansion / T014 / R007
> 性质：只读审计。未修改论文、params.py、Skill、图片、仿真代码、结果 JSON 或数据；未运行新仿真。
> 方法：主线做 git/ripgrep 追溯与文件核查；外部文献检索与物理映射复算各由独立子 Agent 执行，返回结构化摘要。
> 审计对象：上行 Gamma--Gamma 形状参数对 \((\alpha,\beta)=(1.2,0.9)\)、\((1.0,0.7)\)，能否建立可核验的直接文献来源、物理映射或可复算设计压力场景依据。

## 调研问题

1. 是否存在论文/标准/学位论文/权威教材，在可比的上行 FSO、归一化辐照度 Gamma--Gamma 模型中**直接采用**这两组参数？
2. 能否从项目唯一声称参考的物理量（sat.1553 上行 \(\sigma_p^2=0.15/0.25\)）经**可复算、量纲闭合、唯一**的映射得到这两组？
3. 若前两条都不成立，这两组参数能否被诚实地定义为不依赖结果的设计压力场景？
4. 论文应如何在「保留 exact + 直接文献 / 降级为设计压力场景 / 重新物理标定并重跑 / 删除上行场景」四条路线间取舍？

---

## 1. 事实时间线

| 日期/commit | 记录 | 原始理由（verbatim 或近 verbatim） | exact file:line | 证据性质 |
|---|---|---|---|---|
| 2026-07-07 `a46e03db` | 两组参数首次入库 | commit 消息："新增 uplink_moderate(α1.2/β0.9) + uplink_strong(α1.0/β0.7), 参考 sat.1553 σ²_R=0.15/0.25" + "5 seed 实测: NDA 全赢 DA, gain +2.48/+3.07dB（比下行 strong +2.51 更高）" | `git show a46e03db`（commit body）；diff 落于 `projects/simulation/params.py` | 历史理由 = 务实选参 + **结果反向背书**（把 +2.48/+3.07 dB 列为引入理由） |
| 2026-07-07 `a46e03db` | params.py 字段标注 | "设计选择: 参考 sat.1553 上行 σ²_R=0.15, 选对应强度区间 Gamma-Gamma α/β"；"严格 σ²_R→α/β 映射是另一研究方向, 此处务实选两组比现有 strong(α1.5/β0.8)更极端的 α/β 代表对应强度区间"；四处 `source_type: SourceType.assumption`、`audit_flag: AuditFlag.WARNING` | `projects/simulation/params.py:157-200`（diff 原 +1 区段） | **自认 assumption + 自认映射未做**；并把 sat.1553 的 \(\sigma_p^2\) 误标为 "Rytov 方差 σ²_R"（符号/模型偷换） |
| 2026-07-07 `a46e03db` | simulator 镜像 | 与 params.py 同源注释："参考 sat.1553 上行 Rytov 方差 σ²_R=0.15/0.25 … 严格 σ²_R→α/β 映射是另一研究方向" | `projects/simulation/simulator/_b11_params.py:84-94` | 同上；"≈ σ²_R 0.15/0.25" 的 `≈` 即承认非等式 |
| 2026-07-09 | 作者自记账面 | "**没有标定 Rytov 方差 σ²R**（我查了综述 sat.1553 发现它用 lognormal 不是 Gamma-Gamma，我的 α/β 和它的 σ²R 对不上，这个标定是个债）" | `projects/simulation/ADVISOR_BRIEFING_2026-07-09_v2_ccisp.md:157` | 作者自己已确认：sat.1553 是 lognormal 非 GG，且 α/β 对不上 |
| 2026-07-15 | 论文正文表述 | "(\(1.2,0.9\)) and (\(1.0,0.7\)) define the moderate and strong uplink regimes" | `projects/simulation/paper/ccisp2026/sections/system_model.tex:14` | 把 assumption 直接写成 regime 定义，未附来源——导师批注 "(α,β)哪来的" |
| — | 候选扫描记录 | **无**。`rg` 在仓库内未发现任何"曾扫描候选 (α,β) 表格 / 多组备选 / 误差表"的记录 | 全仓库 `rg`（results/json/__pycache__ 排除） | 选参无备选评估痕迹，无法回溯到任何权衡 |

**追溯结论**：两组参数无候选扫描历史，原始理由 = "务实选 + 更极端 + 结果好"三件套，其中第三项（结果）发生在选参之后，属反向背书。

## 2. 物理量定义卡

| 符号 | 原文定义 | 模型 | 单位 | 能否映射到 GG α/β | 证据 |
|---|---|---|---|---|---|
| \(\sigma_p\)（sat.1553） | "σ_p is the scintillation index"；下行方差 \(\sigma^2=e^{\sigma_p^2}-1\)（lognormal） | **Lognormal**（下行）/ **pointing+turbulence combined PDF**（上行 Sc.3/4）；**从未用 Gamma--Gamma** | 无量纲 | **否** | `papers/doi/10.1002_sat.1553/content.md:141-157` |
| \(\sigma_p^2=0.15\)（sat.1553 上行 Sc.3） | Table 1 上行场景 3 的 \(\sigma_p^2\) | Lognormal/combined，**含 pointing error**（\(\theta_0=3\)μrad, \(\sigma_{jitt}=1.7\)μrad） | 无量纲 | **否**（非 plane-wave 弱起伏 Rytov 方差，且含 pointing） | `content.md:152-157`（Table 1） |
| \(\sigma_p^2=0.25\)（sat.1553 上行 Sc.4） | Table 1 上行场景 4 的 \(\sigma_p^2\) | 同上，**含 pointing error**（\(\theta_0=34.5\)μrad, \(\sigma_{jitt}=25.6\)μrad） | 无量纲 | **否** | `content.md:152-157` |
| "σ²_R / Rytov 方差"（params.py 误用标签） | **sat.1553 原文不存在该符号**；params.py 把 \(\sigma_p^2\) 改写为 "Rytov 方差 σ²_R" | params.py 的标注口径 | — | — | params.py:158 vs content.md:141-157 符号不一致 = **符号/模型偷换**（已知陷阱 #1） |
| \((\alpha,\beta)\)（本文） | 归一化辐照度 Gamma--Gamma，两 unit-mean Gamma 变量之积的形状参数 | **Gamma--Gamma** | 无量纲 | 是（定义量本身） | `system_model.tex:14` |

**定义卡结论**：sat.1553 的 \(\sigma_p^2\) 是 lognormal/combined 模型的 scintillation index，含 pointing error，且 sat.1553 全文不用 Gamma--Gamma；它既不是 Rytov 方差，也不能作为 GG (α,β) 映射的直接输入。

## 3. 直接来源检索表

由独立子 Agent A 执行（主线不直接 WebSearch）。仅接受同行评审论文/标准/学位论文/权威教材；命中数字但场景不可比不算 PASS；未读到全文的标 UNVERIFIED。

| pair | 来源 | 是否 exact | 场景可比性 | DIRECT/PARTIAL/FAIL | 证据 |
|---|---|---|---|---|---|
| (1.2,0.9) | 全检索无可比来源；最接近 Sandalidis 2011（*Appl. Opt.* 50(6):952, DOI 10.1364/AO.50.000952，Gaussian-beam 上行 GG+beam-wander），但其 α/β 表**全文未取到**（Optica/ResearchGate/Semantic Scholar 均报错） | 未取到，无法判 | 上行 GG 场景可比，但数值 UNVERIFIED | **FAIL** | 子 Agent A §1；PubMed 摘要未含 α/β 表 |
| (1.0,0.9) | 精确串检索零技术命中；Uysal & Li 2006（*IEEE TWC* 5(6):1229, DOI 10.1109/TWC.2006.1638748，全文已读）只列 (4,4)/(4,2)/(4,1) 等标准对 | 否 | Uysal & Li 为地面 3–5 km 水平链路，不可比 | **FAIL** | 子 Agent A §2 |
| (1.0,0.7) | 同上，精确串检索零命中 | 否 | — | **FAIL** | 子 Agent A §2 |
| "Trinh 2017"（被旧材料标签为下行 4.0/3.0 等的出处） | P.V. Trinh 本人发表目录（sites.google.com/view/phuctrinh/publications，已全文读取）**无** "Gamma-Gamma Fading with Geometric Spreading" 一文；其 2017 条目为 ICC'17 QKD 协议文与 *IEEE Photonics J.* 9(1) mmWave-RF/FSO relaying，均非上行 GG 参数研究；唯一候选 GLOBECOM'17 "Channel modeling for terrestrial FSO links"（Trinh/Carrasco-Casado/Pham）为**地面**链路且 α/β UNVERIFIED | — | 不可比 / 归属存疑 | **FAIL（不可验证）** | 子 Agent A §3 |
| sat.1553 引用链 [7]-[11] | sat.1553 自身模型 = lognormal+pointing（非 GG）；refs [7]-[11] Table 1 全文未取到 | — | sat.1553 本体已非 GG | **FAIL** | 子 Agent A §4；content.md:141-157 确认非 GG |
| 通用性扫描 | (1.2,0.9)/(1.0,0.7) **不是**公认的 GG regime 标记；经典文献（Uysal & Li 2006、Al-Quwaiee 2015 *IEEE JSAC*、Wang & Cheng 2010 *Opt. Express*）标准对为 ≈(4,4) 弱 / ≈(2,2) 中 / <1 强 | — | 目标对物理上"像"强湍流值（近/低于 1），但无任何可比全文来源采用 | — | 子 Agent A §5 |

**直接来源结论**：两条对均 **FAIL**，无法建立 DIRECT、可核验、场景可比的文献来源。两个最有希望的线索（Sandalidis 2011 全文、sat.1553 refs [7]-[11]）因付费墙未闭合，标 UNVERIFIED。"Trinh 2017" 归属无支持。

## 4. 映射复算

由独立子 Agent B 执行。

- **公式与适用条件**：标准 Rytov→GG 映射（Andrews & Phillips, *Laser Beam Propagation through Random Media*, SPIE PM99, 2nd ed. 2005, Ch.9–12），plane wave、Kolmogorov 谱、\(l_0\to0\)、点接收器：
  \(\alpha=[\exp(0.49\sigma_R^2/(1+1.11\sigma_R^{12/5})^{7/6})-1]^{-1}\)，\(\beta=[\exp(0.51\sigma_R^2/(1+0.69\sigma_R^{12/5})^{5/6})-1]^{-1}\)。适用区 \(\sigma_R^2\lesssim1\)（弱—中起伏）。
- **输入及来源**：唯一可用输入 = sat.1553 \(\sigma_p^2=0.15\)（→声称 (1.2,0.9)）、\(0.25\)（→声称 (1.0,0.7)）。
- **预注册容差**：复算 (α,β) 落在目标 ±0.05 内才算命中（复算前声明，非事后放宽）。
- **结果**：
  - \(\sigma_R^2=0.15\) → plane wave **(13.30, 12.66)**；spherical (11.45, 15.30)；目标 (1.2,0.9)。
  - \(\sigma_R^2=0.25\) → plane wave **(8.05, 7.52)**；spherical (6.73, 9.91)；目标 (1.0,0.7)。
  - 偏差约 10×，远超 ±0.05 容差。
- **唯一性/敏感性**：对 \(\sigma_R^2\in(0,50)\) 扫描，plane-wave α 单调降至地板 ≈4.08，**永不进入** ≤1.2 的目标区。目标 α<1.2 处于该弱起伏公式的**饱和区（公式无效）**。且 sat.1553 的 \(\sigma_p^2\) 混合了波型/孔径平均/pointing，同一 \(\sigma_p^2\) 可由多组（波型/孔径/\(C_n^2\)/L）产生不同 (α,β) → **映射非唯一**。
- **额外阻断**：即便忽略模型不符，\(\sigma_p^2\) 也不是 plane-wave Rytov 方差；它含 pointing error 且来自 lognormal/combined 模型。
- **PASS/BLOCKED**：**BLOCKED**。

**映射复算结论**：不存在可复算、量纲闭合、唯一的 \(\sigma_p^2\to(\alpha,\beta)\) 映射；目标对位于标准弱起伏公式的饱和无效区，且 σ_p² 非该公式的合法输入。

## 5. 设计场景审计

| 候选准则 | 是否独立于结果 | 现有 pairs 是否满足 | 是否为历史理由 | 可对外声称边界 |
|---|---|---|---|---|
| A. "比下行 strong (1.5,0.8) 更极端的 (α,β) 代表更强上行湍流"（params.py 实际历史理由） | **否**：排序直觉（已知陷阱 #2）只证明"更小=更强"，不证明 exact pair 的物理出处；且历史理由文本同时引用 +2.48/+3.07 dB 结果 | 满足"更极端"这一弱排序，但不满足任何独立准则 | **是**（commit a46e03db / params.py:159-160） | 仅可声称"按强度递增排序的设计档"，**不可**声称来自文献/物理标定/典型上行值 |
| B. 预先指定的 scintillation-index bracket（如"上行 \(\sigma_I^2\) 覆盖 X–Y"） | 是（可独立于结果预先规定区间） | **未做**——无任何预注册的 \(\sigma_I^2\) 区间；如要补，是**事后新增的设计解释**（已知陷阱 #3：GG 闪烁指数完整式含交叉项，不能只取 1/α+1/β） | 否（不存在） | 若现在补，必须标明为"事后为既有数值构造的解释"，不能冒充历史依据 |
| C. 相对下行 strong 的严重度梯度 / 覆盖区间 | 部分独立（梯度方向独立，但具体数值跨度依赖结果叙事） | 数值跨度满足"上行 > 下行 strong"方向，但 exact pair 的跨度无独立准则 | 部分（方向是历史理由，具体数值非） | 可声称"覆盖比下行 strong 更强的湍流档"，**不可**声称 exact pair 有物理依据 |
| D. 可复算的设计压力选择规则（如"以几何级数覆盖某失效区"） | 是 | **不存在**；无任何记录的规则 | 否（不存在） | 若现在构造，须标明事后设计 |

**设计场景结论**：只有 A 是**历史真实理由**，但它只是"比下行 strong 更极端"的排序直觉，既不独立于结果（commit 同句引用 +2.48/+3.07 dB），也证明不了 exact pair 的依据。B/C/D 若现在补，都是**事后为既有数值编解释**，违反纪律 #1（不事后合理化）。因此两组参数**可被诚实降级为** `representative stress-test regimes`，但**必须显式标注**为设计假设而非文献值/物理标定值/典型上行值，且**不得**把事后构造的 scintillation-index 区间冒充历史准则。

## 6. 四路线比较

| 路线 | 真实性 | 可复算性 | 是否需重跑 | 影响范围 | PASS/BLOCKED |
|---|---|---|---|---|---|
| 1. 保留 exact pairs + 直接文献 | **不成立**——§3 两条对均 FAIL，Sandalidis 2011/sat.1553 refs UNVERIFIED，Trinh2017 无支持 | 不可复算（无来源） | 否 | — | **BLOCKED**（无文献可给） |
| 2. 保留 exact pairs + 降级为 representative stress-test regimes | **成立但有边界**——数值是历史设计假设；只要**显式标注**为 stress-test 而非文献/物理值，且不补事后区间冒充历史 | 可复算（"设计档"是内部约定，不声称外部复现） | 否 | `system_model.tex:14` 改措辞；不动参数/结果/图；改"moderate/strong uplink regimes"为"representative uplink stress-test regimes (design assumptions)"类表述 | **PASS（受限）**——最能保住现有 +2.48/+3.1 dB 上行结果与全部已冻结数据 |
| 3. 重新物理标定并重跑（换新 pairs） | 成立（若补全 Rytov/\(C_n^2\)/波长/孔径/波型输入，可走标准映射） | 可复算（标准公式） | **是**，且范围大 | 必须重跑全部上行相关结果（uplink_moderate/uplink_strong 的 +2.48/+3.07 dB、D009 的 3.1 dB total-energy headline 若含 strong-uplink、Fig.5 网格的上行点、26/29 上行点、workregion 统计）；违反本专题"不运行新仿真"不变量，需用户另批 scope | **BLOCKED**（在本轮约束下不可执行；且 §4 显示 σ_p²→目标对 在标准映射下不可达，需**真正物理输入**而非 sat.1553） |
| 4. 删除上行两档及相关结果 | 成立（最保守） | 可复算（删除不产生新声称） | 否（删除结果） | 删除 `system_model.tex:14` 上行句、`params.py` 上行字段（本轮禁改 params）、Results/Abstract/Conclusion 中所有 +2.48/+3.07/3.1 dB 上行锚点、Fig.5 上行点、上行 26/29 点；削弱"上行受湍流影响更大"论证 | **PASS（受限）**——但损失导师明确要求的上行场景与全部上行有利证据 |

## 7. 推荐 change contract

> 注：R008 是审计/诊断，不授权 WRITE。以下为供主控与用户决策的**候选合同草案**，进入 WRITE 前须用户明确批准。

- **推荐路线**：**路线 2（降级为 representative stress-test regimes）**。
  - 理由：路线 1 无文献（BLOCKED）；路线 3 在本轮"不重跑"约束下 BLOCKED 且 §4 证明 sat.1553 输入本就不可达目标对；路线 4 代价最大且违背导师"上行受湍流影响远大于下行"的明确要求。路线 2 在不重跑、不删数据、不改参数的前提下，把声称从"regime 定义（暗示有物理/文献依据）"收窄到"设计压力场景（明示是 assumption）"，与证据形态一致，符合 D002"内部严格、外部积极、声称收窄"。
- **exact affected files/claims**（路线 2，待批准）：
  - `projects/simulation/paper/ccisp2026/sections/system_model.tex:14`——将 "(1.2,0.9) and (1.0,0.7) define the moderate and strong uplink regimes" 改为明确标注 design assumptions / representative stress-test regimes 的措辞，并不得声称来自文献或物理标定。
  - （可选）若需进一步透明，在该句或邻近加一句"these uplink shape parameters are chosen to represent turbulence severities stronger than the downlink strong regime, and are not derived from measured Rytov variances"类中性边界说明——具体措辞待批准。
- **不应修改**：params.py（本轮禁改）、结果 JSON、图资产、仿真代码、Skill、下行三组（下行来源属另一专项，见 R007 UNRESOLVED）。
- **进入 WRITE 前所需批准/证据**：
  - 用户对"路线 2 + 是否加边界说明句"的明确批准；
  - 批准后须把 system_model.tex:14 改动纳入一个与 R009 非参数精炼合同**分离或显式合并**的批次，并在 fresh build + 独立审查后才算完成。
- **stop conditions**：
  - 若用户要求路线 1（给文献）→ 立即停止，无文献可给；
  - 若用户要求路线 3 → 停止，须先另批 scope 并补真正物理输入（非 sat.1553）；
  - 若路线 2 措辞被要求写成"上行典型/实测/物理标定值"→ 停止，违反证据。

## 8. 独立复核

由独立子 Agent（对全部 R008 证据与结论做模型偷换/事后容差/循环引用/结果反向背书四项检查）执行。

| 检查项 | 结论 | 证据 |
|---|---|---|
| 模型偷换（σ_p²↔Rytov / lognormal↔GG） | **已识别并拒绝** | §2 定义卡 + §4：sat.1553 是 lognormal/combined 非 GG，σ_p² 含 pointing；params.py:158 的 "Rytov 方差 σ²_R" 被标为符号偷换，未采纳为合法映射输入 |
| 事后容差放宽 | **未发生** | §4 容差 ±0.05 为复算前预注册；结果偏差 ~10× 后未放宽，直接 BLOCKED |
| 循环引用（项目文档互证） | **已排除** | §3 不采纳 params.py / ADVISOR_BRIEFING 作为"外部来源"；仅用它们作历史理由证据；外部来源由独立子 Agent 从原论文/目录取 |
| 结果反向背书 | **已识别并拒绝** | §1 时间线标出 commit a46e03db 把 +2.48/+3.07 dB 列为选参理由；§5 把该理由判为"不独立于结果"；未用结果证明选参合理 |

- **Critical**：0
- **Important**：
  - 路线 2 的"stress-test"降级是**诚实但偏弱**的外部声称——审稿人仍可能问"为何是 (1.2,0.9)/(1.0,0.7) 而非其他 stress pair"；需主控/用户权衡是否接受这种弱声称，或转路线 3/4。
  - §3 两个最有希望的线索（Sandalidis 2011 全文、sat.1553 refs [7]-[11]）因付费墙未闭合，标 UNVERIFIED；若用户愿意获取全文，理论上仍可能改变路线 1 结论，但目前证据不支持。
- **Minor**：
  - 子 Agent B 的标准公式常数（Andrews & Phillips PM99）来自二手来源（López-Leyva 2021 等），未对照 SPIE 原书核对，但跨多来源一致；不影响 BLOCKED 结论（即便常数有小差，目标 α<1.2 仍处饱和无效区）。

### 总状态：**BLOCKED**（对"建立可核验的直接文献来源或物理映射"）；**PASS（受限）**仅对"降级为 representative stress-test regimes"这一处理选项。

即：上行两组 (α,β) **无法**建立可核验的直接文献来源或可复算物理映射（路线 1、3 的证据目标 BLOCKED）；唯一不重跑、不删数据、诚实可行的论文处理是路线 2——保留 exact pairs 但**显式降级**为 representative stress-test regimes (design assumptions)，且不得补造事后区间冒充历史准则。是否采用路线 2、是否加边界说明句，需用户批准后方可进入 WRITE。

---

## 附：来源与可追溯性

- commit `a46e03db`（2026-07-07）：`git show a46e03db` body + `params.py` diff；`git log -S "turb_uplink_moderate_alpha"` 确认首次出现、无更早记录。
- `projects/simulation/params.py:157-200`（assumption / WARNING 标注 + 误标 σ²_R）。
- `projects/simulation/simulator/_b11_params.py:84-94`（镜像注释）。
- `projects/simulation/ADVISOR_BRIEFING_2026-07-09_v2_ccisp.md:157`（作者自认"sat.1553 用 lognormal 非 GG，α/β 对不上，是债"）。
- `papers/doi/10.1002_sat.1553/content.md:141-157`（σ_p = scintillation index；lognormal/combined；Table 1 上行 0.15/0.25）。
- `projects/simulation/paper/ccisp2026/sections/system_model.tex:14`（待处理句）。
- 外部文献检索（子 Agent A）：Sandalidis 2011（*Appl. Opt.* 50(6):952, DOI 10.1364/AO.50.000952，全文 UNVERIFIED）；Uysal & Li 2006（*IEEE TWC* 5(6):1229, DOI 10.1109/TWC.2006.1638748，全文已读，标准对无目标值）；Trinh 本人发表目录（无匹配文）；sat.1553 refs [7]-[11]（Table 1 未取到，UNVERIFIED）。
- 物理映射（子 Agent B）：Andrews & Phillips PM99 标准映射；\(\sigma_R^2=0.15\to(13.30,12.66)\)、\(0.25\to(8.05,7.52)\)；目标 α<1.2 在饱和无效区。
- 上游审计：R007（已判上行为 assumption、无 σ_p²→(α,β) 映射）、V007（参数 calibration 来源 PARTIAL）。
