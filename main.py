from srcs.parse import parse_command, get_command_spec, parse_arguments
from srcs.execute import execute
import sys

def main():
    args = sys.argv[1:]
    try:
        cmd, options = parse_command(args)
        cmd_spec = get_command_spec(cmd)
        _, final_option = parse_arguments(options, cmd_spec)
        execute(cmd, final_option)
    except ValueError as v:
        print(f"{v}")
    except KeyboardInterrupt:
        print("키보드 인터럽트 발생")
    except EOFError:
        print("강제종료발생")
if __name__ == "__main__":
    main()