"""Subscriptions module."""

from typing import Type
from uuid import UUID, uuid4
from datetime import datetime

from newsfeed.packages.infrastructure.subscription_storage import SubscriptionStorage


class Subscription:
    """Subscription entity."""

    def __init__(self, id: UUID, from_newsfeed_id: str, to_newsfeed_id: str, subscribed_at):
        assert isinstance(id, UUID)
        self._id = id

        assert isinstance(from_newsfeed_id, str)
        self._from_newsfeed_id = from_newsfeed_id

        assert isinstance(to_newsfeed_id, str)
        self._to_newsfeed_id = to_newsfeed_id

        assert isinstance(subscribed_at, datetime)
        self._subscribed_at = subscribed_at

    @property
    def serialized_data(self):
        """Return serialized data."""
        return {
            'id': str(self._id),
            'from_newsfeed_id': self._from_newsfeed_id,
            'to_newsfeed_id': self._to_newsfeed_id,
            'subscribed_at': self._subscribed_at.timestamp(),
        }


class SubscriptionFactory:
    """Subscription entity factory."""

    def __init__(self, cls: Type[Subscription]):
        """Initialize factory."""
        assert issubclass(cls, Subscription)
        self._cls = cls

    def create_new(self, from_newsfeed_id, to_newsfeed_id) -> Subscription:
        """Create new subscription."""
        return self._cls(
            id=uuid4(),
            from_newsfeed_id=from_newsfeed_id,
            to_newsfeed_id=to_newsfeed_id,
            subscribed_at=datetime.utcnow(),
        )


class SubscriptionSpecification:
    """Subscription specification."""

    def __init__(self):
        """Initialize specification."""

    def is_satisfied_by(self, subscription: Subscription):
        """Check if subscription satisfies specification."""
        return True


class SubscriptionRepository:
    """Subscription repository."""

    def __init__(self, factory: SubscriptionFactory, storage: SubscriptionStorage):
        """Initialize repository."""
        assert isinstance(factory, SubscriptionFactory)
        self._factory = factory

        assert isinstance(storage, SubscriptionStorage)
        self._storage = storage

    async def add(self, subscription: Subscription):
        """Add event to repository."""
        await self._storage.add(subscription.serialized_data)


class SubscriptionService:
    """Subscription service."""

    def __init__(self,
                 factory: SubscriptionFactory,
                 specification: SubscriptionSpecification,
                 repository: SubscriptionRepository):
        """Initialize service."""
        assert isinstance(factory, SubscriptionFactory)
        self._factory = factory

        assert isinstance(specification, SubscriptionSpecification)
        self._specification = specification

        assert isinstance(repository, SubscriptionRepository)
        self._repository = repository

    async def create_subscription(self, subscription_data) -> Subscription:
        """Create subscription."""
        subscription = self._factory.create_new(
            from_newsfeed_id=subscription_data['from_newsfeed_id'],
            to_newsfeed_id=subscription_data['to_newsfeed_id'],
        )
        self._specification.is_satisfied_by(subscription)
        await self._repository.add(subscription)
