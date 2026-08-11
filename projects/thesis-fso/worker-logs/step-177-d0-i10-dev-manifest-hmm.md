# Step 177 — D0 I10 dev manifest / BPS / HMM reducers

> 2026-08-11 | Groundwork Step 4a D0 implementation preflight | AUTHOR GREEN

## 边界

- 只新增 `freeze.py` 与 `test_d0_dev_freeze.py`；未修改 `common/`、session、owner、science 或 P05 日志。
- 未运行 D0 science、I05 全链、benchmark；未 stage/commit/push。

## 代码改动

- `build_dev_manifest`：从认证 owner 生成 dev seeds、12 cells、五 tuple、六 BPS pair、122×6 canonical float.hex grid、枚举与成员基数。
- `expected_bps_primary_keys` / `select_bps_pair`：闭合 7,200 条逻辑主键，保留 M2/M3 N100 双逻辑身份；按 CW-goodput、CWER、B、Nw 做 exact lexicographic selection。
- `exact_binary64_aggregate`：以 `Fraction.from_float` 保存 binary64 exact numerator / power-of-two denominator / count；显式拒绝 ordinary float chunk sum。
- `select_hmm_pair`：强制 role/cell/pol/member 完整性、receipt/cost、sentinel exclusion；按 clean 0.5 + controlled-target 0.5 精确聚合并稳定 tie-break。

## RED

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
python311 -B -m pytest -p no:cacheprovider `
  test_d0_dev_freeze.py::test_df01... `
  test_d0_dev_freeze.py::test_df02... `
  test_d0_dev_freeze.py::test_df03... `
  test_d0_dev_freeze.py::test_df04... `
  test_d0_dev_freeze.py::test_df05... `
  test_d0_dev_freeze.py::test_df06... -q
```

- 结果：`6 failed in 0.30s`，总耗时 `1.1718445s`。
- 失败原因：六个 exact node 均因 `ModuleNotFoundError: No module named 'freeze'` 失败，符合生产模块尚不存在的预期 RED。
- tie-key 显式化的第二个窄 RED：DF03 `1 failed in 0.97s`，缺少 `bps_selection_key`；随后抽取 owner 顺序 key，并由 selector 直接复用。

## GREEN

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
python311 -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_dev_freeze.py -q
```

- 最终 fresh 结果：`6 passed in 3.14s`，总耗时 `3.9482997s`。
- 负向断言：3 类，全部拒绝：CW-goodput 1024-bit 定义篡改、ordinary float summation、HMM member omission。
- DF06 同时覆盖 BPS row order 与 HMM chunk order不改变 objective/winner。

## Hashes

- `freeze.py`: `2fd78127d41439d441377515f1b9e5726d794edcb16e0409c571d8aef0b4a4fc`
- `test_d0_dev_freeze.py`: `7588b3b41e1b308e5c3657251ac567e208cb269f10676845d7913ea4e4c71968`

## 失败点与风险

- P0/P1：0/0。
- 当前接口是 I10 primitive reducer；I13 仍负责 `fit_common_bps` / `fit_b2_statistics` / `select_b2_tuple`、最终 freeze 与 chronology lock，不在本任务越界实现。

## 下一接口

- I13 可消费 `build_dev_manifest`、`select_bps_pair`、`select_hmm_pair` 与 exact aggregate，增加 DF07–DF10/DF12 和最终 immutable freeze boundary。

## 独立验收 P1 最小修复

### 根因

原 reducer 错把未持久化的 `member_keys/normalized_nll_values` 当 chunk 输入，未消费 owner `B2HmmGridChunkRow` 的 lossless aggregate；入口未强制 typed schema，且 cost 计数跨候选累计。

### RED

- DF01–DF06 + 新负向：`11 failed, 3 passed in 11.64s`，总耗时 `12.8278004s`。
- 真实复现：owner-shaped typed row 错拒、bool CWER 错收、7 类 untyped/range/legacy 输入未按 FreezeError fail closed、跨组 member identity 未拒绝、两候选 cost 错累加。

### 修复

- `select_hmm_pair` 只接受 exact `schemas.B2HmmGridChunkRow`，并以 `row_to_mapping → row_from_mapping` 重验 dataclass-replace 绕过。
- 仅消费 `member_count`、两 manifest SHA、canonical grid hex、exact numerator / power-of-two denominator；删除 ad-hoc member/receipt/cost 输入契约。
- member/computation manifest identity 跨 group 唯一；grid index/hex 与 manifest exact 对齐。
- cost 改为 candidate-local；winner exact=`4560/2400/2160`。
- BPS CW 字段要求 exact int，拒绝 bool CWER。

### GREEN

- 最终 fresh 完整 `test_d0_dev_freeze.py`：`14 passed in 14.13s`，总耗时 `15.3500871s`；其中四个 grid index 负向使用 typed dataclass-replace 绕过构造器后仍由 reducer 重验拒绝。
- 负向断言共 12 项，wrong accept/reject=`0/0`；P0/P1=`0/0`。
- final hashes：
  - `freeze.py`: `349825d8d114352fbb055a81a630df18a6d92d2a80fed7eeb47e1b68ac49c100`
  - `test_d0_dev_freeze.py`: `c9040ccf6c55316f467f60788826cc5a660d0dce05401ea2ac3e287dfac520c3`
