"""
CNKI cookie 获取工具

启动有头浏览器，用户手动通过安全验证后，自动保存 cookie 到 cnki_cookies.json。
之后 blit/download 等工具可复用该 cookie 文件。

用法:
    python tools/cnki_login.py
    # 浏览器弹出后，完成安全验证，等待脚本提示"Cookie 已保存"
"""

import asyncio
import json
from pathlib import Path

COOKIE_FILE = Path(__file__).parent.parent / "cnki_cookies.json"


async def main():
    from playwright.async_api import async_playwright

    print("启动浏览器，请在弹出的窗口中完成 CNKI 安全验证。")
    print(f"验证通过后 cookie 将保存到: {COOKIE_FILE}")
    print()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        page = await ctx.new_page()

        await page.goto("https://kns.cnki.net/", timeout=60000)
        print("已打开 CNKI 首页。")

        # 轮询等待安全验证通过（页面标题不再是"安全验证"）
        for _ in range(300):  # 最多等 5 分钟
            await asyncio.sleep(1)
            title = await page.title()
            if "安全验证" not in title and len(title) > 0:
                print(f"验证通过! 页面标题: {title}")
                break
        else:
            print("等待超时（5分钟），保存当前 cookie 供检查。")

        # 再等 2 秒确保 cookie 完整
        await asyncio.sleep(2)

        # 保存 cookies
        cookies = await ctx.cookies()
        COOKIE_FILE.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nCookie 已保存 ({len(cookies)} 条) → {COOKIE_FILE}")

        # 验证: 检查是否能访问论文页面
        print("\n验证访问能力...")
        await page.goto("https://kns.cnki.net/kns8s/defaultresult/index", timeout=30000)
        await asyncio.sleep(3)
        title = await page.title()
        print(f"搜索页标题: {title}")

        if "安全验证" in title:
            print("⚠️  仍在验证页面，cookie 可能未生效。请重新运行。")
        else:
            print("✓ Cookie 有效!")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
