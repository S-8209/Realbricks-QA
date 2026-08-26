# import pytest
# import logging
# from playwright.sync_api import Page, expect
# # from realbricks.test_data.buy_flow_data import secondary_flow_data_buy, secondary_flow_data_sell
# from realbricks.Page.secondary_market_flow import S_buy_flow , S_sell_flow
# from realbricks.Page.add_bank_flow import Add_Bank_flow
# logger = logging.getLogger(__name__)

# class TestBuyClass:
#     # @pytest.mark.parametrize("share_selection,price_selection,share_quantity,price_value", secondary_flow_data_buy)  # ✅    
#     def test_s_buy_flow(self, logged_in_page: Page, share_selection, price_selection, share_quantity, price_value):  # ✅
#         logger.info(
#             f"Starting buy flow | Share Type: {share_selection}, "
#             f"Price Type: {price_selection}, "
#             f"Share Value: {share_quantity}, "
#             f"Amount Value: {price_value}"
#         )
#         try:
#             Buy_flow=S_buy_flow(logged_in_page)
#             Buy_flow.create_buy_order(share_selection, price_selection, share_quantity, price_value)
#             logger.info("Buy order created successfully.")
#             expect(logged_in_page.get_by_text("You’ve made a buy order.")).to_be_visible()
#             expect(logged_in_page.get_by_text("You have successfully requested to buy {} shares ($10 each) of Test Property A. You will be notified through email about any progress made toward your buy order.")).not_to_be_visible()
#         except Exception as e:
#             logger.error(
#                 f"Buy flow failed for Share Type: {share_selection}, "
#                 f"Price Type: {price_selection}. Error: {str(e)}"
#             )
#             raise
#     # @pytest.mark.parametrize("share_selection,price_selection,share_quantity,price_value", secondary_flow_data_sell)
#     def test_sell_flow(self, logged_in_page: Page, share_selection, price_selection, share_quantity, price_value):
#         logger.info(
#             f"Starting sell flow | Share Selection: {share_selection}, "
#             f"Price Selection: {price_selection}, "
#             f"Share Quantity: {share_quantity}, "
#             f"Price Value: {price_value}"
#         )
#         try:
#             sell_flow = S_sell_flow(logged_in_page)
#             sell_flow.create_sell_order(share_selection, price_selection, share_quantity, price_value)
#             logger.info("Sell order created successfully.")
#         except Exception as e:
#             logger.error(
#                 f"Sell flow failed for Share Selection: {share_selection}, "
#                 f"Price Selection: {price_selection}. Error: {str(e)}"
#             )
#             raise