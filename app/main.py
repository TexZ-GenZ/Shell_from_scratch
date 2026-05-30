import shell_state
from shell_builtins import shell_builtins
from shell_commands import build_commands
from shell_completion import setup_readline
from shell_parse import parse_input
from shell_runner import run_builtin, run_external

def main():
    shell_state.COMMANDS = build_commands()
    COMMANDS = shell_state.COMMANDS
    setup_readline()

    while True:
        command = input("$ ")
        if not command:
            continue

        parsed_command, redirect_type, file_path = parse_input(command)
        com = parsed_command[0]

        if com == "exit":
            break

        elif com in shell_builtins.MEMBERS:
            run_builtin(parsed_command, redirect_type, file_path)

        elif com in COMMANDS:
            run_external(parsed_command, redirect_type, file_path)

        else:
            print(f"{com}: command not found")


if __name__ == "__main__":
    main()
