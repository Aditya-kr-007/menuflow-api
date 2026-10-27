from pydantic import BaseModel, ConfigDict


class MenuItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    price: float
    description: str
    available: bool


class MenuResponse(BaseModel):
    status: str = "success"
    count: int
    items: list[MenuItem]
