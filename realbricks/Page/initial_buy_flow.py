import re
import logging
from typing import Optional

from playwright.sync_api import Page
from realbricks.Page.base_page import BasePage
from realbricks.Configs.constants import (
    TIMEOUT_SHORT,
    TIMEOUT_MEDIUM,
    SHARE_TYPE_MAX,
    SHARE_TYPE_CUSTOM,
    SHARE_TYPE_POPULAR,
    SHARE_TYPE_SUGGESTED,
    INITIAL_SHARE_PRICE,
    SHARE_TYPE_EMPTY,
    PLATFORM_FEE,
    PORTFOLIO_URL,
    share_options
)
from realbricks.Utils.utils import clean_value

logger = logging.getLogger(__name__)


class BuyFlow(BasePage):
    """Page object for initial offering buy flow."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # ── Market slider / Buy Now ────────────────────────────────────────────
        self.loc_buy_now_button = (
            page.locator("div.marketslider")
            .nth(0)
            .get_by_role("button", name="Buy Now")
            .nth(0)
        )

        # ── Share selection ────────────────────────────────────────────────────
        self.loc_share_max       = page.locator("span.ant-tag", has_text=re.compile(r"Max"))
        self.loc_share_custom    = page.locator("//input[@id='share']")
        self.loc_share_popular   = page.locator("span.ant-tag", has_text=re.compile(r"Popular"))
        self.loc_share_suggested = page.locator("span.ant-tag", has_text=re.compile(r"Suggested"))

        # ── Place order values ─────────────────────────────────────────────────
        self.loc_total_investment_amount  = page.locator("[class='basic-info__item']").nth(0)
        self.loc_total_purchase_amount    = page.locator("[class='basic-info__item__value fw-600']").nth(1)

        # ── Preview order values ───────────────────────────────────────────────
        self.loc_investment_details = page.locator("[class='d-flex flex-column g-16 fz-14 mb-16']")

        self.loc_share_num                      = self.loc_investment_details.locator("div").nth(0).locator("span").nth(1)
        self.loc_price_per_share                = self.loc_investment_details.locator("div").nth(1).locator("span").nth(1)
        self.loc_total_investment_amount_preview = self.loc_investment_details.locator("div").nth(2).locator("span.fw-600")
        self.loc_platform_fee                   = self.loc_investment_details.locator("div").nth(3).locator("span").nth(1)
        self.loc_total_purchase_amount_preview  = page.locator(
            "[class='d-flex flex-column g-16 fz-14 mt-16']"
        ).locator("span.fw-600")

        # ── Order actions ──────────────────────────────────────────────────────
        self.loc_preview_order = page.get_by_role("button", name="Preview order")
        self.loc_place_order   = page.get_by_role("button", name="Place order")
        self.loc_agree_terms   = page.get_by_role("button", name="Agree to terms")

        # ── Legal checkboxes ───────────────────────────────────────────────────
        self.loc_checkbox_legal        = page.locator("//input[@type='checkbox']")
        self.loc_checkbox_attest       = page.get_by_role(
            "checkbox", name=re.compile(r"I attest that I am")
        )
        self.loc_checkbox_subscription = page.get_by_role(
            "checkbox",
            name="I have read and understand the above Subscription Agreement.",
        )

        # ── Success ────────────────────────────────────────────────────────────
        self.loc_success_heading = page.locator("[class='success__title mb-16']")

        # ── Portfolio validation ───────────────────────────────────────────────
        self.portfolio_navigation = page.get_by_role("link", name="Portfolio.")
        self.open_order           = page.locator("[class='ant-table-row ant-table-row-level-0']").first

    # ── Public flows ───────────────────────────────────────────────────────────

    def click_buy_now(self) -> None:
        """Click Buy Now button on market slider."""
        self.safe_click(self.loc_buy_now_button, "Buy Now button")

    def buy_share(self, pin: str = "0000") -> None:
        """Click Buy Now and enter PIN."""
        logger.info("Starting buy share flow")
        self.click_buy_now()
        self.fill_pin(self.page, pin)
        logger.info("Buy share flow initiated")

    def share_selection(self, share_type: str, amount: Optional[int] = None) -> None:
        """
        Select share amount type.
        share_type: 'max' | 'custom' | 'popular' | 'suggested' | 'empty'
        amount: required only for 'custom' and 'empty'
        """
        logger.info(f"Selecting share type: {share_type} amount: {amount}")
        self.page.locator("[class='buy-content']").wait_for(state="visible")

        if share_type == SHARE_TYPE_MAX:
            self.safe_click(self.loc_share_max, "Max share")

        elif share_type == SHARE_TYPE_CUSTOM:
            if not amount:
                raise ValueError("Amount is required for custom share type")
            self.safe_fill(self.loc_share_custom, amount, "Custom share amount")

        elif share_type == SHARE_TYPE_POPULAR:
            self.safe_click(self.loc_share_popular, "Popular share")

        elif share_type == SHARE_TYPE_SUGGESTED:
            self.safe_click(self.loc_share_suggested, "Suggested share")

        elif share_type == SHARE_TYPE_EMPTY:
            self.safe_fill(self.loc_share_custom, "", "Empty share amount")

        else:
            raise ValueError(f"Invalid share_type: {share_type}")

        logger.info(f"Share selection done: {share_type}")

        # Capture place order screen values after selection
        self.actual_total_investment_value = self.loc_total_investment_amount.text_content()
        self.actual_total_purchase_value   = self.loc_total_purchase_amount.text_content()

    def click_preview_order(self) -> None:
        """Click Preview Order button."""
        self.safe_click(self.loc_preview_order, "Preview order button")

    def capture_preview_values(self) -> None:
        """Capture all values shown on preview order screen."""
        logger.info("Capturing preview order values")
        self.actual_share_num        = self.loc_share_num.text_content()
        self.actual_price_per_share  = self.loc_price_per_share.text_content()
        self.actual_total_investment = self.loc_total_investment_amount_preview.text_content()
        self.actual_platform_fee     = self.loc_platform_fee.text_content()
        self.actual_total_purchase   = self.loc_total_purchase_amount_preview.text_content()
        logger.info(
            f"Preview values captured — "
            f"shares={self.actual_share_num} "
            f"price={self.actual_price_per_share} "
            f"investment={self.actual_total_investment} "
            f"fee={self.actual_platform_fee} "
            f"total={self.actual_total_purchase}"
        )

    def accept_legal_terms(self) -> None:
        """Check all legal checkboxes and place order."""
        logger.info("Accepting legal terms")

        self.loc_checkbox_legal.check()
        logger.info("Checked legal checkbox")

        self.safe_click(self.loc_place_order, "Place order button")

        self.loc_checkbox_attest.check()
        logger.info("Checked attest checkbox")

        self.loc_checkbox_subscription.check()
        logger.info("Checked subscription checkbox")

        self.safe_click(self.loc_agree_terms, "Agree to terms button")
        logger.info("Legal terms accepted successfully")

    def verify_purchase_success(self) -> None:
        """Verify the investor success heading is visible."""
        logger.info("Verifying purchase success")
        self.loc_success_heading.wait_for(state="visible", timeout=TIMEOUT_MEDIUM)
        logger.info("Purchase verified — You're an investor!")

    def calculate_expected_values(self, share_amount: int) -> tuple:
        """
        Calculate expected order values based on share amount.
        Returns (total_investment, total_purchase, share_amount)
        """
        total_investment = share_amount * INITIAL_SHARE_PRICE
        platform_fee     = PLATFORM_FEE
        total_purchase   = total_investment + platform_fee
        logger.info(
            f"Expected values — "
            f"investment={total_investment} "
            f"fee={platform_fee} "
            f"total={total_purchase}"
        )
        return total_investment, total_purchase, share_amount

    def order_creation_portfolio_page(self) -> list:
        """Navigate to portfolio and return first open order details."""
        self.page.goto(PORTFOLIO_URL)
        content = self.open_order.all_text_contents()
        self.page.locator(".fw-600.text-copper.cursor-pointer").nth(0).click()
        logger.info(f"Portfolio order content: {content}")
        return content