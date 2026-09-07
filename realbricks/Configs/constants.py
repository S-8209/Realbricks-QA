# ── URLs ─────────────────────────────────────────────────────────────────────
BASE_URL            = "https://www.staging-fe.realbricks.com"
INITIAL_MARKETPLACE_URL ="https://www.staging-fe.realbricks.com/marketplace/initial"
SIGN_UP_URL         = f"{BASE_URL}/sign-up"
LOGIN_URL           = f"{BASE_URL}/login"
PORTFOLIO_URL       = f"{BASE_URL}/portfolio"
YOPMAIL_URL         = "https://yopmail.com/"
SUCCESS_SIGN_UP_URL = f"{BASE_URL}/sign-up/activation"
ONBOARDING_SUCCESS_URL = f"{BASE_URL}/sign-up/linkbank?utm_source=onboarding&utm_medium=web&utm_content=onboarding_complete"

# ── Timeouts (ms) ────────────────────────────────────────────────────────────
TIMEOUT_SHORT  = 15_000
TIMEOUT_MEDIUM = 30_000
TIMEOUT_LONG   = 60_000

# ── Defaults ─────────────────────────────────────────────────────────────────
DEFAULT_EMAIL =  "sm100@yopmail.com"
DEFAULT_PIN      = "0000"
DEFAULT_PASSWORD = "Test@123"
DEFAULT_AMOUNT   = "100"

# ── Users ────────────────────────────────────────────────────────────────────
QA_USER = {
    "email"   : "sagarv1@yopmail.com",
    "password": DEFAULT_PASSWORD,
    "pin"     : DEFAULT_PIN,
}

FORGET_PASSWORD_USER={
    "email"   : "jj@yopmail.com",
    "password": "Simform@1233",
    "pin"     : DEFAULT_PIN,
    
}

NEW_USER = {
    "email"   : "sen@yopmail.com",
    "password": DEFAULT_PASSWORD,
    "pin"     : DEFAULT_PIN,
}
B_T_USER={
    "email"   : "tyg@yopmail.com",
    "password": DEFAULT_PASSWORD,
    "pin"     : DEFAULT_PIN,
    
}
Insufficient_balance_user={
    "email"   : "niwugyzeb@yopmail.com",
    "password": DEFAULT_PASSWORD,
    "pin"     : DEFAULT_PIN,
    
}

# ── Banks ────────────────────────────────────────────────────────────────────
BANKS = ["Chase", "Bank of America", "Wells Fargo"]

# ── Share types ───────────────────────────────────────────────────────────────
SHARE_TYPE_MAX      = "max"
SHARE_TYPE_CUSTOM   = "custom"
SHARE_TYPE_POPULAR  = "popular"
SHARE_TYPE_SUGGESTED = "suggested"
BEST_ASK            = "lowest_ask"
BEST_BID            = "highest_bid" # ✅ fixed typo
LAST_PRICE          = "last_price"
ALL_SHARES          = "all"
INITIAL_SHARE_PRICE = 10
PLATFORM_FEE        = 2.5
SHARE_TYPE_EMPTY=""

share_options = [
    (SHARE_TYPE_CUSTOM,  1),    # custom amount
    (SHARE_TYPE_MAX,     None),     # max available
    (SHARE_TYPE_POPULAR, None), # popular amount
    (ALL_SHARES,None)
]




# ── Payment types ─────────────────────────────────────────────────────────────
PAYMENT_WALLET = "wallet"
PAYMENT_BANK   = "bank"

# ── Success messages ──────────────────────────────────────────────────────────
SUCCESS_TRANSFER_MESSAGE = "Transfer request created successfully. Your transaction will execute on Admin approval"
SUCCESS_INVESTOR_HEADING = "You're an investor!"
UPLOAD_ID ="/home/sagar/Downloads/test-document-upload-success.png"


TRANSACTION_TYPES = ["All", "Withdrawal", "Deposit", "IPO"]
TIME_PERIODS      = ["Last 7 days", "Last 30 days", "All time"]
SHARE_TYPES       = ["All", "IPO", "Secondary"]

# constants.py
TIME_PERIODS_7="Last 7 days"
TIME_PERIODS_30="Last 30 days"
TIME_PERIODS_ALL_TIME="All time"
# Transaction type filter options
TRANSACTION_TYPE_ALL           = "All"
TRANSACTION_TYPE_PRIMARY_BUY   = "Buy"
TRANSACTION_TYPE_SECONDARY_BUY = "Buy"
TRANSACTION_TYPE_SECONDARY_SELL= "Sell"
TRANSACTION_TYPE_DIVIDEND      = "Dividend"
TRANSACTION_TYPE_WITHDRAWAL    = "Withdrawal"
TRANSACTION_TYPE_DEPOSIT       = "Deposit"

# Share type filter options
SHARE_TYPE_FILTER_ALL       = "All"
SHARE_TYPE_FILTER_PRIMARY   = "Primary"
SHARE_TYPE_FILTER_SECONDARY = "Secondary"


# constants.py

# ── Transaction Status ──────────────────────
VALID_TRANSACTION_STATUSES = [
    "Completed",
    "Pending", 
    "Failed",
    "Cancelled"
]

# ── Transaction Trade Types ─────────────────
VALID_TRADE_TYPES = [
    "Buy - Primary Market (Initial Offering)",
    "Buy - Secondary Market",
    "Sell - Secondary Market",
    "Dividend",
    "Net Proceeds"
]
BALANCE_TRANSACTION_NO_DATA_MESSAGE = "No transactions found"
BALANCE_TRANSACTION_FILTER_NO_RESULTS_MESSAGE = "Applied filters have no transactions"