# [S020] 双线 reference-extension 候选生成

> 2026-08-13 | 方法包装重定向 | DISPATCH_READY
> 2026-08-13 续接 | 候选收口与最后一次 bounded confirmation | P11_DISPATCH_READY

## 目标

纠正长期以期刊级新颖性闭包提前关闭硕士级方法候选的流程偏差；分别从历史资产和新经典方法两端生成可比较的完整方法卡，暂不运行实验。

## 记录

T012 的四档重裁有两处不能继续继承：其一，select-before-execute 是 CCISP 内部执行优化资产，软件等价与调用减少不能证明独立行业问题或 FPGA/PPA 方法；其二，P01 虽是合法候选，但没有理由在其他历史与新候选重建前成为唯一下一包。

本轮冻结两条独立 lane：

- T013：只读历史 inventory、harvest、D/V/H 和必要原始证据，恢复因强邻居、full-general、近期 baseline 缺口、场景迁移或“不是原创”而被提前关闭的硕士级 reference-extension 候选。
- T014：从公认经典 baseline 出发，在当前代码和物理模型真实支持的目标条件下构造新候选；只对前三名做小规模 exact-collision/claim-ceiling 检索。

两条 lane 只产候选卡，不跑实验、不进入 Groundwork/Contract/Execute。主控收到结果后统一比较，不由执行方自行选定论文主线。

硕士级方法最低合同固定为：经典 baseline 正确；目标场景有可验证增益；完整 receiver-visible 输入—动作—输出；不要求全面击败近期强方法；不声称 SOTA。强邻居限制表述，不自动否决。

## 决策引用

- D029：双线重新生成硕士级 reference-extension 候选（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；属于当前“若内部资产不足则定义 method-shaped search target”的写作准备范围，不授权实验。

## 后续

T013/T014 及其后续独立线已回传：

- 历史恢复线确认 P11 complex-LS Butterfly FIR 与 P01 adapter 是最接近可补证的方法候选；P1-M0/P10 仅剩有界检查距离。
- PAIG-KF 在 Step 2 因 primary fulltext 仅 4 篇、B4 承重角色缺全文而证据终止；这不是科学 Kill，但当前不值得继续消耗。
- CVL-BPS 已完成 Step 4a 并被廉价固定小网格吸收：local miss 72/72 blocks，fallback 93.06%，CVL 8263.11 eval/block，高于 correct full 8192；dev-frozen B=3 仅 384 eval/block，且 BER 0.06141 优于 CVL 0.07263。该线关闭。

主控比较后只保留 **P11 complex-LS Butterfly FIR** 作为最后一次 bounded 算法补证。原因是它与 Ch3 CCISP 的 selector/calibration 动作不同，已有完整 pilot→LS→linear Butterfly FIR→检测动作链，且历史 20 dB 局部结果显示 1% pilot LS 相对 50% full-label Adam 具有性能—开销优势；唯一承重缺口是 true-SNR 未实际注入和 blind CMA 是否同任务吸收。

用户明确给出停机条件：若 P11 因 authority 不足、corrected true-SNR 结果失败或同任务 CMA 完全吸收而不能形成方法，则暂停一切自动方法搜索、Groundwork 与实验，不再派新候选，转入新对话做战略讨论。

## 决策引用（续接）

- D030：P11 为最后一次 bounded 方法尝试；失败后暂停自动方法搜索（新建）

## 范围确认（续接）

- 本轮是否在 scope boundary 内：否；原范围明确不含新实验。用户已显式授权“继续”，并要求若仍不行就停止执行转讨论，故以 D030 和 topic-index scope change 开放仅此一个 P11 bounded package。

## 后续（续接）

派发 T015。执行方必须先定位 P11 的合法 GW/authority 位置并完成 sim-preflight；只有证据链可续接时才允许冻结并运行 corrected confirmation。任何非成功终态都触发 `METHOD_SEARCH_PAUSED_FOR_STRATEGIC_DISCUSSION`，不得自动轮换 P01 或新候选。
