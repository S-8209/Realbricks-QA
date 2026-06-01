import re , time
from playwright.sync_api import Playwright, sync_playwright, expect
import json
from plawright.conftest import page
from pathlib import Path
import random
# from Utils.Utils import load_users
class Sign_up ():
    def __init__(self,page):
        self.page =page
            # self.user=user
    # def run(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context()
    # page = context.new_page()
    
    random_num = random.randint(1, 2000)
    email = f"sl{random_num}@yopmail.com"  
    def sign_up(self):
        self.page.goto("https://www.staging-fe.realbricks.com/")
        self.page.get_by_role("link", name="Sign up").click()
        self.page.get_by_role("link", name="Sign up With Email").click()
        self.page.get_by_role("textbox", name="Legal First Name").fill("John")
        self.page.get_by_role("textbox", name="Legal Last Name").fill("Smith")
        self.page.get_by_role("textbox", name="Email").fill(self.email)
        self.page.get_by_role("textbox", name="Phone Number").fill("24523450233")
        self.page.get_by_role("textbox", name="Password").fill("Test@123")
        self.page.get_by_role("checkbox", name="I have read and agree to the").check()
        # time.sleep(9)
        # self.page.locator('[id="signup-form_referredBy"]').fill("JORDAN50")
        self.page.get_by_role("checkbox", name="By checking this box, I").check()
        self.page.get_by_role("button", name="Sign Up").click()
    def  User_onboarding(self):
        self.page.goto("https://yopmail.com/")
        self.page.locator("//input[@id='login']").fill(self.email)
        self.page.get_by_title("Check Inbox @yopmail.com").click()
        iframe_locator = self.page.frame_locator("#ifmail")
        with self.page.context.expect_page() as new_tab:
            iframe_locator.get_by_text("Activate my account").click()
        self.new_page=new_tab.value
        self.new_page.wait_for_load_state()
        for i in range(4):
            self.new_page.locator(f"//input[@id='SingleInput-{i}']").fill("0")
        self.new_page.get_by_text("Save PIN").click()   
        for i in range(4):
            self.new_page.locator(f"//input[@id='SingleInput-{i}']").fill("0")
        self.new_page.get_by_text("Confirm").click()
        self.new_page.get_by_role("radio", name="Yes").check()
        self.new_page.get_by_role("button", name="Continue").click()
        self.new_page.get_by_role("textbox", name="Residential address").click()
        self.new_page.get_by_role("textbox", name="Residential address").fill("222333 PEACHTREE PLACE")
        self.new_page.get_by_role("textbox", name="City").click()
        self.new_page.get_by_role("textbox", name="City").fill("ATLANTA")
        self.new_page.locator("div").filter(has_text=re.compile(r"^CityStateZip code$")).locator("span").first.click()
        self.new_page.locator("div").filter(has_text=re.compile(r"^Alaska$")).nth(1).click()
        self.new_page.get_by_role("textbox", name="Zip code").click()
        self.new_page.get_by_role("textbox", name="Zip code").fill("12345")
        self.new_page.get_by_role("button", name="Continue").click()
        self.new_page.get_by_role("textbox", name="Social security number").click()
        self.new_page.get_by_role("textbox", name="Social security number").fill("112-22-0333")
        self.new_page.get_by_role("textbox", name="Month").click()
        self.new_page.get_by_role("textbox", name="Month").fill("02")
        self.new_page.get_by_role("textbox", name="Day").fill("28")
        self.new_page.get_by_role("textbox", name="Year").fill("1975")
        self.new_page.get_by_role("button", name="Continue").click()
        self.new_page.get_by_role("radio", name="$10,000+").check()
        self.new_page.get_by_role("combobox", name="State").click()
        self.new_page.locator("div").filter(has_text=re.compile(r"^Alaska$")).nth(1).click()
        self.new_page.get_by_role("checkbox", name="I agree to not invest more").check()
        self.new_page.get_by_role("button", name="Continue").click()
        self.new_page.locator("div").filter(has_text=re.compile(r"^I have read and agree to Dwolla's Privacy Policy and Terms and Conditions\.$")).get_by_label("").check()
        self.new_page.get_by_label("").nth(1).check()
        self.new_page.get_by_role("link", name="Confirm").click()
        # self.new_page.get_by_role("link", name="I’ll do this later").click()
        self.new_page.locator("div").filter(has_text=re.compile(r"^I have read and agree to Dwolla's Privacy Policy and Terms and Conditions\.$")).get_by_label("").check()
        self.new_page.get_by_label("").nth(1).check()
        self.new_page.get_by_role("link", name="Confirm").click()
        self.new_page.get_by_role("button", name="Connect bank").click()
        self.new_page.get_by_role("button", name="Continue").click()
        # self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Continue without phone number").click()
        # self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("heading", name="Choose how you'll link your").click()
        # self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("heading", name="Choose how you'll link your").click()
        # self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Continue").click()
        # self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Chase").click()
        # with self.new_page.expect_popup() as page3_info:
        #     self.new_page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Continue to login").click()
        #     self.page3 = page3_info.value
        #     self.page3.get_by_role("button", name="Sign in").click()
        #     self.page3.get_by_role("button", name="Get code").click()
        #     self.page3.get_by_role("button", name="Get code").click()
        #     self.page3.get_by_role("button", name="Continue").click()
        #     self.page3.get_by_role("checkbox", name="I have read and accept the").check()
        #     self.page3.get_by_role("button", name="Connect account information").click()
        #     self.page3.close()
            # self.page2.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("heading", name="Save Chase with Plaid").click()
            # self.page2.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Finish without saving").click()
            # self.page2.get_by_role("button", name="Continue").click()
            
    
    def broke_flow(self):
        self.page.goto("https://www.staging-fe.realbricks.com/login")
        self.page.locator("#email").click()
        self.page.locator("#email").fill("sagar1674@yopmail.com")
        self.page.locator("#password").fill("Test@123")
        self.page.get_by_role("button", name="Log in").click()
        for i in range(4):
                self.page.get_by_role("textbox", name=f"SingleInput-{i}").fill("0")
        self.page.get_by_role("button",name="Complete Account Setup").click()
        self.page.get_by_role("textbox", name="Residential address").fill("222333 PEACHTREE PLACE")
        self.page.get_by_role("textbox", name="City").click()
        self.page.get_by_role("textbox", name="City").fill("ATLANTA")
        self.page.locator("div").filter(has_text=re.compile(r"^CityStateZip code$")).locator("span").first.click()
        self.page.locator("div").filter(has_text=re.compile(r"^Alaska$")).nth(1).click()
        self.page.get_by_role("textbox", name="Zip code").click()
        self.page.get_by_role("textbox", name="Zip code").fill("12345")
        self.page.get_by_role("button", name="Continue").click()
        time.sleep(10)
    #     # ---------------------
    #     context.close()
    #     browser.close()


    # with sync_playwright() as playwright:
    #     run(playwright)
