import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break

        elif command.startswith("echo "):
            print(command[5:])

        elif command.startswith("type "):
            arg = command[5:]
            if arg in ["echo","exit","type"] :
                print(f"{arg} is a shell builtin.")
            else :
                print(f"{arg}: not found")
                
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
