# 提示词：P1 批次 — 流程缺陷修复（8 项）

## 任务

修复 8 个 P1 级别的流程缺陷。改动分散在多个框架文件中，但每个改动都很小（1-3 行）。

## 背景

详见 `.session/framework-evolution/LOG-001-framework-issues-2026-05-15.md` 的 P1-1 到 P1-8。

## 要读的文件

1. `stages/groundwork.md` — P1-1, P1-2
2. `stages/gw-read.md` — P1-2
3. `stages/contract.md` — P1-3
4. `CLAUDE.md` — P1-5
5. `tools/blit.py` — P1-6
6. `tools/pdf_convert.py` — P1-7
7. `tools/litdownload/download_config.py` — P1-8
8. `tools-guide.md` — P1-8

## 具体改动清单

### P1-1: Step 4a/4b 依赖关系未文档化
- **文件**：`stages/groundwork.md`
- **改动**：在编排表下方增加一段"步骤间数据依赖说明"：
  ```
  > **步骤依赖**：Step 4a（方向根基）在 Step 5 前执行，因为 Go/No-Go 决策应先于 Baseline 投入。
  > Step 4b（仿真条件）在 Step 5 后执行，因为需要 Baseline 的具体参数来评估仿真可行性。
  > 如果 Step 4a 结论为 No-Go，则项目终止，不执行 Step 5 及后续。
  ```

### P1-2: GW 完成条件数字不一致
- **文件**：`stages/groundwork.md` 完成条件处
- **改动**：在 "≥8 篇核心文献" 后增加注释：
  ```
  > 5 篇为 Step 3 单步通过门槛（见 gw-read.md），8 篇为 GW 整体完成门槛。
  > Step 3.5 补充检索后通常可达 8+。不足时返回 Step 3.5。
  ```

### P1-3: Contract Step 0 与 GW Step 1-3 重复
- **文件**：`stages/contract.md` Step 0 开头
- **改动**：增加"复用条件"段落：
  ```
  ### 复用条件
  如果 Groundwork 阶段已完成（literature_notes 含 ≥8 篇精读 + Step 3.5 已完成）：
  - **跳过 0.1 系统检索**，直接复用 GW 检索结果
  - **简化 0.2 竞品精读**，仅补充 GW 未覆盖的 Contract 特有竞品（如相同方法在不同场景的应用）
  - **保留 0.3 二轮定向检索**，但范围收窄到 Contract 特有的新颖性验证
  ```

### P1-4: 搜索-下载-转换管线无状态追踪
- **文件**：新建 `.session/framework-evolution/PLAN-004-pipeline-status.md`（只写设计，不立即实现）
- **内容**：设计 `_pipeline-status.json` 的 schema 和更新机制
- **判断**：这个改动需要新增机制，先写设计文档，后续再实现

### P1-5: 子 agent 无执行时间上限
- **文件**：`CLAUDE.md` "子 agent 强制委托" 段落后
- **改动**：增加一条：
  ```
  5. **子 agent 时间上限**：单次子 agent 执行不超过 15 分钟（约 900s）。任务拆分应确保单个子 agent 的工作量在此范围内。如果预计需要更长时间，必须拆分为多个子 agent 分批执行。
  ```

### P1-6: CNKI 搜索无法过滤学位论文
- **文件**：`tools/blit.py` CNKI 搜索函数
- **改动**：增加 `--type` 参数支持，默认值 `journal`，搜索时在 CNKI 页面上选择"期刊"类型
- **注意**：需要读 blit.py 的 CNKI 搜索实现（约 L473-641），找到类型选择的位置

### P1-7: CAJ 格式无法转换
- **文件**：`tools/pdf_convert.py`
- **改动**：在文件输入处理处增加 CAJ 检测：
  ```python
  if input_path.suffix.lower() == '.caj':
      print("错误：CAJ 格式不支持自动转换。请用 CAJ Viewer 或 CNKI 在线阅读器转为 PDF 后重试。")
      sys.exit(1)
  ```

### P1-8: IEEE/CNKI 下载与 litdownload 管线割裂
- **文件**：`tools-guide.md`
- **改动**：在下载工具章节增加一段"两套下载工具的分工"说明：
  ```
  > **下载工具分工**：
  > - `tools/litdownload/`（通过 `tools/download` 调用）：处理 arXiv、OA PDF、Unpaywall。自动写入全局索引、生成 metadata.json 和 content.md。
  > - `tools/blit --download`：处理 IEEE（校园网 IP）和 CNKI（Cookie 认证）。不写全局索引，不自动生成 content.md，需手动运行 `tools/convert` 转换。
  > - 如果 blit 下载了 IEEE/CNKI 论文，应手动将信息追加到 `papers/index.json`。
  ```

## 执行顺序

1. 先改文档（P1-1/2/3/5/8），快速验证
2. 再改代码（P1-6/7），测试
3. P1-4 只写设计文档

## 约束

- 每个改动 1-3 行，不做大规模重构
- P1-4 只写设计不实现
- 改完后 commit 一次
