# realbricks/test/test_portfolio.py

import logging
import re
import pytest
from playwright.sync_api import Page
from realbricks.test_data.portfolio_data import expected_open_order_headers
from realbricks.Page.portfolio_flow import Portfolio_Cal
from realbricks.Utils.utils import clean_value, current_date, values_match
from realbricks.Configs.constants import PLATFORM_FEE

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# ACCOUNT VALUE
# ─────────────────────────────────────────

def test_detailed_portfolio_account_value(logged_in_page: Page):
    """Validate NAV, All Time Gain and Total Account Value math."""
    logger.info("TC - Validating portfolio account value calculations")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()
    portfolio.total_account_value_detailed_data_pop_up()

    def get(label):
        return clean_value(portfolio.total_account_value_detailed_data(label))

    nav                    = get("Net Account Value(NAV)")
    wallet                 = get("Total Wallet balance")
    total_account_value    = get("Total Account Value*")
    all_time_contributions = get("All time contributions")
    realized_appreciation  = get("Realized share appreciation")
    unrealized_appreciation= get("Unrealized share appreciation")
    total_dividends        = get("Total dividends received")
    all_time_gain          = get("All time gain*")

    logger.info(f"NAV={nav}, Wallet={wallet}, Total={total_account_value}")
    logger.info(f"Contributions={all_time_contributions}, Realized={realized_appreciation}")
    logger.info(f"Unrealized={unrealized_appreciation}, Dividends={total_dividends}")
    logger.info(f"All Time Gain={all_time_gain}")

    expected_nav   = all_time_contributions + unrealized_appreciation
    expected_gain  = realized_appreciation + unrealized_appreciation + total_dividends
    expected_total = nav + wallet

    assert values_match(nav, expected_nav), \
        f"NAV mismatch: got {nav}, expected {expected_nav}"
    assert values_match(all_time_gain, expected_gain), \
        f"All time gain mismatch: got {all_time_gain}, expected {expected_gain}"
    assert values_match(total_account_value, expected_total), \
        f"Total Account Value mismatch: got {total_account_value}, expected {expected_total}"

    logger.info("TC - Account value calculations verified successfully")


# ─────────────────────────────────────────
# DIVIDEND
# ─────────────────────────────────────────

def test_dividend_summary(logged_in_page: Page):
    """Validate last and total dividend are non-negative."""
    logger.info("TC - Validating dividend summary")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()

    data           = portfolio.dividend_summary()
    last_dividend  = clean_value(data.get("last_dividend", ""))
    total_dividend = clean_value(data.get("total_dividend", ""))

    logger.info(f"Last Dividend={last_dividend}, Total Dividend={total_dividend}")

    assert last_dividend >= 0,  f"Last dividend is negative: {last_dividend}"
    assert total_dividend >= 0, f"Total dividend is negative: {total_dividend}"

    logger.info("TC - Dividend summary validated successfully")


def test_detailed_dividend(logged_in_page: Page):
    """Validate dividend detail values and URL navigation."""
    logger.info("TC - Validating detailed dividend data")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()

    data = portfolio.dividend_detailed()

    last_quarter_total = clean_value(data.get("last_quarter_total", ""))
    last_quarter_yield = clean_value(data.get("last_quarter_yield", ""))
    ytd_earnings       = clean_value(data.get("ytd_earnings", ""))
    all_time_earnings  = clean_value(data.get("all_time_earnings", ""))
    dividend_yield     = clean_value(data.get("dividend_yield", ""))

    logger.info(f"Last Quarter Total={last_quarter_total}, Yield={last_quarter_yield}")
    logger.info(f"YTD={ytd_earnings}, All Time={all_time_earnings}, Yield={dividend_yield}")

    assert logged_in_page.url.startswith(
        "https://www.staging-fe.realbricks.com/account/transactions"
    ), f"Unexpected URL: {logged_in_page.url}"

    logger.info("TC - Detailed dividend validated successfully")


# ─────────────────────────────────────────
# WALLET
# ─────────────────────────────────────────

def test_wallet_summary(logged_in_page: Page):
    """Validate wallet balance is non-negative."""
    logger.info("TC - Validating wallet summary")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()

    data                 = portfolio.wallet_summary()
    total_wallet_balance = clean_value(data.get("total_wallet_balance", ""))

    logger.info(f"Total Wallet Balance={total_wallet_balance}")

    assert total_wallet_balance >= 0, \
        f"Wallet balance should not be negative: {total_wallet_balance}"

    logger.info("TC - Wallet summary validated successfully")


