# Handoff: A3 进 Groundwork §B + N1 相干 FSO PCS gain 数据门控（两对话并行）

> 来源: S005 | 交接目标: 同时开两个对话并行推进 A3（进 Groundwork）和 N1（补检索门控）
> 日期: 2026-06-16 续 4
> 文件名: H005-a3-groundwork-and-n1-gain-gate.md
> 用法: **本文件一份覆盖两个对话**。每个对话只读自己的"任务块"（任务块 A3 / 任务块 N1）+ 上方共享的"状态/必读/不变量"。两块独立，互不依赖，可同时开。

## 到哪了（状态，两对话共用）

A3/N1 物理可行性预检已完成（S005）。**两个候选都没有 B1 式物理死锁**（B1 = PLL 带宽死锁，D003 永久排除）。但"存疑"性质不对称：

- **A3 = 存疑倾向 PASS**：无死锁（前馈导频无带宽矛盾）+ 针对主导损伤（残余幅度闪烁的相位副产物）+ 三重障碍全是工程量。缺口=星地场景导频增益缺直接测量（Groundwork 可闭合）+ 机制定位需收窄。**下一步：进 Groundwork §B**。
- **N1 = 存疑**：无死锁 + TL-03 边界可厘清 + 主导损伤针对性强，但 **cite=81 是 R006 误判**（D005 已纠正——踩 TL-03 + 55m rain 场景偏离），合法化身锚 Elzanaty blind；**相干 FSO PCS gain 数据完全缺失**（Elzanaty 全 IM/DD 1-2dB）。**下一步：补检索门控**。

**保底骨架（2.2）不变**：纯解析，不受物理可行性波动影响。

## 必读（严格按序，两对话共用）

1. **`topic-index.md`** —— 不变量段落 + 当前范围边界 + 候选总览
2. **`decisions.md` D001 + D003 + D004 + D005** —— D001 评判框架+后续阶段链；D003 B1 物理死锁 FAIL 范本（预检方法论）；D004 扫描边际+路由红线；**D005 N1 锚点纠正**（cite=81 误判 + Elzanaty blind + 相干 gain 门控）
3. **`S005-a3-n1-feasibility-preflight.md`** —— 本轮预检完整结果 + 量级对比表 + 三重障碍判定
4. **`thesis-lessons.md`** 速查表 + **TL-03/04/22/26** —— 物理可行性/反馈陷阱/震撼结果/主导损伤定位依据
5. **`papers/arxiv/1911.11851/content.md`**（Paillier 2020）—— 主导损伤结论（§IV-C：残余幅度闪烁 + 激光相位噪声主导，活塞相位 negligible）+ AGC 机制（line 177：信号噪声等比放大，SNR 不改善；critical SNR +5dB；BER penalty 2.3dB）。**这是两对话的物理判据基础**

## 不变量（两对话都必须遵守）

- **E≥2 不降**（D001）
- **路由红线**（D004）：留激光通信单链路物理/信号处理层，多节点/资源调度=永久排除
- **TL-03/04**：全局自适应/反馈类禁。N1 必须是离线静态非跨 RTT（已锚 Elzanaty blind）
- **D003 主导损伤定位**：针对损伤必须是 Paillier 主导损伤（残余幅度闪烁/激光相位噪声），针对 negligible 湍流相位的直接 FAIL
- **D 排除列 5 类**：需实测/专用硬件/超算/实时物理闭环/数月实测
- **TL-22**：任何"震撼结论"先查物理前提
- **D005**：cite=81 已废为 N1 关键论文；N1 锚 Elzanaty blind；**进 N1 Groundwork 前必须补相干 FSO PCS gain 数据**

## 纪律（和下一步直接相关）

1. 不替细分技术拍板——用户明确"靠 agent 用物理量级和文献证据判断"，已拦两条歧路（排列组合发散 / 互锁锁叙事）
2. 任务按 **≤600s** 切（harness 硬上限，非 AGENTS.md 的 900s——R006 教训）
3. 主对话严禁 WebSearch/webReader；检索用 `tools/search`，实在需 web 在子 agent 内做，返回 ≤500 词摘要
4. 论文功能/贡献断言用 Semantic Scholar API（bash curl）交叉验证，不支持的标"AI 推断未验证"
5. 未到 MVE——Groundwork §B 是 D001 后续阶段链的前置筛选，不是 MVE，不是 Contract

---
---

# 任务块 A3（对话甲做这个，跳过下面的 N1 块）

## 对话甲目标（一句话）

**A3 进 Groundwork §B：先收窄机制定位（前馈 pilot CPE vs AGC 增量），再做三重障碍在 Paillier 主导损伤结论下的重评，最后判 A3 能否进 Groundwork 剩余步骤。**

## 为什么做这个

