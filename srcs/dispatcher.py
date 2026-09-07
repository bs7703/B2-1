from functools import partial
from typing import Callable
from srcs.validator import validate_month, validate_num, validate_suffix, validate_any, validate_under, validate_category
from srcs.schema import CommandSpec
from srcs.transaction import addtransaction, updatetransaction, transactionlist,search, summary
from srcs.category import categoryadd, categorylist,categoryremove
from srcs.butget import budgetset
from srcs.csv_utils import import_csv, export_csv
from srcs.constants import MAX_BUDGET
VALID_COMMANDS: dict[str, CommandSpec] = {
    "add": {
        "pos": None,
        "options": {},
        "options_required": False,
        "required_options": set(),
    },

    "list": {
        "pos": None,
        "options": {
            "limit": validate_num
        },
        "options_required": False,
        "required_options": set(),
    },

    "search": {
        "pos": None,
        "options": {
            "from_date": validate_month,
            "to_date": validate_month,
            "amount": validate_num,
            "type": validate_any,
            "category": validate_category,
        },
        "options_required": True,
        "required_options": set(),
    },

    "summary": {
        "pos": None,
        "options": {
            "month": validate_month,
            "top": validate_num,
        },
        "options_required": True,
        "required_options": {"month"},
    },

    "update": {
        "pos": None,
        "options": {
            "id": validate_num,
        },
        "options_required": True,
        "required_options": {"id"},
    },

    "delete": {
        "pos": None,
        "options": {
            "id": validate_num,
        },
        "options_required": True,
        "required_options": {"id"},
    },

    "import": {
        "pos": None,
        "options": {
            "from": validate_month,
        },
        "options_required": True,
        "required_options": {"from"},
    },

    "export": {
        "pos": None,
        "options": {
            "out": partial(validate_suffix, suffix=".csv"),
            "month": validate_month,
            "from": validate_month,
            "to": validate_month,
        },
        "options_required": True,
        "required_options": {"out", "month"},
    },
}


VALID_SUBCOMMANDS: dict[str, dict[str, CommandSpec]] = {
    "budget": {
        "set": {
            "pos": None,
            "options": {
                "month": validate_month,
                "amount": partial(
                    validate_under,
                    num=MAX_BUDGET
                ),
            },
            "options_required": True,
            "required_options": {"month", "amount"},
        }
    },

    "category": {
        "add": {
            "pos": None,
            "options": {},
            "options_required": False,
            "required_options": set(),
        },

        "list": {
            "pos": None,
            "options": {},
            "options_required": False,
            "required_options": set(),
        },

        "remove": {
            "pos": None,
            "options": {},
            "options_required": False,
            "required_options": set(),
        },
    }
}

VALID_CMD: dict[str, Callable[..., tuple[str, bool]]] = {
    "add": addtransaction,
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