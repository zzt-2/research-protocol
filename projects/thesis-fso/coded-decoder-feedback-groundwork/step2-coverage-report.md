# Coded decoder-feedback Groundwork Step 2 覆盖报告

> 2026-08-09 | terminal: `STEP2_COMPLETE_STEP3_AUTHORIZED`

## 获取与质量门

固定 shortlist 共 7 篇：5 篇取得可 title-check、正文不少于 50 行且含 method/experiment/conclusion 的全文；2 篇经三轮合规通道仍不可得，按 `UNRESOLVED_FULLTEXT` 保留，不用摘要补方法链。

| 论文 | 角色 | 全文状态 | 完整链裁决 |
|---|---|---|---|
| arXiv `2511.21340` | C1 reference M | PASS，172 行 LaTeX 正文 | `PARTIAL_CORE_ONLY` |
| `10.1109/TSP.2006.874844` | finite phase/delay hypothesis direct reference | PASS，1914 行 | `PARTIAL_CORE_ONLY` |
| `10.1109/GLOCOM.2012.6503711` | decoder-aided continuous DD-PLL conventional comparator | PASS，322 行 | `STRONG_NEIGHBOR` |
| `10.1109/IWCMC58020.2023.10182805` | syndrome/CMF global coarse-acquisition B2 | PASS，317 行 | `PARTIAL_CORE_ONLY` |
| `10.1109/TWC.2004.837407` | decoder-extrinsic iterative CPR direct comparator | PASS，2028 行 | `PARTIAL_CORE_ONLY` |
| `10.1117/12.3107192` | coherent-optical cycle-slip B2 candidate | 三轮失败；0 行 | `UNRESOLVED_FULLTEXT` |
| `10.1109/ACCESS.2026.3653159` | recent LDPC-metric synchronization neighbor | 三轮失败；0 行 | `UNRESOLVED_FULLTEXT` |

获取失败不被改写成“不相关”或“无碰撞”。SPIE/ACCESS 继续是 claim ceiling；但用户已明确一两篇全文缺失不自动触发 NO ENTRY，且当前已有 5 篇合格全文覆盖 reference M、global finite bank、continuous decoder-aided CPR 和 recent syndrome/CMF B2，因此 Step 2 不阻断 Step 3。

## 全文事实合成

1. arXiv 2511.21340 的 phase-aware EM 在 20 次 initialization EM 后只运行一次 QPSK 四候选 decoder evidence selection，统一旋转整帧信道响应；动态相位与快速变化是 future-work 边界。
2. TSP 2006 对整帧 `(phase,delay)` bank 逐候选跑固定 `I_H`；turbo 配置是 12 个候选各 1 次迭代，赢家再跑 9 次。没有 mid-frame slip variable、boundary 或 selective re-decode。
3. IWCMC 2023 用 27 个整帧 phase/NFO 网格点的 syndrome 粗筛到 5 个 decoder-CMF 候选，再以全帧 EM refinement；它能压住“扩大 global operating range / 降低 global bank cost”，但不做局部 repair。
4. TWC 2004 APPA 与 GLOBECOM 2012 IHDD/ISDD 已占据 decoder soft/extrinsic 驱动 iterative whole-window/continuous CPR。固定短窗或 per-symbol PLL state 不等于 event-triggered boundary localization，也没有 bounded segment/suffix rollback、clean no-op 或 failure fallback。
5. 5 篇可得全文均未覆盖完整签名 `receiver-visible input → event trigger → detected local boundary → bounded segment/suffix phase action → decoder re-evaluation → fallback → bounded cost → localized output`。因此当前没有 `EXACT_COMPLETE_CHAIN`，但这只是 fixed-fulltext slice，不是领域新颖性闭包。

## Corrected coded-chain 工程边界

P08-R2 fresh audit 的结论为 `AUDIT_COMPLETE / TESTBED_GAP / NO_SCIENTIFIC_TERMINAL`：5G-NR BG2 rate-matched LDPC component、Gray-16QAM、on-air interleaver 和 single-pass hard decoder可复用；Sionna 2.0.1 soft/state/iteration/callback 是 `BOUNDED_ADAPTER`。当前链没有 carrier phase/CFO/slip、phase-hypothesis callee、局部 re-decode 或 persistent controller。

在 method-local impairment、单一 decoder metric、touched-codeword restart、不过度建设 streaming platform 的假设下，fresh 工程下界为 5–6.5 日；没有证据形成 `>7D_BLOCKER`。该估算只开放后续可行性判断，不授权 adapter 或实验。

## 覆盖限制与下一门

- coherent-FSO cycle-slip 的发生模型、合法 phase-jump/slip-rate/window 参数仍缺可读直接全文；必须在 mandatory Step 3.5 定向补物理与 exact-chain evidence。
- ACCESS 2026 的 partial-decision metric、Costas/decoder timing、locality、fallback 与 budget 全部 unresolved。
- “全文未找到 local repair”不等于 target defect 已存在、decoder metric 可定位、O1 有 recoverable headroom或 B2 未解决；这些属于 Step 4a。

结论：`STEP2_COMPLETE_STEP3_AUTHORIZED`。本报告只授权从全文形成 canonical Q#；adapter、defect smoke、MVE 与科学实验继续冻结。

