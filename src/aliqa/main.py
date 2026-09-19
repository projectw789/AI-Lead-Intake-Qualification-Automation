from .python_workflow import python_workflow
from .user_input import first_user_query_input
from .sql_database import display_database

first_query = first_user_query_input()


python_workflow(first_query)

display_func_output = display_database()

# uv run python -m aliqa.main
