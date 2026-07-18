# [R009] 论文逻辑链定稿版（只含有把握的内容）

> 2026-07-11 | 关联：专题 2026-07-09-thesis-writing / S009（逻辑链讨论）/ S010（因果归因调查 + 轻讲决定）
> 状态：定稿（轻讲粒度，用户 2026-07-11 拍板）

## 调研问题

论文（CCISP 2026，4-6 页）的逻辑链怎么讲，既站得住又不超出有把握的范围？

## 定稿原则（用户拍板，2026-07-11）

1. **轻讲**：篇幅放不下深挖 + 别人都不深挖（R002§C 实证）+ 深挖对卖点无贡献
2. **CCISP 无 rebuttal**（过就过，没过就没）→ 没把握的东西不写进论文，比没把握硬写安全
3. **只放有把握的内容**：数据事实 + 标准结论 + 图印证。没把握的物理归因一律不写
4. **不用黑话**：术语查过标准的才用，自造词不进论文

## 有把握 vs 没把握的边界（写论文前先分清）

### 有把握（能进论文）

| # | 内容 | 证据类型 | 来源 |
|---|---|---|---|
| 1 | NDA 升 M₀=8 次幂去调制（代码事实）| 代码 | `_recovery.py:213` `raised = rx**M0`，M₀=8（`_b11_params.py:36`）|
| 2 | DA 用已知 pilot 符号直除去调制（代码事实）| 代码 | `_recovery.py:153` `angle(rx[pilot]/pilot_sym)` |
| 3 | squaring loss 是教科书结论（升幂放大相位估计误差，低 SNR 受限）| 文献 | V&V 1983 IEEE TIT / Mengali-D'Andrea 1997 / Fitz 1997 TCOM |
| 4 | pilot overhead = 1.25dB（25% 带宽代价）| 数学+文献 | 10log10(4/3)=1.249dB，Shieh-Djordjevic 2010 |
| 5 | "盲估低信噪比不如导频"的数据（弱-中湍流低 SNR）| 数据 | `/tmp/check_nda_low_snr.py`：weak DA/NDA=0.71~0.90，mod 0.80~0.94 |
| 6 | 高信噪比区 NDA 净赢（不付带宽 overhead）| 数据+教科书 | 全湍流场景高 SNR NDA 赢（`/tmp/switch_caliber_audit.py`）|
| 7 | crossover 确实存在 + 随湍流左移（数据事实，不附物理归因）| 数据 | `/tmp/verify_logic_chain.py` 断言1：weak 17.9 / mod 16.8 / strong 10.7dB |
| 8 | 切换选对率 26/29（data 口径）| 数据 | `/tmp/switch_caliber_audit.py`：awgn 8/8 + weak 7/7 + mod 7/7 + strong 4/7 |
| 9 | 净增益（naive 口径，强湍流/上行）| 数据（D004 已验证）| strong +1.26dB / up_str +1.85dB |
| 10 | 切换 vs 固定盲估（低 SNR 避险）| 数据（D002 已验证）| +1.3~2.3dB（CI 下界全正）|

### 没把握（不进论文）

| 内容 | 为什么没把握 | 处理 |
|---|---|---|
| crossover 为什么左移的物理机制 | S010 §7 质疑1：低 SNR/高 SNR 两边都没搞清，循环论证 | 论文只呈现数据事实（左移了），不解释为什么 |
| "盲估低信噪比差"是不是全归因 squaring loss | 混淆变量（盲 h 均衡、fft_foe）未排除，受控切片没跑 | 论文只引教科书结论（squaring loss 是因素之一），不声称"唯一主因" |
| effective/instantaneous SNR 用哪个词 | 块级 ≠ per-symbol，子 agent 建议的 instantaneous 可能误导 | 论文避免用这个词，需要时用"per-block SNR"+显式定义 |

## 逻辑链定稿版

