import pytest,time, re
import logging
from playwright.sync_api import Page, expect
from realbricks.Page.balance_transaction import balance_and_transaction
from realbricks.Page.payment_method_for_transactions import payments
from realbricks.Utils.utils import clean_value, values_match
from realbricks.Utils.feature_toggle import is_enabled
from realbricks.Configs.constants import (
    TRANSACTION_TYPE_PRIMARY_BUY,
    TRANSACTION_TYPE_SECONDARY_BUY,
    TRANSACTION_TYPE_SECONDARY_SELL,
    TRANSACTION_TYPE_DIVIDEND,
    TRANSACTION_TYPE_WITHDRAWAL,
    SHARE_TYPE_FILTER_SECONDARY,
    VALID_TRADE_TYPES,
    VALID_TRANSACTION_STATUSES
)

logger =logging.getLogger(__name__)

BALANCE_TRANSACTIONS_URL = "https://www.staging-fe.realbricks.com/account/transactions"

VALID_TRANSACTION_TYPES = [
    TRANSACTION_TYPE_PRIMARY_BUY,
    TRANSACTION_TYPE_SECONDARY_BUY,
    TRANSACTION_TYPE_SECONDARY_SELL,
    TRANSACTION_TYPE_DIVIDEND,
    TRANSACTION_TYPE_WITHDRAWAL,
    "Deposit",
    "IPO",
]

