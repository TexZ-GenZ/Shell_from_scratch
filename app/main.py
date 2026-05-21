import sys
import os
import subprocess


def is_executable_in_path(arg):
    for dir in os.environ["PATH"].split(os.pathsep):
        file_path = os.path.join(dir, arg)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path


def main():
    while True:
        sys.stdout.write("$ ")
        command = input().split()

        if not command:
            continue

        if command[0] == "exit":
            break

        elif command[0] == "echo":
            print(" ".join(command[1:]))

        elif command[0] == "pwd":
            print(os.getcwd())

        elif command[0] == "cd":
            to_path = command[1]
            if to_path == "~":
                os.chdir(os.environ["HOME"])
            elif os.path.isdir(to_path):
                os.chdir(to_path)
            else:
                print(f"cd: {to_path}: No such file or directory")

        elif command[0] == "type":
            arg = " ".join(command[1:])
            if arg in ["echo", "exit", "type", "pwd", "cd"]:
                print(f"{arg} is a shell builtin")
            else:
                file_path = is_executable_in_path(arg)
                if file_path:
                    print(f"{arg} is {file_path}")
                else:
                    print(f"{arg}: not found")

        elif is_executable_in_path(command[0]):
            subprocess.run(command)

        else:
            print(f"{command[0]}: command not found")


if __name__ == "__main__":
    main()
