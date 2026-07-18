# [S070] Step2 失败获取补检

> 2026-07-16 | GW Step2 | 状态：进行中

## 目标

对4篇 DOI 下载失败的直接/FSO邻近论文寻找作者稿、arXiv或可转换来源，避免把失败条目误当已读。

## 记录

再次用 tools/search（S2/OpenAlex/arXiv）补检并归档至 `search-archive/2026-07-17/doi-{1..4}.json` 及 DOI 副本：

- JLT 2023 `10.1109/JLT.2023.3253383`：未找到作者稿/arXiv。
- JLT 2023 `10.1109/JLT.2023.3253673`：三源无结果。
- JLT 2021 `10.1109/JLT.2021.3102664`：仅低相关 OpenAlex 结果。
- JOSAA 2018 `10.1364/JOSAA.35.001204`：仅低相关结果，无作者稿/arXiv。

原 DOI metadata 的 `all_failed` 保留；没有新增 PDF/content，未宣称已读。

## 决策引用

- D055：直接撞车和FSO邻近需Step2/3核查。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

从共享 papers 库选来源可核查、机制相关的替代全文做邻近证据精读，同时明确标注“替代输入”而非失败DOI本身；Step3进度仍需达到5篇质量门槛。
