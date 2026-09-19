from .python_workflow import python_workflow
from .user_input import first_user_query_input


first_query = first_user_query_input()


python_workflow(first_query)

# uv run python -m aliqa.main
