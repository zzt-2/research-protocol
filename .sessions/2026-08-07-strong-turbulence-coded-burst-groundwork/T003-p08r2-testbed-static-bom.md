# Task Brief: P08-R2/Sionna coded-chain 静态 BOM

> 来源: S001 | 产出位置: `.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R003-p08r2-testbed-static-bom.md`
> 日期: 2026-08-07
> 唯一文档: 执行方可读 `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_*`、相关 worker logs 与结果 schema

## 0. TL;DR（执行方先读）

只读检查现有 P08-R2/Sionna 5G NR LDPC/BICM/prefix-LS/stateful trajectory 资产，估算 coded-burst 新 testbed 的最小 adapter 与完整重建工期。绝对禁止运行或修改脚本。

最高纪律：

1. 只读 `rg/Get-Content/git show`；禁止 Python、测试、import、仿真或生成新结果。
2. P08-R2 不是有效科学包，只能按文件事实列工程资产；不继承其历史 verdict。
3. 明确检查当前 channel lifecycle 是否跨 codeword 保持相关性、interleaver 是否可控、raw schema 是否含 codeword/fade/burst 边界。
4. 分别估算“最小 adapter”和“完整 testbed”；若必须重建 coded-chain+时间相关信道+interleaver runner 且明显 >5 天，标风险。
5. 不改 `common/`、`params.py`、旧 raw/result、Skill 或 `p05_run*.log`。

## 1. 背景

P08-R/R2 历史修复保留：5G NR BG2 rate-matched LDPC、Gray-16QAM BICM、3GPP §5.4.2.2 bit interleaver、prefix-LS receiver-visible noise estimation、trajectory-cluster metric 与 per-codeword evidence。但它们的旧科学 verdict 不授权复用；本轮只问工程可用性。

## 2. 任务详情

### 2.1 检查项

- codec identity、码长/码率/每 trajectory codeword 数、Sionna API 位置；
- BICM/interleaver 是否固定在 encoder 内部、能否暴露 permutation/placement adapter；
- channel generator 是否 stateful，相关性持续到 symbol/block/codeword/trajectory 哪一级；
- GG 参数来源、prefix-LS、receiver-visible information 边界；
- raw/result schema 是否支持 per-codeword fade、boundary、LLR、FER/outage 分类；
- runner 是否支持 fixed deep comparator、continuous mapping、parity placement、segmentation；
- delay/overhead 是否已进入 metric。

### 2.2 产出格式

R003 必须包含：资产 BOM（文件:行号/接口/可复用性）；缺失接口表；最小 adapter 工序与人日区间；完整 testbed 工序与人日区间；>5 天风险判定；静态 semantic gaps；明确“未运行/未修改”。

## 3. 已知陷阱

- `num_bits_per_symbol=4` 启用的 3GPP interleaver 不等于可研究的 channel-aware placement 接口。
- `stateful trajectory` 的标签不证明跨 codeword 相关；必须沿 caller→generator 查生命周期。
- 结果里 per-cw FER 不等于记录了 burst boundary/fade trajectory。
- P08-R2 receiver γ-free 修复不证明新 metric/action 合法。

## 4. 验收

- [ ] 所有资产结论都有文件+行号。
- [ ] lifecycle、interleaver controllability、schema、metric 四项有明确 YES/NO/PARTIAL。
- [ ] 两档工期分开，>5 天风险有依据。
- [ ] git status 证明无本任务写入（除 R003 报告）。

## 附：产出回传位置

`.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R003-p08r2-testbed-static-bom.md`
