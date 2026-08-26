
import time,re
from realbricks.Page.base_page import BasePage
from playwright.sync_api import Page

from realbricks.Configs.constants import FORGET_PASSWORD_USER
from realbricks.conftest import page
class Forget_password(BasePage):
    def __init__(self,page:Page):
        self.page=page
        auth_body=page.locator(".auth_form_body")
        # self.success_message=page.get_by_text("You have successfully reset your password.")
    def Forget_password_redirection(self):
        self.page.get_by_role("link",name="Forgot password").click()
        self.page.locator("//input[@id='email']").fill(FORGET_PASSWORD_USER["email"])
        self.page.get_by_role("button",name="Submit").click()
        time.sleep(2)
    def reset_link(self):
        self.page.goto("https://yopmail.com/")
        self.page.locator("//input[@id='login']").fill(FORGET_PASSWORD_USER["email"])
        self.page.get_by_title("Check Inbox @yopmail.com").click()
        iframe_locator = self.page.frame_locator("#ifmail")
    
        with self.page.context.expect_page() as new_tab:
            iframe_locator.get_by_role("link",name="Reset Password").click()
        self.new_page=new_tab.value
        self.new_page.wait_for_load_state()
        self.new_page.locator("div").filter(has_text=re.compile(r"^New password \(min 8 characters\)$")).locator("#password").fill(FORGET_PASSWORD_USER["password"])
        self.new_page.locator("div").filter(has_text=re.compile(r"^Retype password$")).locator("#password").fill(FORGET_PASSWORD_USER["password"])
        self.new_page.get_by_role("button",name="Save Password").click()
        self.success_message=self.new_page.get_by_text("You have successfully reset your password.")
        self.login_redirection=self.new_page.get_by_role("link",name="/login").click()
        return (self.success_message, self.new_page)
        
