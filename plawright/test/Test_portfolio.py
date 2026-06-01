import time
import pytest
from plawright.Page.Buy_Flow import Test_Home_Initial_Buy
from plawright.Utils.Utils import load_users
from plawright.Page.Login_FLow import login_User
from plawright.Page.Portofolio_Calc import Portfolio_Cal
from playwright.sync_api import expect

def clean_value(value):
    """Convert a currency string like '$1,234.56 (5%)' to float 1234.56"""
    return float(value.replace("$", "").replace(",", "").strip().split("(")[0])

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
    TAV = portfolio_validate.total_account_value_data()
    print(f"Total Account Value: {TAV}")
    assert TAV is not None and TAV != "", "Total Account Value should not be empty"

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
        data =portfolio_validate.dividend_summary()
        print(f"\nLast Dividend: {clean_value(data['last_dividend'])}")
        print(f"Total Dividend: {clean_value(data['total_dividend'])}")

def test_detailed_dividend(logged_in_page):
    Detailed_porfolio_validate=Portfolio_Cal(logged_in_page)
    Detailed_porfolio_validate.portfolio_navigation()
    data=Detailed_porfolio_validate.dividend_detailed()
    print(clean_value(data["Last_quarter_dividend_total"]))
    print(clean_value(data["Last_quarter_dividend_yeild"]))

    # print(clean_value(data[1]))


