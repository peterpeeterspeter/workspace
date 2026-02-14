# Tasks Directory

This directory contains task briefs and deliverables for the squad.

## Task Lifecycle

1. **Inbox** — New, unassigned tasks
2. **Assigned** — Has owner(s), not started
3. **In Progress** — Being worked on
4. **Review** — Done, needs approval
5. **Done** — Finished
6. **Blocked** — Stuck, needs resolution

## File Structure

```
tasks/
├── inbox/           # New tasks
├── assigned/        # Tasks with owners
├── in-progress/     # Active work
├── review/          # Pending approval
├── done/            # Completed
└── blocked/         # Stuck tasks
```

## Task Template

Create a new task file in the appropriate directory:

```markdown
# Task: [Title]

**Created:** [Date]
**Assigned to:** [Agent name]
**Status:** [Current status]
**Priority:** [High/Medium/Low]

## Objective
[What does success look like?]

## Context
[Background, why this matters]

## Deliverables
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

## Dependencies
- [ ] [What's needed before starting]

## Due Date
[Date or ASAP]

## Notes
[Any additional context]
```

## Coordination

- Carlottta creates and assigns tasks
- Specialists update task files as they progress
- Move task files between directories as status changes
- Include final deliverables in task file before moving to /done
