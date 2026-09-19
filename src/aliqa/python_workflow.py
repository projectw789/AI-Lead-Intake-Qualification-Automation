from .ai_client import llm_first_query_validation
from .decisions import decision_one, decision_two
from .lead_qualification import customer_profile_creation, customer_priority_qualification
from .sql_database import create_database, save_to_database, display_database
from .pydantic_models import FirstClientQuery, SecondClientQuery


def python_workflow(first_query):
    create_database()

    

    first_ai_response = llm_first_query_validation(first_query)

    final_query_object = decision_one(first_ai_response, first_query)

    if isinstance(final_query_object,FirstClientQuery) or isinstance(final_query_object, SecondClientQuery):
        value, urgency = decision_two(final_query_object)

        customer_obj = customer_profile_creation(final_query_object, value, urgency)

        upd_customer_obj = customer_priority_qualification(customer_obj)

        db_save_func_output = save_to_database(upd_customer_obj)

        if db_save_func_output == True:

            display_func_output = display_database()

            if display_func_output == False:
                print("temp")

            else:
                print(display_func_output)
        else:
            print("temp")
    else:
        print("temp")