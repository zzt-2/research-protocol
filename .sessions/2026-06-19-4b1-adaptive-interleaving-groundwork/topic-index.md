# Topic Index: 4b#1 信道感知自适应交织 Groundwork 执行

> 状态: active | 创建: 2026-06-19 | 最后更新: 2026-06-19（专题新建，接续 thesis-method-redirection closed）

## 专题信息

- **slug**: 2026-06-19-4b1-adaptive-interleaving-groundwork
- **title**: 4b#1 信道感知自适应交织 Groundwork 执行
- **depends_on**: 2026-06-17-thesis-method-redirection（已 closed，D006 方向裁定）
- **启动文件**: `PROMPT-001-groundwork-entry.md`

## 范围边界

- **原始目标**：进 Groundwork 阶段，验证 4b#1（星地 GG 湍流信道感知自适应交织）的物理可行性 + 搭建仿真链路。接续定方向专题（D006）
- **当前范围**：Groundwork §A0/A'/A 可行性预判 + §D MVE（GG-LCR/AFD→B/D 解析可行性 + 自适应>静态>0.5dB pass 标准）+ 仿真链路搭建
- **明确不含**：
  - 不重新定方向（已 D006 裁定 4b#1）
  - 不做完整训练（MVE 只验可行性）
  - 不做 Contract / Execute 阶段
  - 不做 FPGA 实现（FPGA 是后续 Execute 阶段验证章）
- **范围变更记录**：无

## 不变量

- **方向锁定**（D006 继承）：4b#1 信道感知自适应交织（星地 GG 湍流，开环形态）
- **创新定位**（D005 继承）：增量改进（非填补空白）。baseline = 唐承茂 2025 静态卷积交织
- **FPGA 定位**（D003 继承）：当验证章（非方法章）
- **开环约束**（坑3 继承）：仰角确定性排程 + 闪烁指数查表，禁止闭环 CSI 反馈（ρ(RTT)<0.03 失效）
- **TL-03 不迁移**：准静态是载波同步符号级，突发 µs-ms 是动态量，自适应交织不撞 TL-03
- **路由红线 D004 + D 排除列**：单链路纯 DSP，无专用硬件
- **年份+CNKI 双侧交叉验证**（定方向专题教训）：任何文献判断先核对前序筛子
- **解析推导是实现手段非创新核**：GG-Meijer-G 推不出闭式退半解析/数值优化，方向仍成立

## 已确认结论

### 不变量
- 方向已定（D006），不重新讨论
- baseline 是唐承茂 2025，改进点是静态→自适应 + 空空→星地 + LCR/AFD 接入

### 其他结论
（待 Groundwork 推进后填）

## 进展线索

- **PROMPT-001**（新建 2026-06-19）新专题启动提示词，含必读文件清单 + 本轮目标 + 关键约束。详见 `PROMPT-001-groundwork-entry.md`
- **H004**（来源 2026-06-17 专题）定方向专题收尾 handoff，含 D006 方向裁定 + 已知债务 + 下一轮任务。详见 `../2026-06-17-thesis-method-redirection/handoffs/H004-groundwork-entry-4b1-adaptive-interleaving.md`

## 未决项

- GG-Meijer-G 解析推导难度（Groundwork MVE 验证）
- FR-21 oracle 上界（自适应 vs 静态增益是否 >0.5dB）
- 老师"指标提升"量化（MVE 后确定）

## 当前位置

专题新建，待 Groundwork 启动。第一步 = 读 PROMPT-001 必读文件 + §A0/A'/A 可行性预判。
