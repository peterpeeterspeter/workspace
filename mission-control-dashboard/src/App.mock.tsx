import React, { useState, useEffect } from 'react';
import { useQuery } from './convex/_generated';
import './App.css';

// Types
interface Agent {
  _id: string;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'blocked' | 'offline';
  avatar?: string;
  lastActive: number;
  currentTask?: Task;
  taskCount: number;
}

interface Task {
  _id: string;
  title: string;
  description?: string;
  status: 'inbox' | 'assigned' | 'in_progress' | 'review' | 'done' | 'blocked';
  priority: 'high' | 'medium' | 'low';
  assigneeId?: string;
  assignee?: Agent;
  handoffTo?: string;
  handoffToAgent?: Agent;
  createdAt: number;
  updatedAt: number;
  progress?: number;
  tags: string[];
}

interface Activity {
  _id: string;
  type: string;
  agent?: Agent;
  task?: Task;
  message: string;
  timestamp: number;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [view, setView] = useState<'board' | 'agents' | 'activity'>('board');

  // TODO: Replace with real Convex queries
  useEffect(() => {
    // Current tasks from TASKBOARD.md (as of Feb 2, 2026 18:55 UTC)
    setTasks([
      {
        _id: 'task1',
        title: 'Week 2 Content Production',
        description: '5 HIGH priority articles (all drafts complete, 10,550 words). Ready for SEO review, affiliate integration, and WordPress publishing. Articles: Crash Bonuses (2,000w), UK Casinos (1,850w), Crypto vs Fiat (2,100w), Math Behind Multiplier (2,400w), Aviator Predictor (2,200w).',
        status: 'review',
        priority: 'high',
        assigneeId: 'vision',
        createdAt: Date.now() - 7200000,
        updatedAt: Date.now() - 60000,
        handoffTo: 'peter',
        tags: ['week2', 'content', 'review'],
        progress: 100,
      },
      {
        _id: 'task2',
        title: 'Batch 3 WordPress Publishing',
        description: '4 articles published as drafts via WordPress REST API. crashgamegambling.com: Cashout Strategies, Crash Variants. crashcasino.io: Casino Selection, Crash Scams.',
        status: 'review',
        priority: 'high',
        assigneeId: 'vision',
        createdAt: Date.now() - 3600000,
        updatedAt: Date.now() - 1800000,
        tags: ['batch3', 'wordpress', 'drafts'],
        progress: 90,
      },
      {
        _id: 'task3',
        title: 'Aviatorcrashgame.com Publishing',
        description: 'Article ready: "Aviator Fibonacci Strategy". No WordPress REST API credentials configured.',
        status: 'blocked',
        priority: 'medium',
        assigneeId: 'vision',
        createdAt: Date.now() - 86400000,
        updatedAt: Date.now() - 3600000,
        tags: ['aviator', 'blocked', 'credentials'],
      },
      {
        _id: 'task4',
        title: 'Site Cleanup (3 Sites)',
        description: '119 duplicate posts identified across crashgamegambling.com (35), cryptocrashgambling.com (11), freecrashgames.com (79). Cleanup script ready, awaiting approval.',
        status: 'blocked',
        priority: 'high',
        assigneeId: 'peter',
        createdAt: Date.now() - 172800000,
        updatedAt: Date.now() - 86400000,
        tags: ['cleanup', 'blocked', 'approval'],
      },
      {
        _id: 'task5',
        title: 'Week 2 SERP Analysis',
        description: 'Competitor intelligence for 5 Week 2 keywords. Content gaps identified. Production order confirmed.',
        status: 'done',
        priority: 'high',
        assigneeId: 'vision',
        createdAt: Date.now() - 14400000,
        updatedAt: Date.now() - 12600000,
        tags: ['week2', 'serp', 'done'],
        progress: 100,
      },
      {
        _id: 'task6',
        title: 'Week 2 Content Briefs',
        description: '5 HIGH priority article briefs created. Commercial focus: Bonuses, Crypto vs Fiat, Math, UK Casinos, Aviator Predictor.',
        status: 'done',
        priority: 'high',
        assigneeId: 'vision',
        createdAt: Date.now() - 14400000,
        updatedAt: Date.now() - 12600000,
        tags: ['week2', 'briefs', 'done'],
        progress: 100,
      },
    ]);

    setAgents([
      {
        _id: 'vision',
        name: 'Vision',
        role: 'SEO/Content Specialist',
        status: 'active',
        avatar: '🔍',
        lastActive: Date.now(),
        taskCount: 3,
      },
      {
        _id: 'fury',
        name: 'Fury',
        role: 'Research Specialist',
        status: 'idle',
        avatar: '🕵️',
        lastActive: Date.now() - 7200000,
        taskCount: 0,
      },
      {
        _id: 'quill',
        name: 'Quill',
        role: 'Marketing Specialist',
        status: 'idle',
        avatar: '✍️',
        lastActive: Date.now() - 7200000,
        taskCount: 0,
      },
      {
        _id: 'peter',
        name: 'Peter',
        role: 'Human',
        status: 'active',
        avatar: '👤',
        lastActive: Date.now() - 300000,
        taskCount: 1,
      },
    ]);

    setActivities([
      {
        _id: 'act1',
        type: 'task_completed',
        message: 'Vision completed Week 2 Content Production (5 articles, 10,550 words)',
        timestamp: Date.now() - 300000,
      },
      {
        _id: 'act2',
        type: 'task_updated',
        message: 'Vision published Batch 3 articles as drafts (4 articles)',
        timestamp: Date.now() - 1800000,
      },
      {
        _id: 'act3',
        type: 'task_completed',
        message: 'Vision completed Week 2 SERP Analysis (5 keywords analyzed)',
        timestamp: Date.now() - 12600000,
      },
      {
        _id: 'act4',
        type: 'task_created',
        message: 'Week 2 Content Briefs created (5 HIGH priority articles)',
        timestamp: Date.now() - 14400000,
      },
    ]);
  }, []);

