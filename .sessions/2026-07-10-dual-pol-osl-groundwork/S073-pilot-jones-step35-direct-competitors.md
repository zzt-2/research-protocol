# [S073] Pilot Jones Step3.5 直接竞品闭合

> 2026-07-17 | GW Step3.5 | 状态：进行中（provenance纠错后补精读）

## 目标

闭合关键词矩阵、引用链、5篇直接竞品浅读及全文获取债务，判断是否允许进入Step4a。

## 记录

第一轮6/6关键词矩阵查询完成，42条原始、41条canonical去重；实际有效来源为OpenAlex与Semantic Scholar两类，满足≥2源但**不含此前误记的Tavily**。LCOMM 2026 backward=19、forward=0；两组FSO+Gamma-Gamma精确查询均0。第一轮新增必读4篇、建议读1篇，因此未满足`gw-supplement.md`“最后一轮新增必读/建议读=0”的收敛硬判据；已启动第二轮定向检索，不能提前宣称收敛。

5篇直接竞品均完成题名、摘要、正式状态和Q2关系核验，结构化记录为`search-archive/2026-07-16/step35-direct-read5.json`。初次回报把5篇全部标为“无源文件（浅读）”，主控证据指针复核发现该表述错误：OE 2021目录实际已有54KB `content.md`，metadata为`download_status=success`、`content_quality=good`，含完整方法、实验、复杂度、结论与参考文献，已完成正式全文精读；其余4篇仍只能作摘要级证据。L08全文确认：3个线性无关pilot tones、逐block平均、解析RSOP矩阵+inverse，且已有短block增噪/长block失配权衡，不能把这些机制或权衡本身当作新颖性。最强碰撞为OE 2021和JLT 2022 FPT传输矩阵+滑动窗口平均。

OA替代补检也已完成：5篇title精确arXiv查询均为0（实际归档在`search-archive/2026-07-17/step35-arxiv-1.json`至`step35-arxiv-5.json`，不是初报的07-16目录）；IEEE 4篇均只有正式元数据且OA=false/PDF空。OE 2021的DOI/PDF路径曾失败，但Firecrawl HTML抓取随后成功，故其最终状态以论文目录metadata和完整`content.md`为准，不能沿用早先`all_failed`判断。

`projects/thesis-fso/literature_notes.md`已追加L06–L10及竞争分解。Q2只保留为待Step4a检验的问题：OSL GG是否产生既有光纤pilot矩阵估计未处理、且会改变算法结构的病态/动态失配。若只能靠场景替换或EMA参数差异区分，必须Kill。

## 决策引用

- D055：泛称pilot跟踪贡献已否决。
- D056：直接竞品必须在Step4a前检查；本轮已完成摘要级核验，全文债务仍显式保留。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

完成OE 2021全文精读、第二轮检索并集成后再做V028独立门控审查；若第二轮仍新增则按规范进入第三轮（最多3轮）。仅在V028 PASS后把master-state的Step3.5置为完成并进入Step4a。
