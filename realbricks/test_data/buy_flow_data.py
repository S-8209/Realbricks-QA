from realbricks.Configs.constants import (
    SHARE_TYPE_MAX,
    SHARE_TYPE_CUSTOM,
    SHARE_TYPE_POPULAR,
    PAYMENT_WALLET,
    PAYMENT_BANK,
    ALL_SHARES
)

# ── Calculation test data ──────────────────────────────────────────────────────
# Format: (share_type, share_amount)
# Used for verifying order calculations on place order and preview order screens
calculation_data = [
    (SHARE_TYPE_CUSTOM, 1),    # minimum purchase
    (SHARE_TYPE_CUSTOM, 5),    # small amount
    (SHARE_TYPE_CUSTOM, 10),   # medium amount
    (SHARE_TYPE_CUSTOM, 50)
    ]
share_options2=[    
        (SHARE_TYPE_CUSTOM,  "0"),   # custom amount
 
]
# ── Share options ──────────────────────────────────────────────────────────────
# Format: (share_type, amount)
# amount is None for non-custom types
share_options = [
    (SHARE_TYPE_CUSTOM,  "5"),   # custom amount
    (SHARE_TYPE_MAX,     None),  # max available
    (SHARE_TYPE_POPULAR, None),  # popular amount
]

# ── Payment options ────────────────────────────────────────────────────────────
# Format: (payment_type, method_name)
bank_options = [
    (PAYMENT_WALLET, "Realbricks Wallet"),
    (PAYMENT_BANK,   "Chase"),
    (PAYMENT_BANK,   "Bank of America"),
    (PAYMENT_BANK,   "Wells Fargo"),
]

# ── Buy combinations ───────────────────────────────────────────────────────────
# Format: (share_type, share_amount, payment_type, payment_method)
buy_with_wallet = [
    (SHARE_TYPE_CUSTOM, "5",  PAYMENT_WALLET, "Realbricks Wallet"),
    (SHARE_TYPE_MAX,    None, PAYMENT_WALLET, "Realbricks Wallet"),
]

buy_with_bank = [
    (SHARE_TYPE_CUSTOM, "5", PAYMENT_BANK, "Chase"),
    (SHARE_TYPE_CUSTOM, "5", PAYMENT_BANK, "Bank of America"),
]