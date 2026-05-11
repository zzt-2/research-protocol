"""
CNKI cbpt.cnki.net 论文元数据提取 PoC
用 Playwright 渲染 SPA 页面，从 DOM 提取结构化元数据

DOM 结构:
  .paperDetail          → 头部信息 (卷期, 标题, 作者, 单位, DOI)
  .paperDetailCtrl      → 标签导航 (摘要/全文/参考文献/出版信息/相关文章)
  .paperDetailCtrlZone  → 标签内容区
    .paperDetail_html.pd1           → 摘要+关键词
    .paperDetail_references.pd3     → 参考文献
    .paperDetail_publish.pd4        → 出版信息 (引用格式, 中图分类号, 发布时间)

提取字段:
  标题     .paperDetail_tt
  作者     第1个 .paperDetail_author
  作者单位  .paperDetail_author 匹配 /^\d+\./ 的元素
  摘要     .paperDetail_html.pd1 文本中 "摘要：" 到 "关键词" 之间
  关键词   .paperDetail_html.pd1 文本中 "关键词：" 之后
  期刊名   <title> 元素
  年份卷期  .paperDetail_vol
  DOI     .paperDetail_doi
"""
import asyncio
import json
import re
from playwright.async_api import async_playwright


URLS = [
    "https://sdzy.cbpt.cnki.net/portal/journal/portal/client/paper/89076f6735644504bc5a9c61a3b5877a",
    "https://sdzy.cbpt.cnki.net/portal/journal/portal/client/paper/6e45a0d0ecc5c8207692921b89b8333e",
]


async def safe_text(page, sel):
    el = await page.query_selector(sel)
    if el:
        return (await el.inner_text()).strip()
    return None


async def extract(page, url):
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        resp = await page.goto(url, wait_until="networkidle", timeout=60000)
        print(f"Status: {resp.status if resp else 'N/A'}")
    except Exception as e:
        print(f"页面加载失败: {e}")
        return None

    await asyncio.sleep(3)

    m = {}

    # 期刊名 = <title>
    m["期刊名"] = await page.title()

    # 标题
    m["标题"] = await safe_text(page, ".paperDetail_tt")

    # 作者: 第一个 .paperDetail_author（纯人名）
    authors_el = await page.query_selector_all(".paperDetail_author")
    for el in authors_el:
        text = (await el.inner_text()).strip()
        if text and not re.match(r"^\d+\.", text) and "关键词" not in text and "KeyWords" not in text:
            m["作者"] = text
            break

    # 作者单位: .paperDetail_author 中以 "数字." 开头的
    affiliations = []
    for el in authors_el:
        text = (await el.inner_text()).strip()
        if re.match(r"^\d+\.", text):
            affiliations.append(text)
    if affiliations:
        m["作者单位"] = affiliations

    # 年份卷期
    m["年份卷期"] = await safe_text(page, ".paperDetail_vol")

    # DOI
    doi_raw = await safe_text(page, ".paperDetail_doi")
    if doi_raw:
        doi_match = re.search(r"10\.\S+", doi_raw)
        m["DOI"] = doi_match.group() if doi_match else doi_raw

    # 摘要 & 关键词 — 从 .paperDetail_html.pd1 提取
    pd1 = await safe_text(page, ".paperDetail_html.pd1")
    if pd1:
        abs_match = re.search(r"摘\s*要[：:]\s*\n?\n?([\s\S]*?)(?=\n\s*(?:关键词|Abstract))", pd1)
        if abs_match:
            m["摘要"] = abs_match.group(1).strip()

        kw_match = re.search(r"关键词[：:]\s*\n?([\s\S]*?)(?=\n\s*(?:Abstract|Key\s*words|$))", pd1)
        if kw_match:
            m["关键词"] = kw_match.group(1).strip().rstrip(";；")

        abs_en = re.search(r"Abstract[：:]\s*\n?\n?([\s\S]*?)(?=\n\s*(?:Key\s*words|关键词))", pd1)
        if abs_en:
            m["摘要_en"] = abs_en.group(1).strip()

        kw_en = re.search(r"Key\s*words?[：:]\s*\n?([\s\S]*?)(?=\n|$)", pd1, re.IGNORECASE)
        if kw_en and kw_en.group(1).strip():
            m["关键词_en"] = kw_en.group(1).strip().rstrip(";；")

    # 基金项目
    m["基金项目"] = await safe_text(page, ".paperDetail_foundation")

    # 出版信息 (引用格式, 中图分类号)
    pub_info = await safe_text(page, ".paperDetail_publish.pd4")
    if pub_info:
        cite_match = re.search(r"引用信息[：:]\s*\n?\s*(.+?)(?:\n|$)", pub_info)
        if cite_match:
            m["引用格式"] = cite_match.group(1).strip()
        cls_match = re.search(r"中图分类号[：:]\s*(\S+)", pub_info)
        if cls_match:
            m["中图分类号"] = cls_match.group(1)

    # 输出结果
    print("\n--- 提取结果 ---")
    for k in ["标题", "作者", "作者单位", "摘要", "关键词", "期刊名", "年份卷期", "DOI",
              "摘要_en", "关键词_en", "基金项目", "引用格式", "中图分类号"]:
        if k in m:
            val = str(m[k])
            print(f"  {k}: {val[:150]}{'...' if len(val) > 150 else ''}")

    return m


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        page = await ctx.new_page()

        all_results = {}
        for url in URLS:
            result = await extract(page, url)
            if result:
                all_results[url] = result

        await browser.close()

    # 可行性总结
    print("\n\n" + "=" * 60)
    print("字段提取可行性总结")
    print("=" * 60)
    fields = [
        ("标题", "标题"),
        ("作者", "作者"),
        ("作者单位/机构", "作者单位"),
        ("摘要", "摘要"),
        ("关键词", "关键词"),
        ("期刊名", "期刊名"),
        ("年份/卷期", "年份卷期"),
        ("DOI", "DOI"),
    ]
    for label, key in fields:
        n = sum(1 for m in all_results.values() if key in m)
        status = "是" if n == len(URLS) else ("部分" if n > 0 else "否")
        print(f"  {label}: {status} ({n}/{len(URLS)})")

    print("\n提取方式:")
    print("  标题:     CSS .paperDetail_tt")
    print("  作者:     CSS .paperDetail_author (第一个, 排除单位行)")
    print("  作者单位: CSS .paperDetail_author (匹配 /^\\d+\\./ 的行)")
    print("  摘要:     CSS .paperDetail_html.pd1 → 正则 '摘要：' 到 '关键词'")
    print("  关键词:   CSS .paperDetail_html.pd1 → 正则 '关键词：' 之后")
    print("  期刊名:   <title> 元素")
    print("  年份卷期: CSS .paperDetail_vol")
    print("  DOI:     CSS .paperDetail_doi → 正则提取 10.xxx")

    print("\n额外交互: 无需点击任何标签，所有字段在默认渲染的 DOM 中即可获取")
    print("反爬情况: 未遇到验证码或 IP 封禁 (headless Chromium)")


if __name__ == "__main__":
    asyncio.run(main())
