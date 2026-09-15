from pydantic import BaseModel, Field


class FirstClientQuery(BaseModel):
    client_name : str | None
    contact_email : str = Field(min_length = 1)
    budget : float 
    timeframe : str = Field(min_length = 1)
    service : str = Field(min_length=1)
    client_industry : str = Field(min_length = 1)
    product_requirements : list[str] | None
    pain_points : list[str] | None

class SecondClientQuery(BaseModel):
    client_name : str | None
    contact_email : str = Field(min_length=1)
    budget : float | None
    timeframe : str | None
    service : str = Field(min_length=1)
    client_industry : str | None
    product_requirements : list[str] | None
    pain_points : list[str] | None


