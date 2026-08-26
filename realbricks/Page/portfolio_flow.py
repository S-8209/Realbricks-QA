# realbricks/Page/portfolio_flow.py

import re
import logging
from typing import Dict, Tuple, List
from realbricks.Page.base_page import BasePage
from playwright.sync_api import Page
from datetime import datetime
from realbricks.Configs.constants import (
    TIMEOUT_SHORT,
    TIMEOUT_MEDIUM,
)

logger = logging.getLogger(__name__)


class Portfolio_Cal(BasePage):

    # ─────────────────────────────────────────
    # CLASS CONSTANTS — SELECTORS
    # ─────────────────────────────────────────
    PORTFOLIO_CARD_VALUE  = "[class*='portfoliocard__onevalue']"
    ALL_TIME_VALUE        = "[class*='portfoliocard__alltimevalue']"
    WALLET_ONE_VALUE      = "[class*='portfoliocard__onevalue d-flex align-items-center']"
    ACC_VALUE_ROW         = "[class='ant-row acc-value']"
    NET_VALUE_ROW         = "[class='ant-row net-value mb-8']"
    WALLET_NET_VALUE      = "[class='net-value-wrap']"
    DATE_DISPLAY          = "[class='mb-48 text-taupe']"
    WALLET_DETAILS_ICON   = "div:nth-child(3) > .portfoliocard__block > .portfoliocard__alltimevalue > .redirect > .icon-wrap > svg > path"
    SUCCESS_MESSAGE_TEXT  = "Transfer request created successfully. Your transaction will execute on Admin approval"
    ORDER_DATE            = "[class='ant-table-cell']"
    POPUP_ROW_SELECTOR    = ".d-flex.align-items-center.justify-content-space-between"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.today = datetime.now().strftime("%m/%d/%Y")

    # ─────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────

    def portfolio_navigation(self) -> None:
        """Navigate to Portfolio page."""
        logger.info("Navigating to Portfolio page")
        self.page.get_by_role("link", name="Portfolio").click()

    # ─────────────────────────────────────────
    # PORTFOLIO CARD
    # ─────────────────────────────────────────

    def total_account_value_data(self) -> str:
        """Return the Total Account Value shown on the portfolio card."""
        logger.info("Fetching total account value")
        self.page.wait_for_selector(self.PORTFOLIO_CARD_VALUE, timeout=30000)
        return self.page.locator(self.PORTFOLIO_CARD_VALUE).nth(0).text_content() or ""

    def total_account_value_detailed_data_pop_up(self) -> None:
        """Open the P&L detailed popup and wait until data appears."""
        logger.info("Opening P&L detailed popup")
        try:
            self.page.locator("div").filter(
                has_text=re.compile(r".*P & L$")
            ).locator("path").click()
        except Exception:
            logger.warning("P&L click failed — continuing")

        self.page.wait_for_function(
            """
            () => {
                const el = document.querySelector('.ant-modal-content');
                return el && !el.innerText.includes('0.00');
            }
            """,
            timeout=TIMEOUT_SHORT,
        )
        logger.info("P&L popup loaded successfully")

    def total_account_value_detailed_data(self, label: str) -> str:
        """Extract a value from the detailed popup by label."""
        logger.info(f"Fetching popup value for: {label}")
        xpath = f"xpath=//span[text()='{label}']/parent::div/following-sibling::div//h4"
        self.page.wait_for_selector(xpath, timeout=15000)
        return self.page.locator(xpath).text_content() or ""

    # ─────────────────────────────────────────
    # DIVIDEND
    # ─────────────────────────────────────────

    def dividend_summary(self) -> Dict[str, str]:
        """Return last dividend and total dividend summary."""
        logger.info("Fetching dividend summary")
        self.page.wait_for_selector(self.PORTFOLIO_CARD_VALUE, timeout=TIMEOUT_SHORT)

        try:
            btns = self.page.locator("div").filter(
                has_text=re.compile(r".*dividend yield\)Total dividends paid$")
            )
            if btns.count() > 0:
                btns.locator("path").nth(1).click()
        except Exception:
            logger.warning("Dividend summary icon click failed — continuing")

        last_dividend = self.page.locator(self.PORTFOLIO_CARD_VALUE).nth(1).text_content() or ""

        try:
            total_dividend = (
                self.page.locator(self.ALL_TIME_VALUE)
                .nth(1)
                .locator("[class*='value']")
                .text_content()
            ) or ""
        except Exception:
            logger.warning("Total dividend fetch failed — returning empty")
            total_dividend = ""

        return {
            "last_dividend" : last_dividend,
            "total_dividend": total_dividend,
        }

    def dividend_detailed(self) -> Dict[str, str]:
        """Open dividend detailed view and return multiple metrics."""
        logger.info("Fetching detailed dividend data")

        try:
            self.page.locator("div").filter(
                has_text=re.compile(r".*dividend yield\)Total dividends paid$")
            ).get_by_role("img").nth(1).click()
        except Exception:
            logger.warning("Dividend detail icon click failed — continuing")

        self.page.wait_for_function(
            """
            () => {
                const el = document.querySelector("[class*='portfoliocard__onevalue']");
                return el && !el.innerText.includes('0.00');
            }
            """,
            timeout=TIMEOUT_SHORT,
        )

        def _safe_text(selector: str, index: int = 0) -> str:
            try:
                return self.page.locator(selector).nth(index).text_content() or ""
            except Exception:
                logger.warning(f"Could not fetch text for {selector}[{index}]")
                return ""

        try:
            self.page.get_by_role("button", name="view all dividend").click()
        except Exception:
            logger.warning("View all dividend button not found — continuing")

        return {
            "last_quarter_total": _safe_text(self.ACC_VALUE_ROW, 0),
            "last_quarter_yield": _safe_text(self.ACC_VALUE_ROW, 1),
            "ytd_earnings"      : _safe_text(self.NET_VALUE_ROW, 0),
            "all_time_earnings" : _safe_text(self.NET_VALUE_ROW, 1),
            "dividend_yield"    : _safe_text(self.NET_VALUE_ROW, 2),
        }

    # ─────────────────────────────────────────
    # WALLET
    # ─────────────────────────────────────────

    def wallet_summary(self) -> Dict[str, str]:
        """Return wallet summary — total wallet balance."""
        logger.info("Fetching wallet summary")
        self.page.wait_for_selector(self.WALLET_ONE_VALUE, timeout=TIMEOUT_MEDIUM)
        total_wallet_balance = self.page.locator(self.WALLET_ONE_VALUE).text_content() or ""
        return {"total_wallet_balance": total_wallet_balance}

    def wallet_details(self) -> Dict[str, str]:
        """Open wallet details modal and return balances."""
        logger.info("Opening wallet details modal")

        try:
            self.page.locator(self.WALLET_DETAILS_ICON).click()
        except Exception:
            logger.warning("Wallet details icon click failed — continuing")

        self.page.wait_for_function(
            """
            () => {
                const el = document.querySelector("[class*='ant-modal-body']");
                return el && !el.innerText.includes('0.00');
            }
            """,
            timeout=TIMEOUT_MEDIUM,
        )

        return {
            "total_wallet_balance"    : self.page.locator(self.ACC_VALUE_ROW).nth(0).text_content() or "",
            "pending_withdrawals"     : self.page.locator(self.ACC_VALUE_ROW).nth(1).text_content() or "",
            "available_wallet_balance": self.page.locator(self.WALLET_NET_VALUE).nth(0).text_content() or "",
        }

    # ─────────────────────────────────────────
    # TRANSFERS
    # ─────────────────────────────────────────

    def _pick_date(self) -> None:
        """Click date field — date defaults to today so no fill needed."""
        try:
            self.page.get_by_role("textbox", name="Date of transfer").click()
            # Field is readonly — date already set to today
            logger.info(f"Date picker opened — today's date: {self.today}")
        except Exception as e:
            logger.warning(f"Date picker failed: {e}")

    def bank_to_wallet_transfer(self, amount: str = "100") -> None:
        """Initiate a bank to wallet transfer."""
        logger.info(f"Initiating bank to wallet transfer: ${amount}")

        self.page.get_by_text("Transfer", exact=True).click()
        self.page.get_by_role("combobox", name="Transfer from").click()
        self.page.get_by_text(re.compile(r"Chase|Bank of America|Wells Fargo")).click()
        self.page.get_by_role("combobox", name="Transfer to").click()
        self.page.get_by_text(re.compile(r"Realbricks Wallet \$")).nth(1).click()
        self.page.get_by_role("textbox", name="Amount").fill(amount)
        self._pick_date()
        self.page.get_by_role("button", name="Initiate Transfer").click()

        try:
            self.page.get_by_text(f"Your transfer of ${amount} has").wait_for(
                state="visible", timeout=15000
            )
            logger.info("Bank to wallet transfer confirmed")
        except Exception:
            logger.warning("Transfer confirmation not visible — continuing")

    def wallet_to_bank(self, amount: str = "100") -> Dict[str, str]:
        """Initiate a wallet to bank transfer and return result data."""
        logger.info(f"Initiating wallet to bank transfer: ${amount}")

        self.page.get_by_text("Transfer", exact=True).wait_for(state="visible", timeout=5000)

        old_total_wallet_balance = self.page.locator(self.WALLET_ONE_VALUE).nth(0).text_content() or ""

        self.page.get_by_text("Transfer", exact=True).click()
        self.page.get_by_role("combobox", name="Transfer from").click()
        self.page.get_by_text(re.compile(r"Realbricks Wallet \$")).nth(0).click()
        self.page.get_by_role("combobox", name="Transfer to").click()
        self.page.get_by_text(re.compile(r"Chase|Bank of America|Wells Fargo")).nth(1).click()
        self.page.get_by_role("textbox", name="Amount").fill(amount)
        self._pick_date()
        self.page.get_by_role("button", name="Initiate Transfer").click()

        try:
            self.page.get_by_text(f"Your transfer of ${amount} has").wait_for(
                state="visible", timeout=15000
            )
            logger.info("Wallet to bank transfer confirmed")
        except Exception:
            logger.warning("Transfer confirmation not visible — continuing")

        success_message = self.page.get_by_text(self.SUCCESS_MESSAGE_TEXT).text_content() or ""
        transfer_date   = self.page.locator(self.DATE_DISPLAY).text_content() or ""

        self.page.get_by_role("button", name="Done").click()
        self.page.wait_for_selector(self.WALLET_ONE_VALUE, state="visible", timeout=10000)

        updated_total_wallet_balance = self.page.locator(self.WALLET_ONE_VALUE).nth(0).text_content() or ""

        return {
            "old_total_wallet_balance"    : old_total_wallet_balance,
            "updated_total_wallet_balance": updated_total_wallet_balance,
            "success_message"             : success_message,
            "transfer_date"               : transfer_date,
        }

    # ─────────────────────────────────────────
    # OPEN ORDERS
    # ─────────────────────────────────────────

    def open_order_validation(self) -> str:
        """Return property name from first open order row."""
        return self.page.locator("tbody tr").first.locator("td").first.text_content()

    def open_order_section(self) -> bool:
        """Check if open orders section is visible."""
        return self.page.locator("[class='ant-table-content']").is_visible()

    def open_order_headers_visible(self) -> List[str]:
        """Return list of open order table header texts."""
        headers_data = []
        self.page.wait_for_selector(".ant-table-thead .ant-table-cell")
        header = self.page.locator(".ant-table-thead").first.locator(".ant-table-cell")
        for i in range(header.count()):
            headers_data.append(header.nth(i).text_content())
        return headers_data

    def _get_popup_value(self, label: str) -> str:
        """Extract a value from the order detail popup by label."""
        return self.page.locator(self.POPUP_ROW_SELECTOR).filter(
            has_text=label
        ).locator("span").nth(1).text_content() or ""

    def open_orders_1st_data(self) -> Tuple:
        """Extract first row table data and popup detail values."""
        open_order_data = []

        self.page.wait_for_selector(".ant-table-tbody")
        open_order       = self.page.locator(".ant-table-row").first.locator(".ant-table-cell")
        view_detail_order = self.page.locator(".ant-table-row").first.locator(
            "[class='fw-600 text-copper cursor-pointer']"
        )

        for i in range(open_order.count()):
            open_order_data.append(open_order.nth(i).text_content())

        logger.info(f"Open order data extracted: {open_order_data}")

        self.safe_click(view_detail_order, "Opens up the detailed view of open order")

        # Wait for popup to fully load
        self.page.wait_for_selector("p.subhead-2.text-copper.mb-0", state="visible")
        name_locator = self.page.locator("p.subhead-2.text-copper.mb-0")
        self.page.wait_for_function(
            "el => el.textContent.trim().length > 0",
            arg=name_locator.element_handle()
        )
        # property_name_pop_up = name_locator.text_content() or ""
        property_name_pop_up             = self.page.locator("p.subhead-2.text-copper.mb-0").text_content() or ""
        property_status_pop_up           = self._get_popup_value("Status")
        property_type_pop_up             = self._get_popup_value("Type")
        property_category_pop_up         = self._get_popup_value("Category")
        property_quantity_pop_up         = self._get_popup_value("Quantity")
        property_price_per_share_pop_up  = self._get_popup_value("Price per Share")
        property_total_investment_pop_up = self._get_popup_value("Total Investment (USD)")
        property_platform_fee_pop_up     = self._get_popup_value("Platform Fee")
        property_total_purchase_pop_up   = self._get_popup_value("Total Purchase (USD)")

        logger.info(f"Popup data extracted — Property: {property_name_pop_up}, Status: {property_status_pop_up}")

        return (
            open_order_data,
            property_name_pop_up,
            property_status_pop_up,
            property_type_pop_up,
            property_category_pop_up,
            property_quantity_pop_up,
            property_price_per_share_pop_up,
            property_total_investment_pop_up,
            property_platform_fee_pop_up,
            property_total_purchase_pop_up,
        )