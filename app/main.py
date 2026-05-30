import sys
import os
import subprocess
import readline


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
        elif text[i] == '"':
            i += 1
            while i < len(text) and text[i] != '"':
                if text[i] == "\\" and text[i + 1] in ['"', "\\"]:
                    i += 1
                current += text[i]
                i += 1
        elif text[i] == "\\":
            i += 1
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

def redirect(text, redirect_type, file_path=None):
    if redirect_type == "stdout" and file_path:
        if text is not None:
            with open(file_path, "w") as file:
                file.write(text + "\n")
        return
    
    if redirect_type == "stdout_a" and file_path:
        if text is not None:
            with open(file_path, "a") as file:
                file.write(text + "\n")
        return
    
    if redirect_type == "stderr" and file_path:
        with open(file_path, "w"):
            pass
    
    if redirect_type == "stderr_a" and file_path:
        with open(file_path, "a"):
            pass

    if text is not None:
        print(text)

def sanitize(command):
    return [
        ">" if token == "1>"
        else ">>" if token == "1>>"
        else token
        for token in command
    ]
        
def check_redirect(command):
    if "2>>" in command:
        idx = command.index("2>>")
        return command[:idx], "stderr_a", " ".join(command[idx+1:])
    
    elif ">>" in command:
        idx = command.index(">>")
        return command[:idx], "stdout_a", " ".join(command[idx+1:])

    elif "2>" in command:
        idx = command.index("2>")
        return command[:idx], "stderr", " ".join(command[idx+1:])

    elif ">" in command:
        idx = command.index(">")
        return command[:idx], "stdout", " ".join(command[idx+1:])

    return command, None, None

class shell_builtins:
    MEMBERS = ["echo", "exit", "type", "pwd", "cd"]

    def __init__(self, command):
        self.exec = command[0]
        self.args = command[1:]

    def run(self):
        match self.exec:
            case "echo":
                return self.echo()

            case "pwd":
                return self.pwd()

            case "cd":
                return self.cd()

            case "type":
                return self.type()

    def echo(self):
        return " ".join(self.args)

    def pwd(self):
        return os.getcwd()

    def cd(self):
        to_path = " ".join(self.args)

        if to_path == "~":
            os.chdir(os.environ["HOME"])

        elif os.path.isdir(to_path):
            os.chdir(to_path)

        else:
            return f"cd: {to_path}: No such file or directory"

    def type(self):
        arg = " ".join(self.args)

        if arg in shell_builtins.MEMBERS:
            return f"{arg} is a shell builtin"

        if arg in COMMANDS:
            return f"{arg} is {COMMANDS[arg]}"

        return f"{arg}: not found"

def completer(text, state):
    candidates = list(COMMANDS.keys()) + shell_builtins.MEMBERS

    matches = [x for x in candidates if x.startswith(text)]

    if state < len(matches):
        return matches[state] + " "

    return None


def main():
    global COMMANDS
    COMMANDS = {}
    for dir in os.environ["PATH"].split(os.pathsep):
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                path = os.path.join(dir, file)
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    COMMANDS[file] = path
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        command = input("$ ")
        if not command:
            continue

        parsed_command = sanitize(parser(command))
        parsed_command, redirect_type, file_path = check_redirect(parsed_command)
        com = parsed_command[0]

        if com == "exit":
            break

        elif com in shell_builtins.MEMBERS:
            out = shell_builtins(parsed_command).run()
            redirect(out, redirect_type, file_path)

        elif com in COMMANDS :
            if redirect_type == "stdout":
                with open(file_path, "w") as file:
                    subprocess.run([COMMANDS[com], *parsed_command[1:]], stdout=file)

            elif redirect_type == "stderr":
                with open(file_path, "w") as file:
                    subprocess.run([COMMANDS[com], *parsed_command[1:]], stderr=file)
            
            elif redirect_type == "stdout_a" :
                with open(file_path, "a") as file :
                    subprocess.run([COMMANDS[com], *parsed_command[1:]], stdout=file)

            elif redirect_type == "stderr_a":
                with open(file_path, "a") as file:
                    subprocess.run([COMMANDS[com], *parsed_command[1:]], stderr=file)

            else:
                subprocess.run(parsed_command)

        else:
            print(f"{com}: command not found")


if __name__ == "__main__":
    main()
