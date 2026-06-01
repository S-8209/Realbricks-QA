# import pytest

# @pytest.fixture()
# def initia_Check():
#     print("Hello")

# def test_initial_check(initia_Check):
#     print("Sagar")
    
# initia_Check()
# # test_initial_check()
import pytest


def test_example(first_Check,second_check):
    print("2")
    assert first_Check =="pass"
    
def test2(first_Check,second_check):
    print(3)
    assert first_Check =="pass"
