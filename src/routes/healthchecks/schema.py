from pydantic import BaseModel


class HealthCheckReadinessElem(BaseModel):
    """Service health status representation.

    Attributes:
        service (str): Name of the service/module being checked (database)
        is_alive (bool): Boolean indicator of service availability
        msg (str): Detailed status message or error description
    """
    service: str
    is_alive: bool
    msg: str


class HealthCheckReadinessOutScheme(BaseModel):
    """Aggregated health status response for system readiness checks.

    Contains a collection of health statuses for all monitored system components.

    Attributes:
        items (list[HealthCheckReadinessElem]): Collection of service status reports
    """
    items: list[HealthCheckReadinessElem]
