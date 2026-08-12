# Setup Guidelines (Git Basics)

If you haven't used Git/GitHub much before, this doc walks you through everything you need for this assignment, step by step. Don't worry about getting it perfect — the goal is just to get your work committed and pushed so we can review it.

## 1. Install Git

If you don't already have Git installed:

- **Windows:** download and install from [git-scm.com](https://git-scm.com/downloads)
- **Mac:** run `git --version` in Terminal — it'll prompt you to install if missing
- **Linux:** `sudo apt install git` (or your distro's equivalent)

Check it worked:

```bash
git --version
```

## 2. Clone the Repo

This downloads a copy of the repo to your machine.

```bash
git clone https://github.com/Rohanmrao/kangasys-intern-take-home.git
cd kangasys-intern-take-home
```

## 3. Create Your Own Branch

**Do not commit directly to `master`.** Create a new branch off of `master` and do all your work there — this is what we'll review.

```bash
git checkout master
git pull origin master
git checkout -b your-name/device-monitoring-service
```

Example: `neethu/device-monitoring-service`. Branch name doesn't need to be exact — just something clear and yours.

## 4. Do Your Work, Commit as You Go

Don't wait until everything is done to make one giant commit. Commit as you make progress — after setting up the project skeleton, after each feature, after adding tests, etc. We'll be reviewing your commit history too, so a series of small, sensible commits tells us more about how you worked than one big dump at the end.

Basic cycle:

```bash
# check what's changed
git status

# stage the files you want to commit
git add <file-or-folder>
# or, to stage everything you've changed
git add .

# commit with a short, clear message
git commit -m "Add device CRUD endpoints"

# push your branch to GitHub
git push origin your-name/device-monitoring-service
```

The first time you push a new branch, Git may ask you to run:

```bash
git push --set-upstream origin your-name/device-monitoring-service
```

After that, `git push` on its own is enough.

## 5. Keep Pushing

Push regularly — don't just push once at the very end. This is how we track your progress and thought process over the 3 days. There's no such thing as "too many commits."

## 6. Questions? Raise a GitHub Issue

If anything in the problem statement is unclear, or you hit a blocker you want to flag, open a GitHub Issue on the repo rather than guessing silently — asking a good clarifying question is a positive signal, not a negative one.

1. Go to the repo on GitHub: `https://github.com/Rohanmrao/kangasys-intern-take-home`
2. Click the **Issues** tab
3. Click **New Issue**
4. Give it a short title (e.g. "Clarification on alert resolution behavior") and describe your question in the body
5. Click **Submit new issue**

We'll reply on the issue thread.

## 7. Submission

You don't need to open a Pull Request or merge anything. Your branch, with all your commits pushed to GitHub, **is** your submission. When you're done (or time's up), just make sure your latest work is pushed and let us know your branch name.

## Quick Reference

| What you want to do | Command |
|---|---|
| See what's changed | `git status` |
| Stage a file | `git add <file>` |
| Stage everything | `git add .` |
| Commit staged changes | `git commit -m "message"` |
| Push your branch | `git push origin <branch-name>` |
| Switch branches | `git checkout <branch-name>` |
| Create + switch to a new branch | `git checkout -b <branch-name>` |
| Pull latest changes | `git pull origin master` |
