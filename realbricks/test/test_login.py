import pytest, logging
from playwright.sync_api import Page
from realbricks.Page.login_flow import login_User
from realbricks.Configs.constants import  QA_USER
from realbricks.test_data.login_data import INVALID_EMAILS ,INVALID_PINS,INVALID_PASSWORDS
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

class TestLogin:
    def test_login(self, logged_in_page: Page):
        logger.info("TC01 - Starting valid login test")
        try:
            expect(logged_in_page.locator("//h2[normalize-space()='The Realbricks Marketplace']")).to_be_visible()            
            logger.info("TC01 - Login successful")
        except Exception as e:
            logger.error(f"TC01 - Login failed: {str(e)}")
            raise

    @pytest.mark.parametrize("email,password",INVALID_PASSWORDS)
    def test_invalid_password_login(self, login_page, email, password):
        logger.info(f"TC02 - Testing invalid password for: {email}")
        try:
            invalid_user = {**QA_USER, "email": email, "password": password}
            login = login_User(login_page, invalid_user)
            login.Open()
            login.Login()
            login.login_button()
            expect(login.creds).to_be_visible()
            logger.info(f"TC02 - Error message visible for: {email}")
        except Exception as e:
            logger.error(f"TC02 - Test failed for {email}: {str(e)}")
            raise

    @pytest.mark.parametrize("email,password,pin",INVALID_PINS)
    def test_invalid_pin(self, login_page, email, password, pin):
        logger.info(f"TC03 - Testing invalid PIN: {pin} for: {email}")
        try:
            invalid_user = {**QA_USER, "email": email, "password": password, "pin": pin}
            login = login_User(login_page, invalid_user)
            login.Open()
            login.Login()
            login.login_button()
            login.OTP()
            expect(login_page.locator("//div[@role='alert']", has_text="Please enter a valid pin.")).to_be_visible()
            logger.info(f"TC03 - Invalid PIN error visible for: {email}")
        except Exception as e:
            logger.error(f"TC03 - Test failed for {email}: {str(e)}")
            raise

    @pytest.mark.parametrize("email", INVALID_EMAILS)
    def test_invalid_email(self, page, email):
        logger.info(f"TC04 - Testing invalid email: {email}")
        try:
            invalid_user = {**QA_USER, "email": email}
            login = login_User(page, invalid_user)
            login.Open()
            login.Login()
            login.login_button()
            expect(page.locator("//div[@role='alert']", has_text="email must be an email")).to_be_visible()
            logger.info(f"TC04 - Invalid email error visible for: {email}")
        except Exception as e:
            logger.error(f"TC04 - Test failed for {email}: {str(e)}")
            raise
        
    
    def test_empty_email_login(self, page):
        logger.info("TC05 - Testing empty email login")
        try:
            invalid_user = {**QA_USER, "email": "", "password": ""}
            login = login_User(page, invalid_user)
            login.Open()
            login.Login()
            expect(page.get_by_role("button", name="Log in")).to_be_disabled()
            logger.info("TC05 - Login button disabled for empty email")
        except Exception as e:
            logger.error(f"TC05 - Test failed: {str(e)}")
            raise

    def test_empty_password_login(self, page):
        logger.info("TC06 - Testing empty password login")
        try:
            invalid_user = {**QA_USER, "email": "sm100@yopmail.com", "password": "", "pin": "1111"}
            login = login_User(page, invalid_user)
            login.Open()
            login.Login()
            expect(page.get_by_role("button", name="Log in")).to_be_disabled()
            logger.info("TC06 - Login button disabled for empty password")
        except Exception as e:
            logger.error(f"TC06 - Test failed: {str(e)}")
            raise