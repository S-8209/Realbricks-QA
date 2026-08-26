import pytest
import logging
from playwright.sync_api import Page, expect
from realbricks.Page.add_bank_flow import Add_Bank_flow
from realbricks.test_data.sign_up_data import (
    User_with_existing_email,
    Id_upload_user,
    INVALID_SIGNUP_EMAILS,
    INVALID_SIGNUP_PASSWORDS,
    INVALID_SIGNUP_PHONES
)
from realbricks.Configs.constants import SIGN_UP_URL, SUCCESS_SIGN_UP_URL, INITIAL_MARKETPLACE_URL
from realbricks.Page.sign_up import SignUp

logger = logging.getLogger(__name__)


class TestSignUp:

    def test_sign_up(self, sign_up_page: Page, default_user):
        """TC01 - Valid user can sign up successfully."""
        logger.info("TC01 - Starting valid sign up test")
        try:
            sign = SignUp(sign_up_page, default_user)
            email, current_url = sign.sign_up()
            sign.submit_sign_up()
            logger.info(f"Sign up completed with email: {email}")
            assert email == default_user["email"], \
                f"Email mismatch! Expected: {default_user['email']} Got: {email}"
            expect(current_url).to_have_url(SUCCESS_SIGN_UP_URL)
        except Exception as e:
            logger.error(f"TC01 failed: {str(e)}")
            raise

    def test_resend_email(self, sign_up_page: Page, default_user):
        """TC02 - Verify Resend Email."""
        logger.info("TC02 - Resend Email Verification")
        try:
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            sign.submit_sign_up()
            v_email = sign.resend_email_verification()
            expect(sign_up_page.get_by_role("button", name="Resend email")).to_be_disabled(timeout=2000)
            logger.info("Email button disabled")
            expect(sign_up_page.locator("[class='auth__form__description']")).to_contain_text(
                "Check your inbox to activate your account. We sent an email to"
            )
            logger.info(f"Email sent to: {v_email}")
            assert v_email == default_user["email"]
        except Exception as e:
            logger.error(f"TC02 failed: {str(e)}")
            raise

    def test_sign_up_and_onboarding(self, sign_up_page: Page, default_user):
        """TC03 - Valid user can sign up and complete full onboarding."""
        logger.info("TC03 - Starting sign up + onboarding test")
        try:
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            sign.submit_sign_up()
            sign.email_verification()
            sign.pin_setup()
            sign.user_onboarding()
            sign.Investment_range()
            sign.skip_add_bank()
            expect(sign.np).to_have_url(INITIAL_MARKETPLACE_URL)
            logger.info("TC03 - Onboarding completed successfully")
        except Exception as e:
            logger.error(f"TC03 failed: {str(e)}")
            raise

    def test_sign_up_and_onboarding_with_add_bank(self, sign_up_page: Page, default_user):
        """TC04 - Valid user can sign up and complete full onboarding with bank."""
        logger.info("TC04 - Starting sign up + onboarding + add bank test")
        try:
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            sign.submit_sign_up()
            sign.email_verification()
            sign.pin_setup()
            sign.user_onboarding()
            sign.Investment_range()
            sign.add_bank_via_onbaording()
            add_bank = Add_Bank_flow(sign.np)
            add_bank.add_bank_flow()
            logger.info("TC04 - Onboarding with bank completed successfully")
        except Exception as e:
            logger.error(f"TC04 failed: {str(e)}")
            raise

    def test_existing_email(self, sign_up_page: Page):
        """TC05 - Sign up with existing email shows error."""
        logger.info("TC05 - Testing existing email sign up")
        try:
            sign = SignUp(sign_up_page, User_with_existing_email)
            sign.sign_up()
            sign.submit_sign_up()
            expect(sign.loc_duplicate_email).to_be_visible()
            logger.info(f"TC05 - Email already exists: {User_with_existing_email['email']}")
        except Exception as e:
            logger.error(f"TC05 failed: {str(e)}")
            raise

    @pytest.mark.parametrize("email", INVALID_SIGNUP_EMAILS)
    def test_invalid_email(self, sign_up_page: Page, default_user, email):
        """TC06 - Invalid email format shows error."""
        logger.info(f"TC06 - Testing invalid email: {email}")
        try:
            default_user["email"] = email
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            expect(sign.loc_invalid_email_message).to_be_visible()
            expect(sign.loc_button_sign_up).to_be_disabled()
            logger.info(f"TC06 - Email is invalid: {email}")
        except Exception as e:
            logger.error(f"TC06 failed for email {email}: {str(e)}")
            raise

    @pytest.mark.parametrize("password", INVALID_SIGNUP_PASSWORDS)
    def test_invalid_password(self, sign_up_page: Page, default_user, password):
        """TC07 - Invalid password shows error."""
        logger.info(f"TC07 - Testing invalid password: {password}")
        try:
            default_user["password"] = password
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            expect(sign.loc_invalid_password_message).to_be_visible()
            expect(sign.loc_button_sign_up).to_be_disabled()
            logger.info(f"TC07 - Password is invalid: {password}")
        except Exception as e:
            logger.error(f"TC07 failed for password {password}: {str(e)}")
            raise

    @pytest.mark.parametrize("number", INVALID_SIGNUP_PHONES)
    def test_invalid_phone_number(self, sign_up_page: Page, default_user, number):
        """TC08 - Invalid phone number disables sign up button."""
        logger.info(f"TC08 - Testing invalid phone: {number}")
        try:
            default_user["number"] = number
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            expect(sign.loc_button_sign_up).to_be_disabled()
            logger.info(f"TC08 - Phone is invalid: {number}")
        except Exception as e:
            logger.error(f"TC08 failed for phone {number}: {str(e)}")
            raise

    def test_pin_mismatch_on_confirm(self, sign_up_page: Page, default_user):
        """TC09 - PIN mismatch during onboarding shows error."""
        logger.info("TC09 - Testing PIN mismatch")
        try:
            default_user["confirm_pin"] = "1111"
            sign = SignUp(sign_up_page, default_user)
            sign.sign_up()
            sign.submit_sign_up()
            sign.email_verification()
            sign.pin_setup()
            expect(sign.loc_pin_setup_mismatch).to_be_visible()
            logger.info("TC09 - PIN mismatch error shown")
        except Exception as e:
            logger.error(f"TC09 failed: {str(e)}")
            raise

    def test_onboarding_with_upload_id(self, sign_up_page: Page):
        """TC10 - Valid user can complete onboarding with ID upload."""
        logger.info("TC10 - Starting onboarding with ID upload")
        try:
            sign = SignUp(sign_up_page, Id_upload_user)
            sign.sign_up()
            sign.submit_sign_up()
            sign.email_verification()
            sign.pin_setup()
            sign.user_onboarding()
            sign.id_upload()
            sign.Investment_range()
            sign.skip_add_bank()
            expect(sign.np).to_have_url(INITIAL_MARKETPLACE_URL)
            logger.info("TC10 - Onboarding with ID upload completed successfully")
        except Exception as e:
            logger.error(f"TC10 failed: {str(e)}")
            raise