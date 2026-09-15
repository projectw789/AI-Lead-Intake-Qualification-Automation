from .user_input import first_user_query_input, second_user_query_input
from .ai_client import llm_first_query_validation
from .second_query_decision import decision_one

first_query = first_user_query_input()

first_ai_response = llm_first_query_validation(first_query)

decision_one_output = decision_one(first_ai_response, first_query)

print(decision_one_output)

# uv run python -m aliqa.main
