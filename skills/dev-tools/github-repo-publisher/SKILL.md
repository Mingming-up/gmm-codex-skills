---
name: github-repo-publisher
description: Publish a local project or newly prepared repository to GitHub end to end. Use when the user asks Codex to create a GitHub repository, push a local project to GitHub, upload a local repo, create a public/private GitHub repo, or repeat the gmm-codex-skills workflow. Covers GitHub connector limitations, GitHub CLI fallback, Git Credential Manager plus REST API repository creation, remote setup, push, and verification.
---

# GitHub Repo Publisher

## Overview

Publish the local repository all the way to GitHub. Prefer the simplest authenticated path available, but do not stop just because the GitHub connector lacks a create-repository tool.

## Workflow

1. Confirm the target repository name, owner, visibility, and whether README/license/gitignore should be created remotely.
2. Inspect the local project:
   - Run `git status --short --branch`.
   - If it is not a Git repository, initialize it on `main`.
   - Commit the intended files before pushing.
   - For public repos, scan for obvious secrets and local-only paths before push.
3. Resolve the GitHub owner:
   - If the GitHub connector has `_get_user_login`, use it.
   - Otherwise use a user-provided owner or infer only when already clear from an existing remote.
4. Create the remote repository using the best available method:
   - First choice: `gh repo create <owner>/<repo> --public|--private --source . --remote origin --push` when `gh` exists and is authenticated.
   - If `gh` is unavailable, use Git Credential Manager credentials with the GitHub REST API.
   - If an existing repository is provided, skip creation and configure `origin`.
5. Push and verify:
   - Run `git push -u origin main`.
   - Confirm with `git status --short --branch`.
   - If available, call the GitHub connector's `_get_repo` to verify visibility, default branch, permissions, and URL.

## REST API Fallback

Use this route when:

- `gh` is not installed or not authenticated.
- The GitHub connector is authenticated but exposes only existing-repo operations, not create-repo.
- Git Credential Manager already has usable GitHub credentials.

PowerShell pattern:

```powershell
$ErrorActionPreference = 'Stop'
$inputText = "protocol=https`nhost=github.com`n`n"
$cred = $inputText | git credential fill
$user = ($cred | Where-Object { $_ -like 'username=*' } | Select-Object -First 1) -replace '^username=', ''
$pass = ($cred | Where-Object { $_ -like 'password=*' } | Select-Object -First 1) -replace '^password=', ''
if ([string]::IsNullOrWhiteSpace($pass)) { throw 'No GitHub credential available from git credential fill.' }

$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$user`:$pass"))
$body = @{
  name = '<repo-name>'
  private = $false
  auto_init = $false
  description = '<short description>'
} | ConvertTo-Json -Compress

Invoke-RestMethod `
  -Method Post `
  -Uri 'https://api.github.com/user/repos' `
  -Headers @{
    Authorization = "Basic $basic"
    Accept = 'application/vnd.github+json'
    'X-GitHub-Api-Version' = '2022-11-28'
    'User-Agent' = 'codex-repo-publisher'
  } `
  -Body $body `
  -ContentType 'application/json'
```

Do not print `$pass`, `$basic`, or full credential output. Only report the created repository full name and URL.

## Push Details

Set or update the remote:

```powershell
git remote add origin https://github.com/<owner>/<repo>.git
```

If `origin` already exists:

```powershell
git remote set-url origin https://github.com/<owner>/<repo>.git
```

Push:

```powershell
git push -u origin main
```

When escalated commands run as a different Windows user and Git reports `dubious ownership`, avoid changing global config. Use a one-shot safe directory override:

```powershell
git -c safe.directory=<absolute-repo-path> push -u origin main
```

## Failure Handling

- `Repository not found` during push usually means the remote repository does not exist, the owner is wrong, or credentials lack access.
- A working GitHub connector login does not prove repository creation is available; inspect exposed tools before assuming.
- If REST creation returns `422 name already exists`, fetch the repo metadata and either push to the existing repo or ask whether to use a different name.
- If Git Credential Manager has no credential, ask the user to authenticate GitHub CLI, sign in through Git Credential Manager, or provide a different approved path.
