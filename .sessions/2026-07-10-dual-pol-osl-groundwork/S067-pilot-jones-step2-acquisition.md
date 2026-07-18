# [S067] Pilot Jones 候选 Step2 获取

> 2026-07-16 | GW Step2 | 状态：进行中

## 目标

获取 Step1 识别的直接撞车与 FSO 邻近论文，建立可读全文输入和缺口记录。

## 记录

已执行 `bash tools/download --doi` 五篇：

- LCOMM 2026 `10.1109/LCOMM.2026.3651445`：已有 `papers/doi/10.1109_LCOMM.2026.3651445/{source.pdf,content.md,metadata.json}`，metadata success，source=`blit_ieee`；本次工具确认索引已存在。
- JLT 2023 `10.1109/JLT.2023.3253383`：all_failed，metadata 已留在 `papers/doi/10.1109_jlt.2023.3253383/`。
- JLT 2021 `10.1109/JLT.2021.3102664`：all_failed，metadata 已留档。
- JLT 2023 `10.1109/JLT.2023.3253673`：all_failed，metadata 已留档。
- JOSAA 2018 `10.1364/JOSAA.35.001204`：all_failed，metadata 已留档。

未读全文，仅核对下载状态；失败元数据包含 DOI、时间和 `download_method: all_failed`。

## 决策引用

- D055：Step1 窄问题需核对直接/邻近全文。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

先补Step1逐条分类；随后子 agent 精读已获取LCOMM全文，必要时用摘要/正式页面替代失败下载，但不把失败条目当已读。
