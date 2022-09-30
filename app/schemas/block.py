from app.schemas.camel_model import CamelModel


class UnicodeBlockInternal(CamelModel):
    id: int
    block: str
    start_dec: int
    start: str
    finish_dec: int
    finish: str
    total_assigned: int


class UnicodeBlock(CamelModel):
    block: str
    start: str
    finish: str
    total_assigned: int
