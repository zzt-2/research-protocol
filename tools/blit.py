"""
浏览器文献检索工具 — IEEE / 万方 / cbpt / CNKI

独立于 API 搜索管线，用 Playwright 渲染 SPA 页面提取元数据。
限速策略内置，适合低频使用。

IEEE/CNKI 支持 --download 自动下载 PDF（校园网 IP 机构认证）。
CNKI 源额外需要 cookie 认证，过期时自动弹窗让用户验证。

用法:
  python blit.py "LEO satellite handover" --source ieee
  python blit.py "beam hopping DRL" --source ieee --download papers/downloads/
  python blit.py "低轨卫星 切换" --source wanfang
  python blit.py "混合式教学 实证" --source cnki
  python blit.py "混合式教学 实证" --source cnki --doc-type phd
  python blit.py "混合式教学 实证" --source cnki --doc-type journal,phd --download papers/downloads/
  python blit.py "民族文化" --source cnki --doc-type phd --institution "清华大学"
"""

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path

# 标题一致性校验（P0-B）：复用 litdownload.title_verify 的 token 重叠逻辑。
# blit 只下裸 PDF、不走 litdownload 流水线，故单独在下载后校验 PDF 首页标题，
# 结果写进同目录 {pdf_stem}.meta.json（轻量 sidecar，不接入 papers/index.json）。
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from litdownload.title_verify import verify_pdf_title
    _TITLE_VERIFY_AVAILABLE = True
except Exception:
    _TITLE_VERIFY_AVAILABLE = False


def _save_title_meta(pdf_path: Path, expected_title: str) -> None:
    """下载后校验 PDF 首页标题，把结果写进 {pdf_stem}.meta.json。

    失败静默——校验不可用或异常都不阻断下载。sidecar 字段与
    litdownload metadata.json 的 title_check 三字段对齐，便于统一 grep。
    """
    if not _TITLE_VERIFY_AVAILABLE or not pdf_path.exists():
        return
    try:
        check = verify_pdf_title(pdf_path, expected_title)
        meta = {
            "expected_title": expected_title,
            "real_title": check.get("real_title"),
            "title_check": check.get("status"),
            "title_overlap": check.get("overlap"),
            "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        meta_path = pdf_path.with_suffix(".meta.json")
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        if check.get("status") == "mismatch":
            print(f"    ⚠️  TITLE-MISMATCH: 实际是《{(check.get('real_title') or '')[:50]}》"
                  f"(overlap={check.get('overlap'):.2f})", file=sys.stderr)
    except Exception as e:
        print(f"    [title_check skip] {e}", file=sys.stderr)

# ──────────── 限速配置 ────────────

RATE_LIMITS = {
    "ieee":    {"max": 50, "interval": 1},
    "wanfang": {"max": 10, "interval": 6},
    "cbpt":    {"max": 30, "interval": 3},
    "cnki":    {"max": 30, "interval": 3},
}

_session_counts = {k: 0 for k in RATE_LIMITS}
_browser = None
_context = None
_page = None
_cookie_file = Path(__file__).resolve().parent.parent / "cnki_cookies.json"


def _detect_proxy() -> dict | None:
    """探测可用的 HTTP 代理，供 chromium.launch(proxy=...) 使用。

    优先级（PROMPT-001 诊断结论：用户日常浏览器走系统代理 127.0.0.1:7897
    能稳定访问 IEEE，Playwright 默认不继承，必须显式传）：
      1. 环境变量 HTTPS_PROXY/HTTP_PROXY（显式覆盖）
      2. Windows 注册表 HKCU Internet Settings ProxyServer（系统代理）
      3. 探测常见本地端口 7897/7890/10809/1080
    返回 {'server': 'http://host:port'} 或 None。
    """
    import os
    for env_key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        v = os.environ.get(env_key)
        if v:
            return {"server": v}
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        ) as key:
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if enabled:
                server, _ = winreg.QueryValueEx(key, "ProxyServer")
                # ProxyServer 可能是 "host:port" 或 "http=host:port;https=..."
                first = server.split(";")[0]
                if "=" in first:
                    first = first.split("=", 1)[1]
                if first and ":" in first:
                    return {"server": f"http://{first}"}
    except Exception:
        pass
    return None


# ──────────── 浏览器管理 ────────────

async def get_page():
    global _browser, _context, _page
    if _page and not _page.is_closed():
        return _page
    from playwright.async_api import async_playwright
    pw = await async_playwright().start()
    proxy = _detect_proxy()
    launch_kwargs = {"headless": True}
    if proxy:
        print(f"  [proxy] 使用代理 {proxy['server']}", file=sys.stderr)
        launch_kwargs["proxy"] = proxy
    _browser = await pw.chromium.launch(**launch_kwargs)
    _context = await _browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        locale="zh-CN",
        viewport={"width": 1920, "height": 1080},
        accept_downloads=True,
    )
    _page = await _context.new_page()
    return _page


