from fastapi import APIRouter, HTTPException, status

from app.schemas.host import ScanResponse
from app.schemas.scan import ScanRequest
from app.services.nmap_service import NmapService

router = APIRouter()

nmap_service = NmapService()


@router.post(
    "",
    response_model=ScanResponse,
    status_code=status.HTTP_200_OK,
    summary="Run an Nmap scan"
)
async def run_scan(request: ScanRequest):

    try:

        hosts = nmap_service.scan(request.target)

        return ScanResponse(
            target=request.target,
            total_hosts=len(hosts),
            hosts=hosts,
        )

    except RuntimeError as exception:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )