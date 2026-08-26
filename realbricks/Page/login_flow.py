import json , time
from pathlib import Path
from playwright.sync_api import Page

from realbricks.Utils.utils import load_users
from realbricks.Configs.constants import LOGIN_URL ,QA_USER
from realbricks.Page.base_page import BasePage   


class login_User(BasePage):
    def __init__(self,page:Page, user : dict)->None:
        super().__init__(page)
        self.page = page
        self.user=user
        self.fill_email=self.page.locator("#email")
        self.fill_password=self.page.locator("#password")
        self.submit_button=self.page.get_by_role("button", name="Log in")
        self.home_page=page.locator("//h2[normalize-space()='The Realbricks Marketplace']", has_text="The Realbricks Marketplace")
        # self.email_input=page.locator("#email").fill(self.user["email"])
        # ERROR MESSAGES
        self.creds=page.get_by_text("Please enter a valid email and password.")
        
        # self.user = user
    def Open(self):
        self.page.goto(LOGIN_URL)
    def Login(self):
        self.safe_fill(self.fill_email,self.user["email"],"fill email")
        self.safe_fill(self.fill_password,self.user["password"],"Fill passowrd")
    def login_button(self):
        self.safe_click(self.submit_button,"submit button")
    def OTP(self):
        self.fill_pin(self.page,self.user["pin"])
    