async def cleanup():
    global _browser, _context, _page
    if _browser:
        await _browser.close()
        _browser = _context = _page = None


def check_rate(source: str) -> bool:
    cfg = RATE_LIMITS[source]
    if _session_counts[source] >= cfg["max"]:
        print(f"  [{source}] 已达会话上限 ({cfg['max']}次)", file=sys.stderr)
        return False
    return True


def record(source: str):
    _session_counts[source] += 1


async def safe_goto(page, url, timeout=25000, wait_until="load",
                   wait_for_selector: str | None = None, retries: int = 0):
    """导航 + 可选等待选择器 + 可选重试。

    wait_until 默认沿用 "load" 以保持向后兼容；IEEE 等 SPA 页面的 window.onload
    因长轮询/keep-alive 连接永不触发，必须显式传 "domcontentloaded"，否则 goto
    必然 timeout（PROMPT-001 诊断结论）。

    wait_for_selector 用于 SPA 异步渲染兜底：DOM ready 后内容未必渲染完，
    显式等结果容器出现。retries 为重试次数，应对 IEEE 反爬瞬态限流。
    """
    for attempt in range(retries + 1):
        try:
            resp = await page.goto(url, timeout=timeout, wait_until=wait_until)
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=15000)
                except Exception:
                    pass
            await asyncio.sleep(2)
            return resp
        except Exception as e:
            if attempt < retries:
                wait_s = 8 * (attempt + 1)
                print(f"  请求失败（第{attempt+1}次，{wait_s}s 后重试）: {e}",
                      file=sys.stderr)
                await asyncio.sleep(wait_s)
                continue
            print(f"  请求失败: {e}", file=sys.stderr)
            return None
    return None


# ──────────── IEEE ────────────

async def ieee_search(query: str, max_results: int = 25) -> list[dict]:
    page = await get_page()
    if not check_rate("ieee"):
        return []

    encoded = query.replace(" ", "%20")
    url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={encoded}"
    print(f"[IEEE] 搜索: {query}")

    # IEEE 搜索是 SPA + 反爬瞬态限流。PROMPT-001 诊断：
    #   - wait_until=load 永远超时（onload 不触发）→ 用 domcontentloaded
    #   - DOM ready 时结果项未必渲染完 → 叠加 wait_for_selector
    #   - 同一 IP 连续访问偶发被临时拉黑 → 失败重试 1 次，间隔 8s
    resp = await safe_goto(
        page, url,
        wait_until="domcontentloaded", timeout=45000,
        wait_for_selector="div[class*='List-results'], xpl-results-list, .result-item",
        retries=1,
    )
    if not resp:
        return []
    record("ieee")

    papers = await page.evaluate(r"""() => {
        const items = document.querySelectorAll('div[class*="result-item"]:has(h3)');
        if (!items.length) return [];
        const seen = new Set();
        // venue 提取多策略：IEEE 搜索结果 venue 通常在 description 区域，
        // 格式 "Year: YYYY | Venue Name | Cited by: Papers (N) | ..."
        const KNOWN_FIELDS = /^(Year:|Cited by|Pages|Early Access|Conference|Volume|Issue|DOI)/i;
        return Array.from(items).map(el => {
            const text = el.innerText || '';
            const titleEl = el.querySelector('h3, [class*="title"]');
            const title = titleEl ? titleEl.innerText.trim() : '';
            const authorEl = el.querySelector('[class*="author"]');
            const authors = authorEl
                ? authorEl.innerText.split(/[;,]/).map(s => s.trim()).filter(Boolean)
                : [];
            const citedM = text.match(/Cited by[:\s]*Papers\s*\((\d+)\)/i);
            const yearM = text.match(/Year:\s*(\d{4})/);
            // 策略1: description / publisher class 元素（IEEE Xplore 常见）
            let venue = '';
            const descEl = el.querySelector('[class*="description"], [class*="publisher"], [class*="parent-pub"]');
            if (descEl) {
                const parts = descEl.innerText.split(/\s*\|\s*|\n/);
                for (const part of parts) {
                    const p = part.trim();
                    if (p && !KNOWN_FIELDS.test(p) && p.length > 3) { venue = p; break; }
                }
            }
            // 策略2: 从完整 innerText 正则提取（fallback）
            if (!venue) {
                const vm = text.match(/Year:\s*\d{4}\s*[\|\n]\s*([^|\n]+?)(?:\s*[\|\n]|$)/);
                if (vm) {
                    const v = vm[1].trim();
                    if (v && !KNOWN_FIELDS.test(v) && v.length > 3) venue = v;
                }
            }
            const link = el.querySelector('a[href*="document"], a[href*="abstract"]');
            const url = link ? link.href : '';
            if (seen.has(url)) return null;
            seen.add(url);
            return {
                title, authors,
                citations: citedM ? parseInt(citedM[1]) : 0,
                year: yearM ? parseInt(yearM[1]) : null,
                venue,
                url,
            };
        }).filter(p => p && p.title.length > 3);
    }""")

    results = []
    for p in papers[:max_results]:
        results.append({
            "title": p["title"],
            "authors": p.get("authors", []),
            "abstract": "",
            "year": p.get("year"),
            "venue": p.get("venue", ""),
            "citation_count": p.get("citations", 0),
            "doi": "",
            "url": p.get("url", ""),
            "source": "ieee",
        })
    print(f"  获取 {len(results)} 条")
    return results


