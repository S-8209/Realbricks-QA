from playwright.sync_api import sync_playwright

# TODO: replace with your actual staging login URL
LOGIN_URL = "https://staging-fe.realbricks.com/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Navigating to: {LOGIN_URL}")
    page.goto(LOGIN_URL, wait_until="networkidle")
    page.wait_for_timeout(2000)

    print(f"Final URL after navigation: {page.url}")
    print(f"Page title: {page.title()}")

    try:
        page.wait_for_selector("#email", timeout=5000)
        print("#email IS visible within 5 seconds.")
    except Exception as e:
        print(f"#email NOT visible within 5 seconds. ({type(e).__name__})")

    body_text = page.inner_text("body")[:500]
    print("\n--- First 500 chars of visible page text ---")
    print(body_text)
    print("--- end snippet ---\n")

    page.screenshot(path="login_page_screenshot.png", full_page=True)
    with open("login_page_debug.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("Saved: login_page_screenshot.png, login_page_debug.html")

    browser.close()
