import re
import logging
from typing import Optional

from playwright.sync_api import Page
from realbricks.Page.base_page import BasePage

from realbricks.Configs.constants import (
    SIGN_UP_URL,
    LOGIN_URL,
    YOPMAIL_URL,
    DEFAULT_PIN,
    TIMEOUT_SHORT,
    TIMEOUT_MEDIUM,
    TIMEOUT_LONG,
    ONBOARDING_SUCCESS_URL,
    UPLOAD_ID
)

logger = logging.getLogger(__name__)


class SignUp(BasePage):
    """Page object for sign-up and onboarding flows."""

    def __init__(self, page: Page, user: Optional[dict] = None) -> None:
        super().__init__(page)
        self.user = user

        # Sign-up form locators
        self.loc_first_name     = page.get_by_role("textbox",  name="Legal First Name")
        self.loc_last_name      = page.get_by_role("textbox",  name="Legal Last Name")
        self.loc_email          = page.get_by_role("textbox",  name="Email")
        self.loc_phone          = page.get_by_role("textbox",  name="Phone Number")
        self.loc_password       = page.get_by_role("textbox",  name="Password")
        self.loc_checkbox_terms = page.get_by_role("checkbox", name="I have read and agree to the")
        self.loc_checkbox_ref   = page.get_by_role("checkbox", name="By checking this box, I")
        self.loc_button_sign_up = page.get_by_role("button",   name="Sign Up")
        self.loc_fw600          = page.locator("[class='fw-600']")

        # Validation messages
        self.loc_duplicate_email          = page.get_by_text("Email is already registered.")
        self.loc_invalid_email_message    = page.get_by_text("Enter a valid email address.")
        self.loc_invalid_password_message = page.get_by_text("Ensure your password is between 8 and 20 characters long, incorporating a mix of lowercase letters (a-z), uppercase letters (A-Z), numbers (0-9), and special characters (e.g., !#$%&()*+,-./:;<=>?@[]^`{|}~) for enhanced security.")
        self.loc_pin_setup_mismatch       = page.get_by_text("PIN does not match.")

        # Yopmail locators
        self.loc_yopmail_input = page.locator("//input[@id='login']")
        self.loc_yopmail_inbox = page.get_by_title("Check Inbox @yopmail.com")
        self.loc_ifmail_frame  = page.frame_locator("#ifmail")

    def sign_up(self) -> tuple:
        """Fill sign-up form. Returns (email, page)."""
        self.u = self.user
        self.safe_fill(self.loc_first_name, self.u["first_name"], "first_name")
        self.safe_fill(self.loc_last_name,  self.u["last_name"],  "last_name")
        self.safe_fill(self.loc_email,      self.u["email"],      "email")
        self.safe_fill(self.loc_phone,      self.u["number"],     "phone")
        self.safe_fill(self.loc_password,   self.u["password"],   "password")
        self.loc_checkbox_terms.check()
        logger.info("Checked terms checkbox")
        self.loc_checkbox_ref.check()
        logger.info("Checked marketing checkbox")
        logger.info(f"Sign-up form filled: {self.u['email']}")
        return self.u["email"], self.page

    def submit_sign_up(self, wait_for_confirmation: bool = True) -> None:
        """Click Sign Up button and wait for confirmation."""
        self.safe_click(self.loc_button_sign_up, "Sign Up button")
        if wait_for_confirmation:
            self.loc_fw600.wait_for(state="visible")
        logger.info(f"Sign-up submitted: {self.u['email']}")

    def resend_email_verification(self) -> str:
        """Capture verification email text and click resend."""
        v_email = self.loc_fw600.text_content()
        self.safe_click(
            self.page.get_by_role("button", name="Resend email"), "Resend email"
        )
        logger.info("Resend email clicked")
        return v_email

    def email_verification(self) -> Page:
        """Navigate to yopmail, click activation link — opens new tab as self.np."""
        logger.info("Starting email verification via yopmail")
        self.page.goto(YOPMAIL_URL)
        self.safe_fill(self.loc_yopmail_input, self.u["email"], "Yopmail input")
        self.safe_click(self.loc_yopmail_inbox, "Check Inbox")
        with self.page.context.expect_page() as new_tab_info:
            self.loc_ifmail_frame.get_by_text("Activate my account").click()
        self.np = new_tab_info.value
        self.np.wait_for_load_state()
        logger.info("Activation link opened in new tab")
        return self.np

    def pin_setup(self) -> None:
        """Set and confirm PIN on new tab."""
        self.fill_pin(self.np, self.u["pin"])
        self.safe_click(self.np.get_by_text("Save PIN"), "Save PIN")
        self.fill_pin(self.np, self.u["confirm_pin"])
        self.safe_click(self.np.get_by_text("Confirm"), "Confirm PIN")
        logger.info("PIN set and confirmed")

    def user_onboarding(self) -> None:
        """Complete US person, address, SSN/DOB steps on new tab."""
        # US person question
        self.np.get_by_role("radio", name="Yes").check()
        self.click_continue(self.np)
        logger.info("US person question answered")

        # Address
        self.np.get_by_role("textbox", name="Residential address").fill(self.u["residential_address"])
        self.np.get_by_role("textbox", name="City").fill(self.u["city"])
        self.select_dropdown_option_on(
            self.np,
            trigger_locator=self.np.locator(".ant-select-selector"),
            option_text=self.u.get("state", "Georgia"),
        )
        self.np.get_by_role("textbox", name="Zip code").fill(self.u["zip"])
        self.np.get_by_role("textbox", name="Zip code").press("Tab")
        self.click_continue(self.np)
        logger.info("Address step completed")

        # SSN + DOB
        self.np.get_by_role("textbox", name="Social security number").fill(self.u["ssn"])
        self.np.get_by_role("textbox", name="Month").fill(self.u["month"])
        self.np.get_by_role("textbox", name="Day").fill(self.u["day"])
        self.np.get_by_role("textbox", name="Year").fill(self.u["year"])
        self.click_continue(self.np)
        logger.info("SSN and DOB step completed")

    def id_upload(self) -> None:
        """Upload government ID on new tab."""
        self.np.locator("div.ant-select-in-form-item").click()
        self.np.locator("#identification-anchor").get_by_text("Passport", exact=True).click()
        self.np.locator('input[type="file"]').set_input_files(UPLOAD_ID)
        self.click_continue(self.np)
        logger.info("ID uploaded successfully")

    def Investment_range(self) -> None:
        """Complete investment range and Dwolla terms steps on new tab."""
        self.np.locator("[class='ant-radio']").nth(1).check()
        self.select_dropdown_option_on(
            self.np,
            trigger_locator=self.np.locator("div")
                .filter(has_text=re.compile(r"^State$"))
                .locator("span")
                .first,
            option_text=self.u.get("investment_state", "Alabama"),
        )
        self.np.get_by_role("checkbox", name="I agree to not invest more").check()
        self.click_continue(self.np)
        logger.info("Investment range step completed")

        # Dwolla terms
        self.np.locator("div").filter(
            has_text=re.compile(
                r"^I have read and agree to Dwolla's Privacy Policy and Terms and Conditions\.$"
            )
        ).get_by_label("").check()
        self.np.get_by_label("").nth(1).check()
        self.np.get_by_role("link", name="Confirm").click()
        logger.info("Dwolla terms accepted")

    def skip_add_bank(self) -> Page:
        """Skip add bank and navigate to home. Returns new tab page."""
        self.np.wait_for_url(ONBOARDING_SUCCESS_URL)
        self.np.locator("a").nth(1).click()
        self.np.wait_for_load_state("networkidle")
        self.np.locator("a.fw-600.back-link").click()
        logger.info("Onboarding complete — navigated to home")
        return self.np

    def add_bank_via_onbaording(self) -> None:
        """Click Connect bank during onboarding."""
        self.np.wait_for_url(ONBOARDING_SUCCESS_URL)
        self.np.locator("a").nth(1).click()
        self.np.wait_for_load_state("networkidle")
        self.np.get_by_role("button", name="Connect bank").click()
        logger.info("Connect bank clicked")
        
    
    