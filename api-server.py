#!/usr/bin/env python3
"""
Simple API server for Mission Control Phase 2 database
Serves mission-control.db.json via REST API
"""

import json
import os
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import cgi

DB_PATH = Path("/root/.openclaw/workspace/mission-control.db.json")
WORKSPACE = Path("/root/.openclaw/workspace")

class MissionControlAPI(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path

        # CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if path == '/api/tasks':
            self.serve_tasks()
        elif path == '/api/agents':
            self.serve_agents()
        elif path == '/api/activities':
            self.serve_activities()
        elif path == '/api/status':
            self.serve_status()
        else:
            # Serve static files from dashboard directory
            self.serve_static(path)

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Update task in database
            self.update_task(data)

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """Handle OPTIONS for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_tasks(self):
        """Serve all tasks"""
        if not DB_PATH.exists():
            self.wfile.write(json.dumps([]).encode())
            return

        with open(DB_PATH, 'r') as f:
            data = json.load(f)

        # Enrich with agent names
        agents_map = {a['id']: a for a in data.get('agents', [])}
        tasks = data.get('tasks', [])

        for task in tasks:
            if task.get('assignee_id'):
                task['assignee'] = agents_map.get(task['assignee_id'])
            if task.get('handoff_to'):
                task['handoffToAgent'] = agents_map.get(task['handoff_to'])

        self.wfile.write(json.dumps(tasks).encode())

    def serve_agents(self):
        """Serve all agents"""
        if not DB_PATH.exists():
            self.wfile.write(json.dumps([]).encode())
            return

        with open(DB_PATH, 'r') as f:
            data = json.load(f)

        agents = data.get('agents', [])
        tasks = data.get('tasks', [])

        # Count tasks per agent
        for agent in agents:
            agent_tasks = [t for t in tasks if t.get('assignee_id') == agent['id']]
            agent['taskCount'] = len(agent_tasks)

            # Current task
            current_task = next(
                (t for t in agent_tasks if t.get('status') in ['assigned', 'in_progress']),
                None
            )
            agent['currentTask'] = current_task

        self.wfile.write(json.dumps(agents).encode())

    def serve_activities(self):
        """Serve activities"""
        if not DB_PATH.exists():
            self.wfile.write(json.dumps([]).encode())
            return

        with open(DB_PATH, 'r') as f:
            data = json.load(f)

        activities = data.get('activities', [])
        agents_map = {a['id']: a for a in data.get('agents', [])}
        tasks_map = {t['id']: t for t in data.get('tasks', [])}

        # Enrich with agent and task details
        for activity in activities:
            if activity.get('agent_id'):
                activity['agent'] = agents_map.get(activity['agent_id'])
            if activity.get('task_id'):
                activity['task'] = tasks_map.get(activity['task_id'])

        self.wfile.write(json.dumps(activities).encode())

    def serve_status(self):
        """Serve system status"""
        if not DB_PATH.exists():
            self.wfile.write(json.dumps({"status": "error", "message": "Database not found"}).encode())
            return

        with open(DB_PATH, 'r') as f:
            data = json.load(f)

        metadata = data.get('metadata', {})

        self.wfile.write(json.dumps({
            "status": "operational",
            "last_updated": data.get('last_updated'),
            "total_tasks": metadata.get('total_tasks', 0),
            "active_tasks": metadata.get('active_tasks', 0),
            "total_agents": metadata.get('total_agents', 0),
            "active_agents": metadata.get('active_agents', 0)
        }).encode())

    def serve_static(self, path):
        """Serve static files from dashboard directory"""
        dashboard_dir = Path("/root/.openclaw/workspace/mission-control-dashboard")

        # Default to index.html
        if path == '/' or path == '':
            path = '/index.html'

        file_path = dashboard_dir / path.lstrip('/')

        if file_path.exists() and file_path.is_file():
            # Determine content type
            if file_path.suffix == '.js':
                content_type = 'application/javascript'
            elif file_path.suffix == '.css':
                content_type = 'text/css'
            elif file_path.suffix == '.html':
                content_type = 'text/html'
            else:
                content_type = 'application/octet-stream'

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', content_type)
            self.end_headers()

            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def update_task(self, data):
        """Update task in database"""
        if not DB_PATH.exists():
            return

        with open(DB_PATH, 'r') as f:
            db = json.load(f)

        # Find and update task
        for task in db.get('tasks', []):
            if task['id'] == data.get('id'):
                if data.get('status'):
                    task['status'] = data['status']
                if data.get('progress') is not None:
                    task['progress'] = data['progress']
                if data.get('handoff_to'):
                    task['handoff_to'] = data['handoff_to']
                task['updated_at'] = datetime.now().isoformat() + "Z"
                break

        # Save back
        with open(DB_PATH, 'w') as f:
            json.dump(db, f, indent=2)

def run_server(port=5174):
    """Run the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MissionControlAPI)

    print(f"🚀 Mission Control API Server")
    print(f"📊 API: http://localhost:{port}/api")
    print(f"📋 Dashboard: http://localhost:{port}")
    print(f"📁 Database: {DB_PATH}")
    print()
    print(f"Endpoints:")
    print(f"  GET  /api/tasks     - List all tasks")
    print(f"  GET  /api/agents    - List all agents")
    print(f"  GET  /api/activities - List activities")
    print(f"  GET  /api/status    - System status")
    print(f"  POST /api/tasks     - Update task")
    print()
    print(f"Press Ctrl+C to stop")
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
