# Egg Shell (Python)

A small, POSIX-inspired shell built for the CodeCrafters "Build Your Own Shell"
challenge. It supports a set of core shell behaviors, builtins, and utilities
implemented in Python.

## What this shell can do

- Builtins: `echo`, `pwd`, `cd`, `type`, `complete`, `jobs`, `history`, `declare`, `exit`
- External commands by searching `PATH`
- Quoting and escapes for single quotes, double quotes, and backslashes
- Pipes with `|` between commands
- Redirections: `>`, `>>`, `1>`, `1>>`, `2>`, `2>>`
- Background jobs via `&` with `jobs` listing
- Tab completion for commands and file paths
- Basic variable expansion via `declare` and `$VAR` or `${VAR}`
- History support (including `-r`, `-w`, `-a`) and optional `HISTFILE`

## Project layout

- [app/main.py](app/main.py): core shell implementation
- [egg-shell.sh](egg-shell.sh): local runner script (uses `uv`)

## Run locally

This project uses `uv` to run the shell. If you do not have it installed, see
https://docs.astral.sh/uv/ for installation instructions.

```sh
./egg-shell.sh
```

### Optional: run directly with Python

If you prefer to run without `uv`, make sure you have Python 3.14+ available
and run:

```sh
python -m app.main
```

## Development notes

- The shell loads commands from `PATH` on startup.
- If `HISTFILE` is set, history is read and appended on exit.
- Completion specs can be registered using `complete -C <path> <command>`.


