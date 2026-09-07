from typing import Type, TypeVar, Callable, TypedDict, Generic,Optional
from srcs.constants.configs import TRANSACTION_LINE_SIZE, BUDGET_LINE_SIZE, CATEGORY_LINE_SIZE
from srcs.fileformat import Transaction,Budget,Category

G = TypeVar("G")
Validator = Callable[[str], bool]

class CommandSpec(TypedDict):
    pos: Optional[Validator]
    options: dict[str, Optional[Validator]]
    options_required:bool
    required_options: set[str]

class ClassConfig(Generic[G]):
    def __init__(self, line_size:int, dict_type:Type[G]):
        self.line_size = line_size
        self.dict_type = dict_type
class ConfigRegistry(TypedDict):
    transaction: ClassConfig[Transaction]
    budget: ClassConfig[Budget]
    category: ClassConfig[Category]
DATACLASS: ConfigRegistry = {
    "transaction": ClassConfig(TRANSACTION_LINE_SIZE, Transaction),
    "budget": ClassConfig(BUDGET_LINE_SIZE, Budget),
    "category": ClassConfig(CATEGORY_LINE_SIZE, Category),
}

