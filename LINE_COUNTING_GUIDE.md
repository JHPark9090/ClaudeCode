# Line Counting Guide - Regular Tracking System

This guide explains how to track lines of code generated on a regular basis using the same rules as **CODE_GENERATION_DETAILED_COUNT.md**.

---

## Line Counting Rules

These are the same rules from CODE_GENERATION_DETAILED_COUNT.md:

1. ✓ Each file creation counts all lines in the file
2. ✓ Each edit counts only the lines changed
3. ✓ Multiple edits to the same file are counted separately
4. ✓ Comments and blank lines are included (part of code structure)
5. ✓ All file types counted: .py, .md, .sh, .txt

---

## Recommended Approach: Git-Based Tracking

**Why Git?**
- Accurately tracks every line added/removed
- Counts each edit separately (perfect for your rules)
- Can view history anytime
- Automatic statistics generation
- Industry-standard version control

---

## Daily Workflow

### Step 1: Work on Your Code

Do your normal work - create files, edit code, etc.

### Step 2: Run Daily Line Count (End of Day)

```bash
bash daily_line_count.sh
```

**Or with custom commit message:**
```bash
bash daily_line_count.sh "Implemented quantum Hydra models"
```

**What it does:**
1. Counts new files (all lines)
2. Counts edited files (added lines only)
3. Generates today's statistics
4. Commits changes to Git
5. Updates LINE_COUNT_LOG.md

**Output example:**
```
================================================================
Daily Line Count - 2025-10-27 10:30:00
================================================================

New files created:
  QuantumHydra.py: 820 lines
  ClassicalHydra.py: 390 lines
Total new file lines: 1210

Modified files:
  compare_quantum_hydra.py: +50 lines
Total modified lines: 50

================================================================
TOTAL LINES GENERATED TODAY: 1260
  New files:      1210 lines
  Modifications:  50 lines
================================================================
```

### Step 3: View Statistics Anytime

```bash
# View today's statistics
bash view_line_stats.sh today

# View last 7 days
bash view_line_stats.sh week

# View last 30 days
bash view_line_stats.sh month

# View all-time statistics
bash view_line_stats.sh all

# View the markdown log
bash view_line_stats.sh log
```

---

## File Descriptions

### 1. daily_line_count.sh

**Purpose**: Main tracking script to run daily

**Features:**
- Automatically initializes Git if needed
- Counts new and modified lines separately
- Updates LINE_COUNT_LOG.md automatically
- Commits changes with statistics in commit message
- Shows cumulative statistics

**When to run**: At the end of each coding session or day

### 2. view_line_stats.sh

**Purpose**: View statistics anytime without committing

**Options:**
- `today` - Today's changes only
- `week` - Last 7 days summary
- `month` - Last 30 days summary
- `all` - All-time statistics (default)
- `log` - Show the markdown log file

### 3. LINE_COUNT_LOG.md (auto-generated)

**Purpose**: Human-readable daily log

**Format:**
```markdown
## 2025-10-27

**Total: 1260 lines**

- New files: 1210 lines
- Modifications: 50 lines

<details>
<summary>Files changed (click to expand)</summary>

\`\`\`
A  QuantumHydra.py
M  compare_quantum_hydra.py
\`\`\`

</details>
```

---

## Initial Setup

### First Time Setup

```bash
# Make scripts executable
chmod +x daily_line_count.sh view_line_stats.sh

# Run initial commit (if not already using Git)
bash daily_line_count.sh "Initial commit"
```

This will:
1. Initialize Git repository
2. Commit all existing files
3. Create LINE_COUNT_LOG.md

---

## Example Usage Scenarios

### Scenario 1: Daily Tracking

**Morning:**
```bash
# Start working...
```

**Evening:**
```bash
# Commit day's work and count lines
bash daily_line_count.sh "Day 1: Implemented quantum circuits"

# Output:
# TOTAL LINES GENERATED TODAY: 850
#   New files:      820 lines
#   Modifications:  30 lines
```

### Scenario 2: Multiple Sessions Per Day

**Session 1 (Morning):**
```bash
# Work on feature A
bash daily_line_count.sh "Morning: Started feature A"
# Output: 500 lines
```

**Session 2 (Afternoon):**
```bash
# Work on feature B
bash daily_line_count.sh "Afternoon: Completed feature B"
# Output: 300 lines
```

**View total for today:**
```bash
bash view_line_stats.sh today
# Shows combined: 800 lines today
```

### Scenario 3: Weekly Review

```bash
bash view_line_stats.sh week

# Output:
# Last 7 days:
# 2025-10-27 - Day 4: Fixed batch scripts (1188 lines)
# 2025-10-26 - Day 3: Quantum Hydra implementation (6444 lines)
# 2025-10-24 - Day 2: QCNN comparison (16708 lines)
# 2025-10-23 - Day 1: Initial setup (11872 lines)
```

---

## Advanced Usage

### View Detailed Git History

