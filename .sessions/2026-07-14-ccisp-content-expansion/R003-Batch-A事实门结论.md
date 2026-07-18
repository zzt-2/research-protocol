# [R003] Batch A 事实门结论

> 2026-07-14 | 关联：2026-07-14-ccisp-content-expansion / S001 / D003
> 勘误：本报告的总体 FAIL 已由 D004/V003 取代。原分析漏读上游 D005/D006；data-BER 口径与 26/29 已有持久证据，无需新仿真。其余引用、公式、1.9 dB 归属及指标命名修正继续有效。

## 调研问题

在不运行新仿真、不修改数据/JSON/算法的约束下，`CCE-CC-002` 是否已经具备进入正文扩写所需的官方约束、引用、公式实现和结果数字证据链？

## 发现

### 1. 已通过的门

- **官方约束 PASS**：CCISP 2026 官方投稿页于 2026-07-14 核验 full paper 为 5–10 页，声明 double-blind review，并提供官方 Word/LaTeX 模板。官网未明确作者栏具体匿名操作，最终提交前仍需以投稿系统为准。
- **引用门 PASS（经替换/删除）**：11 处 unresolved citation 已逐一找到处置。Paillier、Du、Johst 和 Takimoto 可提供真实条目；Shieh-Djordjevic 不支撑本文 1.25 dB 句，B11 不支撑本文 pilot pattern 和单载波 256-sample window，相关错误归因应删除而不是补假引用。
- **公式实现门 PASS**：最终可形成 8 组公式。接收模型使用 `sqrt(h)`；100-symbol channel block 与 256-sample DSP window 分离；DA 为 pilot phase-time LS；实际选择器为 CV 门控、blind-h proxy、effective-SNR 和固定 13 dB 两层规则。

### 2. 未通过的门：switching 结果公平性

权威 A4 fixed 脚本与 JSON 的 `switching` 结果不能直接作为标准 BER 或公平增益：

- NDA 统计 1024 个信息位错误并除以 1024。
- DA 只统计 768 个数据位错误，但 `da_full` 再除以 1024。
- switching 在选 DA 时沿用上述 768-data-bit 错误数，再统一除以 1024；256 个 pilot 位置没有承载信息，却等效为零错误位。
- 因此 Fig.3 的 `10log10(Pb,NDA/Pb,sw)` 虽由持久 JSON 可复现，但分子和分母对应的信息负载不同。它至多是脚本定义的 normalized error-count ratio，不是标准 information BER，也不能支撑“公平 switching 增益”。

证据：`_a4_switch_30seed_fixed.py:67-68,93-102,207-214,237-263`；对应 JSON 只保存该口径的汇总，没有足够逐块选择/错误数据可离线重算统一 information-bit BER。

### 3. 其他结果处置

- `26/29`：无持久字段或可复算脚本，EXCLUDED。
- `about 1.9 dB`：可追溯，但属于 strong-uplink 工作区的 NDA-vs-DA 等效-SNR优势，不属于 switching。
- crossover：当前生成脚本给出约 18.0/16.9/10.7 dB；旧 17.9/16.8 两值 EXCLUDED。
- 13 dB：固定预校准 effective-SNR 决策阈值，不是观测 crossover。
- 1.249 dB：`10log10(4/3)` 的 total-energy coordinate offset，不笼统称固有 SNR penalty。
- 30-seed 数据与 5-seed 扩展点必须分开披露。

### 4. 可选路线

1. **路线 A（推荐）**：单独授权最小重评——不改算法和参数，只按统一 information-bit/throughput 口径重跑 switching 对比并生成持久 JSON。得到合法 switching 结果后恢复 `CCE-CC-002`。
2. **路线 B**：不跑新仿真，重定位为 DA/NDA 行为分析与选择器实现论文，删除 switching 性能贡献。该路线会降低说服力，并需新 change contract。
3. **路线 C（否决）**：继续使用当前 normalized error-count ratio，并在正文精确定义。该指标非标准且会暴露公平性问题，不符合 D002 的说服力要求。

## 结论

Batch A 总体 FAIL。官方约束、引用和公式实现已闭合，但 switching 的核心结果指标没有统一信息位口径；继续扩写会把不公平比较放大到摘要、结果和结论。按照 `CCE-CC-002` 停止条件，WRITE 必须暂停，等待用户决定是否允许路线 A 的最小重评或另签路线 B 合同。

## 对决策的影响

- 新建 D003，冻结当前 WRITE。
- 不修改论文正文，不回填 `CONCLUSIONS.md` 中的 switching 性能数字。
- 若用户选择路线 A，属于显式范围变更：允许新仿真，但仅限统一口径重评，不授权算法/参数改动。
