import pytest
from plawright.Page.Add_Bank_Flow import Add_Bank_flow
from playwright.sync_api import expect


def test_add_bank_flow(logged_in_page):
    add_bank = Add_Bank_flow(logged_in_page)
    add_bank.add_bank_flow()
    expect(logged_in_page.get_by_text("Link a bank account to potentially receive dividends and purchase shares.")).to_be_visible()
    expect(logged_in_page.get_by_text("Purchase shares and transfer funds from Realbricks directly to your bank.")).to_be_visible()
    expect(logged_in_page.get_by_text("Bank already exists.")).to_be_visible()