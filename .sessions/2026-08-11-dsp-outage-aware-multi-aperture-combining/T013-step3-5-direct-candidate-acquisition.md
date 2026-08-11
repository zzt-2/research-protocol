# [T013] Step 3.5 直接候选获取

> 2026-08-11 | owner: Step 3.5 主线程 | timebox: 15 min

## 目标

只做新高相关候选的已有资产核查、合法获取与内容质量门，不做方法裁决。

## 范围

- MUST DOI：10.1016/j.optcom.2023.129722；10.1016/j.optlastec.2025.113235；10.1016/j.optcom.2025.132812；10.1016/j.optcom.2026.133153。
- SHOULD DOI（时间允许依优先级）：10.1364/OE.561252；10.1109/ICECE54449.2021.9674283；10.1016/j.optcom.2020.126078；10.1016/j.optcom.2020.126468；10.1109/LPT.2017.2777908。
- 先查 worktree 与共享 root 既有全文；缺失项依 `stages/gw-acquire.md` 合法通道止损。不得使用 webReader、ResearchGate 或绕访问控制。
- 不读方法全文、不判 exact collision、不进入 Step 4a。

## 必须输出

- 每篇：title/DOI、已有/新获取/失败、source provenance、路径、SHA256、字节数、有效行数、qualified。
- 失败项列尝试轮次与 limitation；若找到全文，仅做 title/content 质量门。
- 写 `projects/thesis-fso/worker-logs/step-3-5-direct-candidate-acquisition.md`。

## 禁止

- 不修改专题 D/V/H、master-state、registry。
- 不提交、不 push、不碰 unrelated dirty files。
