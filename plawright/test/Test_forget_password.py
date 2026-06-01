import time
import pytest
from plawright.Page.Forget_password import Forget_password
from plawright.Utils.Utils import load_users
from plawright.Page.Login_FLow import login_User
from playwright.sync_api import Playwright, sync_playwright, expect


def test_forget_password(page):
    fp=Forget_password(page)
    fp.Open()
    fp.Forget_password_redirection()
    fp.reset_link()
    expect(page.get_by_text("You have successfully reset your password.")).to_be_visible()