S005 预检判 A3 = 存疑倾向 PASS：物理可行（无死锁、针对主导损伤、三重障碍全工程量），但有两个待闭合点——① 机制定位（"前馈 pilot CPE 替代 VV/AGC 的相位估计角色"=增量清晰 PASS；"导频补幅度本身"=与 Paillier AGC 冗余存疑）；② 星地湍流场景下导频抗 fade 增益缺直接测量。这两个缺口都能在 Groundwork 内闭合，所以 A3 现在可以进 Groundwork。

## 具体待闭合点（S005 指出的，照做）

### 闭合点 1：机制定位收窄（Groundwork 第一步，必做）

A3 用导频补幅度，但 Paillier 已证 **AGC 补偿**就能把幅度问题压住（PLL 1.4ms 收敛，critical SNR +5dB 容限）。**A3 必须回答"导频比 AGC 强在哪"**，否则是 AGC 替代品非增量。

**关键增量论点（物理上成立，需在 Groundwork 数值验证）**：
- AGC 放大信号也放大噪声（Paillier content.md line 177），deep fade 瞬态 SNR 不改善，PLL 仍可能跌破 critical SNR 失锁
- **前馈导频 CPE 无环路稳定性约束，无 critical SNR 失锁风险** —— 这是 A3 真正的增量价值，非冗余
- **必须把 A3 定义收窄为"导频做前馈 CPE 替代 VV/AGC 的相位估计角色"**（增量清晰=PASS）。**不是**"导频补幅度衰减本身"（与 AGC 冗余=存疑）。这个边界在 Groundwork 第一步显式锁定

### 闭合点 2：三重障碍重评（Groundwork §B 空白零假设）

| 障碍 | S005 初判 | Groundwork 要确认 |
|---|---|---|
| 多普勒时变 | 工程量（残频 100MHz 由 CFO 前馈 + ephemeris 预补，Yang FOE 范围 ±fs/2 全覆盖） | 导频间隔/功率与多普勒时间尺度无矛盾——量化确认 |
| deep fade 相位跳变 | 工程量（正是 A3 攻的目标，Paillier 证 +5dB 容限可压；前馈无 critical SNR 失锁） | deep fade 持续时间 vs 导频间隔——量化确认前馈不依赖环路稳定 |
| 单孔径无分集 | 不是障碍（Paillier 单 50cm 孔径 AGC+DPLL 已工作；A3 是 DSP 不引入接收阵列硬件，不命中 D 排除列#2） | 单孔径 scintillation σ²_I=0.684 下导频增益上限——这是性能天花板非物理墙 |

### 闭合点 3：Phase B 补检索（可选，建议做）

S005 指出：星地场景下导频抗 fade 增益未被任何已读论文直接测量。Yang 2026 是光纤 DSCM（无湍流），Valjus pilot+1dB 是符号导频非频域连续音。**补检索**：`frequency-domain pilot tone + free-space optical + turbulence`（`tools/search`，slug 加 `-preflight` 后缀，存 `search-archive/2026-06-16/`）。
- 若确认"频域导频音从未在湍流信道验证过"→ 迁移非平凡性反而增强（更适合硕士论文），物理可行性不受影响
- 若有先例 → 评估是否撞常识重做（E 反例检验）

## 执行建议

1. **先读 `stages/groundwork.md` + `stages/gw-feasibility.md §B`**（AGENTS.md 框架文件规则——进阶段/步骤必先读对应框架文件）。§B 空白零假设是当前正确步骤
2. 闭合点 1（机制定位）——主对话做，需用户确认"前馈 pilot CPE vs AGC 增量"这个定义收窄
3. 闭合点 2（三重障碍重评）——可派子 agent（≤600s）做量化核对，或主对话从 Paillier 正文 + 已读笔记直接推
4. 闭合点 3（补检索）——派子 agent（≤600s）
5. 产出：A3 的 Groundwork §B 判定（PASS 进剩余步骤 / 存疑补什么 / FAIL 的机制）+ 更新 S005 或新建 S006

## 不要做什么（Dead Ends）

- ❌ 跳过机制定位收窄直接进 A3 的 MVE/Contract（D001 后续阶段链——§B 前置未完不进 MVE）
- ❌ 把 A3 理解为"导频补幅度本身"（与 AGC 冗余，会得到错误结论）
- ❌ 在未闭合 §B 前锁"互锁三章"叙事（依赖未验证前提）
- ❌ 改仿真代码/开题报告（范围外）
- ❌ 找第 4/5 方向（用户已拦）
- ❌ 子 agent 按 900s 设计任务（harness 600s 硬上限）

---
---

# 任务块 N1（对话乙做这个，跳过上面的 A3 块）

## 对话乙目标（一句话）

