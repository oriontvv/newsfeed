"""Infrastructure event history storage module."""


class EventHistoryStorage:
    """Event history storage."""

    def __init__(self, config):
        """Initialize storage."""
        self._config = config

    async def add(self, entity_data):
        """Add entity data to the storage."""
        raise NotImplementedError()


class AsyncInMemoryEventHistoryStorage(EventHistoryStorage):
    """Async event history storage that stores events in memory."""

    def __init__(self, config):
        """Initialize queue."""
        super().__init__(config)
        self._storage = {}

    async def add(self, entity_data):
        """Add entity data to the storage."""
        event_fqid = entity_data['event_fqid']
        key = f'{event_fqid["newsfeed_id"]}-{event_fqid["event_id"]}'
        self._storage[key] = entity_data