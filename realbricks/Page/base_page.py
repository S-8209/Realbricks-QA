import logging, re
from playwright.sync_api import Page
from realbricks.Configs.constants import TIMEOUT_LONG , DEFAULT_PIN, TIMEOUT_MEDIUM
logger=logging.getLogger(__name__)

class BasePage:
    def __init__(self,page:Page)->None:
        self.page=page
        self.loc_hover_account_menu=page.locator(".accountnav__actions__item").last

    def safe_click(self,locator,description:str):
        try:
            locator.wait_for(state="visible",timeout=TIMEOUT_LONG)
            locator.click()
            logger.info(f"Clicked: {description}")
        except Exception as e:
            logger.info(f"Click failed [{description}]: {e}")
            raise
    def safe_fill(self,locator,value: str|float,description: str):
        try:
            locator.wait_for(state="visible",timeout=TIMEOUT_LONG)
            locator.fill(str(value))
            logger.info(f"Filled value[{description}]")
        except Exception as e:
            logger.info(f"Fill failed [{description}]: {e}")
            raise
    
    def fill_pin(self,page: Page,pin:str=DEFAULT_PIN)->None:
        for i, ch in enumerate(pin):
            page.locator(f"//input[@id='SingleInput-{i}']").fill(ch)
    # def fill_pin(self,pin:str):
    #         self.page.locator(f"//input[@id='SingleInput-{pin}']").fill()
            
    def click_continue(self, page: Page) -> None:
        """Wait for Continue button to be enabled, then click it."""
        locator = page.get_by_role("button", name="Continue")
        page.locator("button[type='submit']:not([disabled])").wait_for(
            state="visible", timeout=TIMEOUT_LONG
        )
        locator.click()
        logger.info("Clicked: Continue")
        
    
    def select_dropdown_option(self, trigger_locator, option_text: str) -> None:
        """
        Click an Ant Design dropdown trigger, then scroll until
        the matching option is visible and click it.
        """
        trigger_locator.click()
        # Wait for dropdown list to appear
        self.page.wait_for_selector(
            ".ant-select-item-option-content", state="visible", timeout=TIMEOUT_MEDIUM
        )
        virtual_list = self.page.locator(".rc-virtual-list-holder")
        option = self.page.locator(".ant-select-item-option-content", has_text=option_text)

        for _ in range(10):
            if option.count() > 0 and option.first.is_visible():
                option.first.click()
                logger.info(f"Selected dropdown option: {option_text}")
                return
            virtual_list.evaluate("el => el.scrollTop += 300")
            self.page.wait_for_timeout(300)

        raise Exception(f"Dropdown option '{option_text}' not found after scrolling")

    def select_dropdown_option_on(self, page: Page, trigger_locator, option_text: str) -> None:
        """
        Same as select_dropdown_option but operates on a specific page instance
        (e.g. a new tab).
        """
        trigger_locator.click()
        page.wait_for_selector(
            ".ant-select-item-option-content", state="visible", timeout=TIMEOUT_MEDIUM
        )
        virtual_list = page.locator(".rc-virtual-list-holder")
        option = page.locator(".ant-select-item-option-content", has_text=option_text)

        for _ in range(10):
            if option.count() > 0 and option.first.is_visible():
                option.first.click()
                logger.info(f"Selected dropdown option: {option_text}")
                return
            virtual_list.evaluate("el => el.scrollTop += 300")
            page.wait_for_timeout(300)

        raise Exception(f"Dropdown option '{option_text}' not found after scrolling")
    
    
    def select_dropdown_option_on(self, page: Page, trigger_locator, option_text: str) -> None:
        """
        Same as select_dropdown_option but operates on a specific page instance
        (e.g. a new tab).
        """
        trigger_locator.click()
        page.wait_for_selector(
            ".ant-select-item-option-content", state="visible", timeout=TIMEOUT_MEDIUM
        )
        virtual_list = page.locator(".rc-virtual-list-holder")
        option = page.locator(".ant-select-item-option-content", has_text=option_text)

        for _ in range(10):
            if option.count() > 0 and option.first.is_visible():
                option.first.click()
                logger.info(f"Selected dropdown option: {option_text}")
                return
            virtual_list.evaluate("el => el.scrollTop += 300")
            page.wait_for_timeout(300)

        raise Exception(f"Dropdown option '{option_text}' not found after scrolling")

    def select_dropdown_option(self, trigger_locator, option_text: str) -> None:
        """
        Click an Ant Design dropdown trigger, then scroll until
        the matching option is visible and click it.
        """
        trigger_locator.click()
        # Wait for dropdown list to appear
        self.page.wait_for_selector(
            ".ant-select-item-option-content", state="visible", timeout=TIMEOUT_MEDIUM
        )
        virtual_list = self.page.locator(".rc-virtual-list-holder")
        option = self.page.locator(".ant-select-item-option-content", has_text=option_text)

        for _ in range(10):
            if option.count() > 0 and option.first.is_visible():
                option.first.click()
                logger.info(f"Selected dropdown option: {option_text}")
                return
            virtual_list.evaluate("el => el.scrollTop += 300")
            self.page.wait_for_timeout(300)
            
    def navigate_to(self,menu_item:str):
        """Navigate to any page via profile dropdown menu."""
        logger.info(f"Navigating to: {menu_item}")
        self.loc_hover_account_menu.hover()
        self.page.get_by_role("link", name=menu_item).click()
        