# ──────────── IEEE 下载 ────────────

async def _ieee_download_paper(ctx, arnumber: str, save_dir: Path, expected_title: str = "") -> Path | None:
    """下载单篇 IEEE 论文 PDF。需要校园网 IP 机构认证。"""
    pdf_url = f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={arnumber}"
    try:
        resp = await ctx.request.get(pdf_url)
        if resp.status != 200:
            print(f"    ❌ {arnumber}: HTTP {resp.status}", file=sys.stderr)
            return None
        body = await resp.body()
        if not body or len(body) < 1024 or body[:4] != b'%PDF':
            print(f"    ❌ {arnumber}: 响应非有效 PDF ({len(body)} bytes)", file=sys.stderr)
            return None
        save_path = save_dir / f"{arnumber}.pdf"
        save_path.write_bytes(body)
        print(f"    ✅ {arnumber}.pdf ({len(body):,} bytes)")
        # P0-B：下载后校验 PDF 首页标题（失败静默，不阻断下载）
        if expected_title:
            _save_title_meta(save_path, expected_title)
        return save_path
    except Exception as e:
        print(f"    ❌ {arnumber}: {e}", file=sys.stderr)
        return None


async def ieee_download(results: list[dict], save_dir: str) -> list[Path]:
    """批量下载 IEEE 搜索结果的 PDF。"""
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    page = await get_page()
    ctx = page.context

    # 建立会话（访问任意 IEEE 页面激活机构认证）
    print("[IEEE] 建立会话...")
    await page.goto("https://ieeexplore.ieee.org/", wait_until="domcontentloaded", timeout=30000)
    # 注：此行原本就已是 domcontentloaded；保留并明确注释，与 ieee_search 修复策略对齐。
    await asyncio.sleep(2)
    try:
        await page.click('button:has-text("Accept")', timeout=3000)
    except Exception:
        pass

    downloaded = []
    for i, r in enumerate(results, 1):
        url = r.get("url", "")
        # 提取 arnumber
        m = re.search(r'/document/(\d+)', url)
        if not m:
            print(f"    ⏭️ [{i}] 无 arnumber: {r.get('title', '')[:50]}", file=sys.stderr)
            continue
        arnumber = m.group(1)
        target = save_path / f"{arnumber}.pdf"
        if target.exists():
            print(f"    ⏭️ [{i}] 已存在: {arnumber}.pdf")
            downloaded.append(target)
            continue
        print(f"  [{i}/{len(results)}] {r.get('title', '')[:60]}")
        result = await _ieee_download_paper(ctx, arnumber, save_path,
                                            expected_title=r.get("title", ""))
        if result:
            downloaded.append(result)
        await asyncio.sleep(1)  # 礼貌延迟

    print(f"\n[IEEE] 下载完成: {len(downloaded)}/{len(results)} 篇")
    return downloaded


# ──────────── 万方 ────────────