class TestBalanceTransaction:

    @pytest.mark.skipif(
        not is_enabled("wallet_payment"),reason="feature is ot enabled  "
    )
    def test_navigation(self, logged_in_page: Page):
        """Navigating to Balances & Transactions loads the page with valid, consistent balance data."""
        logger.info("TC - Validating Balances & Transactions navigation")
        balance_t = balance_and_transaction(logged_in_page)
        balance_t.navigation()

        assert logged_in_page.url.startswith(BALANCE_TRANSACTIONS_URL), \
            f"Unexpected URL after navigation: {logged_in_page.url}"

        data = balance_t.account_balances()
        total_account_value = clean_value(data["total_account_value"])
        shares_investments  = clean_value(data["shares_investments"])
        wallet_balance       = clean_value(data["wallet_balance"])

        logger.info(f"Total={total_account_value}, Shares={shares_investments}, Wallet={wallet_balance}")

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
        logger.info(f"Latest transaction: {data}")

        assert data["date"], "Transaction date is empty"
        assert data["type"] in VALID_TRANSACTION_TYPES, \
            f"Unexpected transaction type: {data['type']}"
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
        logger.info(f"Transaction count: {count}")
        assert count > 0, "Expected at least one transaction"

        groups = balance_t.get_status_groups()
        logger.info(f"Status groups: {groups}")
        assert groups, "Expected at least one status group header"
        assert all(g and g.strip() for g in groups), \
            f"Found empty status group header: {groups}"

        logger.info("TC - Transaction count and status groups validated successfully")

    def test_transaction_type_filter(self, user_for_every_transaction: Page):
        """Filtering by transaction type should only show matching rows."""
        logger.info("TC - Validating transaction type filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_WITHDRAWAL)
        user_for_every_transaction.wait_for_timeout(500)

        types = balance_t.get_all_transaction_types()
        logger.info(f"Transaction types after filter: {types}")

        assert types, f"Expected at least one '{TRANSACTION_TYPE_WITHDRAWAL}' transaction after filtering"
        assert all(t == TRANSACTION_TYPE_WITHDRAWAL for t in types), \
            f"Filter leaked unrelated types: {types}"

        logger.info("TC - Transaction type filter validated successfully")

    def test_time_period_filter(self, user_for_every_transaction: Page):
        """Filtering by time period should narrow the results, not expand them."""
        logger.info("TC - Validating time period filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        total_count = balance_t.get_transactions_count()

        balance_t.apply_time_period_filter("Last 7 days")
        user_for_every_transaction.wait_for_timeout(500)
        filtered_count = balance_t.get_transactions_count()

        logger.info(f"Total={total_count}, Last 7 days={filtered_count}")
        assert filtered_count <= total_count, \
            f"Filtered count ({filtered_count}) should not exceed total count ({total_count})"

        logger.info("TC - Time period filter validated successfully")

    def test_share_type_filter(self, user_for_every_transaction: Page):
        """Filtering by share type 'Secondary' should only show Secondary Buy/Sell transactions."""
        logger.info("TC - Validating share type filter")
        balance_t = balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()

        balance_t.apply_share_type_filter(SHARE_TYPE_FILTER_SECONDARY)
        user_for_every_transaction.wait_for_timeout(500)

        types = balance_t.get_all_transaction_types()
        logger.info(f"Transaction types after Secondary filter: {types}")

        valid_secondary_types = {TRANSACTION_TYPE_SECONDARY_BUY, TRANSACTION_TYPE_SECONDARY_SELL}
        assert types, "Expected at least one Secondary transaction after filtering"
        assert all(t in valid_secondary_types for t in types), \
            f"Filter leaked unrelated types: {types}"

        logger.info("TC - Share type filter validated successfully")
        
    def test_buy_transaction_values_validation(self,user_for_every_transaction):
        """Calculating the buy values on the buy order detailed pop up"""
        logger.info("TC - Validating share type filter")
        balance_t=balance_and_transaction(user_for_every_transaction)
        balance_t.navigation()
        balance_t.apply_transaction_type_filter(TRANSACTION_TYPE_PRIMARY_BUY)
        balance_t.get_detailed_transaction_pop_up_detail
        transaction_detail_data=balance_t.get_detailed_transaction_pop_up_detail()
        assert re.match(r"[a-f0-9-]{36}", transaction_detail_data["order_number"]), \
            f"Invalid order number format: {transaction_detail_data['order_number']}"
        assert transaction_detail_data["order_status"] in VALID_TRANSACTION_STATUSES,\
            f"Invalid Order status :{transaction_detail_data["order_status"]}"
        assert transaction_detail_data["trade_type"] in VALID_TRADE_TYPES,\
            f" In valid trade types :"{transaction_detail_data["trade_type"]}
        assert
        
        print(
            transaction_detail_data["order_number"], '\n',
            transaction_detail_data["initiated_on"], '\n',
            transaction_detail_data["order_status"], '\n',
            transaction_detail_data["trade_type"], '\n',
            transaction_detail_data["price_per_share"], '\n',
            transaction_detail_data["total_share_amount"], '\n',
            transaction_detail_data["transaction_fee"], '\n',
            transaction_detail_data["platform_fee"], '\n',
            transaction_detail_data["total_cost"]
        )        
    def test_debug_popup(self, logged_in_page: Page):
        balance_t = balance_and_transaction(logged_in_page)
        balance_t.navigation()
        
        # Debug — check what's found
        items = logged_in_page.locator(".trans-item").all()
        print(f"Transaction items found: {len(items)}")
        
        if len(items) > 0:
            first_row = logged_in_page.locator(".trans-item").first
            details = first_row.locator(".trans-item__details")
            print(f"Details found: {details.count()}")
            print(f"Details text: {details.text_content()}")
            
            # Try clicking
            details.click()
            logged_in_page.wait_for_timeout(2000)
            
            # Check if modal opened
            modal = logged_in_page.locator(".ant-modal-content")
            print(f"Modal visible: {modal.is_visible()}")
            
    # def test_navigation1(self, logged_in_page: Page):
    #     balance_t = balance_and_transaction(logged_in_page)
    #     balance_t.navigation()
        
    #     # Debug — print all combobox elements found
    #     combos = logged_in_page.get_by_roloption_texte("combobox").all()
    #     print(f"Total comboboxes found: {len(combos)}")
    #     for i, combo in enumerate(combos):
    #         print(f"Combobox {i}: {combo.get_attribute('id')} — {combo.text_content()}")