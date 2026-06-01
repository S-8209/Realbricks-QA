import pytest 
from playwright.sync_api import Playwright, sync_playwright, expect
from plawright.Page.Login_FLow import login_User
@pytest.fixture(scope="session")
def page():
    print("MY FIXTURE IS RUNNING")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()
# def test_google(page):
#     page.goto("https://google.com")
#     page.pause()
@pytest.fixture
def page(browser):
    """Open a fresh tab before each test, close it after"""
    page = browser.new_page()
    yield page
    page.close()
    
@pytest.fixture
def logged_in_page(page):
    login = login_User(page)
    login.Open()
    login.Login("qa2@yopmail.com", "Test@123")
    login.OTP("0000")
    return page
