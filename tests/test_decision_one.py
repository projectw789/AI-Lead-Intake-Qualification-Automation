from aliqa.pydantic_models import FirstClientQuery, SecondClientQuery
from aliqa.decisions import decision_one


def test_return_first_ai_response():
    mock_first_ai_response = FirstClientQuery(client_name = None, contact_email = "str", budget = 0.0, timeframe_type = "str", timeframe_num = 2, service = "str", client_industry = "str", product_requirements = None, pain_points = None)
    validated_mock_first_ai_response = decision_one(mock_first_ai_response, "str")
    assert isinstance (validated_mock_first_ai_response, FirstClientQuery)
    assert validated_mock_first_ai_response == mock_first_ai_response

def test_return_none():
    mock_none_response = None
    validated_mock_none_response = decision_one(mock_none_response, "str")
    assert validated_mock_none_response == None

def test_return_falseresult_str(monkeypatch):
    def mock_second_query():
        return "test"
    monkeypatch.setattr("aliqa.decisions.second_user_query_input", mock_second_query)
    mock_falseresult_str = decision_one("YAY", "yay2")
    assert mock_falseresult_str == "sorry, the service that you require and your contact email is a minimum for us to accept a query. we also request that you state your desired completion timeframe as a whole number of weeks, e.g. 3 weeks. please restart the applicaton and try again"

def test_return_second_ai_response(monkeypatch):
    def mock_second_query():
        return "Hi, my name is James Carter and my email is james.carter@example.com. I run a digital marketing agency and I'm looking for an AI automation system that can automatically process website enquiries, extract lead details, qualify each lead based on budget and urgency, and store the information in a database. We'd also like it to identify common pain points and summarise each enquiry for our sales team. Our budget is £7,500 and we'd like the system completed within 4 weeks."
    monkeypatch.setattr("aliqa.decisions.second_user_query_input", mock_second_query)
    mock_second_ai_response = decision_one("yay", "Hi, my name is James Carter and my email is james.carter@example.com. I run a digital marketing agency and need an AI automation system to process our website enquiries and qualify leads. Our budget is £7,500 and we'd like it completed within 4 weeks. It should extract useful information from each enquiry and help our sales team understand which leads need attention.")
    assert isinstance(mock_second_ai_response, SecondClientQuery)

def test_return_elif_noneresult_str(monkeypatch):
    def mock_second_llm_call(_,__,___):
        return None
    monkeypatch.setattr("aliqa.decisions.llm_second_query_validation", mock_second_llm_call)
    
    def mock_second_query():
        return "Hi, my name is James Carter and my email is james.carter@example.com. I run a digital marketing agency and I'm looking for an AI automation system that can automatically process website enquiries, extract lead details, qualify each lead based on budget and urgency, and store the information in a database. We'd also like it to identify common pain points and summarise each enquiry for our sales team. Our budget is £7,500 and we'd like the system completed within 4 weeks."
    monkeypatch.setattr("aliqa.decisions.second_user_query_input", mock_second_query)

    mock_noneresult_str = decision_one("YAY", "yay2")
    assert mock_noneresult_str == "sorry, experiencing technical issues, please try again later"



# class FirstClientQuery(BaseModel):
#     client_name : str | None
#     contact_email : str = Field(min_length = 1)
#     budget : float 
#     timeframe_type : str = Field(min_length = 1)
#     timeframe_num : int
#     service : str = Field(min_length=1)
#     client_industry : str = Field(min_length = 1)
#     product_requirements : list[str] | None
#     pain_points : list[str] | None