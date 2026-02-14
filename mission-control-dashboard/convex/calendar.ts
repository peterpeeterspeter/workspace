import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Seed calendar with crashcasino content plan
export const seedCalendar = mutation({
  args: {},
  handler: async (ctx) => {
    // Check if already seeded
    const existing = await ctx.db.query("calendar").collect();
    if (existing.length > 0) {
      return { status: "already_seeded", count: existing.length };
    }

    const now = Date.now();
    let count = 0;

    // Week 1: Foundation (Feb 2-8)
    const week1 = [
      // crashcasino.io
      {
        title: "Is Crash Gambling Rigged? Complete 2026 Fairness Guide",
        site: "crashcasino.io",
        type: "informational_commercial",
        keywords: ["is crash gambling rigged", "crash game fairness", "provably fair"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-03").getTime(),
        week: 1,
        day: 1,
      },
      {
        title: "Provably Fair Crash Games: How to Verify Game Integrity",
        site: "crashcasino.io",
        type: "informational",
        keywords: ["provably fair", "crash game verification", "fair gambling"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-05").getTime(),
        week: 1,
        day: 3,
      },
      {
        title: "Best Crash Casinos 2026: Safe & Verified Sites",
        site: "crashcasino.io",
        type: "commercial",
        keywords: ["best crash casinos", "top crash gambling sites", "safe crash casinos"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-07").getTime(),
        week: 1,
        day: 5,
      },
      // cryptocrashgambling.com
      {
        title: "Bitcoin Crash Gambling: Complete Guide 2026",
        site: "cryptocrashgambling.com",
        type: "informational_commercial",
        keywords: ["bitcoin crash gambling", "BTC crash games", "crypto crash"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-03").getTime(),
        week: 1,
        day: 1,
      },
      {
        title: "Ethereum Crash Gambling: ETH-Friendly Crash Casinos",
        site: "cryptocrashgambling.com",
        type: "informational_commercial",
        keywords: ["ethereum crash gambling", "ETH crash games"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-05").getTime(),
        week: 1,
        day: 3,
      },
      {
        title: "USDT Crash Gambling: Stable & Fast Transactions",
        site: "cryptocrashgambling.com",
        type: "informational_commercial",
        keywords: ["USDT crash gambling", "Tether crash games"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-07").getTime(),
        week: 1,
        day: 5,
      },
      // crashgamegambling.com
      {
        title: "Crash Gambling 101: Ultimate Beginner's Guide",
        site: "crashgamegambling.com",
        type: "informational",
        keywords: ["crash gambling for beginners", "how to play crash", "what is crash gambling"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-03").getTime(),
        week: 1,
        day: 1,
      },
      {
        title: "Crash Gambling Bankroll Management: Don't Go Broke",
        site: "crashgamegambling.com",
        type: "informational",
        keywords: ["crash bankroll management", "crash gambling budget"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-05").getTime(),
        week: 1,
        day: 3,
      },
      {
        title: "How to Play Crash Gambling: Step-by-Step Tutorial",
        site: "crashgamegambling.com",
        type: "informational",
        keywords: ["how to play crash", "crash game tutorial"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-07").getTime(),
        week: 1,
        day: 5,
      },
      // freecrashgames.com
      {
        title: "Best Crash Casinos for India Players 2026",
        site: "freecrashgames.com",
        type: "commercial",
        keywords: ["crash casinos india", "crash gambling india"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-03").getTime(),
        week: 1,
        day: 1,
      },
      {
        title: "Best Crash Casinos for Brazil Players 2026",
        site: "freecrashgames.com",
        type: "commercial",
        keywords: ["crash casinos brazil", "crash gambling brazil"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-05").getTime(),
        week: 1,
        day: 3,
      },
      {
        title: "Best Crash Casinos for Nigeria Players 2026",
        site: "freecrashgames.com",
        type: "commercial",
        keywords: ["crash casinos nigeria", "crash gambling nigeria"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-07").getTime(),
        week: 1,
        day: 5,
      },
      // aviatorcrashgame.com
      {
        title: "Aviator Game: Complete Strategy Guide 2026",
        site: "aviatorcrashgame.com",
        type: "informational_commercial",
        keywords: ["aviator strategy", "aviator game guide", "how to win aviator"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-03").getTime(),
        week: 1,
        day: 1,
      },
      {
        title: "Best Aviator Casinos: Top Sites to Play Aviator",
        site: "aviatorcrashgame.com",
        type: "commercial",
        keywords: ["best aviator casinos", "aviator betting sites"],
        priority: "high" as const,
        scheduledDate: new Date("2026-02-05").getTime(),
        week: 1,
        day: 3,
      },
      {
        title: "Aviator Crash Game: How It Works & RTP Explained",
        site: "aviatorcrashgame.com",
        type: "informational",
        keywords: ["aviator rtp", "aviator game explained", "aviator odds"],
        priority: "medium" as const,
        scheduledDate: new Date("2026-02-07").getTime(),
        week: 1,
        day: 5,
      },
    ];

    // Insert Week 1
    for (const item of week1) {
      await ctx.db.insert("calendar", {
        ...item,
        status: "planned",
        createdAt: now,
        updatedAt: now,
      });
      count++;
    }

    return {
      status: "seeded",
      count,
      sites: ["crashcasino.io", "cryptocrashgambling.com", "crashgamegambling.com", "freecrashgames.com", "aviatorcrashgame.com"],
    };
  },
});

// Get all calendar items
export const getCalendar = query({
  args: {
    site: v.optional(v.string()),
    status: v.optional(v.union(
      v.literal("planned"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("published"),
      v.literal("skipped")
    )),
    week: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    let query = ctx.db.query("calendar");

    if (args.site) {
      query = query.withIndex("by_site", q => q.eq("site", args.site));
    }

    if (args.status) {
      query = query.withIndex("by_status", q => q.eq("status", args.status));
    }

    if (args.week) {
      query = query.withIndex("by_week", q => q.eq("week", args.week));
    }

    const items = await query.collect();

    // Sort by scheduled date
    return items.sort((a, b) => a.scheduledDate - b.scheduledDate);
  },
});

// Get calendar by week range
export const getCalendarWeeks = query({
  args: {
    startWeek: v.number(),
    endWeek: v.number(),
  },
  handler: async (ctx, args) => {
    const items = await ctx.db.query("calendar").collect();

    return items
      .filter(item => item.week >= args.startWeek && item.week <= args.endWeek)
      .sort((a, b) => a.scheduledDate - b.scheduledDate);
  },
});

// Update calendar item status
export const updateCalendarItem = mutation({
  args: {
    calendarId: v.id("calendar"),
    status: v.union(
      v.literal("planned"),
      v.literal("assigned"),
      v.literal("in_progress"),
      v.literal("review"),
      v.literal("published"),
      v.literal("skipped")
    ),
    taskId: v.optional(v.id("tasks")),
    notes: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const updates: any = {
      status: args.status,
      updatedAt: now,
    };

    if (args.taskId) {
      updates.taskId = args.taskId;
    }

    if (args.notes) {
      updates.notes = args.notes;
    }

    await ctx.db.patch(args.calendarId, updates);

    return { success: true };
  },
});

// Get calendar summary by site
export const getCalendarSummary = query({
  args: {},
  handler: async (ctx) => {
    const items = await ctx.db.query("calendar").collect();

    const summary = {
      total: items.length,
      bySite: {} as Record<string, number>,
      byStatus: {} as Record<string, number>,
      byWeek: {} as Record<number, number>,
      byPriority: {
        high: 0,
        medium: 0,
        low: 0,
      },
    };

    for (const item of items) {
      // By site
      summary.bySite[item.site] = (summary.bySite[item.site] || 0) + 1;

      // By status
      summary.byStatus[item.status] = (summary.byStatus[item.status] || 0) + 1;

      // By week
      summary.byWeek[item.week] = (summary.byWeek[item.week] || 0) + 1;

      // By priority
      summary.byPriority[item.priority]++;
    }

    return summary;
  },
});
