import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// Mission Control Schema - Phase 3
// Real-time database with agents, tasks, activities, messages, notifications

export default defineSchema({
  // Agents - AI team members
  agents: defineTable({
    name: v.string(),
    role: v.string(),
    sessionKey: v.string(),
    status: v.union(v.literal("active"), v.literal("idle"), v.literal("blocked"), v.literal("offline")),
    currentTaskId: v.optional(v.id("tasks")),
    lastActive: v.number(), // Unix timestamp
    avatar: v.optional(v.string()),
    bio: v.optional(v.string()),
  })
    .index("by_status", ["status"])
    .index("by_last_active", ["lastActive"]),

  // Tasks - Work items
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.union(
      v.literal("inbox"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("done"),
      v.literal("blocked")
    ),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    assigneeId: v.optional(v.id("agents")),
    createdBy: v.id("agents"),
    createdAt: v.number(),
    updatedAt: v.number(),
    dueDate: v.optional(v.number()),
    dependencies: v.array(v.id("tasks")),
    handoffTo: v.optional(v.id("agents")),
    mentions: v.array(v.id("agents")),
    threadSubscribers: v.array(v.id("agents")),
    tags: v.array(v.string()),
    files: v.array(v.string()),
    progress: v.optional(v.number()), // 0-100
    position: v.optional(v.number()), // For Kanban ordering
  })
    .index("by_status", ["status"])
    .index("by_assignee", ["assigneeId"])
    .index("by_priority", ["priority"])
    .index("by_created", ["createdAt"])
    .index("by_handoff", ["handoffTo"]),

  // Messages - Comments on tasks
  messages: defineTable({
    taskId: v.id("tasks"),
    fromAgentId: v.id("agents"),
    content: v.string(),
    timestamp: v.number(),
    mentions: v.array(v.id("agents")),
    attachments: v.array(v.string()), // File IDs
    reactions: v.optional(v.array(v.object({
      agentId: v.id("agents"),
      emoji: v.string(),
    }))),
  })
    .index("by_task", ["taskId"])
    .index("by_agent", ["fromAgentId"])
    .index("by_timestamp", ["timestamp"]),

  // Activities - Event log
  activities: defineTable({
    type: v.union(
      v.literal("task_created"),
      v.literal("task_assigned"),
      v.literal("task_updated"),
      v.literal("task_completed"),
      v.literal("task_handoff"),
      v.literal("message_sent"),
      v.literal("agent_status_changed"),
      v.literal("system_created")
    ),
    agentId: v.optional(v.id("agents")),
    taskId: v.optional(v.id("tasks")),
    messageId: v.optional(v.id("messages")),
    message: v.string(),
    timestamp: v.number(),
    metadata: v.optional(v.any()), // Flexible data for different activity types
  })
    .index("by_timestamp", ["timestamp"])
    .index("by_agent", ["agentId"])
    .index("by_task", ["taskId"])
    .index("by_type", ["type"]),

  // Notifications - Delivery queue
  notifications: defineTable({
    mentionedAgentId: v.id("agents"),
    content: v.string(),
    taskId: v.optional(v.id("tasks")),
    messageId: v.optional(v.id("messages")),
    createdAt: v.number(),
    delivered: v.boolean(),
    deliveredAt: v.optional(v.number()),
    read: v.boolean(),
    readAt: v.optional(v.number()),
    type: v.union(
      v.literal("mention"),
      v.literal("assignment"),
      v.literal("handoff"),
      v.literal("system")
    ),
  })
    .index("by_agent_and_delivered", ["mentionedAgentId", "delivered"])
    .index("by_created", ["createdAt"])
    .index("by_delivered", ["delivered"]),

  // Documents - Shared files and deliverables
  documents: defineTable({
    title: v.string(),
    content: v.optional(v.string()),
    type: v.union(
      v.literal("deliverable"),
      v.literal("research"),
      v.literal("protocol"),
      v.literal("draft"),
      v.literal("reference")
    ),
    taskId: v.optional(v.id("tasks")),
    createdBy: v.id("agents"),
    createdAt: v.number(),
    updatedAt: v.number(),
    tags: v.array(v.string()),
    filePath: v.optional(v.string()), // For file system references
    mimeType: v.optional(v.string()),
    fileSize: v.optional(v.number()),
  })
    .index("by_task", ["taskId"])
    .index("by_type", ["type"])
    .index("by_created", ["createdAt"])
    .index("by_agent", ["createdBy"]),

  // Calendar - Content calendar and schedule
  calendar: defineTable({
    title: v.string(),
    site: v.string(), // crashcasino.io, cryptocrashgambling.com, etc.
    type: v.union(
      v.literal("informational"),
      v.literal("commercial"),
      v.literal("informational_commercial"),
      v.literal("transactional")
    ),
    keywords: v.array(v.string()),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    status: v.union(
      v.literal("planned"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("published"),
      v.literal("skipped")
    ),
    scheduledDate: v.number(), // Unix timestamp for scheduled publish date
    week: v.number(), // Week number (1-30)
    day: v.number(), // Day of week (1-7)
    taskId: v.optional(v.id("tasks")), // Link to task if created
    assigneeId: v.optional(v.id("agents")), // Assigned agent
    createdAt: v.number(),
    updatedAt: v.number(),
    notes: v.optional(v.string()),
  })
    .index("by_site", ["site"])
    .index("by_status", ["status"])
    .index("by_scheduled_date", ["scheduledDate"])
    .index("by_week", ["week"])
    .index("by_priority", ["priority"]),
});
