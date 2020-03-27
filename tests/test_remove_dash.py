from swagger_parser import remove_dash


def test_empty_string():
    result = remove_dash('')
    assert len(result) == 0


def test_no_dash_string():
    result = remove_dash('thisIs0323')
    assert result == 'thisIs0323'


def test_dash_string():
    result = remove_dash('thisIs-0323')
    assert result == 'thisIs0323'


def test_dash_string_case():
    result = remove_dash('th-isIs-0323')
    assert result == 'thIsIs0323'
