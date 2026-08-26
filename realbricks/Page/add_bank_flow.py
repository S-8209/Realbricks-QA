import logging
from playwright.sync_api import Page
from realbricks.Page.base_page import BasePage
from realbricks.Configs.constants import TIMEOUT_SHORT, TIMEOUT_MEDIUM, TIMEOUT_LONG

logger = logging.getLogger(__name__)

class Add_Bank_flow(BasePage):
    def __init__(self, page: Page, new_page: Page = None):
        super().__init__(page)
        self.active_page = new_page if new_page else page
        
        # Locators
        self.loc_connect_bank = self.active_page.get_by_role("button", name="Connect bank")
        self.loc_payment_methods = self.active_page.get_by_role("link", name="Payment Methods")
        self.loc_add_new = self.active_page.get_by_role("button", name="Add new")
        self.loc_continue = self.active_page.get_by_role("button", name="Continue")
        self.loc_plaid_frame = self.active_page.frame_locator("iframe[title='Plaid Link']")
        self.loc_account_nav = self.active_page.locator(".accountnav__actions__item")

    def onboarding_add_bank(self) -> None:
        """Click Connect bank button during onboarding."""
        logger.info("Clicking Connect bank button")
        self.safe_click(self.loc_connect_bank, "Connect bank button")

    def add_bank_navigation(self) -> None:
        """Navigate to Payment Methods page."""
        logger.info("Navigating to Payment Methods")
        self.safe_click(self.loc_account_nav.nth(1), "Account nav item")
        self.safe_click(self.loc_payment_methods, "Payment Methods link")
        self.safe_click(self.loc_add_new, "Add new button")
        self.active_page.wait_for_timeout(TIMEOUT_SHORT)

    def add_bank_flow(self) -> None:
        """Complete full bank connection flow via Plaid."""
        logger.info("Starting bank connection flow")
        
        # Step 1 — Click Continue
        self.safe_click(self.loc_continue, "Continue button")
        logger.info("Clicked Continue")

        # Step 2 — Plaid iframe interactions
        logger.info("Interacting with Plaid iframe")
        self.loc_plaid_frame.get_by_role("button", name="Continue without phone number").click()
        self.active_page.wait_for_timeout(TIMEOUT_SHORT)
        
        self.loc_plaid_frame.get_by_text("Continue").click()
        self.active_page.wait_for_timeout(TIMEOUT_SHORT)
        
        self.loc_plaid_frame.get_by_role("button", name="Bank of America").click()
        self.active_page.wait_for_timeout(TIMEOUT_SHORT)
        logger.info("Selected Bank of America")

        # Step 3 — Handle login popup
        logger.info("Handling login popup")
        with self.active_page.expect_popup() as popup_info:
            self.loc_plaid_frame.get_by_role("button", name="Continue to login").click()
        
        popup = popup_info.value
        popup.wait_for_load_state("networkidle")
        logger.info("Popup loaded")

        # Step 4 — Complete login in popup
        popup.get_by_role("button", name="Sign in").click()
        popup.get_by_role("button", name="Get code").click()
        popup.get_by_role("button", name="Submit").click()
        popup.locator("label").filter(has_text="Plaid Checking").click()
        popup.get_by_role("button", name="Continue").click()
        popup.get_by_role("checkbox", name="I have read and accept the Terms and Conditions").click()
        popup.get_by_role("button", name="Connect account information").click()
        logger.info("Bank login completed")

        # Step 5 — Finish
        self.active_page.frame_locator("iframe[title='Plaid Link']").get_by_role("button", name="Finish without saving").click()
        self.active_page.wait_for_load_state("networkidle")
        logger.info("Bank connection flow completed")