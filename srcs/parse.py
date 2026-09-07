
from __future__ import annotations
from srcs.dispatcher import VALID_COMMANDS, VALID_SUBCOMMANDS, CommandSpec
from srcs.exception import HelpException
from srcs.constants import HELP_MESSAGES

def parse_command(args: list[str]) -> tuple[str, list[str]]:
    if not args:
        raise ValueError("command가 필요합니다.")
    command = args[0]
    if command in VALID_COMMANDS:
        return command, args[1:]
    if command in VALID_SUBCOMMANDS:
        if len(args) < 2:
            raise ValueError(f"{command}의 subcommand가 필요합니다.")

        subcommand = args[1]

        if subcommand not in VALID_SUBCOMMANDS[command]:
            raise ValueError(f"유효하지 않은 subcommand: {subcommand}")

        return f"{command} {subcommand}", args[2:]

    raise ValueError(f"유효하지 않은 command: {command}")

def get_command_spec(command: str) -> CommandSpec:
    if " " not in command:
        return VALID_COMMANDS[command]

    parent, subcommand = command.split(" ", 1)
    return VALID_SUBCOMMANDS[parent][subcommand]

def parse_arguments(
    args: list[str],
    spec: CommandSpec,
    command: str,
) -> tuple[str | None, dict[str, str]]:

    positional = None
    options: dict[str, str] = {}

    # positional argument
    if args and not args[0].startswith("--"):

        if spec["pos"] is None:
            raise ValueError(
                "positional argument를 사용할 수 없습니다."
            )

        positional = args.pop(0)

        if not spec["pos"](positional):
            raise ValueError(
                f"잘못된 positional argument: {positional}"
            )

        if args:
            raise ValueError(
                "positional argument는 하나만 사용할 수 있습니다."
            )

        return positional, options

    # option parsing
    while args:

        option = args.pop(0)

        if option == "--help":
            raise HelpException(
                HELP_MESSAGES[command]
            )

        if not option.startswith("--"):
            raise ValueError(
                f"잘못된 option 형식: {option}"
            )

        option = option[2:]

        if option not in spec["options"]:
            raise ValueError(
                f"사용할 수 없는 option: --{option}"
            )

        if not args:
            raise ValueError(
                f"--{option}의 값이 필요합니다."
            )

        value = args.pop(0)

        if value.startswith("--"):
            raise ValueError(
                f"--{option}의 값이 필요합니다."
            )

        if option in options:
            raise ValueError(
                f"중복된 option: --{option}"
            )

        validator = spec["options"][option]

        if validator is not None and not validator(value):
            raise ValueError(
                f"잘못된 값: --{option} {value}"
            )

        options[option] = value

    # option 존재 여부 검사
    if spec["options_required"] and not options:
        raise ValueError(
            "최소 하나의 option이 필요합니다."
        )

    # required option 검사
    missing = spec["required_options"] - options.keys()

    if missing:
        missing_str = ", ".join(
            f"--{option}"
            for option in sorted(missing)
        )

        raise ValueError(
            f"필수 option이 없습니다: {missing_str}"
        )

    return positional, options