**N1 相干 FSO PCS gain 数据门控：派子 agent 检索 + 精读，确认相干 FSO（intradyne，非 IM/DD）下 PCS shaping gain 是否存在且 ≥1dB。补到→解除门控，N1 可进 Groundwork；补不到→N1 降级"数据不足"。**

## 为什么做这个

S005 预检判 N1 = 存疑：物理可行（无死锁、TL-03 边界可厘清为 Elzanaty blind、主导损伤针对性强），但 **D005 加了一道数据门控**——Elzanaty 2020（arXiv:2005.02129，已下载精读）的全部 gain（IM/DD, blind: 1dB @ R=1.5/σ_R=0.5；2dB @ R=0.5；2.5dB CSI-aware）都是 **IM/DD M-PAM**，而 N1 假设相干 QAM。**相干 FSO 下 PCS gain 无任何论文直接验证**。用 IM/DD gain 外推到相干 FSO = TL-22 红线（基础数据缺失，外推不可信）。所以进 N1 Groundwork 前必须补这数据。

## 具体待检索（D005 门控的核心）

### 检索目标：相干 FSO（intradyne coherent detection，非 IM/DD）下 PCS shaping gain 的 dB 数字

**检索查询**（`tools/search`，bash wrapper，结果存 `search-archive/2026-06-16/`，slug 加 `-n1-gain-preflight` 后缀避免覆盖现有 JSON）：
- `probabilistic constellation shaping coherent free-space optical QAM turbulence`
- `probabilistic shaping coherent detection FSO M-QAM gamma-gamma`
- `Maxwell-Boltzmann shaping coherent optical wireless turbulence gain`

### 关键论文（可能含相干 PCS gain，需精读）

1. **cite=35**（R006 提及，待精读）："End-to-end optimization of constellation shaping for Wiener phase noise channels with a differentiable blind phase search"（2023, cite=35）—— PCS + 激光相位噪声联合（光纤场景，**相干**）。先用 Semantic Scholar API 查 DOI + abstract：`curl "https://api.semanticscholar.org/graph/v1/paper/search?query=End-to-end+optimization+constellation+shaping+Wiener+phase+noise+differentiable&limit=3&fields=title,externalIds,year,abstract,citationCount"`。拿到 DOI 后 `tools/download` 下 + `tools/convert` 转 md + 精读拿 gain 数字
2. **OFC 2024 Th3C.5**（search-archive 已命中，abstract 无 dB 数字）—— PCS + interleaving 强湍流 65dB link-loss。查 DOI 精读
3. 检索若命中新的相干 FSO PCS 论文，逐一过 E 三检验 + TL-03 边界（必须是离线静态非跨 RTT，cite=81 那种帧级自适应直接砍）

### 门控判定逻辑

| 检索结果 | 判定 | 下一步 |
|---|---|---|
| 找到相干 FSO PCS gain ≥1dB（精读正文，非 abstract）| **门控解除**，N1 可进 Groundwork（锚 Elzanaty blind 框架迁移到相干） | 写 R007 + 建议进 N1 Groundwork §B |
| 找到相干 PCS gain 但 <0.5dB 或无显著 gain | **N1 降级**——gain 太薄撑不起方法章（TL-05 算法贡献需 ≥1dB 且非薄增益） | 写 D006（N1 降级记录）+ 回 D004 切法 ⑦⑧ 深挖 |
| 找不到任何相干 FSO PCS gain 数据（全是 IM/DD）| **N1 标"数据不足"降级**——不能在缺数据时外推 IM/DD gain（TL-22 红线） | 同上，或建议把"相干 FSO PCS gain 测量"本身作为 Groundwork MVE 目标（但这是方法创新风险高，慎选） |

## 执行建议

1. **先读 D005**（decisions.md）——理解门控逻辑 + cite=81 为何是误判（Semantic Scholar abstract 直证）+ Elzanaty blind 为何是合法化身
2. 派子 agent（≤600s）做检索 + 论文下载 + 精读拿 gain 数字。**注意 Semantic Scholar API 有速率限制**（本轮主对话踩过 429），子 agent 调用间加 sleep 或分批
3. 产出：R007（N1 相干 FSO PCS gain 调研）+ 门控判定（解除/降级/数据不足）。若降级 → 新建 D006
4. **不要进 N1 的 Groundwork**——门控未解除前不进（D005 强制）

## 不要做什么（Dead Ends）

- ❌ 把 cite=81 当 N1 关键论文（D005 已废——踩 TL-03 + 场景偏离）
- ❌ 用 Elzanaty 的 IM/DD gain（1-2dB）外推到相干 FSO 直接写进结论（TL-22 红线）
- ❌ 在门控未解除前进 N1 的 Groundwork（D005 强制）
- ❌ 接受"相干 PCS gain 应该和 IM/DD 差不多"这类无数据推断——必须精读正文拿 dB 数字
- ❌ 找第 4/5 方向（用户已拦）
- ❌ 子 agent 按 900s 设计任务（harness 600s 硬上限）

