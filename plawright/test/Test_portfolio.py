import time
import re
import pytest
from plawright.Page.Buy_Flow import Test_Home_Initial_Buy
from plawright.Utils.Utils import load_users
from plawright.Page.Login_FLow import login_User
from plawright.Page.Portofolio_Calc import Portfolio_Cal
from playwright.sync_api import expect


def clean_value(value: str) -> float:
    """Convert a currency string like '$1,234.56 (5%)' to float 1234.56"""
    if not value:
        return 0.0
    return float(re.sub(r"[a-zA-Z$%*\-,]", "", value).strip().split("(")[0])


@pytest.mark.parametrize("user", load_users("Initial_Buy_with_Wallet_Balance"))
def test_initial_open_order(page, user):
    login = login_User(page)
    buy_now = Test_Home_Initial_Buy(page, user)
    portfolio_validate = Portfolio_Cal(page)

    login.Open()
    login.Login(user["email"], user["password"])
    login.OTP(user["pin"])

    buy_now.buy_now()
    buy_now.pin(user["pin"])
    buy_now.share_amount()
    buy_now.preview_order()
    buy_now.pay_with_bank()
    buy_now.accept_legal_terms()

    portfolio_validate.portfolio_data()


@pytest.mark.parametrize("user", load_users("Initial_Buy_with_Wallet_Balance"))
def test_existing_initial_open_order(page, user):
    login = login_User(page)
    portfolio_validate = Portfolio_Cal(page)

    login.Open()
    login.Login(user["email"], user["password"])
    login.OTP(user["pin"])

    portfolio_validate.portfolio_data()


@pytest.mark.parametrize("user", load_users("Initial_Buy_with_Wallet_Balance"))
def test_portfolio_empty_state(page, user):
    login = login_User(page)
    portfolio_validate = Portfolio_Cal(page)

    login.Open()
    login.Login(user["email"], user["password"])
    login.OTP(user["pin"])

    portfolio_validate.portfolio_navigation()
    portfolio_validate.portfolio_data()


def test_portfolio_account_value_data(page):
    login = login_User(page)
    portfolio_validate = Portfolio_Cal(page)

    login.Open()
    login.Login("sagar1595@yopmail.com", "Test@123")
    login.OTP("0000")

    portfolio_validate.portfolio_navigation()
    time.sleep(8)

    tav = portfolio_validate.total_account_value_data()
    print(f"Total Account Value: {tav}")
    assert tav is not None and tav != "", "Total Account Value should not be empty"


def test_detailed_portfolio_account_value(logged_in_page):
    portfolio_validate = Portfolio_Cal(logged_in_page)
    portfolio_validate.portfolio_navigation()
    portfolio_validate.total_account_value_detailed_data_pop_up()

    nav = clean_value(portfolio_validate.total_account_value_detailed_data("Net Account Value(NAV)"))
    wallet = clean_value(portfolio_validate.total_account_value_detailed_data("Total Wallet balance"))
    total_account_value = clean_value(portfolio_validate.total_account_value_detailed_data("Total Account Value*"))
    all_time_contributions = clean_value(portfolio_validate.total_account_value_detailed_data("All time contributions"))
    realized_share_appreciation = clean_value(portfolio_validate.total_account_value_detailed_data("Realized share appreciation"))
    unrealized_share_appreciation = clean_value(portfolio_validate.total_account_value_detailed_data("Unrealized share appreciation"))
    total_dividends_received = clean_value(portfolio_validate.total_account_value_detailed_data("Total dividends received"))
    all_time_gain = clean_value(portfolio_validate.total_account_value_detailed_data("All time gain*"))

    expected_nav = all_time_contributions + unrealized_share_appreciation
    assert round(nav, 2) == round(expected_nav, 2), f"NAV mismatch: {nav} != {expected_nav}"

    expected_all_time_gain = realized_share_appreciation + unrealized_share_appreciation + total_dividends_received
    assert round(all_time_gain, 2) == round(expected_all_time_gain, 2), f"All time gain mismatch: {all_time_gain} != {expected_all_time_gain}"

    expected_total_account_value = nav + wallet
    assert round(total_account_value, 2) == round(expected_total_account_value, 2), f"Total Account Value mismatch: {total_account_value} != {expected_total_account_value}"


def test_dividend_data(logged_in_page):
    portfolio_validate = Portfolio_Cal(logged_in_page)
    portfolio_validate.portfolio_navigation()

    data = portfolio_validate.dividend_summary()
    last = clean_value(data.get("last_dividend", ""))
    total = clean_value(data.get("total_dividend", ""))

    print(f"\nLast Dividend: {last}")
    print(f"Total Dividend: {total}")

    # Basic sanity checks
    assert last >= 0
    assert total >= 0


def test_detailed_dividend(logged_in_page):
    portfolio = Portfolio_Cal(logged_in_page)
    portfolio.portfolio_navigation()
    data = portfolio.dividend_detailed()

    # Use keys returned by Portfolio_Cal.dividend_detailed()
    last_quarter_total = clean_value(data.get("last_quarter_total", ""))
    last_quarter_yield = clean_value(data.get("last_quarter_yield", ""))
    ytd_earnings = clean_value(data.get("ytd_earnings", ""))
    all_time_earnings = clean_value(data.get("all_time_earnings", ""))
    dividend_yield = clean_value(data.get("dividend_yield", ""))

    print(f"Last quarter dividend total: {last_quarter_total}")
    print(f"Last quarter dividend yield: {last_quarter_yield}")
    print(f"Year-to-date dividend earnings: {ytd_earnings}")
    print(f"All-time dividend earnings: {all_time_earnings}")
    print(f"Dividend yield: {dividend_yield}")

    # Verify that the page navigated to transactions for dividends (best-effort)
    assert logged_in_page.url.startswith('https://www.staging-fe.realbricks.com/account/transactions')


def test_wallet_summary(logged_in_page):
    wallet_validate=Portfolio_Cal(logged_in_page)
    wallet_validate.portfolio_navigation()
    data=wallet_validate.wallet_summary()
    total_wallet_balance=clean_value(data.get("total_wallet_balance",""))
    print(f"total_wallet_balance:{total_wallet_balance}")
    
def test_wallet_detailed(logged_in_page):
    wallet_detail=Portfolio_Cal(logged_in_page)
    wallet_detail.portfolio_navigation()
    data=wallet_detail.wallet_details()
    total_wallet_balance=clean_value(data.get("total_wallet_balance",""))
    pending_withdrawals=clean_value(data.get("pending_withdrawals",""))
    available_wallet_balance=clean_value(data.get("available_wallet_balance",""))

    
    
    assert total_wallet_balance==pending_withdrawals+available_wallet_balance
    
    # print(data)
def test_bank_to_wallet_transfer(logged_in_page):
    wallet_transfer=Portfolio_Cal(logged_in_page)
    wallet_transfer.portfolio_navigation()
    wallet_transfer.bank_to_wallet_transfer()
        
def test_wallet_to_bank_transfer(logged_in_page):
    bank_transfer=Portfolio_Cal(logged_in_page)
    bank_transfer.portfolio_navigation()
    data=bank_transfer.wallet_to_bank()
    updated_total_wallet_balance=clean_value(data.get("updated_total_wallet_balance",""))
    old_total_wallet_balance=clean_value(data.get("old_total_wallet_balance",""))
    assert updated_total_wallet_balance<old_total_wallet_balance
    
