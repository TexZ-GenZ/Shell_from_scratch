import os
import readline

import shell_state
from shell_builtins import shell_builtins


def completer(text, state):
    line = readline.get_line_buffer()
    words = line.split()
    if len(words) == 0 or (len(words) == 1 and not line.endswith(" ")):
        candidates = list(shell_state.COMMANDS.keys()) + shell_builtins.MEMBERS
        matches = [x for x in candidates if x.startswith(text)]
        if state < len(matches):
            return matches[state] + " "
    else:
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


def setup_readline():
    readline.set_completer_delims(" \t\n")
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
