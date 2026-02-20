# Mission Control - Task Management Dashboard

**Version:** 2.3.1 (from ClawHub)
**Author:** rdsthomas
**Status:** ✅ Installed and configured

---

## 🎯 What is Mission Control?

A **Kanban-style task management system** designed for AI assistants. You create and prioritize tasks via a web dashboard; the agent executes them automatically when moved to "In Progress".

### The Workflow

```
You create task → Move to "In Progress" → Agent receives work order
                                              ↓
                                   Agent executes task
                                              ↓
Agent updates status → Moves to "Review" → You approve → "Done"
```

---

## ✅ Installation Complete

### Dashboard Files
- ✅ **index.html** (290 KB) - Full-featured dashboard UI
- ✅ **data/tasks.json** - Task database with sample data
- ✅ **Config file** - `~/.clawdbot/mission-control.json`

### CLI Tool
- ✅ **mc-update.sh** - Installed and symlinked to `/usr/local/bin/mc-update.sh`
- ✅ Executable from anywhere

### Sample Tasks Included
1. 🚀 **Onboarding Guide** - Setup instructions
2. 📖 **User Guide** - How to use Mission Control
3. **Example Task** - Template for new tasks

---

## 🚀 Quick Start

### Option 1: Local Access (Works Now)

```bash
# Open dashboard in browser
xdg-open /root/.openclaw/workspace/index.html

# Or open the file directly in your browser
file:///root/.openclaw/workspace/index.html
```

### Option 2: GitHub Pages (Recommended for Remote Access)

1. **Push workspace to GitHub (if not already):**
   ```bash
   cd /root/.openclaw/workspace
   git push origin clean-master
   ```

2. **Enable GitHub Pages:**
   - Go to your repo on GitHub
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `clean-master` (or `main`)
   - Folder: `/root`
   - Save

3. **Access your dashboard:**
   - URL: `https://YOUR-USERNAME.github.io/workspace/`
   - Or: `https://YOUR-USERNAME.github.io/openclaw/` (if using that repo)

---

## 📋 How to Use

### Managing Tasks via Dashboard UI

1. **Create Task:**
   - Click the **"+"** button in any column header
   - Fill in title, description, subtasks, priority, project
   - Save

2. **Move Tasks:**
   - Drag and drop tasks between columns
   - Or use arrow buttons in task detail view

3. **Edit Task:**
   - Click on any task card to open details
   - Edit any field
   - Save changes

4. **Board Columns:**
   - **Permanent** - Recurring tasks (daily checks, etc.)
   - **Backlog** - Waiting to be worked on
   - **In Progress** - Agent is working on this
   - **Review** - Done, awaiting your approval
   - **Done** - Completed and approved

### Managing Tasks via CLI

```bash
# Update task status
mc-update.sh status task_id review
mc-update.sh status task_id done
mc-update.sh status task_id in_progress

# Mark subtask as done
mc-update.sh subtask task_id sub_001 done

# Add progress comment
mc-update.sh comment task_id "Made progress on X, still working on Y"

# Complete task (moves to review + adds summary)
mc-update.sh complete task_id "Implemented feature X, tested, ready for review"

# Mark task as being processed (prevents duplicate processing)
mc-update.sh start task_id
```

---

## 🔄 Webhook Automation (Optional - Requires Tailscale)

For **fully automatic** task execution when you move tasks to "In Progress":

### Prerequisites
1. **Tailscale** (for secure tunnel)
2. **Tailscale Funnel** (to expose webhook endpoint)
3. **GitHub webhook** (to send push events)

### Setup Steps

1. **Install Tailscale:**
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   tailscale up
   ```

2. **Enable Funnel:**
   ```bash
   tailscale funnel 18789
   tailscale funnel status
   ```

3. **Generate webhook token:**
   ```bash
   openssl rand -hex 32
   # Save this token
   ```

4. **Update config:**
   ```bash
   # Edit ~/.clawdbot/mission-control.json
   # Add your hookToken
   ```

5. **Add GitHub webhook:**
   - Repo: Settings → Webhooks → Add webhook
   - URL: `https://YOUR-TAILNET-URL/hooks/github?token=YOUR_TOKEN`
   - Content type: application/json
   - Events: Push events
   - Save

6. **Test:**
   - Create a task in dashboard
   - Move to "In Progress"
   - Agent should receive notification and start working

---

## 📊 Task Structure

### Task Fields

