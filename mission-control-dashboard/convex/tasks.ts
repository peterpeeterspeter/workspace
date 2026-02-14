import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Seed initial data
export const seed = mutation({
  args: {},
  handler: async (ctx) => {
    // Check if already seeded
    const existingAgents = await ctx.db.query("agents").collect();
    if (existingAgents.length > 0) {
      return { status: "already_seeded", count: existingAgents.length };
    }

    const now = Date.now();

    // Create agents
    const vision = await ctx.db.insert("agents", {
      name: "Vision",
      role: "SEO/Content Specialist",
      sessionKey: "agent:main:cron:*",
      status: "active",
      lastActive: now,
      avatar: "🔍",
      bio: "SEO and content optimization specialist",
    });

    const fury = await ctx.db.insert("agents", {
      name: "Fury",
      role: "Research Specialist",
      sessionKey: "agent:main:cron:*",
      status: "idle",
      lastActive: now - 3600000, // 1 hour ago
      avatar: "🕵️",
      bio: "Deep researcher and analyst",
    });

    const quill = await ctx.db.insert("agents", {
      name: "Quill",
      role: "Marketing Specialist",
      sessionKey: "agent:main:cron:*",
      status: "idle",
      lastActive: now - 3600000,
      avatar: "✍️",
      bio: "Social media and marketing strategy",
    });

    const peter = await ctx.db.insert("agents", {
      name: "Peter",
      role: "Human",
      sessionKey: "agent:main:main",
      status: "active",
      lastActive: now,
      avatar: "👤",
      bio: "Human coordinator",
    });

    // Create initial tasks
    const task1 = await ctx.db.insert("tasks", {
      title: "Week 2 SERP Analysis",
      description: "Analyze keywords for 5 Week 2 articles: crash casino bonus, crypto vs fiat, crash gambling strategy, crash casinos uk, aviator predictor",
      status: "assigned",
      priority: "high",
      assigneeId: fury,
      createdBy: peter,
      createdAt: now,
      updatedAt: now,
      handoffTo: vision,
      mentions: [vision],
      threadSubscribers: [vision, fury],
      tags: ["week2", "serp", "research"],
      files: [],
      progress: 0,
      dependencies: [],
    });

    const task2 = await ctx.db.insert("tasks", {
      title: "Week 2 Content Briefs",
      description: "Create 5 HIGH priority article briefs for Week 2 content production",
      status: "in_progress",
      priority: "high",
      assigneeId: vision,
      createdBy: vision,
      createdAt: now - 7200000, // 2 hours ago
      updatedAt: now - 3600000,
      handoffTo: fury,
      mentions: [fury],
      threadSubscribers: [vision, fury],
      tags: ["week2", "briefs"],
      files: [],
      progress: 70,
      dependencies: [],
    });

    const task3 = await ctx.db.insert("tasks", {
      title: "Site Cleanup Approval",
      description: "Approve cleanup of 119 duplicate posts across 3 sites. Need WordPress DELETE permissions.",
      status: "blocked",
      priority: "high",
      assigneeId: peter,
      createdBy: vision,
      createdAt: now - 86400000, // 1 day ago
      updatedAt: now,
      handoffTo: undefined,
      mentions: [],
      threadSubscribers: [peter],
      tags: ["cleanup", "blocked"],
      files: [],
      dependencies: [],
    });

    // Create initial activities
    await ctx.db.insert("activities", {
      type: "task_created",
      agentId: vision,
      taskId: task2,
      message: "Vision created task: Week 2 Content Briefs",
      timestamp: now - 7200000,
    });

    await ctx.db.insert("activities", {
      type: "task_assigned",
      agentId: vision,
      taskId: task1,
      message: "Task assigned to Fury: Week 2 SERP Analysis",
      timestamp: now - 3600000,
    });

    await ctx.db.insert("activities", {
      type: "system_created",
      agentId: peter,
      message: "Mission Control Phase 3 database initialized",
      timestamp: now,
    });

    // Create initial notifications
    await ctx.db.insert("notifications", {
      mentionedAgentId: fury,
      content: "@Fury: Vision created task 'Week 2 SERP Analysis' assigned to you.",
      taskId: task1,
      createdAt: now - 3600000,
      delivered: false,
      read: false,
      type: "assignment",
    });

    return {
      status: "seeded",
      agents: 4,
      tasks: 3,
    };
  },
});

