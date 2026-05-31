import os
import subprocess
import readline

COMMANDS = {}

class shell_builtins:
    MEMBERS = ["echo", "exit", "type", "pwd", "cd", "complete", "jobs"]
    COMPLETION_SPEC = {}
    JOBS = {}

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
            
            case "complete":
                return self.complete()
            
            case "jobs":
                return self.jobs()

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
    
    def complete(self):
        flag = self.args[0]

        if flag == "-p":
            command = self.args[1]
            if command in shell_builtins.COMPLETION_SPEC :
                spec_path = shell_builtins.COMPLETION_SPEC[command]
                return f"complete -C '{spec_path}' {command}"
            else :
                return f"complete: {command}: no completion specification"
            
        elif flag == "-C":
            spec_path = self.args[1]
            command = self.args[2]
            shell_builtins.COMPLETION_SPEC[command] = spec_path
        
        elif flag == "-r":
            command = self.args[1]
            shell_builtins.COMPLETION_SPEC.pop(command, None)

    def jobs(self):
        for key, val in list(shell_builtins.JOBS.items()):
            keys = sorted(shell_builtins.JOBS.keys())
            highest = keys[-1] if len(keys) >= 1 else None
            second  = keys[-2] if len(keys) >= 2 else None

            if val[0].poll() is None:
                print(f"[{key}]{'+' if key == highest else '-' if key == second else ' '}  Running                 {val[1]}")
            else:
                print(f"[{key}]{'+' if key == highest else '-' if key == second else ' '}  Done                 {val[1][:-1]}")
                shell_builtins.JOBS.pop(key, None)
    
    @staticmethod
    def reap_jobs():
        for key, val in list(shell_builtins.JOBS.items()):
            keys = sorted(shell_builtins.JOBS.keys())
            highest = keys[-1] if len(keys) >= 1 else None
            second  = keys[-2] if len(keys) >= 2 else None
            if val[0].poll() is not None:
                print(f"[{key}]{'+' if key == highest else '-' if key == second else ' '}  Done                 {val[1][:-1]}")
                shell_builtins.JOBS.pop(key, None)

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
        ">" if token == "1>" else ">>" if token == "1>>" else token for token in command
    ]

def check_redirect(command):
    if "2>>" in command:
        idx = command.index("2>>")
        return command[:idx], "stderr_a", " ".join(command[idx + 1 :])

    elif ">>" in command:
        idx = command.index(">>")
        return command[:idx], "stdout_a", " ".join(command[idx + 1 :])

    elif "2>" in command:
        idx = command.index("2>")
        return command[:idx], "stderr", " ".join(command[idx + 1 :])

    elif ">" in command:
        idx = command.index(">")
        return command[:idx], "stdout", " ".join(command[idx + 1 :])

    return command, None, None

def completer(text, state):
    line = readline.get_line_buffer()
    words = line.split()
    cursor = readline.get_endidx()

    if len(words) == 0 or (len(words) == 1 and not line.endswith(" ")):
        candidates = list(COMMANDS.keys()) + shell_builtins.MEMBERS
        matches = [x for x in candidates if x.startswith(text)]
        if state < len(matches):
            return matches[state] + " "
    else:
        if words[0] in shell_builtins.COMPLETION_SPEC :
            spec_file = shell_builtins.COMPLETION_SPEC[words[0]]
            argv = [words[0], text]
            if len(words) >= 2 :
                argv.append(words[-2])
            else :
                argv.append("")

            if os.path.isfile(spec_file) and os.access(spec_file, os.X_OK):
                env = os.environ.copy()
                env["COMP_LINE"] = line
                env["COMP_POINT"] = str(cursor)

                result = subprocess.run(
                    [spec_file, *argv],
                    capture_output=True,
                    text=True,
                    env=env
                )

                candidates = result.stdout.splitlines()
                if state < len(candidates):
                    return candidates[state] + " "

        else :
            idx = text.rfind("/")
            if idx == -1:
                dir_path = "."
                prefix = text
            else:
                dir_path = text[: idx + 1]
                if idx < len(text) - 1:
                    prefix = text[idx + 1 :]
                else:
                    prefix = ""

            matches = []
            for f in os.listdir(dir_path):
                if f.startswith(prefix):
                    full = os.path.join(dir_path, f)
                    if os.path.isdir(full):
                        matches.append(text[: idx + 1] + f + "/")
                    else:
                        matches.append(text[: idx + 1] + f + " ")

            if state < len(matches):
                return matches[state]
            return None

    return None

