

from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import Page
import re
def test_buy_flow(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.staging-fe.realbricks.com/login")
    page.locator("#email").click()
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Log in").click()
    for i in range(4):
        page.get_by_role("textbox", name=f"SingleInput-{i}").fill(pin[i])
            
    page.locator("div.marketslider").nth(0).get_by_role("button", name='Buy Now').nth(0).click()
    for i in range(4):
        page.get_by_role("textbox", name=f"SingleInput-{i}").fill("0")
            # page.locator("//input[@id='share']").fill("1")
    page.get_by_text("Max (9.8%)",exact=False).click()
    page.get_by_role("button", name="Preview order").click()
            # page.locator("#checkbox").click()
    page.locator("input.ant-checkbox-input").check()
    page.get_by_role("button", name="Place order").click()
    page.get_by_role("checkbox", name=re.compile(r"I attest that I am")).check()
    page.get_by_role("checkbox", name="I have read and understand the above Subscription Agreement.").check()
    page.get_by_role("button", name="Agree to terms").click()