"""Fixed warehouse. A question with no digit is not a number."""

from latch.domain.hits import WarehouseHit

VALUE = "10.00"


class FixedWarehouse:
    def query_warehouse(self, question: str) -> WarehouseHit:
        if not any(character.isdigit() for character in question):
            return WarehouseHit(None)
        return WarehouseHit(VALUE)
