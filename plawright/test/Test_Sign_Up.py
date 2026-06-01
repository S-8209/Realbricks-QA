import time
import pytest
from plawright.Page.Sign_Up_Flow import Sign_up
from plawright.Utils.Utils import load_users
from plawright.Page.Login_FLow import login_User
from playwright.sync_api import Playwright, sync_playwright, expect

@pytest.mark.smoke
def test_sign_up(page):
    sign=Sign_up(page)
    sign.sign_up()
    sign.User_onboarding()
    # expect(page.get_by_text("Marketplace")).to_be_visible()
    
def test_break_sign_up_flow(page):
    sign=Sign_up(page)
    sign.broke_flow()

    