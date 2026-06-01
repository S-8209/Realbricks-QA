import time
from playwright.sync_api import Page

class Add_Bank_flow:
    def __init__(self,page):
        self.page=page
    def add_bank_flow(self):
        # Navigate to Payment Methods
        self.page.locator(".accountnav__actions__item").nth(1).click()
        self.page.locator(".accountnav__actions__item").nth(1).click()
        self.page.get_by_role("link", name="Payment Methods").click()
        self.page.get_by_role("link", name="Payment Methods").click()
        self.page.get_by_role("button", name="Add new").click()
        time.sleep(2)
        self.page.get_by_role("button", name="Continue").click()
        
        # Wait for Plaid iframe
        plaid_frame = self.page.frame_locator("iframe[title='Plaid Link']")
        plaid_frame.get_by_role("button", name="Continue without phone number").click()
        time.sleep(2)
        plaid_frame.get_by_text("Continue").click()
        time.sleep(2)
        plaid_frame.get_by_role("button", name="Bank of America").click()
        time.sleep(2)
        
        # Handle login popup
        with self.page.expect_popup() as popup_info:
            plaid_frame.get_by_role("button", name="Continue to login").click()
        popup = popup_info.value
        popup.wait_for_load_state("networkidle")
        
        # Complete login in popup
        popup.get_by_role("button", name="Sign in").click()
        popup.get_by_role("button", name="Get code").click()
        popup.get_by_role("button", name="Submit").click()
        popup.locator("label").filter(has_text="Plaid Checking").click()
        popup.get_by_role("button", name="Continue").click()
        popup.get_by_role("checkbox", name="I have read and accept the Terms and Conditions").click()
        popup.get_by_role("button", name="Connect account information").click()
        plaid_frame=self.page.locator("iframe[title=\"Plaid Link\"]").content_frame.get_by_role("button", name="Finish without saving").click()
        time.sleep(10)
        # popup.close()
