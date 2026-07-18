# Task Brief: residual cascade 候选 GW Step 1 检索与撞车审计

> 来源: S036 | 产出位置: `.sessions/2026-07-10-dual-pol-osl-groundwork/R009-residual-cascade-step1-survey.md`
> 日期: 2026-07-16
> 唯一文档: 执行方可读取本任务点名的本地源码、决策文件与 `tools/search` 产出的 JSON；不得修改代码或运行 MVE

---

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol`。D040 已纠正事实：合法 standard-CMA 在当前注册域保持 X/Y 标签（5/5 不 swap，fixed BER≈2e-4），固定权重 ButterflyCNN 则 5/5 clean-swap；oracle≈3.5e-5。

**你的任务**：完成“standard-CMA 始终在线 + 小型 ML residual head 只修 `s-z_cma`”候选的 GW Step 1 文献检索和撞车审计，判断它是否值得进入 Step 2 获取/Step 3 精读。

**产出**：结构化 R009 调研笔记，写到上述路径；检索 JSON 由 `tools/search` 自动保存到 `search-archive/2026-07-16/`。

**最高纪律（违反一条就废了）**：
1. 只做 Step 1；不写算法代码、不跑训练、不跑 BER/MVE。
2. 不把 D036 的“检测后切换完整 ML”误当 residual cascade；本候选始终是 `z_out=z_cma+g(z_cma)`，无 detector-triggered replacement。
3. 不把“没人直接做过”当 Go；必须找到具体 baseline M、条件 C、失效/不足假设 A。
4. web/搜索页对论文功能的断言必须用 DOI 页面、出版商摘要或 Semantic Scholar/OpenAlex abstract 交叉验证；不支持则标“未验证”。
5. 不用 PI-BER 掩盖标签错误；候选的首要合同是 fixed-label 保持，性能增量才是第二层。

---

## 1. 背景（了解即可，不要据此预设结论）

已 Kill 的 D036 是 CMA shadow 运行后用真实符号相关检测 swap，再整段或 1000 blocks 切换到独立 raw-input ML；历史域中 2/5 触发，但 hybrid PI-BER 0/5 胜 ML-only。新候选与之不同：standard-CMA 永久在线并负责标签保持；residual head 接收 CMA 输出，仅学习小残差，不允许覆盖成完整逆均衡器。

候选临时 M-C-A（待检索修正，不是既成事实）：

> M = 合法 standard-CMA；C = 双偏振相干 FSO 的 GG 湍流 + 连续 SOP 漂移；A = CMA 虽保持标签，但有限步长/有限 taps/恒模准则留下稳定可学习的残余误差，使 fixed BER≈2e-4、距 oracle≈3.5e-5 约 5.7×。

最大风险：残差可能没有稳定可学习结构；简单 DSP 已能消除；监督 pilot 预算导致与盲 CMA 不公平；已有 coherent-fiber neural post-equalizer/CMA-assisted NN 直接占点；增量只是场景搬运。

---

## 2. 任务详情

### 2.1 必须回答的问题

1. 2019–2026 是否已有“线性/自适应/CMA 前端 + neural residual/post-equalizer”用于双偏振相干光通信？列直接命中与强邻近。
2. 这些论文的 NN 是完整替换、级联后均衡、残差学习，还是参数/步长预测？不得混类。
3. 是否有 FSO/Gamma-Gamma/SOP 漂移同场景直接命中？
4. 文献把 CMA 后残差归因为什么：非线性、PMD、频偏/相位、有限 taps、噪声增强，还是别的？当前本地信道是否真的包含该结构？
5. 是否存在不使用 ML 的更简单增强 baseline（DD-LMS/RDE/MMA/DFE/Volterra/线性 MMSE/decision-directed tracking）已覆盖主要 gap？
6. 把候选修正成一个可证伪的 Q# M-C-A，并逐条评四判据；任一不过就给出 Step 1 Kill/Defer，不为继续而继续。

### 2.2 执行方式

从项目根目录使用项目脚本，至少覆盖以下六组语义；可按工具实际 CLI 合并，但查询含义不能缺：

```bash
cd /mnt/d/code/study/research-protocol
bash tools/search 'dual polarization coherent optical CMA neural network residual equalizer' --sources s2 --max-per-source 30 --top 30
bash tools/search 'CMA assisted neural network equalizer coherent optical' --sources openalex --max-per-source 30 --top 30
bash tools/search 'hybrid CMA neural post equalizer optical communication' --sources s2 --max-per-source 30 --top 30
bash tools/search 'adaptive linear equalizer neural post equalizer dual polarization' --sources openalex --max-per-source 30 --top 30
bash tools/search 'residual learning coherent optical equalization polarization' --sources arxiv --max-per-source 30 --top 30
bash tools/search 'FSO CMA neural equalizer Gamma Gamma SOP' --sources s2 --max-per-source 30 --top 30
```

如 CLI 参数与上述示例不符，先读 `tools-guide.md` 对应搜索段，按真实 CLI 执行；不得自写网络抓取脚本。去重后对最高相关论文逐篇核 abstract，直接命中优先找全文可获取性，为 Step 2 提供清单，但本轮不批量下载。

### 2.3 产出格式（强制）

R009 必须使用 research note 锚点并包含：

```markdown
# [R009] residual cascade GW Step 1 检索与撞车审计

> 2026-07-16 | 关联：2026-07-10-dual-pol-osl-groundwork / D042

## 调研问题

## 发现
### 1. 检索覆盖与去重数量
### 2. 直接命中
| 论文 | 年份/venue | pipeline | 信息访问 | 对本候选影响 | abstract/DOI 证据 |
### 3. 强邻近与简单 baseline
### 4. FSO 直接覆盖
### 5. 本地信道是否包含可学残差

## 结论
### 候选 Q#（M-C-A）
### 四判据
### Step 1 判定：PASS / DEFER / KILL

## 对决策的影响
```

---

## 3. 已知陷阱

- “CMA+NN”可能只是 CMA 生成训练标签、NN 完整替换 CMA，不是级联 residual。
- fiber 非线性 residual 在本地当前信道没有 Kerr 非线性时不可直接迁移；若增益来自当前模型不存在的损伤，候选应 Kill。
- 只看 PI-BER 会把 ML clean-swap 当成功；文献若不报告 absolute tributary identity，要标口径缺失。
- 2e-4 对 3.5e-5 的 gap 是单一当前域数据，不得直接写成跨域稳定事实。
- 搜索工具零结果不是“绝对空白”；必须记录来源限速/失败情况。

---

## 4. 验收

- [ ] 六组语义均有落盘 JSON 或明确失败记录
- [ ] 直接命中/强邻近/假命中分类清楚
- [ ] 至少核验 5 篇最高相关论文 abstract；不足 5 篇则说明候选池实际规模
- [ ] 明确区分完整替换、切换、级联、残差四种 pipeline
- [ ] Q# 的 M/C/A 与四判据逐项给证据，不用“空白”替代问题
- [ ] 给出可执行的 PASS/DEFER/KILL，不直接建议 MVE

---

## 附：产出回传位置

`.sessions/2026-07-10-dual-pol-osl-groundwork/R009-residual-cascade-step1-survey.md`
