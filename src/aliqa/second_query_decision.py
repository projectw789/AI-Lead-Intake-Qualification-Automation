from .user_input import second_user_query_input
from .pydantic_models import FirstClientQuery, SecondClientQuery
from .ai_client import llm_second_query_validation



def decision_one(first_ai_response, first_query):
    if isinstance(first_ai_response, FirstClientQuery):
        print("Your query has been submitted for processing. Thank You!")
        return first_ai_response

    elif first_ai_response is None:
        print("experiencing technical issues. please try again later.")
        return None

    else:
        second_query = second_user_query_input()
        second_ai_response = llm_second_query_validation(first_ai_response, first_query, second_query)

        if second_ai_response == False:
            return ("sorry, the service that you require and your contact email is a minimum for us to accept a query. we also request that yoy state your desired completion timeframe as a whole number of weeks, e.g. 3 weeks. please restart the applicaton and try again")
            

        elif isinstance(second_ai_response, SecondClientQuery):
            print("query accepted. Thank You!")
            return second_ai_response

        elif second_ai_response is None:
            return ("sorry, experiencing technical issues, please try again later")
            
           
            

            