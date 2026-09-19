from aliqa.pydantic_models import FirstClientQuery, SecondClientQuery
from aliqa.decisions import decision_two
import pytest

@pytest.mark.parametrize(
    "model_type, budget, mock_timeframe_type, mock_timeframe_num, check_value, check_urgency",
    [

    (FirstClientQuery, 1500, "weeks", 10, "Low", "Low"),
    (FirstClientQuery, 4500, "weeks", 5, "Medium", "Medium"),
    (FirstClientQuery, 7500, "weeks", 2, "High", "High"),
    (FirstClientQuery, 12000, "weeks", 1, "Very High", "High"),
   

    (SecondClientQuery, 1500, "weeks", 10, "Low", "Low"),
    (SecondClientQuery, 4500, "weeks", 5, "Medium", "Medium"),
    (SecondClientQuery, 7500, "weeks", 2, "High", "High"),
    (SecondClientQuery, 12000, "weeks", 1, "Very High", "High"),
    (SecondClientQuery, None, None, None, "Unknown", "Unknown")
    ]
)
def test_return_known_value_urgency(model_type, budget, mock_timeframe_type, mock_timeframe_num, check_value, check_urgency):
    mock_final_client_query = model_type(client_name = "str", contact_email = "str", budget = budget, timeframe_type = mock_timeframe_type, timeframe_num = mock_timeframe_num, service = "str", client_industry = "str", product_requirements = None, pain_points = None)
    mock_value, mock_urgency = decision_two(mock_final_client_query)
    assert mock_value == check_value
    assert mock_urgency == check_urgency

