# Getting Started

This is your 15-month AI engineer transition plan execution hub.

---

## 🚀 First Things to Do (This Week)

### Step 1: Set up your repo locally (15 min)
```bash
cd ~/learn/ai-engineer-transition

# Create folder structure
mkdir -p progress/{months,projects}
mkdir -p src
mkdir -p resources
mkdir -p docs

# Copy the files from this guide into their places:
# - README.md (main)
# - progress/README.md
# - progress/daily-log.md
# - progress/months/month-1.md
# - progress/projects/project-1-kaggle.md
# - .gitignore
```

### Step 2: Configure Git (5 min)
```bash
cd ~/learn/ai-engineer-transition

# Set personal account config for this repo
git config user.name "Your Name"
git config user.email "your.personal@email.com"

# Verify
git config user.email
```

### Step 3: Make first commit (5 min)
```bash
git add .
git commit -m "Initial commit: AI engineer transition plan setup"
git push origin main
```

### Step 4: Create GitHub Project (optional but recommended, 10 min)
- Go to your repo on github.com
- Click "Projects" → "New project"
- Choose "Table" view
- Add columns: Backlog, This Week, In Progress, Review, Done
- Create issues for Week 1 tasks

### Step 5: Update dates (2 min)
Edit these files and add today's date:
- `README.md` → "Start date"
- `progress/README.md` → "Start Date"
- `progress/months/month-1.md` → "Started"
- `progress/daily-log.md` → "Week of"

---

## 📋 Weekly Workflow

**Every Sunday (6 PM)**:
1. Review last week in `daily-log.md`
2. Reflect (wins, blockers, learnings)
3. Create new `daily-log.md` for this week
4. Update `progress/README.md` if major milestones hit
5. Plan this week

**Daily (7–8 PM)**:
1. Study (watch videos, read docs)
2. At end of day: Add one-liner to `daily-log.md`
3. Push to GitHub (so you have a backup)

**Daily (11 PM–12 AM)**:
1. Hands-on coding (practice problems, start projects)
2. Commit code to GitHub

**Every Friday (5 PM)**:
1. Weekly reflection in `daily-log.md`
2. Update `progress/months/month-X.md` with progress
3. Plan next week
4. Push everything to GitHub

---

## 🎯 Month 1 Quick Checklist

**This is what you're doing THIS month:**

- [ ] Watch 3Blue1Brown Linear Algebra (4 hours)
- [ ] Learn StatQuest probability basics (3 hours)
- [ ] Complete Kaggle Learn: Pandas + Data Viz (4 hours)
- [ ] Start Andrew Ng ML Specialization Week 1 (2 hours)
- [ ] Choose a Kaggle dataset
- [ ] Create EDA notebook (Project 1 starts)
- [ ] Train a simple baseline model
- [ ] Push Project 1 start to GitHub

**Total time**: ~40 hours (10 hours/week)

---

## 📂 File Locations & When to Update

| File | Purpose | Update When |
|------|---------|-------------|
| `README.md` | Main overview | Every milestone (monthly) |
| `progress/README.md` | Current status | Every week Friday |
| `progress/daily-log.md` | Daily tracking | Every day |
| `progress/months/month-X.md` | Month reflection | Every Friday |
| `progress/projects/project-X.md` | Project status | Every project milestone |
| `src/` | Your code | Commit after coding sessions |

---

## 🔄 Git Workflow for Coding

When you're building a project (e.g., Project 1):

```bash
# Create a feature branch
git checkout -b project-1-eda

# Work on your code
# ... write code, test it ...

# Commit frequently
git add src/project-1-kaggle/
git commit -m "Project 1: Add data exploration notebook"

# Push to GitHub
git push origin project-1-eda

# When done, merge to main
git checkout main
git pull origin main
git merge project-1-eda
git push origin main
```

---

## 📊 Tracking Your Progress

### Visual Progress
- Open `progress/README.md` to see overall status
- Update project tables as you deliver

### Burndown
- Track hours per week in `daily-log.md`
- Target: 15–20 hours/week for next 8 months

### GitHub
- Your commit history will show consistency
- Employers will see: steady progress over 15 months

---

## 🎓 Learning Resources

All resources are listed in `README.md` > Resources section.

**Start with Week 1**:
1. 3Blue1Brown Essence of Linear Algebra (Videos 1-3)
   - https://www.3blue1brown.com/topics/linear-algebra
2. StatQuest Probability Playlist
   - https://www.youtube.com/@statquest/search?query=probability
3. Kaggle Learn Pandas
   - https://www.kaggle.com/learn/pandas

---

## ⚠️ Common Pitfalls

1. **Don't skip daily logging** — consistency matters more than speed
2. **Don't build perfect projects** — ship early, iterate
3. **Don't fall behind on commits** — push to GitHub weekly
4. **Don't ignore blockers** — log them and solve them
5. **Don't do only theory** — code every day

---

## 🆘 If You Get Stuck

1. **On a topic**: Spend 30 min, then move on. Come back later.
2. **On a project**: Break it into smaller tasks. Do one task at a time.
3. **Motivation**: Look at your commit history. You're making progress.
4. **Time**: If you fall behind, adjust weeks, not the plan. Skip nice-to-haves.

---

## Next: Week 1 Tasks

```
❌ Choose dataset for Project 1
❌ Watch 3Blue1Brown LA Videos 1-3
❌ Set up Python env (NumPy, Pandas, Matplotlib)
❌ Do first daily-log.md entry
❌ Push to GitHub
```

---

**Ready to start? Begin with the 3Blue1Brown videos. You've got this!** 🚀
