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


def parse_input(command):
    parsed_command = sanitize(parser(command))
    return check_redirect(parsed_command)
