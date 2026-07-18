# [S071] Pilot Jones 候选 Step3 五篇精读输入

> 2026-07-16 | GW Step3 | 状态：进行中（待V027审查）

## 目标

完成≥5篇可核查全文的结构化精读，区分直接机制撞车与可迁移邻近证据。

## 记录

已精读五篇：

1. LCOMM 2026 `papers/doi/10.1109_LCOMM.2026.3651445/content.md`：FPT频域pilot→4路FPT→2×2 Jones直接补偿，光纤、无时域LS+EMA；方法族直接撞车，OSL GG组合未验证（S069）。
2. JPHOT 2021 `papers/doi/10.1109_jphot.2021.3062727/content.md`：盲M-CMA+NPCA RSOP跟踪，无pilot/EMA；算法族竞争，非OSL，行35–37、103–107、175–219等。
3. TCOMM 2022 `papers/doi/10.1109_tcomm.2022.3171809/content.md`：CW pilot相位噪声BLUE/ML及功率比，不做Jones/RSOP，邻近开销证据，行29–49、63–107、343–363等。
4. JLT 2025 `papers/doi/10.1109_JLT.2025.3533422/content.md`：模拟双偏振Costas PLL，不做pilot/Jones/EMA，载波恢复邻近，行5–9、47–59、231–277等。
5. JLT 2020 `papers/doi/10.1109_jlt.2020.3042546/content.md`：CO-OFDM已知训练符号做TO/CFO/phase/channel estimation，不估2×2 Jones/RSOP，pilot开销邻近，行23–25、47–91、379–428等。

每篇都有 `metadata.json` 来源/状态；此前失败的4篇DOI未被冒充替代。

## 决策引用

- D055：泛称机制撞车，窄问题收敛。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

V027通过后写入literature_notes，执行Step3.5定向补检索，随后Step4a四判据；不因仿真正信号跳过。
