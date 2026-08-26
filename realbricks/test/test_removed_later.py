import json , time
from pathlib import Path
from playwright.sync_api import Page

from realbricks.Utils.utils import load_users
from realbricks.Configs.constants import LOGIN_URL ,QA_USER
from realbricks.Page.base_page import BasePage   
QA_USER1 = {
    "email"   : "sl61114@yopmail.com",
    "password": "Test@123",
    "pin"     : "0000",
}

class login_User(BasePage):
    def __init__(self,page:Page)->None:
        self.page = page

        self.fill_email=self.page.locator("#email")
        self.fill_password=self.page.locator("#password")
        self.submit_button=self.page.get_by_role("button", name="Log in")
        self.back_to_signup=self.page.get_by_role("button",name="Complete Account Setup")
        self.home_page=page.locator("//h2[normalize-space()='The Realbricks Marketplace']", has_text="The Realbricks Marketplace")
        # self.email_input=page.locator("#email").fill(self.user["email"])
        # ERROR MESSAGES
        self.creds=page.get_by_text("Please enter a valid email and password.")
        
        # self.user = user
    def Open(self):
        self.page.goto(LOGIN_URL)
    def Login(self):
        self.safe_fill(self.fill_email,"sl61760@yopmail.com","fill email")
        self.safe_fill(self.fill_password,"Test@123","Fill passowrd")
    def login_button(self):
        self.safe_click(self.submit_button,"submit button")
    def OTP(self):
        self.fill_pin(self.page)
        self.safe_click(self.back_to_signup,"test")
    def select_drop_down(self):
        self.page.locator("div.ant-select-in-form-item").click()
        self.page.locator("#identification-anchor").get_by_text("Passport", exact=True).click()
        # self.page.locator("[class=ant-upload]")..set_input_files("/home/sagar/Downloads/test-document-upload-success.png")
        # with self.page.expect_file_chooser() as fc_info:  
        #     self.page.get_by_role("button",name="Upload ID").click()
        # file=fc_info.value
        # file.set_files("/home/sagar/Downloads/test-document-upload-success.png")
        self.page.locator('input[type="file"]').set_input_files("/home/sagar/Downloads/test-document-upload-success.png")
        

            
def test_d(page: Page):
    sign=login_User(page)
    sign.Open()
    sign.Login()
    sign.login_button()
    sign.OTP()
    sign.select_drop_down()
            