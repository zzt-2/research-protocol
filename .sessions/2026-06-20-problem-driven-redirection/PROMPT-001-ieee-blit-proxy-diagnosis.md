# PROMPT-001: 诊断 IEEE blit 为什么连不上（用户浏览器能登，脚本/Playwright 不能）

> 来源: S004 | 任务性质: 单点诊断（不是主线推进，是还 S004 留下的 IEEE 通道债务）
> 日期: 2026-06-22
> 唯一文档: 执行方只看这一个 + blit.py / blit wrapper。主线已落盘的证据见本文件附录。

---

## 0. TL;DR（先读这段，1 分钟）

**你在**: Windows 10（MINGW64/Git Bash），项目根 `D:\code\study\research-protocol`，bash 路径用 `/d/code/study/research-protocol` 或 `cd` 后用相对路径。

**你的任务**: 查清楚 `tools/blit --source ieee` 为什么连不上 IEEE，而**用户的日常浏览器能正常登 ieeexplore.ieee.org**。核心怀疑是**代理/VPN 出口差异**（日常浏览器走了代理，脚本/Playwright 没继承），不是校园网 IP 问题。

**产出**: 回传一个 ≤300 字的诊断结论，回答 3 个问题：
1. 根因是什么（代理？IP？headless 检测？校园网认证绑定？）
2. 怎么修（改 blit.py 加代理参数？让用户开系统代理？用 persistent context 带用户浏览器 profile？）
3. 修了之后能不能跑通——如果能，跑 1 条 query `satellite optical communication` --source ieee --max 10，回传 JSON 里 results 数组有几条

**最高纪律**:
1. **不要复跑 S004 已经验证过的失败路径**（见下面"已排除路径"，别浪费时间重试）
2. **诊断要有证据**——每个结论配一条命令的输出，不靠猜
3. **不要改框架文件、不要改 .sessions/、不要改 landscape.md**——这是工具诊断任务，只允许临时调试 + 必要时改 `tools/blit.py`（改了要说明改哪几行为什么）
4. **不要自己开 git commit**——诊断完把结论回主线，由主线决定怎么落盘

---

## 1. 背景（了解即可，不对照评价）

- `tools/blit` 是 bash wrapper → 调 `tools/blit.py`（Playwright 渲染 IEEE/万方/cbpt/CNKI 提取元数据）。IEEE 限速 50 次/会话 1s 间隔。
- `blit.py` 的 IEEE 分支（`ieee_search` 函数，约 L137）: 直接 `goto` 搜索结果页，用 `safe_goto`（L119，`wait_until` 默认=`load`，timeout=25s，goto 后 sleep 2s）。
- 还有一条带 cookie 的 IEEE 路径（约 L223-226）会先 `goto` 首页做会话激活，但普通 `--source ieee` 搜索走的是无 cookie 的 `ieee_search`。
- 浏览器初始化（L87-94）: `pw.chromium.launch(headless=True)` + `new_context(user_agent=..., locale="zh-CN", viewport=1920x1080)`。**不传 proxy 参数**。

**项目主线状态**（不展开，知道有这事即可）: S004 地勘已落盘 landscape.md（137 主表，纯 API 覆盖）。IEEE 是用户偏好的主力源，blit 连不上是遗留债务，**修通后可以补 IEEE 内容到 landscape.md**，不修也能用现有 137 条推进。这是优化项不是阻塞项。

---

## 2. 任务详情

### 2.1 要回答的核心问题

**为什么 `tools/blit --source ieee "satellite optical communication"` 超时连不上，而用户的 Chrome/Edge 浏览器能正常打开 ieeexplore.ieee.org 并搜索？**

已知差异维度（按可能性排序）：
- **代理/VPN 出口差异**（最可能）: 用户的日常浏览器配了代理扩展（Clash/SwitchyOmega/V2Ray）或系统 VPN，走某个出口能连 IEEE；curl/Playwright 进程默认不继承代理，走裸出口被 IEEE 限速/封锁。
- **校园网认证绑定浏览器 profile**: 校园网 IP 认证可能绑了用户浏览器的 session/cookie，headless 全新实例没有。
- **headless 检测**: IEEE 对 headless Chromium 反爬更严（但 S004 测过 headless=False 也超时，见已排除路径）。

### 2.2 执行方式（建议诊断顺序，每步留证据）

**第一步：确认系统代理配置**
```bash
powershell.exe -NoProfile -Command "Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select-Object ProxyEnable,ProxyServer,AutoConfigURL | Format-List"
```
看 `ProxyEnable`（1=开了系统代理）、`ProxyServer`（代理地址:端口）、`AutoConfigURL`（PAC 脚本 URL）。如果 `ProxyEnable=1` 有 `ProxyServer`，基本确认是代理问题。

**第二步：探测常见本地代理端口**（Clash 7890/7897、V2Ray 10809、SS 1080）
```bash
powershell.exe -NoProfile -Command "@(7890,7897,1080,10809,2080) | ForEach-Object { \$p=\$_; try { \$t=Test-NetConnection -ComputerName 127.0.0.1 -Port \$p -WarningAction SilentlyContinue; Write-Host \"Port \$p : \$(\$t.TcpTestSucceeded)\" } catch {} }"
```
哪个端口 True 就是有代理在跑。

