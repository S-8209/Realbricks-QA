import logging
from playwright.sync_api import Page
from realbricks.Configs.constants import (
    TIMEOUT_SHORT,
    TIMEOUT_MEDIUM,
    SHARE_TYPE_MAX,
    SHARE_TYPE_CUSTOM,
    SHARE_TYPE_POPULAR,
    SHARE_TYPE_SUGGESTED,
    DEFAULT_PIN,
)

logger = logging.getLogger(__name__)


class BasePage:
    """Shared helpers and locators common to BOTH buy and sell flows.
    Buy-only and sell-only locators live in their own subclass __init__ —
    keeping them here caused a real bug (duplicate names silently overwrote each other)."""

    def __init__(self, page: Page):
        self.page = page
        self.preview_order = page.get_by_role("button", name="Preview order")
        self.check_Box = page.locator("[class='ant-checkbox-input']")
        self.place_order_button = page.get_by_role("button", name="Place order")

    def wait_for_visible(self, selector: str, timeout: int = TIMEOUT_MEDIUM) -> None:
        logger.debug(f"Waiting for visible: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def safe_click(self, locator, description) -> None:
        try:
            locator.wait_for(state="visible", timeout=TIMEOUT_MEDIUM)
            locator.click()
            logger.info(f"Clicked: {description}")
        except Exception as e:
            logger.error(f"Click failed [{description}]: {e}")
            raise

    def safe_fill(self, locator, value: str, description: str = "") -> None:
        try:
            locator.wait_for(state="visible", timeout=TIMEOUT_SHORT)
            locator.fill(value)
            logger.info(f"Filled [{description}]: {value}")
        except Exception as e:
            logger.error(f"Fill failed [{description}]: {e}")
            raise

    def _fill_pin_on(self, target_page: Page, pin: str = DEFAULT_PIN, description: str = "filling PIN") -> None:
        """Fill 4-digit PIN. Shared by buy and sell — was duplicated in both before."""
        logger.info("Filling PIN")
        for i, ch in enumerate(pin):
            target_page.locator(f"//input[@id='SingleInput-{i}']").fill(ch)
        logger.info(f"Clicked: {description}")


class S_buy_flow(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # TODO: "Bridgeport," is hardcoded to one specific property — confirm this is intentional
        # for now, or whether this needs to become a parameter for testing other properties.
        self.buy_click = page.get_by_role("list").filter(has_text="Bridgeport,").get_by_role("button")
        self.custom_share_amount = page.locator("#share")
        self.share_price = page.get_by_role("textbox", name="$")
        self.max_shares_amount = page.get_by_text("Max (9.8%):")
        self.best_ask = page.get_by_text("Best ask: $")
        self.last_price = page.get_by_text("Last price: $")

    def create_buy_order(self, share_selection, price_selection, share_quantity, price_value) -> None:
        logger.info(
            f"Creating buy order | share_selection={share_selection}, price_selection={price_selection}, "
            f"share_quantity={share_quantity}, price_value={price_value}"
        )
        self.safe_click(self.buy_click, "clicking buy button")
        self._fill_pin_on(self.page, DEFAULT_PIN, "filling PIN")

        if share_selection == "custom":
            self.safe_fill(self.custom_share_amount, share_quantity, "filling share amount")
        elif share_selection == "max":
            self.safe_click(self.max_shares_amount, "Max button for share amount")

        if price_selection == "custom":
            self.safe_fill(self.share_price, price_value, "filling share price")
        elif price_selection == "best_ask":
            self.safe_click(self.best_ask, "Best ask i.e Lowest price")
        elif price_selection == "last_traded_price":
            self.safe_click(self.last_price, "last trade price")

        self.safe_click(self.preview_order, "clicking preview order")
        self.safe_click(self.check_Box, "checking terms checkbox")
        self.safe_click(self.place_order_button, "clicking place order button")
        logger.info("Buy order flow completed")


class S_sell_flow(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.portfolio_navigation = page.get_by_role("link", name="Portfolio")
        self.trade_button = page.locator(".ant-table-cell", has_text="Trade").first
        self.sell_flow = page.locator(".trade-tab-label", has_text="Sell")
        self.custom_share_amount = page.locator("#share").nth(1)
        self.custom_ask_price = page.locator("#limit").nth(1)
        self.all_share_button = page.get_by_text("All:")
        self.best_bid_button = page.get_by_text("Best bid: $")
        self.last_price_button = page.get_by_label("Sell").get_by_text("Last price: $")

    def create_sell_order(self, share_selection, price_selection, share_quantity, price_value) -> None:
        logger.info(
            f"Creating sell order | share_selection={share_selection}, price_selection={price_selection}, "
            f"share_quantity={share_quantity}, price_value={price_value}"
        )
        self.safe_click(self.portfolio_navigation, "Navigate to portfolio")
        self.safe_click(self.trade_button, "Click trade button on property row")
        self._fill_pin_on(self.page, DEFAULT_PIN, "filling PIN")
        self.safe_click(self.sell_flow, "Click sell tab")

        if share_selection == "custom":
            self.safe_fill(self.custom_share_amount, share_quantity, "Enter custom share quantity")
        elif share_selection == "all":
            self.safe_click(self.all_share_button, "Click all shares button")

        if price_selection == "custom":
            self.safe_fill(self.custom_ask_price, price_value, "Enter custom ask price")
        elif price_selection == "last_traded_price":
            self.safe_click(self.last_price_button, "Click last traded price button")
        elif price_selection == "best_bid":
            self.safe_click(self.best_bid_button, "Click best bid button")

        self.safe_click(self.preview_order, "Click preview order button")
        self.safe_click(self.check_Box, "Check terms and conditions")
        self.safe_click(self.place_order_button, "Click place order button")
        logger.info("Sell order flow completed")