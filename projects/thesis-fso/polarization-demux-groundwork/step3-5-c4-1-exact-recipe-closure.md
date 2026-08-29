# C4-1 scaled-unitary pilot-LS — Groundwork Step 3.5 exact-recipe closure

> 任务：T064 | 日期：2026-08-30
> task-control：`PASS`（`rdl.task-control.v2` / epoch 9 / CP009 / `GW_STEP3_5_EXACT_RECIPE_CLOSURE`）
> terminal：`SURVIVES_AS_CLASSICAL_MIGRATION`
> 证据范围：三轮 bounded closure；Round 3 被主线程停止指令截断，结论是有界非穷尽判断，不支持“首次”或“SOTA”声称。

## 1. 结论先行

在本轮可得证据内，没有已发表方案同时碰撞以下九个字段：

`known pilots | balanced Xp | unconstrained LS first | scaled polar | gain estimator | direct constrained objective | receiver-visible applicability/fallback | 2×2 demux output | DP-APSK/FSO target scene`

最强通信邻居是 2022 年 data-aided Kabsch/unitary channel estimator：它覆盖已知 pilots、直接 unitary constrained estimator 和 2×2 optical channel estimation，但摘要级证据未覆盖 common-gain estimator、`unconstrained LS → scaled-polar` 顺序、receiver-visible singular-value-ratio applicability/fallback，也不在 DP-(8,8)-16APSK 星地 FSO 场景。Roudas 2010 覆盖短训练 LS 初始化、直接低维 unitary/SU(2) 估计和 2×2 偏振解复用，但现有全文证据没有确认“先做 unconstrained 2×2 matrix LS，再做 scaled-polar”的本候选链，目标也是 PDM-QPSK 光纤。

因此 C4-1 不以完整 recipe collision 关闭；身份必须收窄为：**经典 scaled-polar / Procrustes 结构估计向短-pilot DP-(8,8)-16APSK 星地相干接收的 bounded migration，并显式输出 receiver-visible 适用域诊断。**

## 2. 冻结候选 recipe

采用接收模型

\[
Y = H X_p + N,\qquad X_p\in\mathbb C^{2\times N_p},\quad H\in\mathbb C^{2\times2}.
\]

候选动作严格冻结为：

1. receiver-known 双偏振短 pilots，且平衡设计满足 `XpXpᴴ=cI₂, c>0`；
2. 先做 unconstrained pilot-LS：
   \[
   \widehat H_{LS}=YX_p^H(X_pX_p^H)^{-1};
   \]
3. 对 `ĤLS=U diag(s1,s2)Vᴴ` 做 SVD；
4. 公共尺度估计为 `ĝ=(s1+s2)/2`，scaled-polar 投影为 `ĤSU=ĝUVᴴ`；
5. `ĝ>0` 时，用 `ĤSU⁻¹=ĝ⁻¹VUᴴ` 解复用 payload；
6. 同时输出 receiver-visible `ρ=s1/s2`（`s2≈0` 时标为不可逆/无效）与 applicability 标志。近酉阈值 `τSU` 不在 Step 3.5 拍数值；它只能在下一步候选级 Step 4a 预注册。若不满足 near-unitary / numerical-valid 条件，停止使用 scaled-unitary 主张，回到 unconstrained LS、ridge/Tikhonov 或保留双奇异值的 full-SVD floor。

该 recipe 不包含 EMA、不包含 payload blind/DD tracking、不包含 PDL/PMD/FIR 补偿。

## 3. Balanced-pilot 代数等价结论

直接受约束问题为

\[
\min_{g\ge0,\,Q^HQ=I_2}\|Y-gQX_p\|_F^2.
\]

令 `A=ĤLS`。当 `XpXpᴴ=cI₂` 时，LS 正交分解给出

\[
\|Y-gQX_p\|_F^2
=\underbrace{\|Y-AX_p\|_F^2}_{\text{与 }g,Q\text{ 无关}}
+c\|A-gQ\|_F^2.
\]

