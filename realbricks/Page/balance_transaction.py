import re, time
import logging
from typing import Optional
from playwright.sync_api import Page
from realbricks.Page.base_page import BasePage


logger = logging.getLogger(__name__)

class balance_and_transaction(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # self.loc_nav_link=page.get_by_role("link", name="Balances & Transactions")
        
        self.loc_total_account_value =page.locator(".subhead-1.card__content__number").first
        self.loc_shares_investments  = page.locator(".subhead-1.card__content__number").nth(1)
        self.loc_wallet_balance      = page.locator(".subhead-1.card__content__number").nth(2)
        
        # self.loc_balance_transfer    =page.locator(".card__content__action.text-copper.cursor-pointer.large",has_text="Transfer")
        
        self.loc_balance_transfer    =page.get_by_role("button",name="transfer")
        
        # self.loc_transaction_type_filter = page.locator("//input[@id='transactionType']")
        # self.loc_transaction_type_filter = page.locator("#transactionType")
        self.loc_transaction_type_filter = page.locator(".ant-select").nth(0)
        self.loc_time_period_filter      = page.locator(".ant-select").nth(1)
        self.loc_share_type_filter       = page.locator(".ant-select").nth(2)
        
        # ── Transaction items ───────────────────────
        self.loc_transaction_items  = page.locator(".trans-item")
        self.loc_status_groups      = page.locator(".subhead-3.mb-0")
        
        # self.loc_transactio_detailed_pop_up=self.loc_transaction_items.page.locator(".trans-item__details")
        
    def navigation(self)->None:
        logger.info("Navigating to Balances & Transactions page")
        self.navigate_to("Balances & Transactions")  
        self.loc_total_account_value.wait_for(state="visible")
        self.page.wait_for_function(
            """() => {
                const el = document.querySelector('.subhead-1.card__content__number');
                return el && !el.textContent.includes('0.00');
            }"""
        )
        logger.info("Balances & Transactions page loaded with data")
        
    def account_balances(self)->dict:
        """Capture all summary card values."""
        logger.info("Capturing account balance values")
        return{
            "total_account_value":self.loc_total_account_value.text_content(),
            "shares_investments":self.loc_shares_investments.text_content(),
            "wallet_balance":self.loc_wallet_balance.text_content()}
    def apply_transaction_type_filter(self, option_text: str) -> None:
        """Select an option from the Transaction type dropdown."""
        logger.info(f"Applying transaction type filter: {option_text}")
        self.loc_transaction_type_filter.scroll_into_view_if_needed()
        self.select_dropdown_option(self.loc_transaction_type_filter, option_text)


    def apply_time_period_filter(self, option_text: str) -> None:
        """Select an option from the Time period dropdown."""
        logger.info(f"Applying time period filter: {option_text}")
        self.select_dropdown_option(self.loc_time_period_filter, option_text)

    def apply_share_type_filter(self, option_text: str) -> None:
        """Select an option from the Share type dropdown."""
        logger.info(f"Applying share type filter: {option_text}")
        self.select_dropdown_option(self.loc_share_type_filter, option_text)

    def _load_all_transactions(self, max_scrolls: int = 30) -> None:
        """Scroll down until no new rows appear (transaction list uses infinite scroll)."""
        previous_count = -1
        stable_rounds = 0
        for _ in range(max_scrolls):
            current_count = self.loc_transaction_items.count()
            if current_count == previous_count:
                stable_rounds += 1
                if stable_rounds >= 2:
                    break
            else:
                stable_rounds = 0
            previous_count = current_count

            self.loc_transaction_items.last.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)

        logger.info(f"Loaded {self.loc_transaction_items.count()} transaction rows")

    def get_all_transaction_types(self) -> list:
        """Get the transaction type text for every transaction row, after loading them all."""
        logger.info("Capturing all transaction types")
        self._load_all_transactions()
        items = self.loc_transaction_items
        return [
            items.nth(i).locator(".trans-item__type").first.text_content() or ""
            for i in range(items.count())
        ]


    def get_latest_transaction(self) -> dict[str, str]:
        """Get first transaction row data."""
        logger.info("Capturing latest transaction data")
        first_row = self.loc_transaction_items.first
        return {
            "date"   : first_row.locator(".trans-item__date").text_content() or "",
            "type"   : first_row.locator(".trans-item__type").first.text_content() or "",
            "shares" : first_row.locator(".trans-item__type").nth(1).text_content() or "",
            "details": first_row.locator(".trans-item__details").text_content() or "",
            "amount" : first_row.locator(".trans-item__amount").text_content() or "",
        }

    def get_transactions_count(self) -> int:
        """Get total number of transaction rows, loading all via infinite scroll first."""
        logger.info("Counting transaction rows")
        self._load_all_transactions()
        return self.loc_transaction_items.count()

    def get_status_groups(self) -> list:
        """Get all status group headers, loading all transactions via infinite scroll first."""
        logger.info("Capturing status groups")
        self._load_all_transactions()
        groups = self.loc_status_groups
        return [groups.nth(i).text_content() for i in range(groups.count())]
    
    def get_detailed_transaction_pop_up_detail(self):
        logger.info("Captuaring the pop up")
        self._load_all_transactions()
        first_row = self.loc_transaction_items.first
        first_row.locator(".trans-item__details").click()
        try:
            self.page.wait_for_selector(".ant-modal-content", state="visible", timeout=5000)
            logger.info("Transaction detail popup opened")
        except:
            logger.warning("Modal not found — trying alternative selector")
            self.page.wait_for_selector(".ant-modal", state="visible", timeout=5000)
        return{
        "order_number":self.page.locator(".text-taupe").nth(0).text_content(),   
        "initiated_on":self.page.locator(".text-taupe").nth(1).text_content(),
        "order_status":self.page.locator(".text-taupe").nth(2).text_content(),
        "trade_type":self.page.locator(".mb-0.text-taupe").nth(0).text_content(),
        "share_number":self.page.locator(".mb-0.text-taupe").nth(1).text_content(),
        "price_per_share":self.page.locator(".mb-0.text-taupe").nth(2).text_content(),
        "total_share_amount":self.page.locator(".mb-0.text-taupe").nth(3).text_content(),
        "transaction_fee":self.page.locator(".mb-0.text-taupe").nth(4).text_content(),
        "platform_fee":self.page.locator(".mb-0.text-taupe").nth(5).text_content(),
        "total_cost": self.page.locator("div").last.text_content()
        }