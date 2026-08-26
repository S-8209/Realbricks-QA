import pytest
import logging
from playwright.sync_api import Page, expect
from realbricks.Page.initial_buy_flow import BuyFlow
from realbricks.Page.payment_method_for_transactions import payments
from realbricks.Utils.utils import clean_value, values_match
from realbricks.test_data.buy_flow_data import calculation_data
from realbricks.Configs.constants import (
    SHARE_TYPE_CUSTOM,
    SHARE_TYPE_MAX,
    SHARE_TYPE_EMPTY,
    SHARE_TYPE_POPULAR,
    PAYMENT_WALLET,
    PAYMENT_BANK,
    INITIAL_SHARE_PRICE,
    PLATFORM_FEE,
)

logger = logging.getLogger(__name__)


class TestBuyFlow:

    # ─────────────────────────────────────────
    # HAPPY PATH
    # ─────────────────────────────────────────

    @pytest.mark.run(order=1)
    def test_buy_custom_amount_wallet(self, logged_in_page: Page):
        """TC01 - Buy shares with custom amount using wallet — verify order appears in portfolio."""
        logger.info("TC01 - Buy custom amount with wallet")
        try:
            buy = BuyFlow(logged_in_page)
            pay = payments(logged_in_page)

            buy.buy_share()
            buy.share_selection(share_type=SHARE_TYPE_CUSTOM, amount="1")
            buy.click_preview_order()
            pay.pay_with_wallet()
            buy.accept_legal_terms()
            buy.verify_purchase_success()
            buy.order_creation_portfolio_page()

            logger.info("TC01 - Buy custom amount with wallet completed successfully")
        except Exception as e:
            logger.error(f"TC01 failed — Custom share amount with wallet: {str(e)}")
            raise

    @pytest.mark.run(order=2)
    def test_buy_custom_amount_bank(self, logged_in_page: Page):
        """TC02 - Buy shares with custom amount using bank."""
        logger.info("TC02 - Buy custom amount with bank")
        try:
            buy = BuyFlow(logged_in_page)
            pay = payments(logged_in_page)

            buy.buy_share()
            buy.share_selection(share_type=SHARE_TYPE_CUSTOM, amount="1")
            buy.click_preview_order()
            pay.pay_with_bank("pay with bank")
            buy.accept_legal_terms()
            buy.verify_purchase_success()

            logger.info("TC02 - Buy custom amount with bank completed successfully")
        except Exception as e:
            logger.error(f"TC02 failed — Custom share amount with bank: {str(e)}")
            raise

    # ─────────────────────────────────────────
    # CALCULATION VERIFICATION — PLACE ORDER SCREEN
    # ─────────────────────────────────────────

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("share_type,share_amount", calculation_data)
    def test_verify_create_order_calculations(self, logged_in_page: Page, share_type, share_amount):
        """TC03 - Verify total investment and total purchase on place order screen."""
        logger.info(f"TC03 - Verifying place order screen calculations | share_type={share_type} amount={share_amount}")
        try:
            buy = BuyFlow(logged_in_page)
            buy.buy_share()
            buy.share_selection(share_type, share_amount)

            # Expected values calculated from share amount
            expected_investment, expected_purchase, _ = buy.calculate_expected_values(share_amount)

            # Actual values from place order screen — captured in share_selection
            actual_investment = clean_value(buy.actual_total_investment_value)
            actual_purchase   = clean_value(buy.actual_total_purchase_value)

            assert values_match(actual_investment, expected_investment), \
                f"Total Investment mismatch! Expected: {expected_investment} Got: {actual_investment}"
            assert values_match(actual_purchase, expected_purchase), \
                f"Total Purchase mismatch! Expected: {expected_purchase} Got: {actual_purchase}"

            logger.info(
                f"TC03 - Place order calculations verified | "
                f"Investment={actual_investment} Purchase={actual_purchase}"
            )
        except Exception as e:
            logger.error(f"TC03 failed | share_type={share_type} amount={share_amount} Error: {str(e)}")
            raise

    # ─────────────────────────────────────────
    # CALCULATION VERIFICATION — PREVIEW ORDER SCREEN
    # ─────────────────────────────────────────

    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("share_type,share_amount", calculation_data)
    def test_verify_preview_order_calculations(self, logged_in_page: Page, share_type, share_amount):
        """TC04 - Verify all values on preview order screen."""
        logger.info(f"TC04 - Verifying preview order screen | share_type={share_type} amount={share_amount}")
        try:
            buy = BuyFlow(logged_in_page)
            buy.buy_share()
            buy.share_selection(share_type, share_amount)
            buy.click_preview_order()
            buy.capture_preview_values()  # explicitly capture preview screen values

            # Expected values
            expected_investment, expected_purchase, _ = buy.calculate_expected_values(share_amount)

            # Actual values from preview order screen
            actual_share_num        = clean_value(buy.actual_share_num)
            actual_price_per_share  = clean_value(buy.actual_price_per_share)
            actual_total_investment = clean_value(buy.actual_total_investment)
            actual_platform_fee     = clean_value(buy.actual_platform_fee)
            actual_total_purchase   = clean_value(buy.actual_total_purchase)

            assert values_match(actual_share_num, share_amount), \
                f"Share Amount mismatch! Expected: {share_amount} Got: {actual_share_num}"
            assert values_match(actual_price_per_share, INITIAL_SHARE_PRICE), \
                f"Price per share mismatch! Expected: {INITIAL_SHARE_PRICE} Got: {actual_price_per_share}"
            assert values_match(actual_total_investment, expected_investment), \
                f"Total Investment mismatch! Expected: {expected_investment} Got: {actual_total_investment}"
            assert values_match(actual_platform_fee, PLATFORM_FEE), \
                f"Platform Fee mismatch! Expected: {PLATFORM_FEE} Got: {actual_platform_fee}"
            assert values_match(actual_total_purchase, expected_purchase), \
                f"Total Purchase mismatch! Expected: {expected_purchase} Got: {actual_total_purchase}"

            logger.info(
                f"TC04 - Preview calculations verified | "
                f"Investment={actual_total_investment} Purchase={actual_total_purchase}"
            )
        except Exception as e:
            logger.error(f"TC04 failed | share_type={share_type} amount={share_amount} Error: {str(e)}")
            raise

    # ─────────────────────────────────────────
    # NEGATIVE CASES
    # ─────────────────────────────────────────

    @pytest.mark.run(order=5)
    def test_no_input_for_buy(self, logged_in_page: Page):
        """TC05 - Preview order button disabled when no share amount entered."""
        logger.info("TC05 - Verify preview order disabled for empty share input")
        try:
            buy = BuyFlow(logged_in_page)
            buy.buy_share()
            buy.share_selection(share_type=SHARE_TYPE_EMPTY, amount="")
            expect(buy.loc_preview_order).to_be_disabled()
            logger.info("TC05 - Preview order button disabled as expected")
        except Exception as e:
            logger.error(f"TC05 failed — Empty share input: {str(e)}")
            raise

    @pytest.mark.run(order=6)
    def test_buy_more_than_max(self, logged_in_page: Page):
        """TC06 - Preview order button disabled when shares exceed maximum allowed."""
        logger.info("TC06 - Verify preview order disabled when exceeding max shares")
        try:
            buy = BuyFlow(logged_in_page)
            buy.buy_share()

            # First get max value
            buy.share_selection(share_type=SHARE_TYPE_MAX)
            max_share     = buy.loc_share_custom.input_value()
            exceed_amount = str(int(max_share) + 1)  # exceed by 1

            # Now enter exceeded amount
            buy.share_selection(SHARE_TYPE_CUSTOM, amount=exceed_amount)
            expect(buy.loc_preview_order).to_be_disabled()

            logger.info(f"TC06 - Preview order disabled for exceeded amount: {exceed_amount}")
        except Exception as e:
            logger.error(f"TC06 failed — Exceed max shares: {str(e)}")
            raise
    def test_buy_zero_shares(self,logged_in_page: Page):
        "TC07 - Buy with 0 shares"
        logger.info("TC07 - 0 shares buy")
        buy=BuyFlow(logged_in_page)
        buy.buy_share()
        

    # ─────────────────────────────────────────
    # MAX SHARES — ALWAYS LAST
    # ─────────────────────────────────────────

    @pytest.mark.run(order=7)
    def test_buy_max_amount_wallet(self, logged_in_page: Page):
        """TC08 - Buy max shares using wallet — runs last to avoid disabling buy button."""
        logger.info("TC08 - Buy max amount with wallet")
        try:
            buy = BuyFlow(logged_in_page)
            pay = payments(logged_in_page)

            buy.buy_share()
            buy.share_selection(share_type=SHARE_TYPE_MAX)
            buy.click_preview_order()
            pay.pay_with_wallet()
            buy.accept_legal_terms()
            buy.verify_purchase_success()

            logger.info("TC07 - Buy max amount with wallet completed successfully")
        except Exception as e:
            logger.error(f"TC07 failed — Max share amount with wallet: {str(e)}")
            raise
        
    