若 `A=U diag(s1,s2)Vᴴ`，complex Procrustes 的最优 unitary factor 可取

\[
Q^\star=UV^H,
\]

且

\[
g^\star=\frac{\operatorname{Re}\operatorname{tr}(Q^{\star H}A)}{\|Q^\star\|_F^2}
=\frac{s_1+s_2}{2}.
\]

所以，在 balanced pilots、未加权 Frobenius LS、公共非负实尺度和 `Q∈U(2)` 条件下，**“unconstrained LS → SVD → 两奇异值取均值 → scaled-polar”与直接 scaled-unitary constrained LS 的全体最优解完全等价，不是近似。**

边界如下：

- 非 balanced 时，目标变为由 `R=XpXpᴴ` 加权的 matrix-nearness 问题，普通 polar 一般不再等价；
- `rank(Xp)<2` 时 unconstrained LS 不唯一；
- `A=0` 时 `g*=0`、`Q` 任意且不可求逆；`rank(A)=1` 时 unitary factor可不唯一；
- 若约束硬改为 `SU(2)`、加入 sample weights/noise whitening/ridge 或额外 determinant/phase 条件，已是不同问题；
- Roudas/Kikuchi 均未陈述 balanced-pilot 条件或上述等价式。Schönemann/Higham 只支撑 Procrustes/polar 原子，不能据此认定 target recipe collision。

## 4. 三轮 query / coverage / usage receipt

所有检索均使用项目 `tools/search` / citation 后端；全文和批量引用链由子 agent 消化，主线程未调用 WebSearch/webReader。仓库 bash wrapper 在当前 Windows worktree 因 CRLF 失败，执行方在内存中去除 CRLF 或调用同一 `tools/literature_search.py` 后端；未修改工具源码。首次运行前产生的 tracked `__pycache__` 副作用在提交前按已验证的初始 clean 状态恢复，不计作研究产物。

| 轮次 | 动作与查询 | 实际覆盖 | 结果与分级 | 收口状态 |
|---|---|---|---|---|
| Round 1 | 4 个完成 query：exact `LS→SVD→equal-σ`；direct scaled-unitary LS/Procrustes；unitary Jones pilot polar demux；complex orthogonal Procrustes。另 1 个 pilot-aided Jones query 超时 | 实际有命中源为 OpenAlex + arXiv；S2 限速；SerpAPI 无有效新增 | 完成 query 共 13 条返回；MUST/SHOULD/MAY=`0/0/3`。仅得到 generic Procrustes、polarization modeling 和 LS inner-product-shaping 邻居 | PASS，进入引用链；exact long query 的 0 结果只作 low-recall 信号 |
| Round 2 | Roudas、Kikuchi、Schönemann、Higham 各 forward + backward，共 8/8 chains | OpenAlex 主源；raw=331，按 DOI/否则 title 去重 unique=322；S2 补充未运行 | 新最强邻居为 2022 data-aided Kabsch/unitary estimator；Eldar–Forney 2002 补 scaled/tight-frame 数学邻域。未发现九字段完整 target-scene recipe | `NO_COMPLETE_COLLISION_FOUND_IN_OPENALEX_CHAIN_METADATA`；S2-only recall 与两篇新全文逐式核对为 bounded uncertainty |
| Round 3 | 新术语 reprise：`complex unitary Procrustes channel estimation orthogonal training`；计划词还包括 Kabsch、ULSF/CLSF、nearest scaled unitary | 尝试 S2/OpenAlex/arXiv；首个 query 在停止指令前未返回终端摘要 | 已接收集合为空，MUST/SHOULD/MAY=`0/0/0`；结果数与去重数 unknown | **PARTIAL / bounded uncertainty**；不能把它写成证据性 `0/0 STOP`，按主线程明确停止指令结束，不开第四轮 |

规范检索产物：

