import pytest, re,time
import logging
from datetime import datetime
from playwright.sync_api import Page, expect
from realbricks.Page.balance_transaction import balance_and_transaction
from realbricks.Utils.utils import clean_value, values_match
from realbricks.Utils.feature_toggle import is_enabled
from realbricks.Configs.constants import (
    TRANSACTION_TYPE_PRIMARY_BUY,
    TRANSACTION_TYPE_SECONDARY_BUY,
    TRANSACTION_TYPE_SECONDARY_SELL,
    TRANSACTION_TYPE_DIVIDEND,
    TRANSACTION_TYPE_WITHDRAWAL,
    TRANSACTION_TYPE_DEPOSIT,
    SHARE_TYPE_FILTER_SECONDARY,
    SHARE_TYPE_FILTER_PRIMARY,
    VALID_TRADE_TYPES,
    VALID_TRANSACTION_STATUSES,
    BALANCE_TRANSACTION_FILTER_NO_RESULTS_MESSAGE,
)

logger = logging.getLogger(__name__)

BALANCE_TRANSACTIONS_URL = "https://www.staging-fe.realbricks.com/account/transactions"

VALID_TRANSACTION_TYPES = [
    TRANSACTION_TYPE_PRIMARY_BUY,
    TRANSACTION_TYPE_SECONDARY_BUY,
    TRANSACTION_TYPE_SECONDARY_SELL,
    TRANSACTION_TYPE_DIVIDEND,
    TRANSACTION_TYPE_DEPOSIT,
    TRANSACTION_TYPE_WITHDRAWAL,
    "IPO",
    "Buy (Primary)",
]


