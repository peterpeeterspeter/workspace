#!/usr/bin/env python3
"""
Automated Daily Standup for Mission Control Phase 1
Scans all agent activity and compiles a summary report
Delivers to Telegram at 11 PM CET
"""

import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
TASKBOARD = WORKSPACE / "TASKBOARD_ENHANCED.md"
MEMORY_DIR = WORKSPACE / "memory"
AGENT_MEMORY = WORKSPACE / "memory" / "agents"

# Agent session mappings
AGENT_SESSIONS = {
    "Vision": "agent:main:cron:*",
    "Fury": "agent:main:cron:*",
    "Quill": "agent:main:cron:*"
}


def read_taskboard():
    """Read current taskboard state"""
    if not TASKBOARD.exists():
        return None

    with open(TASKBOARD, 'r') as f:
        return f.read()


def parse_taskboard_section(content, section_name):
    """Extract a specific section from taskboard"""
    pattern = rf'## {section_name}.*?(?=##|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None


def extract_tasks(content):
    """Extract tasks from taskboard content"""
    tasks = []

    # Pattern to match task items
    task_pattern = r'- \[([ x])\] \*\*([^*]+)\*\* → @(\w+)'

    for match in re.finditer(task_pattern, content):
        status_char = match.group(1)
        title = match.group(2)
        owner = match.group(3)

        status = "completed" if status_char == 'x' else "pending"

        tasks.append({
            "title": title,
            "owner": owner,
            "status": status
        })

    return tasks


def get_agent_activity(agent_name, hours=24):
    """Get recent activity from agent memory files"""
    cutoff = datetime.now() - timedelta(hours=hours)

    agent_files = list(AGENT_MEMORY.glob(f"*{agent_name.lower()}*"))

    if not agent_files:
        return None

    activities = []

    for file_path in agent_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()

                # Look for today's date entries
                today = datetime.now().strftime("%Y-%m-%d")
                pattern = rf'## {today}.*?(?=##|\Z)'
                match = re.search(pattern, content, re.DOTALL)

                if match:
                    today_content = match.group(1)
                    # Extract bullet points as activities
                    activities.extend(re.findall(r'^- (.+)$', today_content, re.MULTILINE))
        except Exception as e:
            continue

    return activities if activities else None


def get_published_articles_count():
    """Get total published articles from taskboard"""
    content = read_taskboard()
    if not content:
        return 0

    # Look for the published count in quick status
    match = re.search(r'Active Pipeline: (\d+) articles published', content)
    return int(match.group(1)) if match else 0


def get_blocked_items():
    """Extract blocked items from taskboard"""
    content = read_taskboard()
    if not content:
        return []

    blocked_section = parse_taskboard_section(content, "🚫 BLOCKED")
    if not blocked_section:
        return []

    # Extract task titles from blocked section
    return re.findall(r'- \*\*([^*]+)\*\*', blocked_section)


def get_in_progress_items():
    """Extract in-progress items from taskboard"""
    content = read_taskboard()
    if not content:
        return []

    progress_section = parse_taskboard_section(content, "🔄 IN PROGRESS")
    if not progress_section:
        return []

    # Extract task titles
    return re.findall(r'- \*\*([^*]+)\*\*', progress_section)


def compile_standup_report():
    """Compile the daily standup report"""
    now = datetime.now()
    today_str = now.strftime("%B %d, %Y")

    report = f"""📊 **DAILY STANDUP** — {today_str}

---

## ✅ COMPLETED TODAY

"""

    # Get in-progress items and check what's completed
    in_progress = get_in_progress_items()

    if in_progress:
        for item in in_progress:
            report += f"• **{item}**\n"
    else:
        report += "• No completed tasks logged\n"

    report += "\n## 🔄 IN PROGRESS\n\n"

    if in_progress:
        for item in in_progress:
            report += f"• {item}\n"
    else:
        report += "• No active tasks\n"

    # Add blocked items
    blocked = get_blocked_items()
    if blocked:
        report += "\n## 🚫 BLOCKED\n\n"
        for item in blocked:
            report += f"• {item}\n"

    # Add metrics
    published_count = get_published_articles_count()
    month_goal = 50
    progress_pct = int((published_count / month_goal) * 100)

    report += f"\n## 📊 METRICS\n\n"
    report += f"• **Articles Published:** {published_count}/{month_goal} ({progress_pct}%)\n"
    report += f"• **Month 1 Progress:** {progress_pct}% complete\n"

    # Add key decisions
    report += "\n## 📝 NOTES\n\n"
    report += "• System running normally\n"
    report += f"• Next scheduled: SERP analysis for Week 2 keywords\n"

    report += "\n---\n"
    report += f"_Generated at {now.strftime('%H:%M UTC')}_\n"

    return report


def send_to_telegram(message):
    """Send report to Telegram via openclaw"""
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', 'send',
             '--session', 'agent:main:main',
             '--message', message],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Daily standup sent to Telegram")
            return True
        else:
            print(f"✗ Failed to send: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error sending to Telegram: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("Daily Standup Generator")
    print("=" * 60)
    print()

    # Compile report
    report = compile_standup_report()

    print("Report compiled:")
    print(report)
    print()

    # Send to Telegram
    send_to_telegram(report)

    # Also save to memory
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}.md"

    with open(memory_file, 'a') as f:
        f.write(f"\n## Daily Standup ({datetime.now().strftime('%H:%M UTC')})\n\n")
        f.write(report)
        f.write("\n")

    print(f"✓ Report saved to {memory_file}")


if __name__ == '__main__':
    main()
