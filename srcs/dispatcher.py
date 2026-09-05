from functools import partial
from typing import Callable
import srcs.utils
from srcs.validator import validate_month, validate_num, validate_suffix, validate_any, validate_under, validate_category
from srcs.schema import CommandSpec
from srcs.utils import updatetransaction, transactionlist, categoryadd, categorylist,categoryremove,search,budgetset, import_csv, export_csv, summary
from srcs.constants import MAX_BUDGET
VALID_COMMANDS: dict[str, CommandSpec] = {

    "add": {"pos": None, "options": {}},
    "list": {"pos": None, "options": {"limit": validate_num}},
    "search": {"pos": validate_any, "options": {
        "from_date": validate_month, "to_date": validate_month, "amount": validate_num, "type": validate_any, "category":validate_category
    }},

    "summary": {"pos": None, "options": {"month": validate_month, "top": validate_num}},

    "update": {"pos": None, "options": {"id": validate_num}},

    "delete": {"pos": None, "options": {"id": validate_num}},

    "import": {"pos": None, "options": {"from": validate_month}},

    "export": {"pos": None, "options": {
        "out": partial(validate_suffix, suffix=".csv"),
        "month": validate_month, "from": validate_month, "to": validate_month
    }}
}

VALID_SUBCOMMANDS: dict[str, dict[str, CommandSpec]] = {
    "budget": {
        "set": {"pos": None, "options": {
            "month": validate_month, "amount": partial(validate_under, num=MAX_BUDGET)
        }}
    },
    "category": {
        "add": {"pos": None, "options": {}},
        "list": {"pos": None, "options": {}},
        "remove": {"pos": None, "options": {}}
    }
}

VALID_CMD: dict[str, Callable[..., tuple[str, bool]]] = {
    "add": srcs.utils.addtransaction,
    "update": partial(updatetransaction, update=True),
    "delete": partial(updatetransaction, update=False),
    "list": transactionlist,
    "category add": categoryadd,
    "category list": categorylist,
    "category remove": categoryremove,
    "search": search,
    "budget set": budgetset,
    "import": import_csv, 
    "export": export_csv,
    "summary": summary
}