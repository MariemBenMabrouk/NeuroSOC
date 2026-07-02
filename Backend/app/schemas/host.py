from typing import List, Optional

from pydantic import BaseModel


class Service(BaseModel):
    port: int
    protocol: str
    state: str
    service: str
    product: Optional[str] = None
    version: Optional[str] = None


class Host(BaseModel):
    ip_address: str
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    vendor: Optional[str] = None
    operating_system: Optional[str] = None
    status: str
    services: List[Service] = []


class ScanResponse(BaseModel):
    target: str
    total_hosts: int
    hosts: List[Host]