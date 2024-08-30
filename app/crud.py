from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_models import Event
from app.schemas.event_schema import CreateEvent


async def create_event(db: AsyncSession, event: CreateEvent):
    new_event = Event(description=event.description, time=event.time)
    db.add(new_event)
    try:
        await db.commit()
        await db.refresh(new_event)
    except IntegrityError:
        await db.rollback()
        # I have added this, in case we need to add a
        # constraint in the database; regarding whether
        # event with the same description & time can exist or not
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EventResponse with the same description and time already exists",
        )
    return new_event


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).filter(Event.id == event_id))
    return result.scalars().first()


async def get_events(db: AsyncSession, from_time=None, to_time=None):
    query = select(Event)
    if from_time:
        query = query.filter(Event.time >= from_time)
    if to_time:
        query = query.filter(Event.time <= to_time)
    result = await db.execute(query)
    return result.scalars().all()
