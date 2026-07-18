# [S068] Pilot Jones Step1 逐条候选分类

> 2026-07-16 | GW Step1 | 状态：进行中（分类修正版完成，待V026b审查）

## 目标

补齐 Step1 AI 初筛硬字段，避免只用 relevance_score 宣称检索完成。

## 记录

`search-archive/2026-07-16/pilot-jones-step1-classification.json` 与 S066 的 82 unique 对齐，逐条字段：id/title/doi/source/priority/priority_reason/formal_status/direct_collision/narrow_question_relevance。依据 title+abstract+venue/year，未读全文；Tavily 两个非论文网页已剔除。

修正版加入candidate_key82/82唯一和top-level stats；priority 必读6、建议读14、待确认5、备选5、排除52；formal=56、nonformal_or_unverified=26；direct_collision direct=5、adjacent=26、none=51。Optics Communications 2021改为formal=true；四篇近年直接/邻近论文提升为必读；专利/产品/综述宽direct降为adjacent。覆盖 Jones/SOP direct子方向9条、FSO/偏振/pilot adjacent子方向21条。

## 决策引用

- D055：泛称撞车、窄问题收敛。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

V026通过后，Step1质量门闭合；Step2以3篇direct+FSO邻近优先获取/精读，失败下载保留缺口，不将其当已读。
