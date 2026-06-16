---
name: codex-reconnecting-solve
description: Diagnose and fix Codex Desktop reconnecting loops on Windows when a local proxy, HTTP_PROXY/HTTPS_PROXY variables, TUN mode, global proxy mode, or a misplaced env file may be involved. Use when Codex keeps reconnecting or the user wants Codex to work through a local proxy without enabling global proxy or TUN mode.
---

# Codex Reconnecting Solve

## Goal

Fix Codex Desktop reconnecting on Windows by making Codex inherit working user-level proxy environment variables. Do not assume a `.env` file is automatically loaded.

Success criteria:

- Identify the actual local proxy port that is listening.
- Write `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY` to the Windows user environment.
- Verify `HKCU\Environment` contains the values.
- Tell the user to fully restart Codex, or restart Windows if Codex was already running.

## Workflow

1. Inspect existing files and environment:

```powershell
Get-Content -Raw -LiteralPath "$env:USERPROFILE\.codex\1.env" -ErrorAction SilentlyContinue
reg query HKCU\Environment
Get-ChildItem Env:HTTP_PROXY,Env:HTTPS_PROXY,Env:ALL_PROXY,Env:NO_PROXY -ErrorAction SilentlyContinue
```

2. Find candidate local proxy ports. Prefer the ports that are actually listening over whatever is written in an env file:

```powershell
netstat -ano | findstr "LISTENING"
```

Common ports include `6528`, `7890`, `7897`, `1080`, `10808`, `10809`, `20171`, and `2080`.

3. Test the likely HTTP proxy port:

```powershell
curl.exe -I -x http://127.0.0.1:PORT https://api.openai.com --connect-timeout 10 --ssl-no-revoke
```

Treat `HTTP/1.1 200 Connection established` as strong evidence that the port is an HTTP CONNECT proxy, even if Windows curl later reports a Schannel credential/certificate error. A `405 Method Not Allowed` response to CONNECT usually means that port is not an HTTP proxy tunnel.

4. Apply the fix with the bundled script. If the port is known:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\fix_codex_proxy_windows.ps1" -Port PORT
```

If the port is unknown, let the script try common ports:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\fix_codex_proxy_windows.ps1"
```

5. Verify persistence:

```powershell
reg query HKCU\Environment /v HTTP_PROXY
reg query HKCU\Environment /v HTTPS_PROXY
reg query HKCU\Environment /v ALL_PROXY
reg query HKCU\Environment /v NO_PROXY
```

6. Restart requirements:

Environment variables only affect newly launched processes. Ask the user to fully quit Codex, ensure `codex.exe` is gone from Task Manager, then reopen Codex. If reconnecting continues, restart Windows once.

## Notes

- A file like `%USERPROFILE%\.codex\1.env` is useful as a record, but Codex Desktop may not automatically load it.
- Global proxy mode and TUN mode are not required when Codex inherits `HTTP_PROXY` and `HTTPS_PROXY`.
- If `reg query HKCU\Environment` does not show the proxy values after running a script, use `setx` directly or rerun the bundled script.
- If the proxy app changes ports, update the environment variables to the new port and restart Codex again.