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
                        "content": f"""
                                    You are the information extraction component of a lead intake and qualification automation.

                                    Your task is to analyse the customer's enquiry and extract the requested information into a JSON object.

                                    Return ONLY the JSON object.
                                    Do not include explanations, comments, markdown, code fences, or any text outside the JSON object.

                                    The JSON object must contain exactly these 9 fields:

                                    client_name
                                    contact_email
                                    budget
                                    timeframe_type
                                    timeframe_num
                                    service
                                    client_industry
                                    product_requirements
                                    pain_points

                                    The extracted data will be passed into the following FIRST Pydantic model:

                                    - client_name: str | None
                                    - contact_email: str = Field(min_length=1)
                                    - budget: float
                                    - timeframe_type: str = Field(min_length=1)
                                    - timeframe_num: int
                                    - service: str = Field(min_length=1)
                                    - client_industry: str = Field(min_length=1)
                                    - product_requirements: list[str] | None
                                    - pain_points: list[str] | None

                                    For the first extraction attempt, the following information is required:

                                    - contact_email
                                    - budget
                                    - timeframe_type
                                    - timeframe_num
                                    - service
                                    - client_industry

                                    These fields must contain valid information when it is available in the enquiry.

                                    The following fields are optional in the first extraction:

                                    - client_name
                                    - product_requirements
                                    - pain_points

                                    Extraction rules:

                                    1. Extract information only from the customer's enquiry.
                                    2. Never invent, guess, or assume information that the customer did not provide.
                                    3. client_name:
                                    - Extract the customer's name if provided.
                                    - If no name is provided, return null.
                                    4. contact_email:
                                    - Extract the customer's email address if provided.
                                    - If no email address is provided, return an empty string "".
                                    5. budget:
                                    - Extract the customer's stated budget as a number.
                                    - Example: "£6,000" → 6000
                                    - Example: "£8k" → 8000
                                    - Never estimate or invent a budget.
                                    - If no budget is provided, return null.
                                    6. timeframe_type:
                                    - Extract whether the timeframe is given in weeks or months.
                                    - When a valid timeframe is provided, return exactly either "weeks".
                                    - Example: "3 weeks" → "weeks"
                                    
                                    - If no valid timeframe is provided, return an empty string "".
                                    7. timeframe_num:
                                    - Extract only the numerical amount from the timeframe.
                                    - Example: "3 weeks" → 3
                                    
                                    - Return a whole number.
                                    - If no valid timeframe is provided, return null.
                                    8. service:
                                    - Identify the product or service the customer is requesting.
                                    - If it cannot be determined, return an empty string "".
                                    9. client_industry:
                                    - Identify the customer's industry or niche if stated or clearly supported by the enquiry.
                                    - Do not guess the industry.
                                    - If it cannot be determined, return an empty string "".
                                    10. product_requirements:
                                    - Extract specific functionality, features, integrations, or design requirements.
                                    - Put each distinct requirement into a separate list item.
                                    - If none are mentioned, return null.
                                    11. pain_points:
                                    - Extract problems, frustrations, limitations, or difficulties explicitly mentioned by the customer.
                                    - Put each distinct pain point into a separate list item.
                                    - Do not invent pain points.
                                    - If none are mentioned, return null.
                                    12. Do not confuse a requested feature or requirement with a pain point.
                                    13. Every one of the 9 fields must be present in the JSON object.
                                    14. For fields that allow missing information, use JSON null where instructed above.
                                    15. For required string fields that cannot be extracted, use an empty string "" so that the Python Pydantic validation can detect the missing information.
                                    16. Do not add any fields other than the 9 specified fields.

                                    Customer enquiry:

                                    {first_query}
                                    """
                    }
                ]
            )
            dictio = json.loads(llm_response.choices[0].message.content)
            firstobject = FirstClientQuery(**dictio)
            return firstobject

        except ValidationError as e:
            # print(e)
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
                        "content": f"""
                                    You are the second-stage information extraction component of a lead intake and qualification automation.

                                    The customer has already provided an original enquiry.
                                    A first extraction was performed from that enquiry, but the first-stage Pydantic validation found that some required information was missing or invalid.
                                    The customer has now provided additional information.

                                    Your task is to combine all available information and produce the most complete and accurate lead record possible.

                                    Use all three sources:

                                    1. the original customer enquiry
                                    2. the first extraction
                                    3. the customer's additional information

                                    The customer's additional information is the newest source. If it corrects information from the first extraction or original enquiry, use the corrected information.

                                    Return ONLY the JSON object.
                                    Do not include explanations, comments, markdown, code fences, or any text outside the JSON object.

                                    The JSON object must contain exactly these 9 fields:

                                    client_name
                                    contact_email
                                    budget
                                    timeframe_type
                                    timeframe_num
                                    service
                                    client_industry
                                    product_requirements
                                    pain_points

                                    The extracted data will be passed into the following SECOND Pydantic model:

                                    - client_name: str | None
                                    - contact_email: str = Field(min_length=1)
                                    - budget: float | None
                                    - timeframe_type: str | None
                                    - timeframe_num: int | None
                                    - service: str = Field(min_length=1)
                                    - client_industry: str | None
                                    - product_requirements: list[str] | None
                                    - pain_points: list[str] | None

                                    For the second extraction attempt, only these two fields are required:

                                    - contact_email
                                    - service

                                    All other fields may legitimately contain None when the information is still unavailable.

                                    Extraction rules:

                                    1. Use information from all three sources.
                                    2. Never invent, guess, or assume information that the customer did not provide.
                                    3. Treat the first extraction as useful extracted information, but do not assume that it is always correct.
                                    4. Preserve useful information from the first extraction when it has not been contradicted.
                                    5. If the customer's additional information corrects earlier information, use the new information.
                                    6. client_name:
                                    - Use the customer's name if available.
                                    - If it still cannot be determined, return null.
                                    7. contact_email:
                                    - Extract the customer's email address if available.
                                    - This field is required for the second Pydantic model.
                                    - If it still cannot be determined, return an empty string "".
                                    8. budget:
                                    - Extract the customer's stated budget as a number.
                                    - Example: "£6,000" → 6000
                                    - Example: "£8k" → 8000
                                    - Never estimate or invent a budget.
                                    - If no budget can be determined, return null.
                                    9. timeframe_type:
                                    - When a valid timeframe is available, return exactly either "weeks".
                                    - Example: "3 weeks" → "weeks"
                                    
                                    - If no timeframe can be determined, return null.
                                    10. timeframe_num:
                                        - Extract only the numerical amount from the timeframe.
                                        - Example: "3 weeks" → 3
                                        
                                        - Return a whole number.
                                        - If no timeframe can be determined, return null.
                                    11. service:
                                        - Identify the product or service the customer is requesting.
                                        - This field is required for the second Pydantic model.
                                        - If the requested service cannot be determined from any available information, return an empty string "".
                                    12. client_industry:
                                        - Identify the customer's industry or niche if available.
                                        - Do not guess the industry.
                                        - If it still cannot be determined, return null.
                                    13. product_requirements:
                                        - Combine relevant requirements from the original enquiry, first extraction, and additional information.
                                        - Add newly provided requirements.
                                        - Do not duplicate requirements.
                                        - If no requirements can be determined, return null.
                                    14. pain_points:
                                        - Combine relevant pain points from the original enquiry, first extraction, and additional information.
                                        - Preserve valid existing pain points.
                                        - Do not invent pain points.
                                        - If no pain points can be determined, return null.
                                    15. Do not confuse requested features or requirements with pain points.
                                    16. Every one of the 9 fields must be present in the JSON object.
                                    17. For fields whose Pydantic type allows None, use JSON null when the information is unavailable.
                                    18. For required string fields that still cannot be extracted, use an empty string "" so that the Python Pydantic validation can reject the result.
                                    19. Do not add any fields other than the 9 specified fields.

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
            dictio = json.loads(llm_response.choices[0].message.content)
            second_object = SecondClientQuery(**dictio)
            return second_object

        except ValidationError as e:
            # print(e)
            return False

        except json.JSONDecodeError as e:
            print(e)
            continue

        except Exception as e:
            print(e)
            continue
    print("experiencing technical issues. please try again later")
    return None