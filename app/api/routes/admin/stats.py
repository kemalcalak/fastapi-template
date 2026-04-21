from fastapi import APIRouter

from app.api.deps import CurrentSuperUser, SessionDep
from app.schemas.admin import AdminStats
from app.services.admin.stats_service import get_admin_stats_service

router = APIRouter()


@router.get("/stats", response_model=AdminStats)
async def get_stats(
    _admin: CurrentSuperUser,
    session: SessionDep,
) -> AdminStats:
    """Return aggregate dashboard counts in a single round-trip."""
    return await get_admin_stats_service(session=session)
