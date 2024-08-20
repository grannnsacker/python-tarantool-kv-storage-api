from typing import Annotated

from fastapi import Depends

from app.main import app
from app.repositories import get_connection_repository, ConnectionRepository


@app.on_event("shutdown")
async def event_shutdown(connection_repository: Annotated[ConnectionRepository,
                                                          Depends(get_connection_repository,
                                                                  use_cache=True)]):
    """
    Asynchronous event handler for the "shutdown" event.

    :param connection_repository: ConnectionRepository instance responsible for managing
                                  database connections. Injected through dependency with
                                  optional caching (use_cache=True).

    The function calls discard_connection() to close or clean up the database connection
    when the application is shutting down.
    """
    await connection_repository.discard_connection()