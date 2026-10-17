import pytest
from werkzeug.exceptions import HTTPException
from competition import validate_si_rent_data_user_input


def _call(starts, endings, missing, additional):
    return validate_si_rent_data_user_input(starts, endings, missing, additional)


def test_additional_cards_added_to_available_pool():
    starts = ["100", "200"]
    endings = ["105", "205"]
    missing = ["", ""]
    additional = "300, 301, 302"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert 100 in available
    assert 300 in available
    assert 301 in available
    assert 302 in available


def test_additional_cards_are_allocatable_when_no_boxes_filled():
    starts = ["", ""]
    endings = ["", ""]
    missing = ["", ""]
    additional = "500, 501"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available == [500, 501]


def test_additional_cards_deduplicate_against_box_ranges():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "102, 103"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available.count(102) == 1
    assert available.count(103) == 1


def test_additional_cards_whitespace_handled():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = " 110 , 111 "

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert 110 in available
    assert 111 in available


def test_empty_additional_cards_string_not_added():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = ""

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available == [100, 101, 102, 103, 104, 105]


def test_whitespace_only_additional_cards_not_added():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "   "

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available == [100, 101, 102, 103, 104, 105]


def test_invalid_additional_card_aborts():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "abc"

    with pytest.raises(HTTPException) as excinfo:
        _call(starts, endings, missing, additional)

    assert excinfo.value.code == 400


def test_additional_card_outside_range_still_added():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "999"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert 999 in available


def test_si_box_with_no_missing_cards_allowed():
    starts = ["100"]
    endings = ["105"]
    missing = [""]

    _, _, available, _ = _call(starts, endings, missing, "")

    assert available == [100, 101, 102, 103, 104, 105]


def test_additional_cards_returned_are_only_additional_not_box_ranges():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "200, 201"

    _, _, _, additional_cards = _call(starts, endings, missing, additional)

    assert additional_cards == [200, 201]
    assert 100 not in additional_cards


def test_additional_cards_with_ranges_added_to_available_pool():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "200-202, 300"

    _, _, available, additional_cards = _call(starts, endings, missing, additional)

    assert additional_cards == [200, 201, 202, 300]
    assert 200 in available
    assert 201 in available
    assert 202 in available
    assert 300 in available


def test_additional_cards_range_only_when_no_boxes_filled():
    starts = ["", ""]
    endings = ["", ""]
    missing = ["", ""]
    additional = "500-502"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available == [500, 501, 502]


def test_additional_cards_range_deduplicate_against_box_ranges():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "102-104"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available.count(102) == 1
    assert available.count(103) == 1
    assert available.count(104) == 1


def test_additional_cards_invalid_range_aborts():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "abc-def"

    with pytest.raises(HTTPException) as excinfo:
        _call(starts, endings, missing, additional)

    assert excinfo.value.code == 400


def test_additional_cards_range_start_greater_than_end_aborts():
    starts = ["100"]
    endings = ["105"]
    missing = [""]
    additional = "200-190"

    with pytest.raises(HTTPException) as excinfo:
        _call(starts, endings, missing, additional)

    assert excinfo.value.code == 400


def test_additional_cards_mixed_single_and_range():
    starts = ["", ""]
    endings = ["", ""]
    missing = ["", ""]
    additional = "1-3, 5, 8-10"

    _, _, available, _ = _call(starts, endings, missing, additional)

    assert available == [1, 2, 3, 5, 8, 9, 10]