```json
{
  "id": "unique_task_id",
  "title": "Short, clear name",
  "description": "Detailed instructions (Markdown supported)",
  "status": "backlog",  // permanent|backlog|in_progress|review|done
  "project": "project_id",
  "tags": ["tag1", "tag2"],
  "subtasks": [
    { "id": "sub_001", "title": "Step 1", "done": false }
  ],
  "priority": "high",  // high|medium|low
  "comments": [
    { "author": "Name", "text": "Comment text", "timestamp": "2026-02-20T..." }
  ],
  "createdAt": "2026-02-20T...",
  "dod": "Definition of Done - what success looks like"
}
```

### Status Values

| Status | Meaning |
|--------|---------|
| `permanent` | Recurring tasks (daily checks, etc.) |
| `backlog` | Waiting to be worked on |
| `in_progress` | Agent is working on this |
| `review` | Done, awaiting human approval |
| `done` | Completed and approved |

---

## 🎨 Dashboard Features

- ✅ **Drag & Drop** - Move tasks between columns
- 🔍 **Search** - Filter tasks by text
- 📁 **Project Filter** - Filter by project/category
- ⚙️ **Settings** - Add/edit projects
- 📦 **Archive** - Store completed tasks out of sight
- 👥 **Team** - See repo collaborators (if public)
- 📚 **Docs** - Built-in documentation

---

## 🤖 Agent Capabilities

Carlottta (your AI assistant) can:

- ✅ Create tasks (via CLI or editing tasks.json)
- ✅ Update task status, subtasks, comments
- ✅ Move tasks between columns
- ✅ Delete/archive tasks
- ✅ Receive webhook when you move tasks to "In Progress" (if webhook set up)

---

## 📁 File Structure

```
/root/.openclaw/workspace/
├── index.html                          # Dashboard UI
├── data/
│   ├── tasks.json                      # Task database
│   ├── .tasks-snapshot.json            # Webhook change detection
│   └── .webhook-debug.log              # Webhook debugging
└── skills/mission-control/             # Skill files
    ├── SKILL.md                        # Full skill reference
    ├── README.md                       # Skill readme
    ├── scripts/
    │   └── mc-update.sh                # CLI tool
    └── docs/
        ├── PREREQUISITES.md
        ├── HOW-IT-WORKS.md
        └── TROUBLESHOOTING.md

~/.clawdbot/
└── mission-control.json                # Config file

/usr/local/bin/
└── mc-update.sh                        # Symlinked CLI tool
```

---

## 💡 Use Cases for Peter's Projects

### Photostudio.io
- Track rendering pipeline tasks
- Monitor cost-per-image experiments
- Q/A testing checklist for new features
- Competitor research tasks

### DeBadkamer.com
- Lead generation experiment tracking
- Product catalog updates
- A/B test implementation tasks
- Feature roadmap

### Domain Portfolio
- Domain acquisition workflow
- Auction monitoring tasks
- Valuation research projects
- Outreach campaigns

### General Operations
- Daily/weekly checklists
- System maintenance tasks
- Content calendar management
- Bug tracking

---

## ⚠️ Important Notes

1. **Manual Mode vs Automatic:**
   - **Manual:** Works now via dashboard UI + git commits
   - **Automatic:** Requires Tailscale + webhook setup (optional)

2. **Data Storage:**
   - All tasks stored in `data/tasks.json`
   - Dashboard reads from this file
   - Edit directly or use CLI tool

3. **Git Integration:**
   - Dashboard can commit changes to git
   - Requires GitHub token for write access
   - Setup: Dashboard → Settings → Connect GitHub

4. **Security:**
   - Designed for single-user / trusted-user setups
   - Task authors = people who control the agent
   - For multi-user: Use Clawdbot sandbox and permissions

---

## ✅ Current Status

- ✅ **Installed:** All files in place
- ✅ **Configured:** Config file created
- ✅ **CLI Tool:** Working (`mc-update.sh`)
- ✅ **Sample Data:** Onboarding guides included
- ✅ **Dashboard Ready:** Open via file:// or GitHub Pages
- ⏳ **Webhook:** Requires Tailscale setup (optional)

---

## 🎓 Learning Resources

- **SKILL.md** - Full skill reference
- **docs/PREREQUISITES.md** - Installation requirements
- **docs/HOW-IT-WORKS.md** - Technical architecture
- **docs/TROUBLESHOOTING.md** - Common issues & solutions

---

**Ready to organize your tasks!** 📋✨

---

**Last Updated:** 2026-02-20
**Git Commit:** 764920a8
**Dashboard:** `/root/.openclaw/workspace/index.html`
**CLI Tool:** `mc-update.sh` (from anywhere)
