import re
import logging
from playwright.sync_api import Page
from realbricks.Page.sign_up import BasePage
from realbricks.Configs.constants import PAYMENT_BANK, PAYMENT_WALLET

logger = logging.getLogger(__name__)

class payments(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.loc_payment_icon     = page.locator("span.icon-wrap.cursor-pointer")
        self.loc_payment_dropdown = page.locator("//span[@class='ant-select-selection-item']")
        
        # ✅ Scoped to #bank-anchor — fixes strict mode violation
        self.loc_wallet = page.locator("#bank-anchor").get_by_text(
            re.compile(r"Realbricks Wallet \$")
        )
        self.loc_bank = page.locator("#bank-anchor").get_by_text(
            re.compile(r"Chase|Bank of America|Wells Fargo")
        )
    # ✅ Add this
    def pay_with_wallet(self) -> None:
        self.safe_click(self.loc_payment_icon,     "Payment icon")
        self.safe_click(self.loc_payment_dropdown, "Payment dropdown")
        self.safe_click(self.loc_wallet,           "Realbricks Wallet")
        logger.info("Wallet selected")

    # ✅ Add this
    def pay_with_bank(self, bank_name: str = None) -> None:
        self.safe_click(self.loc_payment_icon,     "Payment icon")
        self.safe_click(self.loc_payment_dropdown, "Payment dropdown")
        self.safe_click(self.loc_bank,"")
        # self.page.get_by_text(re.compile(rf"{bank_name}")).click()
        logger.info(f"Bank selected: {bank_name}")

    def payment_multiple_option(self, payment_type: str, method: str = None) -> None:
        self.safe_click(self.loc_payment_icon,     "Payment icon")
        self.safe_click(self.loc_payment_dropdown, "Payment dropdown")

        if payment_type == PAYMENT_BANK:
            self.page.get_by_text(re.compile(rf"{method}")).click()
            logger.info(f"Bank selected: {method}")

        elif payment_type == PAYMENT_WALLET:
            self.safe_click(self.loc_wallet, "Realbricks Wallet")
            logger.info("Wallet selected")

        else:
            raise ValueError(f"Invalid payment_type: {payment_type}")