- Round 1：`search-archive/2026-08-30/c4-1-exact-ls-svd-scaled-unitary.json`、`c4-1-direct-constrained-scaled-unitary-ls.json`、`c4-1-unitary-jones-pilot-polar-demux.json`、`c4-1-complex-procrustes-unitary-ls.json`、`c4-1-pilot-aided-jones-demux.json`；
- Round 2：`search-archive/2026-08-30/c4-1-round2-{roudas|kikuchi|schonemann|higham}-{forward|backward}.json`。

未新增全文：`0/4`。原因不是把 metadata 当全文，而是停止指令到达前没有完成 2022 Kabsch 与 Eldar–Forney 的获取/精读。该缺口限制穷尽性与原子级公式引用，不改变两者已知目标场景均非 DP-(8,8)-16APSK 星地 FSO 的事实，因此不升级为完整 target-scene collision。

## 5. 全文身份与来源

| 文献 | 身份与来源 | 本轮证据层级 | 与 C4-1 的作用 |
|---|---|---|---|
| Roudas et al., *Optimal Polarization Demultiplexing for Coherent Optical Communications Systems*, JLT 2010, DOI `10.1109/JLT.2009.2035526` | `papers/doi/10.1109_jlt.2009.2035526/content.md`，3712 行；metadata title match | 全文精读 | 最强已精读通信 recipe 邻居；有短训练 LS 初始化、unitary/SU(2)、2×2 demux，但未确认 unconstrained 2×2 matrix LS 后 scaled-polar/common-gain/ratio gate，且为 PDM-QPSK fiber |
| Kikuchi, *Digital coherent optical communication systems: fundamentals and future prospects*, ELEX 2011, DOI `10.1587/ELEX.8.1642` | `papers/doi/10.1587_elex.8.1642/content.md`，544 行；metadata title match | 全文精读 | Jones/PDL/PMD、训练 DD/CMA 与 2×2 butterfly 边界；不是 constrained pilot estimator |
| *Capacity Bounds Under Imperfect Polarization Tracking*, IEEE TCOM 2022, DOI `10.1109/TCOMM.2022.3206803` | Round 2 OpenAlex chain metadata | title + abstract；全文未读 | 最强新邻居：8 pilots/block、data-aided Kabsch/unitary estimate、LS comparator；缺 target scene 与本 recipe 多个字段 |
| Schönemann 1966 / Higham 1986 / Eldar–Forney 2002 | Round 2 Procrustes/polar chains | 前两者经典数学 authority；Eldar–Forney 仅摘要级 | 冻结“unitary/scaled matrix nearness 是经典原子”；不提供通信 I/O 或 target scene |

Roudas 的关键全文指针：训练/pilots `content.md:1289-1299`；直接低维 unitary/SU(2) 参数化 `content.md:601,877-879`；非酉/PDL 边界 `content.md:3263-3265`。Kikuchi 的关键指针：Jones/unitary 与 Hermitian PDL、2×2 butterfly、training DD/CMA `content.md:273-331`。

身份审计注记：T048 生成的 `papers/_read_notes/10.1587_elex.8.1642.md` 头部误写成另一题名并声称 overlap=1.0；本报告采用 `metadata.json.real_title` 与实际正文题名 *Digital coherent optical communication systems: fundamentals and future prospects*。DOI、作者和本轮使用的 Jones/PDL/2×2 DSP 内容身份不受该旧 note 头部错误影响；按 T064 边界不回改 T048 产物。

## 6. 九字段碰撞 ledger

记号：`Y`=明确覆盖，`P`=部分/相邻，`N`=明确不覆盖，`U`=当前证据未知，`—`=对该纯数学原子不适用。

