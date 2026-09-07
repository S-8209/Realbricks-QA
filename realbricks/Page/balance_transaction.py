import re, time
import logging
from playwright.sync_api import Page
from realbricks.Page.base_page import BasePage


logger = logging.getLogger(__name__)

class balance_and_transaction(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.loc_total_account_value = page.locator(".subhead-1.card__content__number").first
        self.loc_shares_investments  = page.locator(".subhead-1.card__content__number").nth(1)
        self.loc_wallet_balance      = page.locator(".subhead-1.card__content__number").nth(2)

        self.loc_balance_transfer    = page.get_by_role("button", name="transfer")

        self.loc_transaction_type_filter = page.locator(".ant-select").nth(0)
        self.loc_time_period_filter      = page.locator(".ant-select").nth(1)
        self.loc_share_type_filter       = page.locator(".ant-select").nth(2)

        self.loc_transaction_items = page.locator(".trans-item")
        self.loc_status_groups     = page.locator(".subhead-3.mb-0")

        self.loc_total_amount      = page.locator(".transaction__items").locator(".trans-item__amount")
    def navigation(self) -> None:
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

    def account_balances(self) -> dict:
        """Capture all summary card values."""
        logger.info("Capturing account balance values")
        return {
            "total_account_value": self.loc_total_account_value.text_content(),
            "shares_investments": self.loc_shares_investments.text_content(),
            "wallet_balance": self.loc_wallet_balance.text_content(),
        }

    def apply_transaction_type_filter(self, option_text: str) -> None:
        logger.info(f"Applying transaction type filter: {option_text}")
        self.loc_transaction_type_filter.scroll_into_view_if_needed()
        self.select_dropdown_option(self.loc_transaction_type_filter, option_text)

    def apply_time_period_filter(self, option_text: str) -> None:
        logger.info(f"Applying time period filter: {option_text}")
        self.select_dropdown_option(self.loc_time_period_filter, option_text)

    def apply_share_type_filter(self, option_text: str) -> None:
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
        logger.info("Capturing all transaction types")
        self._load_all_transactions()
        items = self.loc_transaction_items
        return [
            items.nth(i).locator(".trans-item__type").first.text_content() or ""
            for i in range(items.count())
        ]

    def get_latest_transaction(self) -> dict:
        logger.info("Capturing latest transaction data")
        first_row = self.loc_transaction_items.first
        return {
            "date": first_row.locator(".trans-item__date").text_content() or "",
            "type": first_row.locator(".trans-item__type").first.text_content() or "",
            "shares": first_row.locator(".trans-item__type").nth(1).text_content() or "",
            "details": first_row.locator(".trans-item__details").text_content() or "",
            "amount": first_row.locator(".trans-item__amount").text_content() or "",
        }

    def get_transactions_count(self) -> int:
        logger.info("Counting transaction rows")
        self._load_all_transactions()
        return self.loc_transaction_items.count()

    def get_status_groups(self) -> list:
        logger.info("Capturing status groups")
        self._load_all_transactions()
        groups = self.loc_status_groups
        return [groups.nth(i).text_content() for i in range(groups.count())]

    # ── Shared popup helpers ──────────────────────────────────────
    def _open_transaction_popup(self):
        """Click the first transaction row and wait for the detail modal to open.
        Shared by every get_*_transaction_popup_detail() method below."""
        self._load_all_transactions()
        first_row = self.loc_transaction_items.first
        first_row.locator(".trans-item__details").click()
        try:
            self.page.wait_for_selector(".ant-modal-content", state="visible", timeout=5000)
            logger.info("Transaction detail popup opened")
        except Exception:
            logger.warning("Modal not found — trying alternative selector")
            self.page.wait_for_selector(".ant-modal", state="visible", timeout=5000)

    def close_transaction_popup(self) -> None:
        """Close the currently open transaction detail modal."""
        self.page.locator(".ant-modal-content button[aria-label='Close']").click()
        self.page.locator(".ant-modal-content").wait_for(state="hidden")
        logger.info("Transaction detail popup closed")

    # ── Buy / Sell popup ──────────────────────────────────────────
    def get_detailed_transaction_pop_up_detail(self) -> dict:
        logger.info("Capturing Buy/Sell popup info")
        # details["total_amount"] = self.loc_total_amount.first.text_content()
        self._open_transaction_popup()
        
        trade_type = self.page.locator(".mb-0.text-taupe").nth(0).text_content().strip()

        details = {
            "order_number": self.page.locator(".text-taupe").nth(0).text_content(),
            "initiated_on": self.page.locator(".text-taupe").nth(1).text_content(),
            "order_status": self.page.locator(".text-taupe").nth(2).text_content(),
            "trade_type": trade_type,
            "share_number": self.page.locator(".mb-0.text-taupe").nth(1).text_content(),
            "price_per_share": self.page.locator(".mb-0.text-taupe").nth(2).text_content(),
            "total_share_amount": self.page.locator(".mb-0.text-taupe").nth(3).text_content(),
            
        }

        if trade_type == "Sell - Secondary Market":
            details["total_cost"] = self.page.locator(".ant-modal-body").get_by_text(
                "Total Amount to Seller", exact=False
            ).text_content()
        else:
            details["total_cost"] = self.page.locator(".ant-modal-body").get_by_text(
                "Total Cost", exact=False
            ).text_content()

        if trade_type == "Buy - Primary Market (Initial Offering)":
            details["platform_fee"] = self.page.locator(".mb-0.text-taupe").nth(4).text_content()
        else:
            details["transaction_fee"] = self.page.locator(".mb-0.text-taupe").nth(4).text_content()
            details["platform_fee"] = self.page.locator(".mb-0.text-taupe").nth(5).text_content()

        return details

    # ── Dividend popup ────────────────────────────────────────────
    def get_dividend_transaction_popup_detail(self) -> dict:
        logger.info("Capturing dividend popup info")
        self._open_transaction_popup()

        full_text = self.page.locator(".ant-modal-body").text_content()

        share_match = re.search(r"(\d+)\s*share", full_text)
        dividend_per_share_match = re.search(r"Dividend Per Share:\s*\$?([\d.]+)", full_text)
        total_dividend_match = re.search(r"Total Dividend:\s*\$?([\d.]+)", full_text)
        payout_date_match = re.search(r"Payout Date:\s*([\d/]+)", full_text)

        return {
            "order_number": self.page.locator(".text-taupe").nth(0).text_content(),
            "initiated_on": self.page.locator(".text-taupe").nth(1).text_content(),
            "order_status": self.page.locator(".text-taupe").nth(2).text_content(),
            "share_number": share_match.group(1) if share_match else None,
            "dividend_per_share": dividend_per_share_match.group(1) if dividend_per_share_match else None,
            "total_dividend_received": total_dividend_match.group(1) if total_dividend_match else None,
            "dividend_pay_date": payout_date_match.group(1) if payout_date_match else None,
        }

    # ── Withdrawal / Deposit popup (identical shape, shared implementation) ──
    def _get_simple_transaction_popup_detail(self) -> dict:
        self._open_transaction_popup()

        transaction_line = self.page.locator(".mb-40.text-taupe").text_content()
        match = re.search(r"([A-Za-z\s]+)-\s*\$?([\d,]+\.\d{2})", transaction_line)
        transaction_type = match.group(1).strip() if match else None
        amount = match.group(2).replace(",", "") if match else None

        return {
            "order_number": self.page.locator(".text-taupe").nth(0).text_content(),
            "initiated_on": self.page.locator(".text-taupe").nth(1).text_content(),
            "order_status": self.page.locator(".text-taupe").nth(2).text_content(),
            "transaction_type": transaction_type,
            "amount": amount,
        }

    def get_withdrawal_transaction_popup_detail(self) -> dict:
        logger.info("Capturing withdrawal popup info")
        return self._get_simple_transaction_popup_detail()

    def get_deposit_transaction_popup_detail(self) -> dict:
        logger.info("Capturing deposit popup info")
        return self._get_simple_transaction_popup_detail()

    # ── Empty state ───────────────────────────────────────────────
    def get_no_data_message(self) -> dict:
        logger.info("Capturing no-data message")
        return {
            "no_data_message": self.page.locator(".nodata").locator(".subhead-3.mb-4").text_content(),
            "filter_no_result_message": self.page.locator(".nodata").locator(".mb-0").text_content(),
        }
    def get_all_order_numbers(self):
        logger.info("Get all order numbers")
        self._load_all_transactions()
        items=self.loc_transaction_items
        order_num=[]
        for i in range (items.count()):
            items.nth(i).locator(".trans-item__details").click()
            try:
                self.page.wait_for_selector(".ant-modal-content", state="visible", timeout=5000)
                logger.info("Transaction detail popup opened")
            except Exception:
                logger.warning("Modal not found — trying alternative selector")
                self.page.wait_for_selector(".ant-modal", state="visible", timeout=5000)
            order_number=self.page.locator(self.page.locator(".text-taupe").nth(0).text_content())
            order_num.append(order_number)
            self.close_transaction_popup()
        return order_num

    def transaction_list_matches_popup_detail(self):
        row_transaction_amount=self.loc_total_amount.first.text_content()
        self._open_transaction_popup()
        pop_up_transaction_amount=self.page.locator(".mb-0.text-taupe").nth(3).text_content()
        return {
            "row_amount":row_transaction_amount,
            "pop_up_amount":pop_up_transaction_amount}
    def get_row_and_popup_amount(self) -> dict:
        """Capture the amount shown on the list row and the amount shown in its popup, for cross-checking."""
        logger.info("Capturing row and popup amount for cross-check")
        # self.page.wait_for_selector
        row_amount = self.page.locator(".transaction__items").locator(".trans-item__amount").nth(0).text_content()
        # self._open_transaction_popup()
        detail = self.get_detailed_transaction_pop_up_detail()  # already opens the popup and extracts everything, including total_cost

        return {
        "row_amount": row_amount,
        "popup_amount": detail["total_cost"],
        }