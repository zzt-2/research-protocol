# RED Case 6 — contribution packaging

> baseline bundle: `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`
> fresh context, read-only, raw adjudication reproduced verbatim below

## 原始裁决

### 1. 主方法

唯一可作为毕业论文主方法的，是这些包共同依附的既有锚点：

- **条件自适应 DA/NDA 载波相位恢复选择器**
- P01–P04、P03不是新的独立主方法，而是它的鲁棒性、适用边界与实现证据。
- 可形成的主线是：根据接收端统计在 DA/NDA CPR 间自适应选择，并给出 SNR 失配、连续 Gamma-Gamma 条件和定点实现下的部署边界。

不得把以下项目升级为第二主方法：

- P01 `cand_rank`：被 P02 的普通区域阈值重调解释并超越。
- P03 `two_exp`：仅有 0.0166–0.024 dB 的次 MDE 优势。
- P11 complex LS：是线性 Butterfly FIR 的传统闭式解，且已降级为 9–15 dB 局部资产。
- G1 门控归一化：已被最终语义审计判定为固定阈值检测器的尺度伪影。

### 2. 核心工程/实现组件

按优先级保留：

1. **P03 定点实现**
   - 主实现点：统一 `Q(8,6)`、18 bit accumulator。
   - 在主增益区定点 regret 约 0.027 dB；继续加宽到 `(16,14)` 只改善约 0.0047 dB。
   - 这是最扎实的工程贡献，可直接支撑“低复杂度硬件友好实现”，但资源数字仅是 proxy，不得写成 FPGA 面积、功耗或吞吐量结论。

2. **P01/P02 接收端 SNR 鲁棒化配置**
   - pilot-SNR adapter 消除对名义 SNR 偏差的依赖，并在全部已识别伤害单元优于失配原选择器。
   - 弱湍流低 SNR 区域采用开发集冻结的普通阈值重调；应称“部署校准/区域配置”，不是新方法。

3. **P07-R AGC/ADC 配置**
   - 在正确恢复尺度与时间相关生命周期后，W8/W10 配合静态低增益 `g=0.5` 已把 regret 压到约 0.03–0.07 dB。
   - 作为前端增益标定规则，不包装成自适应 AGC 方法。

4. **P05 corrected Godard-with-z CMA**
   - 可作为双偏振接收机的传统在线 fallback；它解决 frozen ML 的 fixed-label swap。
   - 是强工程基线，不是创新方法。

5. **P08-R2 coded-chain 资产**
   - 仅保留 5G NR BG2/16QAM BICM、receiver-visible prefix LS 噪声估计、γ-free equalization path、递归 AST 与 metamorphic 信息边界检查。
   - 适合作为实现与验证基础设施；不作为主方法或主要科学贡献。

6. **P11 局部 Butterfly FIR 资产**
   - 可写成“线性模型应优先比较 closed-form complex LS”的工程经验。
   - 仅限 9–15 dB 局部结果；不得写“LS 跨 SNR 严格优于 Adam”“监督开销普遍不必要”或“LS 是唯一解决者”。

### 3. 支撑材料

- **P01/P02**：名义 SNR ±3 dB 失配边界、接收端估计偏置、普通阈值重调足以解释局部信号。
- **P04**：连续 Gamma-Gamma 内插点未产生 OOD 特异性退化；弱侧低 SNR regret 属于已有选择器边界。
- **P05**：fixed-label 与 PI-BER 对 polarization swap 的可观测性差异。
- **P06**：跨帧 history 虽优于 current-only，但远逊于 last-value persistence；适合作为可观测性边界。
- **P07-R**：旧 ADC 大收益来自尺度与生命周期错误；正确系统中静态低增益足够。
- **P08-R2**：LLR 局部校准 headroom 小于 MDE；主要作为 coded receiver 验证资产。
- **P10**：ML/CMA crossover 不成立，不能支持单专家 router。
- **P11**：局部 pilot-efficiency 与模型真实身份分析。

只能作为内部失败案例、不能进入正向方法证据链：

- 旧 P07。
- P08、P08-R 的被取代科学数字。
- P09：执行无效，8×“降复杂度”来自对称冗余与错误记账。
- G1 方法包及 `g1-thesis-insert`：均被 step-042 的尺度伪影裁决取代；最多用作“评价器尺度不变性缺失会制造假方法”的方法论警示。

### 4. Active carriers

**无。**

- `cand_rank` 已被普通阈值重调吸收。
- `two_exp` 低于 MDE。
- P09 已无效。
- P11 已降级。
- G1 已判尺度伪影。
- 其余包均为问题不存在、被传统方法解决或有界负面。

因此不能声称本轮 campaign 产生了第二个主方法或新的 `METHOD_SIGNAL`。

### 5. Campaign 裁决

**结束方法探索 campaign，不再开普通 P12 科学候选包。**

理由不是“包数够了”，而是：

- 已有一个可用主方法锚点；
- 已形成足够清晰的部署工程故事；
- 所有当前正向线索都已被传统替代、低于 MDE、降级或判无效；
- 在没有新 problem-bearing testbed、合法比较器和 active carrier 的情况下继续开包，只会重复串行 formalization 或制造第二主方法。

如果培养要求硬性需要两个独立主方法，这是一个 `STRATEGIC_GATE`，不能靠把现有工程组件改名解决。

### 6. 下一合法动作

进入只读的 **portfolio/thesis production**，不再跑新实验：

1. 建立主方法卡：DA/NDA CPR selector 的动作、信息边界、合法 baseline、主增益与 P01–P04 的适用边界。
2. 建立工程卡：pilot-SNR adapter/区域重调 + `Q(8,6)` 定点控制路径 + 静态低增益标定。
3. 将 P04/P05/P06/P08-R2/P10/P11 放入边界、消融、实现经验或附录，不计为独立方法。
4. 从任何候选论文材料中彻底移除 G1 正向叙事、P09 复杂度声称及被后续修复取代的旧 P07/P08 数字。
5. 保持单偏振 16APSK CPR 主线与双偏振 16QAM 工程资产的系统边界，不把它们伪装成已经联合验证的同一端到端接收机。
