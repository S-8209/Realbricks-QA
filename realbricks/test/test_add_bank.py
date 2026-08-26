import pytest
from realbricks.Page.add_bank_flow import Add_Bank_flow
from playwright.sync_api import expect


def test_add_bank_flow(Newly_created_user):
    add_bank = Add_Bank_flow(Newly_created_user)
    add_bank.add_bank_navigation()
    add_bank.add_bank_flow()
    expect(Newly_created_user.get_by_text("Bank added successfully.")).to_be_visible()

def test_already_added_bank(logged_in_page):
    add_bank=Add_Bank_flow(logged_in_page)
    add_bank.add_bank_navigation()
    add_bank.add_bank_flow()
    expect(logged_in_page.get_by_text("Bank already exists.")).to_be_visible()
