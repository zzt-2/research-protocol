# Task Brief: D0 I02 truth-alias and ndarray-container repair (TDD)

> 来源: step-112 FAIL / receiving-review disposition / I02 candidate | 产出位置: `projects/thesis-fso/worker-logs/step-113-d0-i02-truth-container-repair.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Finding disposition / 假设 / 否决条件

- **ACCEPT P1-1**：literal alias set 未覆盖 owner-equivalent spellings，属真实 truth leakage。
- **ACCEPT P1-2**：object/structured ndarray 只锁 outer write flag，内部对象共享可变，属真实 deep-freeze/truth traversal bypass。
- **REJECT P1-3 as non-defect**：T065 的 oracle 是“permission flag mutation 后**相应 action** fail closed”。单个正权限从 true→false 后仅删除对应 action，其他独立工程权限保持，是 capability 的严格子集/单调收紧，不是授权扩大；owner frozen identity 仍由 owner SHA 与 CP/D/V/epoch绑定。不得把三个独立 permission 耦合成 all-or-nothing，也不得因此改 action implementation。
- 假设：用语义 alias predicate + 拒绝 object/structured ndarray 的明确 plain-numeric-array边界，可最小关闭两项真实 P1 并保持 6 tests 与 downstream 数值数组接口。
- 否决条件：必须放宽 Receiver truth；普通 numeric ndarray 被破坏；safe CPR/SHA 名称误杀；权限语义被改成全局熔断；或 15 分钟内无有效 RED/GREEN，则写 INCOMPLETE。

## 冻结输入

```text
contract.py=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
test=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
step-111=17bc5ac48d2350826ee6b40a43e291bfa54a633d3127086b956730d07ce9a2d0
step-112=9f906374838236e9d2ac95b52f23b936a9cad92e6af3c5508bb824c8dd7b6342
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_contract_views.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
3. Create `projects/thesis-fso/worker-logs/step-113-d0-i02-truth-container-repair.md`

## TDD repair

1. 完整读 T067、step112 findings/matrix、candidate/tests、owner views、T065 oracle。先核 hash/protection。
2. **先扩测试**：在现有 CV05 node 中加入 step112 九个同义名，全部 arbitrary-depth reject；加入 object-dtype 和 structured-dtype ndarray（truth dict及 benign mutable list）均以 `ContractError` 拒绝。保持 ordinary numeric/bool ndarrays defensive-copy+readonly 与 safe keys接受。在 CV09 中明确断言每个正 permission false 后 action set 恰为原五项减对应项，锁定 monotonic least-authority semantics。
3. production 修改前运行 CV04/CV05/CV09 exact nodes；有效 RED 必须来自同义 alias/object ndarray assertions，CV09 可保持 GREEN。立即写 test/source SHA、exact output SHA、失败 rows 到 step113。
4. 最小 production repair：
   - 用可审计的语义 name predicate（normalized token/category rules）覆盖 owner 的 payload/TX bits、true phase/CFO/channel/SNR/fade、slip/event、correctness categories；显式 preserve `common_cpr_phase_trace` 与 source/code/content SHA。不得仅把九个测试词机械塞表而留下同类别显然等价旁路。
   - `_assert_receiver_truth_free` 和 `_deep_freeze` 对 `dtype.hasobject` 或 structured `dtype.fields` ndarray fail closed，给稳定 `ContractError`；plain numeric/bool arrays仍 defensive copy + `writeable=False`。不需要为 Receiver 支持 object array。
   - 不改变 action-set实现，除非仅为注释阐明独立 permission 的 monotonic subset。
5. 不改 tests，重跑 exact three nodes和完整文件 6/6；另复现 step112 matrix的相关失败子集（9 aliases + 4 ndarray checks）全通过。
6. 终检只三目标变化、I01 regression/no CV06–08/no runner/science、p05/cache/staging/HEAD；不 commit/push。

## 命令/边界

Windows Python 3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、`-B`、pytest `-p no:cacheprovider`。禁止 benchmark/science/web/search/download/安装。目标 8 分钟，15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；accepted/rejected finding disposition；RED/GREEN/matrix counts；SHA/protection；terminal 仅 `I02_REPAIR_READY_FOR_FRESH_REVERIFICATION` 或 named blocker。
