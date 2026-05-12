# 工具使用场景手册

> agent 按关键词检索即可命中场景，不需要全文阅读。

---

## 检索场景（tools/search）

### S1：广覆盖初始检索

```bash
bash tools/search "关键词" --mode academic --preset scenario-method --top 30
```

适用：项目首次检索、覆盖面不足时的广搜、groundwork Step 1 初始论文池构建。
注意：`scenario-method` 会将查询拆为子查询分别搜索再合并，适合多概念主题。`--top 30` 扩大候选池。单概念查询不需要此 preset。

### S2：定向补充检索

```bash
bash tools/search "新方向关键词" --preset problem-driven
```

适用：二轮检索、发现新方向后补充、cover面缺口报告指出遗漏领域。
注意：`problem-driven` 全源搜索不限制年份，结果量大，配合 `--merge` 合并到已有搜索结果文件。

### S3：引用链挖掘

```bash
bash tools/search --citations 10.1109/TWC.2024.3406952
bash tools/search --citations 10.1109/TWC.2024.3406952 --citations-direction backward
bash tools/search --citations 10.1109/TWC.2024.3406952 --citations-depth 2
```

适用：精读核心论文后扩展论文池；引用图谱、前向引用、后向引用、追踪；Contract 新颖性检索验证方案是否已被做过。
注意：默认 direction=forward（谁引用了它）。`depth=2` 产生大量结果（二阶引用），先用 `depth=1` 确认相关性再加深。OpenAlex 引用数据无限额。结果可用 `--merge` 合并。

### S4：相似论文发现

```bash
bash tools/search --find-similar https://arxiv.org/abs/2405.17150
```

适用：找到一篇好论文后寻找同类、相关工作、相似论文；扩展某方向文献。
注意：需提供论文 URL（arXiv/DOI 链接均可）。基于 Exa 语义搜索，结果按相关性排序。

### S5：正式发表文献补充

```bash
bash tools/search "关键词" --doc-types journal conference
bash tools/blit "关键词" --source ieee
```

适用：预印本占比过高时补充正式发表文献；可引用性不足、发表状态、期刊会议论文补充。
注意：两步配合——先 `--doc-types` API 检索筛类型，再用 blit 浏览器检索补 IEEE 正式发表。搜索结果会自动标注 `publication_status`（published/preprint/unknown）。

### S6：趋势数据

```bash
bash tools/search "关键词" --trend --trend-years 5
```

适用：年度发文趋势、发展趋势分析、领域热度判断；Contract 背景节需要"2-3 年趋势"数据。
注意：`--trend-years` 默认 5 年，可调大。趋势数据来自 OpenAlex，无限额。只返回趋势统计，不返回具体论文，需另做关键词搜索。

### S7：Survey/Review 发现

```bash
bash tools/search "关键词" --preset comparison
```

适用：寻找综述、survey、review、benchmark 论文；快速了解一个领域的全貌和主要流派。
注意：`comparison` 会自动追加 survey/review/benchmark 关键词到查询中。返回的综述论文适合作为精读起点或引用图谱根节点。

### S8：标准文档检索

```bash
bash tools/search "3GPP NTN specification" --doc-types standard --mode standard
```

适用：3GPP、ITU、ETSI、标准规范、技术标准文档查找；Contract 方案引用标准条款。
注意：`--mode standard` 自动路由到 Firecrawl + Exa（标准文档最优源），同时注入 `3GPP ETSI specification` 修饰词。标准文档通常不在学术搜索引擎中。

### S9：代码/实现查找

```bash
bash tools/search "关键词" --preset implementation
```

适用：寻找开源代码、GitHub 实现、复现代码；Groundwork Step 7 baseline 复现阶段。
注意：`implementation` 预设路由到 Exa（category=github），优先返回代码仓库。找到后用 `--find-similar` 可继续扩展相关实现。

---

## 浏览器检索场景（tools/blit）

### B1：IEEE 正式发表检索

```bash
bash tools/blit "LEO satellite handover" --source ieee
```

适用：IEEE 期刊会议论文、正式发表文献补充；API 检索未覆盖的 IEEE Xplore 内容。
注意：50 次/会话，1s 间隔，稳定无反爬。只提取元数据（标题/作者/会议/年份/被引数），下载需机构权限。适合 S5 的第二步补充。

### B2：中文期刊检索

```bash
bash tools/blit "针灸 偏头痛 随机对照试验" --source wanfang
```

适用：中文论文、万方数据库、中文学术期刊、北大核心期刊；中文领域研究补充。
注意：10 次/会话，6s 间隔，严格限速。超过 16 次无间隔会 IP 封禁（~15min 自然解封）。关键词用空格分隔。返回标题/作者/摘要/关键词/期刊/年份/被引数/质量标签。

### B3：单刊定向检索

```bash
bash tools/blit "对外汉语 偏误分析" --source cbpt --journal sdzy
```

适用：CNKI 单刊定向检索、特定期刊论文查找；已知目标期刊时的精确检索。
注意：30 次/会话，3s 间隔。`--journal` 参数为 CNKI 期刊缩写 ID（如 wxdg、sdzy）。适合已知某刊发表过相关论文时精确提取。元数据含作者单位信息。
