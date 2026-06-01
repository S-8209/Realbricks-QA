import pytest

@pytest.fixture(scope="function")
def first_Check():
    print("\nsagar sharma")
    
    return("pass")

    
    
@pytest.fixture(scope="function")
def second_check():
    print("This is first")
    yield
    print("Second")
        