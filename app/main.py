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
        command = input()
        if not command:
            continue
        
        com = command.split()[0]

        if com == "exit":
            break

        elif com == "echo":
            out = ""
            text = command[5:] 

            i = 0
            while i < len(text):
                if text[i] == "'":
                    i += 1
                    while i < len(text) and text[i] != "'":
                        out += text[i]
                        i += 1
                else:
                    if text[i] == " ":
                        out += " "
                        while i < len(text) and text[i] == " ":
                            i += 1
                        i -= 1
                    else :
                        out += text[i]
                i += 1

            print(out)

        elif com == "pwd":
            print(os.getcwd())

        elif com == "cd":
            to_path = command[3:]
            if to_path == "~":
                os.chdir(os.environ["HOME"])
            elif os.path.isdir(to_path):
                os.chdir(to_path)
            else:
                print(f"cd: {to_path}: No such file or directory")

        elif com == "type":
            arg = command[5:]
            if arg in ["echo", "exit", "type", "pwd", "cd"]:
                print(f"{arg} is a shell builtin")
            else:
                file_path = is_executable_in_path(arg)
                if file_path:
                    print(f"{arg} is {file_path}")
                else:
                    print(f"{arg}: not found")

        elif is_executable_in_path(com):
            subprocess.run(command)

        else:
            print(f"{com}: command not found")


if __name__ == "__main__":
    main()
