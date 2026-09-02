# Copilot Instructions for This Repository

## Build, test, and lint commands

This repository contains multiple standalone Python implementations of the same assignment (`Claude/`, `Codex/`, `Me/`). There is no centralized build system or lint/test runner configured.

Run commands from the implementation folder you are working on:

| Purpose | Command |
|---|---|
| Start server | `python fileserver.py` |
| Start client | `python client.py` |
| Single transfer check (PowerShell) | `'test.txt' \| python client.py` |
| Syntax check a file | `python -m py_compile client.py` or `python -m py_compile fileserver.py` |

Use two terminals for transfer checks: start `fileserver.py` first, then run `client.py`.

## High-level architecture

The codebase is organized as parallel variants of one TCP file-transfer assignment:

- `Claude/`: server and client scripts plus sample file and README
- `Codex/`: server and client scripts plus sample file and README
- `Me/`: server and client scripts plus sample file and README
- `Par/readme.md`: additional documentation only

Each variant is a self-contained pair:
1. `fileserver.py` listens on `127.0.0.1:5000`, accepts one client, reads one filename, sends either an error or file bytes.
2. `client.py` connects, sends filename, parses the server response, writes `<name>_downloaded<ext>`, and prints progress.
3. Both scripts exit after a single request/transfer cycle.

## Key conventions

- Keep client/server protocol pairs matched within the same folder. Do not mix `client.py` from one variant with `fileserver.py` from another:
  - `Claude/`: two-step success protocol (`"OK"` then size as a second message), error as plain text.
  - `Codex/`: single header success protocol (`"ACK <size>"`), error as `"File does not exist"`.
  - `Me/`: line-delimited header protocol (`"OK|<size>\n"` or `"ERROR|<message>\n"`).
- Networking constants are defined at module top (`HOST`/`PORT` or `SERVER_IP`/`SERVER_PORT`, plus `BUFFER_SIZE` where used).
- File lookup is relative to the server process working directory; downloaded files are saved in the client working directory with `_downloaded` suffix.
- Implementations are intentionally single-client and single-transfer per run (`listen(1)`, one `accept()`, then shutdown).
