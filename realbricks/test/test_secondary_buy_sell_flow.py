import logging
from playwright.sync_api import Page, expect
from realbricks.Page.secondary_market_flow import S_buy_flow, S_sell_flow

logger = logging.getLogger(__name__)


class TestBuyClass:
    def test_s_buy_flow_custom_amount(self, logged_in_page: Page):
        """Smoke test: place a Secondary Market buy order with custom quantity and custom price."""
        share_selection, price_selection = "custom", "custom"
        share_quantity, price_value = "5", "10.00"

        logger.info(
            f"Starting buy flow | Share Type: {share_selection}, Price Type: {price_selection}, "
            f"Share Value: {share_quantity}, Amount Value: {price_value}"
        )
        try:
            buy_flow = S_buy_flow(logged_in_page)
            buy_flow.create_buy_order(share_selection, price_selection, share_quantity, price_value)
            logger.info("Buy order created successfully.")

            # TODO: confirm this is the exact real success message text before trusting this assertion.
            expect(logged_in_page.get_by_text("You've made a buy order.")).to_be_visible()

            # TODO: the original had a second assertion here asserting a DIFFERENT message is NOT visible:
            # "You have successfully requested to buy {} shares ($10 each) of Test Property A..."
            # This looks like either a leftover from an older UI version, or the wrong assertion direction.
            # Removed until confirmed — don't want to assert against text you haven't verified is correct
            # (or incorrect) in the current app.

        except Exception as e:
            logger.error(
                f"Buy flow failed for Share Type: {share_selection}, Price Type: {price_selection}. Error: {str(e)}"
            )
            raise

    def test_sell_flow_custom_amount(self, logged_in_page: Page):
        """Smoke test: place a Secondary Market sell order with custom quantity and custom price."""
        share_selection, price_selection = "custom", "custom"
        share_quantity, price_value = "5", "10.00"

        logger.info(
            f"Starting sell flow | Share Selection: {share_selection}, Price Selection: {price_selection}, "
            f"Share Quantity: {share_quantity}, Price Value: {price_value}"
        )
        try:
            sell_flow = S_sell_flow(logged_in_page)
            sell_flow.create_sell_order(share_selection, price_selection, share_quantity, price_value)
            logger.info("Sell order created successfully.")

            # TODO: no success-message assertion existed in the original sell test at all —
            # confirm the real success message text and add it here, same as buy.

        except Exception as e:
            logger.error(
                f"Sell flow failed for Share Selection: {share_selection}, Price Selection: {price_selection}. "
                f"Error: {str(e)}"
            )
            raise
        
        
# Secondary Property - RB Frame Investors
# sen@yopmail.com
# e2@yopmail.com
# dc22@yopmail.com
# tyg@yopmail.com