| 对象 | known pilots | balanced Xp | unconstrained LS first | scaled polar | gain estimator | direct constrained objective | visible applicability/fallback | 2×2 demux output | DP-APSK/FSO scene |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **冻结 C4-1** | Y | Y | Y | Y | Y | Y（balanced 下等价表述） | Y（`ρ` + validity；失败回一般 LS 家族） | Y | Y |
| Roudas 2010 | Y | U | P（短训练 LS init；未确认 unconstrained 2×2 matrix LS） | N | N | P（直接两角/SU(2) + constrained CMA） | P（理论失效域，无 ratio flag） | Y | N |
| Kikuchi 2011 | P | U | N | N | N | N | P（PDL/PMD 边界） | Y | N |
| 2022 Kabsch estimator | Y | U | N（Kabsch 与 LS 对照） | N（unitary，未见 scaled polar） | U/N | Y | P（unitary 假设，无已证 ratio fallback） | P | N |
| Schönemann / Higham | — | — | — | Y（unitary/orthogonal polar 原子） | N | Y | N | N | N |
| Eldar–Forney 2002 | — | — | — | P（scaled/tight-frame 邻域） | Y（摘要支持自由 scale） | Y | N | N | N |

**ledger verdict：没有任何一行九字段全 Y；不存在已确认的 `COMPLETE_RECIPE_COLLISION`。** 最强邻居按缺口大小依次为 2022 Kabsch、Roudas 2010、经典 Procrustes/polar/scaled-frame 原子。

## 7. 历史 comparator / negative prior 边界

- B1 `unconstrained LS + EMA`：无 scaled-polar，不是本 action；
- B2 Tikhonov/ridge：保留一般非酉自由度，不是本 action；
- full-SVD floor：保留两个不同奇异值，只稳定求逆，不是取均值的 scaled-unitary projection；
- 以上只作为正确 comparator / negative prior，旧 verdict 不迁移；
- balanced pilots 下 direct scaled-unitary LS 与 LS 后 scaled-polar 是同一个 estimator 的两种表述，不能把二者包装成两个独立方法，也不能把 direct constrained 表述当成“更强不同算法”制造虚假差距。

最强廉价 comparator ladder 冻结为：`unconstrained pilot-LS → ridge/Tikhonov LS → full-SVD singular-value floor`。2022 Kabsch/direct unitary estimator必须作为结构同类邻居进入理论对照；balanced pilots 下只做等价性核验，不做重复性能曲线冒充新对手。

## 8. Terminal、claim ceiling 与可用 claim 句

### Terminal

`SURVIVES_AS_CLASSICAL_MIGRATION`

理由：已精读强通信邻居、完成 exact-action 检索与四个核心的 8 条 OpenAlex 双向链；新发现的 Kabsch、Procrustes、polar、scaled-frame 邻居均未覆盖完整 target-scene recipe。Round 3 与 S2/fulltext 缺口使该结论只能是 bounded、非穷尽 survival，但现有缺口不足以诚实写成已确认 collision。

### Claim ceiling

允许：

> 在 receiver-known balanced short pilots、memoryless near-scaled-unitary 2×2 Jones mixing 和 DP-(8,8)-16APSK 星地相干接收条件下，将经典 constrained-unitary / polar matrix-nearness 结构迁移为 LS 后 scaled-polar 闭式偏振解复用，并用 receiver-visible singular-value ratio 限定适用域与 fallback。

禁止：

- 不得声称发明 polar/Procrustes、scaled-unitary projection 或 unitary Jones estimation；
- 不得声称“首次”、SOTA、普遍最优或已穷尽 literature；
- 不得外推到显著 PDL、PMD、频率选择性 2×2 FIR、不等噪声/未白化前端或任意调制；
- 在 Step 4a 前不得声称 BER/NMSE 增益、方法可行或论文贡献已成立。

## 9. 唯一下一步

仅进入 **C4-1 候选级 Groundwork Step 4a A0/A′/A/B**：以本报告冻结的 recipe、balanced-pilot 等价性、Kabsch/Roudas 强邻居和 comparator ladder 做纸面问题/物理/基线可行性审查。

不得从本报告直接实现、仿真、写正式论文正文、加入 PDL/PMD/FIR 损伤或派生任务外候选。
