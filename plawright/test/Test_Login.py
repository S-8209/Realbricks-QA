import time
import pytest
from plawright.Page.Login_FLow import login_User
from plawright.Utils.Utils import load_users
from playwright.sync_api import Playwright, sync_playwright, expect

@pytest.mark.parametrize("user",load_users("valid_login_user"))
def test_Login(page,user):
    login=login_User(page)
    # data=user
    login.Open()
    #expect(pag(END)e.get_by_role("heading", name="The Realbricks Marketplace")).to_be_visible()
    login.Login(user["email"],user["password"])
    login.Login_button()
    login.OTP(user["pin"])
    expect(page.locator("//h2[normalize-space()='The Realbricks Marketplace']", has_text="The Realbricks Marketplace")).to_be_visible()
    page.close()
    
@pytest.mark.parametrize("user",load_users("Invalid_user_password"))
def test_invalid_password_login(page,user):
    login=login_User(page)
    login.Open()
    login.Login(user["email"],user["password"])
    login.Login_button()

    expect(page.locator("//div[@class='ant-notification-notice-description']",has_text="Please enter a valid email and password.")).to_be_visible()
    
@pytest.mark.parametrize("user",load_users("Invalid_user_pin"))
def test_invalid_pin(page,user):
    login=login_User(page)
    login.Open()
    login.Login(user["email"],user["password"])
    login.Login_button()

    login.OTP(user["pin"])
    expect(page.locator("//div[@role='alert']",has_text="Please enter a valid pin.")).to_be_visible()
    
@pytest.mark.parametrize("email1",[
    "testexample.com",
    "test@",
    "@test.com",
    "test @mail.com",
    "test#mail.com"
])
def test_invalid_email(page,email1):
    login=login_User(page)
    login.Open()
    login.Login(email1,"Test@123")
    login.Login_button()

    expect(page.locator("//div[@role='alert']",has_text="email must be an email")).to_be_visible()
    
@pytest.mark.parametrize("user",load_users("empty_email_login"))
def test_empty_email_login(page,user):
    login=login_User(page)
    login.Open()
    login.Login(user["email"],user["password"])
    expect(page.get_by_role("button",name="Log in")).to_be_disabled()

@pytest.mark.parametrize("user",load_users("empty_password_login"))
def test_empty_password_login(page,user):
    login=login_User(page)
    login.Open()
    login.Login(user["email"],user["password"])
    expect(page.get_by_role("button",name="Log in")).to_be_disabled()
