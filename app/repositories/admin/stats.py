from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user_activity import UserActivity


async def get_admin_stats(session: AsyncSession) -> dict[str, int]:
    """Return aggregate counts used by the admin dashboard in a single round-trip."""
    stmt = select(
        func.count(User.id).label("users_total"),
        func.count().filter(User.is_active.is_(True)).label("users_active"),
        func.count().filter(User.is_verified.is_(True)).label("users_verified"),
    )
    row = (await session.execute(stmt)).one()

    activities_total = (
        await session.execute(select(func.count()).select_from(UserActivity))
    ).scalar_one()

    return {
        "users_total": row.users_total,
        "users_active": row.users_active,
        "users_verified": row.users_verified,
        "activities_total": activities_total,
    }
