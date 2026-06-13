# Smart Resume AI - Git History Reset Guide

This guide details the commands to delete the existing commit history of this repository and perform a fresh first commit under your ownership.

---

## Reset Commands

Execute the following commands in order inside your terminal at the root of the project:

```powershell
# 1. Delete the existing local Git history folder
rmdir /s /q .git

# 2. Re-initialize a fresh local Git repository
git init

# 3. Stage all files for tracking
git add .

# 4. Create the first commit
git commit -m "Initial production release"

# 5. Rename the default branch to 'main'
git branch -M main

# 6. Bind the remote repository URL
git remote add origin https://github.com/IamNamanSingh/Smart-Resume-AI.git

# 7. Force push the clean branch history to GitHub
git push -f -u origin main
```

---

## Detailed Command Explanation

### 1. `rmdir /s /q .git`
Deletes the `.git/` folder containing all previous logs, commits, branches, and tags. This starts the repository with a completely clean slate. 
*(Note: If running on macOS or Linux, use `rm -rf .git` instead.)*

### 2. `git init`
Creates a brand-new local Git repository, initializing an empty `.git/` directory.

### 3. `git add .`
Stages all files in the current workspace (honoring exclusions inside `.gitignore`) to prepare them for the initial commit.

### 4. `git commit -m "Initial production release"`
Creates a snapshot commit of the staged files with the specified release comment message.

### 5. `git branch -M main`
Forces the local branch name to be `main`, adhering to current modern repository standards.

### 6. `git remote add origin https://github.com/IamNamanSingh/Smart-Resume-AI.git`
Registers the target GitHub repository URL as the remote destination named `origin`.

### 7. `git push -f -u origin main`
Force pushes (`-f`) the newly generated branch history to the remote repository and sets (`-u`) the default upstream tracking branch.