def test_wallet_detailed(logged_in_page: Page):
    """Validate total = pending + available wallet balance."""
    logger.info("TC - Validating wallet detailed breakdown")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()

    data                     = portfolio.wallet_details()
    total_wallet_balance     = clean_value(data.get("total_wallet_balance", ""))
    pending_withdrawals      = clean_value(data.get("pending_withdrawals", ""))
    available_wallet_balance = clean_value(data.get("available_wallet_balance", ""))

    logger.info(f"Total={total_wallet_balance}, Pending={pending_withdrawals}, Available={available_wallet_balance}")

    expected_total = pending_withdrawals + available_wallet_balance
    assert values_match(total_wallet_balance, expected_total), \
        f"Wallet mismatch: {total_wallet_balance} != {expected_total}"

    logger.info("TC - Wallet detailed validated successfully")


# ─────────────────────────────────────────
# TRANSFERS
# ─────────────────────────────────────────

def test_bank_to_wallet_transfer(logged_in_page: Page):
    """Initiate bank to wallet transfer."""
    logger.info("TC - Initiating bank to wallet transfer")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()
    portfolio.bank_to_wallet_transfer()
    logger.info("TC - Bank to wallet transfer completed")


def test_wallet_to_bank_transfer(logged_in_page: Page):
    """Validate wallet to bank transfer — message, date, balance."""
    logger.info("TC - Validating wallet to bank transfer")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()

    data = portfolio.wallet_to_bank()

    success_message = data.get("success_message", "")
    transfer_date   = data.get("transfer_date", "")
    old_balance     = clean_value(data.get("old_total_wallet_balance", ""))
    updated_balance = clean_value(data.get("updated_total_wallet_balance", ""))

    logger.info(f"Message={success_message}")
    logger.info(f"Transfer Date={transfer_date}, Expected={current_date()}")
    logger.info(f"Old Balance={old_balance}, Updated Balance={updated_balance}")

    assert "Transfer request created successfully." in success_message, \
        f"Unexpected message: {success_message}"
    assert transfer_date == current_date(), \
        f"Date mismatch: got {transfer_date}, expected {current_date()}"
    assert updated_balance <= old_balance, \
        f"Balance should reduce after transfer: {updated_balance} >= {old_balance}"

    logger.info("TC - Wallet to bank transfer validated successfully")


# ─────────────────────────────────────────
# OPEN ORDERS
# ─────────────────────────────────────────

def test_open_orders_validation(logged_in_page: Page):
    """Validate open orders data integrity."""
    logger.info("TC - Validating open orders")
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()
    result = portfolio.open_order_validation()
    assert result, "Open order property name should not be empty"
    logger.info(f"TC - Open order property name: {result}")


def test_open_order_headers(logged_in_page: Page):
    """Verify open order table headers match expected headers."""
    logger.info("TC - Validating open order table headers")

    try:
        portfolio = Portfolio_Cal(logged_in_page)
        portfolio.portfolio_navigation()

        actual_headers = portfolio.open_order_headers_visible()

        assert actual_headers == expected_open_order_headers, (
            f"\nExpected: {expected_open_order_headers}"
            f"\nActual:   {actual_headers}"
        )
        assert len(actual_headers) == len(expected_open_order_headers)
        logger.info("TC - Open order headers validated successfully")

    except Exception as e:
        logger.error(f"Open order header validation failed: {str(e)}")
        raise

