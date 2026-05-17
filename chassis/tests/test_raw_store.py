import pytest
import pytest_asyncio
from pathlib import Path
from chassis.stores.raw import RawStore
from chassis.models.events import BaseEvent

@pytest_asyncio.fixture
async def store():
    store = RawStore(db_path=Path(":memory:"))
    await store.initialize()
    return store

@pytest.mark.asyncio
async def test_save_event_forces_consolidated_false(store: RawStore):
    """Guardar un evento con consolidated=True debe persistir como False."""
    event = BaseEvent(id="1", consolidated=True)
    await store.save_event(event)
    
    saved_event = await store.get_by_id("1")
    assert saved_event is not None
    assert saved_event.consolidated is False
    assert saved_event.id == "1"

@pytest.mark.asyncio
async def test_save_events_atomic(store: RawStore):
    """save_events persiste todos los eventos o ninguno."""
    events = [
        BaseEvent(id="2", consolidated=True),
        BaseEvent(id="3", consolidated=True)
    ]
    await store.save_events(events)
    
    unconsolidated = await store.get_unconsolidated()
    assert len(unconsolidated) == 2
    for event in unconsolidated:
        assert event.consolidated is False

@pytest.mark.asyncio
async def test_get_unconsolidated_returns_only_false(store: RawStore):
    """get_unconsolidated no retorna eventos ya consolidados."""
    events = [
        BaseEvent(id="4"),
        BaseEvent(id="5")
    ]
    await store.save_events(events)
    
    # Mark one as consolidated
    await store.mark_consolidated(["4"])
    
    unconsolidated = await store.get_unconsolidated()
    assert len(unconsolidated) == 1
    assert unconsolidated[0].id == "5"

@pytest.mark.asyncio
async def test_mark_consolidated_updates_count(store: RawStore):
    """mark_consolidated retorna el número correcto de filas actualizadas."""
    events = [
        BaseEvent(id="6"),
        BaseEvent(id="7"),
        BaseEvent(id="8")
    ]
    await store.save_events(events)
    
    count = await store.mark_consolidated(["6", "7", "999"])
    assert count == 2

@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_missing(store: RawStore):
    """get_by_id retorna None para un event_id inexistente."""
    result = await store.get_by_id("missing")
    assert result is None