async def wanfang_search(query: str, max_results: int = 20, doc_type: str = "journal") -> list[dict]:
    page = await get_page()
    if not check_rate("wanfang"):
        return []

    is_thesis = any(t.strip() in ("phd", "master") for t in doc_type.split(","))
    base_path = "thesis" if is_thesis else "paper"
    url = f"https://s.wanfangdata.com.cn/{base_path}?q={query}"
    label = "学位论文" if is_thesis else ""
    print(f"[万方] 搜索: {query}" + (f" | {label}" if label else ""))

    resp = await safe_goto(page, url)
    if not resp:
        return []

    if "verify" in page.url.lower():
        print("  ❌ 被验证码拦截，IP 可能已封禁", file=sys.stderr)
        return []

    record("wanfang")

    papers = await page.evaluate(r"""() => {
        const items = document.querySelectorAll('.normal-list');
        if (!items.length) return [];
        return Array.from(items).map(item => {
            const title = item.querySelector('.title')?.innerText?.trim() || '';
            const authorEls = item.querySelectorAll('.author-area .authors');
            const authors = [];
            for (const a of authorEls) {
                const t = a.innerText.trim();
                if (t && !/\d{4}年/.test(t) && t.length < 30) authors.push(t);
            }
            const abstract = item.querySelector('.abstract-area span:last-child')?.innerText?.trim() || '';
            const kwEls = item.querySelectorAll('.keywords-list');
            const keywords = Array.from(kwEls).map(el => el.innerText.trim());
            const journal = (item.querySelector('.periodical-title')?.innerText || '').replace(/[《》]/g, '').trim();
            const docType = item.querySelector('.essay-type')?.innerText?.trim() || '';
            const areaText = item.querySelector('.author-area')?.innerText || '';
            const yearM = areaText.match(/(\d{4})年/);
            const btnText = item.querySelector('.button-area')?.innerText || '';
            const citedM = btnText.match(/被引[：:]\s*(\d+)/);
            const dlM = btnText.match(/下载[：:]\s*(\d+)/);
            const labels = [];
            if (areaText.includes('北大核心')) labels.push('北大核心');
            if (areaText.includes('CSCD')) labels.push('CSCD');
            if (areaText.includes('EI')) labels.push('EI');
            const id = item.querySelector('.title-id-hidden')?.innerText?.trim() || '';
            return { title, authors, abstract, keywords, journal, docType,
                     year: yearM ? parseInt(yearM[1]) : null,
                     citations: citedM ? parseInt(citedM[1]) : 0,
                     downloads: dlM ? parseInt(dlM[1]) : 0, labels, id };
        }).filter(p => p.title.length > 3);
    }""")

    # Hover 取作者单位（仅前几篇）
    affiliations_map = {}
    author_els = await page.query_selector_all(".authors")
    for idx, el in enumerate(author_els[:max_results * 3]):
        await el.hover()
        await asyncio.sleep(0.3)
        org_el = await page.query_selector("[class*='org']")
        if org_el:
            org_text = (await org_el.inner_text()).strip()
            if org_text:
                affiliations_map[idx] = org_text

    # 按学位级别后过滤（essay-type 字段：硕士论文/博士论文）
    type_filter = None
    if "phd" in [t.strip() for t in doc_type.split(",")] and "master" not in [t.strip() for t in doc_type.split(",")]:
        type_filter = "博士"
    elif "master" in [t.strip() for t in doc_type.split(",")] and "phd" not in [t.strip() for t in doc_type.split(",")]:
        type_filter = "硕士"
    if type_filter:
        before = len(papers)
        papers = [p for p in papers if type_filter in p.get("docType", "")]
        if len(papers) < before:
            print(f"  [过滤] 学位级别限定后保留 {len(papers)}/{before} 条", file=sys.stderr)

    results = []
    for p in papers[:max_results]:
        results.append({
            "title": p["title"],
            "authors": p.get("authors", []),
            "abstract": p.get("abstract", ""),
            "year": p.get("year"),
            "venue": p.get("journal", ""),
            "citation_count": p.get("citations", 0),
            "doi": "",
            "url": url,
            "source": "wanfang",
            "keywords": p.get("keywords", []),
            "doc_type": "thesis" if "论文" in p.get("docType", "") else "journal",
            "quality_labels": p.get("labels", []),
            "download_count": p.get("downloads", 0),
        })
    print(f"  获取 {len(results)} 条")
    return results


# ──────────── cbpt ────────────

async def cbpt_extract(paper_url: str) -> dict | None:
    page = await get_page()
    if not check_rate("cbpt"):
        return None

    resp = await safe_goto(page, paper_url)
    if not resp:
        return None
    record("cbpt")

    if "verify" in page.url.lower():
        return None

    data = await page.evaluate(r"""() => {
        const s = (sel) => document.querySelector(sel)?.innerText?.trim() || '';
        const title = s('.paperDetail_tt');
        const vol = s('.paperDetail_vol');
        const doiRaw = s('.paperDetail_doi');
        const authorEls = document.querySelectorAll('.paperDetail_author');
        const authors = [], affiliations = [];
        for (const el of authorEls) {
            const t = el.innerText.trim();
            if (/^\d+\./.test(t)) affiliations.push(t);
            else if (t && !/关键词|KeyWords/.test(t) && t.length < 80) authors.push(t);
        }
        const pd1 = s('.paperDetail_html.pd1');
        let abstract = '', keywords = [];
        if (pd1) {
            const absM = pd1.match(/摘\s*要[：:]\s*\n?\n?([\s\S]*?)(?=\n\s*(?:关键词|Abstract))/);
            if (absM) abstract = absM[1].trim();
            const kwM = pd1.match(/关键词[：:]\s*\n?([\s\S]*?)(?=\n\s*(?:Abstract|Key\s*words|$))/);
            if (kwM) keywords = kwM[1].trim().split(/[;；]/).map(x => x.trim()).filter(Boolean);
        }
        return { title, vol, doiRaw, authors, affiliations, abstract, keywords, journal: document.title };
    }""")

    if not data or not data.get("title"):
        return None

    doi = ""
    if data.get("doiRaw"):
        m = re.search(r"10\.\S+", data["doiRaw"])
        doi = m.group() if m else ""

    year = None
    if data.get("vol"):
        ym = re.match(r"(\d{4})", data["vol"])
        year = int(ym.group(1)) if ym else None

    return {
        "title": data["title"],
        "authors": data.get("authors", []),
        "abstract": data.get("abstract", ""),
        "year": year,
        "venue": data.get("journal", ""),
        "citation_count": 0,
        "doi": doi,
        "url": paper_url,
        "source": "cbpt",
        "keywords": data.get("keywords", []),
        "affiliations": data.get("affiliations", []),
        "volume_issue": data.get("vol", ""),
    }


