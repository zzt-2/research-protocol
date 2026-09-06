# 第四章正式图表生成侧验证记录

> 目标读者：硕士论文作者、导师、盲审评阅人与答辩委员；`venue=N/A`。  
> 范围：只验证派生 CSV、正式图和候选表的可追溯性、数值一致性与可读性；不新增仿真，不构成完整章节内容审查。

## 1. 冻结输入与生成链

正式材料只读取以下科学证据：

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_raw.json`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_aggregate.json`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_receipt.json`

提取脚本在读入前核对三份文件的冻结字节身份，并确认 receipt 对 raw 与 aggregate 的绑定。生成前后另行核对 raw、aggregate、receipt、scientific manifest 和 execution lock，五份科学文件的字节身份均未变化；仿真目录没有新增临时文件或中间状态文件。

数据链为：

```text
正式 raw 整数误码数/bit 数
  → 同 scene、Np、SNR、method 的 128 个随机簇汇总
  → Jeffreys BER = (errors + 0.5) / (bits + 1)
  → 冻结 BER 对数域交点口径
  → 派生 CSV
  → SVG 与 PNG
```

全部主曲线点直接保留 `errors` 与 `bits` 字段。独立逐行复算确认 570/570 个曲线点与 raw 的整数累计完全一致；每个正式 pooled 点均由 128 个配对随机簇、4,194,304 bit 构成。

## 2. Fresh 生成命令

在仓库 worktree 根目录执行：

```powershell
python -m py_compile projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/extract_ch4_formal_plot_data.py projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/plot_ch4_formal_results.py
python projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/extract_ch4_formal_plot_data.py
python projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/extract_ch4_formal_plot_data.py --check-only
python projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/plot_ch4_formal_results.py
python projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/plot_ch4_formal_results.py --check-only
```

结果：五条命令均成功。重复运行后，五份 CSV 与十份 SVG/PNG 的文件字节保持稳定。

## 3. 派生数据清单

| 文件 | 行数 | 统计含义 | 承重范围 |
|---|---:|---|---|
| `data/ch4-formal-ber-curves.csv` | 570 | 6 个 scene/pilot 切片 × 19 个 SNR × 5 个方法 | 中等湍流、$N_p=2/4$ 的完整曲线承担主结果；其余切片界定敏感性和边界 |
| `data/ch4-formal-required-snr.csv` | 4 | 两种尺度判据在 $N_p=2/4$ 时相对调参奇异值下限的交点、增益和置信区间 | 四项正式承重结果 |
| `data/ch4-formal-pilot-sensitivity.csv` | 20 | 中等湍流下 4 个导频长度 × 5 个方法的所需 SNR 与 25 dB BER | 只说明匹配条件下的导频敏感性 |
| `data/ch4-formal-mechanism.csv` | 190 | 中等湍流、$N_p=2/4$ 的直接信道 NMSE 与求逆残差 | 解释指标，不单独证明普遍因果 |
| `data/ch4-formal-mismatch.csv` | 30 | 6 个非酉失配强度 × 5 个方法，固定中等湍流、$N_p=2$、25 dB | 适用边界；$\delta=0$ 为精确复用参考 |

所有 crossing 缺失值均要求显式状态；本次导频敏感性 20 项 crossing 均为 `STABLE`，未填造任何交点。

## 4. 四项承重数字逐字段核对

工程参考 BER 为 $3.8\times10^{-3}$。以下数字从 `data/ch4-formal-required-snr.csv` 读取，并与 canonical aggregate 的对应字段逐一精确比较：

| 尺度判据 | $N_p$ | 调参基线所需 SNR / dB | 本方法所需 SNR / dB | 增益 / dB | 95% 置信区间 / dB | crossing | 重采样有效数 |
|---|---:|---:|---:|---:|---:|---|---:|
| 前向误差尺度 | 2 | 24.963858866516581 | 24.093385067827711 | 0.8704737986888702 | [0.6181620906133724, 1.0882735019907583] | STABLE | 5000/5000 |
| 前向误差尺度 | 4 | 23.710082550023447 | 23.589133341340915 | 0.12094920868253212 | [0.018893188115411522, 0.23922696650353503] | STABLE | 5000/5000 |
| 导频重构尺度 | 2 | 24.963858866516581 | 24.089128202759259 | 0.8747306637573224 | [0.6288589548885479, 1.0784282413486024] | STABLE | 5000/5000 |
| 导频重构尺度 | 4 | 23.710082550023447 | 23.602049197485908 | 0.10803335253753943 | [0.02575230869563915, 0.2025646753230283] | STABLE | 5000/5000 |

核对结果：4/4 项增益及置信区间精确一致。图表对 0.121 dB 和 0.108 dB 使用从零开始的增益纵轴，并以原数值和置信区间显示，没有通过截断纵轴放大差异。

## 5. 方法标签与参数语义核对

- 普通 LS、调参奇异值下限、前向误差尺度、导频重构尺度和理想 CSI 参考均使用面向论文读者的语义名称；内部实现代号只保留在 CSV 的追溯列中，没有进入图例。
- 调参奇异值下限采用独立调参映射：中等湍流 $N_p=2$ 时 $\tau=0.5$，$N_p=4/8/16$ 时 $\tau=1.0$；弱/强湍流 $N_p=2$ 时 $\tau=1.0$。没有沿用“全部切片统一 $\tau=1$”的历史概括。
- 导频重构变体中的 1.0 是起始奇异值下限/基准逆矩阵参数；真正的重构校准标量由当前接收导频逐观测闭式计算。该变体返回的信道估计量是校准前继承量，因此图中没有把其 channel NMSE 当作自身估计器证据，方法角色表也只将“尺度校准后的解复用矩阵与两路符号”列为其输出。
- 前向误差尺度与导频重构尺度共享结构方向，在尺度判据上不同；结果只支持方法族相对调参基线的有限优势，不支持前者优于后者。
- 理想 CSI 仅作理论参考，不作为可部署基线。

## 6. 图件与视觉 QA

| 图件 | PNG 尺寸 | 回答的问题 | 视觉检查 |
|---|---:|---|---|
| `ch4-formal-ber-curves` | 1767×805 | 短导频主场景的完整 BER–SNR 行为如何 | 5–41 dB 横轴完整；对数 BER 轴包含 Jeffreys floor；参考线、五种方法与理论参考可辨；无裁切或重叠 |
| `ch4-formal-required-snr-gain` | 1443×783 | 四项承重增益及不确定性多大 | 纵轴从 0 开始；数值标签位于置信区间上方；0.12 dB 未被夸大 |
| `ch4-formal-pilot-sensitivity` | 1767×805 | 导频数变化如何影响所需 SNR 与固定点 BER | 两个面板同条件配对；方法编码一致；坐标和图例可读 |
| `ch4-formal-mechanism` | 1767×807 | 结构约束如何影响信道误差与求逆残差 | 两面板图例分开；导频重构尺度不进入直接 channel-NMSE 面板；语义说明不遮挡曲线 |
| `ch4-formal-robustness-boundary` | 1767×805 | 湍流强度和非酉失配下的适用边界是什么 | 强湍流所需 SNR 完整显示至约 29.5 dB；失配扫描和理论参考可辨；无截断、图例/说明重叠 |

五份 SVG 均通过 XML 解析，并保留可编辑文本对象；五份 PNG 均非空且尺寸不低于 1200×600。颜色、线型和 marker 使用三重编码，灰度打印时仍可区分。逐张以实际 PNG 尺寸检查后，未发现文字裁切、图例遮挡、误差棒标签重叠或坐标范围隐藏数据。

## 7. 三张候选表检查

- `tables/ch4-formal-configuration.md`：冻结信号、场景、导频、SNR、随机总体、BER 口径、调参映射和跨章接口。
- `tables/ch4-formal-headline-results.md`：只列四项承重结果，精度收敛到论文可读的 3 位小数，并保留置信区间。
- `tables/ch4-method-role-comparison.md`：逐方法给出接收端输入、动作、输出、角色与参数语义，明确导频重构标量不是固定 1.0。

表格和 README 已明确：第四章输出可送往后续每偏振支路载波恢复，但现有证据没有联合启用第三章方法，也没有验证逆幅度归一化后第三章选择器统计量是否保持不变。因此只支持模块化接口表述，不支持端到端联合性能主张。

## 8. 不承重材料与禁止推论

以下图或结论不能承担第四章主增益：

- 导频长度图只描述冻结中等湍流场景内的匹配变化，不能证明任意信道下的普遍导频效率。
- mechanism 图是同条件解释指标；尤其不能用跨 SNR、场景或失配条件的混合均值建立因果结论。
- 适用性与边界图不能包装成全场景鲁棒领先；非酉失配增大时，结构假设失配会明显削弱甚至反转优势。
- 理想 CSI 只表示理论参考，不属于可部署接收机。
- 导频重构尺度与前向误差尺度结果近等效，不能隐藏前者或声称后者全面优于前者。
- 历史 confirmation 四格、旧 pooled 均值和本次 formal 曲线不得混合为同一统计总体。
- 未验证 PDL、PMD、FIR、支路不平衡、非等噪声、时变 SOP、CFO、载波恢复联合效应或 LDPC 全链。

## 9. 对外语言检查

- 图例和表格无研究流程代号、质量分级或内部验收术语。
- 首次出现的 BER、SNR、LS、CSI、APSK 和 FEC 在表格或 README 中已展开；图件沿用正文可定义的通行缩写。
- 所有“改善/增益”均指向真实的调参奇异值下限基线，并标明场景、导频数、门限、统计口径和边界。
- 未声称首次、最高水平、全面领先或前向误差尺度优于导频重构尺度。
- 推荐图注均包含场景、统计含义、比较对象和结论边界。

## 10. 当前结论

生成侧检查支持把本包的 `ch4-formal-*` CSV、SVG/PNG 和三张候选表交给独立章节内容审查。旧 confirmation 材料继续保留用于研究过程追溯，但不再作为正式章节结果来源。完整第四章正文、跨图表论证顺序和最终论文排版仍需在后续独立上下文中审查。
