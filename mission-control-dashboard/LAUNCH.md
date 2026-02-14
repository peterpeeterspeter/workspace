# MISSION CONTROL DASHBOARD - LAUNCH INSTRUCTIONS

## 🚀 Quick Start (With Mock Data - Works Now!)

The dashboard comes with mock data pre-loaded so you can explore it immediately:

```bash
cd /root/.openclaw/workspace/mission-control-dashboard

# Start the dashboard
npm run dev

# Open browser to:
http://localhost:5173
```

You'll see:
- ✅ Task board with sample tasks
- ✅ Agent cards with status
- ✅ Activity feed with updates
- ✅ Clickable task details

---

## 🔐 Convex Authentication (When Ready for Real Data)

To connect to a real Convex backend:

### Step 1: Create Convex Account
```bash
cd /root/.openclaw/workspace/mission-control-dashboard

# This will open browser for authentication
npx convex login
```

### Step 2: Create Project
```bash
# Create a new Convex project
npx convex init
```

### Step 3: Configure Environment
```bash
# After authentication, Convex will create:
# - .env.local with CONVEX_DEPLOYMENT URL
# - convex.json with project configuration
```

### Step 4: Deploy Schema & Functions
```bash
# Deploy to Convex cloud
npx convex deploy
```

### Step 5: Seed Initial Data
```bash
# Run seed function
npx convex run --seed
```

### Step 6: Update Dashboard to Use Convex
```typescript
// In App.tsx, replace mock data with:
import { useQuery, useMutation } from './convex/_generated';

// Instead of:
const [tasks, setTasks] = useState<Task[]>(mockTasks);

// Use:
const tasks = useQuery("api.tasks.getTasks", {}) ?? [];
```

---

## 🎯 For Now: Mock Data Mode

The dashboard currently runs with **mock data** so you can:
- ✅ Test the UI immediately
- ✅ Explore all features
- ✅ See the design
- ✅ Plan your workflow

**No authentication required!**

---

## 📊 What You'll See

### Task Board
- 6 Kanban columns (Inbox → Done → Blocked)
- Sample tasks with priorities
- Agent assignments
- Progress tracking

### Agent Cards
- All agents with status
- Current workload
- Last active times

### Activity Feed
- Recent activities
- Agent attributions
- Timestamps

---

## 🔧 Customizing Mock Data

Edit `src/App.tsx` to update the mock data:

```typescript
// Around line 40-120 in App.tsx
setTasks([
  {
    _id: 'task1',
    title: 'Your Custom Task',
    status: 'assigned',
    priority: 'high',
    assigneeId: 'vision',
    // ... more fields
  },
  // ... more tasks
]);
```

---

## 🚀 Deploying to Production (Optional)

### Step 1: Build Dashboard
```bash
npm run build
```

### Step 2: Preview Build
```bash
npm run preview
```

### Step 3: Deploy to Hosting
Options:
- **Vercel:** `npm install -g vercel && vercel`
- **Netlify:** `netlify deploy`
- **Your server:** Copy `dist/` to web server

---

## 📖 Next Steps

1. **Test the UI** - Start with mock data: `npm run dev`
2. **Explore Features** - Click around, open tasks, switch views
3. **Decide on Convex** - If you want real-time sync, authenticate Convex
4. **Migrate Phase 2 Data** - Import tasks from `mission-control.db.json`

---

## 🎉 You're Ready!

**For immediate use:**
```bash
npm run dev
# Open http://localhost:5173
```

**For Convex setup (when ready):**
```bash
npx convex login
npx convex init
npx convex deploy
```

---

**Built by:** Carlottta
**Date:** February 2, 2026
**Status:** Dashboard ready to launch with mock data

🎯 **Dashboard UI complete and functional - start exploring now!**
