from pydantic import BaseModel, Field

class FinalResponse(BaseModel):
    status: str = Field(description='One of: success, failure, uncertainty, missing_information, cancellation')
    answer: str = Field(description='The human-readable answer grounded in evidence.')
