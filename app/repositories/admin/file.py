import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.models.file import File


def _filtered_files_stmt(
    *,
    content_type: str | None,
    uploaded_by: uuid.UUID | None,
) -> Select:
    """Build the filtered base statement shared by count and list queries."""
    stmt = select(File)
    if content_type:
        stmt = stmt.where(File.content_type == content_type)
    if uploaded_by is not None:
        stmt = stmt.where(File.uploaded_by_id == uploaded_by)
    return stmt


async def list_files_admin(
    session: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 50,
    content_type: str | None = None,
    uploaded_by: uuid.UUID | None = None,
) -> tuple[Sequence[File], int]:
    """Return a filtered, paginated file page plus the matching total count."""
    base_stmt = _filtered_files_stmt(content_type=content_type, uploaded_by=uploaded_by)

    count_stmt = base_stmt.with_only_columns(
        func.count(), maintain_column_froms=True
    ).order_by(None)
    total = (await session.execute(count_stmt)).scalar_one()

    rows_stmt = base_stmt.order_by(File.created_at.desc()).offset(skip).limit(limit)
    files = (await session.execute(rows_stmt)).scalars().all()

    return files, total
