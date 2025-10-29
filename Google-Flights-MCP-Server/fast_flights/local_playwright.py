from typing import Any
import asyncio
import nest_asyncio
from playwright.async_api import async_playwright

async def fetch_with_playwright(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        if page.url.startswith("https://consent.google.com"):
            await page.click('text="Accept all"')
        # Wait for flight results to load
        try:
            await page.wait_for_selector('[jsname="IWWDBc"], [jsname="YdtKid"]', timeout=30000)
        except:
            # Fallback to original selector
            locator = page.locator('.eQ35Ce')
            await locator.wait_for(timeout=30000)
        body = await page.evaluate(
            "() => document.querySelector('[role=\"main\"]').innerHTML"
        )
        await browser.close()
    return body

def local_playwright_fetch(params: dict) -> Any:
    url = "https://www.google.com/travel/flights?" + "&".join(f"{k}={v}" for k, v in params.items())
    
    # Apply nest_asyncio to allow nested event loops
    nest_asyncio.apply()
    
    try:
        # Check if we're in an async context
        loop = asyncio.get_running_loop()
        # If we're in an async context, use nest_asyncio to allow nested loops
        body = asyncio.run(fetch_with_playwright(url))
    except RuntimeError:
        # No event loop running, safe to use asyncio.run() directly
        body = asyncio.run(fetch_with_playwright(url))

    class DummyResponse:
        status_code = 200
        text = body
        text_markdown = body

    return DummyResponse