```
背景：星地激光通信，Gamma-Gamma 块衰落信道（标准模型，Al-Habash 2001），
      接收端做载波相位恢复（CPR）

两种方法（DA/NDA trade-off，教科书共识，Mengali-D'Andrea 1997）：
  导频辅助（DA）：用已知 pilot 符号直接除掉调制相位，低信噪比估计精度高
                 代价：花 25% 带宽传 pilot（pilot overhead 1.25dB，Shieh-Djordjevic 2010）
  盲估计（NDA，Mth-power / V&V estimator）：升 M 次幂去调制，不花带宽
                 代价：受 squaring loss 影响，低信噪比相位估计精度下降（V&V 1983）

两法各有优势区（数据支撑，图 2 BER 曲线印证）：
  → 低信噪比区：DA 估计精度优势主导 → DA 净赢（弱-中湍流下 NDA BER 高 10~30%）
  → 高信噪比区：NDA squaring loss 被高信噪比压制 + 不付 overhead → NDA 净赢
  [注：AWGN 全程 NDA 赢——无信道波动，DA 精度优势抵不过 overhead 代价]

BER 曲线交叉（crossover，数据事实）：
  → 两法 BER 曲线有交叉点（低 SNR DA 赢，高 SNR NDA 赢）
  → 交叉点随湍流强度左移（weak ~18dB / mod ~17dB / strong ~11dB）
  [注：只呈现数据事实，不附物理归因——为什么左移没搞清，不写]

切换机制（本工作）：
  → 系统用每块信噪比感知信道条件，自动选更优估计器
  → data 口径选对率 26/29（90%）
  → 低信噪比切 DA 防 squaring loss；高信噪比切 NDA 省 overhead

数字（全 data 口径）：
  净增益（NDA vs DA，强湍流/上行，naive 口径）：+1.26~1.85dB（D004）
  切换 vs 固定 NDA（低信噪比避险）：+1.3~2.3dB（D002）
  选对率：26/29
```

## 跟 S009 修正版的差别

| S009 修正版（待验证） | R009 定稿版 | 改动理由 |
|---|---|---|
| "两法各有死穴" | "两法各有优势区" | "死穴"用词过重，实际是教科书 trade-off |
| "盲估低 SNR 崩溃（升幂放大噪声）" | "盲估受 squaring loss 影响，低 SNR 精度下降" | 用标准术语 + 不夸大成"崩溃"；引 V&V 1983 |
| "crossover 左移（湍流越强 DA 优势区延伸）" | "crossover 随湍流左移（数据事实）" | S010 推翻旧解释，新归因没把握，只留数据事实 |
| "切换是闭环必要环节，不是可选附件" | "切换让系统在两法优势区间自动选优" | D002 证切换净增益不依赖切换本身，"必要环节"过强 |
| "deep fade 伪地板"（已禁，不变量5）| 不出现 | 维持不变量 5 |

## 对决策的影响

- **不新建 D###**：本文件是 research note，不改方向/架构决策。所有数字来自已验证的 D002/D004/D005。
- **S007/D005/R007 勘误已完成**（crossover 方向错误三处标注推翻），本文件继承勘误后的状态。
- **论文写作前置工作清单**（S009 §5）仍待做：术语表 / 公式符号 / 参数表 / 句式映射 / 图表规格。本逻辑链是其中"逻辑链定稿"那一项的产出。

## 结论

逻辑链定稿，只含有把握的内容。核心是 **DA/NDA trade-off（教科书）+ 数据印证 + 切换机制**三段。crossover 只呈现数据事实不附物理归因，"盲估低 SNR 差"引教科书结论不深挖机制。

下一步可以回主线开主控对话，交接逻辑链 + 前置工作清单，主控规划写作流程拆分。

## 附：待查术语清单（论文写之前要敲定的词）

| 术语 | 当前状态 | 处理 |
|---|---|---|
| squaring loss / SNR threshold | ✅ 标准（V&V 1983）| 直接用，引文献 |
| Mth-power / V&V estimator | ✅ 标准 | 直接用 |
| pilot overhead / power penalty | ✅ 标准（1.25dB=10log10(4/3)）| 直接用 |
| deep fade / block fading / Gamma-Gamma | ✅ 标准 | 直接用 |
| DA (Data-Aided) / NDA (Non-Data-Aided) | ✅ 标准 | 直接用 |
| net gain（替代 fair_gain 自造词）| ✅ 已定（S003）| 用 net gain + 脚注说明含 pilot power penalty |
| crossover / crossing point | ❌ 无标准名 | 论文显式定义"SNR at which BER curves intersect" |
| per-block SNR（替代 effective/instantaneous SNR）| ⚠️ 待最终定 | 倾向 per-block + 显式定义，避免 instantaneous 误导 |
| 估计器切换 / estimator switching | ✅ 可接受 | 首次出现写全称 |
| 升幂 / raising to Mth power | ⚠️ 中文写法 | 中文用"升 M 次幂"，英文用"raised to the Mth power" |
