from .user_input import first_user_query_input
from .ai_client import llm_first_query_validation
from .decisions import decision_one, decision_two
from .lead_qualification import customer_value, customer_urgency, customer_profile_creation, customer_priority_qualification
from .pydantic_models import FirstClientQuery, SecondClientQuery



first_query = first_user_query_input()

first_ai_response = llm_first_query_validation(first_query)

final_query_object = decision_one(first_ai_response, first_query)


value, urgency = decision_two(final_query_object)

customer_obj = customer_profile_creation(final_query_object, value, urgency)



# uv run python -m aliqa.main