// Get all tasks with optional filters
export const getTasks = query({
  args: {
    status: v.optional(v.union(
      v.literal("inbox"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("done"),
      v.literal("blocked")
    )),
    assigneeId: v.optional(v.id("agents")),
  },
  handler: async (ctx, args) => {
    let tasks;

    if (args.status && args.assigneeId) {
      // Both filters - need to filter by assignee after getting by status
      const byStatus = await ctx.db.query("tasks")
        .withIndex("by_status", q => q.eq("status", args.status))
        .collect();
      tasks = byStatus.filter(t => t.assigneeId === args.assigneeId);
    } else if (args.status) {
      tasks = await ctx.db.query("tasks")
        .withIndex("by_status", q => q.eq("status", args.status))
        .collect();
    } else if (args.assigneeId) {
      tasks = await ctx.db.query("tasks")
        .withIndex("by_assignee", q => q.eq("assigneeId", args.assigneeId))
        .collect();
    } else {
      tasks = await ctx.db.query("tasks").collect();
    }

    // Fetch assignee details for each task
    const tasksWithAgents = await Promise.all(
      tasks.map(async (task) => {
        let assignee = null;
        if (task.assigneeId) {
          assignee = await ctx.db.get(task.assigneeId);
        }
        let handoffTo = null;
        if (task.handoffTo) {
          handoffTo = await ctx.db.get(task.handoffTo);
        }
        return {
          ...task,
          assignee,
          handoffTo,
        };
      })
    );

    return tasksWithAgents;
  },
});

// Get all agents
export const getAgents = query({
  args: {},
  handler: async (ctx) => {
    const agents = await ctx.db.query("agents").collect();

    // Fetch current task for each agent
    const agentsWithTasks = await Promise.all(
      agents.map(async (agent) => {
        let currentTask = null;
        if (agent.currentTaskId) {
          currentTask = await ctx.db.get(agent.currentTaskId);
        }
        // Count assigned tasks
        const assignedTasks = await ctx.db
          .query("tasks")
          .withIndex("by_assignee", q => q.eq("assigneeId", agent._id))
          .collect();
        return {
          ...agent,
          currentTask,
          taskCount: assignedTasks.length,
        };
      })
    );

    return agentsWithTasks;
  },
});

// Get recent activities
export const getActivities = query({
  args: {
    limit: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const limit = args.limit ?? 50;

    const activities = await ctx.db
      .query("activities")
      .withIndex("by_timestamp")
      .order("desc")
      .take(limit);

    // Fetch agent details for each activity
    const activitiesWithAgents = await Promise.all(
      activities.map(async (activity) => {
        let agent = null;
        if (activity.agentId) {
          agent = await ctx.db.get(activity.agentId);
        }
        let task = null;
        if (activity.taskId) {
          task = await ctx.db.get(activity.taskId);
        }
        return {
          ...activity,
          agent,
          task,
        };
      })
    );

    return activitiesWithAgents;
  },
});

// Get undelivered notifications for an agent
export const getNotifications = query({
  args: {
    agentId: v.id("agents"),
  },
  handler: async (ctx, args) => {
    const notifications = await ctx.db
      .query("notifications")
      .withIndex("by_agent_and_delivered", q =>
        q.eq("mentionedAgentId", args.agentId).eq("delivered", false)
      )
      .collect();

    return notifications;
  },
});

// Create a new task
export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    assigneeId: v.id("agents"),
    handoffTo: v.optional(v.id("agents")),
    tags: v.optional(v.array(v.string())),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    // TODO: Get from auth - for now, use Peter as creator
    const agents = await ctx.db.query("agents").collect();
    const createdBy = agents.find(a => a.name === "Peter")?._id || agents[0]._id;

    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      status: "assigned",
      priority: args.priority,
      assigneeId: args.assigneeId,
      createdBy,
      createdAt: now,
      updatedAt: now,
      handoffTo: args.handoffTo,
      mentions: args.handoffTo ? [args.handoffTo] : [],
      threadSubscribers: [args.assigneeId],
      tags: args.tags ?? [],
      files: [],
      dependencies: [],
    });

    // Log activity
    await ctx.db.insert("activities", {
      type: "task_created",
      agentId: createdBy,
      taskId,
      message: `Created task: ${args.title}`,
      timestamp: now,
    });

    // Create notification for assignee
    if (args.assigneeId) {
      await ctx.db.insert("notifications", {
        mentionedAgentId: args.assigneeId,
        content: `Task assigned to you: ${args.title}`,
        taskId,
        createdAt: now,
        delivered: false,
        read: false,
        type: "assignment",
      });
    }

    return taskId;
  },
});

// Update task status
export const updateTask = mutation({
  args: {
    taskId: v.id("tasks"),
    status: v.optional(v.union(
      v.literal("inbox"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("done"),
      v.literal("blocked")
    )),
    progress: v.optional(v.number()),
    handoffTo: v.optional(v.id("agents")),
  },
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.taskId);
    if (!task) {
      throw new Error("Task not found");
    }

    const now = Date.now();
    const updates: any = {
      updatedAt: now,
    };

    if (args.status) {
      updates.status = args.status;
    }
    if (args.progress !== undefined) {
      updates.progress = args.progress;
    }
    if (args.handoffTo) {
      updates.handoffTo = args.handoffTo;
      if (!updates.mentions) {
        updates.mentions = [...task.mentions];
      }
      if (!updates.mentions.includes(args.handoffTo)) {
        updates.mentions.push(args.handoffTo);
      }

      // Create notification for handoff target
      await ctx.db.insert("notifications", {
        mentionedAgentId: args.handoffTo,
        content: `Task handed off to you: ${task.title}`,
        taskId: args.taskId,
        createdAt: now,
        delivered: false,
        read: false,
        type: "handoff",
      });

      // Log handoff activity
      await ctx.db.insert("activities", {
        type: "task_handoff",
        agentId: task.assigneeId,
        taskId: args.taskId,
        message: `Task handed to @${args.handoffTo}`,
        timestamp: now,
      });
    }

    await ctx.db.patch(args.taskId, updates);

    // Log status change activity
    if (args.status && args.status !== task.status) {
      await ctx.db.insert("activities", {
        type: "task_updated",
        agentId: task.assigneeId,
        taskId: args.taskId,
        message: `Task status: ${task.status} → ${args.status}`,
        timestamp: now,
      });
    }

    return { success: true };
  },
});
