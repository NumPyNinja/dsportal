from ds_code import search


def test_found():
    assert search([12, 42, 26, 9, 60], 12) == "Element Found"


def test_not_found():
    assert search([12, 42, 26, 9, 60], 15) == "Not Found"