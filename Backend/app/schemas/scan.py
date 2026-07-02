from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    target: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Target IP, hostname, or CIDR range"
    )