```bash
# See all commits with file statistics
git log --stat

# See commits from last week
git log --since="1 week ago" --stat

# See what changed in specific commit
git show <commit-hash> --stat

# Compare two dates
git diff --stat \
  $(git rev-list -1 --before="2025-10-23" HEAD) \
  $(git rev-list -1 --before="2025-10-27" HEAD)
```

### Generate Monthly Report

```bash
# Lines added per day in October
git log --since="2025-10-01" --until="2025-10-31" \
  --pretty=format:"%ad" --date=short | sort | uniq -c

# Total lines in October
git diff --stat \
  $(git rev-list -1 --before="2025-10-01" HEAD) \
  $(git rev-list -1 --before="2025-11-01" HEAD)
```

### Count Lines by Author (if multiple people)

```bash
git log --author="Claude" --pretty=tformat: --numstat | \
  awk '{added += $1; removed += $2} END {print "Added:", added, "Removed:", removed}'
```

---

## Comparison with Manual Counting

| Method | Accuracy | Ease of Use | Tracks Edits Separately | Historical View |
|--------|----------|-------------|------------------------|-----------------|
| **Git-based (Recommended)** | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| Manual log file | ✓ | ✓ | ✓ (if diligent) | ✓ |
| File watching script | ✓✓ | ✓✓ | ✗ (hard to track) | ✓ |
| Manual counting | ✓ | ✗ | ✗ | ✗ |

---

## Tips for Accurate Tracking

### 1. Commit Frequently
```bash
# Good: Multiple commits per day
bash daily_line_count.sh "Morning: Feature A"
bash daily_line_count.sh "Afternoon: Feature B"

# Less accurate: One commit for entire week
```

### 2. Use Descriptive Commit Messages
```bash
# Good
bash daily_line_count.sh "Implemented 3 new optimizers (SPSA, CMA, PSO)"

# Less useful
bash daily_line_count.sh "Updates"
```

### 3. Review Before Committing
```bash
# Check what's changed
git status
git diff --stat

# Then commit
bash daily_line_count.sh "Detailed description"
```

### 4. Keep LINE_COUNT_LOG.md Updated
The log file is automatically updated each time you run `daily_line_count.sh`. Review it periodically:
```bash
bash view_line_stats.sh log
```

---

## Troubleshooting

### Problem: Git not initialized

**Solution:**
```bash
bash daily_line_count.sh
# Script will automatically initialize Git
```

### Problem: Want to exclude certain files

**Solution:** Create `.gitignore`:
```bash
cat > .gitignore << EOF
# Ignore these from line counts
__pycache__/
*.pyc
.ipynb_checkpoints/
conda-cache/
conda-envs/
EOF
```

### Problem: Need to count retroactively

**Solution:** If you already have commits:
```bash
# Count lines between two dates
git diff --stat \
  $(git rev-list -1 --before="2025-10-23" HEAD)..HEAD

# Or use the existing CODE_GENERATION_DETAILED_COUNT.md
cat CODE_GENERATION_DETAILED_COUNT.md
```

### Problem: Accidentally committed wrong files

**Solution:**
```bash
# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Check what would be committed
git status

# Re-commit with correct files
bash daily_line_count.sh "Corrected commit"
```

---

## Alternative: Simple Manual Log (If Git Not Desired)

If you prefer not to use Git, here's a simple manual approach:

```bash
# Create simple log script
cat > log_lines.sh << 'EOF'
#!/bin/bash
DATE=$(date +"%Y-%m-%d")
echo "## $DATE" >> manual_line_log.txt
echo "" >> manual_line_log.txt
echo "Files created/edited:" >> manual_line_log.txt
# Manually list your changes here
echo "  QuantumHydra.py: 820 lines (created)" >> manual_line_log.txt
echo "  README.md: 50 lines (edited)" >> manual_line_log.txt
echo "" >> manual_line_log.txt
EOF

chmod +x log_lines.sh
```

**But Git-based is much better because:**
- Automatic line counting
- Can't forget what you changed
- Complete history tracking
- Industry standard

---

## Summary

**For regular line counting, use this simple workflow:**

1. **Daily**: `bash daily_line_count.sh "Description of work"`
2. **View stats**: `bash view_line_stats.sh [today|week|month|all|log]`
3. **Review**: Check LINE_COUNT_LOG.md periodically

**Benefits:**
- ✓ Follows exact rules from CODE_GENERATION_DETAILED_COUNT.md
- ✓ Counts each edit separately
- ✓ Automatic and accurate
- ✓ Historical tracking
- ✓ No manual effort needed

---

## Quick Reference

```bash
# Daily use
bash daily_line_count.sh                # Commit and count today's work
bash daily_line_count.sh "Custom msg"   # With custom message

# View statistics
bash view_line_stats.sh today           # Today only
bash view_line_stats.sh week            # Last 7 days
bash view_line_stats.sh month           # Last 30 days
bash view_line_stats.sh all             # All time (default)
bash view_line_stats.sh log             # Show markdown log

# Git commands
git log --stat                          # Detailed history
git diff --stat HEAD~1                  # Last commit stats
git status                              # Current changes
```

---

*This tracking system ensures accurate, automated line counting that follows the same rules as your manual detailed count.*
