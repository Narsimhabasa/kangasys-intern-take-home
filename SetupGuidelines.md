# Setup Guidelines (Git Basics)

If you haven't used Git/GitHub much before, this doc walks you through everything you need for this assignment, step by step. Don't worry about getting it perfect — the goal is just to get your work committed and pushed so we can review it.

**The short version:** fork this repo to your own GitHub account, do all your work there, then open a Pull Request back to us when you're done.

> **Please do not push branches directly to this repo.** You won't have write access anyway — all your work belongs in *your* fork.

## 1. Install Git

If you don't already have Git installed:

- **Windows:** download and install from [git-scm.com](https://git-scm.com/downloads)
- **Mac:** run `git --version` in Terminal — it'll prompt you to install if missing
- **Linux:** `sudo apt install git` (or your distro's equivalent)

Check it worked:

```bash
git --version
```

You'll also need a free GitHub account — sign up at [github.com](https://github.com) if you don't have one.

## 2. Fork the Repo

A "fork" is your own personal copy of a repo, under your own GitHub account. You can push to it freely without affecting the original.

1. Go to the repo on GitHub: `https://github.com/Rohanmrao/kangasys-intern-take-home`
2. Click the **Fork** button (top right)
3. Leave the settings as they are and click **Create fork**

You'll land on your own copy, at a URL like `https://github.com/YOUR-USERNAME/kangasys-intern-take-home`.

## 3. Clone *Your Fork*

This downloads your fork to your machine. Note the URL uses **your** username, not ours.

```bash
git clone https://github.com/YOUR-USERNAME/kangasys-intern-take-home.git
cd kangasys-intern-take-home
```

## 4. Create a Branch in Your Fork

Inside your fork, make a branch to work on. This keeps your work tidy and makes the Pull Request clean at the end.

```bash
git checkout -b device-monitoring-service
```

Branch name doesn't need to be exact — just something clear.

## 5. Do Your Work, Commit as You Go

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

# push your branch to your fork
git push origin device-monitoring-service
```

The first time you push a new branch, Git may ask you to run:

```bash
git push --set-upstream origin device-monitoring-service
```

After that, `git push` on its own is enough.

## 6. Keep Pushing

Push regularly — don't just push once at the very end. Pushing as you go means that if something goes wrong on your machine, your work is safe, and it lets us see how the solution came together over the 3 days. There's no such thing as "too many commits."

## 7. Open a Pull Request When You're Done

A Pull Request (PR) is how you formally submit your work back to us. **This is your submission.**

1. Push your final commits (see above)
2. Go to your fork on GitHub — you'll usually see a banner saying *"Compare & pull request"*. Click it. (If you don't see it, go to the **Pull requests** tab and click **New pull request**.)
3. Make sure the direction is right:
   - **base repository:** `Rohanmrao/kangasys-intern-take-home`, **base:** `master`
   - **head repository:** `YOUR-USERNAME/kangasys-intern-take-home`, **compare:** `device-monitoring-service`
4. Give it a clear title (e.g. *"Device Monitoring Service — Your Name"*)
5. In the description, add a short summary: what you built, what you'd do with more time, and any assumptions you made
6. Click **Create pull request**

Don't worry about merging it — we'll take it from there. You can keep pushing commits to your branch after opening the PR; they'll show up on the PR automatically, so feel free to open it early if you like.

**Important:** keep your fork public (or add us as a collaborator) so we can actually see the code.

## 8. Questions? Raise a GitHub Issue

If anything in the problem statement is unclear, or you hit a blocker you want to flag, open a GitHub Issue on **our** repo rather than guessing silently — asking a good clarifying question is a positive signal, not a negative one.

1. Go to `https://github.com/Rohanmrao/kangasys-intern-take-home`
2. Click the **Issues** tab
3. Click **New Issue**
4. Give it a short title (e.g. "Clarification on alert resolution behavior") and describe your question in the body
5. Click **Submit new issue**

We'll reply on the issue thread.

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

## Recap

1. **Fork** our repo → 2. **Clone** your fork → 3. **Branch** → 4. **Commit & push** as you go → 5. **Open a PR** back to us
