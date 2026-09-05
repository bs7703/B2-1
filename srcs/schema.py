from typing import Type, TypeVar, Callable, TypedDict, Generic,Optional, Dict
from srcs.constants.configs import TRANSACTION_LINE_SIZE, BUDGET_LINE_SIZE, CATEGORY_LINE_SIZE
from srcs.fileformat import transaction,budget,category

G = TypeVar("G")
Validator = Callable[[str], bool]

class CommandSpec(TypedDict):
    pos: Optional[Validator]
    options: Dict[str, Optional[Validator]]

class ClassConfig(Generic[G]):
    def __init__(self, line_size:int, dict_type:Type[G]):
        self.line_size = line_size
        self.dict_type = dict_type
class ConfigRegistry(TypedDict):
    transaction: ClassConfig[transaction]
    budget: ClassConfig[budget]
    category: ClassConfig[category]
DATACLASS: ConfigRegistry = {
    "transaction": ClassConfig(TRANSACTION_LINE_SIZE, transaction),
    "budget": ClassConfig(BUDGET_LINE_SIZE, budget),
    "category": ClassConfig(CATEGORY_LINE_SIZE, category),
}

