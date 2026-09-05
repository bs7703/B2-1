
from __future__ import annotations
from srcs.dispatcher import VALID_COMMANDS, VALID_SUBCOMMANDS, CommandSpec

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
    spec: CommandSpec
) -> tuple[str | None, dict[str, str]]:

    positional = None
    options:dict[str,str] = {}

    if not args:
        return positional, options

    if not args[0].startswith("--"):
        if spec["pos"] is None:
            raise ValueError("positional argument를 사용할 수 없습니다.")

        positional = args[0]

        if not spec["pos"](positional):
            raise ValueError(f"잘못된 positional argument: {positional}")

        if len(args) > 1:
            raise ValueError("positional argument는 하나만 사용할 수 있습니다.")

        return positional, options

    while args:
        option = args.pop(0)[2:]

        if option == "help":
            # help 처리
            ...

        if option not in spec["options"]:
            raise ValueError(f"사용할 수 없는 option: --{option}")

        if not args:
            raise ValueError(f"--{option}의 값이 필요합니다.")

        value = args.pop(0)

        if value.startswith("--"):
            raise ValueError(f"--{option}의 값이 필요합니다.")

        if option in options:
            raise ValueError(f"중복된 option: --{option}")

        validator = spec["options"][option]

        if validator is not None and not validator(value):
            raise ValueError(f"잘못된 값: --{option} {value}")

        options[option] = value

    return positional, options