---
---

## 接口变更

无（本轮无代码改动）。

## 失败数据附录

### B1（D003，永久排除，两对话参考避免重蹈）
- 核心失败机制：PLL 环路带宽要窄看活塞相位 vs 要宽跟多普勒，不可同时满足，物理死锁
- 决定性实证：Paillier 2020 §IV-C（content.md L194-196），B_L=5MHz DPLL + AO 残余，开关湍流相位 → PLL 输出 "negligible differences"
- 已排除：湍流相位进 PLL 环路 TF / 联合建模多普勒+湍流相位（永久）
- 可复用：Paillier 2020 作 A3/N1 的物理判据基线（主导损伤定位）

### cite=81（D005，R006 误判，对话乙参考避免重蹈）
- 核心误判：R006 把 cite=81（Guiomar 2020）当 N1 关键论文，但 Semantic Scholar abstract 直证它踩 TL-03（moving average channel estimator 驱动帧级自适应=跨 RTT）+ 场景偏离（55m fiber-FSO + rain memory，非 GG deep fade）
- 已排除：cite=81 作 N1 关键论文 / 精读它拿"PCS-FSO 强湍流 deep fade gain"（拿不到，场景不符）
- 可复用：教训——abstract 级判断（R006 全部是 abstract 级）需正文/Semantic Scholar abstract 交叉验证才能定方向锚点

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| N1 相干 FSO PCS gain 数据缺失 | TL-22（震撼结果先查物理前提）/ D005 门控 | Elzanaty 全 IM/DD，相干 FSO gain 无任何论文数据 | 对话乙补检索——找到≥1dB 解除，<0.5dB 或找不到 降级 |
| A3 星地导频抗 fade 增益缺直接测量 | TL-20（仿真先建理论预期） | Yang 是光纤 DSCM，Valjus pilot+1dB 是符号导频 | 对话甲 Groundwork §B 内补 Phase B 检索 + MVE 量化 |
| TL-26（E 三检验全过≠值得做）未沉淀 | D003 建议新增 | thesis-lessons.md 未加，归 doc-steward | doc-steward 专题后续沉淀，非本专题 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| A3 物理死锁检查（对话甲） | 无"两个物理要求矛盾无可工作区间" | D003 方法 | A3 已初判无死锁（S005），Groundwork 复核 |
| A3 主导损伤针对性 | 攻的是 Paillier §IV-C 主导损伤（残余幅度闪烁），非 negligible 活塞相位 | D003 | A3 已初判针对（S005） |
| N1 门控（对话乙） | 相干 FSO PCS gain ≥1dB（精读正文 dB 数字，非 abstract 推断） | D005 + TL-05 | 未验（门控待解） |
| TL-03 边界（两对话） | 方法不跨 RTT（离线静态，非帧级自适应） | TL-03/04 | A3 前馈导频已知参考安全；N1 必须 Elzanaty blind 不能 cite=81 |

## 接收方验证（每个对话启动时必须完成）

- [ ] 已读取 topic-index 的不变量段落（路由红线 / D003 主导损伤定位 / D005 N1 锚点纠正）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - 声称1：A3 无物理死锁（前馈导频无带宽矛盾）→ 验证：读 S005 §物理死锁检查 + Paillier line 206（推荐 open-loop）
  - 声称2：cite=81 踩 TL-03（Semantic Scholar abstract 直证）→ 验证：读 D005 核心证据段 + （可选）curl Semantic Scholar 重验
  - 声称3：Elzanaty 是 IM/DD（非相干）→ 验证：读 papers/arxiv/2005.02129/content.md line 43
- [ ] 已检查 _registry.yaml 中本专题 status=active + depends_on（thesis-direction-pivot / advisor-review-revision）
- [ ] 已确认当前范围未违反"明确不含"（不改仿真代码/开题报告/不做实验/未到 MVE）

## 下一轮

- **对话甲（A3）**：读 `stages/groundwork.md` + `gw-feasibility.md §B` → 闭合点 1（机制定位收窄，需用户确认）→ 闭合点 2（三重障碍重评）→ 闭合点 3（Phase B 补检索）→ A3 §B 判定
- **对话乙（N1）**：读 D005 → 派子 agent 检索相干 FSO PCS gain + 精读 cite=35 → 门控判定 → R007 +（若降级）D006

**两对话产出回传后**，主对话（新开第三个对话，或合并到其中一个的收尾）汇总：A3 §B 判定 + N1 门控结果 → 更新候选总览 → 决定互锁三章是否成立 / 保底骨架是否调整。
