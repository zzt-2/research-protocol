# Task Brief: CP011 step-092 四项治理修复窄复核

> 来源: S001 / D010 / V004 / H003 / step-092 | 产出位置: `projects/thesis-fso/worker-logs/step-093-cp011-step092-narrow-verifier.md`
> 日期: 2026-08-10
> 唯一任务文档: 执行方只复核 step-092 的 P1-1/P1-2/P2-1/P2-2 与保护回执

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，fresh-context 窄复核 step-092 的四项治理修复。不得重审已关闭的 scientific design，不得运行或实现 D0。

**唯一产出**：只写 `projects/thesis-fso/worker-logs/step-093-cp011-step092-narrow-verifier.md`。

**时间纪律**：4–6 分钟目标，10 分钟硬上限。

## 1. 待复核的四项

1. **P1-1 report stale authorization**：`step4a-a0-preflight.md` 原第 19、217、274 行不得再表达 fresh verifier pending / 未授权 / `ONLY_IF_REVERIFIED`；必须与 header、D010/V004/CP011 和 `D0_EXECUTION_AUTHORIZED=YES` 单义一致，同时保留 D0 非 MVE、非 Step 4a Go、非贡献、非 C1-ext。
2. **P1-2 YAML stale budget status**：`d0-defect-smoke-contract.yaml` 必须仍 parse；顶部 verified/authorized 与 `engineering_budget_days.status` 单义一致。只允许 status 当前化，预算数字和 scientific contract 不得改变。
3. **P2-1 report control owner**：控制 owner 必须指 topic + D010 + V004 + H003，不得仍指 D009/V003/H002。
4. **P2-2 voice provenance**：S001 必须给出三条 D010 原话的原始用户合同路径与可核查行号；逐字对照 `C:\Users\zzt\.codex\attachments\121c6695-cba7-4963-a946-21f10e677f58\pasted-text.txt` 第 147、170、174 行。若逐字一致，voice 不应误标 `[转述]`。

## 2. 冻结与保护

修复后 owner SHA256：

```text
report=63f1d0881fb88cad4044737091fb0abaa7aea27d50b8defd48ec6d8c23c3daf8
yaml=32989ffa52a38fd813c9d0e4da6951fbca66ad30ac5d56ead24d9ae466595936
topic=37d795e2cd58283215b556f4a012ec73fbab2d967dd0e6829eb0bc15cd92a70d
decisions=c066b7f14d230b37026519a197c7c260b54551012e5a686432ced967daec29de
verifications=d4967104b0083101c946ff6165d367b3f8b3a27018c706ed4fecfed3cfc2ef5b
H003=059b7210b92f4bebe294b4231851b138da526775daf06b0052cc28f36d58dc28
S001=e137f586ab66d7118c2516be8f2777b19c518efb5e8f123b0eb9b57c86947424
mission=2369908292c26ef68464aac988162e52dbdd0ecc1ff41f19d5adbad76a098baf
master=46aeefaf2ee8f1cfa2e70cfd76d1d975746efe11cb26c3535c5f1b40ae0c342d
registry=1ef6ef6481dbb3ab2fd9cf3e22d4b2c7fefbf106853a65585ffb7a1a708aecdb
voice=852d152e5539d136607d4ade8572d9c82a908f9ab06e6a837d94a0e434c41209
```

protected p05 SHA256 必须仍为：

```text
7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

禁止修改任何 owner、task brief、源码或 protected logs；禁止 D0 implementation/test/run、web/search/download、仿真、adapter、MVE、commit/push。staging 必须为空，`git diff --check` 必须无 whitespace error。

## 3. 产出格式

```markdown
# Step 093 — CP011 step-092 narrow verifier

## Verdict
PASS/FAIL；P0/P1/P2=x/y/z。

## Four-finding closure
P1-1/P1-2/P2-1/P2-2：CLOSED/OPEN，给路径与行号。

## Scientific/control ceiling
D0 only authorized + NOT_RUN；METHOD_SIGNAL=NONE；adapter/C1-ext/MVE/held-out 仍禁止。

## Protection receipt
11 owner 初末 SHA、p05 4/4、YAML parse、staging、git diff --check、唯一写入。
```

## 4. 验收

- [ ] 四项均 CLOSED。
- [ ] PASS 时 P0/P1/P2=`0/0/0`。
- [ ] scientific contract 未被重写，D0 仍 NOT_RUN。
- [ ] 11 owner SHA 11/11、p05 4/4、staging empty。
- [ ] 唯一写入 step-093。