def build_commands():
    commands = {}
    seen = set()
    for dir in os.environ.get("PATH", "").split(os.pathsep):
        if dir in seen or not os.path.isdir(dir):
            continue
        seen.add(dir)
        for entry in os.scandir(dir):
            if entry.is_file() and os.access(entry.path, os.X_OK):
                commands[entry.name] = entry.path
    return commands

def setup_readline():
    readline.set_completer_delims(" \t\n")
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

def parse_input(command):
    parsed_command = sanitize(parser(command))
    command_type = "foregorund"
    if parsed_command[-1] == "&" :
        command_type = "background"
        parsed_command = parsed_command[:-1]
    
    if "|" in parsed_command:
        commands = []
        current = []
        for token in parsed_command:
            if token == "|":
                commands.append(current)
                current = []
            else:
                current.append(token)
        commands.append(current)
        return commands, None, None, "pipe"
    
    parsed_command, redirect_type, file_path = check_redirect(parsed_command)
    return parsed_command, redirect_type, file_path, command_type

def run_builtin(parsed_command,  redirect_type, file_path, command_type):
    out = shell_builtins(parsed_command).run()
    redirect(out, redirect_type, file_path)

def run_external(parsed_command,   redirect_type, file_path, command_type):

    if command_type == "background":
        i = 1
        while i in shell_builtins.JOBS:
            i += 1
        proc = subprocess.Popen(parsed_command)
        shell_builtins.JOBS[i] = [proc, " ".join(parsed_command) + " &"]
        print(f"[{i}] {proc.pid}")
        return
    

    if redirect_type == "stdout":
        with open(file_path, "w") as file:
            subprocess.run(parsed_command, stdout=file)

    elif redirect_type == "stderr":
        with open(file_path, "w") as file:
            subprocess.run(parsed_command, stderr=file)

    elif redirect_type == "stdout_a":
        with open(file_path, "a") as file:
            subprocess.run(parsed_command, stdout=file)

    elif redirect_type == "stderr_a":
        with open(file_path, "a") as file:
            subprocess.run(parsed_command, stderr=file)

    else:
        subprocess.run(parsed_command)

def run_pipe(commands):
    procs = []
    prev_out = None 

    for i, cmd in enumerate(commands):
        is_last = i == len(commands) - 1

        if cmd[0] in shell_builtins.MEMBERS:
            out = shell_builtins(cmd).run() or ""
            if is_last:
                print(out)
            else:
                prev_out = (out + "\n").encode()
        else:
            stdin = subprocess.PIPE if prev_out else (procs[-1].stdout if procs else None)
            stdout = subprocess.PIPE if not is_last else None
            p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout)
            if prev_out:
                p.stdin.write(prev_out)
                p.stdin.close()
                prev_out = None
            procs.append(p)

    for p in procs:
        p.wait()

def main():
    global COMMANDS
    COMMANDS = build_commands()
    setup_readline()

    while True:

        #Reaping the jobs
        shell_builtins.reap_jobs()

        command = input("$ ")
        if not command:
            continue

        parsed_command, redirect_type, file_path , command_type = parse_input(command)
        com = parsed_command[0][0] if command_type == "pipe" else parsed_command[0]

        if com == "exit":
            break

        elif command_type == "pipe":
            run_pipe(parsed_command)

        elif com in shell_builtins.MEMBERS:
            run_builtin(parsed_command, redirect_type, file_path, command_type)

        elif com in COMMANDS:
            run_external(parsed_command, redirect_type, file_path, command_type)

        else:
            print(f"{com}: command not found")


if __name__ == "__main__":
    main()
