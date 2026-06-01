import time , json, pytest , re
import json
from pathlib import Path
from plawright.Utils.Utils import load_users   
from plawright.Page.Login_FLow import login_User 


# def test_buy_order_success(page, user):
class Test_Home_Initial_Buy:
    def __init__(self,page):
        self.page=page
        self.buy_now_button=self.page.locator("div.marketslider").nth(0).get_by_role("button", name='Buy Now').nth(0)

        self.share_Max_amount= self.page.get_by_text("Max (9.8%)",exact=False)
        self.custom_amount =self.page.locator("//input[@id='share']")
        self.popular_amount=self.page.get_by_text(re.compile(r"Popular"))
        self.suggested_amount=self.page.get_by_text(re.compile(r"Suggested"))
        self.preview_order=self.page.get_by_role("button", name="Preview order")
    def buy_share(self):
        self.buy_now_button.click()
        for i in range(4):
            self.enter_pin=self.page.get_by_role("textbox", name=f"SingleInput-{i}").fill("0")
        self.preview_order.click()
    def share_selection(self,share_type,amount=None):
        if share_type=="max":
            self.share_Max_amount.click()
        elif share_type=="custom":
            self.custom_amount.fill(amount)
        elif share_type=="popular":
            self.popular_amount.click()


        
    # def pay_with_wallet(self):
    #     self.page.locator("span.icon-wrap.cursor-pointer").click()
    #     self.page.locator("//span[@class='ant-select-selection-item']").click()
    #     self.page.get_by_text(re.compile(r"Realbricks Wallet")).click()
        
    # def pay_with_bank(self):
    #     time.sleep(2)
    #     self.page.locator("span.icon-wrap.cursor-pointer").click()
    #     self.page.locator("//span[@class='ant-select-selection-item']").click()
    #     # self.page.get_by_text(re.compile(r"Chase Bank | Bank of America | Well fargo")).click()
    #     self.page.get_by_text(re.compile(r"Chase | Bank of America | Wells Fargo")).click()

    def accept_legal_terms(self):
        self.page.locator("//input[@type='checkbox']").check()
        self.page.get_by_role("button", name="Place order").click()
        self.page.get_by_role("checkbox", name=re.compile(r"I attest that I am")).check()
        self.page.get_by_role("checkbox", name="I have read and understand the above Subscription Agreement.").check()
        self.page.get_by_role("button", name="Agree to terms").click()





# page.locator("div").filter(has_text=re.compile(r"^Realbricks Wallet\$1,672\.91$")).locator("svg").click()
#     page.get_by_text("Realbricks Wallet $").click()
#  
#     page.locator(".icon-wrap.ml-auto > svg > path").click()
#     page.locator("div").filter(has_text=re.compile(r"^Realbricks Wallet\$1,672\.91$")).locator("svg").click()
#     page.get_by_text("Realbricks Wallet $").click()
#     page.locator("span").filter(has_text="Realbricks Wallet $").click()
#     page.locator("span").filter(has_text="Realbricks Wallet $").click()
#     page.get_by_text("Manually Added Bank ***").click()
#     page.locator("div").filter(has_text=re.compile(r"^Manually Added Bank\*\*\* 4444$")).get_by_role("img").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
# "