def test_1st_open_order_data(logged_in_page: Page):
    """
    TC - Verify calculations, field validity and popup cross-validation
    for the most recent open order.
    """
    logger.info("TC - Validating open order 1st row data")

    try:
        portfolio = Portfolio_Cal(logged_in_page)
        portfolio.portfolio_navigation()

        (
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
        ) = portfolio.open_orders_1st_data()

        # Extract table values
        property_name  = open_order_data[0]
        quantity       = clean_value(open_order_data[5])
        order_price    = clean_value(open_order_data[6])
        total_purchase = clean_value(open_order_data[4])
        order_type     = open_order_data[3]

        logger.info(f"Table data — Property: {property_name}, Type: {order_type}, Qty: {quantity}, Price: {order_price}")
        logger.info(f"Popup data — Name: {property_name_pop_up}, Status: {property_status_pop_up}, Type: {property_type_pop_up}")

        # ── Calculate expected values ──────────────────────────────────────
        total_investment = quantity * order_price
        if order_type == "IPO":
            expected_total_purchase    = total_investment + PLATFORM_FEE
            expected_platform_fee      = PLATFORM_FEE
        else:
            transaction_fee            = total_investment * 0.01
            expected_total_purchase    = total_investment + PLATFORM_FEE + transaction_fee
            expected_platform_fee      = PLATFORM_FEE

        # ── Table assertions ───────────────────────────────────────────────
        valid_category = ["Purchased", "Awarded"]
        assert open_order_data[1] in valid_category, \
            f"Invalid category: {open_order_data[1]}"

        valid_share_type = ["IPO", "Buy", "Sell"]
        assert order_type in valid_share_type, \
            f"Invalid type: {order_type}"

        funding_percentage = clean_value(open_order_data[8])
        assert 0 <= funding_percentage <= 100, \
            f"Invalid funding percentage: {open_order_data[8]}"

        assert values_match(total_purchase, expected_total_purchase), \
            f"Total Purchase mismatch! Expected: {expected_total_purchase} Got: {total_purchase}"

        # ── Popup field assertions ─────────────────────────────────────────
        # Property name not empty
        assert property_name_pop_up, \
            "Property name in popup is empty"

        # Status format — should contain "% funded" or "Completed"
        valid_statuses = ["funded", "Completed", "Cancelled"]
        assert any(s in property_status_pop_up for s in valid_statuses), \
            f"Invalid status format: {property_status_pop_up}"

        # Type is valid
        assert property_type_pop_up in valid_share_type, \
            f"Invalid type in popup: {property_type_pop_up}"

        # Category is valid
        assert property_category_pop_up in valid_category, \
            f"Invalid category in popup: {property_category_pop_up}"

        # Quantity is positive
        popup_quantity = clean_value(property_quantity_pop_up)
        assert popup_quantity > 0, \
            f"Quantity in popup should be positive: {property_quantity_pop_up}"

        # Price per share is positive
        popup_price = clean_value(property_price_per_share_pop_up)
        assert popup_price > 0, \
            f"Price per share in popup should be positive: {property_price_per_share_pop_up}"

        # Total Investment = Quantity × Price per Share
        popup_total_investment = clean_value(property_total_investment_pop_up)
        assert values_match(popup_total_investment, popup_quantity * popup_price), \
            f"Popup Total Investment mismatch! Expected: {popup_quantity * popup_price} Got: {popup_total_investment}"

        # Platform Fee matches constant
        popup_platform_fee = clean_value(property_platform_fee_pop_up)
        assert values_match(popup_platform_fee, expected_platform_fee), \
            f"Platform Fee mismatch! Expected: {expected_platform_fee} Got: {popup_platform_fee}"

        # Total Purchase = Total Investment + Platform Fee
        popup_total_purchase = clean_value(property_total_purchase_pop_up)
        assert values_match(popup_total_purchase, expected_total_purchase), \
            f"Popup Total Purchase mismatch! Expected: {expected_total_purchase} Got: {popup_total_purchase}"

        # ── Cross-validate table vs popup ──────────────────────────────────
        assert property_name == property_name_pop_up, \
            f"Property name mismatch — Table: {property_name} Popup: {property_name_pop_up}"

        assert order_type == property_type_pop_up, \
            f"Type mismatch — Table: {order_type} Popup: {property_type_pop_up}"

        assert open_order_data[1] == property_category_pop_up, \
            f"Category mismatch — Table: {open_order_data[1]} Popup: {property_category_pop_up}"

        assert values_match(quantity, popup_quantity), \
            f"Quantity mismatch — Table: {quantity} Popup: {popup_quantity}"

        assert values_match(order_price, popup_price), \
            f"Price per share mismatch — Table: {order_price} Popup: {popup_price}"

        assert values_match(total_purchase, popup_total_purchase), \
            f"Total Purchase mismatch — Table: {total_purchase} Popup: {popup_total_purchase}"

        logger.info("TC - Open order data and cross-validation completed successfully")

    except Exception as e:
        logger.error(f"Open order validation failed: {str(e)}")
        raise