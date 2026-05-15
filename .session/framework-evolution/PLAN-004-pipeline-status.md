# P1-4 设计：搜索-下载-转换管线状态追踪

## 问题

当前 `tools/search` → `tools/download` → `tools/convert` 三步管线无统一状态追踪。跨对话恢复时无法快速判断：
- 哪些搜索结果已下载、哪些未下载
- 哪些 PDF 已转换、哪些未转换
- 下载或转换是否有失败记录

每次恢复都需重新扫描文件系统推断状态。

## 设计方案

### Schema：`_pipeline-status.json`

放在搜索结果 JSON 同目录下（`search-archive/{date}/_pipeline-status.json`）：

```json
{
  "search_file": "leo-satellite.json",
  "created": "2026-05-15T10:00:00",
  "updated": "2026-05-15T12:00:00",
  "items": {
    "L001": {
      "search_status": "downloaded",
      "download_time": "2026-05-15T10:05:00",
      "download_method": "arxiv_html",
      "pdf_path": "papers/arxiv/2405.17150/source.html",
      "content_path": "papers/arxiv/2405.17150/content.md",
      "convert_status": "done",
      "convert_time": "2026-05-15T10:06:00",
      "convert_quality": "fast",
      "content_size_kb": 45
    },
    "L002": {
      "search_status": "download_failed",
      "download_time": "2026-05-15T10:10:00",
      "download_method": "unpaywall",
      "error": "403 Forbidden",
      "convert_status": "pending"
    }
  }
}
```

### 状态值

| 字段 | 值 | 含义 |
|------|-----|------|
| search_status | `pending` | 搜索结果中，未尝试下载 |
| | `downloading` | 正在下载 |
| | `downloaded` | 下载成功 |
| | `download_failed` | 下载失败（见 error 字段） |
| | `manual_required` | 需要手动获取（付费墙等） |
| convert_status | `pending` | 未转换 |
| | `converting` | 正在转换 |
| | `done` | 转换成功 |
| | `failed` | 转换失败 |
| | `skipped` | 跳过（已有 content.md 或非 PDF） |

### 更新时机

1. `tools/download` 开始下载某条时 → `search_status: downloading`
2. `tools/download` 完成某条时 → `search_status: downloaded` + 填写路径
3. `tools/download` 失败时 → `search_status: download_failed` + error
4. `tools/convert` 开始时 → `convert_status: converting`
5. `tools/convert` 完成时 → `convert_status: done` + content_path + size
6. `tools/convert` 失败时 → `convert_status: failed`

### 恢复流程

跨对话恢复时：
1. 读 `_pipeline-status.json`
2. 筛选 `search_status: pending` → 重新下载
3. 筛选 `search_status: downloaded` + `convert_status: pending` → 重新转换
4. 筛选 `download_failed` → 展示给用户决定是否手动获取

### 与现有机制的关系

- 不替代 `papers/index.json`（全局索引，记录所有已入库论文）
- 不替代搜索结果 JSON（保留完整搜索元数据）
- 只追踪"搜索结果 → 入库"这个中间过程的状态

### 实现优先级

**低**。当前管线工作正常，跨对话恢复靠文件系统扫描可接受。痛点不够强时不必实现。

建议触发条件：当单个项目搜索结果 >50 条，或频繁跨对话恢复时再实现。
