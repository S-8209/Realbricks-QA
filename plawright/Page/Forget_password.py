
import pytest,time,re
from plawright.Utils.Utils import load_users
from plawright.conftest import page
class Forget_password():
    email="jj@yopmail.com"
    def __init__(self,page):
        self.page=page
    def Open(self):
        self.page.goto("https://www.staging-fe.realbricks.com/login")
    def Forget_password_redirection(self):
        self.page.get_by_role("link",name="Forgot password").click()
        self.page.locator("//input[@id='email']").fill(self.email)
        self.page.get_by_role("button",name="Submit").click()
        time.sleep(2)
    def reset_link(self):
        self.page.goto("https://yopmail.com/")
        self.page.locator("//input[@id='login']").fill(self.email)
        self.page.get_by_title("Check Inbox @yopmail.com").click()
        iframe_locator = self.page.frame_locator("#ifmail")
    
        with self.page.context.expect_page() as new_tab:
            iframe_locator.get_by_role("link",name="Reset Password").click()
        self.new_page=new_tab.value
        self.new_page.wait_for_load_state()
        # self.new_page.get_by_label("New password").fill("Simform@123")
        self.new_page.locator("div").filter(has_text=re.compile(r"^New password \(min 8 characters\)$")).locator("#password").fill("Simform@123")
        self.new_page.locator("div").filter(has_text=re.compile(r"^Retype password$")).locator("#password").fill("Simform@123")
        self.new_page.locator("button",name="Save Password").click()
