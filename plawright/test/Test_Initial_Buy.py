import time
import pytest
from plawright.Page.Buy_Flow import Test_Home_Initial_Buy
from playwright.sync_api import Playwright, sync_playwright, expect
from plawright.Test_data.Buy_flow_data import share_options ,bank_options
from plawright.Page.Payment_method import payments

@pytest.mark.parametrize("share_type, amount",share_options)
@pytest.mark.parametrize("payment_type,method",bank_options)
def test_buy_now_Custom_amount(logged_in_page,share_type,amount,payment_type,method):
    initial_shares_buying = Test_Home_Initial_Buy(logged_in_page)
    payment=payments(logged_in_page)
    initial_shares_buying.buy_share()
    initial_shares_buying.share_selection(share_type=share_type,amount=amount)
    # payment.continue_payment()
    # The code snippet you provided is a test case written in Python using the pytest framework for
    # testing a buy flow process on a website. Let me break down the important parts of the code for
    # you:
    # The code snippet you provided is a test case written in Python using the pytest framework for
    # testing a buy flow process on a website. Let's break down the test case:
    # The code snippet you provided is a test case written in Python using the pytest framework for
    # testing a buy flow process on a website. Let me break down the important parts of the code for
    # you:
    payment.payment_multiple_option(payment_type=payment_type,method=method)
    initial_shares_buying.accept_legal_terms()
    expect(logged_in_page.get_by_role("heading", name="You’re an investor!")).to_be_visible()

# def test_buy_now_Bank(logged_in_page):
#     initial_shares_buying = Test_Home_Initial_Buy(logged_in_page)
#     initial_shares_buying.buy_share(custom_amount=True)
#     initial_shares_buying.pay_with_bank()
#     initial_shares_buying.accept_legal_terms()
#     expect(logged_in_page.get_by_role("heading", name="You’re an investor!")).to_be_visible()
    
# def test_buy_now_Max(logged_in_page):
#     initial_shares_buying = Test_Home_Initial_Buy(logged_in_page)
#     initial_shares_buying.buy_share(max_share=True)
#     initial_shares_buying.pay_with_wallet()
#     initial_shares_buying.accept_legal_terms()
#     expect(logged_in_page.get_by_role("heading", name="You’re an investor!")).to_be_visible()
