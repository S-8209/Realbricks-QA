import time
import pytest, logging
from realbricks.Page.forget_password import Forget_password
from playwright.sync_api import Page
from playwright.sync_api import Playwright, sync_playwright, expect

logger=logging.getLogger(__name__)

def test_forget_password(login_page_redirection:Page):
    logger.info("Forgot Password Page")
    fp=Forget_password(login_page_redirection)
    fp.Forget_password_redirection()
    success_message,new_page=fp.reset_link()
    expect(success_message).to_be_visible()