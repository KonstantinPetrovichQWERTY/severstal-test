import contextlib
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.database.models import Base


class DatabaseSessionManager:
    """Manages asynchronous database connections and sessions for SQLAlchemy.

    Handles the complete lifecycle of database connections including:
    - Engine initialization and configuration
    - Connection pooling
    - Session context management
    - Proper resource cleanup

    Attributes:
        _engine (AsyncEngine | None): SQLAlchemy async engine instance
        _sessionmaker (async_sessionmaker | None): Factory for async sessions
    """

    def __init__(self) -> None:
        """Initialize a new session manager with null engine and session factory."""
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str) -> None:
        """Initialize the database connection engine and session factory.

        Args:
            host (str): Database connection URL
        """

        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self) -> None:
        """Close all connections and cleanup connection pool resources.

        Raises:
            Exception: If called before initializing the engine
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized. `Close` method")

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Async context manager for database connection lifecycle management.

        Provides raw connection handling with automatic transaction rollback on errors.

        Yields:
            AsyncConnection: Active database connection

        Raises:
            Exception: If called before initializing the engine
        """
        if self._engine is None:
            raise Exception(
                "DatabaseSessionManager is not initialized. `Connect` method"
            )

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Async context manager for database session lifecycle management.

        Yields:
            AsyncSession: Database session instance

        Raises:
            Exception: If called before initializing the session factory
        """
        if self._sessionmaker is None:
            raise Exception(
                "DatabaseSessionManager is not initialized. `Session` method"
            )

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection) -> None:
        """Create all database tables using SQLAlchemy Base metadata.

        Primarily used for testing and initial setup.

        Args:
            connection (AsyncConnection): Active database connection
        """
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection) -> None:
        """Drop all database tables using SQLAlchemy Base metadata.

        Primarily used for testing and cleanup.

        Args:
            connection (AsyncConnection): Active database connection
        """
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that provides a database session context.

    Yields:
        AsyncSession: Database session instance for route handlers
    """
    async with sessionmanager.session() as session:
        yield session