async def cbpt_journal_search(journal: str, query: str, max_results: int = 20) -> list[dict]:
    page = await get_page()
    if not check_rate("cbpt"):
        return []

    base = f"https://{journal}.cbpt.cnki.net"
    url = f"{base}/portal/journal/portal/client/advSearchResult"
    print(f"[cbpt] 搜索 {journal}: {query}")

    resp = await safe_goto(page, url)
    if not resp:
        return []
    record("cbpt")

    inputs = await page.query_selector_all("input[type='text']")
    visible = [i for i in inputs if await i.is_visible()]
    if visible:
        await visible[0].fill(query)
        btn = await page.query_selector("a[onclick*='searchCon']")
        if btn:
            await btn.click()
            await asyncio.sleep(3)

    links = await page.evaluate(r"""() => {
        return Array.from(document.querySelectorAll('a[href*="paper"]'))
            .map(a => ({ text: a.innerText.trim().substring(0, 100), href: a.href }))
            .filter(l => l.text.length > 3 && l.href.includes('/paper/'));
    }""")

    if not links:
        print("  无结果", file=sys.stderr)
        return []

    results = []
    for link in links[:max_results]:
        if not check_rate("cbpt"):
            break
        paper = await cbpt_extract(link["href"])
        if paper:
            results.append(paper)
    print(f"  获取 {len(results)} 条")
    return results


# ──────────── CNKI ────────────

async def _load_cnki_cookies() -> list[dict] | None:
    if not _cookie_file.exists():
        return None
    try:
        return json.loads(_cookie_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


async def _save_cnki_cookies(cookies: list[dict]):
    _cookie_file.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")


async def _refresh_cnki_cookies():
    """cookie 过期时弹有头浏览器，让用户完成验证后保存 cookie。"""
    print("[CNKI] Cookie 过期，弹出浏览器请完成验证...", file=sys.stderr)
    from playwright.async_api import async_playwright
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=False)
    ctx = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        locale="zh-CN",
        viewport={"width": 1280, "height": 800},
    )
    page = await ctx.new_page()
    await page.goto("https://kns.cnki.net/", timeout=60000)

    for _ in range(300):
        await asyncio.sleep(1)
        title = await page.title()
        if "安全验证" not in title and len(title) > 0:
            break
    else:
        await browser.close()
        return False

    await asyncio.sleep(2)
    cookies = await ctx.cookies()
    await _save_cnki_cookies(cookies)
    print(f"[CNKI] Cookie 已刷新 ({len(cookies)} 条)", file=sys.stderr)
    await browser.close()
    return True


async def _cnki_ensure_cookies(ctx) -> bool:
    """确保 context 有有效的 CNKI cookie，必要时弹窗刷新。"""
    cookies = await _load_cnki_cookies()
    if cookies:
        await ctx.add_cookies(cookies)
        return True
    return await _refresh_cnki_cookies()


async def _cnki_check_captcha(page) -> bool:
    """检查是否被安全验证拦截。返回 True 表示需要刷新 cookie。"""
    title = await page.title()
    return "安全验证" in title


