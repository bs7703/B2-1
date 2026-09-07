from srcs.parse import parse_command, get_command_spec, parse_arguments
from srcs.execute import execute
from srcs.exception import HelpException
import sys

def main():
    args = sys.argv[1:]
    try:
        cmd, options = parse_command(args)
        cmd_spec = get_command_spec(cmd)
        _, final_option = parse_arguments(options, cmd_spec, cmd)
        execute(cmd, final_option)
    except HelpException as h:
        print(h.message)
    except ValueError as v:
        print(v)
    except TypeError as t:
        print(t)
    except KeyboardInterrupt:
        print("키보드 인터럽트 발생")
    except EOFError:
        print("강제종료발생")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()