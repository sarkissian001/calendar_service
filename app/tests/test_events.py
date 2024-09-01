import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import Response


@pytest.mark.anyio
async def test_create_event(client: AsyncClient, session: AsyncSession):
    url = "/events/"
    event_data = {
        "description": "Some Event",
        "time": "2024-09-01T10:00:00"
    }

    response: Response = await client.post(url, json=event_data)
    assert response.status_code == 200
    data = response.json()

    assert data["description"] == "Some Event"
    assert data["time"] == "2024-09-01T10:00:00"


@pytest.mark.anyio
async def test_get_event_by_id(client: AsyncClient, session: AsyncSession):
    # First, create an event
    create_url = "/events/"
    event_data = {
        "description": "Doctor's appointment",
        "time": "2024-09-01T14:30:00"
    }
    create_response: Response = await client.post(create_url, json=event_data)
    assert create_response.status_code == 200
    created_event = create_response.json()

    # Now retrieve the event by ID
    event_id = created_event["id"]
    get_url = f"/events/{event_id}"
    response: Response = await client.get(get_url)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == event_id
    assert data["description"] == "Doctor's appointment"
    assert data["time"] == "2024-09-01T14:30:00"


@pytest.mark.anyio
async def test_get_events_should_be_empty(client: AsyncClient, session: AsyncSession):
    response = await client.get("/events")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_all_events_should_return_three_events(client: AsyncClient, session: AsyncSession):
    # Create multiple events
    for i in range(3):
        event_data = {
            "description": f"Test  Event N - {i}",
            "time": "2024-09-01T15:00:00"
        }
        create_response: Response = await client.post("/events/", json=event_data)
        assert create_response.status_code == 200

    response: Response = await client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["description"] == "Test  Event N - 0"
    assert data[0]["time"] == "2024-09-01T15:00:00"
    assert data[-1]["description"] == "Test  Event N - 2"


@pytest.mark.anyio
async def test_delete_event(client: AsyncClient, session: AsyncSession):
    # First, create an event
    create_url = "/events/"
    event_data = {
        "description": "Event to delete",
        "time": "2024-09-01T16:00:00"
    }
    create_response: Response = await client.post(create_url, json=event_data)
    assert create_response.status_code == 200
    created_event = create_response.json()
    event_id = created_event["id"]

    # Now delete the event
    delete_url = f"/events/{event_id}"
    delete_response: Response = await client.delete(delete_url)
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["message"] == f"EventResponse with ID {event_id} has been deleted successfully"

    # Verify the event is deleted
    get_url = f"/events/{event_id}"
    get_response: Response = await client.get(get_url)
    assert get_response.status_code == 404  # Should return 404 not found


@pytest.mark.anyio
async def test_get_event_with_formated_date(client: AsyncClient, session: AsyncSession):
    # First, create an event
    create_url = "/events/"
    event_data = {
        "description": "Test Event",
        "time": "2024-09-01T16:00:00"
    }
    create_response: Response = await client.post(create_url, json=event_data)
    assert create_response.status_code == 200

    query_url = f"/events?datetime_format=%m-%d-%Y"
    query_response: Response = await client.get(query_url)
    assert query_response.status_code == 200
    query_data = query_response.json()

    assert query_data[0]["time"] == "09-01-2024"


@pytest.mark.asyncio
async def test_get_events_by_date_range(client):
    # Create events with hardcoded timestamps
    events = [
        {"description": "Test 1", "time": "2024-01-01T01:01:01.000Z"},
        {"description": "Test 2", "time": "2024-01-02T01:01:01.000Z"},
        {"description": "Test 3", "time": "2024-01-03T01:01:01.000Z"},
        {"description": "Test 4", "time": "2024-01-04T01:01:01.000Z"},
        {"description": "Test 5", "time": "2024-01-05T01:01:01.000Z"}
    ]

    # Post the events to the API
    for event in events:
        await client.post("/events/", json=event)

    # Define the date range for the API call
    from_time = "2024-01-02T01:01:01.000Z"
    to_time = "2024-01-04T01:01:01.000Z"

    # Call the API to get events within the date range
    get_url = f"/events?from_time={from_time}&to_time={to_time}"
    response: Response = await client.get(get_url)

    # Verify the response
    assert response.status_code == 200
    data = response.json()

    # We expect events 2, 3, and 4 to be within the range
    expected_descriptions = ["Test 2", "Test 3", "Test 4"]
    returned_descriptions = [event["description"] for event in data]

    assert len(data) == len(expected_descriptions), f"Expected {len(expected_descriptions)} events, got {len(data)}"
    assert sorted(returned_descriptions) == sorted(
        expected_descriptions), f"Expected descriptions: {expected_descriptions}, got: {returned_descriptions}"
