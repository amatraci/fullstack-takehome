from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    number: int = Field(..., ge=0, description="A non-negative integer")