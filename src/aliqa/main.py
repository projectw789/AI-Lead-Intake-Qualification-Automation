from .user_input import first_user_query_input, second_user_query_input
from .ai_client import llm_first_query_validation
from .second_query_decision import decision_one
from .customer_profile import customer_value, customer_urgency, customer_profile_creation

first_query = first_user_query_input()

first_ai_response = llm_first_query_validation(first_query)

final_query_object = decision_one(first_ai_response, first_query)

value = customer_value(final_query_object)

urgency = customer_urgency(final_query_object)

customer_obj = customer_profile_creation(final_query_object, value, urgency)

print(customer_obj)

# uv run python -m aliqa.main
