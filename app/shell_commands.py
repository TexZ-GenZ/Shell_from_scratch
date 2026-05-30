import os


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
