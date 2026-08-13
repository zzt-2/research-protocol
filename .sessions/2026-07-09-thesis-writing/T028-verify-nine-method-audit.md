# [T028] 九方法逐项审计独立终验

## 目标

只读核验 D033/S023/R025/V015 是否忠实综合 T019–T027 回传，并检查 P11、P05、P03、CCISP 四项高风险事实是否写对。

## 范围

- 允许读取本专题 D032–D033、S023、R025、V015、T019–T027，以及相应本地 worker/result/harvest 证据。
- 禁止修改任何文件；禁止运行实验、仿真或复算脚本；禁止联网或检索论文；禁止补 Groundwork 或提出新候选。

## 验收清单

1. 九项均出现且没有用资产分类替代具体 recipe；
2. P11 confirmation=`NOT_RUN`、CMA=`UNRESOLVED`；
3. P05 已纠正为独立 CMA receiver，不称 Butterfly continuation；
4. P03 仅 Q(64,40) 对应 0/132,000 identity，Q(8,6) 不冒充 identity；
5. CCISP headline 只用 9 dB/downlink/fixed NDA/common-payload/0.832–1.496 dB；
6. P06 不冒充 receiver-visible 部署或 BER 改善；
7. 推荐 spine 与证据强弱一致，且没有授权恢复执行；
8. 外部 exact duplicate 均保持 NOT_CHECKED。

## 返回

给出 PASS/PARTIAL/FAIL、逐项检查结果和任何 P0/P1/P2 问题；不要修改文件。
