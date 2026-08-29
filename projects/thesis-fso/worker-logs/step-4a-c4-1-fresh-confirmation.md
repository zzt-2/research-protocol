# Worker Log: T071 C4-1 scaled-unitary fresh confirmation

> 2026-08-30 | base=`3203d0b01a69c113c84a0f159ac2c89b0d1b8d12` | task=`T071` | status=`COMPLETE`

## 范围

只执行 D050 授权的一次固定配方 fresh confirmation。未修改或重跑 development raw，未调参、扩网格、增加损伤、切换 comparator；未改 `common/`、`params.py`、Skill/controller、Ch3/Ch5 或论文正文。

## 启动门与 development 只读复算

1. task-control validator：`PASS`（epoch 12 / CP012 / action class 匹配）。
2. 原目标测试 fresh：`13 passed in 6.10s`。
3. development raw-only reducer 输出到系统临时目录；aggregate SHA256 重算值与冻结值均为 `9c236830edc29c96edbe6698a048c910c4d6775486bc51ec2d82b460a2cc2ccb`，terminal=`C4_STRUCTURED_SIGNAL / PROVISIONAL_A`。
4. 冻结 development hashes：manifest=`ad8361f7…ea2b2`，raw=`cee1a881…8bf0b`，aggregate=`9c236830…2ccb`，receipt=`047a3727…4432c`，correctness=`82ef5637…968d2`。

## TDD 与实现

- RED：新增 5 个 confirmation 合同测试，fresh 运行得到 `5 failed`，失败原因为 `confirmation_manifest.json`、`run_confirmation.py`、`confirmation_reducer.py` 尚不存在。
- GREEN：添加独立 manifest、runner、raw-only reducer/CLI 后，confirmation tests=`5 passed in 2.62s`。
- 暂存时发现 confirmation JSON 未固定 EOL 会让 checkout 改变字节哈希；新增 checkout-stability 回归先得到 `1 failed`，只扩展 seam `.gitattributes` 后得到 `1 passed`。未修改 development artifacts，随后只重跑 reducer 更新 receipt/test hash，未重跑 BER。
- runner 明确写入 `confirmation_raw.json`；reducer 明确写入 `confirmation_aggregate.json` 与 `confirmation_receipt.json`。未调用 development 默认输出路径。
- 结果文件使用 `common.save_results()` 注入元数据；manifest 是固定合同而非结果文件。

## 一次冻结运行

- 四格顺序：`14dB/Np2`、`14dB/Np4`、`18dB/Np2`、`18dB/Np4`。
- 每格 64 windows；seed bases=`7000/7100/7200/7300`。
- B1=`0.01/0.001/0.001/0.01`；B2=`1.0/1.0/1.0/1.0`；primary comparator 固定 B2。
- 运行一次成功并生成 raw；未发生科学门失败、correctness 修复或重跑。

## 结果摘要

| cell | B0 BER | B1 BER | B2 BER | C4 BER | O1 BER | C4−B2 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| 14dB/Np2 | 0.08793068 | 0.08802366 | 0.08277035 | 0.07667112 | 0.05273247 | [-0.00954738,-0.00306168] |
| 14dB/Np4 | 0.07928896 | 0.07931185 | 0.07178736 | 0.06990385 | 0.05725527 | [-0.00354064,-0.00019817] |
| 18dB/Np2 | 0.04305935 | 0.04306221 | 0.03875256 | 0.03550529 | 0.02203321 | [-0.00548053,-0.00143516] |
| 18dB/Np4 | 0.02407551 | 0.02412033 | 0.02216578 | 0.02104330 | 0.01726913 | [-0.00216106,-0.00026414] |

Pooled Np2 mean=`-0.00467324`，95% CI=`[-0.00686385,-0.00282661]`，clusters=`128`。frozen terminal=`C4_CONFIRMED_STRUCTURED_SIGNAL`。这不是 `THESIS_METHOD_READY`。

## Raw-only 与完整性审计

- raw-only fresh 内存复算 scientific payload 与保存 aggregate（排除 `_meta`）完全一致；双方 canonical SHA256=`db0094d500ae6f651e4f5f38bd86f3b3ae25405368e5258c692cf61f0ef86dd7`。
- confirmation manifest SHA256=`18c93796ff3e7e0ebf0bf05ee71c94bfd4027218b31a60d0d917d26581aa8a65`；raw SHA256=`55c31e36b7d11e5d0b9e8225805596e0f0f7b127cde26874c7b0b217b0e23101`。
- receipt 检查项：development hash、manifest hash、confirmation-only split、seed arithmetic/non-overlap、paired realization、paired observation、fixed arm parameters、finiteness、truth firewall 均 `PASS`。
- deployable `receiver_action` 签名只有 `arm/x_pilots/y_pilots/y_payload/parameter`；`H_true` 与 payload truth 仅进入离线 O1/scoring。

## 全项目回归边界

按 sim-preflight 从 `projects/simulation/` 运行 `python -m pytest tests/ -q`，在收集阶段被 3 个范围外既有导入错误阻断：`test_direction_lab_controller.py` 与 `test_direction_lab_evidence_gate.py` 加载错位 `methods` 模块后缺少 `run_b0`；`test_prompt012_divergence_audit.py` 加载的 `r_lcr_ber_impact` 缺少 `BLOCK`。从仓库根与规范工作目录均可复现；本任务未修改这些模块，也未扩大范围修复。T071 seam 的完整 19 项相关测试 fresh PASS。

## 约定变更

无。只新增 T071 独立 confirmation 合同、runner、tests 与 artifacts；development、参数、公式、信号模型和评估方法均未变更。

## 边界与下一步

唯一下一步是另一上下文独立 raw 复算。不得追加第二次 confirmation、救场调参、扩格/损伤或由本执行上下文宣布最终方法就绪。
