from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from .pydantic_models import FirstClientQuery, SecondClientQuery
from pydantic import ValidationError

load_dotenv()

api_key = os.getenv("OPROAPIKEY")

ai_client = OpenAI(api_key = api_key, base_url = "https://openrouter.ai/api/v1")

def llm_first_query_validation(first_query):
    for attempt in range(3):
        try:
            llm_response = ai_client.chat.completions.create(
                model="openrouter/free",
                response_format = {"type":"json_object"},
                messages = [
                    {
                        "role" : "user",
                        "content" :f"""
                                    You are an information extraction system for a business lead qualification automation.

                                    Analyse the customer's enquiry and extract the relevant information into a JSON object.

                                    Return ONLY valid JSON.

                                    The JSON must contain exactly these 8 fields:

                                    client_name
                                    contact_email
                                    budget
                                    timeframe
                                    service
                                    client_industry
                                    product_requirements
                                    pain_points

                                    Use the following formats:

                                    - client_name: string or null
                                    - contact_email: string
                                    - budget: number or null
                                    - timeframe: string
                                    - service: string
                                    - client_industry: string
                                    - product_requirements: list of strings or null
                                    - pain_points: list of strings or null

                                    Rules:

                                    1. Extract information only from the customer's enquiry. Never invent information.
                                    2. client_name should be null if the customer does not provide their name.
                                    3. product_requirements should be null if no specific requirements are mentioned.
                                    4. pain_points should be null if no pain points are mentioned.
                                    5. If budget is not provided, return null. Do not guess a budget.
                                    6. If the customer gives a budget such as "£5,000", return 5000.
                                    7. For timeframe, return the timeframe in clear text, such as "6 weeks" or "within 2 months".
                                    8. service should describe the product or service the customer is requesting.
                                    9. client_industry should describe the customer's business or niche.
                                    10. product_requirements should contain specific functionality, features, or design requirements mentioned by the customer.
                                    11. pain_points should contain problems, frustrations, or weaknesses mentioned by the customer.
                                    12. If a required string field cannot be extracted from the enquiry, return an empty string "".
                                    13. If a required numeric field cannot be extracted, return null.
                                    14. Do not add any fields other than the 8 specified above.

                                    Customer enquiry:

                                    {first_query}
                                    """
                    }
                ]
            )
            dictio = json.loads(llm_response)
            firstobject = FirstClientQuery(**dictio)
            return firstobject

        except ValidationError as e:
            print(e)
            return dictio

        except json.JSONDecodeError as e:
            print(e)
            continue

        except Exception as e:
            print(e)
            continue
    print("experiencing technical issues. please try again later")
    return None



def llm_second_query_validation(first_ai_response, first_query, second_query):
    for attempt in range(3):
        try:
            llm_response = ai_client.chat.completions.create(
                model="openrouter/free",
                response_format = {"type":"json_object"},
                messages = [
                    {
                        "role" : "user",
                        "content" :f"""
                                    You are an information extraction system for a business lead qualification automation.

                                    A customer has provided an original enquiry. An initial extraction was performed, but some information was missing or incomplete. The customer has now provided additional information.

                                    Your task is to combine all available information and produce the most complete and accurate structured representation of the lead possible.

                                    Return ONLY valid JSON.

                                    The JSON must contain exactly these 8 fields:

                                    client_name
                                    contact_email
                                    budget
                                    timeframe
                                    service
                                    client_industry
                                    product_requirements
                                    pain_points

                                    Use these formats:

                                    - client_name: string or null
                                    - contact_email: string or null
                                    - budget: number or null
                                    - timeframe: string or null
                                    - service: string
                                    - client_industry: string or null
                                    - product_requirements: list of strings or null
                                    - pain_points: list of strings or null

                                    Rules:

                                    1. Use information from the original enquiry, the first extraction, and the customer's additional information.
                                    2. Do not invent information.
                                    3. If the customer has provided new or corrected information, use the newest information.
                                    4. Preserve useful information from the first extraction when it is not contradicted by the new information.
                                    5. client_name should be null if the customer's name cannot be determined.
                                    6. contact_email should be null if an email address cannot be determined.
                                    7. budget should be null if a budget cannot be determined.
                                    8. If a budget is given as a monetary amount, return the numerical amount only. For example, "£5,000" should become 5000.
                                    9. timeframe should describe the customer's requested timeframe. It should be null if no timeframe can be determined.
                                    10. service must describe the product or service the customer is requesting.
                                    11. client_industry should describe the customer's business or niche. It should be null if this cannot be determined.
                                    12. product_requirements should contain specific functionality, features, or design requirements mentioned by the customer. It should be null if none can be determined.
                                    13. pain_points should contain problems, frustrations, or weaknesses mentioned by the customer. It should be null if none can be determined.
                                    14. The service field is the minimum required information. If the requested service cannot be determined from any of the available information, return an empty string "".
                                    15. Do not add any fields other than the 8 specified above.

                                    Original customer enquiry:
                                    {first_query}

                                    First extraction:
                                    {first_ai_response}

                                    Customer's additional information:
                                    {second_query}
                                    """                                   
                    }
                ]
            )
            dictio = json.loads(llm_response)
            second_object = SecondClientQuery(**dictio)
            return second_object

        except ValidationError as e:
            print(e)
            return False

        except json.JSONDecodeError as e:
            print(e)
            continue

        except Exception as e:
            print(e)
            continue
    print("experiencing technical issues. please try again later")
    return None