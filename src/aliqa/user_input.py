def first_user_query_input():
    first_query = input("Welcome! \nPlease state your query including a minimum of: \nservice, contact email, industry , budget, timeframe (state desired completion timeframe as a whole number of weeks, e.g. 3 weeks). \nIt's a pleasure to have you with us today!\n\n")
    return first_query

def second_user_query_input():
    second_query = input("It seems that we are missing some key details. Please send a query containing:\nservice, contact email, industry, budget, timeframe (as a whole number of weeks, e.g. 3 weeks).\nThank You! \n\n")
    return second_query
