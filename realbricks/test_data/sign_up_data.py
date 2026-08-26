from realbricks.Utils.utils import _random_email

# ── Base user template ─────────────────────────────────────────────────────────
# All users inherit from this base — override only what's different
_BASE_USER = {
    "first_name":          "John",
    "last_name":           "Smith",
    "number":              "1234567890",
    "email":               "",            # set by default_user fixture in conftest.py
    "password":            "Test@123",
    "pin":                 "0000",
    "confirm_pin":         "0000",
    "residential_address": "222333 PEACHTREE PLACE",
    "city":                "Atlanta",
    "state":               "Georgia",
    "zip":                 "12345",
    "ssn":                 "11-222-3333",
    "month":               "02",
    "day":                 "28",
    "year":                "1975",
    "investment_range":    "$2,001 - $10,000",
    "investment_state":    "Alabama",
}

# ── Valid sign up details ──────────────────────────────────────────────────────
# email is intentionally blank — set by default_user fixture in conftest.py
valid_sign_Up_details = {**_BASE_USER}

# ── ID upload user ─────────────────────────────────────────────────────────────
# Used for test_onboarding_with_upload_id
# Uses a fixed email since it is not created fresh each run
Id_upload_user = {
    **_BASE_USER,
    "first_name": "Document",
    "email":      "idupload@yopmail.com",
}

# ── User with existing email ───────────────────────────────────────────────────
# Used for test_existing_email — must be a pre-existing registered account
User_with_existing_email = {
    **_BASE_USER,
    "email": "sm100@yopmail.com",
}

# ── Invalid onboarding details ─────────────────────────────────────────────────
# Used for negative onboarding tests
invalid_sign_up_details = {
    "first_name": "",
    "last_name":  "",
    "number":     "123",        # too short
    "password":   "weak",       # no special chars, too short
    "email":      "notanemail", # invalid format
}

# ── Parametrize: Invalid emails ────────────────────────────────────────────────
INVALID_SIGNUP_EMAILS = [
    "user@",                  # missing domain
    "@example.com",           # missing local part
    "user.example.com",       # missing @
    "user@.com",              # dot immediately after @
    "user@com",               # missing dot in domain
    "user@@example.com",      # double @
    "user name@example.com",  # space in email
    "user#example.com",       # invalid character
    ".user@example.com",      # starts with dot
    "user.@example.com",      # ends with dot before @
]

# ── Parametrize: Invalid passwords ────────────────────────────────────────────
INVALID_SIGNUP_PASSWORDS = [
    "Test",                  # too short, no special chars
    " ",                     # blank/whitespace only
    "12345",                 # too short, no letters or special chars
    "estassword@12345678",   # too long (exceeds 20 chars)
]

# ── Parametrize: Invalid phone numbers ────────────────────────────────────────
INVALID_SIGNUP_PHONES = [
    " ",                     # blank/whitespace only
    "12345678",              # too short (8 digits)
    "123456789098765",       # too long (15 digits)
]