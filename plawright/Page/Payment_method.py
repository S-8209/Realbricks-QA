import time, re
from playwright.sync_api import Page 

class payments  :
    def __init__(self,page):
        self.page= page
        self.wallet=self.page.get_by_text(re.compile(r"Realbricks Wallet"))
        self.bank=self.page.get_by_text(re.compile(r"Chase | Bank of America | Wells Fargo"))


    # def continue_payment(self):

    def payment_multiple_option(self,payment_type,method=None):
        self.page.locator("span.icon-wrap.cursor-pointer").click()
        self.page.locator("//span[@class='ant-select-selection-item']").click()
        if payment_type=="Bank":
            self.bank.click()
        elif payment_type=="Wallet":
            self.wallet.click()
            
            
            