**第三步：用 curl 带代理测 IEEE**（把上一步发现的端口填进去）
```bash
curl -s -o /dev/null -w "with-proxy HTTP %{http_code} time %{time_total}s\n" --max-time 20 -x http://127.0.0.1:7890 https://ieeexplore.ieee.org/
```
如果带代理后 HTTP 200（不是 418），**根因确认 = 代理**。

**第四步：测 Playwright 带代理能不能连**（关键验证）
```bash
python3 -c "
import asyncio
from playwright.async_api import async_playwright
async def t():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(headless=True, proxy={'server':'http://127.0.0.1:7890'})
        ctx = await b.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        page = await ctx.new_page()
        try:
            r = await page.goto('https://ieeexplore.ieee.org/', wait_until='domcontentloaded', timeout=45000)
            print(f'Playwright+proxy: status={r.status}, title={(await page.title())[:60]}')
        except Exception as e:
            print(f'Playwright+proxy FAILED: {type(e).__name__}: {str(e)[:100]}')
        await b.close()
asyncio.run(t())
"
```
（端口按第二步结果换。如果这一步通了，blit 的修法就清楚了。）

**第五步（可选）**: 如果带代理 Playwright 也通，试着改 `blit.py` 的 `_get_browser`/`ieee_search` 加 proxy 参数（或读环境变量 `HTTP_PROXY`/`HTTPS_PROXY`），跑一条真 query 验证。

### 2.3 产出格式（强制，按这个回传）

```markdown
# IEEE blit 诊断结论

## 根因
[一句话 + 证据命令输出。例："系统代理 127.0.0.1:7890 (Clash) 已开启，Playwright 默认不继承；curl 带代理 HTTP 200，不带 418"]

## 修复方案
[具体到改 blit.py 哪几行 / 或让用户设什么环境变量 / 或改 wrapper。如果需要改 blit.py，贴 diff]

## 验证结果
- 跑的 query: `satellite optical communication` --source ieee --max 10
- JSON results 数组条数: N
- 输出文件: search-archive/2026-06-22/landscape-ieee-<slug>.json
- （如果没跑通）失败现象: [具体报错]

## 债务/副作用
[改了 blit.py 影不影响其他 source（万方/cbpt/cnki）？需要用户做什么配合？]
```

---

## 3. 已排除路径（别重试，S004 验证过都失败）

| 路径 | S004 结果 | 别再试 |
|------|----------|--------|
| urllib 纯 HTTP 直连 IEEE | HTTP 418（反爬，瞬间拒绝） | 这是反爬不是连不上，不用再试 |
| curl 直连（无代理） | HTTP 418, 0.9s | 同上 |
| Playwright headless=True, domcontentloaded, 60s timeout | TimeoutError | 加长 timeout 没用，不是慢 |
| Playwright headless=False, domcontentloaded, 45s timeout | TimeoutError | 不是 headless 检测问题 |
| blit.py 原版（safe_goto wait_until=load, 25s） | Page.goto Timeout | 已知，不用复现 |

**结论**: headless/headed 都一样、加 timeout 没用、urllib 和 curl 都 418 → 问题在出口/IP/代理层面，**不在浏览器参数**。所以诊断方向是**代理/网络出口**，不是调 Playwright 参数。

---

## 4. 验收（主线拿到你的结论后这么检查）

- [ ] 根因有证据（附了一条命令的实际输出，不是"应该是代理"这种猜测）
- [ ] 修复方案可执行（改 blit.py 的话有 diff；改环境的话有具体命令）
- [ ] 如果声称修通了，跑了一条真 query 且 JSON results 数组 >0 条
- [ ] 没动框架文件 / .sessions/ / landscape.md（只动了 tools/blit.py 或 search-archive/）
- [ ] 没自己 git commit

---

## 5. 如果诊断中发现是校园网 IP 问题（不是代理）

也把结论说清楚——可能校园网认证绑了用户浏览器 session，headless 带不了。这种情况修法可能是：让用户在校园网环境跑、或用 `launch_persistent_context` 带用户浏览器 profile（`%USERPROFILE%/AppData/Local/Google/Chrome/User Data`）。但**先验证代理假设**，代理是最可能的。

---

## 附录：S004 已验证的关键事实（主线落盘证据，你不用重读 S004）

- 用户原话: "https://ieeexplore.ieee.org/ 我自己看能登啊"（2026-06-22）——这是本诊断的起点，用户浏览器能用。
- 主线（S004 当轮）的"独立验证"有缺陷: 用 curl 测 IEEE 得 418 就接受了子 agent 的"通道失败"结论，但 curl 和 Playwright 机制不同，curl 的 418 是反爬不等于 Playwright 连不上。子 agent 更离谱: 用 urllib 预检得 418 就停了，**根本没跑 blit**。S004 的"IEEE 通道失败"结论**证据不足**，需要重新诊断。
- landscape.md 已基于纯 API（137 条）落盘，IEEE 修通是**补充覆盖**不是从头来。
- blit.py 关键代码位置: 浏览器初始化 L87-94（`launch` 不传 proxy）、`ieee_search` L137（直接 goto 搜索页）、`safe_goto` L119（`wait_until` 默认 load, timeout 25s）、带 cookie 的 IEEE 会话激活路径 L223-226。
