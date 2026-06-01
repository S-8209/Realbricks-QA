import json
from pathlib import Path
from plawright.Utils.Utils import load_users
class login_User():
    def __init__(self,page):
        self.page = page
        # self.user = user
    def Open(self):
        self.page.goto("https://www.staging-fe.realbricks.com/login")
    def Login(self,email,password):
        self.page.locator("#email").click()
        self.page.locator("#email").fill(email)
        self.page.locator("#password").fill(password)
        self.page.get_by_role("button", name="Log in").click()
    def OTP(self,pin):
        for i in range(4):
                self.page.get_by_role("textbox", name=f"SingleInput-{i}").fill(pin[i])