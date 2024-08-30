from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import pytz

from fastapi import APIRouter, Depends, Query, HTTPException

from app import crud
from app.schemas import event_schema
from app.schemas.event_schema import EventResponse
from app.database.connection import get_db

router = APIRouter()


def convert_to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    else:
        dt = dt.astimezone(pytz.utc)
    return dt


@router.post("/events/", response_model=event_schema.EventResponse)
async def create_event(
    event: event_schema.CreateEvent, db: AsyncSession = Depends(get_db)
):
    # Convert time to UTC before storing
    event.time = convert_to_utc(event.time)

    # Create the event in the database
    db_event = await crud.create_event(db=db, event=event)

    # Return the event with the time formatted as a string
    return event_schema.EventResponse(
        id=db_event.id,
        description=db_event.description,
        time=db_event.time.strftime("%Y-%m-%dT%H:%M:%S"),  # Default to ISO format
    )


@router.get("/events", response_model=list[EventResponse])
async def get_events(
    datetime_format: str = Query(None),
    from_time: datetime = Query(None),
    to_time: datetime = Query(None),
    db: AsyncSession = Depends(get_db),
):
    db_events = await crud.get_events(db, from_time=from_time, to_time=to_time)

    # Format the times if datetime_format is specified
    formatted_events = []
    for event in db_events:
        if datetime_format:
            formatted_time = event.time.strftime(datetime_format)
        else:
            formatted_time = event.time.strftime("%Y-%m-%dT%H:%M:%S")
        formatted_events.append(
            {"id": event.id, "description": event.description, "time": formatted_time}
        )

    return formatted_events


@router.get("/events/{event_id}", response_model=EventResponse)
async def read_event(
    event_id: int,
    datetime_format: str = Query(None),  # Default is None to use original format
    db: AsyncSession = Depends(get_db),
):
    db_event = await crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="EventResponse not found")

    # Apply formatting only if datetime_format is specified
    if datetime_format:
        formatted_time = db_event.time.strftime(datetime_format)
    else:
        formatted_time = db_event.time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "id": db_event.id,
        "description": db_event.description,
        "time": formatted_time,
    }


@router.delete("/events/{event_id}", response_model=dict)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the event by ID
    db_event = await crud.get_event(db, event_id=event_id)

    if db_event is None:
        raise HTTPException(status_code=404, detail="EventResponse not found")

    await db.delete(db_event)
    await db.commit()

    return {"message": f"EventResponse with ID {event_id} has been deleted successfully"}
