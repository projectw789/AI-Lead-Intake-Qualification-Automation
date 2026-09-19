from aliqa.pydantic_models import SecondClientQuery, CustomerProfile, UpdatedCustomerProfile
from aliqa.lead_qualification import customer_value, customer_urgency
import pytest


@pytest.mark.parametrize(
    "budget, expected_value",
    [
        (0, "Low"),
        (2999, "Low"),
        (3000, "Medium"),
        (5999, "Medium"),
        (6000, "High"),
        (8999, "High"),
        (9000, "Very High"),
        (None, "Unknown"),
    ]
)
def test_value_success(budget, expected_value):
    mock_query = SecondClientQuery(client_name = None, contact_email = "str", budget = budget, timeframe_type = None, timeframe_num = 2, service = "str", client_industry = None, product_requirements = None, pain_points = None)
    mock_value = customer_value(mock_query)
    assert mock_value == expected_value

@pytest.mark.parametrize(
    "timeframe_type, timeframe_num, expected_output",
    [
        ("weeks", 1, "High"),
        ("weeks", 2, "High"),
        ("weeks", 3, "Medium"),
        ("weeks", 6, "Medium"),
        ("weeks", 7, "Low"),
        ("weeks", 10, "Low"),
        (None, None, "Unknown"),
    ]
)
def test_urgency_success(timeframe_type, timeframe_num, expected_output):
        mock_query = SecondClientQuery(client_name = None, contact_email = "str", budget = None, timeframe_type = timeframe_type, timeframe_num = timeframe_num, service = "str", client_industry = None, product_requirements = None, pain_points = None)
        mock_urgency = customer_urgency(mock_query)
        assert mock_urgency == expected_output