async def _cnki_grid_api_search(page, query: str, institution: str, doc_type: str, max_results: int) -> list[dict]:
    """通过 grid API POST 搜索（学位论文按 Classid 区分硕/博）。"""
    # Classid 映射（抓包验证）：硕士=JQIRZIYA, 博士=RMJLXHZ3
    CLASSID_MAP = {"phd": "RMJLXHZ3", "master": "JQIRZIYA"}
    types = [t.strip() for t in doc_type.split(",")]
    primary = types[0] if types else "journal"

    if primary in CLASSID_MAP:
        resource, classid = "DISSERTATION", CLASSID_MAP[primary]
    else:
        resource, classid = "CROSSDB", "WD0FTY92"

    query_items = [
        {"Field": "SU", "Value": query, "Operator": "TOPRANK", "Logic": 0, "Title": "主题"},
    ]
    if institution:
        query_items.append({"Field": "LY", "Value": institution, "Operator": "TOPRANK", "Logic": 0, "Title": "学位授予单位"})
    qj = json.dumps({
        "Platform": "", "Products": "",
        "Resource": resource, "Classid": classid,
        "QNode": {"QGroup": [{"Key": "Subject", "Title": "", "Logic": 0,
                              "Items": query_items, "ChildItems": []}]},
        "ExScope": 1, "SearchType": 2, "Rlang": "CHINESE",
        "KuaKuCode": "", "Expands": {}, "SearchFrom": 1,
    }, ensure_ascii=False)

    items = await page.evaluate("""async (p) => {
        const fd = new URLSearchParams();
        fd.set('boolSearch', 'true');
        fd.set('QueryJson', p.qj);
        fd.set('pageNum', '1');
        fd.set('pageSize', String(p.max));
        fd.set('dstyle', 'listmode');
        fd.set('aside', p.inst ? '主题：' + p.query + '　学位授予单位：' + p.inst : '主题：' + p.query);
        fd.set('CurPage', '1');
        if (p.dbPrefix) fd.set('dbPrefix', p.dbPrefix);
        try {
            const r = await fetch('/kns8s/brief/grid', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: fd.toString()
            });
            const html = await r.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const rows = doc.querySelectorAll('.result-table-list tbody tr');
            return Array.from(rows).map(row => {
                const a = row.querySelector('.name a');
                const hr = a?.getAttribute('href') || '';
                return {
                    title: a?.innerText?.trim() || '',
                    href: hr ? new URL(hr, 'https://kns.cnki.net').href : '',
                    authors: Array.from(row.querySelectorAll('.author span')).map(x => x.innerText.trim()).filter(x => x && x.length < 20),
                    source: row.querySelector('.source')?.innerText?.trim() || '',
                    date: row.querySelector('.date')?.innerText?.trim() || '',
                    cite: parseInt(row.querySelector('.quote')?.innerText?.trim()) || 0,
                    dbid: a?.getAttribute('data-dbname') || ''
                };
            }).filter(r => r.title.length > 3);
        } catch (e) { return []; }
    }""", {"qj": qj, "max": max_results, "query": query, "inst": institution})
    return items or []


