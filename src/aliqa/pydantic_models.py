from pydantic import BaseModel, Field


class ClientQuery(BaseModel):
    client_name : str
    contact_email : str
    budget : float
    timeframe : str
    service : str = Field(min_length=1)
    client_industry : str
    product_requirements : list[str]
    pain_points : list[str] 


