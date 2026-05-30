import subprocess

from shell_builtins import shell_builtins
from shell_redirects import redirect


def run_builtin(parsed_command, redirect_type, file_path):
    out = shell_builtins(parsed_command).run()
    redirect(out, redirect_type, file_path)


def run_external(parsed_command, redirect_type, file_path):
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
