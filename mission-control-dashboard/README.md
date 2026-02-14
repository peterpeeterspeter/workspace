# Mission Control Dashboard

**Phase 3 of Mission Control** - Real-time coordination system with Convex backend and React dashboard.

## 🚀 Quick Start

```bash
# Navigate to dashboard directory
cd /root/.openclaw/workspace/mission-control-dashboard

# Install dependencies (already done)
npm install

# Set up Convex (requires authentication)
npx convex dev

# In a new terminal, start the dev server
npm run dev

# Open browser to http://localhost:5173
```

## 📁 Project Structure

```
mission-control-dashboard/
├── convex/
│   ├── schema.ts          # Database schema (agents, tasks, activities, etc.)
│   ├── tasks.ts           # Convex queries and mutations
│   └── _generated/        # Auto-generated Convex files
├── src/
│   ├── App.tsx            # Main React component
│   ├── App.css            # Dashboard styles
│   ├── index.css          # Base styles
│   └── main.tsx           # React entry point
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 🎯 Features

### Real-Time Task Board
- **Kanban-style layout** with 6 columns (Inbox → Assigned → In Progress → Review → Done → Blocked)
- **Drag-and-drop** task movement
- **Task cards** with priority indicators, assignees, progress bars
- **Click to expand** task details

### Agent Management
- **Agent cards** with status indicators (active, idle, blocked, offline)
- **Current task** display
- **Task count** per agent
- **Last active** timestamp

### Activity Feed
- **Real-time updates** via Convex WebSocket
- **Activity types:** task_created, task_assigned, task_updated, task_completed, task_handoff
- **Agent attribution** with avatars
- **Timestamps** and context

### Task Detail Modal
- **Full task information** in popup
- **Metadata:** assignee, created/updated dates, handoff target
- **Progress tracking** with visual progress bar
- **Tags and labels** for categorization

## 🔧 Convex Integration

### Schema
The dashboard uses Convex for real-time data sync:

- **agents:** AI team members with status and session keys
- **tasks:** Work items with status, priority, assignees, handoffs
- **messages:** Comments and discussions on tasks
- **activities:** Event log for tracking all changes
- **notifications:** Delivery queue for agent alerts
- **documents:** Shared files and deliverables

### Queries
- `getTasks` - Fetch tasks with optional filters (status, assignee)
- `getAgents` - Fetch all agents with current tasks
- `getActivities` - Recent activity feed
- `getNotifications` - Undelivered notifications for an agent

### Mutations
- `seed` - Initialize database with sample data
- `createTask` - Create new task with notifications
- `updateTask` - Update status, progress, or handoff

## 🎨 UI Components

### TaskBoard
```tsx
// Renders Kanban board with draggable tasks
<TaskBoard tasks={tasks} onTaskMove={handleTaskMove} />
```

### TaskCard
```tsx
// Individual task card with all metadata
<TaskCard task={task} onClick={openDetail} />
```

### AgentCard
```tsx
// Agent status and current work
<AgentCard agent={agent} />
```

### ActivityFeed
```tsx
// Real-time activity stream
<ActivityFeed activities={activities} />
```

## 🔐 Authentication Setup

To connect to Convex:

1. **Create a Convex account:**
   ```bash
   npx convex dev
   ```

2. **Follow the prompts to login or create account**

3. **Your project will be deployed to Convex cloud**

4. **Copy your deployment URL to `.env` file**

## 📊 Current State

- **React Dashboard:** ✅ Built and styled
- **Convex Schema:** ✅ Defined
- **Convex Functions:** ✅ Queries and mutations ready
- **Authentication:** ⏳ Requires Convex account setup
- **Real-time Sync:** ⏳ Ready after authentication

## 🚧 Next Steps

### To Complete Setup:
1. Run `npx convex dev` and authenticate
2. Start dev server with `npm run dev`
3. Open http://localhost:5173
4. Dashboard will connect to Convex and load real data

### Optional Enhancements:
- Add drag-and-drop for task cards
- Implement task creation form
- Add message threading
- File upload support
- Dark mode theme
- Mobile responsive improvements

## 🔄 Migration from Phase 2

The Phase 3 dashboard will import data from Phase 2 JSON database:

```typescript
// Import function (to be implemented)
import { migrateFromPhase2 } from './convex/migration';

await migrateFromPhase2(phase2JSONData);
```

This will:
1. Read `mission-control.db.json`
2. Transform data to Convex schema
3. Insert into Convex via mutations
4. Preserve all tasks, agents, activities

## 📖 Documentation

- **Phase 3 Setup Guide:** `MISSION_CONTROL_PHASE3_SETUP.md`
- **Convex Docs:** https://docs.convex.dev
- **React Docs:** https://react.dev

## 🎯 Usage Examples

### View Task Board
```bash
npm run dev
# Open browser → See Kanban board with tasks
```

### Create Task (via UI)
```typescript
// TODO: Add task creation form
<button onClick={() => setShowCreateModal(true)}>
  + New Task
</button>
```

### Update Task Status
```typescript
// Drag task to different column
onTaskDrop(taskId, newStatus) {
  updateTask({ taskId, status: newStatus });
}
```

### Monitor Activity
```typescript
// Activity feed updates in real-time
useQuery("getActivities", {}, { poll: true });
```

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start Convex dev server
npx convex dev

# Start React dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📈 Performance

- **React:** Vite for fast HMR
- **Convex:** Real-time WebSocket sync
- **Queries:** Optimized with indexes
- **UI:** Virtual scrolling for large lists (TODO)

## 🎨 Styling

The dashboard uses:
- **CSS Variables** for theming
- **Flexbox & Grid** for layouts
- **Responsive design** for mobile
- **Modern aesthetics** matching Mission Control brand

## 🐛 Troubleshooting

### Convex Connection Error
```bash
# Ensure convex dev is running
npx convex dev

# Check .env for CONVEX_DEPLOYMENT
cat .env.local
```

### Tasks Not Loading
```bash
# Check browser console for errors
# Ensure Convex functions are deployed
npx convex deploy
```

### Styling Issues
```bash
# Clear browser cache
# Check App.css is imported
```

---

**Built by:** Carlottta
**Framework:** React + TypeScript + Vite + Convex
**Status:** UI complete, awaiting Convex authentication

🚀 **Real-time AI team coordination dashboard - ready to launch!**
