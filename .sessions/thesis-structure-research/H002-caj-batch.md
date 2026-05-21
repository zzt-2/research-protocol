# PROMPT: 批量转换 CAJ 文件并精读 37 篇博士论文

## 背景

我们正在分析中国博士论文的"1方向→3问题"结构模式，为学位论文设计提供实证基础。

已完成：

- 5 篇论文全文精读（冷涛、刘晔祺、万莹、汪宇、贾子晔），结果在 `.sessions/thesis-structure-research/analysis-report.md`
- 37 篇 CNKI 博士论文已下载到 `papers/downloads/2026-05-16/batch2/`，全部是 `.caj` 格式

## 问题

37 个 CAJ 文件无法直接转换为 PDF/markdown。需要解决 CAJ→PDF 的转换工具。

### 已尝试但失败的方案

1. `pip install caj2pdf` — 不存在（Python 3.12 / torch venv）
2. `pip install git+https://github.com/JeziL/caj2pdf.git` — 仓库无 setup.py
3. `pip install cajparser` — 不存在
4. Go 版 caj2pdf — 系统无 Go 环境

### CAJ 文件格式

```
$ xxd xxx.caj | head -3
00000000: 484e 0000 9001 0000 8800 0000 0000 0000  HN..............
00000010: 5473 696e 6768 7561 2054 6f6e 6766 616e  Tsinghua Tongfan
00000020: 6720 4f70 7469 6361 6c20 4469 7363 2043  g Optical Disc C
```

HN 格式（清华大学同方光盘），知网专有格式。

### 环境信息

- Python: `~/.venvs/torch/bin/python` (3.12, torch 2.11+cu126)
- pip 镜像: `-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
- OS: WSL2 (Linux 6.6.87.2-microsoft-standard-WSL2)
- 无 Go 环境

## 任务

### Step 1: 解决 CAJ→PDF 转换

可选方案（按优先级）：

1. 找到能在 Python 3.12 下安装的 caj2pdf 版本
2. 安装 Go 并用 Go 版 caj2pdf
3. 用 WSL2 中的 Windows 端 CAJViewer（检查 Windows PATH 是否可调用）
4. 写一个 Python 脚本直接解析 HN 格式（CAJ 内部实际上是图像容器）
5. 用 mupdf / pymupdf 尝试直接读取
6. 其他可行方案

### Step 2: 批量转换

转换 `papers/downloads/2026-05-16/batch2/` 下所有 .caj 为 .pdf，然后用 `tools/convert` 转 markdown。

### Step 3: 批量精读

用子 agent 分批精读（每 agent 3-4 篇），提取每篇的：

- 章节间衔接方式
- 共享元素（系统模型/技术栈/仿真平台）
- 各章独立性
- 对我们的启发

格式同 `analysis-report.md` §5.1 的模板。

### Step 4: 更新综合报告

将批量精读结果整合到 `analysis-report.md` 的 §5 中，特别是验证/修正现有的 4 条共性发现。

## 关键文件

| 文件                                                     | 用途                                                    |
| -------------------------------------------------------- | ------------------------------------------------------- |
| `papers/downloads/2026-05-16/batch2/*.caj`               | 37 篇待转换论文                                         |
| `papers/downloads/2026-05-16/*.md`                       | 5 篇已精读论文的 markdown                               |
| `.sessions/thesis-structure-research/analysis-report.md` | 综合分析报告（需更新 §5）                               |
| `tools/convert`                                          | PDF→markdown 转换工具（bash wrapper，从项目根目录调用） |

## 约束

- 子 agent 精读输出 ≤800 词/篇
- 一次最多 3 个子 agent 并发
- 子 agent 单次执行不超过 15 分钟
