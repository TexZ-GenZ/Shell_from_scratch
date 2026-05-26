import sys
import os
import subprocess


def is_executable_in_path(arg):
    for dir in os.environ["PATH"].split(os.pathsep):
        file_path = os.path.join(dir, arg)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path

def parser(text):
    args = []
    current = ""

    i = 0
    while i < len(text):
        if text[i] == "'":
            i += 1
            while i < len(text) and text[i] != "'":
                current += text[i]
                i += 1
        elif text[i] == "\"":
            i += 1
            while i < len(text) and text[i] != "\"":
                if text[i] == "\\" and text[i+1] in ["\"", "\\"]:
                    i +=1 
                current += text[i]
                i += 1
        elif text[i] == "\\" :
            i+=1
            current += text[i]

        elif text[i] == " ":
            if current:
                args.append(current)
                current = ""

            while i < len(text) and text[i] == " ":
                i += 1
            i -= 1
        else:
            current += text[i]

        i += 1

    if current:
        args.append(current)

    return args


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if not command:
            continue
        
        com = parser(command)[0]

        if com == "exit":
            break

        elif com == "echo":
            print(" ".join(parser(command[5:])))

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
            subprocess.run(parser(command))

        else:
            print(f"{com}: command not found")


if __name__ == "__main__":
    main()
