"""Tests unitaires complets pour valider validate_quantity, line_subtotal_cents et three_for_two_discount_cents."""

import pytest

from supermarket_receipt_api.checkout import (
    validate_quantity,
    line_subtotal_cents,
    three_for_two_discount_cents,
    percentage_discount_cents,
)


@pytest.mark.parametrize("valid_qty", [1, 3, 5, 100])
def test_validate_quantity_nominal(valid_qty: int) -> None:
    assert validate_quantity(valid_qty) == valid_qty


@pytest.mark.parametrize("invalid_value", [0, -1, -10])
def test_validate_quantity_value_error(invalid_value: int) -> None:
    with pytest.raises(ValueError):
        validate_quantity(invalid_value)


@pytest.mark.parametrize("invalid_type", [1.5, "3", True, False, None])
def test_validate_quantity_type_error(invalid_type: object) -> None:
    with pytest.raises(TypeError):
        validate_quantity(invalid_type)  # type: ignore

@pytest.mark.parametrize(
    "unit_price_cents, quantity, unit, expected",
    [
        (100, 2, "piece", 200),
        (199, 1000, "gram", 199),
        (199, 2000, "gram", 398),
        (99, 3, "piece", 297),
    ],
)
def test_line_subtotal_nominal(
    unit_price_cents: int, quantity: int, unit: str, expected: int
) -> None:
    assert line_subtotal_cents(unit_price_cents, quantity, unit) == expected


def test_line_subtotal_errors() -> None:
    with pytest.raises(ValueError):
        line_subtotal_cents(-10, 2, "piece")
    with pytest.raises(ValueError):
        line_subtotal_cents(100, 2, "liter")
    with pytest.raises(TypeError):
        line_subtotal_cents(True, 2, "piece")


@pytest.mark.parametrize(
    "unit_price_cents, quantity, expected_discount",
    [
        (99, 1, 0),   # Moins de 3 : pas de réduction
        (99, 2, 0),   # Moins de 3 : pas de réduction
        (99, 3, 99),  # Exactement 3 : 1 article offert (99c) -> Test clé du bug corrigé
        (99, 4, 99),  # 4 pièces : 1 article offert
        (99, 6, 198), # 6 pièces : 2 articles offerts
    ],
)
def test_three_for_two_discount_nominal(
    unit_price_cents: int, quantity: int, expected_discount: int
) -> None:
    assert three_for_two_discount_cents(unit_price_cents, quantity) == expected_discount


def test_three_for_two_discount_errors() -> None:
    with pytest.raises(ValueError):
        three_for_two_discount_cents(-5, 3)
    with pytest.raises(ValueError):
        three_for_two_discount_cents(99, 0)
    with pytest.raises(TypeError):
        three_for_two_discount_cents(99, True)


@pytest.mark.parametrize(
    "subtotal_cents, discount_percent, expected",
    [(1000, 20, 200), (1200, 10, 120), (800, 25, 200)]
    + [(100 * amount_euros, 10, 10 * amount_euros) for amount_euros in range(20, 114)],
)
def test_percentage_discount_nominal(
    subtotal_cents: int, discount_percent: int, expected: int
) -> None:
    assert percentage_discount_cents(subtotal_cents, discount_percent) == expected