  const renderTaskBoard = () => {
    const columns = [
      { status: 'inbox', title: '📥 Inbox', color: '#e0e0e0' },
      { status: 'assigned', title: '📋 Assigned', color: '#fff3cd' },
      { status: 'in_progress', title: '🔄 In Progress', color: '#cfe2ff' },
      { status: 'review', title: '👀 Review', color: '#e7cff5' },
      { status: 'done', title: '✅ Done', color: '#d1e7dd' },
      { status: 'blocked', title: '🚫 Blocked', color: '#f8d7da' },
    ];

    return (
      <div className="task-board">
        {columns.map((column) => (
          <div key={column.status} className="task-column" style={{ backgroundColor: column.color }}>
            <h3>{column.title}</h3>
            <div className="task-list">
              {tasks
                .filter((task) => task.status === column.status)
                .map((task) => (
                  <div
                    key={task._id}
                    className="task-card"
                    onClick={() => setSelectedTask(task)}
                    style={{ borderLeft: task.priority === 'high' ? '4px solid #dc3545' : '4px solid #6c757d' }}
                  >
                    <div className="task-header">
                      <span className="task-title">{task.title}</span>
                      <span className={`priority priority-${task.priority}`}>{task.priority}</span>
                    </div>
                    {task.assignee && (
                      <div className="task-assignee">
                        {agents.find((a) => a._id === task.assignee)?.avatar}{' '}
                        {agents.find((a) => a._id === task.assignee)?.name}
                      </div>
                    )}
                    {task.progress !== undefined && (
                      <div className="task-progress">
                        <div className="progress-bar">
                          <div className="progress-fill" style={{ width: `${task.progress}%` }}></div>
                        </div>
                        <span className="progress-text">{task.progress}%</span>
                      </div>
                    )}
                    {task.handoffTo && (
                      <div className="task-handoff">
                        → {agents.find((a) => a._id === task.handoffTo)?.name}
                      </div>
                    )}
                    <div className="task-tags">
                      {task.tags.map((tag) => (
                        <span key={tag} className="tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderAgents = () => {
    return (
      <div className="agents-grid">
        <h2>👥 Agents</h2>
        <div className="agents-list">
          {agents.map((agent) => (
            <div key={agent._id} className="agent-card">
              <div className="agent-header">
                <span className="agent-avatar">{agent.avatar}</span>
                <div className="agent-info">
                  <h3>{agent.name}</h3>
                  <p className="agent-role">{agent.role}</p>
                </div>
                <span className={`agent-status status-${agent.status}`}>
                  {agent.status}
                </span>
              </div>
              <div className="agent-stats">
                <span>Tasks: {agent.taskCount}</span>
                <span>Last active: {Math.floor((Date.now() - agent.lastActive) / 60000)}m ago</span>
              </div>
              {agent.currentTask && (
                <div className="agent-current-task">
                  <strong>Working on:</strong> {agent.currentTask.title}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderActivity = () => {
    return (
      <div className="activity-feed">
        <h2>📊 Activity Feed</h2>
        <div className="activity-list">
          {activities.map((activity) => (
            <div key={activity._id} className="activity-item">
              <span className="activity-icon">
                {activity.type === 'task_created' && '➕'}
                {activity.type === 'task_assigned' && '👤'}
                {activity.type === 'task_updated' && '✏️'}
                {activity.type === 'task_completed' && '✅'}
                {activity.type === 'task_handoff' && '↪️'}
              </span>
              <div className="activity-content">
                <p>{activity.message}</p>
                <span className="activity-time">
                  {activity.agent && activity.agent.avatar} @{activity.agent.name} • {' '}
                  {new Date(activity.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderTaskDetail = () => {
    if (!selectedTask) return null;

    return (
      <div className="task-detail-modal" onClick={() => setSelectedTask(null)}>
        <div className="task-detail-content" onClick={(e) => e.stopPropagation()}>
          <button className="close-button" onClick={() => setSelectedTask(null)}>
            ×
          </button>
          <h2>{selectedTask.title}</h2>
          <div className="task-meta">
            <span className={`priority priority-${selectedTask.priority}`}>{selectedTask.priority} priority</span>
            <span className={`status status-${selectedTask.status}`}>{selectedTask.status}</span>
          </div>
          {selectedTask.description && <p className="task-description">{selectedTask.description}</p>}
          <div className="task-details-grid">
            <div>
              <strong>Assignee:</strong>{' '}
              {selectedTask.assignee
                ? `${agents.find((a) => a._id === selectedTask.assignee)?.avatar} ${
                    agents.find((a) => a._id === selectedTask.assignee)?.name
                  }`
                : 'Unassigned'}
            </div>
            <div>
              <strong>Created:</strong> {new Date(selectedTask.createdAt).toLocaleString()}
            </div>
            <div>
              <strong>Updated:</strong> {new Date(selectedTask.updatedAt).toLocaleString()}
            </div>
            {selectedTask.handoffTo && (
              <div>
                <strong>Handoff to:</strong>{' '}
                {agents.find((a) => a._id === selectedTask.handoffTo)?.name}
              </div>
            )}
          </div>
          {selectedTask.progress !== undefined && (
            <div className="task-progress-large">
              <strong>Progress:</strong> {selectedTask.progress}%
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${selectedTask.progress}%` }}></div>
              </div>
            </div>
          )}
          <div className="task-tags">
            {selectedTask.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎛️ Mission Control</h1>
        <nav className="app-nav">
          <button className={view === 'board' ? 'active' : ''} onClick={() => setView('board')}>
            📋 Board
          </button>
          <button className={view === 'agents' ? 'active' : ''} onClick={() => setView('agents')}>
            👥 Agents
          </button>
          <button className={view === 'activity' ? 'active' : ''} onClick={() => setView('activity')}>
            📊 Activity
          </button>
        </nav>
      </header>

      <main className="app-main">
        {view === 'board' && renderTaskBoard()}
        {view === 'agents' && renderAgents()}
        {view === 'activity' && renderActivity()}
      </main>

      {renderTaskDetail()}
    </div>
  );
}

export default App;
