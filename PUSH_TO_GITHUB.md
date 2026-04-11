# Git & GitHub Push Instructions

## Setup Git Credentials

```bash
# Configure git globally (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Initialize Repository & Push

Navigate to project root:
```bash
cd c:\Users\gsv32\OneDrive\Desktop\Value_at_risk
```

### Step 1: Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: IndiaVaR - Value at Risk Analysis Tool"
```

### Step 2: Add Remote Repository
```bash
git remote add origin https://github.com/gsv3245-cpu/Value_at_Risk.git
```

### Step 3: Create Main Branch & Push
```bash
git branch -M main
git push -u origin main
```

## If Repository Already Has Content

If the GitHub repo already has files (like README), pull first:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Pushing Updates (Future)

After making changes:
```bash
git add .
git commit -m "Clear commit message describing changes"
git push origin main
```

## Verifying Push

Check on GitHub:
1. Go to https://github.com/gsv3245-cpu/Value_at_Risk
2. Verify all files are visible
3. Check commit history

---

## Common Git Commands

```bash
# Check status
git status

# View changes
git diff filename

# View history
git log --oneline (last 10 commits)

# Undo last commit (keep changes)
git reset --soft HEAD^

# Undo changes in a file
git checkout -- filename

# Create a new branch
git checkout -b feature/xyz
git push -u origin feature/xyz

# Switch branches
git checkout main
```

---

## GitHub Best Practices

- Keep commits atomic and focused
- Use clear, descriptive commit messages
- Write PR descriptions explaining changes
- Reference issues in commit messages: `Fixes #123`
- Maintain clean git history (avoid merge commits)

For more help: https://git-scm.com/doc
