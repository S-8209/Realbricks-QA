import time , json, pytest , re
import json
from pathlib import Path
from plawright.Utils.Utils import load_users   
from plawright.Page.Login_FLow import login_User 
from plawright.Page.Buy_Flow import Test_Home_Initial_Buy
# from plawright.Page.Add_Bank_Flow import Test_Add_Bank_flow

class Portfolio_Cal:
    def __init__(self,page):
        self.page=page
    def portfolio_navigation(self):
        self.page.get_by_role("link", name="Portfolio").click()

    def portfolio_data(self):
        self.page.get_by_text("View", exact=True).click()
        self.page.get_by_role("button", name="Close").click()
    def portfolio_no_data(self):
        self.page.get_by_text("Start potentially building").click()
        self.page.get_by_text("Once you invest in a series").click()
        self.page.get_by_role("link", name="Browse properties").click()
    
    def total_account_value_data(self): 
        return  self.page.locator("[class*='portfoliocard__onevalue']").nth(0).inner_text()

    def total_account_value_detailed_data_pop_up(self):
        self.page.locator("div").filter(has_text=re.compile(r".*P & L$")).locator("path").click() 
        self.page.wait_for_function("""
                                    ()=>{
                                        const el=document.querySelector('.ant-modal-content');
                                        return el && !el.innerText.includes('0.00')
                                    }""",timeout=60000)
    def total_account_value_detailed_data(self,label):
        return self.page.locator(
            f"xpath=//span[text()='{label}']/parent::div/following-sibling::div//h4"
            ).text_content()
    
    
    def dividend_summary(self):
        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector("[class*='portfoliocard__onevalue']");
                return el && !el.innerText.includes('0.00')
            }""", timeout=60000)
        # Click the dividend details if needed
        self.page.locator("div").filter(has_text=re.compile(r".*dividend yield\\)Total dividends paid$"))\
            .locator("path").nth(1).click()
        last_dividend = self.page.locator("[class*='portfoliocard__onevalue']").nth(1).inner_text()
        total_dividend = self.page.locator("[class*='portfoliocard__alltimevalue.inner-btn'] [class*='value']").first.inner_text()
        return {
            "last_dividend": last_dividend,
            "total_dividend": total_dividend
        }
    def dividend_detailed(self):
        # self.page.locator("div").filter(has_text=re.compile(r".*dividend yield\\)Total dividends paid$"))\
        #     .locator("path").nth(1).click()
        self.page.locator("div").filter(has_text=re.compile(r".*dividend yield\)Total dividends paid$")).get_by_role("img").nth(1).click()

        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector("[class*='portfoliocard__onevalue']");
                return el && !el.innerText.includes('0.00')
            }""", timeout=60000)
        time.sleep(4)
    #     self.page.locator()
        # self.page.get_by_text("Last quarter dividend total$0.47Last quarter dividend yield*0.06%").click()\
        Last_quarter_dividend_total =self.page.locator("[class='ant-row acc-value']").nth(0).text_content()
        Last_quarter_dividend_yeild =self.page.locator("[class='ant-row acc-value']").nth(1).text_content()

        return {"Last_quarter_dividend_total":Last_quarter_dividend_total,
                "Last_quarter_dividend_yeild":Last_quarter_dividend_yeild}
    
    # page.get_by_text("Year-to-date dividend earnings$98.56All time dividend earnings$148.56Dividend").click()
    # page.get_by_text("Each share may distribute a").click()
    # page.get_by_role("button", name="View all dividend").click()
    # page.get_by_role("link", name="Portfolio").click()
    # page.locator("div").filter(has_text=re.compile(r"^\$148\.56\(11\.3% dividend yield\)Total dividends paid$")).get_by_role("img").nth(1).click()
    # page.get_by_text("* “Last Dividend yield” is").click()
    # page.get_by_role("button", name="Close").click()

        # https://www.staging-fe.realbricks.com/account/transactions?transactionsType=dividend
