from typing import Callable
from srcs.fileformat import Transaction
from srcs.comparator import comp_date as cd
class Search():
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
    def match(self, a:Transaction) -> bool:
        return all(comp is None or value is None or comp(value)
            for name, comp in self.comps
            if (value := getattr(a, name)) is not None
        )

def get_search_results(
                       from_date: str | None = None, 
                       to_date: str | None = None, 
                       amount: int | None = None, 
                       type_str: str | None = None,
                       category:str | None = None) -> Search:
    comp_date:Callable[[str], bool] | None  = None
    if from_date or to_date:
        comp_date = lambda d: (not from_date or cd(d, from_date)) and (not to_date or cd(to_date, d))
    comp_amount:Callable[[int], bool] | None = (lambda a: a == amount) if amount is not None else None
    comp_type:Callable[[str], bool]| None = (lambda t: t == type_str) if type_str else None
    comp_category:Callable[[str], bool] | None = (lambda t: t == category) if category else None
    search_engine = Search(comp_date=comp_date,comp_amount=comp_amount,comp_type=comp_type, comp_category=comp_category)
    return search_engine