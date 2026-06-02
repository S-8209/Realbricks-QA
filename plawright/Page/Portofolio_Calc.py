import time
import re
from typing import Dict
from playwright.sync_api import Page

class Portfolio_Cal:
    def __init__(self, page: Page):
        self.page = page

    def portfolio_navigation(self) -> None:
        """Navigate to Portfolio page."""
        self.page.get_by_role("link", name="Portfolio").click()

    def portfolio_data(self) -> None:
        """Open portfolio card and close the modal."""
        self.page.get_by_text("View", exact=True).click()
        self.page.get_by_role("button", name="Close").click()

    def portfolio_no_data(self) -> None:
        """Actions when portfolio is empty - navigate to browse properties."""
        self.page.get_by_text("Start potentially building").click()
        self.page.get_by_text("Once you invest in a series").click()
        self.page.get_by_role("link", name="Browse properties").click()

    def total_account_value_data(self) -> str:
        """Return the Total Account Value shown on the portfolio card."""
        sel = "[class*='portfoliocard__onevalue']"
        self.page.wait_for_selector(sel, timeout=30000)
        return self.page.locator(sel).nth(0).text_content() or ""

    def total_account_value_detailed_data_pop_up(self) -> None:
        """Open the P & L (detailed) popup and wait until data appears."""
        # Click the P & L control (best-effort)
        try:
            self.page.locator("div").filter(has_text=re.compile(r".*P & L$")) .locator("path").click()
        except Exception:
            pass

        # Wait for modal to appear and populate
        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector('.ant-modal-content');
                return el && !el.innerText.includes('0.00')
            }""",
            timeout=60000,
        )

    def total_account_value_detailed_data(self, label: str) -> str:
        """Extract a value from the detailed popup by label."""
        xpath = f"xpath=//span[text()='{label}']/parent::div/following-sibling::div//h4"
        self.page.wait_for_selector(xpath, timeout=15000)
        return self.page.locator(xpath).text_content() or ""

    def dividend_summary(self) -> Dict[str, str]:
        """Return summary dividend values: last dividend and total dividend."""
        sel = "[class*='portfoliocard__onevalue']"
        self.page.wait_for_selector(sel, timeout=60000)

        # Try to open dividend details if there is a click target (best-effort)
        try:
            btns = self.page.locator("div").filter(has_text=re.compile(r".*dividend yield\)Total dividends paid$"))
            if btns.count() > 0:
                btns.locator("path").nth(1).click()
        except Exception:
            pass

        last_dividend = self.page.locator(sel).nth(1).text_content() or ""

        # Try a more specific selector for total dividend, fallback to empty
        try:
            total_dividend = (
                self.page.locator("[class*='portfoliocard__alltimevalue']")
                .nth(1)
                .locator("[class*='value']")
                .text_content()
            ) or ""
        except Exception:
            total_dividend = ""

        return {"last_dividend": last_dividend, "total_dividend": total_dividend}

    def dividend_detailed(self) -> Dict[str, str]:
        """Open dividend detailed view and return multiple metrics."""
        # Best-effort click to open details
        try:
            self.page.locator("div").filter(has_text=re.compile(r".*dividend yield\)Total dividends paid$")) .get_by_role("img").nth(1).click()
        except Exception:
            pass

        # Wait for detailed values
        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector("[class*='portfoliocard__onevalue']");
                return el && !el.innerText.includes('0.00')
            }""",
            timeout=60000,
        )

        def _safe_text(selector: str, index: int = 0) -> str:
            try:
                return self.page.locator(selector).nth(index).text_content() or ""
            except Exception:
                return ""

        last_quarter_total = _safe_text("[class='ant-row acc-value']", 0)
        last_quarter_yield = _safe_text("[class='ant-row acc-value']", 1)
        ytd_earnings = _safe_text("[class='ant-row net-value mb-8']", 0)
        all_time_earnings = _safe_text("[class='ant-row net-value mb-8']", 1)
        dividend_yield = _safe_text("[class='ant-row net-value mb-8']", 2)

        # Optionally click 'view all dividend'
        try:
            self.page.get_by_role("button", name="view all dividend").click()
        except Exception:
            pass

        return {
            "last_quarter_total": last_quarter_total,
            "last_quarter_yield": last_quarter_yield,
            "ytd_earnings": ytd_earnings,
            "all_time_earnings": all_time_earnings,
            "dividend_yield": dividend_yield,
        }

    def wallet_summary(self) -> Dict[str, str]:
        """Return wallet summary values."""
        sel = "[class*='portfoliocard__onevalue d-flex align-items-center']"
        self.page.wait_for_selector(sel, timeout=60000)
        total_wallet_balance = self.page.locator(sel).text_content() or ""
        return {"total_wallet_balance": total_wallet_balance}

    def wallet_details(self) -> Dict[str, str]:
        """Open wallet details modal and return balances."""
        # Click the wallet details icon (best-effort)
        try:
            self.page.locator("div:nth-child(3) > .portfoliocard__block > .portfoliocard__alltimevalue > .redirect > .icon-wrap > svg > path").click()
        except Exception:
            pass

        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector("[class*='ant-modal-body']");
                return el && !el.innerText.includes('0.00')
            }""",
            timeout=60000,
        )

        pending_withdrawals = self.page.locator("[class='ant-row acc-value']").nth(1).text_content() or ""
        available_wallet_balance = self.page.locator("[class='net-value-wrap']").nth(0).text_content() or ""
        total_wallet_balance = self.page.locator("[class='ant-row acc-value']").nth(0).text_content() or ""

        return {
            "total_wallet_balance": total_wallet_balance,
            "pending_withdrawals": pending_withdrawals,
            "available_wallet_balance": available_wallet_balance,
        }

    def bank_to_wallet_transfer(self, amount: str = "100") -> None:
        """Initiate a bank to wallet transfer of given amount."""
        self.page.get_by_text("Transfer", exact=True).click()
        self.page.get_by_role("combobox", name="Transfer from").click()
        # choose a bank
        self.page.get_by_text(re.compile(r"Chase|Bank of America|Wells Fargo")).click()
        self.page.get_by_role("combobox", name="Transfer to").click()
        self.page.get_by_text(re.compile(r"Realbricks Wallet \$")).nth(1).click()
        self.page.get_by_role("textbox", name="Enter amount").click()
        self.page.get_by_role("textbox", name="Amount").fill(amount)
        self.page.get_by_role("textbox", name="Date of transfer").click()
        # pick a date from calendar (best-effort)
        try:
            self.page.locator(".ant-picker").click()
            self.page.get_by_title("-06-02").locator("div").click()
        except Exception:
            pass

        self.page.get_by_role("button", name="Initiate Transfer").click()

        # Optionally wait for transfer confirmation elements
        try:
            self.page.get_by_text(f"Your transfer of ${amount} has").wait_for(state="visible", timeout=15000)
            # self.page.get_by_role("heading", name="Transfer completed").click()
            # self.page.get_by_role("button", name="Done").click()
        except Exception:
            # proceed even if confirmation not found
            pass

    def wallet_to_bank(self, amount: str = "100") -> None:
        self.page.wait_for_function(
            """
            ()=>{
                const el=document.querySelector("[class*='portfoliocard__onevalue d-flex align-items-center']");
                return el && !el.innerText.includes('0.00')
            }""",
            timeout=60000,
        )
        old_total_wallet_balance = self.page.locator("[class*='portfoliocard__onevalue d-flex align-items-center']").nth(0).text_content() or ""
        # return {"total_wallet_balance": total_wallet_balance}        """Initiate a bank to wallet transfer of given amount."""
        self.page.get_by_text("Transfer", exact=True).click()
        self.page.get_by_role("combobox", name="Transfer from").click()
        self.page.get_by_text(re.compile(r"Realbricks Wallet \$")).nth(0).click()

        self.page.get_by_role("combobox", name="Transfer to").click()
        time.sleep(4)
        self.page.get_by_text(re.compile(r"Chase|Bank of America|Wells Fargo")).nth(1).click()
        time.sleep(3)
        self.page.get_by_role("textbox", name="Enter amount").click()
        self.page.get_by_role("textbox", name="Amount").fill(amount)
        self.page.get_by_role("textbox", name="Date of transfer").click()
        # pick a date from calendar (best-effort)
        try:
            self.page.locator(".ant-picker").click()
            self.page.get_by_title("-06-02").locator("div").click()
        except Exception:
            pass

        self.page.get_by_role("button", name="Initiate Transfer").click()

        # Optionally wait for transfer confirmation elements
        try:
            self.page.get_by_text(f"Your transfer of ${amount} has").wait_for(state="visible", timeout=15000)
            # self.page.get_by_role("heading", name="Transfer completed").click()
            # self.page.get_by_role("button", name="Done").click()
        except Exception:
            # proceed even if confirmation not found
            pass
        time.sleep(2)
        self.page.get_by_role("button", name="Done").click()

        updated_total_wallet_balance = self.page.locator("[class*='portfoliocard__onevalue d-flex align-items-center']").nth(0).text_content() or ""
        return {"updated_total_wallet_balance":updated_total_wallet_balance,
                "old_total_wallet_balance":old_total_wallet_balance}

    page.get_by_role("heading", name="Transfer initiated").click()
    page.get_by_text("Transfer request created").click()
    page.get_by_text("Tuesday, June 02,").click()
    page.get_by_role("button", name="Done").click()