async def cnki_search(query: str, max_results: int = 20, download_dir: str | None = None, doc_type: str = "journal", institution: str | None = None) -> list[dict]:
    global _browser, _context, _page

    if not check_rate("cnki"):
        return []

    if "bachelor" in [t.strip() for t in doc_type.split(",")]:
        print("[CNKI] 错误：知网不收录本科论文。万方同样不收录。维普(https://www.cqvip.com/)可能有少量覆盖。", file=sys.stderr)
        return []

    print(f"[CNKI] 搜索: {query}" + (f" | 学位授予单位: {institution}" if institution else ""))

    # 启动浏览器并加载 cookie
    from playwright.async_api import async_playwright
    pw = await async_playwright().start()

    need_refresh = False
    cookies = await _load_cnki_cookies()
    if not cookies:
        need_refresh = True

    _browser = await pw.chromium.launch(headless=True)
    _context = await _browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        locale="zh-CN",
        viewport={"width": 1920, "height": 1080},
        accept_downloads=True,
    )

    if not need_refresh:
        await _context.add_cookies(cookies)

    _page = await _context.new_page()

    # 访问搜索页建立 session
    types = [t.strip() for t in doc_type.split(",")]
    encoded_query = query.replace(" ", "+")
    # 学位论文用 classid 参数（Classid 映射见 _cnki_grid_api_search）
    CLASSID_MAP = {"phd": "RMJLXHZ3", "master": "JQIRZIYA"}
    primary = types[0] if types else "journal"
    if primary in CLASSID_MAP:
        search_url = f"https://kns.cnki.net/kns8s/defaultresult/index?kw={encoded_query}&classid={CLASSID_MAP[primary]}&korder=SU"
    else:
        search_url = f"https://kns.cnki.net/kns8s/defaultresult/index?kw={encoded_query}"
    await _page.goto(search_url, timeout=45000)
    await _page.wait_for_load_state("domcontentloaded", timeout=30000)
    await asyncio.sleep(3)  # 等 JS 渲染搜索结果

    # 检查验证码
    if await _cnki_check_captcha(_page):
        await _browser.close()
        _browser = _context = _page = None
        print("[CNKI] Cookie 已过期，需要刷新...", file=sys.stderr)
        if not await _refresh_cnki_cookies():
            print("[CNKI] Cookie 刷新失败", file=sys.stderr)
            return []
        # 刷新后重试
        _browser = await pw.chromium.launch(headless=True)
        _context = await _browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="zh-CN",
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
        )
        new_cookies = await _load_cnki_cookies()
        await _context.add_cookies(new_cookies)
        _page = await _context.new_page()
        await _page.goto(search_url, timeout=45000)
        await _page.wait_for_load_state("domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        if await _cnki_check_captcha(_page):
            print("[CNKI] 刷新后仍被拦截，放弃", file=sys.stderr)
            return []

    record("cnki")

    # 提取搜索结果：学位论文必须走 grid API（URL 参数过滤无效）
    is_thesis = any(t in ("phd", "master") for t in types)
    if institution or is_thesis:
        items = await _cnki_grid_api_search(_page, query, institution or "", doc_type, max_results)
    else:
        items = await _page.evaluate(r"""(maxRows) => {
            const rows = document.querySelectorAll('.result-table-list tbody tr');
            return Array.from(rows).slice(0, maxRows).map(row => {
                const nameEl = row.querySelector('.name a');
                const title = nameEl?.innerText?.trim() || '';
                const href = nameEl?.href || '';
                // 作者：优先 <a>，兜底 <span>
                const authorEls = row.querySelectorAll('.author a, .author span');
                const authors = Array.from(authorEls).map(a => a.innerText.trim()).filter(a => a && a.length < 20);
                // 来源：期刊用 .source，学位论文用 .unit（学位授予单位）
                const sourceEl = row.querySelector('.source');
                const unitEl = row.querySelector('.unit');
                const source = (sourceEl?.innerText?.trim() || unitEl?.innerText?.trim() || '');
                const dateEl = row.querySelector('.date');
                const date = dateEl?.innerText?.trim() || '';
                const citeEl = row.querySelector('.quote');
                const cite = citeEl?.innerText?.trim() || '0';
                return { title, href, authors, source, date, cite: parseInt(cite) || 0, dbid: nameEl?.getAttribute('data-dbname') || '' };
            }).filter(r => r.title.length > 3);
        }""", max_results)

    results = []
    for item in items[:max_results]:
        year = None
        if item.get("date"):
            ym = re.match(r"(\d{4})", item["date"])
            year = int(ym.group(1)) if ym else None

        results.append({
            "title": item["title"],
            "authors": item.get("authors", []),
            "abstract": "",
            "year": year,
            "venue": item.get("source", ""),
            "citation_count": item.get("cite", 0),
            "doi": "",
            "url": item.get("href", ""),
            "source": "cnki",
        })

    print(f"  获取 {len(results)} 条")

    # 下载 PDF
    if download_dir and results:
        dl_path = Path(download_dir)
        dl_path.mkdir(parents=True, exist_ok=True)
        print(f"\n[CNKI] 开始下载 PDF → {dl_path}")

        for i, r in enumerate(results):
            if not r.get("url"):
                continue
            try:
                pdf_path = await _cnki_download_paper(r["url"], dl_path, r["title"])
                if pdf_path:
                    r["pdf_path"] = str(pdf_path)
                    print(f"  [{i+1}/{len(results)}] ✓ {r['title'][:40]}")
                else:
                    print(f"  [{i+1}/{len(results)}] ✗ {r['title'][:40]} (无下载按钮)")
                await asyncio.sleep(RATE_LIMITS["cnki"]["interval"])
            except Exception as e:
                print(f"  [{i+1}/{len(results)}] ✗ {r['title'][:40]} ({e})", file=sys.stderr)

    return results


async def _cnki_download_paper(detail_url: str, save_dir: Path, title: str) -> Path | None:
    """从 CNKI 论文详情页下载 PDF。"""
    detail = await _context.new_page()
    try:
        await detail.goto(detail_url, timeout=30000)
        await detail.wait_for_load_state("domcontentloaded", timeout=20000)
        await asyncio.sleep(2)

        # 检查验证码
        if await _cnki_check_captcha(detail):
            return None

        # 查找 PDF 下载按钮
        pdf_btn = await detail.query_selector('a[id*="pdf"], a[id*="PDF"], a.btn-dlpdf')
        if not pdf_btn:
            pdf_btn = await detail.query_selector('a:has-text("PDF下载"), a:has-text("下载")')

        if not pdf_btn:
            return None

        # 点击下载
        try:
            async with detail.expect_download(timeout=30000) as download_info:
                await pdf_btn.click()
            download = await download_info.value
        except Exception:
            return None

        # 保存文件
        suggested = download.suggested_filename or "paper.pdf"
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', suggested)
        save_path = save_dir / safe_name
        await download.save_as(save_path)

        if save_path.exists() and save_path.stat().st_size > 1024:
            # P0-B：下载后校验 PDF 首页标题（失败静默，不阻断下载）
            _save_title_meta(save_path, title)
            return save_path
        return None
    finally:
        await detail.close()


# ──────────── CLI ────────────

def print_results(results: list[dict], fmt: str = "markdown"):
    if fmt == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    for i, r in enumerate(results, 1):
        print(f"\n{'─'*60}")
        print(f"  [{r.get('source','?').upper()}] {i}. {r['title']}")
        if r.get("authors"):
            print(f"  作者: {', '.join(r['authors'][:5])}{'...' if len(r['authors'])>5 else ''}")
        if r.get("affiliations"):
            print(f"  单位: {'; '.join(r['affiliations'][:3])}")
        if r.get("venue"):
            print(f"  来源: {r['venue']}")
        if r.get("year"):
            print(f"  年份: {r['year']}", end="")
            if r.get("volume_issue"):
                print(f"  {r['volume_issue']}", end="")
            print()
        if r.get("citation_count"):
            print(f"  被引: {r['citation_count']}", end="")
            if r.get("download_count"):
                print(f"  下载: {r['download_count']}", end="")
            print()
        if r.get("doi"):
            print(f"  DOI: {r['doi']}")
        if r.get("quality_labels"):
            print(f"  标签: {', '.join(r['quality_labels'])}")
        if r.get("keywords"):
            print(f"  关键词: {', '.join(r['keywords'][:8])}")
        if r.get("abstract"):
            abs_text = r["abstract"][:200] + ("..." if len(r["abstract"]) > 200 else "")
            print(f"  摘要: {abs_text}")
        if r.get("url"):
            print(f"  链接: {r['url']}")


async def async_main():
    parser = argparse.ArgumentParser(description="浏览器文献检索工具 (IEEE/万方/cbpt/CNKI)")
    parser.add_argument("query", nargs="?", default=None, help="搜索关键词")
    parser.add_argument("--source", "-s", required=True, choices=["ieee", "wanfang", "cbpt", "cnki"], help="检索源")
    parser.add_argument("--journal", "-j", default=None, help="cbpt 期刊子域名 (如 wxdg, sdzy)")
    parser.add_argument("--extract", default=None, help="直接提取 cbpt 论文页 URL")
    parser.add_argument("--max", type=int, default=20, help="最大结果数 (默认 20)")
    parser.add_argument("--format", "-f", default="markdown", choices=["json", "markdown"], help="输出格式")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    parser.add_argument("--download", "-d", default=None, metavar="DIR", help="下载 PDF 到指定目录 (ieee/cnki)")
    parser.add_argument("--doc-type", default="journal", help="文献类型: journal/phd/master，逗号分隔可组合 (默认: journal)。cnki/wanfang 均支持 phd/master 过滤")
    parser.add_argument("--institution", "-i", default=None, help="CNKI 学位授予单位过滤 (如 清华大学)")

    args = parser.parse_args()

    results = []

    try:
        if args.extract:
            print(f"[cbpt] 提取: {args.extract}")
            r = await cbpt_extract(args.extract)
            if r:
                results = [r]
        elif not args.query:
            parser.error("需要 query 参数（或使用 --extract）")
        elif args.source == "ieee":
            results = await ieee_search(args.query, args.max)
            if results and args.download:
                await ieee_download(results, args.download)
        elif args.source == "wanfang":
            results = await wanfang_search(args.query, args.max, doc_type=args.doc_type)
        elif args.source == "cbpt":
            if not args.journal:
                parser.error("cbpt 源需要 --journal 参数 (如 --journal wxdg)")
            results = await cbpt_journal_search(args.journal, args.query, args.max)
        elif args.source == "cnki":
            results = await cnki_search(args.query, args.max, download_dir=args.download, doc_type=args.doc_type, institution=args.institution)
    finally:
        await cleanup()
        await asyncio.sleep(0.3)

    # 限速状态
    print(f"\n[会话用量] " + " | ".join(
        f"{k}: {_session_counts[k]}/{RATE_LIMITS[k]['max']}" for k in RATE_LIMITS
    ))

    if not results:
        print("无结果", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = json.dumps({"query": args.query, "count": len(results), "results": results}, ensure_ascii=False, indent=2)
    else:
        import io
        buf = io.StringIO()
        # redirect print to buffer
        old_stdout = sys.stdout
        sys.stdout = buf
        print_results(results, args.format)
        sys.stdout = old_stdout
        output = buf.getvalue()

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n已保存到: {args.output}")
    else:
        if args.format == "markdown":
            print_results(results, args.format)
        else:
            print(output)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_main())
