from typing import Callable, Generic
from .constants import G

class Search(Generic[G]):
    def __init__(
        self,
        comp_id: Callable[[int], bool] | None = None,
        comp_date: Callable[[str], bool] | None = None,
        comp_type: Callable[[str], bool] | None = None,
        comp_amount: Callable[[int], bool] | None = None,
        comp_category: Callable[[str], bool] | None = None,
    ):
        self.comps = (
            ("id", comp_id),
            ("date", comp_date),
            ("type", comp_type),
            ("amount", comp_amount),
            ("category", comp_category),
        )

    def match(self, a: G) -> bool:
        return all(comp is None or value is None or comp(value)
            for name, comp in self.comps
            if (value := getattr(a, name)) is not None
        )

