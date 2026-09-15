from .user_input import second_user_query_input
from .pydantic_models import FirstClientQuery, SecondClientQuery
from .ai_client import llm_second_query_validation



def decision_one(first_ai_response, first_query):
    if isinstance(FirstClientQuery, first_ai_response):
        print("Your query has been submitted for processing. Thank You!")
        return first_ai_response

    elif first_ai_response is None:
        print("experiencing technical issues. please try again later.")
        return None

    else:
            for attempt in range(2):
                second_query = second_user_query_input()
                second_ai_response = llm_second_query_validation(first_ai_response, first_query, second_query)

                if second_ai_response == False:
                    print("sorry, the service that you require and your contact email is a minimum for us to accept a query. please try again")
                    continue

                elif isinstance(SecondClientQuery, second_ai_response):
                    print("query accepted. Thank You!")
                    return second_ai_response

                elif second_ai_response is None:
                    print("sorry, experiencing technical issues, please try again later")
                    return None

            