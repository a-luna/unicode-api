from app.schemas.camel_model import CamelModel


class UnicodePlane(CamelModel):
    number: int
    name: str
    abbreviation: str
    start: str
    finish: str
    total_allocated: int
    total_defined: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            "UnicodePlane<"
            f"number={self.number}, "
            f'name="{self.name}", '
            f'abbreviation="{self.abbreviation}", '
            f'start="{self.start}", '
            f'finish="{self.finish}", '
            f"total_allocated={self.total_allocated}, "
            f"total_defined={self.total_defined}"
            ">"
        )


class UnicodePlaneInternal(UnicodePlane):
    start_dec: int
    finish_dec: int
    start_block_id: int
    finish_block_id: int
