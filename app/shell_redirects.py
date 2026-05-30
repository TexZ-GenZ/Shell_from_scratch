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
