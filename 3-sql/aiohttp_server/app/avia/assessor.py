from typing import List

from app.avia.schemas import AirportDC


class AviaAccessor:
    async def get_airports(self) -> List[AirportDC]:
        pass
