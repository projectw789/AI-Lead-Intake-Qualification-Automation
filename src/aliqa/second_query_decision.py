from .user_input import second_user_query_input
from .pydantic_models import FirstClientQuery




def decision(ai_response):
    if isinstance(FirstClientQuery, ai_response):
        print("Your query has been submitted for processing. Thank You!")
        return ai_response

    elif ai_response == False:
        second_query_input = second_user_query_input()
        return second_query_input

    elif ai_response is None:
        print("experiencing technical issues. please try again later.")
        return None