class TestBalanceTransaction:

    # ── Shared helper — used by every popup-based test below ──────
    def _validate_common_transaction_fields(self, data: dict) -> tuple:
        assert re.match(r"[a-f0-9-]{36}", data["order_number"]), \
            f"Invalid order number format: {data['order_number']}"
        assert data["order_status"] in VALID_TRANSACTION_STATUSES, \
            f"Invalid order status: {data['order_status']}"

        trade_type = data["trade_type"].strip()
        assert trade_type in VALID_TRADE_TYPES, f"Invalid trade type: {trade_type}"

        price_per_share = clean_value(data["price_per_share"])
        assert price_per_share > 0, f"Negative price per share: {data['price_per_share']}"

        return trade_type, price_per_share

    @pytest.mark.skipif(not is_enabled("wallet_payment"), reason="feature is not enabled")
    def test_navigation(self, logged_in_page: Page):
        """Navigating to Balances & Transactions loads the page with valid, consistent balance data."""
        logger.info("TC - Validating Balances & Transactions navigation")
        balance_t = balance_and_transaction(logged_in_page)
        balance_t.navigation()

        assert logged_in_page.url.startswith(BALANCE_TRANSACTIONS_URL), \
            f"Unexpected URL after navigation: {logged_in_page.url}"

        data = balance_t.account_balances()
        total_account_value = clean_value(data["total_account_value"])
        shares_investments = clean_value(data["shares_investments"])
        wallet_balance = clean_value(data["wallet_balance"])

        assert total_account_value >= 0, f"Total account value is negative: {total_account_value}"
        assert shares_investments >= 0, f"Shares & investments value is negative: {shares_investments}"
        assert wallet_balance >= 0, f"Wallet balance is negative: {wallet_balance}"

        expected_total = shares_investments + wallet_balance
        assert values_match(total_account_value, expected_total), \
            f"Total account value mismatch: got {total_account_value}, expected {expected_total}"

        logger.info("TC - Balances & Transactions navigation validated successfully")

    def test_transaction(self, logged_in_page: Page):
        """Validate the latest transaction row has well-formed data."""
        logger.info("TC - Validating latest transaction data")
        balance_t = balance_and_transaction(logged_in_page)
        balance_t.navigation()

        data = balance_t.get_latest_transaction()
        assert data["date"], "Transaction date is empty"
        assert data["type"] in VALID_TRANSACTION_TYPES, f"Unexpected transaction type: {data['type']}"
        assert data["details"], "Transaction details is empty"

        amount = clean_value(data["amount"])
        assert amount != 0, f"Transaction amount should not be zero: {data['amount']}"

        logger.info("TC - Latest transaction data validated successfully")

    def test_transaction_count_and_status_groups(self, user_for_every_transaction: Page):
        """Validate the transaction list has entries grouped under status headers."""
        logger.info("TC - Validating transaction count and status groups")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        count = balance_t.get_transactions_count()
        assert count > 0, "Expected at least one transaction"

        groups = balance_t.get_status_groups()
        assert groups, "Expected at least one status group header"
        assert all(g and g.strip() for g in groups), f"Found empty status group header: {groups}"

        logger.info("TC - Transaction count and status groups validated successfully")

    def test_transaction_type_filter(self, user_for_every_transaction: Page):
        """Filtering by transaction type should only show matching rows."""
        logger.info("TC - Validating transaction type filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_WITHDRAWAL)
        user_for_every_transaction.wait_for_load_state("networkidle")

        types = balance_t.get_all_transaction_types()
        assert types, f"Expected at least one '{TRANSACTION_TYPE_WITHDRAWAL}' transaction after filtering"
        assert all(t == TRANSACTION_TYPE_WITHDRAWAL for t in types), f"Filter leaked unrelated types: {types}"

        logger.info("TC - Transaction type filter validated successfully")

    def test_time_period_filter(self, user_for_every_transaction: Page):
        """Filtering by time period should narrow the results, not expand them."""
        logger.info("TC - Validating time period filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        total_count = balance_t.get_transactions_count()
        balance_t.apply_time_period_filter("Last 30 days")
        user_for_every_transaction.wait_for_load_state("networkidle")
        filtered_count = balance_t.get_transactions_count()

        assert filtered_count <= total_count, \
            f"Filtered count ({filtered_count}) should not exceed total count ({total_count})"

        logger.info("TC - Time period filter validated successfully")

    def test_share_type_filter(self, user_for_every_transaction: Page):
        """Filtering by share type 'Secondary' should only show Secondary Buy/Sell transactions."""
        logger.info("TC - Validating share type filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_SECONDARY)
        user_for_every_transaction.wait_for_load_state("networkidle")

        types = balance_t.get_all_transaction_types()
        valid_secondary_types = {TRANSACTION_TYPE_SECONDARY_BUY, TRANSACTION_TYPE_SECONDARY_SELL}
        assert types, "Expected at least one Secondary transaction after filtering"
        assert all(t in valid_secondary_types for t in types), f"Filter leaked unrelated types: {types}"

        logger.info("TC - Share type filter validated successfully")

    def test_primary_buy_transaction_values_validation(self, user_for_every_transaction):
        """Primary Buy: no transaction_fee field, platform_fee should be $0."""
        logger.info("TC - Validating Primary Buy transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_PRIMARY)
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_PRIMARY_BUY)

        data = balance_t.get_detailed_transaction_pop_up_detail()
        trade_type, price_per_share = self._validate_common_transaction_fields(data)

        platform_fee = clean_value(data["platform_fee"])
        assert platform_fee == 0.00 or platform_fee == 2.50 , f"Primary Market should have $0 platform fee, got {platform_fee}"

        total_share_amount = clean_value(data["total_share_amount"])
        expected_total = total_share_amount + platform_fee
        assert values_match(clean_value(data["total_cost"]), expected_total), \
            f"Total cost mismatch: got {data['total_cost']}, expected {expected_total}"

        logger.info("TC - Primary Buy transaction popup validated successfully")

    def test_secondary_buy_transaction_values_validation(self, user_for_every_transaction):
        """Secondary Buy: platform_fee $2.50 flat + transaction_fee as 1% of share value."""
        logger.info("TC - Validating Secondary Buy transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_SECONDARY)
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_SECONDARY_BUY)

        data = balance_t.get_detailed_transaction_pop_up_detail()
        trade_type, price_per_share = self._validate_common_transaction_fields(data)

        platform_fee = clean_value(data["platform_fee"])
        assert platform_fee == 2.5, f"Expected $2.50 platform fee, got {platform_fee}"

        total_share_amount = clean_value(data["total_share_amount"])
        transaction_fee = clean_value(data["transaction_fee"])
        expected_transaction_fee = total_share_amount * 0.01
        assert values_match(transaction_fee, expected_transaction_fee), \
            f"Transaction fee should be 1% of share value: expected {expected_transaction_fee}, got {transaction_fee}"

        expected_total = total_share_amount + transaction_fee + platform_fee
        assert values_match(clean_value(data["total_cost"]), expected_total), \
            f"Total cost mismatch: got {data['total_cost']},   {expected_total}"

        # assert values_match(clean_value(data["total_amount"]),clean_value(data["total_share_amount"])),\
        #     f"Total amount mismatch in the list and pop up values got list value : {data["total_amount"]},pop up value {data["total_share_amount"]}"
        # logger.info("TC - Secondary Buy transaction popup validated successfully")

    def test_secondary_sell_transaction_values_validation(self, user_for_every_transaction):
        """Secondary Sell: proceeds = share value minus fees (opposite direction from Buy)."""
        logger.info("TC - Validating Secondary Sell transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_SECONDARY)
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_SECONDARY_SELL)

        data = balance_t.get_detailed_transaction_pop_up_detail()
        trade_type, price_per_share = self._validate_common_transaction_fields(data)

        platform_fee = clean_value(data["platform_fee"])
        assert platform_fee == 2.5, f"Expected $2.50 platform fee, got {platform_fee}"

        total_share_amount = clean_value(data["total_share_amount"])
        transaction_fee = clean_value(data["transaction_fee"])
        expected_transaction_fee = total_share_amount * 0.01
        assert values_match(transaction_fee, expected_transaction_fee), \
            f"Transaction fee should be 1% of share value: expected {expected_transaction_fee}, got {transaction_fee}"

        expected_proceeds = total_share_amount - transaction_fee - platform_fee
        assert values_match(clean_value(data["total_cost"]), expected_proceeds), \
            f"Proceeds mismatch: got {data['total_cost']}, expected {expected_proceeds}"

        logger.info("TC - Secondary Sell transaction popup validated successfully")

    def test_dividend_transaction_values_validation(self, user_for_every_transaction):
        """Validate the dividend transaction detail popup values and calculation."""
        logger.info("TC - Validating dividend transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_DIVIDEND)
        data = balance_t.get_dividend_transaction_popup_detail()

        assert re.match(r"[a-f0-9-]{36}", data["order_number"]), f"Invalid order number format: {data['order_number']}"
        assert data["order_status"] in VALID_TRANSACTION_STATUSES, f"Invalid order status: {data['order_status']}"
        assert data["initiated_on"], "Initiated date is empty"

        share_number = clean_value(data["share_number"])
        assert share_number > 0, f"Share count should be positive, got {share_number}"

        dividend_per_share = clean_value(data["dividend_per_share"])
        assert dividend_per_share > 0, f"Dividend per share should be positive, got {dividend_per_share}"

        total_dividend_received = clean_value(data["total_dividend_received"])
        assert total_dividend_received > 0, f"Total dividend should be positive, got {total_dividend_received}"

        expected_total_dividend = share_number * dividend_per_share
        assert values_match(total_dividend_received, expected_total_dividend), \
            f"Total dividend mismatch: got {total_dividend_received}, expected {expected_total_dividend}"

        payout_date = data["dividend_pay_date"]
        assert payout_date, "Payout date is empty"
        try:
            datetime.strptime(payout_date.strip(), "%m/%d/%Y")
        except ValueError:
            pytest.fail(f"Payout date is not in expected MM/DD/YYYY format: {payout_date}")

        logger.info("TC - Dividend transaction popup validated successfully")

    def test_withdrawal_transaction_values_validation(self, user_for_every_transaction):
        """Validate the withdrawal transaction detail popup values."""
        logger.info("TC - Validating withdrawal transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_WITHDRAWAL)
        data = balance_t.get_withdrawal_transaction_popup_detail()

        assert re.match(r"[a-f0-9-]{36}", data["order_number"]), f"Invalid order number format: {data['order_number']}"
        assert data["order_status"] in VALID_TRANSACTION_STATUSES, f"Invalid order status: {data['order_status']}"
        assert data["initiated_on"], "Initiated date is empty"
        assert data["transaction_type"] == "Withdrawal", f"Expected 'Withdrawal', got: {data['transaction_type']}"

        amount = clean_value(data["amount"])
        assert amount > 0, f"Withdrawal amount should be positive, got {amount}"

        logger.info("TC - Withdrawal transaction popup validated successfully")

    def test_deposit_transaction_values_validation(self, user_for_every_transaction):
        """Validate the deposit transaction detail popup values."""
        logger.info("TC - Validating deposit transaction popup")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_DEPOSIT)
        data = balance_t.get_deposit_transaction_popup_detail()

        assert re.match(r"[a-f0-9-]{36}", data["order_number"]), f"Invalid order number format: {data['order_number']}"
        assert data["order_status"] in VALID_TRANSACTION_STATUSES, f"Invalid order status: {data['order_status']}"
        assert data["initiated_on"], "Initiated date is empty"
        assert data["transaction_type"] == "Deposit", f"Expected 'Deposit', got: {data['transaction_type']}"

        amount = clean_value(data["amount"])
        assert amount > 0, f"Deposit amount should be positive, got {amount}"

        logger.info("TC - Deposit transaction popup validated successfully")

    def test_filter_with_no_matching_results_shows_empty_state(self, user_for_every_transaction):
        """Validate the case with no matching results."""
        logger.info("TC - Validating case with no matching results")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_PRIMARY)
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_SECONDARY_SELL)

        messages = balance_t.get_no_data_message()
        actual_message = messages["filter_no_result_message"]

        assert actual_message.strip() == BALANCE_TRANSACTION_FILTER_NO_RESULTS_MESSAGE, \
            f"Expected filter empty-state message, got: {actual_message}"

        logger.info("TC - Empty-state message validated successfully")
        
    def test_combined_filters_all_apply_simultaneously(self, user_for_every_transaction):
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_SECONDARY)
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_SECONDARY_BUY)        
        user_for_every_transaction.wait_for_load_state("networkidle")
        types = balance_t.get_all_transaction_types()
        assert all(t == TRANSACTION_TYPE_SECONDARY_BUY for t in types), \
            "One filter overrode or ignored another"
    
    def test_no_duplicate_order_numbers_in_list(self, user_for_every_transaction):
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t._load_all_transactions()
        # would need a get_all_order_numbers() method added to the page object
        order_numbers = balance_t.get_all_order_numbers()
        assert len(order_numbers) == len(set(order_numbers)), "Duplicate order numbers found in list"   
        
    def test_transaction_list_matches_popup_detail(self, user_for_every_transaction):
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_WITHDRAWAL)

        latest = balance_t.get_latest_transaction()
        row_amount = clean_value(latest["amount"])

        popup = balance_t.get_withdrawal_transaction_popup_detail()
        popup_amount = clean_value(popup["amount"])

        assert values_match(row_amount, popup_amount), \
            f"List shows {row_amount}, popup shows {popup_amount} for the same transaction"
    
    def test_transaction_list_matches_popup_detail(self, user_for_every_transaction):
        """The amount shown on the list row should match the total cost shown in its detail popup."""
        logger.info("TC - Validating list row amount matches popup detail")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_SECONDARY_BUY)
        user_for_every_transaction.wait_for_load_state("networkidle") 
        amounts = balance_t.get_row_and_popup_amount()
        row_amount = abs(clean_value(amounts["row_amount"]))
        
        
        popup_amount = abs(clean_value(amounts["popup_amount"]))

        assert values_match(row_amount, popup_amount), \
            f"List row shows {row_amount}, popup shows {popup_amount} for the same transaction"

        logger.info("TC - List row and popup amount cross-check validated successfully")