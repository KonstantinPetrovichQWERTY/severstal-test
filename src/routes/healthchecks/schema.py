from pydantic import BaseModel


class HealthCheckReadinessElem(BaseModel):
    service: str
    is_alive: bool
    msg: str


class HealthCheckReadinessOutScheme(BaseModel):
    items: list[HealthCheckReadinessElem]
