from .pydantic_models import CustomerProfile

def customer_value(final_query_object):
    if final_query_object.budget is None:
        value = "Unknown"

    elif final_query_object.budget >= 0.00 and final_query_object.budget <= 2999.00:
        value = "Low"

    elif final_query_object.budget >= 3000.00 and final_query_object.budget <= 5999.00:
        value = "Medium"

    elif final_query_object.budget >= 6000.00 and final_query_object.budget <= 8999.00:
        value = "High"

    elif final_query_object.budget >= 9000.00:
        value = "Very High"

    return value

def customer_urgency(final_query_object):
    if final_query_object.timeframe_type is None:
        urgency = "Unknown"

    elif final_query_object.timeframe_type.lower() == "weeks":
        if final_query_object.timeframe_num <= 2:
            urgency = "High"

        elif final_query_object.timeframe_num >= 3 and final_query_object.timeframe_num <= 6:
            urgency = "Medium"

        elif final_query_object.timeframe_num >= 7:
            urgency = "Low"

    return urgency

def customer_profile_creation(final_query_object, value, urgency):
    customer_profile_obj = CustomerProfile(**final_query_object.model_dump(), value = value, urgency = urgency)
    return customer_profile_obj