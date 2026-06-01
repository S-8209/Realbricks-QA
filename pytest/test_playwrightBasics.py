import time
from playwright.sync_api import Page
import random

random_num = random.randint(1, 2000)
email = f"sagar{random_num}@yopmail.com"

def test_sign_up(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.staging-fe.realbricks.com/sign-upAuth")
    page.get_by_text("Sign up With Email").click()

    page.locator("//input[@id='firstName']").fill("Jddfdfdohn")
    page.locator("//input[@id='lastName']").fill("Smith")
    page.locator("//input[@id='email']").fill(email)

    i1 = random.randint(1, 9)
    phone_num = f"2{i1}34{i1}533435"
    page.locator("//input[@id='phoneNumber']").fill(phone_num)
    page.locator("//input[@id='password']").fill("Test@123")

    # Agree to terms
    page.locator("label", has_text="I have read and agree to the Realbricks").locator(".ant-checkbox-input").click()

    page.get_by_text("Sign Up").click()
    print(email)
    wait_for_seconds = 5
    page.wait_for_timeout(wait_for_seconds * 1000)

    context.close()
    browser.close()


def test_verification(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
# def test_verification(playwright):
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()

    page.goto("https://yopmail.com/")
    page.locator("//input[@id='login']").fill(email)
    page.get_by_title("Check Inbox @yopmail.com").click()

    iframe_locator = page.frame_locator("#ifmail")

    # Clicking the activation link opens a new tab
    with context.expect_page() as new_tab_info:
        iframe_locator.get_by_text("Activate my account").click()

    new_tab: Page = new_tab_info.value
    new_tab.wait_for_load_state()

    # Enter PIN and confirm
    for i in range(4):
        new_tab.locator(f"//input[@id='SingleInput-{i}']").fill("0")
    new_tab.get_by_text("Save PIN").click()

    for i in range(4):
        new_tab.locator(f"//input[@id='SingleInput-{i}']").fill("0")
    new_tab.get_by_text("Confirm").click()

    new_tab.get_by_label("Yes").check()

    # Identification and document upload
    new_tab.locator("//input[@id='identification']").click()
    new_tab.get_by_title("Passport").click()
    time.sleep(5)
    new_tab.set_input_files("input#passport", "/home/sagar/Downloads/01e4d9e5-e664-4d50-b602-ad4fd0597870_de6fe34d_a8d91771.jpeg")
    new_tab.get_by_text("Continue ").click()
    

    # Address details
    new_tab.locator("//input[@id='address']").fill("222333 PEACHTREE PLACE")
    new_tab.locator("//input[@id='aptNumber']").fill("Testing")
    new_tab.locator("//input[@id='addressLine2']").fill("Atlanta")
    new_tab.locator("//input[@id='city']").fill("Atlanta")
    new_tab.locator("//input[@id='state']").click()
    new_tab.locator("//input[@id='zipCode']").click()
    time.sleep(15)
    context.close()
    browser.close()
    print(email)|{}    