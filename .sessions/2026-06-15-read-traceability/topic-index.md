# 专题: read-traceability（论文精读溯源机制改进）

> 状态: active | 创建: 2026-06-15 | 最后更新: 2026-06-15
> 目标: 建立可追溯的精读笔记/日志机制，解决溯源双向断 + 命名 join key 缺。属框架改动，完成后 close，机制沉淀到 templates/gw-read/CLAUDE。

## 进展线索

- **S001**（新建→architect定稿→实施→dry-run→审计 2026-06-15）精读溯源改进：3 问题诊断 → 两层架构 → architect 评估补 4 处遗漏 → executor 改 4 文件 13 处主线程验证 PASS → dry-run 1 篇端到端跑通机制 PASS，但抓到数据层 title↔content 错配（V001）→ **V002 定向审计反转：R002 6方向9篇关键论文0篇下载（审计无对象），已下载抽样错配率约20%属少数。结论=不需全量审计；待办=下载流水线title一致性校验(治本)+gw-read abort协议(治标)**
- **V001**（dry-run 验证）机制 PASS（双向溯源通）+ 抓到 title↔content 错配（photonics10080914 案例，OPLL标石墨烯实）+ 8 条改进点
- **V002**（title 定向审计）R002 9篇论文0下载（审计无对象）+ 已下载抽样错配20% + 决策不需全量审计
- **H001**（新建 2026-06-15）本轮交接：精读溯源机制落地完成 + research-direction-exploration 精读前置阻断（论文未下载）。下一轮 A=续P0/P1改进 / B=回方向探索主线精读。详见 H001
- **S002 + V003 + V003b + V003c**（实施完成 2026-06-15，H001 路径 A）P0/P1 标题一致性校验全部落地 + 回填 + API 交叉验证：title_verify.py（纯函数+CLI）+ download_output/pipeline 接入 + blit IEEE/CNKI sidecar + gw-read abort 协议 + backfill_titles.py（回填+双重守卫）。全量 237 篇最终：match 72.6%/mismatch 7.6%(18篇真损坏,全程不变)/unverifiable 19.8%。photonics 回归 PASS。回填 81 篇后子agent API 交叉验证（arxiv 44/44 准 + DOI 19/23）抓出 4 篇抓错页面已回滚（3清空+1剥前缀），加 all_failed 守卫 + _looks_like_non_title 二次校验防复发。H001 措辞瑕疵（5→4文件）已修。详见 V003/V003b/V003c，handoff H002。
- **voice.md**（新建）本轮用户原话档案，含"先试一试""blit总忘"等

## 已有基础（勘察来源）

- 规范面勘察：gw-read.md/templates.md/papers index.json 字段分析（explore agent A）
- 现状面勘察：精读笔记分布（4类位置）/ 溯源抽样 / content.md 质量 / 命名空间（explore agent B）
- 需求来源：research-direction-exploration 专题即将开始的 6 方向精读（gw-read）

## 不变量

- 精读笔记的天然组织维度是**论文**（一篇一份），不是时间
- 论文客观内容是**全局共享资产**（papers/ 本就全局），不应塞进临时 project
- 文件名 = paper_id 是天然 join key，一个动作同时解决"集中 + 溯源 + 双向链路"
- content.md 质量问题（html 清洗 / doi 补转 144 篇）是**转换管线问题**，独立于精读流程，不在本专题范围

## 已确认结论

### 不变量
- **两层架构（用户同意，DECIDED）**：客观精读全局 `papers/_read_notes/{paper_id}.md` + 项目级适配 `projects/{name}/read-log.md`
- **content.md 清洗/补转拆出去**（用户决定"不急"，非本专题范围）
- **历史 competitor_notes(6篇) 不回溯迁移**（用户决定"太老了先不管"）
- **paper_id 维度组织**（用户同意，非按日期）

### 其他结论
- framework-evolution 专题已 closed/归档，本改进新开 task 专题
- 探索期（无 project）精读写全局 `papers/_read_notes/`，适配记当前 research-direction-exploration 专题
- `_read_notes` 下划线前缀，与 `_archive`/`_registry` 管理性目录约定一致

## 范围边界

- 原始目标: 建立可追溯精读机制（溯源字段 + 集中存放 + 日志）
- 当前范围: 机制落地完成（4 文件 13 处改动，主线程验证 PASS）。CLAUDE.md/templates.md/gw-read.md/paper-materials-workflow.md 已含源文件路径 [MUST] + 全局 _read_notes + read-log 约定。待方向探索阶段实战精读跑通后 close
- 明确不含: content.md 清洗 / doi 补转 144 篇（拆独立子任务）/ 历史 competitor_notes 迁移
- 范围变更记录: 无

## 未决项

- **待执行**: architect 评估跨模块影响（templates/gw-read/paper-materials-workflow/CLAUDE 链路）→ executor 改 3 框架文件
- ~~全局 index 待定~~ → **已定（architect）**：YAGNI 不建，靠 `ls papers/_read_notes/*.md` + `grep -l {paper_id} projects/*/read-log.md` 按需查，CLAUDE.md 注明"反向查询靠 grep"
- **待实战验证**: 方向探索阶段首次精读（gw-read）跑通 → 全局 `papers/_read_notes/` 落首篇 + read-log 记首条 → 验证溯源闭环 → 本专题 close
- **cosmetic 微瑕（不修）**: CLAUDE.md 路径规则表 77-78 行 pipe 未与原表完美对齐，不影响 markdown 渲染
- **拆出独立子任务（不在本专题）**: content.md 清洗（arxiv_html CSS 污染）+ doi 补转 144 篇