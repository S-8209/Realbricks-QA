# test_data/login_data.py

INVALID_EMAILS = [
    "testexample.com",
    "test@",
    "@test.com",
    "test @mail.com",
    "test#mail.com"
]

INVALID_PASSWORDS = [
    ("sm100@yopmail.com", "Test@1233"),   # wrong password
    ("sm1001@yopmail.com", "Test@14223"),   # non-existent user
]

INVALID_PINS = [
    ("sm101@yopmail.com", "Test@123", "1211"),  # wrong pin
    ("sm101@yopmail.com", "Test@123", "0000"),  # default pin wrong user
]

INVALID_PHONE_NUMBERS = [
    " ",
    "12345678",
    "123456789098765"
]

INVALID_PASSWORDS_SIGNUP = [
    "Test",           # too short
    " ",              # blank
    "12345",          # no special chars
    "estassword@12345678"  # too long
]