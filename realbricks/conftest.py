import os
import pytest
import logging
from playwright.sync_api import sync_playwright, Page
from realbricks.Page.login_flow import login_User
from realbricks.Utils.utils import _random_email
from realbricks.test_data.sign_up_data import valid_sign_Up_details

from realbricks.Configs.constants import (
    SIGN_UP_URL,QA_USER,NEW_USER,LOGIN_URL,Insufficient_balance_user,B_T_USER
)
# from realbricks.Test_data.sign_up_data import build_user
# from realbricks.Page.Sign_Up_Flow import UserData

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ── Browser fixture (session scoped) ──────────────────────────────────────────
@pytest.fixture(scope="session")
def browser():
    """Launch browser once for the entire test session.

    Headless/slow_mo are env-driven: CI sets HEADLESS=true (no display, must
    be headless); local runs default to headed with slow_mo=50 for debugging.
    """
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    slow_mo = int(os.getenv("SLOW_MO", "0" if headless else "50"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        logger.info(f"Browser launched (headless={headless}, slow_mo={slow_mo})")
        yield browser
        browser.close()
        logger.info("Browser closed")


# ── Context fixture (function scoped) ─────────────────────────────────────────
@pytest.fixture(scope="function")
def context(browser):
    """Create a fresh browser context for each test."""
    ctx = browser.new_context()
    logger.info("Browser context created")
    yield ctx
    ctx.close()
    logger.info("Browser context closed")


# ── Page fixture (function scoped) ────────────────────────────────────────────
@pytest.fixture(scope="function")
def page(context) -> Page:
    """Open a fresh tab for each test."""
    page = context.new_page()
    logger.info("New page opened")
    yield page
    page.close()
    logger.info("Page closed")


# ── Logged in page fixture ─────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def logged_in_page(page) -> Page:
    """
    Log in with QA credentials and return the page.
    Used by all tests that require authentication.
    """
    logger.info(f"Logging in as: {QA_USER['email']}")
    login = login_User(page,QA_USER)
    login.Open()
    login.Login()
    login.login_button()
    login.OTP()
    logger.info("Login successful")
    return page
@pytest.fixture(scope="function")
def user_for_every_transaction(page) -> Page:
    """
    Log in with QA credentials and return the page.
    Used by all tests that require authentication.
    """
    logger.info(f"Logging in as: {B_T_USER['email']}")
    login = login_User(page,B_T_USER)
    login.Open()
    login.Login()
    login.login_button()
    login.OTP()
    logger.info("Login successful")
    return page

@pytest.fixture(scope="function")
def Newly_created_user(page) -> Page:
    """
    Log in with QA credentials and return the page.
    Used by all tests that require authentication.
    """
    logger.info(f"Logging in as: {NEW_USER['email']}")
    login = login_User(page,NEW_USER)
    login.Open()
    login.Login()
    login.login_button()
    login.OTP()
    logger.info("Login successful")
    return page

@pytest.fixture(scope="function")
def user_with_insufficient_balance(page)->Page:
    logger.info(f"Logging in as: {Insufficient_balance_user['email']}")
    login = login_User(page,Insufficient_balance_user)
    login.Open()
    login.Login()
    login.login_button()
    login.OTP()
    logger.info("Login successful")
    return page


# ── Sign up page fixture ───────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def sign_up_page(page) -> Page:
    """Navigate to sign up page and return the page."""
    logger.info(f"Navigating to sign up: {SIGN_UP_URL}")
    page.goto(SIGN_UP_URL)
    return page


# ── Default user fixture ───────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def default_user() -> valid_sign_Up_details:
    """
    Build a UserData object with valid test data.
    Email is randomly generated each time.
    """
    user = valid_sign_Up_details
    # logger.info(f"Default user created with email: {user.email}")
    user["email"]=_random_email()
    return user.copy()

@pytest.fixture(scope="function")
def login_page(page)-> Page:
    page.goto(LOGIN_URL)
    return page

# ── Screenshot on failure ──────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot automatically when a test fails."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            try:
                page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Screenshot failed: {e}")   

@pytest.fixture(scope="function")
def login_page_redirection(page):
    page.goto(LOGIN_URL)
    return page

@pytest.fixture(scope="function")
def default_user():
    user = valid_sign_Up_details.copy()
    user["email"] = _random_email()  # fresh random email per test
    return user
