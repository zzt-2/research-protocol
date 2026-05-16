# PROMPT: 修复 blit --source cnki 支持学位论文检索

## 问题

`tools/blit --source cnki` 目前只搜期刊论文（dbPrefix=CJFD），无法检索硕博学位论文。

## 当前实现

文件：`tools/blit.py`

关键行 ~505：
```python
db_filter = "&dbPrefix=CJFD" if doc_type == "journal" else ""
search_url = f"https://kns.cnki.net/kns8s/defaultresult/index?kw={encoded_query}{db_filter}"
```

CNKI 数据库前缀：
- `CJFD` = 中国期刊全文数据库（期刊论文）✅ 已支持
- `CDFD` = 中国博士学位论文全文数据库（博士论文）❌ 未支持
- `CMFD` = 中国优秀硕士学位论文全文数据库（硕士论文）❌ 未支持

## 任务

1. 修改 `doc_type` 参数，新增 `phd`（博士）和 `master`（硕士）两个选项
2. 映射关系：`journal` → `CJFD`，`phd` → `CDFD`，`master` → `CMFD`
3. 默认行为不变（不指定 doc_type 时仍搜期刊）
4. 同时支持组合搜索（如 `--doc-type journal,phd` 搜期刊+博士）

具体改动：
- 修改 `db_filter` 构造逻辑，支持多 dbPrefix
- 修改 argparse 添加新的 doc_type 选项
- 更新文件头的用法说明
- 测试：`bash tools/blit "低轨卫星 深度强化学习" --source cnki --doc-type phd` 应返回博士论文

## 约束

- 只改 `tools/blit.py`，不涉及其他文件
- 改完跑一个测试命令验证能返回结果
- 不写文档，不写 handoff
